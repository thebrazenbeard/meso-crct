import inspect

import pytest

import meso_crct as m


def public(name: str):
    assert hasattr(m, name), f"missing public goal-receipt interface: {name}"
    return getattr(m, name)


def relation(
    *,
    goal_id="goal:g",
    target_id="target:a",
    source_id="goal-map:1",
    producer_id="planner:goals",
    producer_revision="v1",
    currentness=None,
):
    if currentness is None:
        currentness = m.EvidenceCurrentness.CURRENT
    return m.GoalRelation(
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


def producer(producer_id="planner:goals", producer_revision="v1"):
    return m.GoalRelationProducerSpec(
        producer_id=producer_id,
        producer_revision=producer_revision,
    )


def policy(*, revision="r1", producers=None):
    parameters = inspect.signature(m.GoalRelationAdmissionPolicy).parameters
    assert "policy_id" in parameters
    assert "policy_revision" in parameters
    if producers is None:
        producers = (producer(),)
    return m.GoalRelationAdmissionPolicy(
        policy_id="host:goal-relations",
        policy_revision=revision,
        producers=tuple(producers),
    )


def admit(item, policy_obj=None):
    fn = public("admit_goal_relation")
    if policy_obj is None:
        policy_obj = policy()
    return fn(item, policy_obj)


def selected(target_id="target:a"):
    return m.select_target(
        (
            m.TargetState(
                target_id,
                m.CircuitState(
                    salience=m.SalienceState(semantic_relevance=0.8),
                ),
            ),
        )
    )


def test_goal_relation_policy_has_identity_and_legacy_defaults():
    parameters = inspect.signature(m.GoalRelationAdmissionPolicy).parameters
    assert "policy_id" in parameters
    assert "policy_revision" in parameters

    legacy = m.GoalRelationAdmissionPolicy(producers=(producer(),))
    assert legacy.policy_id == "legacy-goal-relation-policy"
    assert legacy.policy_revision == "1"


def test_current_trusted_relation_is_admitted_to_receipt():
    Receipt = public("GoalRelationAdmissionReceipt")
    rel = relation()
    receipt = admit(rel)

    assert isinstance(receipt, Receipt)
    assert receipt.relation == rel
    assert receipt.admission_policy_id == "host:goal-relations"
    assert receipt.admission_policy_revision == "r1"
    assert receipt.admission_input_digest


@pytest.mark.parametrize(
    "currentness",
    [m.EvidenceCurrentness.STALE, m.EvidenceCurrentness.UNKNOWN],
)
def test_noncurrent_relation_cannot_be_admitted(currentness):
    Inadmissible = public("InadmissibleGoalRelation")
    with pytest.raises(Inadmissible):
        admit(relation(currentness=currentness))


@pytest.mark.parametrize(
    "producer_id,producer_revision",
    [
        ("planner:spoof", "v1"),
        ("planner:goals", "v2"),
    ],
)
def test_untrusted_relation_producer_cannot_be_admitted(
    producer_id,
    producer_revision,
):
    Unadmitted = public("UnadmittedGoalRelation")
    with pytest.raises(Unadmitted):
        admit(
            relation(
                producer_id=producer_id,
                producer_revision=producer_revision,
            )
        )


def test_receipt_digest_binds_relation_and_policy():
    baseline = admit(relation(source_id="source:1"))
    changed_source = admit(relation(source_id="source:2"))
    changed_policy = admit(
        relation(source_id="source:1"),
        policy(revision="r2"),
    )

    assert baseline.admission_input_digest != changed_source.admission_input_digest
    assert baseline.admission_input_digest != changed_policy.admission_input_digest


def test_receipt_digest_is_stable_under_producer_spec_order():
    p1 = producer()
    p2 = producer("planner:backup", "v2")
    first = admit(
        relation(),
        policy(producers=(p1, p2)),
    )
    second = admit(
        relation(),
        policy(producers=(p2, p1)),
    )
    assert first.admission_input_digest == second.admission_input_digest


def test_goal_relation_receipt_cannot_be_forged_directly():
    Receipt = public("GoalRelationAdmissionReceipt")
    with pytest.raises(TypeError):
        Receipt(
            relation=relation(),
            admission_policy_id="host:goal-relations",
            admission_policy_revision="r1",
            admission_input_digest="forged",
        )


def test_allocation_sample_preserves_raw_relation_and_admission_receipt():
    rel = relation()
    result = m.AllocationSample.from_selection(
        selected(),
        goal_relations=(rel,),
        goal_relation_policy=policy(),
    )
    assert result is not None
    assert result.goal_relations == (rel,)
    assert len(result.goal_relation_receipts) == 1
    assert result.goal_relation_receipts[0].relation == rel
    assert result.goal_relation_receipts[0].admission_policy_id == "host:goal-relations"


def test_multiple_relations_produce_one_receipt_each():
    rel1 = relation(goal_id="goal:one", source_id="source:1")
    rel2 = relation(goal_id="goal:two", source_id="source:2")
    result = m.AllocationSample.from_selection(
        selected(),
        goal_relations=(rel1, rel2),
        goal_relation_policy=policy(),
    )
    assert result is not None
    assert result.goal_relations == (rel1, rel2)
    assert len(result.goal_relation_receipts) == 2
    assert {receipt.relation.goal_id for receipt in result.goal_relation_receipts} == {
        "goal:one",
        "goal:two",
    }


def test_sample_rejects_receipt_for_relation_it_does_not_store():
    receipt = admit(relation(goal_id="goal:one"))
    other = relation(goal_id="goal:other")

    with pytest.raises(ValueError):
        m.AllocationSample(
            target_id="target:a",
            priority=0.8,
            dominant_driver="semantic_relevance",
            goal_relations=(other,),
            goal_relation_receipts=(receipt,),
        )


def test_legacy_direct_sample_can_have_unattested_relation():
    rel = relation()
    sample = m.AllocationSample(
        target_id="target:a",
        priority=0.8,
        dominant_driver="semantic_relevance",
        goal_relations=(rel,),
    )
    assert sample.goal_relations == (rel,)
    assert sample.goal_relation_receipts == ()


def test_existing_goal_share_audit_is_unchanged_with_receipts():
    rel = relation(goal_id="goal:g")
    sample = m.AllocationSample.from_selection(
        selected(),
        goal_relations=(rel,),
        goal_relation_policy=policy(),
    )
    assert sample is not None
    audit = m.audit_attention_budget(
        (sample,),
        (m.GoalObligation("goal:g", 1.0),),
    )
    assert audit.goal_shares == (("goal:g", 1.0),)
    assert audit.neglected_goals == ()


def test_sample_exposes_attested_and_unattested_goal_relation_views():
    attested = relation(goal_id="goal:attested", source_id="source:attested")
    legacy = relation(goal_id="goal:legacy", source_id="source:legacy")
    receipt = admit(attested)

    sample = m.AllocationSample(
        target_id="target:a",
        priority=0.8,
        dominant_driver="semantic_relevance",
        goal_relations=(attested, legacy),
        goal_relation_receipts=(receipt,),
    )

    assert sample.attested_goal_relations == (attested,)
    assert sample.unattested_goal_relations == (legacy,)
    assert sample.goal_relation_attestation_complete is False


def test_from_selection_goal_relations_are_fully_attested():
    rel1 = relation(goal_id="goal:one", source_id="source:1")
    rel2 = relation(goal_id="goal:two", source_id="source:2")
    sample = m.AllocationSample.from_selection(
        selected(),
        goal_relations=(rel1, rel2),
        goal_relation_policy=policy(),
    )

    assert sample is not None
    assert sample.attested_goal_relations == (rel1, rel2)
    assert sample.unattested_goal_relations == ()
    assert sample.goal_relation_attestation_complete is True


def test_legacy_relation_only_sample_is_visibly_unattested():
    rel = relation()
    sample = m.AllocationSample(
        target_id="target:a",
        priority=0.8,
        dominant_driver="semantic_relevance",
        goal_relations=(rel,),
    )

    assert sample.attested_goal_relations == ()
    assert sample.unattested_goal_relations == (rel,)
    assert sample.goal_relation_attestation_complete is False
