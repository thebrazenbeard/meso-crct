# MESO Goal-Relation Admission Receipt Implementation Plan

> **For agentic workers:** Use the host's task-by-task TDD workflow.

**Goal:** Preserve the exact admission-policy receipt for goal relations used in allocation accounting without breaking existing GoalRelation storage/equality semantics.

**Base:** Draft PR #16 head 59e99109913ab7b6ff692cd89c98e94f558df394.

## Architecture

Extend GoalRelationAdmissionPolicy with policy identity/revision while preserving compatibility defaults.

Add constructor-gated GoalRelationAdmissionReceipt plus admit_goal_relation().

AllocationSample keeps:
- goal_relations: raw accepted propositions;
- goal_relation_receipts: one qualified receipt per relation admitted through from_selection().

Direct legacy AllocationSample construction may still contain relations without receipts.

## Constraints

- Receipt requires CURRENT relation evidence.
- Exact producer ID/revision must be admitted by policy.
- Receipt digest binds relation evidence, goal/target, policy identity/revision and producer set.
- Receipt construction is module-gated.
- AllocationSample validates any supplied receipt refers to a stored raw relation.
- from_selection() issues one receipt per accepted relation.
- Existing goal-share accounting remains unchanged.
- AllocationSample exposes explicit attested/unattested relation views and an attestation-complete signal for future strict consumers.
- Legacy relation-only samples remain supported and visibly have no receipts.
- No desire, consent, obligation, or execution authority semantics are added.

## Red cases

- policy exposes policy_id/revision and retains legacy defaults;
- current trusted relation can be admitted to a receipt;
- stale/unknown relation rejected by admit_goal_relation();
- spoofed/wrong-revision producer rejected;
- receipt digest changes with relation source/policy revision;
- producer-spec order does not change receipt digest;
- direct receipt construction rejected;
- from_selection() stores raw relation unchanged plus matching receipt;
- multiple relations produce one receipt each;
- manually supplied mismatched receipt/sample relation rejected;
- direct legacy sample may contain relation with empty receipt tuple;
- existing allocation audit results unchanged.

## Verification

- focused goal-target/receipt tests;
- full suite;
- compileall;
- git diff --check.

## Out of scope

- obligation-pressure derivation;
- strict audit rejection of legacy unattested samples;
- goal lifecycle;
- consent/action authority;
- merge/runtime activation.
