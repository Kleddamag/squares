"""Bind a generic child node to an independently accepted parent state.

This is a source-ancestry check, not a proof of either node's geometry. The
caller must pass the exact groups and pose rows produced by complete parent
replay; this function returns isolated copies for the child replay.
"""

from __future__ import annotations

import copy
from fractions import Fraction as Q
from typing import Any

from devtools import check_n11_generic_fresh as frozen
from devtools import check_n11_optimality_field_mask0 as geometry

Polygon = frozen.Polygon


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def admit_child_state(
    child: dict[str, Any],
    *,
    parent_source_sha256: str,
    seed_sha256: str,
    case_id: int,
    mask: tuple[int, ...],
    accepted_groups: dict[int, Polygon],
    accepted_rows: dict[int, list[dict[str, Any]]],
) -> tuple[dict[int, Polygon], dict[int, list[dict[str, Any]]]]:
    """Require exact parent hash, seed identity, and complete accepted state."""
    parent = child.get("parent")
    require(
        isinstance(parent, dict) and parent.get("sha256") == parent_source_sha256,
        "child parent source hash",
    )
    require(
        child.get("mask_index") == case_id
        and child.get("mask") == list(mask)
        and Q(child["U"]) == geometry.U
        and Q(child["B"]) == geometry.B
        and child.get("source", {}).get("sha256") == seed_sha256
        and child.get("constraints") == []
        and child.get("guard_source") is None,
        "child case/seed/constraint identity",
    )
    require(
        set(accepted_groups) == set(mask) and set(accepted_rows) == set(mask),
        "accepted parent owner inventory",
    )
    initial = child["initial"]
    require(
        set(initial["groups"]) == set(map(str, mask))
        and set(initial["cell_references"]) == set(map(str, mask)),
        "child initial owner inventory",
    )
    for owner in mask:
        require(
            frozen.hull(frozen.points(initial["groups"][str(owner)]))
            == frozen.hull(accepted_groups[owner]),
            "child initial owned group differs from accepted parent",
        )
        require(
            initial["cell_references"][str(owner)]
            == [row["reference"] for row in accepted_rows[owner]],
            "child pose references differ from accepted parent",
        )
    return copy.deepcopy(accepted_groups), copy.deepcopy(accepted_rows)
