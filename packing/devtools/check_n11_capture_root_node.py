"""Replay root-self capture transitions after its accepted first step.

The source-bound first-step receipt is a premise. Complete later steps promote
ownership only after every closed angle row, common kernel, and exact compressed
point passes. The final partial step is checked but never promoted. This does
not prove the branch tree, local capture, or global optimality.
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
from devtools import check_n11_capture_step0 as first_step
from devtools import check_n11_capture_transition_pilot as primitive
from devtools import check_n11_closed_degenerate_cover as degenerate
from devtools import check_n11_optimality_field_mask0 as geometry
from devtools import n11_integer_collision as integer_collision

STEP0_SHA = "3e8180817ffedff6406c13e1e98ac5beacad54a2d8bd9695c8a238b4467f78af"
STEP0_RESULT_SHA = "8ca86cc3f119c1dc42e14b142d04cf6863934b799b8e8b6818e54830b1d22b78"
INTEGER_COLLISION_SHA = "4a1f71cdc96134af1083c84717912b73801b07933a8f7cd2eff8b998b31eab98"
Point = pilot.Point
Polygon = pilot.Polygon


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def remaining(budget: geometry.Budget) -> None:
    if time.monotonic() >= budget.deadline:
        raise geometry.IncompleteError("root-node replay wall ceiling")


def incomplete_at_limit(stop_step: int) -> None:
    raise geometry.IncompleteError(f"selected step limit {stop_step}/13")


def incomplete_at_row_limit(checked: int, required: int) -> None:
    raise geometry.IncompleteError(f"selected row limit {checked}/{required}")


def source_unchanged() -> bool:
    return (
        first_step.__file__ is not None
        and integer_collision.__file__ is not None
        and pilot.digest(Path(first_step.__file__)) == STEP0_SHA
        and pilot.digest(Path(integer_collision.__file__)) == INTEGER_COLLISION_SHA
        and first_step.dependencies_unchanged()
    )


def extract(path: Path, query: str) -> dict[str, Any]:
    raw = subprocess.run(
        ["jq", "-c", query, str(path)], capture_output=True, check=True, timeout=25
    )
    return geometry.strict_json(raw.stdout)


def reference_key(reference: dict[str, Any]) -> str:
    return json.dumps(reference, sort_keys=True, separators=(",", ":"))


def row_lookup(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result = {reference_key(row["reference"]): row for row in rows}
    require(len(result) == len(rows), "duplicate accepted predecessor reference")
    return result


def match_geometry(source: Any, accepted: Polygon) -> bool:
    return pilot.hull(pilot.points(source)) == pilot.hull(accepted)


def initial_state(
    header: dict[str, Any], adaptive: dict[str, Any], cover: dict[str, Any]
) -> tuple[dict[int, Polygon], dict[int, list[dict[str, Any]]], dict[int, Polygon]]:
    require(
        header["schema"] == "exact_branch_owned_hull_v1"
        and header["node_id"] == "root-self-240"
        and header["mask_index"] == 438
        and tuple(header["mask"]) == pilot.MASK
        and Q(header["U"]) == geometry.U
        and Q(header["B"]) == geometry.B
        and header["parent"] is None
        and header["constraints"] == [],
        "unsupported root-node header",
    )
    cells = {cell["owner"]: cell["rows"] for cell in adaptive["cells"]}
    require(set(cells) == set(pilot.MASK), "final phase-two owner census")
    owned = adaptive["owned_points"]
    require(isinstance(owned, list) and len(owned) == 16, "phase-two owner array")
    bridge.check_hulls_and_refs(
        header["initial"], owned, {owner: len(cells[owner]) for owner in pilot.MASK}
    )
    groups = {owner: pilot.hull(pilot.points(owned[owner])) for owner in pilot.MASK}
    worlds = {owner: first_step.world(cover, owner) for owner in range(16)}
    state: dict[int, list[dict[str, Any]]] = {}
    for owner in pilot.MASK:
        cursor = Q()
        accepted: list[dict[str, Any]] = []
        for index, row in enumerate(cells[owner]):
            lo, hi = (Q(value) for value in row["interval"])
            require(lo == cursor and lo < hi <= 1, "phase-two angle row partition")
            cursor = hi
            outer = primitive.phase2_outer(row, worlds[owner])
            accepted.append(
                {
                    "reference": {"kind": "phase2", "round": 14, "owner": owner, "row": index},
                    "interval": [str(lo), str(hi)],
                    "outer_domain": [[str(x), str(y)] for x, y in outer],
                    "residual_polygons": row["residual_polygons"],
                }
            )
        require(cursor == 1, "phase-two angular inventory incomplete")
        state[owner] = accepted
    return groups, state, worlds


def inherited_domain(
    row: dict[str, Any],
    predecessors: dict[str, dict[str, Any]],
    owned: Polygon,
) -> tuple[Q, Q, Polygon]:
    old = predecessors.get(reference_key(row["prior_reference"]))
    if old is None:
        raise ValueError("row cites unaccepted predecessor")
    lo, hi = (Q(value) for value in row["interval"])
    old_lo, old_hi = (Q(value) for value in old["interval"])
    require(0 <= old_lo <= lo < hi <= old_hi <= 1, "row escapes prior angle interval")
    prior_outer = pilot.hull(pilot.points(old["outer_domain"]))
    cuts = primitive.necessary_self_cuts(row.get("self_hull_cuts", []), owned, lo, hi)
    domain = pilot.hull(geometry.intersect(prior_outer, cuts)) if prior_outer else []
    return lo, hi, domain


def partner_cover(
    proposed: list[dict[str, Any]],
    prior_rows: list[dict[str, Any]],
    owned: Polygon,
    *,
    budget: geometry.Budget,
) -> tuple[list[tuple[Polygon, Polygon]], int]:
    lookup = row_lookup(prior_rows)
    require(bool(proposed), "missing used partner cover")
    cursor = Q()
    live: list[tuple[Polygon, Polygon]] = []
    for row in proposed:
        remaining(budget)
        adapted = {**row, "prior_reference": row["reference"]}
        lo, hi, domain = inherited_domain(adapted, lookup, owned)
        require(lo == cursor, "partner angle cover gap or overlap")
        cursor = hi
        require(match_geometry(row["domain"], domain), "partner pose domain differs")
        if domain:
            core = pilot.convex(row["core"])
            primitive.strict_core(core, lo, hi)
            live.append((domain, core))
        else:
            require(row["core"] == [], "empty partner domain has core")
    require(cursor == 1, "used partner cover incomplete")
    return live, len(proposed)


def check_row(
    row: dict[str, Any],
    index: int,
    step_index: int,
    owner: int,
    *,
    prior_rows: dict[str, dict[str, Any]],
    groups: dict[int, Polygon],
    world: Polygon,
    covers: dict[int, list[tuple[Polygon, Polygon]]],
    budget: geometry.Budget,
    collision_backend: str,
) -> tuple[int, int, int, list[tuple[Q, Q, Q]]]:
    require(
        row["reference"]
        == {"kind": "phase3", "node": "root-self-240", "step": step_index, "row": index},
        "capture row identity",
    )
    lo, hi, domain = inherited_domain(row, prior_rows, groups[owner])
    require(match_geometry(row["input_domain"], domain), "query input domain differs")
    if not domain:
        require(
            row["core_vertices"] == []
            and row["collision_regions"] == []
            and row["residual_polygons"] == [],
            "empty query domain has geometry",
        )
        primitive.verify_row_output(row, [], [], world)
        return 0, 0, 0, []
    core = pilot.convex(row["core_vertices"])
    primitive.strict_core(core, lo, hi)
    extra: list[Polygon] = []
    facets = 0
    for item in row["collision_regions"]:
        partner = item["partner"]
        require(partner in covers and partner != owner, "collision partner unadmitted")
        region = pilot.convex(item["vertices"])
        if covers[partner]:
            checker = (
                integer_collision.universal_collision
                if collision_backend == "integer"
                else primitive.universal_collision
            )
            facets += checker(core, domain, covers[partner], region, budget=budget)
        else:
            require(item["status"] == "EMPTY_PARTNER_COVER", "unsupported empty partner")
            lines = degenerate.convex_halfplanes(domain)
            require(
                all(nx * x + ny * y <= upper for x, y in region for nx, ny, upper in lines),
                "empty-partner region escapes query",
            )
        extra.append(region)
    legal = geometry.intersect(domain, primitive.wall_lines(lo, hi))
    residual = [pilot.convex(polygon) for polygon in row["residual_polygons"]]
    if legal:
        forbidden = [
            pilot.hull([(x - qx, y - qy) for x, y in group for qx, qy in core])
            for other, group in groups.items()
            if other != owner
        ]
        charged = [*forbidden, *extra, *residual]
        coverage = (
            geometry.exact_union_cover(legal, charged, budget=budget)
            if geometry.area2(legal) > 0
            else degenerate.exact_cover_closed_degenerate(legal, charged, budget=budget)
        )
    else:
        require(not residual, "empty legal row has residual")
        coverage = {"events": 0, "probes": 0}
    primitive.verify_row_output(row, core, residual, world)
    planes = [
        (Q(item["normal"][0]), Q(item["normal"][1]), Q(item["upper"]))
        for item in row["common_core_halfplanes"]
    ]
    return coverage["events"], coverage["probes"], facets, planes


class _RowState:
    prior_rows: dict[str, dict[str, Any]] | None = None
    groups: dict[int, Polygon] | None = None
    world: Polygon | None = None
    covers: dict[int, list[tuple[Polygon, Polygon]]] | None = None
    budget: geometry.Budget | None = None
    owner: int | None = None
    step_index: int | None = None
    collision_backend: str | None = None


def _worker_init(
    prior_rows: dict[str, dict[str, Any]],
    groups: dict[int, Polygon],
    world: Polygon,
    covers: dict[int, list[tuple[Polygon, Polygon]]],
    assignment: tuple[geometry.Budget, int, int, str],
) -> None:
    budget, owner, step_index, collision_backend = assignment
    _RowState.prior_rows = prior_rows
    _RowState.groups = groups
    _RowState.world = world
    _RowState.covers = covers
    _RowState.budget = budget
    _RowState.owner = owner
    _RowState.step_index = step_index
    _RowState.collision_backend = collision_backend


def _worker_row(task: tuple[int, dict[str, Any]]) -> tuple[int, int, int, list[tuple[Q, Q, Q]]]:
    prior_rows, groups, world = _RowState.prior_rows, _RowState.groups, _RowState.world
    covers, budget = _RowState.covers, _RowState.budget
    owner, step_index = _RowState.owner, _RowState.step_index
    collision_backend = _RowState.collision_backend
    if (
        prior_rows is None
        or groups is None
        or world is None
        or covers is None
        or budget is None
        or owner is None
        or step_index is None
        or collision_backend is None
    ):
        raise ValueError("capture row worker state missing")
    index, row = task
    return check_row(
        row,
        index,
        step_index,
        owner,
        prior_rows=prior_rows,
        groups=groups,
        world=world,
        covers=covers,
        budget=budget,
        collision_backend=collision_backend,
    )


def check_step(
    source: dict[str, Any],
    groups: dict[int, Polygon],
    cells: dict[int, list[dict[str, Any]]],
    worlds: dict[int, Polygon],
    *,
    workers: int,
    collision_backend: str,
    row_limit: int,
    budget: geometry.Budget,
    progress: dict[str, Any],
) -> None:
    step = source["step"]
    index, owner = step["index"], step["owner"]
    require(type(index) is int and 1 <= index <= 13 and owner in pilot.MASK, "step identity")
    require(step["allowed_half_angle"] == ["0", "1"], "unsupported branch angle scope")
    require(
        {
            int(key): pilot.hull(pilot.points(value))
            for key, value in step["prior_owned_hulls"].items()
        }
        == groups,
        "step prior ownership differs",
    )
    rows = step["rows"]
    require(bool(rows), "empty step rows")
    used = {region["partner"] for row in rows for region in row["collision_regions"]}
    require(
        all(partner in pilot.MASK and partner != owner for partner in used), "partner inventory"
    )
    covers: dict[int, list[tuple[Polygon, Polygon]]] = {}
    admitted_cover_rows = 0
    for partner in sorted(used):
        remaining(budget)
        proposal = step["prior_partner_pose_covers"].get(str(partner))
        require(proposal is not None, "used partner cover missing")
        covers[partner], count = partner_cover(
            proposal, cells[partner], groups[partner], budget=budget
        )
        admitted_cover_rows += count
    prior_rows = row_lookup(cells[owner])
    cursor = Q()
    for row in rows:
        remaining(budget)
        lo, hi = (Q(value) for value in row["interval"])
        require(lo == cursor and lo < hi <= 1, "step angle partition gap or overlap")
        cursor = hi
    selected_rows = rows if row_limit == 0 else rows[:row_limit]
    require(bool(selected_rows), "empty selected row prefix")
    executor: concurrent.futures.ProcessPoolExecutor | None = None
    if workers == 1:
        _worker_init(
            prior_rows,
            groups,
            worlds[owner],
            covers,
            (budget, owner, index, collision_backend),
        )
        checked = map(_worker_row, enumerate(selected_rows))
    else:
        executor = concurrent.futures.ProcessPoolExecutor(
            max_workers=workers,
            mp_context=multiprocessing.get_context("spawn"),
            initializer=_worker_init,
            initargs=(
                prior_rows,
                groups,
                worlds[owner],
                covers,
                (budget, owner, index, collision_backend),
            ),
        )
        checked = executor.map(_worker_row, enumerate(selected_rows))
    planes: list[tuple[Q, Q, Q]] = []
    events = probes = facets = 0
    try:
        for row_index, (row_events, row_probes, row_facets, row_planes) in enumerate(checked):
            remaining(budget)
            events += row_events
            probes += row_probes
            facets += row_facets
            planes.extend(row_planes)
            progress.update(
                current_step=index,
                current_step_rows_checked=row_index + 1,
                current_step_coverage_events=events,
                current_step_coverage_probes=probes,
                current_step_universal_facet_vertex_checks=facets,
                current_step_common_core_planes=len(planes),
            )
    finally:
        if executor is not None:
            executor.shutdown(wait=True, cancel_futures=True)
    if len(selected_rows) < len(rows):
        incomplete_at_row_limit(len(selected_rows), len(rows))
    additions: Polygon = []
    if step["complete"] is True:
        require(cursor == 1 and index <= 12, "complete step angle or index")
        additions = first_step.check_kernel(step, groups[owner], planes)
        next_group = pilot.hull([*groups[owner], *additions])
        require(
            match_geometry(source["next_prior"][str(owner)], next_group)
            and all(
                match_geometry(source["next_prior"][str(other)], group)
                for other, group in groups.items()
                if other != owner
            ),
            "next step does not consume accepted owner update",
        )
        groups[owner] = next_group
        cells[owner] = rows
    else:
        require(
            index == 13
            and cursor < 1
            and step["common_owned_kernel"] == []
            and step.get("inner_grid_compression") is None,
            "unsupported partial step promotion",
        )
    remaining(budget)
    progress["steps"].append(
        {
            "index": index,
            "owner": owner,
            "complete": step["complete"],
            "rows_checked": len(rows),
            "partner_cover_rows": admitted_cover_rows,
            "coverage_events": events,
            "coverage_probes": probes,
            "universal_facet_vertex_checks": facets,
            "common_core_planes": len(planes),
            "compressed_additions": len(additions) if step["complete"] else 0,
        }
    )


def final_state(
    final: dict[str, Any],
    header: dict[str, Any],
    groups: dict[int, Polygon],
    cells: dict[int, list[dict[str, Any]]],
    worlds: dict[int, Polygon],
) -> None:
    require(
        tuple(final["mask"]) == pilot.MASK
        and Q(final["U"]) == geometry.U
        and Q(final["B"]) == geometry.B
        and final["constraints"] == []
        and final["source"] == header["source"]
        and final["guard_source"] == header["guard_source"],
        "final state header differs",
    )
    require(set(final["groups"]) == set(map(str, pilot.MASK)), "final group census")
    require(set(final["cells"]) == set(map(str, pilot.MASK)), "final cell census")
    for owner in pilot.MASK:
        require(
            match_geometry(final["groups"][str(owner)], groups[owner]), "final group differs"
        )
        got = final["cells"][str(owner)]
        accepted = cells[owner]
        require(len(got) == len(accepted), "final row count differs")
        for source_row, checked in zip(got, accepted, strict=True):
            require(
                source_row["reference"] == checked["reference"]
                and [Q(value) for value in source_row["interval"]]
                == [Q(value) for value in checked["interval"]]
                and match_geometry(
                    source_row["outer_domain"], pilot.points(checked["outer_domain"])
                )
                and len(source_row["residual_polygons"]) == len(checked["residual_polygons"])
                and all(
                    match_geometry(poly, pilot.points(reference))
                    for poly, reference in zip(
                        source_row["residual_polygons"],
                        checked["residual_polygons"],
                        strict=True,
                    )
                ),
                "final accepted row differs",
            )
    require(len(final["world"]) == 16, "final world inventory")
    for owner in range(16):
        require(match_geometry(final["world"][owner], worlds[owner]), "final world differs")


def run(args: argparse.Namespace) -> dict[str, Any]:
    started = time.monotonic()
    budget = geometry.Budget(started + args.max_seconds, args.max_events)
    result: dict[str, Any] = {
        "status": "INCOMPLETE",
        "root_node_state_checked": False,
        "capture_tree_proved": False,
        "candidate_capture_proved": False,
        "global_optimality_proved": False,
        "checker_sha256": pilot.digest(Path(__file__)),
        "step0_checker_sha256": STEP0_SHA,
        "step0_result_sha256": STEP0_RESULT_SHA,
        "integer_collision_sha256": INTEGER_COLLISION_SHA,
        "root_source_sha256": bridge.ROOT_SOURCE_SHA,
        "adaptive_sha256": pilot.ADAPTIVE_SHA,
        "max_seconds": args.max_seconds,
        "max_events_per_cover": args.max_events,
        "workers": args.workers,
        "stop_step": args.stop_step,
        "row_limit": args.row_limit,
        "collision_backend": args.collision_backend,
        "steps": [],
    }
    try:
        require(
            math.isfinite(args.max_seconds)
            and args.max_seconds > 0
            and args.max_events > 0
            and 1 <= args.workers <= 3
            and 1 <= args.stop_step <= 13
            and args.row_limit >= 0
            and args.collision_backend in ("reference", "integer"),
            "positive bounded node replay parameters",
        )
        require(source_unchanged(), "imported proof source changed")
        require(
            pilot.digest(args.step0_result) == STEP0_RESULT_SHA, "first-step receipt changed"
        )
        accepted = geometry.strict_json(args.step0_result.read_bytes())
        require(
            accepted["status"] == "PASS_FIRST_CAPTURE_STEP_TRANSITION"
            and accepted["step0_transition_checked"] is True
            and accepted["rows_checked"] == 217
            and accepted["checker_sha256"] == STEP0_SHA
            and accepted["root_source_sha256"] == bridge.ROOT_SOURCE_SHA
            and accepted["adaptive_sha256"] == pilot.ADAPTIVE_SHA
            and accepted["bridge_result_sha256"] == primitive.BRIDGE_RESULT_SHA,
            "accepted first step premise differs",
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
        header = extract(
            args.root_source,
            "{schema,node_id,mask_index,mask,U,B,parent,constraints,initial,source,guard_source,step0:.steps[0],step1_prior:.steps[1].prior_owned_hulls}",
        )
        adaptive = extract(args.adaptive, "{owned_points,cells:.rounds[13].cells}")
        groups, cells, worlds = initial_state(header, adaptive, cover)
        require(
            {
                int(owner): pilot.hull(pilot.points(value))
                for owner, value in header["step0"]["prior_owned_hulls"].items()
            }
            == groups,
            "accepted first step prior differs",
        )
        groups[15] = pilot.hull(pilot.points(header["step1_prior"]["15"]))
        cells[15] = header["step0"]["rows"]
        require(
            all(
                match_geometry(header["step1_prior"][str(owner)], group)
                for owner, group in groups.items()
            ),
            "accepted first step next state differs",
        )
        remaining(budget)
        for index in range(1, args.stop_step + 1):
            source = extract(
                args.root_source,
                "{step:.steps["
                + str(index)
                + "],next_prior:.steps["
                + str(index + 1)
                + "].prior_owned_hulls}",
            )
            check_step(
                source,
                groups,
                cells,
                worlds,
                workers=args.workers,
                collision_backend=args.collision_backend,
                row_limit=args.row_limit if index == args.stop_step else 0,
                budget=budget,
                progress=result,
            )
            result["steps_checked"] = index + 1
        if args.stop_step < 13:
            incomplete_at_limit(args.stop_step)
        final = extract(args.root_source, "{final_state,closed,terminal,contradiction}")
        require(
            final["closed"] is False
            and final["terminal"] is True
            and final["contradiction"] is None,
            "root source closing status differs",
        )
        final_state(final["final_state"], header, groups, cells, worlds)
        require(
            pilot.digest(args.root_source) == bridge.ROOT_SOURCE_SHA
            and pilot.digest(args.adaptive) == pilot.ADAPTIVE_SHA
            and pilot.digest(args.step0_result) == STEP0_RESULT_SHA
            and pilot.digest(Path(__file__)) == result["checker_sha256"]
            and source_unchanged(),
            "source changed during root-node replay",
        )
        remaining(budget)
        result.update(status="PASS_ROOT_NODE_STATE", root_node_state_checked=True)
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
    parser.add_argument("--step0-result", type=Path, required=True)
    parser.add_argument("--stop-step", type=int, default=13)
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument(
        "--collision-backend", choices=("reference", "integer"), default="reference"
    )
    parser.add_argument(
        "--row-limit",
        type=int,
        default=0,
        help="diagnostic prefix of the selected final step; never promotes that step",
    )
    parser.add_argument("--max-seconds", type=float, default=900)
    parser.add_argument("--max-events", type=int, default=20000)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = run(args)
    print(
        json.dumps(
            {
                key: result.get(key)
                for key in (
                    "status",
                    "steps_checked",
                    "current_step",
                    "current_step_rows_checked",
                    "root_node_state_checked",
                    "wall_seconds",
                    "error",
                )
            }
        )
    )
    return 0 if result["status"] == "PASS_ROOT_NODE_STATE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
