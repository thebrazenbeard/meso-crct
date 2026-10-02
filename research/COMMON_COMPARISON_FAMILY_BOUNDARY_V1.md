# MESO Common Comparison-Family Boundary V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / TYPE-BOUNDARY REFINEMENT / NO IMPLEMENTATION`

## Problem

Draft PR #13 introduces partial-order comparison over `ContributionFamilyView`.

That type currently means:

> a normalized family view produced from one or more registered **domain-profile contributions**.

But MESO also needs to compare common appraisals such as:
- effort cost;
- required effort;
- admitted obligation pressure;
- resource cost;
- possibly other shared decision dimensions.

Those are not domain contributions.

Forcing them through `DomainContribution` would break the architecture boundary established in `DOMAIN_PROFILE_INTERFACE_V1.md`.

## Required distinction

```
DOMAIN CONTRIBUTION
!=
COMMON APPRAISAL
!=
COMPARISON FAMILY VIEW
```

A domain profile owns domain-specific meaning.

A common appraisal producer owns shared constructs such as effort or feasibility.

A comparison-family view is a normalized **decision-facing projection** from either source type.

## Why the current name is too narrow

Current:

```
DomainContribution
    ->
ContributionFamilyView
    ->
PartialOrderPolicy
```

This is correct for domain evidence.

It is not correct for:

```
EffortAssessment
    -> ?
    -> PartialOrderPolicy
```

The missing abstraction is generic and source-aware.

## Candidate generic type

Research sketch:

```
ComparisonFamilyView:
    target_id
    family_id
    magnitude
    source_kind
    source_digest
```

Possible `source_kind` values:

```
DOMAIN_AGGREGATE
COMMON_APPRAISAL
POLICY_DERIVED
```

Do not freeze these yet.

The key property is that the comparison layer receives:
- one bounded magnitude for one semantic family;
- a target binding;
- a traceable source lineage.

## Domain adapter

Existing domain aggregation remains valuable:

```
DomainContribution[]
    ->
registered semantic-family normalization
    ->
ContributionFamilyView
```

A thin adapter can then create a generic comparison view while preserving:
- contribution family;
- strongest magnitude;
- contributing kinds;
- source IDs;
- registry/provenance digest.

Do not delete the domain-specific view merely to make the generic interface prettier.

## Common appraisal adapter

Example effort path:

```
EffortAssessment
    ->
validated CURRENT admitted producer
    ->
ComparisonFamilyView(
    family_id = "effort_cost",
    magnitude = assessment.effort_cost,
    source_kind = COMMON_APPRAISAL,
    source_digest = ...
)
```

Important:
- `required_effort` and `willingness_to_exert` are distinct possible families;
- `vigor_proposal` is post-selection and should not automatically enter target comparison;
- the adapter must not emit every effort field merely because it exists.

## No generic field-count voting

The common family boundary does not change the anti-dimension-stuffing rule.

Each source adapter must register:
- which family it may emit;
- producer identity/revision;
- currentness;
- magnitude semantics.

Multiple source kinds mapping to the same family require an explicit fusion policy.

## Source lineage

A generic comparison view should not erase provenance.

At minimum the view must be digest-bound to the evidence used to derive it.

A downstream selection result should therefore be able to prove:
- which family magnitude it compared;
- which exact source cut produced that magnitude;
- which policy interpreted the family direction.

## Why not put EvidenceRef directly on ComparisonFamilyView?

Sometimes a family value is derived from several source records, such as a domain aggregate.

One `EvidenceRef` cannot faithfully represent many-to-one derivation.

A deterministic source digest plus source-kind identity may be more appropriate, with the producer/receipt retaining the expanded lineage.

The exact mechanism remains open.

## Required invariants

```
comparison family != source ontology
family magnitude != global priority
domain profile != common-appraisal producer
common appraisal != domain motive
source multiplicity != motivational force
```

## Migration strategy

Do not rewrite PR #9 or #13 immediately.

Possible bounded migration:

1. introduce `ComparisonFamilyView`;
2. add deterministic adapter from `ContributionFamilyView`;
3. allow partial-order selector to consume generic views;
4. retain legacy domain-view input temporarily through an adapter;
5. add effort adapter only after effort producer/currentness admission is qualified.

This keeps the migration reversible.

## Effort-specific blocker discovered

Current `EffortAssessment` validates numeric ranges but does not yet require:

```
assessment.target_id == assessment.evidence.subject_id
```

and has no producer admission policy.

Therefore effort must not enter the comparison layer yet.

Required preconditions:
- subject binding;
- CURRENT evidence;
- externally supplied producer/revision admission;
- deterministic appraisal digest.

## Admitted obligation pressure

A `GoalObligation` should not automatically become a comparison-family magnitude.

The existing minimum-share constraint is long-horizon control state.

If a local "obligation pressure" family is later introduced, it must be explicitly derived from:
- admitted obligation;
- current allocation window;
- remaining horizon;
- current goal relation.

Do not equate `minimum_nonprotective_share` with local motivational magnitude.

## Hostile review

> **HOSTILE REVIEWER:** A generic comparison-family type is just another abstraction layer around a float.

**PARTIALLY ACCEPTED.** It is justified only if it preserves source lineage and prevents common appraisals from masquerading as domain contributions. If it becomes a naked `family_id + float`, reject it.

> **HOSTILE REVIEWER:** The partial-order selector could simply accept several input types and avoid a new type.

**PARTIALLY ACCEPTED.** Structural polymorphism is mechanically possible. A generic type is preferable only if it gives one auditable provenance contract across source kinds.

> **HOSTILE REVIEWER:** Mapping effort cost into a normalized 0..1 family already hides important units.

**ACCEPTED.** The adapter must be downstream of the effort/resource model that defines the normalization. Raw resource units should not be normalized inside the selector.

## Current conclusion

The next architecture should not force common decision appraisals through `DomainContribution`.

The clean direction is:

```
domain-specific evidence -> domain normalization --\
                                                -> ComparisonFamilyView -> partial order
common appraisal evidence -> common adapter ----/
```

with source lineage preserved and no automatic cross-source fusion.
