import inspect

import pytest

import meso_crct as m


def public(name: str):
    assert hasattr(m, name), f"missing public goal-target interface: {name}"
    return getattr(m, name)


def selected(target_id: str):
    return m.select_target(
        [
            m.TargetState(
                target_id,
                m.CircuitState(
                    salience=m.SalienceState(semantic_relevance=0.8),
                ),
            )
        ]
    )


def admission_policy():
    return m.GoalRelationAdmissionPolicy(
        producers=(
            m.GoalRelationProducerSpec(
                producer_id="planner:goals",
                producer_revision="v1",
            ),
        ),
    )


def relation(
    goal_id: str,
    target_id: str,
    *,
    currentness=None,
    source_id="goal-map:1",
    producer_id="planner:goals",
    producer_revision="v1",
):
    GoalRelation = public("GoalRelation")
    if currentness is None:
        currentness = m.EvidenceCurrentness.CURRENT
    return GoalRelation(
        goal_id=goal_id,
        target_id=target_id,
        evidence=m.EvidenceRef(
            producer_id=producer_id,
            producer_revision=producer_revision,
            subject_id=target_id,
            source_id=source_id,
            currentness=currentness,
        ),
    )


def test_one_goal_can_span_multiple_selected_targets():
    assert "goal_relations" in inspect.signature(m.AllocationWindow.record).parameters
    window = m.AllocationWindow()
    window = window.record(
        selected("target:research-paper"),
        goal_relations=(relation("goal:meso", "target:research-paper"),),
        goal_relation_policy=admission_policy(),
    )
    window = window.record(
        selected("target:source-audit"),
        goal_relations=(
            relation("goal:meso", "target:source-audit", source_id="goal-map:2"),
        ),
        goal_relation_policy=admission_policy(),
    )

    audit = m.audit_allocation_window(
        window,
        obligations=(m.GoalObligation("goal:meso", 1.0),),
    )
    assert audit.goal_shares == (("goal:meso", 1.0),)
    assert audit.neglected_goals == ()


def test_one_target_can_count_toward_multiple_goals_once_each():
    window = m.AllocationWindow().record(
        selected("target:paper"),
        goal_relations=(
            relation("goal:research", "target:paper", source_id="goal-map:r"),
            relation("goal:learning", "target:paper", source_id="goal-map:l"),
        ),
        goal_relation_policy=admission_policy(),
    )
    audit = m.audit_allocation_window(
        window,
        obligations=(
            m.GoalObligation("goal:research", 1.0),
            m.GoalObligation("goal:learning", 1.0),
        ),
    )
    assert dict(audit.goal_shares) == {
        "goal:research": 1.0,
        "goal:learning": 1.0,
    }


def test_duplicate_goal_relations_do_not_double_count_one_sample():
    rel_a = relation("goal:research", "target:paper", source_id="goal-map:a")
    rel_b = relation("goal:research", "target:paper", source_id="goal-map:b")
    window = m.AllocationWindow().record(
        selected("target:paper"),
        goal_relations=(rel_a, rel_b),
        goal_relation_policy=admission_policy(),
    )
    audit = m.audit_allocation_window(
        window,
        obligations=(m.GoalObligation("goal:research", 1.0),),
    )
    assert audit.goal_shares == (("goal:research", 1.0),)


def test_goal_relation_target_must_match_selected_target():
    with pytest.raises(ValueError):
        m.AllocationWindow().record(
            selected("target:a"),
            goal_relations=(relation("goal:g", "target:b"),),
            goal_relation_policy=admission_policy(),
        )


@pytest.mark.parametrize(
    "currentness",
    [m.EvidenceCurrentness.STALE, m.EvidenceCurrentness.UNKNOWN],
)
def test_noncurrent_goal_relation_is_rejected(currentness):
    with pytest.raises(ValueError):
        m.AllocationWindow().record(
            selected("target:a"),
            goal_relations=(
                relation("goal:g", "target:a", currentness=currentness),
            ),
            goal_relation_policy=admission_policy(),
        )


def test_legacy_relation_free_target_equals_goal_fallback_is_preserved():
    sample = m.AllocationSample(
        target_id="goal:maintenance",
        priority=0.8,
        dominant_driver="semantic_relevance",
    )
    audit = m.audit_attention_budget(
        [sample],
        [m.GoalObligation("goal:maintenance", 1.0)],
    )
    assert audit.goal_shares == (("goal:maintenance", 1.0),)


def test_goal_relation_admission_policy_binds_trusted_producer():
    trusted = admission_policy()
    good = relation("goal:g", "target:a")
    spoofed = relation(
        "goal:g",
        "target:a",
        producer_id="planner:spoof",
    )
    wrong_revision = relation(
        "goal:g",
        "target:a",
        producer_revision="v2",
    )

    assert trusted.admits(good)
    assert not trusted.admits(spoofed)
    assert not trusted.admits(wrong_revision)


def test_allocation_record_requires_goal_relation_admission_policy():
    parameters = inspect.signature(m.AllocationWindow.record).parameters
    assert "goal_relation_policy" in parameters

    rel = relation("goal:g", "target:a")
    with pytest.raises(ValueError):
        m.AllocationWindow().record(
            selected("target:a"),
            goal_relations=(rel,),
        )

    accepted = m.AllocationWindow().record(
        selected("target:a"),
        goal_relations=(rel,),
        goal_relation_policy=admission_policy(),
    )
    assert accepted.samples[0].goal_relations == (rel,)


def test_allocation_record_rejects_untrusted_goal_relation_producer():
    with pytest.raises(ValueError):
        m.AllocationWindow().record(
            selected("target:a"),
            goal_relations=(
                relation(
                    "goal:g",
                    "target:a",
                    producer_id="planner:spoof",
                ),
            ),
            goal_relation_policy=admission_policy(),
        )
