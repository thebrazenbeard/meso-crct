import pytest
from meso_crct.allocation import AllocationWindow, AllocationSample, GoalObligation

@pytest.mark.parametrize("value",[True, 0.5, "1", None])
def test_allocation_cycle_counter_requires_integral_value(value):
    with pytest.raises(ValueError,match="no_selection_cycles"):
        AllocationWindow(no_selection_cycles=value)

def test_protective_flag_cannot_be_truthy_string():
    with pytest.raises(ValueError,match="protective"):
        AllocationSample(target_id="goal", priority=0.5, dominant_driver=None, protective="false")

def test_goal_identifier_must_be_text():
    with pytest.raises(ValueError,match="goal_id"):
        GoalObligation(goal_id=123)
