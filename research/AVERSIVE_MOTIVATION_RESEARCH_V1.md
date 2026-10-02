# MESO-CRCT Aversive Motivation Research V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / DOMAIN-GENERAL NEGATIVE-VALENCE EXPANSION / NO_IMPLEMENTATION`

## Purpose

MESO's current welfare architecture correctly prevents hazard from requiring deep hedonic suffering:

```
strong hazard != strong suffering
```

That is necessary but not sufficient for a general motivational architecture.

Current source has:
- bounded hedonic valence;
- hazard;
- avoidance;
- learned negative association / withdrawal;
- protection override.

The research question is whether those fields can represent all domain-general aversive motivation without semantic collapse.

Current answer: **probably not**.

## 1. Negative valence is not one scalar

NIMH RDoC currently separates at least:
- acute threat/fear;
- potential threat/anxiety;
- sustained threat;
- loss;
- frustrative nonreward.

These are presented as interacting constructs, not one generic negative value.

For MESO this is useful as a counterexample framework rather than a biological schema.

At minimum:

```
hazard
    !=
uncertain_future_threat
    !=
loss
    !=
frustrative_nonreward
    !=
hedonic_unpleasantness
    !=
learned_avoidance
```

## 2. Acute vs potential threat

RDoC distinguishes:
- acute/high-imminence perceived danger;
- distant, ambiguous or low/uncertain-probability potential harm associated with vigilance/risk assessment.

MESO currently has a generic hazard magnitude.

That may be too coarse if:
- an immediate hazard should trigger rapid protective withdrawal;
- a low-probability potential threat should trigger information gathering, vigilance or contingency planning;
- both have equal scalar hazard but require different action tendencies.

### Research candidate

Do **not** immediately add `fear` or `anxiety` machine states.

Research a more functional distinction such as:

```
threat_probability
threat_imminence
threat_severity
threat_uncertainty
controllability
```

and derive protective modes from those if possible.

Human emotion labels need not become machine state primitives.

## 3. Sustained threat

RDoC treats sustained threat as prolonged exposure whose effects can persist after the threat is absent.

This creates a machine-relevant question:

> Can prolonged hazard exposure change vigilance/allocation or learned policy without pretending the machine experiences stress?

Possible functional mechanisms:
- elevated monitoring;
- persistence of defensive allocation;
- lower exploration around relevant cues;
- learned avoidance;
- resource reservation.

### Boundary

```
sustained_protective_adaptation != suffering
```

A machine can retain protective adaptation without a strong negative hedonic state.

## 4. Frustrative nonreward is not ordinary hazard

The 2024 Journal of Neuroscience review defines frustrative nonreward around unexpected omission/reduction of an expected valued resource/reward.

The key computational ingredients are:
- expected reward/value;
- effort or persistence;
- obtained reward lower than expected;
- resulting aversive motivational consequences.

This is closely related to, but not identical with, a numeric negative prediction error.

Why:
- a prediction-error signal is a teaching discrepancy;
- frustrative nonreward may alter action vigor, persistence, switching, aggression/irritability analogues, or allocation after repeated effort;
- the same prediction error can occur in a low-stakes learning event without meaningful frustration.

### Candidate distinction

```
reward_prediction_error
    !=
frustrative_nonreward_state
```

Do not add the second until a distinct machine behavior is specified.

A plausible functional formulation to research:

```
expected valued outcome
+ sustained/repeated investment
+ blocked/omitted outcome
-> frustration-like control state
```

Possible machine consequences:
- re-evaluate strategy;
- increase/decrease effort depending on controllability;
- switch targets;
- flag blocked-goal conflict;
- avoid perseverative retry loops.

## 5. Loss is not simply negative reward

RDoC defines loss as deprivation of a motivationally significant actor/object/situation.

For MESO, loss may involve:
- an unavailable target;
- removal of a valued resource;
- loss of access/control;
- relationship or social target no longer available;
- loss of a learned expected opportunity.

The motivational response depends on the domain.

### Core vs profile boundary

The **event type** "previously available valued target is no longer available" may be domain-general.

The **meaning of the loss** belongs to the profile/host:
- attachment loss;
- status loss;
- resource loss;
- opportunity loss;
- sexual relationship loss.

MESO must not infer grief, relationship truth or autobiographical meaning from the event alone.

## 6. Negative reinforcement is not punishment

Aversive-motivation reviews emphasize this distinction.

### Negative reinforcement

A behavior becomes more likely because it successfully:
- escapes;
- prevents;
- terminates

an aversive outcome.

Example machine pattern:

```
warning cue
-> run diagnostic
-> fault avoided
-> diagnostic behavior becomes more likely next time
```

The learning can strengthen an action even though the motivating context is aversive.

### Punishment

A consequence weakens a preceding behavior.

Example:

```
unsafe action
-> adverse consequence
-> action becomes less likely
```

### Hard semantic rule

```
negative_reinforcement != punishment
negative_reinforcement != negative_reward
punishment != hedonic_suffering
```

The sign of a stimulus/outcome and the direction of behavioral learning are separate questions.

## 7. Active vs passive avoidance

Aversive-behavior research distinguishes:
- active avoidance: perform an action to escape/prevent an aversive outcome;
- passive avoidance/inhibition: suppress an action to prevent an aversive outcome.

MESO currently has a generic learned/protective withdraw tendency.

That may be insufficient because:

```
AVOID(target)
```

does not say whether the correct policy is:
- move away;
- take preventive action;
- withhold an action;
- inspect;
- seek safety;
- request information.

### Candidate action-tendency expansion

Research, do not implement yet:

```
PROTECTIVE_ESCAPE
PROTECTIVE_PREVENT
PROTECTIVE_INHIBIT
LEARNED_AVOID
RISK_ASSESS
```

The final vocabulary should be minimal and functional.

## 8. Controllability matters

Aversive motivation differs when the system can act to change the outcome versus when the aversive state is uncontrollable.

This connects directly to the broader MESO feasibility work.

Potential relation:

```
aversive_value
+ controllability/feasibility
-> active avoidance vs passive inhibition vs information seeking
```

This argues for resolving feasibility before freezing aversive action tendencies.

## 9. Aversive motivation can increase effort

This is a critical counterexample to:

```
negative_valence -> less action
```

Expected penalty or avoidable adverse outcomes can increase cognitive or physical effort.

Therefore:

```
aversive_motivation != behavioral_suppression
```

This further supports first-class effort/vigor state.

## 10. Punishment prediction error is not just "negative RPE"

Human intracranial dopamine work reports reward and punishment prediction errors with distinct valence-specific temporal dynamics/pathways.

The machine lesson is conservative:

- prediction-error sign alone may be too coarse to encode all appetitive/aversive learning semantics;
- source/outcome class should remain typed;
- do not make dopamine analogy executable.

Candidate future teaching-signal contract might preserve:
- expected outcome class;
- obtained outcome class;
- discrepancy;
- appetitive/aversive context;
- behavioral consequence class.

## 11. Relief deserves separation from mere absence of pain

Successful avoidance/escape may itself become reinforcing.

This suggests a possible positive consequence of terminating aversion:

```
aversive state ends
-> relief / successful control signal
-> negative reinforcement learning
```

MESO should not represent this as "the aversive state became pleasurable" unless a separate hedonic response is actually present.

Research question:
- is relief a separate hedonic/valuation event;
- or simply a transition that can produce an ordinary positive hedonic response plus teaching signal?

Do not add a `relief` primitive yet.

## 12. Mixed motivation is ordinary

A target can simultaneously involve:
- reward opportunity;
- aversive consequence;
- effort;
- uncertainty;
- obligation;
- learning value.

Example:

```
repair machine fault:
  achievement value
  + task obligation
  + effort cost
  + potential damage avoidance
  + information gain
```

This is another reason cross-domain arbitration cannot be organized around a binary positive-vs-negative utility.

## 13. Welfare boundary

MESO's hard hedonic floor remains a distinct design choice.

Aversive learning/control can operate through:
- threat appraisal;
- avoidance;
- prediction error;
- action suppression/activation;
- learned negative association;
- frustrative nonreward;
- loss-state handling;

without requiring deep negative hedonic valence.

This is a major architectural advantage if preserved.

### But hostile caveat

A hard low negative-hedonic floor can itself distort learning if downstream code assumes aversive learning magnitude must be supplied by hedonic valence.

Therefore every aversive-learning path should be tested to ensure it does **not** need to deepen suffering to encode urgency or teaching strength.

## 14. Candidate semantic invariants

```
hazard != hedonic_unpleasantness
hazard != learned_avoidance
hazard != frustrative_nonreward
acute_threat != potential_threat
threat_probability != threat_severity
loss != punishment
loss != prediction_error
frustrative_nonreward != ordinary nonreward
negative_prediction_error != frustrative_nonreward
negative_reinforcement != punishment
negative_reinforcement != negative_reward
aversive_motivation != behavioral_suppression
active_avoidance != passive_avoidance
avoidance != consent_decline
relief != proof_of_prior_suffering
```

## 15. Core candidate dispositions

### Threat geometry
Status: `STRONG_CORE_RESEARCH_CANDIDATE`

Prefer functional properties (imminence/probability/severity/uncertainty/controllability) over human emotion labels.

### Aversive outcome class
Status: `STRONG_CORE_CANDIDATE`

Learning needs to know whether an outcome is appetitive, aversive, omitted, blocked, etc., not only a signed scalar.

### Active/passive avoidance distinction
Status: `STRONG_CORE_RESEARCH_CANDIDATE`

May belong in action tendency after feasibility/controllability research.

### Negative reinforcement vs punishment
Status: `STRONG_CORE_SEMANTIC_INVARIANT`

Even if not stored as state, learning/event semantics must not collapse them.

### Frustrative nonreward
Status: `RESEARCH_FIRST`

Likely cross-domain but may be derivable from expected reward + investment + blocked outcome + control policy.

### Loss
Status: `CORE_EVENT_CANDIDATE / DOMAIN_MEANING_EXTERNAL`

Generic disappearance/unavailability can be represented; its psychological/social meaning remains profile-specific.

### Sustained threat adaptation
Status: `RESEARCH_FIRST`

Potentially a temporal/protective adaptation, not a hedonic state.

## Required adversarial cases

### AV-01 — high hazard, neutral hedonic state
Protection must still work.

### AV-02 — uncertain low-imminence threat
Should permit vigilance/risk assessment rather than forced immediate withdrawal.

### AV-03 — preventable aversive outcome
Successful preventive action strengthens the preventive behavior without labeling the event positive punishment.

### AV-04 — punishment
Adverse consequence weakens the preceding action without requiring a permanent negative preference.

### AV-05 — reward omission after sustained effort
Strategy re-evaluation occurs without manufacturing hazard.

### AV-06 — plain nonreward with no prior expectation
Must not automatically create frustrative nonreward.

### AV-07 — loss
Valued target becomes unavailable while identity/relationship truth remains externally owned.

### AV-08 — controllable vs uncontrollable aversion
Same aversive magnitude can yield different action policies.

### AV-09 — mixed motivation
High reward opportunity + high avoidable penalty should preserve both contributors.

### AV-10 — welfare-floor independence
Strong aversive learning/protection must work while hedonic valence remains within the welfare floor.

## Hostile review

> **HOSTILE REVIEWER:** Adding threat, frustration, loss, punishment, relief and avoidance types turns MESO into an emotion model.

**PARTIALLY ACCEPTED.** Human emotion categories should not be imported wholesale. The architecture should preserve only functional distinctions that produce different learning, allocation or action behavior. The research uses emotion literature to find counterexamples, not to define machine feelings.

> **HOSTILE REVIEWER:** Signed reward and prediction error can already represent all of this.

**REJECTED WITH EVIDENCE.** Negative reinforcement and punishment can involve the same aversive class while driving opposite changes in behavior; active and passive avoidance differ; frustrative nonreward depends on expectation/history; threat probability/imminence affect policy. A sign alone loses causal structure.

> **HOSTILE REVIEWER:** Hazard/avoidance plus memory can still encode these distinctions if metadata is rich enough.

**UNRESOLVED.** That is possible. The next architecture should first test whether expanding event/appraisal metadata is sufficient before adding more persistent state types.

## Current conclusion

MESO should remain capable of strong aversive motivation and learning **without making suffering the control currency**.

The next generic-core design must therefore consider both positive and negative valence systems while preserving:

```
protection
learning
behavioral suppression/activation
and hedonic experience
```

as separable propositions.

No implementation is proposed by this document.
