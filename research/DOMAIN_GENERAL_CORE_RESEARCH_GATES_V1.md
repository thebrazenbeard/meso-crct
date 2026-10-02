# MESO-CRCT Domain-General Core Research Gates V1

Date: 2026-10-02
Status: `PRE_ARCHITECTURE_GATE / RESEARCH_ONLY`

Architecture work on the next MESO core revision should remain blocked until these questions have explicit decisions.

## Gate 1 — Core/profile boundary

For every proposed state variable:
- identify at least two unrelated domains that need it;
- show that its semantics remain stable;
- provide a counterexample demonstrating why an existing field cannot represent it;
- otherwise keep it domain-specific.

## Gate 2 — Effort

Resolve:
- effort cost;
- willingness to exert effort;
- action vigor;
- fatigue/resource availability.

Required non-equivalences:
```
high effort != low value
high effort != low willingness
high willingness != high pleasure
low vigor != low desire
```

## Gate 3 — Delay and temporal valuation

Resolve:
- outcome delay;
- deadline;
- temporal discounting;
- anticipation;
- persistence.

Do not assume one exponential discount function is canonical.

## Gate 4 — Feasibility / expectancy

Define how a system represents:
- probability of obtaining an outcome;
- confidence in that estimate;
- current feasibility;
- source/currentness.

Hard boundary:
```
desirable != feasible
expected != true
low feasibility != low desire
```

## Gate 5 — Allostasis/resource budgeting

Decide:
- whether predictive future need is core state;
- how actual machine resources are sourced;
- how uncertainty is represented;
- how current deficit differs from predicted demand.

No biological parameter copying.

## Gate 6 — Vigor / activation

Determine whether action vigor is:
- core state;
- derived from effort/value/resource state;
- host-policy output.

It must remain distinct from direction and authorization.

## Gate 7 — Anticipation

Find a counterexample proving whether anticipation requires a new state family or can be represented by:
```
expectancy + incentive salience + delay + learned association
```

Do not add redundant state.

## Gate 8 — Habit

Research:
- action chunks;
- outcome devaluation;
- habit persistence;
- interaction with current desire;
- interruptibility.

Required adversarial case:
- habit remains strong after outcome value drops, while current desire stays low.

## Gate 9 — Cross-domain arbitration

The current fixed precedence must be challenged.

Compare:
- lexicographic;
- constrained;
- Pareto/non-dominance;
- evidence/coalition;
- hybrid approaches.

Required cases include:
- weak motivational vs strong epistemic;
- strong sexuality vs urgent resource constraint;
- caregiving obligation vs achievement reward;
- attachment vs transient social reward;
- protection vs all positive motives.

## Gate 10 — Priority calibration

Current `priority: float` must have a semantic contract.

Questions:
- is 0.8 epistemic priority commensurable with 0.8 incentive priority?
- is priority merely within-mode?
- who calibrates it?
- can a domain author it directly?

If values are not commensurable, cross-mode numeric comparison is invalid.

## Gate 11 — Domain contribution interface

Define what a domain profile may emit.

Candidate principle:
- profile emits typed evidence and state;
- core computes/adjudicates selection;
- profile does not emit an opaque final utility/priority.

No schema yet.

## Gate 12 — Co-active domains

Support events such as:
```
sexuality + attachment
curiosity + achievement
caregiving + protection
play + affiliation
resource need + any other motive
```

Avoid forced single-domain classification.

## Gate 13 — Constraints vs preferences

Classify each rule as:
- hard admissibility constraint;
- obligation;
- preference;
- motivational evidence;
- learned tendency;
- external authority.

Do not allow safety/authority constraints to become tradeable reward terms.

## Gate 14 — Intrinsic motivation

Resolve whether MESO needs:
- one intrinsic-motivation abstraction;
- only typed domains such as epistemic/mastery/play;
- or both.

Current evidence does not justify one naked `intrinsic_reward`.

## Gate 15 — Social motivation

Before a social profile exists, keep distinct:
- social reward;
- affiliation;
- attachment;
- caregiving;
- status/dominance;
- cooperation;
- approval/reputation;
- play;
- sexuality.

A generic social scalar fails the gate.

## Gate 16 — Machine substrate grounding

Every machine “drive” must identify:
- actual measured state;
- source;
- update mechanism;
- persistence/currentness;
- causal role;
- reset/expiry.

No metaphor-only drives.

## Gate 17 — Learning semantics

Decide what each signal may teach.

Examples:
- effort experience can update cost estimates;
- pleasure can participate in teaching but cannot directly write identity;
- information gain can update exploration policy;
- social reward can update actor associations;
- domain reward cannot create consent.

## Gate 18 — Anti-capture across domains

Extend existing allocation tests to:
- curiosity loops;
- achievement obsession;
- status capture;
- affiliation/approval seeking;
- sexuality;
- self-stimulation of resource or reward signals.

The anti-addiction architecture must be domain-general.

## Gate 19 — Learned-policy integration

Research whether:
- MESO remains deterministic/reference only;
- a learned policy consumes MESO state;
- learned appraisal modules can produce typed MESO inputs;
- or parts of arbitration become learned.

Any learned component must preserve testable invariants and provenance/currentness.

## Gate 20 — Minimality

Every proposed new core type must answer:
> What failure occurs without this field?

If no distinct failure can be demonstrated, do not add it.

## Go/no-go

Architecture design can begin after Gates 1–13 have explicit research decisions and a test matrix.

Implementation remains blocked until:
- architecture survives hostile review;
- red tests are specified first;
- current sexuality work is shown not to distort the generic core.
