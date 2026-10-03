"""Attack the clean-room measure verifier with certificates a sound checker must refuse.

An adversarial review tool for `sqverify-fast` (`packing/sqverify_fast`). Every refusal
expectation rests on an exact witness that this tool computes on its own: a centre
where the mutated measure captures, in exact rational arithmetic, less than the
threshold. The rectangle capture is `sqpack.rectangle_density.exact_intersection_area`;
the D4 expansion, the point and segment capture and the axis-direction minimum are
written here, apart from the crate and from `devtools.check_sqverify_fast`.

Families (`--family`, repeatable; default all):

- `axis-exact`: random rectangle measures at direction zero, whose capture is bilinear
  on the event grid, so the exact global minimum over the whole centre domain is
  computed by enumerating vertices. The weights are scaled so that the minimum is the
  threshold minus `2^-k`; the verifier must refuse. At exactly the threshold it may
  verify.
- `pinned`: random measures of formats T, M and L with nasty geometry (slivers, extreme
  densities, coordinates between adjacent binary64 values, points and segments on the
  container's edges), at a random direction. An approximate minimiser is found in
  floating point, the capture there is computed exactly, and the weights are scaled to
  put it a hair under the threshold; the verifier must refuse.
- `edge-atoms`: format L measures with a point or segment exactly on, or a tiny
  rational distance outside, the boundary of the square at a binary64 centre, scaled
  so that the exact capture there is under the threshold; the verifier must refuse,
  and `--probe` must give a centre bound no larger than the exact capture.
- `retained`: retained certificates mutated (scaled to a hair under the threshold at
  the verifier's own least-bound box, one orbit dropped, one orbit nudged by a tiny
  rational) with a witness computed exactly; the verifier must refuse.
- `differential`: `--probe` on random measures at random centres and boxes. The crate's
  exact capture must equal this tool's; its centre and box bounds must not exceed the
  exact capture at the centre and at random rational points of the box.
- `admission`: malformed or premise-violating inputs, which must exit 2.

A verdict of `VERIFIED` (exit 0) on a certificate with an exact witness is a false
acceptance: the tool saves the certificate under `--out` and exits 1. From `packing/`::

    .venv/bin/python3 -m devtools.attack_sqverify_fast \\
        --binary sqverify_fast/target/release/sqverify-fast --budget-seconds 600 \\
        --out benchmarks/measure-verifier/review-rb
"""

from __future__ import annotations

import argparse
import gzip
import json
import math
import random
import subprocess
import sys
import tempfile
import time
from collections import Counter
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any

from sqpack.rectangle_density import exact_intersection_area

PROJECT = Path(__file__).resolve().parents[1]
WEB = PROJECT / "resources/web"
STEP = Fraction(83, 40000)
FAMILIES = ("axis-exact", "pinned", "edge-atoms", "retained", "differential", "admission")

type Pt = tuple[Fraction, Fraction]


# ----------------------------------------------------------------- exact model


@dataclass
class Measure:
    """An orbit-representative measure, the way a certificate lists it."""

    side: Fraction
    core: Fraction
    fmt: str  # "T", "M" or "L"
    rects: list[tuple[Fraction, Fraction, Fraction, Fraction, Fraction]] = field(
        default_factory=list
    )  # x1, y1, x2, y2, orbit mass
    points: list[tuple[Fraction, Fraction, Fraction]] = field(default_factory=list)
    segments: list[tuple[Fraction, Fraction, Fraction, Fraction, Fraction]] = field(
        default_factory=list
    )
    threshold: Fraction = Fraction(1)

    def mass(self) -> Fraction:
        return (
            sum((r[4] for r in self.rects), Fraction(0))
            + sum((p[2] for p in self.points), Fraction(0))
            + sum((s[4] for s in self.segments), Fraction(0))
        )

    def scaled(self, k: Fraction) -> Measure:
        return Measure(
            self.side,
            self.core,
            self.fmt,
            [(*r[:4], r[4] * k) for r in self.rects],
            [(*p[:2], p[2] * k) for p in self.points],
            [(*s[:4], s[4] * k) for s in self.segments],
            self.threshold,
        )


def images(side: Fraction, x: Fraction, y: Fraction) -> list[Pt]:
    """The eight images of a point under the symmetries of the container."""

    rx, ry = side - x, side - y
    return [(x, y), (rx, y), (x, ry), (rx, ry), (y, x), (ry, x), (y, rx), (ry, rx)]


@dataclass
class Expanded:
    """The D4-expanded measure: rectangles with densities, points and segments with masses."""

    rects: list[tuple[Fraction, Fraction, Fraction, Fraction, Fraction]]
    points: list[tuple[Fraction, Fraction, Fraction]]
    segments: list[tuple[Fraction, Fraction, Fraction, Fraction, Fraction]]


def expand(m: Measure) -> Expanded:
    rects = []
    for x1, y1, x2, y2, w in m.rects:
        if w == 0:
            continue
        density = w / 8 / ((x2 - x1) * (y2 - y1))
        for (a, b), (c, d) in zip(images(m.side, x1, y1), images(m.side, x2, y2), strict=True):
            rects.append((min(a, c), min(b, d), max(a, c), max(b, d), density))
    points = [(x, y, w / 8) for px, py, w in m.points if w for x, y in images(m.side, px, py)]
    segments = []
    for x0, y0, x1, y1, w in m.segments:
        if w == 0:
            continue
        for (a, b), (c, d) in zip(images(m.side, x0, y0), images(m.side, x1, y1), strict=True):
            segments.append((a, b, c, d, w / 8))
    return Expanded(rects, points, segments)


def direction(index: int) -> tuple[Fraction, Fraction]:
    t = index * STEP
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def corners(x: Fraction, y: Fraction, c: Fraction, s: Fraction, b: Fraction) -> list[Pt]:
    h = b / 2
    return [
        (x + c * u * h - s * v * h, y + s * u * h + c * v * h)
        for u, v in ((-1, -1), (1, -1), (1, 1), (-1, 1))
    ]


def domain_half(m: Measure, index: int) -> Fraction:
    """Distance from the container's edge to the domain's edge, inside both domains."""

    c, s = direction(index)
    a = m.core * (c + s) / 2
    if m.fmt == "M":
        t = index * STEP
        aa = max(t - STEP / 2, Fraction(0))
        a = max(a, (1 + 2 * aa - aa * aa) / (2 * (1 + aa * aa)))
    return a


def capture(e: Expanded, b: Fraction, x: Fraction, y: Fraction, index: int) -> Fraction:
    """Exact mass in the closed side-`b` square centred at `(x, y)` at net index `index`."""

    c, s = direction(index)
    poly = corners(x, y, c, s, b)
    left = min(p[0] for p in poly)
    right = max(p[0] for p in poly)
    bottom = min(p[1] for p in poly)
    top = max(p[1] for p in poly)
    total = Fraction(0)
    for x1, y1, x2, y2, rho in e.rects:
        if x2 <= left or x1 >= right or y2 <= bottom or y1 >= top:
            continue
        total += rho * exact_intersection_area((x1, y1, x2, y2), poly)
    h = b / 2

    def local(px: Fraction, py: Fraction) -> Pt:
        dx, dy = px - x, py - y
        return c * dx + s * dy, c * dy - s * dx

    for px, py, w in e.points:
        u, v = local(px, py)
        if abs(u) <= h and abs(v) <= h:
            total += w
    for x0, y0, x1, y1, w in e.segments:
        u0, v0 = local(x0, y0)
        u1, v1 = local(x1, y1)
        lo, hi = Fraction(0), Fraction(1)
        for a0, a1 in ((u0, u1), (v0, v1)):
            d = a1 - a0
            if d == 0:
                if abs(a0) > h:
                    hi = lo
                continue
            ta, tb = (-h - a0) / d, (h - a0) / d
            lo, hi = max(lo, min(ta, tb)), min(hi, max(ta, tb))
        if hi > lo:
            total += w * (hi - lo)
    return total


# ----------------------------------------------------- float model, for aiming


def _clip(
    poly: list[tuple[float, float]], axis: int, edge: float, *, keep_above: bool
) -> list[tuple[float, float]]:
    out: list[tuple[float, float]] = []
    if not poly:
        return out
    prev = poly[-1]
    prev_in = (prev[axis] >= edge) if keep_above else (prev[axis] <= edge)
    for cur in poly:
        cur_in = (cur[axis] >= edge) if keep_above else (cur[axis] <= edge)
        if cur_in != prev_in:
            t = (prev[axis] - edge) / (prev[axis] - cur[axis])
            out.append((prev[0] + t * (cur[0] - prev[0]), prev[1] + t * (cur[1] - prev[1])))
        if cur_in:
            out.append(cur)
        prev, prev_in = cur, cur_in
    return out


@dataclass
class FloatModel:
    rects: list[tuple[float, float, float, float, float]]
    points: list[tuple[float, float, float]]
    segments: list[tuple[float, float, float, float, float]]
    b: float

    @classmethod
    def of(cls, e: Expanded, b: Fraction) -> FloatModel:
        return cls(
            [tuple(float(v) for v in r) for r in e.rects],  # type: ignore[misc]
            [tuple(float(v) for v in p) for p in e.points],  # type: ignore[misc]
            [tuple(float(v) for v in sg) for sg in e.segments],  # type: ignore[misc]
            float(b),
        )

    def value(self, x: float, y: float, c: float, s: float) -> float:
        h = self.b / 2
        poly = [
            (x + c * u * h - s * v * h, y + s * u * h + c * v * h)
            for u, v in ((-1, -1), (1, -1), (1, 1), (-1, 1))
        ]
        ext = h * (c + s)
        total = 0.0
        for x1, y1, x2, y2, rho in self.rects:
            if x2 <= x - ext or x1 >= x + ext or y2 <= y - ext or y1 >= y + ext:
                continue
            p = poly
            for axis, edge, above in (
                (0, x1, True),
                (0, x2, False),
                (1, y1, True),
                (1, y2, False),
            ):
                p = _clip(p, axis, edge, keep_above=above)
                if len(p) < 3:
                    break
            if len(p) >= 3:
                area = 0.0
                for i, a in enumerate(p):
                    q = p[(i + 1) % len(p)]
                    area += a[0] * q[1] - a[1] * q[0]
                total += rho * abs(area) / 2
        for px, py, w in self.points:
            dx, dy = px - x, py - y
            if abs(c * dx + s * dy) <= h and abs(c * dy - s * dx) <= h:
                total += w
        for x0, y0, x1, y1, w in self.segments:
            # Midpoint sampling is enough for aiming.
            inside = 0
            for k in range(16):
                lam = (k + 0.5) / 16
                dx, dy = x0 + lam * (x1 - x0) - x, y0 + lam * (y1 - y0) - y
                if abs(c * dx + s * dy) <= h and abs(c * dy - s * dx) <= h:
                    inside += 1
            total += w * inside / 16
        return total


def aim_minimum(
    m: Measure, index: int, rng: random.Random, grid: int = 24
) -> tuple[float, float]:
    """An approximate minimiser of the capture over the centre domain, in floats."""

    fm = FloatModel.of(expand(m), m.core)
    c, s = (float(v) for v in direction(index))
    a = float(domain_half(m, index))
    lo, hi = a, float(m.side) - a
    best = (math.inf, (lo + hi) / 2, (lo + hi) / 2)
    for i in range(grid + 1):
        for j in range(grid + 1):
            x = lo + (hi - lo) * i / grid
            y = lo + (hi - lo) * j / grid
            v = fm.value(x, y, c, s)
            if v < best[0]:
                best = (v, x, y)
    step = (hi - lo) / grid
    v, x, y = best
    while step > 1e-9 * max(1.0, hi):
        moved = False
        for ddx, ddy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
            nx = min(max(x + ddx * step, lo), hi)
            ny = min(max(y + ddy * step, lo), hi)
            nv = fm.value(nx, ny, c, s)
            if nv < v:
                v, x, y, moved = nv, nx, ny, True
                break
        if not moved:
            step /= 2
    del rng
    return x, y


def floor_ratio(q: Fraction, bits: int) -> Fraction:
    """The largest dyadic `p/2^bits` not above `q`."""

    return Fraction(math.floor(q * 2**bits), 2**bits)


def pin(m: Measure, witness_capture: Fraction, eps: Fraction) -> Measure:
    """Scale so that the capture at the witness is at most `threshold (1 - eps)`."""

    target = m.threshold * (1 - eps)
    bits = max(64, int(-math.log2(float(eps))) + 40) if eps > 0 else 400
    k = floor_ratio(target / witness_capture, bits)
    return m.scaled(k)


# ------------------------------------------------------------------ serialise


def tok(q: Fraction) -> str:
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def to_json(m: Measure, n: int) -> dict[str, Any]:
    if m.fmt == "T":
        return {
            "n": n,
            "L": tok(m.side),
            "B": tok(m.core),
            "rectangles": [[tok(v) for v in r[:4]] for r in m.rects],
            "weights": [tok(r[4]) for r in m.rects],
            "coverage_lower_bound_exact": tok(m.threshold),
        }
    if m.fmt == "M":
        return {
            "n": n,
            "L": tok(m.side),
            "B": tok(m.core),
            "rectangles": [
                {"rectangle": [tok(v) for v in r[:4]], "mass": tok(r[4])} for r in m.rects
            ],
            "points": [],
        }
    prims: list[dict[str, Any]] = [
        {"kind": "rectangle", "geometry": [tok(v) for v in r[:4]], "mass": tok(r[4])}
        for r in m.rects
    ]
    prims += [
        {"kind": "point", "geometry": [tok(p[0]), tok(p[1])], "mass": tok(p[2])}
        for p in m.points
    ]
    prims += [
        {"kind": "segment", "geometry": [tok(v) for v in sg[:4]], "mass": tok(sg[4])}
        for sg in m.segments
    ]
    return {
        "schema": "point_line_rectangle_v1",
        "n": n,
        "L": tok(m.side),
        "B": tok(m.core),
        "net": {"step": "83/40000", "last": 200},
        "primitives": prims,
    }


def n_for(m: Measure) -> int:
    return math.floor(m.mass()) + 1


@dataclass
class Runner:
    binary: Path
    work: Path
    out: Path
    max_nodes: int
    seed: int
    log: list[dict[str, Any]] = field(default_factory=list)
    failures: int = 0
    notable: int = 0
    counter: int = 0

    def write(self, data: dict[str, Any]) -> Path:
        self.counter += 1
        path = self.work / f"c{self.counter}.json"
        path.write_text(json.dumps(data))
        return path

    def run(
        self, path: Path, n: int, *extra: str, timeout: float = 900
    ) -> tuple[int, list[dict[str, Any]], str]:
        try:
            r = subprocess.run(
                [str(self.binary), "--candidate", str(path), "--n", str(n), *extra],
                capture_output=True,
                text=True,
                check=False,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return -1, [], "timeout"
        lines = [json.loads(line) for line in r.stdout.splitlines() if line.startswith("{")]
        return r.returncode, lines, r.stderr.strip()

    def expect_refusal(
        self, family: str, m: Measure, index: int, witness: Pt, exact: Fraction, *, note: str
    ) -> None:
        """Run one direction of a certificate with an exact witness below threshold."""

        assert exact < m.threshold
        n = n_for(m)
        data = to_json(m, n)
        path = self.write(data)
        start = time.monotonic()
        code, lines, err = self.run(
            path, n, "--directions", str(index), "--max-nodes", str(self.max_nodes), "--confirm"
        )
        receipt = next((x for x in lines if "r" in x), {})
        row: dict[str, Any] = {
            "family": family,
            "note": note,
            "format": m.fmt,
            "r": index,
            "witness": [str(witness[0]), str(witness[1])],
            "deficit": float((m.threshold - exact) / m.threshold),
            "exit": code,
            "verdict": receipt.get("verdict"),
            "seconds": round(time.monotonic() - start, 3),
        }
        if code == 2:
            row["admission"] = err[:200]
        wit = receipt.get("witness", {})
        if "exact_coverage" in wit:
            row["crate_exact_below"] = wit.get("exact_below_threshold")
            px, py = (Fraction(v) for v in wit["exact_pose"])
            mine = capture(expand(m), m.core, px, py, index)
            if mine != Fraction(wit["exact_coverage"]):
                row["oracle_disagreement"] = [str(mine), wit["exact_coverage"]]
                self.fail(row, data)
        if code == 0:
            row["FALSE_ACCEPTANCE"] = True
            self.fail(row, data)
        elif row["verdict"] == "audit-failed":
            self.notable += 1
            with gzip.open(
                self.out / f"audit-failed-s{self.seed}-{self.notable:03d}.json.gz", "wt"
            ) as handle:
                json.dump({"row": row, "candidate": data}, handle)
        self.log.append(row)

    def fail(self, row: dict[str, Any], data: dict[str, Any]) -> None:
        self.failures += 1
        name = self.out / f"reproducer-s{self.seed}-{self.failures:03d}.json.gz"
        with gzip.open(name, "wt") as handle:
            json.dump({"row": row, "candidate": data}, handle)
        print("FAILURE", json.dumps(row), file=sys.stderr)


# ------------------------------------------------------------ random measures


def nasty(rng: random.Random, lo: Fraction, hi: Fraction) -> Fraction:
    """A coordinate in `[lo, hi]`, sometimes between adjacent binary64 values."""

    u = lo + (hi - lo) * Fraction(rng.randrange(10**6), 10**6)
    kind = rng.random()
    if kind < 0.25:
        f = float(u)
        g = math.nextafter(f, math.inf)
        u = (Fraction(f) + Fraction(g)) / 2 + Fraction(rng.choice((-1, 1)), 10**40)
    elif kind < 0.35:
        u = Fraction(rng.choice((lo, hi)))
    elif kind < 0.45:
        u = Fraction(f"{rng.random() * float(hi - lo) + float(lo):.25f}")
    return min(max(u, lo), hi)


def random_measure(rng: random.Random, fmt: str) -> Measure:
    side = Fraction(rng.randrange(150, 450), 100)
    core = rng.choice(
        (Fraction(9977, 10000), Fraction(1, 2), Fraction(997, 1000), Fraction(3, 4))
    )
    m = Measure(side, core, fmt)
    m.threshold = rng.choice((Fraction(1), Fraction(10001, 10000)))
    if fmt != "T":
        m.threshold = Fraction(1)
    for _ in range(rng.randrange(3, 12)):
        x1 = nasty(rng, Fraction(0), side)
        y1 = nasty(rng, Fraction(0), side)
        shape = rng.random()
        if shape < 0.2:
            w = Fraction(1, 10 ** rng.randrange(6, 16))  # sliver
        else:
            w = Fraction(rng.randrange(1, 1000), 1000) * side / 2
        hgt = Fraction(rng.randrange(1, 1000), 1000) * side / 2
        if rng.random() < 0.5:
            w, hgt = hgt, w
        x2 = min(x1 + w, side)
        y2 = min(y1 + hgt, side)
        if x2 <= x1 or y2 <= y1:
            continue
        mass = Fraction(rng.randrange(1, 10**4), 10**3)
        if rng.random() < 0.1:
            mass *= 10**6  # extreme density
        m.rects.append((x1, y1, x2, y2, mass))
    if fmt == "L":
        for _ in range(rng.randrange(1, 8)):
            m.points.append(
                (
                    nasty(rng, Fraction(0), side),
                    nasty(rng, Fraction(0), side),
                    Fraction(rng.randrange(1, 500), 1000),
                )
            )
        for _ in range(rng.randrange(1, 6)):
            x0, y0 = nasty(rng, Fraction(0), side), nasty(rng, Fraction(0), side)
            if rng.random() < 0.3:
                x1, y1 = x0, nasty(rng, Fraction(0), side)  # axis-parallel
            else:
                x1, y1 = nasty(rng, Fraction(0), side), nasty(rng, Fraction(0), side)
            if (x0, y0) != (x1, y1):
                m.segments.append((x0, y0, x1, y1, Fraction(rng.randrange(1, 500), 1000)))
    if not m.rects and fmt != "L":
        m.rects.append((Fraction(0), Fraction(0), side, side, Fraction(1)))
    # A uniform floor keeps the capture positive everywhere, so a pin is defined.
    m.rects.append(
        (Fraction(0), Fraction(0), side, side, side * side * Fraction(rng.randrange(1, 4), 2))
    )
    return m


EPSILONS = (
    Fraction(1, 10**6),
    Fraction(1, 10**12),
    Fraction(1, 2**53),
    Fraction(1, 2**80),
    Fraction(1, 2**200),
)


def family_pinned(run: Runner, rng: random.Random) -> None:
    fmt = rng.choice("TML")
    m = random_measure(rng, fmt)
    index = rng.choice((0, 1, 2, rng.randrange(201), 100, 199, 200))
    x, y = aim_minimum(m, index, rng)
    witness = (Fraction(x), Fraction(y))
    e = expand(m)
    f = capture(e, m.core, *witness, index)
    if f <= 0:
        return
    eps = rng.choice(EPSILONS)
    pm = pin(m, f, eps)
    exact = capture(expand(pm), pm.core, *witness, index)
    run.expect_refusal("pinned", pm, index, witness, exact, note=f"eps={float(eps):.3g}")


def axis_minimum(m: Measure) -> tuple[Fraction, Pt]:
    """Exact minimum of the axis-aligned capture over `[B/2, L - B/2]^2` (rectangles only)."""

    e = expand(m)
    h = m.core / 2
    lo, hi = h, m.side - h
    events = {lo, hi}
    for x1, y1, x2, y2, _ in e.rects:
        for v in (x1, x2, y1, y2):
            for w in (v - h, v + h):
                if lo < w < hi:
                    events.add(w)
    grid = sorted(events)

    def overlap(p: Fraction, a: Fraction, b: Fraction) -> Fraction:
        return max(Fraction(0), min(p + h, b) - max(p - h, a))

    ox = [[overlap(p, r[0], r[2]) for p in grid] for r in e.rects]
    oy = [[overlap(p, r[1], r[3]) for p in grid] for r in e.rects]
    best: tuple[Fraction, Pt] | None = None
    for i, px in enumerate(grid):
        active = [(k, r[4] * ox[k][i]) for k, r in enumerate(e.rects) if ox[k][i]]
        for j, py in enumerate(grid):
            v = sum((a * oy[k][j] for k, a in active), Fraction(0))
            if best is None or v < best[0]:
                best = (v, (px, py))
    assert best is not None
    return best


def family_axis_exact(run: Runner, rng: random.Random) -> None:
    m = random_measure(rng, "T")
    m.rects = m.rects[:6]
    low, where = axis_minimum(m)
    if low <= 0:
        return
    # Exactly at the threshold, then a hair under it.
    at = m.scaled(m.threshold / low)
    n = n_for(at)
    code, _, err = run.run(run.write(to_json(at, n)), n, "--directions", "0")
    run.log.append(
        {
            "family": "axis-exact",
            "note": "minimum equal to threshold",
            "exit": code,
            "err": err[:120],
        }
    )
    for k in (20, 52, 60, 120, 400):
        eps = Fraction(1, 2**k)
        pm = m.scaled(m.threshold * (1 - eps) / low)
        exact = capture(expand(pm), pm.core, *where, 0)
        run.expect_refusal(
            "axis-exact", pm, 0, where, exact, note=f"minimum = threshold - 2^-{k} relative"
        )


def family_edge_atoms(run: Runner, rng: random.Random) -> None:
    m = random_measure(rng, "L")
    m.points, m.segments = [], []
    index = rng.choice((0, 1, rng.randrange(201), 200))
    c, s = direction(index)
    a = domain_half(m, index)
    xf = float(a + (m.side - 2 * a) * Fraction(rng.randrange(1, 999), 1000))
    yf = float(a + (m.side - 2 * a) * Fraction(rng.randrange(1, 999), 1000))
    x, y = Fraction(xf), Fraction(yf)
    poly = corners(x, y, c, s, m.core)
    gap = rng.choice(
        (Fraction(0), Fraction(1, 10**40), Fraction(1, 2**60), Fraction(1, 10**15))
    )
    k = rng.randrange(4)
    p, q = poly[k], poly[(k + 1) % 4]
    # Outward normal of edge p -> q (counterclockwise polygon).
    nx, ny = q[1] - p[1], p[0] - q[0]
    norm = abs(nx) + abs(ny)
    nx, ny = nx / norm, ny / norm
    kind = rng.choice(("corner", "edge-point", "segment-end", "segment-parallel"))
    mid = ((p[0] + q[0]) / 2 + gap * nx, (p[1] + q[1]) / 2 + gap * ny)
    corner = (p[0] + gap * nx, p[1] + gap * ny)
    heavy = Fraction(rng.randrange(1, 4), 2)

    def inside_box(pt: Pt) -> bool:
        return 0 <= pt[0] <= m.side and 0 <= pt[1] <= m.side

    if kind == "corner" and inside_box(corner):
        m.points.append((*corner, heavy))
    elif kind == "edge-point" and inside_box(mid):
        m.points.append((*mid, heavy))
    elif kind == "segment-end":
        outer = (mid[0] + nx * m.core / 3, mid[1] + ny * m.core / 3)
        if inside_box(outer) and inside_box(mid):
            # From outside, ending on (or `gap` beyond) the edge.
            m.segments.append((*outer, *mid, heavy))
    elif kind == "segment-parallel":
        a0 = (p[0] + gap * nx, p[1] + gap * ny)
        a1 = (q[0] + gap * nx, q[1] + gap * ny)
        if inside_box(a0) and inside_box(a1) and a0 != a1:
            m.segments.append((*a0, *a1, heavy))
    if not (m.points or m.segments):
        return
    e = expand(m)
    f = capture(e, m.core, x, y, index)
    if f <= 0:
        return
    # Probe differential at the centre.
    n = n_for(m)
    path = run.write(to_json(m, n))
    code, lines, err = run.run(path, n, "--probe", f"{index},{xf!r},{yf!r}")
    row: dict[str, Any] = {
        "family": "edge-atoms-probe",
        "note": f"{kind} gap={float(gap):.3g}",
        "r": index,
    }
    if code == 0 and lines:
        crate_exact = Fraction(lines[0]["exact_coverage"])
        centre = Fraction(lines[0]["centre_lower_bound"])
        row["agree"] = crate_exact == f
        row["sound"] = centre <= f
        if crate_exact != f or centre > f:
            row["exact"] = str(f)
            row["crate"] = lines[0]
            run.fail(row, to_json(m, n))
    else:
        row["exit"] = code
        row["err"] = err[:200]
    run.log.append(row)
    eps = rng.choice(EPSILONS)
    pm = pin(m, f, eps)
    exact = capture(expand(pm), pm.core, x, y, index)
    run.expect_refusal(
        "edge-atoms",
        pm,
        index,
        (x, y),
        exact,
        note=f"{kind} gap={float(gap):.3g} eps={float(eps):.3g}",
    )


def family_differential(run: Runner, rng: random.Random) -> None:
    fmt = rng.choice("TML")
    m = random_measure(rng, fmt)
    n = n_for(m)
    data = to_json(m, n)
    path = run.write(data)
    e = expand(m)
    for _ in range(4):
        index = rng.randrange(201)
        a = domain_half(m, index)
        xf = float(a + (m.side - 2 * a) * Fraction(rng.random()))
        yf = float(a + (m.side - 2 * a) * Fraction(rng.random()))
        half = 10.0 ** rng.uniform(-9, -2)
        code, lines, err = run.run(
            path, n, "--probe", f"{index},{xf!r},{yf!r},{half!r},{half!r}"
        )
        row: dict[str, Any] = {"family": "differential", "format": fmt, "r": index}
        if code != 0 or not lines:
            row.update(exit=code, err=err[:200])
            run.log.append(row)
            continue
        reading = lines[0]
        x, y = Fraction(xf), Fraction(yf)
        mine = capture(e, m.core, x, y, index)
        crate = Fraction(reading["exact_coverage"])
        centre = Fraction(reading["centre_lower_bound"])
        box = Fraction(reading["box_lower_bound"])
        box_min = mine
        hq = Fraction(half)
        for _ in range(3):
            px = x + hq * Fraction(rng.randrange(-1000, 1001), 1000)
            py = y + hq * Fraction(rng.randrange(-1000, 1001), 1000)
            box_min = min(box_min, capture(e, m.core, px, py, index))
        row.update(
            agree=crate == mine,
            centre_sound=centre <= mine,
            box_sound=box <= box_min,
            centre_gap=float(mine - centre),
        )
        if crate != mine or centre > mine or box > box_min:
            row.update(
                exact=str(mine), box_min=str(box_min), crate=reading, x=xf, y=yf, half=half
            )
            run.fail(row, data)
        run.log.append(row)


# ----------------------------------------------------- retained certificates


def load_retained(path: Path) -> tuple[Measure, int]:
    with gzip.open(path, "rt") as handle:
        data = json.load(handle, parse_float=Fraction, parse_int=Fraction)

    def q(v: Any) -> Fraction:
        return Fraction(v)

    side, core = q(data["L"]), q(data["B"])
    n = int(data["n"])
    if data.get("schema") == "point_line_rectangle_v1":
        m = Measure(side, core, "L")
        for p in data["primitives"]:
            g = [q(v) for v in p["geometry"]]
            if p["kind"] == "point":
                m.points.append((g[0], g[1], q(p["mass"])))
            elif p["kind"] == "segment":
                m.segments.append((g[0], g[1], g[2], g[3], q(p["mass"])))
            else:
                m.rects.append((g[0], g[1], g[2], g[3], q(p["mass"])))
        return m, n
    rows = data["rectangles"]
    if rows and isinstance(rows[0], dict):
        m = Measure(side, core, "M")
        for row in rows:
            g = [q(v) for v in row["rectangle"]]
            m.rects.append((g[0], g[1], g[2], g[3], q(row["mass"])))
        return m, n
    m = Measure(side, core, "T")
    m.threshold = q(data.get("coverage_lower_bound_exact", 1))
    for row, w in zip(rows, data["weights"], strict=True):
        if q(w):
            g = [q(v) for v in row]
            m.rects.append((g[0], g[1], g[2], g[3], q(w)))
    return m, n


RETAINED = (
    "wand125-rectangle-certificates-2026-09-27/wand125-rectangles/certificates/rect_n32_L595/certified_candidate.json.gz",
    "external-square-certificates-2026-09-22/wand125-density/certificates/cert_n11_L381/certified_candidate.json.gz",
)


def retained_paths() -> list[Path]:
    out = [WEB / p for p in RETAINED if (WEB / p).exists()]
    for pattern in ("mixed_n37_*", "mixed_n101_*"):
        out += sorted(WEB.glob(f"wand125-*/**/{pattern}/candidate.json.gz"))[:1]
    return out


def family_retained(run: Runner, rng: random.Random) -> None:
    path = rng.choice(retained_paths())
    m, n = load_retained(path)
    index = rng.choice((0, 1, rng.randrange(201), 200))
    code, lines, err = run.run(path, n, "--directions", str(index))
    receipt = next((x for x in lines if "r" in x), {})
    box = receipt.get("least_bound_box")
    e = expand(m)
    cands: list[Pt] = []
    if box:
        x, y, dx, dy = (Fraction(box[k]) for k in ("x", "y", "dx", "dy"))
        cands = [(x, y), (x - dx, y - dy), (x + dx, y + dy), (x - dx, y + dy), (x + dx, y - dy)]
    elif receipt.get("argmin"):
        cands = [tuple(Fraction(v) for v in receipt["argmin"])]  # type: ignore[list-item]
    a = domain_half(m, index)
    cands = [p for p in cands if a <= p[0] <= m.side - a and a <= p[1] <= m.side - a]
    mutation = rng.choice(("scale", "drop", "nudge"))
    if mutation == "drop" and len(m.rects) > 1:
        j = rng.randrange(len(m.rects) + len(m.points))
        if j < len(m.rects):
            x1, y1, x2, y2, _ = m.rects.pop(j)
            cands.append(((x1 + x2) / 2, (y1 + y2) / 2))
            note = f"drop rect {j}"
        else:
            px, py, _ = m.points.pop(j - len(m.rects))
            cands.append((px, py))
            note = f"drop point {j - len(m.rects)}"
        e = expand(m)
    elif mutation == "nudge" and m.rects:
        j = rng.randrange(len(m.rects))
        delta = rng.choice((Fraction(1, 10**30), Fraction(1, 10**12), Fraction(1, 2**52)))
        x1, y1, x2, y2, w = m.rects[j]
        if x2 + delta <= m.side:
            m.rects[j] = (x1 + delta, y1, x2 + delta, y2, w)
        note = f"nudge rect {j} by {float(delta):.3g}"
        e = expand(m)
    else:
        note = "scale"
    cands = [p for p in cands if a <= p[0] <= m.side - a and a <= p[1] <= m.side - a]
    if not cands:
        run.log.append(
            {
                "family": "retained",
                "note": f"{note}: no witness in domain",
                "exit": code,
                "err": err[:80],
            }
        )
        return
    values = [(capture(e, m.core, *p, index), p) for p in cands]
    f, where = min(values)
    if f >= m.threshold:
        eps = rng.choice(EPSILONS[:4])
        m = pin(m, f, eps)
        note += f" pinned eps={float(eps):.3g}"
        f = capture(expand(m), m.core, *where, index)
    run.expect_refusal("retained", m, index, where, f, note=f"{path.parent.name}: {note}")


# ----------------------------------------------------------------- admission


def family_admission(run: Runner, rng: random.Random) -> None:
    del rng
    base = {
        "n": 3,
        "L": "2",
        "B": "9977/10000",
        "rectangles": [["0", "0", "2", "2"]],
        "weights": ["5/2"],
    }
    cases: list[tuple[str, Any, int]] = [
        ("mass equal to n", {**base, "weights": ["3"]}, 3),
        (
            "mass a hair under n",
            {
                **base,
                "weights": ["2999999999999999999999999999999/1000000000000000000000000000000"],
            },
            3,
        ),
        ("B (1 + D) = 1", {**base, "B": "40000/40083"}, 3),
        (
            "rectangle past the edge by 1e-30",
            {**base, "rectangles": [["0", "0", "2.000000000000000000000000000001", "2"]]},
            3,
        ),
        (
            "negative zero weight beside",
            {
                **base,
                "rectangles": [["0", "0", "2", "2"], ["0", "0", "1", "1"]],
                "weights": ["5/2", "-0"],
            },
            3,
        ),
        (
            "tiny negative weight",
            {
                **base,
                "rectangles": [["0", "0", "2", "2"], ["0", "0", "1", "1"]],
                "weights": ["5/2", "-1e-300"],
            },
            3,
        ),
        ("NaN weight", {**base, "weights": ["NaN"]}, 3),
        ("huge exponent", {**base, "weights": ["1e999999"]}, 3),
        ("n mismatch", {**base, "n": 4}, 3),
        ("n as float", {**base, "n": 3.0}, 3),
        ("threshold below one", {**base, "coverage_lower_bound_exact": "9999/10000"}, 3),
        ("metadata L disagrees", {**base, "certificate": {"L": "2.0000001"}}, 3),
        (
            "net overridden to 2 directions",
            {**base, "B": "1/2", "certificate": {"D": "1/2", "angle_count": 2}},
            3,
        ),
        (
            "net overridden, coarse",
            {**base, "B": "1/2", "certificate": {"D": "9/20", "angle_count": 3}},
            3,
        ),
        ("total_mass wrong", {**base, "total_mass": "2.4"}, 3),
        ("degenerate positive rect", {**base, "rectangles": [["0", "0", "0", "2"]]}, 3),
        (
            "format L bad net",
            {
                "schema": "point_line_rectangle_v1",
                "n": 3,
                "L": "2",
                "B": "0.99",
                "net": {"step": "1/400", "last": 200},
                "primitives": [
                    {"kind": "rectangle", "geometry": ["0", "0", "2", "2"], "mass": "2"}
                ],
            },
            3,
        ),
        (
            "format L net fine, metadata D override",
            {
                "schema": "point_line_rectangle_v1",
                "n": 3,
                "L": "2",
                "B": "1/2",
                "net": {"step": "83/40000", "last": 200},
                "certificate": {"D": "9/20", "angle_count": 3},
                "primitives": [
                    {"kind": "rectangle", "geometry": ["0", "0", "2", "2"], "mass": "2"}
                ],
            },
            3,
        ),
        (
            "format M nonempty points",
            {
                "n": 3,
                "L": "2",
                "B": "0.99",
                "rectangles": [{"rectangle": ["0", "0", "2", "2"], "mass": "2"}],
                "points": [[1, 1]],
            },
            3,
        ),
        (
            "zero-length segment",
            {
                "schema": "point_line_rectangle_v1",
                "n": 3,
                "L": "2",
                "B": "0.99",
                "net": {"step": "83/40000", "last": 200},
                "primitives": [
                    {"kind": "segment", "geometry": ["1", "1", "1", "1"], "mass": "2"}
                ],
            },
            3,
        ),
    ]
    for name, data, n in cases:
        if name.startswith("threshold"):
            code, _, err = run.run(run.write(data), n, "--directions", "0")
        else:
            code, _, err = run.run(
                run.write(data), n, "--directions", "0", "--max-nodes", "100000"
            )
        run.log.append({"family": "admission", "note": name, "exit": code, "err": err[:160]})
    # Raw-byte cases.
    for name, raw in (
        (
            "duplicate nested key",
            b'{"n":3,"L":"2","B":"0.99","rectangles":[["0","0","2","2"]],"weights":["2"],"certificate":{"D":"1","D":"83/40000"}}',
        ),
        (
            "trailing text after JSON",
            b'{"n":3,"L":"2","B":"0.99","rectangles":[["0","0","2","2"]],"weights":["2"]} x',
        ),
    ):
        run.counter += 1
        path = run.work / f"c{run.counter}.json"
        path.write_bytes(raw)
        code, _, err = run.run(path, 3, "--directions", "0")
        run.log.append({"family": "admission", "note": name, "exit": code, "err": err[:160]})
    good = {**base}
    payload = gzip.compress(json.dumps(good).encode())
    for name, raw in (
        ("gzip with a second member", payload + gzip.compress(b'{"x":1}')),
        ("gzip with trailing garbage", payload + b"garbage"),
    ):
        run.counter += 1
        path = run.work / f"c{run.counter}.json.gz"
        path.write_bytes(raw)
        code, _, err = run.run(path, 3, "--directions", "0")
        run.log.append({"family": "admission", "note": name, "exit": code, "err": err[:160]})


RUNNERS = {
    "axis-exact": family_axis_exact,
    "pinned": family_pinned,
    "edge-atoms": family_edge_atoms,
    "retained": family_retained,
    "differential": family_differential,
}


def summarise(log: list[dict[str, Any]]) -> dict[str, Any]:
    by: dict[str, Counter[str]] = {}
    for row in log:
        key = row["family"]
        outcome = (
            "FALSE_ACCEPTANCE"
            if row.get("FALSE_ACCEPTANCE")
            else row.get("verdict") or f"exit {row.get('exit')}"
            if "exit" in row
            else "sound"
            if row.get("agree", True)
            and row.get("centre_sound", row.get("sound", True))
            and row.get("box_sound", True)
            else "DISAGREEMENT"
        )
        by.setdefault(key, Counter())[str(outcome)] += 1
    return {k: dict(v) for k, v in sorted(by.items())}


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--binary", type=Path, default=PROJECT / "sqverify_fast/target/release/sqverify-fast"
    )
    parser.add_argument("--budget-seconds", type=float, default=300)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--family", action="append", choices=FAMILIES)
    parser.add_argument("--max-nodes", type=int, default=2_000_000)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    families = args.family or list(FAMILIES)
    rng = random.Random(args.seed)
    with tempfile.TemporaryDirectory() as tmp:
        run = Runner(args.binary, Path(tmp), args.out, args.max_nodes, args.seed)
        if "admission" in families:
            family_admission(run, rng)
        loop = [f for f in families if f != "admission"]
        deadline = time.monotonic() + args.budget_seconds
        rounds = 0
        while loop and time.monotonic() < deadline:
            name = loop[rounds % len(loop)]
            rounds += 1
            try:
                RUNNERS[name](run, rng)
            except (ZeroDivisionError, ValueError) as error:
                run.log.append({"family": name, "note": f"skipped: {error}"})
    log_path = args.out / f"attack-seed{args.seed}.jsonl"
    log_path.write_text("".join(json.dumps(row, default=str) + "\n" for row in run.log))
    summary = {
        "seed": args.seed,
        "rows": len(run.log),
        "failures": run.failures,
        "by_family": summarise(run.log),
    }
    print(json.dumps(summary, indent=1))
    return 1 if run.failures else 0


if __name__ == "__main__":
    sys.exit(main())
