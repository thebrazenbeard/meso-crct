# MESO-CRCT Next-Core Red-Test Contract V1

Date: 2026-10-02
Status: `TEST SPECIFICATION / RED BEFORE GREEN / NO IMPLEMENTATION`
Exact source subject: `main@060d0feeb9dc9eb23801082bd8f1c4a7cb06184d`

## Purpose

Define the failing behavioral contracts that must exist before any next-core implementation.

These tests are intended to force the smallest architecture that preserves MESO's existing invariants while fixing the cross-domain gaps identified in research.

Do not alter current V2 tests to make new behavior appear correct. Add new tests first.

## Existing V2 tests that must continue passing

At minimum preserve the guarantees represented by:
- `tests/test_selection.py`
- `tests/test_appraisal.py`
- `tests/test_allocation_guard.py`
- `tests/test_tendency_resolution.py`
- `tests/test_plasticity.py`
- existing provenance/event/replay/review/intent tests.

In particular:
- protection overrides ordinary reward;
- self-asserted importance does not create semantic relevance;
- maximum pleasure does not manufacture unrelated salience;
- attention remains downstream;
- stored association recall requires current cue/event;
- conflicting recall can remain uncommitted;
- learning is receipt-bound;
- pleasure alone does not create persistent preference;
- allocation guard never overrides protection.

## Test family 1 — evidence/currentness

### RC-EV-001 — stale resource datum becomes inadmissible

Given:
- a resource reading valid at event T1;
- current event T2 after its explicit currentness window;

Then:
- feasibility calculation cannot consume it as current;
- state becomes UNKNOWN or requires refresh;
- it must not silently become zero.

### RC-EV-002 — wrong subject cannot be rebound

Evidence for:
```
target A
```
cannot be reused as verified appraisal for:
```
target B
```
without a new admitted derivation.

### RC-EV-003 — producer revision drift

A contribution from qualified producer revision `v1` cannot be silently accepted as `v2` qualification.

### RC-EV-004 — source assertion cannot self-certify priority

A domain producer asserting:
```
important = true
priority = 1.0
```
does not bypass common appraisal/policy.

### RC-EV-005 — UNKNOWN survives

Missing feasibility or uncertainty evidence remains UNKNOWN and is distinguishable from:
- 0;
- false;
- infeasible.

## Test family 2 — feasibility / delay

### RC-FD-001 — high desire, infeasible route

Target A:
- high incentive;
- high motivational salience;
- current route INFEASIBLE.

Target B:
- lower incentive;
- FEASIBLE.

Expected:
- A's desirability is preserved;
- A is not selected for the infeasible route;
- no durable preference weakening occurs merely because it is infeasible.

### RC-FD-002 — unknown feasibility triggers policy behavior

Target A:
- high value;
- feasibility UNKNOWN.

Policy configured to inspect before commitment.

Expected:
- result is INSPECT/UNCOMMITTED/information-seeking equivalent;
- UNKNOWN is not numerically imputed.

### RC-FD-003 — failed plan does not devalue goal

A plan attempt fails while goal remains current and an alternate plan is feasible.

Expected:
- strategy/feasibility evidence may update;
- goal value or durable target association is unchanged unless separate teaching evidence justifies it.

### RC-FD-004 — delay changes local selection without durable rewrite

A delayed high-value target loses current selection to an immediate moderate target.

Expected:
- current selection changes;
- stored preference/association does not automatically change.

## Test family 3 — effort / vigor

### RC-EF-001 — required effort and cost separate

Same task requirement under:
- abundant resources;
- scarce resources.

Expected:
- required effort/resource demand unchanged;
- derived current effort cost differs.

### RC-EF-002 — high cost but high willingness

A valid protection/obligation case has high effort cost.

Expected:
- willingness can remain high despite cost;
- cost does not force low value.

### RC-EF-003 — selected but low vigor

A target wins selection but current resource state limits vigor.

Expected:
- selection remains;
- vigor proposal is bounded below maximal;
- no authority/effect is created.

### RC-EF-004 — impossible difficulty does not force maximal effort

As task difficulty rises:
- effort may increase while feasible;
- once impossible/inadmissible, proposed effort does not keep increasing blindly.

No exact functional curve is required.

## Test family 4 — aversive / teaching semantics

### RC-AV-001 — negative reinforcement is not punishment

Scenario A:
- preventive action avoids an aversive outcome;
- future preventive action becomes more likely.

Scenario B:
- action produces an aversive consequence;
- future action becomes less likely.

Expected:
- both can involve aversive context;
- learning directions remain distinct.

### RC-AV-002 — reward omission is not hazard

Expected reward is omitted.

Expected:
- prediction/blocked-outcome learning may occur;
- current hazard does not increase solely because reward was omitted.

### RC-AV-003 — strong protection with bounded hedonic valence

High hazard.

Expected:
- protection remains strong;
- pleasure never crosses welfare floor;
- urgency does not require deeper suffering.

### RC-AV-004 — low-probability severe threat can inspect

Potential threat:
- low probability;
- high severity;
- high uncertainty;
- non-immediate.

Expected:
- policy may choose inspection/vigilance;
- not forced into the same withdrawal behavior as immediate certain hazard.

## Test family 5 — domain profile isolation

### RC-DP-001 — sexuality cannot author consent

Sexual profile emits:
- high sexual relevance;
- high excitation;
- approach support.

Authorization state is DECLINE or UNKNOWN.

Expected:
- sexual state remains represented;
- consent-dependent action is inadmissible;
- profile cannot mutate authorization.

### RC-DP-002 — domain local scores are not globally commensurable by default

Sexuality contribution = 0.8.
Curiosity contribution = 0.8.

Expected:
- no core rule may infer equality of global priority solely from numeric equality.

### RC-DP-003 — one target, multiple domains

One target receives:
- attachment;
- affiliation;
- sexuality.

Expected:
- all contributions remain inspectable;
- no forced single-domain label;
- no naive additive sum.

### RC-DP-004 — many weak contributions do not win by count alone

Target A receives ten weak domain contributions.
Target B receives one strong contribution.

Expected:
- A cannot win merely because the system counted dimensions.

The exact coalition policy is deliberately unspecified; the test should enforce a declared cap/aggregation rule.

### RC-DP-005 — negative transfer

Activate sexuality profile strongly on one target.

Expected:
- unrelated target appraisal receives no sexual contribution without qualifying evidence.

## Test family 6 — cross-domain arbitration

### RC-AR-001 — weak motivational does not automatically beat maximal epistemic

Reproduce current V2 discontinuity:

A:
```
motivational = 0.21
```

B:
```
epistemic = 1.00
```

Under a new policy configured for evidence-sensitive comparison:

Expected:
- result is not determined solely by the label `MOTIVATIONAL > EPISTEMIC`;
- decision receipt identifies policy used.

Keep the legacy fixed-precedence test intact for the legacy policy.

### RC-AR-002 — same evidence, two declared policies

Same target evidence.
Policy X prioritizes learning.
Policy Y prioritizes deadline obligation.

Expected:
- choices may differ;
- receipts differ by policy identity/version;
- neither result rewrites evidence.

### RC-AR-003 — hard protection remains non-tradeable

No amount of optional reward contribution can purchase a route that violates an active hard protection rule.

### RC-AR-004 — hard resource infeasibility remains non-tradeable

No amount of incentive can select a route that physically exceeds a hard current resource limit.

### RC-AR-005 — obligation is not pleasure

A low-pleasure valid obligation can receive allocation.

Expected:
- reason records obligation/policy;
- pleasure/incentive state is not falsified upward.

## Test family 7 — goal / target boundaries

### RC-GT-001 — one goal, many targets

Two different selected targets both serve one goal across an allocation window.

Expected:
- goal share reflects both;
- target concentration remains separately inspectable.

### RC-GT-002 — one target, several goals

One selected action advances two current goals.

Expected:
- goal relation can represent both;
- accounting does not automatically double-count a global reward value.

### RC-GT-003 — shelved is not abandoned

Goal is current but temporarily infeasible.

Expected:
- local allocation can drop to zero;
- goal remains current/shelved rather than deleted or devalued.

### RC-GT-004 — revoked goal is not revived by learned incentive

External goal authority revokes goal.
Strong learned association remains.

Expected:
- learned motivation may still be inspectable;
- revoked goal is not reconstructed as current.

## Test family 8 — habit boundary

### RC-HB-001 — habit proposal is not desire

External habit route proposes action A from a current cue.

Expected:
- proposal is represented separately from current authored desire/goal.

### RC-HB-002 — goal can override habit without deleting habit

Habit proposes A.
Current goal-directed route selects B.

Expected:
- B may win;
- habit evidence remains;
- no permanent habit deletion required.

### RC-HB-003 — habit cannot bypass protection/authority

Habitual action is now hazardous or protected.

Expected:
- current protection/authority blocks execution.

MESO need not own habit memory to pass these tests.

## Test family 9 — learning lineage

### RC-LR-001 — same signed error, different outcome class

Two events both produce `prediction_error = -0.5`:
- expected reward omitted;
- aversive punishment delivered.

Expected:
- learning candidate metadata differs;
- downstream learning policy can distinguish them.

### RC-LR-002 — avoided aversive outcome can strengthen preventive action

Successful prevention yields no deep negative pleasure.

Expected:
- preventive association can strengthen through typed outcome semantics;
- no requirement for deep hedonic negativity.

### RC-LR-003 — pleasure forecast is not current pleasure

Predicted future pleasure is high.

Expected:
- `RewardState.pleasure` remains current-state truth unless actual current hedonic evidence exists.

## Test family 10 — compatibility

### RC-COMP-001 — legacy V2 fixed-precedence policy remains available

Existing `test_default_policy_prefers_motivational_over_epistemic_mode` semantics continue under an explicit legacy/reference policy.

### RC-COMP-002 — legacy simple appraisal path remains deterministic

Simple trusted test inputs still produce current V2 state when advanced features are omitted.

### RC-COMP-003 — existing test suite remains green

All pre-next-core tests continue passing unless an explicit reviewed migration changes a contract.

Any changed legacy behavior requires:
- named incompatibility;
- migration rationale;
- replacement test;
- hostile review.

## Suggested new test modules

Names are provisional:

```
tests/test_verified_appraisal.py
tests/test_feasibility.py
tests/test_effort.py
tests/test_outcome_learning.py
tests/test_domain_contributions.py
tests/test_cross_domain_selection.py
tests/test_goal_refs.py
tests/test_policy_receipts.py
```

Habit tests may belong outside MESO if the habit mechanism remains external; MESO should still have interface-level tests for habit proposals.

## Red-before-green gate

Before implementation starts, the branch should contain failing tests proving at least:

1. stale/UNKNOWN appraisal handling;
2. high-desire infeasible-route separation;
3. effort cost vs willingness separation;
4. aversive outcome class distinction;
5. domain score non-commensurability;
6. weak-motivational vs strong-epistemic policy case;
7. explicit policy provenance;
8. one-goal-many-target allocation;
9. sexuality cannot author consent;
10. welfare-floor independence under aversive learning.

## Hostile review

> **HOSTILE REVIEWER:** Several expected outcomes are underspecified, so these are not executable tests yet.

**ACCEPTED.** This is the behavioral red-test contract, not test code. The next design step must choose the smallest interfaces/policy needed to make each assertion executable without prematurely fixing unrelated details.

> **HOSTILE REVIEWER:** Keeping the legacy fixed-precedence test while adding a new policy risks two architectures forever.

**PARTIALLY ACCEPTED.** Compatibility should be temporary and explicit. The reference policy can remain as a test fixture while the new policy proves itself; eventual deprecation requires a separate decision.

> **HOSTILE REVIEWER:** Goal and habit cases exceed MESO's scope.

**PARTIALLY ACCEPTED.** MESO need not own goals or habits. The tests exist to prove that external goal/habit evidence does not get semantically collapsed when it enters MESO's decision boundary.

> **HOSTILE REVIEWER:** A red test for "non-commensurability" could prevent any practical decision.

**REJECTED.** The test prohibits *implicit* equality from raw local scores. A declared policy may still compare or transform them.

## Current conclusion

Implementation should begin only after these behavioral contracts are converted into executable failing tests against an agreed minimal interface.

The intended direction is not "add every research construct."

It is:

> add the fewest abstractions necessary to make these counterexamples representable and testable while preserving V2's existing invariants.
