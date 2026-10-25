"""A measured need update is not a self-certified drive or goal completion."""

from datetime import datetime, timedelta, timezone
import math

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
from meso_crct.need_observation import (
    AdmissionClock,
    NeedObservation,
    NeedObservationConflict,
    NeedObservationFuture,
    NeedObservationLedger,
    NeedObservationRecord,
    NeedObservationStale,
    NeedObservationVerifier,
    ObservationNotAdmitted,
    admit_need_observation,
)
from meso_crct.provenance import Provenance, SourceKind


WHEN = datetime(2026, 10, 25, 12, 0, tzinfo=timezone.utc)
CLOCK = AdmissionClock(trusted_as_of=WHEN)


def observed(
    *,
    event_id="environment:42",
    need_id="rest",
    measured_level=0.5,
    observed_at=WHEN,
    source_kind=SourceKind.ENVIRONMENT,
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
        evidence_ref="sensor-sample:42",
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
    with pytest.raises(ValueError, match="external"):
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
    sample = observed(observed_at=datetime(9999, 1, 1, tzinfo=timezone.utc))
    admitted = verifier(sample).admit(sample)
    before = initial()
    with pytest.raises(TypeError, match="clock"):
        admit_need_observation(before, admitted)
    with pytest.raises(NeedObservationFuture, match="future"):
        admit_need_observation(before, admitted, clock=CLOCK)
    assert before.records == ()


def test_valid_new_sample_remains_admissible_after_blocked_future_poison():
    poisoned = observed(observed_at=datetime(9999, 1, 1, tzinfo=timezone.utc))
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

