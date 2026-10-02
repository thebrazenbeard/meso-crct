# MESO-CRCT Effort and Vigor Research V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / STRONG-CORE-CANDIDATE REFINEMENT / NO_IMPLEMENTATION`

## Purpose

The broader MESO research identified effort valuation and action vigor as strong domain-general candidates.

This pass refines the constructs before any schema is proposed.

## 1. Effort is not one variable

At least four questions must remain distinct:

1. **Required effort** — how demanding is the action/task?
2. **Effort cost** — how costly is that demand under current state/resources?
3. **Willingness to exert effort** — is the system prepared to pay that cost for this target?
4. **Exerted effort / vigor** — how much activation/resource is actually mobilized?

Candidate non-equivalences:

```
required_effort != effort_cost
effort_cost != willingness_to_exert
willingness_to_exert != actual_exertion
actual_exertion != action_direction
```

## 2. Effort is not automatically aversive

The "law of least effort" is not universal.

Recent motivational work emphasizes that effort can be:
- avoided;
- tolerated;
- sought for mastery/meaning;
- learned as valuable;
- required for another valued outcome.

Therefore MESO should not hard-code:

```
more effort -> less utility
```

A better question is:
> What is the current cost/meaning of this effort for this actor/system in this context?

For machines, high compute cost can be undesirable under power pressure but acceptable or preferred when quality stakes are high.

## 3. Effort and reward remain separable

Salamone & Correa's review emphasizes dissociation between reward preference/hedonic reactivity and willingness to perform high-effort actions.

A target can be:
- highly liked;
- strongly wanted;
- but not worth the current effort.

Or:
- moderately liked;
- but worth substantial effort due to obligation, mastery, protection or future value.

Thus:

```
liking != effort willingness
wanting != effort willingness
reward magnitude != vigor
```

## 4. Effort allocation is dynamic

Recent neuroeconomic work emphasizes that willingness to work varies moment-to-moment with:
- context;
- reward;
- effort requirement;
- state;
- fatigue/resource state;
- alternatives.

This argues against storing one durable trait-like `motivation_level` and treating it as action capacity.

MESO should appraise effort per candidate/current state.

## 5. Task difficulty and effort investment can be non-monotonic

Integrative work comparing motivational-intensity theory with computational effort models finds convergence around a non-monotonic relation:

- increasing difficulty can increase effort while success remains worthwhile/possible;
- once difficulty exceeds justified or feasible limits, effort can fall sharply.

This is crucial.

A naive scalar rule:

```
effort = difficulty
```

fails.

A more plausible shape depends on:
- target importance/value;
- feasibility;
- required effort;
- resource availability;
- maximum justifiable effort.

This tightly couples the effort research to the feasibility work.

## 6. Effort cost and resource cost are related but not identical

A machine action may require:
- 10 seconds;
- 2 GB memory;
- GPU use;
- API calls;
- network bandwidth;
- operator attention.

Those are resource requirements.

The **effort cost** is their current decision-relevant consequence under:
- resource availability;
- competing demands;
- deadlines;
- budgets;
- opportunity costs;
- policies.

Same action, different state:
```
required resources = same
effort cost = different
```

## 7. Cognitive vs physical/machine effort

Human research distinguishes physical and cognitive effort, with partially overlapping but non-identical mechanisms.

MESO should not need biological labels, but it may need multiple machine effort dimensions:

```
compute
latency
memory
network
energy
external API cost
operator burden
risk/execution complexity
```

Do not sum them into one cost unless the policy explicitly defines exchange rates.

Potential architecture:
- preserve resource vector/evidence;
- derive local policy cost only at comparison time.

## 8. Vigor is after selection, not target value

Current MESO action tendency has a `strength`, but this is tied to the selected decision/recall support.

That may not be the same thing as action vigor.

Vigor could determine:
- parallelism;
- compute allocation;
- retry intensity;
- response speed;
- depth of processing;
- polling/check frequency;
- resource reservation.

These are execution-adjacent properties.

### Boundary

MESO may propose vigor.

The execution host still decides whether and how resources can actually be allocated.

```
vigor_proposal != execution_authority
```

## 9. Vigor should not be inferred from arousal

The separate arousal-boundary research already rejects:

```
global arousal == action vigor
```

Likewise:
- high recruitment does not necessarily mean high vigor;
- high desire does not necessarily mean high vigor;
- high effort does not necessarily mean high vigor.

## 10. Opportunity cost belongs in the effort conversation

Allocating effort to one target consumes resources/time that could serve another.

Current MESO long-horizon allocation tracks selected target share, but not explicit opportunity cost.

Research question:
> Should opportunity cost be a derived property of current alternative targets/resources rather than a stored field?

Likely yes.

Avoid creating:
```
opportunity_cost: float
```
without a transparent derivation.

## 11. Expected value of control is a useful comparison, not a MESO template

Expected Value of Control (EVC)-style models formalize control allocation as expected payoff minus control costs.

This is useful because it separates:
- how much control to allocate;
- payoff;
- cost;
- efficacy.

But a simple EVC scalar may violate MESO's non-fungible boundaries if:
- protection;
- truth;
- authority;
- identity

are represented as ordinary costs/rewards.

Use EVC as a local effort-allocation comparison after hard constraints, not as MESO's universal utility function.

## 12. Effort can be motivated by aversion

Aversive motivation can increase control/effort to avoid a bad outcome.

Therefore:
```
effort willingness
```
must accept both appetitive and aversive reasons without collapsing them.

The output should preserve why effort is being mobilized.

## 13. Effort can be self-reinforcing or identity-relevant — but MESO should be cautious

Human work suggests beliefs about effort, learned industriousness and mastery can make effort itself valued.

For MESO:
- learned positive association with effortful action can exist;
- achievement/mastery profile may value challenge.

But:
```
effortful != virtuous
effortful != meaningful
effortful != authored_identity
```

## 14. Candidate future data model — research sketch only

Do not implement yet.

Potential evidence object:

```
EffortAssessment:
    target_id
    required_resources
    difficulty
    feasibility
    current_resource_state_ref
    expected_duration
    opportunity_set_ref
    source/currentness
```

Potential derived outputs:

```
effort_cost_profile
willingness_to_exert
vigor_proposal
```

The exact split remains open.

## 15. Required counterexamples

### EF-01 — liked but not worth effort
High pleasure/incentive; effort cost prohibitive.

### EF-02 — low pleasure, high justified effort
Care/protection/obligation target receives substantial effort.

### EF-03 — difficulty rise
Moderate difficulty increases effort; impossible difficulty reduces effort.

### EF-04 — same task, changed resources
Required resources constant; effort cost changes due to resource scarcity.

### EF-05 — high priority, low vigor
Selected target remains important but current execution intensity is constrained.

### EF-06 — low priority, high reflexive vigor prohibited
A low-value target cannot become resource-intensive merely because a caller requests high vigor.

### EF-07 — effort seeking
Mastery/play target chooses a harder path even when an easier path reaches the same external outcome.

### EF-08 — aversively motivated effort
System exerts more effort to prevent a negative outcome without calling the prevention pleasure.

### EF-09 — opportunity cost
One target's increased resource allocation changes the cost of competing targets.

### EF-10 — authority
High willingness/vigor does not authorize paid compute or protected effects.

## Candidate disposition refinement

### Required effort
Status: `CORE_APPRAISAL_CANDIDATE`

### Resource requirements
Status: `EXTERNAL_EVIDENCE / APPRAISAL_INPUT`

### Effort cost
Status: `STRONG_CORE_DERIVED_CANDIDATE`

### Willingness to exert
Status: `STRONG_CORE_DECISION_CANDIDATE`

### Action vigor
Status: `STRONG_CORE_POST-SELECTION_CANDIDATE`

### Opportunity cost
Status: `DERIVED_UNTIL_PROVEN_OTHERWISE`

## Hostile review

> **HOSTILE REVIEWER:** This is splitting one intuitive concept into too many variables.

**REJECTED WITH COUNTEREXAMPLES.** Required effort can stay constant while resource state changes cost; cost can be high while willingness remains high; selection can occur while actual vigor remains constrained. Those are mechanically different propositions.

> **HOSTILE REVIEWER:** MESO should not manage compute allocation at all.

**PARTIALLY ACCEPTED.** MESO should not execute or reserve resources by authority. It may still need to represent effort costs and propose vigor so the host can make an informed allocation decision.

> **HOSTILE REVIEWER:** Vigor is implementation-specific and belongs entirely downstream.

**UNRESOLVED.** If vigor only affects execution mechanics, host ownership may be cleaner. If it also changes cognitive-control allocation/depth before execution, a MESO output may be justified. Architecture must test both placements.

## Current conclusion

Effort is now a **strongly justified domain-general research axis**, but not as one scalar.

The minimum distinction likely needs:

```
required effort/resources
-> context-dependent effort cost
-> willingness to exert
-> post-selection vigor proposal
```

with feasibility, resource state and authority remaining explicit.

No implementation is proposed here.
