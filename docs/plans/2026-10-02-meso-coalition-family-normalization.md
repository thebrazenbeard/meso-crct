# MESO Coalition Family Normalization Implementation Plan

> **For agentic workers:** Use the host's available task-by-task implementation workflow. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a standalone, registered semantic-family normalization layer that prevents domain contribution dimension stuffing without changing cross-domain winner selection.

**Architecture:** Keep `DomainContribution` as the profile-local envelope from PR #8. Add an external registry that maps qualified `(domain, profile revision, contribution kind)` triples to semantic families, then normalize current contributions by `(target, family)` using strongest-per-family magnitude while preserving support metadata. The normalizer produces no global score and does not call or modify `select_target`.

**Tech Stack:** Python 3, frozen dataclasses, pytest.

## Global Constraints

- Base is Draft PR #8 head `0db07691b277f75185d76b8810869765bc2543e7`.
- Do not modify V2 arbitration or selection precedence.
- TDD red must be observed before production changes.
- Unregistered contribution kinds are rejected.
- STALE/UNKNOWN contribution evidence is inadmissible to this normalizer.
- Contributions are grouped by semantic family and target.
- Same-family magnitudes use `max`, never sum.
- Support count/source metadata is observational and never converted into extra magnitude.
- Cross-family aggregation/selection remains unresolved and out of scope.

---

### Task 1: Registered family normalization

**Files:**
- Create: `src/meso_crct/domain_aggregation.py`
- Modify: `src/meso_crct/__init__.py`
- Test: `tests/test_domain_aggregation.py`

**Interfaces:**
- Produces `ContributionKindSpec`, `ContributionRegistry`, `ContributionFamilyView`, `UnknownContributionKind`, `InadmissibleContributionEvidence`, and `aggregate_domain_contributions`.
- Consumes PR #8 `DomainContribution`, `EvidenceCurrentness`.

- [ ] **Step 1: Add focused failing tests**
  - Duplicate/alias contributions mapped to one family normalize to the maximum magnitude, not the sum.
  - Distinct semantic families remain distinct.
  - Same family on different targets remains distinct.
  - Unregistered contribution kind raises `UnknownContributionKind`.
  - STALE/UNKNOWN evidence raises `InadmissibleContributionEvidence`.
  - Duplicate registry keys fail construction.
  - Family view exposes support/source metadata but no global `priority`.

- [ ] **Step 2: Verify the relevant failure**
  Run: `python -m pytest -q tests/test_domain_aggregation.py`
  Expected: assertion failures for absent public interfaces; no import/setup error.

- [ ] **Step 3: Implement minimum behavior**
  - Registry ownership is external to profiles.
  - Exact registry key is `(domain_id, profile_revision, contribution_kind)`.
  - Group key is `(target_id, family_id)`.
  - Family magnitude is maximum current registered contribution magnitude.
  - `support_count`, `contribution_kinds`, and `source_ids` are preserved as metadata.

- [ ] **Step 4: Verify focused pass**
  Run identical focused command.
  Expected: all normalization tests pass.

- [ ] **Step 5: Run integration suite**
  Run: `python -m pytest -q`
  Expected: PR #8 suite plus new tests pass; legacy selection behavior unchanged.

- [ ] **Step 6: Commit**
  Commit message: `feat: normalize domain contributions by semantic family`

## Unresolved externally observable decisions

- How normalized family vectors compare across targets.
- Whether independent corroborating sources eventually change confidence and by what rule.
- Which semantic families become globally registered in a future arbitration policy.
- Whether partial incomparability returns an explicit result or always invokes a configured fallback.
