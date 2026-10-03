"""Independently check the exact, conditional n=11 D4 bridge.

This uses only three decoded JSON proof inputs. It does not import the published
verifier, replay the 2,180 mask exclusions, or check the case-438 capture.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Any

F = Fraction
Point = tuple[F, F]
Polygon = tuple[Point, ...]
U = F(387708359002281417731, 10**20)
INPUT_HASHES = {
    "cover": "df7938d9ba27095a38fabe45f8b26b259a2cc896c2ae4aac6bae874f417adc4e",
    "overlay": "845b5f748843dd60fa7e290a5ea1a304da4e439ae229bd73a841aec816f4e700",
    "distance": "4f960f4001faa6c9c1e7521f3a2344f71e10b41cd38a6425f6821cc1fd2ccd47",
}
SURVIVORS = (438, 999, 1462, 1659)
EXPECTED_MASKS = {
    438: (0, 1, 2, 3, 4, 8, 9, 10, 11, 13, 15),
    999: (0, 1, 2, 4, 6, 7, 9, 10, 12, 14, 15),
    1462: (0, 1, 3, 5, 6, 8, 9, 11, 12, 13, 14),
    1659: (0, 2, 3, 4, 5, 6, 7, 11, 12, 13, 14),
}
VIEWS = ((0, 1, 1), (0, -1, 1), (1, -1, 1), (1, 1, 1))


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def cross(a: Point, b: Point, c: Point) -> F:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def hull(points: Any) -> Polygon:
    ordered = sorted(set(points))
    if len(ordered) < 3:
        return tuple(ordered)
    lower: list[Point] = []
    upper: list[Point] = []
    for point in ordered:
        while len(lower) > 1 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    for point in reversed(ordered):
        while len(upper) > 1 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return tuple(lower[:-1] + upper[:-1])


def clip(poly: Polygon, a: F, b: F, c: F) -> Polygon:
    """Intersect a closed convex point/segment/polygon with ax+by <= c."""
    if not poly:
        return ()
    result: list[Point] = []
    edges = (
        ((poly[0], poly[0]),) if len(poly) == 1 else zip(poly, poly[1:] + poly[:1], strict=True)
    )
    for start, end in edges:
        first = a * start[0] + b * start[1] - c
        last = a * end[0] + b * end[1] - c
        if first <= 0:
            result.append(start)
        if (first < 0 < last) or (last < 0 < first):
            t = first / (first - last)
            result.append(
                (start[0] + t * (end[0] - start[0]), start[1] + t * (end[1] - start[1]))
            )
    return hull(result)


def intersection(poly: Polygon, other: Polygon) -> Polygon:
    require(len(other) >= 3, "intersection clipping cell is degenerate")
    for start, end in zip(other, other[1:] + other[:1], strict=True):
        a, b = end[1] - start[1], start[0] - end[0]
        poly = clip(poly, a, b, a * start[0] + b * start[1])
        if not poly:
            break
    return poly


def squared_distance(p: Point, q: Point) -> F:
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def strict_distance_ban(first: Polygon, second: Polygon) -> tuple[bool, F]:
    maximum = max(squared_distance(p, q) for p in first for q in second) * (U - 1) ** 2
    return maximum < 1, maximum


def canonical_masks() -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    raw = list(combinations(range(16), 11))
    canonical = sorted({min(mask, half_turn(mask)) for mask in raw})
    require(len(raw) == 4368 and len(canonical) == 2184, "incorrect mask universe")
    require(
        all(canonical[index] == mask for index, mask in EXPECTED_MASKS.items()),
        "survivor index drift",
    )
    return raw, canonical


def half_turn(mask: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(15 - cell for cell in mask))


def points(value: Any) -> Polygon:
    return hull((F(x), F(y)) for x, y in value)


def check_cover(value: dict[str, Any]) -> tuple[list[Polygon], list[tuple[int, ...]]]:
    records = value["cells"]
    require(len(records) == 16, "not sixteen cover cells")
    sites = [tuple(map(F, row["center"])) for row in records]
    require(len(set(sites)) == 16, "duplicate cover site")
    cells: list[Polygon] = []
    square = ((F(0), F(0)), (F(1), F(0)), (F(1), F(1)), (F(0), F(1)))
    for index, site in enumerate(sites):
        poly = square
        for other_index, other in enumerate(sites):
            if index == other_index:
                continue
            a, b = 2 * (other[0] - site[0]), 2 * (other[1] - site[1])
            c = other[0] ** 2 + other[1] ** 2 - site[0] ** 2 - site[1] ** 2
            poly = clip(poly, a, b, c)
        require(
            len(poly) >= 3 and poly == points(records[index]["vertices"]),
            "Voronoi cell mismatch",
        )
        require(
            max(squared_distance(p, q) for p in poly for q in poly) * (U - 1) ** 2 < 1,
            "cell diameter is not strictly below one",
        )
        cells.append(poly)
    for index, poly in enumerate(cells):
        require(
            hull((1 - p[0], 1 - p[1]) for p in poly) == cells[15 - index],
            "half-turn indexing mismatch",
        )
    require(
        value["symmetry_cell_involution"] == list(reversed(range(16))),
        "reported involution mismatch",
    )
    raw, canonical = canonical_masks()
    require(
        value["all_eleven_cell_subsets"] == [list(mask) for mask in raw],
        "raw mask inventory mismatch",
    )
    require(
        value["canonical_eleven_cell_subsets"] == [list(mask) for mask in canonical],
        "canonical mask inventory mismatch",
    )
    return cells, canonical


def inverse_view(point: Point, view: tuple[int, int, int]) -> Point:
    swap, x_sign, y_sign = view
    x = point[0] if x_sign == 1 else 1 - point[0]
    y = point[1] if y_sign == 1 else 1 - point[1]
    return (y, x) if swap else (x, y)


def check_inventory(
    expected: dict[tuple[int, ...], Polygon], reported: list[dict[str, Any]]
) -> tuple[list[tuple[int, ...]], list[Polygon], dict[int, int]]:
    require(len(reported) == len(expected), "overlay region omission or addition")
    labels: list[tuple[int, ...]] = []
    vertices: list[Polygon] = []
    dimensions: dict[int, int] = {}
    seen: set[tuple[int, ...]] = set()
    for index, row in enumerate(reported):
        key = tuple(row["labels"])
        require(
            row["index"] == index and key in expected and key not in seen,
            "overlay duplicate or wrong index",
        )
        seen.add(key)
        poly = points(row["vertices"])
        require(poly == expected[key], "overlay vertices mismatch")
        dimension = min(len(poly) - 1, 2)
        require(row["dimension"] == dimension, "overlay dimension mismatch")
        dimensions[dimension] = dimensions.get(dimension, 0) + 1
        labels.append(key)
        vertices.append(poly)
    require(seen == set(expected), "overlay inventory incomplete")
    return labels, vertices, dimensions


def check_overlay(
    cells: list[Polygon], value: dict[str, Any]
) -> tuple[list[tuple[int, ...]], list[Polygon], list[int], dict[int, int]]:
    require(
        tuple(tuple(view) for view in value["symmetries"]) == VIEWS,
        "D4 view convention mismatch",
    )
    regions = {(index,): poly for index, poly in enumerate(cells)}
    counts = [16]
    for view in VIEWS[1:]:
        transformed = [hull(inverse_view(point, view) for point in poly) for poly in cells]
        next_regions: dict[tuple[int, ...], Polygon] = {}
        for labels, poly in regions.items():
            for index, cell in enumerate(transformed):
                clipped = intersection(poly, cell)
                if clipped:
                    next_regions[(*labels, index)] = clipped
        regions = next_regions
        counts.append(len(regions))
    require(counts == [16, 56, 124, 220], "closed overlay count mismatch")
    labels, vertices, dimensions = check_inventory(regions, value["regions"])
    require(dimensions == {0: 8, 2: 212}, "closed boundary region census mismatch")
    return labels, vertices, counts, dimensions


def check_bans(vertices: list[Polygon], value: dict[str, Any]) -> set[tuple[int, int]]:
    require(F(value["U"]) == U, "distance cap mismatch")
    banned: set[tuple[int, int]] = set()
    for row in value["pairs"]:
        first, second = row["regions"]
        require(
            type(first) is int and type(second) is int and 0 <= first < second < len(vertices),
            "invalid distance pair",
        )
        require((first, second) not in banned, "duplicate distance pair")
        valid, maximum = strict_distance_ban(vertices[first], vertices[second])
        require(
            valid and maximum == F(row["maximum_squared_center_distance"]),
            "distance ban is not exact and strict",
        )
        banned.add((first, second))
    require(len(banned) == 1572, "distance ban omission or addition")
    return banned


def members(bits: int) -> Any:
    while bits:
        lowest = bits & -bits
        yield lowest.bit_length() - 1
        bits -= lowest


def check_deadline(deadline: float) -> None:
    if time.monotonic() > deadline:
        raise TimeoutError("D4 check exceeded wall ceiling")


def solve_non_target_cases(
    labels: list[tuple[int, ...]],
    banned: set[tuple[int, int]],
    canonical: list[tuple[int, ...]],
    deadline: float,
) -> tuple[list[dict[str, Any]], list[tuple[int, ...]]]:
    allowed = sorted(
        {canonical[index] for index in SURVIVORS[1:]}
        | {half_turn(canonical[index]) for index in SURVIVORS[1:]}
    )
    require(len(allowed) == 6, "non-target raw mask inventory mismatch")
    target_by_cell = [
        sum(1 << index for index, mask in enumerate(allowed) if cell in mask)
        for cell in range(16)
    ]
    source_regions = [
        sum(1 << index for index, row in enumerate(labels) if row[0] == cell)
        for cell in range(16)
    ]
    compatible = [
        sum(
            1 << other
            for other, other_row in enumerate(labels)
            if all(row[view] != other_row[view] for view in range(4))
            and tuple(sorted((index, other))) not in banned
        )
        for index, row in enumerate(labels)
    ]
    outcomes: list[dict[str, Any]] = []
    for mask_index in SURVIVORS[1:]:
        nodes = 0

        def search(domains: dict[int, int], targets: tuple[int, int, int]) -> bool:
            nonlocal nodes
            nodes += 1
            check_deadline(deadline)
            if not domains:
                return True
            possible: dict[int, int] = {}
            for owner, options in domains.items():
                possible[owner] = sum(
                    1 << region
                    for region in members(options)
                    if all(
                        targets[view] & target_by_cell[labels[region][view + 1]]
                        for view in range(3)
                    )
                )
                if not possible[owner]:
                    return False
            owner = min(possible, key=lambda cell: (possible[cell].bit_count(), cell))
            for region in members(possible[owner]):
                next_domains = {
                    cell: options & compatible[region]
                    for cell, options in possible.items()
                    if cell != owner
                }
                if any(not options for options in next_domains.values()):
                    continue
                next_targets = tuple(
                    targets[view] & target_by_cell[labels[region][view + 1]]
                    for view in range(3)
                )
                if search(next_domains, next_targets):
                    return True
            return False

        source = {cell: source_regions[cell] for cell in canonical[mask_index]}
        require(
            not search(source, (63, 63, 63)),
            f"non-target assignment survives case {mask_index}",
        )
        outcomes.append(
            {"source_canonical_index": mask_index, "status": "UNSAT", "nodes": nodes}
        )
    return outcomes, allowed


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(paths: dict[str, Path], *, max_seconds: float) -> dict[str, Any]:
    start = time.monotonic()
    cpu_start = time.process_time()
    require(
        math.isfinite(max_seconds) and max_seconds > 0,
        "wall ceiling must be finite and positive",
    )
    deadline = start + max_seconds
    inputs: dict[str, dict[str, Any]] = {}
    for role, expected in INPUT_HASHES.items():
        path = paths[role]
        require(sha256(path) == expected, f"{role} source hash mismatch")
        inputs[role] = json.loads(path.read_text())
    check_deadline(deadline)
    require(
        inputs["overlay"]["cover_sha256"] == INPUT_HASHES["cover"], "overlay parent mismatch"
    )
    require(
        inputs["distance"]["overlay_sha256"] == INPUT_HASHES["overlay"],
        "distance parent mismatch",
    )
    cells, canonical = check_cover(inputs["cover"])
    check_deadline(deadline)
    labels, vertices, prefixes, dimensions = check_overlay(cells, inputs["overlay"])
    check_deadline(deadline)
    bans = check_bans(vertices, inputs["distance"])
    check_deadline(deadline)
    search, allowed = solve_non_target_cases(labels, bans, canonical, deadline)
    check_deadline(deadline)
    for role, expected in INPUT_HASHES.items():
        require(sha256(paths[role]) == expected, f"{role} source changed during check")
    return {
        "status": "PASS_INDEPENDENT_CONDITIONAL_D4_BRIDGE",
        "scope": (
            "Exact cover, closed four-view overlay, strict pair bans, and three finite "
            "UNSAT checks; 2180 exclusions and case-438 capture remain premises."
        ),
        "global_optimality_proved": False,
        "input_sha256": INPUT_HASHES,
        "checker_sha256": sha256(Path(__file__)),
        "raw_masks": 4368,
        "canonical_masks": 2184,
        "overlay_prefix_counts": prefixes,
        "overlay_dimensions": dimensions,
        "strict_distance_bans": len(bans),
        "allowed_non_target_raw_masks": [list(mask) for mask in allowed],
        "finite_search": search,
        "wall_seconds": time.monotonic() - start,
        "process_cpu_seconds": time.process_time() - cpu_start,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for role in INPUT_HASHES:
        parser.add_argument(f"--{role}", type=Path, required=True)
    parser.add_argument("--max-seconds", type=float, default=45.0)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    paths = {role: getattr(args, role) for role in INPUT_HASHES}
    result = verify(paths, max_seconds=args.max_seconds)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
