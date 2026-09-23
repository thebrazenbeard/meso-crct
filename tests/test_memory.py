import pytest

from meso_crct import (
    AssociationMemory,
    AssociationNotFound,
    CircuitState,
    LearningState,
    MemoryVersionConflict,
    PlasticityPolicy,
    PlasticityReplayError,
    Provenance,
    ProvenanceVerifier,
    SalienceState,
    SourceKind,
    apply_candidate,
    evaluate_transition,
    propose_plasticity,
    revert_last,
)


def candidate_for(
    association_id="cue->outcome",
    *,
    prediction_error=1.0,
    salience=1.0,
    source_id="observation:memory-test-1",
):
    state = CircuitState(
        salience=SalienceState(semantic_relevance=salience),
        learning=LearningState(prediction_error=prediction_error),
    )
    claim = Provenance(
        source_kind=SourceKind.ENVIRONMENT,
        source_id=source_id,
        source_revision="v1",
    )
    verified = ProvenanceVerifier(
        [claim],
        verifier_id="memory-test-verifier",
    ).verify(claim)
    receipt = evaluate_transition(
        before=CircuitState(),
        after=state,
        provenance=verified,
    )
    return propose_plasticity(
        state=state,
        association_id=association_id,
        receipt=receipt,
        policy=PlasticityPolicy(
            maximum_absolute_delta=0.1,
            minimum_salience_gate=0.4,
        ),
    )


def test_apply_candidate_creates_first_version():
    memory = AssociationMemory()
    updated = apply_candidate(
        memory,
        candidate_for(),
        expected_version=0,
    )
    current = updated.current("cue->outcome")
    assert current is not None
    assert current.version == 1
    assert current.strength == pytest.approx(0.1)
    assert memory.current("cue->outcome") is None


def test_stale_writer_fails_version_check():
    memory = apply_candidate(
        AssociationMemory(),
        candidate_for(),
        expected_version=0,
    )
    with pytest.raises(MemoryVersionConflict):
        apply_candidate(
            memory,
            candidate_for(source_id="observation:memory-test-2"),
            expected_version=0,
        )


def test_same_transition_receipt_cannot_be_replayed():
    candidate = candidate_for()
    memory = apply_candidate(
        AssociationMemory(),
        candidate,
        expected_version=0,
    )
    with pytest.raises(PlasticityReplayError):
        apply_candidate(
            memory,
            candidate,
            expected_version=1,
        )


def test_second_distinct_candidate_appends_history():
    first = candidate_for(source_id="observation:memory-test-1")
    second = candidate_for(
        prediction_error=-0.5,
        source_id="observation:memory-test-2",
    )
    memory = apply_candidate(
        AssociationMemory(),
        first,
        expected_version=0,
    )
    memory = apply_candidate(
        memory,
        second,
        expected_version=1,
    )
    history = memory.history("cue->outcome")
    assert len(history) == 2
    assert history[-1].version == 2
    assert history[-1].strength == pytest.approx(0.05)


def test_revert_appends_new_revision_without_deleting_history():
    candidate = candidate_for()
    memory = apply_candidate(
        AssociationMemory(),
        candidate,
        expected_version=0,
    )
    reverted = revert_last(
        memory,
        "cue->outcome",
        expected_version=1,
    )
    history = reverted.history("cue->outcome")
    assert len(history) == 2
    assert history[0].operation == "apply"
    assert history[1].operation == "revert"
    assert history[1].version == 2
    assert history[1].strength == 0.0


def test_revert_missing_association_fails():
    with pytest.raises(AssociationNotFound):
        revert_last(
            AssociationMemory(),
            "missing",
            expected_version=0,
        )


def test_strength_remains_bounded_across_repeated_distinct_updates():
    memory = AssociationMemory()
    for index in range(20):
        candidate = candidate_for(
            source_id=f"observation:memory-test-{index}",
        )
        memory = apply_candidate(
            memory,
            candidate,
            expected_version=index,
        )
    assert memory.current_strength("cue->outcome") == 1.0


def test_revision_ids_are_deterministic_for_same_history():
    candidate = candidate_for()
    first = apply_candidate(
        AssociationMemory(),
        candidate,
        expected_version=0,
    )
    second = apply_candidate(
        AssociationMemory(),
        candidate,
        expected_version=0,
    )
    assert first.revisions[0].revision_id == second.revisions[0].revision_id
