# MESO Finite-Horizon Obligation Service Requirements Plan

> **For agentic workers:** Use the host's task-by-task TDD workflow.

**Goal:** Derive per-goal finite-horizon service requirements from a strict attested allocation audit and admitted minimum-share obligations, without converting obligations into reward, salience, desire, or action authority.

**Base:** Draft PR #22 head `8e2e6c198b8466f022a93039e09f249e715baab6`.

## Public model

`AllocationServiceHorizon(total_nonprotective_slots)`
- finite integer slot horizon;
- must be >= 0;
- represents ordinary/non-protective allocation slots only;
- exposes deterministic `horizon_spec_digest`.

`ObligationServiceState`
- `SATISFIED`
- `ACTIVE`
- `CRITICAL`
- `INDIVIDUALLY_MISSED`

`ObligationServiceRequirement`
- constructor-gated derived receipt;
- `goal_id`;
- `required_total_slots`;
- `served_slots`;
- `remaining_horizon_slots`;
- `remaining_required_slots`;
- `slack_slots`;
- `required_remaining_share: float | None`;
- `state`;
- `obligation_admission_digest`;
- `allocation_audit_input_digest`;
- `horizon_spec_digest`;
- deterministic `requirement_input_digest`.

`derive_obligation_service_requirements(audit_receipt, obligations, horizon)`
- requires `AttestedAllocationAuditReceipt`;
- requires constructor-gated admitted obligations;
- exact obligation admission digests must match the audit receipt;
- horizon total must be >= observed non-protective sample count;
- returns requirements in canonical goal order.

## Math

For admitted goal `g`:

```
H = total_nonprotective_slots
n = audit.nonprotective_samples
q = minimum_nonprotective_share
s = exact attested goal_service_count

required_total_slots = ceil(q * H)
remaining_horizon_slots = H - n
remaining_required_slots = max(0, required_total_slots - s)
slack_slots = remaining_horizon_slots - remaining_required_slots
```

When `remaining_horizon_slots > 0`:

```
required_remaining_share =
    remaining_required_slots / remaining_horizon_slots
```

When `remaining_horizon_slots == 0`, `required_remaining_share = None`.

Use decimalized share text for the ceiling multiplication so binary float edge behavior does not silently undercount.

## State

- `SATISFIED`: remaining_required_slots == 0.
- `INDIVIDUALLY_MISSED`: remaining_required_slots > remaining_horizon_slots.
- `CRITICAL`: remaining_required_slots == remaining_horizon_slots > 0.
- `ACTIVE`: otherwise.

This is **individual** service feasibility only.

## Constraints

- Protective samples do not consume the horizon; use strict audit `nonprotective_samples`.
- One sample may count toward multiple goals.
- No relation/target identity inference occurs here.
- No joint schedulability claim.
- No target selection or guard behavior changes.
- No reward, pleasure, salience, desire, vigor, consent, intent, action authority, or execution fields.
- Requirement provenance binds exact audit + obligation + horizon.

## Red cases

- satisfied;
- active with positive slack;
- critical at zero slack;
- individually missed with negative slack;
- 25% of 10 requires 3 slots;
- zero remaining horizon yields `required_remaining_share is None`;
- protective episodes do not consume horizon slots;
- one sample may satisfy two goals;
- horizon shorter than observed ordinary history is rejected;
- raw obligation is rejected;
- same semantic obligation from different provenance is rejected;
- direct requirement construction is rejected;
- requirement digest changes with horizon/audit/obligation input;
- no motivational/action-authority fields;
- no joint-feasibility field.

## Verification

- focused service-requirement tests;
- strict audit tests;
- full suite;
- compileall;
- git diff --check.

## Out of scope

- using service state to select a goal;
- joint schedulability;
- current goal↔target routing;
- partial-order target selection;
- merge/runtime activation.

## Hostile review outcome

> A goal with positive slack can still be impossible to satisfy jointly with other goals because disjoint goals compete for slots while one shared target may satisfy multiple goals in one slot.

**ACCEPTED.** This tranche exposes only per-goal remaining service and slack. The state name is deliberately \`INDIVIDUALLY_MISSED\`, there is no \`jointly_feasible\` field, and no caller may infer joint schedulability from \`ACTIVE\` or \`CRITICAL\` alone.

A second precision limit remains explicit: \`minimum_nonprotective_share\` is already stored as a Python float upstream. \`Decimal(str(stored_share))\` avoids introducing an additional binary multiplication artifact during finite-slot ceiling, but it cannot recover decimal intent that was already lost before obligation admission. Changing the canonical share representation is a separate schema decision, not silently folded into this tranche.
