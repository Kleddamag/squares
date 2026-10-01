"""Count bounded grid occupancies up to D4 using exact cycle polynomials.

Cells are indexed in row-major order and distinguishable before quotienting.
Squares within a cell are unlabeled. This counts occupancy states, not geometric
packings. A symmetry must preserve every cell capacity or the input is refused.
"""

from __future__ import annotations

import argparse
import json
from typing import TypedDict, cast

MAX_GRID_SIZE = 8
MAX_CAPACITY = 2
MAX_TARGET = 128
MAX_INPUT_BYTES = 4096


class ActionCount(TypedDict):
    name: str
    cycle_profile: list[list[int]]
    fixed_assignments: int


class SymmetryCount(TypedDict):
    schema: str
    grid_size: int
    capacities: list[int]
    target: int
    actions: list[ActionCount]
    fixed_sum: int
    orbit_assignments: int
    counted_objects: str


def grid_action_permutation(size: int, turns: int, *, reflected: bool) -> list[int]:
    result: list[int] = []
    for row in range(size):
        for column in range(size):
            i, j = (size - 1 - row, column) if reflected else (row, column)
            for _ in range(turns):
                i, j = j, size - 1 - i
            result.append(i * size + j)
    return result


def _cycles(permutation: list[int]) -> list[list[int]]:
    seen: set[int] = set()
    cycles: list[list[int]] = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        cycle: list[int] = []
        current = start
        while current not in seen:
            seen.add(current)
            cycle.append(current)
            current = permutation[current]
        if current != start:
            raise ValueError("invalid symmetry permutation")
        cycles.append(cycle)
    return cycles


def _fixed_count(cycles: list[list[int]], capacities: list[int], target: int) -> int:
    coefficients = [1] + [0] * target
    for cycle in cycles:
        capacity = capacities[cycle[0]]
        if any(capacities[index] != capacity for index in cycle):
            raise ValueError("capacities must be invariant under all D4 actions")
        next_coefficients = [0] * (target + 1)
        for degree, count in enumerate(coefficients):
            if count:
                for occupancy in range(capacity + 1):
                    next_degree = degree + len(cycle) * occupancy
                    if next_degree <= target:
                        next_coefficients[next_degree] += count
        coefficients = next_coefficients
    return coefficients[target]


def count_grid_symmetry(grid_size: int, capacities: list[int], target: int) -> SymmetryCount:
    """Return all eight fixed-point counts and their exact Burnside quotient."""
    if type(grid_size) is not int or not 1 <= grid_size <= MAX_GRID_SIZE:
        raise ValueError(f"grid_size must be an integer in 1..{MAX_GRID_SIZE}")
    if type(capacities) is not list or len(capacities) != grid_size * grid_size:
        raise ValueError("capacities must be a complete row-major grid_size^2 list")
    if any(
        type(capacity) is not int or not 0 <= capacity <= MAX_CAPACITY
        for capacity in capacities
    ):
        raise ValueError(f"capacities must be integers in 0..{MAX_CAPACITY}")
    if type(target) is not int or not 0 <= target <= MAX_TARGET:
        raise ValueError(f"target must be an integer in 0..{MAX_TARGET}")

    actions: list[ActionCount] = []
    for reflected in (False, True):
        for turns in range(4):
            name = ("f" if reflected else "r") + str(turns)
            cycles = _cycles(grid_action_permutation(grid_size, turns, reflected=reflected))
            fixed = _fixed_count(cycles, capacities, target)
            profile = sorted([[len(cycle), capacities[cycle[0]]] for cycle in cycles])
            actions.append({"name": name, "cycle_profile": profile, "fixed_assignments": fixed})
    fixed_sum = sum(action["fixed_assignments"] for action in actions)
    if fixed_sum % 8:
        raise ValueError("Burnside fixed-point sum is not divisible by eight")
    return {
        "schema": "grid-symmetry-count/v1",
        "grid_size": grid_size,
        "capacities": capacities.copy(),
        "target": target,
        "actions": actions,
        "fixed_sum": fixed_sum,
        "orbit_assignments": fixed_sum // 8,
        "counted_objects": (
            "D4 orbits of integer occupancies of indexed cells; square identities ignored"
        ),
    }


def _from_json(raw: str) -> SymmetryCount:
    if len(raw.encode("utf-8")) > MAX_INPUT_BYTES:
        raise ValueError(f"input exceeds {MAX_INPUT_BYTES} bytes")
    document = json.loads(raw, object_pairs_hook=_unique_pairs)
    if type(document) is not dict or set(document) != {"grid_size", "capacities", "target"}:
        raise ValueError("input must contain exactly grid_size, capacities, target")
    payload = cast("dict[str, object]", document)
    return count_grid_symmetry(
        cast("int", payload["grid_size"]),
        cast("list[int]", payload["capacities"]),
        cast("int", payload["target"]),
    )


def _unique_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    document: dict[str, object] = {}
    for key, value in pairs:
        if key in document:
            raise ValueError(f"duplicate JSON key: {key}")
        document[key] = value
    return document


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--input", required=True, help="JSON grid_size/capacities/target")
    arguments = parser.parse_args(argv)
    try:
        result = _from_json(str(arguments.input))
    except (UnicodeError, json.JSONDecodeError, RecursionError, ValueError) as error:
        print(
            json.dumps(
                {
                    "schema": "grid-symmetry-count/v1",
                    "error": str(error),
                    "count_completed": False,
                }
            )
        )
        return 2
    else:
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
