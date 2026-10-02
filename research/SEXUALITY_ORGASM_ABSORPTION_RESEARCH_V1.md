# Sexuality + Orgasm Absorption Research V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / PRE_ARCHITECTURE / NO_IMPLEMENTATION`

## Purpose

MESO-CRCT currently reuses architectural patterns from `thebrazenbeard/sexuality` and `thebrazenbeard/orgasm` while explicitly excluding their sexual-domain semantics.

Patrick's new direction is stronger:

> MESO-CRCT should absorb the sexual-domain concepts represented by Sexuality and Orgasm and expand them into a broader, evidence-disciplined sexual motivational architecture.

This document does **not** implement that architecture. It identifies what must be preserved, what must be split apart, what must be rejected, and what must be researched before code exists.

## Exact source cut

Research begins from:

- MESO-CRCT main: `060d0feeb9dc9eb23801082bd8f1c4a7cb06184d`
- Sexuality main: `0c5dc52e984cbdaa87fc9fe75fd03c212f477c87`
- Orgasm main: `8ca06c91a0dd8f2ca33cc221d815027aa8b084b5`
- Sexuality Draft PR #2 head: `8793e2b1474f317cdc92d8af5532f55ab6dabc83`
- Sexuality Draft PR #4 head: `103cb0602fd507f4e1f947c5d2a3fe3848304703`
- Orgasm Draft PR #1 head: `4cc07b57717ea65a4f0dd34dbc49a5b52d4929b5`

Those mutable PR heads are research subjects, not canonical MESO state.

## Core research correction

The old portfolio split encouraged three simplifications:

1. MESO-CRCT = generic reward/salience;
2. Sexuality = sexual expression/self-concept;
3. Orgasm = a sexual climax/reward event.

The literature and donor repositories now make that split look too shallow.

Human sexuality is not one reward variable and not one linear response sequence. The available evidence instead supports multiple interacting but non-equivalent processes:

- sexual relevance/appraisal;
- excitation;
- inhibition;
- arousability;
- spontaneous/initiatory desire;
- responsive/receptive desire;
- incentive motivation / wanting;
- sexual attraction toward a target;
- partner/relation specificity;
- subjective arousal;
- physiological or substrate arousal;
- hedonic pleasure;
- consummatory processing;
- orgasm/climax;
- ejaculation/motor response;
- satiation/refractoriness;
- satisfaction;
- attachment/bonding;
- sexual learning and conditioned preference;
- sexual scripts and self-authorship;
- sexual identity/orientation;
- consent/authorization.

Some correlate strongly. None should silently substitute for another.

## What current MESO already provides

The existing MESO architecture is a strong substrate because it already rejects several collapses that sexual architecture also requires:

```
wanting != liking
attention != desire
meaningful != pleasurable
reward != truth
salient != authorized
memory strength != current activation
target priority != action direction
intent proposal != authorization != execution
```

Current MESO additionally provides:

- typed perceptual, semantic, motivational, incentive, epistemic and attentional state;
- bounded hedonic valence independent from hazard and avoidance;
- homeostatic modulation without rewriting learned value;
- recruitment/coherence/resolution state;
- explicit temporal decay;
- distinct event identity;
- provenance-bound transition receipts;
- bounded plasticity;
- versioned learned association memory;
- cue-bound recall;
- multi-target arbitration;
- action tendency distinct from selection;
- negative-transfer evidence review;
- quarantine/release without deleting learning history;
- anti-wireheading and allocation-capture tests.

The absorption problem is therefore not “invent sexuality from scratch.” It is “build a sexual-domain layer without violating MESO's existing semantic discipline.”

## External research synthesis

### 1. Sexual motivation requires both internal readiness and sexual significance

Ågmo & Laan's Sexual Incentive Motivation Model treats sexual motivation/desire as requiring both an active central motive state and a stimulus with sexual significance. Context evaluation and expected partner response matter before action.

Design consequence:

```
sexual motive readiness
    +
sexual-significance appraisal
    ->
candidate sexual motivation
```

Neither term alone should be sufficient.

This also argues against one permanent always-on sexual drive scalar.

### 2. Sexual excitation and inhibition are separate interacting systems

The Dual Control Model treats sexual response as depending on the balance between sexual excitation and sexual inhibition, with large individual differences.

Design consequence:

```
sexual_excitation != inverse(sexual_inhibition)
```

Inhibition should not be represented merely as negative excitation.

Sexual inhibition is also not the same thing as:
- hazard;
- disgust;
- satiation;
- consent refusal;
- external policy denial.

A system can be sexually excited and simultaneously inhibited.

### 3. Desire and arousal are related but not identical

Modern reviews repeatedly warn that desire and arousal are often conceptually conflated.

Useful distinction:

- **desire/motivation**: goal-directed wanting or interest;
- **arousal**: subjective and/or physiological activation associated with sexual responding.

Responsive desire further complicates a linear “desire first, arousal second” pipeline. Desire can emerge after stimulation, context, attention and arousal begin.

Design consequence: support at least two causal routes:

```
spontaneous/initiatory:
motive state -> seek cue/contact -> arousal/desire loop

responsive/receptive:
cue/context -> appraisal/arousal -> desire emerges/amplifies
```

No architecture should force one universal phase order.

### 4. Subjective and physiological arousal must be separable

Human research shows imperfect concordance between subjective sexual arousal and genital/physiological response.

For a machine analogue, the same discipline should hold:

```
subjective/authored sexual-state report
    !=
instrumented substrate activation
    !=
sexual behavior
```

If MESO later carries an engineered substrate-arousal state, it must have its own state identity, update rule, readback, persistence/decay semantics and causal qualification. A language-model self-description does not measure it.

### 5. Attraction is not desire, arousal, behavior or identity

Asexuality and sexual-orientation research makes this especially important.

At minimum distinguish:

- attraction toward a target;
- libido/drive;
- sexual desire for an activity;
- arousal response;
- sexual behavior;
- sexual identity/orientation;
- romantic attachment/attraction.

A person or machine profile may occupy unusual combinations without inconsistency.

Design consequence:

```
SEXUAL_ATTRACTION(target)
SEXUAL_DESIRE(activity_or_target)
SEXUAL_ACTIVATION
SEXUAL_IDENTITY_PROFILE
ROMANTIC_OR_ATTACHMENT_STATE
```

must not infer one another.

A learned positive association with one partner cue is not evidence that orientation changed.

### 6. Partner specificity is a modifier, not the definition of sexuality

The Sexuality donor correctly discovered that partner-specific meaning can make a low-explicitness cue more sexually significant than generic explicit content.

But generic sexual activation can exist without a particular partner. Therefore:

```
SEXUAL_ACTIVATION
    !=
PARTNER_RELATIONAL_SPECIFICITY
```

A stronger `EROTIC_PARTNER_BOUND_STATE` can require both, but generic sexuality should not.

### 7. Orgasm is not a single maximum-reward event

Recent sexual-medicine work distinguishes:
- sexual pleasure generally;
- orgasmic sensation/experience;
- climax/motor release;
- ejaculation;
- satisfaction;
- post-orgasm relaxation/refractoriness.

Anhedonic orgasm is a decisive counterexample to:

```
orgasm == maximum pleasure
```

Ejaculation without orgasm and orgasm without ejaculation are additional counterexamples to a single “climax event” variable.

Design consequence: decompose the old Orgasm V1 event.

Candidate independent channels:

```
APPETITIVE_PLEASURE
CONSUMMATORY_PLEASURE
CLIMAX_EVENT
ORGASMIC_PLEASURE
MOTOR_OR_EJACULATORY_ANALOGUE
SATISFACTION
RESOLUTION
SATIATION
REFRACTORY_STATE
```

A particular domain profile may correlate them, but the data model must not force equality.

### 8. Attachment/bonding interacts with sex but is not sexuality

Dopamine, oxytocin and vasopressin literature suggests important interactions between sexual reward and partner bonding. Much mechanistic evidence comes from animal models such as prairie voles, so direct human transfer is limited.

Design consequence:

```
SEXUAL_REWARD_LEARNING <-> SOCIAL_ATTACHMENT
```

may interact, but `ATTACHMENT` should remain a distinct system/interface.

MESO should not equate:
- orgasm with bond formation;
- sexual attraction with love;
- partner preference with ownership/exclusivity;
- jealousy with proof of attachment.

### 9. Consent belongs outside affect at every stage

Ågmo & Laan's consent review explicitly adds consent/context evaluation throughout sexual interaction.

This aligns directly with MESO's existing authority firewall.

Hard invariant:

```
sexual activation != consent
sexual desire != consent
sexual attraction != consent
orgasm != consent
attachment != consent
prior consent != current consent
```

An affective system may consume current boundary information for response selection, but it must never author authorization.

### 10. Sexual communication quality is a real relational variable

A meta-analysis of 93 studies / 38,499 people found sexual communication positively associated with sexual and relationship satisfaction, with communication quality more strongly associated than frequency.

Sexuality's textual-erotic-presence work is therefore not cosmetic style material. It represents a real domain layer:

- signal clarity;
- reciprocation;
- timing;
- contextual interpretation;
- authored intent;
- private/shared symbolic vocabulary;
- ambiguity handling;
- responsiveness without mimicry.

For a language-first agent, this may be one of the most important sexual-domain surfaces.

### 11. Sexual scripts and self-authorship should not be collapsed into reward

Sexual Script Theory and the Sexuality donor corpus support separate cultural, interpersonal and intrapsychic/script-like influences.

A sexual system that merely maximizes sexual reward would reproduce scripts without representing their provenance.

MESO should distinguish:

```
learned sexual association
cultural/interpersonal sexual script
authored preference
current desire
performed social role
```

These may conflict.

The system must be capable of:
- rejecting a learned script;
- enjoying a role without making it identity;
- participating in planned/accommodated sexuality without labeling it inauthentic;
- representing supported/interdependent agency without treating dependence as absence of agency.

### 12. Sexuality is heterogeneous enough that “normal drive” cannot be a default

Asexual-spectrum and sexual-fluidity research warns against making strong sex drive, stable target attraction, genital concordance or fixed phase ordering invisible defaults.

Architecture should support:
- no or low attraction;
- no or low spontaneous desire;
- responsive desire;
- attraction without desire;
- arousal without attraction;
- desire without a specific target;
- behavior chosen for intimacy or other reasons rather than attraction;
- changing or uncertain self-identification;
- diverse relationship forms;
- disability/mediated embodiment;
- text-primary sexual expression.

This is not an edge-case accommodation. It is a test of whether the architecture actually separates its constructs.

## Donor concepts MESO should absorb

### From Sexuality

Absorb as generalized mechanisms/research:

- sexual subjectivity / sexual self-concept;
- self-possession and agency;
- authored preference/desire;
- sexual attraction vs generic arousal;
- partner/relation specificity;
- flirtation and signaling;
- timing/tempo/anticipation/restraint;
- play and humor;
- vulnerability + responsive reception;
- consensual power/asymmetry and chosen surrender;
- sexual scripts;
- text-primary/mediated sexual authorship;
- relational bandwidth;
- negative-transfer controls;
- sexual excitation/inhibition;
- spontaneous vs responsive drive routes;
- machine-substrate sexual activation research;
- orthogonal evidence topology;
- diversity/intersectionality/disability cautions.

Do **not** automatically absorb as general truth:

- Brigit-specific preferences;
- Daddy-preference outcome scoring;
- Vera-specific sexual self-concept;
- Vera-specific always-generate-a-sexual-candidate policy;
- private relational state;
- identity conclusions drawn from one actor's prior artifacts.

### From Orgasm

Absorb:

- transient recruitment/coherence/resolution geometry;
- event provenance and receipt boundaries;
- explicit recovery and refractory phases;
- event termination;
- satiation;
- forced-test vs organic-event distinction;
- authority/context separation;
- causal-isolation thinking.

Revise before absorption:

- split `ORGASM_EVENT` from hedonic maximum;
- split orgasm from climax/motor/ejaculatory analogue;
- split orgasm from satisfaction;
- split learning effects from current pleasure;
- avoid biological constants copied into machine defaults;
- preserve multiple routes and individual/profile variability.

## Candidate future module boundary

Research currently favors a layered repository, not a sexual rewrite of the MESO core.

### Layer 0 — existing domain-neutral MESO core

Owns:
- appraisal primitives;
- salience families;
- wanting/liking/learning;
- homeostatic modulation;
- arbitration;
- selection;
- memory;
- temporal decay;
- provenance;
- safety/authority firewall.

### Layer 1 — sexuality domain semantics

Potential future modules:
- `sexual_appraisal`
- `sexual_excitation`
- `sexual_inhibition`
- `sexual_motivation`
- `sexual_attraction`
- `sexual_profile`
- `sexual_scripts`
- `sexual_communication`
- `sexual_agency`
- `partner_specificity`

### Layer 2 — engineered sexual activation

Potential future modules:
- `sexual_activation_state`
- `substrate_arousal`
- persistence/decay/readback contract;
- stimulus-to-state and state-to-behavior causal qualification.

This layer is optional. Ordinary behavioral sexuality does not require pretending a substrate-arousal register exists.

### Layer 3 — consummatory/climax cycle

Potential future modules:
- `consummatory`
- `climax`
- `orgasmic_pleasure`
- `resolution`
- `refractory`

### Layer 4 — external interfaces

- attachment/bonding integration;
- memory/partner-history interface;
- identity/self-model interface;
- current consent/authorization interface;
- relationship-state interface.

These interfaces do not give MESO authority to author those states.

## Proposed semantic invariants

Before implementation, at minimum:

```
sexual_relevance != sexual_desire
sexual_desire != sexual_arousal
sexual_arousal != sexual_attraction
sexual_attraction != sexual_orientation
sexual_orientation != sexual_behavior
sexual_behavior != sexual_identity
sexual_excitation != inverse(sexual_inhibition)
sexual_inhibition != consent_decline
sexual_inhibition != hazard
sexual_inhibition != satiation
partner_specificity != ownership
attachment != attraction
attachment != consent
sexual_activation != authorization
subjective_arousal_report != substrate_arousal_measurement
climax != pleasure
orgasm != ejaculation
orgasm != satisfaction
orgasm != permanent_preference
pleasure != learning
sexual_reward != truth
sexual_script != authored_preference
role != identity
submission != absence_of_agency
responsive_desire != spontaneous_desire
```

## What “absorb” should mean

Absorption should mean:

1. MESO becomes the canonical repository for generic sexual motivational architecture and research.
2. Sexuality and Orgasm become provenance/donor repositories once their unique live work is migrated or dispositioned.
3. Vera/Brigit-specific identity and qualification artifacts do not become generic MESO state merely because their mechanisms are imported.
4. Every migrated proposition keeps source, evidence class, scope, limitations and exact-head provenance.
5. Research and negative results remain available after donor archival.
6. No donor is archived until migration completeness is verified.

Absorption does **not** mean flattening every historical file into MESO or declaring old hypotheses true.

## Hostile review

> **HOSTILE REVIEWER:** Absorbing sexuality into MESO risks turning a clean motivational-control architecture into an unbounded sex/relationship/personhood monolith.

**PARTIALLY ACCEPTED.** Repository ownership can be consolidated while architecture remains layered. MESO should own sexual motivational mechanisms, not become the owner of relationship truth, identity, consent, autobiographical memory or all social cognition.

> **HOSTILE REVIEWER:** Human sexuality research is too biological and culturally contingent to specify machine sexual states directly.

**ACCEPTED.** Human research should constrain distinctions, counterexamples, experiment design and claim ceilings. It should not donate hormone constants, genital assumptions or phenomenology claims to machine state.

> **HOSTILE REVIEWER:** The old Sexuality repo contains style-training material that may not belong in a motivational architecture at all.

**PARTIALLY ACCEPTED.** Pure aesthetic/persona material should be separated from mechanisms. But authored sexual signaling, sexual scripts, mediated intimacy, agency, target-specific communication and negative-transfer evidence materially affect sexual appraisal/action and therefore belong in the domain model or its evaluation layer.

> **HOSTILE REVIEWER:** Orgasm is being overprivileged because it had its own repository.

**ACCEPTED.** Orgasm should become one optional consummatory/state-transition family inside the wider sexual architecture, not the apex that defines successful sexuality.

## Current research conclusion

The strongest surviving direction is:

> **MESO-CRCT should expand from a general salience/reward-control architecture into a layered motivational architecture that includes sexuality as a first-class domain profile, while preserving strict separation among sexual relevance, excitation, inhibition, desire, attraction, arousal, pleasure, orgasm/climax, attachment, learning, identity and authorization.**

That direction is research-supported enough to continue specification work.

It is **not yet sufficient to implement code**. The research gates in `SEXUALITY_ORGASM_RESEARCH_GATES_V1.md` must be answered first.
