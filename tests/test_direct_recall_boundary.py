"""Direct API contract, independent of the multi-recall resolver."""
import pytest
from test_tendency import recall_for
from meso_crct import (
    ActionTendencyPolicy, CircuitState, IntentPolicy, SalienceState,
    TargetState, derive_action_tendency, propose_action_intent, select_target,
)

@pytest.mark.parametrize("error,match,kind,strength,intent_kind", [
    (0.8, 0.0, "uncommitted", 0.8, "hold"),
    (0.8, 1.0, "approach", 0.8, "approach"),
    (-0.8, 1.0, "learned_withdraw", 0.8, "withdraw"),
])
def test_direct_recall_requires_actual_directional_support(error,match,kind,strength,intent_kind):
    recall = recall_for(prediction_error=error, cue_match=match)
    selected = select_target([TargetState("target", CircuitState(
        salience=SalienceState(motivational_salience=0.8)))])
    result = derive_action_tendency(selected, recall=recall, recall_target_id="target",
        policy=ActionTendencyPolicy(minimum_recall_directional_support=0.0))
    assert result.kind.value == kind
    assert result.strength == pytest.approx(strength)
    intent = propose_action_intent(result, policy=IntentPolicy(minimum_committed_strength=0.0))
    assert intent.kind.value == intent_kind
    assert not intent.effect_authorized and not intent.can_execute
