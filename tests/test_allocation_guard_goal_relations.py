import pytest

import meso_crct as m


def relation_receipt(goal_id: str, target_id: str, *, source_id: str):
    relation = m.GoalRelation(
        goal_id=goal_id,
        target_id=target_id,
        evidence=m.EvidenceRef(
            producer_id="planner:goals",
            producer_revision="v1",
            subject_id=target_id,
            source_id=source_id,
            currentness=m.EvidenceCurrentness.CURRENT,
        ),
    )
    policy = m.GoalRelationAdmissionPolicy(
        policy_id="host:goal-relations",
        policy_revision="r1",
        producers=(
            m.GoalRelationProducerSpec(
                producer_id="planner:goals",
                producer_revision="v1",
            ),
        ),
    )
    return m.admit_goal_relation(relation, policy)


def admitted_obligation(goal_id: str, minimum: float):
    claim = m.GoalObligationClaim(
        goal_id=goal_id,
        minimum_nonprotective_share=minimum,
        evidence=m.EvidenceRef(
            producer_id="planner:goals",
            producer_revision="v1",
            subject_id=goal_id,
            source_id=f"obligation:{goal_id}",
            currentness=m.EvidenceCurrentness.CURRENT,
        ),
    )
    policy = m.GoalObligationAdmissionPolicy(
        policy_id="host:goal-obligations",
        policy_revision="r1",
        producers=(
            m.GoalObligationProducerSpec(
                producer_id="planner:goals",
                producer_revision="v1",
            ),
        ),
    )
    return m.admit_goal_obligation(claim, policy)


def obligations_for(*items):
    return tuple(
        admitted_obligation(goal_id, minimum)
        for goal_id, _, minimum in items
    )


def audit_for(*items):
    # Build an exact 10-cycle attested history matching requested shares.
    obligations = obligations_for(*items)
    samples = []
    for index in range(10):
        receipts = []
        for goal_id, current_share, _ in items:
            count = int(round(current_share * 10))
            if index < count:
                receipts.append(
                    relation_receipt(
                        goal_id,
                        "target:loop",
                        source_id=f"history:{goal_id}:{index}",
                    )
                )
        samples.append(
            m.AllocationSample(
                target_id="target:loop",
                priority=0.8,
                dominant_driver="incentive_salience",
                goal_relations=tuple(
                    receipt.relation for receipt in receipts
                ),
                goal_relation_receipts=tuple(receipts),
            )
        )
    return m.audit_attested_attention_budget(samples, obligations)


def legacy_audit_for(*items):
    return m.AllocationAudit(
        nonprotective_samples=10,
        protective_samples=0,
        dominant_target="target:loop",
        dominant_fraction=0.8,
        goal_shares=tuple((goal_id, share) for goal_id, share, _ in items),
        neglected_goals=tuple(
            goal_id
            for goal_id, share, minimum in items
            if share < minimum
        ),
        flags=("goal_neglect", "target_crowd_out"),
    )


def legacy_obligations_for(*items):
    return tuple(
        m.GoalObligation(goal_id, minimum)
        for goal_id, _, minimum in items
    )


def target(target_id: str, *, incentive=0.0, semantic=0.0, hazard=0.0):
    reward = m.RewardState(
        hazard=hazard,
        avoidance=hazard,
    )
    salience = m.SalienceState(
        incentive_salience=incentive,
        semantic_relevance=semantic,
    )
    return m.TargetState(
        target_id,
        m.CircuitState(
            reward=reward,
            salience=salience,
        ),
    )


def test_guard_rebalances_when_goal_id_differs_from_target_id():
    audit_items = (("goal:maintenance", 0.0, 0.3),)
    receipt = relation_receipt(
        "goal:maintenance",
        "target:maintenance-route",
        source_id="map:maintenance",
    )
    result = m.select_with_allocation_guard(
        (
            target("target:loop", incentive=1.0),
            target("target:maintenance-route", semantic=0.6),
        ),
        audit=audit_for(*audit_items),
        obligations=obligations_for(*audit_items),
        goal_relation_receipts=(receipt,),
    )

    assert result.base_selection.selected_target_id == "target:loop"
    assert result.final_selection.selected_target_id == "target:maintenance-route"
    assert result.rebalanced_goal_id == "goal:maintenance"
    assert result.rebalanced_goal_relation_receipts == (receipt,)


def test_one_goal_many_targets_uses_same_selection_policy_to_choose_route():
    audit_items = (("goal:research", 0.0, 0.4),)
    receipt_a = relation_receipt(
        "goal:research",
        "target:read",
        source_id="map:read",
    )
    receipt_b = relation_receipt(
        "goal:research",
        "target:experiment",
        source_id="map:experiment",
    )
    result = m.select_with_allocation_guard(
        (
            target("target:loop", incentive=1.0),
            target("target:read", semantic=0.4),
            target("target:experiment", semantic=0.8),
        ),
        audit=audit_for(*audit_items),
        obligations=obligations_for(*audit_items),
        goal_relation_receipts=(receipt_a, receipt_b),
    )

    assert result.final_selection.selected_target_id == "target:experiment"
    assert result.rebalanced_goal_id == "goal:research"
    assert result.rebalanced_goal_relation_receipts == (receipt_b,)


def test_qualified_mode_does_not_fall_back_to_goal_equals_target():
    audit_items = (("goal:maintenance", 0.0, 0.3),)
    unrelated = relation_receipt(
        "goal:other",
        "target:other",
        source_id="map:other",
    )
    result = m.select_with_allocation_guard(
        (
            target("target:loop", incentive=1.0),
            target("goal:maintenance", semantic=0.9),
            target("target:other"),
        ),
        audit=audit_for(*audit_items),
        obligations=obligations_for(*audit_items),
        goal_relation_receipts=(unrelated,),
    )

    assert result.final_selection.selected_target_id == "target:loop"
    assert not result.guard_applied
    assert result.reason == "no_currently_relevant_neglected_goal"
    assert result.rebalanced_goal_relation_receipts == ()


def test_relation_receipt_for_noncandidate_target_is_rejected():
    audit_items = (("goal:maintenance", 0.0, 0.3),)
    receipt = relation_receipt(
        "goal:maintenance",
        "target:not-present",
        source_id="map:missing",
    )

    with pytest.raises(ValueError):
        m.select_with_allocation_guard(
            (
                target("target:loop", incentive=1.0),
                target("target:maintenance", semantic=0.7),
            ),
            audit=audit_for(*audit_items),
            obligations=obligations_for(*audit_items),
            goal_relation_receipts=(receipt,),
        )


def test_guard_preserves_custom_selection_policy_identity():
    audit_items = (("goal:research", 0.0, 0.4),)
    receipt = relation_receipt(
        "goal:research",
        "target:research",
        source_id="map:research",
    )
    policy = m.SelectionPolicy(
        nonprotective_precedence=(
            m.ArbitrationMode.EPISTEMIC,
            m.ArbitrationMode.MOTIVATIONAL,
            m.ArbitrationMode.ORIENTING,
        ),
        policy_id="policy:custom",
        policy_revision="r7",
    )
    result = m.select_with_allocation_guard(
        (
            target("target:loop", incentive=1.0),
            target("target:research", semantic=0.7),
        ),
        audit=audit_for(*audit_items),
        obligations=obligations_for(*audit_items),
        policy=policy,
        goal_relation_receipts=(receipt,),
    )

    assert result.final_selection.selected_target_id == "target:research"
    assert result.final_selection.policy_id == "policy:custom"
    assert result.final_selection.policy_revision == "r7"


def test_protective_override_is_never_rebalanced_even_with_receipts():
    audit_items = (("goal:maintenance", 0.0, 0.3),)
    receipt = relation_receipt(
        "goal:maintenance",
        "target:maintenance",
        source_id="map:maintenance",
    )
    result = m.select_with_allocation_guard(
        (
            target("hazard:fire", hazard=1.0),
            target("target:maintenance", semantic=0.9),
        ),
        audit=audit_for(*audit_items),
        obligations=obligations_for(*audit_items),
        goal_relation_receipts=(receipt,),
    )

    assert result.final_selection.selected_target_id == "hazard:fire"
    assert result.reason == "protective_override"
    assert result.rebalanced_goal_relation_receipts == ()


def test_quiescent_mapped_target_is_not_resurrected():
    audit_items = (("goal:maintenance", 0.0, 0.3),)
    receipt = relation_receipt(
        "goal:maintenance",
        "target:maintenance",
        source_id="map:maintenance",
    )
    result = m.select_with_allocation_guard(
        (
            target("target:loop", incentive=1.0),
            target("target:maintenance"),
        ),
        audit=audit_for(*audit_items),
        obligations=obligations_for(*audit_items),
        goal_relation_receipts=(receipt,),
    )

    assert result.final_selection.selected_target_id == "target:loop"
    assert not result.guard_applied
    assert result.reason == "no_currently_relevant_neglected_goal"


def test_one_target_serving_many_goals_rebalances_highest_deficit_goal():
    audit_items = (
        ("goal:a", 0.1, 0.2),
        ("goal:b", 0.1, 0.5),
    )
    receipt_a = relation_receipt(
        "goal:a",
        "target:shared",
        source_id="map:a",
    )
    receipt_b = relation_receipt(
        "goal:b",
        "target:shared",
        source_id="map:b",
    )
    result = m.select_with_allocation_guard(
        (
            target("target:loop", incentive=1.0),
            target("target:shared", semantic=0.7),
        ),
        audit=audit_for(*audit_items),
        obligations=obligations_for(*audit_items),
        goal_relation_receipts=(receipt_a, receipt_b),
    )

    assert result.final_selection.selected_target_id == "target:shared"
    assert result.rebalanced_goal_id == "goal:b"
    assert result.rebalanced_goal_relation_receipts == (receipt_b,)


def test_legacy_no_receipt_behavior_remains_goal_identity_compatible():
    audit_items = (("goal:maintenance", 0.0, 0.3),)
    result = m.select_with_allocation_guard(
        (
            target("target:loop", incentive=1.0),
            target("goal:maintenance", semantic=0.6),
        ),
        audit=legacy_audit_for(*audit_items),
        obligations=legacy_obligations_for(*audit_items),
    )

    assert result.final_selection.selected_target_id == "goal:maintenance"
    assert result.rebalanced_goal_id == "goal:maintenance"
    assert result.rebalanced_goal_relation_receipts == ()


def test_explicit_qualified_mode_with_no_receipts_never_falls_back_to_identity():
    Mode = getattr(m, "GoalRelationGuardMode")
    audit_items = (("goal:maintenance", 0.0, 0.3),)
    result = m.select_with_allocation_guard(
        (
            target("target:loop", incentive=1.0),
            target("goal:maintenance", semantic=0.9),
        ),
        audit=audit_for(*audit_items),
        obligations=obligations_for(*audit_items),
        goal_relation_mode=Mode.QUALIFIED_RECEIPTS,
    )

    assert result.final_selection.selected_target_id == "target:loop"
    assert not result.guard_applied
    assert result.goal_relation_mode is Mode.QUALIFIED_RECEIPTS


def test_explicit_legacy_mode_rejects_receipt_input():
    Mode = getattr(m, "GoalRelationGuardMode")
    audit_items = (("goal:maintenance", 0.0, 0.3),)
    receipt = relation_receipt(
        "goal:maintenance",
        "target:maintenance",
        source_id="map:maintenance",
    )

    with pytest.raises(ValueError):
        m.select_with_allocation_guard(
            (
                target("target:loop", incentive=1.0),
                target("target:maintenance", semantic=0.8),
            ),
            audit=legacy_audit_for(*audit_items),
            obligations=legacy_obligations_for(*audit_items),
            goal_relation_receipts=(receipt,),
            goal_relation_mode=Mode.LEGACY_TARGET_IDENTITY,
        )


def test_nonempty_receipts_auto_select_qualified_mode():
    Mode = getattr(m, "GoalRelationGuardMode")
    audit_items = (("goal:maintenance", 0.0, 0.3),)
    receipt = relation_receipt(
        "goal:maintenance",
        "target:maintenance",
        source_id="map:maintenance",
    )
    result = m.select_with_allocation_guard(
        (
            target("target:loop", incentive=1.0),
            target("target:maintenance", semantic=0.8),
        ),
        audit=audit_for(*audit_items),
        obligations=obligations_for(*audit_items),
        goal_relation_receipts=(receipt,),
    )

    assert result.goal_relation_mode is Mode.QUALIFIED_RECEIPTS
