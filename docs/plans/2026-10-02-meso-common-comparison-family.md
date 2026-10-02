# MESO Common Comparison-Family Implementation Plan

> **For agentic workers:** Use the host's task-by-task TDD workflow.

**Goal:** Introduce a neutral, provenance-digest-bound family view so domain aggregates and admitted common appraisals can enter the same partial-order selector without pretending common appraisals are domain contributions.

**Base:** Draft PR #15 head b27a8f22f0fa29084bfb811c7f0704b2039e108f.

## Architecture

Create a constructor-gated ComparisonFamilyView carrying:
- target_id
- family_id
- magnitude
- source_kind
- source_digest

Adapters:
1. comparison_family_from_domain(ContributionFamilyView)
2. comparison_families_from_effort(AdmittedEffortAssessment, fields=...)

EffortComparisonField is intentionally limited to:
- REQUIRED_EFFORT
- EFFORT_COST
- WILLINGNESS_TO_EXERT

VIGOR_PROPOSAL is intentionally excluded because vigor is post-selection/execution-adjacent.

Partial-order selection will canonicalize both:
- new ComparisonFamilyView inputs; and
- legacy ContributionFamilyView inputs via the domain adapter.

This preserves existing Drafts while establishing the neutral future interface.

## Constraints

- Direct ComparisonFamilyView construction without the module token is rejected.
- All magnitudes remain finite [0,1].
- Domain adapter digest binds the exact domain-family aggregate content.
- Effort adapter accepts only AdmittedEffortAssessment, not raw EffortAssessment.
- Effort adapter digest binds the exact admission digest + selected field + projected value.
- No cross-source fusion.
- No automatic family direction.
- No global priority.
- No vigor projection.
- Legacy ContributionFamilyView input produces the same canonical selection digest as its generic domain projection.
- Feasibility wrapper remains compatible.
- No change to V2 select_target().

## Red cases

- direct generic-view construction rejected;
- domain adapter preserves target/family/magnitude and sets DOMAIN_AGGREGATE source;
- domain source digest changes when aggregate content changes;
- admitted effort projects EFFORT_COST correctly;
- raw effort projection rejected;
- effort enum has no vigor member;
- effort source digest changes with admission digest/field/value;
- selector accepts generic comparison views;
- legacy domain view and generic domain projection produce same selection result/input digest;
- selector combines domain generic family + effort generic family without scalar summation;
- duplicate target/family across mixed source types rejected;
- feasibility wrapper accepts generic comparison views;
- legacy V2 selection remains unchanged.

## Verification

- focused tests pass;
- full suite passes;
- compileall passes;
- git diff --check passes.

## Out of scope

- resource-state projection;
- obligation-pressure projection;
- family fusion when multiple source kinds target the same family;
- fallback selection;
- merge/runtime activation.
