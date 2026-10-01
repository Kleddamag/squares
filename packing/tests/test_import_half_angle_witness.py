"""Black-box controls for importing exact half-angle packing sources."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import import_half_angle_witness as importer
from devtools.check_rational_witness_independent import check as independent_check
from devtools.validate_schemas import check as schema_check
from sqpack.witness import load_witness


def _source(path: Path, squares: Sequence[Mapping[str, object]], side: object = "2") -> Path:
    path.write_text(json.dumps({"side": side, "squares": squares}), encoding="utf-8")
    return path


def _args(source: Path, output: Path, *, n: int = 1, side: str = "2") -> list[str]:
    return [
        str(source),
        "--expected-n",
        str(n),
        "--expected-side",
        side,
        "--output",
        str(output),
    ]


def test_rotated_half_angle_yields_exact_cyclic_witness(tmp_path: Path) -> None:
    source = _source(tmp_path / "source.json", [{"x": "1", "y": "1", "t": "1/2"}])
    output = tmp_path / "witness.yaml"

    assert importer.main(_args(source, output)) == 0
    witness = load_witness(output)
    assert schema_check(output) == []
    assert witness["squares"][0]["corners"] == [
        ["11/10", "3/10"],
        ["17/10", "11/10"],
        ["9/10", "17/10"],
        ["3/10", "9/10"],
    ]
    raw_corners = witness["squares"][0]["corners"]
    corners = [tuple(Fraction(value) for value in point) for point in raw_corners]
    first, second, opposite, fourth = corners
    center = ((first[0] + opposite[0]) / 2, (first[1] + opposite[1]) / 2)
    u = (second[0] - first[0], second[1] - first[1])
    v = (fourth[0] - first[0], fourth[1] - first[1])
    assert center == (1, 1)
    assert u == (Fraction(3, 5), Fraction(4, 5))
    assert v == (Fraction(-4, 5), Fraction(3, 5))
    assert u[1] / (1 + u[0]) == Fraction(1, 2)
    assert Fraction(witness["side"]) == 2
    checked = independent_check(output)
    assert checked["verification_passed"] is True
    assert checked["minimum_containment_clearance"] == "3/10"


@pytest.mark.parametrize(
    ("squares", "source_side", "expected_n", "expected_side"),
    [
        ([{"x": "1", "y": "1", "t": "0"}], "2", 2, "2"),
        ([{"x": "1", "y": "1", "t": "0"}], "3", 1, "2"),
        ([{"x": 1.0, "y": "1", "t": "0"}], "2", 1, "2"),
        ([{"x": "1", "y": "1", "t": "NaN"}], "2", 1, "2"),
        ([{"x": "1", "y": "1", "t": "0"}], 2.0, 1, "2"),
    ],
)
def test_malformed_source_refuses_without_output(
    tmp_path: Path,
    squares: list[dict[str, object]],
    source_side: object,
    expected_n: int,
    expected_side: str,
) -> None:
    source = _source(tmp_path / "source.json", squares, source_side)
    output = tmp_path / "witness.yaml"

    assert importer.main(_args(source, output, n=expected_n, side=expected_side)) == 2
    assert not output.exists()


def test_overlapping_squares_refuse_without_output(tmp_path: Path) -> None:
    squares = [
        {"x": "1", "y": "1", "t": "0"},
        {"x": "1", "y": "1", "t": "0"},
    ]
    source = _source(tmp_path / "source.json", squares)
    output = tmp_path / "witness.yaml"

    assert importer.main(_args(source, output, n=2)) == 2
    assert not output.exists()


def test_independent_corner_guard_refuses_noncyclic_adapter_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = _source(tmp_path / "source.json", [{"x": "1", "y": "1", "t": "1/2"}])
    output = tmp_path / "witness.yaml"

    def noncyclic(x: Fraction, y: Fraction, t: Fraction) -> list[tuple[Fraction, Fraction]]:
        assert (x, y, t) == (1, 1, Fraction(1, 2))
        return [
            (Fraction(11, 10), Fraction(3, 10)),
            (Fraction(9, 10), Fraction(17, 10)),
            (Fraction(17, 10), Fraction(11, 10)),
            (Fraction(3, 10), Fraction(9, 10)),
        ]

    monkeypatch.setattr(importer, "_corners", noncyclic)
    assert importer.main(_args(source, output)) == 2
    assert not output.exists()
