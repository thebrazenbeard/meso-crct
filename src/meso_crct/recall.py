"""Guarded association recall for MESO-CRCT.

Stored association strength is not self-activating. Recall requires a current
cue match and a constructor-gated transition receipt for the current event.
Recall can support current motivational salience while preserving learned
direction separately from pleasure and protective hazard.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum
import math

from .circuit import CircuitState
from .memory import AssociationMemory, AssociationNotFound
from .provenance import TransitionReceipt


def _unit(value: float, *, name: str) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return min(1.0, max(0.0, value))


class RecallDirection(StrEnum):
    APPROACH = "approach"
    AVOID = "avoid"
    NEUTRAL = "neutral"


_RECALL_INFLUENCE_TOKEN = object()


@dataclass(frozen=True, slots=True, init=False)
class RecallInfluence:
    association_id: str
    memory_revision_id: str
    cue_receipt_id: str
    cue_match: float
    learned_strength: float
    signed_influence: float
    motivational_support: float
    approach_support: float
    learned_avoidance_support: float
    direction: RecallDirection

    def __init__(
        self,
        *,
        association_id: str,
        memory_revision_id: str,
        cue_receipt_id: str,
        cue_match: float,
        learned_strength: float,
        signed_influence: float,
        motivational_support: float,
        approach_support: float,
        learned_avoidance_support: float,
        direction: RecallDirection,
        _token: object | None = None,
    ) -> None:
        if _token is not _RECALL_INFLUENCE_TOKEN:
            raise TypeError("RecallInfluence must be created by recall_association")
        for name, value in (
            ("association_id", association_id),
            ("memory_revision_id", memory_revision_id),
            ("cue_receipt_id", cue_receipt_id),
        ):
            if not value.strip():
                raise ValueError(f"{name} must be non-empty")
        object.__setattr__(self, "association_id", association_id)
        object.__setattr__(self, "memory_revision_id", memory_revision_id)
        object.__setattr__(self, "cue_receipt_id", cue_receipt_id)
        object.__setattr__(self, "cue_match", _unit(cue_match, name="cue_match"))
        object.__setattr__(self, "learned_strength", float(learned_strength))
        object.__setattr__(self, "signed_influence", float(signed_influence))
        object.__setattr__(
            self,
            "motivational_support",
            _unit(motivational_support, name="motivational_support"),
        )
        object.__setattr__(
            self,
            "approach_support",
            _unit(approach_support, name="approach_support"),
        )
        object.__setattr__(
            self,
            "learned_avoidance_support",
            _unit(learned_avoidance_support, name="learned_avoidance_support"),
        )
        object.__setattr__(self, "direction", direction)


def recall_association(
    *,
    memory: AssociationMemory,
    association_id: str,
    cue_match: float,
    cue_receipt: TransitionReceipt,
) -> RecallInfluence:
    """Recall one learned association only in the presence of a current cue."""
    revision = memory.current(association_id)
    if revision is None:
        raise AssociationNotFound(association_id)

    match = _unit(cue_match, name="cue_match")
    signed = revision.strength * match

    if signed > 0.0:
        direction = RecallDirection.APPROACH
    elif signed < 0.0:
        direction = RecallDirection.AVOID
    else:
        direction = RecallDirection.NEUTRAL

    return RecallInfluence(
        association_id=association_id,
        memory_revision_id=revision.revision_id,
        cue_receipt_id=cue_receipt.receipt_id,
        cue_match=match,
        learned_strength=revision.strength,
        signed_influence=signed,
        motivational_support=abs(signed),
        approach_support=max(0.0, signed),
        learned_avoidance_support=max(0.0, -signed),
        direction=direction,
        _token=_RECALL_INFLUENCE_TOKEN,
    )


def apply_recall_motivation(
    state: CircuitState,
    influence: RecallInfluence,
) -> CircuitState:
    """Apply recall only as bounded motivational support.

    Learned avoidance is kept as metadata on RecallInfluence; it does not
    silently write the hazard/avoidance protection channels.
    """
    motivation = max(
        state.salience.motivational_salience,
        influence.motivational_support,
    )
    salience = state.salience.with_signals(
        motivational_salience=motivation,
    )
    return replace(state, salience=salience)
