# Evidence-Driven Learned Association Review V2

Mechanically valid learning can still be wrong, overgeneralized, or brittle.

Review decisions are therefore bound to explicit evidence rather than a freeform
reason string.

## Evidence objects

Each `ReviewEvidence` binds:

- association ID;
- exact memory revision ID;
- evidence kind;
- evidence outcome;
- human-readable evidence reference;
- constructor-gated transition receipt ID;
- distinct event ID.

Evidence kinds:

- `COUNTEREXAMPLE`
- `HOLDOUT`

Outcomes:

- `SUPPORTS`
- `CONTRADICTS`
- `INCONCLUSIVE`

## Deterministic risk classification

```text
contradictory counterexample
    -> CONTRADICTED

contradictory holdout
    -> SUSPECTED_OVERGENERALIZATION

at least two distinct supporting holdout events + no contradictions
    -> CLEAR

anything weaker
    -> INSUFFICIENT
```

Evidence from different learned revisions cannot be collapsed into one
assessment.

## Quarantine rule

Quarantine requires a current-revision assessment classified as either:

- `CONTRADICTED`; or
- `SUSPECTED_OVERGENERALIZATION`.

The review record stores the exact assessment ID and evidence IDs. Learning
history and association strength remain untouched.

## Release rule

Release requires a current-revision `CLEAR` assessment with the policy's
minimum number of **distinct supportive holdout events** and zero contradictory
evidence. The default reference policy requires two distinct holdout events.

Multiple labels/evidence records tied to the same event count as one event, so
duplicating an observation cannot manufacture clearance.

A reason string alone cannot clear an association.

## Currentness

Evidence and review are both revision-specific.

If learning changes the association revision, prior evidence and review no longer
clear the new revision. New evidence must be collected and assessed.

## Canonical decision cycle

Precomputed recall is revalidated against the current learned revision and
current review record before motivational support is applied. Later quarantine,
release, or learning therefore invalidates older precomputed recall snapshots.

## Ceiling

This governance layer makes the evidence basis explicit and auditable. It does
not prove the holdout set is representative, unbiased, adversarially sufficient,
or scientifically correct.
