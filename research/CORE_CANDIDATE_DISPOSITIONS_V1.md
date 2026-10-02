# MESO-CRCT Core Candidate Dispositions V1

Date: 2026-10-02
Status: `RESEARCH_DECISION_LOG / NOT_ARCHITECTURE_FREEZE`

This log records the current research status of proposed domain-general mechanisms.

## Status vocabulary

- `STRONG_CORE_CANDIDATE`
- `CORE_INTERFACE_CANDIDATE`
- `DERIVED_UNTIL_PROVEN_OTHERWISE`
- `RESEARCH_FIRST`
- `DOMAIN_PROFILE`
- `EXTERNAL_AUTHORITY`
- `REJECT_AS_CORE_COLLAPSE`

## 1. Effort valuation

Status: `STRONG_CORE_CANDIDATE`

Why:
- recurs across reward pursuit, curiosity, achievement, social behavior, caregiving, sex, play and resource acquisition;
- strong neuroscience/RDoC evidence distinguishes effort cost/willingness from reward value;
- current MESO lacks first-class effort semantics.

Required distinction:
```
effort_cost != reward_value != willingness_to_work
```

## 2. Action vigor / behavioral activation

Status: `STRONG_CORE_CANDIDATE`

Why:
- directional choice and activational intensity are empirically dissociable;
- current MESO derives direction but not vigor.

Required distinction:
```
what_to_do != how_vigorously_to_do_it
```

Open:
- state vs derived output.

## 3. Delay / temporal cost

Status: `STRONG_CORE_CANDIDATE`

Why:
- cross-domain;
- RDoC explicitly separates delay in reward valuation;
- necessary for future goals and opportunity cost.

Do not freeze one discount equation.

## 4. Feasibility / expectancy

Status: `STRONG_CORE_CANDIDATE`

Why:
- desirability and attainability are independent;
- cross-domain target selection needs probability/feasibility evidence.

Boundary:
```
expected != true
```

Source/currentness required.

## 5. Predictive allostasis / future resource need

Status: `CORE_INTERFACE_CANDIDATE`

Why:
- current deficit alone misses anticipatory resource regulation;
- machine substrate has real resource states.

Why interface candidate:
- resource truth belongs to host/resource sensors;
- MESO should appraise supplied current/predicted resource state rather than self-attest it.

## 6. Anticipation

Status: `DERIVED_UNTIL_PROVEN_OTHERWISE`

Current hypothesis:
```
anticipation =
    learned expected outcome
    + incentive/hedonic forecast
    + delay
    + uncertainty/feasibility
```

RDoC names reward anticipation as a meaningful construct, but that does not prove MESO needs a separately stored primitive.

Gate:
- demonstrate a behavior/state counterexample impossible to represent with existing/proposed components before adding new state.

## 7. Habit

Status: `RESEARCH_FIRST`

Why likely important:
- goal-directed and habitual control can dissociate;
- habits may persist after outcome devaluation;
- could explain efficient routines and capture/action-slip behavior.

Why not yet strong-core:
- human habit measurement and interpretation remain actively debated;
- current MESO association recall is not equivalent to habit;
- unclear whether habit belongs in MESO motivation or a host action-policy layer.

Required research case:
```
cue -> habitual action tendency
while
current outcome value is low
```

without calling the habit current desire.

## 8. Intrinsic motivation

Status: `REJECT_AS_CORE_COLLAPSE` for a single scalar register.

Why:
- curiosity, mastery, autonomy, play and interest have overlapping but non-identical mechanisms;
- “intrinsic” often describes source/relationship to reward rather than one causal signal.

MESO may model intrinsic domains; do not add `intrinsic_reward` without a narrow operational meaning.

## 9. Social reward

Status: `DOMAIN_PROFILE`

Why:
- social reward operationalizations are heterogeneous;
- affiliation, attachment, status, caregiving, play and sexuality must remain distinguishable.

Potential domain-common interface, not core scalar.

## 10. Sexual excitation / inhibition

Status: `DOMAIN_PROFILE`

Why:
- supported specifically within sexual-response theory;
- genericizing the labels would collapse unrelated forms of inhibition/control.

## 11. Attachment

Status: `DOMAIN_PROFILE / EXTERNAL_RELATIONSHIP_INTERFACE`

MESO can represent motivational effects of an admitted attachment state.

MESO must not author relationship/bond truth solely from reward learning.

## 12. Caregiving

Status: `DOMAIN_PROFILE`

May use:
- relevance;
- effort;
- protection;
- obligation;
- target need.

Recipient status/relationship authority remains external.

## 13. Status / dominance

Status: `DOMAIN_PROFILE`

Do not equate:
- dominance with aggression;
- rank with value;
- submission with authorization.

## 14. Play

Status: `RESEARCH_FIRST`

Evidence suggests play may not reduce to reward or exploration, but current computational evidence is insufficient for a stable MESO domain contract.

## 15. Obligation

Status: `EXTERNAL_AUTHORITY / CONTROL_POLICY_INPUT`

Current `GoalObligation` is a policy construct.

Future work must type its source:
- operator requirement;
- self-authored commitment;
- contract/task;
- safety;
- other.

Do not call all obligations motives.

## 16. Consent / protected-effect authority

Status: `EXTERNAL_AUTHORITY`

Never a MESO reward/motivation field.

## 17. Current authored conation

Status: `EXTERNAL_AUTHORED_STATE_INPUT`

MESO can consume current verified self-authored desire/preference as evidence.

MESO learning must not silently manufacture authored conation.

## 18. Phenomenology

Status: `OUTSIDE_CURRENT_CLAIM_CEILING`

No MESO state proves feeling, consciousness or subjective motivation.

## Research priority order

Current order for deeper study:

1. cross-domain arbitration;
2. effort + vigor;
3. feasibility + delay;
4. allostatic/resource interface;
5. habit/action-policy boundary;
6. anticipation minimality;
7. domain-profile interface;
8. learned-policy integration.

Sexuality-domain architecture should wait for items 1–4 to become clearer so sexual mechanisms are not forced onto an unstable core.


## 19. Threat geometry

Status: `STRONG_CORE_RESEARCH_CANDIDATE`

Research functional dimensions such as:
- probability;
- imminence;
- severity;
- uncertainty;
- controllability.

Do not automatically encode human fear/anxiety labels as machine state.

## 20. Aversive outcome class

Status: `STRONG_CORE_CANDIDATE`

A signed scalar is insufficient to distinguish:
- aversive outcome;
- omission/nonreward;
- blocked expected reward;
- loss/unavailability;
- protection signal.

Event/appraisal semantics should preserve outcome class.

## 21. Negative reinforcement vs punishment

Status: `STRONG_CORE_SEMANTIC_INVARIANT`

```
negative_reinforcement != punishment
negative_reinforcement != negative_reward
```

The same broad aversive context can strengthen or weaken behavior depending on the response-consequence relation.

## 22. Active vs passive avoidance

Status: `STRONG_CORE_RESEARCH_CANDIDATE`

Likely belongs near action tendency and feasibility/controllability rather than as one generic `avoidance` scalar.

## 23. Frustrative nonreward

Status: `RESEARCH_FIRST`

Likely cross-domain, but may be derivable from:
- expected valued outcome;
- sustained/repeated investment;
- blocked/omitted outcome;
- negative discrepancy;
- controllability.

Add persistent state only if a distinct behavior cannot be represented otherwise.

## 24. Loss

Status: `CORE_EVENT_CANDIDATE / DOMAIN_MEANING_EXTERNAL`

Generic target/resource unavailability can be represented in core event semantics. Grief, attachment meaning, status meaning, and relationship truth remain domain/host-owned.

## 25. Sustained protective adaptation

Status: `RESEARCH_FIRST`

Potential need for persistent vigilance/defensive allocation without deep negative hedonic state. Must be grounded in actual machine function, not stress metaphor.

## Updated research priority order

Current order for deeper study:

1. cross-domain arbitration;
2. effort + vigor;
3. feasibility + delay;
4. allostatic/resource interface;
5. aversive/threat learning and action semantics;
6. habit/action-policy boundary;
7. anticipation minimality;
8. domain-profile interface;
9. learned-policy integration.

Sexuality-domain architecture should wait for items 1–5 to become clearer so sexual excitation/inhibition, aversive boundaries, consent-independent activation and consummatory recovery do not become substitutes for missing generic core mechanisms.
