"""Caller-admitted, replay-safe need observations for the homeostatic state.

This reference boundary does not verify sensor custody or make a model report
authoritative. A caller must explicitly bind an entire immutable observation
before admission. Updates are in-memory and cause no downstream effect.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
import math
from typing import Iterable

from ._numeric import finite_real
from .homeostasis import HomeostaticState
from .provenance import Provenance, SourceKind


EXTERNAL_OBSERVATION_SOURCES = frozenset({
    SourceKind.ENVIRONMENT,
    SourceKind.OPERATOR_INPUT,
    SourceKind.TEST_STIMULATION,
})


class ObservationNotAdmitted(ValueError):
    """An observed value was not present in the caller's admitted set."""


class NeedObservationConflict(ValueError):
    """An event identifier already names a different observation."""


class NeedObservationStale(ValueError):
    """A distinct observation is not newer than the last one for its need."""


class NeedObservationFuture(ValueError):
    """An observation exceeds the explicit caller-supplied trusted time ceiling."""


MAX_FUTURE_SKEW_SECONDS = 300.0


@dataclass(frozen=True, slots=True)
class AdmissionClock:
    """Externally supplied UTC admission ceiling, not MESO-derived authority.

    A caller must establish trusted_as_of independently of model output. The
    reference module validates the ceiling's shape but cannot authenticate it.
    """

    trusted_as_of: datetime
    maximum_future_skew_seconds: float = 0.0

    def __post_init__(self) -> None:
        if (
            not isinstance(self.trusted_as_of, datetime)
            or self.trusted_as_of.utcoffset() != timedelta(0)
        ):
            raise ValueError("trusted_as_of must be an aware UTC timestamp")
        object.__setattr__(
            self, "trusted_as_of", self.trusted_as_of.astimezone(timezone.utc)
        )
        skew = self.maximum_future_skew_seconds
        if (
            isinstance(skew, bool)
            or not isinstance(skew, (int, float))
            or not 0.0 <= skew <= MAX_FUTURE_SKEW_SECONDS
            or not math.isfinite(float(skew))
        ):
            raise ValueError("skew must be finite, numeric, and in [0, 300] seconds")
        object.__setattr__(self, "maximum_future_skew_seconds", float(skew))


@dataclass(frozen=True, slots=True)
class NeedObservation:
    """One unverified, externally *claimed* measurement of a named need."""

    event_id: str
    need_id: str
    measured_level: float
    observed_at: datetime
    provenance: Provenance
    evidence_ref: str

    def __post_init__(self) -> None:
        for name in ("event_id", "need_id", "evidence_ref"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be non-empty")
        if isinstance(self.measured_level, bool) or not isinstance(self.measured_level, (int, float)):
            raise ValueError("measured_level must be a numeric measurement, not text or a flag")
        level = finite_real(self.measured_level, name="measured_level")
        if not math.isfinite(level) or not 0.0 <= level <= 1.0:
            raise ValueError("measured_level must be finite and within [0, 1]")
        object.__setattr__(self, "measured_level", level)
        if not isinstance(self.observed_at, datetime) or self.observed_at.utcoffset() != timedelta(0):
            raise ValueError("observed_at must be an aware UTC timestamp")
        object.__setattr__(self, "observed_at", self.observed_at.astimezone(timezone.utc))
        if not isinstance(self.provenance, Provenance) or (
            not isinstance(self.provenance.source_kind, SourceKind)
        ) or (
            self.provenance.source_kind not in EXTERNAL_OBSERVATION_SOURCES
        ):
            raise ValueError("need observations require an external admitted source kind")


_ADMISSION_TOKEN = object()


@dataclass(frozen=True, slots=True, init=False)
class AdmittedNeedObservation:
    """Reference marker of an exact caller-selected claim, not independent trust."""

    observation: NeedObservation
    verifier_id: str

    def __init__(
        self, observation: NeedObservation, verifier_id: str,
        *, _token: object | None = None,
    ) -> None:
        if _token is not _ADMISSION_TOKEN:
            raise TypeError("admission must be issued by NeedObservationVerifier")
        object.__setattr__(self, "observation", observation)
        object.__setattr__(self, "verifier_id", verifier_id)

    @property
    def effect_authorized(self) -> bool:
        return False


class NeedObservationVerifier:
    """Exact-value admission list supplied by an accountable external caller."""

    def __init__(self, accepted: Iterable[NeedObservation], *, verifier_id: str):
        if not isinstance(verifier_id, str) or not verifier_id.strip():
            raise ValueError("verifier_id must be non-empty")
        claims = frozenset(accepted)
        if not all(isinstance(item, NeedObservation) for item in claims):
            raise TypeError("accepted observations must be NeedObservation values")
        self._accepted = claims
        self._verifier_id = verifier_id

    def admit(self, observation: NeedObservation) -> AdmittedNeedObservation:
        if observation not in self._accepted:
            raise ObservationNotAdmitted("observation not bound by caller verifier")
        return AdmittedNeedObservation(
            observation, self._verifier_id, _token=_ADMISSION_TOKEN
        )


@dataclass(frozen=True, slots=True)
class NeedObservationRecord:
    observation: NeedObservation
    verifier_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.observation, NeedObservation):
            raise TypeError("record observation must be typed")
        if not isinstance(self.verifier_id, str) or not self.verifier_id.strip():
            raise ValueError("verifier_id must be non-empty")


@dataclass(frozen=True, slots=True)
class NeedObservationLedger:
    """Immutable, in-memory current need values with accepted event history."""

    homeostasis: HomeostaticState
    records: tuple[NeedObservationRecord, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.homeostasis, HomeostaticState):
            raise TypeError("homeostasis must be typed")
        if not isinstance(self.records, tuple):
            raise TypeError("ledger records must be an immutable tuple")
        seen_events: set[str] = set()
        latest: dict[str, NeedObservation] = {}
        for record in self.records:
            if not isinstance(record, NeedObservationRecord):
                raise TypeError("ledger records must be typed")
            observation = record.observation
            if observation.event_id in seen_events:
                raise NeedObservationConflict("duplicate event ID in ledger")
            seen_events.add(observation.event_id)
            if self.homeostasis.axis(observation.need_id) is None:
                raise ValueError(f"unknown need axis in ledger: {observation.need_id}")
            prior = latest.get(observation.need_id)
            if prior and observation.observed_at <= prior.observed_at:
                raise NeedObservationStale("out-of-order need observation in ledger")
            latest[observation.need_id] = observation
        for need_id, observation in latest.items():
            axis = self.homeostasis.axis(need_id)
            if axis is None or axis.current_level != observation.measured_level:
                raise ValueError(f"latest admitted need level disagrees with ledger: {need_id}")

    @property
    def effect_authorized(self) -> bool:
        return False


def admit_need_observation(
    ledger: NeedObservationLedger,
    admitted: AdmittedNeedObservation,
    *,
    clock: AdmissionClock,
) -> NeedObservationLedger:
    """Admit exactly one caller-selected event, updating one existing need.

    Same event + identical claim is a no-op; a conflicting reuse is rejected.
    A different event must advance the UTC clock of its individual need.
    No goal satisfaction, salience, pleasure, or external tool effects occur.
    """
    if not isinstance(admitted, AdmittedNeedObservation):
        raise TypeError("need update requires an admitted observation")
    if not isinstance(clock, AdmissionClock):
        raise TypeError("need update requires a typed caller-supplied clock")
    observation = admitted.observation
    # Difference comparison cannot overflow at datetime.max as UTC addition can.
    if (
        observation.observed_at > clock.trusted_as_of
        and (observation.observed_at - clock.trusted_as_of).total_seconds()
        > clock.maximum_future_skew_seconds
    ):
        raise NeedObservationFuture("observation is too far in the future")
    for record in ledger.records:
        if record.observation.event_id == observation.event_id:
            if (
                record.observation == observation
                and record.verifier_id == admitted.verifier_id
            ):
                return ledger
            raise NeedObservationConflict("event ID reused for different evidence")

    current = ledger.homeostasis.axis(observation.need_id)
    if current is None:
        raise ValueError(f"unknown need axis: {observation.need_id}")
    for record in ledger.records:
        prior = record.observation
        if (
            prior.need_id == observation.need_id
            and observation.observed_at <= prior.observed_at
        ):
            raise NeedObservationStale(
                f"observation does not advance need clock: {observation.need_id}"
            )

    homeostasis = HomeostaticState(tuple(
        replace(axis, current_level=observation.measured_level)
        if axis.need_id == observation.need_id else axis
        for axis in ledger.homeostasis.axes
    ))
    return NeedObservationLedger(
        homeostasis=homeostasis,
        records=ledger.records + (NeedObservationRecord(
            observation=observation, verifier_id=admitted.verifier_id,
        ),),
    )
