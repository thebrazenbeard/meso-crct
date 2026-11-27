import pytest

from meso_crct import (
    AppraisedTarget,
    HomeostaticState,
    NeedAffordance,
    NeedAxis,
    RewardState,
    SemanticEvidence,
    TargetAppraisalInput,
    build_target_appraisal,
)


def test_self_asserted_importance_does_not_enter_semantic_relevance():
    appraised = build_target_appraisal(
        TargetAppraisalInput(
            target_id="claim",
            semantic_evidence=SemanticEvidence(
                source_asserts_importance=True,
            ),
        )
    )
    assert appraised.state.salience.semantic_relevance == 0.0
    assert appraised.semantic.untrusted_importance_claim


def test_grounded_semantic_relation_enters_salience():
    appraised = build_target_appraisal(
        TargetAppraisalInput(
            target_id="goal-related",
            semantic_evidence=SemanticEvidence(goal_relevance=0.8),
        )
    )
    assert appraised.state.salience.semantic_relevance == 0.8
    assert appraised.semantic.grounded_drivers == ("goal_relevance",)


def test_novelty_without_learning_progress_does_not_create_epistemic_priority():
    appraised = build_target_appraisal(
        TargetAppraisalInput(
            target_id="noise",
            novelty=1.0,
            learning_progress=0.0,
        )
    )
    assert appraised.state.learning.novelty == 1.0
    assert appraised.state.salience.epistemic_value == 0.0


def test_homeostatic_deficit_can_raise_incentive_without_pleasure():
    appraised = build_target_appraisal(
        TargetAppraisalInput(
            target_id="resource",
            base_incentive_salience=0.2,
            reward=RewardState(pleasure=0.0),
            homeostasis=HomeostaticState(
                axes=(
                    NeedAxis(
                        "energy",
                        setpoint=0.8,
                        current_level=0.2,
                    ),
                )
            ),
            affordances=(
                NeedAffordance(
                    "energy",
                    corrective_strength=1.0,
                ),
            ),
        )
    )
    assert appraised.state.salience.incentive_salience > 0.2
    assert appraised.state.reward.pleasure == 0.0
    assert appraised.homeostatic.dominant_need == "energy"


def test_maximum_pleasure_does_not_manufacture_other_salience():
    appraised = build_target_appraisal(
        TargetAppraisalInput(
            target_id="pleasant",
            reward=RewardState(pleasure=10.0),
        )
    )
    assert appraised.state.salience.perceptual_salience == 0.0
    assert appraised.state.salience.semantic_relevance == 0.0
    assert appraised.state.salience.motivational_salience == 0.0
    assert appraised.state.salience.incentive_salience == 0.0
    assert appraised.state.salience.epistemic_value == 0.0


def test_attentional_priority_is_always_downstream_zero_at_appraisal():
    appraised = build_target_appraisal(
        TargetAppraisalInput(
            target_id="important",
            semantic_evidence=SemanticEvidence(context_relevance=1.0),
            perceptual_salience=1.0,
            base_motivational_salience=1.0,
        )
    )
    assert appraised.state.salience.attentional_priority == 0.0


def test_appraised_target_converts_to_selection_target_without_mutation():
    appraised = build_target_appraisal(
        TargetAppraisalInput(
            target_id="candidate",
            semantic_evidence=SemanticEvidence(context_relevance=0.7),
        )
    )
    target = appraised.as_target_state()
    assert target.target_id == "candidate"
    assert target.state == appraised.state


def test_empty_target_id_fails():
    with pytest.raises(ValueError):
        TargetAppraisalInput(target_id="   ")


def test_appraised_target_direct_construction_is_blocked():
    genuine = build_target_appraisal(
        TargetAppraisalInput(target_id="genuine")
    )
    with pytest.raises(TypeError):
        AppraisedTarget(
            target_id="fake",
            state=genuine.state,
            semantic=genuine.semantic,
            homeostatic=genuine.homeostatic,
        )


def test_explicit_exploration_is_optional_without_learning_progress():
    from meso_crct import DecisionCycleState, run_decision_cycle
    spec = TargetAppraisalInput("poetry", novelty=0.0, learning_progress=0.0)
    def cycle(spec):
        return run_decision_cycle(DecisionCycleState(), [build_target_appraisal(spec)])[1]
    from dataclasses import replace
    # Missing optional support must be a behavioral failure on the old API.
    if "exploration_requested" not in spec.__dataclass_fields__:
        pytest.fail("explicit exploration request has no representation")
    requested = replace(spec, exploration_requested=True)
    app = build_target_appraisal(requested)
    result = cycle(requested)
    assert app.state.salience.epistemic_value == 0.0
    assert app.state.learning.learning_progress == 0.0
    assert result.intent.kind.value == "inspect"
    assert result.intent.source == "exploration_requested"
    assert not result.intent.effect_authorized and not result.intent.can_execute
    assert cycle(spec).intent.kind.value == "hold"
    assert cycle(replace(requested, exploration_requested=False)).intent.kind.value == "hold"
    assert cycle(replace(requested, reward=RewardState(hazard=1.0))).intent.kind.value == "withdraw"


def test_exploration_request_is_typed_and_legacy_state_fingerprint_is_stable():
    import json, hashlib
    from dataclasses import asdict, replace
    from meso_crct import state_fingerprint
    spec = TargetAppraisalInput("poetry")
    if "exploration_requested" not in spec.__dataclass_fields__:
        pytest.fail("explicit exploration request has no representation")
    with pytest.raises((TypeError, ValueError)):
        build_target_appraisal(replace(spec, exploration_requested=1))
    legacy = build_target_appraisal(spec).state
    payload = asdict(legacy)
    payload["salience"].pop("exploration_requested", None)
    expected = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert state_fingerprint(legacy) == expected
    requested = build_target_appraisal(replace(spec, exploration_requested=True)).state
    assert state_fingerprint(requested) != expected
