import inspect

import pytest

import meso_crct as m


def public(name: str):
    assert hasattr(m, name), f"missing public obligation-admission interface: {name}"
    return getattr(m, name)


def evidence(*, producer_id="planner:goals", producer_revision="v1", currentness=None, subject_id="goal:g"):
    if currentness is None:
        currentness = m.EvidenceCurrentness.CURRENT
    return m.EvidenceRef(
        producer_id=producer_id,
        producer_revision=producer_revision,
        subject_id=subject_id,
        source_id="goal-obligation:1",
        currentness=currentness,
    )


def claim(*, producer_id="planner:goals", producer_revision="v1", currentness=None, subject_id="goal:g"):
    GoalObligationClaim = public("GoalObligationClaim")
    return GoalObligationClaim(
        goal_id="goal:g",
        minimum_nonprotective_share=0.4,
        evidence=evidence(
            producer_id=producer_id,
            producer_revision=producer_revision,
            currentness=currentness,
            subject_id=subject_id,
        ),
    )


def policy():
    GoalObligationProducerSpec = public("GoalObligationProducerSpec")
    GoalObligationAdmissionPolicy = public("GoalObligationAdmissionPolicy")
    return GoalObligationAdmissionPolicy(
        policy_id="host:goal-obligations",
        policy_revision="r1",
        producers=(
            GoalObligationProducerSpec(
                producer_id="planner:goals",
                producer_revision="v1",
            ),
        ),
    )


def test_current_claim_from_admitted_producer_converts_to_goal_obligation():
    admit = public("admit_goal_obligation")
    admitted = admit(claim(), policy())

    assert isinstance(admitted, m.GoalObligation)
    assert admitted.goal_id == "goal:g"
    assert admitted.minimum_nonprotective_share == 0.4


def test_spoofed_producer_is_rejected():
    Unadmitted = public("UnadmittedGoalObligationClaim")
    admit = public("admit_goal_obligation")

    with pytest.raises(Unadmitted):
        admit(claim(producer_id="planner:spoof"), policy())


def test_wrong_producer_revision_is_rejected():
    Unadmitted = public("UnadmittedGoalObligationClaim")
    admit = public("admit_goal_obligation")

    with pytest.raises(Unadmitted):
        admit(claim(producer_revision="v2"), policy())


@pytest.mark.parametrize(
    "currentness",
    [m.EvidenceCurrentness.STALE, m.EvidenceCurrentness.UNKNOWN],
)
def test_noncurrent_obligation_claim_is_rejected(currentness):
    Inadmissible = public("InadmissibleGoalObligationClaim")
    admit = public("admit_goal_obligation")

    with pytest.raises(Inadmissible):
        admit(claim(currentness=currentness), policy())


def test_evidence_subject_must_match_goal_id():
    GoalObligationClaim = public("GoalObligationClaim")

    with pytest.raises(ValueError):
        GoalObligationClaim(
            goal_id="goal:g",
            minimum_nonprotective_share=0.4,
            evidence=evidence(subject_id="goal:other"),
        )


def test_duplicate_producer_specs_fail_policy_construction():
    GoalObligationProducerSpec = public("GoalObligationProducerSpec")
    GoalObligationAdmissionPolicy = public("GoalObligationAdmissionPolicy")
    spec = GoalObligationProducerSpec(
        producer_id="planner:goals",
        producer_revision="v1",
    )

    with pytest.raises(ValueError):
        GoalObligationAdmissionPolicy(
            policy_id="host:goal-obligations",
            policy_revision="r1",
            producers=(spec, spec),
        )


def test_admission_requires_external_policy_argument():
    admit = public("admit_goal_obligation")
    parameters = inspect.signature(admit).parameters
    assert "policy" in parameters
    assert parameters["policy"].default is inspect.Parameter.empty


def test_legacy_direct_goal_obligation_is_unchanged_and_has_no_action_authority():
    obligation = m.GoalObligation("goal:g", 0.4)
    assert obligation.goal_id == "goal:g"
    assert obligation.minimum_nonprotective_share == 0.4
    assert not hasattr(obligation, "action_authority")
    assert not hasattr(obligation, "consent")


def test_admitted_obligation_retains_claim_and_policy_provenance():
    AdmittedGoalObligation = public("AdmittedGoalObligation")
    GoalObligationAdmissionPolicy = public("GoalObligationAdmissionPolicy")
    parameters = inspect.signature(GoalObligationAdmissionPolicy).parameters
    assert "policy_id" in parameters
    assert "policy_revision" in parameters

    trusted = GoalObligationAdmissionPolicy(
        policy_id="host:goal-obligations",
        policy_revision="r1",
        producers=(
            m.GoalObligationProducerSpec(
                producer_id="planner:goals",
                producer_revision="v1",
            ),
        ),
    )
    admitted = m.admit_goal_obligation(claim(), trusted)

    assert isinstance(admitted, m.GoalObligation)
    assert isinstance(admitted, AdmittedGoalObligation)
    assert admitted.evidence == claim().evidence
    assert admitted.admission_policy_id == "host:goal-obligations"
    assert admitted.admission_policy_revision == "r1"
