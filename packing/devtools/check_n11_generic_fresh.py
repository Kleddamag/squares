"""Independently replay one bounded fresh-wall generic certificate.

The source polygons and status fields are proposals. A seed pass proves only
strict point ownership and the complete wall-row starting state. A row pass
also checks one exact core and closed-domain residual cover. Neither scope
excludes a mask or proves global optimality. A full pass checks all five
sequential states and all 160 closed angle rows before excluding case 2095.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import multiprocessing
import resource
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools import check_n11_optimality_field_mask0 as geometry

PACKET = geometry.PACKET
OBJECTS = PACKET / "receipts/generic-mask2095-intake/objects"
COVER = PACKET / "receipts/d4-independent/objects" / f"{geometry.COVER_SHA}.gz"
MASK_INDEX = 2095
MASK = (1, 2, 3, 4, 6, 7, 8, 10, 11, 12, 14)
GEOMETRY_SHA = "75fc0238f2ac91af9dc9cf57bd00792343dcf3321c395adddebf0f3465113ce5"
SOURCE_PIN = (
    "68adba943c66ee60c65caf8094dfc18f68a622379acf506ed40558f87602f8aa",
    7_032_538,
    "800d8684bb856727acedbf438a27f57918c8ecd679c3df979e30ad826c590594",
    1_230_844,
)
SEED_PIN = (
    "7b6d67e08e29b7ee6401d440d2c128cbf3f5145be5d5f36a29d7edaab4853251",
    732_968,
    "83aebf79b8751a753e07d2693afe377d831035e1b531ad337ad5c79521e823b7",
    49_846,
)
AUDIT_PIN = (
    "bd116d90693c5e719530b2c012e5bd63cccb230efc9e5df15268164584a3661b",
    29_139,
    "25da11f4e602598e4095d0810d1cc09e7dd3589cba9a9ff1db2b6c5db650c8a3",
    5_778,
)
A1_PIN = (geometry.A1_SHA, 122_029, geometry.A1_LFS_SHA, 26_100)
A1_OBJECT = PACKET / "receipts/case-census/objects" / f"{geometry.A1_SHA}.gz"
Point = tuple[Q, Q]
Polygon = list[Point]


class _WorkerState:
    source: dict[str, Any] | None = None
    world: list[Polygon] | None = None


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def remaining(budget: geometry.Budget) -> None:
    if time.monotonic() >= budget.deadline:
        raise geometry.IncompleteError("generic pilot wall ceiling expired")


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_pin(path: Path, pin: tuple[str, int, str, int]) -> dict[str, Any]:
    raw_sha, raw_bytes, packed_sha, packed_bytes = pin
    return geometry.pinned_gzip(
        path,
        packed_bytes=packed_bytes,
        packed_sha=packed_sha,
        raw_bytes=raw_bytes,
        raw_sha=raw_sha,
    )


def points(value: Any) -> Polygon:
    require(isinstance(value, list), "polygon must be a list")
    return [geometry.point(point) for point in value]


def hull(values: Polygon) -> Polygon:
    """Exact monotone-chain convex hull, including singleton/segment inputs."""
    ordered = sorted(set(values))
    if len(ordered) <= 2:
        return ordered

    def turn(a: Point, b: Point, c: Point) -> Q:
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    lower: Polygon = []
    upper: Polygon = []
    for point in ordered:
        while len(lower) >= 2 and turn(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    for point in reversed(ordered):
        while len(upper) >= 2 and turn(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


def convex(value: Any) -> Polygon:
    polygon = points(value)
    require(bool(polygon), "empty proposed region")
    if len(polygon) <= 2:
        return hull(polygon)
    turns = [
        (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        for a, b, c in zip(
            polygon, polygon[1:] + polygon[:1], polygon[2:] + polygon[:2], strict=True
        )
    ]
    require(all(t >= 0 for t in turns) or all(t <= 0 for t in turns), "nonconvex region")
    result = hull(polygon)
    require(geometry.area2(polygon) == geometry.area2(result), "region differs from its hull")
    return result


def _same(left: Polygon, right: Polygon) -> bool:
    return hull(left) == hull(right)


def _encoded(polygon: Polygon) -> list[list[str]]:
    return [[str(x), str(y)] for x, y in hull(polygon)]


def _wall_lines(lo: Q, hi: Q) -> list[tuple[Q, Q, Q]]:
    width = min(sum(geometry.trig(t), Q()) for t in (lo, hi))
    require(
        geometry.quadratic_nonnegative(1 - width, Q(2), -1 - width, lo, hi),
        "full-angle legal-wall envelope fails",
    )
    h = geometry.B * width / 2
    return [
        (Q(1), Q(0), geometry.L - h),
        (Q(-1), Q(0), -h),
        (Q(0), Q(1), geometry.L - h),
        (Q(0), Q(-1), -h),
    ]


def _seed(
    seed: dict[str, Any], cover: dict[str, Any], *, budget: geometry.Budget
) -> tuple[dict[int, Polygon], dict[int, list[dict[str, Any]]], list[Polygon]]:
    require(seed.get("schema") == "generic_wall_seed_v1", "wrong seed schema")
    require(type(seed.get("mask_index")) is int and seed["mask_index"] == MASK_INDEX, "seed ID")
    require(seed.get("mask") == list(MASK), "seed mask changed")
    require(cover["canonical_eleven_cell_subsets"][MASK_INDEX] == list(MASK), "canonical mask")
    require(Q(seed["U"]) == geometry.U and Q(seed["B"]) == geometry.B, "seed U/B")
    require(seed["cover_source"]["sha256"] == geometry.COVER_SHA, "seed cover binding")
    require(type(seed.get("bins")) is int and seed["bins"] == 32, "seed bins")
    require(set(seed["groups"]) == set(map(str, MASK)), "seed group inventory")
    require(set(seed["cells"]) == set(map(str, MASK)), "seed row-owner inventory")
    world = [
        [(geometry.B * x, geometry.B * y) for x, y in geometry.cell_vertices(cover, owner)]
        for owner in range(16)
    ]
    require(len(seed["world"]) == 16, "seed world inventory")
    require(
        all(
            _same(points(source), actual)
            for source, actual in zip(seed["world"], world, strict=True)
        ),
        "seed world differs from admitted D4 cover",
    )
    groups: dict[int, Polygon] = {}
    rows: dict[int, list[dict[str, Any]]] = {}
    for owner in MASK:
        group = points(seed["groups"][str(owner)])
        require(
            group and len(set(group)) == len(group), "seed group has duplicate/empty points"
        )
        for point in group:
            remaining(budget)
            geometry.ownership(geometry.cell_vertices(cover, owner), point, budget=budget)
        groups[owner] = hull(group)
        owner_rows = seed["cells"][str(owner)]
        require(len(owner_rows) == 32, "seed angular inventory changed")
        normalized_rows: list[dict[str, Any]] = []
        for index, row in enumerate(owner_rows):
            remaining(budget)
            lo, hi = (Q(t) for t in row["interval"])
            require((lo, hi) == (Q(index, 32), Q(index + 1, 32)), "seed row gap/overlap")
            domain = geometry.intersect(world[owner], _wall_lines(lo, hi))
            require(_same(points(row["outer_domain"]), domain), "seed legal domain differs")
            require(row["outer_bounds"] == [], "unexpected seed support restriction")
            expected_residual = [domain] if domain else []
            actual_residual = [points(value) for value in row["residual_polygons"]]
            require(
                len(actual_residual) == len(expected_residual)
                and all(
                    _same(actual, expected)
                    for actual, expected in zip(actual_residual, expected_residual, strict=True)
                ),
                "seed residual differs from complete legal domain",
            )
            require(
                row["reference"] == {"kind": "wall_seed", "owner": owner, "row": index},
                "seed row reference changed",
            )
            normalized_rows.append(
                {
                    "interval": [str(lo), str(hi)],
                    "reference": row["reference"],
                    "outer_domain": _encoded(domain),
                    "residual_polygons": [_encoded(poly) for poly in expected_residual],
                }
            )
        rows[owner] = normalized_rows
    require(sum(len(points(group)) for group in seed["groups"].values()) == 77, "seed census")
    return groups, rows, world


def _strict_core(core: Polygon, lo: Q, hi: Q) -> None:
    require(len(core) >= 3 and geometry.area2(core) > 0, "empty or degenerate proposed core")
    for x, y in core:
        for sign in (-1, 1):
            require(
                _quadratic_strict(
                    geometry.B / 2 - sign * x, -2 * sign * y, geometry.B / 2 + sign * x, lo, hi
                )
                and _quadratic_strict(
                    geometry.B / 2 - sign * y, 2 * sign * x, geometry.B / 2 + sign * y, lo, hi
                ),
                "core vertex fails complete-angle strict containment",
            )


def _quadratic_strict(a: Q, b: Q, c: Q, lo: Q, hi: Q) -> bool:
    probes = [lo, hi]
    if c > 0:
        vertex = -b / (2 * c)
        if lo < vertex < hi:
            probes.append(vertex)
    return all(a + b * t + c * t * t > 0 for t in probes)


def _source_header(
    source: dict[str, Any], groups: dict[int, Polygon], rows: dict[int, list[dict[str, Any]]]
) -> None:
    require(source.get("schema") == "exact_generic_owned_hull_v1", "wrong terminal schema")
    require(
        source.get("parent") is None and source.get("constraints") == [], "unsupported ancestry"
    )
    require(source.get("guard_source") is None, "guarded source unsupported")
    require(
        type(source.get("mask_index")) is int and source["mask_index"] == MASK_INDEX,
        "source ID",
    )
    require(source.get("mask") == list(MASK), "source mask changed")
    require(Q(source["U"]) == geometry.U and Q(source["B"]) == geometry.B, "source U/B")
    require(source["source"]["sha256"] == SEED_PIN[0], "terminal seed binding")
    require(source["initial"]["groups"] and source["steps"], "missing initial state/steps")
    require(
        set(source["initial"]["groups"]) == set(map(str, MASK))
        and set(source["initial"]["cell_references"]) == set(map(str, MASK)),
        "source initial owner inventory changed",
    )
    require(
        all(
            _same(points(source["initial"]["groups"][str(owner)]), groups[owner])
            for owner in MASK
        ),
        "source initial owner state differs from proved seed",
    )
    require(
        all(
            source["initial"]["cell_references"][str(owner)]
            == [row["reference"] for row in rows[owner]]
            for owner in MASK
        ),
        "source initial row references differ from proved seed",
    )


def _check_row(
    source: dict[str, Any],
    step: dict[str, Any],
    row: dict[str, Any],
    row_index: int,
    owner: int,
    *,
    prior: dict[int, Polygon],
    predecessor: dict[str, Any],
    world: list[Polygon],
    budget: geometry.Budget,
) -> tuple[dict[str, int], Polygon, list[tuple[Q, Q, Q]], dict[str, Any]]:
    require(row["prior_reference"] == predecessor["reference"], "wrong predecessor row")
    lo, hi = (Q(t) for t in row["interval"])
    require((lo, hi) == (Q(row_index, 32), Q(row_index + 1, 32)), "row interval gap/overlap")
    require([lo, hi] == [Q(t) for t in predecessor["interval"]], "row predecessor interval")
    domain = geometry.intersect(hull(points(predecessor["outer_domain"])), _wall_lines(lo, hi))
    require(_same(points(row["input_domain"]), domain), "row input domain differs")
    require(geometry.area2(domain) > 0, "degenerate generic domain needs separate proof")
    core = convex(row["core_vertices"])
    _strict_core(core, lo, hi)
    require(row["collision_regions"] == [], "unsupported collision region")
    forbidden = [
        hull([(p[0] - q[0], p[1] - q[1]) for p in group for q in core])
        for other, group in prior.items()
        if other != owner
    ]
    residual = [convex(value) for value in row["residual_polygons"]]
    coverage = geometry.exact_union_cover(domain, forbidden + residual, budget=budget)
    require(
        row["reference"]
        == {
            "kind": "phase3",
            "node": source["node_id"],
            "step": step["index"],
            "row": row_index,
        },
        "row reference changed",
    )
    vertices = [point for polygon in residual for point in polygon]
    expected_planes: list[tuple[Q, Q, Q]] = []
    if vertices:
        for p, q in zip(core, core[1:] + core[:1], strict=True):
            nx, ny = q[1] - p[1], p[0] - q[0]
            expected_planes.append(
                (nx, ny, nx * p[0] + ny * p[1] + min(nx * x + ny * y for x, y in vertices))
            )
    actual_planes = [
        (Q(item["normal"][0]), Q(item["normal"][1]), Q(item["upper"]))
        for item in row["common_core_halfplanes"]
    ]
    require(set(actual_planes) == set(expected_planes), "common owned-core facets differ")
    support = [
        (Q(item["normal"][0]), Q(item["normal"][1]), Q(item["upper"]))
        for item in row["outer_bounds"]
    ]
    require(
        all(nx * x + ny * y <= upper for x, y in vertices for nx, ny, upper in support),
        "support bound excludes a residual vertex",
    )
    trusted_outer: Polygon = []
    if vertices:
        trusted_outer = hull(geometry.intersect(world[owner], support))
        require(
            _same(trusted_outer, points(row["outer_domain"])),
            "row support domain differs",
        )
    else:
        require(not support and not row["outer_domain"], "empty residual has a support domain")
    remaining(budget)
    accepted_row = {
        "interval": [str(lo), str(hi)],
        "reference": row["reference"],
        "outer_domain": _encoded(trusted_outer),
        "residual_polygons": [_encoded(polygon) for polygon in residual],
    }
    return coverage, vertices, actual_planes, accepted_row


def _one_row(
    source: dict[str, Any],
    groups: dict[int, Polygon],
    rows: dict[int, list[dict[str, Any]]],
    world: list[Polygon],
    *,
    budget: geometry.Budget,
) -> dict[str, int]:
    _source_header(source, groups, rows)
    step = source["steps"][0]
    require(step["index"] == 0 and step["owner"] == 6, "wrong first step")
    require(step["allowed_half_angle"] == ["0", "1"], "first step angular domain")
    require(step["prior_partner_pose_covers"] == {}, "unsupported partner covers")
    require(
        all(
            _same(points(step["prior_owned_hulls"][str(owner)]), groups[owner])
            for owner in MASK
        ),
        "step prior differs from proved seed",
    )
    coverage, _, _, _ = _check_row(
        source,
        step,
        step["rows"][0],
        0,
        6,
        prior=groups,
        predecessor=rows[6][0],
        world=world,
        budget=budget,
    )
    return coverage


def _compressed(step: dict[str, Any], prior: Polygon, kernel: Polygon) -> Polygon:
    original = hull(prior + kernel)
    require(
        _same(points(step["compression_source_hull"]), original),
        "compression source differs from independently accepted owner hull",
    )
    receipt = step["inner_grid_compression"]
    new_points = points(receipt["vertices"])
    witnesses = receipt["witnesses"]
    denominator = receipt["denominator"]
    require(
        type(denominator) is int and denominator > 0 and len(new_points) == len(witnesses) > 0,
        "compression inventory or grid denominator changed",
    )
    require(
        receipt["original_vertices"] == len(original)
        and receipt["retained_vertices"] == len(new_points),
        "compression counts changed",
    )
    for point, witness in zip(new_points, witnesses, strict=True):
        indices = witness["indices"]
        weights = [Q(value) for value in witness["weights"]]
        require(
            1 <= len(indices) == len(weights) <= 3
            and all(type(index) is int and 0 <= index < len(original) for index in indices)
            and all(weight >= 0 for weight in weights)
            and sum(weights, Q()) == 1,
            "invalid convex-combination witness",
        )
        require(
            all((coordinate * denominator).denominator == 1 for coordinate in point)
            and geometry.point(witness["point"]) == point
            and point
            == tuple(
                sum(
                    (
                        weight * original[index][axis]
                        for index, weight in zip(indices, weights, strict=True)
                    ),
                    Q(),
                )
                for axis in (0, 1)
            ),
            "compressed point is not a proved convex combination",
        )
    return hull(prior + new_points)


def _worker_init(source: dict[str, Any], world: list[Polygon]) -> None:
    _WorkerState.source = source
    _WorkerState.world = world


def _worker_row(
    step_index: int,
    row_index: int,
    prior: dict[int, Polygon],
    predecessor: dict[str, Any],
    budget: geometry.Budget,
) -> tuple[int, dict[str, int], Polygon, list[tuple[Q, Q, Q]], dict[str, Any], float, float]:
    source = _WorkerState.source
    world = _WorkerState.world
    if source is None or world is None:
        raise ValueError("worker lacks source")
    started = time.monotonic()
    cpu_started = time.process_time()
    step = source["steps"][step_index]
    coverage, vertices, planes, accepted = _check_row(
        source,
        step,
        step["rows"][row_index],
        row_index,
        step["owner"],
        prior=prior,
        predecessor=predecessor,
        world=world,
        budget=budget,
    )
    return (
        row_index,
        coverage,
        vertices,
        planes,
        accepted,
        time.monotonic() - started,
        time.process_time() - cpu_started,
    )


def _full(
    source: dict[str, Any],
    audit: dict[str, Any],
    a1: dict[str, Any],
    groups: dict[int, Polygon],
    rows: dict[int, list[dict[str, Any]]],
    *,
    world: list[Polygon],
    result: dict[str, Any],
    budget: geometry.Budget,
    workers: int,
) -> None:
    _source_header(source, groups, rows)
    require(
        audit["required_antecedent_mask"] == list(MASK)
        and audit["transferred_canonical_mask_indices"] == [MASK_INDEX],
        "audit transfer identity changed",
    )
    assignments = [cert for cert in a1["certificates"] if MASK_INDEX in cert["cases"]]
    require(
        len(assignments) == 1
        and assignments[0]["family"] == "generic"
        and assignments[0]["source_sha256"] == SOURCE_PIN[0]
        and assignments[0]["fresh_audit_sha256"] == AUDIT_PIN[0]
        and assignments[0]["cases"] == [MASK_INDEX],
        "A1 baseline does not assign exactly this generic case to the pinned source",
    )
    state_groups = dict(groups)
    state_rows = dict(rows)
    require(len(source["steps"]) == 5, "generic pilot expects five sequential steps")
    seen: set[int] = set()
    step_timings: list[dict[str, object]] = []
    result["rows_checked"] = 0
    result["steps_completed"] = 0
    for step_index, step in enumerate(source["steps"]):
        step_start = time.monotonic()
        result["current_step"] = step_index
        owner = step["owner"]
        require(
            type(step["index"]) is int
            and step["index"] == step_index
            and owner in MASK
            and owner not in seen,
            "generic step order or owner inventory changed",
        )
        require(
            step["allowed_half_angle"] == ["0", "1"]
            and step["prior_partner_pose_covers"] == {},
            "unsupported angle or partner premise",
        )
        require(
            set(step["prior_owned_hulls"]) == set(map(str, MASK))
            and all(
                _same(points(step["prior_owned_hulls"][str(other)]), state_groups[other])
                for other in MASK
            ),
            "step prior does not equal completed predecessor state",
        )
        require(len(step["rows"]) == 32, "step lacks a full closed angle partition")
        new_rows: list[dict[str, Any]] = []
        all_vertices: Polygon = []
        all_planes: list[tuple[Q, Q, Q]] = []
        row_events = 0
        row_probes = 0
        row_cpu = 0.0
        row_timings: list[dict[str, object]] = []
        if workers == 1:
            step_results = []
            for row_index, row in enumerate(step["rows"]):
                remaining(budget)
                result["current_row"] = row_index
                row_started = time.monotonic()
                cpu_started = time.process_time()
                coverage, vertices, planes, accepted = _check_row(
                    source,
                    step,
                    row,
                    row_index,
                    owner,
                    prior=state_groups,
                    predecessor=state_rows[owner][row_index],
                    world=world,
                    budget=budget,
                )
                step_results.append(
                    (
                        row_index,
                        coverage,
                        vertices,
                        planes,
                        accepted,
                        time.monotonic() - row_started,
                        time.process_time() - cpu_started,
                    )
                )
        else:
            # Each row reads one frozen predecessor state. Join every row before
            # committing the next owner state; a failed worker proves no step.
            with concurrent.futures.ProcessPoolExecutor(
                max_workers=workers,
                mp_context=multiprocessing.get_context("spawn"),
                initializer=_worker_init,
                initargs=(source, world),
            ) as pool:
                futures = {
                    pool.submit(
                        _worker_row,
                        step_index,
                        row_index,
                        state_groups,
                        state_rows[owner][row_index],
                        budget,
                    ): row_index
                    for row_index in range(32)
                }
                step_results = []
                for future in concurrent.futures.as_completed(
                    futures, timeout=max(0, budget.deadline - time.monotonic())
                ):
                    remaining(budget)
                    step_results.append(future.result())
        require(len(step_results) == 32, "step worker join is incomplete")
        for row_index, coverage, vertices, planes, accepted, row_wall, cpu in sorted(
            step_results
        ):
            all_vertices.extend(vertices)
            all_planes.extend(planes)
            new_rows.append(accepted)
            row_events += coverage["events"]
            row_probes += coverage["probes"]
            row_cpu += cpu
            result["rows_checked"] += 1
            row_timings.append(
                {
                    "row": row_index,
                    "events": coverage["events"],
                    "probes": coverage["probes"],
                    "wall_seconds": row_wall,
                    "process_cpu_seconds": cpu,
                }
            )
        require(step["complete"] is True, "source step is not complete")
        kernel = points(step["common_owned_kernel"])
        for point in kernel:
            require(
                all(0 <= coordinate <= geometry.L for coordinate in point)
                and all(nx * point[0] + ny * point[1] <= upper for nx, ny, upper in all_planes),
                "promoted kernel point lacks a complete-row ownership proof",
            )
        if all_vertices:
            state_groups[owner] = _compressed(step, state_groups[owner], kernel)
        else:
            require("inner_grid_compression" not in step, "empty residual has compression")
        state_rows[owner] = new_rows
        seen.add(owner)
        result["steps_completed"] = step_index + 1
        step_timings.append(
            {
                "step": step_index,
                "owner": owner,
                "rows": len(new_rows),
                "row_events": row_events,
                "row_probes": row_probes,
                "row_process_cpu_seconds": row_cpu,
                "row_timings": row_timings,
                "wall_seconds": time.monotonic() - step_start,
            }
        )
        result["step_timings"] = step_timings
    require(seen == {6, 10, 7, 14, 11}, "step owner inventory changed")
    final = source["final_state"]
    require(
        final["mask_index"] == MASK_INDEX
        and final["mask"] == list(MASK)
        and Q(final["U"]) == geometry.U
        and Q(final["B"]) == geometry.B
        and final["constraints"] == []
        and final["guard"] == {}
        and final["guard_source"] is None
        and final["source"] == source["source"],
        "final state premise changed",
    )
    require(
        all(_same(points(final["world"][owner]), world[owner]) for owner in range(16)),
        "final world differs from D4 cover",
    )
    require(
        set(final["groups"]) == set(map(str, MASK))
        and all(
            _same(points(final["groups"][str(owner)]), state_groups[owner]) for owner in MASK
        ),
        "final owned hulls differ from accepted induction",
    )
    for owner in MASK:
        given = final["cells"][str(owner)]
        accepted = state_rows[owner]
        require(len(given) == len(accepted) == 32, "final row count changed")
        for source_row, checked_row in zip(given, accepted, strict=True):
            require(
                source_row["reference"] == checked_row["reference"]
                and [Q(t) for t in source_row["interval"]]
                == [Q(t) for t in checked_row["interval"]]
                and _same(
                    points(source_row["outer_domain"]), points(checked_row["outer_domain"])
                )
                and len(source_row["residual_polygons"])
                == len(checked_row["residual_polygons"])
                and all(
                    _same(points(got), points(want))
                    for got, want in zip(
                        source_row["residual_polygons"],
                        checked_row["residual_polygons"],
                        strict=True,
                    )
                ),
                "final row differs from accepted induction",
            )
    require(
        source["contradiction"]
        == {"kind": "all_parent_poses_forbidden", "owner": 11, "step": 4}
        and all(not row["residual_polygons"] for row in state_rows[11]),
        "complete terminal owner contradiction was not independently shown",
    )
    require(source["terminal"] is True and source["closed"] is True, "source is not terminal")
    require(
        source["mask_exclusion_proved"] is False
        and source["global_optimality_proved"] is False,
        "source claim fields changed",
    )
    result["current_step"] = None
    result["current_row"] = None
    remaining(budget)


def run(args: argparse.Namespace) -> dict[str, Any]:
    require(0 < args.max_seconds <= 30, "generic pilot ceiling must be <=30 seconds")
    require(type(args.workers) is int and 1 <= args.workers <= 3, "worker ceiling is 1..3")
    started = time.monotonic()
    cpu_started = time.process_time()
    children_before = resource.getrusage(resource.RUSAGE_CHILDREN)
    budget = geometry.Budget(started + args.max_seconds, args.max_events)
    paths = {
        "source": args.objects / f"{SOURCE_PIN[0]}.gz",
        "seed": args.objects / f"{SEED_PIN[0]}.gz",
        "audit": args.objects / f"{AUDIT_PIN[0]}.gz",
        "a1": A1_OBJECT,
        "cover": COVER,
        "checker": Path(__file__),
        "geometry": Path(geometry.__file__),
    }
    before = {name: _digest(path) for name, path in paths.items()}
    result: dict[str, Any] = {
        "status": "INCOMPLETE",
        "scope": args.scope,
        "mask_index": MASK_INDEX,
        "geometry_verified": False,
        "excluded_case_ids": [],
        "global_optimality_proved": False,
        "source_sha256": dict(before),
        "max_seconds": args.max_seconds,
        "max_events": args.max_events,
        "workers": args.workers,
    }
    try:
        require(before["geometry"] == GEOMETRY_SHA, "shared exact geometry source changed")
        geometry.admit_d4_receipt()
        cover = _load_pin(COVER, (geometry.COVER_SHA, 773_471, geometry.COVER_LFS_SHA, 25_016))
        source = _load_pin(paths["source"], SOURCE_PIN)
        seed = _load_pin(paths["seed"], SEED_PIN)
        audit = _load_pin(paths["audit"], AUDIT_PIN)
        require(audit["source_sha256"] == SOURCE_PIN[0], "audit terminal binding")
        require(audit["root_sha256"] == SEED_PIN[0], "audit seed binding")
        require(audit["cover_sha256"] == geometry.COVER_SHA, "audit cover binding")
        require(audit["mask_index"] == MASK_INDEX and audit["mask"] == list(MASK), "audit mask")
        seed_started = time.monotonic()
        seed_cpu_started = time.process_time()
        groups, rows, world = _seed(seed, cover, budget=budget)
        result["seed_wall_seconds"] = time.monotonic() - seed_started
        result["seed_process_cpu_seconds"] = time.process_time() - seed_cpu_started
        result["owned_seed_points_checked"] = 77
        result["seed_rows_checked"] = 352
        if args.scope == "row":
            result["row_cover"] = _one_row(source, groups, rows, world, budget=budget)
            result["rows_checked"] = 1
        elif args.scope == "full":
            a1 = _load_pin(A1_OBJECT, A1_PIN)
            _full(
                source,
                audit,
                a1,
                groups,
                rows,
                world=world,
                result=result,
                budget=budget,
                workers=args.workers,
            )
        remaining(budget)
        require(
            all(_digest(path) == before[name] for name, path in paths.items()),
            "source changed during generic pilot",
        )
        if args.scope == "full":
            result["status"] = "PASS_ONE_GENERIC_EXCLUSION"
            result["geometry_verified"] = True
            result["excluded_case_ids"] = [MASK_INDEX]
        elif args.scope == "row":
            result["status"] = "PASS_ONE_GENERIC_ROW_DIAGNOSTIC"
        else:
            result["status"] = "PASS_GENERIC_SEED_ONLY"
    except geometry.IncompleteError as error:
        result["error"] = str(error)
    except concurrent.futures.TimeoutError:
        result["error"] = "row workers did not finish before the shared wall ceiling"
    except (ValueError, KeyError, IndexError, TypeError, OSError, RuntimeError) as error:
        result["status"] = "REFUSED"
        result["error"] = str(error)
    result["wall_seconds"] = time.monotonic() - started
    result["coordinator_process_cpu_seconds"] = time.process_time() - cpu_started
    children_after = resource.getrusage(resource.RUSAGE_CHILDREN)
    result["child_process_cpu_seconds"] = (
        children_after.ru_utime
        + children_after.ru_stime
        - children_before.ru_utime
        - children_before.ru_stime
    )
    result["cpu_scope"] = "coordinator and completed child processes in this run"
    atomic_write_text(args.out, json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--objects", type=Path, default=OBJECTS)
    parser.add_argument("--scope", choices=("seed", "row", "full"), required=True)
    parser.add_argument("--max-seconds", type=float, default=30)
    parser.add_argument("--max-events", type=int, default=50_000)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--out", type=Path, required=True)
    result = run(parser.parse_args())
    print(
        json.dumps(
            {key: result.get(key) for key in ("status", "scope", "wall_seconds", "error")}
        )
    )
    return 0 if result["status"].startswith("PASS_") else 2


if __name__ == "__main__":
    sys.exit(main())
