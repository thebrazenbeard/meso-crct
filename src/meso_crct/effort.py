"""Effort appraisal kept separate from value and execution authority."""

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
class EffortAssessment:
    target_id: str
    evidence: EvidenceRef
    required_effort: float
    effort_cost: float
    willingness_to_exert: float
    vigor_proposal: float | None = None

    def __post_init__(self) -> None:
        if not self.target_id.strip():
            raise ValueError("target_id must be non-empty")
        for name in ("required_effort", "effort_cost", "willingness_to_exert"):
            object.__setattr__(self, name, _unit(getattr(self, name), name=name))
        if self.vigor_proposal is not None:
            object.__setattr__(
                self,
                "vigor_proposal",
                _unit(self.vigor_proposal, name="vigor_proposal"),
            )
