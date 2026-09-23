"""Append-only review state for learned associations.

Review state does not alter learned strength or erase learning history. It gates
whether an exact learned revision is currently admitted for recall.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import hashlib
import json


class ReviewDisposition(StrEnum):
    ACTIVE = "active"
    QUARANTINED = "quarantined"


class ReviewAdmission(StrEnum):
    ADMITTED = "admitted"
    QUARANTINED = "quarantined"
    STALE = "stale"


class ReviewNoOpError(ValueError):
    pass


class ReviewIntegrityError(ValueError):
    pass


class AssociationQuarantinedError(ValueError):
    pass


class AssociationReviewStaleError(ValueError):
    pass


_REVIEW_RECORD_TOKEN = object()


@dataclass(frozen=True, slots=True, init=False)
class AssociationReviewRecord:
    association_id: str
    review_version: int
    memory_revision_id: str
    disposition: ReviewDisposition
    reason: str
    parent_review_id: str | None
    review_id: str

    def __init__(
        self,
        *,
        association_id: str,
        review_version: int,
        memory_revision_id: str,
        disposition: ReviewDisposition,
        reason: str,
        parent_review_id: str | None,
        review_id: str,
        _token: object | None = None,
    ) -> None:
        if _token is not _REVIEW_RECORD_TOKEN:
            raise TypeError(
                "AssociationReviewRecord must be created by AssociationReviewRegistry"
            )
        for name, value in (
            ("association_id", association_id),
            ("memory_revision_id", memory_revision_id),
            ("reason", reason),
            ("review_id", review_id),
        ):
            if not value.strip():
                raise ValueError(f"{name} must be non-empty")
        if review_version < 1:
            raise ValueError("review_version must be >= 1")
        object.__setattr__(self, "association_id", association_id)
        object.__setattr__(self, "review_version", review_version)
        object.__setattr__(self, "memory_revision_id", memory_revision_id)
        object.__setattr__(self, "disposition", disposition)
        object.__setattr__(self, "reason", reason)
        object.__setattr__(self, "parent_review_id", parent_review_id)
        object.__setattr__(self, "review_id", review_id)


def _review_id(
    *,
    association_id: str,
    review_version: int,
    memory_revision_id: str,
    disposition: ReviewDisposition,
    reason: str,
    parent_review_id: str | None,
) -> str:
    payload = json.dumps(
        {
            "association_id": association_id,
            "review_version": review_version,
            "memory_revision_id": memory_revision_id,
            "disposition": disposition.value,
            "reason": reason,
            "parent_review_id": parent_review_id,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class AssociationReviewRegistry:
    records: tuple[AssociationReviewRecord, ...] = ()

    def __post_init__(self) -> None:
        latest: dict[str, AssociationReviewRecord] = {}
        for record in self.records:
            prior = latest.get(record.association_id)
            expected_version = 1 if prior is None else prior.review_version + 1
            expected_parent = None if prior is None else prior.review_id
            if record.review_version != expected_version:
                raise ReviewIntegrityError(
                    f"invalid review version chain for {record.association_id}"
                )
            if record.parent_review_id != expected_parent:
                raise ReviewIntegrityError(
                    f"invalid review parent for {record.association_id}"
                )
            expected_id = _review_id(
                association_id=record.association_id,
                review_version=record.review_version,
                memory_revision_id=record.memory_revision_id,
                disposition=record.disposition,
                reason=record.reason,
                parent_review_id=record.parent_review_id,
            )
            if record.review_id != expected_id:
                raise ReviewIntegrityError(
                    f"invalid review digest for {record.association_id}"
                )
            latest[record.association_id] = record

    def current(self, association_id: str) -> AssociationReviewRecord | None:
        for record in reversed(self.records):
            if record.association_id == association_id:
                return record
        return None

    def history(self, association_id: str) -> tuple[AssociationReviewRecord, ...]:
        return tuple(
            record
            for record in self.records
            if record.association_id == association_id
        )

    def admission(
        self,
        *,
        association_id: str,
        memory_revision_id: str,
    ) -> ReviewAdmission:
        record = self.current(association_id)
        if record is None:
            return ReviewAdmission.ADMITTED
        if record.memory_revision_id != memory_revision_id:
            return ReviewAdmission.STALE
        if record.disposition is ReviewDisposition.QUARANTINED:
            return ReviewAdmission.QUARANTINED
        return ReviewAdmission.ADMITTED

    def quarantine(
        self,
        *,
        association_id: str,
        memory_revision_id: str,
        reason: str,
    ) -> "AssociationReviewRegistry":
        return self._append(
            association_id=association_id,
            memory_revision_id=memory_revision_id,
            disposition=ReviewDisposition.QUARANTINED,
            reason=reason,
        )

    def release(
        self,
        *,
        association_id: str,
        memory_revision_id: str,
        reason: str,
    ) -> "AssociationReviewRegistry":
        return self._append(
            association_id=association_id,
            memory_revision_id=memory_revision_id,
            disposition=ReviewDisposition.ACTIVE,
            reason=reason,
        )

    def _append(
        self,
        *,
        association_id: str,
        memory_revision_id: str,
        disposition: ReviewDisposition,
        reason: str,
    ) -> "AssociationReviewRegistry":
        if not association_id.strip():
            raise ValueError("association_id must be non-empty")
        if not memory_revision_id.strip():
            raise ValueError("memory_revision_id must be non-empty")
        if not reason.strip():
            raise ValueError("reason must be non-empty")

        prior = self.current(association_id)
        if (
            prior is not None
            and prior.memory_revision_id == memory_revision_id
            and prior.disposition is disposition
        ):
            raise ReviewNoOpError(
                "review state already matches this exact memory revision"
            )

        review_version = 1 if prior is None else prior.review_version + 1
        parent_review_id = None if prior is None else prior.review_id
        review_id = _review_id(
            association_id=association_id,
            review_version=review_version,
            memory_revision_id=memory_revision_id,
            disposition=disposition,
            reason=reason,
            parent_review_id=parent_review_id,
        )
        record = AssociationReviewRecord(
            association_id=association_id,
            review_version=review_version,
            memory_revision_id=memory_revision_id,
            disposition=disposition,
            reason=reason,
            parent_review_id=parent_review_id,
            review_id=review_id,
            _token=_REVIEW_RECORD_TOKEN,
        )
        return AssociationReviewRegistry(records=self.records + (record,))
