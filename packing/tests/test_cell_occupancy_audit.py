"""Target-free controls for the independent closed-binomial occupancy audit."""

from __future__ import annotations

from copy import deepcopy

import pytest

from devtools import audit_cell_occupancies as audit


def packet(capacities: list[int], coefficients: list[int], total: int) -> dict[str, object]:
    return {
        "schema": audit.SOURCE_SCHEMA,
        "capacities": capacities,
        "target": len(coefficients) - 1,
        "coefficients_through_target": coefficients,
        "target_assignments": coefficients[-1],
        "total_assignments": total,
        "counted_objects": audit.COUNTED_OBJECTS,
    }


@pytest.mark.parametrize(
    ("capacities", "coefficients", "total"),
    [
        ([], [1], 1),
        ([0, 0], [1, 0, 0], 1),
        ([0, 1, 2], [1, 2, 2, 1], 6),
        ([2, 2], [1, 2, 3, 2, 1, 0], 9),
        ([2, 2, 2], [1, 3, 6, 7, 6, 3, 1], 27),
        ([1] * 8, [1, 8, 28, 56, 70, 56, 28, 8, 1, 0], 256),
    ],
)
def test_hand_derived_counts(
    capacities: list[int], coefficients: list[int], total: int
) -> None:
    result = audit.audit_payload(packet(capacities, coefficients, total))
    assert result["audit_passed"] is True
    assert result["producer_imported"] is False
    assert result["recomputed_coefficients_through_target"] == coefficients
    assert result["total_assignments"] == total


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("schema", "unknown"),
        ("capacities", [1, 3]),
        ("capacities", [True, 2]),
        ("capacities", [-1, 2]),
        ("capacities", "1,2"),
        ("capacities", [0] * 65),
        ("target", True),
        ("target", 1.0),
        ("target", -1),
        ("target", 4097),
        ("coefficients_through_target", [1, 2, 1, 1]),
        ("coefficients_through_target", [1, 2, 2]),
        ("coefficients_through_target", [True, 2, 2, 1]),
        ("target_assignments", 2),
        ("target_assignments", True),
        ("total_assignments", 7),
        ("total_assignments", 6.0),
        ("counted_objects", "geometrically feasible packings"),
    ],
)
def test_reject_mutated_fields(field: str, value: object) -> None:
    receipt = deepcopy(packet([1, 2], [1, 2, 2, 1], 6))
    receipt[field] = value
    with pytest.raises(
        (ValueError, TypeError),
        match=r"schema|capacity|capacities|cells|target|coefficient|total|occupancy",
    ):
        audit.audit_payload(receipt)


def test_schema_requires_complete_exact_fields() -> None:
    receipt = packet([1], [1, 1], 2)
    receipt["unexpected"] = 0
    with pytest.raises(ValueError, match="fields"):
        audit.audit_payload(receipt)
    del receipt["unexpected"]
    del receipt["target"]
    with pytest.raises(ValueError, match="fields"):
        audit.audit_payload(receipt)
    with pytest.raises(TypeError, match="object"):
        audit.audit_payload([])


@pytest.mark.parametrize(
    "raw",
    [
        b'{"x":1,"x":2}',
        b'{"x":1.0}',
        b'{"x":NaN}',
        b'{"x":Infinity}',
        b'{"x":' + b"9" * 129 + b"}",
        b" " * (audit.MAX_BYTES + 1),
    ],
)
def test_bounded_parser_refusals(raw: bytes) -> None:
    with pytest.raises(ValueError, match=r"duplicate|noninteger|budget"):
        audit.decode(raw)


def test_binomial_support_and_empty_choice() -> None:
    assert audit.binomial(2, -1) == audit.binomial(2, 3) == 0
    assert audit.coefficient(0, 0, 0) == 1
    assert audit.coefficient(0, 0, 1) == 0
    with pytest.raises(ValueError, match="nonnegative"):
        audit.coefficient(0, 0, -1)
