"""Typed outcome classes for learning-event provenance."""

from enum import Enum


class OutcomeClass(str, Enum):
    APPETITIVE = "appetitive"
    AVERSIVE = "aversive"
    OMISSION = "omission"
    BLOCKED = "blocked"
    LOSS = "loss"
    AVOIDED_AVERSIVE = "avoided_aversive"
    OTHER = "other"
