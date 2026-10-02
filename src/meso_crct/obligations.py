"""Admission of provenance-bound goal allocation obligation claims."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math

from .allocation import GoalObligation
from .evidence import EvidenceCurrentness, EvidenceRef


_GOAL_OBLIGATION_ADMISSION_TOKEN = object()


class InadmissibleGoalObligationClaim(ValueError):
    pass


class UnadmittedGoalObligationClaim(ValueError):
    pass


def _unit(value: float, *, name: str) -> float:
    value = float(value)
    if not math.isfinite(value) or value < 0.0 or value > 1.0:
        raise ValueError(f"{name} must be finite and within [0, 1]")
    return value


@dataclass(frozen=True, slots=True)
class GoalObligationClaim:
    goal_id: str
    minimum_nonprotective_share: float
    evidence: EvidenceRef

    def __post_init__(self) -> None:
        if not self.goal_id.strip():
            raise ValueError("goal_id must be non-empty")
        if self.evidence.subject_id != self.goal_id:
            raise ValueError("goal obligation evidence subject must match goal_id")
        object.__setattr__(
            self,
            "minimum_nonprotective_share",
            _unit(
                self.minimum_nonprotective_share,
                name="minimum_nonprotective_share",
            ),
        )


@dataclass(frozen=True, slots=True)
class GoalObligationProducerSpec:
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
class GoalObligationAdmissionPolicy:
    policy_id: str
    policy_revision: str
    producers: tuple[GoalObligationProducerSpec, ...] = ()

    def __post_init__(self) -> None:
        if not self.policy_id.strip():
            raise ValueError("policy_id must be non-empty")
        if not self.policy_revision.strip():
            raise ValueError("policy_revision must be non-empty")
        keys = tuple(producer.key for producer in self.producers)
        if len(keys) != len(set(keys)):
            raise ValueError("goal obligation producer specs must be unique")

    def admits(self, claim: GoalObligationClaim) -> bool:
        key = (
            claim.evidence.producer_id,
            claim.evidence.producer_revision,
        )
        return any(producer.key == key for producer in self.producers)


@dataclass(frozen=True, slots=True, init=False)
class AdmittedGoalObligation(GoalObligation):
    evidence: EvidenceRef
    admission_policy_id: str
    admission_policy_revision: str
    admission_input_digest: str

    def __init__(
        self,
        goal_id: str,
        minimum_nonprotective_share: float = 0.0,
        *,
        evidence: EvidenceRef,
        admission_policy_id: str,
        admission_policy_revision: str,
        admission_input_digest: str,
        _token: object | None = None,
    ) -> None:
        if _token is not _GOAL_OBLIGATION_ADMISSION_TOKEN:
            raise TypeError(
                "AdmittedGoalObligation must be issued by admit_goal_obligation"
            )
        object.__setattr__(self, "goal_id", goal_id)
        object.__setattr__(
            self,
            "minimum_nonprotective_share",
            minimum_nonprotective_share,
        )
        GoalObligation.__post_init__(self)


        if evidence.subject_id != self.goal_id:
            raise ValueError("admitted obligation evidence subject must match goal_id")
        if not admission_policy_id.strip():
            raise ValueError("admission_policy_id must be non-empty")
        if not admission_policy_revision.strip():
            raise ValueError("admission_policy_revision must be non-empty")
        if not admission_input_digest.strip():
            raise ValueError("admission_input_digest must be non-empty")

        object.__setattr__(self, "evidence", evidence)
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
    claim: GoalObligationClaim,
    policy: GoalObligationAdmissionPolicy,
) -> str:
    payload = {
        "claim": {
            "goal_id": claim.goal_id,
            "minimum_nonprotective_share": claim.minimum_nonprotective_share,
            "evidence": {
                "producer_id": claim.evidence.producer_id,
                "producer_revision": claim.evidence.producer_revision,
                "subject_id": claim.evidence.subject_id,
                "source_id": claim.evidence.source_id,
                "currentness": claim.evidence.currentness.value,
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


def admit_goal_obligation(
    claim: GoalObligationClaim,
    policy: GoalObligationAdmissionPolicy,
) -> AdmittedGoalObligation:
    if claim.evidence.currentness is not EvidenceCurrentness.CURRENT:
        raise InadmissibleGoalObligationClaim(
            "goal obligation claim evidence must be CURRENT"
        )
    if not policy.admits(claim):
        raise UnadmittedGoalObligationClaim(
            "goal obligation claim producer is not admitted"
        )
    return AdmittedGoalObligation(
        goal_id=claim.goal_id,
        minimum_nonprotective_share=claim.minimum_nonprotective_share,
        evidence=claim.evidence,
        admission_policy_id=policy.policy_id,
        admission_policy_revision=policy.policy_revision,
        admission_input_digest=_admission_digest(claim, policy),
        _token=_GOAL_OBLIGATION_ADMISSION_TOKEN,
    )
