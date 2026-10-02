"""Provenance-bearing appraisal evidence primitives."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EvidenceCurrentness(str, Enum):
    CURRENT = "current"
    STALE = "stale"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class EvidenceRef:
    producer_id: str
    producer_revision: str
    subject_id: str
    source_id: str
    currentness: EvidenceCurrentness = EvidenceCurrentness.UNKNOWN

    def __post_init__(self) -> None:
        for name in ("producer_id", "producer_revision", "subject_id", "source_id"):
            value = getattr(self, name)
            if not value.strip():
                raise ValueError(f"{name} must be non-empty")
