"""Event identity counters must be genuine positive integers."""

import math

import pytest

from meso_crct.events import EventSequencer


@pytest.mark.parametrize("invalid", [True, False, 1.0, 1.5, math.nan, math.inf, "1", None])
def test_sequencer_rejects_noninteger_counters(invalid):
    with pytest.raises(ValueError, match="next_sequence must be a positive integer"):
        EventSequencer("source", next_sequence=invalid)


@pytest.mark.parametrize("invalid", ["", "  ", 42, None, False])
def test_sequencer_rejects_invalid_stream_ids(invalid):
    with pytest.raises(ValueError, match="stream_id must be a non-empty string"):
        EventSequencer(invalid)


def test_issued_events_have_monotonic_integer_sequence_and_distinct_identity():
    sequencer = EventSequencer("source", next_sequence=1)
    sequencer, first = sequencer.issue()
    sequencer, second = sequencer.issue()

    assert (first.sequence, second.sequence) == (1, 2)
    assert first.event_id != second.event_id
