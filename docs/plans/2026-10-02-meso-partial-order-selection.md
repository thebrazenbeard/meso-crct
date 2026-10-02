# MESO Partial-Order Selection Implementation Plan

> **For agentic workers:** Use the host's task-by-task TDD workflow.

**Goal:** Add a conservative partial-order selector over normalized semantic-family views without scalarizing across families or replacing hard protection/authority gates.

**Architecture:** Consume ContributionFamilyView objects from the semantic-family normalizer. A PartialOrderPolicy declares a small set of globally comparable family directions. The selector computes strict Pareto dominance among complete candidates, returns a unique winner only when one non-dominated complete target remains and no incomplete target could invalidate the comparison, otherwise returns an explicit incomparable frontier.

**Base:** combined Draft #11 + Draft #9 code at babb8b5418da0180705f6c2dd51d82bebd9a6772.

## Constraints

- Do not modify current V2 select_target() or its fixed precedence.
- Do not sum family magnitudes.
- Do not introduce weights.
- Do not infer family direction from sign or family name.
- Family direction is explicit policy metadata: BENEFIT, COST, CONTEXT_ONLY.
- CONTEXT_ONLY never participates in dominance.
- Missing required comparable evidence must not be imputed.
- Equal vectors do not create a winner.
- Duplicate target/family views are rejected.
- Duplicate policy family specs are rejected.
- The result carries exact policy ID/revision.
- This module assumes hard admissibility/protection/authority filtering occurred before it; it does not grant or infer authority.
- No fallback policy in this tranche.

### Task 1: Partial-order frontier and unique dominance

**Files:**
- Create: src/meso_crct/partial_order.py
- Modify: src/meso_crct/__init__.py
- Test: tests/test_partial_order_selection.py

**Public interfaces:**
- FamilyDirection
- FamilyComparisonSpec
- PartialOrderPolicy
- PartialOrderStatus
- PartialOrderSelectionResult
- select_by_partial_order

**Red cases:**
- Obvious benefit dominance selects the unique winner.
- COST direction reverses numeric preference correctly.
- Genuine tradeoff returns INCOMPARABLE with both targets on the frontier.
- Equal vectors return INCOMPARABLE.
- Missing required family returns INCOMPARABLE and records incomplete targets; no zero imputation.
- CONTEXT_ONLY difference does not establish dominance.
- Duplicate target/family views are rejected.
- Duplicate policy family specs are rejected.
- Empty candidate set returns NO_ADMISSIBLE_CANDIDATE.
- One complete candidate selects.
- One incomplete candidate remains INCOMPARABLE.
- Exact policy identity/revision is preserved in the result.
- Legacy V2 select_target() behavior remains unchanged.

**Verification:**
- Focused test module passes.
- Full suite passes.
- git diff --check passes.
- compileall passes.

**Out of scope:**
- protection/authority filtering;
- feasibility admission;
- obligation-pressure derivation;
- fallback/tie-breaking;
- time/resource allocation across frontier;
- runtime activation or merge.
