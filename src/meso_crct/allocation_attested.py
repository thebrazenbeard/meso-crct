"""Strict allocation auditing over admitted relations and obligations only."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib
import json
from typing import Iterable

from .allocation import (
    AllocationAudit,
    AllocationSample,
    _audit_attention_budget_core,
    _unit,
)
from .obligations import AdmittedGoalObligation


_ATTESTED_ALLOCATION_AUDIT_TOKEN = object()


class UnattestedAllocationSample(ValueError):
    pass


class UnadmittedAllocationObligation(ValueError):
    pass


class AttestedAllocationIntegrityError(ValueError):
    pass


@dataclass(frozen=True, slots=True, init=False)
class AttestedAllocationAuditReceipt:
    audit: AllocationAudit
    audit_input_digest: str
    sample_relation_receipt_digests: tuple[tuple[str, ...], ...]
    obligation_admission_digests: tuple[str, ...]
    goal_service_counts: tuple[tuple[str, int], ...]
    crowdout_fraction: float

    def __init__(
        self,
        *,
        audit: AllocationAudit,
        audit_input_digest: str,
        sample_relation_receipt_digests: tuple[tuple[str, ...], ...] = (),
        obligation_admission_digests: tuple[str, ...] = (),
        goal_service_counts: tuple[tuple[str, int], ...] = (),
        crowdout_fraction: float = 0.75,
        _token: object | None = None,
    ) -> None:
        if _token is not _ATTESTED_ALLOCATION_AUDIT_TOKEN:
            raise TypeError(
                "AttestedAllocationAuditReceipt must be issued by "
                "audit_attested_attention_budget"
            )
        if not audit_input_digest.strip():
            raise ValueError("audit_input_digest must be non-empty")
        object.__setattr__(self, "audit", audit)
        object.__setattr__(self, "audit_input_digest", audit_input_digest)
        object.__setattr__(
            self,
            "sample_relation_receipt_digests",
            sample_relation_receipt_digests,
        )
        object.__setattr__(
            self,
            "obligation_admission_digests",
            obligation_admission_digests,
        )
        object.__setattr__(
            self,
            "goal_service_counts",
            goal_service_counts,
        )
        object.__setattr__(
            self,
            "crowdout_fraction",
            _unit(crowdout_fraction, name="crowdout_fraction"),
        )


def _strict_goal_ids_for_sample(sample: AllocationSample) -> tuple[str, ...]:
    return tuple(
        relation.goal_id
        for relation in sample.attested_goal_relations
    )


def _goal_service_counts(
    *,
    samples: tuple[AllocationSample, ...],
    obligations: tuple[AdmittedGoalObligation, ...],
) -> tuple[tuple[str, int], ...]:
    counts: Counter[str] = Counter()
    obligation_ids = {obligation.goal_id for obligation in obligations}
    for sample in samples:
        if sample.protective:
            continue
        served_goal_ids = {
            relation.goal_id
            for relation in sample.attested_goal_relations
            if relation.goal_id in obligation_ids
        }
        counts.update(served_goal_ids)
    return tuple(
        (obligation.goal_id, counts[obligation.goal_id])
        for obligation in obligations
    )


def _audit_digest(
    *,
    samples: tuple[AllocationSample, ...],
    obligations: tuple[AdmittedGoalObligation, ...],
    goal_service_counts: tuple[tuple[str, int], ...],
    crowdout_fraction: float,
) -> str:
    payload = {
        "crowdout_fraction": crowdout_fraction,
        "samples": [
            {
                "target_id": sample.target_id,
                "priority": sample.priority,
                "dominant_driver": sample.dominant_driver,
                "protective": sample.protective,
                "goal_relation_receipts": sorted(
                    receipt.admission_input_digest
                    for receipt in sample.goal_relation_receipts
                ),
            }
            for sample in samples
        ],
        "goal_service_counts": goal_service_counts,
        "obligations": [
            {
                "goal_id": obligation.goal_id,
                "minimum_nonprotective_share": (
                    obligation.minimum_nonprotective_share
                ),
                "evidence": {
                    "producer_id": obligation.evidence.producer_id,
                    "producer_revision": obligation.evidence.producer_revision,
                    "subject_id": obligation.evidence.subject_id,
                    "source_id": obligation.evidence.source_id,
                    "currentness": obligation.evidence.currentness.value,
                },
                "admission_policy_id": obligation.admission_policy_id,
                "admission_policy_revision": (
                    obligation.admission_policy_revision
                ),
                "admission_input_digest": obligation.admission_input_digest,
            }
            for obligation in obligations
        ],
    }
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def audit_attested_attention_budget(
    samples: Iterable[AllocationSample],
    obligations: Iterable[AdmittedGoalObligation],
    *,
    crowdout_fraction: float = 0.75,
) -> AttestedAllocationAuditReceipt:
    samples = tuple(samples)
    obligations = tuple(obligations)
    crowdout_fraction = _unit(
        crowdout_fraction,
        name="crowdout_fraction",
    )

    for obligation in obligations:
        if not isinstance(obligation, AdmittedGoalObligation):
            raise UnadmittedAllocationObligation(
                "strict allocation audit requires admitted goal obligations"
            )

    goal_ids = tuple(obligation.goal_id for obligation in obligations)
    if len(goal_ids) != len(set(goal_ids)):
        raise ValueError("strict allocation obligations must have unique goal IDs")

    ordered_obligations = tuple(
        sorted(
            obligations,
            key=lambda obligation: (
                obligation.goal_id,
                obligation.admission_input_digest,
            ),
        )
    )

    for sample in samples:
        if not sample.goal_relation_attestation_complete:
            raise UnattestedAllocationSample(
                "strict allocation audit requires every stored goal relation "
                "to have an admission receipt"
            )
        for relation in sample.attested_goal_relations:
            if relation.target_id != sample.target_id:
                raise AttestedAllocationIntegrityError(
                    "attested goal relation target must match allocation sample "
                    "target"
                )

    audit = _audit_attention_budget_core(
        samples,
        ordered_obligations,
        crowdout_fraction=crowdout_fraction,
        goal_ids_for_sample=_strict_goal_ids_for_sample,
    )

    sample_receipt_digests = tuple(
        tuple(
            sorted(
                receipt.admission_input_digest
                for receipt in sample.goal_relation_receipts
            )
        )
        for sample in samples
    )
    obligation_digests = tuple(
        obligation.admission_input_digest
        for obligation in ordered_obligations
    )
    goal_service_counts = _goal_service_counts(
        samples=samples,
        obligations=ordered_obligations,
    )

    return AttestedAllocationAuditReceipt(
        audit=audit,
        audit_input_digest=_audit_digest(
            samples=samples,
            obligations=ordered_obligations,
            goal_service_counts=goal_service_counts,
            crowdout_fraction=crowdout_fraction,
        ),
        sample_relation_receipt_digests=sample_receipt_digests,
        obligation_admission_digests=obligation_digests,
        goal_service_counts=goal_service_counts,
        crowdout_fraction=crowdout_fraction,
        _token=_ATTESTED_ALLOCATION_AUDIT_TOKEN,
    )
