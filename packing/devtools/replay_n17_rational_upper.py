"""Replay the fixed n17 rational upper witness with bounded exact checks.

Run from ``packing/`` with its project interpreter and a fresh output directory.
The accepted exp-235 run-001 receipts are immutable; this entrypoint creates a new run.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import resource
import shlex
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

PACKING = Path(__file__).resolve().parents[1]
SOURCE_DIR = Path(
    "resources/web/n17-kleddamag-certified-bound-2026-09-21/"
    "kleddamag-17-squares-certified-bound"
)
SOURCE = SOURCE_DIR / "upper-packing-certificate.json"
SOURCE_SHA256 = "24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7"
EXPECTED_SIDE = "4675530093604551/1000000000000000"
PYTHON = ".venv/bin/python3"
COMMAND_SECONDS = 90
KILL_GRACE_SECONDS = 5
DATA_LIMIT_KIB = 1_048_576
FILE_LIMIT_KIB = 10_240


@dataclass(frozen=True)
class Step:
    label: str
    expected_exit: int
    command: tuple[str, ...]


def steps(output: Path) -> tuple[Step, ...]:
    """Freeze the command roster and expected exits before any target executes."""
    witness = str(output / "witness.yaml")
    return (
        Step(
            "grid-main",
            0,
            (
                PYTHON,
                "-m",
                "sqpack.cli.witness",
                "verify",
                "witnesses/grid-n004.yaml",
                "--json",
            ),
        ),
        Step(
            "grid-independent",
            0,
            (
                PYTHON,
                "-m",
                "devtools.check_rational_witness_independent",
                "witnesses/grid-n004.yaml",
            ),
        ),
        Step(
            "overlap-main",
            1,
            (
                PYTHON,
                "-m",
                "sqpack.cli.witness",
                "verify",
                "witnesses/overlap-negative-control.yaml",
                "--json",
            ),
        ),
        Step(
            "overlap-independent",
            1,
            (
                PYTHON,
                "-m",
                "devtools.check_rational_witness_independent",
                "witnesses/overlap-negative-control.yaml",
            ),
        ),
        Step(
            "conversion",
            0,
            (
                PYTHON,
                "-m",
                "devtools.import_half_angle_witness",
                str(SOURCE),
                "--expected-n",
                "17",
                "--expected-side",
                EXPECTED_SIDE,
                "--output",
                witness,
            ),
        ),
        Step(
            "target-main", 0, (PYTHON, "-m", "sqpack.cli.witness", "verify", witness, "--json")
        ),
        Step(
            "target-independent",
            0,
            (PYTHON, "-m", "devtools.check_rational_witness_independent", witness),
        ),
        Step("target-source", 0, (PYTHON, str(SOURCE_DIR / "verify_upper.py"), str(SOURCE))),
    )


def _required_environment() -> dict[str, str]:
    env = os.environ.copy()
    for key in ("TMPDIR", "CARGO_TARGET_DIR", "UV_CACHE_DIR"):
        if not env.get(key):
            raise ValueError(f"Set external scratch {key}")
    if not os.access(env["TMPDIR"], os.W_OK):
        raise ValueError("TMPDIR is not writable")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.pop("PYTHONOPTIMIZE", None)
    return env


def _run_git(*arguments: str) -> str:
    process = subprocess.run(
        ("git", *arguments), cwd=PACKING, capture_output=True, text=True, check=False
    )
    if process.returncode:
        raise ValueError(f"git {' '.join(arguments)} refused: {process.stderr.strip()}")
    return process.stdout


def _apply_limits() -> str:
    data_limit = DATA_LIMIT_KIB * 1024
    try:
        _, hard = resource.getrlimit(resource.RLIMIT_DATA)
        resource.setrlimit(resource.RLIMIT_DATA, (data_limit, hard))
    except OSError, ValueError:
        memory_guard = "unavailable-platform-data-limit"
    else:
        memory_guard = f"enforced-data-limit-kib-{DATA_LIMIT_KIB}"
    _, hard_file = resource.getrlimit(resource.RLIMIT_FSIZE)
    resource.setrlimit(resource.RLIMIT_FSIZE, (FILE_LIMIT_KIB * 1024, hard_file))
    return memory_guard


def _utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_step(step: Step, output: Path, env: dict[str, str]) -> None:
    with (output / "commands.log").open("a", encoding="utf-8") as log:
        log.write(shlex.join(step.command) + "\n")
    invocation = (
        "/usr/bin/time",
        "-l",
        "gtimeout",
        "--signal=TERM",
        f"--kill-after={KILL_GRACE_SECONDS}s",
        f"{COMMAND_SECONDS}s",
        *step.command,
    )
    with (
        (output / f"{step.label}.stdout").open("w", encoding="utf-8") as stdout,
        (output / f"{step.label}.stderr").open("w", encoding="utf-8") as stderr,
    ):
        process = subprocess.run(
            invocation, cwd=PACKING, env=env, stdout=stdout, stderr=stderr, check=False
        )
    result = process.returncode if process.returncode >= 0 else 128 - process.returncode
    with (output / "exits.tsv").open("a", encoding="utf-8") as exits:
        exits.write(f"{step.label}\t{result}\t{step.expected_exit}\n")
    if result != step.expected_exit:
        raise ValueError(
            f"Refused at {step.label}: exit {result}, expected {step.expected_exit}"
        )


def replay(output: Path) -> None:
    if Path.cwd().resolve() != PACKING:
        raise ValueError("run from packing/")
    if Path(sys.prefix).resolve() != (PACKING / ".venv").resolve() or not __debug__:
        raise ValueError("run with the unoptimized packing/.venv/bin/python3")
    if output.exists():
        raise ValueError("output directory already exists")
    env = _required_environment()
    _run_git("diff", "--quiet")
    _run_git("diff", "--cached", "--quiet")
    source_digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if source_digest != SOURCE_SHA256:
        raise ValueError("source certificate SHA-256 differs from the frozen input")
    memory_guard = _apply_limits()
    output.mkdir(parents=True)
    (output / "source-integrity.log").write_text(f"{SOURCE}: OK\n", encoding="utf-8")
    uptime = subprocess.run(("uptime",), capture_output=True, text=True, check=True).stdout
    provenance = (
        f"started_at={_utc()}\n"
        + _run_git("rev-parse", "HEAD")
        + _run_git("status", "--short")
        + f"{sys.version}\n"
        + "assertions_enabled=True; optimize=0\n"
        + uptime
        + f"workers=1\ncommand_timeout_seconds={COMMAND_SECONDS}\n"
        + f"file_limit_kib={FILE_LIMIT_KIB}\nmemory_guard={memory_guard}\n"
    )
    (output / "provenance.log").write_text(provenance, encoding="utf-8")
    (output / "exits.tsv").write_text("step\texit\texpected\n", encoding="utf-8")
    for step in steps(output):
        run_step(step, output, env)
    with (output / "provenance.log").open("a", encoding="utf-8") as log:
        log.write(f"finished_at={_utc()}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("output", type=Path)
    args = parser.parse_args(argv)
    try:
        replay(args.output)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    print(
        "All fixed commands returned the expected statuses; "
        "review counts, side and complete outputs before acceptance."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
