"""Standing verifier of saved n17 kernel certificates (seed and node), in exact rationals.

Retained from lane R3's review verifier (exp-249, `audit-W7/verify_cert.py.txt`), with its
mathematics unchanged and its independence kept: it imports nothing from
`sqpack.hull_kernel`, from the checker `check_n17_subpattern`, from the selector or from
the branch and bound. The cells and the cap come from `check_n17_capacity_one_cover`'s
exact polygons, or from a JSON cells file whose SHA-256 the caller states.

What it re-derives, from scratch:

- both objects' digests (the file names) and their canonical JSON; the node's source is
  the seed; the seed's world is the cells; the mask is the node's;
- the seed: every owned point is owned (bisection on the half-angle with an interval
  product bound), every row is the cell cut by the row's legal box;
- the owned-hull chain through every step: the prior hulls equal the state, kernel points
  satisfy every live row's common-core planes (recomputed from the published core and
  residual vertices), compression witnesses are exact convex combinations on the grid;
- every partner pose cover: its domain is the hull of the partner's current residual
  vertices, its core is strictly inside the partner's square over the row;
- for the rows checked in full: the required domain, the strict core, every collision
  region against every live partner row and every facet of the exact Minkowski
  difference, and coverage of the required domain by forbidden, collision and residual
  regions by an exact area argument (the leftover area of a closed clipping subtraction
  must be zero);
- the closure: derived after each step and equal to the declared one, with no step after
  it, and the final state equal to the derived one.

Modes. Full, the default, checks every row of every step and is what admission requires.
`--sample N` checks `N` rows per step drawn by a seeded generator, and every row of the
closure step: a planning check, not an admission.

The receipt names the seed's and node's digests, the cells' source, the mask, the closure,
the mode and the counts, this module's SHA-256 read at import, and PASS or FAIL with the
first failure.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import random
import time
from dataclasses import dataclass, field
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

SCHEMA = "n17-certificate-verification/v1"
KIND = "kernel"
MODULE_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
HULL_LIMIT = 16
GRID = 2**20

Point = tuple[Q, Q]
Plane = tuple[Q, Q, Q]


class VerificationError(Exception):
    """The certificate fails a check; the message names the first that failed."""


def require(condition: bool, message: str) -> None:  # noqa: FBT001
    if not condition:
        raise VerificationError(message)


def point(v: Any) -> Point:
    return (Q(v[0]), Q(v[1]))


def poly(vertices: Any) -> list[Point]:
    return [point(p) for p in vertices]


# ---------------------------------------------------------------------------
# Geometry, written independently of the kernel
# ---------------------------------------------------------------------------


def cross(o: Point, a: Point, b: Point) -> Q:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def hull(points: list[Point]) -> list[Point]:
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    lower: list[Point] = []
    upper: list[Point] = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def area2(polygon: list[Point]) -> Q:
    if len(polygon) < 3:
        return Q(0)
    n = len(polygon)
    return abs(
        sum(
            (
                polygon[i][0] * polygon[(i + 1) % n][1]
                - polygon[(i + 1) % n][0] * polygon[i][1]
                for i in range(n)
            ),
            Q(0),
        )
    )


def clip_closed(polygon: list[Point], a: Q, b: Q, c: Q) -> list[Point]:
    """The polygon cut to the closed half-plane `a x + b y <= c`, exactly."""
    if not polygon:
        return []
    out: list[Point] = []
    n = len(polygon)
    for i in range(n):
        p, q = polygon[i], polygon[(i + 1) % n]
        fp, fq = a * p[0] + b * p[1] - c, a * q[0] + b * q[1] - c
        if fp <= 0:
            out.append(p)
        if (fp < 0 < fq) or (fq < 0 < fp):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    result: list[Point] = []
    for p in out:
        if not result or result[-1] != p:
            result.append(p)
    if len(result) > 1 and result[0] == result[-1]:
        result.pop()
    return result


def planes_of(polygon: list[Point]) -> list[Plane]:
    """Outward half-planes `(a, b, c)`, `a x + b y <= c`, of a convex polygon."""
    h = hull(polygon)
    require(len(h) >= 3, "planes of a degenerate polygon")
    out: list[Plane] = []
    for i in range(len(h)):
        p, q = h[i], h[(i + 1) % len(h)]
        a, b = q[1] - p[1], p[0] - q[0]
        out.append((a, b, a * p[0] + b * p[1]))
    return out


def inside(polygon: list[Point], pt: Point) -> bool:
    return all(a * pt[0] + b * pt[1] <= c for a, b, c in planes_of(polygon))


def same_set(first: list[Point], second: list[Point]) -> bool:
    return hull(first) == hull(second)


def trig(t: Q) -> tuple[Q, Q]:
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def wall_box(lo: Q, hi: Q, cap: Q) -> list[Point]:
    """The closed legal centre box for the half-angle row `[lo, hi]`.

    `cos + sin` is concave in the angle on `[0, pi/2]` and the chart is monotone, so its
    least value on the row is at an endpoint.
    """
    h = min(sum(trig(t), Q(0)) for t in (lo, hi)) / 2
    return [(h, h), (cap - h, h), (cap - h, cap - h), (h, cap - h)]


def intersect_convex(polygon: list[Point], other: list[Point]) -> list[Point]:
    for a, b, c in planes_of(other):
        polygon = clip_closed(polygon, a, b, c)
        if not polygon:
            break
    return polygon


def quad_min_positive(a0: Q, a1: Q, a2: Q, lo: Q, hi: Q) -> bool:
    """`a0 + a1 t + a2 t^2 > 0` on `[lo, hi]`, by the endpoints and an interior vertex."""
    values = [a0 + a1 * lo + a2 * lo * lo, a0 + a1 * hi + a2 * hi * hi]
    if a2 > 0:
        tv = -a1 / (2 * a2)
        if lo < tv < hi:
            values.append(a0 + a1 * tv + a2 * tv * tv)
    return min(values) > 0


def core_strict(core: list[Point], lo: Q, hi: Q) -> bool:
    """Every core vertex has both body coordinates below 1/2 in size over the row.

    The body coordinates are `c x + s y` and `-s x + c y` with the half-angle chart's
    `c`, `s`; both conditions are multiplied by `1 + t^2 > 0`.
    """
    half = Q(1, 2)
    for x, y in core:
        for sg in (1, -1):
            if not quad_min_positive(half - sg * x, -2 * sg * y, half + sg * x, lo, hi):
                return False
            if not quad_min_positive(half - sg * y, 2 * sg * x, half + sg * y, lo, hi):
                return False
    return True


def minkowski_diff(first: list[Point], second: list[Point]) -> list[Point]:
    """`hull(first - second)` for convex polygons."""
    return hull([(a[0] - b[0], a[1] - b[1]) for a in first for b in second])


def owned(
    cell: list[Point], pt: Point, cap: Q, *, lo: Q = Q(0), hi: Q = Q(1), depth: int = 0
) -> bool:
    """The point is strictly inside the square for every centre in the cell cut by the
    legal box and every half-angle in `[lo, hi]`: bisection with an interval product bound.
    """
    legal = intersect_convex(list(cell), wall_box(lo, hi, cap))
    if not legal:
        return True
    c_lo, s_lo = trig(lo)
    c_hi, s_hi = trig(hi)
    c_min, c_max = min(c_lo, c_hi), max(c_lo, c_hi)
    s_min, s_max = min(s_lo, s_hi), max(s_lo, s_hi)
    ok = True
    for vx, vy in legal:
        dx, dy = pt[0] - vx, pt[1] - vy
        for a, d in ((dx, dy), (dy, -dx)):
            values = [a * cc + d * ss for cc in (c_min, c_max) for ss in (s_min, s_max)]
            if max(abs(v) for v in values) >= Q(1, 2):
                ok = False
                break
        if not ok:
            break
    if ok:
        return True
    if depth >= 18:
        return False
    mid = (lo + hi) / 2
    return owned(cell, pt, cap, lo=lo, hi=mid, depth=depth + 1) and owned(
        cell, pt, cap, lo=mid, hi=hi, depth=depth + 1
    )


def subtract_pieces(pieces: list[list[Point]], region: list[Point]) -> list[list[Point]]:
    """Closed convex pieces tiling, up to boundaries, the pieces minus the region."""
    planes = planes_of(region)
    out: list[list[Point]] = []
    for piece in pieces:
        rest = piece
        for a, b, c in planes:
            outside = clip_closed(rest, -a, -b, -c)
            if outside and area2(outside) > 0:
                out.append(outside)
            rest = clip_closed(rest, a, b, c)
            if not rest or area2(rest) == 0:
                break
    return out


def covered_by_area(domain: list[Point], regions: list[list[Point]]) -> tuple[bool, int]:
    """Whether the closed convex regions cover the domain (of positive area), exactly.

    The uncovered set is relatively open, so it is nonempty exactly when the leftover
    area is positive.
    """
    pieces = [domain]
    for region in regions:
        if len(hull(region)) < 3:
            continue
        pieces = subtract_pieces(pieces, region)
        if not pieces:
            return True, 0
    left = sum((area2(p) for p in pieces), Q(0))
    return left == 0, len(pieces)


# ---------------------------------------------------------------------------
# The cells, the objects and the state
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Cells:
    """The frame: cell names and exact polygons in order, the cap, and their source."""

    names: tuple[str, ...]
    polygons: tuple[tuple[Point, ...], ...]
    cap: Q
    source: dict[str, Any]


def cover_cells() -> Cells:
    """The n17 unique-state cover's exact cells, from the cover tool."""
    from devtools import check_n17_capacity_one_cover as cover  # noqa: PLC0415

    cells = cover.build_cover(cover.UNIQUE_24)
    return Cells(
        tuple(cell.name for cell in cells),
        tuple(tuple((Q(x), Q(y)) for x, y in cell.vertices) for cell in cells),
        Q(cover.U),
        {"kind": "cover", "design": cover.UNIQUE_24.name},
    )


def file_cells(path: Path, sha256: str) -> Cells:
    """Cells from a JSON file `{"U", "order", "cells"}` whose digest must be `sha256`."""
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    require(digest == sha256, f"cells file digest {digest} is not the stated one")
    data = json.loads(raw)
    names = tuple(data["order"])
    return Cells(
        names,
        tuple(tuple(poly(data["cells"][name])) for name in names),
        Q(data["U"]),
        {"kind": "file", "path": str(path), "sha256": digest},
    )


def load_object(path: Path, kind: str) -> tuple[dict[str, Any], str]:
    """A gzipped canonical JSON object named by the SHA-256 of its bytes."""
    raw = gzip.decompress(path.read_bytes())
    digest = hashlib.sha256(raw).hexdigest()
    require(path.name == f"{kind}-{digest}.json.gz", f"{kind} digest mismatch: {digest}")
    document = json.loads(raw)
    canonical = json.dumps(document, sort_keys=True, separators=(",", ":")).encode()
    require(hashlib.sha256(canonical).hexdigest() == digest, f"{kind} is not canonical JSON")
    return document, digest


@dataclass
class Row:
    interval: tuple[Q, Q]
    reference: Any
    outer: list[Point]
    residual: list[list[Point]]


@dataclass
class State:
    cells: list[list[Point]]
    cap: Q
    bins: int
    mask: list[int]
    groups: dict[int, list[Point]] = field(default_factory=dict[int, list[Point]])
    rows: dict[int, list[Row]] = field(default_factory=dict[int, list[Row]])
    stats: dict[str, int] = field(default_factory=dict[str, int])

    def tick(self, key: str, amount: int = 1) -> None:
        self.stats[key] = self.stats.get(key, 0) + amount


def check_frame(seed: dict[str, Any], node: dict[str, Any], cells: Cells) -> list[int]:
    require(seed["schema"] == "generic_wall_seed_v1", "seed schema")
    require(node["schema"] == "exact_generic_owned_hull_v1", "node schema")
    for document in (seed, node):
        require(Q(document["U"]) == cells.cap, "the cap is not the cells' cap")
        require(Q(document["B"]) == 1, "field and physical coordinates differ")
    mask = seed["mask"]
    require(node["mask"] == mask, "the node's mask is not the seed's")
    require(
        isinstance(mask, list)
        and len(set(mask)) == len(mask) >= 2
        and all(isinstance(k, int) and 0 <= k < len(cells.names) for k in mask),
        "the mask is not a set of cell indices",
    )
    require(
        node["parent"] is None and node["constraints"] == [] and node["guard_source"] is None,
        "the node is not a root node",
    )
    require(len(seed["world"]) == len(cells.names), "the seed's world has the wrong size")
    for k, polygon in enumerate(cells.polygons):
        require(same_set(poly(seed["world"][k]), list(polygon)), f"world cell {k} differs")
    return mask


def check_seed(state: State, seed: dict[str, Any], node: dict[str, Any]) -> None:
    bins = state.bins
    for o in state.mask:
        points = poly(seed["groups"][str(o)])
        for pt in points:
            require(owned(state.cells[o], pt, state.cap), f"seed point {pt} of {o} not owned")
        state.groups[o] = hull(points)
        seed_rows = seed["cells"][str(o)]
        require(len(seed_rows) == bins, f"seed owner {o} has the wrong number of rows")
        rows: list[Row] = []
        for i, r in enumerate(seed_rows):
            lo, hi = Q(r["interval"][0]), Q(r["interval"][1])
            require((lo, hi) == (Q(i, bins), Q(i + 1, bins)), f"seed row {o}/{i} interval")
            domain = intersect_convex(list(state.cells[o]), wall_box(lo, hi, state.cap))
            require(same_set(poly(r["outer_domain"]), domain), f"seed row {o}/{i} domain")
            residual = [poly(x) for x in r["residual_polygons"]]
            require(
                (residual == [] and domain == [])
                or (len(residual) == 1 and same_set(residual[0], domain)),
                f"seed row {o}/{i} residual",
            )
            require(
                r["reference"] == {"kind": "wall_seed", "owner": o, "row": i},
                f"seed row {o}/{i} reference",
            )
            rows.append(
                Row((lo, hi), r["reference"], hull(domain), [hull(x) for x in residual])
            )
        state.rows[o] = rows
        state.tick("seed_points", len(points))
        state.tick("seed_rows", len(seed_rows))
    for o in state.mask:
        require(
            same_set(poly(node["initial"]["groups"][str(o)]), state.groups[o]),
            f"initial group {o}",
        )
        require(
            node["initial"]["cell_references"][str(o)] == [r.reference for r in state.rows[o]],
            f"initial references {o}",
        )


Partner = tuple[list[Point], list[Point], tuple[Q, Q]]


def check_partners(state: State, step: dict[str, Any], si: int) -> dict[int, list[Partner]]:
    owner = step["owner"]
    partners: dict[int, list[Partner]] = {}
    for key, items in step["prior_partner_pose_covers"].items():
        pj = int(key)
        require(pj in state.mask and pj != owner, f"step {si}: partner {pj}")
        rows = state.rows[pj]
        require(len(items) == len(rows), f"step {si}: partner {pj} cover length")
        live: list[Partner] = []
        for item, r in zip(items, rows, strict=True):
            require(item["reference"] == r.reference, f"step {si}: partner {pj} reference")
            interval = (Q(item["interval"][0]), Q(item["interval"][1]))
            require(interval == r.interval, f"step {si}: partner {pj} interval")
            vertices = [v for polygon in r.residual for v in polygon]
            if not vertices:
                require(item["domain"] == [] and item["core"] == [], f"step {si}: dead row")
                continue
            domain = hull(vertices)
            require(
                same_set(poly(item["domain"]), domain),
                f"step {si} partner {pj} row {r.reference['row']} domain",
            )
            core = hull(poly(item["core"]))
            require(len(core) >= 3 and area2(core) > 0, f"step {si}: partner {pj} core")
            require(core_strict(core, *r.interval), f"step {si} partner {pj} core not strict")
            live.append((domain, core, r.interval))
        require(bool(live), f"step {si}: empty partner cover")
        partners[pj] = live
        state.tick("partner_rows", len(live))
    return partners


def check_collisions(
    state: State,
    row: dict[str, Any],
    *,
    where: str,
    core: list[Point],
    required: list[Point],
    partners: dict[int, list[Partner]],
) -> list[list[Point]]:
    regions: list[list[Point]] = []
    for item in row["collision_regions"]:
        pj = item["partner"]
        require(pj in partners, f"{where}: collision partner {pj}")
        region = hull(poly(item["vertices"]))
        require(len(region) >= 3 and area2(region) > 0, f"{where}: degenerate region")
        require(
            all(inside(required, v) for v in region),
            f"{where}: collision region escapes the required domain",
        )
        for domain, partner_core, _ in partners[pj]:
            difference = minkowski_diff(partner_core, core)
            require(len(difference) >= 3, f"{where}: degenerate difference")
            for a, b, c in planes_of(difference):
                bound = c + min(a * y[0] + b * y[1] for y in domain)
                state.tick("collision_facet_checks", len(region))
                for v in region:
                    require(
                        a * v[0] + b * v[1] <= bound,
                        f"{where} partner {pj}: region escapes the collision set",
                    )
        regions.append(region)
        state.tick("collision_regions")
    return regions


def check_cover(
    state: State,
    owner: int,
    *,
    where: str,
    core: list[Point],
    required: list[Point],
    regions: tuple[list[list[Point]], list[list[Point]]],
) -> None:
    """The required domain is covered by forbidden, collision and residual regions."""
    collisions, residual = regions
    forbidden = [
        minkowski_diff(state.groups[oj], core)
        for oj in state.mask
        if oj != owner and state.groups[oj]
    ]
    every = forbidden + collisions + residual
    if area2(required) > 0:
        ok, left = covered_by_area(required, every)
        require(ok, f"{where}: required domain NOT covered (leftover pieces {left})")
    else:
        points = list(required)
        if len(points) == 2:
            points.append(
                ((points[0][0] + points[1][0]) / 2, (points[0][1] + points[1][1]) / 2)
            )
        for pt in points:
            require(
                any(inside(r, pt) for r in every if len(hull(r)) >= 3)
                or any(pt in r for r in residual),
                f"{where}: degenerate row uncovered",
            )
    state.tick("cover_checks")


def check_step(
    state: State, step: dict[str, Any], si: int, node_id: Any, full: set[int]
) -> tuple[list[Row], list[Plane], bool]:
    owner = step["owner"]
    partners = check_partners(state, step, si)
    new_rows: list[Row] = []
    all_planes: list[Plane] = []
    any_live = False
    for ri, row in enumerate(step["rows"]):
        where = f"step {si} row {ri}"
        prior = state.rows[owner][ri]
        lo, hi = Q(row["interval"][0]), Q(row["interval"][1])
        require(
            (lo, hi) == prior.interval == (Q(ri, state.bins), Q(ri + 1, state.bins)),
            f"{where}: interval",
        )
        require(row["prior_reference"] == prior.reference, f"{where}: prior reference")
        require(
            row["reference"] == {"kind": "phase3", "node": node_id, "step": si, "row": ri},
            f"{where}: reference",
        )
        require(row.get("self_hull_cuts", []) == [], f"{where}: self-hull cuts")
        required = (
            intersect_convex(list(prior.outer), wall_box(lo, hi, state.cap))
            if prior.outer
            else []
        )
        residual = [hull(poly(x)) for x in row["residual_polygons"]]
        vertices = [v for polygon in residual for v in polygon]
        if not required:
            require(
                residual == []
                and row["collision_regions"] == []
                and row["common_core_halfplanes"] == []
                and row["outer_bounds"] == []
                and row["outer_domain"] == [],
                f"{where}: a dead row carries data",
            )
            new_rows.append(Row((lo, hi), row["reference"], [], []))
            continue
        core = hull(poly(row["core_vertices"]))
        require(len(core) >= 3 and area2(core) > 0, f"{where}: degenerate core")
        require(core_strict(core, lo, hi), f"{where}: core not strict")
        planes: list[Plane] = []
        if vertices:
            for k in range(len(core)):
                p, q = core[k], core[(k + 1) % len(core)]
                a, b = q[1] - p[1], p[0] - q[0]
                least = min(a * v[0] + b * v[1] for v in vertices)
                planes.append((a, b, a * p[0] + b * p[1] + least))
        published = [
            (Q(it["normal"][0]), Q(it["normal"][1]), Q(it["upper"]))
            for it in row["common_core_halfplanes"]
        ]
        require(set(published) == set(planes), f"{where}: common-core planes")
        all_planes.extend(planes)
        bounds = [
            (Q(it["normal"][0]), Q(it["normal"][1]), Q(it["upper"]))
            for it in row["outer_bounds"]
        ]
        if vertices:
            any_live = True
            require(len(bounds) == 8, f"{where}: outer bounds")
            for a, b, c in bounds:
                require(all(a * v[0] + b * v[1] <= c for v in vertices), f"{where}: bound")
            outer = list(state.cells[owner])
            for a, b, c in bounds:
                outer = clip_closed(outer, a, b, c)
            outer = hull(outer)
            require(same_set(poly(row["outer_domain"]), outer), f"{where}: outer domain")
        else:
            require(bounds == [] and row["outer_domain"] == [], f"{where}: dead bounds")
            outer = []
        if ri in full:
            state.tick("rows_full")
            regions = check_collisions(
                state, row, where=where, core=core, required=required, partners=partners
            )
            check_cover(
                state,
                owner,
                where=where,
                core=core,
                required=required,
                regions=(regions, residual),
            )
        new_rows.append(Row((lo, hi), row["reference"], outer, residual))
    return new_rows, all_planes, any_live


def compress(
    state: State, step: dict[str, Any], si: int, planes: list[Plane], *, any_live: bool
) -> None:
    owner = step["owner"]
    kernel = poly(step["common_owned_kernel"])
    for pt in kernel:
        require(0 <= pt[0] <= state.cap and 0 <= pt[1] <= state.cap, f"step {si}: kernel")
        require(
            all(a * pt[0] + b * pt[1] <= c for a, b, c in planes),
            f"step {si}: kernel point fails a plane",
        )
    if not (any_live and (state.groups[owner] or kernel)):
        require("inner_grid_compression" not in step, f"step {si}: unexpected compression")
        return
    original = hull(state.groups[owner] + kernel)
    require(same_set(poly(step["compression_source_hull"]), original), f"step {si}: source")
    record = step["inner_grid_compression"]
    points = poly(record["vertices"])
    require(len(points) == len(record["witnesses"]) > 0, f"step {si}: witnesses")
    for pt, witness in zip(points, record["witnesses"], strict=True):
        indices, weights = witness["indices"], [Q(x) for x in witness["weights"]]
        require(
            1 <= len(indices) <= 3
            and all(0 <= k < len(original) for k in indices)
            and all(x >= 0 for x in weights)
            and sum(weights) == 1,
            f"step {si}: witness weights",
        )
        combined = (
            sum(x * original[k][0] for k, x in zip(indices, weights, strict=True)),
            sum(x * original[k][1] for k, x in zip(indices, weights, strict=True)),
        )
        require(combined == pt == point(witness["point"]), f"step {si}: witness point")
        require(
            (pt[0] * GRID).denominator == 1 and (pt[1] * GRID).denominator == 1,
            f"step {si}: off the grid",
        )
    if record.get("mode") == "replace":
        state.groups[owner] = hull(points)
    else:
        state.groups[owner] = hull(state.groups[owner] + points)
    require(len(state.groups[owner]) <= HULL_LIMIT, f"step {si}: owned hull too large")


def derive_closure(state: State, owner: int, si: int) -> dict[str, Any] | None:
    if not any(r.residual for r in state.rows[owner]):
        return {"kind": "all_parent_poses_forbidden", "owner": owner, "step": si}
    for oj in sorted(state.mask):
        if oj != owner and state.groups[oj] and state.groups[owner]:
            common = (
                intersect_convex(list(state.groups[owner]), state.groups[oj])
                if len(state.groups[oj]) >= 3
                else []
            )
            if common:
                return {
                    "kind": "owned_hulls_intersect",
                    "owners": sorted((owner, oj)),
                    "step": si,
                }
    return None


def check_final(state: State, node: dict[str, Any], *, stall: bool) -> None:
    final = node["final_state"]
    for o in state.mask:
        require(same_set(poly(final["groups"][str(o)]), state.groups[o]), f"final group {o}")
        require(len(final["cells"][str(o)]) == len(state.rows[o]), f"final rows {o}")
        for recorded, r in zip(final["cells"][str(o)], state.rows[o], strict=True):
            require(recorded["reference"] == r.reference, f"final reference {o}")
            require(
                same_set(poly(recorded["outer_domain"]), r.outer)
                if r.outer
                else recorded["outer_domain"] == [],
                f"final outer domain {o}",
            )
            require(
                len(recorded["residual_polygons"]) == len(r.residual)
                and all(
                    same_set(poly(a), b)
                    for a, b in zip(recorded["residual_polygons"], r.residual, strict=True)
                ),
                f"final residual {o}",
            )
    require(node["closed"] is (not stall) and node["terminal"] is (not stall), "closed flags")
    require(
        node["mask_exclusion_proved"] is False and node["global_optimality_proved"] is False,
        "the node claims more than a closure",
    )


def verify_objects(
    directory: Path,
    cells: Cells,
    *,
    sample: int | None = None,
    sample_seed: int = 12345,
    progress: bool = False,
) -> dict[str, Any]:
    """Verify the seed and node saved in `directory`; raises on the first failure."""
    seeds = sorted(directory.glob("seed-*.json.gz"))
    nodes = sorted(directory.glob("node-*.json.gz"))
    require(
        len(seeds) == 1 and len(nodes) == 1, "the directory must hold one seed and one node"
    )
    seed, seed_sha = load_object(seeds[0], "seed")
    node, node_sha = load_object(nodes[0], "node")
    require(node["source"]["sha256"] == seed_sha, "the node's source is not the seed")
    mask = check_frame(seed, node, cells)
    bins = seed["bins"]
    require(isinstance(bins, int) and bins > 0, "bins")
    state = State([list(p) for p in cells.polygons], cells.cap, bins, mask)
    clock = time.perf_counter()
    check_seed(state, seed, node)
    contradiction = node["contradiction"]
    stall = contradiction is None
    closure_step = -1 if stall else contradiction["step"]
    rng = random.Random(sample_seed)
    derived: dict[str, Any] | None = None
    steps = node["steps"]
    for si, step in enumerate(steps):
        require(
            step["index"] == si and step["owner"] in mask and step["complete"] is True,
            f"step {si}: header",
        )
        require(step["allowed_half_angle"] == ["0", "1"], f"step {si}: allowed half-angle")
        owner = step["owner"]
        for o in mask:
            require(
                same_set(poly(step["prior_owned_hulls"][str(o)]), state.groups[o]),
                f"step {si}: prior hull {o}",
            )
        full = (
            set(range(bins))
            if sample is None or si == closure_step
            else set(rng.sample(range(bins), min(sample, bins)))
        )
        new_rows, planes, any_live = check_step(state, step, si, node["node_id"], full)
        compress(state, step, si, planes, any_live=any_live)
        state.rows[owner] = new_rows
        state.tick("steps")
        derived = derive_closure(state, owner, si)
        if progress:
            live = sum(1 for r in new_rows if r.residual)
            print(
                json.dumps(
                    {
                        "step": si,
                        "owner": owner,
                        "live_rows": live,
                        "rows_checked_in_full": len(full),
                        "closure": derived is not None,
                        "seconds": round(time.perf_counter() - clock, 1),
                    }
                ),
                flush=True,
            )
        if derived is not None:
            require(
                si == closure_step
                and derived["kind"] == contradiction["kind"]
                and derived.get("owner") == contradiction.get("owner"),
                f"step {si}: the derived closure is not the declared one",
            )
            require(si == len(steps) - 1, "steps after the closure")
            break
    else:
        require(stall, "no closure derived")
    check_final(state, node, stall=stall)
    return {
        "certificate": {"seed_sha256": seed_sha, "node_sha256": node_sha},
        "mask": mask,
        "cells": [cells.names[k] for k in mask],
        "bins": bins,
        "closure": contradiction,
        "closed": not stall,
        "counts": dict(sorted(state.stats.items())),
    }


def verify(
    directory: Path,
    cells: Cells,
    *,
    sample: int | None = None,
    sample_seed: int = 12345,
    progress: bool = False,
) -> dict[str, Any]:
    """The verification receipt: PASS only for a closed certificate that checks in full."""
    clock = time.perf_counter()
    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "verifier": KIND,
        "verifier_sha256": MODULE_SHA256,
        "directory": str(directory),
        "cells_source": cells.source,
        "mode": "full" if sample is None else "sample",
        "sample_rows_per_step": sample,
        "sample_seed": None if sample is None else sample_seed,
    }
    try:
        result = verify_objects(
            directory, cells, sample=sample, sample_seed=sample_seed, progress=progress
        )
    except VerificationError as failure:
        receipt.update(status="FAIL", failure=str(failure))
    except (
        KeyError,
        TypeError,
        ValueError,
        IndexError,
        AttributeError,
        ZeroDivisionError,
        OSError,
    ) as failure:
        receipt.update(status="FAIL", failure=f"malformed certificate: {failure!r}")
    else:
        receipt.update(result)
        closed = result["closed"]
        receipt.update(
            status="PASS" if closed else "FAIL",
            failure=None if closed else "the node is a stall, not a closure",
        )
    receipt["seconds"] = round(time.perf_counter() - clock, 3)
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("directory", type=Path, help="holds seed-*.json.gz, node-*.json.gz")
    _ = parser.add_argument("--cells", type=Path, help="a JSON cells file instead of the cover")
    _ = parser.add_argument("--cells-sha256", help="the cells file's SHA-256, required with it")
    _ = parser.add_argument("--sample", type=int, default=None, help="rows per step (sample)")
    _ = parser.add_argument("--sample-seed", type=int, default=12345)
    _ = parser.add_argument("--output", type=Path, required=True, help="the receipt")
    _ = parser.add_argument("--progress", action="store_true")
    arguments = parser.parse_args(argv)
    if arguments.cells is not None:
        if not arguments.cells_sha256:
            parser.error("--cells needs --cells-sha256")
        cells = file_cells(arguments.cells, arguments.cells_sha256)
    else:
        cells = cover_cells()
    receipt = verify(
        arguments.directory,
        cells,
        sample=arguments.sample,
        sample_seed=arguments.sample_seed,
        progress=arguments.progress,
    )
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    _ = arguments.output.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: receipt.get(k) for k in ("status", "failure", "mode", "seconds")}))
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
