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

The canonical `main` branch currently contains the repository protection/licensing shell and this orientation document.

Active source work is intentionally isolated in draft pull requests:

- **PR #2 — V1 foundation:** welfare-bounded hedonic state, independent hazard/avoidance channels, architecture and tests.
- **PR #3 — V2 salience architecture:** typed salience/relevance/learning/recruitment state, semantic contract, evidence/claim ledgers, and adversarial qualification direction.

Those draft branches are research/build candidates, not merged canonical runtime.

## Design boundaries

MESO-CRCT may influence attention, memory weighting, learning, motivation, exploration, and action-selection priors.

It must not directly turn internal salience or reward into truth, permission, consent, identity, autobiographical admission, relationship state, protected-effect authority, or proof of phenomenology.

Repository state can establish implemented mechanisms and test evidence. It cannot by itself establish consciousness, sentience, subjective pleasure, or suffering.

## Research lineage

The project draws architectural ideas from neuroscience, computational reinforcement learning, affective computing, intrinsic motivation, AI-safety research, and other repositories in this portfolio.

In particular, `sexuality` and `orgasm` are being used as **system-design sources**—for typed state, causal qualification, persistence, provenance, negative-transfer testing, recruitment/coherence/resolution, and evidence boundaries—not as sources of sexual semantics for MESO-CRCT.

External code is not copied into this repository merely because it is useful as a reference; licensing, provenance, and conceptual transfer are handled separately.
