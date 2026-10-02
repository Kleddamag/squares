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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--only", choices=("differential", "controls"))
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
    for ok, line in outcomes:
        print(("  ok   " if ok else "  FAIL ") + line, flush=True)
    if all(ok for ok, _ in outcomes):
        print("SQVERIFY-FAST CHECKS PASSED")
        return 0
    print("SQVERIFY-FAST CHECKS FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
