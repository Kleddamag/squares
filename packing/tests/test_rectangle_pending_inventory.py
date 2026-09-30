"""Fail-closed controls for the three diagnostic pending-inventory consumers."""

from __future__ import annotations

from fractions import Fraction

import pytest

from devtools import rectangle_pending_inventory as inventory
from sqpack import rectangle_density as density


def _candidate() -> density.RectangleDensityCandidate:
    return density.RectangleDensityCandidate(
        11, Fraction(381, 100), Fraction(1), Fraction(1), None, Fraction(1), ()
    )


def _box() -> dict[str, object]:
    return density.PendingBox(
        1, Fraction(2), Fraction(2), Fraction(2), Fraction(2), 4, "node_limit"
    ).as_dict()


def _admit(boxes: object, *, count: object = 1) -> tuple[density.PendingBox, ...]:
    return inventory.admit_pending_boxes(
        boxes,
        unresolved_leaves=count,
        candidate=_candidate(),
        angle=1,
        max_depth=48,
    )


def test_exact_object_and_serialized_census_match() -> None:
    box = _box()
    parsed = _admit([box])
    assert parsed == _admit((parsed[0],))
    assert parsed[0].as_dict() == box


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("angle", True, "metadata"),
        ("depth", True, "metadata"),
        ("left", "1/0", "not a rational"),
        ("left", {}, "rational string"),
        ("right", "99", "outside the exact reduced root"),
        ("left", "2/1", "exact serialization"),
    ],
)
def test_malformed_box_refuses(field: str, value: object, message: str) -> None:
    box = _box()
    box[field] = value
    with pytest.raises(density.CandidateError, match=message):
        _admit([box])


def test_missing_and_duplicate_geometry_refuse() -> None:
    with pytest.raises(density.CandidateError, match="inventory is incomplete"):
        _admit([])
    with pytest.raises(density.CandidateError, match="inventory is incomplete"):
        _admit([_box()], count=True)
    duplicate = {**_box(), "depth": 5}
    with pytest.raises(density.CandidateError, match="duplicate pending box"):
        _admit([_box(), duplicate], count=2)
