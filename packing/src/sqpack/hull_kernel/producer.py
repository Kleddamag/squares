"""A deliberately simple mode-A producer: it proposes, and `sequential` certifies.

Nothing this module returns is evidence. It writes a seed (`generic_wall_seed_v1`) and a
node (`exact_generic_owned_hull_v1`, sequential grammar) for a set of owner cells, and
only `sequential.replay_sequential`, run on exactly those objects, decides whether the
node closes. The policy is the adaptation spec's first producer (section 5, slice 1):

* the seed owns grid points near each cell's vertex centroid, each kept only if
  `ownership` proves it from the cell alone, and gives every owner `bins` uniform rows;
* owners update round-robin in mask order, one complete step each, with no splitting
  and no self-hull cuts or collision regions;
* a row's core is the envelope square: side `(B - slack)/factor` turned to the row's
  midpoint angle, the counting mode's strict core, kept only if `strict_core` accepts it;
* a row's residual is its legal domain minus every other owner's forbidden region
  `K_j - Q_i`, by exact convex subtraction, keeping positive-area pieces of a
  positive-area domain;
* a row's outer domain is its residual's eight supports, rounded outward to `10^-8`;
* the kernel is the intersection of every live row's common-core planes, and it is
  promoted by grid points (denominator `2^20`) inside the hull of the prior hull and the
  kernel, each an exact convex combination of at most three of its vertices.

It stops at the first closure it sees, after `max_rounds` rounds, when a round changes
no owner's rows or hull, or at `stop_at`, leaving the checker time to certify the steps
made so far (a node without closure is a stall, and excludes nothing).
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from fractions import Fraction as Q
from typing import Any

from sqpack.hull_kernel.collision import SUPPORT_NORMALS, outward_round
from sqpack.hull_kernel.counting import row_envelope
from sqpack.hull_kernel.covers import convex_halfplanes
from sqpack.hull_kernel.frame import Frame
from sqpack.hull_kernel.geometry import (
    Budget,
    Halfplane,
    IncompleteError,
    Point,
    Polygon,
    RefusalError,
    area2,
    clip,
    intersect,
)
from sqpack.hull_kernel.induction import (
    common_core_planes,
    encode,
    forbidden_regions,
    hull,
    strict_core,
    wall_lines,
)
from sqpack.hull_kernel.node import Row, points
from sqpack.hull_kernel.ownership import ownership
from sqpack.hull_kernel.sequential import derived_closure, owner_extents

GRID = 2**20


def content_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _grid(value: Q) -> Q:
    return Q(round(value * GRID), GRID)


def _encode_point(point: Point) -> list[str]:
    return [str(point[0]), str(point[1])]


def seed_points(frame: Frame, owner: int, *, budget: Budget) -> list[Point]:
    """Grid points near the cell's vertex centroid that `ownership` proves owned."""
    cell = frame.world(owner)
    cx = sum((x for x, _ in cell), Q()) / len(cell)
    cy = sum((y for _, y in cell), Q()) / len(cell)
    candidates = [(_grid(cx), _grid(cy))]
    candidates.extend(
        (_grid(cx + (x - cx) * fraction), _grid(cy + (y - cy) * fraction))
        for x, y in cell
        for fraction in (Q(1, 8), Q(1, 4))
    )
    owned: list[Point] = []
    for point in dict.fromkeys(candidates):
        try:
            ownership(frame, owner, point, budget=Budget(budget.deadline, 4000))
        except IncompleteError, RefusalError:
            continue
        owned.append(point)
    return owned


def build_seed(
    frame: Frame, mask: Sequence[int], *, bins: int, budget: Budget
) -> dict[str, Any]:
    groups: dict[str, list[list[str]]] = {}
    cells: dict[str, list[Row]] = {}
    for owner in mask:
        owned = seed_points(frame, owner, budget=budget)
        groups[str(owner)] = [_encode_point(point) for point in owned]
        rows: list[Row] = []
        for index in range(bins):
            lo, hi = Q(index, bins), Q(index + 1, bins)
            domain = intersect(frame.world(owner), wall_lines(frame, lo, hi))
            rows.append(
                {
                    "interval": [str(lo), str(hi)],
                    "residual_polygons": [encode(domain)] if domain else [],
                    "outer_domain": encode(domain),
                    "outer_bounds": [],
                    "reference": {"kind": "wall_seed", "owner": owner, "row": index},
                }
            )
        cells[str(owner)] = rows
    return {
        "schema": "generic_wall_seed_v1",
        "mask_index": None,
        "mask": list(mask),
        "U": str(frame.cap),
        "B": str(frame.scale),
        "bins": bins,
        "groups": groups,
        "cells": cells,
        "world": [encode(frame.world(cell)) for cell in range(len(frame.cells))],
    }


def envelope_core(frame: Frame, lo: Q, hi: Q) -> Polygon:
    """The row's strict core: the envelope square turned to the midpoint angle."""
    side, _, c, s = row_envelope(frame, (lo, hi))
    for _ in range(8):
        half = side / 2
        core = hull(
            [(c * u - s * v, s * u + c * v) for u in (-half, half) for v in (-half, half)]
        )
        try:
            strict_core(frame, core, lo, hi)
        except RefusalError:
            side *= 1 - Q(1, 2**20)
            continue
        return core
    raise RefusalError("no envelope core is strictly inside the row")


def subtract(pieces: list[Polygon], region: Polygon, *, keep_area_only: bool) -> list[Polygon]:
    """Convex pieces covering the closure of `pieces` minus the closed convex `region`."""
    planes = convex_halfplanes(region)
    result: list[Polygon] = []
    for piece in pieces:
        rest = piece
        for a, b, c in planes:
            outside = clip(rest, (-a, -b, -c))
            if outside and (area2(outside) > 0 or not keep_area_only):
                result.append(outside)
            rest = clip(rest, (a, b, c))
            if not rest:
                break
    return result


def _barycentric(original: Polygon, point: Point) -> tuple[list[int], list[Q]] | None:
    if len(original) == 1:
        return ([0], [Q(1)]) if original[0] == point else None
    if len(original) == 2:
        return ([original.index(point)], [Q(1)]) if point in original else None
    ax, ay = original[0]
    for j in range(1, len(original) - 1):
        (bx, by), (cx, cy) = original[j], original[j + 1]
        det = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
        if det == 0:
            continue
        px, py = point[0] - ax, point[1] - ay
        u = (px * (cy - ay) - py * (cx - ax)) / det
        v = ((bx - ax) * py - (by - ay) * px) / det
        if u >= 0 and v >= 0 and u + v <= 1:
            return [0, j, j + 1], [1 - u - v, u, v]
    return None


def compress(original: Polygon) -> tuple[list[Point], list[dict[str, Any]]]:
    """Grid points inside `original`, each with its exact convex-combination witness.

    When every vertex is already a grid point (seed points and kernel points are), the
    vertices are kept, each its own witness; otherwise grid points are pulled inward.
    """
    if all((x * GRID).denominator == 1 and (y * GRID).denominator == 1 for x, y in original):
        return list(original), [
            {"point": _encode_point(point), "indices": [index], "weights": ["1"]}
            for index, point in enumerate(original)
        ]
    n = len(original)
    cx = sum((x for x, _ in original), Q()) / n
    cy = sum((y for _, y in original), Q()) / n
    chosen: dict[Point, tuple[list[int], list[Q]]] = {}
    for x, y in original:
        for pull in (Q(1, 2**12), Q(1, 2**8), Q(1, 2**4), Q(1, 4)):
            point = (_grid(x + (cx - x) * pull), _grid(y + (cy - y) * pull))
            witness = _barycentric(original, point)
            if witness is not None:
                chosen.setdefault(point, witness)
                break
    if not chosen:
        for index, point in enumerate(original):
            if (point[0] * GRID).denominator == 1 and (point[1] * GRID).denominator == 1:
                chosen[point] = ([index], [Q(1)])
    if not chosen:
        raise RefusalError("no grid point lies in the compression source hull")
    selected = list(chosen.items())
    return [point for point, _ in selected], [
        {
            "point": _encode_point(point),
            "indices": indices,
            "weights": [str(weight) for weight in weights],
        }
        for point, (indices, weights) in selected
    ]


def cached_core(
    frame: Frame, lo: Q, hi: Q, cores: dict[tuple[Q, Q], Polygon] | None
) -> Polygon:
    if cores is None:
        return envelope_core(frame, lo, hi)
    if (lo, hi) not in cores:
        cores[(lo, hi)] = envelope_core(frame, lo, hi)
    return cores[(lo, hi)]


@dataclass(frozen=True)
class PartnerRow:
    """One live partner row, with what every query row reuses computed once.

    `own` holds, for each outward edge normal `n` of the partner core `Q_r`, the support
    `max over Q_r of n.v` plus `min over D_r of n.y`: the part of that facet's bound that
    does not depend on the query core.
    """

    domain: Polygon
    core: Polygon
    own: tuple[tuple[Q, Q, Q], ...]
    float_domain: tuple[tuple[float, float], ...]
    float_own: tuple[tuple[float, float, float], ...]


def _normals(polygon: Polygon) -> list[tuple[Q, Q]]:
    """Outward edge normals of a counterclockwise convex polygon."""
    return [
        (b[1] - a[1], a[0] - b[0])
        for a, b in zip(polygon, polygon[1:] + polygon[:1], strict=True)
    ]


def prepare_partner(domain: Polygon, core: Polygon) -> PartnerRow:
    own = tuple(
        (
            nx,
            ny,
            max(nx * x + ny * y for x, y in core) + min(nx * x + ny * y for x, y in domain),
        )
        for nx, ny in _normals(core)
    )
    return PartnerRow(
        domain,
        core,
        own,
        tuple((float(x), float(y)) for x, y in domain),
        tuple((float(a), float(b), float(c)) for a, b, c in own),
    )


def collision_planes(core: Polygon, partner: PartnerRow) -> list[Halfplane]:
    """The facets of `Q_r - Q_i`, each shifted by `min over D_r`, by edge merge.

    A Minkowski sum's facet normals are its summands' edge normals: `Q_r`'s, with support
    `h_r(n) - min over Q_i of n.w`, and `-Q_i`'s, which are `-m` for each normal `m` of
    `Q_i`, with support `max over Q_i of m.w - min over Q_r of m.v`. The planes cut out
    exactly the polygon the hull of the pairwise differences bounds, with no hull built.
    """
    planes: list[Halfplane] = [
        (nx, ny, own - min(nx * x + ny * y for x, y in core)) for nx, ny, own in partner.own
    ]
    for mx, my in _normals(core):
        planes.append(
            (
                -mx,
                -my,
                max(mx * x + my * y for x, y in core)
                - min(mx * x + my * y for x, y in partner.core)
                - max(mx * x + my * y for x, y in partner.domain),
            )
        )
    return planes


def _integer_planes(planes: list[Halfplane]) -> list[tuple[int, int, int]]:
    result: list[tuple[int, int, int]] = []
    for a, b, c in planes:
        scale = math.lcm(a.denominator, b.denominator, c.denominator)
        result.append(
            (
                a.numerator * (scale // a.denominator),
                b.numerator * (scale // b.denominator),
                c.numerator * (scale // c.denominator),
            )
        )
    return result


def _satisfies(planes: list[tuple[int, int, int]], point: Point) -> bool:
    """`a x + b y <= c` for every integer plane, at a rational point, by cross-multiplying."""
    x, y = point
    z = math.lcm(x.denominator, y.denominator)
    px, py = x.numerator * (z // x.denominator), y.numerator * (z // y.denominator)
    return all(a * px + b * py <= c * z for a, b, c in planes)


def collision_region(core: Polygon, domain: Polygon, partner_rows: list[PartnerRow]) -> Polygon:
    """A convex part of `domain` every centre of which collides with every partner pose.

    The exact set is the domain cut by every facet `n.p <= h + min over D_r of n.y` of
    every live partner row's `Q_r - Q_i` (`collision_planes`). It is located in floating
    point; the region returned is the hull of grid points pulled inside it and of the
    domain's own vertices, each kept only if it satisfies every one of those halfplanes and
    the domain's exactly, in integers; the checker verifies the same inequalities itself.
    """
    if not _float_collision(core, domain, partner_rows):
        return []
    planes = [plane for partner in partner_rows for plane in collision_planes(core, partner)]
    region = [(float(x), float(y)) for x, y in domain]
    for a, b, c in planes:
        region = _float_clip(region, float(a), float(b), float(c))
        if len(region) < 3:
            return []
    exact = _integer_planes(planes + convex_halfplanes(domain))
    cx = sum(x for x, _ in region) / len(region)
    cy = sum(y for _, y in region) / len(region)
    kept = [vertex for vertex in domain if _satisfies(exact, vertex)]
    for x, y in region:
        for pull in (2.0**-12, 2.0**-6, 2.0**-3):
            point = (
                Q(round((x + (cx - x) * pull) * GRID), GRID),
                Q(round((y + (cy - y) * pull) * GRID), GRID),
            )
            if _satisfies(exact, point):
                kept.append(point)
                break
    polygon = hull(kept)
    return polygon if len(polygon) >= 3 and area2(polygon) > 0 else []


def _float_collision(core: Polygon, domain: Polygon, partner_rows: list[PartnerRow]) -> bool:
    """Whether the collision set meets the domain in floating point: a cheap prefilter
    that only decides whether the exact construction is worth attempting."""
    query = [(float(x), float(y)) for x, y in core]
    query_normals = [
        (b[1] - a[1], a[0] - b[0]) for a, b in zip(query, query[1:] + query[:1], strict=True)
    ]
    region = [(float(x), float(y)) for x, y in domain]
    for partner in partner_rows:
        partner_core = [(float(x), float(y)) for x, y in partner.core]
        planes = [
            (nx, ny, own - min(nx * x + ny * y for x, y in query))
            for nx, ny, own in partner.float_own
        ]
        planes.extend(
            (
                -mx,
                -my,
                max(mx * x + my * y for x, y in query)
                - min(mx * x + my * y for x, y in partner_core)
                - max(mx * x + my * y for x, y in partner.float_domain),
            )
            for mx, my in query_normals
        )
        for a, b, c in planes:
            region = _float_clip(region, a, b, c)
            if len(region) < 3:
                return False
    return True


def partner_cover(
    frame: Frame, accepted: list[Row], cores: dict[tuple[Q, Q], Polygon]
) -> tuple[list[dict[str, Any]], list[PartnerRow]]:
    """A partner's complete pose cover in the grammar, and its live rows."""
    given: list[dict[str, Any]] = []
    live: list[PartnerRow] = []
    for row in accepted:
        vertices = [
            vertex for polygon in row["residual_polygons"] for vertex in points(polygon)
        ]
        item: dict[str, Any] = {
            "reference": row["reference"],
            "interval": row["interval"],
            "domain": [],
            "core": [],
        }
        if vertices:
            lo, hi = (Q(value) for value in row["interval"])
            domain, core = hull(vertices), cached_core(frame, lo, hi, cores)
            item["domain"], item["core"] = encode(domain), encode(core)
            live.append(prepare_partner(domain, core))
        given.append(item)
    return given, live


def bounded_vertices(original: Polygon, limit: int) -> list[int]:
    """Indices of at most `limit` vertices, dropping the one that costs least area first."""
    kept = list(range(len(original)))
    while len(kept) > max(limit, 3):
        losses = []
        for position, index in enumerate(kept):
            a = original[kept[position - 1]]
            b = original[index]
            c = original[kept[(position + 1) % len(kept)]]
            losses.append(abs((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])))
        kept.pop(losses.index(min(losses)))
    return kept


def produce_row(
    frame: Frame,
    *,
    node_id: str,
    step_index: int,
    row_index: int,
    owner: int,
    predecessor: Row,
    groups: dict[int, Polygon],
    partners: dict[int, list[PartnerRow]] | None = None,
    cores: dict[tuple[Q, Q], Polygon] | None = None,
) -> tuple[dict[str, Any], Row, list[Halfplane]]:
    lo, hi = (Q(value) for value in predecessor["interval"])
    reference = {"kind": "phase3", "node": node_id, "step": step_index, "row": row_index}
    required = intersect(hull(points(predecessor["outer_domain"])), wall_lines(frame, lo, hi))
    accepted: Row = {
        "interval": [str(lo), str(hi)],
        "reference": reference,
        "outer_domain": [],
        "residual_polygons": [],
    }
    row: dict[str, Any] = {
        "interval": [str(lo), str(hi)],
        "prior_reference": predecessor["reference"],
        "reference": reference,
        "input_domain": encode(required),
        "core_vertices": [],
        "collision_regions": [],
        "residual_polygons": [],
        "common_core_halfplanes": [],
        "outer_bounds": [],
        "outer_domain": [],
    }
    if not required:
        return row, accepted, []
    core = cached_core(frame, lo, hi, cores)
    row["core_vertices"] = encode(core)
    pieces = [list(required)]
    positive = area2(required) > 0
    removed = [region for region in forbidden_regions(groups, owner, core) if region]
    for partner, live in sorted((partners or {}).items()):
        region = collision_region(core, required, live)
        if region:
            row["collision_regions"].append({"partner": partner, "vertices": encode(region)})
            removed.append(region)
    for region in removed:
        pieces = subtract(pieces, region, keep_area_only=positive)
        if not pieces:
            break
    residual = [hull(piece) for piece in pieces]
    vertices = [point for piece in residual for point in piece]
    planes = common_core_planes(hull(core), vertices)
    row["residual_polygons"] = [encode(piece) for piece in residual]
    row["common_core_halfplanes"] = [
        {"normal": [str(nx), str(ny)], "upper": str(upper)} for nx, ny, upper in planes
    ]
    if vertices:
        bounds = [
            (Q(nx), Q(ny), outward_round(max(nx * x + ny * y for x, y in vertices)))
            for nx, ny in SUPPORT_NORMALS
        ]
        outer = hull(intersect(frame.world(owner), bounds))
        row["outer_bounds"] = [
            {"normal": [str(nx), str(ny)], "upper": str(upper)} for nx, ny, upper in bounds
        ]
        row["outer_domain"] = encode(outer)
        accepted["outer_domain"] = encode(outer)
        accepted["residual_polygons"] = [encode(piece) for piece in residual]
    return row, accepted, planes


def _float_clip(
    polygon: list[tuple[float, float]], a: float, b: float, c: float
) -> list[tuple[float, float]]:
    out: list[tuple[float, float]] = []
    for p, q in zip(polygon, polygon[1:] + polygon[:1], strict=True):
        dp, dq = a * p[0] + b * p[1] - c, a * q[0] + b * q[1] - c
        if dp <= 0:
            out.append(p)
        if dp * dq < 0:
            z = dp / (dp - dq)
            out.append((p[0] + z * (q[0] - p[0]), p[1] + z * (q[1] - p[1])))
    return out


def kernel_points(frame: Frame, planes: list[Halfplane]) -> list[Point]:
    """Grid points proved, exactly, to satisfy every plane; the region is found in floats.

    Clipping a box by a few hundred exact halfplanes in turn compounds denominators, so
    the plane intersection is located in floating point only to choose candidates; each
    candidate is a grid point checked exactly against every plane, as the checker will.
    """
    if not planes:
        return []
    side = float(frame.length)
    region = [(0.0, 0.0), (side, 0.0), (side, side), (0.0, side)]
    for a, b, c in planes:
        region = _float_clip(region, float(a), float(b), float(c))
        if not region:
            return []
    cx = sum(x for x, _ in region) / len(region)
    cy = sum(y for _, y in region) / len(region)
    candidates = [(Q(round(cx * GRID), GRID), Q(round(cy * GRID), GRID))]
    candidates.extend(
        (
            Q(round((x + (cx - x) * pull) * GRID), GRID),
            Q(round((y + (cy - y) * pull) * GRID), GRID),
        )
        for x, y in region
        for pull in (2.0**-12, 2.0**-6, 0.25, 0.5)
    )
    return [
        point
        for point in dict.fromkeys(candidates)
        if all(0 <= coordinate <= frame.length for coordinate in point)
        and all(a * point[0] + b * point[1] <= c for a, b, c in planes)
    ]


@dataclass
class Production:
    seed: dict[str, Any]
    node: dict[str, Any]
    rounds: list[dict[str, Any]] = field(default_factory=list)
    outcome: str = "stalled"


def produce(
    frame: Frame,
    mask: Sequence[int],
    *,
    bins: int = 64,
    max_rounds: int = 8,
    budget: Budget,
    node_id: str = "n17-subpattern",
    progress: Callable[[dict[str, Any]], None] | None = None,
    collision: bool = True,
    hull_limit: int | None = 16,
    stop_at: float | None = None,
) -> Production:
    """Seed, then round-robin complete steps until closure, a stall or the round cap."""
    seed = build_seed(frame, mask, bins=bins, budget=budget)
    seed_sha = content_sha256(seed)
    groups = {owner: hull(points(seed["groups"][str(owner)])) for owner in mask}
    rows: dict[int, list[Row]] = {
        owner: [
            {
                "interval": row["interval"],
                "reference": row["reference"],
                "outer_domain": row["outer_domain"],
                "residual_polygons": row["residual_polygons"],
            }
            for row in seed["cells"][str(owner)]
        ]
        for owner in mask
    }
    initial = {
        "groups": {str(owner): encode(groups[owner]) for owner in mask},
        "cell_references": {
            str(owner): [row["reference"] for row in rows[owner]] for owner in mask
        },
    }
    steps: list[dict[str, Any]] = []
    closure: dict[str, Any] | None = None
    production = Production(seed, {})
    cores: dict[tuple[Q, Q], Polygon] = {}
    previous: list[dict[str, Any]] | None = None
    for round_index in range(max_rounds):
        for owner in mask:
            if time.monotonic() >= budget.deadline:
                raise IncompleteError("producer wall ceiling")
            if stop_at is not None and steps and time.monotonic() >= stop_at:
                production.outcome = "time_cap"
                break
            step_index = len(steps)
            prior_hulls = {str(other): encode(groups[other]) for other in mask}
            covers: dict[str, list[dict[str, Any]]] = {}
            partners: dict[int, list[PartnerRow]] = {}
            if collision:
                for other in mask:
                    if other != owner:
                        given, live = partner_cover(frame, rows[other], cores)
                        if live:
                            covers[str(other)], partners[other] = given, live
            produced = [
                produce_row(
                    frame,
                    node_id=node_id,
                    step_index=step_index,
                    row_index=index,
                    owner=owner,
                    predecessor=predecessor,
                    groups=groups,
                    partners=partners,
                    cores=cores,
                )
                for index, predecessor in enumerate(rows[owner])
            ]
            planes = [plane for _, _, row_planes in produced for plane in row_planes]
            kernel = kernel_points(frame, planes)
            step: dict[str, Any] = {
                "index": step_index,
                "owner": owner,
                "allowed_half_angle": ["0", "1"],
                "prior_partner_pose_covers": covers,
                "prior_owned_hulls": prior_hulls,
                "rows": [row for row, _, _ in produced],
                "complete": True,
                "common_owned_kernel": [_encode_point(point) for point in kernel],
            }
            if any(accepted["residual_polygons"] for _, accepted, _ in produced) and (
                groups[owner] or kernel
            ):
                original = hull(groups[owner] + kernel)
                new_points, witnesses = compress(original)
                receipt: dict[str, Any] = {
                    "vertices": [_encode_point(point) for point in new_points],
                    "witnesses": witnesses,
                    "denominator": GRID,
                    "original_vertices": len(original),
                    "retained_vertices": len(new_points),
                }
                if hull_limit is not None and new_points == original:
                    keep = bounded_vertices(original, hull_limit)
                    new_points = [original[index] for index in keep]
                    receipt.update(
                        vertices=[_encode_point(point) for point in new_points],
                        witnesses=[witnesses[index] for index in keep],
                        retained_vertices=len(new_points),
                        mode="replace",
                    )
                    groups[owner] = hull(new_points)
                else:
                    groups[owner] = hull(groups[owner] + new_points)
                step["compression_source_hull"] = encode(original)
                step["inner_grid_compression"] = receipt
            rows[owner] = [accepted for _, accepted, _ in produced]
            steps.append(step)
            if progress is not None:
                progress(
                    {
                        "round": round_index,
                        "step": step_index,
                        "owner": frame.cell_names[owner],
                        "live_rows": sum(1 for row in rows[owner] if row["residual_polygons"]),
                        "owned_hull_vertices": len(groups[owner]),
                    }
                )
            closure = derived_closure(owner, step_index, groups, rows)
            if closure is not None:
                break
        extents = [owner_extents(frame, owner, rows[owner], groups[owner]) for owner in mask]
        production.rounds.append(
            {"round": round_index, "steps": len(steps), "extents": extents}
        )
        if production.outcome == "time_cap":
            break
        if closure is not None:
            production.outcome = "closed"
            break
        if extents == previous:
            production.outcome = "stalled"
            break
        previous = extents
    else:
        production.outcome = "round_cap"
    source = {"sha256": seed_sha}
    production.node = {
        "schema": "exact_generic_owned_hull_v1",
        "node_id": node_id,
        "parent": None,
        "constraints": [],
        "guard_source": None,
        "mask_index": None,
        "mask": list(mask),
        "U": str(frame.cap),
        "B": str(frame.scale),
        "source": source,
        "initial": initial,
        "steps": steps,
        "final_state": {
            "mask_index": None,
            "mask": list(mask),
            "U": str(frame.cap),
            "B": str(frame.scale),
            "constraints": [],
            "guard": {},
            "guard_source": None,
            "source": source,
            "world": seed["world"],
            "groups": {str(owner): encode(groups[owner]) for owner in mask},
            "cells": {str(owner): rows[owner] for owner in mask},
        },
        "contradiction": closure,
        "closed": closure is not None,
        "terminal": closure is not None,
        "mask_exclusion_proved": False,
        "global_optimality_proved": False,
    }
    return production
