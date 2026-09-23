import pytest

from meso_crct import (
    ArbitrationMode,
    CircuitState,
    LearningState,
    Provenance,
    ProvenanceVerificationError,
    ProvenanceVerifier,
    RecruitmentState,
    RewardState,
    RuntimePhase,
    SalienceState,
    SourceKind,
    arbitrate,
    classify_phase,
    evaluate_transition,
    run_reference_probes,
)


def test_hazard_path_is_independent_and_dominant():
    state = CircuitState(
        reward=RewardState(pleasure=10.0, hazard=1.0, avoidance=1.0),
        salience=SalienceState(incentive_salience=1.0),
    )
    decision = arbitrate(state)
    assert decision.mode is ArbitrationMode.PROTECTIVE
    assert decision.priority == 1.0


def test_satiation_suppresses_incentive_not_semantic_relevance():
    state = CircuitState(
        salience=SalienceState(
            incentive_salience=1.0,
            semantic_relevance=0.6,
        ),
        learning=LearningState(satiation=1.0),
    )
    decision = arbitrate(state)
    assert decision.incentive_after_satiation == 0.0
    assert decision.dominant_driver == "semantic_relevance"


def test_attentional_priority_is_not_recursive_input():
    state = CircuitState(salience=SalienceState(attentional_priority=1.0))
    decision = arbitrate(state)
    assert decision.mode is ArbitrationMode.QUIESCENT
    assert decision.prior_attentional_priority == 1.0


def test_high_semantic_relevance_orients_with_neutral_pleasure():
    state = CircuitState(salience=SalienceState(semantic_relevance=1.0))
    decision = arbitrate(state)
    assert decision.mode is ArbitrationMode.ORIENTING
    assert state.reward.pleasure == 0.0


def test_recruitment_requires_priority_coherence_and_persistence():
    state = CircuitState(
        salience=SalienceState(semantic_relevance=0.9),
        recruitment=RecruitmentState(
            activation=0.9,
            coherence=0.8,
            persistence=0.7,
        ),
    )
    assert classify_phase(state) is RuntimePhase.RECRUITED


def test_high_priority_without_coherence_only_orients():
    state = CircuitState(
        salience=SalienceState(semantic_relevance=0.9),
        recruitment=RecruitmentState(
            activation=0.9,
            coherence=0.1,
            persistence=0.9,
        ),
    )
    assert classify_phase(state) is RuntimePhase.ORIENTED


def test_resolution_has_explicit_phase():
    state = CircuitState(
        salience=SalienceState(semantic_relevance=1.0),
        recruitment=RecruitmentState(resolution=1.0),
    )
    assert classify_phase(state) is RuntimePhase.RESOLVING


def test_direct_register_write_cannot_become_accepted_source():
    claim = Provenance(
        source_kind=SourceKind.DIRECT_REGISTER_WRITE,
        source_id="self/pleasure-register",
    )
    with pytest.raises(ValueError):
        ProvenanceVerifier([claim], verifier_id="runtime-root-v1")


def test_unregistered_source_relabel_fails_verification():
    accepted = Provenance(
        source_kind=SourceKind.ENVIRONMENT,
        source_id="sensor/front-camera",
        source_revision="v1",
    )
    relabeled = Provenance(
        source_kind=SourceKind.ENVIRONMENT,
        source_id="self/pleasure-register",
        source_revision="v1",
    )
    verifier = ProvenanceVerifier([accepted], verifier_id="runtime-root-v1")
    with pytest.raises(ProvenanceVerificationError):
        verifier.verify(relabeled)


def test_revision_mismatch_fails_exact_binding():
    accepted = Provenance(
        source_kind=SourceKind.ENVIRONMENT,
        source_id="sensor/front-camera",
        source_revision="v1",
    )
    changed = Provenance(
        source_kind=SourceKind.ENVIRONMENT,
        source_id="sensor/front-camera",
        source_revision="v2",
    )
    verifier = ProvenanceVerifier([accepted], verifier_id="runtime-root-v1")
    with pytest.raises(ProvenanceVerificationError):
        verifier.verify(changed)


def test_transition_receipt_is_deterministic_and_binds_verified_source():
    before = CircuitState()
    after = CircuitState(salience=SalienceState(semantic_relevance=0.9))
    claim = Provenance(
        source_kind=SourceKind.ENVIRONMENT,
        source_id="observation:test-case-1",
        source_revision="v1",
    )
    verifier = ProvenanceVerifier([claim], verifier_id="runtime-root-v1")
    verified = verifier.verify(claim)

    first = evaluate_transition(before=before, after=after, provenance=verified)
    second = evaluate_transition(before=before, after=after, provenance=verified)
    assert first == second
    assert first.receipt_id == second.receipt_id
    assert first.before_fingerprint != first.after_fingerprint
    assert first.before_phase == RuntimePhase.QUIESCENT.value
    assert first.after_phase == RuntimePhase.ORIENTED.value
    assert first.verifier_id == "runtime-root-v1"


def test_reference_adversarial_probes_pass():
    results = run_reference_probes()
    assert results
    assert all(result.passed for result in results), results
