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

from devtools import supervise_windows as supervisor


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
        ("--worker-memory-gib", "16.1"),
        ("--review-memory-gib", "0"),
        ("--review-memory-gib", "12.1"),
        ("--min-available-gib", "7.9"),
        ("--min-available-gib", "inf"),
    ],
)
def test_numeric_guards_can_only_be_tightened(
    option: str,
    value: str,
    tmp_path: Path,
) -> None:
    with pytest.raises(SystemExit):
        supervisor.validated_arguments(arguments(tmp_path, option, value))


def test_default_guards_and_explicit_absolute_argv(tmp_path: Path) -> None:
    parsed = supervisor.validated_arguments(arguments(tmp_path))
    assert parsed.worker_memory_gib == 16
    assert parsed.review_memory_gib == 12
    assert parsed.min_available_gib == 8
    assert parsed.interval == 1
    assert parsed.command == [sys.executable, "-c", "pass"]
    owner = cast(subprocess.Popen[bytes], SimpleNamespace(_handle=123))
    assert supervisor.process_handle(owner) == 123


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


@pytest.mark.skipif(os.name != "nt", reason="requires actual Windows Job/working sets")
@pytest.mark.parametrize("mode", ["normal", "timeout", "memory"])
def test_native_venv_worker_and_grandchild_are_owned_and_reaped(
    mode: str,
    tmp_path: Path,
) -> None:
    """96MiB allocation; supervisor<=3s, external test<=30s; no research target."""
    worker = tmp_path / "worker.py"
    worker.write_text(WORKER, encoding="utf-8")
    output = tmp_path / "native-job"
    cap = str(80 / 1024) if mode == "memory" else "0.25"
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
        "0.25",
        "--",
        sys.executable,
        str(worker),
        mode,
    ]
    result = subprocess.run(command, capture_output=True, text=True, timeout=30, check=False)
    receipt = json.loads((output / "final.json").read_text())
    expected = {
        "normal": (0, "success"),
        "timeout": (124, "timeout"),
        "memory": (2, "worker-memory-stop"),
    }[mode]
    assert (result.returncode, receipt["status"]) == expected, result.stderr
    assert receipt["assigned_to_job"] is True
    assert receipt["job_active_processes"] == 0
    assert receipt["tree_cleanup_confirmed"] is True
    assert receipt["cleanup_errors"] == []
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
    samples = [json.loads(line) for line in (output / "samples.jsonl").read_text().splitlines()]
    for sample in samples:
        assert {item["pid"] for item in sample["workers"]} <= set(sample["enumerated_job_pids"])
