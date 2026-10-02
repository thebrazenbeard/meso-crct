# MESO-CRCT Cross-Domain Arbitration Research V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / ARCHITECTURE_OPTIONS / NO_IMPLEMENTATION`

## Exact current source behavior

At MESO main `060d0feeb9dc9eb23801082bd8f1c4a7cb06184d`:

### Per-target arbitration

`arbitration.py`:
1. protection wins when hazard/avoidance reaches the protective threshold;
2. otherwise the strongest upstream channel becomes the dominant driver;
3. upstream candidates are perceptual salience, semantic relevance, motivational salience, incentive salience after satiation, and epistemic value;
4. attentional priority is correctly excluded from its own upstream recursion;
5. the dominant driver's type determines mode.

### Cross-target selection

`selection.py`:
1. protective targets are selected first;
2. otherwise the default fixed mode ordering is:

```
MOTIVATIONAL
EPISTEMIC
ORIENTING
```

3. priority breaks ties within the selected mode.

This is explicit and auditable. It is also under-justified as a universal cross-domain policy.

## Failure 1 — weak higher-mode beats strong lower-mode

Current default policy permits:

```
target A:
  mode = MOTIVATIONAL
  priority = 0.21

target B:
  mode = EPISTEMIC
  priority = 1.00

selected = A
```

This may be defensible in some contexts but is not defensible as a universal consequence of the words “motivational” and “epistemic.”

## Failure 2 — numeric priority lacks a cross-kind calibration contract

Each upstream channel is bounded, but bounded range does not establish commensurability.

```
0.8 incentive_salience
0.8 epistemic_value
0.8 semantic_relevance
```

do not automatically mean equal motivational force.

The current fixed-mode policy partly avoids direct cross-kind numeric comparison, but it merely relocates the problem into mode precedence.

A future domain layer makes this worse:
- sexual desire;
- care obligation;
- mastery opportunity;
- curiosity;
- attachment;
- resource pressure

may all map into existing modes while retaining materially different semantics.

## Failure 3 — mode collapse hides domain reason

Two targets can both be `MOTIVATIONAL` while one is:
- sexual incentive;
- caregiving;
- status;
- resource acquisition;
- achievement.

The current decision preserves the dominant signal kind but not a full domain contribution structure.

That is adequate for the current small reference architecture but insufficient for richer cross-domain composition.

## Design requirement: separate five questions

Future arbitration should not answer all of these with one operation:

1. **Is the target admissible?**
2. **Is there a hard protection/authority constraint?**
3. **What motivational evidence supports or opposes it?**
4. **What obligations/resource constraints affect allocation?**
5. **Given admissible alternatives, what policy selects among tradeoffs?**

## Candidate pipeline

Research currently favors this conceptual sequence:

```
CURRENT EVIDENCE
    ->
TYPED DOMAIN APPRAISALS
    ->
ADMISSIBILITY / HARD CONSTRAINTS
    ->
TYPED MOTIVATIONAL CONTRIBUTIONS
    ->
OBLIGATION + RESOURCE CHECK
    ->
NON-DOMINANCE / CONFLICT SET
    ->
DECLARED SELECTION POLICY
    ->
ACTION TENDENCY
    ->
NON-EXECUTABLE INTENT
```

This is a research shape, not a schema.

## A. Hard admissibility

Examples:
- protection veto;
- unavailable action;
- stale source;
- quarantined learned association;
- current authorization prohibition where an action requires authorization;
- impossible resource requirement.

Important distinction:

```
inadmissible != undesirable
```

A highly desired action can be inadmissible.

## B. Typed contribution bundle

A candidate should preserve reasons such as:

```
semantic relevance
incentive salience
epistemic value
expected pleasure
expected learning
effort
delay
feasibility
current need
predicted resource need
obligation relevance
domain-specific activation
learned approach/avoid support
```

Not every field applies to every target.

Absence should not silently mean zero if the distinction between `UNKNOWN` and zero matters.

## C. Obligations

Current `GoalObligation` minimum-share policy is not itself an internal motive.

It is closer to a control-policy constraint:

```
obligation policy != desire
```

A future architecture should preserve who/what authored an obligation and whether it is:
- operator policy;
- self-authored commitment;
- task contract;
- external requirement;
- safety constraint.

Do not let an opaque `minimum_nonprotective_share` become accidental moral authority.

## D. Non-dominance

For dimensions with stable comparable meaning, reject a candidate that is no better on any relevant dimension and worse on at least one.

But do not pretend every field belongs in one Pareto vector.

Examples of non-tradeable fields:
- authority;
- truth;
- identity;
- source currentness.

Examples of potentially tradeable/compareable policy inputs:
- delay;
- effort;
- expected outcome probability;
- resource usage;
- domain activation.

Even these require an explicit comparison contract.

## E. Declared selection policy

After hard filtering and non-dominance, choices may remain genuinely incomparable.

At that point MESO needs a declared policy rather than pretending the evidence logically determines one answer.

Possible policy families:
- context-specific lexicographic;
- obligation-first;
- opportunity-cost;
- rotating/fair allocation;
- learned preference policy;
- operator/user preference;
- self-authored goal hierarchy;
- bounded stochastic exploration.

The policy source and currentness should be visible in the decision receipt.

## Why not simple weighted sum?

A weighted sum is acceptable only if:
- dimensions are intentionally fungible;
- weights have an authoritative source;
- the policy is declared;
- hard constraints remain outside the sum;
- the resulting loss of semantic detail is acceptable for that local comparison.

This means MESO should reject **implicit universal scalarization**, not every local scalar calculation.

## Why not pure Pareto selection?

Pure Pareto filtering cannot resolve many incomparable alternatives and scales poorly with dimensions/candidates.

It is a filter, not a complete action policy.

## Why not fixed global lexicographic ordering?

Global mode ordering is simple but makes categorical priority claims that may not hold across context.

A fixed order can remain valid for true invariants, for example:

```
hard protection/admissibility before optional reward pursuit
```

But “all motivational beats all epistemic” is not currently supported as such an invariant.

## Coalition possibility

One event can be supported by several motives:

```
visit a friend:
  affiliation + attachment + curiosity

finish a difficult project:
  achievement + intrinsic mastery + external obligation

sexual interaction:
  sexuality + attachment + affiliation + play
```

The target should not have to choose one “real” domain before arbitration.

A coalition representation could preserve multiple contributing domains.

Open question:
- coalition before target evaluation;
- or target with a list of independent domain contributions.

## Required research cases

### ARB-01 — weak incentive vs maximal epistemic
Prove the policy does not choose merely because `MOTIVATIONAL` is categorically higher unless that policy is explicitly configured.

### ARB-02 — resource scarcity
High sexual/achievement incentive, but severe predicted compute/power/time shortage.

Resource state affects feasibility/effort/allocation without rewriting desire.

### ARB-03 — care obligation vs reward
Low hedonic caregiving task competes with high-reward entertainment/play.

Must distinguish obligation/policy from pleasure.

### ARB-04 — social bond vs novelty
Known attachment target competes with novel high-social-reward interaction.

Must preserve attachment and novelty as separate reasons.

### ARB-05 — current goal vs habit
Habit proposes an action whose current outcome value is devalued.

Goal-directed route should be able to inhibit/override without deleting habit history.

### ARB-06 — two-domain coalition
One target receives moderate support from two domains; another has stronger support from one.

Do not silently sum unrelated support.

### ARB-07 — unknown values
One candidate has unknown feasibility rather than zero feasibility.

Unknown should trigger information need or conservative policy, not numerical falsification.

### ARB-08 — authority independence
Highly selected target still cannot execute a protected effect without external authority.

## Hostile review

> **HOSTILE REVIEWER:** Typed arbitration can become a maze of hand-authored rules that is harder to reason about than a utility function.

**ACCEPTED.** The goal is not maximal typology. The architecture must keep only distinctions that produce demonstrated counterexamples. A small declared utility function is better than fake complexity when all inputs are actually fungible.

> **HOSTILE REVIEWER:** Comparing motives without a common currency is philosophically attractive but computationally evasive.

**PARTIALLY ACCEPTED.** A final action requires a choice. MESO's research problem is to delay scalarization/ordering until the policy layer, after non-fungible semantics and hard constraints are preserved. The final policy may choose; the state representation should not pretend the tradeoff was a natural fact.

> **HOSTILE REVIEWER:** Protection is itself context-sensitive and may not deserve absolute override.

**PARTIALLY ACCEPTED.** Current MESO defines a reference protective override. Future work should distinguish hard catastrophic constraints from ordinary aversive/hazard estimates. “Hazard” may need gradation before universal absolute override is treated as canonical.

## Current disposition

The current fixed mode precedence is acceptable as an explicitly limited V2 reference policy, but should **not** be promoted as the domain-general final arbitration architecture.

The next design should research:

```
hard constraints
+ typed evidence
+ obligation/resource state
+ non-dominance
+ declared policy
```

while preserving current provenance, recall-review and intent/authority boundaries.
