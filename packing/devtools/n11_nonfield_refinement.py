"""Bind a complete closed-angle refinement to independently accepted pose rows.

One new interval may refine one accepted predecessor. Intervals that cross two
predecessors require a separate union-domain proof and are refused here.
"""

from __future__ import annotations

import json
from fractions import Fraction as Q
from typing import Any


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _key(value: object) -> str:
    require(isinstance(value, dict), "pose row reference")
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def complete_refinement(
    proposed: list[dict[str, Any]],
    accepted: list[dict[str, Any]],
    *,
    max_rows: int,
) -> list[dict[str, Any]]:
    """Return each proposed row's exact accepted predecessor or refuse the partition."""
    require(type(max_rows) is int and max_rows > 0, "refinement row ceiling")
    require(0 < len(proposed) <= max_rows and bool(accepted), "refinement row inventory")
    by_ref = {_key(row["reference"]): row for row in accepted}
    require(len(by_ref) == len(accepted), "duplicate accepted row reference")
    cursor = Q()
    predecessors: list[dict[str, Any]] = []
    for row in proposed:
        lo, hi = (Q(value) for value in row["interval"])
        require(cursor == lo and lo < hi <= 1, "refinement angular gap or overlap")
        cursor = hi
        prior = by_ref.get(_key(row["prior_reference"]))
        if prior is None:
            raise ValueError("refinement predecessor is not accepted")
        old_lo, old_hi = (Q(value) for value in prior["interval"])
        require(old_lo <= lo and hi <= old_hi, "refinement crossed predecessor interval")
        predecessors.append(prior)
    require(cursor == 1, "refinement angular cover incomplete")
    return predecessors
