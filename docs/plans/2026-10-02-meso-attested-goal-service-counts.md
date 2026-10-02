# MESO Attested Goal Service Counts Plan

> **For agentic workers:** Use the host's task-by-task TDD workflow.

**Goal:** Preserve exact integer service counts for admitted goals in `AttestedAllocationAuditReceipt` so finite-horizon service requirements do not reconstruct counts from floating goal shares.

**Base:** Draft PR #21 head `b129d8fdac6ad6cd212c128f3fe6df576d518aaf`.

## Behavior

Add:

```
AttestedAllocationAuditReceipt.goal_service_counts:
    tuple[(goal_id, integer_count), ...]
```

Semantics:
- counts only non-protective samples;
- a sample increments each distinct attested goal relation at most once;
- one sample may increment multiple different goals;
- relation-free samples increment no goal;
- only admitted-obligation goal IDs are emitted;
- output ordering follows canonical obligation ordering;
- zero-count admitted goals are included;
- counts are bound into the strict audit input digest payload.

## Constraints

- Existing `AllocationAudit.goal_shares` remains unchanged.
- Legacy audit unchanged.
- No target-identity fallback in strict mode.
- No horizon math or pressure state in this tranche.

## Red cases

- one attested service sample yields count 1;
- relation-free admitted goal yields count 0;
- duplicate same-goal relations in one sample still count 1;
- one sample serving two admitted goals increments both;
- protective sample does not increment count;
- canonical goal order is stable under obligation input reordering;
- digest changes when service counts change through different attested history.

## Verification

- focused strict-audit tests;
- full suite;
- compileall;
- git diff --check.
