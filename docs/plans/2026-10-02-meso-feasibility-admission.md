# MESO Feasibility Admission Implementation Plan

> **For agentic workers:** Use the host's task-by-task TDD workflow.

**Goal:** Add a conservative feasibility gate before partial-order comparison without mutating motivational state or collapsing UNKNOWN into false/infeasible.

**Base:** Draft PR #13 head 14b0c178953b052fdf77ea1a8b39bd6ce211a71b.

## Architecture

Add a feasibility gate that partitions candidate targets using current FeasibilityAssessment evidence:

- CURRENT + FEASIBLE -> admitted
- CURRENT + INFEASIBLE -> infeasible/excluded
- CURRENT + UNKNOWN -> deferred
- CURRENT + CONDITIONAL -> deferred
- STALE/UNKNOWN currentness -> deferred
- missing assessment -> deferred

Then add a feasibility-aware selection wrapper that runs select_by_partial_order() only over admitted targets. If any deferred target exists, final status is DEFERRED even when the admitted subset has a unique provisional winner.

## Constraints

- FeasibilityAssessment evidence subject must equal target_id.
- Do not mutate DomainContribution, RewardState, memory, GoalObligation, or learned association.
- Do not treat INFEASIBLE as low desire.
- Do not treat UNKNOWN/CONDITIONAL/stale/missing as numeric zero.
- Duplicate assessments for one target are rejected.
- Assessments for noncandidate targets are rejected.
- Result preserves separate infeasible/deferred/missing sets.
- Gate and wrapper inputs are order-stably digest-bound.
- Legacy V2 select_target() remains unchanged.
- No external authority or execution semantics.

### Task 1: Feasibility gate

**Files:**
- Modify: src/meso_crct/feasibility.py
- Create: src/meso_crct/feasibility_gate.py
- Modify: src/meso_crct/__init__.py
- Test: tests/test_feasibility_gate.py

**Red cases:**
- subject mismatch rejected at FeasibilityAssessment construction;
- current FEASIBLE admitted;
- current INFEASIBLE excluded;
- current UNKNOWN deferred;
- current CONDITIONAL deferred;
- STALE/UNKNOWN-currentness assessment deferred regardless of state;
- missing assessment deferred and separately reported;
- duplicate assessment rejected;
- assessment for noncandidate target rejected;
- gate digest order-stable and sensitive to state/evidence changes.

### Task 2: Feasibility-aware partial-order wrapper

**Red cases:**
- unique feasible winner + any deferred target => DEFERRED;
- all current infeasible => NO_ADMISSIBLE_CANDIDATE;
- all resolved + unique Pareto winner => SELECTED;
- all resolved + genuine Pareto tradeoff => INCOMPARABLE;
- family evidence for infeasible/deferred targets is not rewritten;
- wrapper preserves both feasibility and partial-order input digests;
- exact policy identity/revision preserved.

## Out of scope

- satisfying CONDITIONAL conditions;
- refreshing telemetry;
- hard safety/protection veto semantics;
- obligation-pressure derivation;
- fallback chooser;
- runtime activation or merge.
