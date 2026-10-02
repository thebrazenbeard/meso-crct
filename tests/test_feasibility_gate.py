import pytest

import meso_crct as m


def public(name: str):
    assert hasattr(m, name), f"missing public feasibility-gate interface: {name}"
    return getattr(m, name)


def evidence(
    target_id: str,
    *,
    source_id="feasibility:1",
    currentness=None,
):
    if currentness is None:
        currentness = m.EvidenceCurrentness.CURRENT
    return m.EvidenceRef(
        producer_id="planner:feasibility",
        producer_revision="v1",
        subject_id=target_id,
        source_id=source_id,
        currentness=currentness,
    )


def assessment(
    target_id: str,
    state_name: str,
    *,
    source_id="feasibility:1",
    currentness=None,
):
    return m.FeasibilityAssessment(
        target_id=target_id,
        state=getattr(m.FeasibilityState, state_name),
        evidence=evidence(
            target_id,
            source_id=source_id,
            currentness=currentness,
        ),
    )


def view(target_id: str, family_id: str, magnitude: float):
    return m.ContributionFamilyView(
        target_id=target_id,
        family_id=family_id,
        magnitude=magnitude,
        support_count=1,
        contribution_kinds=(family_id,),
        source_ids=(f"src:{target_id}:{family_id}",),
    )


def admission_policy():
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


def comparison_policy():
    return m.PartialOrderPolicy(
        policy_id="policy:test",
        policy_revision="r1",
        families=(
            m.FamilyComparisonSpec(
                family_id="epistemic",
                direction=m.FamilyDirection.BENEFIT,
            ),
            m.FamilyComparisonSpec(
                family_id="effort_cost",
                direction=m.FamilyDirection.COST,
            ),
        ),
    )


def gate(candidates, assessments):
    fn = public("gate_by_feasibility")
    return fn(
        candidate_target_ids=tuple(candidates),
        assessments=tuple(assessments),
        admission_policy=admission_policy(),
    )


def choose(candidates, views, assessments):
    fn = public("select_with_feasibility")
    return fn(
        candidate_target_ids=tuple(candidates),
        family_views=tuple(views),
        feasibility_assessments=tuple(assessments),
        policy=comparison_policy(),
        admission_policy=admission_policy(),
    )


def test_feasibility_assessment_binds_evidence_subject_to_target():
    with pytest.raises(ValueError):
        m.FeasibilityAssessment(
            target_id="target:a",
            state=m.FeasibilityState.FEASIBLE,
            evidence=evidence("target:b"),
        )


def test_current_feasible_is_admitted():
    result = gate(("a",), (assessment("a", "FEASIBLE"),))
    assert result.admitted_target_ids == ("a",)
    assert result.infeasible_target_ids == ()
    assert result.deferred_target_ids == ()


def test_current_infeasible_is_excluded():
    result = gate(("a",), (assessment("a", "INFEASIBLE"),))
    assert result.admitted_target_ids == ()
    assert result.infeasible_target_ids == ("a",)
    assert result.deferred_target_ids == ()


@pytest.mark.parametrize("state_name", ["UNKNOWN", "CONDITIONAL"])
def test_unknown_and_conditional_are_deferred(state_name):
    result = gate(("a",), (assessment("a", state_name),))
    assert result.admitted_target_ids == ()
    assert result.infeasible_target_ids == ()
    assert result.deferred_target_ids == ("a",)


@pytest.mark.parametrize(
    "state_name,currentness",
    [
        ("FEASIBLE", m.EvidenceCurrentness.STALE),
        ("INFEASIBLE", m.EvidenceCurrentness.STALE),
        ("FEASIBLE", m.EvidenceCurrentness.UNKNOWN),
        ("INFEASIBLE", m.EvidenceCurrentness.UNKNOWN),
    ],
)
def test_noncurrent_assessment_is_deferred_regardless_of_state(
    state_name,
    currentness,
):
    result = gate(
        ("a",),
        (
            assessment(
                "a",
                state_name,
                currentness=currentness,
            ),
        ),
    )
    assert result.admitted_target_ids == ()
    assert result.infeasible_target_ids == ()
    assert result.deferred_target_ids == ("a",)


def test_missing_assessment_is_deferred_and_reported():
    result = gate(("a",), ())
    assert result.deferred_target_ids == ("a",)
    assert result.missing_assessment_target_ids == ("a",)


def test_duplicate_assessment_for_target_is_rejected():
    with pytest.raises(ValueError):
        gate(
            ("a",),
            (
                assessment("a", "FEASIBLE", source_id="f:1"),
                assessment("a", "FEASIBLE", source_id="f:2"),
            ),
        )


def test_assessment_for_noncandidate_target_is_rejected():
    with pytest.raises(ValueError):
        gate(
            ("a",),
            (assessment("b", "FEASIBLE"),),
        )


def test_gate_digest_is_order_stable_and_changes_with_state():
    first = gate(
        ("a", "b"),
        (
            assessment("a", "FEASIBLE", source_id="f:a"),
            assessment("b", "INFEASIBLE", source_id="f:b"),
        ),
    )
    reordered = gate(
        ("b", "a"),
        (
            assessment("b", "INFEASIBLE", source_id="f:b"),
            assessment("a", "FEASIBLE", source_id="f:a"),
        ),
    )
    changed = gate(
        ("a", "b"),
        (
            assessment("a", "FEASIBLE", source_id="f:a"),
            assessment("b", "UNKNOWN", source_id="f:b"),
        ),
    )
    assert hasattr(first, "gate_input_digest")
    assert first.gate_input_digest == reordered.gate_input_digest
    assert first.gate_input_digest != changed.gate_input_digest


def test_unique_feasible_winner_plus_deferred_target_is_deferred():
    FeasibilityAwareStatus = public("FeasibilityAwareStatus")
    result = choose(
        ("a", "b"),
        (
            view("a", "epistemic", 0.9),
            view("a", "effort_cost", 0.2),
            view("b", "epistemic", 0.2),
            view("b", "effort_cost", 0.9),
        ),
        (
            assessment("a", "FEASIBLE", source_id="f:a"),
            assessment("b", "UNKNOWN", source_id="f:b"),
        ),
    )
    assert result.status is FeasibilityAwareStatus.DEFERRED
    assert result.selected_target_id is None
    assert result.provisional_frontier_target_ids == ("a",)
    assert result.deferred_target_ids == ("b",)


def test_all_current_infeasible_yields_no_admissible_candidate():
    FeasibilityAwareStatus = public("FeasibilityAwareStatus")
    result = choose(
        ("a", "b"),
        (
            view("a", "epistemic", 0.9),
            view("a", "effort_cost", 0.2),
            view("b", "epistemic", 0.8),
            view("b", "effort_cost", 0.3),
        ),
        (
            assessment("a", "INFEASIBLE", source_id="f:a"),
            assessment("b", "INFEASIBLE", source_id="f:b"),
        ),
    )
    assert result.status is FeasibilityAwareStatus.NO_ADMISSIBLE_CANDIDATE
    assert result.selected_target_id is None
    assert set(result.infeasible_target_ids) == {"a", "b"}


def test_all_resolved_unique_pareto_winner_is_selected():
    FeasibilityAwareStatus = public("FeasibilityAwareStatus")
    result = choose(
        ("a", "b"),
        (
            view("a", "epistemic", 0.9),
            view("a", "effort_cost", 0.2),
            view("b", "epistemic", 0.6),
            view("b", "effort_cost", 0.4),
        ),
        (
            assessment("a", "FEASIBLE", source_id="f:a"),
            assessment("b", "FEASIBLE", source_id="f:b"),
        ),
    )
    assert result.status is FeasibilityAwareStatus.SELECTED
    assert result.selected_target_id == "a"
    assert result.provisional_frontier_target_ids == ("a",)


def test_all_resolved_pareto_tradeoff_remains_incomparable():
    FeasibilityAwareStatus = public("FeasibilityAwareStatus")
    result = choose(
        ("a", "b"),
        (
            view("a", "epistemic", 0.9),
            view("a", "effort_cost", 0.8),
            view("b", "epistemic", 0.6),
            view("b", "effort_cost", 0.2),
        ),
        (
            assessment("a", "FEASIBLE", source_id="f:a"),
            assessment("b", "FEASIBLE", source_id="f:b"),
        ),
    )
    assert result.status is FeasibilityAwareStatus.INCOMPARABLE
    assert result.selected_target_id is None
    assert set(result.provisional_frontier_target_ids) == {"a", "b"}


def test_infeasible_and_deferred_family_evidence_is_not_rewritten():
    original = (
        view("a", "epistemic", 0.9),
        view("a", "effort_cost", 0.2),
        view("b", "epistemic", 0.2),
        view("b", "effort_cost", 0.9),
    )
    result = choose(
        ("a", "b"),
        original,
        (
            assessment("a", "INFEASIBLE", source_id="f:a"),
            assessment("b", "UNKNOWN", source_id="f:b"),
        ),
    )
    assert original[0].magnitude == 0.9
    assert original[1].magnitude == 0.2
    assert original[2].magnitude == 0.2
    assert original[3].magnitude == 0.9
    assert result.infeasible_target_ids == ("a",)
    assert result.deferred_target_ids == ("b",)


def test_wrapper_preserves_gate_partial_digest_and_policy_identity():
    result = choose(
        ("a",),
        (
            view("a", "epistemic", 0.9),
            view("a", "effort_cost", 0.2),
        ),
        (assessment("a", "FEASIBLE"),),
    )
    assert result.feasibility_input_digest
    assert result.partial_order_input_digest
    assert result.policy_id == "policy:test"
    assert result.policy_revision == "r1"
    assert result.admission_policy_id == "host:feasibility"
    assert result.admission_policy_revision == "r1"


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


def test_feasibility_gate_requires_external_producer_admission_policy():
    import inspect

    FeasibilityProducerSpec = public("FeasibilityProducerSpec")
    FeasibilityAdmissionPolicy = public("FeasibilityAdmissionPolicy")
    Unadmitted = public("UnadmittedFeasibilityAssessment")

    parameters = inspect.signature(m.gate_by_feasibility).parameters
    assert "admission_policy" in parameters
    assert parameters["admission_policy"].default is inspect.Parameter.empty

    trusted = FeasibilityAdmissionPolicy(
        policy_id="host:feasibility",
        policy_revision="r1",
        producers=(
            FeasibilityProducerSpec(
                producer_id="planner:feasibility",
                producer_revision="v1",
            ),
        ),
    )
    spoofed = m.FeasibilityAssessment(
        target_id="a",
        state=m.FeasibilityState.FEASIBLE,
        evidence=m.EvidenceRef(
            producer_id="planner:spoof",
            producer_revision="v1",
            subject_id="a",
            source_id="f:spoof",
            currentness=m.EvidenceCurrentness.CURRENT,
        ),
    )

    with pytest.raises(Unadmitted):
        m.gate_by_feasibility(
            candidate_target_ids=("a",),
            assessments=(spoofed,),
            admission_policy=trusted,
        )


def test_wrapper_digest_binds_all_family_inputs_including_deferred_targets():
    base_views = (
        view("a", "epistemic", 0.9),
        view("a", "effort_cost", 0.2),
        view("b", "epistemic", 0.2),
        view("b", "effort_cost", 0.9),
    )
    assessments = (
        assessment("a", "FEASIBLE", source_id="f:a"),
        assessment("b", "UNKNOWN", source_id="f:b"),
    )
    first = choose(("a", "b"), base_views, assessments)
    changed_deferred_view = choose(
        ("a", "b"),
        (
            view("a", "epistemic", 0.9),
            view("a", "effort_cost", 0.2),
            view("b", "epistemic", 0.7),
            view("b", "effort_cost", 0.9),
        ),
        assessments,
    )
    reordered = choose(
        ("b", "a"),
        tuple(reversed(base_views)),
        tuple(reversed(assessments)),
    )

    assert hasattr(first, "decision_input_digest")
    assert first.decision_input_digest == reordered.decision_input_digest
    assert first.decision_input_digest != changed_deferred_view.decision_input_digest
