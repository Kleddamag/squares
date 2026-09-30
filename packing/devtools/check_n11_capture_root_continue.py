"""Independently check one later mask-438 root-induction round.

The accepted previous-round receipt is a premise. Every current owner sees the
same frozen prior state and previous row inventory. A round advances only after
all eleven complete owner results join exactly to the next source state.
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
from devtools import check_n11_capture_root_round1 as first
from devtools import check_n11_closed_degenerate_cover as degenerate
from devtools import check_n11_optimality_field_mask0 as geometry

REPO = Path(__file__).resolve().parents[2]
SOURCE_REVISION = "f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c"
FIRST_SHA = "50eef26bff3aee127e9ad508b1587014514c8e5f1cf9a3214e8ace7a92d88afd"
FIRST_RESULT_SHA = "488f26c0effe528f29d2cc06f60766e2c1f845f2aac93f65b18c0c4d3b5e76a4"
LEGACY_SHA = "dbde306a481333b470f1e2613ff05fd2be65c9711dd135615d65548932cebdd3"
DEGENERATE_SHA = "858c61c3ffa464a12be0fda9a14f802d7d9ea22f9b6aaa2b06c6974f0caa5385"
Point = pilot.Point
Polygon = pilot.Polygon


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require_time(deadline: float, message: str) -> None:
    if time.monotonic() >= deadline:
        raise geometry.IncompleteError(message)


def source_identity() -> None:
    require(pilot.digest(Path(pilot.__file__)) == first.PILOT_SHA, "pilot source changed")
    require(pilot.digest(Path(first.__file__)) == FIRST_SHA, "round-one source changed")
    require(pilot.digest(Path(geometry.__file__)) == pilot.GEOMETRY_SHA, "geometry changed")
    require(pilot.digest(Path(degenerate.__file__)) == DEGENERATE_SHA, "cover helper changed")


def selected_query(index: int) -> str:
    require(1 <= index <= 14, "root round index")
    next_prior = f".rounds[{index}].prior_owned_points" if index < 14 else ".owned_points"
    return (
        "{mask_index,mask,parent_Uplus,parent_side,cover_sha256,seed_sha256,branch,"
        f"round:.rounds[{index - 1}],next_prior:{next_prior}}}"
    )


def extract(adaptive: Path, index: int) -> tuple[dict[str, Any], bytes]:
    raw = subprocess.run(
        ["jq", "-c", selected_query(index), str(adaptive)],
        capture_output=True,
        check=True,
        timeout=20,
    ).stdout
    return geometry.strict_json(raw), raw


def admit_previous(
    previous_receipt: Path,
    previous_source: dict[str, Any],
    previous_bytes: bytes,
    current_source: dict[str, Any],
    index: int,
) -> dict[str, Any]:
    previous_path = previous_receipt / "result.json"
    previous_raw = previous_path.read_bytes()
    if index == 2:
        require(digest(previous_raw) == FIRST_RESULT_SHA, "round-one receipt changed")
    previous = geometry.strict_json(previous_raw)
    expected_checker = (
        FIRST_SHA if index == 2 else LEGACY_SHA if index <= 8 else pilot.digest(Path(__file__))
    )
    require(
        previous["status"] in ("PASS_ONE_ROOT_ROUND", "PASS_CONDITIONAL_ROOT_ROUND")
        and previous["round"] == index - 1
        and previous["owners_completed"] == list(pilot.MASK)
        and previous["adaptive_sha256"] == pilot.ADAPTIVE_SHA
        and previous["seed_sha256"] == pilot.SEED_SHA
        and previous["cover_sha256"] == geometry.COVER_SHA
        and previous["pilot_sha256"] == first.PILOT_SHA
        and previous["geometry_sha256"] == pilot.GEOMETRY_SHA
        and previous["checker_sha256"] == expected_checker
        and (index <= 8 or previous["degenerate_sha256"] == DEGENERATE_SHA),
        "previous independent receipt is not admitted",
    )
    require(
        previous["selected_round_sha256"] == digest(previous_bytes),
        "previous receipt/source differs",
    )
    prior = current_source["round"]["prior_owned_points"]
    require(
        previous_source["next_prior"] == prior
        and previous["next_state_sha256"]
        == digest(json.dumps(prior, separators=(",", ":")).encode()),
        "previous accepted next state differs",
    )
    require(
        previous_source["round"]["index"] == index - 1
        and previous_source["round"]["complete"] is True,
        "previous round source incomplete",
    )
    for owner in pilot.MASK:
        worker_path = previous_receipt / f"owner-{owner:02d}.json"
        worker = geometry.strict_json(worker_path.read_bytes())
        require(
            worker["status"] == "PASS_CONDITIONAL_OWNER_UPDATE"
            and worker["owner"] == owner
            and worker["round_sha256"] == digest(previous_bytes)
            and worker["pilot_sha256"] == first.PILOT_SHA
            and worker["geometry_sha256"] == pilot.GEOMETRY_SHA
            and worker["checker_sha256"] == previous["checker_sha256"]
            and (index <= 8 or worker["degenerate_sha256"] == DEGENERATE_SHA),
            f"previous owner {owner} receipt differs",
        )
    return previous


def inherited_domain(
    row: dict[str, Any],
    previous_rows: list[dict[str, Any]],
    world: Polygon,
    round_index: int,
) -> Polygon:
    lo, hi = (Q(value) for value in row["interval"])
    restriction = row["domain_restriction"]
    old_index = restriction["previous_row"]
    require(type(old_index) is int and 0 <= old_index < len(previous_rows), "previous row")
    old = previous_rows[old_index]
    old_lo, old_hi = (Q(value) for value in old["interval"])
    require(
        restriction["previous_round"] == round_index - 1 and old_lo <= lo < hi <= old_hi,
        "angle interval escapes accepted previous row",
    )
    previous_vertices = [
        point for polygon in old["residual_polygons"] for point in pilot.convex(polygon)
    ]
    if not previous_vertices:
        require(
            restriction["kind"] == "previous_angle_excluded"
            and row["input_domain"] == []
            and row["residual_polygons"] == []
            and row["common_core_strips"] == [],
            "excluded angle retains geometry",
        )
        return []
    require(restriction["kind"] == "previous_residual_outer_support", "support kind")
    require(len(restriction["bounds"]) == 8, "outer support inventory")
    normals = [
        (Q(1), Q()),
        (Q(-1), Q()),
        (Q(), Q(1)),
        (Q(), Q(-1)),
        (Q(1), Q(1)),
        (Q(1), Q(-1)),
        (Q(-1), Q(1)),
        (Q(-1), Q(-1)),
    ]
    lines: list[tuple[Q, Q, Q]] = []
    for bound, expected in zip(restriction["bounds"], normals, strict=True):
        normal = pilot.points([bound["normal"]])[0]
        upper = Q(bound["upper"])
        require(normal == expected, "support normal inventory differs")
        require(
            all(normal[0] * x + normal[1] * y <= upper for x, y in previous_vertices),
            "support cuts accepted previous residual",
        )
        lines.append((normal[0], normal[1], upper))
    domain = geometry.intersect(world, lines)
    require(
        pilot.hull(pilot.points(row["input_domain"])) == pilot.hull(domain),
        "source input domain differs from independent restriction",
    )
    return domain


def checked_row(
    row: dict[str, Any],
    previous_rows: list[dict[str, Any]],
    world: Polygon,
    other_hulls: dict[int, Polygon],
    round_index: int,
    *,
    budget: geometry.Budget,
) -> tuple[dict[str, int], list[tuple[Point, Q, Q]], Polygon]:
    lo, hi = (Q(value) for value in row["interval"])
    domain = inherited_domain(row, previous_rows, world, round_index)
    _, halfwidth, cosine, sine = geometry.row_envelope((lo, hi))
    core = Q(row["core_side"])
    require(
        pilot.strict_core(core, lo, hi, cosine, sine)
        and Q(row["reference_half_angle"]) == (lo + hi) / 2,
        "whole-angle core or reference differs",
    )
    if not domain:
        return {"events": 0, "probes": 0}, [], []
    legal = geometry.intersect(
        domain,
        [
            (Q(1), Q(), geometry.L / 2 + halfwidth),
            (Q(-1), Q(), -geometry.L / 2 + halfwidth),
            (Q(), Q(1), geometry.L / 2 + halfwidth),
            (Q(), Q(-1), -geometry.L / 2 + halfwidth),
        ],
    )
    if not legal:
        require(
            row["residual_polygons"] == [] and row["common_core_strips"] == [],
            "empty legal domain retains geometry",
        )
        return {"events": 0, "probes": 0}, [], []
    corners = [
        (core * (a * cosine - b * sine) / 2, core * (a * sine + b * cosine) / 2)
        for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))
    ]
    forbidden = [
        pilot.hull([(x + u, y + v) for x, y in group for u, v in corners])
        for group in other_hulls.values()
    ]
    residual = [pilot.convex(polygon) for polygon in row["residual_polygons"]]
    regions = forbidden + residual
    coverage = (
        geometry.exact_union_cover(legal, regions, budget=budget)
        if geometry.area2(legal) > 0
        else degenerate.exact_cover_closed_degenerate(legal, regions, budget=budget)
    )
    vertices = [point for polygon in residual for point in polygon]
    strips: list[tuple[Point, Q, Q]] = []
    if vertices:
        for normal in ((cosine, sine), (-sine, cosine)):
            values = [normal[0] * x + normal[1] * y for x, y in vertices]
            strips.append((normal, max(values) - core / 2, min(values) + core / 2))
    proposed = row["common_core_strips"]
    require(len(proposed) == len(strips), "common-core strip inventory differs")
    for item, (normal, lower, upper) in zip(proposed, strips, strict=True):
        require(
            pilot.points([item["normal"]])[0] == normal
            and Q(item["lower"]) == lower
            and Q(item["upper"]) == upper,
            "common-core strip differs",
        )
    return coverage, strips, vertices


def checked_owner(
    cell: dict[str, Any],
    previous_cell: dict[str, Any],
    groups: dict[int, Polygon],
    cover: dict[str, Any],
    round_index: int,
    *,
    budget: geometry.Budget,
    progress: dict[str, Any],
) -> dict[str, Any]:
    owner = cell["owner"]
    require(owner in pilot.MASK and previous_cell["owner"] == owner, "owner differs")
    require(cell["complete"] is True and bool(cell["rows"]), "owner round incomplete")
    world = [(geometry.B * x, geometry.B * y) for x, y in geometry.cell_vertices(cover, owner)]
    other_hulls = {index: pilot.hull(groups[index]) for index in pilot.MASK if index != owner}
    cursor = Q()
    strips: list[tuple[Point, Q, Q]] = []
    vertices: Polygon = []
    retained: list[list[str]] = []
    events = probes = 0
    for row_index, row in enumerate(cell["rows"]):
        if time.monotonic() >= budget.deadline:
            raise geometry.IncompleteError(f"owner {owner} row ceiling after {row_index}")
        lo, hi = (Q(value) for value in row["interval"])
        require(lo == cursor and lo < hi <= 1, "current angle partition gap or overlap")
        coverage, row_strips, row_vertices = checked_row(
            row, previous_cell["rows"], world, other_hulls, round_index, budget=budget
        )
        progress["rows_checked"] = row_index + 1
        events += coverage["events"]
        probes += coverage["probes"]
        if row_vertices:
            strips.extend(row_strips)
            vertices.extend(row_vertices)
            retained.append([str(lo), str(hi)])
        cursor = hi
    require(cursor == 1 and retained == cell["retained_angle_intervals"], "retained rows")
    kernel = pilot.points(cell["common_core_kernel"])
    require(bool(kernel) == bool(vertices), "unsupported empty owner kernel")
    for point in kernel:
        require(all(0 <= value <= geometry.L for value in point), "kernel outside container")
        require(
            all(
                low <= normal[0] * point[0] + normal[1] * point[1] <= high
                for normal, low, high in strips
            ),
            "kernel outside accepted common core",
        )
    if vertices:
        require(
            [
                [
                    str(min(point[axis] for point in vertices)),
                    str(max(point[axis] for point in vertices)),
                ]
                for axis in (0, 1)
            ]
            == cell["center_bounds_field"],
            "center bounds differ",
        )
        new_points = first.compressed_points(cell, groups[owner], kernel)
    else:
        require(cell.get("center_bounds_field") in (None, []), "empty owner center bounds")
        new_points = []
    if time.monotonic() >= budget.deadline:
        raise geometry.IncompleteError(f"owner {owner} deadline after compression")
    return {
        "status": "PASS_CONDITIONAL_OWNER_UPDATE",
        "owner": owner,
        "rows_checked": len(cell["rows"]),
        "retained_rows": len(retained),
        "new_points": [[str(x), str(y)] for x, y in new_points],
        "events": events,
        "probes": probes,
        "root_induction_proved": False,
        "candidate_capture_proved": False,
        "global_optimality_proved": False,
    }


def worker(args: argparse.Namespace) -> int:
    started = time.monotonic()
    cpu_started = time.process_time()
    result: dict[str, Any] = {
        "status": "INCOMPLETE",
        "round": args.round,
        "owner": args.owner,
        "rows_checked": 0,
    }
    try:
        require(2 <= args.round <= 14 and 0 < args.max_owner_seconds <= 30, "worker limits")
        source_identity()
        round_bytes = args.round_source.read_bytes()
        previous_bytes = args.previous_source.read_bytes()
        prior_bytes = args.prior_state.read_bytes()
        require(digest(round_bytes) == args.round_sha256, "current source changed")
        require(digest(previous_bytes) == args.previous_sha256, "previous source changed")
        require(digest(prior_bytes) == args.prior_sha256, "accepted prior changed")
        selected = geometry.strict_json(round_bytes)
        previous_selected = geometry.strict_json(previous_bytes)
        admit_previous(
            args.previous_receipt, previous_selected, previous_bytes, selected, args.round
        )
        state = json.loads(prior_bytes)
        require(isinstance(state, list) and len(state) == 16, "prior inventory")
        require(selected["round"]["prior_owned_points"] == state, "worker prior differs")
        groups = {owner: pilot.points(state[owner]) for owner in range(16)}
        previous_cells = {cell["owner"]: cell for cell in previous_selected["round"]["cells"]}
        cells = {cell["owner"]: cell for cell in selected["round"]["cells"]}
        require(
            sorted(cells) == list(pilot.MASK)
            and sorted(previous_cells) == list(pilot.MASK)
            and len(selected["round"]["cells"])
            == len(previous_selected["round"]["cells"])
            == 11,
            "owner inventory",
        )
        cover = geometry.pinned_gzip(
            pilot.COVER,
            packed_bytes=25016,
            packed_sha=geometry.COVER_LFS_SHA,
            raw_bytes=773471,
            raw_sha=geometry.COVER_SHA,
        )
        result.update(
            checked_owner(
                cells[args.owner],
                previous_cells[args.owner],
                groups,
                cover,
                args.round,
                budget=geometry.Budget(started + args.max_owner_seconds, args.max_events),
                progress=result,
            )
        )
        require(
            digest(args.round_source.read_bytes()) == args.round_sha256
            and digest(args.previous_source.read_bytes()) == args.previous_sha256
            and digest(args.prior_state.read_bytes()) == args.prior_sha256
            and pilot.digest(args.previous_receipt / "result.json")
            == args.previous_result_sha256,
            "worker source changed",
        )
        source_identity()
        require_time(started + args.max_owner_seconds, "worker deadline after source recheck")
    except geometry.IncompleteError as error:
        result.update(status="INCOMPLETE", error=str(error))
    except (ValueError, KeyError, IndexError, TypeError, OSError) as error:
        result.update(status="REFUSED", error=str(error))
    result.update(
        wall_seconds=time.monotonic() - started,
        process_cpu_seconds=time.process_time() - cpu_started,
        round_sha256=args.round_sha256,
        previous_sha256=args.previous_sha256,
        prior_sha256=args.prior_sha256,
        previous_result_sha256=args.previous_result_sha256,
        checker_sha256=pilot.digest(Path(__file__)),
        pilot_sha256=first.PILOT_SHA,
        geometry_sha256=pilot.GEOMETRY_SHA,
        degenerate_sha256=DEGENERATE_SHA,
    )
    atomic_write_text(args.worker_output, json.dumps(result, indent=2, sort_keys=True) + "\n")
    return 0 if result["status"] == "PASS_CONDITIONAL_OWNER_UPDATE" else 2


def require_complete_owners(owner_results: dict[int, dict[str, Any]]) -> None:
    statuses = [item["status"] for item in owner_results.values()]
    require(
        all(status != "REFUSED" for status in statuses),
        "one or more owner updates refused",
    )
    if set(owner_results) != set(pilot.MASK) or any(
        status == "INCOMPLETE" for status in statuses
    ):
        raise geometry.IncompleteError("one or more owner updates incomplete")
    require(
        all(status == "PASS_CONDITIONAL_OWNER_UPDATE" for status in statuses),
        "one or more owner updates refused",
    )


def run(args: argparse.Namespace) -> dict[str, Any]:
    require(Path("/Volumes/spud-ext1").is_mount(), "external scratch unavailable")
    scratch = args.scratch_root.resolve()
    require(scratch.is_relative_to(Path("/Volumes/spud-ext1/agent-scratch")), "scratch path")
    scratch.mkdir(parents=True, exist_ok=True)
    require(
        2 <= args.round <= 14 and 1 <= args.workers <= 3 and 0 < args.max_owner_seconds <= 30,
        "round or worker limits",
    )
    require(not args.out.exists(), "round receipt directory already exists")
    args.out.mkdir(parents=True)
    began = time.monotonic()
    result: dict[str, Any] = {
        "status": "INCOMPLETE",
        "round": args.round,
        "owners_required": list(pilot.MASK),
        "root_induction_proved": False,
        "candidate_capture_proved": False,
        "global_optimality_proved": False,
        "checker_sha256": pilot.digest(Path(__file__)),
        "pilot_sha256": first.PILOT_SHA,
        "geometry_sha256": pilot.GEOMETRY_SHA,
        "degenerate_sha256": DEGENERATE_SHA,
        "source_revision": SOURCE_REVISION,
        "adaptive_sha256": pilot.ADAPTIVE_SHA,
        "seed_sha256": pilot.SEED_SHA,
        "cover_sha256": geometry.COVER_SHA,
        "workers": args.workers,
        "max_owner_seconds": args.max_owner_seconds,
        "max_events_per_geometry_call": args.max_events,
    }
    try:
        source_identity()
        geometry.admit_d4_receipt()
        require(pilot.digest(args.adaptive) == pilot.ADAPTIVE_SHA, "adaptive source changed")
        previous_selected, previous_bytes = extract(args.adaptive, args.round - 1)
        selected, selected_bytes = extract(args.adaptive, args.round)
        require(pilot.digest(args.adaptive) == pilot.ADAPTIVE_SHA, "adaptive extraction drift")
        previous = admit_previous(
            args.previous_receipt, previous_selected, previous_bytes, selected, args.round
        )
        result["previous_result_sha256"] = pilot.digest(args.previous_receipt / "result.json")
        result["previous_selected_sha256"] = digest(previous_bytes)
        result["selected_round_sha256"] = digest(selected_bytes)
        result["accepted_prior_sha256"] = previous["next_state_sha256"]
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
        require(rnd["index"] == args.round and rnd["complete"] is True, "round incomplete")
        require(
            len(rnd["cells"]) == 11
            and sorted(cell["owner"] for cell in rnd["cells"]) == list(pilot.MASK),
            "round owner inventory differs",
        )
        with tempfile.TemporaryDirectory(dir=scratch) as temporary:
            work = Path(temporary)
            current_file, previous_file, prior_file = (
                work / "current.json",
                work / "previous.json",
                work / "prior.json",
            )
            current_file.write_bytes(selected_bytes)
            previous_file.write_bytes(previous_bytes)
            prior = rnd["prior_owned_points"]
            prior_bytes = json.dumps(prior, separators=(",", ":")).encode()
            prior_file.write_bytes(prior_bytes)
            prior_sha = digest(prior_bytes)
            owner_results: dict[int, dict[str, Any]] = {}
            for start in range(0, 11, args.workers):
                batch = list(pilot.MASK[start : start + args.workers])
                processes: list[tuple[int, subprocess.Popen[str], float, Path]] = []
                for owner in batch:
                    output = args.out / f"owner-{owner:02d}.json"
                    command = [
                        sys.executable,
                        "-m",
                        "devtools.check_n11_capture_root_continue",
                        "--worker",
                        "--round",
                        str(args.round),
                        "--round-source",
                        str(current_file),
                        "--round-sha256",
                        digest(selected_bytes),
                        "--previous-source",
                        str(previous_file),
                        "--previous-sha256",
                        digest(previous_bytes),
                        "--prior-state",
                        str(prior_file),
                        "--prior-sha256",
                        prior_sha,
                        "--previous-receipt",
                        str(args.previous_receipt),
                        "--previous-result-sha256",
                        result["previous_result_sha256"],
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
                                1, args.max_owner_seconds + 5 - (time.monotonic() - launched)
                            )
                        )
                    except subprocess.TimeoutExpired:
                        expired = True
                        os.killpg(process.pid, signal.SIGKILL)
                        stdout, stderr = process.communicate()
                    if expired:
                        result.setdefault("timed_out_owners", []).append(owner)
                        continue
                    require(not stdout and not stderr, f"owner {owner} unexpected output")
                    require(
                        output.is_file() and process.returncode in (0, 2),
                        f"owner {owner} crashed",
                    )
                    owner_result = geometry.strict_json(output.read_bytes())
                    require(
                        owner_result.get("round") == args.round
                        and owner_result.get("owner") == owner
                        and owner_result.get("round_sha256") == digest(selected_bytes)
                        and owner_result.get("previous_sha256") == digest(previous_bytes)
                        and owner_result.get("prior_sha256") == prior_sha
                        and owner_result.get("previous_result_sha256")
                        == result["previous_result_sha256"]
                        and owner_result.get("checker_sha256") == result["checker_sha256"]
                        and owner_result.get("pilot_sha256") == first.PILOT_SHA
                        and owner_result.get("geometry_sha256") == pilot.GEOMETRY_SHA
                        and owner_result.get("degenerate_sha256") == DEGENERATE_SHA,
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
            require_complete_owners(owner_results)
            groups = {owner: pilot.points(prior[owner]) for owner in range(16)}
            additions = 0
            for owner in pilot.MASK:
                for point in pilot.points(owner_results[owner]["new_points"]):
                    if point not in groups[owner]:
                        groups[owner].append(point)
                        additions += 1
            require(additions == rnd["added_owned_vertices"], "round additions differ")
            next_state = first.canonical_groups(groups)
            require(next_state == selected["next_prior"], "next-round state differs")
            result["new_owned_points"] = additions
            result["rows_checked"] = sum(
                item["rows_checked"] for item in owner_results.values()
            )
            result["next_state_sha256"] = digest(
                json.dumps(next_state, separators=(",", ":")).encode()
            )
            require(
                pilot.digest(args.adaptive) == pilot.ADAPTIVE_SHA
                and pilot.digest(args.previous_receipt / "result.json")
                == result["previous_result_sha256"]
                and pilot.digest(Path(__file__)) == result["checker_sha256"],
                "round source changed",
            )
            source_identity()
            result["status"] = "PASS_CONDITIONAL_ROOT_ROUND"
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
    parser.add_argument("--round", type=int, required=True)
    parser.add_argument("--round-source", type=Path)
    parser.add_argument("--round-sha256")
    parser.add_argument("--previous-source", type=Path)
    parser.add_argument("--previous-sha256")
    parser.add_argument("--prior-state", type=Path)
    parser.add_argument("--prior-sha256")
    parser.add_argument("--previous-receipt", type=Path, required=True)
    parser.add_argument("--previous-result-sha256")
    parser.add_argument("--owner", type=int)
    parser.add_argument("--worker-output", type=Path)
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
                for key in (
                    "status",
                    "round",
                    "owners_completed",
                    "rows_checked",
                    "wall_seconds",
                    "error",
                )
            }
        )
    )
    return 0 if result["status"] == "PASS_CONDITIONAL_ROOT_ROUND" else 2


if __name__ == "__main__":
    sys.exit(main())
