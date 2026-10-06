"""Diagnose a selector flag the kernel stalls on: where its survivors are, whether the
pattern can be placed after all, and what holds the kernel open (H-267). A diagnostic,
not a certificate.

A flag is a sub-pattern the float selector (`select_n17_sub_patterns`) could not place.
The kernel (`check_n17_subpattern`) tries to exclude it by ownership induction over angle
rows; when it stalls, either the pattern fits at the cap and no sound prover can exclude it
(a false flag), or it does not fit and the induction is too weak to show it. This tool
separates the two as far as evidence allows.

Survivors (`domains`). A saved node's `final_state` holds every owner's rows as the
induction left them: a row is an interval of the half-angle chart `t = tan(theta/2)` on
`[0, 1]` and the residual polygons of centres not yet excluded at those angles; a row with
a residual is live. Every pose of a real placement lies in its owner's survivors, since
each cut is proved. `final_state` sorts before `steps` in the canonical bytes, so it is
read off the front of the file by `check_n17_subpattern.stream_node` without parsing a
step. Per owner the summary gives the live angle blocks with their centre extents, the
first-order core and wall losses of the live rows (`row_losses`), the kernel's owned hull,
and the ideal owned region of the survivors (`ideal_owned`: what every surviving square
covers), overall and per 15-degree sector (`sector_owned`), which is what a branch on
the owner's angle would give each child to cut with.

Placement (`place`). The selector's own `search`, warm started from survivor samples, and
a multistart of the selector's descent from survivor samples. The best pose is broken
down constraint by constraint (`breakdown`): each pair's separating-axis gap, each wall
and each cell halfplane. `largest_side` bisects on the side `s` of the squares, the cells
and the cap held fixed, for the largest side the search still places, a measure of the
obstruction in length units; `angle_profile` holds one owner at a series of angles and
reports the least violation found at each. A pose the search places is rounded to
rationals, each angle to a rational half-angle `t`, which gives a rational cosine and
sine, and checked exactly (`exact_check`): `sqpack.verify.verify_packing` over `Fraction`
for unit shape, container and pairwise separation, touching included, and each centre in
its closed cell. Only that check makes a placement count; `check` re-runs it on a
recorded placement.

Support (`support`). For sampled surviving poses of each owner, whether every partner has
a surviving pose that clears it (`pairwise_support`). A pose every partner supports is
beyond any sound cut that reasons from one partner at a time, however fine the rows or
exact the core; a pose some partner cannot support, by a margin, is one the kernel keeps
only through its losses. The split is between a stall that needs joint reasoning and one
that needs a sharper pairwise cut.

Margins (`margins`). For each cell, the largest side found for the pattern without it,
from the best pose: how much room each cell's absence leaves.
"""

from __future__ import annotations

import argparse
import functools
import json
import math
import time
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import minimize

from devtools import check_n17_capacity_one_cover as cover
from devtools import select_n17_sub_patterns as selector
from devtools.check_n17_subpattern import stream_node
from devtools.provenance import REPO, provenance, repository_path
from sqpack.verify import verify_packing

SCHEMA = "n17-flag-diagnosis/v1"
PLACEMENT_SCHEMA = "n17-flag-placement/v1"
STATUS = (
    "diagnostic, not a certificate: survivors are read from a saved node, placements are "
    "float searches, and only the exact check of a rounded placement counts"
)
PROVENANCE = provenance(Path(__file__))
Floats = NDArray[np.float64]
# A surviving pose is tested against a residual with this slack, in length units: the
# residuals are exact, the float test of a point against them is not.
INSIDE = 1e-9


# ---------------------------------------------------------------------------
# Survivors
# ---------------------------------------------------------------------------


def theta_of(t: float) -> float:
    """The angle of the half-angle chart value `t = tan(theta/2)`."""
    return 2.0 * math.atan(t)


def t_of(theta: float) -> float:
    """The chart value of an angle, taken modulo a quarter turn into `[0, pi/2)`."""
    return math.tan(math.fmod(math.fmod(theta, math.pi / 2) + math.pi / 2, math.pi / 2) / 2)


def polygon_area(polygon: Floats) -> float:
    if len(polygon) < 3:
        return 0.0
    x, y = polygon[:, 0], polygon[:, 1]
    return abs(float(np.dot(x, np.roll(y, -1)) - np.dot(np.roll(x, -1), y))) / 2


def inside_convex(polygon: Floats, point: tuple[float, float], slack: float = INSIDE) -> bool:
    """Whether a point lies in a convex polygon of either orientation, within `slack`."""
    if len(polygon) < 3:
        return False
    edges = np.roll(polygon, -1, axis=0) - polygon
    offsets = np.asarray(point) - polygon
    cross = edges[:, 0] * offsets[:, 1] - edges[:, 1] * offsets[:, 0]
    lengths = np.hypot(edges[:, 0], edges[:, 1])
    lengths[lengths == 0] = 1.0
    signed = cross / lengths
    return bool(np.all(signed >= -slack) or np.all(signed <= slack))


@dataclass(frozen=True)
class Row:
    """One angle row: its chart interval and the residual centres it leaves."""

    t_lo: float
    t_hi: float
    residuals: tuple[Floats, ...]

    @property
    def live(self) -> bool:
        return bool(self.residuals)

    @property
    def area(self) -> float:
        return sum(polygon_area(polygon) for polygon in self.residuals)


@dataclass(frozen=True)
class Owner:
    """An owner's rows as the induction left them, and its owned hull."""

    cell: int
    name: str
    rows: tuple[Row, ...]
    owned: Floats

    def live_rows(self) -> list[Row]:
        return [row for row in self.rows if row.live]

    @functools.cached_property
    def sampler(self) -> tuple[list[Row], Floats, list[Floats]]:
        """The live rows, their sampling weights (residual area) and, per row, its
        residuals' areas: computed once, since sampling draws from them many times."""
        live = self.live_rows()
        weights = np.array([row.area for row in live]) + 1e-12
        areas = [np.array([polygon_area(p) for p in row.residuals]) + 1e-15 for row in live]
        return live, weights / weights.sum(), [area / area.sum() for area in areas]

    def holds(self, pose: tuple[float, float, float]) -> bool:
        """Whether a pose `(x, y, theta)` lies in the survivors, within `INSIDE`."""
        t = t_of(pose[2])
        for row in self.rows:
            if row.t_lo - 1e-12 <= t <= row.t_hi + 1e-12 and any(
                inside_convex(polygon, (pose[0], pose[1])) for polygon in row.residuals
            ):
                return True
        return False


@dataclass(frozen=True)
class Survivors:
    """Every owner of a saved node, in mask order, with the node's identity."""

    mask: tuple[int, ...]
    owners: tuple[Owner, ...]
    node_file: str
    node_id: str


def _floats(polygon: list[list[str]]) -> Floats:
    return np.array([[float(Fraction(x)), float(Fraction(y))] for x, y in polygon])


def recorded_path(path: Path) -> str:
    """A path as a record names it: repository-relative inside the repository, and the
    file name alone outside it, where saved objects are named by their content id."""
    return repository_path(path) if path.resolve().is_relative_to(REPO) else path.name


def read_survivors(node_file: Path, names: tuple[str, ...]) -> Survivors:
    """The final rows and owned hulls of a saved node, read without parsing a step."""
    header, _ = stream_node(node_file)
    final = header["final_state"]
    mask = tuple(int(cell) for cell in header["mask"])
    owners: list[Owner] = []
    for cell in mask:
        rows = tuple(
            Row(
                float(Fraction(row["interval"][0])),
                float(Fraction(row["interval"][1])),
                tuple(_floats(polygon) for polygon in row["residual_polygons"]),
            )
            for row in final["cells"][str(cell)]
        )
        owners.append(Owner(cell, names[cell], rows, _floats(final["groups"][str(cell)])))
    return Survivors(mask, tuple(owners), recorded_path(node_file), str(header["node_id"]))


def angle_blocks(owner: Owner) -> list[dict[str, Any]]:
    """Maximal runs of consecutive live rows, each with its angles and centre extents."""
    blocks: list[list[Row]] = []
    for row in owner.rows:
        if row.live and blocks and blocks[-1][-1].t_hi == row.t_lo and blocks[-1][-1].live:
            blocks[-1].append(row)
        elif row.live:
            blocks.append([row])
    summary: list[dict[str, Any]] = []
    for block in blocks:
        points = np.concatenate([polygon for row in block for polygon in row.residuals])
        summary.append(
            {
                "degrees": [
                    round(math.degrees(theta_of(block[0].t_lo)), 4),
                    round(math.degrees(theta_of(block[-1].t_hi)), 4),
                ],
                "rows": len(block),
                "x": [round(float(points[:, 0].min()), 5), round(float(points[:, 0].max()), 5)],
                "y": [round(float(points[:, 1].min()), 5), round(float(points[:, 1].max()), 5)],
                "largest_residual_area": round(max(row.area for row in block), 7),
                "ideal_owned_area": round(polygon_area(ideal_owned(block)), 6),
            }
        )
    return summary


SECTOR_DEGREES = 15.0


def sector_owned(owner: Owner, width: float = SECTOR_DEGREES) -> list[dict[str, Any]]:
    """The ideal owned area if the owner were confined to one angle sector: what a branch
    on its angle alone would give each child to cut with, before any further cut."""
    sectors: list[dict[str, Any]] = []
    start = 0.0
    while start < 90.0 - 1e-9:
        rows = [
            row
            for row in owner.live_rows()
            if math.degrees(theta_of(row.t_lo)) < start + width - 1e-9
            and math.degrees(theta_of(row.t_hi)) > start + 1e-9
        ]
        if rows:
            sectors.append(
                {
                    "degrees": [start, start + width],
                    "live_rows": len(rows),
                    "ideal_owned_area": round(polygon_area(ideal_owned(rows)), 6),
                }
            )
        start += width
    return sectors


def half_extent(theta: float) -> float:
    """A unit square's axis-parallel half-extent `(|cos| + |sin|)/2` at an angle."""
    return (abs(math.cos(theta)) + abs(math.sin(theta))) / 2


def row_losses(row: Row, cap: float) -> dict[str, float]:
    """A row's two first-order losses, in length units, as floats for planning.

    The core loss: the envelope core (the producer's default) is the square at the row's
    middle angle shrunk to fit every square of the row, half-side `1/(2 (cos(D/2) +
    sin(D/2)))` for row width `D`, so each face loses `1/2` minus that. The wall loss: the
    legal box uses the least half-extent over the row, so a centre may sit nearer a wall
    by the spread of the half-extent over the row, when a residual vertex lies in that
    band (`producer.wall_loss`)."""
    lo, hi = theta_of(row.t_lo), theta_of(row.t_hi)
    width = hi - lo
    core = 0.5 - 0.5 / (math.cos(width / 2) + math.sin(width / 2))
    least = min(half_extent(lo), half_extent(hi))
    most = (
        half_extent(math.pi / 4)
        if lo < math.pi / 4 < hi
        else max(half_extent(lo), half_extent(hi))
    )
    near = any(
        min(float(x), float(y)) < most or max(float(x), float(y)) > cap - most
        for polygon in row.residuals
        for x, y in polygon
    )
    return {"core": core, "wall": most - least if near else 0.0}


def clip_convex(polygon: Floats, a: float, b: float, c: float) -> Floats:
    """The part of a convex polygon with `a x + b y <= c`."""
    if len(polygon) == 0:
        return polygon
    values = polygon @ np.array([a, b]) - c
    out: list[Floats] = []
    for index in range(len(polygon)):
        p, q = polygon[index], polygon[(index + 1) % len(polygon)]
        vp, vq = values[index], values[(index + 1) % len(polygon)]
        if vp <= 0:
            out.append(p)
        if (vp < 0 < vq) or (vq < 0 < vp):
            out.append(p + vp / (vp - vq) * (q - p))
    return np.array(out) if out else np.empty((0, 2))


def ideal_owned(rows: list[Row], *, angles_per_row: int = 3) -> Floats:
    """The points every surviving pose's square covers, in floats: the intersection of the
    squares at every residual vertex and `angles_per_row` angles of each row. At a fixed
    angle the intersection over a convex residual is the one over its vertices; sampling
    the angles makes this an outer estimate of the exact intersection over the row."""
    points = np.concatenate([polygon for row in rows for polygon in row.residuals])
    low, high = points.min(axis=0) - 1.0, points.max(axis=0) + 1.0
    region = np.array(
        [[low[0], low[1]], [high[0], low[1]], [high[0], high[1]], [low[0], high[1]]]
    )
    for row in rows:
        lo, hi = theta_of(row.t_lo), theta_of(row.t_hi)
        vertices = np.concatenate(row.residuals)
        for theta in np.linspace(lo, hi, angles_per_row):
            for normal in (theta, theta + math.pi / 2):
                n = np.array([math.cos(normal), math.sin(normal)])
                reach = vertices @ n
                region = clip_convex(region, n[0], n[1], float(reach.min()) + 0.5)
                region = clip_convex(region, -n[0], -n[1], -float(reach.max()) + 0.5)
                if len(region) == 0:
                    return region
    return region


def chart_widths(rows: Sequence[Row]) -> dict[str, int]:
    """How many rows have each width in the chart, `1/64` for a seed row at 64 bins."""
    counts: dict[int, int] = {}
    for row in rows:
        denominator = round(1 / (row.t_hi - row.t_lo))
        counts[denominator] = counts.get(denominator, 0) + 1
    return {f"1/{n}": counts[n] for n in sorted(counts)}


def summarise(survivors: Survivors, cap: float = selector.CAP) -> dict[str, Any]:
    """Per owner: rows, live rows, live angle blocks, centre extents, the row losses at the
    live rows, the owned hull and the ideal owned region of the survivors (`ideal_owned`)."""
    owners: dict[str, Any] = {}
    for owner in survivors.owners:
        live = owner.live_rows()
        record: dict[str, Any] = {
            "cell": owner.cell,
            "rows": len(owner.rows),
            "live_rows": len(live),
            "live_degrees": round(
                sum(math.degrees(theta_of(r.t_hi) - theta_of(r.t_lo)) for r in live), 4
            ),
            "rows_by_chart_width": chart_widths(owner.rows),
            "owned_hull_vertices": len(owner.owned),
            "owned_hull_area": round(polygon_area(owner.owned), 6),
        }
        if live:
            points = np.concatenate([polygon for row in live for polygon in row.residuals])
            record["x"] = [
                round(float(points[:, 0].min()), 5),
                round(float(points[:, 0].max()), 5),
            ]
            record["y"] = [
                round(float(points[:, 1].min()), 5),
                round(float(points[:, 1].max()), 5),
            ]
            record["largest_residual_area"] = round(max(row.area for row in live), 7)
            widths = [math.degrees(theta_of(r.t_hi) - theta_of(r.t_lo)) for r in live]
            record["live_row_degrees"] = [round(min(widths), 4), round(max(widths), 4)]
            record["live_rows_by_chart_width"] = chart_widths(live)
            losses = [row_losses(r, cap) for r in live]
            record["largest_core_loss"] = round(max(loss["core"] for loss in losses), 6)
            record["largest_wall_loss"] = round(max(loss["wall"] for loss in losses), 6)
            record["ideal_owned_area"] = round(polygon_area(ideal_owned(live)), 6)
            record["blocks"] = angle_blocks(owner)
            record["sectors"] = sector_owned(owner)
        owners[owner.name] = record
    return {
        "node_file": survivors.node_file,
        "node_id": survivors.node_id,
        "live_rows": sum(len(owner.live_rows()) for owner in survivors.owners),
        "rows": sum(len(owner.rows) for owner in survivors.owners),
        "owners": owners,
    }


# ---------------------------------------------------------------------------
# Placement from the survivors
# ---------------------------------------------------------------------------


def _point_in(polygon: Floats, rng: np.random.Generator) -> tuple[float, float]:
    """A point uniform in a convex polygon, by fan triangles weighted by area."""
    if len(polygon) < 3:
        weights = rng.dirichlet(np.ones(len(polygon)))
        point = weights @ polygon
        return float(point[0]), float(point[1])
    anchor = polygon[0]
    triangles = [(anchor, polygon[i], polygon[i + 1]) for i in range(1, len(polygon) - 1)]
    areas = np.array([polygon_area(np.array(triangle)) for triangle in triangles])
    total = float(areas.sum())
    index = int(rng.choice(len(triangles), p=areas / total)) if total > 0 else 0
    a, b, c = triangles[index]
    r, s = rng.random(), rng.random()
    if r + s > 1:
        r, s = 1 - r, 1 - s
    point = a + r * (b - a) + s * (c - a)
    return float(point[0]), float(point[1])


def sample_pose_of(owner: Owner, rng: np.random.Generator) -> tuple[float, float, float]:
    """One owner's pose in its survivors: a live row by residual area, an angle uniform in
    the row, a centre uniform in one of its residuals."""
    live, weights, areas = owner.sampler
    if not live:
        raise ValueError(f"{owner.name} has no live row: the node closed")
    index = int(rng.choice(len(live), p=weights))
    row = live[index]
    polygon = row.residuals[int(rng.choice(len(areas[index]), p=areas[index]))]
    x, y = _point_in(polygon, rng)
    return x, y, float(rng.uniform(theta_of(row.t_lo), theta_of(row.t_hi)))


def sample_pose(survivors: Survivors, rng: np.random.Generator) -> Floats:
    """A pose in the survivors, one owner at a time (`sample_pose_of`), in mask order."""
    return np.array([sample_pose_of(owner, rng) for owner in survivors.owners])


def in_survivors(survivors: Survivors, pose: Floats) -> list[bool]:
    """For each owner, whether its row of the pose lies in its survivors."""
    return [
        owner.holds((float(row[0]), float(row[1]), float(row[2])))
        for owner, row in zip(survivors.owners, pose, strict=True)
    ]


def breakdown(
    geometry: selector.Geometry, cells: tuple[int, ...], pose: Floats, *, limit: int = 16
) -> list[dict[str, Any]]:
    """Every constraint of a pose with its gap in length units, tightest first: each pair's
    best separating-axis gap, each square's four walls and each cell halfplane. A negative
    gap is a violation; the selector's violation is the least gap, negated."""
    cap = geometry.cap
    names = [geometry.names[cell] for cell in cells]
    x, y, angle = pose[:, 0], pose[:, 1], pose[:, 2]
    rows: list[dict[str, Any]] = []
    support = (np.abs(np.cos(angle)) + np.abs(np.sin(angle))) / 2
    for i, name in enumerate(names):
        for wall, gap in (
            ("x=0", x[i] - support[i]),
            ("x=U", cap - support[i] - x[i]),
            ("y=0", y[i] - support[i]),
            ("y=U", cap - support[i] - y[i]),
        ):
            rows.append({"kind": "wall", "what": f"{name} {wall}", "gap": float(gap)})
        planes = geometry.halfplanes[cells[i]]
        for edge, (a, b, c) in enumerate(planes):
            gap = c - (a * x[i] + b * y[i])
            rows.append({"kind": "cell", "what": f"{name} edge {edge}", "gap": float(gap)})
    for i in range(len(cells)):
        for j in range(i + 1, len(cells)):
            if not geometry.interact[cells[i], cells[j]]:
                continue
            dx, dy = x[j] - x[i], y[j] - y[i]
            best, axis_of = -math.inf, ""
            for owner, base in ((names[i], angle[i]), (names[j], angle[j])):
                for turn in (0.0, math.pi / 2):
                    axis = base + turn
                    reach = abs(math.cos(axis) * dx + math.sin(axis) * dy)
                    half_i = (
                        abs(math.cos(angle[i] - axis)) + abs(math.sin(angle[i] - axis))
                    ) / 2
                    half_j = (
                        abs(math.cos(angle[j] - axis)) + abs(math.sin(angle[j] - axis))
                    ) / 2
                    gap = reach - half_i - half_j
                    if gap > best:
                        best, axis_of = gap, f"{owner} {'edge' if turn == 0 else 'edge+90'}"
            rows.append(
                {
                    "kind": "pair",
                    "what": f"{names[i]} / {names[j]}",
                    "gap": float(best),
                    "axis": axis_of,
                }
            )
    rows.sort(key=lambda row: row["gap"])
    return [{**row, "gap": round(row["gap"], 7)} for row in rows[:limit]]


def pose_record(
    geometry: selector.Geometry,
    survivors: Survivors | None,
    cells: tuple[int, ...],
    pose: Floats,
) -> dict[str, Any]:
    """A pose with its violation, its components, its binding constraints and, given the
    survivors, which owners it leaves outside them."""
    problem = selector.Problem(geometry, cells)
    record: dict[str, Any] = {
        "violation": problem.violation(pose),
        "components": problem.violations(pose),
        "pose": [
            {
                "cell": geometry.names[cell],
                "x": float(row[0]),
                "y": float(row[1]),
                "degrees": round(math.degrees(float(row[2])) % 90, 4),
            }
            for cell, row in zip(cells, pose, strict=True)
        ],
        "binding": breakdown(geometry, cells, pose),
    }
    if survivors is not None:
        held = in_survivors(survivors, pose)
        record["outside_survivors"] = [
            owner.name
            for owner, inside in zip(survivors.owners, held, strict=True)
            if not inside
        ]
    return record


def multistart(
    geometry: selector.Geometry,
    survivors: Survivors,
    *,
    starts: int,
    seed: int,
) -> dict[str, Any]:
    """Descents of the selector's penalty from survivor samples, each scored by the
    selector's violation; the best is polished and finished as the selector does."""
    cells = survivors.mask
    problem = selector.Problem(geometry, cells, fast=True)
    rng = np.random.default_rng(seed)
    values: list[float] = []
    best: tuple[float, Floats] | None = None
    clock = time.perf_counter()
    with selector.single_thread_blas():
        for _ in range(starts):
            pose = problem.descend(sample_pose(survivors, rng), polish=False)
            value = problem.violation(pose)
            values.append(value)
            if best is None or value < best[0]:
                best = (value, pose)
    assert best is not None
    polished = selector.finish(problem, problem.descend(best[1], polish=True))
    if problem.violation(polished) < best[0]:
        best = (problem.violation(polished), polished)
    ordered = sorted(values)
    return {
        "starts": starts,
        "seed": seed,
        "placed": best[0] <= selector.MARGIN,
        "violation_quantiles": {
            q: ordered[min(len(ordered) - 1, int(float(q) * len(ordered)))]
            for q in ("0", "0.01", "0.1", "0.5")
        },
        "best": pose_record(geometry, survivors, cells, best[1]),
        "best_pose": best[1].tolist(),
        "seconds": round(time.perf_counter() - clock, 2),
    }


def selector_search(
    geometry: selector.Geometry,
    survivors: Survivors,
    *,
    warm_count: int,
    seed: int,
    budget: selector.Budget,
) -> dict[str, Any]:
    """The selector's own `search`, warm started from survivor samples (each with a row to
    redraw in the deep stage, cycling over the owners)."""
    cells = survivors.mask
    rng = np.random.default_rng(seed)
    warm = [(index % len(cells), sample_pose(survivors, rng)) for index in range(warm_count)]
    clock = time.perf_counter()
    verdict = selector.search(geometry, cells, rng, budget, warm)
    return {
        "warm_starts": warm_count,
        "seed": seed,
        "budget": {
            "starts": budget.starts,
            "hops": budget.hops,
            "deep_starts": budget.deep_starts,
            "deep_hops": budget.deep_hops,
            "margin": budget.margin,
        },
        "placed": verdict.feasible,
        "attempts": verdict.attempts,
        "found_by": verdict.found_by,
        "best": pose_record(geometry, survivors, cells, verdict.pose),
        "best_pose": verdict.pose.tolist(),
        "seconds": round(time.perf_counter() - clock, 2),
    }


# ---------------------------------------------------------------------------
# How far from placeable: the largest side that fits
# ---------------------------------------------------------------------------


def scaled_geometry(geometry: selector.Geometry, side: float) -> selector.Geometry:
    """The pattern for squares of side `side`, as unit squares: every length over `side`."""
    return selector.make_geometry(
        [polygon / side for polygon in geometry.polygons],
        list(geometry.names),
        cap=geometry.cap / side,
    )


def largest_side(
    geometry: selector.Geometry,
    cells: tuple[int, ...],
    start: Floats,
    *,
    survivors: Survivors | None = None,
    seed: int = 1,
    starts: int = 24,
    steps: int = 14,
    low: float = 0.9,
    high: float = 1.0,
) -> dict[str, Any]:
    """The largest side `s` at which the search places squares of side `s` with centres in
    the pattern's cells and inside the container, by bisection on `s` in `[low, high]`.

    A side is placed when one of `starts` descents (the best pose so far rescaled, then
    survivor samples or cell samples) reaches the selector's margin. A placement at `s` is
    evidence that `s` fits; a failure is not evidence that it does not, so the result is
    a float lower estimate of the largest fitting side, not a bound on it. When no side
    in the range fails, `first_unplaced_side` is None and the side is at least `high`
    less the last step."""
    rng = np.random.default_rng(seed)
    placed_side, placed_pose = 0.0, None
    failed = False
    best = start.copy()

    def attempt(side: float) -> Floats | None:
        nonlocal best
        problem = selector.Problem(scaled_geometry(geometry, side), cells, fast=True)
        tries = [best.copy()]
        for _ in range(starts - 1):
            sample = (
                sample_pose(survivors, rng)
                if survivors is not None and rng.random() < 0.5
                else problem.random_pose(rng) * np.array([side, side, 1.0])
            )
            tries.append(sample)
        for index, pose in enumerate(tries):
            scaled = pose.copy()
            scaled[:, :2] /= side
            found = problem.descend(scaled, polish=False)
            if problem.violation(found) > selector.MARGIN:
                found = selector.finish(problem, found) if index == 0 else found
            if problem.violation(found) <= selector.MARGIN:
                found[:, :2] *= side
                return found
        return None

    with selector.single_thread_blas():
        if (found := attempt(low)) is None:
            return {"placed_side": None, "searched": [low, high]}
        placed_side, placed_pose, best = low, found, found
        for _ in range(steps):
            middle = (low + high) / 2
            found = attempt(middle)
            if found is None:
                high, failed = middle, True
            else:
                low, placed_side, placed_pose, best = middle, middle, found, found
    assert placed_pose is not None
    return {
        "placed_side": placed_side,
        "first_unplaced_side": high if failed else None,
        "pose_at_placed_side": placed_pose.tolist(),
    }


def minus_one_margins(
    geometry: selector.Geometry,
    cells: tuple[int, ...],
    pose: Floats,
    *,
    seed: int = 1,
    starts: int = 12,
    steps: int = 8,
) -> dict[str, Any]:
    """For each cell, the largest side found for the pattern without it, from the pattern's
    pose less that square: how much room each cell's absence leaves, so how much each
    cell costs. Above one, the smaller pattern fits with slack; a side with no unplaced
    side above it is the top of the bisection, and the true one may be larger."""
    margins: dict[str, Any] = {}
    for row, cell in enumerate(cells):
        rest = cells[:row] + cells[row + 1 :]
        found = largest_side(
            geometry,
            rest,
            np.delete(pose, row, axis=0),
            seed=seed,
            starts=starts,
            steps=steps,
            low=0.95,
            high=1.2,
        )
        margins[geometry.names[cell]] = {
            key: found[key] for key in ("placed_side", "first_unplaced_side") if key in found
        }
    return margins


# ---------------------------------------------------------------------------
# Exact check of a rounded placement
# ---------------------------------------------------------------------------


def _sign(value: Fraction) -> int:
    return (value > 0) - (value < 0)


def rational_pose(
    pose: Floats, *, angle_denominator: int = 10**6, position_denominator: int = 10**6
) -> list[tuple[Fraction, Fraction, Fraction]]:
    """Each row `(x, y, theta)` as `(x, y, t)` in rationals, `t = tan(theta/2)` of the angle
    taken into `[0, pi/2)`; the rational `t` gives a rational cosine and sine."""
    return [
        (
            Fraction(float(x)).limit_denominator(position_denominator),
            Fraction(float(y)).limit_denominator(position_denominator),
            Fraction(t_of(float(theta))).limit_denominator(angle_denominator),
        )
        for x, y, theta in pose
    ]


def exact_square(x: Fraction, y: Fraction, t: Fraction) -> list[tuple[Fraction, Fraction]]:
    """The corners of the unit square centred at `(x, y)` turned by `2 atan t`, exactly,
    in the order `sqpack.verify.corners_from_poses` gives."""
    c, s = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
    ux, uy, vx, vy = c / 2, s / 2, -s / 2, c / 2
    return [
        (x - ux - vx, y - uy - vy),
        (x + ux - vx, y + uy - vy),
        (x + ux + vx, y + uy + vy),
        (x - ux + vx, y - uy + vy),
    ]


def in_closed_cell(
    polygon: tuple[tuple[Fraction, Fraction], ...], x: Fraction, y: Fraction
) -> bool:
    """Whether a point lies in a closed convex polygon of either orientation, exactly."""
    signs = set()
    for index, (px, py) in enumerate(polygon):
        qx, qy = polygon[(index + 1) % len(polygon)]
        signs.add(_sign((qx - px) * (y - py) - (qy - py) * (x - px)))
    return not ({1, -1} <= signs)


def exact_check(
    cell_names: list[str], poses: list[tuple[Fraction, Fraction, Fraction]], design: str
) -> dict[str, Any]:
    """The rounded placement checked exactly: unit squares in `[0, U]^2` with pairwise
    disjoint interiors (`verify_packing` over `Fraction`), each centre in its closed cell,
    and each pair's least separating-axis gap in floats for the reader."""
    cells = {cell.name: cell.vertices for cell in cover.build_cover(cover.DESIGNS[design])}
    squares = [exact_square(x, y, t) for x, y, t in poses]
    report = verify_packing(squares, cover.U, sign=_sign)
    outside = [
        name
        for name, (x, y, _) in zip(cell_names, poses, strict=True)
        if not in_closed_cell(cells[name], x, y)
    ]
    gaps: list[float] = []
    for i, first in enumerate(squares):
        for second in squares[i + 1 :]:
            best = -math.inf
            for axis in [*_axes(first), *_axes(second)]:
                a = [axis[0] * px + axis[1] * py for px, py in first]
                b = [axis[0] * px + axis[1] * py for px, py in second]
                best = max(best, float(max(min(b) - max(a), min(a) - max(b))))
            gaps.append(best)
    walls = min(
        float(min(px, py, cover.U - px, cover.U - py))
        for square in squares
        for px, py in square
    )
    return {
        "valid": report.valid and not outside,
        "packing_failures": [list(failure) for failure in report.failures],
        "touching_pairs": report.touching_pairs,
        "centres_outside_cells": outside,
        "least_pair_gap": min(gaps) if gaps else None,
        "least_wall_gap": walls,
    }


def _axes(square: list[tuple[Fraction, Fraction]]) -> list[tuple[Fraction, Fraction]]:
    """The square's two edge directions, unit length since the cosine and sine are exact."""
    (ax, ay), (bx, by), (_, _), (dx, dy) = square
    return [(bx - ax, by - ay), (dx - ax, dy - ay)]


# ---------------------------------------------------------------------------
# Pairwise support: what any one-partner-at-a-time cut could still remove
# ---------------------------------------------------------------------------


def pair_gaps(first: Floats, second: Floats) -> Floats:
    """The separating-axis gap of one square against a batch: positive apart, zero
    touching, negative overlapping. `first` is one pose `(x, y, theta)`, `second` a batch."""
    dx, dy = second[:, 0] - first[0], second[:, 1] - first[1]
    best = np.full(len(second), -np.inf)
    for base in (np.full(len(second), first[2]), second[:, 2]):
        for turn in (0.0, math.pi / 2):
            axis = base + turn
            reach = np.abs(np.cos(axis) * dx + np.sin(axis) * dy)
            own = (np.abs(np.cos(first[2] - axis)) + np.abs(np.sin(first[2] - axis))) / 2
            other = (
                np.abs(np.cos(second[:, 2] - axis)) + np.abs(np.sin(second[:, 2] - axis))
            ) / 2
            best = np.maximum(best, reach - own - other)
    return best


@dataclass(frozen=True)
class Pool:
    """Poses spread over an owner's survivors for support searches: for every live row,
    every residual's vertices, centroid and two interior points, at the row's two ends and
    middle. Thin residuals, where a square rests on a wall at its own turn, are covered
    as well as wide ones, which sampling by area would miss."""

    poses: Floats
    rows: NDArray[np.intp]
    polygons: NDArray[np.intp]


def make_pool(owner: Owner, rng: np.random.Generator) -> Pool:
    poses: list[tuple[float, float, float]] = []
    rows: list[int] = []
    polygons: list[int] = []
    for index, row in enumerate(owner.live_rows()):
        lo, hi = theta_of(row.t_lo), theta_of(row.t_hi)
        for number, polygon in enumerate(row.residuals):
            points = [(float(x), float(y)) for x, y in polygon]
            points.append((float(polygon[:, 0].mean()), float(polygon[:, 1].mean())))
            points += [_point_in(polygon, rng) for _ in range(2)]
            for x, y in points:
                for theta in (lo, (lo + hi) / 2, hi):
                    poses.append((x, y, theta))
                    rows.append(index)
                    polygons.append(number)
    return Pool(np.array(poses), np.array(rows), np.array(polygons))


def best_support(
    pose: Floats,
    partner: Owner,
    pool: Pool,
    rng: np.random.Generator,
    *,
    refine: int,
    candidates: int = 4,
) -> float:
    """The largest gap a partner's surviving pose leaves a pose, as far as found: the best
    of the pool, then, if every pool pose overlaps, a local search from the best few that
    never leaves the partner's survivors (each move is a convex combination with a point of
    the same residual and a turn within the same row). A lower estimate of the largest gap."""
    gaps = pair_gaps(pose, pool.poses)
    best = float(gaps.max())
    if best >= 0.0 or not refine:
        return best
    live = partner.live_rows()
    for start in np.argsort(gaps)[-candidates:]:
        row = live[int(pool.rows[start])]
        polygon = row.residuals[int(pool.polygons[start])]
        lo, hi = theta_of(row.t_lo), theta_of(row.t_hi)
        current, value = pool.poses[start].copy(), float(gaps[start])
        for step in range(refine):
            shrink = 1.0 - step / refine
            weight = 0.3 * shrink
            trial = current.copy()
            trial[:2] = (1.0 - weight) * current[:2] + weight * np.array(
                _point_in(polygon, rng)
            )
            trial[2] = min(hi, max(lo, current[2] + rng.normal(0.0, 0.3 * (hi - lo) * shrink)))
            gap = float(pair_gaps(pose, trial[None, :])[0])
            if gap > value:
                current, value = trial, gap
        best = max(best, value)
        if best >= 0.0:
            break
    return best


def pairwise_support(
    geometry: selector.Geometry,
    survivors: Survivors,
    *,
    samples: int,
    seed: int,
    refine: int = 200,
) -> dict[str, Any]:
    """For each owner, the share of its sampled surviving poses that every interacting
    partner supports, and for each partner how far the poses it does not support are from
    support.

    A pose is supported by a partner when some surviving pose of the partner leaves it a gap
    of at least zero (`best_support`, from the partner's `Pool`). A supported pose cannot
    be removed by any sound cut that reasons from one partner at a time against that
    partner's survivors, however fine its rows or exact its core: such a cut must hold at
    every pose the partner keeps, and one of them is clear. The kernel's owned-hull and
    collision cuts are of that kind. A pose that no partner pose clears, by a margin `m`,
    could be removed by an exact one-partner cut, and the kernel's losses (core, wall, the
    owned hull's common point) are what keep it. Partner poses are searched, not
    enumerated, so the supported share is a lower bound and each margin an upper bound on
    the true one."""
    rng = np.random.default_rng(seed)
    owners = survivors.owners
    pools = [make_pool(owner, rng) for owner in owners]
    record: dict[str, Any] = {
        "samples": samples,
        "partner_pool": {
            owner.name: len(pool.poses) for owner, pool in zip(owners, pools, strict=True)
        },
        "refine": refine,
        "owners": {},
    }
    for index, owner in enumerate(owners):
        margins: dict[str, list[float]] = {}
        cuts: list[float] = []
        for _ in range(samples):
            pose = np.array(sample_pose_of(owner, rng))
            cut = 0.0
            for other_index, other in enumerate(owners):
                if other_index == index or not geometry.interact[owner.cell, other.cell]:
                    continue
                gap = best_support(pose, other, pools[other_index], rng, refine=refine)
                if gap < 0.0:
                    margins.setdefault(other.name, []).append(-gap)
                    cut = max(cut, -gap)
            cuts.append(cut)
        unsupported = sorted(cut for cut in cuts if cut > 0.0)
        record["owners"][owner.name] = {
            "supported_share": 1.0 - len(unsupported) / samples,
            # Per unsupported pose, its largest margin over the partners: the loss a
            # one-partner cut may have and still remove it. The least of them is the
            # loss that would remove every sampled pose.
            "cut_margin": (
                {
                    "least": unsupported[0],
                    "tenth_percentile": float(np.quantile(unsupported, 0.1)),
                    "median": float(np.median(unsupported)),
                }
                if unsupported
                else None
            ),
            "unsupported_by": {
                name: {
                    "poses": len(values),
                    "median_margin": float(np.median(values)),
                    "largest_margin": float(np.max(values)),
                }
                for name, values in sorted(margins.items(), key=lambda item: -len(item[1]))
            },
        }
    return record


# ---------------------------------------------------------------------------
# Profiles: the best violation with one owner pinned
# ---------------------------------------------------------------------------


def pinned_descent(
    problem: selector.Problem, start: Floats, pins: dict[int, float], *, polish: bool
) -> Floats:
    """One L-BFGS-B descent of the selector's penalty with some coordinates held fixed.

    `pins` maps a coordinate of the descent vector (`x` rows first, then `y`, then the
    angles) to its value; the rest descend as in `Problem.descend`."""
    z = problem.pack(start)
    bounds: list[tuple[float | None, float | None]] = [(None, None)] * len(z)
    for index, value in pins.items():
        z[index] = value
        bounds[index] = (value, value)
    options: dict[str, Any] = (
        {"maxiter": 3000, "ftol": 1e-24, "gtol": 1e-18, "maxcor": 30}
        if polish
        else {"maxiter": 600, "ftol": 1e-15, "gtol": 1e-12, "maxcor": 20}
    )
    result = minimize(
        problem.objective, z, jac=True, method="L-BFGS-B", bounds=bounds, options=options
    )
    return problem.pose(np.asarray(result.x, dtype=np.float64))


def angle_profile(
    geometry: selector.Geometry,
    survivors: Survivors,
    owner: int,
    degrees: list[float],
    *,
    best_pose: Floats,
    starts: int,
    seed: int,
) -> list[dict[str, Any]]:
    """For each angle, the least violation found with the owner (its row in the mask) held
    at that angle: the best pose so far with the angle replaced, then survivor samples."""
    cells = survivors.mask
    problem = selector.Problem(geometry, cells, fast=True)
    rng = np.random.default_rng(seed)
    index = 2 * problem.k + owner
    profile: list[dict[str, Any]] = []
    with selector.single_thread_blas():
        for degree in degrees:
            angle = math.radians(degree)
            best: tuple[float, Floats] | None = None
            for attempt in range(starts):
                start = best_pose.copy() if attempt == 0 else sample_pose(survivors, rng)
                start[owner, 2] = angle
                pose = pinned_descent(problem, start, {index: angle}, polish=False)
                value = problem.violation(pose)
                if best is None or value < best[0]:
                    best = (value, pose)
            assert best is not None
            polished = pinned_descent(problem, best[1], {index: angle}, polish=True)
            value = min(best[0], problem.violation(polished))
            profile.append(
                {
                    "degrees": degree,
                    "violation": value,
                    "in_survivors": survivors.owners[owner].holds(
                        (float(polished[owner, 0]), float(polished[owner, 1]), angle)
                    ),
                }
            )
    return profile


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def placement_record(
    geometry: selector.Geometry, cells: tuple[int, ...], pose: Floats, design: str
) -> dict[str, Any]:
    """A placed pose rounded to rationals and checked exactly; the record a receipt keeps."""
    rows = rational_pose(pose)
    names = [geometry.names[cell] for cell in cells]
    return {
        "schema": PLACEMENT_SCHEMA,
        "design": design,
        "cap": str(cover.U),
        "squares": [
            {"cell": name, "x": str(x), "y": str(y), "t": str(t)}
            for name, (x, y, t) in zip(names, rows, strict=True)
        ],
        "exact": exact_check(names, rows, design),
    }


def read_placement(
    record: dict[str, Any],
) -> tuple[list[str], list[tuple[Fraction, Fraction, Fraction]]]:
    names = [square["cell"] for square in record["squares"]]
    rows = [
        (Fraction(square["x"]), Fraction(square["y"]), Fraction(square["t"]))
        for square in record["squares"]
    ]
    return names, rows


def diagnose(
    node_file: Path,
    *,
    design: str = selector.DEFAULT_DESIGN,
    seed: int = 1,
    starts: int = 200,
    warm: int = 64,
    budget: selector.Budget | None = None,
    profile_degrees: list[float] | None = None,
    profile_starts: int = 6,
    side_steps: int = 12,
) -> dict[str, Any]:
    """Survivors, the survivor-seeded searches, the largest side and the angle profiles of
    the owners that kept every row; with an exact check of any placement found."""
    clock = time.perf_counter()
    geometry = selector.cover_geometry(design)
    survivors = read_survivors(node_file, geometry.names)
    cells = survivors.mask
    record: dict[str, Any] = {
        "schema": SCHEMA,
        "status": STATUS,
        "design": design,
        "cells": [geometry.names[cell] for cell in cells],
        "mask": list(cells),
        "survivors": summarise(survivors),
    }
    spread = multistart(geometry, survivors, starts=starts, seed=seed)
    record["multistart"] = spread
    found = selector_search(
        geometry, survivors, warm_count=warm, seed=seed, budget=budget or selector.Budget()
    )
    record["selector_search"] = found
    best = min(
        (np.array(spread["best_pose"]), np.array(found["best_pose"])),
        key=selector.Problem(geometry, cells).violation,
    )
    if spread["placed"] or found["placed"]:
        record["placement"] = placement_record(geometry, cells, best, design)
    record["largest_side"] = largest_side(
        geometry, cells, best, survivors=survivors, seed=seed, steps=side_steps
    )
    stuck = [
        index
        for index, owner in enumerate(survivors.owners)
        if len(owner.live_rows()) == len(owner.rows)
    ]
    degrees = (
        profile_degrees if profile_degrees is not None else [0.0, 15.0, 30.0, 45.0, 60.0, 75.0]
    )
    record["angle_profiles"] = {
        survivors.owners[index].name: angle_profile(
            geometry,
            survivors,
            index,
            degrees,
            best_pose=best,
            starts=profile_starts,
            seed=seed,
        )
        for index in stuck
    }
    record["provenance"] = PROVENANCE
    record["seconds"] = round(time.perf_counter() - clock, 1)
    return record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    domains = commands.add_parser("domains", help="summarise a saved node's survivors")
    domains.add_argument("node", type=Path, help="a saved node-<sha256>.json.gz")
    domains.add_argument("--design", default=selector.DEFAULT_DESIGN)
    domains.add_argument("--output", type=Path)
    place = commands.add_parser("place", help="the survivor-seeded searches and profiles")
    place.add_argument("node", type=Path, help="a saved node-<sha256>.json.gz")
    place.add_argument("--design", default=selector.DEFAULT_DESIGN)
    place.add_argument("--seed", type=int, default=1)
    place.add_argument("--starts", type=int, default=200)
    place.add_argument("--warm", type=int, default=64)
    place.add_argument("--deep-starts", type=int, default=selector.Budget().deep_starts)
    place.add_argument("--deep-hops", type=int, default=selector.Budget().deep_hops)
    place.add_argument("--profile-starts", type=int, default=6)
    place.add_argument("--side-steps", type=int, default=12)
    place.add_argument("--output", type=Path)
    support = commands.add_parser(
        "support", help="the share of each owner's survivors every partner supports"
    )
    support.add_argument("node", type=Path, help="a saved node-<sha256>.json.gz")
    support.add_argument("--design", default=selector.DEFAULT_DESIGN)
    support.add_argument("--seed", type=int, default=1)
    support.add_argument("--samples", type=int, default=400)
    support.add_argument("--refine", type=int, default=200)
    support.add_argument("--output", type=Path)
    check = commands.add_parser("check", help="re-check a recorded placement exactly")
    check.add_argument("receipt", type=Path)
    margins = commands.add_parser(
        "margins", help="the largest side without each cell, from a `place` receipt's best pose"
    )
    margins.add_argument("receipt", type=Path)
    margins.add_argument("--seed", type=int, default=1)
    margins.add_argument("--starts", type=int, default=12)
    margins.add_argument("--steps", type=int, default=8)
    margins.add_argument("--output", type=Path)
    arguments = parser.parse_args(argv)
    if arguments.command == "check":
        document = json.loads(arguments.receipt.read_text(encoding="utf-8"))
        placement = document.get("placement", document)
        names, rows = read_placement(placement)
        result = exact_check(names, rows, placement["design"])
        print(json.dumps(result, indent=1, sort_keys=True))
        return 0 if result["valid"] else 2
    if arguments.command == "domains":
        geometry = selector.cover_geometry(arguments.design)
        record = summarise(read_survivors(arguments.node, geometry.names))
    elif arguments.command == "support":
        geometry = selector.cover_geometry(arguments.design)
        survivors = read_survivors(arguments.node, geometry.names)
        clock = time.perf_counter()
        record = {
            "schema": SCHEMA,
            "status": STATUS,
            "node_file": survivors.node_file,
            "support": pairwise_support(
                geometry,
                survivors,
                samples=arguments.samples,
                refine=arguments.refine,
                seed=arguments.seed,
            ),
            "provenance": PROVENANCE,
            "seconds": round(time.perf_counter() - clock, 1),
        }
    elif arguments.command == "margins":
        document = json.loads(arguments.receipt.read_text(encoding="utf-8"))
        geometry = selector.cover_geometry(document["design"])
        cells = tuple(document["mask"])
        problem = selector.Problem(geometry, cells)
        best = min(
            (np.array(document[key]["best_pose"]) for key in ("multistart", "selector_search")),
            key=problem.violation,
        )
        clock = time.perf_counter()
        with selector.single_thread_blas():
            found = minus_one_margins(
                geometry,
                cells,
                best,
                seed=arguments.seed,
                starts=arguments.starts,
                steps=arguments.steps,
            )
        record = {
            "schema": SCHEMA,
            "status": STATUS,
            "source": recorded_path(arguments.receipt),
            "cells": [geometry.names[cell] for cell in cells],
            "best_violation": problem.violation(best),
            "without": found,
            "provenance": PROVENANCE,
            "seconds": round(time.perf_counter() - clock, 1),
        }
    else:
        record = diagnose(
            arguments.node,
            design=arguments.design,
            seed=arguments.seed,
            starts=arguments.starts,
            warm=arguments.warm,
            budget=selector.Budget(
                deep_starts=arguments.deep_starts, deep_hops=arguments.deep_hops
            ),
            profile_starts=arguments.profile_starts,
            side_steps=arguments.side_steps,
        )
    encoded = json.dumps(record, indent=1, sort_keys=True) + "\n"
    if arguments.output is not None:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
