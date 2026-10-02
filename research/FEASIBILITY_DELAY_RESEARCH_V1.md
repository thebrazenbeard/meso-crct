# MESO-CRCT Feasibility, Expectancy, and Delay Research V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / STRONG-CORE-CANDIDATE REFINEMENT / NO_IMPLEMENTATION`

## Purpose

MESO currently represents target significance and learned value but not whether a desired outcome is realistically attainable, how long it will take, or how those estimates change over a pursuit.

Those omissions matter across:
- sexuality;
- curiosity;
- achievement;
- caregiving;
- resource regulation;
- affiliation;
- status;
- protection.

## 1. Desirability and attainability must be separate

A target can be:
- highly desirable and highly feasible;
- highly desirable and currently infeasible;
- weakly desirable but easy;
- undesirable but unavoidable/obligatory.

Therefore:

```
desirability != feasibility
value != probability_of_success
motivation != capability
```

Classical expectancy-value theories and contemporary future-reward research repeatedly separate value/desirability from expectancy/feasibility.

MESO should preserve the same distinction functionally without copying one psychological theory wholesale.

## 2. Feasibility is not truth

A feasibility estimate is an estimate.

It should carry:
- source;
- evidence;
- confidence/uncertainty;
- observed-at/currentness;
- scope;
- assumptions.

Hard boundary:

```
high_feasibility != guaranteed_success
low_feasibility != impossible
unknown_feasibility != zero
```

This aligns with MESO's broader source/currentness discipline.

## 3. Controllability is related but distinct

Feasibility asks:
> Can this target/outcome be achieved?

Controllability asks:
> Can this actor's action materially affect the outcome?

Examples:
- a favorable outcome may be likely but uncontrollable;
- a difficult outcome may be low-probability but strongly controllable;
- an aversive event may be unavoidable but its consequences mitigable.

This distinction matters especially for:
- threat;
- avoidance;
- frustration;
- goal persistence.

Candidate non-equivalence:

```
feasibility != controllability
```

## 4. Delay is an independent cost/context dimension

A desired outcome can be:
- immediate;
- delayed;
- available only after a sequence;
- subject to a deadline;
- available at an uncertain time.

Delay does not merely lower value in one universal way.

Human delay discounting often departs from simple exponential consistency; preferences can change as outcomes approach.

MESO should not canonize:
```
discounted_value = value * exp(-k * delay)
```

or any other one-function rule as universally correct.

## 5. Delay of reward and delay of effort are different

Future-reward research shows that the timing of **effort** can affect decisions separately from the timing of reward.

Potential state:

```
reward_delay
effort_onset_delay
expected_duration
deadline
```

may matter independently.

A future action can have:
- delayed reward;
- immediate effort;
or:
- immediate reward;
- delayed future cost.

Those are not equivalent plans.

## 6. Temporary preference and dynamic inconsistency

A long-horizon goal can be preferred at T0 but lose to a smaller/easier/immediate option at T1 as delays and costs change.

This is not necessarily a corruption of stored preference.

Possible causes:
- changing current state;
- changing opportunity set;
- nonlinear temporal valuation;
- changed resource cost;
- changed feasibility;
- new evidence.

### MESO consequence

Do not rewrite durable preference merely because local current selection changes.

```
current choice != permanent preference revision
```

This fits MESO's existing separation of transient activation from durable association.

## 7. Progress tracking should be separate from target desirability

Future-goal pursuit requires representing:
- selected goal;
- plan/route;
- current step;
- progress;
- remaining effort/delay;
- changed feasibility.

MESO does not need to become a planner, but it may need to consume plan-state evidence.

Likely interface:

```
PLAN/GOAL PROVIDER
    -> progress / remaining cost / feasibility evidence
    -> MESO appraisal
```

MESO should not own all task planning.

## 8. Failure can update different things

A failed attempt can mean:
- target is impossible;
- selected strategy was poor;
- more effort is required;
- external state changed;
- random failure occurred;
- estimate was wrong;
- target is still valuable.

Therefore one negative prediction error must not automatically:
- lower target desirability;
- lower self-efficacy/feasibility;
- create learned avoidance.

Teaching needs proposition-specific targets.

Potential learning subjects:
```
target_value_association
strategy_success_probability
resource_cost_estimate
time_estimate
hazard_estimate
cue_outcome_association
```

## 9. Delay and opportunity cost

Waiting for one target can exclude other targets.

Delay therefore affects:
- target availability;
- opportunity cost;
- allocation;
- persistence.

But:
```
long_delay != low_value
```

A target can remain deeply valued while deprioritized locally.

## 10. Deadlines are not just negative delay

A deadline changes feasibility over time.

Example:
```
target value = constant
time remaining -> decreases
required effort -> constant
feasibility -> eventually collapses
```

Deadline pressure may increase effort before the task becomes impossible.

This couples:
- time;
- effort;
- feasibility;
- vigor.

## 11. Uncertainty about timing or success is separate from low expectation

A target can have:
- expected probability 0.5 with high confidence;
- expected probability 0.5 with huge uncertainty.

Those states can support different behavior:
- act;
- inspect;
- gather information;
- hedge;
- delay commitment.

Candidate distinction:

```
expected_probability != uncertainty
```

MESO's epistemic system may consume uncertainty rather than feasibility silently absorbing it.

## 12. Potential threat is a useful counterexample

A low-probability threat can still demand vigilance because:
- severity may be high;
- uncertainty may be high;
- controllability may be low;
- cost of missing it may be enormous.

Thus:
```
probability alone != protective priority
```

This again argues for typed threat geometry.

## 13. Sexuality example

A sexual motive can be high while:
- partner unavailable;
- context inappropriate;
- action infeasible;
- consent unknown/declined.

The motive need not vanish.

```
desire persists
while
feasible authorized action = none
```

This is why feasibility/authorization should not be multiplied into sexual activation itself.

## 14. Caregiving example

A desired care outcome can be low-feasibility but still obligation-relevant.

MESO should be able to:
- preserve importance;
- surface low feasibility;
- encourage strategy/information search if policy supports it;
without pretending value is low.

## 15. Candidate architecture — research sketch

Potential evidence types:

```
OutcomeExpectancy:
    target
    probability_or_range
    uncertainty
    source
    observed_at
    expiry/supersession

FeasibilityAssessment:
    target
    actor/capability scope
    feasible_state = FEASIBLE | INFEASIBLE | UNKNOWN | CONDITIONAL
    constraints
    source/currentness

TemporalCost:
    target
    reward_delay
    effort_onset_delay
    expected_duration
    deadline
    uncertainty
```

Do not implement these exact classes yet.

## 16. Required adversarial cases

### FD-01 — valuable but infeasible
Preserve value while blocking impossible action route.

### FD-02 — unknown feasibility
Do not convert UNKNOWN to zero or true.

### FD-03 — likely but uncontrollable
Outcome probability high; agent influence low.

### FD-04 — controllable but unlikely
Low base probability; action materially improves it.

### FD-05 — delayed high-value target
Delay affects current allocation without rewriting durable value.

### FD-06 — temporary preference
Immediate lower-value option temporarily wins without durable preference mutation.

### FD-07 — deadline
Vigor/effort can rise as remaining time falls, then action becomes infeasible after deadline.

### FD-08 — failed strategy
Failure updates strategy expectancy but leaves target value intact.

### FD-09 — threat
Low probability + high severity/uncertainty can still justify vigilance.

### FD-10 — authority
Feasible and desirable protected effect remains non-executable without authority.

## Candidate dispositions

### Outcome expectancy
Status: `STRONG_CORE_APPRAISAL_CANDIDATE`

### Feasibility
Status: `STRONG_CORE_APPRAISAL_CANDIDATE`

### Controllability
Status: `STRONG_CORE_RESEARCH_CANDIDATE`

May be essential for aversive/effort domains.

### Reward/effort delay
Status: `STRONG_CORE_APPRAISAL_CANDIDATE`

### Deadline/progress
Status: `EXTERNAL_PLAN_STATE / APPRAISAL_INPUT`

MESO should consume rather than own detailed planning.

### Temporal discount function
Status: `POLICY / DERIVED; NO UNIVERSAL DEFAULT YET`

### Temporary preference
Status: `DERIVED PHENOMENON, NOT A STATE PRIMITIVE`

## Hostile review

> **HOSTILE REVIEWER:** Feasibility and expectancy belong in a planner, not motivation.

**PARTIALLY ACCEPTED.** The planner or capability system should own the evidence. MESO still needs access to it because willingness, effort and selection depend on whether outcomes/actions appear attainable.

> **HOSTILE REVIEWER:** Delay is just another cost. One scalar cost field would be simpler.

**REJECTED FOR NOW.** Delay interacts with preference over time, deadlines and effort timing in ways that a generic cost scalar can hide. A local declared policy may later scalarize it, but source state should preserve temporal semantics.

> **HOSTILE REVIEWER:** Tracking temporary preferences risks anthropomorphizing a machine.

**REJECTED.** The functional phenomenon is simply time-dependent local choice without necessarily rewriting durable stored preference. No human feeling claim is required.

## Current conclusion

MESO likely needs explicit access to:

```
expectancy
feasibility
controllability
delay
deadline/progress evidence
```

but most of those facts should be externally produced and provenance-bound.

The core should use them for appraisal/effort/arbitration without becoming the planner or capability authority.

No implementation is proposed here.
