"""Count bounded cell-occupancy vectors by exact coefficient dynamic programming.

For capacities c_i, coefficient k of product_i(1+x+...+x^c_i) counts integer
vectors (a_i) with 0 <= a_i <= c_i and sum_i a_i = k. Cells are distinct, but
the squares within a cell are not labeled. These counts do not prove that any
occupancy vector has a geometric packing or count placements of labeled squares.
"""

from __future__ import annotations

import argparse
import json
from math import prod
from typing import TypedDict, cast

MAX_CELLS = 64
MAX_CAPACITY = 64
MAX_TARGET = 4096
MAX_INPUT_BYTES = 4096
MAX_OUTPUT_BYTES = 1024 * 1024


class OccupancyCount(TypedDict):
    schema: str
    capacities: list[int]
    target: int
    coefficients_through_target: list[int]
    target_assignments: int
    total_assignments: int
    counted_objects: str


def count_cell_occupancies(capacities: list[int], target: int) -> OccupancyCount:
    """Return exact coefficients through target and both requested assignment counts."""
    if type(capacities) is not list or len(capacities) > MAX_CELLS:
        raise ValueError(f"capacities must be a list of at most {MAX_CELLS} integers")
    if type(target) is not int or not 0 <= target <= MAX_TARGET:
        raise ValueError(f"target must be an integer between 0 and {MAX_TARGET}")
    if any(
        type(capacity) is not int or not 0 <= capacity <= MAX_CAPACITY
        for capacity in capacities
    ):
        raise ValueError(f"each capacity must be an integer between 0 and {MAX_CAPACITY}")

    coefficients = [1] + [0] * target
    for capacity in capacities:
        next_coefficients: list[int] = []
        window = 0
        for degree in range(target + 1):
            window += coefficients[degree]
            if degree > capacity:
                window -= coefficients[degree - capacity - 1]
            next_coefficients.append(window)
        coefficients = next_coefficients
    return {
        "schema": "cell-occupancy-count/v1",
        "capacities": capacities.copy(),
        "target": target,
        "coefficients_through_target": coefficients,
        "target_assignments": coefficients[target],
        "total_assignments": prod(capacity + 1 for capacity in capacities),
        "counted_objects": "integer occupancies of indexed cells; square identities ignored",
    }


def _serialized_count(capacities_argument: str, target_argument: str) -> str:
    if len(capacities_argument.encode("utf-8")) > MAX_INPUT_BYTES:
        raise ValueError(f"capacities input exceeds {MAX_INPUT_BYTES} bytes")
    capacities = cast("list[int]", json.loads(capacities_argument))
    result = count_cell_occupancies(capacities, int(target_argument))
    serialized = json.dumps(result, sort_keys=True, separators=(",", ":"))
    if len(serialized.encode("utf-8")) > MAX_OUTPUT_BYTES:
        raise ValueError(f"result exceeds {MAX_OUTPUT_BYTES} bytes")
    return serialized


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument(
        "--capacities", required=True, help="JSON list of nonnegative cell capacities"
    )
    _ = parser.add_argument("--target", required=True, help="exact occupancy sum to count")
    args = parser.parse_args(argv)
    try:
        serialized = _serialized_count(str(args.capacities), str(args.target))
    except (UnicodeError, json.JSONDecodeError, ValueError, RecursionError) as error:
        print(
            json.dumps(
                {
                    "schema": "cell-occupancy-count/v1",
                    "error": str(error),
                    "count_completed": False,
                },
                sort_keys=True,
            )
        )
        return 2
    else:
        print(serialized)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
