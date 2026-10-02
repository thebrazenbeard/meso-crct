# MESO End-to-End Attested Allocation Guard Plan

> **For agentic workers:** Use the host's task-by-task TDD workflow.

**Goal:** Make `QUALIFIED_RECEIPTS` an end-to-end attested allocation-control path rather than mixing qualified current mappings with a legacy/raw historical audit.

**Base:** Draft PR #20 head `6d2dde236ef342b8a8e7217f52dbb2a4633cb12a`.

## Contract

`select_with_allocation_guard()` accepts either:
- legacy `AllocationAudit`; or
- strict `AttestedAllocationAuditReceipt`.

### QUALIFIED_RECEIPTS mode

Requires:
- `AttestedAllocationAuditReceipt`;
- every supplied obligation is constructor-gated `AdmittedGoalObligation`;
- supplied obligation admission digests exactly equal the audit receipt's certified obligation digests.

Uses:
- `audit_receipt.audit` for deficit/neglect state;
- current `GoalRelationAdmissionReceipt` values for current goal->candidate mappings.

Returns:
- the strict audit input digest in `AllocationGuardResult.allocation_audit_input_digest`;
- exact supporting current goal-relation receipts when a rebalance occurs.

### LEGACY_TARGET_IDENTITY mode

Requires:
- naked `AllocationAudit`;
- does not accept `AttestedAllocationAuditReceipt`;
- preserves raw `GoalObligation` compatibility;
- `allocation_audit_input_digest` is `None`.

## Constraints

- Nonempty current goal-relation receipts still auto-select qualified mode.
- Explicit qualified mode with zero current mappings still requires a strict audit receipt.
- Explicit legacy mode + current relation receipts remains invalid.
- Strict audit receipt + obligation mismatch is rejected before selection.
- Raw obligations in qualified mode are rejected.
- Protective override remains absolute after input qualification.
- Same selection policy and current mapping behavior from PR #18 remain unchanged.
- No local obligation-pressure scalar is introduced.
- No execution/consent authority is introduced.

## Red cases

- qualified mode + naked audit -> `UnattestedAllocationAudit`;
- qualified mode + raw obligation -> `UnadmittedAllocationObligation`;
- strict audit receipt + different admitted obligation digest set -> `AllocationAuditObligationMismatch`;
- strict audit receipt + exact admitted obligations permits rebalance;
- result preserves `allocation_audit_input_digest`;
- explicit qualified mode with zero mapping receipts still requires strict audit;
- legacy mode rejects strict audit receipt rather than reinterpreting it;
- legacy naked audit/raw obligation behavior remains unchanged;
- protective result remains unchanged when strict inputs are valid.

## Verification

- focused new attested-guard tests;
- migrated goal-aware guard tests;
- unchanged legacy allocation-guard tests;
- full suite;
- compileall;
- git diff --check.

## Out of scope

- remaining-horizon service pressure;
- partial-order allocation-guard migration;
- goal lifecycle;
- merge/runtime activation.
