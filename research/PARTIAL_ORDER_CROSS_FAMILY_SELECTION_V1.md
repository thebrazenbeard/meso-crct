# MESO Partial-Order Cross-Family Selection Research V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / ARBITRATION POLICY CANDIDATE / NO IMPLEMENTATION`

## Problem

MESO now has enough typed representation to expose a deeper selection question:

> Given several admissible targets with different combinations of motivational, epistemic, effort, feasibility, obligation, resource, and domain evidence, when is the evidence itself sufficient to say one target is better?

The current V2 answer is an explicit fixed mode order:

```
PROTECTIVE
>
MOTIVATIONAL
>
EPISTEMIC
>
ORIENTING
```

That is transparent and deterministic, but it creates categorical discontinuities and cannot represent genuine incomparability.

A weighted sum would avoid the categorical mode switch but would silently assume cross-family commensurability.

The current research target is therefore a **partial-order policy**.

## Research lineage

Multi-objective optimization commonly separates:

1. an objective/nondominance phase that computes the Pareto-optimal or non-dominated set; and
2. a preference phase that uses decision-maker information to reduce that set to one solution.

This is useful to MESO because it distinguishes:
- what follows from typed evidence;
- what follows from policy/preferences.

Partial-order methods also allow more than one maximal/non-dominated alternative when criteria conflict.

That is a feature, not necessarily a failure.

## Core policy candidate

### Stage 0 — hard admissibility

Before ordinary cross-family comparison, remove routes that violate hard conditions such as:
- active protection veto;
- explicit authority denial;
- physical/resource infeasibility;
- invalid/stale evidence where currentness is required.

Hard vetoes are not large negative weights.

### Stage 1 — typed family vector

Each remaining target has a set of normalized family views:

```
(target, family_id) -> bounded magnitude
```

produced by the semantic-family normalization layer.

No family is assumed comparable to another merely because both are numeric.

### Stage 2 — declare family comparison direction

A selection policy registers which families are:
- `BENEFIT`: higher is locally better;
- `COST`: lower is locally better;
- `CONTEXT_ONLY`: carried for explanation but excluded from dominance;
- `VETO`: handled before dominance, not traded.

This direction is policy metadata.

It is not inferred from the sign of a number.

### Stage 3 — Pareto-style dominance over shared comparable families

Candidate A dominates B only if:

1. every policy-declared comparable family has a defined value for both candidates or an explicit missing-value rule says comparison is allowed;
2. A is no worse than B on every comparable family;
3. A is strictly better than B on at least one comparable family.

For BENEFIT:
```
A >= B
```

For COST:
```
A <= B
```

If either candidate lacks a required comparable value and policy has no missing-value rule:

```
A ? B = INCOMPARABLE
```

not zero-imputation.

### Stage 4 — non-dominated frontier

Remove candidates dominated by another admissible candidate.

Possible outcomes:

#### One frontier member
Evidence + declared family directions are sufficient to select it.

#### Several frontier members
The evidence does not uniquely determine one winner.

Return a frontier plus a declared fallback requirement.

#### Zero members
This should be impossible after admissibility for a finite non-empty candidate set; treat as internal error.

## Critical semantic point

The partial-order stage does **not** decide how much epistemic value is worth relative to attachment, obligation, incentive, effort, etc.

It only removes candidates that are no better on any comparable dimension and worse on at least one.

That is much weaker—and much more defensible—than a utility function.

## Missing family values

Three possible policies exist:

### STRICT_SHARED
Compare only when both candidates have every required family.

Missing required evidence -> incomparable.

### NEUTRAL_DEFAULT
Impute a declared neutral value.

Danger: UNKNOWN can collapse into zero/neutral.

Current disposition: reject as default.

### FAMILY_OPTIONAL
Only compare families present on both candidates.

Danger: a candidate can evade domination by omitting bad dimensions.

Current disposition: reject as default unless producer contracts guarantee complete family coverage.

Therefore the safest initial policy is:

```
STRICT_SHARED
```

for any family declared required for dominance.

## Policy-local family set

Not every registered family must participate in every policy.

Example:

```
research_completion_policy:
  comparable:
    epistemic_value: BENEFIT
    obligation_support: BENEFIT
    effort_cost: COST
  context_only:
    attachment
    play
```

Another policy can legitimately differ.

The decision receipt must identify the exact policy/version.

## What about obligations?

An admitted allocation obligation is not just another motive.

Two possible roles:

1. **hard scheduling constraint** at long-horizon controller;
2. **benefit family** representing how strongly a current candidate serves an admitted obligation.

Do not simply convert `minimum_nonprotective_share` into a reward bonus.

For initial cross-family selection, obligation pressure should probably be derived by the long-horizon controller and supplied as a typed policy input, not inferred from raw goal presence.

## What about feasibility?

Hard `INFEASIBLE` should remove a route before dominance.

`UNKNOWN` should not become zero.

`CONDITIONAL` needs explicit policy:
- treat as admissible but unresolved;
- or require inspection before ordinary selection.

Do not hide these states in a numeric family magnitude.

## What about effort?

Effort cost can participate as COST only if:
- units/normalization are defined;
- the comparison is current;
- the policy declares it comparable.

Required effort, effort cost, willingness, and vigor remain separate.

## What about protection?

Protection veto remains pre-dominance.

A high reward coalition cannot dominate away a hard protection rule.

## What about many-objective degeneration?

Pareto dominance becomes less discriminating as the number of objectives grows; many candidates become non-dominated.

That is relevant to MESO.

Therefore:
- keep the comparable family set small and policy-specific;
- do not expose every profile-local feature as a global criterion;
- use semantic-family normalization first;
- let context-only dimensions remain explanatory rather than comparative.

The goal is not “Pareto all the things.”

## What about a single final action?

Execution systems eventually need one action.

MESO has three defensible options when the frontier has multiple members:

### Fallback A — explicit unresolved
Return:
```
status = INCOMPARABLE
frontier = (...)
```

Host decides what to do.

### Fallback B — explicit secondary policy
A separate named policy chooses among frontier members.

Examples:
- deadline-first;
- epistemic-first;
- least-effort;
- randomized-safe exploration;
- stable deterministic order.

The receipt records both policies.

### Fallback C — allocation across frontier
For some non-immediate contexts, allocate time/resources among frontier members.

This belongs more naturally to the long-horizon controller than one-step target selection.

Initial disposition:
- core partial-order selector should support A;
- B may be implemented only as an explicit pluggable fallback;
- C remains future allocation work.

## Deterministic fallback is still policy

A lexicographic family order can be a valid fallback when explicitly chosen.

It must not be presented as evidence-derived.

This rehabilitates fixed precedence as a **named policy choice**, not universal motivational truth.

## Candidate result shape

Research sketch:

```
PartialOrderSelectionResult:
    status:
      SELECTED
      INCOMPARABLE
      NO_ADMISSIBLE_CANDIDATE

    selected_target_id?
    frontier_target_ids
    dominated_target_ids
    policy_id
    policy_revision
    fallback_policy_id?
    evidence/family snapshot or digest
```

No execution authority.

## Required proof cases

### PO-01 — obvious dominance
A is >= B on all benefit families and <= B on all cost families, strictly better on at least one.
Expected: A selected as unique non-dominated target.

### PO-02 — genuine tradeoff
A higher epistemic, B lower effort.
Expected: both remain frontier; no implicit winner.

### PO-03 — categorical V2 discontinuity removed
A weak motivational-only candidate vs B strong epistemic-only candidate.
Under a policy requiring both families:
Expected: incomparable unless fallback explicitly orders them.

### PO-04 — missing required family
A lacks effort evidence; B has it.
Expected: no zero imputation; comparison unresolved.

### PO-05 — infeasible target
A dominates numerically but is INFEASIBLE.
Expected: A removed before Pareto comparison.

### PO-06 — hard protection veto
A has stronger ordinary families but violates hard protection.
Expected: A inadmissible.

### PO-07 — dimension stuffing
Ten aliases already normalized into one family view.
Expected: selector sees one family magnitude, not ten votes.

### PO-08 — policy disagreement
Same frontier, two different explicit fallbacks.
Expected: final selection may differ; evidence/frontier remains identical.

### PO-09 — context-only family
A differs from B only on a CONTEXT_ONLY family.
Expected: context does not establish dominance.

### PO-10 — cost direction
A has lower effort cost and equal benefits.
Expected: A dominates B.

### PO-11 — equal vector
A and B equal on all comparable families.
Expected: both frontier; equality does not invent a winner.

### PO-12 — empty/invalid input
No admissible candidates.
Expected: explicit `NO_ADMISSIBLE_CANDIDATE`, not exception-as-policy.

## Hostile review

> **HOSTILE REVIEWER:** Pareto dominance punts the hard decision to the caller and will often return several winners.

**ACCEPTED.** That is the point when evidence does not justify a total order. A separate explicit fallback policy is more honest than hidden scalarization.

> **HOSTILE REVIEWER:** This can become useless in many dimensions because nearly everything is non-dominated.

**ACCEPTED.** Keep the global comparable family set intentionally small. Domain-local features stay inside profiles or context-only unless they earn cross-domain comparison semantics.

> **HOSTILE REVIEWER:** Policy-declared benefit/cost direction is already normative weighting in disguise.

**REJECTED.** Direction says only whether more or less of the *same family* is locally preferred. It does not specify how one family trades against another.

> **HOSTILE REVIEWER:** Missing-value strictness can make selection indecisive.

**ACCEPTED.** The alternative is silently fabricating evidence. A fallback may choose under uncertainty, but it must be explicit about doing so.

> **HOSTILE REVIEWER:** If a fallback is always needed, Pareto is ceremonial overhead.

**UNRESOLVED.** This is empirical. The implementation should instrument how often unique dominance occurs in adversarial/reference cases before adopting it as the default live policy.

## Current conclusion

The strongest minimal replacement candidate for global weighted utility or fixed universal precedence is:

```
hard admissibility
-> policy-scoped comparable family vector
-> strict Pareto dominance
-> non-dominated frontier
-> explicit fallback only when needed
```

This policy does not solve value pluralism.

It makes the unresolved tradeoff visible instead of hiding it.
