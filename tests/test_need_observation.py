"""A measured need update is not a self-certified drive or goal completion."""

import math
from datetime import UTC, datetime, timedelta, timezone

import pytest

from meso_crct import (
    CircuitState,
    DynamicsConfig,
    HomeostaticState,
    NeedAffordance,
    NeedAxis,
    TargetAppraisalInput,
    advance_without_input,
    build_target_appraisal,
)
from meso_crct import (
    NeedObservationCapacity as PublicNeedObservationCapacity,
)
from meso_crct.need_observation import (
    MAX_NEED_OBSERVATION_AXES,
    MAX_NEED_OBSERVATION_CLAIMS,
    MAX_NEED_OBSERVATION_FIELD_CHARS,
    MAX_NEED_OBSERVATION_RECORDS,
    AdmissionClock,
    NeedObservation,
    NeedObservationCapacity,
    NeedObservationConflict,
    NeedObservationExpired,
    NeedObservationFuture,
    NeedObservationLedger,
    NeedObservationRecord,
    NeedObservationStale,
    NeedObservationVerifier,
    ObservationNotAdmitted,
    admit_need_observation,
)
from meso_crct.provenance import Provenance, SourceKind

WHEN = datetime(2026, 10, 25, 12, 0, tzinfo=UTC)
CLOCK = AdmissionClock(trusted_as_of=WHEN)


def observed(
    *,
    event_id="environment:42",
    need_id="rest",
    measured_level=0.5,
    observed_at=WHEN,
    source_kind=SourceKind.ENVIRONMENT,
    evidence_ref="sensor-sample:42",
):
    return NeedObservation(
        event_id=event_id,
        need_id=need_id,
        measured_level=measured_level,
        observed_at=observed_at,
        provenance=Provenance(
            source_kind=source_kind,
            source_id="sensor:rest",
            source_revision="v1",
        ),
        evidence_ref=evidence_ref,
    )


def initial():
    return NeedObservationLedger(
        homeostasis=HomeostaticState((
            NeedAxis("rest", setpoint=0.9, current_level=0.1),
            NeedAxis("safety", setpoint=0.8, current_level=0.3),
        ))
    )


def verifier(*accepted):
    return NeedObservationVerifier(accepted, verifier_id="operator-admission-v1")


def test_no_observation_never_forges_need_recovery_or_satisfaction():
    ledger = initial()
    assert ledger.homeostasis.axis("rest").deficit == pytest.approx(0.8)
    assert ledger.records == ()
    assert ledger.effect_authorized is False


def test_capacity_error_is_exported_through_public_package_api():
    assert PublicNeedObservationCapacity is NeedObservationCapacity


def test_explicit_exact_claim_admission_updates_only_one_need():
    ledger = initial()
    sample = observed()
    admitted = verifier(sample).admit(sample)
    updated = admit_need_observation(ledger, admitted, clock=CLOCK)
    assert updated.homeostasis.axis("rest").current_level == 0.5
    assert updated.homeostasis.axis("rest").deficit == pytest.approx(0.4)
    assert updated.homeostasis.axis("safety") == ledger.homeostasis.axis("safety")
    assert ledger.homeostasis.axis("rest").current_level == 0.1
    assert len(updated.records) == 1
    assert updated.records[0].verifier_id == "operator-admission-v1"
    assert updated.effect_authorized is False


def test_unadmitted_or_modified_sample_cannot_update_need():
    ledger = initial()
    sample = observed()
    with pytest.raises(TypeError):
        admit_need_observation(ledger, sample, clock=CLOCK)
    with pytest.raises(ObservationNotAdmitted):
        verifier(sample).admit(observed(measured_level=0.9))


def test_model_self_asserted_internal_state_cannot_be_an_observation():
    with pytest.raises(ValueError, match="external"):
        observed(source_kind=SourceKind.INTERNAL_STATE)
    with pytest.raises(ValueError, match="external"):
        observed(source_kind=SourceKind.DIRECT_REGISTER_WRITE)
    # A raw string that compares equal to a StrEnum is not a typed source claim.
    with pytest.raises(ValueError, match="source_kind"):
        observed(source_kind="environment")


@pytest.mark.parametrize("bad", [math.nan, math.inf, -math.inf, -0.01, 1.01, True, False, "0.5", None])
def test_observed_level_is_finite_and_not_silently_clamped(bad):
    with pytest.raises(ValueError):
        observed(measured_level=bad)


def test_unaware_or_non_utc_timestamp_is_rejected():
    with pytest.raises(ValueError, match="UTC"):
        observed(observed_at=WHEN.replace(tzinfo=None))
    with pytest.raises(ValueError, match="UTC"):
        observed(observed_at=WHEN.astimezone(timezone(timedelta(hours=-4))))


def test_exact_event_replay_is_idempotent_and_conflict_is_rejected():
    base = initial()
    sample = observed()
    accepted = admit_need_observation(base, verifier(sample).admit(sample), clock=CLOCK)
    assert admit_need_observation(accepted, verifier(sample).admit(sample), clock=CLOCK) is accepted

    changed = observed(measured_level=0.7)
    with pytest.raises(NeedObservationConflict):
        admit_need_observation(accepted, verifier(changed).admit(changed), clock=CLOCK)


def test_stale_or_same_time_distinct_event_cannot_roll_back_need():
    latest = observed(event_id="environment:new", observed_at=WHEN)
    accepted = admit_need_observation(initial(), verifier(latest).admit(latest), clock=CLOCK)
    for timestamp in (WHEN, WHEN - timedelta(seconds=1)):
        old = observed(event_id=f"environment:stale-{timestamp.isoformat()}", observed_at=timestamp)
        with pytest.raises(NeedObservationStale):
            admit_need_observation(accepted, verifier(old).admit(old), clock=CLOCK)


def test_independent_need_axes_have_independent_observation_clocks():
    rest = observed()
    after_rest = admit_need_observation(initial(), verifier(rest).admit(rest), clock=CLOCK)
    safety = observed(event_id="environment:safe", need_id="safety", observed_at=WHEN)
    updated = admit_need_observation(after_rest, verifier(safety).admit(safety), clock=CLOCK)
    assert updated.homeostasis.axis("safety").current_level == 0.5
    assert len(updated.records) == 2


def test_reconstructed_ledger_rejects_state_record_disagreement():
    sample = observed()
    with pytest.raises(ValueError, match="latest admitted"):
        NeedObservationLedger(
            homeostasis=initial().homeostasis,
            records=(NeedObservationRecord(sample, "caller-v1"),),
        )


def test_unknown_need_and_unaccepted_source_cannot_create_need_axes():
    unknown = observed(need_id="imagined_need")
    with pytest.raises(ValueError, match="unknown need"):
        admit_need_observation(initial(), verifier(unknown).admit(unknown), clock=CLOCK)


def test_admitted_level_changes_appraisal_pressure_not_hedonic_welfare():
    original = initial()
    correction = observed()
    updated = admit_need_observation(original, verifier(correction).admit(correction), clock=CLOCK)

    def appraise(ledger):
        return build_target_appraisal(TargetAppraisalInput(
            target_id="rest_target",
            homeostasis=ledger.homeostasis,
            affordances=(NeedAffordance("rest", 1.0),),
        )).state

    before = appraise(original)
    after = appraise(updated)
    assert before.salience.incentive_salience == pytest.approx(0.8)
    assert after.salience.incentive_salience == pytest.approx(0.4)
    assert before.reward.pleasure == after.reward.pleasure == 0.0


def test_admission_requires_explicit_trusted_clock_and_rejects_9999_poisoning():
    sample = observed(observed_at=datetime(9999, 1, 1, tzinfo=UTC))
    admitted = verifier(sample).admit(sample)
    before = initial()
    with pytest.raises(TypeError, match="clock"):
        admit_need_observation(before, admitted)
    with pytest.raises(NeedObservationFuture, match="future"):
        admit_need_observation(before, admitted, clock=CLOCK)
    assert before.records == ()


def test_valid_new_sample_remains_admissible_after_blocked_future_poison():
    poisoned = observed(observed_at=datetime(9999, 1, 1, tzinfo=UTC))
    before = initial()
    with pytest.raises(NeedObservationFuture):
        admit_need_observation(before, verifier(poisoned).admit(poisoned), clock=CLOCK)
    valid = observed(event_id="environment:valid", measured_level=0.7)
    result = admit_need_observation(before, verifier(valid).admit(valid), clock=CLOCK)
    assert result.homeostasis.axis("rest").current_level == 0.7


def test_clock_policy_bounds_future_skew_and_rejects_untrusted_types():
    for as_of in (WHEN.replace(tzinfo=None), "2026-10-25T12:00:00Z", WHEN.astimezone(timezone(timedelta(hours=-4)))):
        with pytest.raises(ValueError):
            AdmissionClock(trusted_as_of=as_of)
    for skew in (True, "30", math.nan, math.inf, -1, 301, 10**10000):
        with pytest.raises(ValueError, match="skew"):
            AdmissionClock(trusted_as_of=WHEN, maximum_future_skew_seconds=skew)
    assert AdmissionClock(trusted_as_of=WHEN, maximum_future_skew_seconds=300).maximum_future_skew_seconds == 300.0


def test_small_future_skew_is_explicitly_bounded_and_replay_safe():
    just_after = observed(observed_at=WHEN + timedelta(seconds=30))
    with pytest.raises(NeedObservationFuture):
        admit_need_observation(initial(), verifier(just_after).admit(just_after), clock=CLOCK)
    policy = AdmissionClock(trusted_as_of=WHEN, maximum_future_skew_seconds=30)
    admitted = admit_need_observation(initial(), verifier(just_after).admit(just_after), clock=policy)
    assert admitted.homeostasis.axis("rest").current_level == 0.5
    with pytest.raises(TypeError, match="clock"):
        admit_need_observation(initial(), verifier(just_after).admit(just_after), clock=None)
    assert admit_need_observation(admitted, verifier(just_after).admit(just_after), clock=policy) is admitted


def test_optional_observation_age_ceiling_rejects_expired_first_measurement():
    ancient = observed(observed_at=WHEN - timedelta(seconds=11))
    accepted = verifier(ancient).admit(ancient)
    before = initial()

    # The original caller contract remains valid without an opt-in expiry.
    assert admit_need_observation(before, accepted, clock=CLOCK).homeostasis.axis("rest").current_level == 0.5

    policy = AdmissionClock(trusted_as_of=WHEN, maximum_observation_age_seconds=10)
    with pytest.raises(NeedObservationExpired, match="expired"):
        admit_need_observation(before, accepted, clock=policy)
    assert before.homeostasis.axis("rest").current_level == 0.1
    assert before.records == ()

    edge = observed(event_id="environment:boundary", observed_at=WHEN - timedelta(seconds=10))
    updated = admit_need_observation(before, verifier(edge).admit(edge), clock=policy)
    assert updated.homeostasis.axis("rest").current_level == 0.5
    # Exactly admitted history remains replay-idempotent after the window expires.
    much_later = AdmissionClock(trusted_as_of=WHEN + timedelta(days=3), maximum_observation_age_seconds=10)
    assert admit_need_observation(updated, verifier(edge).admit(edge), clock=much_later) is updated


def test_opt_in_observation_age_policy_is_typed_bounded_and_independent_of_future_skew():
    for bad in (True, False, "10", -1, math.nan, math.inf, -math.inf, 10**10000):
        with pytest.raises(ValueError, match="age"):
            AdmissionClock(trusted_as_of=WHEN, maximum_observation_age_seconds=bad)
    assert AdmissionClock(trusted_as_of=WHEN).maximum_observation_age_seconds is None

    # An explicitly permitted future sample isn't accidentally treated as old.
    future = observed(observed_at=WHEN + timedelta(seconds=4))
    policy = AdmissionClock(
        trusted_as_of=WHEN,
        maximum_future_skew_seconds=4,
        maximum_observation_age_seconds=0,
    )
    assert admit_need_observation(initial(), verifier(future).admit(future), clock=policy).records


def test_no_new_input_time_tick_does_not_mint_satisfaction():
    ledger = initial()
    circuit = CircuitState(homeostasis=ledger.homeostasis)
    config = DynamicsConfig(
        hedonic_half_life_seconds=10,
        salience_half_life_seconds=10,
        learning_half_life_seconds=10,
        satiation_half_life_seconds=10,
        recruitment_half_life_seconds=10,
    )
    after = advance_without_input(circuit, elapsed_seconds=1000, config=config)
    assert after.homeostasis == ledger.homeostasis
    assert after.homeostasis.axis("rest").deficit == pytest.approx(0.8)
    assert ledger.records == ()


def test_full_event_history_fails_closed_without_erasing_replay_provenance():
    ledger = initial()
    first = None
    for index in range(MAX_NEED_OBSERVATION_RECORDS):
        sample = observed(
            event_id=f"environment:bounded:{index}",
            observed_at=WHEN - timedelta(seconds=MAX_NEED_OBSERVATION_RECORDS - index),
        )
        admitted = verifier(sample).admit(sample)
        first = first or admitted
        ledger = admit_need_observation(ledger, admitted, clock=CLOCK)

    assert len(ledger.records) == MAX_NEED_OBSERVATION_RECORDS
    assert admit_need_observation(ledger, first, clock=CLOCK) is ledger
    assert ledger.records[0].observation == first.observation

    # Evicting a historical event to make room would allow old IDs to be
    # reused and invalidate the evidence lineage. Full is an explicit STOP.
    additional = observed(event_id="environment:bounded:overflow", observed_at=WHEN)
    with pytest.raises(NeedObservationCapacity, match="capacity"):
        admit_need_observation(ledger, verifier(additional).admit(additional), clock=CLOCK)
    assert len(ledger.records) == MAX_NEED_OBSERVATION_RECORDS

    different_replay = observed(
        event_id=first.observation.event_id,
        measured_level=0.6,
        observed_at=first.observation.observed_at,
    )
    with pytest.raises(NeedObservationConflict):
        admit_need_observation(ledger, verifier(different_replay).admit(different_replay), clock=CLOCK)


@pytest.mark.parametrize("field", ["event_id", "need_id", "evidence_ref"])
def test_large_observation_identifiers_are_rejected_before_ledger_admission(field):
    with pytest.raises(NeedObservationCapacity, match=field):
        observed(**{field: "x" * (MAX_NEED_OBSERVATION_FIELD_CHARS + 1)})


@pytest.mark.parametrize("field", ["source_id", "source_revision"])
def test_large_provenance_claims_are_rejected_before_ledger_admission(field):
    with pytest.raises(NeedObservationCapacity, match=field):
        observed_source = Provenance(
            source_kind=SourceKind.ENVIRONMENT,
            source_id="sensor:rest" if field != "source_id" else "x" * (MAX_NEED_OBSERVATION_FIELD_CHARS + 1),
            source_revision="v1" if field != "source_revision" else "x" * (MAX_NEED_OBSERVATION_FIELD_CHARS + 1),
        )
        NeedObservation(
            event_id="environment:42", need_id="rest", measured_level=0.5,
            observed_at=WHEN, provenance=observed_source, evidence_ref="sensor:42",
        )


def test_verifier_rejects_unbounded_claim_generator_and_identifier():
    yielded = 0

    def never_ending():
        nonlocal yielded
        while True:
            yielded += 1
            yield observed(event_id=f"environment:{yielded}")

    with pytest.raises(NeedObservationCapacity, match="accepted"):
        NeedObservationVerifier(never_ending(), verifier_id="operator")
    assert yielded == MAX_NEED_OBSERVATION_CLAIMS + 1
    with pytest.raises(NeedObservationCapacity, match="verifier_id"):
        NeedObservationVerifier((), verifier_id="x" * (MAX_NEED_OBSERVATION_FIELD_CHARS + 1))


def test_resource_budget_exact_boundary_values_are_accepted():
    sample = observed(event_id="e" * MAX_NEED_OBSERVATION_FIELD_CHARS)
    admitted = verifier(sample).admit(sample)
    assert admit_need_observation(initial(), admitted, clock=CLOCK).records[0].observation == sample
    allowed = tuple(observed(event_id=f"distinct:{index}") for index in range(MAX_NEED_OBSERVATION_CLAIMS))
    assert verifier(*allowed).admit(allowed[-1]).observation == allowed[-1]
    axes = HomeostaticState(tuple(
        NeedAxis(f"need:{index}", setpoint=1.0, current_level=0.5)
        for index in range(MAX_NEED_OBSERVATION_AXES)
    ))
    assert len(NeedObservationLedger(homeostasis=axes).homeostasis.axes) == MAX_NEED_OBSERVATION_AXES


def test_ledger_rejects_outsize_reconstructed_history_and_axis_set():
    sample = observed()
    record = NeedObservationRecord(sample, "operator")
    with pytest.raises(NeedObservationCapacity, match="history"):
        NeedObservationLedger(
            homeostasis=initial().homeostasis,
            records=(record,) * (MAX_NEED_OBSERVATION_RECORDS + 1),
        )
    oversized = HomeostaticState(tuple(
        NeedAxis(f"need:{index}", setpoint=1.0, current_level=0.5)
        for index in range(MAX_NEED_OBSERVATION_AXES + 1)
    ))
    with pytest.raises(NeedObservationCapacity, match="axes"):
        NeedObservationLedger(homeostasis=oversized)
    large_axis_name = HomeostaticState((
        NeedAxis("n" * (MAX_NEED_OBSERVATION_FIELD_CHARS + 1), setpoint=1, current_level=0),
    ))
    with pytest.raises(NeedObservationCapacity, match="need_id"):
        NeedObservationLedger(homeostasis=large_axis_name)

