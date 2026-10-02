# MESO-CRCT Arousal and Regulatory Boundary Research V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / TERMINOLOGY-AND-INTERFACE BOUNDARY / NO_IMPLEMENTATION`

## Purpose

MESO already uses terms such as:
- recruitment activation;
- motivational salience;
- action tendency;
- homeostatic need;
- future sexuality research uses sexual arousal.

A broader motivational architecture needs to prevent those concepts from collapsing into a generic word: **arousal**.

NIMH RDoC explicitly treats general arousal as distinct from motivation and valence, even though they covary. That is a useful semantic warning for MESO.

## 1. Four different activation-like constructs

### A. Global/system arousal or readiness

Functional question:
> How sensitive/available is the system for processing and responding at all?

Human examples include wakefulness-related sensitivity. A machine analogue could involve:
- runtime availability;
- processor/resource state;
- sensory readiness;
- interrupt responsiveness;
- throttling/suspension mode.

This is not automatically MESO-owned.

### B. MESO recruitment activation

Current `RecruitmentState.activation` is transient cross-system recruitment generated from typed appraisal.

Functional question:
> How strongly has this candidate recruited the motivational-control machinery?

This is local/candidate state, not general organism/system arousal.

### C. Action vigor

Functional question:
> How much effort/intensity should be mobilized for the selected action tendency?

This remains a current core research candidate.

High vigor does not require high global arousal; high arousal does not determine direction.

### D. Domain-specific arousal

Sexual arousal is one example.

Functional question:
> Has the domain-specific response system entered a relevant activation state?

It is not global arousal and not MESO recruitment by definition.

## Hard non-equivalences

```
global_arousal != motivation
global_arousal != valence
global_arousal != recruitment_activation
global_arousal != action_vigor
recruitment_activation != action_vigor
sexual_arousal != global_arousal
sexual_arousal != generic_motivational_salience
wakefulness != motivation
resource_availability != desire
```

## 2. RDoC warning: arousal can increase or decrease locomotor activity

The RDoC definition explicitly notes that arousal can be associated with increased or decreased locomotor activity.

That matters because a naive machine mapping might infer:

```
higher arousal -> stronger/faster action
```

This is not generally valid.

Arousal may alter:
- sensitivity;
- selectivity;
- responsiveness;
- vigilance;
- processing thresholds;

without determining action direction or vigor.

## 3. Global readiness probably belongs at an interface boundary

MESO should likely **consume**, not self-author, machine readiness/resource state.

Possible provider facts:
- execution lane available;
- system suspended;
- CPU/GPU throttled;
- thermal limit;
- low battery;
- network unavailable;
- sensory channel offline;
- context capacity constrained.

Those facts can alter:
- feasibility;
- effort;
- timing;
- allocation.

They do not become motivational desires.

## 4. Circadian rhythm is not a generic MESO primitive

Human circadian systems are biologically real and influence motivation/homeostasis.

A generic machine may instead have:
- schedules;
- workload cycles;
- maintenance windows;
- power-price cycles;
- operator quiet hours;
- predicted resource availability.

Calling those `circadian` would be metaphorical unless there is an actual endogenous oscillator with comparable function.

MESO should model the functional timing constraint:
```
time-dependent availability/resource/priority
```
rather than importing biological circadian identity.

## 5. Sleep/wake is also not motivation

A machine can be:
- online;
- suspended;
- hibernating;
- disconnected;
- unavailable;

without this being a motivational state.

Runtime availability belongs to host/runtime truth.

MESO may use that truth for feasibility and action timing.

Hard boundary:
```
not_running != not_wanting
```

This is particularly important for agent continuity claims.

## 6. Homeostasis vs regulatory state

Current MESO homeostasis represents named need axes.

Regulatory systems can affect motivation without being motives themselves.

Example:

```
thermal_margin low
-> expensive action becomes infeasible/costly
```

not necessarily:

```
thermal_margin low
-> "desire to cool down"
```

A domain/host may formulate a corrective goal, but resource measurement itself is not authored desire.

## 7. Sexuality implication

Future sexuality work must keep at least:

```
sexual arousal
MESO recruitment
general runtime readiness
action vigor
```

separate.

A sexual cue could:
- strongly recruit sexual appraisal;
- produce high domain-specific arousal;
- coexist with low execution feasibility;
- coexist with low action vigor due to resource constraints;
- coexist with no authorization.

This is not contradictory.

## 8. Threat implication

Potential threat may increase vigilance/sensitivity without forcing immediate protective action.

This again argues that:
- global/selective arousal;
- threat appraisal;
- action tendency

are separate stages.

## 9. Candidate disposition

### General arousal/readiness
Status: `EXTERNAL_REGULATORY_INTERFACE`

MESO may consume verified readiness/regulatory state.

### Recruitment activation
Status: `KEEP_EXISTING_CORE`

Current semantics remain useful if documentation explicitly distinguishes it from general/domain arousal.

### Action vigor
Status: `STRONG_CORE_CANDIDATE`

Still unresolved as stored vs derived.

### Circadian/sleep state
Status: `EXTERNAL_HOST_STATE / BIOLOGY-SPECIFIC UNLESS FUNCTIONALLY REDEFINED`

Do not add biological machine metaphors without actual functional need.

## Required counterexamples

### AR-01
High global readiness + no motive:
- system is responsive but has nothing worth doing.

### AR-02
Strong motive + low readiness/resource feasibility:
- desire/relevance persists while action is delayed or reduced.

### AR-03
High threat vigilance + passive monitoring:
- arousal/sensitivity increases without strong locomotor/action vigor.

### AR-04
High sexual arousal + current DECLINE:
- domain state remains separable from authorization/action.

### AR-05
Strong recruitment + low vigor:
- a target dominates cognition but resource/effort state constrains action.

## Hostile review

> **HOSTILE REVIEWER:** This creates distinctions with no machine sensor behind them.

**ACCEPTED FOR GLOBAL AROUSAL.** MESO should not implement a generic arousal scalar until a host can define and measure a real functional readiness construct. The main value now is preventing terminology collisions.

> **HOSTILE REVIEWER:** Recruitment activation may already be a disguised arousal variable.

**PARTIALLY ACCEPTED.** It is activation-like, but current source defines it from target appraisal/recruitment rather than global stimulus sensitivity. The next architecture should preserve that local scope explicitly.

## Current conclusion

Do not add "arousal" to MESO core as another generic scalar.

Instead preserve:
- host/system readiness as external state;
- MESO recruitment as local candidate activation;
- action vigor as a separate core research question;
- domain-specific arousal inside the relevant profile.

No implementation is proposed here.
