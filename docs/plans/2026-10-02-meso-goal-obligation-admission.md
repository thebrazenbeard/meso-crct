# MESO Goal Obligation Admission Implementation Plan

> **For agentic workers:** Use the host's available task-by-task implementation workflow. Steps use checkbox syntax for tracking.

**Goal:** Add a provenance/currentness/admission gate for raw goal-allocation obligation claims without changing GoalObligation audit semantics or creating action authority.

**Architecture:** Add a standalone obligations module. Raw GoalObligationClaim objects carry EvidenceRef. A host-supplied GoalObligationAdmissionPolicy admits exact producer ID/revision pairs. admit_goal_obligation() validates currentness, subject identity, and producer admission, then returns the existing GoalObligation type.

**Tech Stack:** Python 3, frozen dataclasses, pytest.

## Global Constraints

- Base is Draft PR #10 head d7721a341c04728db73d74736870d80dda797191.
- TDD red before implementation.
- Existing direct GoalObligation construction remains unchanged for V2 compatibility.
- Raw claims never self-authorize.
- STALE/UNKNOWN evidence cannot become active obligation.
- Evidence subject must equal claim goal_id.
- Admission policy is supplied externally; MESO does not invent trusted producers.
- Admitted GoalObligation remains allocation-floor semantics only.
- No consent or external action authority field is introduced.
---

### Task 1: Goal obligation claim admission

**Files:**
- Create: src/meso_crct/obligations.py
- Modify: src/meso_crct/__init__.py
- Test: tests/test_goal_obligation_admission.py

**Interfaces:**
- GoalObligationClaim
- GoalObligationProducerSpec
- GoalObligationAdmissionPolicy
- InadmissibleGoalObligationClaim
- UnadmittedGoalObligationClaim
- admit_goal_obligation

- [ ] Step 1: Add focused failing tests.
  - Current claim from admitted producer/revision converts to GoalObligation.
  - Spoofed producer is rejected.
  - Wrong producer revision is rejected.
  - STALE/UNKNOWN claim evidence is rejected.
  - Evidence subject mismatch is rejected.
  - Duplicate producer specs fail policy construction.
  - Admission requires an external policy argument.
  - Legacy direct GoalObligation construction still behaves as before.
  - Admitted GoalObligation exposes no execution/action-authority field.

- [ ] Step 2: Verify expected RED.
  Run: python -m pytest -q tests/test_goal_obligation_admission.py
  Expected: explicit missing-interface assertion failures, not import/setup errors.
- [ ] Step 3: Implement minimum behavior.
  Keep admission exact on producer ID + producer revision. Do not infer trust from goal content, relation evidence, or the claim itself.

- [ ] Step 4: Verify focused GREEN.
  Run identical focused command.

- [ ] Step 5: Run integration suite.
  Run: python -m pytest -q
  Expected: PR #10 suite plus new tests pass.

- [ ] Step 6: Commit.
  Commit message: feat: admit provenance-bound goal obligations

## Unresolved externally observable decisions

- Which host/governance subsystem authors the admission policy in a live runtime.
- Revocation/expiry beyond EvidenceCurrentness.
- Goal lifecycle semantics.
- Whether admitted obligation provenance should eventually be retained in audit receipts rather than converted to the legacy GoalObligation value object.
