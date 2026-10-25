"""Reject coerced numbers at public synthetic-state and policy boundaries."""

from datetime import datetime, timezone

import pytest

from meso_crct.allocation import AllocationSample, GoalObligation
from meso_crct.control import ControlPolicy
from meso_crct.dynamics import DynamicsConfig, decay_toward
from meso_crct.evaluation_env import derive_epistemic_value
from meso_crct.homeostasis import HomeostaticState, NeedAffordance, NeedAxis, modulate_incentive_salience
from meso_crct.intent import IntentPolicy
from meso_crct.need_observation import NeedObservation
from meso_crct.plasticity import PlasticityPolicy
from meso_crct.provenance import Provenance, SourceKind
from meso_crct.recall_resolution import RecallResolutionPolicy
from meso_crct.recruitment import RecruitmentPolicy
from meso_crct.semantic import SemanticEvidence
from meso_crct.salience import LearningState, RecruitmentState, SalienceState
from meso_crct.state import RewardState
from meso_crct.tendency import ActionTendencyPolicy


FACTORIES = (
    lambda value: RewardState.from_external(pleasure=value),
    lambda value: RewardState.from_external(hazard=value),
    lambda value: RewardState.from_external(avoidance=value),
    lambda value: SalienceState(incentive_salience=value),
    lambda value: LearningState(prediction_error=value),
    lambda value: RecruitmentState(activation=value),
    lambda value: NeedAxis("rest", setpoint=value, current_level=0.5),
    lambda value: NeedAffordance("rest", corrective_strength=value),
    lambda value: NeedObservation(
        event_id="synthetic", need_id="rest", measured_level=value,
        observed_at=datetime(2026, 10, 25, tzinfo=timezone.utc),
        provenance=Provenance(SourceKind.ENVIRONMENT, "sensor", "v1"),
        evidence_ref="synthetic",
    ),
    lambda value: modulate_incentive_salience(
        base_incentive=value, homeostasis=HomeostaticState(), affordances=()
    ),
    lambda value: SemanticEvidence(context_relevance=value),
    lambda value: DynamicsConfig(
        hedonic_half_life_seconds=value,
        salience_half_life_seconds=1.0,
        learning_half_life_seconds=1.0,
        satiation_half_life_seconds=1.0,
        recruitment_half_life_seconds=1.0,
    ),
    lambda value: decay_toward(0.5, baseline=0.0, elapsed_seconds=value, half_life_seconds=1.0),
    lambda value: RecruitmentPolicy(persistence_retention=value),
    lambda value: PlasticityPolicy(maximum_absolute_delta=value, minimum_salience_gate=0.0),
    lambda value: IntentPolicy(minimum_committed_strength=value),
    lambda value: ActionTendencyPolicy(minimum_recall_directional_support=value),
    lambda value: RecallResolutionPolicy(conflict_margin=value),
    lambda value: GoalObligation("goal", minimum_nonprotective_share=value),
    lambda value: AllocationSample("target", priority=value, dominant_driver=None),
    lambda value: ControlPolicy(crowdout_fraction=value),
    lambda value: derive_epistemic_value(novelty=value, learning_progress=1.0),
)


@pytest.mark.parametrize("factory", FACTORIES)
@pytest.mark.parametrize(
    "invalid", (True, False, "0.5", None, 10**10000),
    ids=("true", "false", "numeric-string", "null", "oversized-int"),
)
def test_numeric_boundaries_reject_bools_strings_nulls_and_oversized_ints(factory, invalid):
    with pytest.raises(ValueError, match="finite|numeric|number"):
        factory(invalid)


def test_finite_numeric_inputs_still_use_existing_clamps_and_bounds():
    assert RewardState.from_external(pleasure=12).pleasure == 10.0
    assert RewardState.from_external(pleasure=-1).pleasure == -0.1
    assert RewardState.from_external(hazard=3).hazard == 1.0
    assert SalienceState(incentive_salience=3).incentive_salience == 1.0
    assert SalienceState(incentive_salience=-2).incentive_salience == 0.0
    assert NeedAxis("rest", setpoint=2, current_level=0).setpoint == 1.0
    assert IntentPolicy(minimum_committed_strength=2).minimum_committed_strength == 1.0
    assert decay_toward(1, baseline=0, elapsed_seconds=1, half_life_seconds=1) == 0.5


@pytest.mark.parametrize("invalid", ("false", 0, 1, None))
def test_semantic_importance_claim_requires_actual_boolean(invalid):
    with pytest.raises(ValueError, match="source_asserts_importance"):
        SemanticEvidence(source_asserts_importance=invalid)


def test_semantic_importance_boolean_remains_untrusted_evidence():
    from meso_crct.semantic import assess_semantic_relevance

    assessment = assess_semantic_relevance(SemanticEvidence(source_asserts_importance=True))
    assert assessment.relevance == 0.0
    assert assessment.untrusted_importance_claim is True
