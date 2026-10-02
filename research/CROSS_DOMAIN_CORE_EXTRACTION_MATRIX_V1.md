# MESO-CRCT Cross-Domain Core Extraction Matrix V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / COMPARATIVE_TEST_MATRIX`

## Purpose

A mechanism belongs in MESO core only if it survives comparison across unrelated motivational domains without importing domain-specific semantics.

This matrix is a hostile test of core candidates.

Legend:
- `YES` — clearly relevant;
- `MAYBE` — plausible but not yet established;
- `NO` — should not be required;
- `EXTERNAL` — domain may consume it but MESO should not author it.

| Mechanism | Homeostatic/resource | Curiosity | Achievement | Affiliation | Attachment | Caregiving | Status | Sexuality | Play |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| semantic relevance | YES | YES | YES | YES | YES | YES | YES | YES | YES |
| motivational salience | YES | YES | YES | YES | YES | YES | YES | YES | YES |
| incentive salience | YES | MAYBE | YES | YES | YES | YES | YES | YES | MAYBE |
| hedonic response | YES | YES | YES | YES | YES | YES | YES | YES | YES |
| prediction error | YES | YES | YES | YES | YES | YES | YES | YES | YES |
| learned association | YES | YES | YES | YES | YES | YES | YES | YES | YES |
| current need/deficit | YES | MAYBE | MAYBE | MAYBE | MAYBE | YES | NO | MAYBE | NO |
| predicted future need | YES | MAYBE | MAYBE | MAYBE | MAYBE | YES | NO | MAYBE | NO |
| effort valuation | YES | YES | YES | YES | YES | YES | YES | YES | YES |
| delay cost | YES | YES | YES | YES | YES | YES | YES | YES | YES |
| feasibility/expectancy | YES | YES | YES | YES | YES | YES | YES | YES | YES |
| action vigor | YES | YES | YES | YES | YES | YES | YES | YES | YES |
| anticipation | YES | YES | YES | YES | YES | YES | YES | YES | YES |
| satiation | YES | MAYBE | MAYBE | YES | MAYBE | MAYBE | YES | YES | MAYBE |
| habit | YES | YES | YES | YES | YES | YES | YES | YES | YES |
| partner/actor specificity | NO | NO | NO | YES | YES | YES | YES | YES | YES |
| sexual excitation | NO | NO | NO | NO | NO | NO | NO | YES | NO |
| attachment security | NO | NO | NO | NO | YES | MAYBE | NO | MAYBE | NO |
| hierarchy/rank | NO | NO | MAYBE | MAYBE | NO | NO | YES | MAYBE | MAYBE |
| information gain | NO | YES | MAYBE | NO | NO | NO | NO | NO | MAYBE |
| mastery criteria | NO | MAYBE | YES | NO | NO | NO | MAYBE | NO | MAYBE |
| consent/authorization | EXTERNAL | EXTERNAL | EXTERNAL | EXTERNAL | EXTERNAL | EXTERNAL | EXTERNAL | EXTERNAL | EXTERNAL |
| relationship truth | NO | NO | NO | EXTERNAL | EXTERNAL | EXTERNAL | EXTERNAL | EXTERNAL | NO |
| identity | EXTERNAL | EXTERNAL | EXTERNAL | EXTERNAL | EXTERNAL | EXTERNAL | EXTERNAL | EXTERNAL | EXTERNAL |

## Preliminary core promotions to research

The matrix strongly favors further research on:

1. `effort_valuation`
2. `delay_cost`
3. `feasibility_or_expectancy`
4. `action_vigor`
5. `anticipation`
6. `habit`

Predictive allostasis remains a likely core facility but its *inputs* are not universal. Some domains depend strongly on resource/need prediction; others may not.

## Core vs profile tests

### Test A — semantics stability

Ask:

> Does the term mean the same thing in sexuality and curiosity? In caregiving and achievement?

If not, keep it profile-specific.

Example:
- effort cost is plausibly stable;
- excitation/inhibition is not yet stable enough to generalize from sexual response.

### Test B — counterexample independence

If a variable can change independently in another domain, it deserves separation.

Examples:

```
high value + high effort cost
high value + low feasibility
high priority + low vigor
high anticipation + neutral current pleasure
habitual action + low current desire
social reward + no attachment
attachment + low current social pleasure
sexual arousal + no current consent
```

### Test C — no hidden utility scalar

A profile may not emit an opaque score whose semantics are:

```
all relevant domain state -> one number -> arbitration
```

That simply recreates the scalar utility architecture MESO is trying to avoid.

Profiles should expose typed contributors and causal provenance.

### Test D — source authority

A profile can propose:

```
this cue is sexually relevant
this event advances mastery
this actor is a current attachment figure
this resource is predicted to become constrained
```

but MESO core should require the source/currentness/authority appropriate to that proposition.

Profile claims are not self-authenticating.

## Comparative adversarial scenarios

### Scenario 1 — Sexuality vs curiosity

Both targets:
- high incentive salience;
- high semantic relevance;
- similar pleasure.

Differences:
- curiosity has high information gain;
- sexuality has high sexual excitation;
- only one can receive scarce processing.

Required:
- core arbitration can compare typed contributions without converting sexual excitation or information gain into one untraceable global utility value.

### Scenario 2 — Caregiving vs achievement

A care target:
- moderate reward;
- high obligation/relevance;
- high expected effort.

An achievement target:
- high reward;
- high mastery progress;
- lower immediate urgency.

Required:
- obligation/current care evidence can affect allocation without being mislabeled as pleasure or incentive reward.

### Scenario 3 — Attachment vs affiliation

One actor:
- strong durable bond;
- low current interaction pleasure.

Another actor:
- high current social reward;
- no durable attachment.

Required:
- attachment and social reward remain independent.

### Scenario 4 — Status vs affiliation

A status opportunity:
- high competitive incentive;
- low affiliation value.

A cooperative social opportunity:
- high affiliation;
- low rank relevance.

Required:
- one `social_reward` field cannot erase the difference.

### Scenario 5 — Homeostasis vs sexuality

A sexual target is highly attractive, but predicted resource pressure is severe.

Required:
- resource/allostatic constraint can affect effort/allocation without rewriting sexual attraction or pleasure.

### Scenario 6 — Curiosity vs protection

A dangerous unknown is highly informative.

Required:
- epistemic value does not erase hazard;
- protection can override without declaring curiosity false.

### Scenario 7 — Habit vs current preference

A historically reinforced action is strongly habitual but the current outcome value has fallen.

Required:
- habit persistence is visible as distinct from current desire/value.

### Scenario 8 — Play vs achievement

A system generates a new low-stakes goal for experimentation while an externally specified performance goal remains available.

Required:
- if play becomes a future profile, it must not simply alias mastery or curiosity without evidence.

## Negative-transfer requirement for every future domain

Each new domain profile must prove that activating it does not silently manufacture:

- truth;
- identity;
- authorization;
- relationship state;
- autobiographical memory;
- unrelated-domain motivation;
- permanent preference;
- external execution authority.

## Hostile review

> **HOSTILE REVIEWER:** A matrix with many YES values may be circular because MESO's existing abstractions were chosen broadly enough to fit anything.

**ACCEPTED.** Core promotion requires more than conceptual applicability. It eventually needs executable counterexamples showing that omitting the variable causes distinct failure across at least two unrelated domains.

> **HOSTILE REVIEWER:** “Effort,” “delay,” and “feasibility” could still be represented only inside target-specific appraisals rather than as global core state.

**UNRESOLVED.** That is exactly the next architecture question. The research only says these dimensions recur; it does not yet determine their storage/composition interface.

> **HOSTILE REVIEWER:** Social and relational domains could drag MESO into identity management.

**ACCEPTED.** Actor and relationship identity must remain external source-bound context. MESO may motivate toward an actor; it does not get to define who that actor is or what relationship exists.

## Current result

The comparative exercise supports keeping sexuality explicitly subordinate to a broader MESO substrate and identifies several likely generic frontiers. It does not authorize implementation.
