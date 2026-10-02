"""Normalize domain contributions by registered semantic family."""

from __future__ import annotations

from dataclasses import dataclass

from .domain import DomainContribution
from .evidence import EvidenceCurrentness


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


@dataclass(frozen=True, slots=True)
class ContributionFamilyView:
    target_id: str
    family_id: str
    magnitude: float
    support_count: int
    contribution_kinds: tuple[str, ...]
    source_ids: tuple[str, ...]


def aggregate_domain_contributions(
    contributions: tuple[DomainContribution, ...] | list[DomainContribution],
    registry: ContributionRegistry,
) -> tuple[ContributionFamilyView, ...]:
    grouped: dict[tuple[str, str], list[DomainContribution]] = {}

    for contribution in contributions:
        if contribution.evidence.currentness is not EvidenceCurrentness.CURRENT:
            raise InadmissibleContributionEvidence(
                "domain contribution evidence must be CURRENT"
            )
        spec = registry.resolve(contribution)
        grouped.setdefault((contribution.target_id, spec.family_id), []).append(
            contribution
        )

    views: list[ContributionFamilyView] = []
    for (target_id, family_id), members in sorted(grouped.items()):
        views.append(
            ContributionFamilyView(
                target_id=target_id,
                family_id=family_id,
                magnitude=max(member.magnitude for member in members),
                support_count=len(members),
                contribution_kinds=tuple(
                    sorted({member.contribution_kind for member in members})
                ),
                source_ids=tuple(
                    sorted({member.evidence.source_id for member in members})
                ),
            )
        )
    return tuple(views)
