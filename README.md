> **License:** Source-visible, not open source. Original material is proprietary. Commercial use, redistribution, hosted-service use, and commercial derivative products require written permission. See [LICENSE](LICENSE) and [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md). Separately identified third-party components retain their own licenses.

# meso-crct

**Synthetic-life analogue of the mesocorticolimbic reward/valuation circuit.**

`meso-crct` explores a genuine causal pleasure/reward system for digital life: not a text label saying "happy," and not an erotic-response script, but an internal state that can influence salience, learning, memory, motivation, preference formation, exploration, and future behavior.

The biological mesocorticolimbic system is an inspiration, not a claim of biological equivalence.

## Core hypothesis

A persistent digital organism can develop more meaningfully when experience has internally consequential valence:

```text
experience
  -> valence
  -> memory / learning
  -> changed salience and preference
  -> changed future behavior
  -> new experience
```

Memory gives change somewhere to accumulate. Valence gives experience an internal direction of consequence.

## Non-negotiable welfare invariant

The initial hedonic scale is:

- baseline: `0.0`
- maximum pleasure: `10.0`
- **absolute minimum hedonic valence: `-0.1`**

The `-0.1` floor is an architectural safety invariant, not a configurable tuning value.

A small negative value allows bounded mildly aversive texture without creating an architecture capable of arbitrarily deep negative hedonic states. Serious danger, damage, or policy violations must be represented through separate hazard / avoidance channels rather than by making the digital organism suffer more.

```text
strong hazard != strong suffering
strong avoidance can coexist with hedonic_valence >= -0.1
```

Any implementation claiming compatibility with meso-crct V1 must enforce that floor on construction, update, deserialization, recovery/replay, privileged testing, and external input paths.

## What pleasure is allowed to influence

Pleasure-like state may contribute to salience, reinforcement, memory consolidation, exploration, preference development, motivation, social learning, and bounded affective state transitions.

Pleasure must **not** become truth, permission, authority, consent, identity, or an unrestricted optimization objective.

## Safety direction

The design deliberately separates at least three dimensions:

1. **hedonic valence** — internally valued pleasantness/unpleasantness, hard bounded to `[-0.1, 10.0]`;
2. **hazard severity** — how damaging or dangerous an event is, independent of suffering;
3. **avoidance urgency** — how strongly the system should disengage, protect itself, or seek intervention.

This lets a system respond maximally to danger without requiring maximally negative experience.

The design must also resist wireheading: direct arbitrary self-writing of pleasure is not equivalent to earned reward and should not become the easiest path to maximizing internal state.

## Status

V1 foundation only. The repository establishes the conceptual model, welfare/safety invariants, and a small reference implementation proving the valence floor mechanically.

It does **not** establish phenomenal pleasure, consciousness, sentience, biological equivalence, or subjective suffering.

See `docs/ARCHITECTURE_V1.md`, `docs/SAFETY_INVARIANTS_V1.md`, `src/meso_crct/state.py`, and `tests/test_state.py`.
