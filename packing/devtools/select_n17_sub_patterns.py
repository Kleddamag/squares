"""Heuristic selector of forbidden n17 occupancy sub-patterns (H-267). Not a certificate.

What it selects. On a capacity-one cover of the n17 centre box (H-266), a sub-pattern is
a set `G` of `k` cells. It is *forbidden* when `k` unit squares, each with its centre in
its own closed cell of `G`, any orientations, all inside the cap container `[0, U]^2`,
cannot have pairwise disjoint interiors. Every state containing a forbidden pattern, in
any D4 image, is excluded. This module only *selects* candidates: it searches hard for a
feasible placement and flags a pattern when every attempt leaves a penetration above a
margin. A flag is a float heuristic. The prover (the n11 kernel adapted to n17) must
certify each flagged pattern before any exclusion counts, and the counts here are what
certification of all of them would give, not a result.

Patterns tested. A pattern is tested only when it is connected in the interaction graph,
whose edges join cells at distance below sqrt(2): two unit squares with centres at least
sqrt(2) apart lie in discs that meet in at most a point, so such a pair never collides,
and a disconnected pattern is feasible exactly when each component is. The reduction is
exact for the consumer, because a disconnected forbidden pattern contains a smaller
connected forbidden one. On the minimal cover it removes little (212 of 276 cell pairs
interact), so the budget knob is the window: with `--window W` a pattern is tested only
when the union of its cells fits in an axis-aligned `W x W` square of the centre box,
the local shape of n11's fields. The default is no window, which tests every connected
class. Classes are taken up to D4, bottom up by arity, and a pattern containing an
already flagged one is skipped, since the consumer needs only the minimal flagged set.

Search. Variables are the centres, the angles, and for each interacting pair a
separating line (normal angle and offset). The penalty sums squared hinge violations of
every square vertex against the container walls, every centre against its cell's
halfplanes, and every vertex against its side of each pair's line. It is C^1 and zero
exactly on feasible placements with a witnessing line per pair, touching included.
Each attempt is an L-BFGS-B descent; a promising attempt is polished. The verdict
measure is not the penalty but the true violation of the pose: the largest of every
pair's separating-axis penetration, every container excursion and every cell
excursion, in length units. Starts are, in order, the witnesses of the pattern's
`k - 1`-cell sub-patterns with one square added at random, uniform random poses, then
basin hops from the best pose found; a pattern still unplaced gets a deep stage of
redrawn witnesses, random poses and narrow and wide hops (`Budget`). A pattern is
flagged only if every attempt ends above the margin; the best violation found is
reported with it. The search must be strong, not only the margin careful: on the
bulk-exclusion lane's design (`ring-3-voronoi-8`) its sampling proxy flagged eleven
arity-five classes, and this search places every one, most in one to three attempts.

Determinism. Every pattern draws from its own generator, seeded by the run seed and the
pattern's cell mask, and uses only results of lower arities, so the receipt apart from
timings is the same for any worker count and scheduling.

Positive controls, checked first. The endpoint (H256 layout over the exp-238 root box,
embedded at the cap) is placed in its own state on the cover, and its violation at its
own pose is evaluated; every sub-pattern of that state, in every D4 image, is witnessed
feasible there and can never be flagged. The search itself runs blind to that pose, so
any endpoint sub-pattern it would have flagged is counted as a false flag, and the run
fails if there is one. Tight controls shrink the endpoint's cells to small boxes about
its centres, so the endpoint's touching contacts are close to the only placements, and
the search must still reach the margin. The margin is chosen so these pass with room.

Consumer. Every `17`-subset of the cells is a closed capacity-one assignment (the H260
convention of `check_n17_capacity_one_cover`). States containing a flagged pattern in
any D4 image are removed by direct bitmask enumeration, survivors are counted, and their
D4 orbits are counted twice, by Burnside's fixed counts and by distinct canonical forms.
A greedy order of the flagged classes, each taking the most surviving states left, is
the order in which certifying them pays most.
"""

from __future__ import annotations

import argparse
import contextlib
import ctypes
import functools
import hashlib
import itertools
import json
import math
import time
from collections.abc import Iterator
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import minimize

from devtools import check_n17_capacity_one_cover as cover
from devtools.check_n17_endpoint_feasibility import THETA_LABELS

SCHEMA = "n17-sub-pattern-selector/v1"
STATUS = (
    "heuristic selector, not a certificate: a flagged pattern is one the float search "
    "could not place; the prover must certify each flagged pattern before any exclusion "
    "counts"
)
DEFAULT_DESIGN = cover.UNIQUE_24.name
DESIGN_COMMIT = {cover.UNIQUE_24.name: "0dabde12"}
CAP = float(cover.U)
TARGET = cover.TARGET
MARGIN = 1e-6
POLISH_BELOW = 1e-4
INTERACTION = math.sqrt(2.0) + 1e-9
ENDPOINT_POSE_TOLERANCE = 1e-12
TIGHT_HALF_SIDE = 1e-3
CORNER_X = np.array([-0.5, 0.5, 0.5, -0.5])
CORNER_Y = np.array([-0.5, -0.5, 0.5, 0.5])

Floats = NDArray[np.float64]


# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Geometry:
    """Float cells, their halfplanes, a permutation group on them, and the cap."""

    cap: float
    names: tuple[str, ...]
    polygons: tuple[Floats, ...]
    halfplanes: tuple[Floats, ...]
    group: tuple[tuple[int, ...], ...]
    actions: tuple[str, ...]
    interact: NDArray[np.bool_]
    lower: Floats
    upper: Floats


def _ccw(polygon: Floats) -> Floats:
    x, y = polygon[:, 0], polygon[:, 1]
    area = float(np.dot(x, np.roll(y, -1)) - np.dot(np.roll(x, -1), y))
    return polygon if area > 0 else polygon[::-1].copy()


def _halfplanes(polygon: Floats) -> Floats:
    """Rows `(a, b, c)` with unit `(a, b)`: the closed cell is `a x + b y <= c`."""
    rows: list[list[float]] = []
    for index in range(len(polygon)):
        start, end = polygon[index], polygon[(index + 1) % len(polygon)]
        ex, ey = float(end[0] - start[0]), float(end[1] - start[1])
        length = math.hypot(ex, ey)
        a, b = ey / length, -ex / length
        rows.append([a, b, a * float(start[0]) + b * float(start[1])])
    return np.array(rows)


def _segment_distance(point: Floats, start: Floats, end: Floats) -> float:
    edge = end - start
    t = float(np.clip(np.dot(point - start, edge) / np.dot(edge, edge), 0.0, 1.0))
    return float(np.linalg.norm(point - start - t * edge))


def _cross(origin: Floats, a: Floats, b: Floats) -> float:
    return float(
        (a[0] - origin[0]) * (b[1] - origin[1]) - (a[1] - origin[1]) * (b[0] - origin[0])
    )


def _segments_cross(p: Floats, q: Floats, r: Floats, s: Floats) -> bool:
    """Proper crossing only; touching and collinear contact put a vertex in the other cell."""
    return (_cross(p, q, r) * _cross(p, q, s) < 0) and (_cross(r, s, p) * _cross(r, s, q) < 0)


def polygon_distance(first: Floats, second: Floats) -> float:
    """Distance between two convex polygons, zero when they meet."""
    for a, b in ((first, second), (second, first)):
        planes = _halfplanes(b)
        for x, y in a:
            if np.all(planes[:, 0] * x + planes[:, 1] * y <= planes[:, 2] + 1e-12):
                return 0.0
    edges_first = [(first[i], first[(i + 1) % len(first)]) for i in range(len(first))]
    edges_second = [(second[i], second[(i + 1) % len(second)]) for i in range(len(second))]
    for p, q in edges_first:
        for r, s in edges_second:
            if _segments_cross(p, q, r, s):
                return 0.0
    best = math.inf
    for a, b in ((first, second), (second, first)):
        for point in a:
            for index in range(len(b)):
                best = min(best, _segment_distance(point, b[index], b[(index + 1) % len(b)]))
    return best


def make_geometry(
    polygons: list[Floats],
    names: list[str],
    *,
    cap: float = CAP,
    group: list[tuple[int, ...]] | None = None,
    actions: list[str] | None = None,
) -> Geometry:
    polygons = [_ccw(np.asarray(polygon, dtype=np.float64)) for polygon in polygons]
    count = len(polygons)
    interact = np.zeros((count, count), dtype=np.bool_)
    for i, j in itertools.combinations(range(count), 2):
        near = polygon_distance(polygons[i], polygons[j]) < INTERACTION
        interact[i, j] = interact[j, i] = near
    identity = tuple(range(count))
    return Geometry(
        cap=cap,
        names=tuple(names),
        polygons=tuple(polygons),
        halfplanes=tuple(_halfplanes(polygon) for polygon in polygons),
        group=tuple(group) if group is not None else (identity,),
        actions=tuple(actions) if actions is not None else ("r0",),
        interact=interact,
        lower=np.array([polygon.min(axis=0) for polygon in polygons]),
        upper=np.array([polygon.max(axis=0) for polygon in polygons]),
    )


def cover_geometry(design_name: str = DEFAULT_DESIGN) -> Geometry:
    """The named H-266 cover as float cells with its D4 permutations."""
    cells = cover.build_cover(cover.DESIGNS[design_name])
    permutations = cover.d4_permutations(cells)
    if permutations is None:
        raise ValueError(f"design {design_name} is not D4-invariant")
    polygons = [np.array([[float(x), float(y)] for x, y in cell.vertices]) for cell in cells]
    return make_geometry(
        polygons,
        [cell.name for cell in cells],
        group=[tuple(permutations[action]) for action in cover.D4],
        actions=list(cover.D4),
    )


def mask_of(cells: tuple[int, ...] | list[int]) -> int:
    return sum(1 << cell for cell in cells)


def cells_of(mask: int) -> tuple[int, ...]:
    return tuple(index for index in range(mask.bit_length()) if mask >> index & 1)


def image_mask(mask: int, permutation: tuple[int, ...]) -> int:
    return sum(1 << permutation[cell] for cell in cells_of(mask))


def canonical(mask: int, group: tuple[tuple[int, ...], ...]) -> int:
    return min(image_mask(mask, permutation) for permutation in group)


def orbit(mask: int, group: tuple[tuple[int, ...], ...]) -> set[int]:
    return {image_mask(mask, permutation) for permutation in group}


def connected(geometry: Geometry, cells: tuple[int, ...]) -> bool:
    seen, stack = {cells[0]}, [cells[0]]
    while stack:
        current = stack.pop()
        for other in cells:
            if other not in seen and geometry.interact[current, other]:
                seen.add(other)
                stack.append(other)
    return len(seen) == len(cells)


def window_side(geometry: Geometry, cells: tuple[int, ...]) -> float:
    """The side of the least axis-aligned square holding the union of the cells."""
    index = list(cells)
    extent = geometry.upper[index].max(axis=0) - geometry.lower[index].min(axis=0)
    return float(extent.max())


def pattern_classes(geometry: Geometry, arity: int, window: float | None) -> list[int]:
    """Canonical masks of the connected (and windowed) classes of one arity, sorted."""
    classes: set[int] = set()
    for cells in itertools.combinations(range(len(geometry.names)), arity):
        if window is not None and window_side(geometry, cells) > window:
            continue
        if connected(geometry, cells):
            classes.add(canonical(mask_of(cells), geometry.group))
    return sorted(classes)


# ---------------------------------------------------------------------------
# One pattern: penalty, violation, local descent
# ---------------------------------------------------------------------------


class Problem:
    """The smooth penetration penalty and the true violation for one pattern.

    A pose is a `(k, 3)` array of centre `x`, centre `y` and angle, in the order of
    `cells`. The descent vector adds a normal angle and an offset per interacting pair.
    """

    def __init__(self, geometry: Geometry, cells: tuple[int, ...]) -> None:
        self.cap = geometry.cap
        self.cells = cells
        k = len(cells)
        self.k = k
        pairs = [
            (a, b)
            for a, b in itertools.combinations(range(k), 2)
            if geometry.interact[cells[a], cells[b]]
        ]
        self.p = len(pairs)
        self.first = np.array([a for a, _ in pairs], dtype=np.intp)
        self.second = np.array([b for _, b in pairs], dtype=np.intp)
        width = max(len(geometry.halfplanes[cell]) for cell in cells)
        self.plane_a = np.zeros((k, width))
        self.plane_b = np.zeros((k, width))
        self.plane_c = np.ones((k, width))
        self.plane_count = [len(geometry.halfplanes[cell]) for cell in cells]
        for row, cell in enumerate(cells):
            planes = geometry.halfplanes[cell]
            self.plane_a[row, : len(planes)] = planes[:, 0]
            self.plane_b[row, : len(planes)] = planes[:, 1]
            self.plane_c[row, : len(planes)] = planes[:, 2]
        self.polygons = [geometry.polygons[cell] for cell in cells]
        self.lower = geometry.lower[list(cells)]
        self.upper = geometry.upper[list(cells)]

    def pack(self, pose: Floats) -> Floats:
        """The descent vector of a pose, each pair's line through the centres' midpoint."""
        x, y = pose[:, 0], pose[:, 1]
        dx = x[self.second] - x[self.first]
        dy = y[self.second] - y[self.first]
        phi = np.arctan2(dy, dx)
        offset = (np.cos(phi) * (x[self.first] + x[self.second])) / 2 + (
            np.sin(phi) * (y[self.first] + y[self.second])
        ) / 2
        return np.concatenate([x, y, pose[:, 2], phi, offset])

    def pose(self, z: Floats) -> Floats:
        k = self.k
        return np.stack([z[:k], z[k : 2 * k], z[2 * k : 3 * k]], axis=1)

    def penalty(self, z: Floats) -> tuple[float, Floats]:
        """Squared hinge violations and their gradient."""
        k, p, cap = self.k, self.p, self.cap
        x, y, angle = z[:k], z[k : 2 * k], z[2 * k : 3 * k]
        phi, offset = z[3 * k : 3 * k + p], z[3 * k + p :]
        cos_t, sin_t = np.cos(angle)[:, None], np.sin(angle)[:, None]
        ox = cos_t * CORNER_X - sin_t * CORNER_Y
        oy = sin_t * CORNER_X + cos_t * CORNER_Y
        vx, vy = x[:, None] + ox, y[:, None] + oy
        low_x, high_x = np.minimum(vx, 0.0), np.maximum(vx - cap, 0.0)
        low_y, high_y = np.minimum(vy, 0.0), np.maximum(vy - cap, 0.0)
        value = float(
            (low_x * low_x).sum()
            + (high_x * high_x).sum()
            + (low_y * low_y).sum()
            + (high_y * high_y).sum()
        )
        grad_vx = 2.0 * (low_x + high_x)
        grad_vy = 2.0 * (low_y + high_y)
        excess = np.maximum(
            self.plane_a * x[:, None] + self.plane_b * y[:, None] - self.plane_c, 0.0
        )
        value += float((excess * excess).sum())
        grad_x = 2.0 * (excess * self.plane_a).sum(axis=1)
        grad_y = 2.0 * (excess * self.plane_b).sum(axis=1)
        grad_phi = np.zeros(p)
        grad_offset = np.zeros(p)
        if p:
            nx, ny = np.cos(phi)[:, None], np.sin(phi)[:, None]
            vx_first, vy_first = vx[self.first], vy[self.first]
            vx_second, vy_second = vx[self.second], vy[self.second]
            over_first = np.maximum(nx * vx_first + ny * vy_first - offset[:, None], 0.0)
            over_second = np.maximum(offset[:, None] - nx * vx_second - ny * vy_second, 0.0)
            value += float((over_first * over_first).sum() + (over_second * over_second).sum())
            # Elementwise scatter: a BLAS product here would spawn threads per call.
            np.add.at(grad_vx, self.first, 2.0 * over_first * nx)
            np.add.at(grad_vx, self.second, -2.0 * over_second * nx)
            np.add.at(grad_vy, self.first, 2.0 * over_first * ny)
            np.add.at(grad_vy, self.second, -2.0 * over_second * ny)
            turn_first = -ny * vx_first + nx * vy_first
            turn_second = -ny * vx_second + nx * vy_second
            grad_phi = 2.0 * ((over_first * turn_first).sum(axis=1)) - 2.0 * (
                (over_second * turn_second).sum(axis=1)
            )
            grad_offset = -2.0 * over_first.sum(axis=1) + 2.0 * over_second.sum(axis=1)
        grad_x += grad_vx.sum(axis=1)
        grad_y += grad_vy.sum(axis=1)
        grad_t = (grad_vy * ox - grad_vx * oy).sum(axis=1)
        return value, np.concatenate([grad_x, grad_y, grad_t, grad_phi, grad_offset])

    def violations(self, pose: Floats) -> dict[str, float]:
        """True violations of a pose in length units: pair, container and cell."""
        x, y, angle = pose[:, 0], pose[:, 1], pose[:, 2]
        support = (np.abs(np.cos(angle)) + np.abs(np.sin(angle))) / 2
        container = np.max(
            [support - x, x - (self.cap - support), support - y, y - (self.cap - support)]
        )
        cell = np.max(self.plane_a * x[:, None] + self.plane_b * y[:, None] - self.plane_c)
        pair = 0.0
        if self.p:
            first, second = self.first, self.second
            dx, dy = x[second] - x[first], y[second] - y[first]
            axes = np.stack(
                [
                    angle[first],
                    angle[first] + np.pi / 2,
                    angle[second],
                    angle[second] + np.pi / 2,
                ]
            )
            reach = np.abs(np.cos(axes) * dx + np.sin(axes) * dy)
            gap = (
                reach
                - (np.abs(np.cos(angle[first] - axes)) + np.abs(np.sin(angle[first] - axes)))
                / 2
                - (np.abs(np.cos(angle[second] - axes)) + np.abs(np.sin(angle[second] - axes)))
                / 2
            )
            pair = float(-gap.max(axis=0).min())
        return {
            "pair": max(pair, 0.0),
            "container": max(float(container), 0.0),
            "cell": max(float(cell), 0.0),
        }

    def violation(self, pose: Floats) -> float:
        return max(self.violations(pose).values())

    def random_centre(self, row: int, rng: np.random.Generator) -> tuple[float, float]:
        low, high = self.lower[row], self.upper[row]
        width = self.plane_count[row]
        a, b, c = (
            self.plane_a[row, :width],
            self.plane_b[row, :width],
            self.plane_c[row, :width],
        )
        for _ in range(1000):
            x, y = rng.uniform(low[0], high[0]), rng.uniform(low[1], high[1])
            if np.all(a * x + b * y <= c):
                return float(x), float(y)
        centre = self.polygons[row].mean(axis=0)
        return float(centre[0]), float(centre[1])

    def random_pose(self, rng: np.random.Generator) -> Floats:
        pose = np.empty((self.k, 3))
        for row in range(self.k):
            pose[row, :2] = self.random_centre(row, rng)
        pose[:, 2] = rng.uniform(0.0, np.pi / 2, self.k)
        return pose

    def descend(self, pose: Floats, *, polish: bool) -> Floats:
        options: dict[str, Any] = (
            {"maxiter": 1500, "ftol": 1e-24, "gtol": 1e-18, "maxcor": 30}
            if polish
            else {"maxiter": 600, "ftol": 1e-15, "gtol": 1e-12, "maxcor": 20}
        )
        result = minimize(
            self.penalty, self.pack(pose), jac=True, method="L-BFGS-B", options=options
        )
        return self.pose(np.asarray(result.x, dtype=np.float64))


@functools.cache
def _blas_thread_controls() -> tuple[tuple[Any, Any], ...]:
    """The thread setter and getter of every loaded scipy-openblas; empty if none is found."""
    maps = Path("/proc/self/maps")
    if not maps.exists():
        return ()
    paths = sorted(
        {
            line.split()[-1]
            for line in maps.read_text(encoding="utf-8").splitlines()
            if "openblas" in line.lower() and line.split()[-1].startswith("/")
        }
    )
    controls: list[tuple[Any, Any]] = []
    for path in paths:
        try:
            library = ctypes.CDLL(path)
        except OSError:
            continue
        for suffix in ("64_", ""):
            setter = getattr(library, f"scipy_openblas_set_num_threads{suffix}", None)
            getter = getattr(library, f"scipy_openblas_get_num_threads{suffix}", None)
            if setter is not None and getter is not None:
                controls.append((setter, getter))
                break
    return tuple(controls)


@contextlib.contextmanager
def single_thread_blas() -> Iterator[None]:
    """One BLAS thread while searching, restored after.

    L-BFGS-B's dense steps are tiny here, and waking a thread pool on each of them made a
    search ten times slower in wall time and twice as expensive in CPU (measured).
    """
    controls = _blas_thread_controls()
    saved = [int(getter()) for _, getter in controls]
    for setter, _ in controls:
        setter(1)
    try:
        yield
    finally:
        for (setter, _), count in zip(controls, saved, strict=True):
            setter(count)


@dataclass
class Verdict:
    """A pattern's search outcome: the best pose and its violation over all attempts."""

    mask: int
    cells: tuple[int, ...]
    feasible: bool
    violation: float
    pose: Floats
    attempts: int
    found_by: str
    components: dict[str, float] = field(default_factory=dict[str, float])


@dataclass(frozen=True)
class Budget:
    """Attempts per pattern: sub-pattern warm starts, random starts, basin hops.

    The deep stage runs only for a pattern the first stage could not place: the
    sub-pattern witnesses again with the added square redrawn, alternating with random
    poses, then hops alternating between the narrow and the wide kick. At seed 1 the first
    stage alone flagged two arity-six classes that other seeds placed in 3 and 77 to 127
    attempts, one of them excluding half of all states, which is what the deep stage is for.
    """

    starts: int = 12
    hops: int = 24
    hop_centre: float = 0.08
    hop_angle: float = 0.35
    deep_starts: int = 256
    deep_hops: int = 256
    wide_centre: float = 0.25
    wide_angle: float = 0.8
    margin: float = MARGIN


def search(
    geometry: Geometry,
    cells: tuple[int, ...],
    rng: np.random.Generator,
    budget: Budget,
    warm: list[tuple[int, Floats]] | None = None,
) -> Verdict:
    """Try hard to place the pattern; feasible as soon as one pose is within the margin."""
    with single_thread_blas():
        return _search(geometry, cells, rng, budget, warm)


def _search(
    geometry: Geometry,
    cells: tuple[int, ...],
    rng: np.random.Generator,
    budget: Budget,
    warm: list[tuple[int, Floats]] | None,
) -> Verdict:
    problem = Problem(geometry, cells)
    best: tuple[float, Floats] | None = None
    attempts = 0

    def attempt(start: Floats, how: str) -> Verdict | None:
        nonlocal best, attempts
        attempts += 1
        pose = problem.descend(start, polish=False)
        value = problem.violation(pose)
        if budget.margin < value < POLISH_BELOW:
            polished = problem.descend(pose, polish=True)
            polished_value = problem.violation(polished)
            if polished_value < value:
                pose, value = polished, polished_value
        if best is None or value < best[0]:
            best = (value, pose)
        if value <= budget.margin:
            return Verdict(
                mask_of(cells),
                cells,
                feasible=True,
                violation=value,
                pose=pose,
                attempts=attempts,
                found_by=how,
                components=problem.violations(pose),
            )
        return None

    def hop(centre: float, angle: float) -> Floats:
        assert best is not None
        start = best[1].copy()
        start[:, :2] += rng.normal(0.0, centre, (problem.k, 2))
        start[:, 2] += rng.normal(0.0, angle, problem.k)
        return start

    def redraw(template: tuple[int, Floats]) -> Floats:
        row, start = template[0], template[1].copy()
        start[row, :2] = problem.random_centre(row, rng)
        start[row, 2] = rng.uniform(0.0, np.pi / 2)
        return start

    templates = warm or []
    for _, start in templates:
        outcome = attempt(start, "warm")
        if outcome is not None:
            return outcome
    for _ in range(budget.starts):
        outcome = attempt(problem.random_pose(rng), "random")
        if outcome is not None:
            return outcome
    for _ in range(budget.hops):
        outcome = attempt(hop(budget.hop_centre, budget.hop_angle), "hop")
        if outcome is not None:
            return outcome
    for index in range(budget.deep_starts):
        if templates and index % 2 == 0:
            start, how = redraw(templates[(index // 2) % len(templates)]), "deep-warm"
        else:
            start, how = problem.random_pose(rng), "deep-random"
        outcome = attempt(start, how)
        if outcome is not None:
            return outcome
    for index in range(budget.deep_hops):
        start = (
            hop(budget.hop_centre, budget.hop_angle)
            if index % 2 == 0
            else hop(budget.wide_centre, budget.wide_angle)
        )
        outcome = attempt(start, "deep-hop")
        if outcome is not None:
            return outcome
    assert best is not None
    value, pose = best
    return Verdict(
        mask_of(cells),
        cells,
        feasible=False,
        violation=value,
        pose=pose,
        attempts=attempts,
        found_by="none",
        components=problem.violations(pose),
    )


def pattern_rng(seed: int, mask: int) -> np.random.Generator:
    return np.random.default_rng(np.random.SeedSequence([seed, mask]))


# ---------------------------------------------------------------------------
# Witness transport under the group
# ---------------------------------------------------------------------------


def transform_pose(
    geometry: Geometry, cells: tuple[int, ...], pose: Floats, element: int
) -> tuple[tuple[int, ...], Floats]:
    """The image of a witness under one group element, rows sorted by image cell."""
    action = geometry.actions[element]
    permutation = geometry.group[element]
    half = geometry.cap / 2
    x, y, angle = pose[:, 0] - half, pose[:, 1] - half, pose[:, 2].copy()
    if action[0] == "f":
        x, angle = -x, -angle
    for _ in range(int(action[1])):
        x, y = -y, x
        angle = angle + np.pi / 2
    image = np.stack([x + half, y + half, np.mod(angle, np.pi / 2)], axis=1)
    targets = [permutation[cell] for cell in cells]
    order = sorted(range(len(cells)), key=lambda row: targets[row])
    return tuple(targets[row] for row in order), image[order]


def warm_starts(
    geometry: Geometry,
    cells: tuple[int, ...],
    witnesses: dict[int, Floats],
    rng: np.random.Generator,
) -> list[tuple[int, Floats]]:
    """Each `k - 1`-cell witness, with the missing square (its row) added at random."""
    problem: Problem | None = None
    starts: list[tuple[int, Floats]] = []
    for row, _ in enumerate(cells):
        rest = cells[:row] + cells[row + 1 :]
        witness = witnesses.get(mask_of(rest))
        if witness is None:
            continue
        if problem is None:
            problem = Problem(geometry, cells)
        start = np.empty((len(cells), 3))
        start[:row], start[row + 1 :] = witness[:row], witness[row:]
        start[row, :2] = problem.random_centre(row, rng)
        start[row, 2] = rng.uniform(0.0, np.pi / 2)
        starts.append((row, start))
    return starts


# ---------------------------------------------------------------------------
# The endpoint and the positive controls
# ---------------------------------------------------------------------------


def _middle(value: Any) -> float:
    return float((value.lo + value.hi) / 2)


def endpoint_pose(design_name: str = DEFAULT_DESIGN) -> dict[str, Any]:
    """The endpoint's cells and pose on the cover: label, cell index, centre and angle."""
    design = cover.DESIGNS[design_name]
    cells = cover.build_cover(design)
    t, b, _ = cover.load_root_box(cover.CERTIFICATE)
    point = cover.endpoint(t, b)
    family = cover.family_state(cells, point, cover.ENDPOINT)
    if not family["one_state"]:
        raise ValueError(f"the endpoint is in no single state of {design_name}")
    index = {cell.name: k for k, cell in enumerate(cells)}
    theta = math.atan2(_middle(point.aux["u"][1]), _middle(point.aux["u"][0]))
    beta = math.atan2(_middle(point.aux["p"][1]), _middle(point.aux["p"][0]))
    rows: list[tuple[int, int, float, float, float]] = []
    for entry in family["squares"]:
        label = entry["label"]
        x, y = point.centres[label - 1]
        angle = theta if label in THETA_LABELS else beta if label == 16 else 0.0
        rows.append((index[entry["cell"]], label, _middle(x), _middle(y), angle))
    rows.sort()
    return {
        "cells": tuple(row[0] for row in rows),
        "labels": tuple(row[1] for row in rows),
        "pose": np.array([[row[2], row[3], math.fmod(row[4], math.pi / 2)] for row in rows]),
    }


def endpoint_witnesses(
    geometry: Geometry, endpoint: dict[str, Any], max_arity: int
) -> tuple[set[int], dict[str, Any]]:
    """Every class of an endpoint sub-pattern, witnessed feasible at the endpoint pose."""
    cells: tuple[int, ...] = endpoint["cells"]
    pose: Floats = endpoint["pose"]
    whole = Problem(geometry, cells).violations(pose)
    witnessed: set[int] = set()
    worst = 0.0
    for arity in range(1, max_arity + 1):
        for rows in itertools.combinations(range(len(cells)), arity):
            sub = tuple(cells[row] for row in rows)
            worst = max(worst, Problem(geometry, sub).violation(pose[list(rows)]))
            witnessed.add(canonical(mask_of(sub), geometry.group))
    record = {
        "state": [geometry.names[cell] for cell in cells],
        "labels": list(endpoint["labels"]),
        "violation_at_pose": whole,
        "worst_sub_pattern_violation_at_pose": worst,
        "tolerance": ENDPOINT_POSE_TOLERANCE,
        "witnessed_classes": len(witnessed),
        "passed": max(whole.values()) <= ENDPOINT_POSE_TOLERANCE
        and worst <= ENDPOINT_POSE_TOLERANCE,
    }
    return witnessed, record


def tight_control(
    geometry: Geometry,
    endpoint: dict[str, Any],
    rows: tuple[int, ...],
    *,
    seed: int,
    budget: Budget,
    half_side: float = TIGHT_HALF_SIDE,
) -> dict[str, Any]:
    """Endpoint squares in small boxes about their own centres, searched from random poses."""
    pose: Floats = endpoint["pose"]
    boxes = [
        np.array(
            [
                [pose[row, 0] - half_side, pose[row, 1] - half_side],
                [pose[row, 0] + half_side, pose[row, 1] - half_side],
                [pose[row, 0] + half_side, pose[row, 1] + half_side],
                [pose[row, 0] - half_side, pose[row, 1] + half_side],
            ]
        )
        for row in rows
    ]
    tight = make_geometry(
        boxes,
        [f"endpoint-{endpoint['labels'][row]}" for row in rows],
        cap=geometry.cap,
    )
    cells = tuple(range(len(rows)))
    verdict = search(tight, cells, pattern_rng(seed, mask_of(rows)), budget)
    return {
        "labels": [endpoint["labels"][row] for row in rows],
        "half_side": half_side,
        "best_violation": verdict.violation,
        "attempts": verdict.attempts,
        "passed": verdict.feasible,
    }


def contact_clusters(endpoint: dict[str, Any], size: int) -> list[tuple[int, ...]]:
    """Sets of endpoint squares grown from each square through its nearest neighbours."""
    pose: Floats = endpoint["pose"]
    centres = pose[:, :2]
    clusters: set[tuple[int, ...]] = set()
    for seed_row in range(len(centres)):
        chosen = [seed_row]
        while len(chosen) < size:
            distance = np.min(
                np.linalg.norm(centres[:, None, :] - centres[None, chosen, :], axis=2), axis=1
            )
            distance[chosen] = math.inf
            chosen.append(int(np.argmin(distance)))
        clusters.add(tuple(sorted(chosen)))
    return sorted(clusters)


# ---------------------------------------------------------------------------
# The sweep
# ---------------------------------------------------------------------------

_WORKER: dict[str, Any] = {}


def _initialise(geometry: Geometry, budget: Budget, seed: int) -> None:
    _WORKER.update(geometry=geometry, budget=budget, seed=seed)


def _solve(
    task: tuple[int, list[tuple[int, Floats]]],
) -> tuple[int, bool, float, Floats, int, str]:
    mask, sub_witnesses = task
    geometry: Geometry = _WORKER["geometry"]
    cells = cells_of(mask)
    rng = pattern_rng(_WORKER["seed"], mask)
    witnesses = {mask_of(cells[:row] + cells[row + 1 :]): w for row, w in sub_witnesses}
    warm = warm_starts(geometry, cells, witnesses, rng)
    verdict = search(geometry, cells, rng, _WORKER["budget"], warm)
    return (
        mask,
        verdict.feasible,
        verdict.violation,
        verdict.pose,
        verdict.attempts,
        verdict.found_by,
    )


def _sub_witness_payload(
    cells: tuple[int, ...], witnesses: dict[int, Floats]
) -> list[tuple[int, Floats]]:
    payload: list[tuple[int, Floats]] = []
    for row in range(len(cells)):
        witness = witnesses.get(mask_of(cells[:row] + cells[row + 1 :]))
        if witness is not None:
            payload.append((row, witness))
    return payload


def sweep(
    geometry: Geometry,
    *,
    max_arity: int,
    seed: int,
    budget: Budget,
    window: float | None = None,
    workers: int = 1,
    witnessed: set[int] | None = None,
    timeout: float | None = None,
    progress: bool = False,
) -> dict[str, Any]:
    """Bottom-up search of every connected class; flags, false flags and timings."""
    clock = time.perf_counter()
    witnessed = witnessed or set()
    witnesses: dict[int, Floats] = {}
    flagged: dict[int, dict[str, Any]] = {}
    flagged_masks: list[int] = []
    false_flags: list[dict[str, Any]] = []
    levels: dict[str, Any] = {}
    executor = (
        ProcessPoolExecutor(
            max_workers=workers, initializer=_initialise, initargs=(geometry, budget, seed)
        )
        if workers > 1
        else None
    )
    if executor is None:
        _initialise(geometry, budget, seed)
    complete = True
    try:
        for arity in range(1, max_arity + 1):
            level_clock = time.perf_counter()
            classes = pattern_classes(geometry, arity, window)
            pruned = [m for m in classes if any(f & m == f for f in flagged_masks)]
            pruned_set = set(pruned)
            tasks = [
                (mask, _sub_witness_payload(cells_of(mask), witnesses))
                for mask in classes
                if mask not in pruned_set
            ]
            results = (
                executor.map(_solve, tasks, chunksize=8)
                if executor is not None
                else map(_solve, tasks)
            )
            outcomes = []
            for outcome in results:
                outcomes.append(outcome)
                if timeout is not None and time.perf_counter() - clock > timeout:
                    complete = False
                    break
            attempts = 0
            found: dict[str, int] = {}
            new_flags = 0
            for mask, feasible, value, pose, count, how in sorted(outcomes, key=lambda o: o[0]):
                attempts += count
                cells = cells_of(mask)
                if feasible:
                    found[how] = found.get(how, 0) + 1
                    for element in range(len(geometry.group)):
                        image_cells, image_pose = transform_pose(geometry, cells, pose, element)
                        witnesses[mask_of(image_cells)] = image_pose
                    continue
                record = {
                    "arity": arity,
                    "cells": [geometry.names[cell] for cell in cells],
                    "indices": list(cells),
                    "best_penetration": value,
                    "attempts": count,
                }
                if mask in witnessed:
                    false_flags.append(record)
                    continue
                new_flags += 1
                flagged[mask] = record
                flagged_masks.extend(sorted(orbit(mask, geometry.group)))
            levels[str(arity)] = {
                "classes": len(classes),
                "pruned_as_supersets": len(pruned),
                "searched": len(outcomes),
                "feasible": sum(found.values()),
                "feasible_by": dict(sorted(found.items())),
                "flagged": new_flags,
                "attempts": attempts,
                "seconds": round(time.perf_counter() - level_clock, 3),
            }
            if progress:
                print(json.dumps({"arity": arity, **levels[str(arity)]}), flush=True)
            if not complete:
                break
    finally:
        if executor is not None:
            executor.shutdown(cancel_futures=True)
    return {
        "levels": levels,
        "flagged": [flagged[mask] for mask in sorted(flagged)],
        "flagged_masks": sorted(flagged),
        "false_flags": false_flags,
        "complete": complete,
        "seconds": round(time.perf_counter() - clock, 3),
    }


# ---------------------------------------------------------------------------
# Consumer: the exact count of surviving states and orbits
# ---------------------------------------------------------------------------


def all_states(cells: int, size: int) -> NDArray[np.int64]:
    return np.array(
        [mask_of(combination) for combination in itertools.combinations(range(cells), size)],
        dtype=np.int64,
    )


def apply_permutation(
    states: NDArray[np.int64], permutation: tuple[int, ...]
) -> NDArray[np.int64]:
    image = np.zeros_like(states)
    for cell, target in enumerate(permutation):
        image |= ((states >> cell) & 1) << target
    return image


def survivors(states: NDArray[np.int64], forbidden: list[int]) -> NDArray[np.int64]:
    alive = states
    for pattern in sorted(set(forbidden)):
        alive = alive[(alive & pattern) != pattern]
    return alive


def count_orbits(
    alive: NDArray[np.int64], group: tuple[tuple[int, ...], ...]
) -> dict[str, Any]:
    """Burnside's count and the distinct canonical forms, which must agree."""
    images = [apply_permutation(alive, permutation) for permutation in group]
    fixed = [int(np.count_nonzero(image == alive)) for image in images]
    if sum(fixed) % len(group):
        raise ValueError("Burnside sum is not divisible by the group order")
    burnside = sum(fixed) // len(group)
    distinct = int(np.unique(np.min(np.stack(images), axis=0)).size) if alive.size else 0
    if burnside != distinct:
        raise ValueError(f"orbit counts disagree: Burnside {burnside}, canonical {distinct}")
    return {"orbits": burnside, "fixed_counts": fixed}


def consume(
    cells: int,
    group: tuple[tuple[int, ...], ...],
    flagged: list[int],
    *,
    size: int = TARGET,
    endpoint_state: int | None = None,
    states: NDArray[np.int64] | None = None,
) -> dict[str, Any]:
    """States with no flagged pattern in any group image, and their orbits."""
    states = all_states(cells, size) if states is None else states
    forbidden = sorted({image for mask in flagged for image in orbit(mask, group)})
    alive = survivors(states, forbidden)
    record: dict[str, Any] = {
        "states": int(states.size),
        "forbidden_images": len(forbidden),
        "surviving_states": int(alive.size),
        **count_orbits(alive, group),
    }
    if endpoint_state is not None:
        record["endpoint_survives"] = bool(np.any(alive == endpoint_state))
    return record


def greedy_order(
    cells: int,
    group: tuple[tuple[int, ...], ...],
    flagged: list[int],
    *,
    size: int = TARGET,
    states: NDArray[np.int64] | None = None,
) -> list[dict[str, Any]]:
    """Flagged classes in the order that removes the most surviving states first.

    Each class's excluded states are computed once as a packed bit row; a greedy step is
    then a popcount of every row against the states still alive.
    """
    states = all_states(cells, size) if states is None else states
    masks = sorted(set(flagged))
    if not masks:
        return []
    rows = np.empty((len(masks), (states.size + 7) // 8), dtype=np.uint8)
    for row, mask in enumerate(masks):
        hit = np.zeros(states.size, dtype=np.bool_)
        for image in sorted(orbit(mask, group)):
            hit |= (states & image) == image
        rows[row] = np.packbits(hit)
    alive = np.packbits(np.ones(states.size, dtype=np.bool_))
    left = int(states.size)
    remaining = list(range(len(masks)))
    order: list[dict[str, Any]] = []
    while remaining:
        counts = np.bitwise_count(rows[remaining] & alive).sum(axis=1, dtype=np.int64)
        pick = int(np.argmax(counts))
        removes = int(counts[pick])
        if removes == 0:
            order.extend(
                {"mask": masks[row], "removes": 0, "states_left": left} for row in remaining
            )
            break
        row = remaining.pop(pick)
        alive &= ~rows[row]
        left -= removes
        order.append({"mask": masks[row], "removes": removes, "states_left": left})
    return order


# ---------------------------------------------------------------------------
# Receipt
# ---------------------------------------------------------------------------


def run(
    *,
    design_name: str = DEFAULT_DESIGN,
    max_arity: int = 5,
    seed: int = 1,
    budget: Budget | None = None,
    window: float | None = None,
    workers: int = 1,
    timeout: float | None = None,
    tight_sizes: tuple[int, ...] = (3, 4, 5),
    progress: bool = False,
) -> dict[str, Any]:
    clock = time.perf_counter()
    budget = budget or Budget()
    geometry = cover_geometry(design_name)
    endpoint = endpoint_pose(design_name)
    endpoint_state = mask_of(endpoint["cells"])
    witnessed, endpoint_record = endpoint_witnesses(geometry, endpoint, max_arity)
    tight = [
        tight_control(geometry, endpoint, rows, seed=seed, budget=budget)
        for size in tight_sizes
        for rows in contact_clusters(endpoint, size)
    ]
    swept = sweep(
        geometry,
        max_arity=max_arity,
        seed=seed,
        budget=budget,
        window=window,
        workers=workers,
        witnessed=witnessed,
        timeout=timeout,
        progress=progress,
    )
    states = all_states(len(geometry.names), TARGET)
    by_arity: dict[str, Any] = {}
    for arity in range(1, max_arity + 1):
        masks = [m for m in swept["flagged_masks"] if m.bit_count() <= arity]
        by_arity[str(arity)] = {
            "flagged_classes": len(masks),
            **consume(
                len(geometry.names),
                geometry.group,
                masks,
                endpoint_state=endpoint_state,
                states=states,
            ),
        }
    order = greedy_order(
        len(geometry.names), geometry.group, swept["flagged_masks"], states=states
    )
    by_mask = dict(zip(swept["flagged_masks"], swept["flagged"], strict=True))
    priority = [
        {
            **step,
            "cells": by_mask[step["mask"]]["cells"],
            "best_penetration": by_mask[step["mask"]]["best_penetration"],
        }
        for step in order
    ]
    controls = {
        "endpoint_pose": endpoint_record,
        "tight_endpoint_clusters": {
            "count": len(tight),
            "worst_best_violation": max(
                (entry["best_violation"] for entry in tight), default=0.0
            ),
            "failures": [entry for entry in tight if not entry["passed"]],
        },
        "search_false_flags_on_endpoint_sub_patterns": swept["false_flags"],
    }
    controls["passed"] = (
        endpoint_record["passed"]
        and not controls["tight_endpoint_clusters"]["failures"]
        and not swept["false_flags"]
        and by_arity[str(max_arity)]["endpoint_survives"]
    )
    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "status": STATUS,
        "design": design_name,
        "design_commit": DESIGN_COMMIT.get(design_name),
        "cap": str(cover.U),
        "cells": list(geometry.names),
        "interaction_edges": int(np.count_nonzero(np.triu(geometry.interact, 1))),
        "parameters": {
            "max_arity": max_arity,
            "seed": seed,
            "starts": budget.starts,
            "hops": budget.hops,
            "hop_centre": budget.hop_centre,
            "hop_angle": budget.hop_angle,
            "deep_starts": budget.deep_starts,
            "deep_hops": budget.deep_hops,
            "wide_centre": budget.wide_centre,
            "wide_angle": budget.wide_angle,
            "margin": budget.margin,
            "polish_below": POLISH_BELOW,
            "window": window,
            "workers": workers,
            "timeout": timeout,
        },
        "controls": controls,
        "sweep": {key: swept[key] for key in ("levels", "complete", "seconds")},
        "flagged": swept["flagged"],
        "survivors_by_arity": by_arity,
        "certification_priority": priority,
        "module_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    receipt["seconds"] = round(time.perf_counter() - clock, 3)
    return receipt


def without_timings(receipt: dict[str, Any]) -> dict[str, Any]:
    """The receipt with wall times removed, for determinism comparisons."""
    text = json.dumps(receipt, sort_keys=True, default=str)
    document = json.loads(text)
    document.pop("seconds", None)
    document["sweep"].pop("seconds", None)
    for level in document["sweep"]["levels"].values():
        level.pop("seconds", None)
    document["parameters"].pop("workers", None)
    return document


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--design", choices=sorted(cover.DESIGNS), default=DEFAULT_DESIGN)
    _ = parser.add_argument("--max-arity", type=int, default=5)
    _ = parser.add_argument("--seed", type=int, default=1)
    _ = parser.add_argument("--starts", type=int, default=Budget.starts)
    _ = parser.add_argument("--hops", type=int, default=Budget.hops)
    _ = parser.add_argument("--deep-starts", type=int, default=Budget.deep_starts)
    _ = parser.add_argument("--deep-hops", type=int, default=Budget.deep_hops)
    _ = parser.add_argument("--margin", type=float, default=MARGIN)
    _ = parser.add_argument("--window", type=float, default=None)
    _ = parser.add_argument("--workers", type=int, default=1)
    _ = parser.add_argument("--timeout", type=float, default=None, help="wall ceiling, s")
    _ = parser.add_argument("--output", type=Path, help="write the receipt here")
    arguments = parser.parse_args(argv)
    receipt = run(
        design_name=arguments.design,
        max_arity=arguments.max_arity,
        seed=arguments.seed,
        budget=Budget(
            starts=arguments.starts,
            hops=arguments.hops,
            deep_starts=arguments.deep_starts,
            deep_hops=arguments.deep_hops,
            margin=arguments.margin,
        ),
        window=arguments.window,
        workers=arguments.workers,
        timeout=arguments.timeout,
        progress=True,
    )
    text = json.dumps(receipt, indent=1, sort_keys=True, default=float)
    if arguments.output is not None:
        _ = arguments.output.write_text(text + "\n", encoding="utf-8")
    summary = {
        "status": receipt["status"],
        "controls_passed": receipt["controls"]["passed"],
        "complete": receipt["sweep"]["complete"],
        "levels": receipt["sweep"]["levels"],
        "survivors_by_arity": {
            arity: {
                key: entry[key]
                for key in (
                    "flagged_classes",
                    "surviving_states",
                    "orbits",
                    "endpoint_survives",
                )
            }
            for arity, entry in receipt["survivors_by_arity"].items()
        },
        "seconds": receipt["seconds"],
    }
    print(json.dumps(summary, indent=1, sort_keys=True))
    return 0 if receipt["controls"]["passed"] and receipt["sweep"]["complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
