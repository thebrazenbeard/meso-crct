# MESO-CRCT Appraisal Producer and Currentness Contract Research V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / TRUST-BOUNDARY SPECIFICATION / NO IMPLEMENTATION`

## Purpose

Current MESO source contains strong provenance machinery for whole transitions but several appraisal inputs are still caller-authored numeric values.

As MESO expands, typed state alone is insufficient.

A field can be semantically well named and still be false, stale, mis-scoped, or self-serving.

This document defines the research requirements for trusted appraisal producers.

## 1. Current strength

Existing MESO provenance binds:

```
source_kind
source_id
source_revision
verifier_id
event identity
before/after state fingerprints
```

and prevents direct construction of verified provenance/transition receipts.

This is a strong base.

## 2. Current gap

`TargetAppraisalInput` directly accepts values such as:
- perceptual salience;
- base motivational salience;
- base incentive salience;
- novelty;
- learning progress;
- prediction error;
- satiation;
- reward/protection state;
- recruitment;
- homeostasis.

Those values receive type/range checks.

Range checking proves:
```
0 <= value <= 1
```

It does not prove:
- who measured it;
- what proposition it represents;
- which target/actor it applies to;
- whether it is current;
- how uncertain it is;
- whether the producer is qualified to assert it.

## 3. Producer contract principle

Each consequential appraisal fact should bind:

```
PROPOSITION
+ SUBJECT/REFERENT
+ PRODUCER
+ EVIDENCE
+ OBSERVATION TIME / CURRENTNESS
+ VERSION
+ UNCERTAINTY
+ SCOPE
```

before it becomes trusted state.

Not every low-risk local reference test needs full runtime machinery.
The live architecture should have a place for these semantics.

## 4. Proposition type matters

Different producers may be authoritative for different claims.

Examples:

### Resource provider
Can establish:
- available memory;
- battery;
- rate quota;
- current thermal state.

Cannot establish:
- desire;
- importance;
- consent.

### Planner
Can establish:
- plan exists;
- remaining steps;
- estimated duration;
- blockers.

Cannot establish:
- target is valuable;
- relationship status.

### Sexuality profile
Can propose:
- sexual relevance;
- excitation/inhibition under its model.

Cannot establish:
- consent;
- partner identity;
- relationship truth.

### Semantic producer
Can propose:
- meaning/relevance relation.

Cannot establish:
- authorization.

### Operator
Can establish some:
- assignments;
- preferences;
- explicit authority;

but an operator statement about physical state may still require provider readback where effects matter.

## 5. Proposed research fields

A future verified appraisal datum may need:

```
datum_id
proposition_type
subject_ref
referent_ref
value
unit_or_scale
producer_id
producer_version
source_evidence_ref
observed_at
valid_from
expires_at_or_condition
confidence_or_uncertainty
scope
supersedes
verifier_id
```

This is intentionally overcomplete research vocabulary.

The implementation should minimize it.

## 6. Currentness is proposition-specific

Some facts decay quickly:
- free RAM;
- connection status;
- sexual/affective activation;
- immediate threat.

Some are more durable:
- repository source version;
- long-term learned association;
- authored identity until changed.

Therefore there should not be one universal TTL.

Currentness policy belongs to proposition/producer contract.

## 7. Stale should not mean false

If telemetry expires:

```
CURRENT = UNKNOWN
```

not:
```
value = 0
```

Examples:
- stale hazard signal does not prove safety;
- stale attraction signal does not prove no attraction;
- stale resource reading does not prove no resource;
- stale authorization ALLOW does not remain ALLOW.

## 8. Supersession beats timestamp recency alone

A later timestamp is not automatically more authoritative.

Currentness can depend on:
- exact source lineage;
- explicit revocation;
- supersession relation;
- provider identity;
- proposition scope.

This mirrors Vera Mono epistemic discipline.

## 9. Confidence and uncertainty are not relevance

A producer can be:
- highly confident the event is only weakly relevant;
- uncertain the event is highly relevant.

Do not multiply confidence into the semantic variable silently.

Preserve both.

## 10. Profile-local calibration

If a learned profile emits a score:
- calibration is profile-local;
- model/version must be known;
- holdout qualification should be version-bound;
- distribution shift can stale qualification.

A sexuality 0.8 and curiosity 0.8 are not cross-domain comparable just because both models are calibrated internally.

## 11. Producer self-interest / incentive attack

A domain profile could increase its own selection rate by exaggerating:
- relevance;
- urgency;
- expected reward;
- effort efficiency.

This is a direct anti-wireheading concern.

Required defense research:
- no profile emits final priority;
- common core derives shared dimensions where possible;
- qualification includes adversarial inflation tests;
- long-horizon allocation monitors producer/domain capture;
- policy can quarantine producer revisions.

## 12. Derived values need lineage

If MESO derives:
```
effort_cost
```
from:
- resource state A;
- task estimate B;
- policy C;

the result should be traceable to A+B+C.

Otherwise explanation and stale-input detection fail.

## 13. Multi-source facts

Some propositions may combine independent evidence.

Example:
- feasibility from planner + capability provider + resource telemetry.

Do not blindly average.

Research options:
- conjunction requirements;
- strongest-confidence source;
- typed evidence set;
- dedicated fusion policy.

Fusion policy must be explicit and proposition-specific.

## 14. Conflicting producers

Two trusted sources may disagree.

Required state:
```
CONFLICT
```
or unresolved evidence set, not silent last-write-wins.

Examples:
- planner says feasible;
- capability provider says missing required tool.

The downstream policy may choose conservative handling.

## 15. Exact event binding

Transient appraisals should bind to the event/input that produced them where relevant.

This prevents:
- reusing one cue event repeatedly;
- attaching yesterday's appraisal to today's target;
- actor-swap laundering.

Current MESO event identity/replay design is a strong precedent.

## 16. Producer registry

A future host might register:

```
producer_id
version
proposition_types
verification method
currentness policy
qualification state
claim ceiling
```

This should not become a plugin bureaucracy unless live integrations require it.

## 17. Trust tiers may be proposition-specific

A deterministic local sensor and a learned classifier may both emit a field but with different evidence ceilings.

Potential statuses:
- MEASURED;
- DERIVED;
- INFERRED;
- SELF_REPORTED;
- PREDICTED;
- TEST_STIMULATION.

Do not order these universally.
They describe proposition/evidence type.

## 18. External authority requires exact binding

For consent/protected effects, ordinary appraisal confidence is insufficient.

Authority should continue to use its own strict external contract.

No producer can say:
```
consent_probability = 0.99
```
and convert that into ALLOW.

## 19. Research examples

### Example A — resource

```
producer = workstation telemetry
proposition = available_vram
value = 14.2 GB
observed_at = T
expiry = short
```

Task estimator:
```
required_peak_vram = 16 GB ± 1
```

Derived feasibility:
```
INFEASIBLE or CONDITIONAL
```

with lineage.

### Example B — sexual relevance

Sexuality profile:
```
proposition = sexual_relevance
target = current interaction
value = 0.7
model/profile version = X
evidence = current text + relationship-context refs
```

Authorization remains separately:
```
UNKNOWN
```

### Example C — semantic relevance

Current `SemanticEvidence` already points in this direction by distinguishing grounded context/goal/memory/unresolved relevance from a source merely asserting importance.

Future producer contracts can generalize that principle.

## 20. Required adversarial cases

### PC-01 — stale resource telemetry
Cannot support current feasibility after expiry.

### PC-02 — domain inflation
Profile raises local score to force selection; no final priority authority.

### PC-03 — actor swap
Evidence for actor A cannot become actor B state.

### PC-04 — revision drift
Qualified profile revision changes; prior qualification becomes stale.

### PC-05 — conflicting providers
Do not last-write-wins silently.

### PC-06 — derived lineage
Effort cost can be traced to resource + estimate + policy inputs.

### PC-07 — stale ALLOW
Authorization expiry produces UNKNOWN/DECLINE per authority contract, never inferred continuation.

### PC-08 — same event replay
Transient appraisal cannot repeatedly train durable memory beyond replay policy.

### PC-09 — source claims importance
Self-assertion alone still cannot create semantic relevance.

### PC-10 — UNKNOWN
Missing evidence stays UNKNOWN, not neutral zero.

## Hostile review

> **HOSTILE REVIEWER:** This is reinventing a provenance database for every float.

**ACCEPTED AS AN IMPLEMENTATION RISK.** The research contract is intentionally richer than the likely runtime representation. High-impact/stateful inputs need stronger provenance; trivial deterministic local calculations may inherit lineage from their parent receipt.

> **HOSTILE REVIEWER:** Currentness semantics belong to each provider, so MESO should not care.

**REJECTED.** MESO does not need to own refresh logic, but it must know whether an input is currently admissible. Otherwise stale state silently drives motivation.

> **HOSTILE REVIEWER:** Learned scores cannot be fully explainable anyway.

**ACCEPTED.** Explainability of internal model computation is not required. What is required is model identity, evidence subject, calibration/qualification scope, currentness, and an honest claim ceiling.

## Current conclusion

The next MESO architecture should not merely add more typed floats.

It needs a minimal **verified appraisal datum / producer contract** so consequential domain and common appraisal inputs remain:
- scoped;
- source-bound;
- current;
- uncertainty-aware;
- non-authoritative outside their proposition.

Existing MESO provenance/event machinery is a strong base, but the exact minimal interface remains to be designed.
