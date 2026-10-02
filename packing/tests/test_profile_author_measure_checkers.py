"""Refusal and parsing controls for the author-checker profile, with no compilation."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

from benchmarks.profile_author_measure_checkers import (
    Direction,
    Family,
    locality_census,
    matches,
    parse_callgrind,
    parse_gprof_flat,
)

GPROF = """\
Flat profile:

Each sample counts as 0.01 seconds.
  %   cumulative   self              self     total
 time   seconds   seconds    calls  ms/call  ms/call  name
 61.20      6.12     6.12 63860000     0.00     0.00  kernel_a(int, double)
 20.00      8.12     2.00                             library_b
 18.80     10.00     1.88                             main
"""

CALLGRIND = """\
--------------------------------------------------------------------------------
Ir
--------------------------------------------------------------------------------
1,000,000 (100.0%)  PROGRAM TOTALS

--------------------------------------------------------------------------------
Ir                file:function
--------------------------------------------------------------------------------
600,000 (60.00%)  /w/prog.cpp:kernel_a(int, double) [/w/checker]
250,000 (25.00%)  ./math/s_lib.c:library_b [/usr/lib/x86_64-linux-gnu/libm.so.6]
"""


def test_gprof_rows_keep_calls_and_uncounted_library_functions() -> None:
    rows = parse_gprof_flat(GPROF)
    assert [row["function"] for row in rows] == [
        "kernel_a(int, double)",
        "library_b",
        "main",
    ]
    assert rows[0]["calls"] == 63860000
    assert rows[1]["calls"] is None
    assert rows[1]["self_seconds"] == 2.0


def test_callgrind_total_and_function_names_without_paths() -> None:
    total, rows = parse_callgrind(CALLGRIND)
    assert total == 1_000_000
    assert rows[0] == {
        "function": "kernel_a(int, double)",
        "instructions": 600_000,
        "percent": 60.0,
    }
    assert rows[1]["function"] == "library_b"


def test_callgrind_without_a_program_total_is_refused() -> None:
    try:
        parse_callgrind("600,000 (60.00%)  f.c:g [b]\n")
    except ValueError:
        return
    raise AssertionError("an annotation with no program total was accepted")


def test_a_complete_run_must_reproduce_every_recorded_field() -> None:
    recorded = {"status": "verified", "nodes": 10, "leaves": 6, "lower_bound": 1.0001}
    direction = Direction(30, recorded)
    observed = {"status": "verified", "nodes": 10, "leaves": 6, "lower": 1.0001}
    assert matches(direction, observed) is True
    assert matches(direction, observed | {"nodes": 11}) is False
    assert matches(direction, observed | {"leaves": 5}) is False
    assert matches(direction, observed | {"lower": 1.00011}) is False
    assert matches(direction, observed | {"status": "unresolved"}) is False


def test_an_open_frontier_is_not_a_match_even_with_the_recorded_nodes() -> None:
    direction = Direction(3, {"nodes": 5, "lower": 1.0}, node_limit=5)
    observed = {"status": "ANGLE_VERIFIED", "nodes": 5, "lower": 1.0, "frontier_boxes": 0}
    assert matches(direction, observed) is True
    assert matches(direction, observed | {"frontier_boxes": 2}) is False
    assert matches(direction, observed | {"status": "ANGLE_UNRESOLVED"}) is False


def test_a_bounded_prefix_claims_no_match() -> None:
    direction = Direction(0, {"nodes": 2_072_307}, node_limit=100, complete=False)
    assert matches(direction, {"status": "ANGLE_UNRESOLVED", "nodes": 100}) is None


def _family(pieces: list[tuple[str, tuple[float, ...]]]) -> Family:
    def unused(*_args: object) -> dict[str, object]:
        raise AssertionError

    return Family(
        name="toy",
        certificate="toy",
        source=Path("toy.cpp"),
        source_sha256="",
        pieces=pieces,
        side=Fraction(4),
        core=Fraction(1, 2),
        directions=[],
        prepare=unused,
        argv=lambda _binary, _direction: [],
        observe=unused,
        domain_half_width=lambda _index: Fraction(1),
        attribution_nodes=None,
        callgrind_nodes=None,
    )


def test_locality_census_separates_inside_straddling_and_distant_pieces() -> None:
    # Axis direction, one centre per cell of a 1 x 1 grid: the centre is (2.5, 2.5).
    pieces = [
        ("point", (2.5, 2.5)),  # at the centre: inside every core of a small box
        ("point", (2.75, 2.5)),  # on the core's edge: straddling
        ("rectangle", (0.0, 0.0, 0.5, 0.5)),  # far away
        ("segment", (2.5, 2.0, 2.5, 3.0)),  # crosses the core: straddling
    ]
    census = locality_census(_family(pieces), 0, scales=(9,), grid=1)
    counts = census["half_width_E_over_2^9"]
    assert census["pieces"] == 4
    assert counts["inside"]["max"] == 1
    assert counts["straddling"]["max"] == 2
    assert counts["near"]["max"] == 3
