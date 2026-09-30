"""Check one r1 capture row against the independently accepted root state.

The inherited center cut is checked exactly on every owner-15 outer domain.
The selected row's geometry is replayed, but no ownership update, branch closure,
candidate capture, or global result follows from this diagnostic.
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import subprocess
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools import check_n11_capture_root_bridge as bridge
from devtools import check_n11_capture_root_node as root
from devtools import check_n11_capture_root_pilot as pilot
from devtools import check_n11_optimality_field_mask0 as geometry

ROOT_CHECKER_SHA = "2804989aff9414e712855d099aab659bb645f05cd9b2f72259b97a1d22cefcb8"
ROOT_RESULT_SHA = "0d55007a6c5092c0e276ec4e6a2f8524a32ddc4d527ffa3a930f088ff11bccc4"
R1_SOURCE_SHA = "63c6e29d75491d51aa9abc404e35eb99bc862456f07bf7aa3c20f7b1c9ea5e52"
ROOT_PATH = "/workspace/eleven-square/research/candidate-capture/root-self-240.json"
R1_NODE = "r1-portable-v1"


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def root_receipt_digest(path: Path) -> str:
    digest = pilot.digest(path)
    require(digest == ROOT_RESULT_SHA, "accepted root receipt changed")
    return digest


def admit_root_result(record: dict[str, Any]) -> None:
    require(
        record.get("status") == "PASS_ROOT_NODE_STATE"
        and record.get("root_node_state_checked") is True
        and record.get("capture_tree_proved") is False
        and record.get("candidate_capture_proved") is False
        and record.get("global_optimality_proved") is False
        and record.get("checker_sha256") == ROOT_CHECKER_SHA
        and record.get("root_source_sha256") == bridge.ROOT_SOURCE_SHA
        and record.get("adaptive_sha256") == pilot.ADAPTIVE_SHA
        and record.get("step0_result_sha256") == root.STEP0_RESULT_SHA
        and record.get("collision_backend") == "integer"
        and record.get("row_limit") == 0
        and record.get("stop_step") == 13
        and record.get("steps_checked") == 14
        and len(record.get("steps", [])) == 13
        and [step["index"] for step in record["steps"]] == list(range(1, 14))
        and all(step["complete"] is True for step in record["steps"][:-1])
        and record["steps"][-1]["complete"] is False,
        "complete accepted root-node receipt required",
    )


def center_cut() -> tuple[Q, Q, Q]:
    return Q(), Q(-1), -geometry.B * (geometry.U / 2 + Q(5, 4))


def branch_state(
    parent: dict[str, Any], initial: dict[str, Any]
) -> tuple[dict[int, pilot.Polygon], dict[int, list[dict[str, Any]]]]:
    require(
        set(parent["groups"]) == set(map(str, pilot.MASK))
        and set(parent["cells"]) == set(map(str, pilot.MASK)),
        "parent state owner inventory",
    )
    require(
        set(initial["groups"]) == set(parent["groups"])
        and set(initial["cell_references"]) == set(parent["cells"]),
        "child initial owner inventory",
    )
    groups: dict[int, pilot.Polygon] = {}
    cells: dict[int, list[dict[str, Any]]] = {}
    for owner in pilot.MASK:
        key = str(owner)
        groups[owner] = pilot.hull(pilot.points(parent["groups"][key]))
        require(
            pilot.hull(pilot.points(initial["groups"][key])) == groups[owner],
            "child initial ownership differs from accepted root",
        )
        inherited = parent["cells"][key]
        require(
            initial["cell_references"][key] == [row["reference"] for row in inherited],
            "child initial row references differ from accepted root",
        )
        cells[owner] = copy.deepcopy(inherited)
        if owner == 15:
            for row in cells[owner]:
                original = pilot.hull(pilot.points(row["outer_domain"]))
                clipped = geometry.intersect(original, [center_cut()]) if original else []
                row["outer_domain"] = [[str(x), str(y)] for x, y in pilot.hull(clipped)]
    return groups, cells


def check_r1_header(source: dict[str, Any], parent: dict[str, Any]) -> None:
    require(
        source["schema"] == "exact_branch_owned_hull_v1"
        and source["node_id"] == R1_NODE
        and source["mask_index"] == 438
        and tuple(source["mask"]) == pilot.MASK
        and Q(source["U"]) == geometry.U
        and Q(source["B"]) == geometry.B
        and source["parent"] == {"path": ROOT_PATH, "sha256": bridge.ROOT_SOURCE_SHA}
        and source["source"] == parent["source"]
        and source["guard_source"] == parent["guard_source"],
        "r1 source ancestry or frame differs",
    )
    nx, ny, upper = center_cut()
    require(
        source["constraints"]
        == [
            {
                "owner": 15,
                "normal": [int(nx), int(ny)],
                "upper_field": str(upper),
                "axis": 1,
                "bound_centered_unit": "5/4",
                "keep": "ge",
            }
        ],
        "r1 closed center condition differs",
    )


def run(args: argparse.Namespace) -> dict[str, Any]:
    started = time.monotonic()
    budget = geometry.Budget(started + args.max_seconds, args.max_events)
    result: dict[str, Any] = {
        "status": "INCOMPLETE",
        "selected_row_geometry_checked": False,
        "complete_step_checked": False,
        "branch_capture_proved": False,
        "candidate_capture_proved": False,
        "global_optimality_proved": False,
        "checker_sha256": pilot.digest(Path(__file__)),
        "root_checker_sha256": ROOT_CHECKER_SHA,
        "root_source_sha256": bridge.ROOT_SOURCE_SHA,
        "r1_source_sha256": R1_SOURCE_SHA,
        "root_result_sha256": None,
        "row_index": args.row_index,
        "max_seconds": args.max_seconds,
        "max_events": args.max_events,
    }
    try:
        require(
            math.isfinite(args.max_seconds)
            and args.max_seconds > 0
            and args.max_events > 0
            and args.row_index >= 0,
            "bounded r1 row parameters",
        )
        require(
            root.__file__ is not None
            and pilot.digest(Path(root.__file__)) == ROOT_CHECKER_SHA
            and root.source_unchanged(),
            "imported root proof source changed",
        )
        result["root_result_sha256"] = root_receipt_digest(args.root_result)
        require(pilot.digest(args.root_source) == bridge.ROOT_SOURCE_SHA, "root source changed")
        require(pilot.digest(args.r1_source) == R1_SOURCE_SHA, "r1 source changed")
        root_receipt = geometry.strict_json(args.root_result.read_bytes())
        admit_root_result(root_receipt)
        parent = root.extract(args.root_source, ".final_state")
        source = root.extract(
            args.r1_source,
            "{schema,node_id,mask_index,mask,U,B,parent,constraints,initial,source,guard_source,step0:.steps[0]}",
        )
        check_r1_header(source, parent)
        groups, cells = branch_state(parent, source["initial"])
        step = source["step0"]
        require(
            step["index"] == 0
            and step["owner"] == 15
            and step["complete"] is True
            and step["allowed_half_angle"] == ["0", "1"]
            and {
                int(owner): pilot.hull(pilot.points(value))
                for owner, value in step["prior_owned_hulls"].items()
            }
            == groups,
            "r1 first-step predecessor state differs",
        )
        rows = step["rows"]
        require(0 <= args.row_index < len(rows), "selected r1 row outside source")
        row = rows[args.row_index]
        require(
            row["reference"]
            == {"kind": "phase3", "node": R1_NODE, "step": 0, "row": args.row_index},
            "selected r1 row identity differs",
        )
        used = {region["partner"] for region in row["collision_regions"]}
        covers: dict[int, list[tuple[pilot.Polygon, pilot.Polygon]]] = {}
        admitted = 0
        for partner in sorted(used):
            root.remaining(budget)
            require(partner in pilot.MASK and partner != 15, "invalid collision partner")
            proposal = step["prior_partner_pose_covers"].get(str(partner))
            require(proposal is not None, "used partner cover missing")
            covers[partner], count = root.partner_cover(
                proposal, cells[partner], groups[partner], budget=budget
            )
            admitted += count
        adapted = {
            **row,
            "reference": {
                "kind": "phase3",
                "node": "root-self-240",
                "step": 0,
                "row": args.row_index,
            },
        }
        world = pilot.points(parent["world"][15])
        events, probes, facets, planes = root.check_row(
            adapted,
            args.row_index,
            0,
            15,
            prior_rows=root.row_lookup(cells[15]),
            groups=groups,
            world=world,
            covers=covers,
            budget=budget,
            collision_backend="integer",
        )
        require(
            pilot.digest(args.root_source) == bridge.ROOT_SOURCE_SHA
            and pilot.digest(args.r1_source) == R1_SOURCE_SHA
            and root_receipt_digest(args.root_result) == ROOT_RESULT_SHA
            and pilot.digest(Path(__file__)) == result["checker_sha256"]
            and root.__file__ is not None
            and pilot.digest(Path(root.__file__)) == ROOT_CHECKER_SHA
            and root.source_unchanged(),
            "source changed during r1 row check",
        )
        root.remaining(budget)
        result.update(
            status="PASS_R1_SELECTED_ROW_DIAGNOSTIC",
            selected_row_geometry_checked=True,
            partner_cover_rows=admitted,
            coverage_events=events,
            coverage_probes=probes,
            universal_facet_vertex_checks=facets,
            common_core_planes=len(planes),
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
    parser.add_argument("--root-source", type=Path, required=True)
    parser.add_argument("--r1-source", type=Path, required=True)
    parser.add_argument("--root-result", type=Path, required=True)
    parser.add_argument("--row-index", type=int, default=0)
    parser.add_argument("--max-seconds", type=float, default=30)
    parser.add_argument("--max-events", type=int, default=20000)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = run(args)
    print(
        json.dumps(
            {
                key: result.get(key)
                for key in ("status", "selected_row_geometry_checked", "wall_seconds", "error")
            }
        )
    )
    return 0 if result["status"] == "PASS_R1_SELECTED_ROW_DIAGNOSTIC" else 2


if __name__ == "__main__":
    raise SystemExit(main())
