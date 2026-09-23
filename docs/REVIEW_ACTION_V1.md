# Review Action Proposal V1

Evidence classification and review mutation are separate steps.

```text
evidence
  -> exact-revision assessment
  -> non-mutating review proposal
  -> separately governed memory mutation
```

`propose_review_action()` emits one of:

- `QUARANTINE`
- `RELEASE`
- `HOLD`

Reference mapping:

- `CONTRADICTED` or `SUSPECTED_OVERGENERALIZATION` -> propose quarantine unless already quarantined;
- `CLEAR` -> propose release only when currently quarantined;
- `INSUFFICIENT` -> hold.

A proposal never changes `AssociationMemory`.

Every `ReviewActionProposal` has:

```text
mutation_authorized = false
can_mutate = false
```

The actual mutation still requires `quarantine_association()` or
`release_association()` with the exact evidence assessment.

This mirrors the larger MESO-CRCT authority boundary:

```text
evidence conclusion != permission != effect
```
