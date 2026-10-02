"""Admission of provenance-bound goal allocation obligation claims."""

from __future__ import annotations

from dataclasses import dataclass
import math

from .allocation import GoalObligation
from .evidence import EvidenceCurrentness, EvidenceRef


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


@dataclass(frozen=True, slots=True, kw_only=True)
class AdmittedGoalObligation(GoalObligation):
    evidence: EvidenceRef
    admission_policy_id: str
    admission_policy_revision: str

    def __post_init__(self) -> None:
        super(AdmittedGoalObligation, self).__post_init__()
        if not self.admission_policy_id.strip():
            raise ValueError("admission_policy_id must be non-empty")
        if not self.admission_policy_revision.strip():
            raise ValueError("admission_policy_revision must be non-empty")


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
    )
