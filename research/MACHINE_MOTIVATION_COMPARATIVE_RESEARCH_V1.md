# MESO-CRCT Machine Motivation Comparative Research V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / MACHINE-SIDE COMPARISON / NO_IMPLEMENTATION`

## Purpose

Human neuroscience supplies useful distinctions, but MESO is an engineered machine architecture. This pass asks whether reinforcement learning, developmental robotics, multi-objective control and safe-RL literature provide cleaner computational abstractions than biological analogy.

## 1. Multi-objective RL validates the problem, not MESO's solution

Modern MORL explicitly recognizes that real tasks contain multiple conflicting objectives and commonly represents reward as a vector rather than one scalar.

That aligns with MESO's refusal to treat:
- pleasure;
- hazard;
- epistemic value;
- incentive salience;
- effort;
- social motives;
- domain-specific relevance

as interchangeable.

However, many MORL methods eventually scalarize the objective vector to choose a policy.

MESO should not assume scalarization is wrong in every engineering context. It should instead ask:

> When does scalarization destroy distinctions that MESO has declared semantically or normatively non-fungible?

Examples:
- hazard must not be traded against pleasure by an arbitrary weight;
- authorization must not enter reward optimization at all;
- truth confidence must not be purchased by reward;
- domain-specific state should remain inspectable after arbitration.

## 2. Pareto reasoning is useful but insufficient

Pareto-optimal reasoning can preserve multiple objectives without a fixed weighted sum.

Useful property:
- a candidate that is worse on every relevant dimension can be rejected without defining a common unit.

Limitation:
- Pareto sets can be large;
- incomparability does not itself choose an action;
- normative hard constraints still need explicit representation;
- a learned Pareto frontier does not preserve semantic source/provenance by itself.

MESO can borrow the idea of non-dominance without becoming a MORL library.

## 3. Constrained optimization resembles MESO protection more closely than ordinary reward tradeoff

Safe-RL literature often formulates problems as:

```
maximize objective
subject to constraint
```

MESO's protection/authority boundaries often have this character.

Examples:

```
do not violate protection
do not treat authorization as reward
do not use quarantined memory
do not execute protected effects without authority
```

This supports an architectural distinction among:

1. **hard admissibility constraints**;
2. **typed motivational evidence**;
3. **preference/trade-off policy**.

Those should not be represented as peer reward terms.

## 4. Current MESO arbitration has a hidden policy problem even without a scalar utility

The current implementation avoids weighted sums but uses fixed nonprotective mode precedence:

```
MOTIVATIONAL > EPISTEMIC > ORIENTING
```

followed by within-mode priority.

This creates a discontinuity:

```
motivational priority = 0.21
epistemic priority    = 1.00
=> motivational target wins locally
```

The policy is transparent, which is better than a hidden weighted sum, but transparency does not make the ordering justified.

This becomes more problematic as new domains arrive.

A sexuality target, caregiving target and achievement target could all currently collapse into `MOTIVATIONAL` mode and then compete by a single `priority` field whose calibration may not be equivalent across domains.

## 5. Core research target: typed comparison without accidental fungibility

Future research should compare at least four families of arbitration:

### A. Fixed lexicographic precedence

Example:
```
protection > obligation > motivational > epistemic > orienting
```

Strengths:
- easy to audit;
- can encode hard priorities.

Weaknesses:
- brittle;
- weak high-rank signals dominate strong lower-rank signals;
- hard to justify universal ordering.

### B. Constrained typed selection

Example:
1. reject inadmissible targets;
2. enforce minimum obligations/resource constraints;
3. compare remaining candidates within a declared policy.

Strengths:
- aligns with safe-RL constraint formulations;
- keeps protection outside tradeoff.

Weakness:
- still needs a comparison rule after constraints.

### C. Pareto / non-dominance filtering

Keep typed dimension vectors and eliminate strictly dominated candidates before policy selection.

Strengths:
- preserves non-fungibility longer;
- exposes tradeoffs.

Weaknesses:
- many candidates remain incomparable;
- dimensional normalization and relevance still matter.

### D. Coalition/evidence-based arbitration

Each target carries a typed evidence bundle:
- motive classes;
- source/currentness;
- activation;
- expected benefit;
- effort;
- delay;
- feasibility;
- learning/information value;
- obligation;
- resource pressure;
- protection.

A policy chooses from the evidence structure rather than from one reward vector.

Strengths:
- best fit with current MESO semantics;
- preserves explanation and reversibility evidence.

Weakness:
- policy complexity;
- risk of recreating hand-written utility through many rules.

Current research preference: **B + C + D hybrid for further study**, not implementation:
- hard constraints/admissibility first;
- Pareto/non-dominance where dimensions are meaningfully comparable;
- explicit policy over remaining typed evidence;
- full explanation receipt.

## 6. Intrinsic motivation research supports typed epistemic motives

Information-theoretic intrinsic-motivation work distinguishes novelty, surprise and skill learning.

This supports MESO's current decision not to equate:
```
novelty
surprise
learning progress
epistemic value
```

A future curiosity profile should likely use those as typed evidence rather than one `curiosity_reward`.

## 7. Homeostatic RL supports state-dependent reward but exposes a warning

Homeostatic RL and related models show how reward can depend on internal state and deviation from viable ranges.

Useful lesson:
- the same external outcome can have different motivational value under different internal state.

Warning:
- if all need satisfaction becomes scalar reward, independent need semantics disappear.

MESO's current strongest-match need modulation is deliberately conservative. Future work on allostasis should preserve need identity and source evidence even if a learning algorithm consumes a derived teaching signal.

## 8. Multi-objective decomposition is conceptually useful for domain profiles

MORL decomposition methods preserve separate objective contributions and can learn different compromises.

MESO domain profiles could similarly remain separate contributors:
```
sexuality
curiosity
caregiving
achievement
affiliation
resource regulation
...
```

But profiles should not be treated as objectives with arbitrary human-authored weights by default.

A profile may contain several motives internally, and one event may activate multiple profiles.

## 9. Machine resource motivation should use real substrate evidence

A machine allostatic/resource profile should not imitate hunger unless there is an actual analogous controlled quantity.

Candidate real machine resources:
- available compute;
- power/energy;
- thermal margin;
- memory pressure;
- storage;
- network budget;
- latency budget;
- context/token budget;
- rate limits;
- deadline slack;
- task backlog.

A host resource sensor can provide current/predicted state to MESO.

Hard boundary:
```
resource pressure != suffering
resource pressure != permission
resource pressure != truth
```

## 10. Preference learning vs motivational state

Interactive MORL sometimes learns a user's utility/preferences.

MESO must keep:
```
learned operator preference
    !=
agent motivational state
    !=
protected-effect authority
```

A learned preference model may shape ordinary choice but cannot manufacture authority.

## 11. Why MESO should not simply become an RL agent

MESO's useful role is narrower and more inspectable:

```
evidence + internal state
    -> typed appraisal
    -> motivation/learning/control state
    -> bounded selection/tendency proposal
```

The host can use those outputs inside a larger policy/runtime.

Making MESO itself an unconstrained end-to-end RL policy would:
- blur motivation with action policy;
- make semantic invariants harder to inspect;
- create more direct reward-hacking paths;
- weaken the existing intent/authorization/execution separation.

A trained policy can later consume MESO state or be evaluated against MESO invariants without MESO becoming identical to that policy.

## 12. Research consequences for sexuality

The machine-side review reinforces the corrected placement:

- sexuality supplies domain-specific appraisal/state;
- MESO supplies general learning, allocation, effort, temporal and reward machinery;
- sexual state does not become the global objective;
- orgasm/climax does not become a generic reward terminal;
- sexual reward may teach bounded associations but does not author identity/consent/relationship truth.

## Hostile review

> **HOSTILE REVIEWER:** MESO's typed architecture may be elegant documentation around an arbitrary hand-coded policy. A learned MORL policy could outperform it while handling tradeoffs automatically.

**PARTIALLY ACCEPTED.** Learned policies may outperform fixed rules. MESO's value proposition is semantic separation, inspectability, provenance and hard invariants. Future research should test whether a learned policy can operate over typed MESO state while remaining constrained by those invariants rather than replacing them.

> **HOSTILE REVIEWER:** Refusing scalarization entirely can make action selection impossible.

**ACCEPTED.** MESO should reject *unjustified hidden scalarization*, not mathematics. Local scalar comparisons may be appropriate within a semantically coherent dimension or a declared policy. The architectural requirement is that non-fungible dimensions and hard constraints are not silently converted into exchange rates.

> **HOSTILE REVIEWER:** A Pareto/evidence hybrid may be computationally excessive for ordinary agent decisions.

**ACCEPTED AS A PERFORMANCE CONSTRAINT.** Research should seek a minimal decision rule that preserves necessary distinctions. Expensive frontier computation is not a requirement.

## Current result

Machine-side research supports MESO as a typed motivational-control layer rather than a universal reward function or end-to-end RL agent.

The most important next architecture problem is **cross-domain arbitration**:
- how to compare co-active motives;
- which states are hard constraints;
- which dimensions are genuinely comparable;
- how to preserve reason/provenance through selection;
- how to avoid both hidden scalar utility and brittle global precedence.

No implementation is proposed here.
