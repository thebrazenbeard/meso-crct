# MESO Next-Core Representation Tranche Implementation Plan

> **For agentic workers:** Use the host's available task-by-task implementation workflow. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the smallest settled next-core representation interfaces without changing MESO's cross-domain winner-selection algorithm.

**Architecture:** Preserve the current V2 state/arbitration/memory pipeline. Add provenance-bearing evidence and feasibility types beside it, add typed effort/outcome metadata, and make domain/policy provenance explicit. Existing fixed-precedence selection remains the legacy/reference policy; no evidence-sensitive cross-domain comparator is implemented in this tranche.

**Tech Stack:** Python 3, frozen dataclasses/enums, pytest.

## Global Constraints

- Work only on `test/next-core-red-contract-20261002`, never `main`.
- Existing V2 behavior and 226-test baseline remain green.
- TDD: each new behavior must be observed failing first for the expected reason.
- No cross-domain arbitration replacement, no scalar utility function, no runtime activation, no donor archival.
- Unknown/currentness semantics must remain distinct from numeric zero.
- Domain-local magnitude is not global priority.
- Authorization/consent is not part of motivational evidence.
- Persistent learning remains transition-receipt-bound.

---

### Task 1: Add provenance-bearing appraisal evidence and feasibility

**Files:**
- Create: `src/meso_crct/evidence.py`
- Create: `src/meso_crct/feasibility.py`
- Modify: `src/meso_crct/__init__.py`
- Test: `tests/test_next_core_evidence.py`

**Interfaces:**
- Produces `EvidenceCurrentness`, `EvidenceRef`, `FeasibilityState`, `FeasibilityAssessment`.
- `EvidenceRef` binds producer/source/subject/currentness; it does not create authority.
- `FeasibilityAssessment` keeps FEASIBLE, INFEASIBLE, UNKNOWN and CONDITIONAL distinct and optionally carries success expectation, uncertainty, controllability and delay.

- [ ] **Step 1: Add the focused failing tests**
  - Public exports exist.
  - UNKNOWN is distinct from INFEASIBLE.
  - Blank producer/source/subject IDs fail.
  - Probability-like values are bounded 0..1.
  - Negative delay fails.
  - STALE/UNKNOWN evidence is representable and is not coerced to a zero value.

- [ ] **Step 2: Verify the relevant failure**
  Run: `python -m pytest -q tests/test_next_core_evidence.py`
  Expected: assertion failures proving the public evidence/feasibility interfaces are absent, with no import/setup error.

- [ ] **Step 3: Implement the minimum behavior**
  Use frozen, slotted dataclasses and enums consistent with the existing repository. Do not add TTL logic; currentness is an explicit producer-supplied state in this tranche.

- [ ] **Step 4: Verify the focused pass**
  Run the identical focused command.
  Expected: all evidence/feasibility tests pass.

- [ ] **Step 5: Run the affected integration check**
  Run: `python -m pytest -q`
  Expected: prior suite plus new tests pass.

- [ ] **Step 6: Commit the passing deliverable**
  Commit message: `feat: add verified feasibility evidence primitives`

### Task 2: Separate effort semantics and type learning outcomes

**Files:**
- Create: `src/meso_crct/effort.py`
- Create: `src/meso_crct/outcomes.py`
- Modify: `src/meso_crct/plasticity.py`
- Modify: `src/meso_crct/__init__.py`
- Test: `tests/test_next_core_effort_outcomes.py`

**Interfaces:**
- Produces `EffortAssessment` with independently represented `required_effort`, `effort_cost`, `willingness_to_exert`, optional `vigor_proposal`, plus `EvidenceRef`.
- Produces `OutcomeClass`.
- Extends `PlasticityCandidate` and `propose_plasticity` with `outcome_class`, defaulting to `OTHER` for V2 compatibility.

- [ ] **Step 1: Add the focused failing tests**
  - Effort cost and willingness can differ.
  - Required effort can remain constant while current cost differs.
  - Vigor may be absent and does not create execution authority.
  - Same signed prediction error can yield candidates with different `OutcomeClass`.
  - Existing callers with no outcome class receive `OutcomeClass.OTHER`.

- [ ] **Step 2: Verify the relevant failure**
  Run: `python -m pytest -q tests/test_next_core_effort_outcomes.py`
  Expected: missing-interface assertion failures, not setup errors.

- [ ] **Step 3: Implement the minimum behavior**
  Keep effort numbers local normalized assessments; they are not global utility. Outcome class changes metadata only; do not alter the V2 delta formula in this tranche.

- [ ] **Step 4: Verify the focused pass**
  Run identical focused command.
  Expected: all tests pass.

- [ ] **Step 5: Run the affected integration check**
  Run: `python -m pytest -q`
  Expected: full suite passes with existing plasticity behavior unchanged.

- [ ] **Step 6: Commit the passing deliverable**
  Commit message: `feat: separate effort and learning outcome semantics`

### Task 3: Add domain contribution and selection-policy provenance

**Files:**
- Create: `src/meso_crct/domain.py`
- Modify: `src/meso_crct/selection.py`
- Modify: `src/meso_crct/__init__.py`
- Test: `tests/test_next_core_domain_policy.py`

**Interfaces:**
- Produces `DomainContribution` carrying profile/domain identity, profile revision, target, contribution kind, local magnitude, optional direction, and `EvidenceRef`.
- Extends `SelectionPolicy` with `policy_id` and `policy_revision`.
- Extends `SelectionResult` to report the exact policy identity/revision used.
- Keeps the existing nonprotective precedence behavior unchanged.

- [ ] **Step 1: Add the focused failing tests**
  - Domain contribution requires nonempty domain/profile revision/target/kind.
  - Domain contribution has local `magnitude` but no `priority` field.
  - Default selection reports `legacy-v2` policy identity.
  - Custom policy identity/revision is echoed in `SelectionResult`.
  - Existing weak/strong mode-precedence behavior remains unchanged under the legacy policy.

- [ ] **Step 2: Verify the relevant failure**
  Run: `python -m pytest -q tests/test_next_core_domain_policy.py`
  Expected: missing-interface/provenance assertion failures, not a changed arbitration result.

- [ ] **Step 3: Implement the minimum behavior**
  Do not make `DomainContribution` participate in `select_target` yet. Policy provenance is observational metadata only in this tranche.

- [ ] **Step 4: Verify the focused pass**
  Run identical focused command.
  Expected: all tests pass.

- [ ] **Step 5: Run the affected integration check**
  Run: `python -m pytest -q`
  Expected: all tests pass; legacy selection semantics unchanged.

- [ ] **Step 6: Commit the passing deliverable**
  Commit message: `feat: expose domain and selection policy provenance`

## Unresolved externally observable decisions

The following remain outside this tranche and therefore do not block it:
- the replacement cross-domain selection algorithm;
- coalition aggregation / dimension-stuffing policy;
- goal/plan reference schema and goal-share accounting;
- whether action vigor is ultimately stored by MESO or only proposed to the host;
- whether habit proposals are integrated at MESO selection or a later host action-policy layer.
