# MESO-CRCT Domain-General Motivation Taxonomy V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / PRE_ARCHITECTURE / NO_IMPLEMENTATION`

## Purpose

MESO-CRCT is not a sexuality system.

It is a domain-general architecture for motivational state, reward/valuation, learning, salience, effort, allocation, action tendency, and bounded welfare/control. Sexuality is one domain that can use that substrate.

This research pass asks a broader question:

> Which mechanisms belong in MESO core because they recur across qualitatively different motives, and which mechanisms belong in domain profiles because their semantics depend on a particular class of goal, relationship, need, or activity?

The distinction matters because a rich sexuality implementation could otherwise accidentally make the generic core sex-shaped.

## Exact source cut

This pass starts from MESO-CRCT main:

`060d0feeb9dc9eb23801082bd8f1c4a7cb06184d`

The parallel sexuality research branch is a research input, not the base of this branch.

## Current MESO core already gets several important things right

MESO already keeps apart:

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

It also already has:

- typed perceptual/semantic/motivational/incentive/epistemic signals;
- hedonic state independent from hazard/avoidance;
- current homeostatic deficit;
- recruitment/coherence;
- temporal decay;
- provenance and distinct event identity;
- bounded plasticity and durable association memory;
- cue-bound recall;
- multi-target arbitration;
- allocation capture detection/correction;
- typed action tendency;
- negative-transfer review and quarantine.

The question is what the next genuinely domain-general layers are.

## Research-derived core candidates

### 1. Effort valuation / willingness to work

The 2024 Annual Review by Salamone & Correa emphasizes that motivation has both directional and activational aspects. Dopamine-related systems are strongly implicated in behavioral activation, vigor and effort-based choice rather than acting as a generic pleasure transmitter.

RDoC likewise treats effort valuation as part of reward valuation.

MESO currently asks which target wins and what direction applies, but it does not yet give effort cost its own first-class typed representation.

Candidate distinction:

```
target_value
    !=
effort_cost
    !=
willingness_to_exert_effort
    !=
action_vigor
```

These should remain independently inspectable.

### 2. Delay / temporal cost

RDoC reward valuation explicitly distinguishes reward probability, delay and effort.

A future MESO target can therefore be:

```
highly_desirable
highly_likely
very_delayed
very_effortful
```

without forcing those properties into one scalar.

Delay belongs in core because it affects food, sex, achievement, curiosity, social goals, caregiving, work, play and long-term planning.

### 3. Expectancy / feasibility

Goal pursuit depends not only on desirability but also on whether an outcome is expected to be obtainable.

Candidate separation:

```
desirability != feasibility
expected_outcome != current_value
prediction_error != feasibility
```

A target may be highly desirable but currently infeasible.

### 4. Predictive allostasis / resource budgeting

Current MESO homeostasis is reactive: a need axis can create a deficit that increases incentive pressure.

Allostasis research motivates a broader predictive layer: future internal/resource requirements can alter current behavior before a deficit exists.

Candidate distinction:

```
current_deficit
    !=
predicted_future_need
    !=
resource_budget
    !=
effort_cost
```

For a machine substrate this does not mean hormones or metabolism by analogy. It could mean predicted compute, energy, time, memory pressure, latency, thermal/power state, attention budget, token budget or other host-defined resources.

A domain may consume allostatic state, but domain code should not own resource truth.

### 5. Action vigor / activation

Current MESO action tendency answers direction:
- approach;
- learned withdrawal;
- protective withdrawal;
- inspect;
- uncommitted.

That does not answer **how much activation/effort should be mobilized**.

Candidate separation:

```
action_direction != action_vigor
priority != vigor
pleasure != vigor
```

### 6. Reward anticipation vs initial response vs satiation

RDoC distinguishes:
- reward anticipation;
- initial response to reward;
- reward satiation.

MESO already has incentive salience, hedonic state and satiation, but a formal anticipatory representation may deserve explicit treatment if it cannot be reduced cleanly to incentive salience.

Research question:

> Is anticipation a distinct state family, or a temporal configuration of expectancy + incentive salience + learned association?

Do not add a new state merely because neuroscience has a label; require a mechanical counterexample.

### 7. Habit / outcome-insensitive persistence

RDoC includes habit within Positive Valence Systems.

MESO already has learned association and replay controls but does not appear to have a distinct habit/action-chunk system.

Potential core distinction:

```
goal_directed_action
    !=
habitual_action
    !=
current_desire
```

A learned sequence may continue despite changed outcome value. That creates both useful automation and capture risk.

Research first; implementation is not yet justified.

## Candidate domain profiles

These are not claims that MESO must build every human behavioral system. They are comparative probes: if the core cannot support them without semantic distortion, the core is probably under-specified.

### A. Homeostatic/resource regulation

Examples:
- hunger/thirst in biology;
- compute/energy/thermal/time/resource pressure in machines.

Uses:
- need state;
- predicted need;
- incentive modulation;
- effort/resource valuation;
- satiation.

Domain-specific:
- what counts as a resource;
- setpoints/ranges;
- sensor/currentness authority;
- corrective affordances.

### B. Epistemic curiosity / exploration

2024 reviews distinguish information seeking from ordinary extrinsic reward and emphasize uncertainty, information gain and learning progress.

Uses:
- epistemic value;
- novelty;
- uncertainty;
- learning progress;
- effort/delay;
- exploration allocation.

Domain-specific:
- knowledge-gap representation;
- information source quality;
- learning-progress measurement;
- stopping criteria.

Important non-equivalence:

```
novelty != curiosity
uncertainty != value
information_gain != pleasure
learning_progress != truth
```

### C. Achievement / mastery / competence

Uses:
- explicit goals;
- progress;
- effort valuation;
- delay;
- feasibility;
- persistence;
- self-generated challenge;
- learning/reward.

Domain-specific:
- mastery criteria;
- performance comparison;
- competence model;
- task-specific feedback.

Do not make achievement equivalent to external praise or status.

### D. Affiliation / social reward

A 2024 Psychological Bulletin systematic review found major heterogeneity in what research calls social reward and identified intimacy/sensory richness and immediacy/interactive engagement as important differentiating properties.

Uses:
- reward responsiveness;
- learned association;
- partner/actor specificity;
- social prediction;
- approach;
- satiation/need.

Domain-specific:
- social actor identity/currentness;
- reciprocal interaction;
- intimacy/immediacy;
- relationship context.

```
social_reward != attachment
social_reward != approval
social_reward != status
social_reward != sexuality
```

### E. Attachment / bonding

Human attachment research overlaps with reward/motivation/social cognition systems but should not be collapsed into generic social reward.

Uses:
- actor-specific learned value;
- proximity/availability relevance;
- separation/reunion state;
- memory;
- social prediction.

Domain-specific:
- bond identity;
- attachment-security constructs;
- relationship continuity/currentness.

MESO should probably interface with rather than own relationship truth.

### F. Caregiving

Caregiving and attachment are complementary but non-identical motivational systems.

Uses:
- target-specific relevance;
- need appraisal;
- effort;
- protective priority;
- action tendency;
- long-horizon allocation.

Domain-specific:
- dependent/beneficiary state;
- care obligations;
- vulnerability;
- role/currentness.

Hard boundary:

```
caregiving != attachment
caregiving != ownership
caregiving != authority_over_recipient
```

### G. Status / dominance / competition

2024 reviews of social dominance implicate mesocorticolimbic mechanisms but also emphasize social recognition, decision making and action across multiple circuits.

Uses:
- target appraisal;
- reward;
- effort;
- social prediction;
- action tendency;
- learning.

Domain-specific:
- hierarchy representation;
- competition;
- rank/status meaning;
- social counterparty.

Hard boundaries:

```
status_motivation != aggression
dominance != authority
submission != consent
rank != worth
```

### H. Play

Evidence here is less mature as a computational domain.

Recent behavioral work suggests at least some play differs from both exploration and exploitation, including spontaneous generation of new goals. Comparative/social-play literature also treats play as socially and cognitively complex.

Current disposition: `RESEARCH_FIRST`.

Possible uses:
- intrinsic motivation;
- novelty;
- flexible goal creation;
- low-stakes exploration;
- social affiliation;
- learning.

Do not yet create `play_drive` merely because play is recognizable behavior.

### I. Sexuality

Sexuality is one first-class domain profile, not MESO's identity.

Uses nearly every MESO substrate:
- relevance;
- excitation/inhibition;
- incentive salience;
- attraction/desire;
- partner specificity;
- pleasure;
- effort/delay;
- learning;
- anticipation;
- satiation/recovery;
- allocation;
- negative-transfer controls.

Its richness makes it a powerful stress test for the core.

Domain-specific sexual semantics must never leak into unrelated profiles.

## Cross-domain extraction rule

A mechanism should move into MESO core only when all of the following are plausibly true:

1. it appears in multiple materially different motivational domains;
2. its operational meaning remains stable across those domains;
3. domain-specific content can be supplied as typed input rather than hard-coded into the mechanism;
4. moving it to core reduces duplication without weakening semantic boundaries;
5. adversarial cases can show the mechanism does not import one domain's assumptions into another.

Otherwise it remains a domain-profile mechanism.

## Example: anticipation

Sexual anticipation, curiosity about an answer, anticipation of social contact and anticipation of food may all share temporal predictive structure.

The core candidate is not “sexual anticipation” or “social anticipation.”

It might instead be:

```
EXPECTED_OUTCOME_STATE(
    target,
    expected_value,
    probability,
    delay,
    uncertainty,
    source
)
```

Domain profiles then interpret the target semantics.

This is an example, not a frozen schema.

## Example: excitation/inhibition

Sexual excitation/inhibition should **not** automatically become generic MESO excitation/inhibition.

Why:
- the Dual Control Model concerns sexual response;
- “inhibition” elsewhere may mean hazard, action suppression, satiation, cognitive control, social restraint, or low feasibility;
- reusing the word could collapse distinct causal mechanisms.

Only a later cross-domain comparison could justify a generic gating abstraction.

## Domain composition rather than one-driver-at-a-time

Real behavior often involves multiple motives simultaneously:

```
caregiving + attachment + effort cost
curiosity + achievement + fatigue/resource pressure
sexuality + attachment + social reward
status + affiliation + protection
play + curiosity + affiliation
```

MESO's arbitration architecture should therefore support co-active domain proposals rather than forcing every event into one exclusive motivational category.

Research question:

> Should domains produce typed contributions into one common arbitration surface, or should higher-level coalitions form before arbitration?

No implementation decision yet.

## Social motivation warning

Social reward research shows that “social” is not one reward type. Human social motivation may involve:
- affiliation;
- attachment;
- caregiving;
- status/dominance;
- cooperation;
- play;
- sexuality;
- approval/reputation;
- belonging.

Do not create one generic `social_reward` scalar and call the problem solved.

## Intrinsic motivation warning

Intrinsic vs extrinsic motivation is also not just “internal reward vs external reward.”

Current reviews note conceptual and measurement ambiguity. Curiosity, mastery, autonomy, play and interest may overlap but should not be prematurely represented as one intrinsic-reward channel.

MESO should preserve source/reason provenance for motivational value.

## Hostile review

> **HOSTILE REVIEWER:** This taxonomy could become an encyclopedia of human motives instead of an engineering architecture.

**ACCEPTED.** Domain candidates are stress tests, not a commitment to implement each as a module. Core extraction requires repeated cross-domain mechanical evidence.

> **HOSTILE REVIEWER:** Biological behavioral systems do not map cleanly onto machine agents.

**ACCEPTED.** The biological literature constrains distinctions and supplies counterexamples. Machine domains must be defined by actual functional state and host evidence, not metaphor.

> **HOSTILE REVIEWER:** Domain profiles may just recreate a global utility function through the back door if every profile emits “priority.”

**ACCEPTED AS A MAJOR RISK.** Profiles should emit typed evidence/state, not opaque utility scores. MESO arbitration must preserve why a target is active, what cost/need/reward channels contributed, and what information would reverse the decision.

## Current conclusion

MESO should remain a **domain-general motivational substrate**.

Current research suggests its next generic frontiers are more likely to be:

1. effort valuation;
2. delay/temporal cost;
3. expectancy/feasibility;
4. predictive allostasis/resource budgeting;
5. action vigor/activation;
6. possibly anticipation;
7. possibly habit.

Sexuality, curiosity, achievement, affiliation, attachment, caregiving, status/competition and perhaps play should be used as comparative domains to validate those abstractions.

No implementation is authorized by this document.
