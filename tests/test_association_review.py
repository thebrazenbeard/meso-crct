import pytest

from meso_crct import (
    AssociationMemory,
    AssociationQuarantinedError,
    AssociationReviewRecord,
    AssociationReviewStaleError,
    CircuitState,
    EventSequencer,
    LearningState,
    PlasticityPolicy,
    Provenance,
    ProvenanceVerifier,
    ReviewDisposition,
    ReviewNoOpError,
    SalienceState,
    SourceKind,
    apply_candidate,
    evaluate_transition,
    propose_plasticity,
    quarantine_association,
    recall_association,
    release_association,
)


def verified(source_id: str):
    claim = Provenance(
        source_kind=SourceKind.ENVIRONMENT,
        source_id=source_id,
        source_revision="v1",
    )
    return ProvenanceVerifier(
        [claim],
        verifier_id="review-test-verifier",
    ).verify(claim)


def learned_memory(*, prediction_error=0.8, stream="learn-1"):
    state = CircuitState(
        salience=SalienceState(semantic_relevance=1.0),
        learning=LearningState(prediction_error=prediction_error),
    )
    _, event = EventSequencer(stream).issue()
    receipt = evaluate_transition(
        before=CircuitState(),
        after=state,
        provenance=verified(stream),
        event=event,
    )
    candidate = propose_plasticity(
        state=state,
        association_id="cue->outcome",
        receipt=receipt,
        policy=PlasticityPolicy(
            maximum_absolute_delta=1.0,
            minimum_salience_gate=0.0,
        ),
    )
    return apply_candidate(
        AssociationMemory(),
        candidate,
        expected_version=0,
    )


def add_learning(memory, *, prediction_error=0.2, stream="learn-2"):
    state = CircuitState(
        salience=SalienceState(semantic_relevance=1.0),
        learning=LearningState(prediction_error=prediction_error),
    )
    _, event = EventSequencer(stream).issue()
    receipt = evaluate_transition(
        before=CircuitState(),
        after=state,
        provenance=verified(stream),
        event=event,
    )
    candidate = propose_plasticity(
        state=state,
        association_id="cue->outcome",
        receipt=receipt,
        policy=PlasticityPolicy(
            maximum_absolute_delta=1.0,
            minimum_salience_gate=0.0,
        ),
    )
    return apply_candidate(
        memory,
        candidate,
        expected_version=memory.current_version("cue->outcome"),
    )


def cue_receipt(stream="cue"):
    state = CircuitState(
        salience=SalienceState(perceptual_salience=0.8),
    )
    _, event = EventSequencer(stream).issue()
    return evaluate_transition(
        before=CircuitState(),
        after=state,
        provenance=verified(stream),
        event=event,
    )


def test_review_record_cannot_be_constructed_directly():
    with pytest.raises(TypeError):
        AssociationReviewRecord(
            association_id="cue->outcome",
            review_version=1,
            memory_revision_id="fake",
            disposition=ReviewDisposition.QUARANTINED,
            reason="fake",
            parent_review_id=None,
            review_id="fake",
        )


def test_quarantine_preserves_learning_but_blocks_recall():
    memory = learned_memory()
    revision = memory.current("cue->outcome")
    assert revision is not None

    quarantined = quarantine_association(
        memory,
        "cue->outcome",
        reason="suspected negative transfer",
    )

    assert quarantined.revisions == memory.revisions
    assert quarantined.current_strength("cue->outcome") == pytest.approx(0.8)
    assert quarantined.current("cue->outcome").revision_id == revision.revision_id

    with pytest.raises(AssociationQuarantinedError):
        recall_association(
            memory=quarantined,
            association_id="cue->outcome",
            cue_match=1.0,
            cue_receipt=cue_receipt(),
        )


def test_release_restores_same_revision_recall_without_rewriting_memory():
    memory = learned_memory()
    quarantined = quarantine_association(
        memory,
        "cue->outcome",
        reason="hold for review",
    )
    released = release_association(
        quarantined,
        "cue->outcome",
        reason="review cleared current revision",
    )

    influence = recall_association(
        memory=released,
        association_id="cue->outcome",
        cue_match=1.0,
        cue_receipt=cue_receipt(),
    )

    assert released.revisions == memory.revisions
    assert len(released.reviews.history("cue->outcome")) == 2
    assert influence.review_record_id == released.reviews.current(
        "cue->outcome"
    ).review_id


def test_learning_change_after_release_makes_review_stale_until_re_reviewed():
    memory = learned_memory()
    memory = quarantine_association(
        memory,
        "cue->outcome",
        reason="initial concern",
    )
    memory = release_association(
        memory,
        "cue->outcome",
        reason="initial revision cleared",
    )
    changed = add_learning(memory)

    assert changed.current_version("cue->outcome") == 2
    with pytest.raises(AssociationReviewStaleError):
        recall_association(
            memory=changed,
            association_id="cue->outcome",
            cue_match=1.0,
            cue_receipt=cue_receipt("cue-after-change"),
        )

    re_reviewed = release_association(
        changed,
        "cue->outcome",
        reason="new revision reviewed",
    )
    influence = recall_association(
        memory=re_reviewed,
        association_id="cue->outcome",
        cue_match=1.0,
        cue_receipt=cue_receipt("cue-after-rereview"),
    )
    assert influence.learned_strength == pytest.approx(1.0)


def test_review_log_is_append_only_and_rejects_same_state_noop():
    memory = learned_memory()
    quarantined = quarantine_association(
        memory,
        "cue->outcome",
        reason="first hold",
    )
    first = quarantined.reviews.current("cue->outcome")
    assert first is not None

    with pytest.raises(ReviewNoOpError):
        quarantine_association(
            quarantined,
            "cue->outcome",
            reason="duplicate hold",
        )

    released = release_association(
        quarantined,
        "cue->outcome",
        reason="cleared",
    )
    history = released.reviews.history("cue->outcome")
    assert len(history) == 2
    assert history[0].review_id == first.review_id
    assert history[1].parent_review_id == first.review_id
    assert history[0].disposition is ReviewDisposition.QUARANTINED
    assert history[1].disposition is ReviewDisposition.ACTIVE


def test_unreviewed_association_remains_recallable_for_backward_compatible_admission():
    memory = learned_memory()
    influence = recall_association(
        memory=memory,
        association_id="cue->outcome",
        cue_match=1.0,
        cue_receipt=cue_receipt(),
    )
    assert influence.review_record_id is None
    assert influence.learned_strength == pytest.approx(0.8)
