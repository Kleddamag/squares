"""Proposition 5.1 of Karakuş 2026 is decided by a branch and bound, not read off the paper.

`T-083` and the lower half of `T-084` rest on Karakuş's strip measure, whose per-square
bound, Proposition 5.1, `devtools.check_karakus_strip_measure` decides over the square's
pose. These tests hold that program to its retained certificate, re-decided leaf by leaf;
hold its closed-form profile and point-row rule to the exact polygon scorer of
`devtools.check_nagamochi_lemma1_counterexample`, a separately written evaluator, on
explicit squares in explicit containers; sample the soundness of every bound and rule
against that scorer, and show the sampling rejects a deliberately unsound rule; sample the
proposition itself, including squares that both strip lines cut; and check that it refuses
three mutated measures whose witnesses that same scorer finds at most one.
"""

from __future__ import annotations

import json
import random
from fractions import Fraction

import pytest

import devtools.check_karakus_strip_measure as strip
from devtools.check_karakus_strip_measure import (
    CONTROLS,
    KARAKUS,
    LAMBDA_MAX,
    PART_B_V,
    RECEIPT,
    Box,
    Control,
    Measure,
    Orientation,
    StripMeasureError,
    bounds,
    corner_bounds,
    cos_sin,
    main,
    point_value,
    square_vertices,
    verify_tree,
    walk_tree,
)
from devtools.check_nagamochi_lemma1_counterexample import Measure as PolygonMeasure
from devtools.check_nagamochi_lemma1_counterexample import (
    clip_to_rectangle,
    karakus_strip_measure,
    segment_length_inside,
    signed_area,
)

Point = tuple[Fraction, Fraction]
Polygon = tuple[Point, ...]

ONE = Fraction(1)
TEN = Fraction(10)


def _retained() -> dict[str, object]:
    return json.loads(RECEIPT.read_text(encoding="utf-8"))


def _tree(part: str) -> str:
    parts = _retained()["parts"]
    assert isinstance(parts, dict)
    record = parts[part]
    assert isinstance(record, dict)
    tree = record["tree"]
    assert isinstance(tree, str)
    return tree


@pytest.mark.slow
def test_the_tool_replays_and_matches_its_receipt() -> None:
    assert main([]) == 0


def test_the_retained_trees_re_decide_leaf_by_leaf() -> None:
    seen = verify_tree("A", _tree("A"))
    assert seen["c"] > 0
    assert seen["m"] > seen["a"] + seen["c"]
    assert verify_tree("B", _tree("B")) == {"a": 1}


def test_a_leaf_relabelled_to_a_rule_that_fails_is_refused() -> None:
    tree = _tree("A")
    # The first margin leaf, relabelled as a corner leaf: it lies outside the corner box.
    corrupted = tree.replace("m", "c", 1)
    with pytest.raises(StripMeasureError):
        verify_tree("A", corrupted)


def test_a_truncated_or_overlong_tree_is_refused() -> None:
    tree = _tree("B")
    with pytest.raises(StripMeasureError):
        verify_tree("B", tree[:-1])
    with pytest.raises(StripMeasureError):
        verify_tree("B", tree + "a")


def test_the_certificate_does_not_hold_for_a_weaker_measure() -> None:
    with pytest.raises(StripMeasureError):
        verify_tree("A", _tree("A"), Measure(point=Fraction(49, 100)))


def test_the_bound_is_tight_at_the_floor_square() -> None:
    """At `theta = 0`, `u = 1`, `F - 1 = (lambda - 1)(lambda + 1/2)`: no slack at lambda = 1."""
    for lam in (Fraction(1000001, 1000000), Fraction(1001, 1000), LAMBDA_MAX):
        value = point_value(Fraction(0), lam, ONE, KARAKUS)
        assert value - 1 == (lam - 1) * (lam + Fraction(1, 2))


# -- the independent scorer ---------------------------------------------------------------


def _row_chord(polygon: Polygon, y: Fraction) -> tuple[Fraction, Fraction] | None:
    """The chord of a convex polygon at height `y`, or None when `y` misses its interior."""
    xs: list[Fraction] = []
    for i, (x1, y1) in enumerate(polygon):
        x2, y2 = polygon[(i + 1) % len(polygon)]
        if y1 == y:
            xs.append(x1)
        if (y1 - y) * (y2 - y) < 0:
            xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
    heights = [p[1] for p in polygon]
    if not xs or not min(heights) < y < max(heights):
        return None
    return min(xs), max(xs)


def _placed(tau: Fraction, lam: Fraction, u: Fraction, row: Fraction) -> Polygon:
    """The square with its lowest vertex at height `1 - u`, shifted so that its open chord
    at the point row starts at the integer 2: it then holds a point of the row exactly when
    the chord is longer than one, the fewest the row can give."""
    base = tuple((x, y + 1 - u) for x, y in square_vertices(tau, lam))
    chord = _row_chord(base, row)
    shift = Fraction(5, 2) if chord is None else 2 - chord[0]
    return tuple((x + shift, y) for x, y in base)


def _strip(a: Fraction, b: Fraction, measure: Measure) -> PolygonMeasure:
    """The strip measure with the controls' weights, built on the other module's types."""
    base = karakus_strip_measure(a, b)
    rectangles = base.rectangles
    segments = tuple((p, q, measure.line) for p, q, _ in base.segments)
    lower, upper = 1 - measure.offset, b - 1 + measure.offset
    points = tuple(
        ((x, lower if y < b / 2 else upper), measure.point) for (x, y), _ in base.points
    )
    return PolygonMeasure(rectangles, segments, points)


def _poses() -> list[tuple[Fraction, Fraction, Fraction]]:
    taus = (Fraction(0), Fraction(1, 50), Fraction(1, 7), Fraction(3, 10), Fraction(2, 5))
    lams = (Fraction(10001, 10000), Fraction(1001, 1000), LAMBDA_MAX)
    return [(t, lam, Fraction(k, 13)) for t in taus for lam in lams for k in range(1, 14)]


@pytest.mark.parametrize(("tau", "lam", "u"), _poses())
def test_the_closed_form_is_the_independent_scorer_on_explicit_squares(
    tau: Fraction, lam: Fraction, u: Fraction
) -> None:
    square = _placed(tau, lam, u, Fraction(4, 5))
    assert min(x for x, _ in square) > 0
    scored = karakus_strip_measure(TEN, TEN).score(square, closed=False)
    assert scored == point_value(tau, lam, u, KARAKUS)


def _control_poses() -> list[tuple[Control, tuple[Fraction, Fraction, Fraction]]]:
    """Each control's declared witness and the counterexample its own search found."""
    controls = _retained()["controls"]
    assert isinstance(controls, list)
    poses: list[tuple[Control, tuple[Fraction, Fraction, Fraction]]] = []
    for control, record in zip(CONTROLS, controls, strict=True):
        assert isinstance(record, dict)
        assert record["name"] == control.name
        found = record["found_by_search"]
        assert isinstance(found, dict)
        poses.append((control, control.witness))
        poses.append(
            (control, (Fraction(found["tau"]), Fraction(found["lambda"]), Fraction(found["u"])))
        )
    return poses


@pytest.mark.parametrize(("control", "pose"), _control_poses())
def test_each_control_counterexample_scores_at_most_one_on_the_independent_scorer(
    control: Control, pose: tuple[Fraction, Fraction, Fraction]
) -> None:
    tau, lam, u = pose
    square = _placed(tau, lam, u, 1 - control.measure.offset)
    mutated = _strip(TEN, TEN, control.measure).score(square, closed=False)
    assert mutated == point_value(tau, lam, u, control.measure)
    assert mutated <= 1
    assert karakus_strip_measure(TEN, TEN).score(square, closed=False) > 1


def _random_square(rng: random.Random, a: Fraction, b: Fraction, *, both: bool) -> Polygon:
    """A square of side in `(1, 101/100]` inside `[0, a] x [0, b]`, at any orientation."""
    tau = Fraction(rng.randrange(0, 1000), 1000)
    lam = 1 + Fraction(rng.randrange(1, 1001), 100000)
    c, s = cos_sin(tau)
    height = lam * (c + s)
    x0 = lam * s + (a - lam * (c + s)) * Fraction(rng.randrange(0, 1001), 1000)
    if both:
        # Straddle both strip lines: the lowest vertex below 1, the top above b - 1.
        low, high = max(Fraction(0), b - 1 - height), min(ONE, b - height)
        if low >= high:
            return ()
        z0 = low + (high - low) * Fraction(rng.randrange(1, 1000), 1000)
    else:
        z0 = (b - height) * Fraction(rng.randrange(0, 1001), 1000)
    return tuple((x + x0, y + z0) for x, y in square_vertices(tau, lam))


@pytest.mark.parametrize(
    ("a", "b"),
    [(Fraction(2), Fraction(3)), (Fraction(7, 2), Fraction(13, 4)), (Fraction(5), Fraction(6))],
)
def test_sampled_squares_score_above_one(a: Fraction, b: Fraction) -> None:
    rng = random.Random(f"karakus-5.1-{a}-{b}")
    measure = karakus_strip_measure(a, b)
    both = 0
    for i in range(400):
        square = _random_square(rng, a, b, both=i % 2 == 0)
        if not square:
            continue
        assert all(0 <= x <= a and 0 <= y <= b for x, y in square)
        heights = [y for _, y in square]
        both += min(heights) < 1 and max(heights) > b - 1
        assert measure.score(square, closed=False) > 1
    if b <= Fraction(13, 4):
        assert both > 50


def test_part_b_reaches_every_depth_both_lines_can_cut() -> None:
    assert (1 + PART_B_V) ** 2 >= 2 * LAMBDA_MAX**2


# -- the rules' soundness, sampled against exact geometry ------------------------------------

#: A frame wide enough to hold every square the sampler builds, lowest vertex at the origin.
FRAME = Fraction(5)


def _open_chord(square: Polygon, y: Fraction) -> Fraction:
    """The open square's chord at height `y`, by the other module's segment clipper."""
    return segment_length_inside(
        square, ((-FRAME, y), (FRAME, y), Fraction(1, 2)), closed=False
    )


def _exact(tau: Fraction, lam: Fraction, v: Fraction, measure: Measure) -> tuple[Fraction, int]:
    """`E(v)` and the point-row indicator at one pose, from the explicit square alone."""
    square = square_vertices(tau, lam)
    below = clip_to_rectangle(square, (-FRAME, -FRAME, FRAME, v, ONE))
    area = abs(signed_area(below)) if len(below) >= 3 else Fraction(0)
    row = int(_open_chord(square, v - measure.offset) > 1)
    return -area + measure.line * _open_chord(square, v), row


def _box_poses(box: Box) -> list[tuple[Fraction, Fraction, Fraction]]:
    """The box's eight corners and centre, with `lambda = 1` and `v = 0` pulled inside, since
    every bound need hold only at `lambda > 1` and a cut at `v = 0` is no cut."""
    t0, t1, l0, l1, v0, v1 = box
    lo = l0 + (l1 - l0) / 1024 if l0 == 1 else l0
    vlo = v0 + (v1 - v0) / 1024 if v0 == 0 else v0
    corners = [(t, lam, v) for t in (t0, t1) for lam in (lo, l1) for v in (vlo, v1)]
    return [*corners, ((t0 + t1) / 2, (lo + l1) / 2, (vlo + v1) / 2)]


def _enclosed(o: Orientation, tau: Fraction) -> bool:
    c, s = cos_sin(tau)
    values = ((min(c, s), o.m), (max(c, s), o.big_m), (c * s, o.p), (c + s, o.h))
    return all(low <= value <= high for value, (low, high) in values)


def _corner_holds(
    o: Orientation, pose: tuple[Fraction, Fraction, Fraction], f: Fraction
) -> bool:
    """`F > 1`, and the corner rule's expansion in `delta` under its cell's `F - 1`."""
    tau, lam, v = pose
    c, s = cos_sin(tau)
    m, big = min(c, s), max(c, s)
    bound = corner_bounds(o, KARAKUS)
    delta = lam - 1
    if lam * m <= v <= lam * big and 2 * big * (f - 1) < bound.k0 + bound.k1 * delta:
        return False
    if v > lam * big and 2 * c * s * (f - 1) < bound.q0 * bound.bracket + bound.t1 * delta:
        return False
    return f > 1


def soundness_violations(
    part: str, leaves: list[tuple[str, Box]], measure: Measure = KARAKUS
) -> list[str]:
    """Every sampled pose at which a leaf's bounds or its rule's own inequality fail."""
    found: list[str] = []
    for code, box in leaves:
        o, b = bounds(box, measure, rows=part == "A")
        for pose in _box_poses(box):
            tau, lam, _ = pose
            gain, row = _exact(*pose, measure)
            f = lam * lam + gain + measure.point * row
            checks = {
                "enclosure": _enclosed(o, tau),
                "gain": b.e_lo <= gain,
                "row": b.w_lo <= row,
                "margin": code != "m" or box[2] ** 2 + b.e_lo + measure.point * b.w_lo <= f,
                "area": code != "a" or b.e_lo + measure.point * b.w_lo <= f - lam * lam,
                "corner": code != "c" or _corner_holds(o, pose, f),
            }
            found += [
                f"{part} {code} {box} {pose}: {name}" for name, ok in checks.items() if not ok
            ]
    return found


def _leaves(part: str) -> list[tuple[str, Box]]:
    return [(code, box) for code, box in walk_tree(part, _tree(part)) if code != "S"]


def _sampled_leaves() -> list[tuple[str, Box]]:
    """Every seventeenth margin leaf of part A and every area and corner leaf."""
    leaves = _leaves("A")
    return leaves[::17] + [(code, box) for code, box in leaves if code in "ac"]


def test_sampled_poses_respect_every_bound_and_rule() -> None:
    assert soundness_violations("A", _sampled_leaves()) == []
    assert soundness_violations("B", _leaves("B")) == []


@pytest.mark.slow
def test_every_retained_leaf_respects_every_bound_and_rule() -> None:
    assert soundness_violations("A", _leaves("A")) == []


def test_the_sampling_rejects_an_unsound_point_row_rule(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The row rule with the least `p` in place of the greatest claims a point the chord does
    not reach. The certificate still replays under it and the three controls are still
    refused (the review of 2026-10-06, finding 1), so the sampling must catch it."""

    def least_p(o: Orientation, box: Box, measure: Measure) -> int:
        _, _, l0, _, v0, v1 = box
        p0 = o.p[0]
        return int(p0 < v0 - measure.offset and v1 - measure.offset < l0 * o.h[0] - p0)

    monkeypatch.setattr(strip, "row_lower", least_p)
    violations = soundness_violations("A", _sampled_leaves())
    assert any(item.endswith(": row") for item in violations)
    # The rules that lean on the false row bound fail with it; nothing else does.
    assert {item.rsplit(": ", 1)[1] for item in violations} <= {"row", "margin", "area"}
