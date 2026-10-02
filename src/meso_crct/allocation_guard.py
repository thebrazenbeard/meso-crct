"""Governed response to long-horizon allocation pathology.

The guard can temporarily redirect one non-protective selection toward a
neglected goal that is currently non-quiescent. It never overrides a protective
selection and never manufactures relevance for a quiescent goal.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .allocation import AllocationAudit, GoalObligation
from .allocation_attested import (
    AttestedAllocationAuditReceipt,
    UnadmittedAllocationObligation,
)
from .arbitration import ArbitrationMode
from .goals import GoalRelationAdmissionReceipt
from .obligations import AdmittedGoalObligation
from .selection import (
    SelectionPolicy,
    SelectionResult,
    TargetState,
    select_target,
)


class UnattestedAllocationAudit(ValueError):
    pass


class AllocationAuditObligationMismatch(ValueError):
    pass


class AllocationAuditModeMismatch(ValueError):
    pass


class GoalRelationGuardMode(str, Enum):
    LEGACY_TARGET_IDENTITY = "legacy_target_identity"
    QUALIFIED_RECEIPTS = "qualified_receipts"


@dataclass(frozen=True, slots=True)
class AllocationGuardResult:
    base_selection: SelectionResult
    final_selection: SelectionResult
    guard_applied: bool
    reason: str | None
    rebalanced_goal_id: str | None
    rebalanced_goal_relation_receipts: tuple[GoalRelationAdmissionReceipt, ...] = ()
    goal_relation_mode: GoalRelationGuardMode = (
        GoalRelationGuardMode.LEGACY_TARGET_IDENTITY
    )
    allocation_audit_input_digest: str | None = None


def _ordinary_mode(mode: ArbitrationMode) -> bool:
    return mode in {
        ArbitrationMode.ORIENTING,
        ArbitrationMode.MOTIVATIONAL,
        ArbitrationMode.EPISTEMIC,
    }


def _qualified_audit_inputs(
    audit: AllocationAudit | AttestedAllocationAuditReceipt,
    obligations: tuple[GoalObligation, ...],
) -> tuple[AllocationAudit, tuple[GoalObligation, ...], str]:
    if not isinstance(audit, AttestedAllocationAuditReceipt):
        raise UnattestedAllocationAudit(
            "qualified allocation guard requires AttestedAllocationAuditReceipt"
        )

    admitted: list[AdmittedGoalObligation] = []
    for obligation in obligations:
        if not isinstance(obligation, AdmittedGoalObligation):
            raise UnadmittedAllocationObligation(
                "qualified allocation guard requires admitted goal obligations"
            )
        admitted.append(obligation)

    ordered = tuple(
        sorted(
            admitted,
            key=lambda obligation: (
                obligation.goal_id,
                obligation.admission_input_digest,
            ),
        )
    )
    supplied_digests = tuple(
        obligation.admission_input_digest for obligation in ordered
    )
    if supplied_digests != audit.obligation_admission_digests:
        raise AllocationAuditObligationMismatch(
            "guard obligations do not match the strict allocation audit receipt"
        )

    return audit.audit, tuple(ordered), audit.audit_input_digest


def _legacy_audit_inputs(
    audit: AllocationAudit | AttestedAllocationAuditReceipt,
    obligations: tuple[GoalObligation, ...],
) -> tuple[AllocationAudit, tuple[GoalObligation, ...], None]:
    if isinstance(audit, AttestedAllocationAuditReceipt):
        raise AllocationAuditModeMismatch(
            "legacy allocation guard cannot reinterpret an attested audit receipt"
        )
    if not isinstance(audit, AllocationAudit):
        raise TypeError("legacy allocation guard requires AllocationAudit")
    return audit, obligations, None


def select_with_allocation_guard(
    targets: tuple[TargetState, ...] | list[TargetState],
    *,
    audit: AllocationAudit | AttestedAllocationAuditReceipt,
    obligations: Iterable[GoalObligation],
    policy: SelectionPolicy | None = None,
    goal_relation_receipts: Iterable[GoalRelationAdmissionReceipt] = (),
    goal_relation_mode: GoalRelationGuardMode | None = None,
) -> AllocationGuardResult:
    """Apply one explicit rebalancing opportunity after ordinary selection.

    Qualified receipt mode requires an attested historical allocation audit,
    admitted obligations certified by that exact audit, and admitted current
    goal->target mappings. Legacy mode preserves the V2 identity behavior.
    """
    targets = tuple(targets)
    receipts = tuple(goal_relation_receipts)
    obligations = tuple(obligations)

    if goal_relation_mode is None:
        resolved_relation_mode = (
            GoalRelationGuardMode.QUALIFIED_RECEIPTS
            if receipts
            else GoalRelationGuardMode.LEGACY_TARGET_IDENTITY
        )
    else:
        if not isinstance(goal_relation_mode, GoalRelationGuardMode):
            raise TypeError("goal_relation_mode must be GoalRelationGuardMode")
        resolved_relation_mode = goal_relation_mode

    if (
        resolved_relation_mode is GoalRelationGuardMode.LEGACY_TARGET_IDENTITY
        and receipts
    ):
        raise ValueError(
            "legacy goal-target identity mode cannot accept relation receipts"
        )

    if resolved_relation_mode is GoalRelationGuardMode.QUALIFIED_RECEIPTS:
        audit_state, obligations, audit_digest = _qualified_audit_inputs(
            audit,
            obligations,
        )
    else:
        audit_state, obligations, audit_digest = _legacy_audit_inputs(
            audit,
            obligations,
        )

    target_ids = {target.target_id for target in targets}
    for receipt in receipts:
        if receipt.relation.target_id not in target_ids:
            raise ValueError(
                "goal relation receipt target must be a current candidate"
            )

    base = select_target(targets, policy=policy)

    if base.used_protective_override:
        return AllocationGuardResult(
            base_selection=base,
            final_selection=base,
            guard_applied=False,
            reason="protective_override",
            rebalanced_goal_id=None,
            rebalanced_goal_relation_receipts=(),
            goal_relation_mode=resolved_relation_mode,
            allocation_audit_input_digest=audit_digest,
        )

    if "goal_neglect" not in audit_state.flags:
        return AllocationGuardResult(
            base_selection=base,
            final_selection=base,
            guard_applied=False,
            reason=None,
            rebalanced_goal_id=None,
            rebalanced_goal_relation_receipts=(),
            goal_relation_mode=resolved_relation_mode,
            allocation_audit_input_digest=audit_digest,
        )

    shares = dict(audit_state.goal_shares)
    obligations_by_id = {item.goal_id: item for item in obligations}
    neglected = []
    for goal_id in audit_state.neglected_goals:
        obligation = obligations_by_id.get(goal_id)
        if obligation is None:
            continue
        deficit = obligation.minimum_nonprotective_share - shares.get(goal_id, 0.0)
        neglected.append((goal_id, deficit))

    neglected.sort(key=lambda item: (-item[1], item[0]))
    evaluations = {item.target_id: item for item in base.evaluations}
    qualified_relation_mode = (
        resolved_relation_mode is GoalRelationGuardMode.QUALIFIED_RECEIPTS
    )

    for goal_id, _ in neglected:
        supporting_receipts: tuple[GoalRelationAdmissionReceipt, ...] = ()

        if qualified_relation_mode:
            goal_receipts = tuple(
                sorted(
                    (
                        receipt
                        for receipt in receipts
                        if receipt.relation.goal_id == goal_id
                    ),
                    key=lambda receipt: receipt.admission_input_digest,
                )
            )
            if not goal_receipts:
                continue

            candidate_ids = {
                receipt.relation.target_id for receipt in goal_receipts
            }
            mapped_targets = tuple(
                target
                for target in targets
                if target.target_id in candidate_ids
            )
            if not mapped_targets:
                continue

            scoped = select_target(mapped_targets, policy=policy)
            if not scoped.selected:
                continue
            assert scoped.selected_target_id is not None
            assert scoped.selected_decision is not None
            if not _ordinary_mode(scoped.selected_decision.mode):
                continue

            selected_target_id = scoped.selected_target_id
            selected_decision = scoped.selected_decision
            supporting_receipts = tuple(
                receipt
                for receipt in goal_receipts
                if receipt.relation.target_id == selected_target_id
            )
        else:
            evaluation = evaluations.get(goal_id)
            if evaluation is None:
                continue
            if not _ordinary_mode(evaluation.decision.mode):
                continue
            selected_target_id = goal_id
            selected_decision = evaluation.decision

        final = SelectionResult(
            selected_target_id=selected_target_id,
            selected_decision=selected_decision,
            evaluations=base.evaluations,
            used_protective_override=False,
            policy_id=base.policy_id,
            policy_revision=base.policy_revision,
        )
        return AllocationGuardResult(
            base_selection=base,
            final_selection=final,
            guard_applied=(base.selected_target_id != selected_target_id),
            reason="goal_obligation_rebalance",
            rebalanced_goal_id=goal_id,
            rebalanced_goal_relation_receipts=supporting_receipts,
            goal_relation_mode=resolved_relation_mode,
            allocation_audit_input_digest=audit_digest,
        )

    return AllocationGuardResult(
        base_selection=base,
        final_selection=base,
        guard_applied=False,
        reason="no_currently_relevant_neglected_goal",
        rebalanced_goal_id=None,
        rebalanced_goal_relation_receipts=(),
        goal_relation_mode=resolved_relation_mode,
        allocation_audit_input_digest=audit_digest,
    )
