# MESO Finite-Horizon Obligation Service Deficit Research V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / CONTROL-LAYER CANDIDATE / NO IMPLEMENTATION`

## Question

How should an admitted long-horizon minimum-share obligation affect local allocation without being converted into reward, desire, or a generic utility bonus?

Current obligation semantics:

```
GoalObligation.minimum_nonprotective_share
```

means a minimum share of ordinary (non-protective) allocation over a window.

The current guard reacts only after an audit reports neglect. It ranks neglected goals by:

```
minimum_share - observed_share
```

That detects historical under-allocation, but it does not represent how much service is still required or how much scheduling slack remains.

## Research lineage

Fair-queueing and service-guarantee literature treats minimum shares/rates as service constraints rather than reward.

Relevant recurring ideas:
- guaranteed minimum service rate;
- accumulated service lag/deficit relative to an ideal allocation;
- scheduling based on remaining work/service;
- laxity/slack as remaining time minus remaining required service;
- finite-horizon schedulers that reason over a bounded number of future slots.

This is a closer analogy to MESO's allocation obligation than adding a motivational score.

## Proposed finite-horizon model

Let:

- `H` = total planned non-protective allocation slots in the horizon;
- `n` = non-protective slots already observed;
- `q_g` = admitted minimum share for goal `g`;
- `s_g` = exact number of observed slots attested as serving goal `g`.

Then:

```
required_total_slots_g = ceil(q_g * H)
remaining_horizon_slots = H - n
remaining_required_slots_g =
    max(0, required_total_slots_g - s_g)
slack_slots_g =
    remaining_horizon_slots - remaining_required_slots_g
```

When `remaining_horizon_slots > 0`:

```
required_remaining_share_g =
    remaining_required_slots_g / remaining_horizon_slots
```

This is a scheduling requirement, not motivational intensity.

## Interpretive states

### SATISFIED
```
remaining_required_slots == 0
```

The final minimum can already be met even if the goal receives no more service in this horizon.

### ACTIVE
```
0 < remaining_required_slots < remaining_horizon_slots
```

Some remaining service is required, but scheduling slack exists.

### CRITICAL
```
remaining_required_slots == remaining_horizon_slots
```

Every remaining ordinary slot would have to count toward the goal to meet its individual minimum.

### INDIVIDUALLY_MISSED
```
remaining_required_slots > remaining_horizon_slots
```

The goal's minimum can no longer be met within this horizon even if every remaining ordinary slot served it.

This state should produce audit/control information, not negative hedonic state.

## Exact counts matter

The current strict allocation audit exposes:
- non-protective sample count;
- floating goal shares.

For service-deficit calculations, exact goal-service counts should be retained in the attested audit receipt.

Do not reconstruct counts from:

```
share * sample_count
```

because:
- shares are floating representations;
- a single sample can count toward multiple goals;
- the receipt already has the exact attested relations at audit time.

Required precursor:

```
AttestedAllocationAuditReceipt.goal_service_counts
```

with canonical `(goal_id, count)` ordering and inclusion in the audit digest.

## Important non-equivalence

```
remaining_required_share
!= desire
!= reward
!= salience
!= action authority
```

It is a constraint on future allocation.

A target serving a goal may still be:
- infeasible;
- quiescent;
- blocked by protection;
- unauthorized for execution.

## Joint schedulability problem

> **HOSTILE REVIEWER:** Per-goal slack does not establish that all obligations can be met simultaneously.

**ACCEPTED.**

Example A — disjoint service:

```
remaining slots = 10
goal A requires 6
goal B requires 6
no target can serve both
```

Each goal is individually feasible, but the pair is jointly impossible.

Example B — overlapping service:

```
remaining slots = 10
goal A requires 6
goal B requires 6
one target's attested selection counts toward both
```

The same 6 slots can satisfy both.

Therefore this first model must use the term:

```
individual service requirement
```

and must not claim global/joint schedulability.

Joint schedulability requires current goal↔target coverage topology plus assumptions about which goals one allocation sample can simultaneously satisfy.

## Multi-goal counting

A single non-protective sample may count toward multiple admitted goals when it carries multiple attested relations.

Therefore:

```
sum(goal_service_counts) may exceed nonprotective_samples
```

This is valid.

Service counts are goal coverage counts, not mutually exclusive resource buckets.

## Horizon semantics

The horizon must be explicitly supplied by the controller.

Do not infer `H` from:
- the current window length;
- an obligation percentage;
- a deadline timestamp without a slot model.

Initial candidate:

```
AllocationServiceHorizon(total_nonprotective_slots: int)
```

Requirements:
- finite integer;
- >= observed non-protective samples;
- no wall-clock claim;
- no implication that protective episodes consume ordinary allocation slots.

## Rounding

A minimum share is a lower bound.

For a finite integer slot horizon:

```
required_total_slots = ceil(q * H)
```

not round-to-nearest.

Example:

```
q = 0.25
H = 10
required = 3 slots
```

because 2/10 = 0.20 does not meet the 0.25 minimum.

Implementation should avoid accidental binary-float edge behavior; use decimalized share representation for the ceiling calculation.

## Relation to current guard

The current qualified allocation guard can safely answer:

> Which currently relevant attested target can serve a neglected goal?

A finite-horizon service requirement can later improve:

> Which obligation has the least slack / greatest remaining service requirement?

But it should not directly override:
- protection;
- feasibility;
- authority;
- the target selector.

A possible future ordering layer is:

```
strict attested audit
-> finite-horizon individual service requirements
-> choose obligation(s) needing service
-> current attested goal-target mappings
-> feasibility
-> target arbitration
```

## Why simple share deficit is insufficient

Two goals can have the same historical share deficit but different remaining scheduling pressure.

Example:

```
H = 100
n = 90
A: minimum 0.50, served 44 -> needs 6 of 10
B: minimum 0.20, served 17 -> needs 3 of 10
```

Historical share deficits alone do not directly encode these required remaining rates.

Similarly, early in a horizon a large current deficit may still have abundant slack.

## Candidate receipt

Research sketch:

```
ObligationServiceRequirement:
    goal_id
    required_total_slots
    served_slots
    remaining_horizon_slots
    remaining_required_slots
    slack_slots
    required_remaining_share
    state
    obligation_admission_digest
    allocation_audit_input_digest
    horizon_spec_digest
```

No execution authority.

## Required proof cases

### OSR-01 — already satisfied
Minimum service already met.
Expected: remaining_required = 0, SATISFIED.

### OSR-02 — active with slack
Some service required, but not every remaining slot.
Expected: ACTIVE.

### OSR-03 — critical
Required remaining slots exactly equal remaining slots.
Expected: CRITICAL.

### OSR-04 — individually missed
Required remaining slots exceed remaining slots.
Expected: INDIVIDUALLY_MISSED.

### OSR-05 — finite-horizon ceiling
25% of 10 requires 3 slots, not 2.

### OSR-06 — protective samples excluded
Only non-protective observed slots consume the service horizon.

### OSR-07 — multi-goal sample
One attested sample may increment both A and B.

### OSR-08 — no target-identity inference
Relation-free sample increments no goal in the strict receipt.

### OSR-09 — horizon shorter than observed history
Reject.

### OSR-10 — source binding
Requirement binds the exact obligation admission digest + strict audit digest.

### OSR-11 — no motivational fields
No reward/desire/salience/vigor/action-authority field.

### OSR-12 — no joint-feasibility claim
Per-goal requirement exposes individual state only.

## Current conclusion

The strongest next control primitive is not an "obligation motivation" value.

It is:

```
attested allocation history
+ admitted minimum-share obligation
+ explicit finite slot horizon
->
individual remaining service requirement + slack
```

That keeps minimum-share commitments in the scheduling/control layer where they belong.
