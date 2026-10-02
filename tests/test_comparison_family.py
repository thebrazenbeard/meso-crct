import pytest

import meso_crct as m


def public(name: str):
    assert hasattr(m, name), f"missing public comparison-family interface: {name}"
    return getattr(m, name)


def domain_view(target_id: str, family_id: str, magnitude: float, *, source_id=None):
    if source_id is None:
        source_id = f"src:{target_id}:{family_id}"
    return m.ContributionFamilyView(
        target_id=target_id,
        family_id=family_id,
        magnitude=magnitude,
        support_count=1,
        contribution_kinds=(family_id,),
        source_ids=(source_id,),
    )


def admitted_effort(
    target_id: str,
    *,
    required=0.5,
    cost=0.4,
    willingness=0.8,
    policy_revision="r1",
):
    raw = m.EffortAssessment(
        target_id=target_id,
        evidence=m.EvidenceRef(
            producer_id="planner:effort",
            producer_revision="v1",
            subject_id=target_id,
            source_id=f"effort:{target_id}",
            currentness=m.EvidenceCurrentness.CURRENT,
        ),
        required_effort=required,
        effort_cost=cost,
        willingness_to_exert=willingness,
        vigor_proposal=0.6,
    )
    policy = m.EffortAdmissionPolicy(
        policy_id="host:effort",
        policy_revision=policy_revision,
        producers=(
            m.EffortProducerSpec(
                producer_id="planner:effort",
                producer_revision="v1",
            ),
        ),
    )
    return m.admit_effort_assessment(raw, policy)


def partial_policy(*families):
    specs = []
    for family_id, direction in families:
        specs.append(
            m.FamilyComparisonSpec(
                family_id=family_id,
                direction=getattr(m.FamilyDirection, direction),
            )
        )
    return m.PartialOrderPolicy(
        policy_id="policy:test",
        policy_revision="r1",
        families=tuple(specs),
    )


def feasibility_policy():
    return m.FeasibilityAdmissionPolicy(
        policy_id="host:feasibility",
        policy_revision="r1",
        producers=(
            m.FeasibilityProducerSpec(
                producer_id="planner:feasibility",
                producer_revision="v1",
            ),
        ),
    )


def feasible(target_id: str):
    return m.FeasibilityAssessment(
        target_id=target_id,
        state=m.FeasibilityState.FEASIBLE,
        evidence=m.EvidenceRef(
            producer_id="planner:feasibility",
            producer_revision="v1",
            subject_id=target_id,
            source_id=f"feasibility:{target_id}",
            currentness=m.EvidenceCurrentness.CURRENT,
        ),
    )


def test_comparison_family_view_rejects_direct_construction():
    ComparisonFamilyView = public("ComparisonFamilyView")
    SourceKind = public("ComparisonFamilySourceKind")
    with pytest.raises(TypeError):
        ComparisonFamilyView(
            target_id="a",
            family_id="epistemic",
            magnitude=0.8,
            source_kind=SourceKind.DOMAIN_AGGREGATE,
            source_digest="abc",
        )


def test_domain_adapter_preserves_value_and_source_kind():
    SourceKind = public("ComparisonFamilySourceKind")
    adapter = public("comparison_family_from_domain")
    legacy = domain_view("a", "epistemic", 0.8)

    generic = adapter(legacy)

    assert generic.target_id == "a"
    assert generic.family_id == "epistemic"
    assert generic.magnitude == 0.8
    assert generic.source_kind is SourceKind.LEGACY_DOMAIN_VIEW
    assert generic.source_digest


def test_domain_adapter_digest_binds_exact_aggregate_content():
    adapter = public("comparison_family_from_domain")
    first = adapter(domain_view("a", "epistemic", 0.8, source_id="src:1"))
    changed_value = adapter(domain_view("a", "epistemic", 0.7, source_id="src:1"))
    changed_source = adapter(domain_view("a", "epistemic", 0.8, source_id="src:2"))

    assert first.source_digest != changed_value.source_digest
    assert first.source_digest != changed_source.source_digest


def test_admitted_effort_projects_effort_cost():
    EffortField = public("EffortComparisonField")
    SourceKind = public("ComparisonFamilySourceKind")
    project = public("comparison_families_from_effort")

    views = project(
        admitted_effort("a", cost=0.35),
        fields=(EffortField.EFFORT_COST,),
    )

    assert len(views) == 1
    view = views[0]
    assert view.target_id == "a"
    assert view.family_id == "effort_cost"
    assert view.magnitude == 0.35
    assert view.source_kind is SourceKind.EFFORT_APPRAISAL
    assert view.source_digest


def test_raw_effort_cannot_be_projected():
    EffortField = public("EffortComparisonField")
    project = public("comparison_families_from_effort")
    raw = m.EffortAssessment(
        target_id="a",
        evidence=m.EvidenceRef(
            producer_id="planner:effort",
            producer_revision="v1",
            subject_id="a",
            source_id="effort:a",
            currentness=m.EvidenceCurrentness.CURRENT,
        ),
        required_effort=0.5,
        effort_cost=0.4,
        willingness_to_exert=0.8,
    )

    with pytest.raises(TypeError):
        project(raw, fields=(EffortField.EFFORT_COST,))


def test_effort_projection_enum_excludes_vigor():
    EffortField = public("EffortComparisonField")
    assert not hasattr(EffortField, "VIGOR_PROPOSAL")
    assert {member.name for member in EffortField} == {
        "REQUIRED_EFFORT",
        "EFFORT_COST",
        "WILLINGNESS_TO_EXERT",
    }


def test_effort_projection_digest_binds_admission_and_field():
    EffortField = public("EffortComparisonField")
    project = public("comparison_families_from_effort")
    admitted = admitted_effort("a", required=0.5, cost=0.4)

    cost = project(admitted, fields=(EffortField.EFFORT_COST,))[0]
    required = project(admitted, fields=(EffortField.REQUIRED_EFFORT,))[0]
    changed_policy = project(
        admitted_effort("a", required=0.5, cost=0.4, policy_revision="r2"),
        fields=(EffortField.EFFORT_COST,),
    )[0]

    assert cost.source_digest != required.source_digest
    assert cost.source_digest != changed_policy.source_digest


def test_partial_order_accepts_generic_comparison_views():
    adapter = public("comparison_family_from_domain")
    views = (
        adapter(domain_view("a", "epistemic", 0.9)),
        adapter(domain_view("b", "epistemic", 0.6)),
    )
    result = m.select_by_partial_order(
        candidate_target_ids=("a", "b"),
        family_views=views,
        policy=partial_policy(("epistemic", "BENEFIT")),
    )
    assert result.selected_target_id == "a"


def test_legacy_and_generic_domain_paths_have_same_canonical_decision_digest():
    adapter = public("comparison_family_from_domain")
    legacy_views = (
        domain_view("a", "epistemic", 0.9, source_id="src:a"),
        domain_view("b", "epistemic", 0.6, source_id="src:b"),
    )
    generic_views = tuple(adapter(view) for view in legacy_views)
    policy = partial_policy(("epistemic", "BENEFIT"))

    legacy = m.select_by_partial_order(
        candidate_target_ids=("a", "b"),
        family_views=legacy_views,
        policy=policy,
    )
    generic = m.select_by_partial_order(
        candidate_target_ids=("a", "b"),
        family_views=generic_views,
        policy=policy,
    )

    assert legacy.selected_target_id == generic.selected_target_id == "a"
    assert legacy.decision_input_digest == generic.decision_input_digest


def test_selector_combines_domain_and_admitted_effort_generic_families():
    EffortField = public("EffortComparisonField")
    domain_adapter = public("comparison_family_from_domain")
    effort_adapter = public("comparison_families_from_effort")

    views = (
        domain_adapter(domain_view("a", "epistemic", 0.8)),
        *effort_adapter(
            admitted_effort("a", cost=0.2),
            fields=(EffortField.EFFORT_COST,),
        ),
        domain_adapter(domain_view("b", "epistemic", 0.8)),
        *effort_adapter(
            admitted_effort("b", cost=0.7),
            fields=(EffortField.EFFORT_COST,),
        ),
    )
    result = m.select_by_partial_order(
        candidate_target_ids=("a", "b"),
        family_views=views,
        policy=partial_policy(
            ("epistemic", "BENEFIT"),
            ("effort_cost", "COST"),
        ),
    )
    assert result.selected_target_id == "a"


def test_duplicate_target_family_across_legacy_and_generic_is_rejected():
    adapter = public("comparison_family_from_domain")
    legacy = domain_view("a", "epistemic", 0.8)
    generic = adapter(legacy)

    with pytest.raises(ValueError):
        m.select_by_partial_order(
            candidate_target_ids=("a",),
            family_views=(legacy, generic),
            policy=partial_policy(("epistemic", "BENEFIT")),
        )


def test_feasibility_wrapper_accepts_generic_comparison_views():
    adapter = public("comparison_family_from_domain")
    views = (
        adapter(domain_view("a", "epistemic", 0.9)),
        adapter(domain_view("a", "effort_cost", 0.2)),
    )
    result = m.select_with_feasibility(
        candidate_target_ids=("a",),
        family_views=views,
        feasibility_assessments=(feasible("a"),),
        policy=partial_policy(
            ("epistemic", "BENEFIT"),
            ("effort_cost", "COST"),
        ),
        admission_policy=feasibility_policy(),
    )
    assert result.selected_target_id == "a"


def test_legacy_v2_selection_remains_unchanged():
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
