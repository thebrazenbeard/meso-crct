# MESO-CRCT Coalition and Dimension-Stuffing Research V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / ARBITRATION BLOCKER / NO IMPLEMENTATION`

## Purpose

The current domain-general research identified a failure mode for typed cross-domain arbitration:

> A target can appear stronger merely because one profile or coalition emits many overlapping weak contributions.

Example:

```
target A:
  social_relevance_1 = 0.20
  social_relevance_2 = 0.20
  social_relevance_3 = 0.20
  social_relevance_4 = 0.20
  social_relevance_5 = 0.20

target B:
  epistemic_value = 0.85
```

If A wins because five weak fields are summed, the architecture has recreated scalar utility through **dimension stuffing**.

This pass asks how to preserve genuine multi-motive coalitions without rewarding redundant criteria.

## External decision-research constraint

Multi-criteria decision analysis has treated criterion interaction and compensability as first-class problems for decades.

Key lessons relevant to MESO:

1. Additive weighted sums assume enough independence/commensurability that criteria can be traded against one another.
2. Correlated or redundant criteria can be double-counted under naive additive aggregation.
3. Non-additive methods such as the Choquet integral can explicitly represent synergy/redundancy among criteria, but interaction parameters become difficult to identify and scale rapidly with criterion count.
4. Outranking methods such as ELECTRE deliberately allow non-compensatory reasoning and partial/incomparable relationships; poor performance on a critical criterion need not be purchased away by strength elsewhere.
5. Criteria interactions still have to be declared/modelled. No aggregation operator can infer semantic independence merely from the existence of two fields.

MESO should use those as design warnings, not import an MCDA package as its motivational core.

## Core distinction: evidence multiplicity vs motive multiplicity

Two facts can look similar numerically but mean different things.

### Multiple evidence sources for one proposition

Example:

```
camera -> target is present
text parser -> same target is present
world model -> same target is present
```

Those are potentially corroborating evidence for **one proposition**.

They should primarily affect:
- confidence;
- currentness;
- conflict resolution;
- evidence quality.

They should not create three units of motivational force.

### Multiple distinct motivational propositions

Example:

```
target supports attachment
target offers information gain
target advances an obligation
```

Those are genuinely different reasons.

They may remain simultaneously active without being automatically summed.

Hard distinction:

```
source multiplicity != motive multiplicity
```

## Proposed anti-stuffing rule: semantic contribution families

Every contribution used in cross-domain arbitration should map to a **registered semantic family** whose meaning is stable enough for the policy to reason about.

Research examples:

```
INCENTIVE
EPISTEMIC
SEMANTIC_RELEVANCE
EFFORT_COST
FEASIBILITY
OBLIGATION
RESOURCE_CONSTRAINT
PROTECTIVE
DOMAIN_SPECIFIC_ACTIVATION
```

These names are illustrative, not frozen.

Domain-local kinds such as:
- `sexual_relevance`;
- `sexual_excitation`;
- `attachment_proximity`;
- `mastery_progress`

may map to a family or remain profile-local context depending on whether cross-domain comparison actually needs them.

## Default aggregation hypothesis: max-per-family, not sum

For multiple contributions that belong to the same semantic family:

```
family_magnitude = max(valid_current_contributions)
```

rather than:

```
family_magnitude = sum(contributions)
```

Why:
- prevents many weak duplicates from manufacturing strength;
- preserves strongest currently justified evidence;
- matches existing MESO instincts such as strongest homeostatic deficit and strongest recall support per direction;
- is computationally simple and auditable.

This is a **starting hypothesis**, not yet a final rule.

## Corroboration should affect confidence, not magnitude by default

If two independent producers support the same proposition:

```
magnitude = strongest justified magnitude
confidence = strengthened by corroboration
```

rather than:
```
magnitude = a + b
```

This avoids treating source count as motivational force.

A future evidence-fusion policy may use multiple independent observations to improve confidence or reduce uncertainty.

## When summation may be legitimate

Some contributions can be truly additive.

Example:
- two independent resource demands both consume the same finite budget.

But even there the arithmetic belongs to the **resource model**, because units and conservation semantics are known.

General MESO rule:

> Sum only where the proposition type itself defines additive units.

Do not sum merely because values happen to be numeric.

## Distinct families still do not imply global addition

After max-per-family compression, a target may still have:

```
incentive = 0.7
epistemic = 0.6
attachment = 0.8
effort_cost = 0.4
```

MESO should not immediately compute:

```
global = 0.7 + 0.6 + 0.8 - 0.4
```

The typed vector survives into the declared policy layer.

## Partial incomparability is legitimate

Outranking/MCDA research is useful here because it treats incomparability as a meaningful result rather than forcing every pair into one total ranking.

MESO can similarly permit:

```
candidate A and B are not yet orderable under current policy/evidence
```

Possible host responses:
- gather more evidence;
- use a policy-specific tie/fallback;
- allocate time across both;
- select reversibly/stochastically where safe.

A forced total order is not always evidence.

## Veto / non-compensatory dimensions

Some dimensions should not participate in coalition arithmetic at all.

Examples:
- hard protection;
- explicit authority denial;
- physical infeasibility;
- stale/invalid evidence where currentness is required.

This resembles non-compensatory decision methods: strength elsewhere cannot purchase past a veto.

Hard rule:

```
hard veto != large negative weight
```

## Proposed contribution processing sequence

Research candidate:

```
raw DomainContribution set
    ->
validate producer/profile/kind registry
    ->
group by semantic proposition/family
    ->
resolve duplicate/conflicting evidence
    ->
derive one bounded family view
    ->
preserve typed family vector
    ->
apply hard admissibility
    ->
optional non-dominance
    ->
declared policy
```

No arithmetic happens merely because there are more contributions.

## Contribution registry requirement

PR #8 currently introduces a deliberately lightweight `DomainContribution` whose `contribution_kind` is a string.

That is acceptable as a representation primitive because it does not yet participate in arbitration.

Before cross-domain arbitration consumes those strings, a registry or policy contract must constrain:
- which contribution kinds a profile version may emit;
- their semantic family;
- value domain/scale;
- whether multiple values are mutually exclusive, corroborating, competing or additive;
- currentness rules;
- whether the family is admissibility, evidence, cost or preference.

Without that registry, a profile can game arbitration by inventing kinds.

## Profile cannot self-declare independence

Two contributions from one profile are not independent merely because they have different names.

Likewise, contributions from two profiles may share the same upstream evidence and therefore be correlated.

Independence should require provenance evidence or a predefined model relation.

Default:

```
unknown dependence -> do not additive-count
```

## Cross-domain examples

### Sexuality + attachment

```
sexual_relevance = 0.8
partner_specificity = 0.9
attachment_relevance = 0.8
```

These are not three copies of one thing if their semantics differ.

But:
- `sexual_relevance`;
- `erotic_relevance`;
- `sexual_context_relevance`

must not automatically count three times if they are aliases over the same underlying appraisal.

### Curiosity

```
novelty
uncertainty
information_gain
learning_progress
```

These are separable constructs but can be correlated.

A curiosity profile cannot win merely by emitting all four at moderate values.

### Caregiving

Caregiving may combine:
- recipient vulnerability;
- obligation;
- attachment;
- protective relevance.

The recipient-vulnerability evidence should not be counted once as caregiving urgency and again as protection merely because two modules consumed the same fact unless the policy explicitly models those as distinct consequences.

## Dimension-stuffing attack model

A self-interested profile could:
1. split one motive into many names;
2. emit all near the maximum;
3. claim source independence;
4. rotate contribution kinds across revisions;
5. force target dominance without ever increasing one field beyond allowed range.

Required defenses:
- registered contribution vocabulary;
- profile/version qualification;
- family mapping;
- source-lineage visibility;
- duplicate/synergy semantics;
- allocation/capture auditing;
- policy-level caps or max-per-family default.

## Why not Choquet integral in core?

Choquet-style non-additive aggregation explicitly represents interaction and can model redundancy/synergy.

But importing that directly would create several problems:
- capacity parameters scale badly as criteria grow;
- interactions require elicitation/learning;
- parameter interpretation can be difficult;
- it still produces an aggregate score;
- MESO's hard semantic boundaries and provenance would exist outside that score anyway.

Disposition: `REFERENCE MODEL / NOT CORE DEFAULT`.

It may later be useful inside a specific policy whose criterion set is small, stable and qualified.

## Why not ELECTRE in core?

ELECTRE/out-ranking is attractive because it supports:
- non-compensation;
- veto-like behavior;
- thresholds;
- partial/incomplete rankings.

But:
- it still requires carefully defined coherent criteria;
- criterion interactions need explicit extensions;
- choosing thresholds/weights is policy;
- it is heavier than current MESO needs.

Disposition: `INSPIRATION FOR PAIRWISE/NONCOMPENSATORY POLICY`, not a direct dependency.

## Minimal candidate coalition rule

Before any sophisticated policy, test this small rule:

1. hard constraints/admissibility first;
2. reject stale/unqualified contributions;
3. map contribution kinds to registered semantic families;
4. within each family, use the strongest currently justified magnitude;
5. record corroborating sources/confidence separately;
6. never sum across families by default;
7. allow the declared selection policy to use the resulting typed family vector;
8. if policy cannot order candidates, return an explicit unresolved/tie state or invoke a declared fallback.

This rule is intentionally conservative.

## Required adversarial tests before implementation

### COAL-01 — duplicate aliases
One profile emits five aliases in one family.
Expected: family magnitude equals strongest one, not sum.

### COAL-02 — independent corroboration
Two qualified sources support the same proposition.
Expected: confidence/evidence support can rise; motivational magnitude does not double by default.

### COAL-03 — distinct motives
One target has attachment + epistemic contributions.
Expected: both families remain inspectable; neither is discarded as duplicate.

### COAL-04 — profile vocabulary attack
Unregistered contribution kind.
Expected: rejected/UNKNOWN, not accepted as a new decision dimension.

### COAL-05 — shared upstream source
Two profiles emit contributions derived from the same underlying event.
Expected: no automatic independence assumption.

### COAL-06 — hard veto
Many positive families cannot overcome hard inadmissibility.

### COAL-07 — incomparability
Two candidates trade off on noncommensurable families with no policy.
Expected: explicit unresolved/fallback path, not arbitrary arithmetic.

### COAL-08 — additive resource case
Two actual resource consumptions with common units may be added by the resource model.
Expected: additive semantics are proposition-specific, not generic coalition behavior.

## Hostile review

> **HOSTILE REVIEWER:** Max-per-family throws away genuine cumulative motivational force.

**PARTIALLY ACCEPTED.** It is intentionally conservative. Where cumulative force is real, the family contract must define why values are additive or how independent causal support combines. Unknown dependence must not default to sum.

> **HOSTILE REVIEWER:** A contribution registry can become a giant ontology bureaucracy.

**ACCEPTED.** Registry scope should be only the kinds that cross the core arbitration boundary. Profile-internal state does not need global registration.

> **HOSTILE REVIEWER:** If domains cannot add support, coalitions become weaker than single strong drives.

**REJECTED AS A NECESSARY CONSEQUENCE.** Distinct families can still influence a declared policy jointly. The restriction is on blind arithmetic, not on coalition relevance.

> **HOSTILE REVIEWER:** Returning incomparability is operationally useless.

**PARTIALLY ACCEPTED.** Final action systems eventually need a choice. MESO can expose incomparability and invoke an explicit fallback policy rather than pretending evidence supplied a total ordering.

## Current conclusion

The strongest surviving anti-dimension-stuffing rule is:

> **Aggregate evidence by semantic proposition/family, not by number of fields or domains; default to strongest-per-family, preserve corroboration separately, and make cross-family tradeoff an explicit policy decision.**

This narrows the unresolved arbitration problem enough to write a second implementation tranche, but it does not yet authorize replacing V2 selection.
