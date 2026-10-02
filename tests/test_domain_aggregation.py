import pytest

import meso_crct as m


def public(name: str):
    assert hasattr(m, name), f"missing public coalition interface: {name}"
    return getattr(m, name)


def evidence(source_id: str, currentness=None):
    if currentness is None:
        currentness = m.EvidenceCurrentness.CURRENT
    return m.EvidenceRef(
        producer_id="profile:test",
        producer_revision="v1",
        subject_id="target:a",
        source_id=source_id,
        currentness=currentness,
    )


def contribution(kind: str, magnitude: float, *, target_id="target:a", source_id="src:1", currentness=None):
    return m.DomainContribution(
        domain_id="sexuality",
        profile_revision="v1",
        target_id=target_id,
        contribution_kind=kind,
        magnitude=magnitude,
        evidence=evidence(source_id, currentness=currentness),
    )


def spec(kind: str, family: str):
    ContributionKindSpec = public("ContributionKindSpec")
    return ContributionKindSpec(
        domain_id="sexuality",
        profile_revision="v1",
        contribution_kind=kind,
        family_id=family,
    )


def registry(*specs):
    ContributionRegistry = public("ContributionRegistry")
    return ContributionRegistry(specs=tuple(specs))


def aggregate(items, reg):
    fn = public("aggregate_domain_contributions")
    return fn(tuple(items), reg)


def test_same_family_uses_strongest_magnitude_not_sum():
    reg = registry(
        spec("sexual_relevance", "domain_activation"),
        spec("erotic_relevance", "domain_activation"),
    )
    views = aggregate(
        [
            contribution("sexual_relevance", 0.2, source_id="src:1"),
            contribution("erotic_relevance", 0.4, source_id="src:2"),
            contribution("sexual_relevance", 0.3, source_id="src:3"),
        ],
        reg,
    )

    assert len(views) == 1
    view = views[0]
    assert view.target_id == "target:a"
    assert view.family_id == "domain_activation"
    assert view.magnitude == 0.4
    assert view.support_count == 3
    assert set(view.contribution_kinds) == {"sexual_relevance", "erotic_relevance"}
    assert set(view.source_ids) == {"src:1", "src:2", "src:3"}
    assert not hasattr(view, "priority")


def test_distinct_families_remain_distinct():
    reg = registry(
        spec("sexual_relevance", "domain_activation"),
        spec("sexual_inhibition", "domain_inhibition"),
    )
    views = aggregate(
        [
            contribution("sexual_relevance", 0.8, source_id="src:a"),
            contribution("sexual_inhibition", 0.6, source_id="src:b"),
        ],
        reg,
    )
    assert {(v.family_id, v.magnitude) for v in views} == {
        ("domain_activation", 0.8),
        ("domain_inhibition", 0.6),
    }


def test_same_family_on_different_targets_stays_separate():
    reg = registry(spec("sexual_relevance", "domain_activation"))
    views = aggregate(
        [
            contribution("sexual_relevance", 0.8, target_id="target:a", source_id="src:a"),
            contribution("sexual_relevance", 0.5, target_id="target:b", source_id="src:b"),
        ],
        reg,
    )
    assert {(v.target_id, v.magnitude) for v in views} == {
        ("target:a", 0.8),
        ("target:b", 0.5),
    }


def test_unregistered_contribution_kind_is_rejected():
    UnknownContributionKind = public("UnknownContributionKind")
    reg = registry(spec("sexual_relevance", "domain_activation"))
    with pytest.raises(UnknownContributionKind):
        aggregate([contribution("invented_dimension", 0.9)], reg)


@pytest.mark.parametrize(
    "currentness",
    [m.EvidenceCurrentness.STALE, m.EvidenceCurrentness.UNKNOWN],
)
def test_noncurrent_contribution_evidence_is_inadmissible(currentness):
    InadmissibleContributionEvidence = public("InadmissibleContributionEvidence")
    reg = registry(spec("sexual_relevance", "domain_activation"))
    with pytest.raises(InadmissibleContributionEvidence):
        aggregate(
            [contribution("sexual_relevance", 0.8, currentness=currentness)],
            reg,
        )


def test_duplicate_registry_key_fails_construction():
    ContributionRegistry = public("ContributionRegistry")
    duplicate = spec("sexual_relevance", "domain_activation")
    with pytest.raises(ValueError):
        ContributionRegistry(specs=(duplicate, duplicate))
