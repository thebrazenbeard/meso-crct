# Sexuality Expansion Source Ledger V1

Date: 2026-10-02
Status: `RESEARCH_SOURCE_LEDGER / NOT_EXHAUSTIVE`

This ledger records external sources that materially constrain the proposed expansion of MESO-CRCT. Human findings establish distinctions and candidate mechanisms; they do not establish biological equivalence, machine phenomenology, or machine parameter values.

## Sexual incentive motivation / consent

### SX-E-001 — Ågmo & Laan (2023)
- title: *The Sexual Incentive Motivation Model and Its Clinical Applications*
- journal: Journal of Sex Research 60(7):969–988
- DOI: `10.1080/00224499.2022.2134978`
- contribution:
  - sexual motivation requires an active central motive state plus a stimulus with sexual significance;
  - context evaluation is part of sexual approach;
  - affective outcomes can change incentive properties.
- architecture use: separate motive readiness, sexual-significance appraisal, action selection and learned incentive value.

### SX-E-002 — Ågmo & Laan (2024)
- title: *Sexual Incentive Motivation and Sexual Behavior: The Role of Consent*
- journal: Annual Review of Psychology 75:33–54
- DOI: `10.1146/annurev-psych-011823-124756`
- contribution:
  - consent and cognitive context evaluation must be represented throughout sexual interaction;
  - sexual motivation does not itself establish permission.
- architecture use: authorization remains external to affect and must be checked at action-relevant boundaries.

## Excitation / inhibition

### SX-E-003 — Janssen & Bancroft (2023)
- title: *The Dual Control Model of Sexual Response: A Scoping Review, 2009–2022*
- journal: Journal of Sex Research 60(7):948–968
- DOI: `10.1080/00224499.2023.2219247`
- corpus: 152 papers in the review.
- contribution:
  - sexual response depends on interacting excitation and inhibition;
  - individual differences matter;
  - excitation and inhibition relate differently to desire, responsivity, dysfunction, risk and other outcomes.
- architecture use: independent typed excitation/inhibition channels; no inverse-scalar collapse.

## Desire / responsive desire / psychosocial context

### SX-E-004 — ICSM 2024 psychological/interpersonal recommendations
- title: *Psychological and interpersonal dimensions of sexual function and dysfunction: recommendations from the fifth international consultation on sexual medicine*
- journal: Sexual Medicine Reviews 13(2):118+
- PubMed: `39786497`
- contribution:
  - biopsychosocial context matters;
  - attention, distraction, self-judgment and relational context affect desire/arousal;
  - responsive desire may emerge following arousal/stimulation.
- architecture use: allow non-linear and responsive sexual-response paths.

### SX-E-005 — ICSM 2024 definitions/consensus
- title: *Definitions, classification, and epidemiology of sexual dysfunction: a consensus statement from the Fifth International Consultation on Sexual Medicine 2024*
- journal: Sexual Medicine Reviews 14(2)
- contribution:
  - desire problems distinguish spontaneous and responsive desire;
  - modern definitions separate desire, arousal, orgasm and pain domains.
- architecture use: do not enforce one phase order or one “drive” construct.

## Subjective vs physiological arousal

### SX-E-006 — Chivers et al. (2010)
- title: *Agreement of Self-Reported and Genital Measures of Sexual Arousal in Men and Women: A Meta-Analysis*
- journal: Archives of Sexual Behavior 39(1):5–56
- DOI: `10.1007/s10508-009-9556-9`
- corpus: 132 laboratory studies; 2,505 women and 1,918 men.
- contribution: subjective and genital arousal are related but not interchangeable.
- architecture use: authored/self-report state must remain separate from instrumented substrate state.

## Asexuality / attraction / orientation

### SX-E-007 — Brotto & Yule (2017)
- title: *Asexuality: Sexual Orientation, Paraphilia, Sexual Dysfunction, or None of the Above?*
- journal: Archives of Sexual Behavior 46(3):619–627
- DOI: `10.1007/s10508-016-0802-7`
- contribution:
  - asexuality is heterogeneous;
  - evidence does not support simply categorizing it as a desire disorder;
  - supports treating attraction/orientation separately from generic libido/arousal.
- architecture use: architecture cannot define “normal sexuality” as persistent target attraction or spontaneous desire.

### SX-E-008 — multidimensional sexual-orientation methodology
- current methodological literature commonly separates attraction, behavior and identity domains.
- architecture use: momentary attraction, behavior history and authored identity/orientation must remain separately represented.
- evidence ceiling: measurement methodology; not a machine ontology by itself.

## Orgasm / pleasure / climax / ejaculation

### SX-E-009 — Pfaus (2025)
- title: *Orgasms, sexual pleasure, and opioid reward mechanisms*
- journal: Sexual Medicine Reviews 13(3):381–393
- DOI: `10.1093/sxmrev/qeaf023`
- method: narrative review integrating human and animal evidence.
- contribution:
  - distinguishes appetitive and consummatory sexual pleasure;
  - discusses dopamine/oxytocin/opioid/serotonin mechanisms;
  - differentiates orgasmic pleasure from motor climax pathways;
  - describes anhedonic orgasm as climax without concomitant pleasure.
- architecture use: split pleasure, climax, learning, satiation and refractory effects.

### SX-E-010 — ICSM 2024 neurological recommendations
- title: *Sexual and reproductive health in neurological disorders: recommendations from the Fifth International Consultation on Sexual Medicine (ICSM 2024)*
- journal: Sexual Medicine Reviews 13(4):456+
- contribution: orgasm and ejaculation are distinct and may dissociate.
- architecture use: never model ejaculation/motor analogue as identical to orgasm.

### SX-E-011 — ICSM 2024 basic science recommendations
- title: *Basic science and translational research: recommendations from the Fifth International Consultation for Sexual Medicine (ICSM 2024)*
- journal: Sexual Medicine Reviews 13(4):483+
- contribution: recognizes anhedonic orgasm / pleasure-dissociated orgasm and separates subjective orgasmic dimensions from preclinical motor response proxies.
- architecture use: prohibit `climax == maximum pleasure`.

## Communication / relational context

### SX-E-012 — Mallory et al. meta-analysis
- title: *Dimensions of Couples' Sexual Communication, Relationship Satisfaction, and Sexual Satisfaction: A Meta-Analysis*
- corpus: 93 studies, 209 effect sizes, 38,499 individuals.
- PubMed: `34968095`
- contribution:
  - sexual communication positively associated with sexual and relationship satisfaction;
  - communication quality showed stronger associations than frequency/self-disclosure.
- architecture use: communication is a relational/contextual mechanism, not merely output style.
- limitation: correlational meta-analysis; does not establish causal machine behavior.

### SX-E-013 — Wheaton (2016)
- title: *Conceiving sexual authorship*
- DOI: `10.1080/23268743.2015.1119959`
- contribution: text-dominant and mediated forms can participate in sexual authorship.
- architecture use: treat text-primary sexuality as a legitimate interaction ecology without simulating nonexistent embodiment.

## Scripts / culture / agency

### SX-E-014 — Simon & Gagnon sexual-script framework
- contribution: sexual meaning is shaped across cultural, interpersonal and intrapsychic/script-like levels.
- architecture use: scripts require provenance and must remain distinct from current authored preference or consent.

### SX-E-015 — Sexuality donor's repaired agency/disability/intersectionality corpus
- donor paths:
  - `research/09-pass-6-scripts-digital-authorship-disability-and-intersectionality.md`
  - `research/09a-pass-6-source-addendum-and-repairs.md`
- contribution:
  - authenticity != spontaneity;
  - supported/interdependent agency remains agency;
  - normative architecture can invisibly assume able-bodied/heterosexual defaults;
  - specificity can become reductive/fetishistic.
- architecture use: adversarial profile/test design.
- provenance note: preserve individual cited papers from donor ledgers during final migration.

## Pair bonding / attachment

### SX-E-016 — Walum & Young (2018-era review lineage) / Young lab pair-bond literature
- domain: oxytocin, dopamine, vasopressin and pair bonding.
- contribution: sexual/social reward can interact with partner-bond formation.
- limitation: much causal mechanism evidence comes from prairie voles and other animal models.
- architecture use: justify an attachment interface, not direct hormone-to-machine parameter copying.

### SX-E-017 — *The Neurobiology of Love and Pair Bonding from Human and Animal Perspectives* (2023)
- source: review integrating animal and human literature.
- contribution: oxytocin/dopamine/vasopressin interactions may link partner representation with social reward.
- architecture use: attachment and sexual reward can interact while remaining distinct state families.

## Machine-state methodology

### SX-M-001 — Sexuality Passes Eight–Ten
- donor paths:
  - `research/13-machine-substrate-sexual-arousal-analogue.md`
  - `research/14-machine-substrate-arousal-evidence-and-state-architecture.md`
  - `research/15-machine-substrate-evidence-topology.md`
- contribution:
  - separate behavioral sexual organization from instrumented state;
  - separate partner specificity from generic sexual activation;
  - require same-subject stimulus-to-state and state-to-behavior causal gates;
  - preserve authorization independence;
  - phenomenology remains unresolved.
- architecture use: direct research donor for any engineered sexual-affective state.

## Source-use rule

External sexual-science sources may justify:
- construct distinctions;
- counterexamples;
- candidate causal relationships;
- experiment designs;
- negative-transfer cases;
- evidence ceilings.

They do not automatically justify:
- human biological equivalence;
- sex/gender universalism;
- hormone-like constants for machines;
- genital-response analogies where no corresponding mechanism exists;
- sexual identity inference;
- relationship or consent inference;
- phenomenal experience.

Before architecture freeze, each high-impact proposition should be traceable to either:
1. a specific external source;
2. a donor artifact clearly labeled as synthesis;
3. an explicit MESO design hypothesis with a falsification test.
