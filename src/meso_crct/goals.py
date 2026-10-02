"""Provenance-bearing relations between selected targets and external goals."""

from __future__ import annotations

from dataclasses import dataclass

from .evidence import EvidenceRef


@dataclass(frozen=True, slots=True)
class GoalRelation:
    goal_id: str
    target_id: str
    evidence: EvidenceRef

    def __post_init__(self) -> None:
        if not self.goal_id.strip():
            raise ValueError("goal_id must be non-empty")
        if not self.target_id.strip():
            raise ValueError("target_id must be non-empty")
        if self.evidence.subject_id != self.target_id:
            raise ValueError("goal relation evidence subject must match target_id")


@dataclass(frozen=True, slots=True)
class GoalRelationProducerSpec:
    producer_id: str
    producer_revision: str

    def __post_init__(self) -> None:
        if not self.producer_id.strip():
            raise ValueError("producer_id must be non-empty")
        if not self.producer_revision.strip():
            raise ValueError("producer_revision must be non-empty")

    @property
    def key(self) -> tuple[str, str]:
        return (self.producer_id, self.producer_revision)


@dataclass(frozen=True, slots=True)
class GoalRelationAdmissionPolicy:
    producers: tuple[GoalRelationProducerSpec, ...] = ()

    def __post_init__(self) -> None:
        keys = tuple(producer.key for producer in self.producers)
        if len(keys) != len(set(keys)):
            raise ValueError("goal relation producer specs must be unique")

    def admits(self, relation: GoalRelation) -> bool:
        key = (
            relation.evidence.producer_id,
            relation.evidence.producer_revision,
        )
        return any(producer.key == key for producer in self.producers)
