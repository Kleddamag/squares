"""Replay a pinned capture child with exact inherited center/angle conditions.

The accepted parent's complete source state is the premise. Every row and used
partner sees the full closed branch conditions. A complete all-empty terminal
owner cover closes that node without adding ownership points. Other complete
steps join rows before compression; a final partial step cannot promote state.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import copy
import hashlib
import json
import math
import multiprocessing
import subprocess
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, NamedTuple

from strif import atomic_write_text

from devtools import check_n11_capture_branch_r1 as branch
from devtools import check_n11_capture_branch_r1_node as r1node
from devtools import check_n11_capture_root_bridge as bridge
from devtools import check_n11_capture_root_node as root
from devtools import check_n11_capture_root_pilot as pilot
from devtools import check_n11_capture_transition_pilot as primitive
from devtools import check_n11_optimality_field_mask0 as geometry

R1_NODE_CHECKER_SHA = "3e1bfc6471acc48ccbbce00a5c546f4f7e1e4e0cdd1bb3ce51247bfc94b10ce1"
R1_RESULT_SHA = "677719a04426aa53a9ebe3bf8d597e78079313eec2e387bc6f4e4655fd5610f4"
R1_PATH = "/workspace/eleven-square/research/candidate-capture/tree438-rebuilt/r1.json"
ROOT_FINAL_SHA = "46001c7f39fd2382696f82bd24e1049722ac27b8fc04f0626e124bc50a27e979"
R1_FINAL_SHA = "fd24cc9ef4e3c6a0e61707516e608fe6b4dbb66e791ffd9cc8048b35f812330a"


def center_constraint(keep: str) -> dict[str, Any]:
    sign = 1 if keep == "le" else -1
    return {
        "owner": 15,
        "normal": [0, sign],
        "upper_field": str(sign * geometry.B * (geometry.U / 2 + Q(5, 4))),
        "axis": 1,
        "bound_centered_unit": "5/4",
        "keep": keep,
    }


def angle_constraint(owner: int, bound: Q, keep: str) -> dict[str, Any]:
    return {"kind": "half_angle", "owner": owner, "bound_half_angle": str(bound), "keep": keep}


class Pin(NamedTuple):
    node_id: str
    source_sha: str
    parent_path: str
    parent_source_sha: str
    parent_result_sha: str
    parent_checker_sha: str
    parent_final_sha: str
    parent_status: str
    constraints: list[dict[str, Any]]
    steps: int
    terminal: tuple[int, int] | None


PINS = {
    "far15": Pin(
        "far15y-self-300",
        "e25a5de42cb45d9057660bb6d5942f980672e5d6e6b97e361c10931359c2f486",
        branch.ROOT_PATH,
        bridge.ROOT_SOURCE_SHA,
        branch.ROOT_RESULT_SHA,
        branch.ROOT_CHECKER_SHA,
        ROOT_FINAL_SHA,
        "PASS_ROOT_NODE_STATE",
        [center_constraint("le")],
        8,
        (8, 7),
    ),
    "r10": Pin(
        "r10-portable-v1",
        "58da537ee50dee6f21848f166a4d685961ebae6de4077835e40eef1fc1f89f48",
        R1_PATH,
        branch.R1_SOURCE_SHA,
        R1_RESULT_SHA,
        R1_NODE_CHECKER_SHA,
        R1_FINAL_SHA,
        "PASS_R1_NODE_STATE",
        [center_constraint("ge"), angle_constraint(13, Q(147, 512), "le")],
        13,
        None,
    ),
    "near13": Pin(
        "near13-self-180",
        "a2f30c9246b770a2da91e45489f7b9343c345c105e00333f7ca67ab66b53db09",
        R1_PATH,
        branch.R1_SOURCE_SHA,
        R1_RESULT_SHA,
        R1_NODE_CHECKER_SHA,
        R1_FINAL_SHA,
        "PASS_R1_NODE_STATE",
        [center_constraint("ge"), angle_constraint(13, Q(147, 512), "ge")],
        44,
        None,
    ),
}


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def dependencies_unchanged() -> bool:
    return (
        r1node.__file__ is not None
        and branch.__file__ is not None
        and root.__file__ is not None
        and pilot.digest(Path(r1node.__file__)) == R1_NODE_CHECKER_SHA
        and pilot.digest(Path(branch.__file__)) == r1node.BRANCH_PILOT_SHA
        and pilot.digest(Path(root.__file__)) == branch.ROOT_CHECKER_SHA
        and root.source_unchanged()
    )


def admit_parent(record: dict[str, Any], pin: Pin) -> None:
    require(
        record.get("status") == pin.parent_status
        and record.get("checker_sha256") == pin.parent_checker_sha,
        "parent receipt checker or accepted scope differs",
    )
    if pin.parent_source_sha == bridge.ROOT_SOURCE_SHA:
        branch.admit_root_result(record)
    else:
        require(
            record.get("status") == "PASS_R1_NODE_STATE"
            and record.get("r1_node_state_checked") is True
            and record.get("capture_tree_proved") is False
            and record.get("candidate_capture_proved") is False
            and record.get("global_optimality_proved") is False
            and record.get("checker_sha256") == R1_NODE_CHECKER_SHA
            and record.get("r1_source_sha256") == branch.R1_SOURCE_SHA
            and record.get("root_result_sha256") == branch.ROOT_RESULT_SHA
            and record.get("steps_checked") == 9
            and len(record.get("steps", [])) == 9
            and [step["index"] for step in record["steps"]] == list(range(9))
            and all(step["complete"] is True for step in record["steps"][:-1])
            and record["steps"][-1]["complete"] is False,
            "accepted complete r1 parent receipt required",
        )


def angle_domain(owner: int, constraints: list[dict[str, Any]]) -> tuple[Q, Q]:
    lo, hi = Q(), Q(1)
    for condition in constraints:
        if condition.get("kind") != "half_angle" or condition["owner"] != owner:
            continue
        bound = Q(condition["bound_half_angle"])
        if condition["keep"] == "ge":
            lo = max(lo, bound)
        else:
            require(condition["keep"] == "le", "unsupported angle direction")
            hi = min(hi, bound)
    require(0 <= lo < hi <= 1, "unsupported empty/singleton angular branch")
    return lo, hi


def center_lines(owner: int, constraints: list[dict[str, Any]]) -> list[tuple[Q, Q, Q]]:
    return [
        (Q(condition["normal"][0]), Q(condition["normal"][1]), Q(condition["upper_field"]))
        for condition in constraints
        if condition.get("kind") != "half_angle" and condition["owner"] == owner
    ]


def conditional_view(
    cells: dict[int, list[dict[str, Any]]], constraints: list[dict[str, Any]]
) -> dict[int, list[dict[str, Any]]]:
    visible: dict[int, list[dict[str, Any]]] = {}
    for owner in pilot.MASK:
        allowed_lo, allowed_hi = angle_domain(owner, constraints)
        lines = center_lines(owner, constraints)
        cursor = allowed_lo
        retained: list[dict[str, Any]] = []
        for original in cells[owner]:
            old_lo, old_hi = (Q(value) for value in original["interval"])
            lo, hi = max(old_lo, allowed_lo), min(old_hi, allowed_hi)
            if lo >= hi:
                continue
            require(lo == cursor, "inherited closed angular cover gap or overlap")
            cursor = hi
            row = copy.deepcopy(original)
            row["interval"] = [str(lo), str(hi)]
            outer = pilot.hull(pilot.points(row["outer_domain"]))
            clipped = geometry.intersect(outer, lines) if outer and lines else outer
            row["outer_domain"] = [[str(x), str(y)] for x, y in pilot.hull(clipped)]
            retained.append(row)
        require(bool(retained) and cursor == allowed_hi, "inherited closed angle incomplete")
        visible[owner] = retained
    return visible


def initial_state(
    parent: dict[str, Any], initial: dict[str, Any]
) -> tuple[dict[int, pilot.Polygon], dict[int, list[dict[str, Any]]]]:
    require(
        set(parent["groups"]) == set(map(str, pilot.MASK))
        and set(parent["cells"]) == set(map(str, pilot.MASK))
        and set(initial["groups"]) == set(parent["groups"])
        and set(initial["cell_references"]) == set(parent["cells"]),
        "child/parent owner inventory",
    )
    groups: dict[int, pilot.Polygon] = {}
    cells: dict[int, list[dict[str, Any]]] = {}
    for owner in pilot.MASK:
        key = str(owner)
        groups[owner] = pilot.hull(pilot.points(parent["groups"][key]))
        require(
            pilot.hull(pilot.points(initial["groups"][key])) == groups[owner]
            and initial["cell_references"][key]
            == [row["reference"] for row in parent["cells"][key]],
            "child initial state differs from accepted parent",
        )
        cells[owner] = copy.deepcopy(parent["cells"][key])
    return groups, cells


def check_header(source: dict[str, Any], parent: dict[str, Any], pin: Pin) -> None:
    require(
        source["schema"] == "exact_branch_owned_hull_v1"
        and source["node_id"] == pin.node_id
        and source["mask_index"] == 438
        and tuple(source["mask"]) == pilot.MASK
        and Q(source["U"]) == geometry.U
        and Q(source["B"]) == geometry.B
        and source["parent"] == {"path": pin.parent_path, "sha256": pin.parent_source_sha}
        and source["constraints"] == pin.constraints
        and source["source"] == parent["source"]
        and source["guard_source"] == parent["guard_source"],
        "pinned child ancestry, condition, or frame differs",
    )
    require(
        parent["constraints"] == pin.constraints[:-1]
        or parent["constraints"] == pin.constraints,
        "child condition not inherited from parent",
    )


def canonical_sha(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def terminal_rows_empty(rows: list[dict[str, Any]]) -> bool:
    return all(row["residual_polygons"] == [] and row["outer_domain"] == [] for row in rows)


def check_next_prior(
    next_prior: Any,
    groups: dict[int, pilot.Polygon],
    owner: int,
    next_group: pilot.Polygon,
    *,
    index: int,
    pin: Pin,
) -> None:
    if index == pin.steps - 1:
        require(
            pin.terminal is None and next_prior is None,
            "final complete child step has unsupported successor",
        )
        return
    require(isinstance(next_prior, dict), "missing next child ownership state")
    require(
        all(
            root.match_geometry(next_prior[str(other)], next_group if other == owner else group)
            for other, group in groups.items()
        ),
        "next child step does not consume accepted owner update",
    )


def partner_cover(
    proposed: list[dict[str, Any]],
    prior_rows: list[dict[str, Any]],
    owned: pilot.Polygon,
    *,
    allowed: tuple[Q, Q],
    budget: geometry.Budget,
) -> tuple[list[tuple[pilot.Polygon, pilot.Polygon]], int]:
    lookup = root.row_lookup(prior_rows)
    require(bool(proposed), "missing used partner cover")
    cursor = allowed[0]
    live: list[tuple[pilot.Polygon, pilot.Polygon]] = []
    for row in proposed:
        root.remaining(budget)
        adapted = {**row, "prior_reference": row["reference"]}
        lo, hi, domain = root.inherited_domain(adapted, lookup, owned)
        require(lo == cursor and hi <= allowed[1], "partner closed angle gap or overflow")
        cursor = hi
        require(root.match_geometry(row["domain"], domain), "partner center domain differs")
        if domain:
            core = pilot.convex(row["core"])
            primitive.strict_core(core, lo, hi)
            live.append((domain, core))
        else:
            require(row["core"] == [], "empty partner domain has core")
    require(cursor == allowed[1], "used partner angle cover incomplete")
    return live, len(proposed)


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
        raise ValueError("child row worker state missing")
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
    pin: Pin,
    *,
    workers: int,
    budget: geometry.Budget,
    progress: dict[str, Any],
) -> None:
    step = source["step"]
    index, owner = step["index"], step["owner"]
    require(
        type(index) is int and 0 <= index < pin.steps and owner in pilot.MASK,
        "child step identity",
    )
    allowed = angle_domain(owner, pin.constraints)
    require(
        [Q(value) for value in step["allowed_half_angle"]] == list(allowed),
        "child step angle scope",
    )
    require(
        {
            int(key): pilot.hull(pilot.points(value))
            for key, value in step["prior_owned_hulls"].items()
        }
        == groups,
        "child step prior ownership differs",
    )
    rows = step["rows"]
    require(bool(rows), "empty child step rows")
    visible = conditional_view(cells, pin.constraints)
    used = {region["partner"] for row in rows for region in row["collision_regions"]}
    require(
        all(partner in pilot.MASK and partner != owner for partner in used),
        "child partner inventory",
    )
    covers: dict[int, list[tuple[pilot.Polygon, pilot.Polygon]]] = {}
    admitted_cover_rows = 0
    for partner in sorted(used):
        root.remaining(budget)
        proposal = step["prior_partner_pose_covers"].get(str(partner))
        require(proposal is not None, "used child partner cover missing")
        covers[partner], count = partner_cover(
            proposal,
            visible[partner],
            groups[partner],
            allowed=angle_domain(partner, pin.constraints),
            budget=budget,
        )
        admitted_cover_rows += count
    cursor = allowed[0]
    adapted_rows: list[dict[str, Any]] = []
    for row_index, row in enumerate(rows):
        root.remaining(budget)
        require(
            row["reference"]
            == {"kind": "phase3", "node": pin.node_id, "step": index, "row": row_index},
            "child row identity differs",
        )
        lo, hi = (Q(value) for value in row["interval"])
        require(
            lo == cursor and lo < hi <= allowed[1], "child step closed angle gap or overlap"
        )
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
    terminal = pin.terminal == (owner, index)
    additions: pilot.Polygon = []
    if terminal:
        require(
            step["complete"] is True
            and index == pin.steps - 1
            and cursor == allowed[1]
            and step.get("inner_grid_compression") is None
            and terminal_rows_empty(rows),
            "terminal child poses not all independently excluded",
        )
        cells[owner] = rows
        progress["terminal_empty_pose_checked"] = True
    elif step["complete"] is True:
        require(cursor == allowed[1], "complete child step angle")
        additions = root.first_step.check_kernel(step, groups[owner], planes)
        next_group = pilot.hull([*groups[owner], *additions])
        check_next_prior(source["next_prior"], groups, owner, next_group, index=index, pin=pin)
        groups[owner] = next_group
        cells[owner] = rows
    else:
        require(
            pin.terminal is None
            and index == pin.steps - 1
            and cursor < allowed[1]
            and step["common_owned_kernel"] == []
            and step.get("inner_grid_compression") is None,
            "unsupported child partial-step promotion",
        )
    root.remaining(budget)
    progress["steps"].append(
        {
            "index": index,
            "owner": owner,
            "complete": step["complete"],
            "terminal": terminal,
            "rows_checked": len(rows),
            "partner_cover_rows": admitted_cover_rows,
            "coverage_events": events,
            "coverage_probes": probes,
            "universal_facet_vertex_checks": facets,
            "common_core_planes": len(planes),
            "compressed_additions": len(additions),
        }
    )


def run(args: argparse.Namespace) -> dict[str, Any]:
    started = time.monotonic()
    budget = geometry.Budget(started + args.max_seconds, args.max_events)
    result: dict[str, Any] = {
        "status": "INCOMPLETE",
        "child_node_state_checked": False,
        "terminal_empty_pose_checked": False,
        "capture_tree_proved": False,
        "candidate_capture_proved": False,
        "global_optimality_proved": False,
        "checker_sha256": pilot.digest(Path(__file__)),
        "node": args.node,
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
            and 1 <= args.workers <= 3
            and args.node in PINS,
            "positive bounded pinned child replay parameters",
        )
        pin = PINS[args.node]
        result.update(
            child_source_sha256=pin.source_sha,
            parent_source_sha256=pin.parent_source_sha,
            parent_result_sha256=pin.parent_result_sha,
            node_id=pin.node_id,
            constraints=pin.constraints,
        )
        require(dependencies_unchanged(), "imported child proof source changed")
        require(
            pilot.digest(args.parent_result) == pin.parent_result_sha,
            "accepted parent receipt changed",
        )
        require(
            pilot.digest(args.parent_source) == pin.parent_source_sha,
            "accepted parent source changed",
        )
        require(pilot.digest(args.child_source) == pin.source_sha, "child source changed")
        admit_parent(geometry.strict_json(args.parent_result.read_bytes()), pin)
        parent = root.extract(args.parent_source, ".final_state")
        require(
            canonical_sha(parent) == pin.parent_final_sha, "accepted parent final state differs"
        )
        header = root.extract(
            args.child_source,
            "{schema,node_id,mask_index,mask,U,B,parent,constraints,initial,source,guard_source}",
        )
        check_header(header, parent, pin)
        groups, cells = initial_state(parent, header["initial"])
        worlds = {owner: pilot.points(parent["world"][owner]) for owner in range(16)}
        for index in range(pin.steps):
            root.remaining(budget)
            source = root.extract(
                args.child_source,
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
                pin,
                workers=args.workers,
                budget=budget,
                progress=result,
            )
            result["steps_checked"] = index + 1
        final = root.extract(args.child_source, "{final_state,closed,terminal,contradiction}")
        if pin.terminal is None:
            require(
                final["closed"] is False
                and final["terminal"] is True
                and final["contradiction"] is None,
                "nonterminal child closing status differs",
            )
        else:
            owner, step_index = pin.terminal
            require(
                final["closed"] is True
                and final["terminal"] is True
                and final["contradiction"]
                == {
                    "kind": "all_parent_poses_forbidden",
                    "owner": owner,
                    "step": step_index,
                }
                and result["terminal_empty_pose_checked"] is True,
                "terminal child contradiction differs",
            )
        require(
            final["final_state"]["constraints"] == pin.constraints,
            "final child conditions differ",
        )
        normalized_final = {**final["final_state"], "constraints": []}
        root.final_state(normalized_final, header, groups, cells, worlds)
        result["final_state_canonical_sha256"] = canonical_sha(final["final_state"])
        require(
            pilot.digest(args.parent_result) == pin.parent_result_sha
            and pilot.digest(args.parent_source) == pin.parent_source_sha
            and pilot.digest(args.child_source) == pin.source_sha
            and pilot.digest(Path(__file__)) == result["checker_sha256"]
            and dependencies_unchanged(),
            "source changed during child-node replay",
        )
        root.remaining(budget)
        result.update(
            status="PASS_CHILD_TERMINAL_CONTRADICTION"
            if pin.terminal
            else "PASS_CHILD_NODE_STATE",
            child_node_state_checked=True,
        )
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
    parser.add_argument("--node", choices=sorted(PINS), required=True)
    parser.add_argument("--parent-source", type=Path, required=True)
    parser.add_argument("--child-source", type=Path, required=True)
    parser.add_argument("--parent-result", type=Path, required=True)
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
                    "child_node_state_checked",
                    "terminal_empty_pose_checked",
                    "wall_seconds",
                    "error",
                )
            }
        )
    )
    return 0 if result["status"].startswith("PASS_CHILD_") else 2


if __name__ == "__main__":
    raise SystemExit(main())
