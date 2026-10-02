# MESO-CRCT Domain-General Motivation Source Ledger V1

Date: 2026-10-02
Status: `RESEARCH_SOURCE_LEDGER / PRE_ARCHITECTURE`

This ledger records sources that materially constrain the domain-general MESO research pass. Human/animal neuroscience can justify distinctions, candidate mechanisms, counterexamples and test designs. It does not establish biological equivalence for machine state.

## Core reward / positive valence

### DG-E-001 — NIMH RDoC Positive Valence Systems
- source: National Institute of Mental Health
- constructs:
  - Reward Responsiveness
    - Reward Anticipation
    - Initial Response to Reward
    - Reward Satiation
  - Reward Learning
    - Probabilistic and Reinforcement Learning
    - Reward Prediction Error
    - Habit
  - Reward Valuation
    - Reward probability
    - Delay
    - Effort
- contribution:
  - supports separating anticipation, response, satiation, learning, prediction error, habit, probability, delay and effort;
  - provides a useful dimensional framework rather than one generic reward variable.
- architecture use:
  - comparative checklist for MESO typed state;
  - not a requirement to mirror RDoC literally.

### DG-E-002 — Dexter et al. / cross-species RDoC review (2024/2025)
- title: *Cross-species translational paradigms for assessing positive valence system as defined by the RDoC matrix*
- journal: Journal of Neurochemistry 169(1)
- DOI: `10.1111/jnc.16243`
- contribution:
  - reward responsiveness, reward learning and reward valuation are related but dissociable;
  - motivates cross-domain and cross-species testing of component processes.
- architecture use:
  - reinforces MESO's anti-collapse stance.

## Effort / vigor / activation

### DG-E-003 — Salamone & Correa (2024)
- title: *The Neurobiology of Activational Aspects of Motivation: Exertion of Effort, Effort-Based Decision Making, and the Role of Dopamine*
- journal: Annual Review of Psychology 75:1–32
- DOI: `10.1146/annurev-psych-020223-012208`
- contribution:
  - motivation has directional and activational components;
  - effort-related decision making and behavioral activation are dissociable from hedonic reward;
  - dopamine is not adequately described as a generic reward/pleasure transmitter.
- architecture use:
  - motivates first-class effort valuation and action-vigor research.

### DG-E-004 — Job, Mlynski & Nikitin (2024)
- title: *Challenging the law of least effort*
- journal: Current Opinion in Psychology 60:101881
- DOI: `10.1016/j.copsyc.2024.101881`
- contribution:
  - effort is not universally avoided;
  - people can seek effort due to learning, health, broader goals, learned industriousness and meaning/beliefs about effort.
- architecture use:
  - effort cost must not be equated with negative value;
  - `effort_cost != unwillingness_to_exert_effort`.

## Curiosity / epistemic motivation

### DG-E-005 — Monosov (2024)
- title: *Curiosity: primate neural circuits for novelty and information seeking*
- journal: Nature Reviews Neuroscience 25:195–208
- DOI: `10.1038/s41583-023-00784-9`
- contribution:
  - organisms seek novel objects and information even where there is no conventional extrinsic reward payoff;
  - information-seeking and novelty have dedicated motivational relevance.
- architecture use:
  - validates MESO's separate epistemic-value channel;
  - discourages reducing curiosity to ordinary reward.

### DG-E-006 — Oudeyer et al. review lineage / 2024 curiosity synthesis
- title: *Curiosity and the dynamics of optimal exploration*
- journal: Trends in Cognitive Sciences 28(5):441–453
- DOI: `10.1016/j.tics.2024.02.001`
- contribution:
  - integrates uncertainty/information gain with learning-progress accounts;
  - curiosity changes dynamically over learning;
  - curiosity must be balanced with other drives such as safety and hunger.
- architecture use:
  - learning progress and uncertainty should remain distinguishable;
  - domain arbitration should allow curiosity to compete/cooperate with other motives.

## Intrinsic motivation

### DG-E-007 — Morris et al. (2022)
- title: *On what motivates us: a detailed review of intrinsic v. extrinsic motivation*
- journal: Psychological Medicine 52(10):1801–1816
- DOI: `10.1017/S0033291722001611`
- contribution:
  - intrinsic motivation is a meaningful but conceptually complex construct;
  - intrinsic and extrinsic motivation differ in associated rewards/outcomes while sharing computational features.
- architecture use:
  - do not create one untyped `intrinsic_reward` register;
  - preserve motive-source provenance and domain semantics.

## Social reward / affiliation

### DG-E-008 — Stijovic et al. (2024)
- title: *Defining social reward: A systematic review of human and animal studies*
- journal: Psychological Bulletin 150(12):1472–1509
- DOI: `10.1037/bul0000455`
- corpus:
  - 384 studies;
  - 42,118 participants/subjects.
- contribution:
  - “social reward” is operationalized heterogeneously;
  - sensory richness/intimacy and active interaction/immediacy explain major differences across paradigms;
  - review explicitly notes implications for AI and human-computer interaction.
- architecture use:
  - do not implement one generic social-reward scalar;
  - social-domain appraisal should track interaction properties and actor specificity.

## Attachment / affiliation

### DG-E-009 — Bortolini et al. (2024)
- title: *The extended neural architecture of human attachment: An fMRI coordinate-based meta-analysis of affiliative studies*
- journal: Neuroscience & Biobehavioral Reviews 159:105584
- DOI: `10.1016/j.neubiorev.2024.105584`
- corpus:
  - 79 fMRI studies;
  - personalized attachment figures including babies, partners, family and friends.
- contribution:
  - attachment engages reward, motivation and social-cognition systems but is distributed beyond a single reward circuit.
- architecture use:
  - attachment can interact with MESO but should not be collapsed into generic social reward.

### DG-E-010 — attachment/caregiving interaction review
- title: *Neural basis of attachment-caregiving systems interaction: insights from neuroimaging studies*
- contribution:
  - attachment and caregiving are complementary but distinguishable behavioral systems.
- architecture use:
  - care and attachment should remain distinct domain semantics.

## Social dominance / rank

### DG-E-011 — Choi, Jeong & Koo (2024)
- title: *Mesocorticolimbic circuit mechanisms of social dominance behavior*
- journal: Experimental & Molecular Medicine 56:1889–1899
- DOI: `10.1038/s12276-024-01299-8`
- contribution:
  - dominance behavior involves social recognition, decision making and action across multiple circuits;
  - mesocorticolimbic mechanisms participate without making status equivalent to reward.
- architecture use:
  - status/dominance should be a domain profile consuming general valuation/effort/learning machinery.

### DG-E-012 — Battivelli et al. (2024)
- title: *How can ethology inform the neuroscience of fear, aggression and dominance?*
- journal: Nature Reviews Neuroscience 25:809–819
- DOI: `10.1038/s41583-024-00858-2`
- contribution:
  - behavior must be interpreted in ecological/contextual function rather than only circuit activation.
- architecture use:
  - status/dominance, aggression and protection must not be collapsed.

## Allostasis / interoception / resource regulation

### DG-E-013 — Chen et al. / Annual Review of Physiology (2024)
- title: *The Coding Logic of Interoception*
- DOI: `10.1146/annurev-physiol-042222-023455`
- contribution:
  - interoception monitors diverse internal signals and supports homeostasis, motivational drives and autonomic/cognitive/behavioral regulation.
- architecture use:
  - machine resource-state producers may inform motivation but must remain source-typed.

### DG-E-014 — Sterling (2019)
- title: *Allostasis: A Brain-Centered, Predictive Mode of Physiological Regulation*
- journal: Trends in Neurosciences
- DOI: `10.1016/j.tins.2019.07.010`
- contribution:
  - allostasis emphasizes predictive regulation before error/deficit emerges.
- architecture use:
  - candidate distinction between current deficit and predicted future need.

### DG-E-015 — Barrett et al. / allostatic-gradient framework (2024)
- title: *Allostasis as a core feature of hierarchical gradients in the human brain*
- PMCID: `PMC11117115`
- contribution:
  - integrates predictive processing and allostasis at large-scale brain-organization level.
- architecture use:
  - supports predictive resource-regulation research, not direct machine biological equivalence.

### DG-E-016 — interoceptive reinforcement-learning review (2025)
- title: *The interoceptive origin of reinforcement learning*
- PMCID: `PMC12400946`
- contribution:
  - argues that biological primary reward can depend on internal state and downstream physiological consequences rather than immediate sensory gratification.
- architecture use:
  - reinforces `reward != sensory pleasure`;
  - resource/homeostatic consequences may affect teaching signals.

## Goals / future reward / delay

### DG-E-017 — future-reward pursuit review (2025)
- title: *The amygdala and the pursuit of future rewards*
- Frontiers in Neuroscience
- contribution:
  - separates goal formation and pursuit;
  - highlights reward attributes, effort and delay costs;
  - discusses temporary preferences and future-goal persistence.
- architecture use:
  - supports explicit feasibility/delay/effort research.

## Achievement / mastery

### DG-E-018 — Bross, Nett & Daumiller (2024)
- title: *Interrelations Among Achievement Goals and Achievement Emotions: A Meta-Analytic Examination*
- journal: Educational Psychology Review 36:98
- corpus:
  - 2,644 effect sizes;
  - 355 studies;
  - 155,208 participants.
- contribution:
  - achievement goals are heterogeneous and interact differently with emotion.
- architecture use:
  - do not equate achievement motivation with one performance scalar or external praise.

### DG-E-019 — motivation/achievement longitudinal meta-analysis (2024)
- title: *The reciprocity between various motivation constructs and academic achievement*
- contribution:
  - motivation-achievement effects are heterogeneous and differ by construct.
- architecture use:
  - reinforces typed goal/motive representation rather than one achievement-drive value.

## Play

### DG-E-020 — Rule et al. (2024 preprint)
- title: *Children’s play differs from both exploring and exploiting*
- DOI: `10.31219/osf.io/bzd3f`
- status: preprint / lower evidence ceiling.
- contribution:
  - play condition produced behavior distinguishable from exploration and exploitation;
  - play involved spontaneous generation of new goals.
- architecture use:
  - justifies keeping play as a research frontier rather than silently treating it as curiosity/reward.
- limitation:
  - not sufficient to establish a generic `play_drive`.

### DG-E-021 — Kaplan (2024)
- title: *The evolution of social play in songbirds, parrots and cockatoos*
- journal: Neuroscience & Biobehavioral Reviews 161:105621
- DOI: `10.1016/j.neubiorev.2024.105621`
- contribution:
  - social play has emotional, social, innovative and cognitive dimensions;
  - comparative evidence remains uneven.
- architecture use:
  - play remains a separate research candidate.

## Source-use rule

These sources can support:
- construct separation;
- cross-domain recurrence;
- failure/counterexample design;
- candidate core-vs-profile placement;
- evidence ceilings.

They cannot by themselves establish:
- machine biological equivalence;
- one universal taxonomy of motivation;
- consciousness or felt motivation;
- that every human motive should become a MESO module;
- exact numerical parameter values for machine state.
