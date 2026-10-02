# MESO-CRCT Exact-Source Core Gap Audit V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / EXACT-SOURCE AUDIT / NO_IMPLEMENTATION`

Exact implementation subject:
`main@060d0feeb9dc9eb23801082bd8f1c4a7cb06184d`

Files inspected:
- `state.py`
- `circuit.py`
- `salience.py`
- `homeostasis.py`
- `dynamics.py`
- `appraisal.py`
- `arbitration.py`
- `selection.py`
- `allocation.py`
- `control.py`
- `decision_cycle.py`
- `tendency.py`
- `plasticity.py`
- `recall.py`
- `recall_resolution.py`
- `episode.py`

## 1. What current source actually represents

### Reward/protection
`RewardState` owns:
- `pleasure` in hard range `[-0.1, 10.0]`;
- `hazard` in `[0,1]`;
- `avoidance` in `[0,1]`.

This correctly allows protection without deep hedonic suffering.

### Salience
`SalienceState` owns:
- perceptual salience;
- semantic relevance;
- motivational salience;
- incentive salience;
- epistemic value;
- attentional priority.

### Learning
`LearningState` owns:
- signed prediction error;
- novelty;
- learning progress;
- satiation.

### Recruitment
`RecruitmentState` owns:
- activation;
- coherence;
- persistence;
- resolution.

### Homeostasis
Named need axes own:
- setpoint;
- current level;
- sensitivity;
- derived deficit/surplus.

Target affordances can boost incentive salience from the strongest matching deficit.

### Durable learned association
Persistent association strength is signed and cue-bound at recall:
- positive -> approach support;
- negative -> learned avoidance support.

Stored association does not self-activate.

## 2. What the current source deliberately does not represent

There is no first-class source type for:
- effort cost;
- willingness to exert effort;
- action vigor;
- delay/temporal cost;
- outcome probability/feasibility;
- predicted future resource need/allostasis;
- domain identity/contribution;
- habit/action chunk;
- threat imminence/probability/uncertainty/controllability;
- active vs passive avoidance;
- reward omission/frustrative nonreward;
- loss/unavailability as a typed event;
- appetitive vs aversive teaching-signal class;
- obligation source/authority class.

This is not necessarily a defect for V2. It marks the research frontier.

## 3. Signed prediction error is currently under-typed

`LearningState.prediction_error` is one number in `[-1,1]`.

`propose_plasticity()` computes:

```
delta = prediction_error
      * strongest_salience_gate
      * maximum_absolute_delta
```

if the gate is high enough.

This means current persistent association learning does **not** itself record whether the teaching discrepancy came from:
- unexpectedly greater reward;
- unexpectedly lower reward;
- aversive outcome;
- avoided aversive outcome;
- reward omission;
- loss;
- blocked goal;
- other outcome class.

A negative value therefore carries direction but not causal semantics.

### Risk

The same negative prediction-error sign can represent very different events.

Future domain profiles could incorrectly treat all negative teaching signals as:
```
learn avoidance
```
even when the correct consequence is:
- lower expected value;
- switch strategy;
- increase effort;
- update feasibility;
- update threat estimate;
- record loss;
- no durable preference change.

### Research consequence

Teaching-signal provenance likely needs richer typed outcome semantics before sexuality or other domains depend heavily on negative outcomes.

## 4. Homeostasis is reactive, not predictive

Current `NeedAxis` knows present setpoint and current level.

It has no:
- trajectory;
- consumption forecast;
- replenishment forecast;
- uncertainty;
- deadline;
- resource reservation.

Thus:
```
current_level >= setpoint
```
implies no deficit boost even if a known future demand will shortly exceed resources.

This is the exact source gap behind the allostasis research candidate.

## 5. Homeostatic combination uses strongest need only

Multiple need deficits do not sum; the largest matched `deficit * corrective_strength` wins.

This was intentionally chosen to prevent many weak needs from creating artificial extreme wanting.

That is a defensible reference policy, not a general theorem.

Potential future cases:
- two independently necessary resources;
- one target partially corrects multiple deficits;
- a resource bottleneck where the weakest reserve matters;
- competing corrective affordances.

Do not replace strongest-match until cross-domain tests establish a failure.

## 6. Current arbitration destroys some secondary structure

`arbitrate()` preserves:
- dominant driver;
- supporting drivers near the dominant score;
- effective incentive after satiation.

But it returns one:
- mode;
- priority.

Downstream target selection primarily sees that reduced result.

Therefore an appraised target with:
```
epistemic = 0.95
incentive = 0.90
semantic = 0.85
```
and another with:
```
incentive = 0.91
others low
```
may lose meaningful coalition structure after reduction.

The current result is explainable but lossy.

### Research consequence

Cross-domain work should test whether target selection needs:
- full typed appraisal state;
- a compact typed contribution bundle;
- or the current dominant/support representation plus new fields.

Do not assume all full state must flow into selection.

## 7. Current selection has a category discontinuity

Fixed default:
```
MOTIVATIONAL > EPISTEMIC > ORIENTING
```

causes categorical selection across targets regardless of numeric strength.

This is the clearest current source-level blocker to treating V2 arbitration as the final domain-general architecture.

## 8. Allocation health is target-ID based, not motive based

`AllocationWindow` records:
- selected target;
- priority;
- dominant driver;
- protective flag.

It can detect target crowd-out and incentive capture.

It cannot directly detect:
- domain crowd-out across many target IDs;
- one motive using rotating targets to evade concentration detection;
- cross-module subthreshold capture;
- resource overconsumption;
- effort overexertion;
- habitual repetition under changing target IDs.

This matters for:
- sexuality;
- curiosity;
- status;
- achievement;
- approval seeking.

### Research candidate

Future allocation receipts may need typed motive/domain contribution **without trusting caller-authored labels**.

## 9. Action tendency conflates some kinds of approach/avoidance

Current kinds:
- protective withdraw;
- learned withdraw;
- approach;
- inspect;
- uncommitted.

This is deliberately small.

Research now identifies possible missing distinctions:
- active escape;
- preventive action;
- behavioral inhibition;
- approach with low vigor;
- approach despite high effort;
- risk assessment under potential threat.

Do not expand the enum yet. First determine which distinctions alter host behavior and cannot be represented elsewhere.

## 10. Recall correctly separates negative learned value from hazard

This is a strong existing invariant.

A negative association:
- yields learned avoidance support;
- can drive `LEARNED_WITHDRAW`;
- does **not** write current hazard;
- does not rewrite pleasure.

That is directly compatible with the aversive research direction.

Preserve it.

## 11. Recall conflict resolution is strongest-per-direction

Multiple recalled influences are not summed.

The resolver uses:
- strongest approach support;
- strongest avoidance support;
- threshold;
- conflict margin.

This avoids accumulation attacks from many weak associations.

But it may underrepresent independent convergent evidence.

Research question:
> When, if ever, may independent same-direction learned evidence aggregate?

Any aggregation would need:
- independence evidence;
- replay control;
- source diversity;
- bounded accumulation.

Do not change current behavior without adversarial evidence.

## 12. Satiation only directly attenuates incentive salience in arbitration

Current:
```
effective_incentive = incentive_salience * (1 - satiation)
```

Satiation does not directly lower:
- motivational salience;
- epistemic value;
- semantic relevance;
- learned approach support.

This is sensible for a generic reference but raises future domain questions.

Examples:
- sexual refractory/satiation should probably not erase relationship relevance;
- curiosity satiation may reduce epistemic pursuit differently;
- social satiation may not behave like consummatory satiation;
- resource need satisfaction is already represented separately.

Conclusion:
- keep generic satiation narrow;
- domain profiles may need domain-specific recovery/satiation mechanics.

## 13. Temporal dynamics use family-wide half-lives

Current `DynamicsConfig` has one half-life for all salience channels and one for learning-state novelty/prediction-error/learning-progress.

That is deliberately simple.

Potential problem:
- semantic relevance may remain current longer than perceptual conspicuity;
- incentive activation may decay differently from epistemic novelty;
- potential threat vigilance may persist differently from a transient sensory cue.

Research decision:
- do not proliferate half-lives unless a real domain test fails under family-wide decay.

## 14. Protection never decays without explicit trusted update

Current hazard/avoidance remain unchanged under `advance_without_input()`.

This is conservative and currentness-safe:
```
time passing != evidence threat ended
```

But it can produce permanent protective state if no producer refresh arrives.

That is a host/source-liveness problem, not a reason to auto-decay hazard.

Future threat state needs:
- source currentness;
- expiry where semantically valid;
- explicit cleared/resolved evidence;
- UNKNOWN when the provider becomes stale.

Do not infer safety from silence.

## 15. Obligations are policy values without source provenance

`GoalObligation(goal_id, minimum_nonprotective_share)` contains no:
- authority source;
- issuer;
- creation evidence;
- expiry;
- currentness;
- obligation class.

For current deterministic tests this is acceptable.

For a real runtime this risks:
```
caller number -> de facto behavioral authority
```

Future obligation policy needs provenance before it participates in live allocation.

## 16. Current appraisal input trusts several caller-authored numeric values

`TargetAppraisalInput` directly accepts:
- perceptual salience;
- base motivational salience;
- base incentive salience;
- novelty;
- learning progress;
- prediction error;
- satiation;
- reward/protective state;
- recruitment;
- homeostasis.

Semantic relevance is comparatively stronger because it passes through a dedicated grounded semantic-evidence path.

### Research consequence

As MESO becomes more consequential, other fields may need producer-specific verified evidence contracts too.

The architecture should not mistake:
```
typed numeric field
```
for:
```
trusted measurement
```

## 17. Domain identity is absent — and that may be good

Current MESO source knows targets and signal kinds, not “sexuality”, “curiosity”, “caregiving”, etc.

That prevents domain assumptions from leaking into core.

Future domain-profile support should preserve this advantage:
- domain metadata may exist in typed contribution objects;
- core mechanisms should consume capabilities/evidence rather than giant domain conditionals.

Avoid:
```
if domain == "sexuality": ...
elif domain == "caregiving": ...
```
inside general arbitration wherever possible.

## 18. Exact-source strengths to preserve

Do not lose these while expanding:

1. welfare floor independent from protection;
2. attention cannot recursively self-author upstream salience;
3. stored associations require current cues;
4. event identity is distinct from state/content identity;
5. replay controls;
6. provenance-bound receipts;
7. persistent learning separate from transient activation;
8. negative learned recall does not manufacture hazard;
9. protection is explicit and independently inspectable;
10. intent remains non-executable;
11. review/quarantine preserves history;
12. local selection and long-horizon allocation are separate layers.

## Core gap ranking after source inspection

### Tier A — strongest demonstrated architectural gaps
1. cross-domain comparison/arbitration;
2. effort/vigor;
3. feasibility/delay;
4. obligation provenance;
5. aversive outcome / teaching-signal semantics.

### Tier B — strong interface gaps
6. predictive resource/allostatic evidence;
7. threat geometry/currentness;
8. domain contribution provenance for allocation audits.

### Tier C — research first
9. habit;
10. anticipation as independent state;
11. frustrative nonreward state;
12. active/passive avoidance enum expansion;
13. finer temporal decay parameters;
14. learned-evidence aggregation.

## Hostile review

> **HOSTILE REVIEWER:** Most of these are not defects; they are simply features V2 never claimed to support.

**ACCEPTED.** This is a gap audit against the newly expanded MESO mission, not a bug report against V2.

> **HOSTILE REVIEWER:** Adding all Tier A/B concepts at once would destroy the elegant small state model.

**ACCEPTED.** The next architecture should add the minimum types required by failing cross-domain cases. This document ranks research pressure; it does not prescribe one field per bullet.

> **HOSTILE REVIEWER:** Caller-authored numeric input is unavoidable somewhere.

**ACCEPTED.** The issue is not that an API accepts numbers. The issue is whether downstream claims remember who produced them, under what contract, and whether they remain current.

## Current conclusion

The current executable MESO stack is a coherent V2 reference for typed reward/salience/learning/protection.

The new domain-general mission reveals several missing semantics, but the correct next move is **not** to bolt every research construct onto `CircuitState`.

The next move is to design the smallest revised appraisal/arbitration interface that can pass the cross-domain and aversive counterexamples while preserving V2's existing invariants.
