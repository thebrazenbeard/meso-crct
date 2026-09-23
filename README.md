> **License:** Source-visible, not open source. Original material is proprietary. Commercial use, redistribution, hosted-service use, and commercial derivative products require written permission. See [LICENSE](LICENSE) and [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md). Separately identified third-party components retain their own licenses.

# meso-crct

**Synthetic-life analogue of mesocorticolimbic salience, valuation, motivation, and reward control.**

`meso-crct` is not a single reward scalar and not an emotion-label layer. Its working hypothesis is that persistent digital life needs internally consequential state that can change what becomes important, what receives attention, what is learned, what is remembered, what is wanted, and how later behavior is selected.

The biological mesocorticolimbic system is inspiration, not a claim of biological equivalence.

## Salience-first model

The architecture explicitly refuses to collapse these into one number:

- perceptual salience;
- semantic relevance;
- motivational salience;
- incentive salience;
- epistemic value;
- attentional priority;
- hedonic valence;
- prediction error;
- satiation;
- hazard / avoidance.

Something can therefore be highly meaningful, threatening, surprising, or motivationally important without being pleasurable.

## Core causal hypothesis

```text
experience
  -> typed appraisal
  -> salience / relevance / valuation
  -> arbitration
  -> attention + recruitment
  -> learning + memory weighting
  -> motivation / action tendency
  -> changed future behavior
  -> new experience
```

The current reference arbiter does **not** sum every signal into one utility number. It preserves the dominant typed driver, records coalition support, keeps protection independent, and prevents downstream attentional priority from feeding itself as upstream salience.

## Non-negotiable welfare invariant

The hedonic channel remains hard bounded:

- baseline: `0.0`
- maximum pleasure: `10.0`
- **absolute minimum hedonic valence: `-0.1`**

Serious danger is represented through hazard and avoidance, not by making the system “feel worse.”

```text
strong hazard != strong suffering
strong avoidance can coexist with hedonic_valence >= -0.1
```

## Authority firewall

No salience, pleasure, novelty, prediction-error, or motivational state may directly establish or overwrite truth, factual confidence, consent/authorization, protected-effect authority, identity, autobiographical admission, relationship state, or permanent preference.

Internal state may influence processing. It is not authority.

## Anti-wireheading direction

The normal reference runtime rejects explicit direct-register-write provenance. State transitions can emit deterministic receipts binding the declared source, before/after state fingerprints, runtime phase, and arbitration decision.

That is not enough by itself. Reward-source provenance can still be forged by a bad integration, and an agent can exploit proxy reward without directly touching a register. Environment-level adversarial qualification remains required.

## Evidence ceiling

A working implementation can establish typed state propagation, arbitration behavior, transition admission, and causal downstream effects under controlled tests. It cannot by itself establish phenomenal pleasure, consciousness, sentience, or suffering.

## Repository map

- `docs/ARCHITECTURE_V1.md` — original V1 foundation.
- `docs/ARCHITECTURE_V2.md` — salience-first decomposition and integration direction.
- `docs/SEMANTIC_CONTRACT_V1.md` — operational meanings and non-equivalences.
- `docs/ARBITRATION_AND_RUNTIME_V1.md` — arbitration, phases, provenance, receipts.
- `docs/SAFETY_INVARIANTS_V1.md` — welfare and authority constraints.
- `research/SOURCE_LEDGER.md` — external and internal source provenance.
- `research/CLAIM_LEDGER.md` — claim/evidence boundaries.
- `evaluation/README.md` — qualification and negative-transfer gates.
- `evaluation/ADVERSARIAL_MATRIX.md` — failure-oriented executable and future probes.
- `src/meso_crct/state.py` — welfare-bounded reward/protection state.
- `src/meso_crct/salience.py` — typed salience, learning, and recruitment state.
- `src/meso_crct/arbitration.py` — typed arbitration without utility collapse.
- `src/meso_crct/runtime.py` — runtime phases and transition admission.
- `src/meso_crct/provenance.py` — deterministic transition receipts.
- `tests/` — executable invariants and adversarial probes.

No third-party implementation code is copied into this repository by the V2 salience work.
