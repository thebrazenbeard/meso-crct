# MESO Goal-Target Allocation Boundary Implementation Plan

> **For agentic workers:** Use the host's available task-by-task implementation workflow. Steps use checkbox syntax for tracking.

**Goal:** Separate goal attribution from selected target identity in long-horizon allocation accounting while preserving V2 compatibility.

**Architecture:** Add a provenance-bearing GoalRelation that states a current target-to-goal relationship. AllocationWindow.record() may receive zero or more current goal relations for the selected target and stores them with the sample. Audits count goal participation from those relations; legacy samples with no relations retain the V2 goal_id == target_id fallback.

**Tech Stack:** Python 3, frozen dataclasses, pytest.

## Global Constraints

- Base is Draft PR #8 head 0db07691b277f75185d76b8810869765bc2543e7.
- Do not alter local target selection/arbitration.
- TDD red before implementation.
- Target identity and goal identity remain distinct.
- Goal relations must be source/currentness bound with EvidenceRef.
- STALE/UNKNOWN goal relations are inadmissible at record time.
- A relation must refer to the actually selected target.
- Duplicate goal relations for one sample may not double-count allocation.
- One target may serve multiple goals.
- One goal may span multiple different selected targets.
- Existing V2 allocation tests must remain green through an explicit legacy fallback.
- This tranche does not implement goal lifecycle, planner state, goal creation, or obligation authority.

---

### Task 1: Provenance-bearing goal relations

**Files:**
- Create: src/meso_crct/goals.py
- Modify: src/meso_crct/allocation.py
- Modify: src/meso_crct/__init__.py
- Test: tests/test_goal_target_allocation.py

**Interfaces:**
- Produces GoalRelation(goal_id, target_id, evidence).
- Extends AllocationSample with immutable goal_relations.
- Extends AllocationWindow.record(result, *, goal_relations=()).
- audit_attention_budget computes goal share from unique current goal relations; a relation-free sample uses the legacy target_id == goal_id rule.

- [ ] Step 1: Add focused failing tests.
  - Two different targets related to one goal produce a combined goal share.
  - One selected target related to two goals counts once toward each goal.
  - Duplicate relations for the same goal in one sample do not double-count.
  - A relation whose target does not match the selected target is rejected.
  - STALE/UNKNOWN relation evidence is rejected.
  - Existing relation-free legacy sample still counts when target ID equals goal ID.
- [ ] Step 2: Verify expected RED.
  Run: python -m pytest -q tests/test_goal_target_allocation.py
  Expected: assertion failures for the absent public GoalRelation/recording contract, not import/setup errors.

- [ ] Step 3: Implement minimum behavior.
  Keep GoalObligation unchanged. A GoalRelation records only a current relation; it does not create a goal, obligation, desire, or authority.

- [ ] Step 4: Verify focused GREEN.
  Run identical command.
  Expected: all new tests pass.

- [ ] Step 5: Run integration suite.
  Run: python -m pytest -q
  Expected: existing 242 tests plus new tests pass.

- [ ] Step 6: Commit.
  Commit message: feat: separate goal attribution from target identity

## Unresolved externally observable decisions

- Goal lifecycle states such as active, shelved, revoked, completed.
- Provenance/authority model for GoalObligation.
- Whether goal relations should eventually live in a planner-owned receipt rather than directly in allocation samples.
- Whether domain and goal allocation audits should share a common contribution ledger.
