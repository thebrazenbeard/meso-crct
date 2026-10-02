# MESO Goal-Aware Allocation Guard Implementation Plan

> **For agentic workers:** Use the host's task-by-task TDD workflow.

**Goal:** Remove the obsolete `goal_id == target_id` assumption from long-horizon allocation rebalancing while preserving legacy behavior when no qualified current goal↔target relation receipts are supplied.

**Base:** Draft PR #17 head `92cd399f9dec7020b552f0b885248a27ea5963d9`.

## Architecture

Extend `select_with_allocation_guard()` with an optional tuple of current `GoalRelationAdmissionReceipt` objects.

Two explicit modes:

1. **Qualified relation mode** — when at least one receipt is supplied:
   - only receipt-backed target mappings may satisfy a neglected goal;
   - no implicit `goal_id == target_id` fallback;
   - receipts whose target is not among current candidates are rejected;
   - if several current targets serve one neglected goal, choose among those targets using the same explicit `SelectionPolicy`.

2. **Legacy identity mode** — when no receipts are supplied:
   - preserve existing `goal_id == target_id` behavior for compatibility.

The guard result retains the exact receipt(s) that justified any qualified rebalance.

## Constraints

- Protective override remains absolute.
- Goal relations do not manufacture relevance: quiescent mapped targets remain ineligible.
- One goal may map to many targets.
- One target may serve many goals.
- Largest obligation-share deficit is still considered first.
- Qualified mode never falls back to identity for an unmapped goal.
- Goal-relation mode is explicit: callers can require QUALIFIED_RECEIPTS even when the receipt set is empty; nonempty receipts auto-select qualified mode for compatibility, while explicit legacy mode rejects receipt input.
- Receipt target must exist in the current target set.
- Final `SelectionResult` preserves the original selection policy ID/revision.
- Rebalanced receipt set is deterministic and limited to the selected target + selected neglected goal.
- Existing legacy tests remain unchanged.
- No obligation-pressure scalar is introduced.
- No consent or action authority is introduced.

## Red cases

- goal ID different from target ID rebalances through an admitted receipt;
- one neglected goal with multiple mapped targets chooses the best currently relevant target under the same selection policy;
- qualified mode does not fall back to a same-named target lacking a receipt;
- relation receipt for a noncandidate target is rejected;
- result preserves the exact receipt(s) supporting the chosen target/goal;
- custom selection policy ID/revision survives guard rebalancing;
- protective override remains untouched;
- legacy no-receipt behavior remains unchanged;
- quiescent mapped target is not resurrected;
- one target serving multiple goals can satisfy the highest-deficit neglected goal.

## Verification

- focused allocation-guard tests;
- full suite;
- compileall;
- git diff --check.

## Out of scope

- deriving obligation pressure from remaining horizon;
- strict attested-only allocation auditing;
- goal lifecycle;
- cross-family fallback selection;
- merge/runtime activation.
