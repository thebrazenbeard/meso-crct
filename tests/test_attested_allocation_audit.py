import pytest

import meso_crct as m


def public(name: str):
    assert hasattr(m, name), f"missing public attested-audit interface: {name}"
    return getattr(m, name)


def admitted_obligation(
    goal_id="goal:g",
    share=0.5,
    *,
    source_id="obligation:1",
    policy_revision="r1",
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
        policy_revision=policy_revision,
        producers=(
            m.GoalObligationProducerSpec(
                producer_id="planner:goals",
                producer_revision="v1",
            ),
        ),
    )
    return m.admit_goal_obligation(claim, policy)


def relation_receipt(goal_id, target_id, *, source_id):
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


def sample(
    target_id,
    *,
    receipts=(),
    raw_relations=None,
    protective=False,
    priority=0.5,
):
    if raw_relations is None:
        raw_relations = tuple(receipt.relation for receipt in receipts)
    return m.AllocationSample(
        target_id=target_id,
        priority=priority,
        dominant_driver="semantic_relevance",
        protective=protective,
        goal_relations=tuple(raw_relations),
        goal_relation_receipts=tuple(receipts),
    )


def strict(samples, obligations, *, crowdout_fraction=0.75):
    fn = public("audit_attested_attention_budget")
    return fn(
        tuple(samples),
        tuple(obligations),
        crowdout_fraction=crowdout_fraction,
    )


def test_raw_goal_obligation_is_rejected():
    Error = public("UnadmittedAllocationObligation")
    with pytest.raises(Error):
        strict(
            (sample("target:a"),),
            (m.GoalObligation("goal:g", 0.5),),
        )


def test_unattested_stored_relation_is_rejected():
    Error = public("UnattestedAllocationSample")
    relation = m.GoalRelation(
        goal_id="goal:g",
        target_id="target:a",
        evidence=m.EvidenceRef(
            producer_id="planner:goals",
            producer_revision="v1",
            subject_id="target:a",
            source_id="map:raw",
            currentness=m.EvidenceCurrentness.CURRENT,
        ),
    )
    with pytest.raises(Error):
        strict(
            (
                sample(
                    "target:a",
                    raw_relations=(relation,),
                ),
            ),
            (admitted_obligation(),),
        )


def test_attested_relation_must_bind_the_sample_target():
    Error = public("AttestedAllocationIntegrityError")
    receipt = relation_receipt(
        "goal:g",
        "target:b",
        source_id="map:wrong-target",
    )
    misbound = sample(
        "target:a",
        receipts=(receipt,),
    )

    with pytest.raises(Error):
        strict(
            (misbound,),
            (admitted_obligation(),),
        )


def test_fully_attested_relation_counts_toward_admitted_goal():
    receipt = relation_receipt(
        "goal:g",
        "target:a",
        source_id="map:1",
    )
    result = strict(
        (sample("target:a", receipts=(receipt,)),),
        (admitted_obligation(share=1.0),),
    )

    assert result.audit.goal_shares == (("goal:g", 1.0),)
    assert result.audit.neglected_goals == ()
    assert result.audit_input_digest


def test_relation_free_sample_has_no_target_identity_fallback_in_strict_mode():
    result = strict(
        (sample("goal:g"),),
        (admitted_obligation(share=1.0),),
    )

    assert result.audit.goal_shares == (("goal:g", 0.0),)
    assert result.audit.neglected_goals == ("goal:g",)


def test_legacy_audit_still_uses_target_identity_fallback():
    legacy = m.audit_attention_budget(
        (sample("goal:g"),),
        (m.GoalObligation("goal:g", 1.0),),
    )
    assert legacy.goal_shares == (("goal:g", 1.0),)
    assert legacy.neglected_goals == ()


def test_duplicate_same_goal_relations_count_once_per_sample():
    r1 = relation_receipt(
        "goal:g",
        "target:a",
        source_id="map:1",
    )
    r2 = relation_receipt(
        "goal:g",
        "target:a",
        source_id="map:2",
    )
    result = strict(
        (sample("target:a", receipts=(r1, r2)),),
        (admitted_obligation(share=1.0),),
    )
    assert result.audit.goal_shares == (("goal:g", 1.0),)


def test_duplicate_obligation_goal_ids_are_rejected():
    with pytest.raises(ValueError):
        strict(
            (sample("target:a"),),
            (
                admitted_obligation(share=0.2, source_id="obligation:1"),
                admitted_obligation(share=0.4, source_id="obligation:2"),
            ),
        )


def test_attested_audit_receipt_cannot_be_forged_directly():
    Receipt = public("AttestedAllocationAuditReceipt")
    audit = m.AllocationAudit(
        nonprotective_samples=1,
        protective_samples=0,
        dominant_target="target:a",
        dominant_fraction=1.0,
        goal_shares=(("goal:g", 1.0),),
        neglected_goals=(),
        flags=(),
    )
    with pytest.raises(TypeError):
        Receipt(
            audit=audit,
            audit_input_digest="forged",
        )


def test_audit_digest_binds_relation_evidence_and_obligation_admission():
    r1 = relation_receipt(
        "goal:g",
        "target:a",
        source_id="map:1",
    )
    r2 = relation_receipt(
        "goal:g",
        "target:a",
        source_id="map:2",
    )

    baseline = strict(
        (sample("target:a", receipts=(r1,)),),
        (admitted_obligation(source_id="obligation:1"),),
    )
    changed_relation = strict(
        (sample("target:a", receipts=(r2,)),),
        (admitted_obligation(source_id="obligation:1"),),
    )
    changed_obligation = strict(
        (sample("target:a", receipts=(r1,)),),
        (admitted_obligation(source_id="obligation:2"),),
    )

    assert baseline.audit_input_digest != changed_relation.audit_input_digest
    assert baseline.audit_input_digest != changed_obligation.audit_input_digest


def test_obligation_input_order_does_not_change_strict_audit_or_digest():
    ra = relation_receipt(
        "goal:a",
        "target:shared",
        source_id="map:a",
    )
    rb = relation_receipt(
        "goal:b",
        "target:shared",
        source_id="map:b",
    )
    a = admitted_obligation(
        "goal:a",
        0.5,
        source_id="obligation:a",
    )
    b = admitted_obligation(
        "goal:b",
        0.5,
        source_id="obligation:b",
    )
    samples = (sample("target:shared", receipts=(ra, rb)),)

    first = strict(samples, (a, b))
    second = strict(samples, (b, a))

    assert first.audit == second.audit
    assert first.audit_input_digest == second.audit_input_digest
    assert first.audit.goal_shares == (
        ("goal:a", 1.0),
        ("goal:b", 1.0),
    )


def test_protective_sample_does_not_contribute_ordinary_goal_share():
    receipt = relation_receipt(
        "goal:g",
        "hazard:fire",
        source_id="map:protective",
    )
    result = strict(
        (
            sample(
                "hazard:fire",
                receipts=(receipt,),
                protective=True,
                priority=1.0,
            ),
        ),
        (admitted_obligation(share=1.0),),
    )

    assert result.audit.nonprotective_samples == 0
    assert result.audit.protective_samples == 1
    assert result.audit.goal_shares == (("goal:g", 0.0),)
