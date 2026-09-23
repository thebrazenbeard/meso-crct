"""Non-mutating review-action proposals from evidence assessments."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .review import ReviewDisposition
from .review_evidence import ReviewEvidenceAssessment, ReviewRiskClass


class ReviewActionKind(StrEnum):
    QUARANTINE = "quarantine"
    RELEASE = "release"
    HOLD = "hold"


_ACTION_PROPOSAL_TOKEN = object()


@dataclass(frozen=True, slots=True, init=False)
class ReviewActionProposal:
    association_id: str
    memory_revision_id: str
    assessment_id: str
    action: ReviewActionKind
    risk_class: ReviewRiskClass
    evidence_ids: tuple[str, ...]
    current_disposition: ReviewDisposition | None
    mutation_authorized: bool

    def __init__(
        self,
        *,
        association_id: str,
        memory_revision_id: str,
        assessment_id: str,
        action: ReviewActionKind,
        risk_class: ReviewRiskClass,
        evidence_ids: tuple[str, ...],
        current_disposition: ReviewDisposition | None,
        _token: object | None = None,
    ) -> None:
        if _token is not _ACTION_PROPOSAL_TOKEN:
            raise TypeError(
                "ReviewActionProposal must be created by propose_review_action"
            )
        object.__setattr__(self, "association_id", association_id)
        object.__setattr__(self, "memory_revision_id", memory_revision_id)
        object.__setattr__(self, "assessment_id", assessment_id)
        object.__setattr__(self, "action", action)
        object.__setattr__(self, "risk_class", risk_class)
        object.__setattr__(self, "evidence_ids", tuple(evidence_ids))
        object.__setattr__(self, "current_disposition", current_disposition)
        object.__setattr__(self, "mutation_authorized", False)

    @property
    def can_mutate(self) -> bool:
        return False


def propose_review_action(
    assessment: ReviewEvidenceAssessment,
    *,
    current_disposition: ReviewDisposition | None = None,
) -> ReviewActionProposal:
    """Map evidence state to a non-mutating governance proposal."""
    if assessment.risk_class in {
        ReviewRiskClass.CONTRADICTED,
        ReviewRiskClass.SUSPECTED_OVERGENERALIZATION,
    }:
        action = (
            ReviewActionKind.HOLD
            if current_disposition is ReviewDisposition.QUARANTINED
            else ReviewActionKind.QUARANTINE
        )
    elif assessment.risk_class is ReviewRiskClass.CLEAR:
        action = (
            ReviewActionKind.RELEASE
            if current_disposition is ReviewDisposition.QUARANTINED
            else ReviewActionKind.HOLD
        )
    else:
        action = ReviewActionKind.HOLD

    return ReviewActionProposal(
        association_id=assessment.association_id,
        memory_revision_id=assessment.memory_revision_id,
        assessment_id=assessment.assessment_id,
        action=action,
        risk_class=assessment.risk_class,
        evidence_ids=assessment.evidence_ids,
        current_disposition=current_disposition,
        _token=_ACTION_PROPOSAL_TOKEN,
    )
