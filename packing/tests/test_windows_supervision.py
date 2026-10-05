"""Portable CLI seams and bounded native owned-tree memory/cleanup controls."""

from __future__ import annotations

import ctypes
import importlib
import json
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import cast

import pytest
from yaml import safe_load

from devtools import supervise_windows as supervisor

REPOSITORY = Path(__file__).resolve().parents[2]
WINDOWS_WORKFLOW = REPOSITORY / ".github/workflows/windows-supervision.yml"
#: The native gate's own wall ceiling. A cold job measured 55 s on 2026-10-05, run
#: 37256926662: 28 s of checkout, 10 s of `uv sync`, 5 s of tests.
WINDOWS_JOB_CEILING_MINUTES = 5


def arguments(tmp_path: Path, *options: str) -> list[str]:
    return [
        "--cwd",
        str(tmp_path),
        "--output-dir",
        str(tmp_path / "job"),
        "--timeout",
        "3",
        *options,
        "--",
        sys.executable,
        "-c",
        "pass",
    ]


def test_import_and_help_never_load_windows_dll(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*_arguments: object, **_keywords: object) -> None:
        pytest.fail("import/help attempted a Windows DLL load")

    monkeypatch.setattr(ctypes, "WinDLL", forbidden, raising=False)
    importlib.reload(supervisor)
    with pytest.raises(SystemExit) as stopped:
        supervisor.main(["--help"])
    assert stopped.value.code == 0


def test_non_windows_execution_refuses_without_launch_or_receipt(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(supervisor, "os", SimpleNamespace(name="posix"))

    def forbidden(*_arguments: object, **_keywords: object) -> None:
        pytest.fail("unsupported host attempted a child launch")

    monkeypatch.setattr(supervisor.subprocess, "Popen", forbidden)
    assert supervisor.main(arguments(tmp_path)) == 2
    assert not (tmp_path / "job").exists()
    with pytest.raises(RuntimeError, match="Windows is required"):
        supervisor.WindowsJob()


@pytest.mark.parametrize(
    ("option", "value"),
    [
        ("--timeout", "0"),
        ("--timeout", "1801"),
        ("--timeout", "nan"),
        ("--interval", "0.09"),
        ("--interval", "5.1"),
        ("--worker-memory-gib", "0"),
        ("--worker-memory-gib", "-1"),
        ("--review-memory-gib", "0"),
        ("--review-memory-gib", "-1"),
        ("--min-available-gib", "-1"),
        ("--min-available-gib", "inf"),
    ],
)
def test_numeric_guards_refuse_invalid_limits(
    option: str,
    value: str,
    tmp_path: Path,
) -> None:
    with pytest.raises(SystemExit):
        supervisor.validated_arguments(arguments(tmp_path, option, value))


def test_default_guards_and_explicit_absolute_argv(tmp_path: Path) -> None:
    parsed = supervisor.validated_arguments(arguments(tmp_path))
    assert parsed.worker_memory_gib == supervisor.DEFAULT_WORKER_MEMORY_GIB == 16
    assert parsed.review_memory_gib == supervisor.DEFAULT_REVIEW_MEMORY_GIB == 12
    assert parsed.min_available_gib == supervisor.DEFAULT_MIN_AVAILABLE_GIB == 8
    assert supervisor.guard_warnings(parsed) == []
    assert parsed.interval == 1
    assert parsed.command == [sys.executable, "-c", "pass"]
    owner = cast(subprocess.Popen[bytes], SimpleNamespace(_handle=123))
    assert supervisor.process_handle(owner) == 123


def test_memory_policy_is_configurable_and_finite_products_do_not_overflow(
    tmp_path: Path,
) -> None:
    parsed = supervisor.validated_arguments(
        arguments(
            tmp_path,
            "--worker-memory-gib",
            "32",
            "--review-memory-gib",
            "64",
            "--min-available-gib",
            "0",
        )
    )
    assert parsed.worker_memory_gib == 32
    assert parsed.review_memory_gib == 64
    assert parsed.min_available_gib == 0
    assert supervisor.gib_bytes(0.25) == 256 * 1024**2
    assert supervisor.gib_bytes(0.0) == 0
    assert supervisor.gib_bytes(1e300) > 0


def test_a_lowered_floor_warns_rather_than_refuses(tmp_path: Path) -> None:
    parsed = supervisor.validated_arguments(arguments(tmp_path, "--min-available-gib", "0.25"))
    assert parsed.min_available_gib == 0.25
    (warning,) = supervisor.guard_warnings(parsed)
    assert "lowered to 0.25 GiB from the 8 GiB default" in warning


def test_a_review_mark_at_or_above_the_hard_stop_is_warned_about(tmp_path: Path) -> None:
    parsed = supervisor.validated_arguments(
        arguments(tmp_path, "--worker-memory-gib", "4", "--review-memory-gib", "4")
    )
    (warning,) = supervisor.guard_warnings(parsed)
    assert "not below the hard stop" in warning


def worker_at(gib: float, peak_gib: float | None = None) -> dict[str, int]:
    return {
        "pid": 1,
        "working_set_bytes": supervisor.gib_bytes(gib),
        "peak_working_set_bytes": supervisor.gib_bytes(gib if peak_gib is None else peak_gib),
    }


def test_both_default_worker_thresholds_are_reachable() -> None:
    """The review mark fires below the hard stop, and a worker growing past both meets
    the review mark first and the stop afterwards. Before Review A both thresholds
    stopped the run, so at the defaults the 16 GiB stop could never be the first."""
    stop = supervisor.gib_bytes(supervisor.DEFAULT_WORKER_MEMORY_GIB)
    review = supervisor.gib_bytes(supervisor.DEFAULT_REVIEW_MEMORY_GIB)
    assert review < stop

    def crossed(gib: float, peak_gib: float | None = None) -> tuple[bool, bool]:
        over_stop, over_review = supervisor.memory_crossings(
            [worker_at(gib, peak_gib)], stop, review
        )
        return bool(over_stop), bool(over_review)

    assert crossed(11.9) == (False, False)
    assert crossed(12) == (False, True)
    assert crossed(15.9) == (False, True)
    assert crossed(16) == (True, True)
    # A spike between samples is judged by the OS-reported peak.
    assert crossed(1, peak_gib=16.5) == (True, True)


def test_root_success_with_terminated_descendants_is_reported_distinctly() -> None:
    cleaned = {"descendants_termination_requested": True}
    finished = {"descendants_termination_requested": False}
    assert supervisor.final_status("success", finished, []) == "success"
    assert supervisor.final_status("success", cleaned, []) == "success-with-cleanup"
    assert supervisor.final_status("timeout", cleaned, []) == "timeout"
    assert supervisor.final_status("success", cleaned, ["Job close: x"]) == "cleanup-failed"
    assert supervisor.EXIT_CODES["success"] == supervisor.EXIT_CODES["success-with-cleanup"]
    assert supervisor.EXIT_CODES.get("cleanup-failed", 2) == 2


def test_command_requires_an_existing_absolute_executable(tmp_path: Path) -> None:
    supplied = arguments(tmp_path)
    supplied[-3] = "relative-python"
    with pytest.raises(SystemExit):
        supervisor.validated_arguments(supplied)


def test_existing_evidence_is_never_overwritten(tmp_path: Path) -> None:
    directory = tmp_path / "job"
    directory.mkdir()
    evidence = directory / "keep.txt"
    evidence.write_text("retained")
    with pytest.raises(RuntimeError, match="must be empty"):
        supervisor.supervise(supervisor.validated_arguments(arguments(tmp_path)))
    assert evidence.read_text() == "retained"


def test_atomic_json_preserves_exact_content(tmp_path: Path) -> None:
    path = tmp_path / "receipt.json"
    expected = {"status": "tested", "integer": 2**60, "rows": [1, 2]}
    supervisor.durable_json(path, expected)
    assert json.loads(path.read_text()) == expected
    assert not path.with_suffix(".json.tmp").exists()


WORKER = """import json, os, subprocess, sys, time
child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(20)"])
print(json.dumps({"worker_pid": os.getpid(), "grandchild_launcher_pid": child.pid}), flush=True)
allocation = bytearray(96 * 1024**2)
for offset in range(0, len(allocation), 4096):
    allocation[offset] = 1
time.sleep(0.8 if sys.argv[1] == "normal" else 20)
"""


#: The native cases. `.github/workflows/windows-supervision.yml` requires exactly this many
#: to execute, which `test_the_windows_workflow_runs_every_native_case_under_a_ceiling`
#: holds.
NATIVE_MODES = ("normal", "timeout", "memory")
EIGHTY_MIB_IN_GIB = str(80 / 1024)


@pytest.mark.skipif(os.name != "nt", reason="requires actual Windows Job/working sets")
@pytest.mark.parametrize("mode", NATIVE_MODES)
def test_native_venv_worker_and_grandchild_are_owned_and_reaped(
    mode: str,
    tmp_path: Path,
) -> None:
    """96 MiB allocation; supervisor at most 3 s, external test at most 30 s.

    `normal` sets the review mark at 80 MiB and the hard stop at 0.25 GiB, so the worker
    crosses the mark and runs to completion; `memory` sets the hard stop at 80 MiB, so
    the same worker is stopped.
    """
    worker = tmp_path / "worker.py"
    worker.write_text(WORKER, encoding="utf-8")
    output = tmp_path / "native-job"
    cap = EIGHTY_MIB_IN_GIB if mode == "memory" else "0.25"
    review = EIGHTY_MIB_IN_GIB if mode == "normal" else "0.25"
    command = [
        sys.executable,
        "-m",
        "devtools.supervise_windows",
        "--cwd",
        str(tmp_path),
        "--output-dir",
        str(output),
        "--timeout",
        "1.2" if mode == "timeout" else "3",
        "--interval",
        "0.1",
        "--worker-memory-gib",
        cap,
        "--review-memory-gib",
        review,
        "--min-available-gib",
        "0.25",
        "--",
        sys.executable,
        str(worker),
        mode,
    ]
    result = subprocess.run(command, capture_output=True, text=True, timeout=30, check=False)
    receipt = json.loads((output / "final.json").read_text())
    expected = {
        "normal": (0, "success-with-cleanup"),
        "timeout": (124, "timeout"),
        "memory": (2, "worker-memory-stop"),
    }[mode]
    assert (result.returncode, receipt["status"]) == expected, result.stderr
    assert receipt["schema"] == supervisor.RECEIPT_SCHEMA
    assert receipt["assigned_to_job"] is True
    assert receipt["worker_memory_review_crossed"] is (mode == "normal")
    assert receipt["job_active_processes"] == 0
    assert receipt["tree_cleanup_confirmed"] is True
    assert receipt["cleanup_errors"] == []
    if mode == "normal":
        assert receipt["root_status"] == "exited-zero"
        assert receipt["root_exited_before_cleanup"] is True
        assert receipt["live_descendants_before_cleanup"] >= 1
        assert receipt["descendants_termination_requested"] is True
    assert all(item["exit_signalled"] for item in receipt["cleanup_process_identity_checks"])
    assert receipt["peak_observed_worker_working_set_bytes"] >= 96 * 1024**2
    assert (
        receipt["peak_root_working_set_bytes"]
        < receipt["peak_observed_worker_working_set_bytes"]
    )
    worker_ids = json.loads((output / "stdout.log").read_text().splitlines()[0])
    if mode != "normal":
        identities = {item["pid"] for item in receipt["cleanup_process_identity_checks"]}
        assert worker_ids["worker_pid"] in identities
        assert worker_ids["grandchild_launcher_pid"] in identities
    if mode == "memory":
        assert any(
            item["pid"] == worker_ids["worker_pid"] for item in receipt["worker_memory_trigger"]
        )
    if mode == "normal":
        assert "worker_memory_trigger" not in receipt
        assert any(
            item["pid"] == worker_ids["worker_pid"]
            for item in receipt["worker_memory_review_trigger"]["workers"]
        )
        assert "review mark; still running" in result.stderr
    samples = [json.loads(line) for line in (output / "samples.jsonl").read_text().splitlines()]
    for sample in samples:
        assert {item["pid"] for item in sample["workers"]} <= set(sample["enumerated_job_pids"])


def test_the_windows_workflow_runs_every_native_case_under_a_ceiling() -> None:
    """Review A1: the native path is gated on `windows-latest`, cheaply.

    The gate is its own workflow rather than a lane of `packing-required`: the wall
    contract in `devtools/gate-budgets.yaml` registers a workflow with an aggregator, a
    wall-check step and recorded samples, which is far more than one 55-second job.
    So it is path-filtered to what it tests, bounded by `timeout-minutes`, and held
    here to the same action pins and interpreter as the main gate.
    """
    workflow = safe_load(WINDOWS_WORKFLOW.read_text(encoding="utf-8"))
    validation = safe_load(
        (REPOSITORY / ".github/workflows/packing-validation.yml").read_text(encoding="utf-8")
    )

    def uses(document: dict) -> set[str]:
        return {
            str(step["uses"])
            for job in document["jobs"].values()
            for step in job.get("steps", [])
            if "uses" in step
        }

    assert uses(workflow) <= uses(validation), sorted(uses(workflow) - uses(validation))

    owned = {
        ".github/workflows/windows-supervision.yml",
        "packing/devtools/supervise_windows.py",
        "packing/tests/test_windows_supervision.py",
    }
    for event in ("pull_request", "push"):
        assert owned <= set(workflow["on"][event]["paths"]), event

    (job,) = workflow["jobs"].values()
    assert job["runs-on"] == "windows-latest"
    assert 0 < job["timeout-minutes"] <= WINDOWS_JOB_CEILING_MINUTES

    setup = next(
        step for step in job["steps"] if str(step.get("uses", "")).startswith("astral-sh/")
    )
    python = (REPOSITORY / "packing/.python-version").read_text(encoding="utf-8").strip()
    assert setup["with"]["python-version"] == python

    command = next(step["run"] for step in job["steps"] if "pytest" in step.get("run", ""))
    assert "tests/test_windows_supervision.py" in command
    selector = command.split(" -k ")[1].split()[0]
    assert selector in test_native_venv_worker_and_grandchild_are_owned_and_reaped.__name__
    assert f"-ne {len(NATIVE_MODES)} " in command
    assert "skipped -ne 0" in command
