> **License:** Source-visible, not open source. Original material is proprietary. Commercial use, redistribution, hosted-service use, and commercial derivative products require written permission. See [LICENSE](LICENSE) and [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md). Separately identified third-party components retain their own licenses.

# meso-crct

**Synthetic-life analogue of mesocorticolimbic salience, valuation, motivation, and reward control.**

`meso-crct` is not a single reward scalar and not an emotion-label layer. Its working hypothesis is that persistent digital life needs internally consequential state that can change what becomes important, what receives attention, what is learned, what is remembered, what is wanted, and how later behavior is selected.

The biological mesocorticolimbic system is inspiration, not a claim of biological equivalence.

## Salience-first model

The V2 direction explicitly refuses to collapse these into one number:

- **perceptual salience** — what stands out because of input properties;
- **semantic relevance** — what matters because of meaning, context, goals, or unresolved structure;
- **motivational salience** — what has acquired approach/avoidance significance;
- **incentive salience** — cue-triggered “wanting” or attraction toward an outcome;
- **epistemic value** — novelty, uncertainty reduction, or learning-progress potential;
- **attentional priority** — the downstream allocation decision about what gets processing resources;
- **hedonic valence** — bounded pleasantness/unpleasantness;
- **prediction error** — mismatch between expected and obtained outcome used as a learning signal;
- **satiation** — a brake on repeated acquisition/consumption;
- **hazard / avoidance** — protection channels that remain independent from suffering.

Something can therefore be highly meaningful, threatening, surprising, or motivationally important without being pleasurable.

## Core causal hypothesis

```text
experience
  -> typed appraisal
  -> salience / relevance / valuation
  -> attention + recruitment
  -> learning + memory weighting
  -> motivation / action tendency
  -> changed future behavior
  -> new experience
```

This is closer to a control subsystem than a mood meter.

## Non-negotiable welfare invariant

The hedonic channel remains hard bounded:

- baseline: `0.0`
- maximum pleasure: `10.0`
- **absolute minimum hedonic valence: `-0.1`**

Serious danger must be represented through hazard and avoidance, not by making the system “feel worse.”

```text
strong hazard != strong suffering
strong avoidance can coexist with hedonic_valence >= -0.1
```

## Authority firewall

No salience, pleasure, novelty, prediction-error, or motivational state may directly establish or overwrite truth, factual confidence, consent/authorization, protected-effect authority, identity, autobiographical admission, relationship state, or permanent preference.

Internal state may influence processing. It is not authority.

## Anti-wireheading direction

The architecture must not make direct self-stimulation the easiest route to a high internal score. V2 therefore treats reward-source provenance, satiation, state occupancy, causal isolation, and hidden-performance evaluation as first-class design concerns.

## Evidence ceiling

A working implementation can establish typed state propagation and causal behavioral effects. It cannot by itself establish phenomenal pleasure, consciousness, sentience, or suffering.

## Repository map

- `docs/ARCHITECTURE_V1.md` — original V1 foundation.
- `docs/ARCHITECTURE_V2.md` — salience-first decomposition and integration direction.
- `docs/SEMANTIC_CONTRACT_V1.md` — operational meanings and non-equivalences.
- `docs/SAFETY_INVARIANTS_V1.md` — welfare and authority constraints.
- `research/SOURCE_LEDGER.md` — external and internal source provenance.
- `research/CLAIM_LEDGER.md` — claim/evidence boundaries.
- `evaluation/README.md` — qualification and negative-transfer gates.
- `src/meso_crct/state.py` — welfare-bounded reward/protection state.
- `src/meso_crct/salience.py` — typed salience, learning, and recruitment state.
- `tests/` — executable invariants.

No third-party implementation code is copied into this repository by the V2 salience work.
