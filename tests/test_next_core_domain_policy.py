import inspect

import pytest

import meso_crct as m


def public(name: str):
    assert hasattr(m, name), f"missing public next-core interface: {name}"
    return getattr(m, name)


def evidence():
    return m.EvidenceRef(
        producer_id="profile:sexuality",
        producer_revision="profile-v1",
        subject_id="target:conversation",
        source_id="event:current",
        currentness=m.EvidenceCurrentness.CURRENT,
    )


def test_domain_contribution_is_local_evidence_not_global_priority():
    DomainContribution = public("DomainContribution")
    contribution = DomainContribution(
        domain_id="sexuality",
        profile_revision="v1",
        target_id="target:conversation",
        contribution_kind="sexual_relevance",
        magnitude=0.8,
        evidence=evidence(),
        direction="approach",
    )

    assert contribution.magnitude == 0.8
    assert contribution.contribution_kind == "sexual_relevance"
    assert not hasattr(contribution, "priority")


def test_domain_contribution_rejects_blank_identity_fields():
    DomainContribution = public("DomainContribution")
    base = dict(
        domain_id="sexuality",
        profile_revision="v1",
        target_id="target:conversation",
        contribution_kind="sexual_relevance",
        magnitude=0.8,
        evidence=evidence(),
    )
    for field in ("domain_id", "profile_revision", "target_id", "contribution_kind"):
        kwargs = dict(base)
        kwargs[field] = "   "
        with pytest.raises(ValueError):
            DomainContribution(**kwargs)


def test_domain_contribution_magnitude_is_locally_bounded():
    DomainContribution = public("DomainContribution")
    with pytest.raises(ValueError):
        DomainContribution(
            domain_id="sexuality",
            profile_revision="v1",
            target_id="target:conversation",
            contribution_kind="sexual_relevance",
            magnitude=1.1,
            evidence=evidence(),
        )


def test_default_selection_reports_legacy_policy_identity():
    result = m.select_target([
        m.TargetState(
            "pursue",
            m.CircuitState(
                salience=m.SalienceState(motivational_salience=0.7),
            ),
        ),
    ])
    assert hasattr(result, "policy_id"), "selection result must expose policy_id"
    assert hasattr(result, "policy_revision"), "selection result must expose policy_revision"
    assert result.policy_id == "legacy-v2"
    assert result.policy_revision == "1"


def test_custom_selection_policy_identity_is_echoed_without_changing_precedence():
    parameters = inspect.signature(m.SelectionPolicy).parameters
    assert "policy_id" in parameters, "SelectionPolicy must accept policy_id"
    assert "policy_revision" in parameters, "SelectionPolicy must accept policy_revision"
    policy = m.SelectionPolicy(
        nonprotective_precedence=(
            m.ArbitrationMode.EPISTEMIC,
            m.ArbitrationMode.MOTIVATIONAL,
            m.ArbitrationMode.ORIENTING,
        ),
        policy_id="research:epistemic-first",
        policy_revision="r1",
    )
    result = m.select_target([
        m.TargetState(
            "learn",
            m.CircuitState(salience=m.SalienceState(epistemic_value=0.6)),
        ),
        m.TargetState(
            "pursue",
            m.CircuitState(salience=m.SalienceState(motivational_salience=1.0)),
        ),
    ], policy=policy)

    assert result.selected_target_id == "learn"
    assert result.policy_id == "research:epistemic-first"
    assert result.policy_revision == "r1"


def test_legacy_default_precedence_remains_unchanged():
    result = m.select_target([
        m.TargetState(
            "learn",
            m.CircuitState(salience=m.SalienceState(epistemic_value=1.0)),
        ),
        m.TargetState(
            "pursue",
            m.CircuitState(salience=m.SalienceState(motivational_salience=0.21)),
        ),
    ])
    assert result.selected_target_id == "pursue"
