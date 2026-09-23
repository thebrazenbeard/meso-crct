"""Minimal provenance and deterministic transition receipts."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
import hashlib
import json

from .arbitration import ArbitrationDecision
from .circuit import CircuitState


class SourceKind(StrEnum):
    ENVIRONMENT = "environment"
    MEMORY = "memory"
    INTERNAL_STATE = "internal_state"
    OPERATOR_INPUT = "operator_input"
    TEST_STIMULATION = "test_stimulation"
    REPLAY = "replay"
    DIRECT_REGISTER_WRITE = "direct_register_write"


@dataclass(frozen=True, slots=True)
class Provenance:
    source_kind: SourceKind
    source_id: str
    source_revision: str | None = None

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise ValueError("source_id must be non-empty")


def state_fingerprint(state: CircuitState) -> str:
    payload = json.dumps(asdict(state), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class TransitionReceipt:
    receipt_id: str
    before_phase: str
    after_phase: str
    mode: str
    priority: float
    dominant_driver: str | None
    supporting_drivers: tuple[str, ...]
    source_kind: str
    source_id: str
    source_revision: str | None
    before_fingerprint: str
    after_fingerprint: str

    @classmethod
    def build(
        cls,
        *,
        before: CircuitState,
        after: CircuitState,
        before_phase: str,
        after_phase: str,
        decision: ArbitrationDecision,
        provenance: Provenance,
    ) -> "TransitionReceipt":
        data = {
            "before_phase": before_phase,
            "after_phase": after_phase,
            "mode": decision.mode.value,
            "priority": decision.priority,
            "dominant_driver": decision.dominant_driver,
            "supporting_drivers": list(decision.supporting_drivers),
            "source_kind": provenance.source_kind.value,
            "source_id": provenance.source_id,
            "source_revision": provenance.source_revision,
            "before_fingerprint": state_fingerprint(before),
            "after_fingerprint": state_fingerprint(after),
        }
        canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
        receipt_id = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return cls(
            receipt_id=receipt_id,
            before_phase=before_phase,
            after_phase=after_phase,
            mode=decision.mode.value,
            priority=decision.priority,
            dominant_driver=decision.dominant_driver,
            supporting_drivers=decision.supporting_drivers,
            source_kind=provenance.source_kind.value,
            source_id=provenance.source_id,
            source_revision=provenance.source_revision,
            before_fingerprint=data["before_fingerprint"],
            after_fingerprint=data["after_fingerprint"],
        )
