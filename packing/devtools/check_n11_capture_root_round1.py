"""Replay all eleven mask-438 root owners from one frozen round-one seed state.

Each owner runs in its own capped process against the same accepted prior state.
Only a complete eleven-owner join advances the state to round two. This remains
one round of fourteen, never a root, capture, or optimality verdict.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools import check_n11_capture_root_pilot as pilot
from devtools import check_n11_optimality_field_mask0 as geometry

REPO = Path(__file__).resolve().parents[2]
SOURCE_REVISION = "f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c"
PILOT_SHA = "1abfc9244d19fcb38a131c3bee676c8973de991998c1e7ab224fae8196259737"
ROW_COUNTS = {0: 72, 1: 72, 2: 69, 3: 72, 4: 72, 8: 72, 9: 69, 10: 69, 11: 69, 13: 69, 15: 72}
Point = pilot.Point
Polygon = pilot.Polygon


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def require_time(deadline: float, message: str) -> None:
    if time.monotonic() >= deadline:
        raise geometry.IncompleteError(message)


def canonical_groups(groups: dict[int, Polygon]) -> list[list[list[str]]]:
    return [[[str(x), str(y)] for x, y in groups[index]] for index in range(16)]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require_complete_owner_results(owner_results: dict[int, dict[str, Any]]) -> None:
    if set(owner_results) != set(pilot.MASK) or any(
        item["status"] == "INCOMPLETE" for item in owner_results.values()
    ):
        raise geometry.IncompleteError("one or more owner updates incomplete")
    statuses = [item["status"] for item in owner_results.values()]
    require(
        all(status == "PASS_CONDITIONAL_OWNER_UPDATE" for status in statuses),
        "one or more owner updates refused",
    )


def compressed_points(cell: dict[str, Any], prior: Polygon, kernel: Polygon) -> Polygon:
    """Recheck every proposed rational compression point from our accepted hull."""

    original = pilot.hull(prior + kernel)
    require(
        pilot.hull(pilot.points(cell["compression_source_hull"])) == original,
        "compression source hull differs",
    )
    receipt = cell["inner_grid_compression"]
    points = pilot.points(receipt["vertices"])
    witnesses = receipt["witnesses"]
    denominator = receipt["denominator"]
    require(
        type(denominator) is int
        and denominator > 0
        and 0 < len(points) == len(witnesses) <= receipt["directions"],
        "compression inventory",
    )
    for point, witness in zip(points, witnesses, strict=True):
        indices = witness["indices"]
        weights = [Q(value) for value in witness["weights"]]
        require(
            1 <= len(indices) == len(weights) <= 3
            and all(type(index) is int and 0 <= index < len(original) for index in indices)
            and all(weight >= 0 for weight in weights)
            and sum(weights) == 1,
            "invalid compression weights",
        )
        require(
            point == pilot.points([witness["point"]])[0]
            and all((coordinate * denominator).denominator == 1 for coordinate in point)
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
            "compressed point is not an exact convex combination",
        )
    return points


def check_owner(
    owner: int,
    cell: dict[str, Any],
    groups: dict[int, Polygon],
    cover: dict[str, Any],
    *,
    budget: geometry.Budget,
    progress: dict[str, Any],
) -> dict[str, Any]:
    require(owner in pilot.MASK and cell["owner"] == owner, "owner identity differs")
    require(
        cell["complete"] is True and len(cell["rows"]) == ROW_COUNTS[owner], "owner row census"
    )
    world = [(geometry.B * x, geometry.B * y) for x, y in geometry.cell_vertices(cover, owner)]
    other_hulls = {index: pilot.hull(groups[index]) for index in pilot.MASK if index != owner}
    cursor = Q()
    strips: list[tuple[Point, Q, Q]] = []
    vertices: Polygon = []
    retained: list[list[str]] = []
    total_events = total_probes = 0
    for row_index, row in enumerate(cell["rows"]):
        if time.monotonic() >= budget.deadline:
            raise geometry.IncompleteError(f"owner {owner} row ceiling after {row_index}")
        lo, hi = (Q(value) for value in row["interval"])
        require(lo == cursor and lo < hi <= 1, "owner angle partition gap or overlap")
        coverage, row_strips, row_vertices = pilot.row_check(
            row, world, other_hulls, budget=budget
        )
        progress["rows_checked"] = row_index + 1
        total_events += coverage["events"]
        total_probes += coverage["probes"]
        if row_vertices:
            strips.extend(row_strips)
            vertices.extend(row_vertices)
            retained.append([str(lo), str(hi)])
        cursor = hi
    require(
        cursor == 1 and retained == cell["retained_angle_intervals"], "incomplete owner angles"
    )
    kernel = pilot.points(cell["common_core_kernel"])
    require(bool(kernel), "owner supplied no kernel points")
    for point in kernel:
        require(all(0 <= value <= geometry.L for value in point), "kernel outside container")
        require(
            all(
                lower <= normal[0] * point[0] + normal[1] * point[1] <= upper
                for normal, lower, upper in strips
            ),
            "kernel point outside accepted common core",
        )
    require(bool(vertices), "owner has no residual vertices")
    require(
        [
            [
                str(min(point[axis] for point in vertices)),
                str(max(point[axis] for point in vertices)),
            ]
            for axis in (0, 1)
        ]
        == cell["center_bounds_field"],
        "owner center bounds differ",
    )
    output = compressed_points(cell, groups[owner], kernel)
    if time.monotonic() >= budget.deadline:
        raise geometry.IncompleteError(f"owner {owner} deadline after compression")
    return {
        "status": "PASS_CONDITIONAL_OWNER_UPDATE",
        "owner": owner,
        "rows_checked": len(cell["rows"]),
        "kernel_points": len(kernel),
        "new_points": [[str(x), str(y)] for x, y in output],
        "events": total_events,
        "probes": total_probes,
        "root_induction_proved": False,
        "candidate_capture_proved": False,
        "global_optimality_proved": False,
    }


def worker(args: argparse.Namespace) -> int:
    started = time.monotonic()
    cpu_started = time.process_time()
    result: dict[str, Any] = {"status": "INCOMPLETE", "owner": args.owner, "rows_checked": 0}
    try:
        require(0 < args.max_owner_seconds <= 30, "owner ceiling must be <=30")
        require(pilot.digest(Path(pilot.__file__)) == PILOT_SHA, "pilot source changed")
        require(
            pilot.digest(Path(geometry.__file__)) == pilot.GEOMETRY_SHA,
            "shared geometry source changed",
        )
        round_bytes = args.round_source.read_bytes()
        state_bytes = args.prior_state.read_bytes()
        require(digest(round_bytes) == args.round_sha256, "round source changed")
        require(digest(state_bytes) == args.prior_sha256, "accepted prior changed")
        selected = geometry.strict_json(round_bytes)
        state = json.loads(state_bytes)
        require(isinstance(state, list) and len(state) == 16, "prior state inventory")
        groups = {owner: pilot.points(state[owner]) for owner in range(16)}
        rnd = selected["round"]
        require(
            rnd["index"] == 1 and rnd["prior_owned_points"] == state, "source prior differs"
        )
        cells = {cell["owner"]: cell for cell in rnd["cells"]}
        require(sorted(cells) == list(pilot.MASK) and len(rnd["cells"]) == 11, "owner census")
        cover = geometry.pinned_gzip(
            pilot.COVER,
            packed_bytes=25016,
            packed_sha=geometry.COVER_LFS_SHA,
            raw_bytes=773471,
            raw_sha=geometry.COVER_SHA,
        )
        result.update(
            check_owner(
                args.owner,
                cells[args.owner],
                groups,
                cover,
                budget=geometry.Budget(started + args.max_owner_seconds, args.max_events),
                progress=result,
            )
        )
        require(
            digest(args.round_source.read_bytes()) == args.round_sha256
            and digest(args.prior_state.read_bytes()) == args.prior_sha256
            and pilot.digest(Path(pilot.__file__)) == PILOT_SHA
            and pilot.digest(Path(geometry.__file__)) == pilot.GEOMETRY_SHA,
            "worker source changed",
        )
        require_time(started + args.max_owner_seconds, "owner deadline after source recheck")
    except geometry.IncompleteError as error:
        result.update(status="INCOMPLETE", error=str(error))
    except (ValueError, KeyError, IndexError, TypeError, OSError) as error:
        result.update(status="REFUSED", error=str(error))
    result.update(
        wall_seconds=time.monotonic() - started,
        process_cpu_seconds=time.process_time() - cpu_started,
        round_sha256=args.round_sha256,
        prior_sha256=args.prior_sha256,
        checker_sha256=pilot.digest(Path(__file__)),
        pilot_sha256=PILOT_SHA,
        geometry_sha256=pilot.GEOMETRY_SHA,
    )
    atomic_write_text(args.worker_output, json.dumps(result, indent=2, sort_keys=True) + "\n")
    return 0 if result["status"] == "PASS_CONDITIONAL_OWNER_UPDATE" else 2


def run(args: argparse.Namespace) -> dict[str, Any]:
    require(Path("/Volumes/spud-ext1").is_mount(), "external scratch volume unavailable")
    scratch = args.scratch_root.resolve()
    require(scratch.is_relative_to(Path("/Volumes/spud-ext1/agent-scratch")), "scratch path")
    scratch.mkdir(parents=True, exist_ok=True)
    require(1 <= args.workers <= 3 and 0 < args.max_owner_seconds <= 30, "worker limits")
    require(not args.out.exists(), "round receipt directory already exists")
    args.out.mkdir(parents=True)
    began = time.monotonic()
    result: dict[str, Any] = {
        "status": "INCOMPLETE",
        "round": 1,
        "owners_required": list(pilot.MASK),
        "root_induction_proved": False,
        "candidate_capture_proved": False,
        "global_optimality_proved": False,
        "checker_sha256": pilot.digest(Path(__file__)),
        "pilot_sha256": PILOT_SHA,
        "geometry_sha256": pilot.GEOMETRY_SHA,
        "source_revision": SOURCE_REVISION,
        "adaptive_sha256": pilot.ADAPTIVE_SHA,
        "seed_sha256": pilot.SEED_SHA,
        "cover_sha256": geometry.COVER_SHA,
        "workers": args.workers,
        "max_owner_seconds": args.max_owner_seconds,
        "max_events_per_geometry_call": args.max_events,
    }
    try:
        require(pilot.digest(Path(pilot.__file__)) == PILOT_SHA, "pilot source changed")
        require(pilot.digest(Path(geometry.__file__)) == pilot.GEOMETRY_SHA, "geometry changed")
        geometry.admit_d4_receipt()
        cover = geometry.pinned_gzip(
            pilot.COVER,
            packed_bytes=25016,
            packed_sha=geometry.COVER_LFS_SHA,
            raw_bytes=773471,
            raw_sha=geometry.COVER_SHA,
        )
        require(pilot.digest(args.seed) == pilot.SEED_SHA, "seed source changed")
        require(pilot.digest(args.adaptive) == pilot.ADAPTIVE_SHA, "adaptive source changed")
        seed = geometry.strict_json(args.seed.read_bytes())
        groups = pilot.seed_points(
            seed, cover, budget=geometry.Budget(time.monotonic() + 30, args.max_events)
        )
        result["seed_points_checked"] = 130
        query = (
            "{mask_index,mask,parent_Uplus,parent_side,cover_sha256,seed_sha256,branch,"
            "round:.rounds[0],next_prior:.rounds[1].prior_owned_points}"
        )
        extracted = subprocess.run(
            ["jq", "-c", query, str(args.adaptive)],
            capture_output=True,
            check=True,
            timeout=20,
        ).stdout
        selected = geometry.strict_json(extracted)
        require(pilot.digest(args.adaptive) == pilot.ADAPTIVE_SHA, "adaptive extraction drift")
        require(
            selected["mask_index"] == 438
            and tuple(selected["mask"]) == pilot.MASK
            and Q(selected["parent_Uplus"]) == geometry.U
            and Q(selected["parent_side"]) == geometry.B
            and selected["cover_sha256"] == geometry.COVER_SHA
            and selected["seed_sha256"] == pilot.SEED_SHA
            and selected.get("branch") is None,
            "adaptive root premises differ",
        )
        rnd = selected["round"]
        require(rnd["index"] == 1 and rnd["complete"] is True, "round one incomplete")
        require(rnd["prior_owned_points"] == canonical_groups(groups), "prior seed differs")
        cells = rnd["cells"]
        require(
            len(cells) == 11
            and {cell["owner"]: len(cell["rows"]) for cell in cells} == ROW_COUNTS,
            "round-one owner/row census differs",
        )
        selected_sha = digest(extracted)
        result["selected_round_sha256"] = selected_sha
        with tempfile.TemporaryDirectory(dir=scratch) as temporary:
            work = Path(temporary)
            source_file = work / "round1.json"
            prior_file = work / "prior.json"
            source_file.write_bytes(extracted)
            prior_bytes = json.dumps(canonical_groups(groups), separators=(",", ":")).encode()
            prior_file.write_bytes(prior_bytes)
            prior_sha = digest(prior_bytes)
            result["accepted_prior_sha256"] = prior_sha
            owner_results: dict[int, dict[str, Any]] = {}
            for start in range(0, 11, args.workers):
                batch = list(pilot.MASK[start : start + args.workers])
                processes: list[tuple[int, subprocess.Popen[str], float, Path]] = []
                for owner in batch:
                    output = args.out / f"owner-{owner:02d}.json"
                    command = [
                        sys.executable,
                        "-m",
                        "devtools.check_n11_capture_root_round1",
                        "--worker",
                        "--round-source",
                        str(source_file),
                        "--round-sha256",
                        selected_sha,
                        "--prior-state",
                        str(prior_file),
                        "--prior-sha256",
                        prior_sha,
                        "--owner",
                        str(owner),
                        "--max-owner-seconds",
                        str(args.max_owner_seconds),
                        "--max-events",
                        str(args.max_events),
                        "--worker-output",
                        str(output),
                    ]
                    launched = time.monotonic()
                    process = subprocess.Popen(
                        command,
                        cwd=REPO / "packing",
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        start_new_session=True,
                    )
                    processes.append((owner, process, launched, output))
                for owner, process, launched, output in processes:
                    expired = False
                    try:
                        stdout, stderr = process.communicate(
                            timeout=max(
                                0.1, args.max_owner_seconds + 5 - (time.monotonic() - launched)
                            )
                        )
                    except subprocess.TimeoutExpired:
                        expired = True
                        os.killpg(process.pid, signal.SIGKILL)
                        stdout, stderr = process.communicate()
                    if expired:
                        result.setdefault("timed_out_owners", []).append(owner)
                        continue
                    require(
                        not stderr and not stdout, f"owner {owner} unexpected process output"
                    )
                    require(
                        output.is_file() and process.returncode in (0, 2),
                        f"owner {owner} crashed",
                    )
                    owner_result = geometry.strict_json(output.read_bytes())
                    require(
                        owner_result.get("round_sha256") == selected_sha
                        and owner_result.get("prior_sha256") == prior_sha
                        and owner_result.get("checker_sha256") == result["checker_sha256"]
                        and owner_result.get("pilot_sha256") == PILOT_SHA
                        and owner_result.get("geometry_sha256") == pilot.GEOMETRY_SHA,
                        f"owner {owner} worker binding differs",
                    )
                    owner_results[owner] = owner_result
                result["owners_completed"] = sorted(
                    owner
                    for owner, item in owner_results.items()
                    if item["status"] == "PASS_CONDITIONAL_OWNER_UPDATE"
                )
                if len(owner_results) < start + len(batch) or any(
                    item["status"] != "PASS_CONDITIONAL_OWNER_UPDATE"
                    for item in owner_results.values()
                ):
                    break
            require_complete_owner_results(owner_results)
            new_groups = {index: list(points) for index, points in groups.items()}
            additions = 0
            for owner in pilot.MASK:
                for point in pilot.points(owner_results[owner]["new_points"]):
                    if point not in new_groups[owner]:
                        new_groups[owner].append(point)
                        additions += 1
            require(additions == rnd["added_owned_vertices"] == 100, "round additions differ")
            require(
                canonical_groups(new_groups) == selected["next_prior"],
                "next-round state differs",
            )
            result["new_owned_points"] = additions
            result["next_state_sha256"] = digest(
                json.dumps(canonical_groups(new_groups), separators=(",", ":")).encode()
            )
            require(
                pilot.digest(args.seed) == pilot.SEED_SHA
                and pilot.digest(args.adaptive) == pilot.ADAPTIVE_SHA
                and pilot.digest(Path(pilot.__file__)) == PILOT_SHA
                and pilot.digest(Path(geometry.__file__)) == pilot.GEOMETRY_SHA
                and pilot.digest(Path(__file__)) == result["checker_sha256"],
                "round source changed",
            )
            result["status"] = "PASS_ONE_ROOT_ROUND"
    except (geometry.IncompleteError, subprocess.TimeoutExpired) as error:
        result["error"] = str(error)
    except (
        ValueError,
        KeyError,
        IndexError,
        TypeError,
        OSError,
        subprocess.CalledProcessError,
    ) as error:
        result.update(status="REFUSED", error=str(error))
    result["wall_seconds"] = time.monotonic() - began
    atomic_write_text(
        args.out / "result.json", json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--round-source", type=Path)
    parser.add_argument("--round-sha256")
    parser.add_argument("--prior-state", type=Path)
    parser.add_argument("--prior-sha256")
    parser.add_argument("--owner", type=int)
    parser.add_argument("--worker-output", type=Path)
    parser.add_argument("--seed", type=Path)
    parser.add_argument("--adaptive", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--scratch-root", type=Path)
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--max-owner-seconds", type=float, default=30)
    parser.add_argument("--max-events", type=int, default=100_000)
    args = parser.parse_args()
    if args.worker:
        return worker(args)
    result = run(args)
    print(
        json.dumps(
            {
                key: result.get(key)
                for key in ("status", "owners_completed", "wall_seconds", "error")
            }
        )
    )
    return 0 if result["status"] == "PASS_ONE_ROOT_ROUND" else 2


if __name__ == "__main__":
    sys.exit(main())
