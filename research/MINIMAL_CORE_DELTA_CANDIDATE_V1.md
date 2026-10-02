# MESO-CRCT Minimal Core Delta Candidate V1

Date: 2026-10-02
Status: `RESEARCH_CANDIDATE / PRE-IMPLEMENTATION / NO CODE`
Exact research base: `main@060d0feeb9dc9eb23801082bd8f1c4a7cb06184d`

## Purpose

The research corpus intentionally explored more concepts than should become runtime types.

This document compresses the work into the **smallest candidate delta** that appears capable of passing the current cross-domain proof cases without turning MESO into a general cognitive architecture.

It is not an implementation plan.

## Preserve from V2

Unless a red test proves otherwise, keep:
- `RewardState` with bounded pleasure plus independent hazard/avoidance;
- typed `SalienceState`;
- `LearningState`;
- `RecruitmentState`;
- `HomeostaticState`;
- exact event identity;
- provenance verification and transition receipts;
- bounded plasticity;
- versioned association memory;
- cue-bound recall;
- review/quarantine;
- non-executable intent;
- separation of local selection from long-horizon allocation health.

The next core should extend these invariants rather than replace them wholesale.

## Delta 1 — verified appraisal evidence

### Problem

Current appraisal accepts several consequential values as caller-authored floats. Type/range validation does not establish proposition, source, scope, currentness or uncertainty.

### Candidate minimum

A common evidence header conceptually needs:

```
proposition_kind
subject_or_target_ref
producer_id
producer_revision
source/evidence_ref
currentness
value
uncertainty?
```

Do not force every datum into one universal generic object if typed payloads are cleaner.

### Why it earns core status

The same trust problem recurs across:
- resource telemetry;
- feasibility;
- threat estimates;
- domain-profile contributions;
- learned/derived appraisal;
- plan-state inputs.

Without this, the next architecture merely adds more caller-authored numbers.

## Delta 2 — outcome feasibility appraisal

### Problem

Current MESO cannot cleanly represent:
- highly desired but infeasible;
- likely but uncontrollable;
- unknown feasibility;
- delayed outcome;
- failure of one route without devaluing the goal.

### Candidate minimum

Start with the smallest semantics that satisfy proof cases:

```
feasibility:
  FEASIBLE | INFEASIBLE | UNKNOWN | CONDITIONAL

expected_success:
  optional bounded estimate + uncertainty

controllability:
  optional bounded estimate + uncertainty

delay:
  optional duration/temporal relation
```

Keep detailed plan/deadline/progress state external until a red test requires more.

### Boundary

```
desirability != feasibility
expected != true
unknown != zero
failed_plan != devalued_goal
```

## Delta 3 — effort assessment

### Problem

Current source has no explicit representation of effort/resource cost.

### Minimal split

Do not introduce one `effort` scalar.

Research minimum:

```
required_resource_evidence
-> context-dependent effort_cost
-> willingness_to_exert
-> optional post-selection vigor proposal
```

The first implementation candidate should likely persist only what must be compared or explained; derived values should remain derived when possible.

### Boundary

```
required_effort != effort_cost
effort_cost != willingness
willingness != vigor
vigor != authority
```

## Delta 4 — typed outcome / teaching semantics

### Problem

Current `prediction_error: float` has sign and magnitude but not enough causal meaning for richer learning.

A negative discrepancy can reflect:
- lower-than-expected reward;
- punishment;
- aversive outcome;
- reward omission;
- blocked expected reward;
- loss;
- failed strategy.

Those should not necessarily update the same association in the same way.

### Candidate minimum

Add an outcome/teaching class at the event or learning-proposal boundary rather than exploding `LearningState`.

Research sketch:

```
OutcomeClass:
  APPETITIVE
  AVERSIVE
  OMISSION
  BLOCKED
  LOSS
  AVOIDED_AVERSIVE
  OTHER
```

The exact enum is not frozen.

### Boundary

```
negative_reinforcement != punishment
negative_prediction_error != learned_avoidance
reward_omission != hazard
```

## Delta 5 — domain contribution envelope

### Problem

A first-class sexuality profile and later domains need to contribute local semantics without emitting final opaque priority.

### Candidate minimum

A profile contribution needs enough structure to preserve:

```
domain/profile identity + revision
target/referent
contribution kind
local magnitude/state
direction if applicable
source/currentness
```

A domain profile may emit several contributions for one target.
A target may receive contributions from several domains.

### Prohibition

A profile does not emit globally authoritative:

```
priority = 0.92
```

without a declared common policy explaining how that number is comparable.

## Delta 6 — explicit selection policy object

### Problem

Current fixed precedence is transparent but too rigid as the final domain-general rule.

### Candidate minimum

Separate evidence from policy.

A selection policy should explicitly define:
- hard admissibility/protection handling;
- treatment of UNKNOWN;
- any comparable dimensions;
- coalition aggregation/caps;
- tie/fallback rule;
- obligation treatment;
- policy provenance/version.

### Important

This does **not** require one universal policy.

The same evidence may yield different legitimate choices under two declared policies.

That is preferable to hiding policy in field names or normalization constants.

## Delta 7 — goal/target reference separation

### Problem

Current allocation tests use a practical V2 shorthand in which a goal ID can equal a selected target ID.

That fails for:
- one goal, many targets/actions;
- one target serving multiple goals;
- temporary shelving;
- failed plan with intact goal;
- domain/motive coalition.

### Candidate minimum

Do not import a planner into MESO.

MESO likely needs only references:

```
TargetRef
GoalRef?
PlanRef?
```

with the goal/plan owner external.

The first implementation may need only `target_id` plus optional `goal_refs` and source/currentness.

## Delta 8 — long-horizon contribution accounting

### Problem

Current target concentration can be evaded by rotating target IDs within one motive/domain.

### Candidate minimum

Do **not** add every possible allocation axis.

Add domain/goal allocation accounting only if trustworthy contribution/goal refs exist and a red test proves target-only auditing fails.

This delta is conditional on the red-test contract.

## Explicit non-deltas

Do **not** currently add core primitives for:

### Anticipation
Derived until proven otherwise from:
```
future outcome + expectancy + delay + predicted value + cue/association + incentive effect
```

### Habit
Keep outside MESO core as an action-policy/cached-routine proposal unless runtime evidence proves otherwise.

### Global arousal
Keep host/runtime readiness separate from:
- recruitment activation;
- action vigor;
- domain-specific arousal.

### Sexual excitation/inhibition
Remain sexuality-profile semantics.

### Relationship/attachment truth
Remain externally owned.

### Consent/authorization
Remain external authority state.

### Phenomenology
Outside current claim ceiling.

## Proposed minimal flow

Research candidate:

```
CURRENT EXTERNAL EVIDENCE
    ->
VERIFIED APPRAISAL DATA
    ->
CORE + DOMAIN APPRAISAL
    ->
HARD ADMISSIBILITY / PROTECTION
    ->
OUTCOME + EFFORT + RESOURCE CONTEXT
    ->
TYPED DOMAIN CONTRIBUTIONS
    ->
DECLARED SELECTION POLICY
    ->
ACTION TENDENCY
    ->
NON-EXECUTABLE INTENT
```

Persistent learning branches from verified event/outcome evidence and remains receipt-bound.

## Smallest likely source-surface change

If the red tests support this compression, the next code revision should try to touch as few conceptual surfaces as possible:

1. appraisal/evidence types;
2. selection policy and decision receipt;
3. learning outcome semantics;
4. optional goal/domain contribution references;
5. allocation audit only where proof cases demand it.

Avoid broad rewrites of:
- memory;
- event identity;
- review;
- intent;
- homeostasis;
- runtime phases

unless a test demonstrates a dependency.

## Migration compatibility

Existing V2 construction paths should remain usable for simple/reference cases where:
- evidence is locally trusted test stimulation;
- no domain contribution is needed;
- no cross-domain feasibility/effort comparison is required.

A compatibility layer may translate legacy V2 fields into explicitly `TEST_STIMULATION` or reference-local evidence.

Do not silently treat legacy raw values as production-trusted.

## Hostile review

> **HOSTILE REVIEWER:** Seven deltas is not "minimal."

**PARTIALLY ACCEPTED.** Several are interfaces, not new persistent state families. The red tests should try to collapse them further. In particular, goal references, domain contributions and verified appraisal data may share one envelope.

> **HOSTILE REVIEWER:** A typed selection policy plus typed evidence is just a verbose utility function.

**REJECTED AS A NECESSARY CONCLUSION.** It can degenerate into one. The distinction survives only if hard non-fungible constraints remain outside tradeoff, UNKNOWN stays representable, and policy provenance is explicit. The red tests are designed to catch disguised scalarization.

> **HOSTILE REVIEWER:** Outcome class belongs in domain profiles, not core learning.

**PARTIALLY ACCEPTED.** The exact semantic vocabulary may be producer-specific. What core learning needs is enough typed outcome provenance to avoid treating every negative prediction error identically.

> **HOSTILE REVIEWER:** Goal references are task-management creep.

**ACCEPTED AS A RISK.** The minimum implementation should use opaque external refs only; MESO must not own plan graphs, completion state or task scheduling.

## Current disposition

The smallest credible next-core hypothesis is:

```
verified evidence
+ feasibility/effort context
+ typed outcome semantics
+ typed domain contributions
+ explicit policy
```

with existing V2 state, provenance, memory and intent boundaries preserved.

Implementation remains blocked until the red-test contract is accepted and the delta survives it.
