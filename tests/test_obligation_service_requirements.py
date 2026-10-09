import pytest

import meso_crct as m


def admitted_obligation(
    goal_id: str,
    share: float,
    *,
    source_id: str | None = None,
):
    source_id = source_id or f"obligation:{goal_id}"
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


def relation_receipt(goal_id: str, target_id: str, source_id: str):
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


def sample(target_id: str, *, goal_ids=(), protective=False):
    receipts = tuple(
        relation_receipt(
            goal_id,
            target_id,
            f"map:{target_id}:{goal_id}",
        )
        for goal_id in goal_ids
    )
    return m.AllocationSample(
        target_id=target_id,
        priority=1.0,
        dominant_driver="semantic_relevance",
        protective=protective,
        goal_relations=tuple(receipt.relation for receipt in receipts),
        goal_relation_receipts=receipts,
    )


def strict_receipt(samples, obligations):
    return m.audit_attested_attention_budget(
        tuple(samples),
        tuple(obligations),
    )


def derive(samples, obligations, horizon_slots):
    receipt = strict_receipt(samples, obligations)
    horizon = m.AllocationServiceHorizon(horizon_slots)
    return m.derive_obligation_service_requirements(
        receipt,
        obligations,
        horizon,
    )


def only(requirements):
    assert len(requirements) == 1
    return requirements[0]


def test_satisfied_requirement_needs_no_more_service():
    obligation = admitted_obligation("goal:g", 0.3)
    requirement = only(
        derive(
            (
                sample("target:1", goal_ids=("goal:g",)),
                sample("target:2", goal_ids=("goal:g",)),
                sample("target:3", goal_ids=("goal:g",)),
                sample("target:4"),
            ),
            (obligation,),
            10,
        )
    )

    assert requirement.required_total_slots == 3
    assert requirement.served_slots == 3
    assert requirement.remaining_horizon_slots == 6
    assert requirement.remaining_required_slots == 0
    assert requirement.slack_slots == 6
    assert requirement.required_remaining_share == 0.0
    assert requirement.state is m.ObligationServiceState.SATISFIED


def test_active_requirement_reports_remaining_share_and_slack():
    obligation = admitted_obligation("goal:g", 0.5)
    requirement = only(
        derive(
            (
                sample("target:1", goal_ids=("goal:g",)),
                sample("target:2", goal_ids=("goal:g",)),
                sample("target:3"),
                sample("target:4"),
            ),
            (obligation,),
            10,
        )
    )

    assert requirement.required_total_slots == 5
    assert requirement.served_slots == 2
    assert requirement.remaining_horizon_slots == 6
    assert requirement.remaining_required_slots == 3
    assert requirement.slack_slots == 3
    assert requirement.required_remaining_share == 0.5
    assert requirement.state is m.ObligationServiceState.ACTIVE


def test_critical_requirement_has_zero_slack():
    obligation = admitted_obligation("goal:g", 0.6)
    requirement = only(
        derive(
            (
                sample("target:1"),
                sample("target:2"),
                sample("target:3"),
                sample("target:4"),
            ),
            (obligation,),
            10,
        )
    )

    assert requirement.required_total_slots == 6
    assert requirement.remaining_horizon_slots == 6
    assert requirement.remaining_required_slots == 6
    assert requirement.slack_slots == 0
    assert requirement.required_remaining_share == 1.0
    assert requirement.state is m.ObligationServiceState.CRITICAL


def test_individually_missed_requirement_has_negative_slack():
    obligation = admitted_obligation("goal:g", 0.8)
    requirement = only(
        derive(
            (
                sample("target:1", goal_ids=("goal:g",)),
                sample("target:2", goal_ids=("goal:g",)),
                sample("target:3", goal_ids=("goal:g",)),
                sample("target:4", goal_ids=("goal:g",)),
                sample("target:5", goal_ids=("goal:g",)),
                sample("target:6"),
                sample("target:7"),
                sample("target:8"),
            ),
            (obligation,),
            10,
        )
    )

    assert requirement.required_total_slots == 8
    assert requirement.served_slots == 5
    assert requirement.remaining_horizon_slots == 2
    assert requirement.remaining_required_slots == 3
    assert requirement.slack_slots == -1
    assert requirement.required_remaining_share == 1.5
    assert requirement.state is m.ObligationServiceState.INDIVIDUALLY_MISSED


def test_minimum_share_uses_ceiling_for_finite_slot_horizon():
    obligation = admitted_obligation("goal:g", 0.25)
    requirement = only(
        derive(
            (),
            (obligation,),
            10,
        )
    )
    assert requirement.required_total_slots == 3


def test_zero_remaining_horizon_has_no_remaining_share_ratio():
    obligation = admitted_obligation("goal:g", 0.5)
    requirement = only(
        derive(
            (
                sample("target:1", goal_ids=("goal:g",)),
                sample("target:2"),
            ),
            (obligation,),
            2,
        )
    )
    assert requirement.remaining_horizon_slots == 0
    assert requirement.remaining_required_slots == 0
    assert requirement.required_remaining_share is None
    assert requirement.state is m.ObligationServiceState.SATISFIED


def test_protective_samples_do_not_consume_service_horizon():
    obligation = admitted_obligation("goal:g", 0.5)
    requirement = only(
        derive(
            (
                sample("target:ordinary"),
                sample("hazard:fire", protective=True),
            ),
            (obligation,),
            4,
        )
    )
    assert requirement.remaining_horizon_slots == 3


def test_one_sample_may_satisfy_multiple_goals():
    a = admitted_obligation("goal:a", 0.5)
    b = admitted_obligation("goal:b", 0.5)
    requirements = derive(
        (sample("target:shared", goal_ids=("goal:a", "goal:b")),),
        (b, a),
        2,
    )

    assert tuple(item.goal_id for item in requirements) == ("goal:a", "goal:b")
    assert tuple(item.served_slots for item in requirements) == (1, 1)
    assert tuple(item.state for item in requirements) == (
        m.ObligationServiceState.SATISFIED,
        m.ObligationServiceState.SATISFIED,
    )


def test_horizon_shorter_than_observed_nonprotective_history_is_rejected():
    obligation = admitted_obligation("goal:g", 0.5)
    receipt = strict_receipt(
        (
            sample("target:1"),
            sample("target:2"),
            sample("hazard:fire", protective=True),
        ),
        (obligation,),
    )

    with pytest.raises(ValueError):
        m.derive_obligation_service_requirements(
            receipt,
            (obligation,),
            m.AllocationServiceHorizon(1),
        )


def test_raw_obligation_is_rejected():
    admitted = admitted_obligation("goal:g", 0.5)
    receipt = strict_receipt((), (admitted,))

    with pytest.raises(m.UnadmittedAllocationObligation):
        m.derive_obligation_service_requirements(
            receipt,
            (m.GoalObligation("goal:g", 0.5),),
            m.AllocationServiceHorizon(10),
        )


def test_same_values_from_different_obligation_provenance_are_rejected():
    certified = admitted_obligation(
        "goal:g",
        0.5,
        source_id="obligation:certified",
    )
    different = admitted_obligation(
        "goal:g",
        0.5,
        source_id="obligation:different",
    )
    receipt = strict_receipt((), (certified,))

    with pytest.raises(m.ServiceRequirementObligationMismatch):
        m.derive_obligation_service_requirements(
            receipt,
            (different,),
            m.AllocationServiceHorizon(10),
        )


def test_requirement_cannot_be_forged_directly():
    with pytest.raises(TypeError):
        m.ObligationServiceRequirement(
            goal_id="goal:g",
            required_total_slots=5,
            served_slots=0,
            remaining_horizon_slots=10,
            remaining_required_slots=5,
            slack_slots=5,
            required_remaining_share=0.5,
            state=m.ObligationServiceState.ACTIVE,
            obligation_admission_digest="obligation",
            allocation_audit_input_digest="audit",
            horizon_spec_digest="horizon",
            requirement_input_digest="forged",
        )


def test_requirement_digest_binds_horizon_audit_and_obligation_inputs():
    obligation = admitted_obligation("goal:g", 0.5)
    baseline = only(derive((), (obligation,), 10))
    changed_horizon = only(derive((), (obligation,), 11))

    served = only(
        derive(
            (sample("target:1", goal_ids=("goal:g",)),),
            (obligation,),
            10,
        )
    )
    changed_obligation = only(
        derive(
            (),
            (
                admitted_obligation(
                    "goal:g",
                    0.5,
                    source_id="obligation:other",
                ),
            ),
            10,
        )
    )

    assert baseline.requirement_input_digest != changed_horizon.requirement_input_digest
    assert baseline.requirement_input_digest != served.requirement_input_digest
    assert baseline.requirement_input_digest != changed_obligation.requirement_input_digest


def test_requirement_exposes_no_motivational_or_action_authority_fields():
    obligation = admitted_obligation("goal:g", 0.5)
    requirement = only(derive((), (obligation,), 10))

    for name in (
        "reward",
        "pleasure",
        "salience",
        "desire",
        "vigor",
        "consent",
        "intent",
        "action_authority",
        "execution_authority",
        "jointly_feasible",
    ):
        assert not hasattr(requirement, name)


def test_horizon_requires_plain_nonnegative_integer_slots():
    with pytest.raises((TypeError, ValueError)):
        m.AllocationServiceHorizon(-1)
    with pytest.raises((TypeError, ValueError)):
        m.AllocationServiceHorizon(1.5)
    with pytest.raises((TypeError, ValueError)):
        m.AllocationServiceHorizon(True)


@pytest.mark.parametrize(
    ("share", "expected"),
    [
        (0.1, 10**29 + 1),
        (0.25, 25 * 10**28 + 1),
    ],
)
def test_huge_finite_horizon_ceiling_never_rounds_required_service_down(
    share: float, expected: int
):
    # The default Decimal precision (28 digits) rounded these products down
    # and silently omitted one required service slot.
    obligation = admitted_obligation("goal:huge", share)
    requirement = only(derive((), (obligation,), 10**30 + 1))
    assert requirement.required_total_slots == expected

