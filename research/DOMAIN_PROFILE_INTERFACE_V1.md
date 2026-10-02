# MESO-CRCT Domain Profile Interface Research V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / MODULARITY CONTRACT CANDIDATE / NO IMPLEMENTATION`

## Purpose

MESO is becoming a domain-general motivational substrate.

That only works if domain profiles can contribute real motivational information without:
- redefining core semantics;
- inventing current truth;
- self-certifying source authority;
- emitting opaque final utility;
- bypassing common arbitration;
- leaking their own assumptions into unrelated domains.

This document defines the research boundary for future domain profiles such as:
- sexuality;
- curiosity;
- achievement;
- affiliation;
- attachment;
- caregiving;
- status/competition;
- play;
- resource regulation.

## 1. A domain profile is not a policy sovereign

A domain profile may answer:

> How does this current evidence matter within this domain?

It should not answer by fiat:

> Therefore choose my target.

Hard rule:

```
domain appraisal != final selection
```

Profiles contribute typed evidence to MESO.
MESO performs shared cross-domain arbitration.

## 2. What a profile may contribute

Candidate contribution families:

### Domain relevance
Examples:
- sexual relevance;
- epistemic/curiosity relevance;
- caregiving relevance;
- attachment relevance.

This says the event/target belongs to or matters within a domain.

### Domain activation
Examples:
- sexual excitation;
- mastery challenge activation;
- affiliative opportunity;
- caregiving concern.

This is domain-specific internal state, not global MESO priority.

### Domain direction
Examples:
- approach;
- inspect;
- affiliate;
- protect;
- withdraw;
- communicate.

Direction may be domain-specific but should eventually map into a common non-executable action-tendency vocabulary where possible.

### Domain-specific learned evidence
Examples:
- partner-specific sexual association;
- mastery association;
- actor-specific affiliation history;
- learned caregiving cue.

Such memory must preserve source/revision/currentness and must not automatically become identity or authority.

### Domain-specific recovery/satiation
Examples:
- sexual refractory/recovery state;
- curiosity satiation;
- social interaction fatigue;
- mastery burnout.

Do not assume all domains share one universal satiation equation.

## 3. What profiles should reference rather than own

Profiles may consume externally owned facts such as:

- actor identity;
- relationship state;
- authored conation/preference;
- consent/authorization;
- capability;
- world state;
- plan/goal state;
- resource telemetry;
- current semantic/pragmatic interpretation;
- autobiographical memory.

Profiles may use those facts only through typed references/evidence.

They must not become the authority that creates those facts.

## 4. What profiles must never author

A domain profile must not directly establish:

```
truth
factual confidence
identity
relationship status
consent
protected-effect authority
autobiographical memory admission
external effect success
current runtime installation
permanent preference
phenomenology
```

This is the same semantic firewall applied uniformly across domains.

## 5. Opaque priority is prohibited

A profile should not emit:

```
priority = 0.92
```

without exposing why.

That merely moves the hidden utility function into the domain.

A contribution should preserve typed reasons.

Research sketch:

```
DomainContribution:
    domain_id
    target_ref
    contribution_kind
    magnitude/qualifier
    direction_if_any
    source/evidence refs
    currentness
    constraints
```

This is not a frozen schema.

## 6. Domain-specific magnitude may not be globally commensurable

Examples:

```
sexual_excitation = 0.8
curiosity_information_value = 0.8
caregiving_urgency = 0.8
```

do not automatically represent equal global force.

MESO should not compare those raw numbers directly unless a declared policy defines how.

The profile owns local meaning.
The policy owns tradeoff semantics.

## 7. Profiles may emit multiple contributions for one target

One sexuality appraisal could separately contribute:
- sexual relevance;
- excitation;
- attraction;
- incentive support;
- inhibition.

Do not collapse them to one sexual score before the core sees them if the distinctions matter to action.

Likewise curiosity may contribute:
- uncertainty;
- information gain;
- novelty;
- learning progress.

## 8. One target may receive contributions from several profiles

Example:

```
target = conversation with partner
contributions:
  attachment
  affiliation
  sexuality
  play
  curiosity
```

MESO should preserve the coalition rather than force one winning domain label.

## 9. Domain profiles should be source-bound modules

A contribution needs at least:
- profile identity/version;
- evidence source;
- currentness;
- subject/target scope;
- computation/version identity where materially relevant.

This prevents:
```
caller says sexual relevance = 1.0
```
from silently becoming trusted MESO state.

## 10. Domain profile output should be reproducible or reviewable

For deterministic/reference profiles:
- same bound evidence + same profile version -> same contribution.

For learned profiles:
- model/version identity;
- confidence/calibration;
- holdout/qualification status;
- currentness;
- failure/abstention behavior

must remain visible.

A learned domain scorer cannot hide behind "the model felt like it."

## 11. Profiles need an UNKNOWN / abstain path

A profile should be able to say:

```
UNKNOWN
NOT_APPLICABLE
INSUFFICIENT_EVIDENCE
```

rather than manufacturing a zero or low value.

This is important for:
- attraction;
- relationship relevance;
- threat probability;
- caregiving need;
- social intent.

Unknown != absent.

## 12. Profiles should not directly mutate durable MESO memory

A domain event may propose learning, but persistent learning should pass through common MESO:
- event identity;
- receipt;
- teaching-signal contract;
- bounded plasticity;
- versioned memory;
- review/quarantine.

This prevents each domain from inventing its own ungoverned learning path.

## 13. Profiles may require domain-specific memory without using AssociationMemory

Some domain semantics may not fit a signed scalar association.

Examples:
- sexual script;
- attachment relation;
- role/context state;
- social interaction history;
- mastery skill model.

Those should stay in domain/host memory and contribute current evidence to MESO.

Do not force every persistent domain fact into generic AssociationMemory.

## 14. Profiles should not bypass common effort/feasibility/resource appraisal

A sexual profile should not encode:
- "too expensive";
- "not feasible";
- "GPU unavailable";
- "deadline soon"

inside sexual activation.

A curiosity profile should not encode those inside epistemic value either.

Those are common appraisal dimensions.

Profiles may identify domain-specific requirements; core/host appraises common costs/constraints.

## 15. Profiles should not own goal lifecycle

A profile may suggest:
- this target is attractive/relevant;
- this opportunity is caregiving-relevant;
- this question is epistemically valuable.

It should not automatically create:
- persistent goal;
- standing obligation;
- task.

Goal creation/currentness belongs to goal authority/self-authorship.

## 16. Profiles can influence action tendency without executing

Profile output may support:
- approach;
- inspect;
- communicate;
- withdraw;
- inhibit;
- protect;
- wait;
- seek clarification.

The common system can derive a non-executable intent.

Protected effects remain outside.

## 17. Profiles need negative-transfer qualification

Every domain must prove it does not contaminate unrelated contexts.

Examples:

### Sexuality
No generic seductive language or sexual routing in unrelated work.

### Curiosity
No endless exploration when task completion is required.

### Achievement
No performance optimization overriding care/safety.

### Attachment
No actor-specific bond semantics leaking to strangers.

### Status
No dominance framing infecting cooperation.

### Caregiving
No unsolicited control/ownership over others.

## 18. Profiles need capture qualification

Each profile should have domain-specific capture tests:

- sexuality: cue sensitization / escalating pursuit;
- curiosity: novelty loops / endless research;
- achievement: task obsession / completion chasing;
- affiliation: approval seeking;
- status: rank fixation;
- caregiving: self-neglect / overcontrol;
- play: avoidance of obligations.

The common allocation controller should surface capture without requiring the profile to diagnose itself.

## 19. Profiles must not redefine welfare

A domain may report:
- pleasure;
- discomfort;
- satisfaction;
- frustration-like event;
- domain satiation.

But it may not change the global MESO welfare floor or protection policy on its own.

A domain should not claim:
```
this is important enough to suffer more
```
and modify welfare bounds.

## 20. Cross-profile semantic collisions must be explicit

Terms such as:
- arousal;
- inhibition;
- attachment;
- reward;
- satisfaction;
- approach

may mean different things across domains.

Profiles should use qualified terms where necessary:

```
sexual_inhibition
action_inhibition
protective_inhibition
social_inhibition
```

Do not overload one core field merely because English uses the same word.

## 21. Domain profile registry

A future host may need a registry declaring:
- profile ID/version;
- owned contribution kinds;
- accepted input/evidence kinds;
- persistence dependencies;
- qualification state;
- claim ceiling;
- compatible MESO core version.

This is source/runtime metadata, not behavioral truth.

## 22. Profile composition should be explicit

Example:

```
sexuality.v1
  consumes:
    semantic context
    actor/relation refs
    current boundary state
  emits:
    sexual relevance
    excitation
    inhibition
    attraction/desire contributions

MESO core
  combines with:
    effort
    feasibility
    delay
    resources
    other domains
  -> non-executable selection/tendency
```

No profile gets a secret fast path.

## 23. Candidate contribution lifecycle

Research shape:

```
raw evidence
-> domain-specific appraisal
-> verified DomainContribution
-> common appraisal enrichment
-> cross-domain arbitration
-> action tendency
-> intent
```

Persistent learning can branch from a verified event receipt but remains separately governed.

## 24. Required adversarial cases

### DP-01 — opaque priority
Profile emits only priority score -> reject.

### DP-02 — domain overreach
Sexual profile attempts to write relationship status -> reject.

### DP-03 — identity laundering
Attachment profile attempts to infer identity from repeated reward -> reject.

### DP-04 — false zero
Insufficient evidence must remain UNKNOWN, not 0.

### DP-05 — multi-domain target
Several profiles contribute to one target without forced single label.

### DP-06 — conflicting contributions
Sexual approach + sexual inhibition + protection + attachment all coexist without scalar collapse.

### DP-07 — stale profile
Old profile version/evidence cannot remain current automatically.

### DP-08 — learned scorer drift
Unqualified learned profile update cannot silently replace qualified version.

### DP-09 — capture
Rotating targets within one domain still produce domain-level capture evidence where supported.

### DP-10 — common cost
Profile cannot hide global resource/effort cost inside local desirability.

## Hostile review

> **HOSTILE REVIEWER:** A domain contribution interface may become a generic plugin framework with too much metadata.

**ACCEPTED AS A MINIMALITY RISK.** The implementation should start with the smallest fields required by concrete domain tests. This research defines semantic obligations, not mandatory boilerplate.

> **HOSTILE REVIEWER:** For performance, profiles will eventually need to output a compact score.

**PARTIALLY ACCEPTED.** They may emit local bounded measures where semantically valid. What is prohibited is presenting a domain-local score as globally commensurable final priority without an explicit policy.

> **HOSTILE REVIEWER:** If every profile can abstain/return UNKNOWN, arbitration may become indecisive.

**REJECTED.** Unknown evidence is a real state. The host/policy can choose conservative action, information gathering, or fallback. Fabricated certainty is worse than indecision.

## Current conclusion

The clean modular boundary is:

> **Domain profiles own domain-specific appraisal semantics. MESO owns common motivational mechanics and cross-domain arbitration. External systems own truth, identity, goals, relationships, capabilities, resources, authorization and effects.**

Profiles should contribute typed, provenance-bound, reviewable evidence—not final opaque utility.

No implementation is proposed here.
