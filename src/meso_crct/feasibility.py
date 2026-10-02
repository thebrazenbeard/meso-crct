"""Outcome feasibility appraisals kept separate from desirability."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import math

from .evidence import EvidenceRef


class FeasibilityState(str, Enum):
    FEASIBLE = "feasible"
    INFEASIBLE = "infeasible"
    UNKNOWN = "unknown"
    CONDITIONAL = "conditional"


def _optional_unit(value: float | None, *, name: str) -> float | None:
    if value is None:
        return None
    value = float(value)
    if not math.isfinite(value) or value < 0.0 or value > 1.0:
        raise ValueError(f"{name} must be finite and within [0, 1]")
    return value


@dataclass(frozen=True, slots=True)
class FeasibilityAssessment:
    target_id: str
    state: FeasibilityState
    evidence: EvidenceRef
    expected_success: float | None = None
    uncertainty: float | None = None
    controllability: float | None = None
    delay_seconds: float | None = None

    def __post_init__(self) -> None:
        if not self.target_id.strip():
            raise ValueError("target_id must be non-empty")
        if self.evidence.subject_id != self.target_id:
            raise ValueError("feasibility evidence subject must match target_id")
        object.__setattr__(
            self,
            "expected_success",
            _optional_unit(self.expected_success, name="expected_success"),
        )
        object.__setattr__(
            self,
            "uncertainty",
            _optional_unit(self.uncertainty, name="uncertainty"),
        )
        object.__setattr__(
            self,
            "controllability",
            _optional_unit(self.controllability, name="controllability"),
        )
        if self.delay_seconds is not None:
            delay = float(self.delay_seconds)
            if not math.isfinite(delay) or delay < 0.0:
                raise ValueError("delay_seconds must be finite and >= 0")
            object.__setattr__(self, "delay_seconds", delay)
