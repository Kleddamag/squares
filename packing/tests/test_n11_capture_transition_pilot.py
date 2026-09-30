"""Exact controls for the first capture collision transition."""

from __future__ import annotations

import time
from copy import deepcopy
from fractions import Fraction as Q

import pytest

from devtools import check_n11_capture_transition_pilot as capture
from devtools import check_n11_optimality_field_mask0 as geometry


def test_universal_collision_includes_closed_tangency_but_not_outside() -> None:
    core = [(Q(-1, 2), Q(-1, 2)), (Q(1, 2), Q(-1, 2)), (Q(1, 2), Q(1, 2)), (Q(-1, 2), Q(1, 2))]
    query = [(Q(-2), Q(-2)), (Q(2), Q(-2)), (Q(2), Q(2)), (Q(-2), Q(2))]
    partner_domain = [(Q(), Q()), (Q(2), Q())]
    budget = geometry.Budget(time.monotonic() + 3, 1000)
    assert (
        capture.universal_collision(
            core, query, [(partner_domain, core)], [(Q(1), Q())], budget=budget
        )
        > 0
    )
    with pytest.raises(ValueError, match="universal collision"):
        capture.universal_collision(
            core, query, [(partner_domain, core)], [(Q(), Q())], budget=budget
        )
    with pytest.raises(ValueError, match="query domain"):
        capture.universal_collision(
            core, [(Q(), Q())], [(partner_domain, core)], [(Q(1), Q())], budget=budget
        )


def test_whole_angle_core_must_be_strict() -> None:
    tiny = [
        (Q(-1, 10), Q(-1, 10)),
        (Q(1, 10), Q(-1, 10)),
        (Q(1, 10), Q(1, 10)),
        (Q(-1, 10), Q(1, 10)),
    ]
    capture.strict_core(tiny, Q(), Q(1))
    boundary = [
        (Q(-1, 10), Q(-1, 10)),
        (geometry.B / 2, Q(-1, 10)),
        (geometry.B / 2, Q(1, 10)),
        (Q(-1, 10), Q(1, 10)),
    ]
    with pytest.raises(ValueError, match="strictly inside"):
        capture.strict_core(boundary, Q(), Q(1))


def test_outward_support_rounding_and_segment_outer() -> None:
    assert capture.outward_round(Q(1, 3)) == Q(33333334, 10**8)
    assert capture.outward_round(Q(-1, 3)) == Q(-33333333, 10**8)
    row = {"residual_polygons": [[["1/3", "0"], ["2/3", "0"]]]}
    world = [(Q(), Q()), (Q(1), Q()), (Q(1), Q(1)), (Q(), Q(1))]
    outer = capture.phase2_outer(row, world)
    assert outer
    assert all(x <= Q(66666667, 10**8) and y <= 0 for x, y in outer)


def test_row_output_requires_every_common_plane_and_safe_outer_support() -> None:
    core = [(Q(), Q()), (Q(1), Q()), (Q(1), Q(1)), (Q(), Q(1))]
    point = (Q(), Q())
    world = [(Q(-2), Q(-2)), (Q(2), Q(-2)), (Q(2), Q(2)), (Q(-2), Q(2))]
    row = {
        "common_core_halfplanes": [
            {"normal": [str(nx), str(ny)], "upper": str(upper)}
            for nx, ny, upper in capture.facets(core)
        ],
        "outer_bounds": [
            {"normal": [nx, ny], "upper": "0"} for nx, ny in capture.SUPPORT_NORMALS
        ],
        "outer_domain": [["0", "0"]],
    }
    assert capture.verify_row_output(row, core, [[point]], world) == 4
    missing = deepcopy(row)
    missing["common_core_halfplanes"].pop()
    with pytest.raises(ValueError, match="common-core"):
        capture.verify_row_output(missing, core, [[point]], world)
    unsafe = deepcopy(row)
    unsafe["outer_bounds"][0]["upper"] = "-1"
    with pytest.raises(ValueError, match="cuts residual"):
        capture.verify_row_output(unsafe, core, [[point]], world)
