"""Independently audit counts of occupancy vectors for capacities zero, one and two.

This uses an exact closed binomial sum and imports no dynamic-programming producer.
It verifies the finite integer census only. The validity of geometric cell capacities,
complete coverage and any comparison with another cover remain separate premises.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from math import comb
from pathlib import Path
from typing import cast

MAX_CELLS = 64
MAX_TARGET = 4096
MAX_BYTES = 1024 * 1024
MAX_INTEGER_DIGITS = 128
SOURCE_SCHEMA = "cell-occupancy-count/v1"
AUDIT_SCHEMA = "cell-occupancy-audit/v1"
COUNTED_OBJECTS = "integer occupancies of indexed cells; square identities ignored"
KEYS = {
    "schema",
    "capacities",
    "target",
    "coefficients_through_target",
    "target_assignments",
    "total_assignments",
    "counted_objects",
}


def plain_integer(value: object, label: str, maximum: int) -> int:
    """Accept JSON integers, excluding booleans and integers outside a fixed budget."""
    if type(value) is not int or not 0 <= value <= maximum:
        raise ValueError(f"{label} must be an integer in [0, {maximum}]")
    return value


def binomial(n: int, k: int) -> int:
    """The combinatorial zero convention outside a binomial coefficient's support."""
    return comb(n, k) if 0 <= k <= n else 0


def coefficient(ones: int, twos: int, target: int) -> int:
    """Choose doubled cells, then singly occupied cells from those remaining.

    For exactly k doubled cells, choose them from the twos, then choose target-2k
    singleton cells from ones+twos-k available cells. The cases are disjoint and
    exhaust every vector. Capacity-zero cells each contribute exactly one choice.
    """
    if min(ones, twos, target) < 0:
        raise ValueError("coefficient arguments must be nonnegative")
    if target > ones + 2 * twos:
        return 0
    return sum(
        comb(twos, doubled) * binomial(ones + twos - doubled, target - 2 * doubled)
        for doubled in range(min(twos, target // 2) + 1)
    )


def audit_payload(payload: object) -> dict[str, object]:
    """Recompute every supplied count without using producer arithmetic."""
    if not isinstance(payload, dict):
        raise TypeError("receipt must be a JSON object")
    receipt = cast(dict[str, object], payload)
    if set(receipt) != KEYS:
        raise ValueError("receipt fields differ from the fixed source schema")
    if receipt["schema"] != SOURCE_SCHEMA:
        raise ValueError("unsupported receipt schema")
    if receipt["counted_objects"] != COUNTED_OBJECTS:
        raise ValueError("counted objects differ from the declared occupancy vectors")
    raw_capacities = receipt["capacities"]
    if not isinstance(raw_capacities, list):
        raise TypeError("capacities must be a JSON list")
    capacity_values = cast(list[object], raw_capacities)
    if len(capacity_values) > MAX_CELLS:
        raise ValueError("too many cells")
    capacities = [plain_integer(value, "capacity", 2) for value in capacity_values]
    target = plain_integer(receipt["target"], "target", MAX_TARGET)
    raw_coefficients = receipt["coefficients_through_target"]
    if not isinstance(raw_coefficients, list):
        raise TypeError("coefficients must be a JSON list")
    coefficient_values = cast(list[object], raw_coefficients)
    if len(coefficient_values) != target + 1:
        raise ValueError("coefficient prefix must have target+1 entries")
    ones, twos = capacities.count(1), capacities.count(2)
    total = 2**ones * 3**twos
    reported = [plain_integer(value, "coefficient", total) for value in coefficient_values]
    expected = [coefficient(ones, twos, degree) for degree in range(target + 1)]
    if reported != expected:
        raise ValueError("coefficient prefix differs from independent binomial counts")
    if (
        plain_integer(receipt["target_assignments"], "target_assignments", total)
        != expected[-1]
    ):
        raise ValueError("target count differs from independent binomial count")
    if plain_integer(receipt["total_assignments"], "total_assignments", 3**MAX_CELLS) != total:
        raise ValueError("total count differs from the product of cell choices")
    return {
        "schema": AUDIT_SCHEMA,
        "audit_passed": True,
        "method": "closed-binomial-sum",
        "producer_imported": False,
        "capacities": capacities,
        "target": target,
        "coefficients_checked": len(expected),
        "recomputed_coefficients_through_target": expected,
        "target_assignments": expected[-1],
        "total_assignments": total,
        "counted_objects": COUNTED_OBJECTS,
        "scope": "integer occupancy census only; no geometric feasibility or capacity proof",
    }


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON field: {key}")
        result[key] = value
    return result


def bounded_integer(token: str) -> int:
    if len(token.lstrip("-")) > MAX_INTEGER_DIGITS:
        raise ValueError("JSON integer exceeds the parser budget")
    return int(token)


def refuse_noninteger(token: str) -> object:
    raise ValueError(f"noninteger JSON number is unsupported: {token[:32]}")


def decode(raw: bytes) -> object:
    if len(raw) > MAX_BYTES:
        raise ValueError("receipt exceeds the byte budget")
    return json.loads(
        raw,
        object_pairs_hook=unique_object,
        parse_int=bounded_integer,
        parse_float=refuse_noninteger,
        parse_constant=refuse_noninteger,
    )


def audit(path: Path) -> dict[str, object]:
    with path.open("rb") as source:
        raw = source.read(MAX_BYTES + 1)
    result = audit_payload(decode(raw))
    result["receipt_bytes"] = len(raw)
    result["receipt_sha256"] = hashlib.sha256(raw).hexdigest()
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args(argv)
    try:
        result = audit(args.receipt)
    except (ValueError, OSError, TypeError, RecursionError) as error:
        print(json.dumps({"schema": AUDIT_SCHEMA, "audit_passed": False, "error": str(error)}))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
