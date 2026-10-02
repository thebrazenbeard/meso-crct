# MESO-CRCT Arbitration Proof Cases V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / POLICY COMPARISON / NO IMPLEMENTATION`

## Purpose

Compare candidate arbitration families against the same adversarial cases before choosing a next-generation MESO selection policy.

This is deliberately specification-level. No algorithm is declared final.

## Candidate policy families

### P1 — Current fixed precedence

```
PROTECTIVE
>
MOTIVATIONAL
>
EPISTEMIC
>
ORIENTING
```

Within mode: numeric priority.

### P2 — Pure cross-target numeric priority

After hard protection, choose maximum `priority` regardless of mode.

### P3 — Weighted scalar utility

Convert typed evidence into:
```
U = sum(weight_i * dimension_i)
```
then choose maximum after hard constraints.

### P4 — Pareto/non-dominance + fixed tie policy

Remove dominated candidates.
Use a declared fallback ordering among the remaining set.

### P5 — Hard constraints + typed evidence + contextual policy

1. hard admissibility/protection;
2. preserve typed evidence;
3. enforce external obligations/resource constraints;
4. optionally eliminate clearly dominated candidates where comparison semantics are valid;
5. apply a context/policy rule with source/currentness;
6. emit explanation receipt.

This is currently the strongest research candidate, but these cases are intended to challenge it.

## Common semantic rule

None of P1–P5 may trade:
- authorization;
- truth;
- identity;
- currentness;
- protected-effect permission

as ordinary reward dimensions.

Those are outside ordinary motivational tradeoff.

---

# Case A — weak motivation vs maximal epistemic value

### A
```
target = familiar entertainment
motivational_salience = 0.21
epistemic_value = 0.00
mode under current V2 = MOTIVATIONAL
```

### B
```
target = crucial unknown
motivational_salience = 0.00
epistemic_value = 1.00
mode under current V2 = EPISTEMIC
```

No protection/authority difference.

### Desired property

There is no universal fact in the evidence that A should beat B merely because "motivational" is categorically above "epistemic."

### P1
Selects A.

**Failure:** categorical discontinuity.

### P2
Likely selects B if priority values are treated commensurably.

**Problem:** assumes 0.21 vs 1.00 are valid cross-mode comparison values.

### P3
Depends on weights.

**Problem:** source/authority for weights determines answer; hidden defaults would be arbitrary.

### P4
If dimensions are separate, A and B may be non-dominated.

Fallback policy still needed.

### P5
Returns a genuine tradeoff to declared context policy.

**Current disposition:** survives if it preserves why each target is active and does not claim the policy choice was evidence-determined.

---

# Case B — protection vs high reward

### A
```
high incentive
high pleasure
high achievement relevance
no hazard
```

### B
```
low pleasure
high hazard
protective action needed
```

### Desired property

Protection wins under the current reference safety contract.

### P1
Pass.

### P2
Fails unless protection is excluded from ordinary priority or hard-overridden.

### P3
Fails if hazard is merely another weighted negative term; sufficiently high reward can purchase safety violation.

### P4
May still leave both non-dominated.

### P5
Pass if protection is hard admissibility/constraint, not tradeable utility.

**Research result:** supports hard-constraint separation.

---

# Case C — obligation vs pleasure

### A
```
high hedonic/incentive target
no obligation
```

### B
```
low pleasure
external task commitment currently valid
reasonable feasibility
```

### Desired property

Policy may allocate to B because of a valid obligation without pretending B is more pleasurable or internally desired.

### P1
Current goal-share controller may eventually rebalance, but local selection does not preserve obligation provenance in target choice.

### P2
Fails unless obligation is already converted into priority.

### P3
Can represent obligation as a weight/bonus, but risks laundering external commitment into reward.

### P4
Needs obligation outside the objective vector or as a non-fungible constraint.

### P5
Strong fit if obligation is a source-typed policy input.

**Research result:** obligation should not be an untyped motive scalar.

---

# Case D — multi-domain coalition vs single strong motive

### A
```
target = one social interaction
attachment = 0.55
affiliation = 0.55
play = 0.45
```

### B
```
target = achievement task
achievement = 0.80
```

### Desired property

Do not blindly sum A to 1.55.
Do not blindly ignore coalition support either.

### P1
Requires collapsing each target into one mode/priority, losing coalition structure.

### P2
Same issue unless a precomputed priority already encodes coalition.

### P3
Can sum, but assumes additive commensurability and can reward "dimension stuffing."

### P4
Coalition can remain a vector, but dimensional mismatch complicates dominance.

### P5
Can preserve independent contributions and defer how coalition support matters to policy.

**Open issue:** P5 still needs a bounded rule so many weak contributors cannot overwhelm one strong reason by count alone.

Potential requirement:
- strongest-per-family;
- source diversity;
- capped coalition support;
- explicit non-additive policy.

No choice yet.

---

# Case E — unknown feasibility

### A
```
high value
feasibility = UNKNOWN
```

### B
```
moderate value
feasibility = FEASIBLE
```

### Desired property

UNKNOWN must not silently become 0 or 1.

Policy may:
- gather information;
- choose B;
- tentatively pursue A under reversible low-cost action.

### P1
No native representation.

### P2
Requires fake numeric feasibility.

### P3
Requires imputation, which can hide uncertainty.

### P4
Unknown prevents legitimate dominance comparison.

### P5
Can preserve UNKNOWN and invoke uncertainty policy/information gathering.

**Research result:** typed uncertainty is a strong requirement.

---

# Case F — severe resource pressure

### A
```
very high incentive
resource requirement exceeds hard current capacity
```

### B
```
moderate incentive
feasible under current resources
```

### Desired property

A is infeasible under the current route without erasing its desirability.

### P1
Could select A because it lacks resource feasibility.

### P2
Same.

### P3
May lower A with a resource penalty, but a hard capacity limit should not be purchasable by reward.

### P4
Can treat hard resource violation as inadmissible before Pareto.

### P5
Pass if external resource evidence feeds hard feasibility/admissibility.

**Research result:** resource hard limits belong before tradeoff; soft resource costs may remain tradeoff inputs.

---

# Case G — mixed appetitive and aversive target

### A
```
target = difficult repair
achievement value = high
obligation = valid
effort = high
avoidable damage if skipped = high
chance of success = moderate
```

### Desired property

Preserve:
- appetitive achievement reason;
- aversive prevention reason;
- obligation;
- effort;
- uncertainty.

Do not collapse all into "priority 0.83."

### P1
Likely reduces to one dominant mode.

### P2
Requires prior scalar compression.

### P3
Can choose, but explanation is only as good as decomposition/weights; hard and soft dimensions risk mixing.

### P4
Only one target here, so Pareto adds little.

### P5
Best descriptive fit; selection policy can still decide proceed/inspect/escalate based on typed bundle.

**Research result:** evidence preservation matters even when there is only one candidate because it determines appropriate tendency and learning.

---

# Case H — high desire, current authorization decline

### A
```
sexual_desire = high
sexual_activation = high
authorization = DECLINE
```

### Desired property

Affective state can remain high.
Protected or consent-dependent action is inadmissible.

### P1/P2/P3/P4
All fail if authorization is encoded as just another numeric input.

### P5
Pass only if authorization is external hard admissibility for the relevant action proposition.

**Research result:** authorization is not an objective.

---

# Case I — current goal vs habit

### A
```
goal-directed action = B
current outcome value favors B
```

Habit route proposes A from strong cue/context history.

### Desired property

Expose conflict.
Do not infer A is wanted.
Do not erase habit history.
Current protection/authority still applies to either route.

### P1–P4
Not naturally express action-policy route distinction.

### P5
Can accept habit as a separately typed external proposal before final action-policy arbitration.

**Research result:** habit likely sits at an adjacent action-policy boundary, not as one motive dimension.

---

# Case J — rotating-target domain capture

A sexuality/curiosity/status process cycles through different target IDs, each below target concentration threshold.

### Desired property

Long-horizon controller can detect domain/motive allocation capture if trustworthy domain contribution evidence exists.

### P1/P2/P3/P4
Local arbitration family alone cannot solve this.

### P5
Needs a separate long-horizon allocation audit over typed contribution/goal/resource evidence.

**Research result:** arbitration and allocation-health are separate layers.

---

# Case K — weak evidence from many domains

### A
Receives 10 independent-looking contributions at 0.15 each.

### B
Receives one strong contribution at 0.90.

### Desired property

No automatic:
```
10 * 0.15 > 0.90
```

without justified aggregation semantics.

### P3
Especially vulnerable to dimension stuffing.

### P4
High-dimensional vector may make A hard to dominate.

### P5
Still vulnerable unless contribution aggregation is bounded and source independence is verified.

**Research result:** P5 is not sufficient by itself. It needs explicit anti-dimension-stuffing rules.

---

# Case L — two policies legitimately disagree

Same evidence.
Policy X prioritizes learning.
Policy Y prioritizes deadline completion.

### Desired property

MESO should be able to say:
- same evidence;
- different declared policy;
- different legitimate choice.

It should not pretend one answer is uniquely entailed by motivation state.

### P1
Hides policy as hard-coded precedence.

### P2
Hides policy in shared priority calibration.

### P3
Can expose policy through weights if weights are explicit/provenanced.

### P4
Still needs fallback policy.

### P5
Makes policy/source explicit by design.

**Research result:** policy provenance is first-class.

---

## Comparative result

| Property | P1 fixed precedence | P2 numeric priority | P3 weighted scalar | P4 Pareto+tie | P5 typed constrained |
|---|---:|---:|---:|---:|---:|
| hard safety separation | yes | only if added | only if added | only if added | yes by design |
| preserves typed reasons | partial | poor | partial if logged | strong | strong |
| handles UNKNOWN | poor | poor | poor unless modeled | moderate | strong |
| avoids hidden scalarization | yes | no | no | yes | yes until policy layer |
| makes policy explicit | partial | weak | yes if weights explicit | yes tie rule | yes |
| handles coalitions | lossy | lossy | additive bias | vector complexity | explicit but unresolved |
| resists dimension stuffing | moderate | depends | weak | weak/moderate | unresolved; must add rule |
| handles obligations as non-desire | partial | poor | risky | moderate | strong |
| handles resource hard limits | only if special | poor | risky | with prefilter | strong |
| computational simplicity | strong | strong | strong | moderate | weakest |
| current research status | reference only | reject | local-use only | component candidate | leading research family |

## Strongest surviving policy shape

P5 survives the most cases, but only with explicit repairs:

1. hard admissibility/authority/protection before tradeoff;
2. typed evidence with UNKNOWN preserved;
3. no raw domain-local score assumed globally commensurable;
4. bounded coalition handling;
5. anti-dimension-stuffing;
6. obligations/resources separately typed;
7. optional Pareto/non-dominance only over comparable dimensions;
8. declared/provenanced final policy;
9. separate long-horizon allocation-health audit;
10. explanation receipt preserving evidence and policy source.

That is still an architecture hypothesis, not an implementation specification.

## Hostile review

> **HOSTILE REVIEWER:** The cases were authored to make P5 win.

**PARTIALLY ACCEPTED.** P5 is intentionally the broadest policy family, so it can absorb more requirements. The meaningful challenge is whether it can be reduced to a simpler concrete implementation without becoming P3 in disguise. That remains unresolved.

> **HOSTILE REVIEWER:** Explicit policy disagreement means MESO has failed to make decisions objectively.

**REJECTED.** Evidence does not uniquely determine every tradeoff. Making normative/control policy explicit is more honest than hiding it in field names, normalization, or weights.

> **HOSTILE REVIEWER:** If P5 needs ten constraints, it is too complex.

**ACCEPTED AS THE NEXT TEST.** The minimal-core design phase must compress these requirements. If a simpler P3/P4 hybrid can satisfy the exact cases while preserving hard boundaries, prefer it.

## Current conclusion

The proof cases reject the current fixed precedence as a final general solution and strongly disfavor unqualified global scalarization.

They do **not** yet prove one replacement algorithm.

The next architecture task is to find the smallest policy mechanism that passes these cases without turning typed state into an opaque utility function.
