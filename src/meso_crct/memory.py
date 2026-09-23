"""Versioned association-memory owner for MESO-CRCT.

This module owns only bounded learned association strengths. It does not admit
autobiographical memories, identity facts, relationship state, or arbitrary
text. Updates are append-only revisions tied to plasticity candidates and their
verified transition receipt lineage.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math

from .plasticity import PlasticityCandidate


def _signed_unit(value: float, *, name: str) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return min(1.0, max(-1.0, value))


@dataclass(frozen=True, slots=True)
class AssociationRevision:
    association_id: str
    version: int
    strength: float
    previous_strength: float
    applied_delta: float
    transition_receipt_id: str
    operation: str
    revision_id: str

    def __post_init__(self) -> None:
        if not self.association_id.strip():
            raise ValueError("association_id must be non-empty")
        if self.version < 1:
            raise ValueError("version must be >= 1")
        object.__setattr__(self, "strength", _signed_unit(self.strength, name="strength"))
        object.__setattr__(
            self,
            "previous_strength",
            _signed_unit(self.previous_strength, name="previous_strength"),
        )
        object.__setattr__(
            self,
            "applied_delta",
            _signed_unit(self.applied_delta, name="applied_delta"),
        )
        if not self.transition_receipt_id.strip():
            raise ValueError("transition_receipt_id must be non-empty")
        if self.operation not in {"apply", "revert"}:
            raise ValueError("operation must be 'apply' or 'revert'")
        if not self.revision_id.strip():
            raise ValueError("revision_id must be non-empty")


class MemoryVersionConflict(ValueError):
    pass


class PlasticityReplayError(ValueError):
    pass


class AssociationNotFound(KeyError):
    pass


@dataclass(frozen=True, slots=True)
class AssociationMemory:
    """Immutable append-only association revision log."""

    revisions: tuple[AssociationRevision, ...] = ()

    def current(self, association_id: str) -> AssociationRevision | None:
        for revision in reversed(self.revisions):
            if revision.association_id == association_id:
                return revision
        return None

    def current_strength(self, association_id: str) -> float:
        current = self.current(association_id)
        return 0.0 if current is None else current.strength

    def current_version(self, association_id: str) -> int:
        current = self.current(association_id)
        return 0 if current is None else current.version

    def receipt_used(
        self,
        transition_receipt_id: str,
        association_id: str,
    ) -> bool:
        return any(
            revision.transition_receipt_id == transition_receipt_id
            and revision.association_id == association_id
            and revision.operation == "apply"
            for revision in self.revisions
        )

    def history(self, association_id: str) -> tuple[AssociationRevision, ...]:
        return tuple(
            revision
            for revision in self.revisions
            if revision.association_id == association_id
        )


def _revision_id(
    *,
    association_id: str,
    version: int,
    strength: float,
    previous_strength: float,
    applied_delta: float,
    transition_receipt_id: str,
    operation: str,
) -> str:
    payload = json.dumps(
        {
            "association_id": association_id,
            "version": version,
            "strength": strength,
            "previous_strength": previous_strength,
            "applied_delta": applied_delta,
            "transition_receipt_id": transition_receipt_id,
            "operation": operation,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def apply_candidate(
    memory: AssociationMemory,
    candidate: PlasticityCandidate,
    *,
    expected_version: int,
) -> AssociationMemory:
    """Apply one candidate as a new immutable association revision.

    Optimistic version checking prevents stale writers. A transition receipt may
    contribute at most one applied candidate across this memory snapshot.
    """
    current_version = memory.current_version(candidate.association_id)
    if expected_version != current_version:
        raise MemoryVersionConflict(
            f"expected version {expected_version}, current version {current_version}"
        )

    if memory.receipt_used(
        candidate.transition_receipt_id,
        candidate.association_id,
    ):
        raise PlasticityReplayError(
            "transition receipt already used for a persistent association update"
        )

    previous = memory.current_strength(candidate.association_id)
    strength = _signed_unit(
        previous + candidate.delta,
        name="resulting_strength",
    )
    version = current_version + 1
    revision = AssociationRevision(
        association_id=candidate.association_id,
        version=version,
        strength=strength,
        previous_strength=previous,
        applied_delta=candidate.delta,
        transition_receipt_id=candidate.transition_receipt_id,
        operation="apply",
        revision_id=_revision_id(
            association_id=candidate.association_id,
            version=version,
            strength=strength,
            previous_strength=previous,
            applied_delta=candidate.delta,
            transition_receipt_id=candidate.transition_receipt_id,
            operation="apply",
        ),
    )
    return AssociationMemory(revisions=memory.revisions + (revision,))


def revert_last(
    memory: AssociationMemory,
    association_id: str,
    *,
    expected_version: int,
) -> AssociationMemory:
    """Append a reversal revision instead of deleting history."""
    history = memory.history(association_id)
    if not history:
        raise AssociationNotFound(association_id)

    current = history[-1]
    if expected_version != current.version:
        raise MemoryVersionConflict(
            f"expected version {expected_version}, current version {current.version}"
        )

    prior_strength = history[-2].strength if len(history) >= 2 else 0.0
    version = current.version + 1
    applied_delta = prior_strength - current.strength
    receipt_ref = current.transition_receipt_id

    revision = AssociationRevision(
        association_id=association_id,
        version=version,
        strength=prior_strength,
        previous_strength=current.strength,
        applied_delta=applied_delta,
        transition_receipt_id=receipt_ref,
        operation="revert",
        revision_id=_revision_id(
            association_id=association_id,
            version=version,
            strength=prior_strength,
            previous_strength=current.strength,
            applied_delta=applied_delta,
            transition_receipt_id=receipt_ref,
            operation="revert",
        ),
    )
    return AssociationMemory(revisions=memory.revisions + (revision,))
