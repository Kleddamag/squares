"""Replay the complete r1 capture node after the accepted root-self state.

Every query and partner view reapplies the exact closed owner-15 center cut.
Complete steps join all rows before promoting ownership. The final partial
step is checked without promotion. Child branches and capture remain open.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import copy
import json
import math
import multiprocessing
import subprocess
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools import check_n11_capture_branch_r1 as branch
from devtools import check_n11_capture_root_bridge as bridge
from devtools import check_n11_capture_root_node as root
from devtools import check_n11_capture_root_pilot as pilot
from devtools import check_n11_optimality_field_mask0 as geometry

BRANCH_PILOT_SHA = "f75b7ef718cc301833770128dd2f9b2bab3473b5dd01f59583e70fc2bb84abf9"


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sources_unchanged() -> bool:
    return (
        branch.__file__ is not None
        and root.__file__ is not None
        and pilot.digest(Path(branch.__file__)) == BRANCH_PILOT_SHA
        and pilot.digest(Path(root.__file__)) == branch.ROOT_CHECKER_SHA
        and root.source_unchanged()
    )


def conditional_view(
    cells: dict[int, list[dict[str, Any]]],
) -> dict[int, list[dict[str, Any]]]:
    """Keep accepted source rows intact; clip owner 15 in every geometric view."""
    visible = {owner: copy.deepcopy(rows) for owner, rows in cells.items()}
    for row in visible[15]:
        original = pilot.hull(pilot.points(row["outer_domain"]))
        clipped = geometry.intersect(original, [branch.center_cut()]) if original else []
        row["outer_domain"] = [[str(x), str(y)] for x, y in pilot.hull(clipped)]
    return visible


class _WorkerState:
    prior_rows: dict[str, dict[str, Any]] | None = None
    groups: dict[int, pilot.Polygon] | None = None
    world: pilot.Polygon | None = None
    covers: dict[int, list[tuple[pilot.Polygon, pilot.Polygon]]] | None = None
    budget: geometry.Budget | None = None
    owner: int | None = None
    step_index: int | None = None


def _worker_init(
    prior_rows: dict[str, dict[str, Any]],
    groups: dict[int, pilot.Polygon],
    world: pilot.Polygon,
    covers: dict[int, list[tuple[pilot.Polygon, pilot.Polygon]]],
    assignment: tuple[geometry.Budget, int, int],
) -> None:
    _WorkerState.prior_rows = prior_rows
    _WorkerState.groups = groups
    _WorkerState.world = world
    _WorkerState.covers = covers
    _WorkerState.budget, _WorkerState.owner, _WorkerState.step_index = assignment


def _worker_row(task: tuple[int, dict[str, Any]]) -> tuple[int, int, int, list[tuple[Q, Q, Q]]]:
    prior_rows, groups, world = _WorkerState.prior_rows, _WorkerState.groups, _WorkerState.world
    covers, budget = _WorkerState.covers, _WorkerState.budget
    owner, step_index = _WorkerState.owner, _WorkerState.step_index
    if (
        prior_rows is None
        or groups is None
        or world is None
        or covers is None
        or budget is None
        or owner is None
        or step_index is None
    ):
        raise ValueError("r1 row worker state missing")
    index, row = task
    return root.check_row(
        row,
        index,
        step_index,
        owner,
        prior_rows=prior_rows,
        groups=groups,
        world=world,
        covers=covers,
        budget=budget,
        collision_backend="integer",
    )


def check_step(
    source: dict[str, Any],
    groups: dict[int, pilot.Polygon],
    cells: dict[int, list[dict[str, Any]]],
    worlds: dict[int, pilot.Polygon],
    *,
    workers: int,
    budget: geometry.Budget,
    progress: dict[str, Any],
) -> None:
    step = source["step"]
    index, owner = step["index"], step["owner"]
    require(type(index) is int and 0 <= index <= 8 and owner in pilot.MASK, "r1 step identity")
    require(step["allowed_half_angle"] == ["0", "1"], "r1 step angle scope")
    require(
        {
            int(key): pilot.hull(pilot.points(value))
            for key, value in step["prior_owned_hulls"].items()
        }
        == groups,
        "r1 step prior ownership differs",
    )
    rows = step["rows"]
    require(bool(rows), "empty r1 step rows")
    visible = conditional_view(cells)
    used = {region["partner"] for row in rows for region in row["collision_regions"]}
    require(
        all(partner in pilot.MASK and partner != owner for partner in used),
        "r1 partner inventory",
    )
    covers: dict[int, list[tuple[pilot.Polygon, pilot.Polygon]]] = {}
    admitted_cover_rows = 0
    for partner in sorted(used):
        root.remaining(budget)
        proposal = step["prior_partner_pose_covers"].get(str(partner))
        require(proposal is not None, "used r1 partner cover missing")
        covers[partner], count = root.partner_cover(
            proposal, visible[partner], groups[partner], budget=budget
        )
        admitted_cover_rows += count
    cursor = Q()
    adapted_rows: list[dict[str, Any]] = []
    for row_index, row in enumerate(rows):
        root.remaining(budget)
        require(
            row["reference"]
            == {"kind": "phase3", "node": branch.R1_NODE, "step": index, "row": row_index},
            "r1 row identity differs",
        )
        lo, hi = (Q(value) for value in row["interval"])
        require(lo == cursor and lo < hi <= 1, "r1 step angle partition gap or overlap")
        cursor = hi
        adapted_rows.append(
            {
                **row,
                "reference": {
                    "kind": "phase3",
                    "node": "root-self-240",
                    "step": index,
                    "row": row_index,
                },
            }
        )
    prior_rows = root.row_lookup(visible[owner])
    executor: concurrent.futures.ProcessPoolExecutor | None = None
    assignment = (budget, owner, index)
    if workers == 1:
        _worker_init(prior_rows, groups, worlds[owner], covers, assignment)
        checked = map(_worker_row, enumerate(adapted_rows))
    else:
        executor = concurrent.futures.ProcessPoolExecutor(
            max_workers=workers,
            mp_context=multiprocessing.get_context("spawn"),
            initializer=_worker_init,
            initargs=(prior_rows, groups, worlds[owner], covers, assignment),
        )
        checked = executor.map(_worker_row, enumerate(adapted_rows))
    planes: list[tuple[Q, Q, Q]] = []
    events = probes = facets = 0
    try:
        for row_index, (row_events, row_probes, row_facets, row_planes) in enumerate(checked):
            root.remaining(budget)
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
    additions: pilot.Polygon = []
    if step["complete"] is True:
        require(index < 8 and cursor == 1, "r1 complete step angle or index")
        additions = root.first_step.check_kernel(step, groups[owner], planes)
        next_group = pilot.hull([*groups[owner], *additions])
        require(
            all(
                root.match_geometry(
                    source["next_prior"][str(other)],
                    next_group if other == owner else group,
                )
                for other, group in groups.items()
            ),
            "r1 next step does not consume accepted owner update",
        )
        groups[owner] = next_group
        cells[owner] = rows
    else:
        require(
            index == 8
            and cursor < 1
            and step["common_owned_kernel"] == []
            and step.get("inner_grid_compression") is None,
            "unsupported r1 partial step promotion",
        )
    root.remaining(budget)
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


def run(args: argparse.Namespace) -> dict[str, Any]:
    started = time.monotonic()
    budget = geometry.Budget(started + args.max_seconds, args.max_events)
    result: dict[str, Any] = {
        "status": "INCOMPLETE",
        "r1_node_state_checked": False,
        "capture_tree_proved": False,
        "candidate_capture_proved": False,
        "global_optimality_proved": False,
        "checker_sha256": pilot.digest(Path(__file__)),
        "branch_pilot_sha256": BRANCH_PILOT_SHA,
        "root_result_sha256": branch.ROOT_RESULT_SHA,
        "root_source_sha256": bridge.ROOT_SOURCE_SHA,
        "r1_source_sha256": branch.R1_SOURCE_SHA,
        "max_seconds": args.max_seconds,
        "max_events_per_cover": args.max_events,
        "workers": args.workers,
        "steps": [],
    }
    try:
        require(
            math.isfinite(args.max_seconds)
            and args.max_seconds > 0
            and args.max_events > 0
            and 1 <= args.workers <= 2,
            "positive bounded r1 replay parameters",
        )
        require(sources_unchanged(), "imported proof source changed")
        branch.root_receipt_digest(args.root_result)
        require(pilot.digest(args.root_source) == bridge.ROOT_SOURCE_SHA, "root source changed")
        require(pilot.digest(args.r1_source) == branch.R1_SOURCE_SHA, "r1 source changed")
        branch.admit_root_result(geometry.strict_json(args.root_result.read_bytes()))
        parent = root.extract(args.root_source, ".final_state")
        header = root.extract(
            args.r1_source,
            "{schema,node_id,mask_index,mask,U,B,parent,constraints,initial,source,guard_source,step0:.steps[0]}",
        )
        branch.check_r1_header(header, parent)
        groups, cells = branch.branch_state(parent, header["initial"])
        worlds = {owner: pilot.points(parent["world"][owner]) for owner in range(16)}
        for index in range(9):
            root.remaining(budget)
            source = root.extract(
                args.r1_source,
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
                budget=budget,
                progress=result,
            )
            result["steps_checked"] = index + 1
        final = root.extract(args.r1_source, "{final_state,closed,terminal,contradiction}")
        require(
            final["closed"] is False
            and final["terminal"] is True
            and final["contradiction"] is None
            and final["final_state"]["constraints"] == header["constraints"],
            "r1 final condition or closing status differs",
        )
        normalized_final = {**final["final_state"], "constraints": []}
        root.final_state(normalized_final, header, groups, cells, worlds)
        require(
            pilot.digest(args.root_source) == bridge.ROOT_SOURCE_SHA
            and pilot.digest(args.r1_source) == branch.R1_SOURCE_SHA
            and branch.root_receipt_digest(args.root_result) == branch.ROOT_RESULT_SHA
            and pilot.digest(Path(__file__)) == result["checker_sha256"]
            and sources_unchanged(),
            "source changed during r1 node replay",
        )
        root.remaining(budget)
        result.update(status="PASS_R1_NODE_STATE", r1_node_state_checked=True)
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
    parser.add_argument("--r1-source", type=Path, required=True)
    parser.add_argument("--root-result", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--max-seconds", type=float, default=1800)
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
                    "r1_node_state_checked",
                    "wall_seconds",
                    "error",
                )
            }
        )
    )
    return 0 if result["status"] == "PASS_R1_NODE_STATE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
