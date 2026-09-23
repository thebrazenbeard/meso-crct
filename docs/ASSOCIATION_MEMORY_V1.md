# Versioned Association Memory V1

This layer is the first durable owner for MESO-CRCT learning output.

It owns only bounded numeric **association strengths**. It does not accept free
text, autobiographical episodes, identity claims, relationship state, consent,
or other semantic authority.

## Admission path

```text
verified transition
  -> bounded plasticity candidate
  -> association-memory version check
  -> append-only revision
```

A plasticity candidate is therefore not durable merely because it exists.

## Optimistic versioning

Every association has a monotonically increasing version.

An update must name the current expected version. Stale writers fail instead of
silently overwriting newer learning.

## Replay protection

A verified transition receipt may contribute at most one applied persistent
update in a memory snapshot.

This prevents the same event from being replayed repeatedly to manufacture
learning strength.

## Reversal

`revert_last()` appends a new revision returning the association to its prior
strength. It does not delete history.

That makes negative-transfer repair auditable:

```text
bad learned update
  -> review
  -> explicit reversal revision
  -> history preserved
```

## Bounds

Association strengths remain in `[-1, 1]` even under repeated updates.

## Claim ceiling

This module implements versioned learned associations.

It does not establish:
- autobiographical memory;
- permanent personal preference;
- identity;
- belief truth;
- phenomenology.

Those remain distinct admission problems.
