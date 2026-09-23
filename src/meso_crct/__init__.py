"""meso-crct synthetic salience/reward/valuation primitives."""

from .circuit import CircuitState
from .salience import LearningState, RecruitmentState, SalienceState, SignalKind
from .state import (
    BASELINE_PLEASURE,
    MAX_PLEASURE,
    MIN_PLEASURE,
    RewardState,
    clamp_pleasure,
)

__all__ = [
    "BASELINE_PLEASURE",
    "MAX_PLEASURE",
    "MIN_PLEASURE",
    "RewardState",
    "clamp_pleasure",
    "SignalKind",
    "SalienceState",
    "LearningState",
    "RecruitmentState",
    "CircuitState",
]
