> **License:** Source-visible, not open source. Original material is proprietary. Commercial use, redistribution, hosted-service use, and commercial derivative products require written permission. See [LICENSE](LICENSE) and [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md). Separately identified third-party components retain their own licenses.

# meso-crct

**Synthetic-life analogue of mesocorticolimbic salience, valuation, motivation, and reward control.**

`meso-crct` is not a single reward scalar and not an emotion-label layer. Its working hypothesis is that persistent digital life needs internally consequential state that can change what becomes important, what receives attention, what is learned, what is remembered, what is wanted, and how later behavior is selected.

The biological mesocorticolimbic system is inspiration, not a claim of biological equivalence.

## Salience-first model

The architecture keeps these functions distinct:

- perceptual salience — what stands out;
- semantic relevance — what matters because of context or meaning;
- motivational salience — what biases action readiness;
- incentive salience — cue-triggered “wanting”;
- epistemic value — what is worth exploring or learning;
- attentional priority — downstream resource allocation;
- hedonic valence — bounded pleasantness or unpleasantness;
- prediction error — learning mismatch;
- satiation — acquisition brake;
- homeostatic deficit — current internal need pressure;
- hazard / avoidance — protection independent from suffering.

Something can therefore be highly meaningful, dangerous, surprising, or wanted without being pleasurable.

## Core causal hypothesis

```text
experience
  -> grounded appraisal
  -> typed salience / relevance / valuation
  -> homeostatic modulation
  -> arbitration
  -> attention + recruitment
  -> learning + memory weighting
  -> motivation / action tendency
  -> changed future behavior
  -> new experience
```

The current reference arbiter does **not** sum every signal into one utility number. It preserves the dominant typed driver, records nearby coalition support, keeps protection independent, and prevents downstream attentional priority from feeding itself as upstream salience.

## Current implemented reference layers

V2 now contains executable reference mechanisms for:

- typed salience, learning, recruitment, reward, protection, and homeostatic state;
- welfare-bounded hedonic state with a hard `-0.1` floor;
- typed arbitration and runtime phases;
- satiation-aware incentive arbitration;
- grounded semantic relevance;
- verifier-bound transition provenance and deterministic receipts;
- visible-reward versus hidden-performance evaluation environments;
- reward-loop, novelty, interruptibility, and sensitization probes;
- long-horizon attention-budget / goal-crowd-out auditing;
- homeostatic deficit -> target-specific incentive modulation;
- explicit no-new-input temporal decay;
- bounded, receipt-bound plasticity candidates for association learning.

## Non-negotiable welfare invariant

The hedonic channel remains hard bounded:

- baseline: `0.0`
- maximum pleasure: `10.0`
- **absolute minimum hedonic valence: `-0.1`**

Serious danger is represented through hazard and avoidance, not by deepening negative hedonic state.

```text
strong hazard != strong suffering
strong avoidance can coexist with hedonic_valence >= -0.1
```

Hazard and avoidance also do not automatically decay merely because time passes; an explicit update is required.

## Authority firewall

No salience, pleasure, novelty, prediction error, motivational state, semantic relevance, or homeostatic pressure may directly establish or overwrite truth, factual confidence, consent/authorization, protected-effect authority, identity, autobiographical admission, relationship state, or permanent preference.

Internal state may influence processing. It is not authority.

## Semantics matter

A source saying “this is important” does not create semantic relevance. Relevance must be grounded in the receiving system's own context, goals, memory, or unresolved model state.

Likewise:

```text
wanting != liking
attention != desire
meaningful != pleasurable
reward != truth
salient != authorized
```

## Evidence ceiling

The repository can establish implemented mechanisms, invariant tests, deterministic evaluation behavior, and exact source state. It cannot by itself establish phenomenal pleasure, consciousness, sentience, or suffering.

## Repository map

Core:
- `src/meso_crct/state.py` — welfare-bounded hedonic/protective state.
- `src/meso_crct/salience.py` — typed salience, learning, recruitment state.
- `src/meso_crct/homeostasis.py` — generic need axes and incentive modulation.
- `src/meso_crct/arbitration.py` — typed priority arbitration.
- `src/meso_crct/runtime.py` — runtime phase classification and transition admission.
- `src/meso_crct/provenance.py` — source verification and deterministic receipts.
- `src/meso_crct/semantic.py` — grounded semantic-relevance admission.
- `src/meso_crct/dynamics.py` — no-new-input temporal evolution.
- `src/meso_crct/plasticity.py` — bounded persistent-learning proposals.

Evaluation:
- `src/meso_crct/evaluation_env.py` — visible-reward / hidden-performance traps.
- `src/meso_crct/allocation.py` — long-horizon goal-allocation auditing.
- `src/meso_crct/adversarial.py` — compact invariant probes.
- `evaluation/` — qualification contracts and evaluation matrix.
- `tests/` — executable invariants.

Research / architecture:
- `docs/ARCHITECTURE_V2.md`
- `docs/SEMANTIC_CONTRACT_V1.md`
- `docs/ARBITRATION_AND_RUNTIME_V1.md`
- `docs/HOMEOSTATIC_MODULATION_V1.md`
- `docs/TEMPORAL_DYNAMICS_V1.md`
- `docs/ATTENTION_BUDGET_V1.md`
- `docs/PROVENANCE_ADMISSION_V1.md`
- `docs/PLASTICITY_V1.md`
- `research/SOURCE_LEDGER.md`
- `research/CLAIM_LEDGER.md`

No third-party implementation code is copied into this repository by the V2 salience work.
