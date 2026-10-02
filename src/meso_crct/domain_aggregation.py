"""Normalize domain contributions by registered semantic family."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math

from .domain import DomainContribution
from .evidence import EvidenceCurrentness


_AGGREGATION_VIEW_TOKEN = object()


class UnknownContributionKind(ValueError):
    pass


class InadmissibleContributionEvidence(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class ContributionKindSpec:
    domain_id: str
    profile_revision: str
    contribution_kind: str
    family_id: str
    producer_id: str
    producer_revision: str

    def __post_init__(self) -> None:
        for name in (
            "domain_id",
            "profile_revision",
            "contribution_kind",
            "family_id",
            "producer_id",
            "producer_revision",
        ):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")

    @property
    def key(self) -> tuple[str, str, str]:
        return (self.domain_id, self.profile_revision, self.contribution_kind)


@dataclass(frozen=True, slots=True)
class ContributionRegistry:
    specs: tuple[ContributionKindSpec, ...] = ()

    def __post_init__(self) -> None:
        keys = tuple(spec.key for spec in self.specs)
        if len(keys) != len(set(keys)):
            raise ValueError("contribution registry keys must be unique")

    def resolve(self, contribution: DomainContribution) -> ContributionKindSpec:
        key = (
            contribution.domain_id,
            contribution.profile_revision,
            contribution.contribution_kind,
        )
        for spec in self.specs:
            if spec.key != key:
                continue
            if contribution.evidence.producer_id != spec.producer_id:
                raise InadmissibleContributionEvidence(
                    "domain contribution evidence producer does not match registry"
                )
            if contribution.evidence.producer_revision != spec.producer_revision:
                raise InadmissibleContributionEvidence(
                    "domain contribution evidence revision does not match registry"
                )
            return spec
        raise UnknownContributionKind(
            "unregistered contribution kind: "
            f"{contribution.domain_id}/{contribution.profile_revision}/"
            f"{contribution.contribution_kind}"
        )


@dataclass(frozen=True, slots=True, init=False)
class ContributionFamilyView:
    target_id: str
    family_id: str
    magnitude: float
    support_count: int
    contribution_kinds: tuple[str, ...]
    source_ids: tuple[str, ...]
    aggregation_digest: str | None

    def __init__(
        self,
        *,
        target_id: str,
        family_id: str,
        magnitude: float,
        support_count: int,
        contribution_kinds: tuple[str, ...],
        source_ids: tuple[str, ...],
        aggregation_digest: str | None = None,
        _token: object | None = None,
    ) -> None:
        if not target_id.strip():
            raise ValueError("target_id must be non-empty")
        if not family_id.strip():
            raise ValueError("family_id must be non-empty")
        value = float(magnitude)
        if not math.isfinite(value) or value < 0.0 or value > 1.0:
            raise ValueError("magnitude must be finite and within [0, 1]")
        if support_count < 1:
            raise ValueError("support_count must be >= 1")
        if any(not item.strip() for item in contribution_kinds):
            raise ValueError("contribution_kinds must be non-empty strings")
        if any(not item.strip() for item in source_ids):
            raise ValueError("source_ids must be non-empty strings")
        if aggregation_digest is not None:
            if _token is not _AGGREGATION_VIEW_TOKEN:
                raise TypeError(
                    "aggregation_digest may only be issued by "
                    "aggregate_domain_contributions"
                )
            if not aggregation_digest.strip():
                raise ValueError("aggregation_digest must be non-empty")

        object.__setattr__(self, "target_id", target_id)
        object.__setattr__(self, "family_id", family_id)
        object.__setattr__(self, "magnitude", value)
        object.__setattr__(self, "support_count", int(support_count))
        object.__setattr__(self, "contribution_kinds", tuple(contribution_kinds))
        object.__setattr__(self, "source_ids", tuple(source_ids))
        object.__setattr__(self, "aggregation_digest", aggregation_digest)


def _aggregation_digest(
    *,
    target_id: str,
    family_id: str,
    magnitude: float,
    members: list[tuple[DomainContribution, ContributionKindSpec]],
) -> str:
    payload = {
        "target_id": target_id,
        "family_id": family_id,
        "magnitude": magnitude,
        "members": sorted(
            (
                {
                    "contribution": {
                        "domain_id": contribution.domain_id,
                        "profile_revision": contribution.profile_revision,
                        "target_id": contribution.target_id,
                        "contribution_kind": contribution.contribution_kind,
                        "magnitude": contribution.magnitude,
                        "direction": contribution.direction,
                        "evidence": {
                            "producer_id": contribution.evidence.producer_id,
                            "producer_revision": contribution.evidence.producer_revision,
                            "subject_id": contribution.evidence.subject_id,
                            "source_id": contribution.evidence.source_id,
                            "currentness": contribution.evidence.currentness.value,
                        },
                    },
                    "resolved_spec": {
                        "domain_id": spec.domain_id,
                        "profile_revision": spec.profile_revision,
                        "contribution_kind": spec.contribution_kind,
                        "family_id": spec.family_id,
                        "producer_id": spec.producer_id,
                        "producer_revision": spec.producer_revision,
                    },
                }
                for contribution, spec in members
            ),
            key=lambda item: json.dumps(
                item,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=True,
            ),
        ),
    }
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def aggregate_domain_contributions(
    contributions: tuple[DomainContribution, ...] | list[DomainContribution],
    registry: ContributionRegistry,
) -> tuple[ContributionFamilyView, ...]:
    grouped: dict[
        tuple[str, str],
        list[tuple[DomainContribution, ContributionKindSpec]],
    ] = {}

    for contribution in contributions:
        if contribution.evidence.currentness is not EvidenceCurrentness.CURRENT:
            raise InadmissibleContributionEvidence(
                "domain contribution evidence must be CURRENT"
            )
        spec = registry.resolve(contribution)
        grouped.setdefault((contribution.target_id, spec.family_id), []).append(
            (contribution, spec)
        )

    views: list[ContributionFamilyView] = []
    for (target_id, family_id), members in sorted(grouped.items()):
        contributions_only = tuple(member for member, _ in members)
        magnitude = max(member.magnitude for member in contributions_only)
        views.append(
            ContributionFamilyView(
                target_id=target_id,
                family_id=family_id,
                magnitude=magnitude,
                support_count=len(members),
                contribution_kinds=tuple(
                    sorted(
                        {
                            member.contribution_kind
                            for member in contributions_only
                        }
                    )
                ),
                source_ids=tuple(
                    sorted(
                        {
                            member.evidence.source_id
                            for member in contributions_only
                        }
                    )
                ),
                aggregation_digest=_aggregation_digest(
                    target_id=target_id,
                    family_id=family_id,
                    magnitude=magnitude,
                    members=members,
                ),
                _token=_AGGREGATION_VIEW_TOKEN,
            )
        )
    return tuple(views)
