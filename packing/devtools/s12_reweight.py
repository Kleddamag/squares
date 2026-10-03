"""Re-weight evand's s(12) points by linear programming at a larger container.

`devtools.s12_angle_net_rescale` scales Daniel's certificate whole, weights included, and
stops where some placement loses a point. This tool keeps the scaled point set and solves
for new weights: one variable per D4 orbit of points, one row per placement the source's
verifier reports as near-tight, minimum total weight subject to every row capturing at
least ``1 + margin``. The scaled points carry no weight from the source; what is reused is
the geometry.

**Rows come from the verifier.** The source's ``verify/`` has a diagnostic dump,
``TIGHT_DUMP``, that lists each cell of its arrangement sweep whose captured weight is at
most a threshold, as an interval of centres in the bin's rotated frame over its common
denominator. The points a cell's squares contain are constant on the open cell, so the set
is decided here exactly, in integers, at the cell's midpoint; no floating-point membership
enters a row. Each round writes the current weights as a certificate, dumps the near-tight
cells of every ``stride``-th bin (``offset`` rotating between rounds), adds the new
coverage sets as rows, and re-solves.

**Floats propose, the verifier decides.** The LP is solved in floating point by HiGHS. Its
weights are rounded *up* to integer numerators over ``W``, which can only raise every
captured weight, and the total is computed exactly. A weight file from here is a candidate
and nothing more: `devtools.s12_angle_net_rescale verify` runs the complete sweep, and only
its receipt says anything about ``s(12)``.

Usage (from ``packing/``)::

    uv run --frozen --all-extras --group dev python -m devtools.s12_reweight \\
        --work WORK --multiplier 1000 --denominator 3949000 --net 96000 \\
        --rounds 12 --stride 24 --output CERT.txt --log LOG.jsonl
"""

from __future__ import annotations

import argparse
import json
import math
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

from devtools.s12_angle_net_rescale import (
    Certificate,
    bin_count,
    binary_path,
    load_source,
    parse_certificate,
    rescale,
    run_verifier,
)

#: The source's weight denominator, kept so a re-weighted file reads like the original.
WEIGHT_SCALE = 10_000_000


def d4_orbits(cert: Certificate) -> tuple[tuple[int, ...], ...]:
    """Indices of the points grouped by the container's D4 images, in exact integers."""
    units = cert.side * cert.denominator
    if units.denominator != 1:
        raise ValueError("container is off the coordinate grid")
    u = int(units)
    where: dict[tuple[int, int], list[int]] = {}
    for index, (x, y, _) in enumerate(cert.points):
        where.setdefault((x, y), []).append(index)
    seen: set[int] = set()
    orbits: list[tuple[int, ...]] = []
    for index, (x, y, _) in enumerate(cert.points):
        if index in seen:
            continue
        images = {
            (x, y), (u - x, y), (x, u - y), (u - x, u - y),
            (y, x), (u - y, x), (y, u - x), (u - y, u - x),
        }  # fmt: skip
        members: list[int] = []
        for image in sorted(images):
            if image not in where:
                raise ValueError(
                    f"point {index} has an image outside the set: not D4-symmetric"
                )
            members.extend(where[image])
        orbit = tuple(sorted(set(members)))
        seen.update(orbit)
        orbits.append(orbit)
    return tuple(orbits)


@dataclass(frozen=True, slots=True)
class BinFrame:
    """A dump's bin header: the rotation ``(cn, sn)/g`` and half-side ``hh`` over ``DEN``."""

    k: int
    den: int
    cn: int
    sn: int
    g: int
    hh: int
    sg_n: int
    sg_d: int
    wm_d: int


def cell_members(
    cert: Certificate, frame: BinFrame, cell: tuple[int, int, int, int]
) -> frozenset[int]:
    """Points in the closed ``sigma_k`` square centred at the open cell's midpoint, exactly.

    In the source's sweep a point ``(X, Y)/D`` sits at ``q = R(-theta_k) p`` over ``DEN``,
    numerators ``(cn X + sn Y) k1`` and ``(-sn X + cn Y) k1`` with ``k1 = 2 sg_d wm_d``, and
    a centre ``u`` captures it when ``|q - u|`` is at most ``hh`` in both coordinates. With
    ``u`` the midpoint ``((a+b)/2, (c0+c1)/2)`` everything doubles to integers.
    """
    return _Frame(cert, frame).members(cell)


class _Frame:
    """One bin's rotated points, with a float prefilter in front of the exact test."""

    def __init__(self, cert: Certificate, frame: BinFrame) -> None:
        k1 = 2 * frame.sg_d * frame.wm_d
        self.q = [
            (2 * (frame.cn * x + frame.sn * y) * k1, 2 * (-frame.sn * x + frame.cn * y) * k1)
            for x, y, _ in cert.points
        ]
        self.qf = np.array(self.q, dtype=np.float64)
        self.reach = 2 * frame.hh

    def members(self, cell: tuple[int, int, int, int]) -> frozenset[int]:
        a, b, c0, c1 = cell
        mid0, mid1 = a + b, c0 + c1
        loose = self.reach * (1 + 1e-9)
        near = np.nonzero(
            (np.abs(self.qf[:, 0] - mid0) <= loose) & (np.abs(self.qf[:, 1] - mid1) <= loose)
        )[0]
        return frozenset(
            int(i)
            for i in near
            if abs(self.q[i][0] - mid0) <= self.reach and abs(self.q[i][1] - mid1) <= self.reach
        )


def parse_dump(text: str) -> list[tuple[BinFrame, tuple[int, int, int, int], int]]:
    """``(frame, cell, captured numerator)`` for every cell line of a ``TIGHT_DUMP`` file."""
    frames: dict[int, BinFrame] = {}
    cells: list[tuple[BinFrame, tuple[int, int, int, int], int]] = []
    for line in text.splitlines():
        if line.startswith("bin "):
            f = line.split()
            k = int(f[1])
            frames[k] = BinFrame(
                k=k,
                den=int(f[4]),
                cn=int(f[5]),
                sn=int(f[6]),
                g=int(f[7]),
                hh=int(f[8]),
                sg_n=int(f[9]),
                sg_d=int(f[10]),
                wm_d=int(f[12]),
            )
        elif line.startswith("c "):
            f = line.split()
            cells.append(
                (frames[int(f[1])], (int(f[2]), int(f[3]), int(f[4]), int(f[5])), int(f[6]))
            )
    return cells


@dataclass
class Rows:
    """Coverage sets as orbit-count vectors, deduplicated."""

    orbit_of: np.ndarray
    n_orbits: int
    seen: set[bytes] = field(default_factory=set)
    rows: list[np.ndarray] = field(default_factory=list)

    def add(self, members: frozenset[int]) -> bool:
        counts = np.bincount(self.orbit_of[sorted(members)], minlength=self.n_orbits).astype(
            np.float64
        )
        key = counts.tobytes()
        if key in self.seen:
            return False
        self.seen.add(key)
        self.rows.append(counts)
        return True


def solve(rows: Rows, sizes: np.ndarray, margin: float) -> np.ndarray:
    """Least ``sum |O| w_O`` with every held row capturing ``1 + margin``."""
    matrix = np.vstack(rows.rows)
    done = linprog(
        c=sizes,
        A_ub=-matrix,
        b_ub=-(1.0 + margin) * np.ones(len(rows.rows)),
        bounds=(0, None),
        method="highs",
    )
    if done.status != 0:
        raise RuntimeError(f"LP failed: {done.message}")
    return np.asarray(done.x)


def with_weights(
    cert: Certificate, orbits: tuple[tuple[int, ...], ...], weights: np.ndarray
) -> Certificate:
    """Orbit weights rounded up to numerators over `WEIGHT_SCALE`; zero-weight points kept."""
    numerators = [0] * len(cert.points)
    for orbit, w in zip(orbits, weights, strict=True):
        value = max(0, math.ceil(float(w) * WEIGHT_SCALE - 1e-9))
        for index in orbit:
            numerators[index] = value
    points = tuple((x, y, numerators[i]) for i, (x, y, _) in enumerate(cert.points))
    return Certificate(cert.s_num, cert.s_den, cert.denominator, WEIGHT_SCALE, points)


def dump_rows(
    work: Path,
    certificate: Path,
    net: int,
    bins: list[int],
    threshold: int,
    *,
    workers: int,
) -> tuple[list[tuple[BinFrame, tuple[int, int, int, int], int]], str | None]:
    """Near-tight cells of the chosen bins and the least captured weight among them."""
    binary = binary_path(work, overflow_checked=False)
    scratch = Path(tempfile.mkdtemp(dir=work))

    def one(k: int) -> tuple[str, str | None]:
        out = scratch / f"dump-{k}.txt"
        verdict, _ = run_verifier(
            binary,
            certificate,
            net,
            threads=1,
            bins=(k, k),
            extra_env={
                "TIGHT_DUMP": str(out),
                "TIGHT_THRESH": str(threshold),
                "TIGHT_MAX": "2000000000",
            },
        )
        text = out.read_text(encoding="ascii")
        out.unlink()
        return text, verdict.least_weight

    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(one, bins))
    scratch.rmdir()
    cells = [cell for text, _ in results for cell in parse_dump(text)]
    least = min((w for _, w in results if w is not None), key=Fraction, default=None)
    return cells, least


def _same_points(a: Certificate, b: Certificate) -> bool:
    """The same source points, possibly at another scale: proportional integer coordinates."""
    if len(a.points) != len(b.points):
        return False
    (ax, ay, _), (bx, by, _) = max(a.points), max(b.points)
    return (
        all(
            x * bx == u * ax and y * bx == v * ax
            for (x, y, _), (u, v, _) in zip(a.points, b.points, strict=True)
        )
        and ay * bx == by * ax
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--multiplier", type=int, required=True)
    parser.add_argument("--denominator", type=int, required=True)
    parser.add_argument("--net", type=int, required=True)
    parser.add_argument("--rounds", type=int, default=10)
    parser.add_argument("--stride", type=int, default=24)
    parser.add_argument("--slack", type=float, default=0.004, help="dump cells below 1 + slack")
    parser.add_argument("--margin", type=float, default=2e-6, help="LP rows ask for 1 + margin")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument(
        "--rows-cache", type=Path, help="coverage rows kept between runs (.npy)"
    )
    parser.add_argument(
        "--focus", type=str, default="", help="bins swept every round, comma-separated"
    )
    parser.add_argument("--start", type=Path, help="weights to start from (default: Daniel's)")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--log", type=Path, required=True)
    args = parser.parse_args(argv)

    source = load_source()
    scaled = rescale(source, args.multiplier, args.denominator)
    if args.start is not None:
        # a weighting of the same source points at any scale: keep this run's geometry
        start = parse_certificate(args.start.read_bytes())
        if not _same_points(start, scaled):
            raise ValueError("--start is not a weighting of the source's points")
        scaled = Certificate(
            scaled.s_num,
            scaled.s_den,
            scaled.denominator,
            start.weight_scale,
            tuple(
                (x, y, w)
                for (x, y, _), (_, _, w) in zip(scaled.points, start.points, strict=True)
            ),
        )
    orbits = d4_orbits(scaled)
    orbit_of = np.empty(len(scaled.points), dtype=np.int64)
    for o, orbit in enumerate(orbits):
        orbit_of[list(orbit)] = o
    sizes = np.array([len(o) for o in orbits], dtype=np.float64)
    rows = Rows(orbit_of, len(orbits))
    if args.rows_cache is not None and args.rows_cache.exists():
        for row in np.load(args.rows_cache):
            key = row.tobytes()
            if key not in rows.seen:
                rows.seen.add(key)
                rows.rows.append(row)
    focus = sorted({int(k) for k in args.focus.split(",") if k.strip()})
    current = scaled
    last = bin_count(args.net)
    args.log.parent.mkdir(parents=True, exist_ok=True)
    candidate = args.work / "reweight-candidate.txt"
    for round_index in range(args.rounds):
        started = time.monotonic()
        candidate.write_text(current.text(), encoding="ascii")
        offset = (round_index * 7) % args.stride
        bins = list(range(offset, last, args.stride))
        bins = sorted(set(bins) | {0} | {k for k in focus if 0 <= k < last})
        threshold = int(current.weight_scale * (1 + args.slack))
        cells, least = dump_rows(
            args.work, candidate, args.net, bins, threshold, workers=args.workers
        )
        frames: dict[int, _Frame] = {}
        added = 0
        for frame, cell, _ in cells:
            if frame.k not in frames:
                frames[frame.k] = _Frame(current, frame)
            added += rows.add(frames[frame.k].members(cell))
        weights = solve(rows, sizes, args.margin)
        current = with_weights(current, orbits, weights)
        record = {
            "round": round_index,
            "offset": offset,
            "bins": len(bins),
            "least_before": least,
            "cells": len(cells),
            "rows_added": added,
            "rows": len(rows.rows),
            "lp_total": float(sizes @ weights),
            "total": str(current.total_weight),
            "total_float": float(current.total_weight),
            "seconds": round(time.monotonic() - started, 1),
        }
        print(json.dumps(record), flush=True)
        with args.log.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record) + "\n")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(current.text(), encoding="ascii")
        if args.rows_cache is not None:
            np.save(args.rows_cache, np.vstack(rows.rows))
        if added == 0 and least is not None and Fraction(least) >= 1:
            break
    return 0 if current.total_weight < 12 else 1


if __name__ == "__main__":
    raise SystemExit(main())
