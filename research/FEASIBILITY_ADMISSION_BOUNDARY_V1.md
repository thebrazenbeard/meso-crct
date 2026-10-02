# MESO Feasibility Admission Boundary V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / BOUNDARY SETTLED ENOUGH FOR RED TESTS`

## Purpose

The partial-order selector in Draft PR #13 intentionally assumes hard admissibility happened upstream.

This document defines the smallest feasibility gate needed before ordinary cross-family comparison.

## Core rule

Feasibility is not desirability.

```
high desire + infeasible route
```

must preserve the desire while excluding the route from ordinary selection.

Likewise:

```
UNKNOWN feasibility
```

must not become:
- zero value;
- false;
- infeasible;
- high effort;
- low desire.

## State disposition

### FEASIBLE
A CURRENT assessment may admit the target to ordinary comparison.

### INFEASIBLE
A CURRENT assessment excludes the target from ordinary comparison.

The target's motivational state remains untouched.

### UNKNOWN
Defer.

Do not select through ordinary comparison and do not classify as infeasible.

### CONDITIONAL
Defer until the condition is independently satisfied/resolved.

The current `FeasibilityAssessment` does not encode enough condition semantics to convert CONDITIONAL into FEASIBLE by itself.

## Currentness rule

If the feasibility assessment evidence is:
- STALE;
- UNKNOWN currentness;

the assessment state cannot be trusted as current.

Therefore the target is deferred rather than admitted or rejected.

Example:

```
old state = INFEASIBLE
evidence = STALE
```

does not prove:
```
currently infeasible
```

## Missing assessment

No assessment is not equivalent to FEASIBLE.

Initial conservative disposition:

```
missing assessment -> DEFER
```

A later policy may explicitly define domains where feasibility evidence is not required, but that must be a named policy choice.

## Subject binding

A feasibility assessment about target A must not be re-used as evidence for target B.

Required invariant:

```
assessment.target_id == assessment.evidence.subject_id
```

This is a provenance integrity rule, not a motivational rule.

## Gate output

Research candidate:

```
FeasibilityGateResult:
    admitted_target_ids
    deferred_target_ids
    infeasible_target_ids
    missing_assessment_target_ids
    gate_input_digest
```

The gate should be deterministic and order-stable.

## Integration with partial-order selection

Candidate pipeline:

```
candidate targets
+ current feasibility assessments
    ->
feasibility gate
    ->
FEASIBLE subset
    ->
partial-order family selector
```

If any target is DEFERRED, an otherwise unique Pareto winner is not yet a fully evidence-determined global winner because the deferred target could become admissible after refresh.

Therefore a feasibility-aware wrapper should surface a deferred/unresolved final status rather than silently selecting among only the known-feasible subset.

## Proposed wrapper status

```
SELECTED
INCOMPARABLE
DEFERRED
NO_ADMISSIBLE_CANDIDATE
```

### SELECTED
Only when:
- no deferred targets remain;
- at least one feasible target exists;
- partial-order comparison yields a unique winner.

### INCOMPARABLE
No deferred targets remain, but multiple non-dominated feasible targets remain.

### DEFERRED
At least one target has:
- UNKNOWN;
- CONDITIONAL;
- stale assessment;
- unknown-currentness assessment;
- missing assessment.

### NO_ADMISSIBLE_CANDIDATE
No deferred targets and no feasible target remain.

This can occur when all current assessed targets are INFEASIBLE.

## Infeasibility does not rewrite motive or learning

The gate must not:
- mutate `DomainContribution`;
- change `RewardState`;
- weaken learned association;
- alter `GoalObligation`;
- write memory.

It only controls whether a current route enters ordinary comparison.

## Required tests

### FG-01 — feasible admitted
CURRENT FEASIBLE target enters the admissible set.

### FG-02 — infeasible excluded
CURRENT INFEASIBLE target is excluded while its family evidence remains unchanged.

### FG-03 — unknown deferred
CURRENT UNKNOWN target is deferred.

### FG-04 — conditional deferred
CURRENT CONDITIONAL target is deferred.

### FG-05 — stale state deferred
STALE FEASIBLE or INFEASIBLE assessment is deferred.

### FG-06 — missing assessment deferred
No feasibility assessment produces DEFER, not FEASIBLE.

### FG-07 — subject mismatch rejected
Assessment evidence subject cannot differ from target ID.

### FG-08 — duplicate assessment rejected
Two assessments for the same target are invalid input.

### FG-09 — unique feasible + deferred other
Final wrapper status is DEFERRED, not SELECTED.

### FG-10 — all infeasible
Final wrapper status is NO_ADMISSIBLE_CANDIDATE.

### FG-11 — all resolved and Pareto unique
Wrapper returns SELECTED and preserves partial-order result identity.

### FG-12 — all resolved and Pareto tradeoff
Wrapper returns INCOMPARABLE.

### FG-13 — digest
Gate/result digest changes when feasibility state/evidence changes and is stable under input reordering.

## Hostile review

> **HOSTILE REVIEWER:** Deferring every missing or conditional feasibility state could make MESO unusably conservative.

**ACCEPTED AS A POLICY COST.** The first reference implementation should be conservative because it lacks enough semantics to distinguish benign missing evidence from materially unresolved feasibility. A future policy can relax this explicitly for bounded domains.

> **HOSTILE REVIEWER:** A stale INFEASIBLE assessment should probably still block dangerous actions.

**PARTIALLY ACCEPTED.** Feasibility is not protection. If the evidence represents a safety veto, it belongs in the protection/authority layer, which may use different stale-data rules. This gate only answers current route feasibility.

> **HOSTILE REVIEWER:** The wrapper duplicates the partial-order result.

**PARTIALLY ACCEPTED.** A wrapper is justified only if it preserves the reason selection is unresolved: deferred feasibility versus genuine cross-family incomparability. Those are different propositions and should not share one status.

## Conclusion

The smallest defensible feasibility admission rule is:

```
CURRENT FEASIBLE -> ADMIT
CURRENT INFEASIBLE -> EXCLUDE
UNKNOWN / CONDITIONAL / STALE / MISSING -> DEFER
```

with target-subject binding and no motivational mutation.
