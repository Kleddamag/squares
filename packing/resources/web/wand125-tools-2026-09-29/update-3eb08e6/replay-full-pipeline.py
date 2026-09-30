"""Replay one bounded upstream n=3 rectangle certificate through real verify.cpp.

Run from the repository root with the project Python 3.14 after sourcing the
mandated external-scratch env.sh. This checks the unmodified upstream process,
not a matched kernel benchmark or an n=11 optimality claim.
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
from contextlib import suppress
from fractions import Fraction
from pathlib import Path
from typing import cast

REPO = Path(__file__).resolve().parents[5]
UPSTREAM = REPO / "attic/wand125-tools"
FIXTURE = REPO / "packing/resources/web/wand125-tools-2026-09-29/native-analytic-control.json"
FIXTURE_SHA = "bfd6e4dea67a048321836c69c9c9fe782687ffc512ccb1afc43249212ba5f01e"
REVISION = "3eb08e6c675d8d5aa953cb93da049a3f3cdc6123"
SOURCE_PATHS = ("solver/certify.py", "solver/run_verify.py", "solver/verify.cpp")
MAX_SECONDS = 60.0
REPLAY_COMMAND = (
    "source /Volumes/spud-ext1/agent-scratch/wand125-tools-01a0ebfc/env.sh && "
    "packing/.venv/bin/python3 "
    "packing/resources/web/wand125-tools-2026-09-29/update-3eb08e6/"
    "replay-full-pipeline.py"
)


def require(condition: object, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git(*args: str) -> bytes:
    return subprocess.check_output(("git", "-C", str(UPSTREAM), *args))


def json_object(raw: bytes) -> dict[str, object]:
    value = cast(object, json.loads(raw))
    require(isinstance(value, dict), "JSON result is not an object")
    return cast(dict[str, object], value)


def source_identities() -> dict[str, str]:
    require(git("rev-parse", "HEAD").decode().strip() == REVISION, "upstream checkout changed")
    result: dict[str, str] = {}
    for path in SOURCE_PATHS:
        raw = (UPSTREAM / path).read_bytes()
        require(raw == git("show", f"{REVISION}:{path}"), f"source bytes changed: {path}")
        result[path] = sha(raw)
    return result


def fixture_identity() -> tuple[bytes, dict[str, object], Fraction]:
    raw = FIXTURE.read_bytes()
    require(sha(raw) == FIXTURE_SHA, "retained analytic fixture changed")
    data = json_object(raw)
    require(type(data.get("n")) is int and data["n"] == 3, "fixture n changed")
    weights = data.get("weights")
    rectangles = data.get("rectangles")
    if not isinstance(weights, list) or not isinstance(rectangles, list):
        raise TypeError("fixture support/weight inventory changed")
    weight_rows = cast(list[object], weights)
    rectangle_rows = cast(list[object], rectangles)
    require(
        len(weight_rows) == len(rectangle_rows)
        and all(isinstance(value, str) for value in weight_rows),
        "fixture support/weight inventory changed",
    )
    mass = sum((Fraction(value) for value in cast(list[str], weight_rows)), Fraction())
    require(0 < mass < 3, "fixture exact mass fails n=3 packing budget")
    require(Fraction(cast(str, data["L"])) == Fraction(3, 2), "fixture L changed")
    require(Fraction(cast(str, data["B"])) == Fraction(9977, 10000), "fixture B changed")
    return raw, data, mass


def file_sha(path: Path) -> str:
    return sha(path.read_bytes())


def checked_result(
    out: Path, raw: bytes, candidate: dict[str, object], mass: Fraction, sources: dict[str, str]
) -> dict[str, object]:
    names = (
        "certificate_input.txt",
        "certificate_metadata.json",
        "verification_summary.json",
        "verified_angles.jsonl",
        "certified_candidate.json",
        "verify.cpp",
        "run_verify.py",
        "verify",
    )
    require(
        all((out / name).is_file() for name in names), "upstream output inventory incomplete"
    )
    meta = json_object((out / "certificate_metadata.json").read_bytes())
    summary = json_object((out / "verification_summary.json").read_bytes())
    final = json_object((out / "certified_candidate.json").read_bytes())
    angles = [
        json_object(line.encode())
        for line in (out / "verified_angles.jsonl").read_text().splitlines()
    ]
    require(meta.get("source_sha256") == sha(raw), "candidate source identity differs")
    require(
        meta.get("input_sha256") == file_sha(out / "certificate_input.txt"),
        "generated input identity differs",
    )
    mass_text = meta.get("mass_exact")
    require(isinstance(mass_text, str) and Fraction(mass_text) == mass, "metadata mass differs")
    require(
        meta.get("angle_count") == 201 and meta.get("rescaled") is False,
        "upstream preparation scope changed",
    )
    require(
        summary.get("status") == "VERIFIED" and summary.get("angle_cases") == 201,
        "upstream summary did not verify all angles",
    )
    require(summary.get("input_sha256") == meta["input_sha256"], "summary input differs")
    require(
        summary.get("verifier_source_sha256") == sources["solver/verify.cpp"],
        "verifier source differs",
    )
    require(summary.get("target_lower_bound_exact") == "10001/10000", "coverage target changed")
    ids: list[int] = []
    for row in angles:
        index, lower = row.get("r"), row.get("lower_bound")
        require(type(index) is int and type(lower) in (int, float), "malformed angle result")
        ids.append(cast(int, index))
        require(
            row.get("status") == "verified" and cast(float, lower) >= 1.0001,
            "one angle is not verified at the target",
        )
    require(
        len(ids) == 201 and sorted(ids) == list(range(201)),
        "angle census is not exactly 0 through 200",
    )
    require(
        final.get("status") == "VERIFIED_CONTINUOUS_DENSITY"
        and final.get("globally_verified") is True,
        "final certified artifact status changed",
    )
    require(
        final.get("certificate") == meta
        and final.get("coverage_lower_bound_exact") == "10001/10000",
        "final certified artifact premise differs",
    )
    require(
        all(
            final.get(key) == candidate.get(key)
            for key in ("n", "L", "B", "rectangles", "weights")
        ),
        "final certified artifact changed the candidate",
    )
    require(
        file_sha(out / "verify.cpp") == sources["solver/verify.cpp"]
        and file_sha(out / "run_verify.py") == sources["solver/run_verify.py"],
        "copied verifier source differs",
    )
    return {
        "status": "PASS_UPSTREAM_201_ANGLE_PIPELINE_ONLY",
        "angle_cases": 201,
        "angle_ids_exactly_0_through_200": True,
        "mass_exact": str(mass),
        "target_lower_bound_exact": "10001/10000",
        "node_count": summary["nodes"],
        "leaf_count": summary["leaves"],
        "minimum_printed_leaf_lower_bound": summary["minimum_printed_leaf_lower_bound"],
        "upstream_verifier_wall_seconds_after_compilation": summary["wall_seconds"],
        "output_sha256": {name: file_sha(out / name) for name in names},
        "analytic_n3_density_coverage_verified": True,
        "global_n11_optimality_proved": False,
        "speed_parity_measured": False,
    }


def replay() -> dict[str, object]:
    sources = source_identities()
    raw, candidate, mass = fixture_identity()
    mount_root = Path("/Volumes/spud-ext1")
    scratch = Path(os.environ["TMPDIR"]).resolve()
    require(mount_root.is_mount(), "external scratch volume is not mounted")
    require(scratch.is_dir() and os.access(scratch, os.W_OK), "external TMPDIR unavailable")
    require(
        scratch.is_relative_to(mount_root / "agent-scratch"),
        "TMPDIR is not external scratch",
    )
    result: dict[str, object] = {
        "status": "INCOMPLETE",
        "upstream_commit": REVISION,
        "upstream_source_sha256": sources,
        "fixture_sha256": sha(raw),
        "control_runner_sha256": file_sha(Path(__file__)),
        "replay_command_from_repository_root": REPLAY_COMMAND,
        "workers": 1,
        "outer_wall_ceiling_seconds": MAX_SECONDS,
        "mass_exact": str(mass),
        "fixture_mass_below_n_checked_before_launch": True,
        "analytic_n3_density_coverage_verified": False,
        "global_n11_optimality_proved": False,
        "speed_parity_measured": False,
    }
    with tempfile.TemporaryDirectory(prefix="wand125-full-pipeline-", dir=scratch) as name:
        snapshot = Path(name) / "candidate.json"
        with snapshot.open("xb") as stream:
            _ = stream.write(raw)
        require(file_sha(snapshot) == sha(raw), "candidate snapshot copy differs")
        result["candidate_snapshot_sha256"] = sha(raw)
        out = Path(name) / "certificate"
        command = (
            sys.executable,
            str(UPSTREAM / "solver/certify.py"),
            str(snapshot),
            "--out",
            str(out),
            "--workers",
            "1",
        )
        start = time.monotonic()
        proc = subprocess.Popen(
            command,
            cwd=UPSTREAM / "solver",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
        timed_out = False
        try:
            stdout, stderr = proc.communicate(timeout=MAX_SECONDS)
        except subprocess.TimeoutExpired:
            timed_out = True
            with suppress(ProcessLookupError):
                os.killpg(proc.pid, signal.SIGKILL)
            stdout, stderr = proc.communicate()
        result["outer_wall_seconds"] = time.monotonic() - start
        result["process_exit_code"] = proc.returncode
        result["timed_out"] = timed_out
        result["stdout_sha256"] = sha(stdout)
        result["stdout_bytes"] = len(stdout)
        result["stderr_sha256"] = sha(stderr)
        result["stderr_bytes"] = len(stderr)
        snapshot_unchanged = snapshot.is_file() and file_sha(snapshot) == sha(raw)
        fixture_unchanged = FIXTURE.is_file() and file_sha(FIXTURE) == sha(raw)
        mounted_after = mount_root.is_mount()
        result["candidate_snapshot_unchanged_after_run"] = snapshot_unchanged
        result["retained_fixture_unchanged_after_run"] = fixture_unchanged
        result["external_volume_mounted_after_run"] = mounted_after
        if not (snapshot_unchanged and fixture_unchanged and mounted_after):
            result["reason"] = "candidate snapshot, retained fixture, or external mount changed"
        elif timed_out:
            result["reason"] = "outer process-group wall ceiling"
        elif proc.returncode != 0:
            result["reason"] = "upstream certifier exited nonzero"
            result["stderr_tail"] = stderr.decode("utf-8", errors="replace")[-500:]
        else:
            try:
                result.update(checked_result(out, raw, candidate, mass, sources))
            except (ValueError, KeyError, TypeError) as error:
                result["reason"] = f"upstream output admission failed: {error}"
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = cast(Path | None, args.output)
    result = replay()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output:
        with output.open("x", encoding="utf-8") as stream:
            _ = stream.write(encoded)
    _ = sys.stdout.write(encoded)
    if result["status"] != "PASS_UPSTREAM_201_ANGLE_PIPELINE_ONLY":
        sys.exit(2)


if __name__ == "__main__":
    main()
