"""Partial-order selection over normalized semantic-family views."""

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


class FamilyDirection(str, Enum):
    BENEFIT = "benefit"
    COST = "cost"
    CONTEXT_ONLY = "context_only"


@dataclass(frozen=True, slots=True)
class FamilyComparisonSpec:
    family_id: str
    direction: FamilyDirection

    def __post_init__(self) -> None:
        if not self.family_id.strip():
            raise ValueError("family_id must be non-empty")


@dataclass(frozen=True, slots=True)
class PartialOrderPolicy:
    policy_id: str
    policy_revision: str
    families: tuple[FamilyComparisonSpec, ...] = ()

    def __post_init__(self) -> None:
        if not self.policy_id.strip():
            raise ValueError("policy_id must be non-empty")
        if not self.policy_revision.strip():
            raise ValueError("policy_revision must be non-empty")
        family_ids = tuple(spec.family_id for spec in self.families)
        if len(family_ids) != len(set(family_ids)):
            raise ValueError("partial-order policy family IDs must be unique")


class PartialOrderStatus(str, Enum):
    SELECTED = "selected"
    INCOMPARABLE = "incomparable"
    NO_ADMISSIBLE_CANDIDATE = "no_admissible_candidate"


@dataclass(frozen=True, slots=True)
class PartialOrderSelectionResult:
    status: PartialOrderStatus
    selected_target_id: str | None
    frontier_target_ids: tuple[str, ...]
    dominated_target_ids: tuple[str, ...]
    incomplete_target_ids: tuple[str, ...]
    policy_id: str
    policy_revision: str
    decision_input_digest: str


def _decision_input_digest(
    *,
    candidate_target_ids: tuple[str, ...],
    family_views: tuple[ComparisonFamilyView | ContributionFamilyView, ...],
    policy: PartialOrderPolicy,
) -> str:
    payload = {
        "candidates": sorted(candidate_target_ids),
        "policy": {
            "policy_id": policy.policy_id,
            "policy_revision": policy.policy_revision,
            "families": sorted(
                (
                    spec.family_id,
                    spec.direction.value,
                )
                for spec in policy.families
            ),
        },
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
    }
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _dominates(
    left: dict[str, float],
    right: dict[str, float],
    comparable_specs: tuple[FamilyComparisonSpec, ...],
) -> bool:
    strictly_better = False
    for spec in comparable_specs:
        left_value = left[spec.family_id]
        right_value = right[spec.family_id]
        if spec.direction is FamilyDirection.BENEFIT:
            if left_value < right_value:
                return False
            if left_value > right_value:
                strictly_better = True
        elif spec.direction is FamilyDirection.COST:
            if left_value > right_value:
                return False
            if left_value < right_value:
                strictly_better = True
        else:
            raise AssertionError("context-only family reached dominance comparison")
    return strictly_better


def select_by_partial_order(
    *,
    candidate_target_ids: tuple[str, ...],
    family_views: tuple[ComparisonFamilyView | ContributionFamilyView, ...],
    policy: PartialOrderPolicy,
) -> PartialOrderSelectionResult:
    if len(candidate_target_ids) != len(set(candidate_target_ids)):
        raise ValueError("candidate_target_ids must be unique")
    for target_id in candidate_target_ids:
        if not target_id.strip():
            raise ValueError("candidate target IDs must be non-empty")

    candidate_set = set(candidate_target_ids)
    by_target: dict[str, dict[str, float]] = {
        target_id: {} for target_id in candidate_target_ids
    }
    seen_view_keys: set[tuple[str, str]] = set()

    for view in family_views:
        generic = as_comparison_family_view(view)
        if generic.target_id not in candidate_set:
            raise ValueError(
                f"family view target is not a candidate: {generic.target_id}"
            )
        key = (generic.target_id, generic.family_id)
        if key in seen_view_keys:
            raise ValueError(
                f"duplicate target/family view: "
                f"{generic.target_id}/{generic.family_id}"
            )
        seen_view_keys.add(key)
        by_target[generic.target_id][generic.family_id] = generic.magnitude

    input_digest = _decision_input_digest(
        candidate_target_ids=candidate_target_ids,
        family_views=family_views,
        policy=policy,
    )

    if not candidate_target_ids:
        return PartialOrderSelectionResult(
            status=PartialOrderStatus.NO_ADMISSIBLE_CANDIDATE,
            selected_target_id=None,
            frontier_target_ids=(),
            dominated_target_ids=(),
            incomplete_target_ids=(),
            policy_id=policy.policy_id,
            policy_revision=policy.policy_revision,
            decision_input_digest=input_digest,
        )

    comparable_specs = tuple(
        spec
        for spec in policy.families
        if spec.direction is not FamilyDirection.CONTEXT_ONLY
    )
    required_family_ids = tuple(spec.family_id for spec in comparable_specs)

    incomplete = tuple(
        sorted(
            target_id
            for target_id in candidate_target_ids
            if any(
                family_id not in by_target[target_id]
                for family_id in required_family_ids
            )
        )
    )
    incomplete_set = set(incomplete)
    complete = tuple(
        target_id
        for target_id in candidate_target_ids
        if target_id not in incomplete_set
    )

    dominated: set[str] = set()
    for right_id in complete:
        for left_id in complete:
            if left_id == right_id:
                continue
            if _dominates(
                by_target[left_id],
                by_target[right_id],
                comparable_specs,
            ):
                dominated.add(right_id)
                break

    complete_frontier = tuple(
        target_id for target_id in complete if target_id not in dominated
    )
    frontier = tuple(sorted(set(complete_frontier) | incomplete_set))
    dominated_ids = tuple(sorted(dominated))

    if incomplete:
        status = PartialOrderStatus.INCOMPARABLE
        selected_target_id = None
    elif len(frontier) == 1:
        status = PartialOrderStatus.SELECTED
        selected_target_id = frontier[0]
    else:
        status = PartialOrderStatus.INCOMPARABLE
        selected_target_id = None

    return PartialOrderSelectionResult(
        status=status,
        selected_target_id=selected_target_id,
        frontier_target_ids=frontier,
        dominated_target_ids=dominated_ids,
        incomplete_target_ids=incomplete,
        policy_id=policy.policy_id,
        policy_revision=policy.policy_revision,
        decision_input_digest=input_digest,
    )
