# MESO-CRCT Predictive Resource and Allostasis Research V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / CORE-INTERFACE REFINEMENT / NO_IMPLEMENTATION`

## Purpose

Current MESO homeostasis is reactive:

```
setpoint - current_level -> deficit
deficit × corrective_affordance -> incentive boost
```

That is deliberately small and useful.

A more general architecture also needs to consider actions whose resource consequences are predictable **before** a deficit appears.

This pass asks how to add predictive resource awareness without turning MESO into a biologically themed resource manager.

## 1. Homeostasis and allostasis solve different functional problems

### Reactive homeostasis
Responds to current deviation from a desired operating range.

### Predictive/allostatic regulation
Changes current policy in anticipation of expected future demand or environmental state.

Functional machine example:

```
battery = 65%
current deficit = none
predicted task demand = 55%
required reserve after task = 20%
=> task is currently resource-infeasible without recharge
```

A reactive deficit-only system sees no problem at 65%.

## 2. Predictive resource state is not a motive

A forecast such as:
```
expected GPU memory pressure = high
```
is a state estimate.

It does not imply:
```
the agent wants less memory use
```

A policy, goal, or viability constraint determines how the forecast matters.

Hard boundary:

```
resource_state != desire
resource_forecast != conation
resource_pressure != suffering
```

## 3. Real machine resources should replace biological metaphors

Candidate machine resources:
- power/energy;
- thermal margin;
- CPU/GPU compute;
- VRAM/RAM;
- storage;
- network bandwidth;
- API quota/rate limits;
- monetary/spend budget;
- context/token capacity;
- wall-clock/deadline budget;
- execution-lane availability;
- operator-attention requirement.

Not all are suitable MESO inputs.

For each candidate ask:
1. Is it actually measured?
2. Who owns the measurement?
3. Is the measurement current?
4. Is the resource replenishable?
5. Is it hard-limited or merely costly?
6. Does MESO need it for appraisal or can the host precompute feasibility?

## 4. Resource measurement belongs outside MESO

The producer could be:
- operating system;
- scheduler;
- device telemetry;
- API provider;
- budget service;
- task planner;
- execution controller.

MESO should receive provenance-bound resource evidence.

```
RESOURCE_PROVIDER
    -> current state + forecast + uncertainty
    -> MESO appraisal
```

MESO must not self-attest:
- “battery low”;
- “GPU available”;
- “budget remains”;
- “token capacity sufficient.”

## 5. Predicted demand is also externally grounded

A task/resource estimator may provide:
- expected consumption;
- uncertainty/range;
- peak requirement;
- expected duration;
- recoverability;
- fallback options.

MESO can combine:
```
current resource state
+
predicted demand
+
reserve/policy requirement
```
to evaluate resource feasibility.

But a domain profile should not invent favorable resource estimates merely to increase its chance of selection.

## 6. Setpoints may be policy, not natural truth

Current `NeedAxis.setpoint` is a convenient generic abstraction.

For a machine:
- 20% battery reserve;
- 2 GB free memory;
- $0 spend ceiling;
- thermal safety margin

may come from:
- hard safety requirements;
- operator configuration;
- optimization policy;
- application contract.

These have different authority.

Future resource regulation should type:
```
hard minimum
soft target
reserve policy
preferred operating range
```
rather than calling all of them setpoints.

## 7. Predictive regulation can change action before need exists

Candidate functional transitions:

```
future deficit predicted
-> increase relevance of replenishment target

future resource shortfall predicted
-> lower feasibility of expensive target

future deadline/resource collision predicted
-> alter plan/effort allocation
```

These are different effects.

Do not make every predicted shortfall simply boost a “resource acquisition” incentive.

## 8. Multiple resources should not collapse into one vitality scalar

An action may be:
- low energy;
- high latency;
- high API spend;
- low memory.

Another may reverse those tradeoffs.

A scalar:
```
resource_health = 0.63
```
would erase which constraint matters.

Prefer typed resource dimensions plus a declared local policy.

## 9. Bottleneck vs additive resource cost

Some resources behave as hard bottlenecks:

```
needs 20 GB VRAM
available 16 GB
=> infeasible
```

Others can trade off:

```
slower CPU path vs paid GPU path
```

Therefore resource appraisal should distinguish:
- hard requirement;
- consumptive cost;
- recoverable capacity;
- substitutable resource;
- reserve constraint.

This links to constrained arbitration.

## 10. Resource rationality is a useful machine-side comparison

Resource-rational theories ask how limited computation itself changes optimal inference/decision strategy.

MESO can borrow one principle:

> The cost of deciding is itself part of the environment.

But MESO should not make every cognition choice a utility optimization problem.

Useful applications:
- how much evidence to gather;
- how much reasoning depth to allocate;
- whether another model/tool call is worth the latency/compute;
- whether exact computation is worth resource cost.

## 11. Prediction uncertainty matters

A forecast:
```
expected task cost = 20 units ± 1
```
differs from:
```
expected task cost = 20 units ± 20
```

Under high uncertainty, policy may:
- reserve more;
- gather information;
- choose robust plan;
- defer.

Do not hide uncertainty inside a pessimistic scalar.

## 12. Allostatic adaptation should not silently rewrite goals

If resource pressure repeatedly causes a target to lose selection, MESO should not infer:
```
target is no longer wanted
```

It may instead learn:
- this strategy is expensive;
- this timing is bad;
- this resource forecast matters;
- seek cheaper route.

Again:
```
selection history != authored preference
```

## 13. Long-horizon resource debt / load

Biological allostatic load is a health concept and should not be copied literally.

But machines can accumulate real persistent costs:
- thermal wear;
- battery cycle wear;
- quota depletion;
- backlog;
- financial spend;
- memory pressure;
- storage growth.

If such costs matter, represent the actual quantity.

Do not call it stress or allostatic load unless the term has a precise implementation meaning.

## 14. Relationship to homeostatic NeedAxis

Current `NeedAxis` may remain useful for bounded synthetic/abstract needs.

Do not force real resource evidence into it if doing so loses:
- units;
- uncertainty;
- hard limits;
- future forecast;
- provenance.

Potential future split:

```
HomeostaticNeedState
ResourceState
ResourceForecast
ResourcePolicy
```

Whether all four are needed remains open.

## 15. Relationship to effort and feasibility

Predictive resource evidence primarily affects:
- feasibility;
- effort cost;
- vigor limits;
- timing.

It may secondarily alter incentive for corrective/replenishment action.

Conceptual path:

```
resource evidence
-> feasibility / effort appraisal
-> arbitration
-> vigor proposal
```

not:

```
resource evidence
-> global reward scalar
```

## 16. Relationship to protection

Some resource conditions are safety-critical:
- overheating;
- imminent battery shutdown;
- storage corruption risk.

Those may feed a hard protection/admissibility layer.

Others are merely costs.

```
low budget != hazard
high latency != hazard
thermal emergency may be hazard
```

The provider/policy must type the distinction.

## 17. Required adversarial cases

### RA-01 — future shortfall before deficit
No current deficit; predicted task consumption violates reserve.

### RA-02 — forecast uncertainty
Same expected cost, different uncertainty -> different robust policy possible.

### RA-03 — bottleneck
One hard resource shortage makes target infeasible despite high other capacity.

### RA-04 — substitution
Paid fast resource and free slow resource are alternative plans, not one averaged capacity.

### RA-05 — preference preservation
Target repeatedly delayed due to resource shortage without durable value reduction.

### RA-06 — false producer claim
Domain profile cannot self-declare “resources available” without accepted provider evidence.

### RA-07 — stale telemetry
Old resource state must not remain current indefinitely.

### RA-08 — protected spend
High expected value does not authorize paid compute.

### RA-09 — replenish
Corrective action can gain incentive from forecasted shortage without pretending shortage is painful.

### RA-10 — mixed resources
Different resources conflict; no hidden one-number health score.

## Candidate dispositions

### Current homeostatic NeedAxis
Status: `KEEP_EXISTING_CORE / ABSTRACT NEED MODEL`

### Actual machine resource state
Status: `EXTERNAL_VERIFIED_STATE`

### Predicted resource demand
Status: `EXTERNAL_VERIFIED_OR_ESTIMATED_STATE`

### Resource feasibility/cost derivation
Status: `STRONG_CORE_APPRAISAL_CANDIDATE`

### Reserve/operating policy
Status: `EXTERNAL_POLICY / AUTHORITY-TYPED`

### Predictive need modulation
Status: `CORE_RESEARCH_CANDIDATE`

### One global resource-health scalar
Status: `REJECT_AS_CORE_COLLAPSE`

## Hostile review

> **HOSTILE REVIEWER:** This belongs entirely in a scheduler; MESO should receive only a final feasibility flag.

**PARTIALLY ACCEPTED.** That may be the right minimal architecture for some deployments. The counterargument is that effort, resource tradeoffs and corrective motivation may require richer evidence. The next design should compare both interfaces.

> **HOSTILE REVIEWER:** Calling this allostasis adds biology-flavored jargon with no benefit.

**ACCEPTED AS A NAMING RISK.** The durable engineering term may simply be `predictive resource regulation`. “Allostasis” is useful as research provenance, not necessarily as API vocabulary.

> **HOSTILE REVIEWER:** The host can manipulate resource forecasts to steer MESO.

**ACCEPTED.** Resource providers are part of the trust boundary. Provenance/currentness and independent readback matter where consequences are significant.

## Current conclusion

The research supports **predictive resource regulation** as a domain-general interface problem.

The safest current architecture direction is:

```
external resource truth/forecast
-> MESO feasibility + effort appraisal
-> constrained arbitration
-> bounded vigor proposal
```

while keeping:
- desire;
- identity;
- authority;
- suffering

out of raw resource state.

No implementation is proposed here.
