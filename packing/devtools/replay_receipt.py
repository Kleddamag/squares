"""Run one replay command and write its receipt: header, combined output, and footer.

Every replay of an external checker here leaves a receipt in one shape, the one the
September 28 evand packet's ``receipts/*.log`` already use::

    # command: <argv, shell-quoted>
    # cwd: <a label for the working directory>
    # python3: <which interpreter the command uses, or "not used by this command">
    # host: <cores> cores; load <1 5 15>; started <UTC>
    <the command's stdout and stderr, interleaved, unmodified>
    # finished <UTC>; exit <code>; wall <s> s; CPU <s> s (user <s> + sys <s>); load <1 5 15>

CPU is user plus system time of the command and every descendant it waited for, read
from ``getrusage(RUSAGE_CHILDREN)`` before and after. The tool exits with the command's
own status, so a failed replay stays failed in the caller.

Usage (from ``packing/``)::

    uv run --frozen python -m devtools.replay_receipt --receipt OUT.log \\
        --cwd-label "s12/ of a scratch export of evand/square-packing 08e8a5fa" \\
        --chdir SCRATCH/s12 -- verify2/target/release/zmx2 cert COVER --d4 --threads 3

``--json`` also prints the footer's fields as one JSON object on stderr, for a driver
that collects several receipts into one ``replays.json``.
"""

from __future__ import annotations

import argparse
import json
import os
import resource
import shlex
import subprocess
import sys
import time
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path


def _utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load() -> str:
    one, five, fifteen = os.getloadavg()
    return f"{one:.2f} {five:.2f} {fifteen:.2f}"


def run(
    argv: Sequence[str],
    *,
    receipt: Path,
    cwd_label: str,
    python_note: str,
    chdir: Path | None,
) -> dict[str, object]:
    """Run ``argv`` with its output streamed into ``receipt``; return the footer fields."""
    receipt.parent.mkdir(parents=True, exist_ok=True)
    started = _utc()
    load_start = _load()
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    t0 = time.monotonic()
    with receipt.open("w", encoding="utf-8") as out:
        out.write(f"# command: {shlex.join(argv)}\n")
        out.write(f"# cwd: {cwd_label}\n")
        out.write(f"# python3: {python_note}\n")
        out.write(f"# host: {os.cpu_count()} cores; load {load_start}; started {started}\n")
        out.flush()
        proc = subprocess.run(
            argv, cwd=chdir, stdout=out, stderr=subprocess.STDOUT, check=False
        )
        wall = time.monotonic() - t0
        after = resource.getrusage(resource.RUSAGE_CHILDREN)
        user = after.ru_utime - before.ru_utime
        system = after.ru_stime - before.ru_stime
        finished = _utc()
        load_end = _load()
        out.write(
            f"# finished {finished}; exit {proc.returncode}; wall {wall:.3f} s; "
            f"CPU {user + system:.1f} s (user {user:.3f} + sys {system:.3f}); load {load_end}\n"
        )
    return {
        "receipt": str(receipt),
        "command": shlex.join(argv),
        "started_utc": started,
        "load_average_at_start": load_start,
        "ended_utc": finished,
        "exit": proc.returncode,
        "wall_seconds": round(wall, 1),
        "cpu_seconds": round(user + system, 1),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--receipt", type=Path, required=True, help="receipt file to write")
    parser.add_argument(
        "--cwd-label", required=True, help="how the receipt names the working directory"
    )
    parser.add_argument(
        "--python-note",
        default="not used by this command",
        help="which python3 the command runs, for the receipt header",
    )
    parser.add_argument(
        "--chdir", type=Path, default=None, help="directory to run the command in"
    )
    parser.add_argument(
        "--json", action="store_true", help="print the footer fields as JSON on stderr"
    )
    parser.add_argument("command", nargs=argparse.REMAINDER, help="-- then the command")
    args = parser.parse_args(argv)
    command = list(args.command)
    if command[:1] == ["--"]:
        command = command[1:]
    if not command:
        parser.error("no command given after --")
    fields = run(
        command,
        receipt=args.receipt,
        cwd_label=args.cwd_label,
        python_note=args.python_note,
        chdir=args.chdir,
    )
    if args.json:
        print(json.dumps(fields), file=sys.stderr)
    return int(fields["exit"])  # type: ignore[call-overload]


if __name__ == "__main__":
    raise SystemExit(main())
