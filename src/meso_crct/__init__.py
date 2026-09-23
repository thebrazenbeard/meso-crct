"""meso-crct synthetic salience/reward/valuation primitives."""

from .adversarial import ProbeResult, run_reference_probes
from .allocation import (
    AllocationAudit,
    AllocationSample,
    GoalObligation,
    audit_attention_budget,
)
from .arbitration import ArbitrationDecision, ArbitrationMode, arbitrate
from .circuit import CircuitState
from .dynamics import DynamicsConfig, advance_without_input, decay_toward
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
from .homeostasis import (
    HomeostaticModulation,
    HomeostaticState,
    NeedAffordance,
    NeedAxis,
    modulate_incentive_salience,
)
from .plasticity import (
    PlasticityCandidate,
    PlasticityPolicy,
    preview_association_strength,
    propose_plasticity,
)
from .provenance import (
    Provenance,
    ProvenanceVerificationError,
    ProvenanceVerifier,
    SourceKind,
    TransitionReceipt,
    VerifiedProvenance,
    state_fingerprint,
)
from .runtime import (
    RuntimeFrame,
    RuntimePhase,
    classify_phase,
    evaluate_transition,
    frame,
)
from .salience import LearningState, RecruitmentState, SalienceState, SignalKind
from .semantic import SemanticAssessment, SemanticEvidence, assess_semantic_relevance
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
    "DynamicsConfig",
    "decay_toward",
    "advance_without_input",
    "NeedAxis",
    "NeedAffordance",
    "HomeostaticState",
    "HomeostaticModulation",
    "modulate_incentive_salience",
    "ArbitrationMode",
    "ArbitrationDecision",
    "arbitrate",
    "GoalObligation",
    "AllocationSample",
    "AllocationAudit",
    "audit_attention_budget",
    "SourceKind",
    "Provenance",
    "VerifiedProvenance",
    "ProvenanceVerifier",
    "ProvenanceVerificationError",
    "TransitionReceipt",
    "state_fingerprint",
    "RuntimePhase",
    "RuntimeFrame",
    "classify_phase",
    "frame",
    "evaluate_transition",
    "PlasticityPolicy",
    "PlasticityCandidate",
    "propose_plasticity",
    "preview_association_strength",
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
    "SemanticEvidence",
    "SemanticAssessment",
    "assess_semantic_relevance",
]
