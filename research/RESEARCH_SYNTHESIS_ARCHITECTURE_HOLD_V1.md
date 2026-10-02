# MESO-CRCT Research Synthesis and Architecture Hold V1

Date: 2026-10-02
Status: `RESEARCH_SYNTHESIS / ARCHITECTURE_HOLD / NO_IMPLEMENTATION`

## Purpose

This document consolidates the current research branch into four buckets:

1. settled semantic boundaries;
2. strong architecture candidates;
3. unresolved research questions;
4. explicit blockers to implementation.

It is intentionally not an architecture specification.

## A. Settled boundaries

The following conclusions have survived the current literature review, exact-source audit, machine-side comparison and hostile review strongly enough to treat them as design constraints.

### A1. MESO remains domain-general

MESO-CRCT is a general motivational/reward/salience/learning/control substrate.

Sexuality is one domain profile.
Curiosity, achievement, affiliation, attachment, caregiving, status, resource regulation and play are comparative domains, not MESO's identity.

### A2. Domain profiles do not own common truth or authority

Profiles may contribute typed domain appraisal.

They must not author:
- factual truth;
- identity;
- relationship truth;
- consent;
- protected-effect authority;
- autobiographical memory admission;
- external-effect success;
- permanent preference;
- phenomenology.

### A3. Motivation remains typed

Preserve at least:

```
wanting != liking
attention != desire
meaningful != pleasurable
reward != truth
salient != authorized
current activation != durable learning
target priority != action direction
intent != execution
```

### A4. Protection does not require suffering

Strong hazard/avoidance/protection must remain possible while hedonic valence stays within the welfare bound.

Aversive learning cannot rely on making hedonic suffering deeper.

### A5. Negative reinforcement is not punishment

Outcome valence and behavioral learning direction are independent.

### A6. Current choice does not rewrite durable preference

Local selection can change due to:
- feasibility;
- delay;
- resource state;
- effort;
- opportunity set;
- obligation;
- protection;
- temporary activation

without implying durable preference changed.

### A7. Target, goal, plan, action, motive and obligation are distinct

Current V2 may use shorthand identities in tests.
The expanded architecture must not.

### A8. Habit is not present desire

Repeated/cached action cannot establish current goal, conation or preference.

Current research places habit/action chunks outside MESO core unless later evidence requires a tighter interface.

### A9. Anticipation does not currently justify a primitive scalar

Treat anticipation as a derived future-outcome appraisal until a counterexample proves independent state is necessary.

### A10. Global readiness, MESO recruitment, domain arousal and action vigor are distinct

Do not introduce one generic `arousal` variable.

## B. Strong architecture candidates

These have enough cross-domain evidence to justify architecture design work once arbitration is resolved.

### B1. Effort decomposition

Likely minimum distinction:

```
required resources/effort
-> context-dependent effort cost
-> willingness to exert
-> post-selection vigor proposal
```

### B2. Feasibility / expectancy / controllability

MESO likely needs provenance-bound access to:
- outcome expectancy;
- feasibility;
- uncertainty;
- controllability;
- delay;
- deadlines/progress evidence.

Most source truth should remain external.

### B3. Predictive resource regulation

External resource telemetry/forecast should inform:
- feasibility;
- effort;
- allocation;
- vigor constraints.

Do not turn telemetry into desire or one resource-health scalar.

### B4. Richer aversive semantics

Likely research-supported additions at appraisal/event level:
- threat probability/imminence/severity/uncertainty/controllability;
- appetitive vs aversive vs omitted/blocked/lost outcome class;
- active vs passive/preventive avoidance distinctions where behavior requires them.

Do not add human emotion labels merely because literature uses them.

### B5. Domain contribution interface

Profiles should emit provenance-bound typed contributions rather than final priority.

One target may receive multiple domain contributions.
One domain may emit multiple distinct contributions.

### B6. Multi-goal allocation

Long-horizon health likely needs more than target-ID concentration.

Research candidates:
- goal allocation;
- domain/motive allocation;
- resource allocation.

Only add dimensions that have trustworthy producers and demonstrated capture cases.

## C. Unresolved architecture questions

### C1. Cross-domain arbitration

This is the primary blocker.

Current V2 fixed precedence:

```
PROTECTIVE
then
MOTIVATIONAL > EPISTEMIC > ORIENTING
```

is transparent but not justified as the final general policy.

Current research direction to test:

```
hard admissibility/constraints
+ typed contributions
+ obligation/resource state
+ non-dominance where valid
+ declared selection policy
```

No final algorithm selected.

### C2. Priority calibration

A bounded `0..1` value does not prove commensurability across kinds/domains.

Need a semantic contract before cross-domain numeric comparison.

### C3. Teaching signal semantics

Current signed `prediction_error` is under-typed.

Need to determine whether persistent learning requires explicit outcome class:
- better/worse reward;
- aversive event;
- avoided aversive event;
- omission;
- loss;
- blocked goal;
- other.

### C4. Habit boundary

Current preference:
- habit memory/action chunks external;
- MESO consumes current habit proposal/conflict evidence.

Still needs runtime-use-case validation.

### C5. Threat/action vocabulary

Current `protective_withdraw` may be too coarse.

Possible distinctions:
- escape;
- prevent;
- inhibit;
- risk-assess;
- learned avoid.

Only add if host behavior differs materially.

### C6. Learning aggregation

Current recall uses strongest support per direction rather than summing.

Need evidence before permitting independent convergent association aggregation.

### C7. Time dynamics

Current family-wide half-lives are intentionally simple.

No reason yet to proliferate per-signal decay constants without failing domain tests.

### C8. Learned-policy integration

Open options:
- MESO stays deterministic reference layer;
- learned appraisal produces typed inputs;
- learned policy consumes MESO state;
- some arbitration becomes learned under hard invariants.

No decision yet.

## D. Explicit blockers to implementation

No next-generation core implementation should begin until these are resolved enough to write red tests first:

1. cross-domain arbitration policy;
2. priority/calibration semantics;
3. effort/vigor interface;
4. feasibility/delay/controllability interface;
5. predictive resource-provider/currentness contract;
6. aversive outcome/teaching semantics;
7. goal/target/domain/obligation reference model;
8. domain-profile contribution contract;
9. required provenance/currentness for non-semantic numeric producers;
10. minimal exact adversarial test matrix.

Sexuality architecture has an additional dependency:
- it should not reimplement sexual-only versions of generic effort, feasibility, resource, aversive or arbitration mechanisms.

## E. Current source disposition

MESO main at the research cut remains a coherent V2 reference implementation.

The newly identified gaps are **not retroactive bugs** unless current V2 claims to solve those broader problems.

The research expands the mission.

Therefore:

```
CURRENT_V2 = VALID_REFERENCE_WITH_EXPLICIT_CEILING
NEXT_CORE = RESEARCH_BLOCKED
SEXUALITY_PROFILE = RESEARCH_BLOCKED_ON_CORE
IMPLEMENTATION = NOT_STARTED
```

## F. Proposed next research sequence

### F1 — Arbitration proof cases

Build a specification-only adversarial table showing how candidate arbitration families behave on the same cases:
- weak motivational vs maximal epistemic;
- protection vs reward;
- obligation vs pleasure;
- multi-domain coalition;
- unknown feasibility;
- severe resource pressure;
- mixed appetitive/aversive target.

No code.

### F2 — Producer/currentness contract

Define what a trusted appraisal producer must prove:
- subject;
- source;
- revision;
- observation time/currentness;
- confidence/uncertainty;
- proposition type;
- expiry/supersession.

Reuse existing provenance machinery conceptually.

### F3 — Minimal core delta

After F1/F2, identify the smallest set of new abstractions required.

The target should be fewer new types than the research vocabulary.

### F4 — Red-test specification

Write the test contract before implementation.

### F5 — Only then design implementation

No coding before hostile review of the minimal delta.

## Hostile review

> **HOSTILE REVIEWER:** The research has become larger than the implementation and risks analysis paralysis.

**ACCEPTED AS A PROCESS RISK.** The next phase should compress, not expand. New research should be admitted only if it changes a blocker, invalidates a candidate, or supplies a missing adversarial case.

> **HOSTILE REVIEWER:** The architecture hold is artificial; effort/feasibility/resource types could be implemented now independently.

**PARTIALLY ACCEPTED.** They could be implemented locally, but their interface and role depend on arbitration and producer/currentness semantics. Premature code would likely create another migration.

> **HOSTILE REVIEWER:** A typed motivational system may still eventually require a scalar choice function.

**ACCEPTED.** The prohibition is against hidden/unjustified universal scalarization. A declared local policy may scalarize compatible dimensions after hard constraints and semantic provenance are preserved.

## Current conclusion

The research phase has reached a useful compression point.

The next useful work is **not more taxonomy**.

It is to prove the arbitration and producer interfaces against concrete adversarial cases, identify the minimum core delta, specify red tests, and only then consider implementation.
