"""Shared strict finite real-number admission for synthetic state boundaries.

Python booleans are integers for arithmetic, but they are not measurements.
Text conversion is likewise not a valid typed observation or policy input.
"""

from __future__ import annotations

import math


def finite_real(value: int | float, *, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite numeric value")
    try:
        result = float(value)
    except (OverflowError, TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite numeric value") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be a finite numeric value")
    return result
