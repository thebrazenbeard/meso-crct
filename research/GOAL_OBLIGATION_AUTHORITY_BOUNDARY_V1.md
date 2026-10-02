# MESO Goal Obligation Authority Boundary V1

Date: 2026-10-02
Status: `RESEARCH_ONLY / BOUNDARY SETTLED ENOUGH FOR RED TESTS`

## Problem

Draft PR #10 separates target identity from goal attribution, but the existing `GoalObligation` type still has a deeper ambiguity:

```
GoalObligation(goal_id, minimum_nonprotective_share)
```

states that a goal should receive a minimum share of ordinary allocation, but it does not say:
- who asserted that obligation;
- whether that producer is currently admitted to author allocation obligations;
- whether the assertion is current;
- whether the obligation is self-authored, user-authored, system policy, or some other source.

That is an evidence/authority gap.

## Fresh cross-repository constraints

Current Vera Mono contracts explicitly require:

```
REQUEST != AUTHORITY
DESIRE != CONSENT
RELATIONSHIP_CONTEXT != ACTION_AUTHORITY
```

and also preserve the more general chain:

```
AUTHORITY != ATTEMPT != EFFECT != VERIFIED_EFFECT
```

Those distinctions apply directly here.

## Required semantic separations

```
goal exists
!= target serves goal
!= goal is desired
!= goal is an allocation obligation
!= producer is admitted to author that obligation
!= obligation authorizes an external action
!= consent
```

A valid goal relation from PR #10 therefore does not prove an obligation.

Likewise, an admitted allocation obligation does not authorize execution of any protected or external effect.

## Ownership boundary

MESO should not invent who has authority.

The host/governance layer must supply an explicit admission policy identifying which producer identity/revision may author **allocation-obligation claims**.

MESO may then:
1. validate currentness;
2. validate producer identity/revision against that supplied policy;
3. convert an admitted claim into an allocation obligation used by its audit.

This is policy enforcement, not policy authorship.

## Proposed types

Research candidate:

```
GoalObligationClaim(
    goal_id,
    minimum_nonprotective_share,
    evidence: EvidenceRef,
)

GoalObligationProducerSpec(
    producer_id,
    producer_revision,
)

GoalObligationAdmissionPolicy(
    producers=(...)
)

admit_goal_obligation(claim, policy) -> GoalObligation
```

Important: the policy is an input from outside the claim.

The claim does not self-authorize.

## Currentness

A claim with:
- `CURRENT` evidence may be considered for admission;
- `STALE` or `UNKNOWN` evidence must not silently become an active obligation.

This mirrors the appraisal/goal-relation currentness discipline already established in Drafts #8 and #10.

## Why not put authority fields directly on GoalObligation?

Because `GoalObligation` is already used as the **post-admission audit input** in V2.

Changing it into a self-describing authority object would conflate:
- the obligation itself;
- the evidence that someone asserted it;
- the policy that decides whether that producer is allowed to assert it.

Keeping a separate claim/admission step preserves proposition type.

## Legacy compatibility

Existing V2 callers may continue constructing `GoalObligation` directly.

That path is a compatibility/configuration path, not proof that the object carries provenance or action authority.

New provenance-sensitive callers should use:

```
claim -> host-supplied admission policy -> admitted GoalObligation
```

## Action-authority firewall

Even an admitted goal allocation obligation means only:

> “Count this goal against this long-horizon allocation floor.”

It must not imply:
- permission to send messages;
- permission to spend money;
- permission to modify external state;
- consent to intimate/sexual action;
- authority to merge/deploy/delete;
- permission to bypass effect contracts.

Hard rule:

```
allocation obligation != execution authority
```

## Adversarial tests

### OBL-01 — admitted current producer
A CURRENT claim from an admitted producer/revision converts to a `GoalObligation`.

### OBL-02 — spoofed producer
Same claim content from an unadmitted producer is rejected.

### OBL-03 — wrong producer revision
Admitted producer ID with an unadmitted revision is rejected.

### OBL-04 — stale/unknown claim
STALE or UNKNOWN evidence is rejected.

### OBL-05 — evidence subject mismatch
The claim's evidence subject must identify the same goal the claim names.

### OBL-06 — claim cannot self-authorize
Producer metadata carried in the claim alone is insufficient without an external admission policy.

### OBL-07 — legacy compatibility
Direct V2 `GoalObligation` construction remains behaviorally unchanged.

### OBL-08 — no execution authority
The resulting `GoalObligation` exposes allocation-floor semantics only; no action/execution authority field is introduced.

## Hostile review

> **HOSTILE REVIEWER:** If the host already decides which producer is trusted, MESO does not need any obligation-admission code.

**PARTIALLY ACCEPTED.** The host owns the policy, but a typed admission gate in MESO makes the boundary testable and prevents callers from accidentally treating raw claims as admitted obligations.

> **HOSTILE REVIEWER:** Keeping direct legacy `GoalObligation` construction means provenance can still be bypassed.

**ACCEPTED.** That is a compatibility debt, not something this tranche can erase without breaking V2. The interface must label direct construction as configuration/legacy and require the claim path for provenance-sensitive use.

> **HOSTILE REVIEWER:** A producer allowlist is not a full authority system.

**ACCEPTED.** It is intentionally not one. It only binds this narrow proposition type: who may author allocation-obligation claims. Protected external effects remain governed elsewhere.

## Conclusion

The strongest surviving rule is:

> **Treat goal obligations as post-admission allocation constraints. Raw obligation claims require CURRENT provenance plus an externally supplied producer/revision admission policy; neither claims nor admitted obligations imply consent or external action authority.**
