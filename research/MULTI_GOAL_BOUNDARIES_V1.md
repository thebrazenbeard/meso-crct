# MESO-CRCT Multi-Goal and Goal-Target Boundary Research V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / SEMANTIC-BOUNDARY REFINEMENT / NO_IMPLEMENTATION`

## Purpose

Current MESO is target-centric:
- appraisal builds a `target_id`;
- selection chooses a `selected_target`;
- allocation history records selected target IDs.

But `allocation.py` also names its policy objects `GoalObligation(goal_id, ...)` and compares those goal IDs directly to selected target IDs.

For the current reference tests, this is compact.

For a multi-domain architecture, it risks collapsing:

```
target
goal
plan
action
domain/motive
obligation
```

into one identifier.

This pass defines the conceptual boundary before richer arbitration is designed.

## 1. Proposed semantic vocabulary

### Target
The current object/opportunity/state/referent being appraised.

Examples:
- a document;
- a person;
- a repair;
- a research question;
- a food item;
- a sexual interaction opportunity.

A target can be relevant to multiple goals.

### Goal
A desired future state or outcome being pursued.

Examples:
- finish a research audit;
- maintain a resource reserve;
- repair a machine;
- learn a topic;
- maintain a relationship.

Goals require an authority/provenance model:
- self-authored;
- operator-assigned;
- contractual;
- inferred candidate;
- system maintenance.

MESO should not silently author goals from salience.

### Plan / strategy
A route for achieving a goal.

One goal can have multiple plans.

A failed plan does not necessarily mean the goal lost value.

### Action
A concrete candidate behavior/step.

MESO may emit a non-executable action tendency/intent proposal, but execution remains external.

### Domain contribution / motive
Why the goal/target/action matters motivationally.

Examples:
- curiosity;
- achievement;
- sexuality;
- caregiving;
- attachment;
- protection;
- resource regulation.

Multiple motives can support one goal.

### Obligation
A policy/commitment that constrains allocation.

An obligation may relate to a goal but is not the goal itself and is not necessarily a desire.

## Hard non-equivalences

```
target != goal
goal != plan
plan != action
motive != goal
motive != obligation
obligation != desire
selected_target != durable_goal
failed_plan != devalued_goal
shelved_goal != abandoned_goal
disengaged_goal != impossible_goal
```

## 2. Current source conflation

Current allocation history stores:
```
selected_target: str | None
```

Current obligations store:
```
goal_id: str
```

and minimum shares are computed by counting:
```
event.selected_target == goal_id
```

Thus the current reference semantics effectively assume:
```
allocation-goal identity == selected-target identity
```

That assumption should not become canonical.

## 3. Why it fails with multi-step goals

Goal:
```
research MESO motivation
```

Possible targets/actions:
- read effort paper;
- inspect source code;
- compare Sexuality;
- write research ledger;
- run hostile review.

Allocation among those targets still serves one goal.

If the goal requires a minimum share, counting each target separately can falsely report neglect.

Conversely, one target may serve multiple goals:
```
read one paper
-> curiosity + MESO research obligation + skill development
```

A one-ID model cannot represent this faithfully.

## 4. Multiple-goal research emphasizes dynamic allocation

Research on multiple-goal pursuit treats self-regulation as managing competing demands on limited time/resources.

Relevant processes include:
- prioritization;
- shielding;
- switching;
- shelving;
- disengagement;
- re-engagement;
- adaptation of goals.

The machine lesson is not to copy human self-regulation.

It is that:
```
one target selected now
```
is not sufficient state for:
```
which goals are alive, deferred, blocked, completed, or abandoned?
```

## 5. Goal shelving vs disengagement

Research distinguishes:
- **shelving** — temporary withdrawal/deprioritization;
- **disengagement** — more durable withdrawal from goal pursuit.

This is an excellent MESO counterexample.

If a high-value goal is temporarily infeasible:
- MESO should permit shelving/deprioritization;
- durable goal value/identity should not be deleted.

```
not selected now != abandoned
```

This mirrors current MESO's good distinction:
```
transient activation != persistent memory
```

## 6. Persistence should not be a virtue by default

Human goal research increasingly treats timely disengagement from unattainable goals as potentially adaptive.

Machine analogue:
- repeated failure should not force infinite retry;
- sunk effort should not imply continued pursuit;
- inability to reach a route may justify strategy switch or goal review.

But MESO should not autonomously delete a protected/operator-authored goal merely because it looks hard.

### Boundary

MESO may propose:
- continue;
- reduce allocation;
- seek alternate plan;
- shelf;
- request goal review.

Actual goal revocation may belong to the goal authority.

## 7. Goal conflict can be structural or resource-based

Two goals may conflict because:
- they need the same scarce resource/time;
- achieving one directly prevents the other;
- their action requirements contradict;
- one changes the state needed by another.

Those are different conflicts.

Potential typed conflict evidence:
```
RESOURCE_CONFLICT
ACTION_CONFLICT
STATE_CONFLICT
POLICY_CONFLICT
UNKNOWN
```

Do not implement this vocabulary yet.

## 8. Goals can facilitate one another

Not all multi-goal relationships are competitive.

One action can:
- serve several goals;
- reduce future effort for another goal;
- create information useful elsewhere;
- satisfy multiple domains.

Cross-domain arbitration should therefore not treat every active motive as fighting for a zero-sum slot.

## 9. Domain/motive coalition vs goal identity

Example:

```
goal: spend time with partner
motives:
  attachment
  affiliation
  sexuality
  play
```

Same goal, multiple motivational contributors.

Another:

```
goal: repair furnace
motives:
  obligation
  protection
  achievement
  curiosity
```

Therefore the future contribution model should attach motive/domain evidence to goal/target/action without making domain equal goal.

## 10. Goals may be externally authored

A live agent can have:
- operator-assigned task;
- self-authored goal;
- contract obligation;
- safety maintenance target;
- inferred opportunity.

They should not all be treated as equivalent internal desire.

Potential authority classes:
```
SELF_AUTHORED
OPERATOR_ASSIGNED
CONTRACTUAL
SYSTEM_MAINTENANCE
INFERRED_CANDIDATE
```

This is only a research sketch.

## 11. Goal currentness matters

A stored goal can be:
- active;
- completed;
- revoked;
- superseded;
- expired;
- blocked;
- shelved;
- unknown-currentness.

MESO should not revive an old goal merely because learned associations still support it.

This parallels conation/currentness rules.

## 12. Progress evidence should not live in motivation by default

A planner/task system should own:
- plan;
- subtask graph;
- progress;
- completion evidence;
- blockers.

MESO can consume:
- remaining effort;
- delay;
- feasibility;
- progress relevance.

It does not need to become Project Runner.

## 13. Goal pursuit and habit

Habit can select actions without current goal valuation.

Therefore future action policy may have:
```
goal-directed route
habitual route
```

MESO must not infer:
```
action occurred -> goal was active
```

This also protects conation semantics.

## 14. Goal pursuit and sexuality

Sexual state may generate:
- target relevance;
- desire;
- action tendency.

It must not automatically manufacture a durable goal such as:
```
pursue this person
```

Likewise:
- attraction != pursuit goal;
- fantasy != pursuit goal;
- arousal != pursuit goal.

A sexual interaction goal, if any, requires separate authored/contextual state.

## 15. Goal pursuit and aversion

Avoidance can also be goal-directed:

```
goal: prevent damage
action: run diagnostic
motive: protection
learning: negative reinforcement
```

This demonstrates again:
```
goal != valence
```

## 16. Candidate future interface

Research sketch only:

```
GoalRef:
    goal_id
    authority/source
    currentness
    lifecycle_state

TargetRef:
    target_id
    current evidence

PlanRef:
    plan_id
    goal_id
    provider/currentness

Contribution:
    domain/motive kind
    target/goal/action scope
    typed evidence

CandidateAction:
    action_id
    plan/goal refs
    resource/feasibility evidence
```

Do not implement until the minimality gate is applied.

## 17. Allocation accounting should likely move from target IDs to goal/contribution evidence

Current target-share auditing is useful for capture tests.

Future long-horizon health may need separate views:
- target concentration;
- goal allocation;
- domain/motive allocation;
- resource allocation;
- protection/obligation allocation.

This prevents a capture process from evading detection by rotating target IDs inside one motive.

But every new dimension creates gaming risk.

Only add dimensions whose producer identity/currentness can be verified.

## 18. Required adversarial cases

### MG-01 — one goal, many targets
Different actions/targets all contribute to one goal; goal-share accounting remains coherent.

### MG-02 — one target, many goals
One selected action advances multiple goals without double-counting arbitrary reward.

### MG-03 — shelved goal
High-value goal temporarily infeasible; not selected but remains active/shelved.

### MG-04 — revoked goal
Learned incentive remains but goal authority says revoked; MESO does not revive it as active goal.

### MG-05 — failed plan
Plan fails; alternate plan remains viable; target value need not change.

### MG-06 — infeasible goal
MESO may recommend review/shelving without unilaterally deleting external goal authority.

### MG-07 — obligation without desire
Operator-assigned goal receives allocation despite low internal incentive; record reason honestly.

### MG-08 — desire without goal
Sexual/curiosity motive active but no durable pursuit goal is authored.

### MG-09 — rotating-target capture
One motive cycles through target IDs; motive/domain concentration remains detectable if such auditing is later added.

### MG-10 — habit
Habitual action occurs without current goal; no false goal reconstruction.

## Candidate dispositions

### Goal identity/lifecycle
Status: `EXTERNAL_GOAL_SYSTEM / CORE_REFERENCE INTERFACE`

### Target identity
Status: `KEEP CORE APPRAISAL CONCEPT`

### Plan/progress
Status: `EXTERNAL PLANNER INTERFACE`

### Domain/motive contribution
Status: `CORE RESEARCH INTERFACE CANDIDATE`

### Obligation
Status: `EXTERNAL POLICY/COMMITMENT INPUT`

### Goal shelving/disengagement
Status: `EXTERNAL GOAL-LIFECYCLE ACTION / MESO MAY PROPOSE`

### Multi-goal allocation auditing
Status: `STRONG CORE RESEARCH CANDIDATE`

## Hostile review

> **HOSTILE REVIEWER:** This is architecture creep into task management.

**ACCEPTED AS A BOUNDARY.** MESO should not own plans/tasks. It needs only enough typed references to avoid confusing what is wanted, what is being acted on, why, and under whose authority.

> **HOSTILE REVIEWER:** Adding goal/domain allocation audits will create another governance bureaucracy.

**PARTIALLY ACCEPTED.** The current target-window audit already solves real capture problems. New axes should be added only after an adversarial capture case defeats target-only auditing.

> **HOSTILE REVIEWER:** A selected target is often good enough to stand in for a goal.

**ACCEPTED FOR SIMPLE CASES.** The architecture can allow a 1:1 shorthand. It should not make that shorthand the semantic definition.

## Current conclusion

The expanded MESO architecture should not use one ID for target, goal, plan, motive and obligation.

The likely clean boundary is:

```
external goal/plan/currentness
    ->
MESO target/domain appraisal
    ->
cross-domain allocation/arbitration
    ->
non-executable action proposal
```

with explicit references preserving what proposition each layer owns.

No implementation is proposed here.
