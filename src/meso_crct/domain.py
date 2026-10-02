"""Domain-local motivational contributions for shared MESO arbitration."""

from __future__ import annotations

from dataclasses import dataclass
import math

from .evidence import EvidenceRef


def _unit(value: float, *, name: str) -> float:
    value = float(value)
    if not math.isfinite(value) or value < 0.0 or value > 1.0:
        raise ValueError(f"{name} must be finite and within [0, 1]")
    return value


@dataclass(frozen=True, slots=True)
class DomainContribution:
    domain_id: str
    profile_revision: str
    target_id: str
    contribution_kind: str
    magnitude: float
    evidence: EvidenceRef
    direction: str | None = None

    def __post_init__(self) -> None:
        for name in ("domain_id", "profile_revision", "target_id", "contribution_kind"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        object.__setattr__(self, "magnitude", _unit(self.magnitude, name="magnitude"))
        if self.direction is not None and not self.direction.strip():
            raise ValueError("direction must be non-empty when provided")
