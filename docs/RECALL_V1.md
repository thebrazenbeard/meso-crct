# Guarded Association Recall V1

Persistent association strength is not self-activating.

The reference recall path requires both:

1. a current stored association revision;
2. a current constructor-gated transition receipt plus an explicit cue-match
   strength.

```text
stored association
    + current cue evidence
    -> bounded recall influence
    -> current motivational support
```

A stored association with `cue_match = 0` contributes no current motivation.

## Direction stays separate

Association strength is signed.

Positive strength produces approach support. Negative strength produces learned
avoidance support. Both can make a cue motivationally salient, but learned
negative direction does **not** silently write the system's hazard or protective
avoidance channels.

Likewise recall does not rewrite pleasure.

```text
learned association
    !=
current pleasure
    !=
current hazard
```

## Lineage

Each recall influence binds:

- the exact current association revision ID;
- the exact current cue transition receipt ID.

`RecallInfluence` is constructor-gated and is produced through
`recall_association()`.

## Current integration

`apply_recall_motivation()` can raise current motivational salience to the
recall support magnitude. It never lowers stronger current motivation and does
not alter reward/protection state.

This closes the first full reference loop:

```text
experience
  -> salience + prediction error
  -> bounded plasticity
  -> versioned association memory
  -> later cue
  -> guarded recall
  -> current motivational salience
```
