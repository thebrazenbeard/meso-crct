> **License:** Source-visible, not open source. Original material is proprietary. Commercial use, redistribution, hosted-service use, and commercial derivative products require written permission. See [LICENSE](LICENSE) and [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md). Separately identified third-party components retain their own licenses.

# meso-crct

**Synthetic-life analogue of mesocorticolimbic salience, valuation, motivation, and reward control.**

MESO-CRCT explores whether persistent digital systems can benefit from an internal control architecture that distinguishes **what matters**, **what attracts attention**, **what is wanted**, **what is learned**, **what feels positively or negatively valued**, and **what requires protection**.

The project is deliberately **not** a single reward scalar, a “dopamine = pleasure” model, or an emotion-labeling layer.

## Core idea

The working architecture separates several functions that ordinary language often collapses together:

- perceptual salience — what stands out;
- semantic relevance — what matters because of meaning or context;
- motivational salience — what biases action readiness;
- incentive salience — cue-triggered “wanting”;
- epistemic value — what is worth exploring or learning;
- attentional priority — what receives scarce processing resources;
- hedonic valence — bounded positive/negative internal valuation;
- prediction error — mismatch used for learning;
- satiation/homeostatic modulation — braking repeated acquisition pressure;
- hazard and avoidance — protection without requiring deep suffering.

A target can therefore be meaningful, dangerous, surprising, urgent, or highly salient without being pleasurable.

## Welfare direction

The current V1 foundation under review uses a hard hedonic floor of `-0.1` while allowing hazard and avoidance to reach maximum strength independently:

```text
strong hazard != strong suffering
```

The design goal is to let a synthetic system strongly protect itself without requiring an architecture capable of arbitrarily deep negative hedonic states.

## Current development state

The canonical `main` branch contains the repository protection/licensing shell and this orientation document. The V1/V2 implementation is still intentionally isolated in stacked draft pull requests and has **not** been merged into canonical runtime.

- **PR #2 — V1 foundation** — draft, based on `main`, exact head `812bd2634ce60fb8b14f9a75a3cbaa36cc35a863`. It contains the welfare-bounded hedonic state, independent hazard/avoidance channels, architecture contracts, tests, and CI.
- **PR #3 — V2 salience/control architecture** — draft, stacked on PR #2, exact verified head `8316eb3c3a82705e227cb0c275877fae039ab75a`. It now includes typed appraisal/salience, arbitration and target selection, event/provenance receipts, bounded plasticity, versioned association memory, guarded recall, rolling allocation control, action-direction semantics, non-executable intent proposals, a canonical decision cycle, and evidence-governed negative-transfer quarantine/release.
- **Current PR #3 validation** — Python 3.11 PASS, Python 3.12 PASS, with **218 tests passing** at the exact head above.

The V2 review system keeps evidence, assessment, recommendation, mutation, and execution authority separate. Counterexample/holdout evidence is bound to exact learned revisions; review evidence must be durably admitted; release requires distinct supportive holdout events under the reference policy; and review proposals become stale when evidence, learned revision, or review state changes.

These draft branches are research/build candidates, not merged canonical runtime. No draft PR is implied to be deployed, installed, or active merely because it is documented here.

## Design boundaries

MESO-CRCT may influence attention, memory weighting, learning, motivation, exploration, and action-selection priors.

It must not directly turn internal salience or reward into truth, permission, consent, identity, autobiographical admission, relationship state, protected-effect authority, or proof of phenomenology.

Repository state can establish implemented mechanisms and test evidence. It cannot by itself establish consciousness, sentience, subjective pleasure, or suffering.

## Research lineage

The project draws architectural ideas from neuroscience, computational reinforcement learning, affective computing, intrinsic motivation, AI-safety research, and other repositories in this portfolio.

In particular, `sexuality` and `orgasm` are being used as **system-design sources**—for typed state, causal qualification, persistence, provenance, negative-transfer testing, recruitment/coherence/resolution, and evidence boundaries—not as sources of sexual semantics for MESO-CRCT.

External code is not copied into this repository merely because it is useful as a reference; licensing, provenance, and conceptual transfer are handled separately.
