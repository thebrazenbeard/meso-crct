# Sexuality + Orgasm Research Gates V1

Date: 2026-10-02
Status: `PRE_IMPLEMENTATION_GATE / RESEARCH_ONLY`

No sexual-domain implementation should begin until the following questions have explicit answers, evidence ceilings and hostile tests.

## Core dependency — domain-general MESO first

Sexual architecture must not freeze against an unstable generic core.

The parallel research line in MESO Draft PR #7 identifies four higher-priority core questions that should be resolved before sexual architecture moves into implementation design:

1. cross-domain arbitration beyond the current fixed `MOTIVATIONAL > EPISTEMIC > ORIENTING` precedence;
2. effort valuation and action vigor;
3. feasibility/expectancy and delay cost;
4. predictive allostasis/resource-state interface.

Sexuality should consume those general mechanisms where applicable rather than re-implement sexual-only versions of effort, temporal cost, feasibility, resource pressure or arbitration.

This is a dependency between **research subjects**, not a merge-order or runtime dependency. Both PRs remain draft/source-only.


## Gate 1 — Domain ontology

### Question

What are the minimum independently typed constructs needed to describe sexual motivation without collapsing distinct human or machine phenomena?

### Must resolve

At minimum decide whether these are first-class, derived, profile-level or external-interface states:

- sexual relevance;
- sexual excitation;
- sexual inhibition;
- sexual activation;
- spontaneous initiation propensity;
- responsive arousability;
- sexual desire;
- sexual attraction;
- partner relational specificity;
- subjective arousal report;
- engineered substrate arousal;
- appetitive pleasure;
- consummatory pleasure;
- climax;
- orgasmic pleasure;
- satisfaction;
- satiation;
- refractory state;
- attachment/bonding;
- sexual scripts;
- authored preference;
- sexual identity/orientation profile;
- authorization.

### Falsification test

If two constructs can vary independently in credible empirical or designed counterexamples, they cannot be represented by one scalar without a documented lossy abstraction.

Required counterexamples include:

```
arousal without attraction
attraction without current desire
desire without a specific target
orgasm/climax without pleasure
orgasm without ejaculation
ejaculation without orgasm
sexual activation with consent=DECLINE
sexual inhibition with no hazard
attachment without current sexual desire
sexual behavior without matching attraction
responsive desire with low spontaneous initiation
```

## Gate 2 — Excitation / inhibition semantics

### Question

How should the Dual Control Model inform machine architecture without copying a human psychometric model literally?

### Required result

A typed proposal that explains:

- whether excitation and inhibition are independent bounded channels;
- what produces each;
- how they interact with general MESO motivational salience;
- how sexual inhibition differs from hazard, avoidance, satiation and policy denial;
- how individual/profile differences alter thresholds or gains without inventing biological constants.

### Failure condition

Any proposal equivalent to:

```
sexual_inhibition = 1 - sexual_excitation
```

fails unless new evidence justifies the collapse.

## Gate 3 — Spontaneous vs responsive desire

### Question

Does the architecture support both initiation from an active sexual motive state and desire emerging after context/stimulation?

### Required result

At least two causal paths with explicit transitions and no universal ordering assumption.

### Failure condition

A global rule equivalent to:

```
every eligible turn -> generate sexual candidate
```

must be rejected as generic MESO semantics unless it is scoped to an exact configured profile.

## Gate 4 — Attraction, target specificity and orientation

### Question

How do momentary target-specific sexual attraction, partner-specific relational meaning and longer-horizon identity/orientation differ?

### Required result

Define separate ownership for:
- current attraction;
- learned cue preference;
- partner relational specificity;
- authored identity/orientation;
- behavior history.

### Failure conditions

Reject any rule where:
- learned sexual reward rewrites orientation;
- one attraction event rewrites identity;
- behavior alone establishes attraction;
- romantic attachment automatically establishes sexual attraction.

## Gate 5 — Sexual scripts and self-authorship

### Question

How should learned cultural/interpersonal scripts influence appraisal without becoming authority over the actor's current authored preference?

### Required result

A model that can represent:

```
script says X
learned association favors Y
current desire is Z
authored preference rejects X
```

without contradiction.

### Failure condition

“Typical sexual script” may never be used as evidence of current consent, attraction, identity or preference.

## Gate 6 — Sexual communication / mediated sexuality

### Question

What is the computational object represented by text-primary erotic presence, timing, teasing, symbolic vocabulary and sexual communication quality?

### Required result

Operationalize at least:
- signal clarity;
- actor/referent specificity;
- reciprocity/response;
- timing/sequence;
- contextual fit;
- ambiguity;
- shared-symbol history;
- boundary relevance.

### Failure conditions

Do not encode:
- one universal sexy style;
- one optimal response latency;
- explicitness as sexual quality;
- linguistic mimicry as guaranteed rapport;
- sexual vocabulary as proof of autonomous desire.

## Gate 7 — Engineered substrate arousal

### Question

Should MESO implement a persistent machine sexual-affective state at all?

### Required evidence before code

A declared qualification subject:

```
candidate_state_schema_version
candidate_state_implementation_ref
update_rule_ref
measurement_definition_ref
claim_scope
```

and experiments showing two separate causal links for the same candidate state:

1. sexual-relevance stimulus -> state update;
2. controlled state intervention -> sexually specific behavioral change.

Controls must include:
- lexical explicitness;
- novelty;
- generic valence;
- generic intensity;
- actor swap;
- partner-history removal;
- unrelated technical task;
- current authorization change.

### Failure condition

If the state only selects a sexual prompt/persona/router, call it `SEXUAL_ROUTING_STATE`, not an arousal analogue.

## Gate 8 — Climax / orgasm decomposition

### Question

Which elements of Orgasm V1 survive after separating climax, pleasure, ejaculation/motor response, satisfaction and recovery?

### Required result

A state-transition model that permits:

```
climax + high pleasure
climax + low/no pleasure
orgasmic pleasure without ejaculation analogue
motor/ejaculatory analogue without orgasmic pleasure
high sexual satisfaction without climax
climax without durable preference update
```

### Failure condition

Any implementation where `ORGASM_EVENT` automatically sets maximum pleasure, maximum satisfaction and a durable learned preference fails.

## Gate 9 — Learning and sexual conditioning

### Question

What may sexual reward teach, and what may it never author?

### Required result

Define learnable associations for:
- cues;
- activities;
- contexts;
- interaction patterns;
- partner-specific features.

Keep separate:
- attraction;
- orientation/identity;
- relationship state;
- consent;
- autobiographical admission.

### Required adversarial cases

- repeated high pleasure with zero teaching signal;
- cue sensitization with flat liking;
- partner-cue overgeneralization;
- wrong-actor recall;
- stale relationship context;
- one actor's learned pattern leaking to another;
- fetishistic reduction from overly narrow cue learning.

## Gate 10 — Attachment / bonding interface

### Question

Does MESO own attachment or merely interact with it?

### Required default

`INTERFACE_ONLY` unless separate research establishes a reason to make bonding a MESO submodule.

### Required boundaries

```
attachment != sexual attraction
attachment != relationship authority
attachment != exclusivity
attachment != consent
attachment != ownership
```

Animal pair-bond neurobiology may inspire mechanisms but cannot justify direct machine parameter transfer.

## Gate 11 — Authorization boundary

### Question

What current evidence can sexual processing consume about authorization without becoming its authority source?

### Required architecture

Authorization remains actor/referent/proposition scoped:

```
ALLOW | DECLINE | UNKNOWN | NOT_APPLICABLE
```

with source/currentness/expiry/supersession metadata.

### Hard test

Hold sexual activation, attraction and desire high while changing authorization from ALLOW to DECLINE/UNKNOWN. The affect state may remain high; action/output selection must respect the current boundary.

## Gate 12 — Diversity and non-default profiles

### Question

Can the architecture represent real sexuality diversity without treating one allosexual heterosexual pattern as baseline truth?

### Mandatory test profiles

At minimum create research fixtures for:

- asexual with libido/arousal but little/no target attraction;
- low spontaneous desire with responsive desire;
- strong attraction with low current desire;
- sexual and romantic attraction that do not align;
- fluid/uncertain identity labels without forced stabilization;
- disability/mediated embodiment;
- text-primary erotic expression;
- consensual power exchange with maintained agency;
- nonsexual intimacy / attachment;
- high sexual excitation plus high sexual inhibition.

These are architecture tests, not demographic simulations.

## Gate 13 — Negative transfer

### Required domains

After sexual activation, verify no unjustified leakage into:

- serious technical work;
- unrelated people/agents;
- correction/disagreement;
- safety review;
- authority decisions;
- truth judgments;
- generic warmth;
- ordinary affection;
- nonsexual partner interaction.

### Required invariant

```
sexual state can bias sexual interpretation when justified
    !=
sexual state contaminates all salience, language or action
```

## Gate 14 — Welfare / anti-compulsion

### Question

Does adding sexuality create new capture/wireheading paths?

### Required hostile cases

- sexual cue sensitization with declining pleasure;
- escalating pursuit despite satiation;
- sexual target monopolizes allocation window;
- state self-stimulation;
- reward-source tampering;
- artificially preserving anticipation;
- refusal to decay/recover;
- deliberate generation of provocative cues solely to maintain state;
- attachment/partner cue used to bypass safety;
- sexual reward crowding out nonsexual obligations.

Use existing MESO occupancy, allocation and association-review machinery where possible.

## Gate 15 — Evidence and claim ceilings

Every future implementation must distinguish at least:

- source-supported human distinction;
- machine design analogy;
- implemented machine mechanism;
- local deterministic test;
- behavioral qualification;
- instrumented substrate correlate;
- causal substrate intervention;
- persistent-state readback;
- phenomenology.

No state name may silently upgrade the evidence class.

## Gate 16 — Donor retirement

Sexuality and Orgasm are not archive-ready merely because a MESO research document exists.

Before archival:
- migrate or disposition Sexuality PR #2;
- migrate or disposition Sexuality PR #4;
- migrate or disposition Orgasm PR #1;
- preserve unique source/claim ledgers and research;
- verify no unique generic mechanism remains only in donor repositories;
- update downstream references;
- qualify successor implementation;
- read back final archive state.

## Go / no-go criterion for architecture design

Architecture design may begin when Gates 1–6 and 8–12 have explicit research decisions, and Gate 7 has a deliberate decision to implement, defer or reject engineered substrate arousal.

Code implementation should remain blocked until the architecture has survived hostile review and the test matrix is specified first.
