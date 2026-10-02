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


## Machine decision / multi-objective control

### DG-M-001 — Wang et al. (2026)
- title: *Multi-objective reinforcement learning: a comprehensive survey of theories, algorithms, benchmarks and applications*
- journal: Systems Science & Control Engineering 14(1)
- DOI: `10.1080/21642583.2026.2672169`
- contribution:
  - surveys vector-valued objectives, scalarization, Pareto fronts/coverage sets, interactive preference learning, and constrained formulations;
  - explicitly notes that reducing multiple objectives to a single scalar can oversimplify real-world decision problems.
- architecture use:
  - supports researching typed/non-dominated decision structures while keeping MESO-specific semantic invariants.

### DG-M-002 — Felten, Talbi & Danoy (2024)
- title: *Multi-Objective Reinforcement Learning Based on Decomposition: A Taxonomy and Framework*
- journal: Journal of Artificial Intelligence Research 79:679–723
- DOI: `10.1613/jair.1.15702`
- contribution:
  - decomposition-based MORL preserves separate objectives and supports multiple trade-off policies.
- architecture use:
  - comparison point for domain-profile contribution and vector preservation;
  - not evidence that MESO should optimize an ordinary MORL objective.

### DG-M-003 — Wachi, Shen & Sui (2024)
- title: *A Survey of Constraint Formulations in Safe Reinforcement Learning*
- venue: IJCAI 2024 Survey Track
- DOI: `10.24963/ijcai.2024/913`
- contribution:
  - surveys multiple ways to formulate safety constraints separately from reward optimization.
- architecture use:
  - supports separating hard admissibility/protection from motivational tradeoffs.

### DG-M-004 — Gu et al. (2024)
- title: *A Review of Safe Reinforcement Learning: Methods, Theories, and Applications*
- journal: IEEE Transactions on Pattern Analysis and Machine Intelligence 46(12):11216–11235
- DOI: `10.1109/TPAMI.2024.3457538`
- contribution:
  - broad review of safe-RL methods and constraints in real-world deployment.
- architecture use:
  - comparison surface for protection/constraint semantics.

### DG-M-005 — Aubret et al. (2023)
- title: *An Information-Theoretic Perspective on Intrinsic Motivation in Reinforcement Learning: A Survey*
- journal: Entropy 25(2):327
- DOI: `10.3390/e25020327`
- contribution:
  - separates surprise, novelty and skill-learning perspectives in computational intrinsic motivation.
- architecture use:
  - supports typed epistemic motives rather than one generic intrinsic-reward scalar.

## Habit / goal-directed control

### DG-E-022 — Gillan (2024)
- title: *Leveraging cognitive neuroscience for making and breaking real-world habits*
- journal: Trends in Cognitive Sciences
- DOI: `10.1016/j.tics.2024.10.006`
- contribution:
  - frames behavior as a balance between stimulus-response habit processes and goal-directed action-outcome processes;
  - habits can provide cognitive efficiency but create action slips when overexpressed.
- architecture use:
  - supports a distinct habit research track;
  - does not settle whether habit belongs in MESO core or host action policy.

### DG-E-023 — Bouton (2024)
- title: *Habit and persistence*
- journal: Journal of the Experimental Analysis of Behavior 121(1):88–96
- DOI: `10.1002/jeab.894`
- contribution:
  - distinguishes goal-directed actions dependent on remembered outcome value from habits evoked by antecedent cues.
- architecture use:
  - supplies the core devaluation counterexample: behavior can persist after current outcome value falls.

### DG-E-024 — León et al. (2026)
- title: *The evaluation of devaluation: Deficient outcome devaluation leads to wrongly considering goal-directed actions as habits*
- journal: Behavior Research Methods
- DOI: `10.3758/s13428-026-03099-6`
- contribution:
  - cautions that human habit classification can be distorted by devaluation methodology.
- architecture use:
  - reason to keep habit at `RESEARCH_FIRST` rather than prematurely freezing a dual-system implementation.

### DG-E-025 — Correa/Salamone effort systems review lineage (2026)
- title: *Neurochemical drivers of effort: The roles of dopamine and beyond in physical and cognitive exertion*
- journal: Neuroscience & Biobehavioral Reviews
- contribution:
  - effort motivation reflects interactions across multiple neuromodulatory systems;
  - dopamine is important for energizing behavior but not a sufficient single-transmitter explanation.
- architecture use:
  - reinforces functional effort/vigor types rather than dopamine imitation.


## Negative valence / aversive motivation

### DG-E-026 — NIMH RDoC Negative Valence Systems
- current constructs:
  - Acute Threat ("Fear")
  - Potential Threat ("Anxiety")
  - Sustained Threat
  - Loss
  - Frustrative Nonreward
- contribution:
  - provides explicit counterexamples to a single generic negative-value construct;
  - distinguishes immediate danger, uncertain/distant harm, persistent threat adaptation, deprivation/loss, and blocked expected reward.
- architecture use:
  - functional differentiation only; MESO need not copy human emotion labels.

### DG-E-027 — Papini et al. (2024)
- title: *Frustrative Nonreward: Behavior, Circuits, Neurochemistry, and Disorders*
- journal: Journal of Neuroscience 44(40):e1021242024
- DOI: `10.1523/JNEUROSCI.1021-24.2024`
- contribution:
  - frustrative nonreward depends on surprising omission/reduction of an expected valued resource;
  - distinguishes plain nonreward from expectation-violating blocked reward;
  - links FNR to later motivational, learning and social consequences.
- architecture use:
  - test whether MESO needs a distinct blocked-expected-reward control state beyond numeric prediction error.

### DG-E-028 — Yee et al. (2022)
- title: *Aversive motivation and cognitive control*
- journal: Neuroscience & Biobehavioral Reviews 133:104493
- DOI: `10.1016/j.neubiorev.2021.12.016`
- contribution:
  - negative reinforcement and punishment have distinct behavioral/computational roles;
  - aversive incentives can either activate or inhibit behavior depending on context;
  - mixed appetitive/aversive motivation is important for control allocation.
- architecture use:
  - prohibit `aversive == suppress behavior`;
  - preserve outcome valence separately from learning-direction semantics.

### DG-E-029 — Bravo-Rivera / aversive behavior review lineage (2022)
- title: *Neural systems for aversively motivated behavior*
- series: Advances in Motivation Science 9:33–55
- DOI: `10.1016/bs.adms.2022.01.002`
- contribution:
  - active and passive avoidance differ in neural, motivational and affective consequences;
  - perceived controllability changes avoidance strategy.
- architecture use:
  - motivates active/preventive vs inhibitory avoidance research and links it to feasibility/controllability.

### DG-E-030 — Sands et al. (2023)
- title: *Subsecond fluctuations in extracellular dopamine encode reward and punishment prediction errors in humans*
- journal: Science Advances 9(48):eadi4927
- DOI: `10.1126/sciadv.adi4927`
- contribution:
  - intracranial human data found reward and punishment prediction errors with distinct valence-specific temporal dynamics.
- architecture use:
  - preserve outcome/teaching-signal class rather than assuming one unsigned or sign-only dopamine analogue.
- ceiling:
  - small neurosurgical human sample; does not define a machine learning rule.


## Arousal / regulatory systems

### DG-E-031 — NIMH RDoC Arousal and Regulatory Systems
- current constructs:
  - Arousal
  - Circadian Rhythms
  - Sleep-Wakefulness
- key boundary:
  - NIMH explicitly defines arousal as distinct from motivation and valence while allowing covariance/interactions.
- architecture use:
  - prevent MESO recruitment, action vigor and domain-specific arousal from collapsing into one generic scalar;
  - treat machine runtime/readiness state as an external functional interface unless a measurable core construct is defined.

### DG-E-032 — NIMH RDoC Arousal construct
- contribution:
  - arousal concerns sensitivity to external/internal stimuli;
  - can modulate selectivity and responsiveness;
  - can accompany increased or decreased locomotor behavior.
- architecture use:
  - reject `more arousal == more action vigor`.

### DG-E-033 — NIMH RDoC Sleep-Wakefulness / Circadian constructs
- contribution:
  - sleep/wake, circadian timing and momentary arousal are overlapping but distinguishable regulatory systems.
- architecture use:
  - machine suspension/availability and time-dependent scheduling should not be mislabeled as motive or desire.


## Effort / control-allocation refinements

### DG-E-034 — Silvestrini, Musslick, Berry & Vassena (2023)
- title: *An integrative effort: Bridging motivational intensity theory and recent neurocomputational and neuronal models of effort and control allocation*
- journal: Psychological Review
- DOI: `10.1037/rev0000372`
- contribution:
  - integrates motivational-intensity theory with Expected Value of Control, reinforcement meta-learner and neuronal effort models;
  - highlights non-monotonic relations between task difficulty and effort allocation.
- architecture use:
  - reject `difficulty == exerted effort`;
  - couple willingness/effort allocation to feasibility and justified maximum effort.

### DG-E-035 — Yee (2024)
- title: *Neural and Computational Mechanisms of Motivation and Decision-making*
- journal: Journal of Cognitive Neuroscience
- DOI: `10.1162/jocn_a_02258`
- contribution:
  - emphasizes computational decomposition of incentive effects on decision components;
  - argues organisms may optimize toward desired internal state rather than merely external incentive value.
- architecture use:
  - comparison surface for effort, homeostasis and internal-state-dependent motivation;
  - not a universal MESO objective.

### DG-E-036 — Scholey, Lugtmeijer & Apps (2024)
- title: *The neuroeconomics of work: Computational and neural mechanisms of the dynamics of effort-based decisions*
- DOI: `10.31234/osf.io/csbv7`
- status: preprint / lower evidence ceiling.
- contribution:
  - reviews dynamic, context-dependent willingness to exert effort across motivational domains.
- architecture use:
  - treat effort appraisal as current-state/candidate dependent, not one stable motivation trait.


## Future goal / feasibility / temporal-cost refinement

### DG-E-037 — Johnson & Grabenhorst (2025; volume 2024)
- title: *The amygdala and the pursuit of future rewards*
- journal: Frontiers in Neuroscience 18:1517231
- DOI: `10.3389/fnins.2024.1517231`
- contribution:
  - reviews goal formation and stepwise pursuit of future rewards;
  - separates subjective reward value from effort and delay costs;
  - discusses expectancy/value, dynamic inconsistency and progress tracking.
- architecture use:
  - preserve target value, delay, effort and feasibility as distinct appraisal inputs;
  - do not treat changing current choice as automatic permanent-preference mutation.

### DG-E-038 — acute stress / delay-discounting meta-analysis (2024)
- title: *No effects of acute stress on monetary delay discounting: A systematic literature review and meta-analysis*
- journal: Neurobiology of Stress 31:100653
- DOI: `10.1016/j.ynstr.2024.100653`
- contribution:
  - demonstrates that seemingly intuitive context effects on delay discounting do not necessarily survive aggregate evidence.
- architecture use:
  - warning against hard-coding folk assumptions about stress automatically making agents short-sighted.


## Predictive resource regulation / allostasis refinements

### DG-E-039 — Mushiake (2023)
- title: *Allostasis and Homeostasis: Dynamic Adaptive Systems from a Neurophysiological Perspective*
- DOI: `10.11477/mf.1416202504`
- contribution:
  - distinguishes reactive homeostasis from predictive regulation/dynamic adjustment.
- architecture use:
  - research provenance for current-deficit vs predicted-future-demand separation.

### DG-E-040 — Ohira (2023)
- title: *Integration of Interoception, Decision-Making, and Affect: Allostasis as Predictive Processing*
- DOI: `10.11477/mf.1416202505`
- contribution:
  - reviews predictive-processing/allostasis framing.
- architecture use:
  - motivates forecast/current-state separation only; no requirement to import predictive-processing theory wholesale.

### DG-M-006 — Ngo et al. (2022)
- title: *Homeostatic and Allostatic Principles for Behavioral Regulation in Desert Reptiles: A Robotic Evaluation*
- DOI: `10.1007/978-3-031-20470-8_33`
- contribution:
  - computational/robotic demonstration that dynamic reweighting using interoceptive/exteroceptive state can improve adaptation over reactive homeostasis in the tested model.
- architecture use:
  - machine-side evidence that predictive/dynamic resource regulation can be operational rather than purely metaphorical.
- ceiling:
  - specific bio-inspired simulated robot; not a general MESO algorithm.

### DG-M-007 — resource-rationality research lineage
- contribution:
  - computational resource constraints can rationally alter inference/decision strategies.
- architecture use:
  - evaluate cost of reasoning/tool use itself where real compute/latency/budget evidence exists;
  - do not infer one universal resource-utility function.


## Multi-goal pursuit / persistence / disengagement

### DG-E-041 — Neal, Ballard & Vancouver (2017)
- title: *Dynamic Self-Regulation and Multiple-Goal Pursuit*
- journal: Annual Review of Organizational Psychology and Organizational Behavior
- DOI: `10.1146/annurev-orgpsych-032516-113156`
- contribution:
  - reviews how actors manage competing demands on time/resources, select goals/tasks, sequence work, and adjust goals.
- architecture use:
  - distinguish current target selection from persistent multi-goal state and resource allocation.

### DG-E-042 — Kim et al. (2023)
- title: *Self-regulatory processes within and between diverse goals: The multiple goals regulation framework*
- journal: Educational Psychologist
- DOI: `10.1080/00461520.2022.2158828`
- contribution:
  - emphasizes goal prioritizing, shielding and switching within multi-goal regulation.
- architecture use:
  - comparative vocabulary for multi-goal allocation; no direct machine transfer.

### DG-E-043 — Brandstätter & Bernecker (2022)
- title: *Persistence and Disengagement in Personal Goal Pursuit*
- journal: Annual Review of Psychology 73
- DOI: `10.1146/annurev-psych-020821-110710`
- contribution:
  - persistence and timely disengagement can both be adaptive;
  - reviews expectancy-value and volitional determinants.
- architecture use:
  - reject `persistence == success`;
  - distinguish goal lifecycle from momentary selection.

### DG-E-044 — Mayer & Freund (2022)
- title: *Better off without? Benefits and costs of resolving goal conflict through goal shelving and goal disengagement*
- journal: Motivation and Emotion
- DOI: `10.1007/s11031-022-09966-x`
- contribution:
  - experimentally distinguishes temporary goal shelving from disengagement.
- architecture use:
  - supports `not selected now != abandoned goal`.

### DG-E-045 — Gorges & Grund (2017)
- title: *Aiming at a Moving Target: Theoretical and Methodological Considerations in the Study of Intraindividual Goal Conflict between Personal Goals*
- journal: Frontiers in Psychology
- DOI: `10.3389/fpsyg.2017.02011`
- contribution:
  - distinguishes resource conflict from other/inherent goal conflict and highlights heterogeneity of goal-conflict constructs.
- architecture use:
  - do not collapse all multi-goal conflict into one competition scalar.


## Criteria interaction / non-compensatory aggregation

### DG-M-008 — Greco, Słowiński & Wallenius (2025)
- title: *Fifty years of multiple criteria decision analysis: From classical methods to robust ordinal regression*
- journal: European Journal of Operational Research 323(2):351–377
- DOI: `10.1016/j.ejor.2024.07.038`
- contribution:
  - reviews major MCDA schools, preference elicitation, criteria aggregation and recommendation development over five decades.
- architecture use:
  - confirms that aggregation method and preference model are policy choices rather than neutral consequences of having several numeric criteria.

### DG-M-009 — Figueira, Greco & Roy (2009)
- title: *ELECTRE methods with interaction between criteria: An extension of the concordance index*
- journal: European Journal of Operational Research 199(2):478–495
- DOI: `10.1016/j.ejor.2008.11.025`
- contribution:
  - explicitly models mutual strengthening, mutual weakening and antagonistic interactions between criteria;
  - demonstrates that interacting criteria require declared interaction semantics.
- architecture use:
  - supports the anti-dimension-stuffing rule that differently named contributions cannot be presumed independent/additive.

### DG-M-010 — Ishii & Sugeno / Choquet survey lineage (2015 survey)
- title: *A Short Survey on the Usage of Choquet Integral and its Associated Fuzzy Measure in Multiple Attribute Analysis*
- journal: Procedia Computer Science 59:427–434
- DOI: `10.1016/j.procs.2015.07.560`
- contribution:
  - reviews Choquet-based aggregation specifically because ordinary additive aggregation cannot naturally represent criterion interactions;
  - notes the parameter-identification complexity that grows with the number of attributes.
- architecture use:
  - Choquet is a useful reference for redundancy/synergy, but its parameter complexity argues against making it MESO's default core aggregator.

### DG-M-011 — Marichal (2004)
- title: *Tolerant or intolerant character of interacting criteria in aggregation by the Choquet integral*
- journal: European Journal of Operational Research 155(3):771–791
- DOI: `10.1016/S0377-2217(02)00885-8`
- contribution:
  - treats statistical correlation/redundancy, substitutability/complementarity and decisive criteria as distinct interaction patterns.
- architecture use:
  - supports separating evidence redundancy from genuinely distinct motivational reasons.

### DG-M-012 — ELECTRE / outranking review lineage
- reference: Govindan & Jepsen (2016), *ELECTRE: A comprehensive literature review on methodologies and applications*
- journal: European Journal of Operational Research 250(1):1–29
- DOI: `10.1016/j.ejor.2015.07.019`
- contribution:
  - reviews a large ELECTRE literature built around outranking rather than a single compensatory utility score.
- architecture use:
  - supports researching partial/incomplete ordering and non-compensatory vetoes as alternatives to universal scalarization.
