"""The interval route for T-056 and T-057: its arithmetic, its refusals and its receipts."""

from __future__ import annotations

import ast
import json
from dataclasses import replace
from decimal import ROUND_CEILING, ROUND_FLOOR, Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath
import pytest

from devtools import upper_bound_intervals as intervals
from devtools import upper_bound_packets as packets

SCALE = 10**40
#: Where the certified ceiling sits more than one unit above the printed side: n = 306 is
#: Couzo's packing of 3 October (T-092), the others his of 26 and 27 September (T-056).
TRAILING = {206, 259, 305, 306}


def _contains(enclosure: intervals.Iv, value: Any, scale: int) -> bool:
    return mpmath.mpf(enclosure.lo) / scale <= value <= mpmath.mpf(enclosure.hi) / scale


@pytest.mark.parametrize(
    ("angle", "unit"),
    [
        ("0", "radians"),
        ("0.32015710560680055000", "radians"),
        ("-0.469390294287837018", "radians"),
        ("1.57079633331250923", "radians"),
        ("-3.75053939718131214E-15", "radians"),
        ("6.5", "radians"),
        ("30", "degrees"),
        ("-135.25", "degrees"),
    ],
)
def test_cos_and_sin_are_enclosed_within_a_unit_of_the_last_place(
    angle: str, unit: str
) -> None:
    """mpmath at 120 digits is an oracle here only; the route itself never calls it."""
    cosine, sine = intervals.cos_sin(angle, unit, SCALE)
    with mpmath.workdps(120):
        radians = mpmath.mpf(angle) * (mpmath.pi / 180 if unit == "degrees" else 1)
        assert _contains(cosine, mpmath.cos(radians), SCALE)
        assert _contains(sine, mpmath.sin(radians), SCALE)
    assert cosine.hi - cosine.lo <= 3
    assert sine.hi - sine.lo <= 3


def test_an_axis_aligned_angle_is_exact() -> None:
    assert intervals.cos_sin("0.00000000000000000e+00", "radians", SCALE) == (
        intervals.Iv(SCALE, SCALE),
        intervals.Iv(0, 0),
    )


def test_pi_is_enclosed() -> None:
    big = 10**60
    pi = intervals.pi_enclosure(big)
    with mpmath.workdps(100):
        assert _contains(pi, mpmath.pi, big)
    assert pi.hi - pi.lo < 1000


def _pose(side: str, *squares: tuple[str, str, str], unit: str = "radians") -> intervals.Pose:
    return intervals.Pose(n=len(squares), side=side, unit=unit, squares=squares)


def test_a_two_by_two_grid_passes_with_its_four_contacts_decided_exactly() -> None:
    grid = _pose(
        "2",
        ("0.5", "0.5", "0"),
        ("1.5", "0.5", "0"),
        ("0.5", "1.5", "0"),
        ("1.5", "1.5", "0"),
    )
    decision = intervals.decide(grid)
    assert decision.verdict == intervals.VERIFIED
    assert decision.side == intervals.Iv(2 * SCALE, 2 * SCALE)
    assert decision.bound == "2"
    assert decision.printed == intervals.CERTIFIED
    # The diagonal pairs' centres are exactly sqrt(2) apart, so the circles decide them.
    assert (decision.pairs_pruned, decision.separated, decision.touching) == (2, 4, 4)
    assert decision.walls.certified == 16


def test_a_rotated_square_has_extent_root_two_and_its_side_is_decided_both_ways() -> None:
    diamond = _pose("1.5", ("0.75", "0.75", "45"), unit="degrees")
    decision = intervals.decide(diamond, Fraction("1.41421"))
    with mpmath.workdps(60):
        assert _contains(decision.side, mpmath.sqrt(2), decision.scale)
    assert decision.printed == intervals.CERTIFIED
    assert decision.claimed == intervals.REFUTED
    assert decision.verdict == intervals.REFUSED
    assert intervals.decide(diamond, Fraction("1.41422")).verdict == intervals.VERIFIED


def test_touching_is_allowed_and_overlap_is_refused() -> None:
    touching = _pose("2", ("0.5", "0.5", "0"), ("1.5", "0.5", "0"))
    assert intervals.decide(touching).verdict == intervals.VERIFIED
    overlapping = _pose("2", ("0.5", "0.5", "0"), ("1.4999", "0.5", "0"))
    decision = intervals.decide(overlapping)
    assert decision.verdict == intervals.REFUSED
    assert decision.overlapping == ((1, 2),)


def _near_contact(rounding: str) -> intervals.Pose:
    """Two squares at 0.5 rad, the second one unit along the first's edge, rounded at 50
    places: outward leaves a gap below 1e-49, inward an overlap below 1e-49."""
    with mpmath.workdps(80):
        step = [str(mpmath.nstr(mpmath.cos(0.5), 70)), str(mpmath.nstr(mpmath.sin(0.5), 70))]
    with localcontext() as context:
        context.prec = 100
        shift = [Decimal(value).quantize(Decimal("1e-50"), rounding=rounding) for value in step]
        centre = [format(Decimal(3) + value, "f") for value in shift]
    return _pose("6", ("3", "3", "0.5"), (centre[0], centre[1], "0.5"))


def test_a_gap_below_the_first_precision_is_decided_by_raising_it() -> None:
    open_pair = intervals.decide(_near_contact(ROUND_CEILING))
    assert open_pair.tried[0] == 50
    assert len(open_pair.tried) > 1
    assert open_pair.verdict == intervals.VERIFIED
    assert open_pair.least_gap.lo >= 0
    assert Fraction(open_pair.least_gap.hi, open_pair.scale) < Fraction(1, 10**49)
    closed_pair = intervals.decide(_near_contact(ROUND_FLOOR))
    assert len(closed_pair.tried) > 1
    assert closed_pair.verdict == intervals.REFUSED
    assert closed_pair.overlapping == ((1, 2),)
    assert intervals.decide(_near_contact(ROUND_CEILING), digits=(50,)).verdict == (
        intervals.UNDECIDED
    )


def test_an_angle_is_read_in_its_declared_unit() -> None:
    """Two squares at 45 degrees stacked on their common diagonal clear each other by
    0.75 * sqrt(2) - 1; read as 0.785 degrees instead, they overlap."""
    diamonds = _pose(
        "3", ("1", "1", "0.7853981633974483"), ("1.75", "1.75", "0.7853981633974483")
    )
    assert intervals.decide(diamonds).verdict == intervals.VERIFIED
    in_degrees = _pose("3", ("1", "1", "45"), ("1.75", "1.75", "45"), unit="degrees")
    assert intervals.decide(in_degrees).verdict == intervals.VERIFIED
    misread = replace(diamonds, unit="degrees")
    assert intervals.decide(misread).verdict == intervals.REFUSED
    with pytest.raises(ValueError, match="unknown angle unit"):
        intervals.cos_sin("1", "gradians", SCALE)


@pytest.mark.parametrize("source", packets.CERTIFIED, ids=lambda source: source.id)
def test_the_retained_poses_rebuild_the_pinned_upstream_files(source: packets.Source) -> None:
    poses = [intervals.read_pose(source.fact(n)) for n in packets.cases(source)]
    for pose in poses:
        assert intervals.rebuilds_upstream(source, *intervals.upstream_bytes(source, pose)), (
            pose.n
        )
    misread = replace(poses[0], unit="degrees")
    assert not intervals.rebuilds_upstream(source, *intervals.upstream_bytes(source, misread))


def test_the_mutated_controls_are_refused_on_the_exact_routes_own_pose() -> None:
    rows = intervals.control_rows(packets.FRANCISCOUZO, 68, 31)
    by_name = {row["control"]: row for row in rows}
    assert all(row["verdict"] == intervals.REFUSED for row in rows)
    assert by_name["side-shrunk-1e-15"]["claimed_side_fits"] == intervals.REFUTED
    assert by_name["square-31-shifted-1e-6"]["first_overlaps"] == [[31, 42], [31, 62]]
    assert by_name["angles-read-as-degrees"]["overlapping_pairs"] > 0


@pytest.mark.parametrize("source", packets.CERTIFIED, ids=lambda source: source.id)
def test_the_control_receipts_are_what_the_controls_decide(source: packets.Source) -> None:
    stored = json.loads(intervals.control_receipt(source).read_text(encoding="utf-8"))
    assert stored == intervals.controls(source)


def _receipt(source: packets.Source) -> dict[int, dict[str, Any]]:
    record = json.loads(intervals.receipt(source).read_text(encoding="utf-8"))
    return {row["n"]: row for row in record["cases"]}


def test_every_case_verifies_and_agrees_with_the_exact_route() -> None:
    trailing = set()
    for source in packets.CERTIFIED:
        rows = _receipt(source)
        exact = packets.certification(source)
        assert set(rows) == set(packets.cases(source))
        for n, row in rows.items():
            assert row["verdict"] == intervals.VERIFIED, n
            assert row["exact_route"] == {**row["exact_route"], "agrees": True}, n
            assert row["units_above_printed"] == exact[n]["units_above_printed"], n
            assert row["printed_side_fits"] == (
                intervals.CERTIFIED if row["units_above_printed"] == 0 else intervals.REFUTED
            ), n
            if isinstance(row["units_above_printed"], int) and row["units_above_printed"] > 1:
                trailing.add(n)
    assert trailing == TRAILING


#: Every case, so the whole interval route replays in the ordinary suite: about 0.1 s each.
CASES = [(source, n) for source in packets.CERTIFIED for n in sorted(packets.cases(source))]


@pytest.mark.parametrize(("source", "n"), CASES, ids=[f"n{n}" for _, n in CASES])
def test_each_case_decided_again_is_its_receipt_row(source: packets.Source, n: int) -> None:
    fresh = intervals.row(source, n)
    stored = _receipt(source)[n]
    fresh.pop("wall_seconds")
    stored.pop("wall_seconds")
    assert fresh == stored


def test_de_winters_reported_clearances_are_what_the_pose_gives() -> None:
    """He reports wall clearance at least 1.000005e-14 at square 65 and pair gap at least
    2.10001e-14 at squares 79 and 81, counting from zero."""
    row = _receipt(packets.DE_WINTER)[211]
    frame, pairs = row["frame"], row["pairs"]
    assert isinstance(frame, dict)
    assert isinstance(pairs, dict)
    assert frame["least_wall_square"] == 66
    assert Fraction(frame["least_wall_clearance"][0]) >= Fraction("1.00000e-14")
    assert pairs["least_gap_squares"] == [80, 82]
    assert pairs["least_gap"] == ["2.10001e-14", "2.10001e-14"]


def test_the_route_shares_no_geometry_with_the_exact_one() -> None:
    """It imports nothing from sqpack but the YAML loader, nothing of either exact
    checker, no mpmath, and from the packet tool only its records and readers."""
    path = Path(intervals.__file__)
    tree = ast.parse(path.read_text(encoding="utf-8"))
    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
            modules.update(f"{node.module}.{alias.name}" for alias in node.names)
    project = {name for name in modules if name.startswith(("sqpack", "devtools", "mpmath"))}
    assert project == {
        "devtools",
        "devtools.upper_bound_packets",
        "sqpack.yamlio",
        "sqpack.yamlio.safe_load",
    }
    used = {
        node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == "packets"
    }
    assert used <= {
        "Source",
        "FRANCISCOUZO",
        "DE_WINTER",
        "CERTIFIED",
        "BY_ID",
        "cases",
        "acquisition",
        "certification",
        "CONTROL_N",
        "CONTROL_SHIFT_SQUARE",
    }
