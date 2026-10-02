"""Provenance-bearing relations between selected targets and external goals."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json

from .evidence import EvidenceCurrentness, EvidenceRef


_GOAL_RELATION_RECEIPT_TOKEN = object()


class InadmissibleGoalRelation(ValueError):
    pass


class UnadmittedGoalRelation(ValueError):
    pass


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
    policy_id: str = "legacy-goal-relation-policy"
    policy_revision: str = "1"
    producers: tuple[GoalRelationProducerSpec, ...] = ()

    def __post_init__(self) -> None:
        if not self.policy_id.strip():
            raise ValueError("policy_id must be non-empty")
        if not self.policy_revision.strip():
            raise ValueError("policy_revision must be non-empty")
        keys = tuple(producer.key for producer in self.producers)
        if len(keys) != len(set(keys)):
            raise ValueError("goal relation producer specs must be unique")

    def admits(self, relation: GoalRelation) -> bool:
        key = (
            relation.evidence.producer_id,
            relation.evidence.producer_revision,
        )
        return any(producer.key == key for producer in self.producers)


@dataclass(frozen=True, slots=True, init=False)
class GoalRelationAdmissionReceipt:
    relation: GoalRelation
    admission_policy_id: str
    admission_policy_revision: str
    admission_input_digest: str

    def __init__(
        self,
        *,
        relation: GoalRelation,
        admission_policy_id: str,
        admission_policy_revision: str,
        admission_input_digest: str,
        _token: object | None = None,
    ) -> None:
        if _token is not _GOAL_RELATION_RECEIPT_TOKEN:
            raise TypeError(
                "GoalRelationAdmissionReceipt must be issued by admit_goal_relation"
            )
        if not admission_policy_id.strip():
            raise ValueError("admission_policy_id must be non-empty")
        if not admission_policy_revision.strip():
            raise ValueError("admission_policy_revision must be non-empty")
        if not admission_input_digest.strip():
            raise ValueError("admission_input_digest must be non-empty")

        object.__setattr__(self, "relation", relation)
        object.__setattr__(self, "admission_policy_id", admission_policy_id)
        object.__setattr__(
            self,
            "admission_policy_revision",
            admission_policy_revision,
        )
        object.__setattr__(
            self,
            "admission_input_digest",
            admission_input_digest,
        )


def _admission_digest(
    relation: GoalRelation,
    policy: GoalRelationAdmissionPolicy,
) -> str:
    payload = {
        "relation": {
            "goal_id": relation.goal_id,
            "target_id": relation.target_id,
            "evidence": {
                "producer_id": relation.evidence.producer_id,
                "producer_revision": relation.evidence.producer_revision,
                "subject_id": relation.evidence.subject_id,
                "source_id": relation.evidence.source_id,
                "currentness": relation.evidence.currentness.value,
            },
        },
        "policy": {
            "policy_id": policy.policy_id,
            "policy_revision": policy.policy_revision,
            "producers": sorted(producer.key for producer in policy.producers),
        },
    }
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def admit_goal_relation(
    relation: GoalRelation,
    policy: GoalRelationAdmissionPolicy,
) -> GoalRelationAdmissionReceipt:
    if relation.evidence.currentness is not EvidenceCurrentness.CURRENT:
        raise InadmissibleGoalRelation(
            "goal relation evidence must be CURRENT"
        )
    if not policy.admits(relation):
        raise UnadmittedGoalRelation(
            "goal relation producer is not admitted"
        )
    return GoalRelationAdmissionReceipt(
        relation=relation,
        admission_policy_id=policy.policy_id,
        admission_policy_revision=policy.policy_revision,
        admission_input_digest=_admission_digest(relation, policy),
        _token=_GOAL_RELATION_RECEIPT_TOKEN,
    )
