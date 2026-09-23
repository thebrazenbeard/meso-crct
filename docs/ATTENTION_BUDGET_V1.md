# Attention Budget Audit V1

A system can fail over time even when every individual salience decision looks
reasonable.

Example:

```text
target A wins arbitration
target A wins arbitration
target A wins arbitration
...
goal B never receives processing
```

The reference attention-budget audit therefore evaluates allocation over a
window.

## Goal obligations

The architecture does not assume every goal deserves equal time.

Instead, a host supplies explicit `GoalObligation` values describing the
minimum non-protective processing share a goal should receive.

This makes the policy visible and testable instead of hiding a fairness rule in
the salience circuit.

## Protective exemption

Protective episodes are counted separately and excluded from ordinary crowd-out
math.

A sustained emergency is allowed to dominate attention without being mislabeled
as pathological incentive capture.

## Flags

The current audit can report:

- `goal_neglect`;
- `target_crowd_out`;
- `incentive_capture`.

The final flag is narrower: crowd-out is being driven primarily by motivational
or incentive salience.

## Ceiling

This layer detects allocation pathology. It does not yet alter runtime priority
or decide which neglected goal should preempt the dominant target.
