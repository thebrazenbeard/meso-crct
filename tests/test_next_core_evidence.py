import pytest

import meso_crct as m


def public(name: str):
    assert hasattr(m, name), f"missing public next-core interface: {name}"
    return getattr(m, name)


def evidence(currentness_name: str = "CURRENT"):
    EvidenceCurrentness = public("EvidenceCurrentness")
    EvidenceRef = public("EvidenceRef")
    return EvidenceRef(
        producer_id="provider:resource",
        producer_revision="rev-1",
        subject_id="target:job",
        source_id="observation:1",
        currentness=getattr(EvidenceCurrentness, currentness_name),
    )


def test_feasibility_preserves_unknown_as_distinct_from_infeasible():
    FeasibilityState = public("FeasibilityState")
    FeasibilityAssessment = public("FeasibilityAssessment")

    unknown = FeasibilityAssessment(
        target_id="target:job",
        state=FeasibilityState.UNKNOWN,
        evidence=evidence("UNKNOWN"),
    )
    infeasible = FeasibilityAssessment(
        target_id="target:job",
        state=FeasibilityState.INFEASIBLE,
        evidence=evidence(),
    )

    assert unknown.state is FeasibilityState.UNKNOWN
    assert infeasible.state is FeasibilityState.INFEASIBLE
    assert unknown.state is not infeasible.state


def test_evidence_currentness_is_explicit_not_a_numeric_zero():
    EvidenceCurrentness = public("EvidenceCurrentness")
    current = evidence("CURRENT")
    stale = evidence("STALE")
    unknown = evidence("UNKNOWN")

    assert current.currentness is EvidenceCurrentness.CURRENT
    assert stale.currentness is EvidenceCurrentness.STALE
    assert unknown.currentness is EvidenceCurrentness.UNKNOWN
    assert not isinstance(unknown.currentness, (int, float))


def test_evidence_rejects_blank_identity_fields():
    EvidenceCurrentness = public("EvidenceCurrentness")
    EvidenceRef = public("EvidenceRef")

    for field in ("producer_id", "producer_revision", "subject_id", "source_id"):
        kwargs = dict(
            producer_id="provider:resource",
            producer_revision="rev-1",
            subject_id="target:job",
            source_id="observation:1",
            currentness=EvidenceCurrentness.CURRENT,
        )
        kwargs[field] = "   "
        with pytest.raises(ValueError):
            EvidenceRef(**kwargs)


def test_feasibility_probability_fields_are_bounded():
    FeasibilityState = public("FeasibilityState")
    FeasibilityAssessment = public("FeasibilityAssessment")

    with pytest.raises(ValueError):
        FeasibilityAssessment(
            target_id="target:job",
            state=FeasibilityState.FEASIBLE,
            evidence=evidence(),
            expected_success=1.1,
        )

    with pytest.raises(ValueError):
        FeasibilityAssessment(
            target_id="target:job",
            state=FeasibilityState.CONDITIONAL,
            evidence=evidence(),
            uncertainty=-0.1,
        )


def test_feasibility_rejects_negative_delay():
    FeasibilityState = public("FeasibilityState")
    FeasibilityAssessment = public("FeasibilityAssessment")

    with pytest.raises(ValueError):
        FeasibilityAssessment(
            target_id="target:job",
            state=FeasibilityState.FEASIBLE,
            evidence=evidence(),
            delay_seconds=-1.0,
        )
