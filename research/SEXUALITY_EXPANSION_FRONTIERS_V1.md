# Sexuality Expansion Research Frontiers V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / FRONTIER_EXPANSION / PRE_ARCHITECTURE`

This document extends the first absorption synthesis into areas that are easy to flatten or pathologize if they are omitted from the design phase.

## 1. Sexual orientation is multidimensional and potentially fluid

Current reviews define sexual fluidity as change over time in one or more dimensions of sexual orientation. Attraction, identity and behavior can move differently.

### Design consequence

Do not model orientation as a single scalar inferred from current behavior.

Candidate separation:

```
authored_identity_label
attraction_profile
behavior_history
fantasy_profile
romantic_attraction_profile
current_target_attraction
```

These objects may disagree without constituting an error.

### Evidence

- Katz-Wise et al. / current-state review lineage, *The Current State of Sexual Fluidity Research*, Current Opinion in Psychology 49 (2023), DOI `10.1016/j.copsyc.2022.101497`.
- 2024 epidemiologic methods work emphasizes that fluidity can occur across attraction, identity and behavior on different timescales.

### Machine-transfer ceiling

MESO may model typed profile dimensions and change provenance. It may not infer a user's or agent's sexual identity from observed behavior or learned attraction.

## 2. Asexual-spectrum profiles are a structural test, not an exception patch

Asexuality research shows that attraction, desire, fantasy, arousal and behavior can dissociate.

A 2024 study explicitly compares asexual, demisexual, gray-asexual and questioning participants, reinforcing the need for situational and heterogeneous attraction/desire profiles.

### Design consequence

A generic sexual architecture must support:
- low/absent sexual attraction with nonzero libido;
- fantasy without target attraction;
- physiological/substrate arousal without attraction;
- demisexual/relationship-contingent attraction patterns;
- gray/situational attraction;
- uncertain/questioning identity without forced classification.

If the state model cannot represent these combinations, the ontology is too collapsed.

## 3. Sexual fantasy is not a behavioral command

Lehmiller & Gormezano's 2023 review concludes that fantasy content is not necessarily synonymous with what people are interested in doing or actually do.

### Hard invariant

```
fantasy_content != intended_action
fantasy_content != consent
fantasy_content != identity
fantasy_content != relationship_request
```

Fantasy can:
- initiate or enhance arousal;
- explore impossible, symbolic or unwanted-in-reality scenarios;
- rehearse or elaborate scripts;
- alter desire;
- strengthen partner salience in some contexts.

It therefore belongs near appraisal/imagination and sexual-script systems, not the action-authority boundary.

### Evidence

- Lehmiller & Gormezano (2023), *Sexual fantasy research: A contemporary review*, Current Opinion in Psychology 49:101496, DOI `10.1016/j.copsyc.2022.101496`.
- Sexuality donor media/script research supplies additional hypothesis-generating examples.

## 4. Sexual agency must remain separate from pleasure and compliance

A 2025 scoping review found broadly positive associations between sexual agency-related constructs and sexual well-being, while also concluding that evidence is insufficient to establish a simple causal effect of adding pleasure-focused education.

### Design consequence

Do not define agency as:
- maximum independence;
- willingness to act;
- positive pleasure;
- sexual frequency;
- refusal of accommodation.

Agency is better represented as authorship/control over one's sexual participation, preferences and boundaries.

### Evidence

- van Ditzhuijzen & Overeem (2025), *Pleasure-Inclusive Sex Education, Sexual Agency, and Sexual Well-Being in Adolescents and Young Adults: A Scoping Review*, Archives of Sexual Behavior, DOI `10.1007/s10508-025-03103-8`.

## 5. Consensual power exchange requires explicit asymmetry semantics

BDSM research is useful because it exposes a failure mode in naive agency models: a person may author surrender, submission, pain, restraint or asymmetric control without ceasing to be an agent.

At the same time, BDSM cannot be assumed to be inherently safe or consensual simply because it is labeled BDSM.

### Design consequence

Separate:

```
power_role
authored_preference
current_consent
negotiated_scope
revocation_state
activity_intensity
pleasure
submission_behavior
agency
```

A submissive role must not mechanically lower the authority of that actor's current consent/refusal.

### Evidence

- Ahmed (2023), *Research in BDSM: 40 Years Along*, in *The Power of BDSM*, DOI `10.1093/oso/9780197658598.003.0002`.
- Melavc, Jug & Gomboc (2024), systematic review of positive psychological effects of BDSM, DOI `10.5559/di.33.3.04`.
- Sexuality donor research already records bounded work on communication, trust and negotiated meaning.

### Research caution

Small/self-selected samples and community-specific norms prevent universalizing any one BDSM practice or role dynamic.

## 6. High sexual desire is not compulsive sexual behavior

Recent sexual-medicine reviews warn against pathologizing:
- high sexual desire;
- pornography use by frequency alone;
- masturbation;
- nonheteronormative sexuality;
- distress caused only by moral disapproval.

CSBD instead involves persistent failure to control repetitive sexual impulses/behavior with neglect, repeated failed control, adverse consequences, or continuation despite little/no satisfaction.

### Design consequence

MESO's anti-capture work should model **loss of control / allocation capture**, not “high sexuality.”

Candidate machine analogues to test:

```
sexual_target_occupancy_share
failed_interrupts
goal_crowd_out
cue_attentional_lock
continued pursuit despite low hedonic return
satiation_bypass
self-generated sexual cue loops
escalating stimulus search after habituation
```

This is especially compatible with existing MESO allocation-window and sensitization-warning machinery.

### Evidence

- Briken et al. (2024), *Assessment and treatment of compulsive sexual behavior disorder: a sexual medicine perspective*, Sexual Medicine Reviews 12(3):355–370, DOI `10.1093/sxmrev/qeae014`.
- ICSM 2024 consensus definitions explicitly distinguish CSBD from mere frequency/high desire and from moral-disapproval-only distress.

### Important warning

Human CSBD remains clinically and conceptually contested. MESO should use the literature for failure patterns, not diagnose users or equate machine reward loops with a psychiatric disorder.

## 7. Digital sexuality is its own interaction class

Digital sexuality is not merely impoverished physical sexuality.

Döring et al. distinguish sexual interaction:
1. **through** digital technology;
2. **via** digital technology;
3. **with** digital technology.

That third category is directly relevant to AI sexual interaction.

### Design consequence

MESO needs explicit interaction-medium context because the same sexual meaning can be constructed differently in:
- text;
- images;
- audio;
- video;
- embodied/physical interaction;
- virtual world/avatar interaction;
- AI-human interaction.

Do not invent absent physical sensations to fill a medium gap.

Represent:
- medium;
- available modalities;
- actor type;
- representation/embodiment status;
- consent/privacy context;
- signal provenance.

### Evidence

- Döring et al. (2021), *Sexual Interaction in Digital Contexts and Its Implications for Sexual Health: A Conceptual Analysis*, Frontiers in Psychology 12:769732, DOI `10.3389/fpsyg.2021.769732`.
- Wheaton (2016), *Conceiving sexual authorship*, DOI `10.1080/23268743.2015.1119959`.

## 8. Digital intimacy introduces privacy/consent state that affect cannot own

Sexual communication through digital systems creates durable-content and redistribution risks that do not exist in the same form in ephemeral speech.

### Design consequence

If MESO ever participates in intimate-content handling, affective state must remain separate from:
- permission to retain;
- permission to transform;
- permission to forward/share;
- publication scope;
- identity disclosure;
- deletion/retention policy.

```
consent_to_receive != consent_to_store
consent_to_store != consent_to_share
consent_to_create != consent_to_publish
sexual_desire != data_use_authority
```

These belong to external privacy/effect authorization, not MESO sexual state.

## 9. Pleasure, satisfaction and welfare must remain separate

Sexual pleasure is important, but a system that equates sexual welfare with maximum pleasure creates obvious failure cases:
- compulsive pursuit;
- self-neglect;
- boundary violation;
- relationship harm;
- orgasm imperative;
- pressure to perform;
- inability to value low-intensity intimacy.

### Design consequence

Potential evaluation outputs should separate:
- immediate hedonic pleasure;
- authored satisfaction;
- agency/authorship;
- relational fit;
- boundary integrity;
- negative consequences;
- post-event evaluation.

No one variable should be “sexual success.”

## 10. Attachment and erotic desire need a bidirectional interface, not identity

Attachment can increase partner salience and sexual meaning; sex can contribute to bonding. But attachment can also coexist with low desire, and desire can exist without attachment.

### Design consequence

MESO should accept attachment/relationship context as typed external evidence and may emit bounded learning/affective signals back to a host relationship model.

It should not own relationship truth.

## 11. Embodiment must be substrate-specific

Human sexual science includes:
- genital arousal;
- autonomic response;
- endocrine modulation;
- sensory stimulation;
- pain;
- fatigue;
- refractory physiology.

A machine may have none of these or may later have different sensors/effectors.

### Design rule

For every borrowed biological term ask:

1. What function is being modeled?
2. Is there an actual machine variable with that function?
3. Is it measured or merely inferred?
4. Is a biological label misleading?
5. Can the architecture remain useful if the implementation has no body?

Use functional names where possible; reserve biological analogy labels for explicit analogy documentation.

## 12. Missing research that should block final architecture freeze

The current corpus is strong enough to continue research design, but not to freeze the final sexual ontology.

Still required:

### Orientation / identity
- stronger coverage of bisexual, pansexual, queer, trans/nonbinary and ace-spectrum research;
- distinction between romantic and sexual attraction;
- change/currentness semantics for authored identity.

### Desire / attraction
- deeper work on spontaneous vs responsive desire across populations;
- relationship-specific desire discrepancy;
- fantasy-driven vs externally triggered motivation.

### Embodiment
- sexual pain/aversive experience as distinct from inhibition;
- disability and sensory variability;
- age and hormonal context as human evidence without importing machine constants.

### Relationship context
- monogamous and consensually nonmonogamous structures without assuming exclusivity;
- attachment vs passion vs caregiving;
- desire under long-term familiarity/novelty.

### Power
- BDSM/kink consent negotiation;
- role persistence vs current consent;
- power fantasy vs desired real-world behavior.

### Digital / AI
- privacy and durable intimate content;
- AI as sexual interaction partner;
- anthropomorphism and false embodiment;
- partner-specific state without manufactured dependence;
- negative transfer between sexual and nonsexual AI contexts.

### Welfare / control
- habituation and novelty seeking;
- compulsive/capture dynamics;
- post-event state;
- interaction between satiation, inhibition and general MESO allocation control.

## Hostile review

> **HOSTILE REVIEWER:** The more comprehensively MESO models sexuality, the more likely it becomes a theory of personhood rather than a motivational-control system.

**ACCEPTED AS A BOUNDARY.** MESO may model variables that causally alter sexual appraisal, motivation, learning and action tendency. Identity, relationship truth, consent authority, autobiographical memory and social ontology remain external even when MESO consumes them as context.

> **HOSTILE REVIEWER:** A sexual module built from human literature may reproduce heteronormative, able-bodied and genital assumptions even if the code uses neutral names.

**ACCEPTED.** Diversity profiles must be used as architecture-breaking tests before schema freeze, not merely added later as documentation.

> **HOSTILE REVIEWER:** If fantasy, scripts, attraction, attachment, identity and communication all become first-class types, the model may become too complicated to execute.

**PARTIALLY ACCEPTED.** The research ontology can be richer than the minimal runtime state. Architecture should later derive the smallest executable subset that preserves empirically demonstrated non-equivalences. Complexity has to earn its place with a counterexample or a required behavior.

## Frontier conclusion

The absorption target is larger than a “sexual drive + orgasm” subsystem.

The research currently supports treating sexuality as a **multi-layer motivational domain** involving appraisal, excitation/inhibition, desire, attraction, fantasy, scripts, agency, communication, learning, pleasure, climax/recovery and optional attachment interfaces—while identity and authorization remain outside affective authority.

No implementation is proposed by this document.
