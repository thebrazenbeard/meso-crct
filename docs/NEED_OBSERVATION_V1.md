# Caller-admitted need observation V1

This is a minimal **in-memory**, immutable update boundary for externally
observed levels on existing MESO-CRCT `NeedAxis` records. It closes one part of
the control-loop gap; it does **not** create an endogenous drive, install a
sensor, persist to disk, or connect to Volition/Pre-Active.

## Admission sequence

1. A caller obtains an external measurement independently of MESO's own
   salience, pleasure, or intent output.
2. `NeedObservation` captures an event ID, need ID, finite measured level in
   `[0,1]`, aware UTC timestamp, typed external-source provenance, and a
   non-empty evidence reference. Internal-state, memory, replay, and direct
   register-write source kinds are rejected.
3. A separately accountable caller constructs `NeedObservationVerifier` with
   the **exact complete observations** it agrees to admit. An arbitrary raw
   `NeedObservation` cannot update a ledger.
4. The caller also supplies a typed `AdmissionClock(trusted_as_of=...)`
   established **independently** of any model output. Admission fails closed
   without it. The default future allowance is zero; a caller may explicitly
   permit up to 300 seconds with `maximum_future_skew_seconds`. UTC-only,
   finite numeric bounds reject malformed clocks. Any observation beyond
   `trusted_as_of + allowed_skew` is rejected **before ledger mutation**,
   including claimed readings dated in year 9999. Optionally, callers can set
   `maximum_observation_age_seconds` to a finite, nonnegative duration no
   greater than 366 days (31,622,400 seconds). The default `None` preserves
   historical admission behavior. With this policy enabled, a distinct
   observation older than the caller-supplied UTC time by more than the chosen
   age is rejected as `NeedObservationExpired`; the age boundary itself is
   accepted. This does **not** authenticate the clock or physical reading.
5. `admit_need_observation(ledger, admitted, clock=clock)` updates only that existing `NeedAxis.current_level`
   in a new `HomeostaticState` and appends a typed record with the caller's
   verifier label. Other need axes, their setpoints/sensitivities, and reward
   state remain unchanged.
6. Reuse of an identical event and verifier is an idempotent no-op. A reused
   event ID with different evidence/verifier is an error; another event with a
   non-increasing timestamp for the same need is stale. Different needs have
   independent clocks. Reconstructed ledger snapshots validate this ordering
   and agreement between the latest admitted measurement and current level.
   Admission checks future skew first, then existing-event replay/conflict,
   then optional age expiry, then the bounded history capacity (256 records)
   and per-need ordering. Consequently exact previously admitted events remain
   replay-idempotent after their age window, but novel expired events cannot
   consume history capacity or modify need state.

For instance, if `NeedAxis('rest', setpoint=0.9, current_level=0.1)` receives an
admitted measured level of `0.5`, deficit changes from `0.8` to `0.4` at the
next appraisal. The module does not infer that a goal was completed, that the
reading is authentic, or that a protected action is permitted.

## Unverified boundaries

- The caller-selected exact-value allowlist is **not independent evidence
  custody**, an identity check, a sensor signature, or a permission grant. A
  malicious caller controlling the verifier can select a false reading; the
  reference code cannot prove otherwise. Public Python constructors and
  module-private tokens are not cryptographic access controls.
- The API checks `observed_at` against an **explicit caller-supplied UTC time
  ceiling** with at most five minutes of stated skew and optional maximum age.
  It never invents a clock from its own model/system state. It cannot verify that the caller's clock is
  honestly measured or independently administered. If the caller fabricates an
  advanced `trusted_as_of`, future-date poisoning remains possible, so real
  deployments require authenticated custody and trusted clock-source policy.
- `NeedObservationLedger` is in-memory immutable state, not a durable storage
  transaction; restart persistence, cross-process concurrency, locking, and
  snapshot authenticity are unimplemented.
- `effect_authorized` remains `False`. No direct `record_satisfaction`, goal
  completion, Pre-Active queue, external I/O, consent, truth, identity, or
  subjective welfare effect is inferred from a need-level change. A later
  separately verified **goal-linked outcome** would be required for Volition
  satisfaction; this module deliberately does not implement it.
- History exported by `conations`, `sexuality`, or `orgasm` is not a live need
  observation merely because it has a dated status, digest, or emotive label.

The intended eventual integration cycle is an *externally observed need* →
MESO target appraisal → protected non-executable intent proposal → separately
authorized task/effect boundary → independently observed outcome → new admitted
need update. Without an admitted outcome, the unmet need remains unchanged.

## Testing

`tests/test_need_observation.py` covers exact-value admission, nonfinite and
  untyped source rejection, independent need clocks, stale/conflicting replay,
  future-date poisoning, strict time ceiling, bounded skew, optional expired
  first-sample rejection with replay preservation, immutable updates, and
  reconstructed-state consistency. No real-world clock custody, sensor, or
  external effect is exercised.
