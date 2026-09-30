"""Focused exact controls for the conditional mask-438 root pilot."""

from __future__ import annotations

from fractions import Fraction as Q

import pytest

from devtools import check_n11_capture_root_pilot as pilot
from devtools import check_n11_optimality_field_mask0 as geometry


def test_strict_core_rejects_touching_boundary_and_checks_whole_interval() -> None:
    assert pilot.strict_core(geometry.B / 2, Q(), Q(1, 64), Q(1), Q())
    assert not pilot.strict_core(geometry.B, Q(), Q(1, 64), Q(1), Q())
    assert not pilot.strict_core(Q(), Q(), Q(1, 64), Q(1), Q())
    assert pilot.quadratic_positive(Q(1), Q(-2), Q(2), Q(), Q(1))
    assert not pilot.quadratic_positive(Q(1), Q(-2), Q(1), Q(), Q(1))
    assert not pilot.quadratic_positive(Q(1, 4), Q(-1), Q(1), Q(), Q(1))
    assert not pilot.quadratic_positive(Q(1, 5), Q(-1), Q(1), Q(), Q(1))


def test_convex_region_controls_keep_degenerate_sets_without_enlarging_bowties() -> None:
    assert pilot.convex([["0", "0"]]) == [(Q(), Q())]
    assert pilot.convex([["0", "0"], ["1", "0"], ["1/2", "0"]]) == [
        (Q(), Q()),
        (Q(1), Q()),
    ]
    with pytest.raises(ValueError, match="region"):
        pilot.convex([["0", "0"], ["1", "1"], ["0", "1"], ["1", "0"]])


def test_exact_union_refuses_uncovered_and_zero_area_residuals() -> None:
    world = [(Q(1), Q(1)), (Q(2), Q(1)), (Q(2), Q(2)), (Q(1), Q(2))]
    side, _, _, _ = geometry.row_envelope((Q(), Q(1, 64)))
    base = {
        "interval": ["0", "1/64"],
        "reference_half_angle": "1/128",
        "core_side": str(side),
        "domain_restriction": {"kind": "original_cell"},
        "input_domain": [[str(x), str(y)] for x, y in world],
        "common_core_strips": [],
    }
    budget = geometry.Budget(float("inf"), 1000)
    for residual in (
        [[["1", "1"]]],
        [[["1", "1"], ["3/2", "1"], ["3/2", "2"], ["1", "2"]]],
    ):
        with pytest.raises(ValueError, match="uncovered"):
            pilot.row_check({**base, "residual_polygons": residual}, world, {}, budget=budget)


def test_compression_requires_exact_nonnegative_convex_witnesses() -> None:
    prior = [(Q(), Q()), (Q(1), Q()), (Q(1), Q(1)), (Q(), Q(1))]
    base = {
        "compression_source_hull": [[str(x), str(y)] for x, y in prior],
        "inner_grid_compression": {
            "denominator": 1,
            "vertices": [["0", "0"]] * 7,
            "witnesses": [
                {"point": ["0", "0"], "indices": [0], "weights": ["1"]} for _ in range(7)
            ],
        },
    }
    assert len(pilot.compressed_points(base, prior, [])) == 7
    bad = {
        **base,
        "inner_grid_compression": {
            **base["inner_grid_compression"],
            "witnesses": [
                {"point": ["0", "0"], "indices": [0], "weights": ["-1"]},
                *base["inner_grid_compression"]["witnesses"][1:],
            ],
        },
    }
    with pytest.raises(ValueError, match="convex combination"):
        pilot.compressed_points(bad, prior, [])
