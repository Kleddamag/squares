"""Exact partner-pose ancestry for a fresh-wall generic exclusion.

The caller supplies one accepted, immutable state from the preceding step.
This module validates a complete closed-angle partner cover against that state.
It does not treat publisher collision labels or row counts as proof.
"""

# The frozen pilot exports no public strict-core or hull-equality API yet.
# ruff: noqa: SLF001
# pyright: reportPrivateUsage=false

from __future__ import annotations

import json
import time
from fractions import Fraction as Q
from typing import Any

from devtools import check_n11_capture_transition_pilot as collision
from devtools import check_n11_generic_fresh as frozen
from devtools import check_n11_optimality_field_mask0 as geometry
from devtools import n11_integer_collision as integer_collision

Polygon = frozen.Polygon


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _reference_key(value: object) -> str:
    require(isinstance(value, dict), "partner predecessor reference")
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def admitted_partner_covers(
    proposed: dict[str, Any],
    *,
    query_owner: int,
    mask: tuple[int, ...],
    accepted_groups: dict[int, Polygon],
    accepted_rows: dict[int, list[dict[str, Any]]],
    budget: geometry.Budget,
    center_planes: dict[int, list[tuple[Q, Q, Q]]] | None = None,
) -> tuple[dict[int, list[tuple[Polygon, Polygon]]], dict[str, int]]:
    """Return every live pre-wall domain and whole-angle strict partner core."""
    require(isinstance(proposed, dict), "partner cover map")
    require(
        all(key.isdecimal() and str(int(key)) == key for key in proposed),
        "partner owner key",
    )
    owners = {int(key) for key in proposed}
    require(owners <= set(mask) - {query_owner}, "partner owner outside accepted mask")
    live: dict[int, list[tuple[Polygon, Polygon]]] = {}
    total = empty = 0
    for owner in sorted(owners):
        require(
            owner in accepted_groups and owner in accepted_rows,
            "partner missing accepted state",
        )
        rows = proposed[str(owner)]
        require(isinstance(rows, list) and bool(rows), "partner angular inventory")
        prior_rows = accepted_rows[owner]
        by_reference = {_reference_key(row["reference"]): row for row in prior_rows}
        require(len(by_reference) == len(prior_rows), "duplicate accepted partner reference")
        cursor = Q()
        live[owner] = []
        for row in rows:
            if time.monotonic() >= budget.deadline:
                raise geometry.IncompleteError("partner cover wall ceiling")
            total += 1
            require(total <= budget.max_nodes, "partner cover row ceiling")
            require(isinstance(row, dict), "partner row")
            lo, hi = (Q(value) for value in row["interval"])
            require(cursor == lo and lo < hi <= 1, "partner angular gap or overlap")
            cursor = hi
            old = by_reference.get(_reference_key(row["reference"]))
            if old is None:
                raise ValueError("partner predecessor is not accepted")
            old_lo, old_hi = (Q(value) for value in old["interval"])
            require(old_lo <= lo < hi <= old_hi, "partner interval escaped predecessor")
            previous_outer = frozen.hull(frozen.points(old["outer_domain"]))
            cuts = collision.necessary_self_cuts(
                row.get("self_hull_cuts", []), accepted_groups[owner], lo, hi
            )
            required = geometry.intersect(
                previous_outer, cuts + (center_planes or {}).get(owner, [])
            )
            if not required:
                require(row["domain"] == [] and row["core"] == [], "empty partner row")
                empty += 1
                continue
            domain = frozen.convex(row["domain"])
            require(
                frozen._same(domain, required), "partner domain differs from accepted prior"
            )
            core = frozen.convex(row["core"])
            frozen._strict_core(core, lo, hi)
            live[owner].append((required, core))
        require(cursor == 1, "partner angular cover incomplete")
    return live, {"rows": total, "empty_rows": empty, "live_rows": total - empty}


def admitted_collision_regions(
    proposed: list[dict[str, Any]],
    *,
    query_core: Polygon,
    query_pre_wall_domain: Polygon,
    partners: dict[int, list[tuple[Polygon, Polygon]]],
    budget: geometry.Budget,
    backend: str = "reference",
) -> tuple[list[Polygon], int]:
    """Prove every selected source region lies in a universal core collision set."""
    require(backend in ("reference", "integer"), "collision backend")
    kernel = (
        integer_collision.universal_collision
        if backend == "integer"
        else collision.universal_collision
    )
    regions: list[Polygon] = []
    seen: set[int] = set()
    checks = 0
    for item in proposed:
        owner = item.get("partner")
        if type(owner) is not int or owner not in partners or owner in seen:
            raise ValueError("collision partner identity")
        seen.add(owner)
        require(
            item.get("status") == "EXACT_UNIVERSAL_COLLISION_KERNEL"
            and item.get("live_rows") == len(partners[owner]),
            "collision source scope",
        )
        region = frozen.convex(item["vertices"])
        checks += kernel(
            query_core, query_pre_wall_domain, partners[owner], region, budget=budget
        )
        regions.append(region)
    return regions, checks
