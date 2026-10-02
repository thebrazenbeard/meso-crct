import pytest

import meso_crct as m


def public(name: str):
    assert hasattr(m, name), f"missing public attested-guard interface: {name}"
    return getattr(m, name)


def admitted_obligation(
    *,
    goal_id="goal:g",
    share=0.5,
    source_id="obligation:1",
):
    claim = m.GoalObligationClaim(
        goal_id=goal_id,
        minimum_nonprotective_share=share,
        evidence=m.EvidenceRef(
            producer_id="planner:goals",
            producer_revision="v1",
            subject_id=goal_id,
            source_id=source_id,
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


def relation_receipt(
    *,
    goal_id="goal:g",
    target_id="target:route",
    source_id="map:1",
):
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


def strict_audit(obligations):
    samples = (
        m.AllocationSample(
            target_id="target:loop",
            priority=1.0,
            dominant_driver="incentive_salience",
        ),
    )
    return m.audit_attested_attention_budget(samples, obligations)


def targets(*, protective=False):
    if protective:
        return (
            m.TargetState(
                "hazard:fire",
                m.CircuitState(
                    reward=m.RewardState(hazard=1.0, avoidance=1.0),
                ),
            ),
            m.TargetState(
                "target:route",
                m.CircuitState(
                    salience=m.SalienceState(semantic_relevance=0.8),
                ),
            ),
        )
    return (
        m.TargetState(
            "target:loop",
            m.CircuitState(
                salience=m.SalienceState(incentive_salience=1.0),
            ),
        ),
        m.TargetState(
            "target:route",
            m.CircuitState(
                salience=m.SalienceState(semantic_relevance=0.8),
            ),
        ),
    )


def legacy_audit():
    return m.AllocationAudit(
        nonprotective_samples=1,
        protective_samples=0,
        dominant_target="target:loop",
        dominant_fraction=1.0,
        goal_shares=(("goal:g", 0.0),),
        neglected_goals=("goal:g",),
        flags=("goal_neglect", "target_crowd_out", "incentive_capture"),
    )


def test_qualified_mode_rejects_naked_legacy_audit():
    Error = public("UnattestedAllocationAudit")
    obligation = admitted_obligation()
    with pytest.raises(Error):
        m.select_with_allocation_guard(
            targets(),
            audit=legacy_audit(),
            obligations=(obligation,),
            goal_relation_receipts=(relation_receipt(),),
        )


def test_qualified_mode_rejects_raw_goal_obligation():
    obligation = admitted_obligation()
    audit_receipt = strict_audit((obligation,))

    with pytest.raises(m.UnadmittedAllocationObligation):
        m.select_with_allocation_guard(
            targets(),
            audit=audit_receipt,
            obligations=(m.GoalObligation("goal:g", 0.5),),
            goal_relation_receipts=(relation_receipt(),),
        )


def test_qualified_mode_rejects_obligations_not_certified_by_audit():
    Error = public("AllocationAuditObligationMismatch")
    certified = admitted_obligation(source_id="obligation:certified")
    different = admitted_obligation(source_id="obligation:different")
    audit_receipt = strict_audit((certified,))

    with pytest.raises(Error):
        m.select_with_allocation_guard(
            targets(),
            audit=audit_receipt,
            obligations=(different,),
            goal_relation_receipts=(relation_receipt(),),
        )


def test_qualified_mode_accepts_exact_attested_audit_and_obligations():
    obligation = admitted_obligation()
    audit_receipt = strict_audit((obligation,))
    mapping = relation_receipt()

    result = m.select_with_allocation_guard(
        targets(),
        audit=audit_receipt,
        obligations=(obligation,),
        goal_relation_receipts=(mapping,),
    )

    assert result.goal_relation_mode is m.GoalRelationGuardMode.QUALIFIED_RECEIPTS
    assert result.base_selection.selected_target_id == "target:loop"
    assert result.final_selection.selected_target_id == "target:route"
    assert result.rebalanced_goal_id == "goal:g"
    assert result.rebalanced_goal_relation_receipts == (mapping,)
    assert result.allocation_audit_input_digest == audit_receipt.audit_input_digest


def test_explicit_qualified_mode_without_current_mappings_still_requires_strict_audit():
    Error = public("UnattestedAllocationAudit")
    obligation = admitted_obligation()

    with pytest.raises(Error):
        m.select_with_allocation_guard(
            targets(),
            audit=legacy_audit(),
            obligations=(obligation,),
            goal_relation_mode=m.GoalRelationGuardMode.QUALIFIED_RECEIPTS,
        )


def test_explicit_qualified_mode_without_current_mappings_accepts_strict_audit():
    obligation = admitted_obligation()
    audit_receipt = strict_audit((obligation,))

    result = m.select_with_allocation_guard(
        targets(),
        audit=audit_receipt,
        obligations=(obligation,),
        goal_relation_mode=m.GoalRelationGuardMode.QUALIFIED_RECEIPTS,
    )

    assert result.final_selection == result.base_selection
    assert result.reason == "no_currently_relevant_neglected_goal"
    assert result.allocation_audit_input_digest == audit_receipt.audit_input_digest


def test_legacy_mode_rejects_strict_audit_receipt():
    Error = public("AllocationAuditModeMismatch")
    obligation = admitted_obligation()
    audit_receipt = strict_audit((obligation,))

    with pytest.raises(Error):
        m.select_with_allocation_guard(
            targets(),
            audit=audit_receipt,
            obligations=(m.GoalObligation("goal:g", 0.5),),
            goal_relation_mode=m.GoalRelationGuardMode.LEGACY_TARGET_IDENTITY,
        )


def test_legacy_mode_still_accepts_naked_audit_and_raw_obligation():
    result = m.select_with_allocation_guard(
        (
            m.TargetState(
                "target:loop",
                m.CircuitState(
                    salience=m.SalienceState(incentive_salience=1.0),
                ),
            ),
            m.TargetState(
                "goal:g",
                m.CircuitState(
                    salience=m.SalienceState(semantic_relevance=0.8),
                ),
            ),
        ),
        audit=legacy_audit(),
        obligations=(m.GoalObligation("goal:g", 0.5),),
        goal_relation_mode=m.GoalRelationGuardMode.LEGACY_TARGET_IDENTITY,
    )

    assert result.final_selection.selected_target_id == "goal:g"
    assert result.allocation_audit_input_digest is None


def test_protective_override_survives_with_valid_strict_inputs():
    obligation = admitted_obligation()
    audit_receipt = strict_audit((obligation,))

    result = m.select_with_allocation_guard(
        targets(protective=True),
        audit=audit_receipt,
        obligations=(obligation,),
        goal_relation_receipts=(relation_receipt(),),
    )

    assert result.final_selection.selected_target_id == "hazard:fire"
    assert result.reason == "protective_override"
    assert result.allocation_audit_input_digest == audit_receipt.audit_input_digest
