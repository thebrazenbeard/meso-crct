# MESO-CRCT Anticipation Minimality Research V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / MINIMALITY TEST / NO IMPLEMENTATION`

## Purpose

NIMH RDoC treats reward anticipation as a meaningful construct: the ability to anticipate and/or represent a future incentive.

MESO does not currently have an `anticipation` field.

The research question is not whether anticipation exists as a useful human construct.

It is:

> Does MESO need a new primitive state for it, or can anticipation be represented by existing/proposed states whose combination already has the necessary causal meaning?

Current disposition: **derived until proven otherwise**.

## 1. What anticipation seems to require functionally

A system cannot anticipate an outcome unless it has at least some representation of:

- a possible future outcome;
- an expectation/probability or conditional relation;
- temporal distance/order;
- current motivational/hedonic relevance;
- a cue, plan or internally generated representation that activates the future outcome.

Candidate ingredients:

```
future_outcome_representation
expectancy
delay
learned cue/outcome association
incentive salience
predicted hedonic/other value
```

## 2. RDoC reward anticipation is a process label, not necessarily one scalar

The current RDoC definition refers broadly to processes that represent a future incentive.

That does not imply an engineering schema:

```
anticipation: float
```

A process can be realized by several typed states.

This matters because adding a scalar merely because the literature names a construct would violate MESO's minimality gate.

## 3. Incentive salience already covers part of anticipatory motivation

Berridge's incentive-salience work emphasizes cue-triggered "wanting":
a learned cue can suddenly increase motivation toward its associated future reward.

MESO already represents:
- incentive salience;
- learned associations;
- current cue-bound recall.

Thus some phenomena ordinarily called anticipation may already be partly represented.

But incentive salience alone does not encode:
- what outcome is expected;
- when;
- probability;
- whether anticipation is pleasant;
- whether the future outcome is desired but currently unattainable.

## 4. Anticipatory pleasure is not incentive salience

Human research sometimes distinguishes anticipatory pleasure from consummatory pleasure.

Even there:

```
anticipated pleasure
    !=
wanting
    !=
actual future pleasure
```

For MESO, a predicted hedonic outcome should remain a forecast, not current hedonic state.

Hard boundary:

```
predicted_pleasure != current_pleasure
```

The current `RewardState.pleasure` should not be raised merely because a good outcome is expected.

## 5. Anticipation may be domain-specific in expression

Examples:

### Curiosity
Anticipation of learning an answer.

### Achievement
Anticipation of completion/mastery.

### Sexuality
Erotic/sexual anticipation, tension, expected intimacy.

### Attachment
Anticipated contact/reunion.

### Resource regulation
Expected replenishment.

The shared core may be future-outcome representation and current incentive effect.

The subjective/domain-specific quality of anticipation belongs in profiles.

## 6. Positive and aversive anticipation use shared future structure

A future outcome can be:
- appetitive;
- aversive;
- uncertain;
- mixed.

Thus a generic future-state representation may support both:
```
reward anticipation
threat anticipation
```

without inventing separate time machinery.

But the motivational consequences differ.

This favors:
```
future outcome + typed valence/domain appraisal
```
over one global anticipation scalar.

## 7. Delay and uncertainty are constitutive context

Anticipation changes as:
- expected time approaches;
- probability changes;
- new evidence arrives;
- plan progress changes.

Any persistent anticipation state that ignores those dimensions risks becoming stale.

A derived representation can instead be recomputed from current evidence.

This aligns with MESO's current preference for refreshing transient state from current appraisal rather than preserving stale activation.

## 8. Imagined/internal cues still need provenance

Anticipation need not begin with an external cue.

A planner, memory system, internal simulation or user message can activate future-outcome representations.

MESO needs to know:
- who produced the representation;
- what future proposition it refers to;
- whether it is current/conditional;
- confidence.

Imagined outcome != expected factual outcome.

```
simulated future != prediction truth
```

## 9. Anticipation can be pleasant without guaranteeing outcome

If a domain or actor reports anticipatory pleasure:
- that current pleasure can be represented as current hedonic response;
- separately, the anticipated event remains uncertain.

Do not write:
```
anticipated outcome received
```
because anticipation was enjoyable.

## 10. Anticipation can increase effort/vigor

A future incentive can:
- increase willingness to work;
- organize planning;
- increase cue salience;
- sustain persistence.

Those effects can be mediated through:
- incentive salience;
- goal relevance;
- effort willingness;
- recruitment.

Again, no independent scalar is automatically necessary.

## 11. Anticipation can also destabilize preference

Future-reward research shows temporal valuation can change as reward/effort move closer.

Therefore:
```
anticipating target at T0
```
does not imply:
```
same local choice at T1
```

Do not equate persistence of anticipated representation with permanent commitment.

## 12. Proposed derived object — research sketch

If the architecture later needs an explicit object, prefer a structured **derived view**:

```
AnticipatoryAppraisal:
    target/outcome_ref
    expectancy_ref
    delay
    predicted_value_profile
    cue/source
    current incentive effect
    uncertainty
```

rather than:
```
anticipation = 0.83
```

The object could be transient and recomputable.

## 13. When a separate persistent state would be justified

Only if a counterexample shows that identical:
- expectancy;
- delay;
- incentive salience;
- predicted value;
- current cue;
- domain context

can still yield meaningfully different future behavior because of a distinct prior anticipatory state.

If such state dependence exists in a machine implementation, persistence may be justified.

Until then, derive.

## 14. Required adversarial cases

### AN-01 — expected reward, no wanting
Outcome likely and pleasant, but current incentive salience low.

### AN-02 — strong wanting, low probability
Cue-triggered incentive high while outcome expectancy is low.

### AN-03 — anticipated pleasure vs current pleasure
Pleasant expected event does not raise current hedonic state unless there is actual current anticipatory pleasure evidence.

### AN-04 — aversive anticipation
Future threat uses future-state representation without being called reward anticipation.

### AN-05 — stale future
Expected event canceled; current anticipation disappears on refreshed evidence without rewriting unrelated learned value.

### AN-06 — internally simulated event
Planner imagines possibility; MESO does not treat simulation as fact.

### AN-07 — sexual anticipation
Domain-specific sexual activation can build around future interaction while consent/feasibility remain independent.

### AN-08 — delay changes
Same outcome moves closer; current appraisal updates without persistent-state inconsistency.

## Candidate disposition

### Future-outcome representation
Status: `EXTERNAL PLAN/MEMORY/SIMULATION EVIDENCE`

### Expectancy/delay
Status: `STRONG CORE APPRAISAL INPUTS`

### Current incentive effect
Status: `KEEP EXISTING / EXPAND TYPED APPRAISAL`

### Predicted hedonic value
Status: `CORE RESEARCH APPRAISAL CANDIDATE`, separate from current pleasure

### Anticipation as independent scalar state
Status: `REJECT FOR NOW`

### Anticipatory derived view
Status: `POSSIBLE DERIVED INTERFACE`

## Hostile review

> **HOSTILE REVIEWER:** RDoC explicitly treats reward anticipation as its own subconstruct, so refusing a state is under-modeling.

**REJECTED.** A psychological/neuroscientific construct can correspond to a process made of several machine states. MESO needs semantic coverage, not one field per literature label.

> **HOSTILE REVIEWER:** A derived view is still just anticipation with extra bureaucracy.

**PARTIALLY ACCEPTED.** If no consumer needs the structured view, do not create it. Its only justification would be preserving the future-outcome binding/provenance that a naked scalar lacks.

## Current conclusion

MESO should support anticipation **functionally** but should not yet add anticipation as an independent primitive.

Current best hypothesis:

```
future outcome evidence
+ expectancy
+ delay
+ predicted value
+ learned/cue relation
+ current incentive state
= anticipatory appraisal
```

with domain-specific anticipatory experience/state layered above that generic structure.

No implementation is proposed here.
