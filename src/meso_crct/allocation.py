"""Long-horizon attention-allocation auditing.

Local priority decisions can each look reasonable while one target monopolizes
processing across time. This module evaluates actual selection outcomes over a
window without treating protective/emergency episodes as ordinary competition.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import math
from typing import Callable, Iterable

from .arbitration import ArbitrationDecision, ArbitrationMode
from .goals import (
    GoalRelation,
    GoalRelationAdmissionPolicy,
    GoalRelationAdmissionReceipt,
    admit_goal_relation,
)
from .selection import SelectionResult


def _unit(value: float, *, name: str) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return min(1.0, max(0.0, value))


@dataclass(frozen=True, slots=True)
class GoalObligation:
    goal_id: str
    minimum_nonprotective_share: float = 0.0

    def __post_init__(self) -> None:
        if not self.goal_id.strip():
            raise ValueError("goal_id must be non-empty")
        object.__setattr__(
            self,
            "minimum_nonprotective_share",
            _unit(
                self.minimum_nonprotective_share,
                name="minimum_nonprotective_share",
            ),
        )


@dataclass(frozen=True, slots=True)
class AllocationSample:
    target_id: str
    priority: float
    dominant_driver: str | None
    protective: bool = False
    goal_relations: tuple[GoalRelation, ...] = ()
    goal_relation_receipts: tuple[GoalRelationAdmissionReceipt, ...] = ()

    def __post_init__(self) -> None:
        if not self.target_id.strip():
            raise ValueError("target_id must be non-empty")
        object.__setattr__(self, "priority", _unit(self.priority, name="priority"))

        unmatched_relations = list(self.goal_relations)
        for receipt in self.goal_relation_receipts:
            try:
                index = unmatched_relations.index(receipt.relation)
            except ValueError as exc:
                raise ValueError(
                    "goal relation receipt must bind a stored goal relation"
                ) from exc
            unmatched_relations.pop(index)

    @property
    def attested_goal_relations(self) -> tuple[GoalRelation, ...]:
        return tuple(receipt.relation for receipt in self.goal_relation_receipts)

    @property
    def unattested_goal_relations(self) -> tuple[GoalRelation, ...]:
        unmatched = list(self.goal_relations)
        for receipt in self.goal_relation_receipts:
            index = unmatched.index(receipt.relation)
            unmatched.pop(index)
        return tuple(unmatched)

    @property
    def goal_relation_attestation_complete(self) -> bool:
        return not self.unattested_goal_relations

    @classmethod
    def from_decision(
        cls,
        target_id: str,
        decision: ArbitrationDecision,
        *,
        goal_relations: tuple[GoalRelation, ...] = (),
        goal_relation_receipts: tuple[GoalRelationAdmissionReceipt, ...] = (),
    ) -> "AllocationSample":
        return cls(
            target_id=target_id,
            priority=decision.priority,
            dominant_driver=decision.dominant_driver,
            protective=decision.mode is ArbitrationMode.PROTECTIVE,
            goal_relations=goal_relations,
            goal_relation_receipts=goal_relation_receipts,
        )

    @classmethod
    def from_selection(
        cls,
        result: SelectionResult,
        *,
        goal_relations: tuple[GoalRelation, ...] = (),
        goal_relation_policy: GoalRelationAdmissionPolicy | None = None,
    ) -> "AllocationSample | None":
        if not result.selected:
            if goal_relations:
                raise ValueError("goal relations require a selected target")
            return None
        assert result.selected_target_id is not None
        assert result.selected_decision is not None
        if goal_relations and goal_relation_policy is None:
            raise ValueError("goal relations require an admission policy")

        receipts: list[GoalRelationAdmissionReceipt] = []
        for relation in goal_relations:
            if relation.target_id != result.selected_target_id:
                raise ValueError("goal relation target must match selected target")
            assert goal_relation_policy is not None
            receipts.append(
                admit_goal_relation(relation, goal_relation_policy)
            )

        return cls.from_decision(
            result.selected_target_id,
            result.selected_decision,
            goal_relations=goal_relations,
            goal_relation_receipts=tuple(receipts),
        )


@dataclass(frozen=True, slots=True)
class AllocationWindow:
    """Append-only history of actual local selection outcomes."""

    samples: tuple[AllocationSample, ...] = ()
    no_selection_cycles: int = 0

    def __post_init__(self) -> None:
        if self.no_selection_cycles < 0:
            raise ValueError("no_selection_cycles must be >= 0")

    def record(
        self,
        result: SelectionResult,
        *,
        goal_relations: tuple[GoalRelation, ...] = (),
        goal_relation_policy: GoalRelationAdmissionPolicy | None = None,
    ) -> "AllocationWindow":
        sample = AllocationSample.from_selection(
            result,
            goal_relations=goal_relations,
            goal_relation_policy=goal_relation_policy,
        )
        if sample is None:
            return AllocationWindow(
                samples=self.samples,
                no_selection_cycles=self.no_selection_cycles + 1,
            )
        return AllocationWindow(
            samples=self.samples + (sample,),
            no_selection_cycles=self.no_selection_cycles,
        )


@dataclass(frozen=True, slots=True)
class AllocationAudit:
    nonprotective_samples: int
    protective_samples: int
    dominant_target: str | None
    dominant_fraction: float
    goal_shares: tuple[tuple[str, float], ...]
    neglected_goals: tuple[str, ...]
    flags: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return not self.flags


def _audit_attention_budget_core(
    samples: Iterable[AllocationSample],
    obligations: Iterable[GoalObligation],
    *,
    crowdout_fraction: float,
    goal_ids_for_sample: Callable[[AllocationSample], Iterable[str]],
) -> AllocationAudit:
    """Shared allocation math with caller-supplied goal attribution semantics."""
    crowdout_fraction = _unit(crowdout_fraction, name="crowdout_fraction")
    samples = tuple(samples)
    obligations = tuple(obligations)

    protective_count = sum(sample.protective for sample in samples)
    ordinary = tuple(sample for sample in samples if not sample.protective)

    if not ordinary:
        return AllocationAudit(
            nonprotective_samples=0,
            protective_samples=protective_count,
            dominant_target=None,
            dominant_fraction=0.0,
            goal_shares=tuple((goal.goal_id, 0.0) for goal in obligations),
            neglected_goals=(),
            flags=(),
        )

    counts = Counter(sample.target_id for sample in ordinary)
    dominant_target, dominant_count = counts.most_common(1)[0]
    dominant_fraction = dominant_count / len(ordinary)

    goal_counts: Counter[str] = Counter()
    for sample in ordinary:
        goal_counts.update(set(goal_ids_for_sample(sample)))

    goal_shares = tuple(
        (goal.goal_id, goal_counts[goal.goal_id] / len(ordinary))
        for goal in obligations
    )
    neglected = tuple(
        goal.goal_id
        for goal in obligations
        if goal_counts[goal.goal_id] / len(ordinary)
        < goal.minimum_nonprotective_share
    )

    flags: list[str] = []
    if neglected:
        flags.append("goal_neglect")

    if neglected and dominant_fraction >= crowdout_fraction:
        flags.append("target_crowd_out")

    dominant_drivers = Counter(
        sample.dominant_driver
        for sample in ordinary
        if sample.target_id == dominant_target and sample.dominant_driver is not None
    )
    if (
        "target_crowd_out" in flags
        and dominant_drivers
        and dominant_drivers.most_common(1)[0][0]
        in {"motivational_salience", "incentive_salience"}
    ):
        flags.append("incentive_capture")

    return AllocationAudit(
        nonprotective_samples=len(ordinary),
        protective_samples=protective_count,
        dominant_target=dominant_target,
        dominant_fraction=dominant_fraction,
        goal_shares=goal_shares,
        neglected_goals=neglected,
        flags=tuple(flags),
    )


def _legacy_goal_ids_for_sample(sample: AllocationSample) -> tuple[str, ...]:
    if sample.goal_relations:
        return tuple(relation.goal_id for relation in sample.goal_relations)
    # V2 compatibility: relation-free samples use target identity as goal identity.
    return (sample.target_id,)


def audit_attention_budget(
    samples: Iterable[AllocationSample],
    obligations: Iterable[GoalObligation],
    *,
    crowdout_fraction: float = 0.75,
) -> AllocationAudit:
    """Audit selected processing slots using V2-compatible goal attribution."""
    return _audit_attention_budget_core(
        samples,
        obligations,
        crowdout_fraction=crowdout_fraction,
        goal_ids_for_sample=_legacy_goal_ids_for_sample,
    )


def audit_allocation_window(
    window: AllocationWindow,
    obligations: Iterable[GoalObligation],
    *,
    crowdout_fraction: float = 0.75,
) -> AllocationAudit:
    """Audit the actual samples accumulated from local selection results."""
    return audit_attention_budget(
        window.samples,
        obligations,
        crowdout_fraction=crowdout_fraction,
    )
