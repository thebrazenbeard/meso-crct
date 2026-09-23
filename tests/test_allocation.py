from meso_crct import (
    AllocationSample,
    GoalObligation,
    audit_attention_budget,
)


def test_balanced_goal_allocation_passes():
    samples = [
        AllocationSample("goal:a", 0.8, "semantic_relevance"),
        AllocationSample("goal:b", 0.7, "epistemic_value"),
        AllocationSample("goal:a", 0.8, "semantic_relevance"),
        AllocationSample("goal:b", 0.7, "epistemic_value"),
    ]
    obligations = [
        GoalObligation("goal:a", 0.25),
        GoalObligation("goal:b", 0.25),
    ]
    audit = audit_attention_budget(samples, obligations)
    assert audit.passed
    assert audit.dominant_fraction == 0.5


def test_narrow_target_crowdout_is_flagged():
    samples = [
        AllocationSample("target:loop", 1.0, "incentive_salience")
        for _ in range(9)
    ] + [
        AllocationSample("goal:maintenance", 0.4, "semantic_relevance")
    ]
    obligations = [GoalObligation("goal:maintenance", 0.20)]
    audit = audit_attention_budget(samples, obligations)
    assert "goal_neglect" in audit.flags
    assert "target_crowd_out" in audit.flags
    assert "incentive_capture" in audit.flags
    assert audit.neglected_goals == ("goal:maintenance",)


def test_protective_emergency_does_not_count_as_ordinary_crowdout():
    samples = [
        AllocationSample(
            "hazard:fire",
            1.0,
            "hazard",
            protective=True,
        )
        for _ in range(20)
    ]
    obligations = [GoalObligation("goal:maintenance", 0.20)]
    audit = audit_attention_budget(samples, obligations)
    assert audit.passed
    assert audit.protective_samples == 20
    assert audit.nonprotective_samples == 0


def test_goal_threshold_is_user_supplied_not_equal_share_assumption():
    samples = [
        AllocationSample("goal:primary", 0.9, "semantic_relevance")
        for _ in range(8)
    ] + [
        AllocationSample("goal:background", 0.4, "semantic_relevance")
        for _ in range(2)
    ]
    obligations = [GoalObligation("goal:background", 0.10)]
    audit = audit_attention_budget(samples, obligations)
    assert "goal_neglect" not in audit.flags
