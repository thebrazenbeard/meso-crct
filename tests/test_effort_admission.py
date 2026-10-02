import inspect

import pytest

import meso_crct as m


def public(name: str):
    assert hasattr(m, name), f"missing public effort-admission interface: {name}"
    return getattr(m, name)


def evidence(
    target_id="target:a",
    *,
    producer_id="planner:effort",
    producer_revision="v1",
    source_id="effort:1",
    currentness=None,
):
    if currentness is None:
        currentness = m.EvidenceCurrentness.CURRENT
    return m.EvidenceRef(
        producer_id=producer_id,
        producer_revision=producer_revision,
        subject_id=target_id,
        source_id=source_id,
        currentness=currentness,
    )


def assessment(
    target_id="target:a",
    *,
    producer_id="planner:effort",
    producer_revision="v1",
    source_id="effort:1",
    currentness=None,
    required_effort=0.6,
    effort_cost=0.4,
    willingness_to_exert=0.8,
    vigor_proposal=0.5,
):
    return m.EffortAssessment(
        target_id=target_id,
        evidence=evidence(
            target_id,
            producer_id=producer_id,
            producer_revision=producer_revision,
            source_id=source_id,
            currentness=currentness,
        ),
        required_effort=required_effort,
        effort_cost=effort_cost,
        willingness_to_exert=willingness_to_exert,
        vigor_proposal=vigor_proposal,
    )


def policy(*, policy_revision="r1", producers=None):
    EffortProducerSpec = public("EffortProducerSpec")
    EffortAdmissionPolicy = public("EffortAdmissionPolicy")
    if producers is None:
        producers = (
            EffortProducerSpec(
                producer_id="planner:effort",
                producer_revision="v1",
            ),
        )
    return EffortAdmissionPolicy(
        policy_id="host:effort",
        policy_revision=policy_revision,
        producers=tuple(producers),
    )


def admit(item, policy_obj=None):
    fn = public("admit_effort_assessment")
    if policy_obj is None:
        policy_obj = policy()
    return fn(item, policy_obj)


def test_effort_assessment_binds_evidence_subject_to_target():
    with pytest.raises(ValueError):
        m.EffortAssessment(
            target_id="target:a",
            evidence=evidence("target:b"),
            required_effort=0.6,
            effort_cost=0.4,
            willingness_to_exert=0.8,
        )


def test_current_trusted_effort_assessment_is_admitted():
    Admitted = public("AdmittedEffortAssessment")
    original = assessment()
    admitted = admit(original)

    assert isinstance(admitted, m.EffortAssessment)
    assert isinstance(admitted, Admitted)
    assert admitted.target_id == original.target_id
    assert admitted.required_effort == original.required_effort
    assert admitted.effort_cost == original.effort_cost
    assert admitted.willingness_to_exert == original.willingness_to_exert
    assert admitted.vigor_proposal == original.vigor_proposal
    assert admitted.evidence == original.evidence


@pytest.mark.parametrize(
    "currentness",
    [m.EvidenceCurrentness.STALE, m.EvidenceCurrentness.UNKNOWN],
)
def test_noncurrent_effort_assessment_is_not_admitted(currentness):
    Inadmissible = public("InadmissibleEffortAssessment")
    with pytest.raises(Inadmissible):
        admit(assessment(currentness=currentness))


def test_spoofed_effort_producer_is_rejected():
    Unadmitted = public("UnadmittedEffortAssessment")
    with pytest.raises(Unadmitted):
        admit(assessment(producer_id="planner:spoof"))


def test_wrong_effort_producer_revision_is_rejected():
    Unadmitted = public("UnadmittedEffortAssessment")
    with pytest.raises(Unadmitted):
        admit(assessment(producer_revision="v2"))


def test_duplicate_effort_producer_specs_are_rejected():
    EffortProducerSpec = public("EffortProducerSpec")
    EffortAdmissionPolicy = public("EffortAdmissionPolicy")
    spec = EffortProducerSpec(
        producer_id="planner:effort",
        producer_revision="v1",
    )
    with pytest.raises(ValueError):
        EffortAdmissionPolicy(
            policy_id="host:effort",
            policy_revision="r1",
            producers=(spec, spec),
        )


def test_effort_admission_requires_external_policy_argument():
    fn = public("admit_effort_assessment")
    parameters = inspect.signature(fn).parameters
    assert "policy" in parameters
    assert parameters["policy"].default is inspect.Parameter.empty


def test_admitted_effort_retains_policy_identity_and_digest():
    admitted = admit(assessment())
    assert admitted.admission_policy_id == "host:effort"
    assert admitted.admission_policy_revision == "r1"
    assert admitted.admission_input_digest


def test_admission_digest_changes_with_assessment_or_policy_revision():
    base = admit(assessment())
    changed_assessment = admit(assessment(effort_cost=0.7))
    changed_policy = admit(
        assessment(),
        policy(policy_revision="r2"),
    )

    assert base.admission_input_digest != changed_assessment.admission_input_digest
    assert base.admission_input_digest != changed_policy.admission_input_digest


def test_admission_digest_is_stable_under_producer_spec_order():
    EffortProducerSpec = public("EffortProducerSpec")
    p1 = EffortProducerSpec(
        producer_id="planner:effort",
        producer_revision="v1",
    )
    p2 = EffortProducerSpec(
        producer_id="planner:backup",
        producer_revision="v2",
    )
    first = admit(
        assessment(),
        policy(producers=(p1, p2)),
    )
    second = admit(
        assessment(),
        policy(producers=(p2, p1)),
    )
    assert first.admission_input_digest == second.admission_input_digest


def test_admitted_effort_does_not_create_execution_authority():
    admitted = admit(assessment())
    for name in ("action_authority", "consent", "can_execute", "effect_authorized"):
        assert not hasattr(admitted, name)


def test_legacy_direct_effort_assessment_remains_semantically_separate():
    raw = assessment(vigor_proposal=None)
    assert raw.required_effort == 0.6
    assert raw.effort_cost == 0.4
    assert raw.willingness_to_exert == 0.8
    assert raw.vigor_proposal is None
    assert not hasattr(raw, "admission_policy_id")
