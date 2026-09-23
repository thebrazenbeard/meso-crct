# Bounded Plasticity Candidate V1

The V2 architecture now includes the first persistent-learning bridge.

Transient salience or pleasure does **not** directly become permanent preference.
Instead, the reference layer can propose a bounded association-strength change
when two conditions hold:

1. there is a non-zero signed prediction-error teaching signal;
2. at least one typed salience channel crosses an explicit policy gate.

The strongest qualifying salience driver gates the proposal. The candidate
delta is bounded by a host-supplied maximum absolute update.

```text
delta
  = prediction_error
  * strongest_qualifying_salience
  * maximum_absolute_delta
```

Every candidate is bound to the deterministic receipt of the verified
transition that produced it.

## Important boundary

The module only **proposes** and previews an association update. It does not own
durable storage and does not silently admit autobiographical memory or permanent
identity/preference claims.

This preserves:

```text
transient pleasure
    !=
automatic permanent preference
```

and

```text
high salience
    !=
learning without a teaching signal
```

The next memory-owner layer can decide how accepted candidates are stored,
reversed, versioned, and tested for negative transfer.
