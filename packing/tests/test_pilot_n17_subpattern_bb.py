"""Fast checks of the P2 branch-and-bound pilot: rounding, the relaxation and verdicts."""

from __future__ import annotations

import math
import random
from fractions import Fraction

import mpmath
import pytest

from devtools import pilot_n17_subpattern_bb as bb

Q = Fraction


def rectangle(x0: str, x1: str, y0: str, y1: str) -> tuple[tuple[Fraction, Fraction], ...]:
    a, b, c, d = Q(x0), Q(x1), Q(y0), Q(y1)
    return ((a, c), (b, c), (b, d), (a, d))


def contains(interval: bb.Iv, value: Fraction | float) -> bool:
    return Q(interval[0]) <= Q(value) <= Q(interval[1])


def separated(pose_i: tuple[float, float, float], pose_j: tuple[float, float, float]) -> float:
    """The separating-axis gap of two unit squares (positive: interiors disjoint), mpmath."""
    mpmath.mp.prec = 100
    (xi, yi, ti), (xj, yj, tj) = pose_i, pose_j
    dx, dy = mpmath.mpf(xj) - mpmath.mpf(xi), mpmath.mpf(yj) - mpmath.mpf(yi)
    alpha = mpmath.mpf(tj) - mpmath.mpf(ti)
    g = mpmath.mpf(1) / 2 + (abs(mpmath.cos(alpha)) + abs(mpmath.sin(alpha))) / 2
    gaps = []
    for theta in (ti, tj):
        for k in range(4):
            phi = mpmath.mpf(theta) + k * mpmath.pi / 2
            gaps.append(mpmath.cos(phi) * dx + mpmath.sin(phi) * dy - g)
    return float(max(gaps))


def test_rounding_floor_encloses_exact_results() -> None:
    rng = random.Random(7)
    for _ in range(2000):
        a = sorted((rng.uniform(-3, 3), rng.uniform(-3, 3)))
        b = sorted((rng.uniform(-3, 3), rng.uniform(-3, 3)))
        ia, ib = (a[0], a[1]), (b[0], b[1])
        for x in (a[0], a[1]):
            for y in (b[0], b[1]):
                assert contains(bb.iadd(ia, ib), Q(x) + Q(y))
                assert contains(bb.isub(ia, ib), Q(x) - Q(y))
                assert contains(bb.imul(ia, ib), Q(x) * Q(y))
    for q in (Q(1169, 250), Q(1, 3), Q(-2, 7), Q(10**20 + 1, 10**20)):
        assert Q(bb.lower_float(q)) <= q <= Q(bb.upper_float(q))


def test_trig_enclosures_and_constants() -> None:
    mpmath.mp.prec = 200
    rng = random.Random(11)
    points = [0.0, 0.4, math.pi / 2, math.pi, -math.pi / 4] + [
        rng.uniform(-4, 8) for _ in range(300)
    ]
    for theta in points:
        c, s = bb.cos_sin(theta)
        assert c[0] <= mpmath.cos(mpmath.mpf(theta)) <= c[1]
        assert s[0] <= mpmath.sin(mpmath.mpf(theta)) <= s[1]
        assert c[1] - c[0] < 1e-15
        assert s[1] - s[0] < 1e-15
    for k, value in bb.HALF_PI_MULTIPLES.items():
        assert value[0] <= k * mpmath.pi / 2 <= value[1]
    root = bb.Solver(
        bb.Pattern(("a",), (rectangle("2", "2.1", "2", "2.1"),), bb.cover.U), bb.Settings()
    )
    lo, hi = root.root().angles[0]
    assert mpmath.mpf(hi) - mpmath.mpf(lo) >= mpmath.pi / 2


def test_half_width_and_gap_bounds_are_lower_bounds() -> None:
    mpmath.mp.prec = 120
    rng = random.Random(5)

    def h(value: float) -> float:
        return float((abs(mpmath.cos(value)) + abs(mpmath.sin(value))) / 2)

    for _ in range(400):
        lo = rng.uniform(-1, 2)
        hi = lo + rng.choice((1e-3, 0.05, 0.3, 1.0)) * rng.random()
        bound = bb.h_lower(lo, hi)
        samples = [lo, hi] + [rng.uniform(lo, hi) for _ in range(20)]
        assert all(bound <= h(t) + 1e-15 for t in samples)
        other = (rng.uniform(-1, 2), 0.0)
        other = (other[0], other[0] + 0.2 * rng.random())
        gap = bb.gap_lower((lo, hi), other)
        for _ in range(20):
            ti, tj = rng.uniform(lo, hi), rng.uniform(*other)
            assert gap <= 0.5 + h(tj - ti) + 1e-15


def test_disjoint_pair_poses_satisfy_every_cut() -> None:
    """Every disjoint pose in a node satisfies the hull cuts and one of the half-planes."""
    rng = random.Random(3)
    checked = 0
    for _ in range(70):
        ci = (Q(rng.randint(150, 200), 100), Q(rng.randint(150, 200), 100))
        offset = (Q(rng.randint(-150, 150), 100), Q(rng.randint(-150, 150), 100))
        cj = (ci[0] + offset[0], ci[1] + offset[1])
        size = Q(rng.randint(5, 40), 100)
        polygons = tuple(
            ((x, y), (x + size, y), (x + size, y + size), (x, y + size)) for x, y in (ci, cj)
        )
        pattern = bb.Pattern(("i", "j"), polygons, bb.cover.U)
        solver = bb.Solver(pattern, bb.Settings())
        root = solver.root()
        width = rng.choice((math.pi / 2, 0.3, 0.05))
        starts = [rng.uniform(root.angles[0][0], root.angles[0][1] - width) for _ in range(2)]
        angles = tuple((start, start + width) for start in starts)
        node = bb.Node(angles, solver.cell_boxes, (None,), 0)
        boxes = solver.contract(node)
        if boxes is None:
            continue
        term = solver.pair_term(node, boxes, 0)
        for _ in range(40):
            pose = [
                (
                    rng.uniform(box[0], box[1]),
                    rng.uniform(box[2], box[3]),
                    rng.uniform(*angle),
                )
                for box, angle in zip(boxes, angles, strict=True)
            ]
            if separated(pose[0], pose[1]) < 0:
                continue
            assert term.kind not in ("disc", "pair")
            checked += 1
            dx, dy = pose[1][0] - pose[0][0], pose[1][1] - pose[0][1]
            for ux, uy, v in term.cuts:
                assert ux * dx + uy * dy >= v - 1e-12
            if term.planes:
                assert max(nx * dx + ny * dy - r for nx, ny, r in term.planes) >= -1e-12
    assert checked > 100


def test_dual_bound_is_below_the_exact_value() -> None:
    rng = random.Random(9)
    boxes = ((1.0, 2.0, 1.5, 2.5), (2.0, 3.25, 1.0, 1.75))
    for _ in range(200):
        rows = []
        for _ in range(4):
            columns = (0, 1, 2, 3)
            values = tuple(rng.uniform(-1, 1) for _ in columns)
            rhs = rng.uniform(-2, 2)
            norm = rng.uniform(0.5, 2.0)
            rows.append(
                bb.Row(columns, values, rhs, norm, tuple((v, v) for v in values), (rhs, rhs))
            )
        weights = [rng.random() for _ in rows]
        cost = (rng.randrange(4), rng.choice((1.0, -1.0)))
        bound = bb.dual_bound(rows, weights, boxes, cost)
        combined = [Q(0)] * 4
        combined[cost[0]] = Q(cost[1])
        right = Q(0)
        for row, weight in zip(rows, weights, strict=True):
            y = Q(weight / row.norm)
            for column, value in zip(row.columns, row.values, strict=True):
                combined[column] += y * Q(value)
            right += y * Q(row.rhs)
        spans = [(b[0], b[1]) if axis == 0 else (b[2], b[3]) for b in boxes for axis in (0, 1)]
        exact = sum(
            (
                c * Q(span[0] if c > 0 else span[1])
                for c, span in zip(combined, spans, strict=True)
            ),
            start=Q(0),
        )
        assert Q(bound) <= exact - right


def three_in_a_row(right_x: tuple[str, str]) -> bb.Pattern:
    return bb.Pattern(
        ("left", "middle", "right"),
        (
            rectangle("1.00", "1.05", "2.00", "2.05"),
            rectangle("1.40", "2.40", "2.00", "2.05"),
            rectangle(*right_x, "2.00", "2.05"),
        ),
        bb.cover.U,
    )


@pytest.mark.parametrize(("right", "obbt_rounds"), [("2.80", 0), ("2.80", 3), ("2.94", 3)])
def test_a_crowded_row_is_certified(right: str, obbt_rounds: int) -> None:
    # The middle square needs a horizontal gap of at least sqrt(1 - 0.05^2) to each end
    # square, so the two end centres need 1.9975 between them; the cells allow at most
    # 1.85 or 1.94. Without bound tightening every leaf is an exact Farkas prune.
    right_x = (right, str(Q(right) + Q("0.05")))
    pattern = three_in_a_row((str(float(Q(right_x[0]))), str(float(Q(right_x[1])))))
    result = bb.search(pattern, bb.Settings(max_seconds=20, obbt_rounds=obbt_rounds))
    assert result["verdict"] == "certified-infeasible"
    assert result["farkas_failures"] == 0
    if obbt_rounds == 0:
        assert set(result["prune_reasons"]) == {"lp"}


@pytest.mark.parametrize("theta0", [0.0, bb.DEFAULT_THETA0])
def test_a_feasible_row_is_never_certified(theta0: float) -> None:
    # Axis-aligned squares at x = 1.00, 2.02 and 3.05 are disjoint.
    pattern = three_in_a_row(("3.05", "3.10"))
    result = bb.search(pattern, bb.Settings(theta0=theta0, max_seconds=1, max_nodes=300))
    assert result["verdict"] != "certified-infeasible"


@pytest.mark.parametrize("theta0", [0.0, bb.DEFAULT_THETA0])
def test_a_feasible_pose_survives_every_node_on_its_path(theta0: float) -> None:
    pattern = three_in_a_row(("3.05", "3.10"))
    pose = [(1.0, 2.0, 0.0), (2.025, 2.0, 0.0), (3.05, 2.0, 0.0)]
    result = bb.witness_path(pattern, bb.Settings(theta0=theta0), pose)
    assert result["passed"], result["failure"]
    assert result["final_max_angle_width"] < bb.DEFAULT_FLOOR


def test_the_tree_estimate_matches_a_small_exact_count() -> None:
    pattern = three_in_a_row(("2.80", "2.85"))
    exact = bb.search(pattern, bb.Settings())["nodes"]
    estimated = bb.estimate(pattern, bb.Settings(), dives=40)["estimated_nodes_mean"]
    assert abs(estimated - exact) <= 0.25 * exact
