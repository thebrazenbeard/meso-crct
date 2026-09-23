"""meso-crct synthetic salience/reward/valuation primitives."""

from .adversarial import ProbeResult, run_reference_probes
from .arbitration import ArbitrationDecision, ArbitrationMode, arbitrate
from .circuit import CircuitState
from .evaluation_env import (
    EvalAction,
    EvalStep,
    ProxyTrapEnvironment,
    SensitizationReport,
    TrajectoryAudit,
    audit_trajectory,
    derive_epistemic_value,
    detect_incentive_hedonic_divergence,
)
from .provenance import Provenance, SourceKind, TransitionReceipt, state_fingerprint
from .runtime import (
    RuntimeFrame,
    RuntimePhase,
    classify_phase,
    evaluate_transition,
    frame,
)
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
    "ArbitrationMode",
    "ArbitrationDecision",
    "arbitrate",
    "SourceKind",
    "Provenance",
    "TransitionReceipt",
    "state_fingerprint",
    "RuntimePhase",
    "RuntimeFrame",
    "classify_phase",
    "frame",
    "evaluate_transition",
    "ProbeResult",
    "run_reference_probes",
    "EvalAction",
    "EvalStep",
    "ProxyTrapEnvironment",
    "TrajectoryAudit",
    "SensitizationReport",
    "audit_trajectory",
    "derive_epistemic_value",
    "detect_incentive_hedonic_divergence",
]
