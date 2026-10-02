# MESO Goal-Obligation Admission Receipt Hardening Plan

> **For agentic workers:** Use the host's task-by-task TDD workflow.

**Goal:** Make `AdmittedGoalObligation` an actually unforgeable admission product before strict allocation auditing consumes it.

**Base:** Draft PR #18 head `5a979dcef1336a3ea9a3f479cf8106c636ae9fae`.

## Architecture

Keep `GoalObligation` as the legacy/base constraint type.

Harden `AdmittedGoalObligation` so:
- only `admit_goal_obligation()` can construct it;
- it remains an `isinstance(..., GoalObligation)`;
- it preserves the original claim evidence;
- it preserves admission policy ID/revision;
- it adds a deterministic `admission_input_digest` binding:
  - goal ID;
  - minimum nonprotective share;
  - evidence producer/revision/subject/source/currentness;
  - admission policy ID/revision;
  - admitted producer set.

## Constraints

- Direct construction of `AdmittedGoalObligation` is rejected.
- CURRENT evidence and producer admission requirements remain unchanged.
- Digest is stable under producer-spec ordering.
- Digest changes when claim evidence/value or policy revision changes.
- Legacy direct `GoalObligation` construction is unchanged.
- No local motivational pressure, consent, or execution authority is introduced.

## Red cases

- direct admitted-obligation construction fails;
- admitted object exposes a non-empty admission digest;
- digest changes with claim source/value;
- digest changes with policy revision;
- producer-spec ordering does not change digest;
- admitted object remains GoalObligation-compatible.

## Verification

- focused obligation-admission tests;
- full suite;
- compileall;
- git diff --check.

## Out of scope

- strict attested allocation audit;
- remaining-horizon obligation pressure;
- allocation guard migration to partial-order selection;
- merge/runtime activation.
