"""Synthetic controls for the independent H256 receipt audit; no target files read."""

from __future__ import annotations

import copy
import itertools
from fractions import Fraction
from typing import Any

import pytest

from devtools import audit_n17_endpoint_receipt as audit


def test_interval_arithmetic_and_outside_domain_reconstruction() -> None:
    assert audit.multiply((Fraction(-2), Fraction(3)), (Fraction(-4), Fraction(5))) == (
        Fraction(-12),
        Fraction(15),
    )
    assert audit.divide((Fraction(1), Fraction(2)), (Fraction(-4), Fraction(-2))) == (
        Fraction(-1),
        Fraction(-1, 4),
    )
    assert audit.absolute((Fraction(-2), Fraction(3))) == (Fraction(0), Fraction(3))
    assert audit.absolute((Fraction(-4), Fraction(-2))) == (Fraction(2), Fraction(4))
    with pytest.raises(audit.AuditError, match="contains zero"):
        audit.divide(audit.point(1), (Fraction(-1), Fraction(1)))
    # This hand-computable point lies outside the H254 target chart.
    layout = audit.reconstruct(audit.point(Fraction(1, 2)), audit.point(Fraction(1, 4)))
    assert layout.side == audit.point(Fraction(32, 7))
    assert layout.axes["u"] == (audit.point(Fraction(3, 5)), audit.point(Fraction(4, 5)))
    assert layout.axes["p"] == (audit.point(Fraction(15, 17)), audit.point(Fraction(-8, 17)))
    assert set(layout.centres) == set(range(1, 18))
    for first, second in (("u", "v"), ("p", "q")):
        assert audit.dot(layout.axes[first], layout.axes[first]) == audit.point(1)
        assert audit.dot(layout.axes[first], layout.axes[second]) == audit.point(0)
    assert layout.wall_gap(1, "left") == audit.point(0)
    assert layout.pair_gap(1, 2, "ex", "forward") == audit.point(0)


def test_bounded_chunk_parser_and_canonical_refusal() -> None:
    value = "1" + "0" * 5000 + "/3"
    assert audit.rational(value) == Fraction(10**5000, 3)
    for invalid in ("-0", "2/4", "1/1", "01", "1/0", "0/3", True, 0):
        with pytest.raises(audit.AuditError):
            audit.rational(invalid)
    with pytest.raises(audit.AuditError):
        audit.rational("1" * (2 * audit.MAX_DIGITS + 3))
    with pytest.raises(audit.AuditError, match="reversed"):
        audit.read_interval(["1", "0"])


@pytest.mark.parametrize("raw", [b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":1234567890123}'])
def test_json_refuses_ambiguous_or_unbounded_numbers(raw: bytes) -> None:
    with pytest.raises(audit.AuditError):
        audit.decode(raw)


class SyntheticLayout(audit.Layout):
    """An algebra-free control oracle; it cannot establish any H255/H256 theorem."""

    def wall_gap(self, label: int, wall: str) -> audit.Interval:
        assert label in range(1, 18)
        assert wall in ("left", "right", "bottom", "top")
        return audit.point(1)

    def pair_gap(self, left: int, right: int, axis: str, direction: str) -> audit.Interval:
        assert 1 <= left < right <= 17
        assert axis in ("ex", "ey", "u", "v", "p", "q")
        assert direction in ("forward", "reverse")
        return audit.point(1)


def synthetic_records() -> dict[str, Any]:
    manifest = audit.identity_manifest()
    walls = []
    for label, wall in itertools.product(range(1, 18), ("left", "right", "bottom", "top")):
        identity = (label, wall) in audit.ANCHORS
        walls.append(
            {
                "label": label,
                "wall": wall,
                "kind": "identity" if identity else "strict",
                "bound": ["0", "0"] if identity else ["1", "1"],
                "bound_scope": "certified_root" if identity else "whole_box",
                "passed": True,
            }
        )
    pairs = []
    for left, right in itertools.combinations(range(1, 18), 2):
        identity = (left, right) in manifest
        row: dict[str, Any] = {
            "left": left,
            "right": right,
            "kind": "identity" if identity else "strict",
            "bound": ["0", "0"] if identity else ["1", "1"],
            "bound_scope": "certified_root" if identity else "whole_box",
            "passed": True,
        }
        if identity:
            row["identity"] = copy.deepcopy(manifest[(left, right)])
        else:
            row.update(axis="ex", direction="forward")
        pairs.append(row)
    return {"walls": walls, "pairs": pairs, "counts": dict(audit.COUNTS)}


def test_complete_obligations_and_mutation_controls() -> None:
    layout = SyntheticLayout({}, {}, {}, {}, audit.point(1))
    original = synthetic_records()
    audit.audit_obligations(original, layout)
    # Each independent mutation targets a distinct coverage/scope/arithmetic guard.
    for mutation in (
        "duplicate_pair",
        "missing_wall",
        "wall_endpoint",
        "pair_endpoint",
        "scope",
        "identity_direction",
        "failed",
        "kind",
    ):
        altered = copy.deepcopy(original)
        strict_wall = next(row for row in altered["walls"] if row["kind"] == "strict")
        strict_pair = next(row for row in altered["pairs"] if row["kind"] == "strict")
        corner = next(row for row in altered["pairs"] if (row["left"], row["right"]) == (2, 3))
        if mutation == "duplicate_pair":
            altered["pairs"][-1] = altered["pairs"][0]
        elif mutation == "missing_wall":
            altered["walls"].pop()
        elif mutation == "wall_endpoint":
            strict_wall["bound"] = ["1", "2"]
        elif mutation == "pair_endpoint":
            strict_pair["bound"] = ["1/2", "1"]
        elif mutation == "scope":
            strict_pair["bound_scope"] = "certified_root"
        elif mutation == "identity_direction":
            corner["identity"]["axes"][0]["from"] = 2
        elif mutation == "failed":
            strict_wall["passed"] = False
        else:
            strict_pair["kind"] = "identity"
        with pytest.raises(audit.AuditError):
            audit.audit_obligations(altered, layout)


def test_exact_endpoint_and_positivity_requirements() -> None:
    audit.match((Fraction(1, 3), Fraction(2, 3)), ["1/3", "2/3"], "control", positive=True)
    with pytest.raises(audit.AuditError, match="differs"):
        audit.match((Fraction(1, 3), Fraction(2, 3)), ["1/3", "3/4"], "control", positive=True)
    with pytest.raises(audit.AuditError, match="nonpositive"):
        audit.match((Fraction(0), Fraction(1)), ["0", "1"], "control", positive=True)
    assert audit.exact_structure({"a": [1, True]}, {"a": [1, True]})
    assert not audit.exact_structure({"a": [1, True]}, {"a": [1.0, True]})
    assert not audit.exact_structure({"a": [1, True]}, {"a": [True, True]})


def test_side_comparison_and_directed_decimal_enclosure() -> None:
    report = audit.side_summary((Fraction(1, 3), Fraction(2, 3)))
    lo, hi = map(Fraction, report["outward_decimal_enclosure"])
    assert lo <= Fraction(1, 3)
    assert hi >= Fraction(2, 3)
    assert report["exact_upper_strictly_below_retained_rational_upper"] is True
    cap = Fraction(4675530093604551, 10**15)
    report = audit.side_summary((cap, cap))
    assert report["exact_upper_at_most_retained_rational_upper"] is True
    assert report["exact_upper_strictly_below_retained_rational_upper"] is False
