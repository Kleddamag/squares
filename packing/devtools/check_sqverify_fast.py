"""Hold the clean-room measure verifier to an exact oracle and to mutation controls.

Two checks of `sqverify-fast` (`packing/sqverify_fast`), both refusable:

- `differential`: at sampled centres of retained certificates, the verifier's certified
  centre bound must lie below the exact coverage that `sqpack.rectangle_density`
  computes in rational arithmetic, and within `1e-9` of it; its certified bound over a
  small box around the centre must lie below the exact coverage at the box's corners
  and centre.
- `controls`: certificates mutated so that an exact witness centre captures less than
  the threshold must be refused at that direction, while the original is verified
  there; malformed or premise-violating inputs must be refused at admission (exit 2).
  The mutations are the stage-4 controls retained in the 1 October packet (scale every
  weight by 99/100; drop the top contributor) and this tool's own: scale to exactly
  one part in a million below the threshold at the witness, drop the orbit that
  contributes most at the least-bound box's centre, push the mass to `n`, and six
  format violations.
- `mixed`: the same for formats M and L (`think-4vf7`). The differential compares
  with an exact evaluator of points, segments and rectangles written here, apart from
  the crate's oracle; the controls are the retained stage-4 controls of the mixed n37
  and linear n101 certificates, a scaling to one part in a million below the threshold
  at each witness, and a fault injected at an early box of the linear certificate at
  an oblique direction and at direction zero, where it runs by branch and bound.

Prints one line per check and `SQVERIFY-FAST CHECKS PASSED` when every check passes;
exits 1 otherwise. From `packing/`, after `cargo build --release` in
`sqverify_fast/`::

    .venv/bin/python3 -m devtools.check_sqverify_fast \\
        --binary sqverify_fast/target/release/sqverify-fast
"""

from __future__ import annotations

import argparse
import gzip
import json
import random
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from sqpack.rectangle_density import (
    DensityRectangle,
    coverage_at_point,
    exact_intersection_area,
    load_candidate,
    square_polygon,
)

PROJECT = Path(__file__).resolve().parents[1]
WEB = PROJECT / "resources/web"
STEP = Fraction(83, 40000)
# The retained stage-4 controls of formats M and L: packet and receipt folder.
MIXED_CONTROLS = (
    ("wand125-point-and-mixed-2026-10-01", "n37"),
    ("wand125-linear-certificates-2026-10-02", "n101"),
)


def candidate_path(packet: str, certificate: str) -> Path:
    return (
        WEB
        / f"wand125-rectangle-certificates-{packet}"
        / "wand125-rectangles/certificates"
        / certificate
        / "certified_candidate.json.gz"
    )


def direction(index: int) -> tuple[Fraction, Fraction]:
    t = index * STEP
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def read_raw(path: Path) -> dict[str, Any]:
    """Read a candidate keeping every decimal token as its exact text."""
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        value: dict[str, Any] = json.load(stream, parse_float=str)
    return value


def run_binary(
    binary: Path, candidate: Path, n: int, *extra: str
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(binary), "--candidate", str(candidate), "--n", str(n), *extra],
        capture_output=True,
        text=True,
        check=False,
        timeout=3600,
    )


def probe(binary: Path, candidate: Path, n: int, spec: str) -> dict[str, Any]:
    result = run_binary(binary, candidate, n, "--probe", spec)
    if result.returncode != 0:
        raise SystemExit(f"probe {spec} failed: {result.stderr}")
    value: dict[str, Any] = json.loads(result.stdout)
    return value


def differential(binary: Path, rng: random.Random, *, quick: bool) -> list[tuple[bool, str]]:
    outcomes: list[tuple[bool, str]] = []
    certificates = [("2026-09-27", "rect_n32_L595", 32)]
    if not quick:
        certificates.append(("2026-09-27", "rect_n78_L8955", 78))
    for packet, certificate, n in certificates:
        path = candidate_path(packet, certificate)
        exact_candidate = load_candidate(path, n=n)
        side = float(exact_candidate.side)
        for index in (1, 200) if quick else (1, 57, 133, 200):
            cosine, sine = direction(index)
            extent = float(exact_candidate.core_side * (cosine + sine) / 2)
            worst_gap = 0.0
            ok = True
            for _ in range(2 if quick else 4):
                x = side / 2 + rng.random() * (side / 2 - extent)
                y = side / 2 + rng.random() * (side / 2 - extent)
                half = 10.0 ** rng.uniform(-6, -3)
                reading = probe(binary, path, n, f"{index},{x!r},{y!r},{half!r},{half!r}")
                exact = Fraction(reading["exact_coverage"])
                centre = Fraction(reading["centre_lower_bound"])
                gap = float(exact - centre)
                worst_gap = max(worst_gap, gap)
                if centre > exact or gap > 1e-9:
                    ok = False
                box = Fraction(reading["box_lower_bound"])
                for px, py in (
                    (x - half, y - half),
                    (x + half, y + half),
                    (x - half, y + half),
                ):
                    value = coverage_at_point(
                        exact_candidate, Fraction(px), Fraction(py), cosine, sine
                    )
                    if box > value:
                        ok = False
            outcomes.append(
                (
                    ok,
                    (
                        f"differential {certificate} r={index}: centre bound below exact, "
                        f"worst gap {worst_gap:.2e}; box bound below exact at box points"
                    ),
                )
            )
    return outcomes


def orbit_images(side: Fraction, row: list[Fraction]) -> list[tuple[Fraction, ...]]:
    x1, y1, x2, y2 = row
    images: list[tuple[Fraction, ...]] = []
    for a1, b1, a2, b2 in ((x1, y1, x2, y2), (y1, x1, y2, x2)):
        for l1, l2 in ((a1, a2), (side - a2, side - a1)):
            for m1, m2 in ((b1, b2), (side - b2, side - b1)):
                images.append((l1, m1, l2, m2))
    return images


def top_orbit(
    raw: dict[str, Any], x: Fraction, y: Fraction, index: int
) -> tuple[int, Fraction]:
    """The positive orbit capturing the most mass at a centre, exactly."""
    side = Fraction(raw["L"])
    core = Fraction(raw["B"])
    cosine, sine = direction(index)
    polygon = square_polygon(x, y, cosine, sine, core)
    best = (-1, Fraction(0))
    for row_index, (row, weight) in enumerate(
        zip(raw["rectangles"], raw["weights"], strict=True)
    ):
        w = Fraction(weight)
        if w == 0:
            continue
        coordinates = [Fraction(v) for v in row]
        area = (coordinates[2] - coordinates[0]) * (coordinates[3] - coordinates[1])
        density = w / (8 * area)
        total = Fraction(0)
        for image in orbit_images(side, coordinates):
            if abs(float(image[0] + image[2]) / 2 - float(x)) > 1.5:
                continue
            if abs(float(image[1] + image[3]) / 2 - float(y)) > 1.5:
                continue
            total += density * exact_intersection_area(
                DensityRectangle(image[0], image[1], image[2], image[3], density), polygon
            )
        if total > best[1]:
            best = (row_index, total)
    return best


def write(raw: dict[str, Any], directory: Path, name: str) -> Path:
    path = directory / f"{name}.json"
    path.write_text(json.dumps(raw), encoding="utf-8")
    return path


def scaled(raw: dict[str, Any], factor: Fraction) -> dict[str, Any]:
    copy = json.loads(json.dumps(raw))
    copy["weights"] = [str(Fraction(w) * factor) for w in raw["weights"]]
    copy.pop("certificate", None)
    return copy


def refused_at(
    binary: Path, path: Path, n: int, index: int, threshold: str
) -> tuple[bool, str]:
    result = run_binary(
        binary, path, n, "--directions", str(index), "--threshold", threshold, "--confirm"
    )
    rows = [json.loads(line) for line in result.stdout.splitlines() if line.startswith("{")]
    row = next((r for r in rows if r.get("r") == index), {})
    return (
        result.returncode == 1 and row.get("verdict") != "verified",
        str(row.get("verdict")),
    )


def controls(binary: Path, scratch: Path, *, quick: bool) -> list[tuple[bool, str]]:
    outcomes: list[tuple[bool, str]] = []
    # The retained stage-4 controls, rebuilt from their recorded mutations.
    receipt = json.loads(
        (
            WEB
            / "wand125-rectangle-certificates-2026-10-01/receipts/controls/rect_n41_L676.json"
        ).read_text(encoding="utf-8")
    )
    path = candidate_path("2026-10-01", receipt["certificate"])
    raw = read_raw(path)
    n = int(receipt["n"])
    index = int(receipt["direction"])
    original = run_binary(binary, path, n, "--directions", str(index), "--threshold", "1")
    outcomes.append(
        (
            original.returncode == 0,
            f"control original {receipt['certificate']} r={index} verified",
        )
    )
    for run in receipt["runs"]:
        mutation = run.get("mutation")
        if not mutation:
            continue
        if "factor" in mutation:
            mutated = scaled(raw, Fraction(mutation["factor"]))
        else:
            mutated = json.loads(json.dumps(raw))
            mutated["weights"][int(mutation["row"])] = "0"
            mutated.pop("certificate", None)
        mutant = write(mutated, scratch, f"n41-{run['name']}")
        ok, verdict = refused_at(binary, mutant, n, index, "1")
        outcomes.append(
            (
                ok,
                f"control {run['name']} {receipt['certificate']} r={index} refused ({verdict})",
            )
        )
    # Own controls on the same witness: one part in a million below the threshold.
    witness_x = Fraction(receipt["witness"]["centre"][0])
    witness_y = Fraction(receipt["witness"]["centre"][1])
    coverage = Fraction(receipt["witness"]["coverage_exact"])
    factor = (1 - Fraction(1, 10**6)) / coverage
    mutant = write(scaled(raw, factor), scratch, "n41-near-threshold")
    ok, verdict = refused_at(binary, mutant, n, index, "1")
    outcomes.append(
        (ok, f"control near-threshold (1 - 1e-6 at the witness) r={index} refused ({verdict})")
    )
    # Own control: drop the orbit contributing most at the witness.
    row, contribution = top_orbit(raw, witness_x, witness_y, index)
    if coverage - contribution < 1:
        mutated = json.loads(json.dumps(raw))
        mutated["weights"][row] = "0"
        mutated.pop("certificate", None)
        mutant = write(mutated, scratch, "n41-drop-own-top")
        ok, verdict = refused_at(binary, mutant, n, index, "1")
        outcomes.append(
            (ok, f"control drop-own-top-orbit row {row} r={index} refused ({verdict})")
        )
    # Own controls on n32 at the least-bound box of two directions.
    path32 = candidate_path("2026-09-27", "rect_n32_L595")
    raw32 = read_raw(path32)
    for index32 in (1,) if quick else (1, 100):
        result = run_binary(
            binary, path32, 32, "--directions", str(index32), "--threshold", "1"
        )
        rows = [json.loads(line) for line in result.stdout.splitlines() if line.startswith("{")]
        row32 = next(r for r in rows if r.get("r") == index32)
        box = row32["least_bound_box"]
        cx, cy = Fraction(box["x"]), Fraction(box["y"])
        candidate32 = load_candidate(path32, n=32)
        cosine, sine = direction(index32)
        value = coverage_at_point(candidate32, cx, cy, cosine, sine)
        mutant = write(
            scaled(raw32, (1 - Fraction(1, 10**6)) / value), scratch, f"n32-near-{index32}"
        )
        ok, verdict = refused_at(binary, mutant, 32, index32, "1")
        outcomes.append(
            (
                ok,
                f"control n32 near-threshold at least box r={index32} refused ({verdict})",
            )
        )
        top, contribution = top_orbit(raw32, cx, cy, index32)
        if value - contribution < 1:
            mutated = json.loads(json.dumps(raw32))
            mutated["weights"][top] = "0"
            mutated.pop("certificate", None)
            mutant = write(mutated, scratch, f"n32-drop-{index32}")
            ok, verdict = refused_at(binary, mutant, 32, index32, "1")
            outcomes.append(
                (
                    ok,
                    f"control n32 drop-top at least box r={index32} refused ({verdict})",
                )
            )
    # Fault injection (spec 4.2): one boundary rectangle classified inside at one box.
    # The audit must refuse: every box with --audit-every 1, and with the default
    # sampling when the fault is high in the tree, where its subtree is audited.
    for node, audit in ((2, "1"), (2, "1024"), (1000, "1")) if not quick else ((2, "1"),):
        result = run_binary(
            binary,
            path32,
            32,
            "--directions",
            "1",
            "--audit-every",
            audit,
            "--inject-fault-at-node",
            str(node),
        )
        rows = [json.loads(line) for line in result.stdout.splitlines() if line.startswith("{")]
        row = next((r for r in rows if r.get("r") == 1), {})
        ok = result.returncode == 1 and row.get("verdict") == "audit-failed"
        outcomes.append(
            (ok, f"fault at box {node}, audit every {audit}: refused ({row.get('verdict')})")
        )
    # Admission refusals.
    mass = sum((Fraction(w) for w in raw32["weights"]), Fraction(0))
    malformed: list[tuple[str, dict[str, Any] | str]] = [
        ("mass-at-n", scaled(raw32, Fraction(32) / mass)),
        ("negative-weight", {**raw32, "weights": ["-1", *raw32["weights"][1:]]}),
        ("count-mismatch", {**raw32, "n": 33}),
        (
            "outside-container",
            {
                **raw32,
                "rectangles": [["-0.5", "1", "1", "2"], *raw32["rectangles"][1:]],
                "weights": ["1/100", *raw32["weights"][1:]],
            },
        ),
        (
            "degenerate-rectangle",
            {
                **raw32,
                "rectangles": [["2", "1", "1", "2"], *raw32["rectangles"][1:]],
                "weights": ["1/100", *raw32["weights"][1:]],
            },
        ),
        ("duplicate-key", json.dumps(raw32)[:-1] + ', "L": "1000"}'),
    ]
    for name, body in malformed:
        target = scratch / f"n32-{name}.json"
        target.write_text(body if isinstance(body, str) else json.dumps(body), encoding="utf-8")
        result = run_binary(binary, target, 32, "--directions", "1")
        outcomes.append(
            (result.returncode == 2, f"admission refuses {name} (exit {result.returncode})")
        )
    return outcomes


def mixed_rows(raw: dict[str, Any]) -> list[tuple[str, list[Fraction], Fraction]]:
    """A format M or L candidate's rows as (kind, geometry, mass), exactly."""
    if raw.get("schema") == "point_line_rectangle_v1":
        return [
            (str(row["kind"]), [Fraction(v) for v in row["geometry"]], Fraction(row["mass"]))
            for row in raw["primitives"]
        ]
    return [
        ("rectangle", [Fraction(v) for v in row["rectangle"]], Fraction(row["mass"]))
        for row in raw["rectangles"]
    ]


def d4_points(side: Fraction, x: Fraction, y: Fraction) -> list[tuple[Fraction, Fraction]]:
    """The eight images of a point, in a fixed order of the group's elements."""
    return [
        (first, second)
        for a, b in ((x, y), (y, x))
        for first in (a, side - a)
        for second in (b, side - b)
    ]


def mixed_exact(raw: dict[str, Any], x: Fraction, y: Fraction, index: int) -> Fraction:
    """Exact capture of a format M or L measure by the closed core at one centre.

    Written from spec 1.2 apart from the crate's oracle: every row is an orbit
    representative whose eight images carry an eighth of its mass; a point counts when
    it lies in the closed square, a segment by the parametric length of its closed
    intersection, a rectangle by area.
    """
    side, core = Fraction(raw["L"]), Fraction(raw["B"])
    half = core / 2
    cosine, sine = direction(index)
    polygon = square_polygon(x, y, cosine, sine, core)

    def local(point: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
        dx, dy = point[0] - x, point[1] - y
        return cosine * dx + sine * dy, cosine * dy - sine * dx

    total = Fraction(0)
    for kind, geometry, mass in mixed_rows(raw):
        if mass == 0:
            continue
        share = mass / 8
        if kind == "rectangle":
            area = (geometry[2] - geometry[0]) * (geometry[3] - geometry[1])
            for image in orbit_images(side, geometry):
                # The core lies within B / sqrt(2) < 0.71 of its centre on each axis.
                if not (
                    float(image[0]) < float(x) + 0.71
                    and float(image[2]) > float(x) - 0.71
                    and float(image[1]) < float(y) + 0.71
                    and float(image[3]) > float(y) - 0.71
                ):
                    continue
                corners = (image[0], image[1], image[2], image[3])
                total += share / area * exact_intersection_area(corners, polygon)
        elif kind == "point":
            for point in d4_points(side, geometry[0], geometry[1]):
                u, v = local(point)
                if abs(u) <= half and abs(v) <= half:
                    total += share
        else:
            starts = d4_points(side, geometry[0], geometry[1])
            ends = d4_points(side, geometry[2], geometry[3])
            for start, end in zip(starts, ends, strict=True):
                low, high = Fraction(0), Fraction(1)
                for a, b in zip(local(start), local(end), strict=True):
                    slope = b - a
                    if slope == 0:
                        if abs(a) > half:
                            high = Fraction(-1)
                        continue
                    t1, t2 = (-half - a) / slope, (half - a) / slope
                    low, high = max(low, min(t1, t2)), min(high, max(t1, t2))
                if high > low:
                    total += share * (high - low)
    return total


def axis_minimum_dense(raw: dict[str, Any], upper: Fraction) -> float:
    """The least capture over every axis-grid vertex of a rectangle measure, in floats.

    A dense cross-check of the vertex sweep (lemma A1) on `[L/2, upper]^2`: every
    breakpoint `edge +- B/2` in range and both ends, the capture at each vertex as
    one matrix product of the per-rectangle interval overlaps.
    """
    side, core = Fraction(raw["L"]), Fraction(raw["B"])
    half = core / 2
    lower = side / 2
    images: list[tuple[Fraction, ...]] = []
    densities: list[Fraction] = []
    for _kind, geometry, mass in mixed_rows(raw):
        if mass == 0:
            continue
        area = (geometry[2] - geometry[0]) * (geometry[3] - geometry[1])
        for image in orbit_images(side, geometry):
            images.append(image)
            densities.append(mass / 8 / area)
    events = {lower, upper}
    for image in images:
        for edge in image:
            for event in (edge - half, edge + half):
                if lower <= event <= upper:
                    events.add(event)
    grid = np.array([float(event) for event in sorted(events)])
    corners = np.array([[float(v) for v in image] for image in images])
    rho = np.array([float(d) for d in densities])
    h = float(half)

    def overlap(low: np.ndarray, high: np.ndarray) -> np.ndarray:
        return np.clip(
            np.minimum(grid[:, None] + h, high) - np.maximum(grid[:, None] - h, low), 0, None
        )

    capture = (overlap(corners[:, 0], corners[:, 2]) * rho) @ overlap(
        corners[:, 1], corners[:, 3]
    ).T
    return float(capture.min())


def mixed_candidate(packet: str, receipt: dict[str, Any]) -> Path:
    return WEB / packet / "square-packing-bounds" / receipt["directory"] / "candidate.json.gz"


def mixed_mutant(
    raw: dict[str, Any], *, factor: Fraction = Fraction(1), drop: int = -1
) -> dict[str, Any]:
    """A copy with every mass scaled, or one row dropped, and `total_mass` recomputed."""
    copy = json.loads(json.dumps(raw))
    key, field = (
        ("primitives", "mass")
        if raw.get("schema") == "point_line_rectangle_v1"
        else ("rectangles", "mass")
    )
    if drop >= 0:
        copy[key].pop(drop)
    for row in copy[key]:
        row[field] = str(Fraction(row[field]) * factor)
    copy["total_mass"] = str(sum((Fraction(row[field]) for row in copy[key]), Fraction(0)))
    return copy


def mixed_refused(binary: Path, path: Path, n: int, index: int) -> tuple[bool, str]:
    """Refused at the declared threshold, with the stopping centre's exact capture."""
    result = run_binary(binary, path, n, "--directions", str(index), "--confirm")
    rows = [json.loads(line) for line in result.stdout.splitlines() if line.startswith("{")]
    row = next((r for r in rows if r.get("r") == index), {})
    witness = row.get("witness") or {}
    below = witness.get("exact_below_threshold")
    return (
        result.returncode == 1 and row.get("verdict") != "verified",
        f"{row.get('verdict')}, exact capture below 1 at the stop: {below}",
    )


def mixed(
    binary: Path, scratch: Path, rng: random.Random, *, quick: bool
) -> list[tuple[bool, str]]:
    outcomes: list[tuple[bool, str]] = []
    for packet, folder in MIXED_CONTROLS[1:] if quick else MIXED_CONTROLS:
        receipt = json.loads(
            (WEB / packet / "receipts" / folder / "control.json").read_text(encoding="utf-8")
        )
        path = mixed_candidate(packet, receipt)
        raw = read_raw(path)
        n = int(receipt["n"])
        index = int(receipt["index"])
        name = receipt["directory"].rsplit("/", 1)[-1]
        side, core = Fraction(raw["L"]), Fraction(raw["B"])
        # Differential: certified centre and box bounds against the exact capture.
        for r in (0, index) if quick else (0, 1, index, 200):
            cosine, sine = direction(r)
            extent = float(core * (cosine + sine) / 2)
            ok = True
            worst = 0.0
            for _ in range(2 if quick else 3):
                x = float(side) / 2 + rng.random() * (float(side) / 2 - extent)
                y = float(side) / 2 + rng.random() * (float(side) / 2 - extent)
                half = 10.0 ** rng.uniform(-6, -3)
                reading = probe(binary, path, n, f"{r},{x!r},{y!r},{half!r},{half!r}")
                exact = mixed_exact(raw, Fraction(x), Fraction(y), r)
                ok &= Fraction(reading["exact_coverage"]) == exact
                centre = Fraction(reading["centre_lower_bound"])
                worst = max(worst, float(exact - centre))
                ok &= centre <= exact
                box = Fraction(reading["box_lower_bound"])
                for px, py in (
                    (x - half, y - half),
                    (x + half, y + half),
                    (x + half, y - half),
                ):
                    ok &= box <= mixed_exact(raw, Fraction(px), Fraction(py), r)
            outcomes.append(
                (
                    ok,
                    (
                        f"mixed differential {name} r={r}: the crate's oracle equals this "
                        f"tool's exact capture; centre bound below it (worst gap {worst:.1e}),"
                        " box bound below it at box corners"
                    ),
                )
            )
        if raw.get("schema") != "point_line_rectangle_v1":
            # Format M at r = 0: the sweep on the per-bin domain [L/2, L - 1/2]^2.
            # Its certified minimum sits below the dense float one by the width the
            # column sweep's interval steps accumulate, about 1e-9 on mixed_n37_L644.
            result = run_binary(binary, path, n, "--directions", "0")
            row = json.loads(result.stdout.splitlines()[0])
            dense = axis_minimum_dense(raw, side - Fraction(1, 2))
            swept = float(row["min_certified_lower_bound"])
            outcomes.append(
                (
                    swept <= dense and dense - swept < 1e-8,
                    (
                        f"axis sweep {name} on the per-bin domain: {swept!r} against a"
                        f" dense float evaluation of every vertex, {dense!r}"
                    ),
                )
            )
        original = run_binary(binary, path, n, "--directions", str(index))
        outcomes.append(
            (original.returncode == 0, f"control original {name} r={index} verified")
        )
        for run in receipt["runs"]:
            mutation = run.get("mutation")
            if not mutation:
                continue
            if "factor" in mutation:
                mutated = mixed_mutant(raw, factor=Fraction(mutation["factor"]))
            else:
                row = int(mutation["row"])
                _kind, geometry, mass = mixed_rows(raw)[row]
                recorded = mutation.get("rectangle") or mutation["primitive"]["geometry"]
                if geometry != [Fraction(v) for v in recorded] or mass != Fraction(
                    mutation.get("mass") or mutation["primitive"]["mass"]
                ):
                    outcomes.append((False, f"control {run['name']} {name}: row {row} differs"))
                    continue
                mutated = mixed_mutant(raw, drop=row)
            mutant = write(mutated, scratch, f"{name}-{run['name']}")
            ok, verdict = mixed_refused(binary, mutant, n, index)
            outcomes.append((ok, f"control {run['name']} {name} r={index} refused ({verdict})"))
        # The near-threshold control costs the full check's exact centre
        # evaluations; the gate's quick run keeps the retained controls only.
        if not quick:
            coverage = Fraction(receipt["witness"]["coverage_exact"])
            witness = [Fraction(v) for v in receipt["witness"]["centre"]]
            if mixed_exact(raw, witness[0], witness[1], index) != coverage:
                outcomes.append(
                    (False, f"{name}: this tool's exact capture differs at the witness")
                )
            mutant = write(
                mixed_mutant(raw, factor=(1 - Fraction(1, 10**6)) / coverage),
                scratch,
                f"{name}-near",
            )
            ok, verdict = mixed_refused(binary, mutant, n, index)
            outcomes.append(
                (
                    ok,
                    (
                        f"control near-threshold (1 - 1e-6 at the witness) {name} r={index}"
                        f" refused ({verdict})"
                    ),
                )
            )
        if raw.get("schema") == "point_line_rectangle_v1":
            for r, node in ((index, 2), (0, 2)) if not quick else ((index, 2),):
                result = run_binary(
                    binary,
                    path,
                    n,
                    "--directions",
                    str(r),
                    "--audit-every",
                    "1",
                    "--inject-fault-at-node",
                    str(node),
                )
                rows = [
                    json.loads(line)
                    for line in result.stdout.splitlines()
                    if line.startswith("{")
                ]
                row = next((x for x in rows if x.get("r") == r), {})
                ok = result.returncode == 1 and row.get("verdict") == "audit-failed"
                outcomes.append(
                    (
                        ok,
                        (
                            f"fault at box {node} of {name} r={r}, audit every 1: refused"
                            f" ({row.get('verdict')})"
                        ),
                    )
                )
    return outcomes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--only", choices=("differential", "controls", "mixed"))
    parser.add_argument(
        "--quick",
        action="store_true",
        help="the gate subset: n32 only, two directions, one n32 control direction",
    )
    parser.add_argument("--seed", type=int, default=20261002)
    args = parser.parse_args(argv)
    binary = args.binary.resolve()
    outcomes: list[tuple[bool, str]] = []
    if args.only in (None, "differential"):
        outcomes += differential(binary, random.Random(args.seed), quick=args.quick)
    if args.only in (None, "controls"):
        with tempfile.TemporaryDirectory(prefix="sqverify-fast-controls-") as scratch:
            outcomes += controls(binary, Path(scratch), quick=args.quick)
    if args.only in (None, "mixed"):
        with tempfile.TemporaryDirectory(prefix="sqverify-fast-mixed-") as scratch:
            outcomes += mixed(
                binary, Path(scratch), random.Random(args.seed + 1), quick=args.quick
            )
    for ok, line in outcomes:
        print(("  ok   " if ok else "  FAIL ") + line, flush=True)
    if all(ok for ok, _ in outcomes):
        print("SQVERIFY-FAST CHECKS PASSED")
        return 0
    print("SQVERIFY-FAST CHECKS FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
