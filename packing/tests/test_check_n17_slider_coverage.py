"""Exact controls for the H-268 slider-coverage checker."""

from __future__ import annotations

import math
import random
from fractions import Fraction as Q
from functools import cache

from devtools.check_n17_slider_coverage import (
    Rect,
    Scene,
    SixBox,
    along_v_rect,
    b_cover,
    build_scene,
    five_rect,
    rects_overlap,
    six_cover,
    six_overlaps,
    trig,
)


@cache
def scene() -> Scene:
    return build_scene()


def _float_overlap(first: list[tuple[float, float]], second: list[tuple[float, float]]) -> bool:
    for polygon in (first, second):
        for index, (x0, y0) in enumerate(polygon):
            x1, y1 = polygon[(index + 1) % len(polygon)]
            nx, ny = y1 - y0, x0 - x1
            a = [nx * x + ny * y for x, y in first]
            b = [nx * x + ny * y for x, y in second]
            if max(a) <= min(b) + 1e-12 or max(b) <= min(a) + 1e-12:
                return False
    return True


def _square(x: float, y: float, phi: float) -> list[tuple[float, float]]:
    c, s = math.cos(phi), math.sin(phi)
    return [
        (x + i * c / 2 - j * s / 2, y + i * s / 2 + j * c / 2)
        for i, j in ((1, 1), (-1, 1), (-1, -1), (1, -1))
    ]


def test_rect_overlap_is_strict() -> None:
    unit = Rect(Q(0), Q(0), Q(1), Q(0), Q(1, 2), Q(1, 2))
    touching = Rect(Q(1), Q(0), Q(1), Q(0), Q(1, 2), Q(1, 2))
    pressed = Rect(Q(99, 100), Q(0), Q(1), Q(0), Q(1, 2), Q(1, 2))
    diamond = Rect(Q(11, 10), Q(0), Q(3, 5), Q(4, 5), Q(1, 2), Q(1, 2))
    kissing = Rect(Q(6, 5), Q(0), Q(3, 5), Q(4, 5), Q(1, 2), Q(1, 2))
    assert not rects_overlap(unit, touching)
    assert rects_overlap(unit, pressed)
    # A turned square reaches 7/10 along e_x: it overlaps at 11/10 and touches at 6/5.
    assert rects_overlap(unit, diamond)
    assert not rects_overlap(unit, kissing)


def test_scene_binds_the_cell_and_the_non_sliders() -> None:
    built = scene()
    assert built.cell == (Q(1009, 375), Q(849, 250), Q(1, 2), Q(1411, 1000))
    assert sorted(built.fixed) == [1, 2, 3, 4, 7, 8, 9, 10, 12, 14, 15, 16, 17]
    assert built.half == Q(1, 2) - Q(2, 5000)
    # The slider rectangles keep their squeezing face: 5's left face at a1, 13's at z2.
    five = five_rect(built, (Q(1, 4), Q(3, 4)))
    assert five is not None
    assert five.p < Q(1, 4) + Q(1, 1000)
    thirteen = along_v_rect(built, 13, (Q(-1, 2), Q(0)), 1)
    assert thirteen is not None
    assert thirteen.q < Q(1, 4) + Q(1, 1000)


def test_six_overlap_is_sound_on_samples() -> None:
    rng = random.Random(268)
    obstacle = Rect(Q(0), Q(0), Q(3, 5), Q(4, 5), Q(1, 2), Q(1, 2))
    corners = [(float(x), float(y)) for x, y in obstacle.vertices()]
    corners = [corners[0], corners[1], corners[3], corners[2]]
    checked = 0
    for _ in range(300):
        t0 = Q(rng.randrange(0, 16), 16)
        x0 = Q(rng.randrange(-24, 24), 16)
        y0 = Q(rng.randrange(-24, 24), 16)
        box = SixBox((t0, t0 + Q(1, 16)), (x0, x0 + Q(1, 16)), (y0, y0 + Q(1, 16)))
        cos, sin = trig(box.t)
        if not six_overlaps(obstacle, box, cos, sin):
            continue
        checked += 1
        for _ in range(5):
            tau = rng.uniform(float(box.t[0]), float(box.t[1]))
            phi = 2 * math.atan(tau)
            x = rng.uniform(float(box.x[0]), float(box.x[1]))
            y = rng.uniform(float(box.y[0]), float(box.y[1]))
            assert _float_overlap(_square(x, y, phi), corners)
    assert checked > 20


def test_squeeze_closes_inside_the_cell() -> None:
    built = scene()
    five = five_rect(built, (Q(1, 4), Q(1, 2)))
    thirteen = along_v_rect(built, 13, (Q(-1, 4), Q(1, 16)), 1)
    assert five is not None
    assert thirteen is not None
    result = six_cover([*built.fixed.values(), five, thirteen], built.cell, built.outer)
    assert result.closed


def test_control_whole_box_cell_is_refused() -> None:
    built = scene()
    lo, hi = built.outer
    whole = (lo + Q(1, 2), hi - Q(1, 2), lo + Q(1, 2), hi - Q(1, 2))
    five = five_rect(built, (Q(1), Q(9, 8)))
    thirteen = along_v_rect(built, 13, (Q(-1, 4), Q(1, 16)), 1)
    assert five is not None
    assert thirteen is not None
    obstacles = [*built.fixed.values(), five, thirteen]
    assert six_cover(obstacles, built.cell, built.outer).closed
    refused = six_cover(obstacles, whole, built.outer, node_limit=20_000)
    assert not refused.closed
    assert refused.witness is not None
    assert refused.witness.x[0] > built.cell[1]


def test_b_bound_needs_the_tight_z_bound() -> None:
    built = scene()
    assert b_cover(built, Q(1, 12), Q(-1, 20)).passed
    loose = b_cover(built, Q(1, 12), Q(-1, 8))
    assert not loose.passed
    assert loose.failure is not None
