"""Fail-closed controls for the resident exact-geometry process boundary."""

from __future__ import annotations

import sys
import time
from fractions import Fraction
from pathlib import Path

import pytest

from sqpack.rectangle_density import (
    CandidateError,
    RectangleDensityCandidate,
    load_candidate,
    verify_candidate,
)

PACKING = Path(__file__).resolve().parents[1]
ANALYTIC = PACKING / "resources/web/wand125-tools-2026-09-29/native-analytic-control.json"


def _fake_server(tmp_path: Path, mode: str) -> Path:
    source = f"""#!{sys.executable}
import hashlib
import json
import sys
import time

mode = {mode!r}
opening = sys.stdin.buffer.readline().rstrip(b"\\n")
digest = hashlib.sha256(opening).hexdigest()
count = len(json.loads(opening)["rectangles"])
ready = {{"version": 1, "status": "ready", "table_sha256": digest, "rectangle_count": count}}
sys.stdout.write(json.dumps(ready) + "\\n")
sys.stdout.flush()
for line in sys.stdin.buffer:
    query = json.loads(line)
    if mode == "partial":
        sys.stdout.write('{{"version":')
        sys.stdout.flush()
        time.sleep(5)
    response = {{"version": 1, "sequence": query["sequence"], "table_sha256": digest,
                "coverages": ["1"] * len(query["polygons"])}}
    if mode == "wrong_sequence":
        response["sequence"] += 1
    if mode == "duplicate_key":
        sys.stdout.write('{{"version":1,"version":1}}\\n')
    else:
        sys.stdout.write(json.dumps(response) + "\\n")
    sys.stdout.flush()
    if mode in ("wrong_sequence", "duplicate_key"):
        break
if mode == "extra_output":
    sys.stdout.write('unsolicited\\n')
    sys.stdout.flush()
if mode == "shutdown_hang":
    time.sleep(5)
"""
    binary = tmp_path / f"fake-{mode}"
    binary.write_text(source, encoding="utf-8")
    binary.chmod(0o700)
    return binary


def _candidate() -> RectangleDensityCandidate:
    return load_candidate(ANALYTIC, n=3, expected_side=Fraction(3, 2))


@pytest.mark.parametrize("mode", ["wrong_sequence", "duplicate_key", "extra_output"])
def test_invalid_resident_response_refuses(tmp_path: Path, mode: str) -> None:
    with pytest.raises(CandidateError, match="Rust exact geometry refused"):
        verify_candidate(
            _candidate(),
            angle_indices=(0,),
            max_nodes_per_angle=1 if mode != "extra_output" else 0,
            max_seconds=2,
            backend="rust",
            rust_binary=_fake_server(tmp_path, mode),
        )


def test_partial_line_timeout_retains_unresolved_event_census(tmp_path: Path) -> None:
    start = time.monotonic()
    report = verify_candidate(
        _candidate(),
        angle_indices=(0,),
        max_seconds=0.5,
        backend="rust",
        rust_binary=_fake_server(tmp_path, "partial"),
    )
    assert time.monotonic() - start < 2
    assert report.status == "INCONCLUSIVE"
    assert report.backend_timeout
    assert len(report.angles) == 1
    assert report.angles[0].nodes == 0
    assert report.angles[0].unresolved_leaves > 0
    assert report.angles[0].stop_cause == "time_limit"


def test_shutdown_timeout_cannot_promote_completed_angles(tmp_path: Path) -> None:
    report = verify_candidate(
        _candidate(),
        angle_indices=(0,),
        max_seconds=0.5,
        backend="rust",
        rust_binary=_fake_server(tmp_path, "shutdown_hang"),
    )
    assert report.status == "INCONCLUSIVE"
    assert report.backend_timeout
    assert len(report.angles) == 1
    assert report.angles[0].status == "VERIFIED"
    assert report.angles[0].nodes > 0


def test_unsupported_mixed_bound_is_refused_before_child_start(tmp_path: Path) -> None:
    with pytest.raises(CandidateError, match="common-core only"):
        verify_candidate(
            _candidate(),
            angle_indices=(1,),
            bound_mode="corner-min",
            backend="rust",
            rust_binary=_fake_server(tmp_path, "shutdown_hang"),
        )
