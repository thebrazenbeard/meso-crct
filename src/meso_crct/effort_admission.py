"""Admission of provenance-bound effort appraisals."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json

from .effort import EffortAssessment
from .evidence import EvidenceCurrentness


class InadmissibleEffortAssessment(ValueError):
    pass


class UnadmittedEffortAssessment(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class EffortProducerSpec:
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
class EffortAdmissionPolicy:
    policy_id: str
    policy_revision: str
    producers: tuple[EffortProducerSpec, ...] = ()

    def __post_init__(self) -> None:
        if not self.policy_id.strip():
            raise ValueError("policy_id must be non-empty")
        if not self.policy_revision.strip():
            raise ValueError("policy_revision must be non-empty")
        keys = tuple(producer.key for producer in self.producers)
        if len(keys) != len(set(keys)):
            raise ValueError("effort producer specs must be unique")

    def admits(self, assessment: EffortAssessment) -> bool:
        key = (
            assessment.evidence.producer_id,
            assessment.evidence.producer_revision,
        )
        return any(producer.key == key for producer in self.producers)


@dataclass(frozen=True, slots=True, kw_only=True)
class AdmittedEffortAssessment(EffortAssessment):
    admission_policy_id: str
    admission_policy_revision: str
    admission_input_digest: str

    def __post_init__(self) -> None:
        super(AdmittedEffortAssessment, self).__post_init__()
        if not self.admission_policy_id.strip():
            raise ValueError("admission_policy_id must be non-empty")
        if not self.admission_policy_revision.strip():
            raise ValueError("admission_policy_revision must be non-empty")
        if not self.admission_input_digest.strip():
            raise ValueError("admission_input_digest must be non-empty")


def _admission_digest(
    assessment: EffortAssessment,
    policy: EffortAdmissionPolicy,
) -> str:
    payload = {
        "assessment": {
            "target_id": assessment.target_id,
            "required_effort": assessment.required_effort,
            "effort_cost": assessment.effort_cost,
            "willingness_to_exert": assessment.willingness_to_exert,
            "vigor_proposal": assessment.vigor_proposal,
            "evidence": {
                "producer_id": assessment.evidence.producer_id,
                "producer_revision": assessment.evidence.producer_revision,
                "subject_id": assessment.evidence.subject_id,
                "source_id": assessment.evidence.source_id,
                "currentness": assessment.evidence.currentness.value,
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


def admit_effort_assessment(
    assessment: EffortAssessment,
    policy: EffortAdmissionPolicy,
) -> AdmittedEffortAssessment:
    if assessment.evidence.currentness is not EvidenceCurrentness.CURRENT:
        raise InadmissibleEffortAssessment(
            "effort assessment evidence must be CURRENT"
        )
    if not policy.admits(assessment):
        raise UnadmittedEffortAssessment(
            "effort assessment producer is not admitted"
        )
    return AdmittedEffortAssessment(
        target_id=assessment.target_id,
        evidence=assessment.evidence,
        required_effort=assessment.required_effort,
        effort_cost=assessment.effort_cost,
        willingness_to_exert=assessment.willingness_to_exert,
        vigor_proposal=assessment.vigor_proposal,
        admission_policy_id=policy.policy_id,
        admission_policy_revision=policy.policy_revision,
        admission_input_digest=_admission_digest(assessment, policy),
    )
