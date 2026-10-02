# MESO Goal-Relation Admission Receipt Boundary V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / PROVENANCE BOUNDARY / NO IMPLEMENTATION`

## Problem

Current goal-target allocation code validates each `GoalRelation` against:
- CURRENT evidence;
- matching selected target;
- a `GoalRelationAdmissionPolicy`.

It then stores only the raw `GoalRelation` in `AllocationSample`.

Therefore later allocation audits can observe:

```
target X counted toward goal G
```

but cannot prove:
- which admission policy allowed that mapping;
- which policy revision was used;
- that the stored relation actually passed the admission gate rather than being manually constructed into a sample.

This is the same provenance-loss pattern already corrected for admitted goal obligations.

## Required distinction

```
raw goal relation
!= admitted goal relation
!= allocation sample containing a relation
```

The relation states a proposition.

The admission receipt states that a particular host-supplied policy accepted that proposition for allocation accounting.

Neither implies:
- desire;
- consent;
- external action authority.

## Compatibility constraint

Existing callers and tests already use `GoalRelation` directly.

Do not replace the stored relation with a subclass if that needlessly breaks equality/serialization expectations.

Prefer:

```
AllocationSample:
    goal_relations
    goal_relation_receipts
```

with one receipt per strongly admitted relation.

Legacy/directly constructed samples may have relations without receipts; that state must be identifiable as weaker provenance.

## Candidate receipt

```
GoalRelationAdmissionReceipt:
    relation_digest
    goal_id
    target_id
    source/evidence digest
    admission_policy_id
    admission_policy_revision
    receipt_digest
```

The constructor should be gated so callers cannot hand-author a qualified receipt.

## Policy identity

`GoalRelationAdmissionPolicy` currently binds producers but lacks its own identity/revision.

Add:
- `policy_id`;
- `policy_revision`.

For compatibility, legacy/default identity may be provided when callers omit them.

New provenance-sensitive callers should provide explicit host policy identity.

## Receipt binding

The receipt digest should bind:
- goal ID;
- target ID;
- evidence producer ID/revision;
- evidence subject;
- evidence source ID;
- evidence currentness;
- admission policy ID/revision;
- admitted producer set.

Changing any of those changes the receipt digest.

## AllocationSample invariant

For samples created through `from_selection()` with goal relations:

1. admission policy is required;
2. each relation must match the selected target;
3. evidence must be CURRENT;
4. policy must admit the producer/revision;
5. a receipt is issued for each admitted relation;
6. stored raw relation and receipt remain one-to-one and digest-bound.

## Legacy samples

Directly constructed `AllocationSample` objects with goal relations but no receipts may remain supported as:

```
LEGACY / UNATTESTED RELATION ACCOUNTING
```

A future strict audit mode may reject them, but this tranche should not silently break V2 compatibility.

## Downstream obligation-pressure implication

Do not derive local obligation pressure from a raw goal relation alone.

A strong derivation should require:
- admitted goal obligation;
- allocation state;
- current goal relation;
- goal-relation admission receipt.

Otherwise a caller could manufacture a target→goal mapping and thereby manufacture obligation pressure.

## Hostile review

> **HOSTILE REVIEWER:** The relation evidence already contains producer identity; a second receipt is redundant.

**REJECTED.** Producer identity proves who asserted the relation, not that the host admitted that producer/revision for allocation accounting under a particular policy.

> **HOSTILE REVIEWER:** Storing both relation and receipt duplicates state.

**ACCEPTED AS A SMALL COST.** It preserves compatibility while keeping admission provenance explicit. Replacing the relation object would create a broader migration for little gain.

> **HOSTILE REVIEWER:** A receipt can still be forged if it is just another dataclass.

**ACCEPTED.** Qualified receipt construction must be module-gated, consistent with other trusted MESO receipts.

## Current conclusion

The smallest defensible repair is:

```
raw GoalRelation
+ CURRENT evidence
+ host admission policy
-> constructor-gated GoalRelationAdmissionReceipt
-> AllocationSample stores relation + receipt
```

with legacy relation-only samples remaining visibly weaker rather than silently upgraded.
