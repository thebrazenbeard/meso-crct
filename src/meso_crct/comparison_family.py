"""Neutral decision-facing semantic-family views and source adapters."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
import math

from .domain_aggregation import ContributionFamilyView
from .effort_admission import AdmittedEffortAssessment


_COMPARISON_VIEW_TOKEN = object()


class ComparisonFamilySourceKind(str, Enum):
    DOMAIN_AGGREGATE = "domain_aggregate"
    LEGACY_DOMAIN_VIEW = "legacy_domain_view"
    EFFORT_APPRAISAL = "effort_appraisal"


class EffortComparisonField(str, Enum):
    REQUIRED_EFFORT = "required_effort"
    EFFORT_COST = "effort_cost"
    WILLINGNESS_TO_EXERT = "willingness_to_exert"


@dataclass(frozen=True, slots=True, init=False)
class ComparisonFamilyView:
    target_id: str
    family_id: str
    magnitude: float
    source_kind: ComparisonFamilySourceKind
    source_digest: str

    def __init__(
        self,
        *,
        target_id: str,
        family_id: str,
        magnitude: float,
        source_kind: ComparisonFamilySourceKind,
        source_digest: str,
        _token: object | None = None,
    ) -> None:
        if _token is not _COMPARISON_VIEW_TOKEN:
            raise TypeError(
                "ComparisonFamilyView must be created by an admitted source adapter"
            )
        if not target_id.strip():
            raise ValueError("target_id must be non-empty")
        if not family_id.strip():
            raise ValueError("family_id must be non-empty")
        value = float(magnitude)
        if not math.isfinite(value) or value < 0.0 or value > 1.0:
            raise ValueError("magnitude must be finite and within [0, 1]")
        if not source_digest.strip():
            raise ValueError("source_digest must be non-empty")

        object.__setattr__(self, "target_id", target_id)
        object.__setattr__(self, "family_id", family_id)
        object.__setattr__(self, "magnitude", value)
        object.__setattr__(self, "source_kind", source_kind)
        object.__setattr__(self, "source_digest", source_digest)


def _digest(payload: object) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def comparison_family_from_domain(
    view: ContributionFamilyView,
) -> ComparisonFamilyView:
    if not isinstance(view, ContributionFamilyView):
        raise TypeError("view must be a ContributionFamilyView")
    if not view.target_id.strip():
        raise ValueError("domain family target_id must be non-empty")
    if not view.family_id.strip():
        raise ValueError("domain family family_id must be non-empty")
    magnitude = float(view.magnitude)
    if not math.isfinite(magnitude) or magnitude < 0.0 or magnitude > 1.0:
        raise ValueError(
            "domain family magnitude must be finite and within [0, 1]"
        )
    if view.support_count < 1:
        raise ValueError("domain family support_count must be >= 1")
    if any(not value.strip() for value in view.contribution_kinds):
        raise ValueError("domain contribution kinds must be non-empty")
    if any(not value.strip() for value in view.source_ids):
        raise ValueError("domain source IDs must be non-empty")

    if view.aggregation_digest:
        source_kind = ComparisonFamilySourceKind.DOMAIN_AGGREGATE
        source_digest = view.aggregation_digest
    else:
        source_kind = ComparisonFamilySourceKind.LEGACY_DOMAIN_VIEW
        source_digest = _digest(
            {
                "source_kind": source_kind.value,
                "target_id": view.target_id,
                "family_id": view.family_id,
                "magnitude": magnitude,
                "support_count": view.support_count,
                "contribution_kinds": sorted(view.contribution_kinds),
                "source_ids": sorted(view.source_ids),
            }
        )

    return ComparisonFamilyView(
        target_id=view.target_id,
        family_id=view.family_id,
        magnitude=magnitude,
        source_kind=source_kind,
        source_digest=source_digest,
        _token=_COMPARISON_VIEW_TOKEN,
    )


def comparison_families_from_effort(
    assessment: AdmittedEffortAssessment,
    *,
    fields: tuple[EffortComparisonField, ...],
) -> tuple[ComparisonFamilyView, ...]:
    if not isinstance(assessment, AdmittedEffortAssessment):
        raise TypeError(
            "effort comparison projection requires AdmittedEffortAssessment"
        )
    if len(fields) != len(set(fields)):
        raise ValueError("effort comparison fields must be unique")

    views: list[ComparisonFamilyView] = []
    for field in fields:
        if not isinstance(field, EffortComparisonField):
            raise TypeError("fields must contain EffortComparisonField values")
        magnitude = float(getattr(assessment, field.value))
        source_digest = _digest(
            {
                "source_kind": ComparisonFamilySourceKind.EFFORT_APPRAISAL.value,
                "target_id": assessment.target_id,
                "family_id": field.value,
                "magnitude": magnitude,
                "admission_input_digest": assessment.admission_input_digest,
                "admission_policy_id": assessment.admission_policy_id,
                "admission_policy_revision": assessment.admission_policy_revision,
                "field": field.value,
            }
        )
        views.append(
            ComparisonFamilyView(
                target_id=assessment.target_id,
                family_id=field.value,
                magnitude=magnitude,
                source_kind=ComparisonFamilySourceKind.EFFORT_APPRAISAL,
                source_digest=source_digest,
                _token=_COMPARISON_VIEW_TOKEN,
            )
        )
    return tuple(views)


def as_comparison_family_view(
    view: ComparisonFamilyView | ContributionFamilyView,
) -> ComparisonFamilyView:
    if isinstance(view, ComparisonFamilyView):
        return view
    if isinstance(view, ContributionFamilyView):
        return comparison_family_from_domain(view)
    raise TypeError(
        "family view must be ComparisonFamilyView or ContributionFamilyView"
    )
