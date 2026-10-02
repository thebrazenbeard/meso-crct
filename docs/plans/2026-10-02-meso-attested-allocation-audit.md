# MESO Attested Allocation Audit Implementation Plan

> **For agentic workers:** Use the host's task-by-task TDD workflow.

**Goal:** Add a strict allocation-audit path whose goal accounting depends only on admitted goal↔target relations and admitted goal obligations, while preserving the existing legacy audit unchanged.

**Base:** Draft PR #19 head `288ebce4c71516bd86516bcdca8539940ac69c34`.

## Architecture

Refactor the existing allocation math into one private core that accepts a goal-ID resolver per sample.

Keep `audit_attention_budget()` as the compatibility surface:
- raw stored goal relations are used when present;
- otherwise `target_id == goal_id` remains the V2 fallback.

Add `audit_attested_attention_budget()` in a separate module to avoid allocation/obligation import cycles.

Strict audit requirements:
- every obligation is a constructor-gated `AdmittedGoalObligation`;
- obligation goal IDs are unique;
- every stored goal relation on every sample has a matching `GoalRelationAdmissionReceipt`;
- every attested relation target matches the sample target;
- relation-free samples contribute to no goal (no identity fallback);
- duplicate same-goal relations within one sample count once;
- protective samples remain excluded from ordinary goal-share accounting;
- the result is wrapped in constructor-gated `AttestedAllocationAuditReceipt`;
- receipt digest binds the exact chronological sample window, relation admission digests, admitted obligation digests, and crowdout threshold.

## Constraints

- Legacy audit semantics and tests remain unchanged.
- Strict audit never accepts raw `GoalObligation`.
- Strict audit never silently ignores an unattested stored relation.
- Strict audit never infers goal identity from target identity.
- The audit receipt is not action authority.
- No obligation-pressure or local selection behavior is added.

## Red cases

- raw obligation rejected;
- sample with unattested stored relation rejected;
- attested relation whose target differs from sample target rejected;
- fully attested relation counts toward its admitted goal;
- relation-free sample with target ID equal to goal ID does not count in strict mode;
- legacy audit still performs target-identity fallback;
- duplicate same-goal attested relations count once;
- duplicate obligation goal IDs rejected;
- direct strict-audit receipt construction rejected;
- digest changes when relation evidence or obligation admission changes;
- digest is stable under obligation input ordering;
- protective samples do not contribute ordinary goal share.

## Verification

- focused strict-audit tests;
- existing allocation tests;
- full suite;
- compileall;
- git diff --check.

## Out of scope

- requiring strict audit receipts in the allocation guard;
- remaining-horizon service pressure;
- partial-order allocation guard;
- merge/runtime activation.
