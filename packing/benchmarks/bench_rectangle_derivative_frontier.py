"""Measure an exact derivative bound on one fresh native n11 frontier, without proof credit."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import platform
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any, NoReturn

from strif import atomic_write_bytes, atomic_write_text

from benchmarks import bench_rectangle_verifier_parity as supervisor
from devtools import rectangle_derivative_bound as gradient
from devtools import verify_rectangle_density as native_cli
from sqpack import rectangle_density as density

REPO = Path(__file__).resolve().parents[2]
PACKING = REPO / "packing"
EFFECTIVE_CUTOFF = Fraction(2252024993666617, 2251799813685248)


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _incomplete(message: str) -> NoReturn:
    raise gradient.DiagnosticDeadlineError(message)


def _rational(value: object) -> Fraction:
    if type(value) is not str:
        raise ValueError("pending box coordinate must be a rational string")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError("pending box coordinate is not a rational") from error


def _admit_frontier(
    report: object,
    candidate: density.RectangleDensityCandidate,
    *,
    candidate_sha: str,
    checker_sha: str,
) -> tuple[density.PendingBox, ...]:
    """Read all exact pending boxes from this run's complete fixed-work census."""
    _require(isinstance(report, dict), "frontier report is not an object")
    assert isinstance(report, dict)
    expected = {
        "candidate_sha256": candidate_sha,
        "checker_source_sha256": checker_sha,
        "checker": "sqpack.rectangle_density:native-exact-v2",
        "n": 11,
        "L": str(candidate.side),
        "B": str(candidate.core_side),
        "mass": str(candidate.mass),
        "threshold": str(EFFECTIVE_CUTOFF),
        "bound_mode": "common-core",
        "requested_angle_count": 1,
        "angle_count": 1,
        "max_nodes_per_angle": 1000,
        "max_depth": 48,
        "max_seconds": 30.0,
        "retain_pending_boxes": True,
        "status": "INCONCLUSIVE",
    }
    _require(
        all(report.get(key) == value for key, value in expected.items()),
        "frontier input, source, or settings differ",
    )
    _require(
        all(
            type(report.get(key)) is int
            for key in (
                "n",
                "requested_angle_count",
                "angle_count",
                "max_nodes_per_angle",
                "max_depth",
            )
        )
        and type(report.get("max_seconds")) is float
        and type(report.get("retain_pending_boxes")) is bool,
        "frontier numeric or Boolean field type differs",
    )
    rows = report.get("angles")
    _require(isinstance(rows, list) and len(rows) == 1, "frontier angle census differs")
    assert isinstance(rows, list)
    row = rows[0]
    if (
        isinstance(row, dict)
        and type(row.get("index")) is int
        and row["index"] == 1
        and row.get("status") == "INCONCLUSIVE"
        and type(row.get("nodes")) is int
        and 0 <= row["nodes"] <= 1000
        and row.get("stop_cause") == "time_limit"
    ):
        _incomplete("frontier reached its internal deadline")
    _require(
        isinstance(row, dict)
        and type(row.get("index")) is int
        and row["index"] == 1
        and row.get("status") == "INCONCLUSIVE"
        and type(row.get("nodes")) is int
        and row["nodes"] == 1000
        and type(row.get("accepted_leaves")) is int
        and row["accepted_leaves"] >= 0
        and row.get("stop_cause") == "node_limit"
        and type(row.get("unresolved_leaves")) is int
        and row["unresolved_leaves"] > 0,
        "frontier did not complete fixed work with pending boxes",
    )
    raw_boxes = row.get("pending_boxes")
    _require(
        isinstance(raw_boxes, list) and len(raw_boxes) == row["unresolved_leaves"],
        "frontier pending inventory is incomplete",
    )
    assert isinstance(raw_boxes, list)
    cosine, sine = density._angle(1)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    extent = candidate.core_side * (cosine + sine) / 2
    legal_low, legal_high = candidate.side / 2, candidate.side - extent
    boxes: list[density.PendingBox] = []
    seen: set[tuple[Fraction, Fraction, Fraction, Fraction]] = set()
    for item in raw_boxes:
        _require(isinstance(item, dict), "pending box is not an object")
        assert isinstance(item, dict)
        _require(
            set(item) == {"angle", "left", "bottom", "right", "top", "depth", "stop_cause"},
            "pending box fields differ",
        )
        _require(
            type(item["angle"]) is int
            and item["angle"] == 1
            and type(item["depth"]) is int
            and 0 <= item["depth"] <= 48
            and item["stop_cause"] in {"node_limit", "depth_limit", "point_box"},
            "pending box metadata differs",
        )
        box = density.PendingBox(
            1,
            _rational(item["left"]),
            _rational(item["bottom"]),
            _rational(item["right"]),
            _rational(item["top"]),
            item["depth"],
            item["stop_cause"],
        )
        _require(
            legal_low <= box.left <= box.right <= legal_high
            and legal_low <= box.bottom <= box.top <= legal_high,
            "pending box lies outside the exact reduced root",
        )
        identity = (box.left, box.bottom, box.right, box.top)
        _require(identity not in seen, "duplicate pending box")
        seen.add(identity)
        _require(box.as_dict() == item, "pending box exact serialization differs")
        boxes.append(box)
    return tuple(boxes)


def _parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--candidate-sha256", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--frontier-outer-seconds", type=float, default=40.0)
    parser.add_argument("--diagnostic-seconds", type=float, default=120.0)
    return parser.parse_args()


def main() -> int:
    args = _parse()
    overall_started = time.monotonic()
    overall_cpu_started = time.process_time()
    if (
        args.out.exists()
        or not math.isfinite(args.frontier_outer_seconds)
        or not 30 < args.frontier_outer_seconds <= 40
        or not math.isfinite(args.diagnostic_seconds)
        or not 0 < args.diagnostic_seconds <= 120
    ):
        print(json.dumps({"status": "REFUSED", "error": "invalid diagnostic settings"}))
        return 1
    checker_path = Path(density.__file__)
    module_path = Path(gradient.__file__)
    cli_path = Path(native_cli.__file__)
    runner_path = Path(__file__)
    supervisor_path = Path(supervisor.__file__)
    try:
        preflight_started = time.monotonic()
        preflight_cpu_started = time.process_time()
        source = args.candidate.resolve()
        _require(source.is_relative_to(REPO), "candidate must be retained in the repository")
        candidate_bytes = source.read_bytes()
        _require(_digest(candidate_bytes) == args.candidate_sha256, "candidate SHA differs")
        relative = source.relative_to(REPO).as_posix()
        committed = subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", f"HEAD:{relative}"], text=True
        ).strip()
        blob = subprocess.check_output(
            ["git", "-C", str(REPO), "hash-object", str(source)], text=True
        ).strip()
        _require(committed == blob, "candidate bytes differ from committed HEAD")
        source_bytes = {
            "checker": checker_path.read_bytes(),
            "gradient": module_path.read_bytes(),
            "cli": cli_path.read_bytes(),
            "runner": runner_path.read_bytes(),
            "supervisor": supervisor_path.read_bytes(),
        }
        git_head = subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True
        ).strip()
        git_dirty = bool(
            subprocess.check_output(
                ["git", "-C", str(REPO), "status", "--porcelain"], text=True
            ).strip()
        )
        candidate = density.load_candidate_bytes(
            candidate_bytes,
            n=11,
            expected_side=Fraction(381, 100),
            target=EFFECTIVE_CUTOFF,
        )
        args.out.mkdir(parents=True)
        command = [
            sys.executable,
            "-m",
            "devtools.verify_rectangle_density",
            str(source),
            "--n",
            "11",
            "--side",
            "381/100",
            "--threshold",
            str(EFFECTIVE_CUTOFF),
            "--angles",
            "1",
            "--max-nodes-per-angle",
            "1000",
            "--max-depth",
            "48",
            "--max-seconds",
            "30.0",
            "--retain-pending-boxes",
            "--timing",
        ]
        preflight_wall = time.monotonic() - preflight_started
        preflight_cpu = time.process_time() - preflight_cpu_started
        frontier_timing, stdout, stderr = supervisor.run_command(
            command, cwd=PACKING, timeout=args.frontier_outer_seconds
        )
        atomic_write_bytes(
            args.out / "frontier.stdout.json.gz", gzip.compress(stdout.encode(), mtime=0)
        )
        atomic_write_text(args.out / "frontier.stderr", stderr)
        if frontier_timing["timed_out"]:
            _incomplete("frontier supervisor deadline reached")
        _require(frontier_timing["exit_code"] == 2, "frontier did not return INCONCLUSIVE")
        diagnostic_started = time.monotonic()
        cpu_started = time.process_time()
        deadline = diagnostic_started + args.diagnostic_seconds
        report = json.loads(stdout)
        boxes = _admit_frontier(
            report,
            candidate,
            candidate_sha=_digest(candidate_bytes),
            checker_sha=_digest(source_bytes["checker"]),
        )
        if time.monotonic() >= deadline:
            _incomplete("diagnostic expired during frontier admission")
        edges = gradient.build_signed_edges(candidate.rectangles, deadline=deadline)
        comparisons: list[dict[str, Any]] = []
        for index, box in enumerate(boxes):
            result = gradient.bound_pending(candidate, box, edges, deadline=deadline)
            comparisons.append(
                {
                    "id": index,
                    "box": box.as_dict(),
                    **result.as_dict(),
                    "closes_old_gap": result.common < candidate.target <= result.combined,
                    "closed_by_new_bound": result.combined >= candidate.target,
                }
            )
        _require(len(comparisons) == len(boxes), "diagnostic inventory is incomplete")
        _require(
            source.read_bytes() == candidate_bytes
            and checker_path.read_bytes() == source_bytes["checker"]
            and module_path.read_bytes() == source_bytes["gradient"]
            and cli_path.read_bytes() == source_bytes["cli"]
            and runner_path.read_bytes() == source_bytes["runner"]
            and supervisor_path.read_bytes() == source_bytes["supervisor"]
            and subprocess.check_output(
                ["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True
            ).strip()
            == git_head,
            "input or source changed during diagnostic",
        )
        if time.monotonic() >= deadline:
            _incomplete("diagnostic expired before final source check")
        diagnostic_wall = time.monotonic() - diagnostic_started
        diagnostic_cpu = time.process_time() - cpu_started
        result_json: dict[str, Any] = {
            "status": "DIAGNOSTIC_ONLY",
            "proof_credit": False,
            "speed_parity_established": False,
            "candidate": relative,
            "candidate_sha256": _digest(candidate_bytes),
            "candidate_git_blob": blob,
            "git_head": git_head,
            "git_dirty_at_start": git_dirty,
            "platform": platform.platform(),
            "python_version": sys.version,
            "sources_sha256": {key: _digest(value) for key, value in source_bytes.items()},
            "frontier_stdout_decoded_sha256": _digest(stdout.encode()),
            "preflight_wall_seconds": preflight_wall,
            "preflight_process_cpu_seconds": preflight_cpu,
            "frontier_process": frontier_timing,
            "frontier": report["angles"][0],
            "effective_threshold": str(EFFECTIVE_CUTOFF),
            "signed_edges_x": len(edges.x),
            "signed_edges_y": len(edges.y),
            "pending_boxes": len(boxes),
            "evaluated_boxes": len(comparisons),
            "newly_closed_boxes": sum(bool(row["closes_old_gap"]) for row in comparisons),
            "diagnostic_wall_seconds": diagnostic_wall,
            "diagnostic_process_cpu_seconds": diagnostic_cpu,
            "total_wall_seconds": time.monotonic() - overall_started,
            "total_process_cpu_seconds": time.process_time() - overall_cpu_started,
            "comparisons": comparisons,
        }
        atomic_write_text(args.out / "result.json", json.dumps(result_json, indent=2) + "\n")
    except (
        density.CandidateError,
        gradient.DiagnosticDeadlineError,
        OSError,
        OverflowError,
        ValueError,
        TypeError,
        subprocess.CalledProcessError,
    ) as error:
        status = (
            "INCOMPLETE" if isinstance(error, gradient.DiagnosticDeadlineError) else "REFUSED"
        )
        if args.out.exists():
            atomic_write_text(
                args.out / "result.json",
                json.dumps(
                    {
                        "status": status,
                        "proof_credit": False,
                        "error": str(error),
                        "total_wall_seconds": time.monotonic() - overall_started,
                        "total_process_cpu_seconds": time.process_time() - overall_cpu_started,
                    }
                )
                + "\n",
            )
        print(json.dumps({"status": status, "error": str(error)}))
        return 2
    print(
        json.dumps(
            {
                "status": "DIAGNOSTIC_ONLY",
                "pending_boxes": len(boxes),
                "newly_closed_boxes": result_json["newly_closed_boxes"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
