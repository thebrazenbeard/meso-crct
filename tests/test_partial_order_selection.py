import pytest

import meso_crct as m


def public(name: str):
    assert hasattr(m, name), f"missing public partial-order interface: {name}"
    return getattr(m, name)


def view(target_id: str, family_id: str, magnitude: float):
    ContributionFamilyView = public("ContributionFamilyView")
    return ContributionFamilyView(
        target_id=target_id,
        family_id=family_id,
        magnitude=magnitude,
        support_count=1,
        contribution_kinds=(family_id,),
        source_ids=(f"src:{target_id}:{family_id}",),
    )


def spec(family_id: str, direction_name: str):
    FamilyComparisonSpec = public("FamilyComparisonSpec")
    FamilyDirection = public("FamilyDirection")
    return FamilyComparisonSpec(
        family_id=family_id,
        direction=getattr(FamilyDirection, direction_name),
    )


def policy(*specs):
    PartialOrderPolicy = public("PartialOrderPolicy")
    return PartialOrderPolicy(
        policy_id="policy:test",
        policy_revision="r1",
        families=tuple(specs),
    )


def select(candidates, views, policy_obj):
    fn = public("select_by_partial_order")
    return fn(
        candidate_target_ids=tuple(candidates),
        family_views=tuple(views),
        policy=policy_obj,
    )


def test_obvious_benefit_dominance_selects_unique_winner():
    PartialOrderStatus = public("PartialOrderStatus")
    result = select(
        ("a", "b"),
        (
            view("a", "epistemic", 0.9),
            view("a", "motivation", 0.8),
            view("b", "epistemic", 0.6),
            view("b", "motivation", 0.8),
        ),
        policy(
            spec("epistemic", "BENEFIT"),
            spec("motivation", "BENEFIT"),
        ),
    )
    assert result.status is PartialOrderStatus.SELECTED
    assert result.selected_target_id == "a"
    assert result.frontier_target_ids == ("a",)
    assert result.dominated_target_ids == ("b",)


def test_cost_direction_prefers_lower_value():
    PartialOrderStatus = public("PartialOrderStatus")
    result = select(
        ("a", "b"),
        (
            view("a", "motivation", 0.8),
            view("a", "effort_cost", 0.2),
            view("b", "motivation", 0.8),
            view("b", "effort_cost", 0.7),
        ),
        policy(
            spec("motivation", "BENEFIT"),
            spec("effort_cost", "COST"),
        ),
    )
    assert result.status is PartialOrderStatus.SELECTED
    assert result.selected_target_id == "a"


def test_genuine_tradeoff_returns_incomparable_frontier():
    PartialOrderStatus = public("PartialOrderStatus")
    result = select(
        ("a", "b"),
        (
            view("a", "epistemic", 0.9),
            view("a", "effort_cost", 0.8),
            view("b", "epistemic", 0.6),
            view("b", "effort_cost", 0.2),
        ),
        policy(
            spec("epistemic", "BENEFIT"),
            spec("effort_cost", "COST"),
        ),
    )
    assert result.status is PartialOrderStatus.INCOMPARABLE
    assert result.selected_target_id is None
    assert set(result.frontier_target_ids) == {"a", "b"}
    assert result.dominated_target_ids == ()


def test_equal_vectors_do_not_invent_a_winner():
    PartialOrderStatus = public("PartialOrderStatus")
    result = select(
        ("a", "b"),
        (
            view("a", "epistemic", 0.8),
            view("b", "epistemic", 0.8),
        ),
        policy(spec("epistemic", "BENEFIT")),
    )
    assert result.status is PartialOrderStatus.INCOMPARABLE
    assert set(result.frontier_target_ids) == {"a", "b"}


def test_missing_required_family_is_incomplete_not_zero():
    PartialOrderStatus = public("PartialOrderStatus")
    result = select(
        ("a", "b"),
        (
            view("a", "epistemic", 1.0),
            view("a", "effort_cost", 0.1),
            view("b", "epistemic", 0.2),
        ),
        policy(
            spec("epistemic", "BENEFIT"),
            spec("effort_cost", "COST"),
        ),
    )
    assert result.status is PartialOrderStatus.INCOMPARABLE
    assert result.selected_target_id is None
    assert result.incomplete_target_ids == ("b",)
    assert "b" in result.frontier_target_ids


def test_context_only_family_does_not_establish_dominance():
    PartialOrderStatus = public("PartialOrderStatus")
    result = select(
        ("a", "b"),
        (
            view("a", "epistemic", 0.8),
            view("b", "epistemic", 0.8),
            view("a", "attachment", 1.0),
            view("b", "attachment", 0.0),
        ),
        policy(
            spec("epistemic", "BENEFIT"),
            spec("attachment", "CONTEXT_ONLY"),
        ),
    )
    assert result.status is PartialOrderStatus.INCOMPARABLE
    assert set(result.frontier_target_ids) == {"a", "b"}


def test_duplicate_target_family_views_are_rejected():
    with pytest.raises(ValueError):
        select(
            ("a",),
            (
                view("a", "epistemic", 0.7),
                view("a", "epistemic", 0.8),
            ),
            policy(spec("epistemic", "BENEFIT")),
        )


def test_duplicate_policy_family_specs_are_rejected():
    PartialOrderPolicy = public("PartialOrderPolicy")
    with pytest.raises(ValueError):
        PartialOrderPolicy(
            policy_id="policy:test",
            policy_revision="r1",
            families=(
                spec("epistemic", "BENEFIT"),
                spec("epistemic", "COST"),
            ),
        )


def test_empty_candidate_set_is_explicit():
    PartialOrderStatus = public("PartialOrderStatus")
    result = select(
        (),
        (),
        policy(spec("epistemic", "BENEFIT")),
    )
    assert result.status is PartialOrderStatus.NO_ADMISSIBLE_CANDIDATE
    assert result.selected_target_id is None
    assert result.frontier_target_ids == ()


def test_one_complete_candidate_selects():
    PartialOrderStatus = public("PartialOrderStatus")
    result = select(
        ("a",),
        (view("a", "epistemic", 0.8),),
        policy(spec("epistemic", "BENEFIT")),
    )
    assert result.status is PartialOrderStatus.SELECTED
    assert result.selected_target_id == "a"


def test_one_incomplete_candidate_remains_incomparable():
    PartialOrderStatus = public("PartialOrderStatus")
    result = select(
        ("a",),
        (),
        policy(spec("epistemic", "BENEFIT")),
    )
    assert result.status is PartialOrderStatus.INCOMPARABLE
    assert result.selected_target_id is None
    assert result.frontier_target_ids == ("a",)
    assert result.incomplete_target_ids == ("a",)


def test_result_preserves_exact_policy_identity():
    result = select(
        ("a",),
        (view("a", "epistemic", 0.8),),
        policy(spec("epistemic", "BENEFIT")),
    )
    assert result.policy_id == "policy:test"
    assert result.policy_revision == "r1"


def test_legacy_v2_selection_behavior_is_unchanged():
    result = m.select_target(
        [
            m.TargetState(
                "learn",
                m.CircuitState(
                    salience=m.SalienceState(epistemic_value=1.0),
                ),
            ),
            m.TargetState(
                "pursue",
                m.CircuitState(
                    salience=m.SalienceState(motivational_salience=0.21),
                ),
            ),
        ]
    )
    assert result.selected_target_id == "pursue"
    assert result.policy_id == "legacy-v2"


def test_result_digest_binds_exact_inputs_and_is_order_stable():
    policy_a = policy(
        spec("epistemic", "BENEFIT"),
        spec("effort_cost", "COST"),
    )
    views_a = (
        view("a", "epistemic", 0.9),
        view("a", "effort_cost", 0.2),
        view("b", "epistemic", 0.7),
        view("b", "effort_cost", 0.4),
    )

    first = select(("a", "b"), views_a, policy_a)
    reordered = select(
        ("b", "a"),
        tuple(reversed(views_a)),
        policy_a,
    )
    changed_value = select(
        ("a", "b"),
        (
            view("a", "epistemic", 0.8),
            view("a", "effort_cost", 0.2),
            view("b", "epistemic", 0.7),
            view("b", "effort_cost", 0.4),
        ),
        policy_a,
    )
    changed_policy = select(
        ("a", "b"),
        views_a,
        m.PartialOrderPolicy(
            policy_id="policy:test",
            policy_revision="r2",
            families=policy_a.families,
        ),
    )

    assert hasattr(first, "decision_input_digest")
    assert first.decision_input_digest == reordered.decision_input_digest
    assert first.decision_input_digest != changed_value.decision_input_digest
    assert first.decision_input_digest != changed_policy.decision_input_digest


@pytest.mark.parametrize("magnitude", [-0.1, 1.1, float("nan"), float("inf")])
def test_selector_rejects_invalid_family_magnitude(magnitude):
    with pytest.raises(ValueError):
        select(
            ("a",),
            (view("a", "epistemic", magnitude),),
            policy(spec("epistemic", "BENEFIT")),
        )


def test_selector_rejects_blank_family_id():
    with pytest.raises(ValueError):
        select(
            ("a",),
            (view("a", "   ", 0.8),),
            policy(spec("epistemic", "BENEFIT")),
        )
