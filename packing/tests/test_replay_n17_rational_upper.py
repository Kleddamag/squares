"""Cheap contract checks for the n17 replay launcher; never run its target."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from devtools import replay_n17_rational_upper as replay


def test_frozen_steps_keep_controls_before_the_target() -> None:
    output = Path("new-run")
    steps = replay.steps(output)

    assert [(step.label, step.expected_exit) for step in steps] == [
        ("grid-main", 0),
        ("grid-independent", 0),
        ("overlap-main", 1),
        ("overlap-independent", 1),
        ("conversion", 0),
        ("target-main", 0),
        ("target-independent", 0),
        ("target-source", 0),
    ]
    assert all(step.command[0] == ".venv/bin/python3" for step in steps)
    assert steps[4].command == (
        ".venv/bin/python3",
        "-m",
        "devtools.import_half_angle_witness",
        str(replay.SOURCE),
        "--expected-n",
        "17",
        "--expected-side",
        replay.EXPECTED_SIDE,
        "--output",
        "new-run/witness.yaml",
    )
    assert steps[-1].command == (
        ".venv/bin/python3",
        str(replay.SOURCE_DIR / "verify_upper.py"),
        str(replay.SOURCE),
    )


def test_step_runner_records_expected_negative_exit_and_timeout_wrapper(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[tuple[str, ...]] = []

    def fake_run(command: tuple[str, ...], **kwargs: Any) -> SimpleNamespace:
        calls.append(command)
        kwargs["stdout"].write("negative control\n")
        kwargs["stderr"].write("measured resources\n")
        return SimpleNamespace(returncode=1)

    monkeypatch.setattr(replay.subprocess, "run", fake_run)
    replay.run_step(replay.steps(tmp_path)[2], tmp_path, {})

    assert calls == [
        (
            "/usr/bin/time",
            "-l",
            "gtimeout",
            "--signal=TERM",
            "--kill-after=5s",
            "90s",
            *replay.steps(tmp_path)[2].command,
        )
    ]
    assert (tmp_path / "exits.tsv").read_text() == "overlap-main\t1\t1\n"
    assert (tmp_path / "overlap-main.stdout").read_text() == "negative control\n"
    assert (tmp_path / "overlap-main.stderr").read_text() == "measured resources\n"


def test_existing_output_refuses_before_a_step(tmp_path: Path) -> None:
    assert replay.main([str(tmp_path)]) == 2
    assert not (tmp_path / "commands.log").exists()
