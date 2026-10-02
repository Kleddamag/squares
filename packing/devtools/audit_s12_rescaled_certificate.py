"""Exact preflight of squarepacker's rescaled s(12) certificate, and its two controls.

jlevy/squares#309 reports ``s(12) >= 31360/7901`` from Evan Daniel's 1,736-point
weighted certificate ``s12_lower_3.9686.txt`` (``T-049``) with every coordinate and the
container multiplied by ``7902/7901`` and the weights unchanged. This command decides
that description in exact rational arithmetic, from the two retained files and nothing
else:

- the reporter's file in ``squarepacker-s12-lower-bound-2026-10-02`` and Daniel's in
  ``evand-square-packing-2026-09-26`` have the reviewed SHA-256 digests;
- both are plain point certificates in Daniel's format, ``s_num s_den D W m`` and ``m``
  triples ``X Y w`` of nonnegative integers, with nothing after them;
- the container is exactly ``31360/7901``, which is ``7902/7901`` times Daniel's
  ``15680/3951``, the advance over it is ``15680/31216851``, and point ``i`` of the new
  file is point ``i`` of Daniel's with both coordinates scaled by ``7902/7901`` and the
  same weight;
- every weight is nonnegative, every point lies in the closed container, the multiset of
  weighted points is invariant under the container's symmetry group, and the total weight
  is ``119738036/10^7 < 12``; and
- the reporter's own control ``controls/scaled_further_31360_7900.txt`` is the same
  integers over ``7900``, the new file scaled again by ``7901/7900``.

It decides nothing about coverage: whether every closed unit square in the container
captures weight at least one is the checkers' question.

``--write-controls DIR`` also writes the two mutated certificates the replays must
refuse, deterministically: ``scaled-7901-7900.txt``, the new file over ``7900`` (byte
for byte the reporter's control), and ``weights-minus-57.txt``, the new file with every
weight lowered by ``57/10^7``. The least captured weight the reporter and Daniel's
verifier record is ``10000056/10^7``, attained by a pose capturing at least one point, so
that pose captures at most ``9999999/10^7`` in the second control and any correct checker
refuses it. Both keep the symmetry, so Daniel's verifier still sweeps ``[0, 45]`` degrees.

Usage, from ``packing/``::

    uv run --frozen --all-extras --group dev \\
        python -m devtools.audit_s12_rescaled_certificate \\
        --output OUT.json [--write-controls DIR]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools.retained_data import read_retained_bytes

REPO = Path(__file__).resolve().parents[2]
WEB = REPO / "packing/resources/web"
PACKET = WEB / "squarepacker-s12-lower-bound-2026-10-02"
SOURCE = PACKET / "s12-lower-bound"
CERTIFICATE = SOURCE / "s12_lower_3.969118.txt"
CERTIFICATE_SHA256 = "6ad9b0e8257166687f4e861b97f024f4993d7b2125897173b2f5e9f6e2167578"
REPORTER_CONTROL = SOURCE / "controls/scaled_further_31360_7900.txt"
REPORTER_CONTROL_SHA256 = "04d7105c5b6d8b85cd0655f544b5c59163f9a36fa86814601a30c4114d1526f1"
DANIEL = (
    WEB / "evand-square-packing-2026-09-26/square-packing/s12/certificates/s12_lower_3.9686.txt"
)
#: The digest `devtools.verify_evand_angle_net_native` pins for the same file (T-049).
DANIEL_SHA256 = "75f1cc891a8b8739b92b50c7ddbd85a493efa58cf2e921d58ce4ac7c2dcabe78"

N = 12
SIDE = Fraction(31360, 7901)
DANIEL_SIDE = Fraction(15680, 3951)
FACTOR = Fraction(7902, 7901)
TOTAL = 119738036
#: The least captured weight both reported checkers print at N = 24000, over W.
REPORTED_MINIMUM = 10000056
WEIGHT_STEP = REPORTED_MINIMUM - 10_000_000 + 1
CONTROLS = ("scaled-7901-7900", "weights-minus-57")


@dataclass(frozen=True, slots=True)
class PointCertificate:
    """A plain certificate in Daniel's text format, as integers."""

    s_num: int
    s_den: int
    denominator: int
    weight_scale: int
    points: tuple[tuple[int, int, int], ...]

    @property
    def side(self) -> Fraction:
        return Fraction(self.s_num, self.s_den)

    def render(self) -> bytes:
        """The text the reporter's files use: a header of four lines, one point a line."""
        lines = [
            f"{self.s_num} {self.s_den}",
            str(self.denominator),
            str(self.weight_scale),
            str(len(self.points)),
            *(f"{x} {y} {w}" for x, y, w in self.points),
        ]
        return ("\n".join(lines) + "\n").encode()


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse(data: bytes) -> PointCertificate:
    """Daniel's ``s_num s_den D W m (X Y w)^m``, refusing anything else."""
    tokens = data.split()
    _require(all(t.isdigit() for t in tokens), "the format holds nonnegative integers only")
    values = [int(t) for t in tokens]
    _require(len(values) >= 5, "truncated header")
    s_num, s_den, denominator, weight_scale, count = values[:5]
    _require(min(s_num, s_den, denominator, weight_scale) > 0, "nonpositive header")
    _require(len(values) == 5 + 3 * count, "point count does not match the file")
    points = tuple(
        (values[5 + 3 * i], values[6 + 3 * i], values[7 + 3 * i]) for i in range(count)
    )
    return PointCertificate(s_num, s_den, denominator, weight_scale, points)


def read(path: Path, expected: str) -> tuple[bytes, PointCertificate]:
    data = read_retained_bytes(path)
    _require(sha256(data) == expected, f"{path.name} differs from the reviewed bytes")
    return data, parse(data)


def weighted_points(cert: PointCertificate) -> Counter[tuple[Fraction, Fraction, int]]:
    d = cert.denominator
    return Counter((Fraction(x, d), Fraction(y, d), w) for x, y, w in cert.points if w)


def d4_invariant(cert: PointCertificate) -> bool:
    """Is the multiset of weighted points fixed by the container's symmetries?"""
    side = cert.side
    points = weighted_points(cert)
    maps = (
        lambda x, y: (side - x, y),
        lambda x, y: (x, side - y),
        lambda x, y: (y, x),
    )
    return all(
        Counter({(*f(x, y), w): k for (x, y, w), k in points.items()}) == points for f in maps
    )


def scaled(a: PointCertificate, b: PointCertificate, factor: Fraction) -> bool:
    """Is ``b`` exactly ``a`` with every coordinate and the side times ``factor``?"""
    if b.side != factor * a.side or len(a.points) != len(b.points):
        return False
    return all(
        Fraction(xb, b.denominator) == factor * Fraction(xa, a.denominator)
        and Fraction(yb, b.denominator) == factor * Fraction(ya, a.denominator)
        and wb == wa
        for (xa, ya, wa), (xb, yb, wb) in zip(a.points, b.points, strict=True)
    )


def controls(cert: PointCertificate) -> dict[str, PointCertificate]:
    """The two mutations the replays must refuse."""
    _require(cert.denominator == 7901, "the controls are defined on the reported file")
    _require(min(w for _, _, w in cert.points) > WEIGHT_STEP, "a weight would go negative")
    return {
        "scaled-7901-7900": PointCertificate(
            cert.s_num, 7900, 7900, cert.weight_scale, cert.points
        ),
        "weights-minus-57": PointCertificate(
            cert.s_num,
            cert.s_den,
            cert.denominator,
            cert.weight_scale,
            tuple((x, y, w - WEIGHT_STEP) for x, y, w in cert.points),
        ),
    }


def audit() -> dict[str, Any]:
    """Every exact check of the module docstring, as named booleans and values."""
    new_bytes, new = read(CERTIFICATE, CERTIFICATE_SHA256)
    old_bytes, old = read(DANIEL, DANIEL_SHA256)
    control_bytes, reporter_control = read(REPORTER_CONTROL, REPORTER_CONTROL_SHA256)
    side = new.side
    total = sum(w for _, _, w in new.points)
    weights = [w for _, _, w in new.points]
    in_container = all(
        Fraction(x, new.denominator) <= side and Fraction(y, new.denominator) <= side
        for x, y, _ in new.points
    )
    mutated = controls(new)
    checks = {
        "certificate_digest": sha256(new_bytes) == CERTIFICATE_SHA256,
        "daniel_digest": sha256(old_bytes) == DANIEL_SHA256,
        "container_is_31360_over_7901": side == SIDE,
        "daniel_container_is_15680_over_3951": old.side == DANIEL_SIDE,
        "same_point_count": len(new.points) == len(old.points) == 1736,
        "same_weight_scale": new.weight_scale == old.weight_scale == 10**7,
        "pointwise_daniel_times_7902_over_7901": scaled(old, new, FACTOR),
        "integers_are_twice_daniels": all(
            (xb, yb, wb) == (2 * xa, 2 * ya, wa)
            for (xa, ya, wa), (xb, yb, wb) in zip(old.points, new.points, strict=True)
        ),
        "weights_nonnegative": min(weights) >= 0,
        "points_in_container": in_container,
        "d4_invariant": d4_invariant(new),
        "total_below_n": total < N * new.weight_scale,
        "total_equals_daniels": total == sum(w for _, _, w in old.points) == TOTAL,
        "reporter_control_is_new_times_7901_over_7900": scaled(
            new, reporter_control, Fraction(7901, 7900)
        ),
        "first_control_is_the_reporters": mutated["scaled-7901-7900"].render() == control_bytes,
        "rendering_is_byte_exact": new.render() == new_bytes,
    }
    return {
        "schema": "S12RescaledPreflight/v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "issue": "https://github.com/jlevy/squares/issues/309",
        "certificate": str(CERTIFICATE.relative_to(REPO)),
        "certificate_sha256": CERTIFICATE_SHA256,
        "daniel_certificate": str(DANIEL.relative_to(REPO)),
        "daniel_sha256": DANIEL_SHA256,
        "checks": checks,
        "side": str(side),
        "daniel_side": str(old.side),
        "factor": str(side / old.side),
        "advance": str(side - old.side),
        "points": len(new.points),
        "zero_weight_points": sum(1 for w in weights if w == 0),
        "least_weight": f"{min(weights)}/{new.weight_scale}",
        "total_weight": f"{total}/{new.weight_scale}",
        "counting_gap": str(N - Fraction(total, new.weight_scale)),
        "controls": {
            name: {
                "sha256": sha256(cert.render()),
                "side": str(cert.side),
                "total_weight": f"{sum(w for _, _, w in cert.points)}/{cert.weight_scale}",
                "d4_invariant": d4_invariant(cert),
            }
            for name, cert in mutated.items()
        },
        "weight_step": f"{WEIGHT_STEP}/{new.weight_scale}",
    }


def write_controls(directory: Path) -> dict[str, Path]:
    _, new = read(CERTIFICATE, CERTIFICATE_SHA256)
    directory.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}
    for name, cert in controls(new).items():
        path = directory / f"{name}.txt"
        path.write_bytes(cert.render())
        written[name] = path
    return written


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--output", type=Path, help="write the receipt here as JSON")
    parser.add_argument("--write-controls", type=Path, help="write the two controls here")
    args = parser.parse_args(argv)
    result = audit()
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with atomic_output_file(args.output) as handle:
            handle.write_text(text)
    if args.write_controls:
        for name, path in write_controls(args.write_controls).items():
            print(f"{name}: {path} sha256 {sha256(path.read_bytes())}")
    failed = [name for name, ok in result["checks"].items() if not ok]
    total = len(result["checks"])
    print(f"{result['status']}: {total - len(failed)} of {total} checks")
    for name in failed:
        print(f"  failed: {name}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
