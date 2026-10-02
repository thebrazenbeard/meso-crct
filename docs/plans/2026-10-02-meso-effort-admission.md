# MESO Effort Admission Implementation Plan

> **For agentic workers:** Use the host's task-by-task TDD workflow.

**Goal:** Make common effort appraisals provenance/currentness-qualified before they can later enter cross-family comparison.

**Base:** Draft PR #14 head 63278d38560b2c9835b5ec66db30f7e254df8d4b.

## Architecture

Keep EffortAssessment as the local semantic object separating:
- required_effort
- effort_cost
- willingness_to_exert
- optional vigor_proposal

Add a separate admission layer:
- EffortProducerSpec
- EffortAdmissionPolicy
- AdmittedEffortAssessment
- admit_effort_assessment()

The admission policy is supplied externally and binds exact producer ID/revision. Admission requires CURRENT evidence and preserves a deterministic digest over the exact assessment + policy.

## Constraints

- EffortAssessment.evidence.subject_id must equal target_id.
- STALE/UNKNOWN evidence cannot be admitted.
- Producer identity/revision is exact.
- Assessment cannot self-authorize.
- Admission does not imply execution authority or consent.
- Vigor remains a proposal, not execution.
- No cross-family projection in this tranche.
- Existing EffortAssessment callers remain compatible apart from rejecting subject mismatch.
- No modification to V2 selection.

## Red cases

- subject mismatch rejected;
- current trusted assessment admitted;
- stale/unknown currentness rejected;
- spoofed producer rejected;
- wrong producer revision rejected;
- duplicate producer specs rejected;
- policy argument required;
- admitted assessment preserves original values and evidence;
- exact policy ID/revision retained;
- deterministic admission digest changes with assessment/policy changes;
- no action_authority/consent/can_execute fields;
- legacy direct EffortAssessment construction otherwise unchanged.

## Verification

- focused tests pass;
- full suite passes;
- compileall passes;
- git diff --check passes.

## Out of scope

- mapping effort fields into comparison families;
- effort normalization from physical units;
- resource telemetry;
- action vigor execution;
- merge/runtime activation.
