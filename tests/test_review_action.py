import pytest

from meso_crct import (
    CircuitState,
    EventSequencer,
    Provenance,
    ProvenanceVerifier,
    ReviewActionKind,
    ReviewActionProposal,
    ReviewDisposition,
    ReviewEvidenceKind,
    ReviewEvidenceOutcome,
    SalienceState,
    SourceKind,
    assess_review_evidence,
    bind_review_evidence,
    evaluate_transition,
    propose_review_action,
)


def receipt(stream):
    state = CircuitState(
        salience=SalienceState(semantic_relevance=0.5),
    )
    claim = Provenance(
        source_kind=SourceKind.ENVIRONMENT,
        source_id=stream,
        source_revision="v1",
    )
    verified = ProvenanceVerifier(
        [claim],
        verifier_id="review-action-verifier",
    ).verify(claim)
    _, event = EventSequencer(stream).issue()
    return evaluate_transition(
        before=CircuitState(),
        after=state,
        provenance=verified,
        event=event,
    )


def assessment(outcome, *, kind=ReviewEvidenceKind.HOLDOUT, count=1):
    evidence = []
    for index in range(count):
        ref = f"case-{index}"
        evidence.append(
            bind_review_evidence(
                association_id="cue->outcome",
                memory_revision_id="rev-1",
                kind=kind,
                outcome=outcome,
                evidence_ref=ref,
                receipt=receipt(ref),
            )
        )
    return assess_review_evidence(evidence)


def test_review_action_proposal_cannot_be_constructed_directly():
    assessed = assessment(
        ReviewEvidenceOutcome.CONTRADICTS,
        kind=ReviewEvidenceKind.COUNTEREXAMPLE,
    )
    with pytest.raises(TypeError):
        ReviewActionProposal(
            association_id=assessed.association_id,
            memory_revision_id=assessed.memory_revision_id,
            assessment_id=assessed.assessment_id,
            action=ReviewActionKind.QUARANTINE,
            risk_class=assessed.risk_class,
            evidence_ids=assessed.evidence_ids,
            current_disposition=None,
        )


def test_contradicted_active_association_proposes_quarantine():
    proposal = propose_review_action(
        assessment(
            ReviewEvidenceOutcome.CONTRADICTS,
            kind=ReviewEvidenceKind.COUNTEREXAMPLE,
        ),
        current_disposition=ReviewDisposition.ACTIVE,
    )
    assert proposal.action is ReviewActionKind.QUARANTINE
    assert not proposal.mutation_authorized
    assert not proposal.can_mutate


def test_suspected_overgeneralization_unreviewed_proposes_quarantine():
    proposal = propose_review_action(
        assessment(ReviewEvidenceOutcome.CONTRADICTS),
        current_disposition=None,
    )
    assert proposal.action is ReviewActionKind.QUARANTINE


def test_already_quarantined_bad_evidence_holds_state():
    proposal = propose_review_action(
        assessment(ReviewEvidenceOutcome.CONTRADICTS),
        current_disposition=ReviewDisposition.QUARANTINED,
    )
    assert proposal.action is ReviewActionKind.HOLD


def test_clear_quarantined_association_proposes_release():
    proposal = propose_review_action(
        assessment(ReviewEvidenceOutcome.SUPPORTS, count=2),
        current_disposition=ReviewDisposition.QUARANTINED,
    )
    assert proposal.action is ReviewActionKind.RELEASE


def test_clear_unreviewed_association_does_not_create_unneeded_mutation():
    proposal = propose_review_action(
        assessment(ReviewEvidenceOutcome.SUPPORTS, count=2),
        current_disposition=None,
    )
    assert proposal.action is ReviewActionKind.HOLD


def test_insufficient_evidence_always_holds():
    proposal = propose_review_action(
        assessment(ReviewEvidenceOutcome.SUPPORTS, count=1),
        current_disposition=ReviewDisposition.QUARANTINED,
    )
    assert proposal.action is ReviewActionKind.HOLD
