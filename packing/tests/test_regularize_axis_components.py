"""The regularizer on fixtures small enough to be checked by hand.

Three synthetic witnesses, each built so the exact answer is known before the tool runs:
a row with slack that compacts into the wall and each other, a block one part in ten to
the thirteenth off its lattice that snaps onto it, and a square whose slide would run
into a tilted neighbour and so must stop short and be refused.  A fourth case holds the
tool to its boundary: it never writes under `witnesses/` or `atlas/`.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools.regularize_axis_components import (
    ATLAS_GAP,
    ROOT,
    SNAP_TOLERANCE,
    WITNESS_SCHEMA,
    atlas_contacts,
    axis_square,
    centre,
    interior_overlap_interval,
    lattice_target,
    main,
    regularize,
    slide_limit,
)
from sqpack.witness import exact_verify, load_witness, witness_document

HALF = Fraction(1, 2)


def decimal_witness(
    squares: list[tuple[str, str, str]], side: str, *, name: str = "fixture"
) -> dict[str, Any]:
    """A decimal centre-angle Witness/v2 record, the kind every Couzo witness is."""
    return {
        "id": f"W-{name}",
        "n": len(squares),
        "side": side,
        "square_size": "1",
        "representation": "center-angle",
        "scalar": {"kind": "decimal"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "radians",
        },
        "squares": [
            {"id": index, "center": [x, y], "angle": angle}
            for index, (x, y, angle) in enumerate(squares, start=1)
        ],
        "claim": {
            "coordinate_provenance": "numerically-checked",
            "method": "numerical-f64",
            "precision": {"binary_bits": 53, "rounding": "nearest-even"},
            "tolerance": "1e-9",
            "limitations": "synthetic fixture",
        },
        "source": {"path": "tests/synthetic"},
    }


def write_witness(path: Path, witness: dict[str, Any]) -> Path:
    path.write_text(witness_document(witness, schema=str(WITNESS_SCHEMA)), encoding="utf-8")
    return path


# A square pinned in a container's top-right corner, so the exact frame's side is exactly
# the declared one and the right-wall lattice sits at side - 1/2, not a hair below it.
PIN_3 = ("2.5", "2.5", "0")
PIN_4 = ("3.5", "3.5", "0")


def test_a_row_with_slack_compacts_into_the_wall_and_each_other() -> None:
    """Three squares drift 0.03, 0.06 and 0.09 right of their slots; all three come home."""
    witness = decimal_witness(
        [("0.53", "0.5", "0"), ("1.56", "0.5", "0"), ("2.59", "0.5", "0"), PIN_4], "4"
    )
    report, view = regularize(witness, source_path="tests/synthetic")

    centres = [
        centre([(Fraction(x), Fraction(y)) for x, y in s["corners"]]) for s in view["squares"]
    ]
    assert centres[:3] == [(HALF, HALF), (Fraction(3, 2), HALF), (Fraction(5, 2), HALF)]
    assert view["side"] == "4"
    assert report["exact_verification"]["repository_verifier"]["valid"] is True
    # Before: only the bottom wall counts for each (0.03 is three gaps).  After: the
    # first touches the left wall, the bottom and its neighbour; the last has a hole on
    # its right, half a side short of the far wall's lattice.
    assert report["atlas_contacts"]["histogram_before"][1] == 3
    assert [s["contacts_after"] for s in report["squares"][:3]] == [3, 3, 2]
    assert report["squares"][2]["light_faces"] == {"right": "hole"}
    assert report["regularization"]["moves"]["compactions"] == 3
    assert report["regularization"]["moves"]["converged"] is True
    assert report["regularization"]["exact_contacts_after"] == 2
    assert view["certificate"]["kind"] == "regularized-view"
    assert "regularized" in view["claim"]["limitations"]


def test_a_block_off_its_lattice_by_a_hair_snaps_onto_it_exactly() -> None:
    """A 2-by-2 block a few 1e-13 off the lattice lands on it, by snaps only.

    The residuals leave 2e-13 between neighbours, room for the 1e-15 tilts: two squares
    whose centres are exactly a side apart cannot both be tilted, and the exact frame
    would refuse such a fixture rather than dilate it.
    """
    witness = decimal_witness(
        [
            ("0.5000000000001", "0.5", "1e-15"),
            ("1.5000000000003", "0.5", "-2e-15"),
            ("0.5000000000001", "1.5000000000002", "0"),
            ("1.5000000000003", "1.5000000000002", "3e-16"),
            PIN_3,
        ],
        "3",
    )
    report, view = regularize(witness, source_path="tests/synthetic")

    centres = [
        centre([(Fraction(x), Fraction(y)) for x, y in s["corners"]]) for s in view["squares"]
    ]
    assert centres[:4] == [
        (HALF, HALF),
        (Fraction(3, 2), HALF),
        (HALF, Fraction(3, 2)),
        (Fraction(3, 2), Fraction(3, 2)),
    ]
    moves = report["regularization"]["moves"]
    assert moves["compactions"] == 0
    assert moves["snaps"] == 4
    assert Fraction(moves["largest_move"]) <= SNAP_TOLERANCE
    assert report["regularization"]["statuses"] == {"exact-axis": 5}
    # Every square of the block was already dark under the atlas rule and stays so: a snap
    # changes the representation, not the drawing.
    assert [s["contacts_before"] for s in report["squares"][:4]] == [4, 4, 4, 4]
    assert [s["contacts_after"] for s in report["squares"][:4]] == [4, 4, 4, 4]
    assert report["regularization"]["exact_contacts_after"] == 4
    assert report["exact_verification"]["repository_verifier"]["touching_pairs"] == 4


def test_a_slide_into_a_tilted_square_stops_short_and_is_refused() -> None:
    """The tilted diamond's lower corner dips 0.02 into the lane the square would sweep."""
    # The diamond at 45 degrees has its lowest corner at (1, 0.98): at height 1 it spans
    # x in [0.98, 1.02], so the square at 1.53 may slide only 0.01 before touching it.
    diamond_y = str(Fraction("0.98") + Fraction("0.70710678118654752440084436210484904"))
    witness = decimal_witness(
        [
            ("0.5", "0.5", "0"),
            ("1.53", "0.5", "0"),
            ("1.0", diamond_y, "0.78539816339744830962"),
            PIN,
        ],
        "3",
    )
    report, view = regularize(witness, source_path="tests/synthetic")

    moved = report["squares"][1]
    assert moved["moves"] == []
    (refused,) = moved["rejected_moves"]
    assert refused["blockers"] == ["square:3"]
    assert refused["reached_target"] is False
    assert Fraction(refused["distance"]) < Fraction("0.0100001")
    assert Fraction(refused["distance"]) > Fraction("0.0099999")
    assert refused["contacts_before"] == refused["contacts_after"] == 1
    assert moved["light_faces"] == {
        "left": "tilted-neighbour",
        "right": "hole",
        "top": "tilted-neighbour",
    }
    centres = [
        centre([(Fraction(x), Fraction(y)) for x, y in s["corners"]]) for s in view["squares"]
    ]
    assert centres[1] == (Fraction("1.53"), HALF)
    assert report["exact_verification"]["repository_verifier"]["valid"] is True


def test_exact_slide_limits_on_rational_corners() -> None:
    """The collision time is exact: a touching neighbour is a zero-gap stop, not an overlap."""
    moving = axis_square((Fraction(3, 2) + Fraction(3, 100), HALF))
    neighbour = axis_square((HALF, HALF))
    far = axis_square((HALF, Fraction(5, 2)))
    limit, blockers = slide_limit(
        moving, (-1, 0), Fraction(3, 100), [("1", neighbour), ("far", far)], Fraction(3)
    )
    assert limit == Fraction(3, 100)
    assert [(b.kind, b.name) for b in blockers] == [("target", ""), ("square", "1")]
    # Touching from below along the whole slide is not an overlap at any distance.
    below = axis_square((Fraction(3, 2), Fraction(-1, 2)))
    assert interior_overlap_interval(moving, (-1, 0), below) is None
    # The wall stops a slide that asks for more room than there is.
    limit, blockers = slide_limit(neighbour, (-1, 0), Fraction(1), [], Fraction(3))
    assert limit == 0
    assert [(b.kind, b.name) for b in blockers] == [("wall", "x=0")]


def test_lattice_targets_seat_from_the_nearer_wall() -> None:
    side = Fraction("10.607174680178947")
    assert lattice_target(Fraction("0.5298"), side) == HALF
    assert lattice_target(Fraction("8.1061"), side) == side - HALF - 2
    assert lattice_target(Fraction("6.722"), side) == Fraction(13, 2)
    assert lattice_target(Fraction(1), Fraction(3)) == HALF


def test_the_atlas_rule_counts_as_the_workbench_does() -> None:
    poses = [(0.5, 0.5, 0.0), (1.5, 0.5, 0.0), (0.5, 1.5, 0.0), (1.5, 1.5, 1e-9)]
    assert atlas_contacts(poses, 2.0) == [4, 4, 4, 4]
    slack = [(0.5, 0.5, 0.0), (1.5 + 2 * ATLAS_GAP, 0.5, 0.0), (1.0, 1.5, 0.8)]
    assert atlas_contacts(slack, 2.0) == [2, 1, 0]


def test_the_command_writes_a_verifiable_view_only_where_it_is_told(tmp_path: Path) -> None:
    witness = decimal_witness(
        [("0.53", "0.5", "0"), ("1.56", "0.5", "0"), PIN], "3", name="cli"
    )
    source = write_witness(tmp_path / "cli.yaml", witness)
    output = tmp_path / "out"

    assert main([str(source), "--output-dir", str(output)]) == 0
    report = json.loads((output / "cli-regularized.json").read_text())
    assert report["exact_verification"]["passed"] is True
    assert report["exact_verification"]["independent_checker"]["verification_passed"] is True
    view = load_witness(output / "cli-regularized.yaml", fallback_schema=WITNESS_SCHEMA)
    result, verdict = exact_verify(view)
    assert verdict.valid is True
    assert result["coordinate_provenance"] == "verified"
    assert view["certificate"]["derived_from"] == "W-cli"

    assert main([str(source), "--output-dir", str(ROOT / "witnesses" / "nowhere")]) == 2
    assert main([str(source), "--output-dir", str(ROOT / "atlas")]) == 2
    assert not (ROOT / "witnesses" / "nowhere").exists()
