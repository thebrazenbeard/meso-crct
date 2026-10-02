# MESO-CRCT Habit and Action-Policy Boundary Research V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / BOUNDARY REFINEMENT / NO_IMPLEMENTATION`

## Purpose

Habit is repeatedly identified in reward/motivation frameworks, including NIMH RDoC Positive Valence Systems.

But MESO is intended to be a motivational-control substrate, not a full action-policy runtime.

The core question is therefore:

> Does habit belong inside MESO, or should MESO expose motivational state to a separate action-policy system that can contain both goal-directed and habitual routes?

Current research favors the second answer unless executable counterexamples later require deeper integration.

## 1. Habit is not the same thing as learned association

Current MESO persistent memory stores signed associations.

A current cue can recall:
- approach support;
- learned avoidance support.

That is still value/motivation-linked recall.

Habit research instead emphasizes stimulus/context -> response relations that can persist without current outcome value being actively represented.

Therefore:

```
learned association != habit
learned approach tendency != habit
repeated behavior != habit
```

## 2. Goal-directed action and habit use different information

Simplified research distinction:

### Goal-directed
Action depends on:
- action-outcome knowledge;
- current outcome value;
- planning/prospection.

### Habitual
Response can be evoked by:
- cue/context;
- learned stimulus-response structure;
with reduced dependence on currently represented outcome value.

This yields the defining counterexample:

```
outcome devalued
goal-directed response falls
habitual response may persist
```

## 3. Human habit measurement is not clean enough to overclaim

The 2026 devaluation paper shows an important methodology warning:
apparent outcome-insensitive/habitual behavior can be produced when the outcome was not actually devalued for the participant.

For MESO this is a general research lesson:

> Do not declare a process "habitual" merely because behavior failed to change after a supposed value update. Verify that the value update actually reached the decision subject.

This fits MESO's exact-source/currentness discipline.

## 4. Habit may be an efficiency mechanism rather than a motive

Habits can reduce computational demand for familiar behavior.

That suggests a machine analogue might be:
- cached action;
- macro/action chunk;
- default routine;
- compiled policy;
- reusable plan fragment.

Those are action-control/execution objects.

They are not necessarily motivational states.

Possible architecture:

```
MESO goal-directed tendency
               -> ACTION POLICY ARBITER -> intent
       /
HABIT/CACHED ROUTINE
```

with current protection/authority checks after both routes.

## 5. Habit must never bypass protection or authority

Even if a routine is highly practiced:

```
habit != permission
habit != current authority
habit != current truth
habit != current goal
```

Before execution, habit-derived action should still face:
- current environment evidence;
- protection/admissibility;
- protected-effect authority;
- capability/currentness.

## 6. Habit must not be reconstructed as desire

If an action occurs automatically:

```
action occurred
```

does not establish:

```
actor currently wanted the outcome
```

This is especially important for:
- conations;
- sexuality;
- social behavior;
- identity claims.

Repeated automatic behavior is not authored preference by itself.

## 7. Habit formation and MESO learning may interact

MESO could supply:
- repeated event identity;
- outcome/prediction evidence;
- motivational/reward history.

An action-policy system could separately learn:
- cue -> response reliability;
- action chunk;
- context dependence.

MESO may need readback:
- habit candidate active;
- habit confidence;
- cue match;
- expected action.

But MESO should not necessarily own the habit memory.

## 8. Habit vs action tendency

Current `ActionTendency` is derived after target selection:
- approach;
- learned withdraw;
- protective withdraw;
- inspect;
- uncommitted.

A habit can be more specific:
```
when context C -> perform action A
```

Thus action tendency is too abstract to represent a habit.

That is another reason not to force habit into current MESO memory.

## 9. Habit and vigor

Habit can determine *what action is automatically cued*.

Vigor determines *how intensely/resources are mobilized*.

```
habit != vigor
```

A routine can be habitual but low vigor, or goal-directed but high vigor.

## 10. Habit and goal conflict

A habit-derived action may conflict with:
- current goal;
- current authored conation;
- protection;
- operator task;
- changed environment.

The action-policy boundary needs a mechanism for goal-directed inhibition/override.

MESO could supply:
- current selected goal-directed tendency;
- target value;
- conflict signal.

The host/action-policy layer can then decide how to resolve habitual vs goal-directed proposals under declared policy.

## 11. Habit and compulsivity

Habit is not the same thing as compulsivity.

A habit may be:
- efficient;
- harmless;
- easily interrupted.

Compulsivity involves broader persistence/loss-of-control patterns.

Do not use:
```
habit strength
```
as a diagnosis or direct proxy for compulsivity.

## 12. Habits of thought are even less suitable for immediate core inclusion

Recent reviews discuss automaticized cognitive patterns/beliefs as possible habits of thought.

MESO should not broaden itself into:
- belief formation;
- thought control;
- cognitive schema ownership

under the habit label.

If cognitive routine caching becomes relevant, treat it as a separate producer/interface.

## 13. Candidate interface — research sketch

Possible external habit proposal:

```
HabitProposal:
    habit_id
    cue_event_id
    context_match
    proposed_action
    learned_at_revision
    confidence
    source/currentness
```

MESO/host could compare that with:

```
GoalDirectedProposal:
    selected_target
    goal_ref
    action_tendency
    expected_value evidence
    effort/feasibility
```

Both remain non-executable until authority/admissibility passes.

Do not implement these exact types yet.

## 14. Required adversarial cases

### HB-01 — devaluation
Outcome truly loses value; goal-directed action falls; habit may remain.

### HB-02 — failed devaluation manipulation
Value did not actually change; persistent action must not be mislabeled habit.

### HB-03 — goal-habit conflict
Habit proposes A, current goal proposes B; conflict remains visible.

### HB-04 — habit and protection
Habitual action becomes hazardous; protection blocks it.

### HB-05 — habit and authority
Habitual protected effect remains unauthorized.

### HB-06 — habit and conation
Routine executes; system does not infer authored desire from execution.

### HB-07 — habit context drift
Cue/context changed materially; stale habit proposal is suppressed or reviewed.

### HB-08 — efficient benign routine
Habit remains usable without forcing full expensive goal-directed recomputation every time.

### HB-09 — negative habit
Avoidance routine can be habitual without current hazard being high.

### HB-10 — capture
Habitual repetition consumes excessive allocation; anti-capture system can surface it.

## Candidate disposition

### Habit representation
Status: `EXTERNAL ACTION-POLICY CANDIDATE`

### Habit proposal/current cue binding
Status: `CORE INTERFACE CANDIDATE`

### Habit-vs-goal arbitration
Status: `HOST / DECISION-POLICY RESEARCH BOUNDARY`

### Habit memory inside AssociationMemory
Status: `REJECT FOR NOW`

Current association memory has different semantics.

## Hostile review

> **HOSTILE REVIEWER:** If habit influences action, excluding it from MESO makes the motivation model incomplete.

**PARTIALLY ACCEPTED.** MESO must be able to account for habitual proposals when they compete with current motivation. That does not require MESO to own the habit-learning implementation.

> **HOSTILE REVIEWER:** Two action systems are needless complexity for an AI agent.

**UNRESOLVED.** Many machines already use cached routines/macros/policies alongside deliberative planning. Whether MESO needs a formal dual route depends on actual runtime use cases.

> **HOSTILE REVIEWER:** A learned policy is basically one giant habit system.

**REJECTED AS TOO COARSE.** A learned policy may contain goal-conditioned, model-based, reactive and habitual-like behavior. The architecture should classify mechanisms by functional evidence, not implementation technology.

## Current conclusion

Habit should not be promoted to a MESO core state merely because reward frameworks mention it.

The stronger current boundary is:

```
MESO motivation/goal-directed evidence
        +
external habit/action-policy proposal
        ->
declared current action-policy arbitration
        ->
non-executable intent
```

with protection/currentness/authority still enforced downstream.

No implementation is proposed here.
