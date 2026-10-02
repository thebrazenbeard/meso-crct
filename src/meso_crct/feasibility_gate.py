"""Conservative feasibility admission before partial-order comparison."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json

from .comparison_family import (
    ComparisonFamilyView,
    as_comparison_family_view,
)
from .domain_aggregation import ContributionFamilyView
from .evidence import EvidenceCurrentness
from .feasibility import FeasibilityAssessment, FeasibilityState
from .partial_order import (
    PartialOrderPolicy,
    PartialOrderStatus,
    select_by_partial_order,
)


class UnadmittedFeasibilityAssessment(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class FeasibilityProducerSpec:
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
class FeasibilityAdmissionPolicy:
    policy_id: str
    policy_revision: str
    producers: tuple[FeasibilityProducerSpec, ...] = ()

    def __post_init__(self) -> None:
        if not self.policy_id.strip():
            raise ValueError("policy_id must be non-empty")
        if not self.policy_revision.strip():
            raise ValueError("policy_revision must be non-empty")
        keys = tuple(producer.key for producer in self.producers)
        if len(keys) != len(set(keys)):
            raise ValueError("feasibility producer specs must be unique")

    def admits(self, assessment: FeasibilityAssessment) -> bool:
        key = (
            assessment.evidence.producer_id,
            assessment.evidence.producer_revision,
        )
        return any(producer.key == key for producer in self.producers)


@dataclass(frozen=True, slots=True)
class FeasibilityGateResult:
    admitted_target_ids: tuple[str, ...]
    deferred_target_ids: tuple[str, ...]
    infeasible_target_ids: tuple[str, ...]
    missing_assessment_target_ids: tuple[str, ...]
    gate_input_digest: str
    admission_policy_id: str
    admission_policy_revision: str


class FeasibilityAwareStatus(str, Enum):
    SELECTED = "selected"
    INCOMPARABLE = "incomparable"
    DEFERRED = "deferred"
    NO_ADMISSIBLE_CANDIDATE = "no_admissible_candidate"


@dataclass(frozen=True, slots=True)
class FeasibilityAwareSelectionResult:
    status: FeasibilityAwareStatus
    selected_target_id: str | None
    provisional_frontier_target_ids: tuple[str, ...]
    dominated_target_ids: tuple[str, ...]
    incomplete_target_ids: tuple[str, ...]
    infeasible_target_ids: tuple[str, ...]
    deferred_target_ids: tuple[str, ...]
    missing_assessment_target_ids: tuple[str, ...]
    feasibility_input_digest: str
    partial_order_input_digest: str
    policy_id: str
    policy_revision: str
    admission_policy_id: str
    admission_policy_revision: str
    decision_input_digest: str


def _wrapper_digest(
    *,
    candidate_target_ids: tuple[str, ...],
    family_views: tuple[ComparisonFamilyView | ContributionFamilyView, ...],
    feasibility_input_digest: str,
    partial_order_input_digest: str,
) -> str:
    payload = {
        "candidates": sorted(candidate_target_ids),
        "family_views": sorted(
            (
                generic.target_id,
                generic.family_id,
                generic.magnitude,
                generic.source_kind.value,
                generic.source_digest,
            )
            for generic in (
                as_comparison_family_view(view) for view in family_views
            )
        ),
        "feasibility_input_digest": feasibility_input_digest,
        "partial_order_input_digest": partial_order_input_digest,
    }
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _gate_digest(
    *,
    candidate_target_ids: tuple[str, ...],
    assessments: tuple[FeasibilityAssessment, ...],
    admission_policy: FeasibilityAdmissionPolicy,
) -> str:
    payload = {
        "candidates": sorted(candidate_target_ids),
        "admission_policy": {
            "policy_id": admission_policy.policy_id,
            "policy_revision": admission_policy.policy_revision,
            "producers": sorted(
                producer.key for producer in admission_policy.producers
            ),
        },
        "assessments": sorted(
            (
                assessment.target_id,
                assessment.state.value,
                assessment.expected_success,
                assessment.uncertainty,
                assessment.controllability,
                assessment.delay_seconds,
                assessment.evidence.producer_id,
                assessment.evidence.producer_revision,
                assessment.evidence.subject_id,
                assessment.evidence.source_id,
                assessment.evidence.currentness.value,
            )
            for assessment in assessments
        ),
    }
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def gate_by_feasibility(
    *,
    candidate_target_ids: tuple[str, ...],
    assessments: tuple[FeasibilityAssessment, ...],
    admission_policy: FeasibilityAdmissionPolicy,
) -> FeasibilityGateResult:
    if len(candidate_target_ids) != len(set(candidate_target_ids)):
        raise ValueError("candidate_target_ids must be unique")
    for target_id in candidate_target_ids:
        if not target_id.strip():
            raise ValueError("candidate target IDs must be non-empty")

    candidate_set = set(candidate_target_ids)
    by_target: dict[str, FeasibilityAssessment] = {}
    for assessment in assessments:
        if assessment.target_id not in candidate_set:
            raise ValueError(
                f"feasibility assessment target is not a candidate: "
                f"{assessment.target_id}"
            )
        if assessment.target_id in by_target:
            raise ValueError(
                f"duplicate feasibility assessment: {assessment.target_id}"
            )
        if not admission_policy.admits(assessment):
            raise UnadmittedFeasibilityAssessment(
                "feasibility assessment producer is not admitted"
            )
        by_target[assessment.target_id] = assessment

    admitted: list[str] = []
    deferred: list[str] = []
    infeasible: list[str] = []
    missing: list[str] = []

    for target_id in candidate_target_ids:
        assessment = by_target.get(target_id)
        if assessment is None:
            deferred.append(target_id)
            missing.append(target_id)
            continue

        if assessment.evidence.currentness is not EvidenceCurrentness.CURRENT:
            deferred.append(target_id)
            continue

        if assessment.state is FeasibilityState.FEASIBLE:
            admitted.append(target_id)
        elif assessment.state is FeasibilityState.INFEASIBLE:
            infeasible.append(target_id)
        else:
            deferred.append(target_id)

    return FeasibilityGateResult(
        admitted_target_ids=tuple(sorted(admitted)),
        deferred_target_ids=tuple(sorted(deferred)),
        infeasible_target_ids=tuple(sorted(infeasible)),
        missing_assessment_target_ids=tuple(sorted(missing)),
        gate_input_digest=_gate_digest(
            candidate_target_ids=candidate_target_ids,
            assessments=assessments,
            admission_policy=admission_policy,
        ),
        admission_policy_id=admission_policy.policy_id,
        admission_policy_revision=admission_policy.policy_revision,
    )


def select_with_feasibility(
    *,
    candidate_target_ids: tuple[str, ...],
    family_views: tuple[ComparisonFamilyView | ContributionFamilyView, ...],
    feasibility_assessments: tuple[FeasibilityAssessment, ...],
    policy: PartialOrderPolicy,
    admission_policy: FeasibilityAdmissionPolicy,
) -> FeasibilityAwareSelectionResult:
    candidate_set = set(candidate_target_ids)
    for view in family_views:
        if view.target_id not in candidate_set:
            raise ValueError(
                f"family view target is not a candidate: {view.target_id}"
            )

    gate = gate_by_feasibility(
        candidate_target_ids=candidate_target_ids,
        assessments=feasibility_assessments,
        admission_policy=admission_policy,
    )
    admitted_set = set(gate.admitted_target_ids)
    admitted_views = tuple(
        view for view in family_views if view.target_id in admitted_set
    )

    partial = select_by_partial_order(
        candidate_target_ids=gate.admitted_target_ids,
        family_views=admitted_views,
        policy=policy,
    )

    if gate.deferred_target_ids:
        status = FeasibilityAwareStatus.DEFERRED
        selected_target_id = None
    elif partial.status is PartialOrderStatus.SELECTED:
        status = FeasibilityAwareStatus.SELECTED
        selected_target_id = partial.selected_target_id
    elif partial.status is PartialOrderStatus.INCOMPARABLE:
        status = FeasibilityAwareStatus.INCOMPARABLE
        selected_target_id = None
    else:
        status = FeasibilityAwareStatus.NO_ADMISSIBLE_CANDIDATE
        selected_target_id = None

    return FeasibilityAwareSelectionResult(
        status=status,
        selected_target_id=selected_target_id,
        provisional_frontier_target_ids=partial.frontier_target_ids,
        dominated_target_ids=partial.dominated_target_ids,
        incomplete_target_ids=partial.incomplete_target_ids,
        infeasible_target_ids=gate.infeasible_target_ids,
        deferred_target_ids=gate.deferred_target_ids,
        missing_assessment_target_ids=gate.missing_assessment_target_ids,
        feasibility_input_digest=gate.gate_input_digest,
        partial_order_input_digest=partial.decision_input_digest,
        policy_id=partial.policy_id,
        policy_revision=partial.policy_revision,
        admission_policy_id=gate.admission_policy_id,
        admission_policy_revision=gate.admission_policy_revision,
        decision_input_digest=_wrapper_digest(
            candidate_target_ids=candidate_target_ids,
            family_views=family_views,
            feasibility_input_digest=gate.gate_input_digest,
            partial_order_input_digest=partial.decision_input_digest,
        ),
    )
