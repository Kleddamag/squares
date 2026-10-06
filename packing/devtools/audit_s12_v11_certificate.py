"""Exact preflight of squarepacker's v1.1 s(12) certificate, and its two controls.

jlevy/squares#363 reports ``s(12) >= 7943/2000 = 3.9715`` from ``s12_lower_3.9715.txt``
of squarepacker/s12-lower-bound v1.1: Evan Daniel's 1,736 points of
``s12_lower_3.9686.txt`` (``T-049``) dilated by ``(7943/2000)/(15680/3951)`` and rounded
to the grid ``1/4000000`` one D4 orbit at a time, with new weights found by linear
programming. This command decides that description in exact rational arithmetic, from
the retained files and nothing else:

- the reporter's file in ``squarepacker-s12-lower-bound-2026-10-05`` and Daniel's in
  ``evand-square-packing-2026-09-26`` have the reviewed SHA-256 digests, and the
  reporter's bytes are the canonical rendering of their integers;
- the container is exactly ``7943/2000`` over ``D = 4000000`` and ``W = 10^7``, the
  dilation is ``31382793/31360000``, and the advance over ``T-079``'s
  ``15680000/3949423`` is ``10266889/7898846000``;
- the points are Daniel's points dilated, matched one to one, every coordinate within
  ``11/39200000`` of its exact image, as the source states (the file lists them in
  another order, so the match is found here, not read from the line numbers);
- every weight is positive, every point lies in the closed container, the points are
  distinct, the weighted multiset is invariant under the container's symmetry group, it
  has 223 orbits, and the total weight is ``119974808/10^7 < 12``;
- the points in the closed corner square ``[0, 1]^2`` are 58 and weigh ``10000050/10^7``,
  the least captured weight both reported checkers print at ``N = 96000``; and
- the reporter's two controls are rebuilt here from their descriptions, byte for byte:
  the heaviest orbit lowered by ``100/10^7``, and the same integers over ``3999600``.

It also records, as facts and not as checks, the quantities behind the source's account
of why these points stop near ``3.9715``: the rows of points nearest ``x = 1`` and
``x = 2``, and the side ``(560/141) sigma_0`` past which the test square of bin 0 fits
between the wall and the first row, with ``sigma_0`` exact and as Daniel's verifier rounds
it.

It decides nothing about coverage: whether every closed unit square in the container
captures weight at least one is the checkers' question.

Usage, from ``packing/``::

    uv run --frozen --all-extras --group dev python -m devtools.audit_s12_v11_certificate \\
        --output OUT.json [--write-controls DIR]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools.audit_s12_rescaled_certificate import (
    DANIEL,
    DANIEL_SHA256,
    DANIEL_SIDE,
    PointCertificate,
    d4_invariant,
    read,
    sha256,
)

REPO = Path(__file__).resolve().parents[2]
WEB = REPO / "packing/resources/web"
PACKET = WEB / "squarepacker-s12-lower-bound-2026-10-05"
SOURCE = PACKET / "s12-lower-bound"
CERTIFICATE = SOURCE / "s12_lower_3.9715.txt"
CERTIFICATE_SHA256 = "e2f326b28142cf22402f88357f4c7fe4680a08a32ae785b493adac335bcc2685"
REPORTER_CONTROLS = {
    "lowered-orbit": (
        SOURCE / "controls/3.9715/control1_lowered_orbit.txt",
        "1c42bbb4cf21ee75d9e13e3947cde199559f5207f71662394ed66eecfd05aad9",
    ),
    "regrid-3999600": (
        SOURCE / "controls/3.9715/control2_scaled_further.txt",
        "f1796e271c6b877692ee06520153636cb7386e331724a720e966ec49c42b8560",
    ),
}
CONTROLS = tuple(REPORTER_CONTROLS)

N = 12
SIDE = Fraction(7943, 2000)
#: T-079, the verified bound this certificate would supersede.
ROUTE_B_SIDE = Fraction(15680000, 3949423)
DENOMINATOR = 4_000_000
WEIGHT_SCALE = 10_000_000
POINTS = 1736
ORBITS = 223
TOTAL = 119974808
#: The source's bound on every coordinate's distance from its exact dilated image.
ROUNDING = Fraction(11, 39200000)
#: The least captured weight both reported checkers print at N = 96000, over W.
REPORTED_MINIMUM = 10000050
CORNER_POINTS = 58
#: Control 1 lowers each point of the heaviest orbit by this many units of 10^-7.
ORBIT_STEP = 100
REGRID = 3_999_600
NET = 96_000
#: Daniel's verifier rounds sigma_k down to this grid (`verify/src/main.rs`).
SIGMA_SCALE = 1_000_000


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def side_units(cert: PointCertificate) -> int:
    """The container side in coordinate units, an integer for a well-formed file."""
    units = Fraction(cert.s_num * cert.denominator, cert.s_den)
    _require(units.denominator == 1, "the container is off the coordinate grid")
    return units.numerator


def orbit_key(x: int, y: int, units: int) -> tuple[int, int]:
    """The least of the eight images of ``(x, y)`` under the container's symmetries."""
    images = (
        (x, y), (units - x, y), (x, units - y), (units - x, units - y),
        (y, x), (units - y, x), (y, units - x), (units - y, units - x),
    )  # fmt: skip
    return min(images)


def orbits(cert: PointCertificate) -> dict[tuple[int, int], list[int]]:
    """Point indices grouped by their D4 orbit."""
    units = side_units(cert)
    grouped: dict[tuple[int, int], list[int]] = {}
    for index, (x, y, _) in enumerate(cert.points):
        grouped.setdefault(orbit_key(x, y, units), []).append(index)
    return grouped


def heaviest_orbit(cert: PointCertificate) -> list[int]:
    """The indices of the one orbit of greatest weight per point."""
    grouped = orbits(cert)
    weight = {key: cert.points[indices[0]][2] for key, indices in grouped.items()}
    top = max(weight.values())
    (key,) = [k for k, w in weight.items() if w == top]
    return grouped[key]


def controls(cert: PointCertificate) -> dict[str, PointCertificate]:
    """The reporter's two mutations, rebuilt from their descriptions."""
    _require(cert.denominator == DENOMINATOR, "the controls are defined on the reported file")
    lowered = set(heaviest_orbit(cert))
    return {
        "lowered-orbit": PointCertificate(
            cert.s_num,
            cert.s_den,
            cert.denominator,
            cert.weight_scale,
            tuple(
                (x, y, w - ORBIT_STEP if i in lowered else w)
                for i, (x, y, w) in enumerate(cert.points)
            ),
        ),
        "regrid-3999600": PointCertificate(
            cert.s_num, REGRID, REGRID, cert.weight_scale, cert.points
        ),
    }


def sigma0(net: int) -> Fraction:
    """``1/(cos d + sin d)`` for bin 0's gap ``d = 2 arctan(1/N)``, exactly."""
    return Fraction(net * net + 1, net * net - 1 + 2 * net)


def rows_near(cert: PointCertificate, target: Fraction) -> dict[str, Any]:
    """The column of points with abscissa nearest ``target``, and how many lie on it."""
    xs = {Fraction(x, cert.denominator) for x, _, _ in cert.points}
    nearest = min(xs, key=lambda x: (abs(x - target), x))
    count = sum(1 for x, _, _ in cert.points if Fraction(x, cert.denominator) == nearest)
    return {"x": str(nearest), "x_decimal": f"{float(nearest):.9f}", "points": count}


def dilation_match(
    old: PointCertificate, new: PointCertificate, factor: Fraction
) -> Fraction | None:
    """The largest coordinate error of a one-to-one match of ``new`` to ``old`` dilated.

    Each of Daniel's points is sent to the one unused reporter's point within `ROUNDING`
    of its exact image in both coordinates; ``None`` when some point has none or more than
    one, or a reporter's point is left over, so a returned value is a bijection's.
    """
    unused = {(x, y) for x, y, _ in new.points}
    _require(len(unused) == len(new.points), "repeated point")
    tolerance = ROUNDING * new.denominator
    worst = Fraction(0)
    for xa, ya, _ in old.points:
        ix = factor * Fraction(xa, old.denominator) * new.denominator
        iy = factor * Fraction(ya, old.denominator) * new.denominator
        candidates = [
            (x, y)
            for x in range(math.ceil(ix - tolerance), math.floor(ix + tolerance) + 1)
            for y in range(math.ceil(iy - tolerance), math.floor(iy + tolerance) + 1)
            if (x, y) in unused
        ]
        if len(candidates) != 1:
            return None
        (x, y) = candidates[0]
        unused.remove((x, y))
        worst = max(worst, abs(x - ix) / new.denominator, abs(y - iy) / new.denominator)
    return worst if not unused else None


def audit() -> dict[str, Any]:
    """Every exact check of the module docstring, as named booleans and values."""
    new_bytes, new = read(CERTIFICATE, CERTIFICATE_SHA256)
    old_bytes, old = read(DANIEL, DANIEL_SHA256)
    side = new.side
    factor = side / old.side
    weights = [w for _, _, w in new.points]
    total = sum(weights)
    deviation = dilation_match(old, new, factor)
    in_container = all(
        Fraction(x, new.denominator) <= side and Fraction(y, new.denominator) <= side
        for x, y, _ in new.points
    )
    corner = [
        w
        for x, y, w in new.points
        if Fraction(x, new.denominator) <= 1 and Fraction(y, new.denominator) <= 1
    ]
    grouped = orbits(new)
    heaviest = heaviest_orbit(new)
    mutated = controls(new)
    reporter = {
        name: read(path, digest)[0] for name, (path, digest) in REPORTER_CONTROLS.items()
    }
    checks = {
        "certificate_digest": sha256(new_bytes) == CERTIFICATE_SHA256,
        "daniel_digest": sha256(old_bytes) == DANIEL_SHA256,
        "rendering_is_byte_exact": new.render() == new_bytes,
        "header_is_15886000_4000000_4000000_10000000_1736": (
            new.s_num,
            new.s_den,
            new.denominator,
            new.weight_scale,
            len(new.points),
        )
        == (15886000, DENOMINATOR, DENOMINATOR, WEIGHT_SCALE, POINTS),
        "container_is_7943_over_2000": side == SIDE,
        "daniel_container_is_15680_over_3951": old.side == DANIEL_SIDE,
        "dilation_is_31382793_over_31360000": factor == Fraction(31382793, 31360000),
        "advance_over_t079_is_10266889_over_7898846000": side - ROUTE_B_SIDE
        == Fraction(10266889, 7898846000),
        "same_point_count_as_daniels": len(new.points) == len(old.points) == POINTS,
        "points_are_daniels_dilated_within_11_over_39200000": deviation is not None
        and deviation <= ROUNDING,
        "weights_positive": min(weights) > 0,
        "points_in_container": in_container,
        "points_distinct": len({(x, y) for x, y, _ in new.points}) == len(new.points),
        "d4_invariant": d4_invariant(new),
        "orbit_count_is_223": len(grouped) == ORBITS,
        "total_is_119974808": total == TOTAL,
        "total_below_n": total < N * new.weight_scale,
        "corner_square_holds_58_points_of_the_reported_minimum": (
            len(corner) == CORNER_POINTS and sum(corner) == REPORTED_MINIMUM
        ),
        "heaviest_orbit_has_8_points_2_in_the_corner": len(heaviest) == 8
        and sum(
            1
            for i in heaviest
            if Fraction(new.points[i][0], new.denominator) <= 1
            and Fraction(new.points[i][1], new.denominator) <= 1
        )
        == 2,
        **{
            f"control_{name}_is_the_reporters": mutated[name].render() == reporter[name]
            for name in CONTROLS
        },
    }
    exact_sigma = sigma0(NET)
    rounded_sigma = Fraction(int(exact_sigma * SIGMA_SCALE), SIGMA_SCALE)
    first_row = rows_near(new, Fraction(1))
    return {
        "schema": "S12V11Preflight/v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "issue": "https://github.com/jlevy/squares/issues/363",
        "certificate": str(CERTIFICATE.relative_to(REPO)),
        "certificate_sha256": CERTIFICATE_SHA256,
        "daniel_certificate": str(DANIEL.relative_to(REPO)),
        "daniel_sha256": DANIEL_SHA256,
        "checks": checks,
        "side": str(side),
        "side_decimal": f"{float(side):.10f}",
        "daniel_side": str(old.side),
        "dilation": str(factor),
        "route_b_side": str(ROUTE_B_SIDE),
        "advance_over_route_b": str(side - ROUTE_B_SIDE),
        "max_coordinate_deviation": str(deviation),
        "max_coordinate_deviation_decimal": None
        if deviation is None
        else f"{float(deviation):.3e}",
        "points": len(new.points),
        "orbits": len(grouped),
        "least_weight": f"{min(weights)}/{new.weight_scale}",
        "greatest_weight": f"{max(weights)}/{new.weight_scale}",
        "total_weight": f"{total}/{new.weight_scale}",
        "counting_gap": str(N - Fraction(total, new.weight_scale)),
        "corner_square": {"points": len(corner), "weight": f"{sum(corner)}/{new.weight_scale}"},
        "heaviest_orbit": {
            "points": [list(new.points[i]) for i in heaviest],
            "weight_each": f"{new.points[heaviest[0]][2]}/{new.weight_scale}",
        },
        "controls": {
            name: {
                "sha256": sha256(cert.render()),
                "side": str(cert.side),
                "total_weight": f"{sum(w for _, _, w in cert.points)}/{cert.weight_scale}",
                "d4_invariant": d4_invariant(cert),
            }
            for name, cert in mutated.items()
        },
        "stops_near": {
            "note": (
                "Facts behind the source's account, not checks. Daniel's rows near x = 1 "
                "and x = 2 scale with the container, so the first lies at (141/560) s; "
                "bin 0's test square of side sigma_0 fits between it and the wall once "
                "that exceeds sigma_0, at s = (560/141) sigma_0."
            ),
            "row_near_1": first_row,
            "row_near_2": rows_near(new, Fraction(2)),
            "first_row_over_side": str(Fraction(first_row["x"]) / side),
            "net": NET,
            "sigma_0_exact": str(exact_sigma),
            "sigma_0_daniel_rounded": str(rounded_sigma),
            "slip_side_exact_sigma": f"{float(Fraction(560, 141) * exact_sigma):.9f}",
            "slip_side_daniel_sigma": f"{float(Fraction(560, 141) * rounded_sigma):.9f}",
            "limit_560_over_141": f"{float(Fraction(560, 141)):.9f}",
        },
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
