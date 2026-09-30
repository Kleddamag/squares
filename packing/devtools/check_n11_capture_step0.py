"""Replay the first complete root-self capture owner update with exact geometry.

The accepted adaptive root is an explicit premise. This checks every row of the
first capture step, then its common kernel and exact compressed additions. It
does not accept the capture tree, local guard, or global exclusion.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import math
import multiprocessing
import subprocess
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools import check_n11_capture_root_bridge as bridge
from devtools import check_n11_capture_root_pilot as pilot
from devtools import check_n11_capture_root_round1 as first
from devtools import check_n11_capture_transition_pilot as rowcheck
from devtools import check_n11_closed_degenerate_cover as degenerate
from devtools import check_n11_optimality_field_mask0 as geometry

ROW_CHECKER_SHA = "22c5b4d1f23d48bcc4333bd279df41ba022c337109d063073771349b2854b309"
FIRST_SHA = "50eef26bff3aee127e9ad508b1587014514c8e5f1cf9a3214e8ace7a92d88afd"
Point = pilot.Point
Polygon = pilot.Polygon


class _RowState:
    prior_rows: list[dict[str, Any]] | None = None
    groups: dict[int, Polygon] | None = None
    world15: Polygon | None = None
    partner: list[tuple[Polygon, Polygon]] | None = None
    budget: geometry.Budget | None = None


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def remaining(budget: geometry.Budget) -> None:
    if time.monotonic() >= budget.deadline:
        raise geometry.IncompleteError("capture step0 wall ceiling")


def dependencies_unchanged() -> bool:
    modules = {"row": (rowcheck, ROW_CHECKER_SHA), "first": (first, FIRST_SHA)}
    return rowcheck.dependencies_unchanged() and all(
        module.__file__ is not None and pilot.digest(Path(module.__file__)) == expected
        for module, expected in modules.values()
    )


def extract(path: Path, query: str) -> dict[str, Any]:
    raw = subprocess.run(
        ["jq", "-c", query, str(path)], capture_output=True, check=True, timeout=20
    )
    return geometry.strict_json(raw.stdout)


def world(cover: dict[str, Any], owner: int) -> Polygon:
    return [(geometry.B * x, geometry.B * y) for x, y in geometry.cell_vertices(cover, owner)]


def check_row(
    row: dict[str, Any],
    index: int,
    prior_rows: list[dict[str, Any]],
    *,
    groups: dict[int, Polygon],
    world15: Polygon,
    partner: list[tuple[Polygon, Polygon]],
    budget: geometry.Budget,
) -> tuple[int, int, int, list[tuple[Q, Q, Q]]]:
    reference = row["prior_reference"]
    old_index = reference["row"]
    require(
        reference == {"kind": "phase2", "round": 14, "owner": 15, "row": old_index}
        and type(old_index) is int
        and 0 <= old_index < len(prior_rows),
        "query predecessor reference",
    )
    require(
        row["reference"]
        == {"kind": "phase3", "node": "root-self-240", "step": 0, "row": index},
        "capture row reference",
    )
    lo, hi, domain = rowcheck.row_domain(row, prior_rows[old_index], groups[15], world15)
    require(rowcheck.same(pilot.points(row["input_domain"]), domain), "query input domain")
    if not domain:
        require(
            row["core_vertices"] == []
            and row["collision_regions"] == []
            and row["residual_polygons"] == [],
            "empty query domain has geometry",
        )
        rowcheck.verify_row_output(row, [], [], world15)
        return 0, 0, 0, []
    core = pilot.convex(row["core_vertices"])
    rowcheck.strict_core(core, lo, hi)
    regions: list[Polygon] = []
    facet_checks = 0
    for item in row["collision_regions"]:
        require(item["partner"] == 10, "unsupported collision partner")
        region = pilot.convex(item["vertices"])
        facet_checks += rowcheck.universal_collision(
            core, domain, partner, region, budget=budget
        )
        regions.append(region)
    legal = geometry.intersect(domain, rowcheck.wall_lines(lo, hi))
    residual = [pilot.convex(polygon) for polygon in row["residual_polygons"]]
    if legal:
        forbidden = [
            pilot.hull([(x - qx, y - qy) for x, y in group for qx, qy in core])
            for owner, group in groups.items()
            if owner != 15
        ]
        charged = [*forbidden, *regions, *residual]
        coverage = (
            geometry.exact_union_cover(legal, charged, budget=budget)
            if geometry.area2(legal) > 0
            else degenerate.exact_cover_closed_degenerate(legal, charged, budget=budget)
        )
    else:
        require(not residual, "empty legal domain has residual")
        coverage = {"events": 0, "probes": 0}
    rowcheck.verify_row_output(row, core, residual, world15)
    planes = [
        (Q(item["normal"][0]), Q(item["normal"][1]), Q(item["upper"]))
        for item in row["common_core_halfplanes"]
    ]
    return coverage["events"], coverage["probes"], facet_checks, planes


def check_kernel(step: dict[str, Any], prior: Polygon, planes: list[tuple[Q, Q, Q]]) -> Polygon:
    kernel = pilot.convex(step["common_owned_kernel"])
    require(bool(planes), "unsupported empty common core")
    for point in kernel:
        require(
            all(0 <= coordinate <= geometry.L for coordinate in point),
            "kernel outside container",
        )
        require(
            all(nx * point[0] + ny * point[1] <= upper for nx, ny, upper in planes),
            "kernel outside one accepted row core",
        )
    return first.compressed_points(step, prior, kernel)


def _worker_init(
    prior_rows: list[dict[str, Any]],
    groups: dict[int, Polygon],
    world15: Polygon,
    partner: list[tuple[Polygon, Polygon]],
    budget: geometry.Budget,
) -> None:
    _RowState.prior_rows = prior_rows
    _RowState.groups = groups
    _RowState.world15 = world15
    _RowState.partner = partner
    _RowState.budget = budget


def _worker_row(task: tuple[int, dict[str, Any]]) -> tuple[int, int, int, list[tuple[Q, Q, Q]]]:
    prior_rows = _RowState.prior_rows
    groups = _RowState.groups
    world15 = _RowState.world15
    partner = _RowState.partner
    budget = _RowState.budget
    if (
        prior_rows is None
        or groups is None
        or world15 is None
        or partner is None
        or budget is None
    ):
        raise ValueError("row worker state missing")
    index, row = task
    return check_row(
        row,
        index,
        prior_rows,
        groups=groups,
        world15=world15,
        partner=partner,
        budget=budget,
    )


def check_step0(
    root: dict[str, Any],
    adaptive: dict[str, Any],
    cover: dict[str, Any],
    *,
    row_limit: int,
    workers: int,
    budget: geometry.Budget,
    progress: dict[str, Any],
) -> None:
    step = root["step"]
    require(
        root["parent"] is None
        and root["constraints"] == []
        and step["index"] == 0
        and step["owner"] == 15
        and step["allowed_half_angle"] == ["0", "1"]
        and step["complete"] is True,
        "unsupported capture-root step scope",
    )
    rows = step["rows"]
    require(len(rows) == 217 and 1 <= row_limit <= len(rows), "step row limit")
    cells = {cell["owner"]: cell["rows"] for cell in adaptive["cells"]}
    require(set(cells) == {10, 15}, "selected phase-two cell inventory")
    groups = {
        int(owner): pilot.hull(pilot.points(points))
        for owner, points in root["initial"]["groups"].items()
    }
    require(set(groups) == set(pilot.MASK), "initial group inventory")
    prior_hulls = {
        int(owner): pilot.hull(pilot.points(points))
        for owner, points in step["prior_owned_hulls"].items()
    }
    require(prior_hulls == groups, "step prior hull differs from accepted root")
    world10, world15 = world(cover, 10), world(cover, 15)
    partner, partner_rows = rowcheck.partner_cover(
        step["partner10"], cells[10], 10, groups[10], world10, budget=budget
    )
    progress.update(partner_cover_rows=partner_rows, live_partner_rows=len(partner))
    cursor = Q()
    planes: list[tuple[Q, Q, Q]] = []
    total_events = total_probes = total_facets = 0
    for row in rows[:row_limit]:
        remaining(budget)
        lo, hi = (Q(value) for value in row["interval"])
        require(lo == cursor and lo < hi <= 1, "step angular partition gap or overlap")
        cursor = hi
    remaining(budget)
    executor: concurrent.futures.ProcessPoolExecutor | None = None
    if workers == 1:
        _worker_init(cells[15], groups, world15, partner, budget)
        checked = map(_worker_row, enumerate(rows[:row_limit]))
    else:
        executor = concurrent.futures.ProcessPoolExecutor(
            max_workers=workers,
            mp_context=multiprocessing.get_context("spawn"),
            initializer=_worker_init,
            initargs=(cells[15], groups, world15, partner, budget),
        )
        checked = executor.map(_worker_row, enumerate(rows[:row_limit]))
    try:
        for index, (events, probes, facets, row_planes) in enumerate(checked):
            remaining(budget)
            total_events += events
            total_probes += probes
            total_facets += facets
            planes.extend(row_planes)
            progress.update(
                rows_checked=index + 1,
                coverage_events=total_events,
                coverage_probes=total_probes,
                universal_facet_vertex_checks=total_facets,
            )
    finally:
        if executor is not None:
            executor.shutdown(wait=True, cancel_futures=True)
    if row_limit < len(rows):
        raise geometry.IncompleteError(f"selected row limit {row_limit}/{len(rows)}")
    require(cursor == 1, "step angular partition incomplete")
    additions = check_kernel(step, groups[15], planes)
    resulting = pilot.hull([*groups[15], *additions])
    next_prior = {
        int(owner): pilot.hull(pilot.points(points))
        for owner, points in root["step1_prior"].items()
    }
    require(set(next_prior) == set(pilot.MASK), "next step prior inventory")
    require(
        all(
            next_prior[owner] == (resulting if owner == 15 else groups[owner])
            for owner in pilot.MASK
        ),
        "next step does not consume accepted owner update",
    )
    remaining(budget)
    progress.update(
        step0_join_checked=True,
        kernel_vertices=len(pilot.points(step["common_owned_kernel"])),
        common_core_planes=len(planes),
        compressed_additions=len(additions),
    )


def run(args: argparse.Namespace) -> dict[str, Any]:
    started = time.monotonic()
    budget = geometry.Budget(started + args.max_seconds, args.max_events)
    result: dict[str, Any] = {
        "status": "INCOMPLETE",
        "step0_transition_checked": False,
        "candidate_capture_proved": False,
        "global_optimality_proved": False,
        "rows_checked": 0,
        "checker_sha256": pilot.digest(Path(__file__)),
        "row_checker_sha256": ROW_CHECKER_SHA,
        "root_source_sha256": bridge.ROOT_SOURCE_SHA,
        "adaptive_sha256": pilot.ADAPTIVE_SHA,
        "bridge_result_sha256": rowcheck.BRIDGE_RESULT_SHA,
        "max_seconds": args.max_seconds,
        "max_events_per_cover": args.max_events,
        "row_limit": args.row_limit,
        "workers": args.workers,
    }
    try:
        require(
            math.isfinite(args.max_seconds)
            and args.max_seconds > 0
            and args.max_events > 0
            and 1 <= args.workers <= 3,
            "positive bounded worker budgets required",
        )
        require(dependencies_unchanged(), "imported proof source changed")
        require(
            pilot.digest(args.bridge_result) == rowcheck.BRIDGE_RESULT_SHA,
            "accepted root bridge changed",
        )
        require(pilot.digest(args.root_source) == bridge.ROOT_SOURCE_SHA, "root source changed")
        require(pilot.digest(args.adaptive) == pilot.ADAPTIVE_SHA, "adaptive source changed")
        geometry.admit_d4_receipt()
        cover = geometry.pinned_gzip(
            pilot.COVER,
            packed_bytes=25016,
            packed_sha=geometry.COVER_LFS_SHA,
            raw_bytes=773471,
            raw_sha=geometry.COVER_SHA,
        )
        root = extract(
            args.root_source,
            '{parent,constraints,initial,step:(.steps[0]|{index,owner,allowed_half_angle,complete,prior_owned_hulls,rows,partner10:.prior_partner_pose_covers["10"],common_owned_kernel,compression_source_hull,inner_grid_compression}),step1_prior:.steps[1].prior_owned_hulls}',
        )
        adaptive = extract(
            args.adaptive,
            "{cells:[.rounds[13].cells[]|select(.owner==10 or .owner==15)|{owner,rows}]}",
        )
        remaining(budget)
        check_step0(
            root,
            adaptive,
            cover,
            row_limit=args.row_limit,
            workers=args.workers,
            budget=budget,
            progress=result,
        )
        require(
            pilot.digest(args.root_source) == bridge.ROOT_SOURCE_SHA
            and pilot.digest(args.adaptive) == pilot.ADAPTIVE_SHA
            and pilot.digest(args.bridge_result) == rowcheck.BRIDGE_RESULT_SHA
            and pilot.digest(Path(__file__)) == result["checker_sha256"]
            and dependencies_unchanged(),
            "source changed during step replay",
        )
        remaining(budget)
        result["step0_transition_checked"] = True
        result["status"] = "PASS_FIRST_CAPTURE_STEP_TRANSITION"
    except geometry.IncompleteError as error:
        result["error"] = str(error)
    except (
        ValueError,
        KeyError,
        IndexError,
        TypeError,
        OSError,
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
    ) as error:
        result.update(status="REFUSED", error=str(error))
    result["wall_seconds"] = time.monotonic() - started
    atomic_write_text(args.out, json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root-source", type=Path, required=True)
    parser.add_argument("--adaptive", type=Path, required=True)
    parser.add_argument("--bridge-result", type=Path, required=True)
    parser.add_argument("--row-limit", type=int, default=217)
    parser.add_argument("--max-seconds", type=float, default=180)
    parser.add_argument("--max-events", type=int, default=20000)
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = run(args)
    print(
        json.dumps(
            {
                key: result.get(key)
                for key in (
                    "status",
                    "rows_checked",
                    "partner_cover_rows",
                    "live_partner_rows",
                    "coverage_events",
                    "universal_facet_vertex_checks",
                    "compressed_additions",
                    "wall_seconds",
                    "error",
                )
            }
        )
    )
    return 0 if result["status"] == "PASS_FIRST_CAPTURE_STEP_TRANSITION" else 2


if __name__ == "__main__":
    raise SystemExit(main())
