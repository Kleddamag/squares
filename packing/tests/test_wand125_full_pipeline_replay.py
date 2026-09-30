"""Portable admission controls for the retained upstream pipeline replay.

Synthetic output rows exercise receipt refusal only; they are not certificates.
"""

from __future__ import annotations

import hashlib
import json
import runpy
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path
from typing import cast

import pytest

REPO = Path(__file__).resolve().parents[2]
SCRIPT = (
    REPO
    / "packing/resources/web/wand125-tools-2026-09-29/update-3eb08e6/replay-full-pipeline.py"
)
FIXTURE = REPO / "packing/resources/web/wand125-tools-2026-09-29/native-analytic-control.json"
CheckedResult = Callable[
    [Path, bytes, dict[str, object], Fraction, dict[str, str]], dict[str, object]
]


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def checked_result() -> CheckedResult:
    namespace = runpy.run_path(str(SCRIPT))
    return cast(CheckedResult, namespace["checked_result"])


@pytest.fixture
def synthetic_output(tmp_path: Path) -> tuple[Path, bytes, dict[str, object], dict[str, str]]:
    raw = FIXTURE.read_bytes()
    candidate = cast(dict[str, object], json.loads(raw))
    cpp, runner, input_bytes = b"pinned-cpp-test", b"pinned-runner-test", b"input-test"
    sources = {"solver/verify.cpp": digest(cpp), "solver/run_verify.py": digest(runner)}
    meta: dict[str, object] = {
        "source_sha256": digest(raw),
        "input_sha256": digest(input_bytes),
        "mass_exact": "1683003/625000",
        "angle_count": 201,
        "rescaled": False,
    }
    summary = {
        "status": "VERIFIED",
        "angle_cases": 201,
        "input_sha256": digest(input_bytes),
        "verifier_source_sha256": digest(cpp),
        "target_lower_bound_exact": "10001/10000",
        "nodes": 201,
        "leaves": 201,
        "minimum_printed_leaf_lower_bound": 1.01,
        "wall_seconds": 1.0,
    }
    final = {
        **candidate,
        "status": "VERIFIED_CONTINUOUS_DENSITY",
        "globally_verified": True,
        "certificate": meta,
        "coverage_lower_bound_exact": "10001/10000",
    }
    for name, data in (
        ("certificate_input.txt", input_bytes),
        ("certificate_metadata.json", json.dumps(meta).encode()),
        ("verification_summary.json", json.dumps(summary).encode()),
        ("certified_candidate.json", json.dumps(final).encode()),
        ("verify.cpp", cpp),
        ("run_verify.py", runner),
        ("verify", b"fake-binary"),
    ):
        _ = (tmp_path / name).write_bytes(data)
    rows = [{"r": index, "status": "verified", "lower_bound": 1.01} for index in range(201)]
    _ = (tmp_path / "verified_angles.jsonl").write_text(
        "\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8"
    )
    return tmp_path, raw, candidate, sources


def test_duplicate_angle_refuses(
    synthetic_output: tuple[Path, bytes, dict[str, object], dict[str, str]],
) -> None:
    out, raw, candidate, sources = synthetic_output
    check = checked_result()
    accepted = check(out, raw, candidate, Fraction(1683003, 625000), sources)
    assert accepted["status"] == "PASS_UPSTREAM_201_ANGLE_PIPELINE_ONLY"
    rows = (out / "verified_angles.jsonl").read_text().splitlines()
    rows[-1] = rows[0]
    _ = (out / "verified_angles.jsonl").write_text("\n".join(rows) + "\n")
    with pytest.raises(ValueError, match="angle census"):
        _ = check(out, raw, candidate, Fraction(1683003, 625000), sources)


def test_stale_final_geometry_refuses(
    synthetic_output: tuple[Path, bytes, dict[str, object], dict[str, str]],
) -> None:
    out, raw, candidate, sources = synthetic_output
    final = cast(dict[str, object], json.loads((out / "certified_candidate.json").read_bytes()))
    final["weights"] = ["1"]
    _ = (out / "certified_candidate.json").write_text(json.dumps(final))
    with pytest.raises(ValueError, match="changed the candidate"):
        _ = checked_result()(out, raw, candidate, Fraction(1683003, 625000), sources)
