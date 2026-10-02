import inspect

import pytest

import meso_crct as m


def public(name: str):
    assert hasattr(m, name), f"missing public next-core interface: {name}"
    return getattr(m, name)


def evidence():
    return m.EvidenceRef(
        producer_id="provider:effort",
        producer_revision="rev-1",
        subject_id="target:job",
        source_id="estimate:1",
        currentness=m.EvidenceCurrentness.CURRENT,
    )


def receipt_for(state):
    before = m.CircuitState()
    claim = m.Provenance(
        source_kind=m.SourceKind.ENVIRONMENT,
        source_id="observation:next-core-outcome",
        source_revision="v1",
    )
    verified = m.ProvenanceVerifier(
        [claim],
        verifier_id="next-core-outcome-verifier",
    ).verify(claim)
    _, event = m.EventSequencer("next-core-outcome-stream").issue()
    return m.evaluate_transition(
        before=before,
        after=state,
        provenance=verified,
        event=event,
    )


def policy():
    return m.PlasticityPolicy(
        maximum_absolute_delta=0.1,
        minimum_salience_gate=0.0,
    )


def learning_state(prediction_error: float):
    return m.CircuitState(
        salience=m.SalienceState(semantic_relevance=1.0),
        learning=m.LearningState(prediction_error=prediction_error),
    )


def test_effort_keeps_required_cost_and_willingness_separate():
    EffortAssessment = public("EffortAssessment")

    abundant = EffortAssessment(
        target_id="target:job",
        evidence=evidence(),
        required_effort=0.7,
        effort_cost=0.2,
        willingness_to_exert=0.9,
    )
    scarce = EffortAssessment(
        target_id="target:job",
        evidence=evidence(),
        required_effort=0.7,
        effort_cost=0.9,
        willingness_to_exert=0.6,
    )

    assert abundant.required_effort == scarce.required_effort == 0.7
    assert abundant.effort_cost != scarce.effort_cost
    assert abundant.willingness_to_exert != scarce.willingness_to_exert


def test_effort_allows_vigor_to_be_absent():
    EffortAssessment = public("EffortAssessment")
    assessment = EffortAssessment(
        target_id="target:job",
        evidence=evidence(),
        required_effort=0.5,
        effort_cost=0.5,
        willingness_to_exert=0.8,
    )
    assert assessment.vigor_proposal is None


def test_effort_unit_fields_reject_out_of_range_values():
    EffortAssessment = public("EffortAssessment")
    with pytest.raises(ValueError):
        EffortAssessment(
            target_id="target:job",
            evidence=evidence(),
            required_effort=1.1,
            effort_cost=0.2,
            willingness_to_exert=0.9,
        )


def test_propose_plasticity_accepts_typed_outcome_class():
    OutcomeClass = public("OutcomeClass")
    assert "outcome_class" in inspect.signature(m.propose_plasticity).parameters

    state = learning_state(-0.5)
    omission = m.propose_plasticity(
        state=state,
        association_id="cue->outcome",
        receipt=receipt_for(state),
        policy=policy(),
        outcome_class=OutcomeClass.OMISSION,
    )
    aversive = m.propose_plasticity(
        state=state,
        association_id="cue->outcome",
        receipt=receipt_for(state),
        policy=policy(),
        outcome_class=OutcomeClass.AVERSIVE,
    )

    assert omission.teaching_signal == aversive.teaching_signal == -0.5
    assert omission.outcome_class is OutcomeClass.OMISSION
    assert aversive.outcome_class is OutcomeClass.AVERSIVE


def test_legacy_plasticity_defaults_outcome_class_to_other():
    OutcomeClass = public("OutcomeClass")
    state = learning_state(0.5)
    candidate = m.propose_plasticity(
        state=state,
        association_id="cue->outcome",
        receipt=receipt_for(state),
        policy=policy(),
    )
    assert hasattr(candidate, "outcome_class")
    assert candidate.outcome_class is OutcomeClass.OTHER
