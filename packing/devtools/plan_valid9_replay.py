"""Price, shard and check a full replay of Daniel's exact checker on ``ValidTilt9``.

jlevy/squares#316 claims ``s(k^2 - 4) = k`` for every ``k >= 5``; for ``k >= 8`` it rests
on ``ValidTilt9``: every unit square tilted by ``0 < theta <= 45`` degrees with centre in
``[0, 9/2]^2`` has mass at least 1 under the box cover ``K4_k008_box9.txt``. Daniel's
``qx2_zm.py`` run ``qx2_k4x_k008`` decides it over 16,200 D4 root boxes, and its record
``run_k4x_k008_leaves.jsonl.gz``, which the October 3 evand packet retains, carries every
root's CPU time and leaf list. This tool is ``devtools.plan_valid7_replay`` for that run:
it reuses that tool's record reader, partition and rectangles, and replaces what is
fixed to side 7 there with the 9 by 9 box. It decides nothing about a leaf; the checker
does.

``stage --work DIR [--s12]``
    Copies the retained checker into ``DIR/checker`` and the decompressed cover into
    ``DIR/K4_k008_box9.txt``, refusing any file whose SHA-256 is not the one the run's
    record header names, and makes ``DIR/runs`` and ``DIR/receipts``. ``--s12`` also
    stages the complete upstream ``s12`` subtree at ``DIR/s12``: every ``.gz`` the packet
    stores for size decompressed, the record at its upstream path, and every file checked
    against the acquisition manifest and, under ``certificates/k2m4``, the bundle's own
    ``SHA256SUMS``. The bundle's ``verify.sh`` and ``verify.sh --full`` run there.
``plan --shards N [--speed S] [--cores K] [--python P] [--json OUT]``
    Prices the replay from the record's per-root CPU and splits it into at most ``N``
    shards of nearly equal CPU. The unit is a centre cell, the eight roots of one 1/10
    by 1/10 centre square; cells are taken in x-major order over the 45 by 45 grid and
    cut into runs of consecutive cells, so a shard is at most three rectangles, each one
    ``qx2_zm.py`` run with the published settings, its own region flags and its own
    ``--resume`` record. An interrupted run is finished by running the same command
    again. ``--speed`` is this host's CPU seconds per recorded CPU second, measured with
    ``region`` against a calibration receipt. Each shard gets two wall estimates: the
    even split ``CPU / cores``, and the list-scheduling bound ``CPU / cores + (1 - 1 /
    cores) * largest root`` summed over its runs, which no run of the pool can exceed.
``region --x LO HI --y LO HI``
    The recorded CPU and root count of one rectangle of centres, for calibration.
``compare SHARD... [--partial] [--json OUT]``
    Checks a sharded replay against the published record, as the bundle's
    ``verify.sh --full`` does for one unsharded run: each shard's header names the
    retained checker and cover; its argv is the published settings plus region and
    process flags only; no root is recorded twice; together the shards hold exactly the
    16,200 published roots (``--partial``: only published ones, for a calibration); none
    has an uncertified box; and each root's leaf list equals the published one.

From ``packing/``::

    uv run --frozen --all-extras --group dev python -m devtools.plan_valid9_replay \\
        plan --shards 12 --speed 1.0
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from collections.abc import Sequence
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import cast

from strif import atomic_write_text

from devtools.plan_valid7_replay import (
    PITCH,
    QX2_REGION_FLAGS,
    QX2_SETTINGS,
    WEB,
    Box,
    Cell,
    Rect,
    Root,
    partition,
    read_record,
    rectangles,
)

PACKET = WEB / "evand-square-packing-2026-10-03"
S12 = PACKET / "square-packing/s12"
K2M4 = S12 / "certificates/k2m4"
#: The cover is over 1,000 lines, so the packet stores it as deterministic ``gzip -9n``.
COVER_GZ = K2M4 / "K4_k008_box9.txt.gz"
COVER_NAME = "K4_k008_box9.txt"
COVER_SHA256 = "4151d7c4059d5dcf56130c9373e6b5b60635e1a4250f46562d7ecc4d64a27801"
CHECKER = K2M4 / "qx2_zm/checker"
#: Byte-identical to upstream ``s12/certificates/k2m4/qx2_zm/run_k4x_k008_leaves.jsonl.gz``.
RECORD = PACKET / "record/run_k4x_k008_leaves.jsonl.gz"
RECORD_UPSTREAM = "s12/certificates/k2m4/qx2_zm/run_k4x_k008_leaves.jsonl.gz"
RECORD_SHA256 = "e8f1f2bff3a5d8ca4c75dd2c689439aa6453b1f6741931c54000d023a03e43dd"
MANIFEST = PACKET / "acquisition/upstream-subtree.sha256"
#: The files run ``qx2_k4x_k008``'s header names, by SHA-256 (``k2m4/SHA256SUMS``); the
#: same four files as the k = 7 run V3.
FILES = {
    "qx2_zm.py": "6294052a37ce66c5d84b55afd606e3a52f463e22b876bf44b5aa903aefb7e737",
    "zm_mixed.py": "1fd203469bb43a55ca7ce376b9717437e0970eead31941ec7fa100ab24d5ba95",
    "zeromargin.py": "640fe453c1a32f4aa580ca2b1261c6406923a4d7c131f65604a432c7fc2086ab",
    "mixed_cover.py": "bb89de15ecf5821dd7e1a36ebab8a50d792a406b7fb0f5cb38059f99ef74aae5",
}
SIDE = Fraction(9)
#: Centre cells per side of the D4 region ``[0, 9/2]^2``.
GRID = int(SIDE / 2 / PITCH)
ROOTS = 16_200


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@cache
def published() -> tuple[dict[str, object], tuple[Root, ...]]:
    """The published record's header and roots, read once."""
    if _sha256(RECORD.read_bytes()) != RECORD_SHA256:
        msg = f"{RECORD} is not e8f1f2bf"
        raise SystemExit(msg)
    record = read_record(RECORD, "qx2")
    return record.header, tuple(record.roots)


def command(rect: Rect, record: str, cores: int, python: str) -> list[str]:
    """``qx2_zm.py`` for one rectangle of centres, run from a staged work directory."""
    x0, x1, y0, y1 = (str(v) for v in rect)
    return [
        python, "checker/qx2_zm.py", COVER_NAME,
        "--depth", "18", "--nproc", str(cores), "--exact-umax", "1/2",
        "--exact-from", "3", "--progress", "200",
        "--cx-lo", x0, "--cx-hi", x1, "--cy-lo", y0, "--cy-hi", y1,
        "--resume", record, "--dump-leaves",
    ]  # fmt: skip


def cells(roots: Sequence[Root]) -> list[tuple[Cell, float, float]]:
    """Every centre cell in x-major order, with its recorded CPU and its largest root's."""
    total: defaultdict[Cell, float] = defaultdict(float)
    largest: defaultdict[Cell, float] = defaultdict(float)
    for root in roots:
        key = (root.box[0], root.box[2])
        total[key] += root.cpu
        largest[key] = max(largest[key], root.cpu)
    keys = [(PITCH * i, PITCH * j) for i in range(GRID) for j in range(GRID)]
    return [(key, total[key], largest[key]) for key in keys]


def _hours(seconds: float) -> float:
    return round(seconds / 3600, 2)


def plan(
    shards: int, *, speed: float = 1.0, cores: int = 4, python: str = "python3"
) -> dict[str, object]:
    """The price of the replay and its shards, with each shard's commands."""
    _, roots = published()
    grid = cells(roots)
    out: list[dict[str, object]] = []
    for k, (start, stop) in enumerate(partition([c for _, c, _ in grid], shards), 1):
        runs: list[dict[str, object]] = []
        bound = 0.0
        for j, rect in enumerate(rectangles(start, stop, GRID), 1):
            name = f"qx2_k008_shard{k:02d}_{j}"
            x0, x1, y0, y1 = rect
            inside = [
                (c, m) for (x, y), c, m in grid[start:stop]
                if x0 <= x < x1 and y0 <= y < y1
            ]  # fmt: skip
            run_cpu = sum(c for c, _ in inside)
            run_largest = max((m for _, m in inside), default=0.0)
            bound += run_cpu / cores + (1 - 1 / cores) * run_largest
            runs.append({
                "rectangle": [str(v) for v in rect],
                "cells": len(inside),
                "priced_cpu_hours": _hours(run_cpu),
                "record": f"runs/{name}.jsonl",
                "receipt": f"receipts/{name}.log",
                "command": command(rect, f"runs/{name}.jsonl", cores, python),
            })  # fmt: skip
        recorded = sum(c for _, c, _ in grid[start:stop])
        largest = max((m for _, _, m in grid[start:stop]), default=0.0)
        out.append({
            "shard": k,
            "cells": stop - start,
            "priced_cpu_hours": _hours(recorded),
            "largest_root_seconds": round(largest, 1),
            "wall_hours_estimate": _hours(max(recorded / cores, largest) * speed),
            "wall_hours_bound": _hours(bound * speed),
            "runs": runs,
        })  # fmt: skip
    total = sum(root.cpu for root in roots)
    return {
        "kind": "valid9-replay-plan/v1",
        "checker": "qx2",
        "run": "qx2_k4x_k008",
        "roots": len(roots),
        "recorded_cpu_hours": _hours(total),
        "speed": speed,
        "cores_per_shard": cores,
        "host_cpu_hours_estimate": _hours(total * speed),
        "shards": out,
    }


def region(x: tuple[Fraction, Fraction], y: tuple[Fraction, Fraction]) -> dict[str, object]:
    """The recorded CPU of the roots whose centre box lies in one rectangle."""
    _, roots = published()
    inside = [
        root for root in roots
        if x[0] <= root.box[0] and root.box[1] <= x[1]
        and y[0] <= root.box[2] and root.box[3] <= y[1]
    ]  # fmt: skip
    return {
        "checker": "qx2",
        "region": [str(v) for v in (*x, *y)],
        "roots": len(inside),
        "recorded_cpu_seconds": round(sum(root.cpu for root in inside), 1),
        "largest_root_seconds": round(max((r.cpu for r in inside), default=0.0), 1),
    }


def argv_problems(name: str, header: dict[str, object]) -> list[str]:
    """The record's argv is the published settings, plus region and process flags only."""
    argv = [str(v) for v in cast("list[object]", header.get("argv", []))]
    allowed = {"--nproc", "--progress", "--resume", *QX2_REGION_FLAGS, *QX2_SETTINGS}
    pairs = [argv[i : i + 2] for i in range(len(argv) - 1)]
    problems = [
        f"{name}: argv does not set {flag} {value}"
        for flag, value in zip(QX2_SETTINGS[:-1:2], QX2_SETTINGS[1:-1:2], strict=True)
        if [flag, value] not in pairs
    ]
    if QX2_SETTINGS[-1] not in argv:
        problems.append(f"{name}: argv lacks {QX2_SETTINGS[-1]}")
    problems += [
        f"{name}: argv changes a setting with {flag}"
        for flag in argv
        if flag.startswith("--") and flag not in allowed
    ]
    return problems


def compare(shards: Sequence[Path], *, partial: bool = False) -> dict[str, object]:
    """Check a sharded replay against the published record; ``ok`` and every problem.

    ``partial`` asks only that the shards' roots be published ones, not all of them: a
    calibration over one region, not a replay.
    """
    _, roots = published()
    reference = {root.box: root for root in roots}
    want = {**FILES, "input": COVER_SHA256}
    problems: list[str] = []
    seen: Counter[Box] = Counter()
    differ = matched = leaves = 0
    for path in shards:
        record = read_record(path, "qx2")
        if record.header.get("sha256") != want:
            problems.append(f"{path.name}: header digests are not the retained files")
        problems += argv_problems(path.name, record.header)
        for root in record.roots:
            seen[root.box] += 1
            if root.bad:
                box = [str(v) for v in root.box]
                problems.append(f"{path.name}: root {box} has {root.bad} uncertified")
            ref = reference.get(root.box)
            if ref is None:
                continue
            if root.leaves == ref.leaves:
                matched += 1
                leaves += len(root.leaves)
            else:
                differ += 1
    if repeated := sum(1 for n in seen.values() if n > 1):
        problems.append(f"{repeated} roots recorded more than once")
    if not partial and (missing := len(set(reference) - set(seen))):
        problems.append(f"{missing} published roots are missing")
    if extra := len(set(seen) - set(reference)):
        problems.append(f"{extra} roots are not published roots")
    if differ:
        problems.append(f"{differ} roots have leaves other than the published ones")
    return {
        "kind": "valid9-sharded-replay-compare/v1",
        "checker": "qx2",
        "run": "qx2_k4x_k008",
        "ok": not problems,
        "problems": problems,
        "shards": [p.name for p in shards],
        "roots": len(seen),
        "roots_matching_published_leaves": matched,
        "leaves_matching": leaves,
        "partial": partial,
    }


def _cover_bytes() -> bytes:
    data = gzip.decompress(COVER_GZ.read_bytes())
    if _sha256(data) != COVER_SHA256:
        msg = f"the retained cover is {_sha256(data)[:16]}, not 4151d7c4"
        raise SystemExit(msg)
    return data


def _manifest() -> dict[str, str]:
    """The acquisition manifest: upstream path under ``s12/`` to SHA-256."""
    out: dict[str, str] = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        digest, path = line.split(maxsplit=1)
        out[path.removeprefix("./")] = digest
    return out


def _sha256sums() -> dict[str, str]:
    """The bundle's own ``k2m4/SHA256SUMS``, keyed by upstream path."""
    out: dict[str, str] = {}
    for line in (K2M4 / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, path = line.split(maxsplit=1)
        out[f"s12/certificates/k2m4/{path}"] = digest
    return out


def _upstream_bytes(path: str) -> bytes:
    """One upstream file's bytes from the packet: as stored, decompressed, or the record."""
    if path == RECORD_UPSTREAM:
        return RECORD.read_bytes()
    stored = PACKET / "square-packing" / path
    if stored.exists():
        return stored.read_bytes()
    packed = stored.with_name(stored.name + ".gz")
    if packed.exists():
        return gzip.decompress(packed.read_bytes())
    msg = f"{path} is in the manifest but not in the packet"
    raise SystemExit(msg)


def stage_s12(target: Path) -> int:
    """Stage the upstream ``s12`` subtree at ``target``; return the file count."""
    sums = _sha256sums()
    manifest = _manifest()
    for path, digest in sorted(manifest.items()):
        data = _upstream_bytes(path)
        got = _sha256(data)
        if got != digest or sums.get(path, digest) != digest:
            msg = f"{path} is {got[:16]}, the manifest names {digest[:16]}"
            raise SystemExit(msg)
        out = target / path.removeprefix("s12/")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        if out.suffix == ".sh":
            out.chmod(0o755)
    if missing := set(sums) - set(manifest):
        msg = f"SHA256SUMS names files the manifest lacks: {sorted(missing)}"
        raise SystemExit(msg)
    return len(manifest)


def stage(work: Path, *, s12: bool = False) -> dict[str, object]:
    """Copy the retained checker and cover into ``work``; return each file's SHA-256."""
    header, _ = published()
    named = cast("dict[str, str]", header.get("sha256", {}))
    if named != {**FILES, "input": COVER_SHA256}:
        msg = "the record header names files other than the retained ones"
        raise SystemExit(msg)
    (work / "runs").mkdir(parents=True, exist_ok=True)
    (work / "receipts").mkdir(exist_ok=True)
    (work / "checker").mkdir(exist_ok=True)
    staged: dict[str, object] = {}
    for name in FILES:
        data = (CHECKER / name).read_bytes()
        if (digest := _sha256(data)) != named[name]:
            msg = f"{CHECKER / name} is {digest[:16]}, the record names {named[name][:16]}"
            raise SystemExit(msg)
        (work / "checker" / name).write_bytes(data)
        staged[f"checker/{name}"] = digest
    (work / COVER_NAME).write_bytes(_cover_bytes())
    staged[COVER_NAME] = COVER_SHA256
    if s12:
        staged["s12_files"] = stage_s12(work / "s12")
    return staged


def _fraction_pair(values: Sequence[str]) -> tuple[Fraction, Fraction]:
    return Fraction(values[0]), Fraction(values[1])


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    sub = parser.add_subparsers(dest="action", required=True)
    for action in ("stage", "plan", "region", "compare"):
        p = sub.add_parser(action)
        p.add_argument("--json", type=Path, help="also write the result here")
        if action == "stage":
            p.add_argument("--work", type=Path, required=True)
            p.add_argument("--s12", action="store_true", help="also stage DIR/s12")
        if action == "plan":
            p.add_argument("--shards", type=int, required=True)
            p.add_argument("--speed", type=float, default=1.0)
            p.add_argument("--cores", type=int, default=4)
            p.add_argument("--python", default="python3", help="interpreter in the commands")
        if action == "region":
            p.add_argument("--x", nargs=2, required=True)
            p.add_argument("--y", nargs=2, required=True)
        if action == "compare":
            p.add_argument("shards", nargs="+", type=Path)
            p.add_argument("--partial", action="store_true", help="one region, not the grid")
    args = parser.parse_args(argv)
    result: dict[str, object]
    if args.action == "stage":
        result = {"staged": stage(args.work, s12=args.s12)}
    elif args.action == "plan":
        result = plan(args.shards, speed=args.speed, cores=args.cores, python=args.python)
    elif args.action == "region":
        result = region(_fraction_pair(args.x), _fraction_pair(args.y))
    else:
        result = compare(args.shards, partial=args.partial)
    text = json.dumps(result, indent=2) + "\n"
    if args.json:
        atomic_write_text(args.json, text)
    print(text, end="")
    return 0 if result.get("ok", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
