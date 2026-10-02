"""H-268: square 6 in its H-266 cover cell keeps the n17 slides inside the box B_W.

Claim. Take any packing of 17 unit squares in the endpoint's container whose 45
non-slider coordinates lie within `r = 1/5000` of the endpoint family (exp-244's
neighbourhood) and whose square 6 has its centre in the closed cover cell `side-S2`
of `check_n17_capacity_one_cover`, at any orientation. Then the slides satisfy
`a <= A`, `z >= Z` and `b <= B` for the thresholds passed (default the box `B_W` of
`check_n17_local_minimum.DECLARED_BOX`: `A = 1/4`, `Z = -1/8`, `B = 1/12`).

Everything is in the cover frame (the endpoint embedded concentrically), with every
endpoint quantity an exact interval over the exp-238 root box (`cover.endpoint`).

Inner rectangles. A unit square whose centre is displaced by `|delta| <= r sqrt 2`
and turned by `|omega| <= r` from its nominal pose contains the nominal square shrunk
to half-side `H = 1/2 - 2r`: a point with nominal frame coordinates bounded by `H`
has, in the moved frame, a coordinate at most `H (1 + r) + r sqrt 2
= 1/2 - r (3/2 - sqrt 2) - 2 r^2 < 1/2`. A slider moving over an interval (`a` for
square 5 along `-e_x`, `b` for 11 along `-v`, `z` for 13 along `+v`) gives the
intersection of these shrunk squares over the interval, a rectangle shorter along the
slide by the interval's width. Each such set is replaced by a rectangle with rational
centre and rational unit axes (`t` rounded to `2^-32`), shrunk by `2^-28` more, and its
containment in the exact set is checked vertex by vertex in interval arithmetic over the
root box. If two of these inner rectangles overlap (strict separating-axis test on
exact rationals), the two real squares overlap; if one leaves the outer container
bound, its square leaves the container.

Square 6. It is a full unit square at an unknown turn `phi`, which by the square's
symmetry ranges over `[0, pi/2]`, parametrised by `tau = tan(phi/2)` in `[0, 1]` so
that `cos phi` and `sin phi` are exact monotone rationals on every `tau` interval
(rounded outward to `2^-40`). A box of `(tau, x6, y6)` inside the cell is closed when,
for every point of it, square 6 overlaps one inner rectangle (all four separating
axes overlap strictly, with interval bounds) or leaves the container.

Slide domain. Each slider's physical range comes from its centre lying at least `1/2`
from every wall. The `(a, z)` domain is split adaptively: a part inside the target is
accepted, and every other part must be closed by a pair overlap among squares 5, 13 and
the non-slider squares, by the container, or by a branch and bound over square 6.
Because the intersection rectangle of square 5 over `[a1, a2]` keeps its left face at
`a1`, and that of square 13 over `[z1, z2]` keeps its lower-right face at `z2`, a wide
slide interval loses nothing on the face that squeezes square 6. The `(b, z)` domain,
with `z` above the certified `Z`, is closed the same way by squares 11 and 13 without
square 6.

Controls. Replacing the cell by every centre the container allows, or deleting square
13, must leave an open box for the `a` bound.

Not covered. The exp-238 root box is used; the exp-237 midpoint the local theorem uses
lies inside it. Squares 5, 11 and 13 turn by at most `r`, as in exp-244.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from devtools import check_n17_capacity_one_cover as cover
from devtools.check_n17_endpoint_feasibility import THETA_LABELS, Box
from devtools.check_n17_local_minimum import DECLARED_BOX, DECLARED_RADIUS

SCHEMA = "n17-slider-coverage/v1"
SIX_CELL = "side-S2"
SLIDERS = frozenset((5, 6, 11, 13))
GRID = 2**40
ANGLE_GRID = 2**32
KAPPA = Q(1, 2**28)
MAX_SLIDE_WIDTH = Q(7, 8)
SLIDE_STEP = Q(1, 2**12)
SIX_STEP = Q(1, 2**11)
SIX_NODE_LIMIT = 200_000
CONTROL_NODE_LIMIT = 20_000
NEAR = Q(3, 2)

Interval = tuple[Q, Q]


def _down(value: Q, grid: int = GRID) -> Q:
    return Q(math.floor(value * grid), grid)


def _up(value: Q, grid: int = GRID) -> Q:
    return Q(math.ceil(value * grid), grid)


def _mul(a: Interval, b: Interval) -> Interval:
    values = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    return min(values), max(values)


def _scale(k: Q, a: Interval) -> Interval:
    return (k * a[0], k * a[1]) if k >= 0 else (k * a[1], k * a[0])


def _add(a: Interval, b: Interval) -> Interval:
    return a[0] + b[0], a[1] + b[1]


def _abs_lo(a: Interval) -> Q:
    return Q(0) if a[0] <= 0 <= a[1] else min(abs(a[0]), abs(a[1]))


def _abs_hi(a: Interval) -> Q:
    return max(abs(a[0]), abs(a[1]))


@dataclass(frozen=True)
class Rect:
    """A rectangle: centre, unit axis `u` (with `v = (-u_y, u_x)`), half-extents."""

    cx: Q
    cy: Q
    ux: Q
    uy: Q
    p: Q
    q: Q

    def support(self, nx: Q, ny: Q) -> Q:
        return self.p * abs(nx * self.ux + ny * self.uy) + self.q * abs(
            -nx * self.uy + ny * self.ux
        )

    def vertices(self) -> tuple[tuple[Q, Q], ...]:
        vx, vy = -self.uy, self.ux
        return tuple(
            (
                self.cx + i * self.p * self.ux + j * self.q * vx,
                self.cy + i * self.p * self.uy + j * self.q * vy,
            )
            for i in (1, -1)
            for j in (1, -1)
        )

    def record(self) -> dict[str, str]:
        return {
            "centre": f"{float(self.cx):.9f},{float(self.cy):.9f}",
            "half": f"{float(self.p):.9f},{float(self.q):.9f}",
        }


def rects_overlap(first: Rect, second: Rect) -> bool:
    """Strict interior overlap of two rectangles, by all four separating axes."""
    dx, dy = second.cx - first.cx, second.cy - first.cy
    for nx, ny in (
        (first.ux, first.uy),
        (-first.uy, first.ux),
        (second.ux, second.uy),
        (-second.uy, second.ux),
    ):
        if abs(nx * dx + ny * dy) >= first.support(nx, ny) + second.support(nx, ny):
            return False
    return True


def leaves(rect: Rect, outer: Interval) -> bool:
    """Some vertex strictly outside the outer container bound."""
    lo, hi = outer
    return any(not (lo <= x <= hi and lo <= y <= hi) for x, y in rect.vertices())


@dataclass(frozen=True)
class Pose:
    """A square's exact nominal pose: centre and `u` axis as root-box intervals."""

    cx: Box
    cy: Box
    ux: Box
    uy: Box
    approx: tuple[Q, Q]


def _mid(box: Box) -> Q:
    return Q(round((box.lo + box.hi) / 2 * GRID), GRID)


def inner_rect(pose: Pose, offset: tuple[Box, Box], half_u: Q, half_v: Q) -> Rect | None:
    """A rational rectangle inside the pose's shrunk square moved by `offset`, checked."""
    if half_u <= KAPPA or half_v <= KAPPA:
        return None
    cx, cy = pose.cx + offset[0], pose.cy + offset[1]
    rect = Rect(_mid(cx), _mid(cy), *pose.approx, half_u - KAPPA, half_v - KAPPA)
    for x, y in rect.vertices():
        ex, ey = Box.point(x) - cx, Box.point(y) - cy
        along_u = (pose.ux * ex + pose.uy * ey).absolute().hi
        along_v = (pose.ux * ey - pose.uy * ex).absolute().hi
        if along_u > half_u or along_v > half_v:
            raise ValueError("inner rectangle is not inside the exact shrunk square")
    return rect


@dataclass(frozen=True)
class Scene:
    poses: dict[int, Pose]
    v: tuple[Box, Box]
    outer: Interval
    half: Q
    radius: Q
    cell: tuple[Q, Q, Q, Q]
    fixed: dict[int, Rect]
    provenance: dict[str, Any]


def _cell_box(name: str) -> tuple[Q, Q, Q, Q]:
    design = cover.DESIGNS["ring-3-voronoi-8-tabbed"]
    for cell in cover.build_cover(design):
        if cell.name == name:
            xs = [x for x, _ in cell.vertices]
            ys = [y for _, y in cell.vertices]
            if len(cell.vertices) != 4 or len(set(xs)) != 2 or len(set(ys)) != 2:
                raise ValueError("square 6's cell must be an axis-parallel rectangle")
            return min(xs), max(xs), min(ys), max(ys)
    raise ValueError(f"no cell {name}")


def build_scene(radius: Q = DECLARED_RADIUS, cell: tuple[Q, Q, Q, Q] | None = None) -> Scene:
    t_box, b_box, provenance = cover.load_root_box(cover.CERTIFICATE)
    point = cover.endpoint(t_box, b_box)
    aux = point.aux
    t_q = Q(round(t_box.lo * ANGLE_GRID), ANGLE_GRID)
    b_q = Q(round(b_box.lo * ANGLE_GRID), ANGLE_GRID)
    theta = ((1 - t_q * t_q) / (1 + t_q * t_q), 2 * t_q / (1 + t_q * t_q))
    beta = ((1 - b_q * b_q) / (1 + b_q * b_q), -2 * b_q / (1 + b_q * b_q))
    one, zero = Box.point(Q(1)), Box.point(Q(0))
    poses: dict[int, Pose] = {}
    for label, (cx, cy) in enumerate(point.centres, start=1):
        if label in THETA_LABELS:
            poses[label] = Pose(cx, cy, Box.cast(aux["c"]), Box.cast(aux["s"]), theta)
        elif label == 16:
            poses[label] = Pose(cx, cy, Box.cast(aux["d"]), -Box.cast(aux["e"]), beta)
        else:
            poses[label] = Pose(cx, cy, one, zero, (Q(1), Q(0)))
    shift = Box.cast(point.shift)
    outer = (shift.lo, cover.U - shift.lo)
    half = Q(1, 2) - 2 * radius
    six_cell = _cell_box(SIX_CELL) if cell is None else cell
    origin = (zero, zero)
    fixed = {
        label: rect
        for label, pose in poses.items()
        if label not in SLIDERS and (rect := inner_rect(pose, origin, half, half)) is not None
    }
    vx, vy = point.v
    return Scene(
        poses=poses,
        v=(Box.cast(vx), Box.cast(vy)),
        outer=outer,
        half=half,
        radius=radius,
        cell=six_cell,
        fixed=fixed,
        provenance=provenance,
    )


# ---------------------------------------------------------------------------
# Slider rectangles
# ---------------------------------------------------------------------------


def five_rect(scene: Scene, a: Interval) -> Rect | None:
    mid, width = (a[0] + a[1]) / 2, a[1] - a[0]
    offset = (Box.point(-mid), Box.point(Q(0)))
    return inner_rect(scene.poses[5], offset, scene.half - width / 2, scene.half)


def along_v_rect(scene: Scene, label: int, w: Interval, sign: int) -> Rect | None:
    mid, width = (w[0] + w[1]) / 2, w[1] - w[0]
    offset = (scene.v[0] * (sign * mid), scene.v[1] * (sign * mid))
    return inner_rect(scene.poses[label], offset, scene.half, scene.half - width / 2)


def physical_range(scene: Scene, label: int, direction: tuple[Box, Box]) -> Interval:
    """Range of `w` with the centre `c + w d + eps u` (|eps| <= r) at least 1/2 from walls."""
    pose = scene.poses[label]
    lo, hi = scene.outer
    eps = Box(-scene.radius, scene.radius)
    lows: list[Q] = []
    highs: list[Q] = []
    for centre, step, wobble in (
        (pose.cx, direction[0], eps * pose.ux),
        (pose.cy, direction[1], eps * pose.uy),
    ):
        if step.lo <= 0 <= step.hi:
            if step.lo == step.hi:
                continue
            raise ValueError("slide direction component straddles zero")
        first = (Box.point(lo + Q(1, 2)) - centre - wobble) / step
        second = (Box.point(hi - Q(1, 2)) - centre - wobble) / step
        if step.lo > 0:
            lows.append(first.lo)
            highs.append(second.hi)
        else:
            lows.append(second.lo)
            highs.append(first.hi)
    return _down(max(lows), 2**10), _up(min(highs), 2**10)


# ---------------------------------------------------------------------------
# Square 6
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SixBox:
    t: Interval
    x: Interval
    y: Interval


def trig(t: Interval) -> tuple[Interval, Interval]:
    t1, t2 = t
    cos = (_down((1 - t2 * t2) / (1 + t2 * t2)), _up((1 - t1 * t1) / (1 + t1 * t1)))
    sin = (_down(2 * t1 / (1 + t1 * t1)), _up(2 * t2 / (1 + t2 * t2)))
    return cos, sin


def six_overlaps(rect: Rect, box: SixBox, cos: Interval, sin: Interval) -> bool:
    """Square 6 overlaps `rect` at every point of `box` (outward interval bounds)."""
    dx = (box.x[0] - rect.cx, box.x[1] - rect.cx)
    dy = (box.y[0] - rect.cy, box.y[1] - rect.cy)
    for nx, ny, extent in ((rect.ux, rect.uy, rect.p), (-rect.uy, rect.ux, rect.q)):
        reach = _abs_hi(_add(_scale(nx, dx), _scale(ny, dy)))
        along = _add(_scale(nx, cos), _scale(ny, sin))
        across = _add(_scale(-nx, sin), _scale(ny, cos))
        if reach >= extent + (_abs_lo(along) + _abs_lo(across)) / 2:
            return False
    neg_sin = (-sin[1], -sin[0])
    for ax, ay in ((cos, sin), (neg_sin, cos)):
        reach = _abs_hi(_add(_mul(ax, dx), _mul(ay, dy)))
        on_u = _add(_scale(rect.ux, ax), _scale(rect.uy, ay))
        on_v = _add(_scale(-rect.uy, ax), _scale(rect.ux, ay))
        if reach >= Q(1, 2) + rect.p * _abs_lo(on_u) + rect.q * _abs_lo(on_v):
            return False
    return True


def six_leaves(box: SixBox, cos: Interval, sin: Interval, outer: Interval) -> bool:
    lo, hi = outer
    reach = (_abs_lo(cos) + _abs_lo(sin)) / 2
    return (
        box.x[1] - reach < lo
        or box.x[0] + reach > hi
        or box.y[1] - reach < lo
        or box.y[0] + reach > hi
    )


def _split(box: SixBox) -> tuple[SixBox, SixBox]:
    widths = (2 * (box.t[1] - box.t[0]), box.x[1] - box.x[0], box.y[1] - box.y[0])
    axis = widths.index(max(widths))
    lo, hi = (box.t, box.x, box.y)[axis]
    mid = (lo + hi) / 2
    parts = [(box.t, box.x, box.y), (box.t, box.x, box.y)]
    left, right = list(parts[0]), list(parts[1])
    left[axis], right[axis] = (lo, mid), (mid, hi)
    return SixBox(*left), SixBox(*right)


@dataclass
class SixResult:
    closed: bool
    nodes: int
    witness: SixBox | None
    exhausted: bool = False


def six_cover(
    obstacles: list[Rect],
    cell: tuple[Q, Q, Q, Q],
    outer: Interval,
    *,
    node_limit: int = SIX_NODE_LIMIT,
) -> SixResult:
    """Branch and bound: every turn and every centre of square 6 in the cell is blocked."""
    x0, x1, y0, y1 = cell
    near = [
        rect
        for rect in obstacles
        if max(rect.cx - x1, x0 - rect.cx, 0) ** 2 + max(rect.cy - y1, y0 - rect.cy, 0) ** 2
        < (NEAR + max(rect.p, rect.q)) ** 2
    ]
    stack = [SixBox((Q(i, 8), Q(i + 1, 8)), (x0, x1), (y0, y1)) for i in range(8)]
    nodes = 0
    while stack:
        box = stack.pop()
        nodes += 1
        if nodes > node_limit:
            return SixResult(closed=False, nodes=nodes, witness=box, exhausted=True)
        cos, sin = trig(box.t)
        if six_leaves(box, cos, sin, outer) or any(
            six_overlaps(rect, box, cos, sin) for rect in near
        ):
            continue
        if max(box.t[1] - box.t[0], box.x[1] - box.x[0], box.y[1] - box.y[0]) <= SIX_STEP:
            return SixResult(closed=False, nodes=nodes, witness=box)
        stack.extend(_split(box))
    return SixResult(closed=True, nodes=nodes, witness=None)


# ---------------------------------------------------------------------------
# The slide domains
# ---------------------------------------------------------------------------


@dataclass
class Outcome:
    passed: bool
    leaves: dict[str, int]
    six_nodes: int
    failure: dict[str, Any] | None


def _pair_reason(rects: dict[str, Rect], fixed: dict[int, Rect], outer: Interval) -> str | None:
    for name, rect in rects.items():
        if leaves(rect, outer):
            return f"{name}-container"
        for label, other in fixed.items():
            if rects_overlap(rect, other):
                return f"{name}-{label}"
    names = sorted(rects)
    for i, first in enumerate(names):
        for second in names[i + 1 :]:
            if rects_overlap(rects[first], rects[second]):
                return f"{first}-{second}"
    return None


def slide_cover(
    scene: Scene,
    a_max: Q,
    z_min: Q,
    *,
    without: frozenset[int] = frozenset(),
    node_limit: int = SIX_NODE_LIMIT,
) -> Outcome:
    """Every `(a, z)` outside `a <= a_max, z >= z_min` is infeasible."""
    a_range = physical_range(scene, 5, (Box.point(Q(-1)), Box.point(Q(0))))
    z_range = physical_range(scene, 13, scene.v)
    fixed = {label: rect for label, rect in scene.fixed.items() if label not in without}
    stack: list[tuple[Interval, Interval]] = [(a_range, z_range)]
    counts: dict[str, int] = {}
    six_nodes = 0
    while stack:
        a, z = stack.pop()
        if a[1] <= a_max and z[0] >= z_min:
            counts["target"] = counts.get("target", 0) + 1
            continue
        if a[0] < a_max < a[1]:
            stack += [((a[0], a_max), z), ((a_max, a[1]), z)]
            continue
        if z[0] < z_min < z[1]:
            stack += [(a, (z[0], z_min)), (a, (z_min, z[1]))]
            continue
        wide_a, wide_z = a[1] - a[0], z[1] - z[0]
        if max(wide_a, wide_z) > MAX_SLIDE_WIDTH:
            stack += _halve(a, z)
            continue
        rects: dict[str, Rect] = {}
        five = five_rect(scene, a)
        if five is not None:
            rects["5"] = five
        if 13 not in without:
            thirteen = along_v_rect(scene, 13, z, 1)
            if thirteen is not None:
                rects["13"] = thirteen
        reason = _pair_reason(rects, fixed, scene.outer)
        if reason is None:
            result = six_cover(
                [*fixed.values(), *rects.values()],
                scene.cell,
                scene.outer,
                node_limit=node_limit,
            )
            six_nodes += result.nodes
            if result.closed:
                reason = "six"
            elif result.exhausted or max(wide_a, wide_z) <= SLIDE_STEP:
                witness = result.witness
                return Outcome(
                    passed=False,
                    leaves=counts,
                    six_nodes=six_nodes,
                    failure={
                        "node_limit_reached": result.exhausted,
                        "a": [str(a[0]), str(a[1])],
                        "z": [str(z[0]), str(z[1])],
                        "six_box": None
                        if witness is None
                        else {
                            "tau": [float(v) for v in witness.t],
                            "x": [float(v) for v in witness.x],
                            "y": [float(v) for v in witness.y],
                        },
                    },
                )
        if reason is None:
            stack += _halve(a, z)
            continue
        key = "six" if reason == "six" else "pair"
        counts[key] = counts.get(key, 0) + 1
    return Outcome(passed=True, leaves=counts, six_nodes=six_nodes, failure=None)


def _halve(a: Interval, z: Interval) -> list[tuple[Interval, Interval]]:
    if a[1] - a[0] >= z[1] - z[0]:
        mid = (a[0] + a[1]) / 2
        return [((a[0], mid), z), ((mid, a[1]), z)]
    mid = (z[0] + z[1]) / 2
    return [(a, (z[0], mid)), (a, (mid, z[1]))]


def b_cover(scene: Scene, b_max: Q, z_min: Q) -> Outcome:
    """Every `(b, z)` with `z >= z_min` and `b > b_max` is infeasible (squares 11, 13)."""
    minus_v = (-scene.v[0], -scene.v[1])
    b_range = physical_range(scene, 11, minus_v)
    z_range = physical_range(scene, 13, scene.v)
    stack: list[tuple[Interval, Interval]] = [
        ((max(b_range[0], b_max), b_range[1]), (z_min, z_range[1]))
    ]
    counts: dict[str, int] = {}
    while stack:
        b, z = stack.pop()
        if b[1] <= b[0]:
            continue
        wide = max(b[1] - b[0], z[1] - z[0])
        if wide <= MAX_SLIDE_WIDTH:
            candidates = (
                ("11", along_v_rect(scene, 11, b, -1)),
                ("13", along_v_rect(scene, 13, z, 1)),
            )
            rects = {name: rect for name, rect in candidates if rect is not None}
            reason = _pair_reason(rects, scene.fixed, scene.outer)
            if reason is not None:
                counts["pair"] = counts.get("pair", 0) + 1
                continue
            if wide <= SLIDE_STEP:
                return Outcome(
                    passed=False,
                    leaves=counts,
                    six_nodes=0,
                    failure={"b": [str(b[0]), str(b[1])], "z": [str(z[0]), str(z[1])]},
                )
        if b[1] - b[0] >= z[1] - z[0]:
            mid = (b[0] + b[1]) / 2
            stack += [((b[0], mid), z), ((mid, b[1]), z)]
        else:
            mid = (z[0] + z[1]) / 2
            stack += [(b, (z[0], mid)), (b, (mid, z[1]))]
    return Outcome(passed=True, leaves=counts, six_nodes=0, failure=None)


# ---------------------------------------------------------------------------
# Receipt
# ---------------------------------------------------------------------------


def _outcome_record(outcome: Outcome) -> dict[str, Any]:
    return {
        "passed": outcome.passed,
        "leaves": outcome.leaves,
        "six_nodes": outcome.six_nodes,
        "failure": outcome.failure,
    }


def run(
    a_max: Q,
    z_min: Q,
    b_max: Q,
    *,
    tight: tuple[Q, Q] | None = None,
    controls: bool = True,
) -> dict[str, Any]:
    started = time.monotonic()
    scene = build_scene()
    timings: dict[str, float] = {}
    stage = time.monotonic()
    claim = slide_cover(scene, a_max, z_min)
    timings["a_z"] = time.monotonic() - stage
    z_for_b = z_min
    tight_record: dict[str, Any] | None = None
    if tight is not None:
        stage = time.monotonic()
        tight_outcome = slide_cover(scene, *tight)
        timings["tight"] = time.monotonic() - stage
        tight_record = {
            "a_max": str(tight[0]),
            "z_min": str(tight[1]),
            "margins": {
                "a": str(DECLARED_BOX[0][1] - tight[0]),
                "z": str(tight[1] - DECLARED_BOX[2][0]),
            },
            **_outcome_record(tight_outcome),
        }
        if tight_outcome.passed:
            z_for_b = max(z_min, tight[1])
    stage = time.monotonic()
    b_outcome = b_cover(scene, b_max, z_for_b)
    timings["b"] = time.monotonic() - stage
    control_records: dict[str, Any] = {}
    if controls:
        stage = time.monotonic()
        lo, hi = scene.outer
        whole = (lo + Q(1, 2), hi - Q(1, 2), lo + Q(1, 2), hi - Q(1, 2))
        whole_scene = build_scene(cell=whole)
        refused_whole = slide_cover(whole_scene, a_max, z_min, node_limit=CONTROL_NODE_LIMIT)
        refused_13 = slide_cover(scene, a_max, z_min, without=frozenset({13}))
        control_records = {
            "whole_box_cell_refused": not refused_whole.passed,
            "whole_box_cell": _outcome_record(refused_whole),
            "without_13_refused": not refused_13.passed,
            "without_13": _outcome_record(refused_13),
        }
        timings["controls"] = time.monotonic() - stage
    checks = {
        "a_z_bound": claim.passed,
        "b_bound": b_outcome.passed,
    }
    if controls:
        checks["controls_refused"] = bool(
            control_records["whole_box_cell_refused"] and control_records["without_13_refused"]
        )
    timings["total"] = time.monotonic() - started
    source = Path(__file__).read_bytes()
    return {
        "schema": SCHEMA,
        "scope": (
            "H-268 slide bounds from square 6's H-266 cell at any turn, the other "
            "non-slider coordinates within the radius; exact rationals, outward intervals"
        ),
        "module_sha256": hashlib.sha256(source).hexdigest(),
        "root": scene.provenance,
        "radius": str(scene.radius),
        "cell": {"name": SIX_CELL, "box": [str(v) for v in scene.cell]},
        "outer_container": [str(v) for v in scene.outer],
        "thresholds": {"a_max": str(a_max), "z_min": str(z_min), "b_max": str(b_max)},
        "margins": {
            "a": str(DECLARED_BOX[0][1] - a_max),
            "z": str(z_min - DECLARED_BOX[2][0]),
            "b": str(DECLARED_BOX[1][1] - b_max),
        },
        "a_z": _outcome_record(claim),
        "tight": tight_record,
        "b": {"z_min_used": str(z_for_b), **_outcome_record(b_outcome)},
        "controls": control_records,
        "checks": checks,
        "passed": all(checks.values()),
        "timing_seconds": {key: round(value, 3) for key, value in timings.items()},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or SCHEMA).splitlines()[0])
    parser.add_argument("--a-max", type=Q, default=DECLARED_BOX[0][1])
    parser.add_argument("--z-min", type=Q, default=DECLARED_BOX[2][0])
    parser.add_argument("--b-max", type=Q, default=DECLARED_BOX[1][1])
    parser.add_argument("--tight-a", type=Q, default=None)
    parser.add_argument("--tight-z", type=Q, default=None)
    parser.add_argument("--no-controls", action="store_true")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args(argv)
    tight = None
    if args.tight_a is not None or args.tight_z is not None:
        tight = (
            args.a_max if args.tight_a is None else args.tight_a,
            args.z_min if args.tight_z is None else args.tight_z,
        )
    try:
        receipt = run(
            args.a_max, args.z_min, args.b_max, tight=tight, controls=not args.no_controls
        )
    except (ValueError, OSError, KeyError) as error:
        print(json.dumps({"schema": SCHEMA, "passed": False, "error": str(error)}))
        return 2
    encoded = json.dumps(receipt, sort_keys=True, indent=1)
    if args.output is not None:
        args.output.write_text(encoded + "\n")
    summary = {key: receipt[key] for key in ("passed", "checks", "thresholds", "margins")}
    summary["timing_seconds"] = receipt["timing_seconds"]
    sys.stdout.write(json.dumps(summary, sort_keys=True) + "\n")
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
