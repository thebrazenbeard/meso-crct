"""Distinct runtime event identity for MESO-CRCT.

State/content identity and event identity are separate. Two experiences may
produce identical state transitions while still being distinct events.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib


_EVENT_IDENTITY_TOKEN = object()


def _validate_stream_id(stream_id: str) -> None:
    if not isinstance(stream_id, str) or not stream_id.strip():
        raise ValueError("stream_id must be a non-empty string")


def _validate_sequence(sequence: int, *, name: str) -> None:
    # bool is an int subclass, while NaN and floats can keep issuing the same
    # event ID indefinitely when used as immutable sequence counters.
    if isinstance(sequence, bool) or not isinstance(sequence, int) or sequence < 1:
        raise ValueError(f"{name} must be a positive integer")


@dataclass(frozen=True, slots=True, init=False)
class EventIdentity:
    stream_id: str
    sequence: int
    event_id: str

    def __init__(
        self,
        stream_id: str,
        sequence: int,
        event_id: str,
        *,
        _token: object | None = None,
    ) -> None:
        if _token is not _EVENT_IDENTITY_TOKEN:
            raise TypeError("EventIdentity must be issued by EventSequencer")
        _validate_stream_id(stream_id)
        _validate_sequence(sequence, name="sequence")
        if not isinstance(event_id, str) or not event_id.strip():
            raise ValueError("event_id must be a non-empty string")
        object.__setattr__(self, "stream_id", stream_id)
        object.__setattr__(self, "sequence", sequence)
        object.__setattr__(self, "event_id", event_id)


@dataclass(frozen=True, slots=True)
class EventSequencer:
    """Immutable reference event sequencer."""

    stream_id: str
    next_sequence: int = 1

    def __post_init__(self) -> None:
        _validate_stream_id(self.stream_id)
        _validate_sequence(self.next_sequence, name="next_sequence")

    def issue(self) -> tuple["EventSequencer", EventIdentity]:
        sequence = self.next_sequence
        payload = f"{self.stream_id}:{sequence}".encode("utf-8")
        event_id = hashlib.sha256(payload).hexdigest()
        event = EventIdentity(
            stream_id=self.stream_id,
            sequence=sequence,
            event_id=event_id,
            _token=_EVENT_IDENTITY_TOKEN,
        )
        return (
            EventSequencer(
                stream_id=self.stream_id,
                next_sequence=sequence + 1,
            ),
            event,
        )
