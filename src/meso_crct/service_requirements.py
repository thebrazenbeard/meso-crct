"""Finite-horizon service requirements for admitted allocation obligations."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
import hashlib
import json
from typing import Iterable

from .allocation_attested import (
    AttestedAllocationAuditReceipt,
    UnadmittedAllocationObligation,
)
from .obligations import AdmittedGoalObligation


_OBLIGATION_SERVICE_REQUIREMENT_TOKEN = object()


class ServiceRequirementObligationMismatch(ValueError):
    pass


class ObligationServiceState(str, Enum):
    SATISFIED = "satisfied"
    ACTIVE = "active"
    CRITICAL = "critical"
    INDIVIDUALLY_MISSED = "individually_missed"


@dataclass(frozen=True, slots=True)
class AllocationServiceHorizon:
    total_nonprotective_slots: int

    def __post_init__(self) -> None:
        if (
            isinstance(self.total_nonprotective_slots, bool)
            or not isinstance(self.total_nonprotective_slots, int)
        ):
            raise TypeError("total_nonprotective_slots must be an integer")
        if self.total_nonprotective_slots < 0:
            raise ValueError("total_nonprotective_slots must be >= 0")

    @property
    def horizon_spec_digest(self) -> str:
        encoded = json.dumps(
            {
                "total_nonprotective_slots": self.total_nonprotective_slots,
            },
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True, init=False)
class ObligationServiceRequirement:
    goal_id: str
    required_total_slots: int
    served_slots: int
    remaining_horizon_slots: int
    remaining_required_slots: int
    slack_slots: int
    required_remaining_share: float | None
    state: ObligationServiceState
    obligation_admission_digest: str
    allocation_audit_input_digest: str
    horizon_spec_digest: str
    requirement_input_digest: str

    def __init__(
        self,
        *,
        goal_id: str,
        required_total_slots: int,
        served_slots: int,
        remaining_horizon_slots: int,
        remaining_required_slots: int,
        slack_slots: int,
        required_remaining_share: float | None,
        state: ObligationServiceState,
        obligation_admission_digest: str,
        allocation_audit_input_digest: str,
        horizon_spec_digest: str,
        requirement_input_digest: str,
        _token: object | None = None,
    ) -> None:
        if _token is not _OBLIGATION_SERVICE_REQUIREMENT_TOKEN:
            raise TypeError(
                "ObligationServiceRequirement must be issued by "
                "derive_obligation_service_requirements"
            )
        object.__setattr__(self, "goal_id", goal_id)
        object.__setattr__(self, "required_total_slots", required_total_slots)
        object.__setattr__(self, "served_slots", served_slots)
        object.__setattr__(
            self,
            "remaining_horizon_slots",
            remaining_horizon_slots,
        )
        object.__setattr__(
            self,
            "remaining_required_slots",
            remaining_required_slots,
        )
        object.__setattr__(self, "slack_slots", slack_slots)
        object.__setattr__(
            self,
            "required_remaining_share",
            required_remaining_share,
        )
        object.__setattr__(self, "state", state)
        object.__setattr__(
            self,
            "obligation_admission_digest",
            obligation_admission_digest,
        )
        object.__setattr__(
            self,
            "allocation_audit_input_digest",
            allocation_audit_input_digest,
        )
        object.__setattr__(
            self,
            "horizon_spec_digest",
            horizon_spec_digest,
        )
        object.__setattr__(
            self,
            "requirement_input_digest",
            requirement_input_digest,
        )


def _required_slots(
    minimum_share: float,
    total_slots: int,
) -> int:
    # Avoid Decimal context precision rounding a large finite horizon down.
    # The admitted share's decimal representation is an exact ratio.
    numerator, denominator = Decimal(str(minimum_share)).as_integer_ratio()
    return (numerator * total_slots + denominator - 1) // denominator


def _state_for(
    *,
    remaining_required_slots: int,
    remaining_horizon_slots: int,
) -> ObligationServiceState:
    if remaining_required_slots == 0:
        return ObligationServiceState.SATISFIED
    if remaining_required_slots > remaining_horizon_slots:
        return ObligationServiceState.INDIVIDUALLY_MISSED
    if remaining_required_slots == remaining_horizon_slots:
        return ObligationServiceState.CRITICAL
    return ObligationServiceState.ACTIVE


def _requirement_digest(
    *,
    goal_id: str,
    obligation_admission_digest: str,
    allocation_audit_input_digest: str,
    horizon_spec_digest: str,
) -> str:
    encoded = json.dumps(
        {
            "goal_id": goal_id,
            "obligation_admission_digest": obligation_admission_digest,
            "allocation_audit_input_digest": allocation_audit_input_digest,
            "horizon_spec_digest": horizon_spec_digest,
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def derive_obligation_service_requirements(
    audit_receipt: AttestedAllocationAuditReceipt,
    obligations: Iterable[AdmittedGoalObligation],
    horizon: AllocationServiceHorizon,
) -> tuple[ObligationServiceRequirement, ...]:
    if not isinstance(audit_receipt, AttestedAllocationAuditReceipt):
        raise TypeError(
            "audit_receipt must be AttestedAllocationAuditReceipt"
        )
    if not isinstance(horizon, AllocationServiceHorizon):
        raise TypeError("horizon must be AllocationServiceHorizon")

    obligations = tuple(obligations)
    admitted: list[AdmittedGoalObligation] = []
    for obligation in obligations:
        if not isinstance(obligation, AdmittedGoalObligation):
            raise UnadmittedAllocationObligation(
                "service requirements require admitted goal obligations"
            )
        admitted.append(obligation)

    ordered = tuple(
        sorted(
            admitted,
            key=lambda obligation: (
                obligation.goal_id,
                obligation.admission_input_digest,
            ),
        )
    )
    supplied_digests = tuple(
        obligation.admission_input_digest for obligation in ordered
    )
    if supplied_digests != audit_receipt.obligation_admission_digests:
        raise ServiceRequirementObligationMismatch(
            "service requirement obligations do not match the allocation audit"
        )

    observed_slots = audit_receipt.audit.nonprotective_samples
    if horizon.total_nonprotective_slots < observed_slots:
        raise ValueError(
            "service horizon cannot be shorter than observed nonprotective history"
        )

    remaining_horizon_slots = (
        horizon.total_nonprotective_slots - observed_slots
    )
    counts = dict(audit_receipt.goal_service_counts)
    requirements: list[ObligationServiceRequirement] = []

    for obligation in ordered:
        required_total_slots = _required_slots(
            obligation.minimum_nonprotective_share,
            horizon.total_nonprotective_slots,
        )
        served_slots = counts.get(obligation.goal_id, 0)
        remaining_required_slots = max(
            0,
            required_total_slots - served_slots,
        )
        slack_slots = (
            remaining_horizon_slots - remaining_required_slots
        )
        required_remaining_share = (
            None
            if remaining_horizon_slots == 0
            else remaining_required_slots / remaining_horizon_slots
        )
        state = _state_for(
            remaining_required_slots=remaining_required_slots,
            remaining_horizon_slots=remaining_horizon_slots,
        )
        requirement_input_digest = _requirement_digest(
            goal_id=obligation.goal_id,
            obligation_admission_digest=obligation.admission_input_digest,
            allocation_audit_input_digest=audit_receipt.audit_input_digest,
            horizon_spec_digest=horizon.horizon_spec_digest,
        )
        requirements.append(
            ObligationServiceRequirement(
                goal_id=obligation.goal_id,
                required_total_slots=required_total_slots,
                served_slots=served_slots,
                remaining_horizon_slots=remaining_horizon_slots,
                remaining_required_slots=remaining_required_slots,
                slack_slots=slack_slots,
                required_remaining_share=required_remaining_share,
                state=state,
                obligation_admission_digest=(
                    obligation.admission_input_digest
                ),
                allocation_audit_input_digest=(
                    audit_receipt.audit_input_digest
                ),
                horizon_spec_digest=horizon.horizon_spec_digest,
                requirement_input_digest=requirement_input_digest,
                _token=_OBLIGATION_SERVICE_REQUIREMENT_TOKEN,
            )
        )

    return tuple(requirements)
