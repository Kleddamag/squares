#!/usr/bin/env python3
"""Decide the September 2026 upper-bound packings again, by interval arithmetic on each pose.

`devtools.upper_bound_packets` certifies T-056 (Francisco Couzo's 49 packings) and T-057
(Joost de Winter's ``n = 211``) by rounding each source pose to an exact rational packing
and deciding that packing over ``Q``. This module is the method-distinct second route. It
decides the pose exactly as the source prints it: decimal centres, decimal angles in their
declared unit, and the true cosine and sine of each angle, which are transcendental and are
never replaced by rationals. Every quantity is enclosed, and every decision is read off the
enclosure's sign.

The arithmetic is decimal fixed-point intervals. A quantity is a pair of integers
``[lo, hi]`` standing for ``[lo / 10^D, hi / 10^D]``; sums and differences are exact, and a
product rounds its lower end down and its upper end up by integer floor division. A printed
decimal of at most ``D`` places is a point interval, so every centre is exact. Cosine and
sine are their Taylor polynomials summed with directed rounding, widened by the Lagrange
bound ``|x|^(N+1)/(N+1)!`` on the remainder; an angle in degrees is converted with an
enclosure of ``pi`` from Machin's formula. Nothing is taken from mpmath, from ``sqpack``'s
geometry, or from either of the exact route's checkers.

What is decided, for each pose:

- **Pairs.** A pair whose centres are at least ``sqrt(2)`` apart is disjoint, since each
  square lies in the disc of radius ``sqrt(2)/2`` about its centre; that test is exact on
  the printed centres. Every other pair is decided by the separating-axis test over the
  four edge normals: on the axis of one square's edge the pair's gap is
  ``|a . (c_j - c_i)| - 1/2 - (|cos(t_j - t_i)| + |sin(t_j - t_i)|)/2``, enclosed. A pair is
  *separated* when some axis's gap has a nonnegative lower end, *overlapping* when every
  axis's gap has a negative upper end, and *undecided* otherwise.
- **The side.** Each vertex ``c +- e1/2 +- e2/2`` is enclosed, and so is the pose's own
  extent, ``max(max x - min x, max y - min y)`` over all vertices: the least side of a
  square container of this pose, the same quantity the exact route calls a certificate's
  side. The pose, translated so its least enclosed ``x`` and ``y`` are zero, has every
  vertex in ``[0, U]^2`` for ``U`` the larger of the printed side and the extent's upper
  end rounded up at the printed precision, and that ``U`` is the bound the case proves.
- **The printed frame.** Whether the pose as placed lies in ``[0, s]^2`` for the printed
  side ``s``, and its least wall clearance, for comparison with what a source reports.

Anything undecided at ``D`` digits is decided again at twice the digits, up to
`DIGITS[-1]`.

A pose is read from the packet's retained facts, which both routes read. The one checksum
here crosses the boundary those facts were made across: the upstream file, which the packet
may not retain, against the transcription of it that the packet keeps. The pose is written
back out as the upstream file prints it, and those bytes must have the SHA-256 that the
acquisition record took from the clone at the pinned revision; a digit, a sign, a row or
the angle unit transcribed wrongly would fail it. No digest of a file committed here is
taken or stored: the facts and receipts are identified by their paths, and Git holds their
bytes.

Subcommands, run from ``packing/``:

``certify [--source ID] [--n N ...] [--workers K]``
    Decide each case, write ``receipts/interval-certification.json`` beside the exact
    route's receipts, one row per case, and the negative controls to
    ``receipts/interval-negative-controls.json``.

``check [--source ID] [--n N ...] [--workers K]``
    The replay: decide every case and control again and require each receipt row to be
    what it records, wall seconds aside. About ten seconds on one worker.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from collections.abc import Callable, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, replace
from decimal import ROUND_CEILING, ROUND_FLOOR, Context, Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any, NamedTuple

from strif import atomic_output_file

from devtools import upper_bound_packets as packets
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
#: Decimal digits of the fixed-point scale, tried in turn while anything is undecided.
DIGITS = (40, 80, 160, 320, 640)
#: Extra digits the trigonometric series carry before rounding out to the working scale.
GUARD = 12
TOOL = "python -m devtools.upper_bound_intervals certify"
RECEIPT = "interval-certification.json"
CONTROLS = "interval-negative-controls.json"
#: Only the parts named here are shared with the exact route; none of them is geometry.
SHARED = (
    "the packets' retained facts, read through sqpack.yamlio",
    "upper_bound_packets.Source records and acquisition record (paths and printed sides)",
    "the exact route's receipt, read only to compare its verified value with this one",
)
VERIFIED, REFUSED, UNDECIDED = "VERIFIED", "REFUSED", "UNDECIDED"
CERTIFIED, REFUTED = "certified", "refuted"


# --------------------------------------------------------------------------------------
# Interval arithmetic at a decimal fixed-point scale
# --------------------------------------------------------------------------------------


class Iv(NamedTuple):
    """The closed interval ``[lo / scale, hi / scale]`` for the scale in use."""

    lo: int
    hi: int


def _ceil_div(numerator: int, denominator: int) -> int:
    return -(-numerator // denominator)


def enclose(value: Fraction, scale: int) -> Iv:
    """The narrowest interval at ``scale`` containing ``value``: a point where it is one."""
    scaled = value * scale
    return Iv(
        scaled.numerator // scaled.denominator, _ceil_div(scaled.numerator, scaled.denominator)
    )


def add(left: Iv, right: Iv) -> Iv:
    return Iv(left.lo + right.lo, left.hi + right.hi)


def sub(left: Iv, right: Iv) -> Iv:
    return Iv(left.lo - right.hi, left.hi - right.lo)


def neg(value: Iv) -> Iv:
    return Iv(-value.hi, -value.lo)


def mul(left: Iv, right: Iv, scale: int) -> Iv:
    """The product, its lower end rounded down and its upper end up."""
    products = (left.lo * right.lo, left.lo * right.hi, left.hi * right.lo, left.hi * right.hi)
    return Iv(min(products) // scale, _ceil_div(max(products), scale))


def scale_by(value: Iv, factor: int, scale: int) -> Iv:
    """The product with an exact scaled integer, such as a centre difference."""
    low, high = value.lo * factor, value.hi * factor
    if low > high:
        low, high = high, low
    return Iv(low // scale, _ceil_div(high, scale))


def magnitude(value: Iv) -> Iv:
    if value.lo >= 0:
        return value
    if value.hi <= 0:
        return neg(value)
    return Iv(0, max(-value.lo, value.hi))


def halve(value: Iv) -> Iv:
    return Iv(value.lo // 2, _ceil_div(value.hi, 2))


def _arctan_inverse(x: int, big: int) -> Iv:
    """``arctan(1/x)`` at scale ``big``, from its alternating series and the next term."""
    low = high = 0
    k = 0
    while True:
        divisor = (2 * k + 1) * x ** (2 * k + 1)
        term_low, term_high = big // divisor, _ceil_div(big, divisor)
        if term_high <= 1:
            # An alternating series of decreasing terms is within its next term of any
            # partial sum. The sums above already round outward; the extra unit is slack.
            return Iv(low - term_high - 1, high + term_high + 1)
        if k % 2 == 0:
            low, high = low + term_low, high + term_high
        else:
            low, high = low - term_high, high - term_low
        k += 1


def pi_enclosure(big: int) -> Iv:
    """``pi = 16 arctan(1/5) - 4 arctan(1/239)`` (Machin), enclosed at scale ``big``."""
    fifth, other = _arctan_inverse(5, big), _arctan_inverse(239, big)
    return Iv(16 * fifth.lo - 4 * other.hi, 16 * fifth.hi - 4 * other.lo)


def _series(point: Fraction, big: int) -> tuple[Iv, Iv]:
    """``cos`` and ``sin`` of a rational ``point`` at scale ``big``, remainder included.

    The Taylor polynomial of degree ``N`` of either function differs from it by at most
    ``|x|^(N+1)/(N+1)!``, since every derivative is bounded by one; the terms
    ``|x|^k/k!`` are carried as enclosures rounded outward at every step.
    """
    p, q = abs(point.numerator), point.denominator
    term = Iv(big, big)  # |x|^0 / 0!
    cosine = Iv(0, 0)
    sine = Iv(0, 0)
    k = 0
    while True:
        positive = (k // 2) % 2 == 0
        signed = term if positive else neg(term)
        if k % 2 == 0:
            cosine = add(cosine, signed)
        else:
            sine = add(sine, signed)
        k += 1
        term = Iv(term.lo * p // (q * k), _ceil_div(term.hi * p, q * k))
        if term.hi * 1000 <= 10**GUARD:
            remainder = Iv(-term.hi, term.hi)
            if point < 0:
                sine = neg(sine)
            return add(cosine, remainder), add(sine, remainder)


def cos_sin(angle: str, unit: str, scale: int) -> tuple[Iv, Iv]:
    """Enclosures of the cosine and sine of a printed angle in its declared unit."""
    big = scale * 10**GUARD
    value = Fraction(angle)
    if unit == "radians":
        point, spread = value, 0
    elif unit == "degrees":
        pi = pi_enclosure(big)
        ends = sorted((value * pi.lo / 180, value * pi.hi / 180))
        low = enclose(ends[0], 1).lo  # at scale big, the radians' lower end, rounded down
        high = enclose(ends[1], 1).hi
        point, spread = Fraction(low, big), high - low
    else:
        raise ValueError(f"unknown angle unit {unit!r}")
    cosine, sine = _series(point, big)
    # |cos t - cos u| and |sin t - sin u| are at most |t - u|, so a spread in the angle
    # widens both by the same amount.
    widen = Iv(-spread, spread)
    cosine, sine = add(cosine, widen), add(sine, widen)

    def rescale(value: Iv) -> Iv:
        unit_scale = 10**GUARD
        low, high = value.lo // unit_scale, _ceil_div(value.hi, unit_scale)
        return Iv(max(low, -scale), min(high, scale))

    return rescale(cosine), rescale(sine)


# --------------------------------------------------------------------------------------
# Poses
# --------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Pose:
    """A packing as its source prints it: decimal strings, nothing converted."""

    n: int
    side: str
    unit: str
    squares: tuple[tuple[str, str, str], ...]


def places(value: str) -> int:
    exponent = Decimal(value).as_tuple().exponent
    assert isinstance(exponent, int)
    return max(0, -exponent)


def read_pose(path: Path) -> Pose:
    """A retained Witness/v2 fact file, which carries the source's literals verbatim."""
    witness = safe_load(path.read_text(encoding="utf-8"))["witness"]
    expected = {
        "square_size": "1",
        "representation": "center-angle",
        "scalar": {"kind": "decimal"},
    }
    for key, value in expected.items():
        if witness[key] != value:
            raise ValueError(f"{path}: {key} is {witness[key]!r}, not {value!r}")
    coordinates = witness["coordinates"]
    if coordinates["origin"] != "lower-left" or coordinates["axes"] != "x-right-y-up":
        raise ValueError(f"{path}: unexpected frame {coordinates}")
    squares = witness["squares"]
    if [square["id"] for square in squares] != list(range(1, witness["n"] + 1)):
        raise ValueError(f"{path}: square ids are not 1..n")
    return Pose(
        n=witness["n"],
        side=witness["side"],
        unit=coordinates["angle_unit"],
        squares=tuple(
            (square["center"][0], square["center"][1], square["angle"]) for square in squares
        ),
    )


def upstream_bytes(source: packets.Source, pose: Pose) -> tuple[str, bytes]:
    """The upstream file this pose was read from, rebuilt byte for byte from the pose.

    Couzo prints a three-line header and ``x y theta`` rows; de Winter a JSON record whose
    other fields the acquisition record keeps. A digit, a sign or the angle unit read
    wrongly anywhere would change the bytes, and so their digest.
    """
    case = packets.cases(source)[pose.n]
    if source.layout == "couzo":
        unit = {"radians": "rad", "degrees": "deg"}[pose.unit]
        rows = "".join(f"{x} {y} {theta}\n" for x, y, theta in pose.squares)
        text = f"# n = {pose.n}\n# s = {pose.side}\n# x y theta({unit})\n{rows}"
        return case["file"], text.encode("utf-8")
    if source.layout == "de-winter":
        record = {
            "n": pose.n,
            "s": pose.side,
            "unit_square_side": "1",
            "angle_unit": pose.unit,
            "record_improvement": case["record_improvement"],
            "squares": [{"x": x, "y": y, "theta": theta} for x, y, theta in pose.squares],
            "verification": case["verification"],
            "previous_verified_s": case["previous_verified_s"],
            "method": case["method"],
        }
        return case["file"], (json.dumps(record, indent=2) + "\n").encode("utf-8")
    raise ValueError(f"no upstream layout for {source.id}")


def rebuilds_upstream(source: packets.Source, name: str, rebuilt: bytes) -> bool:
    """Whether bytes rebuilt from the facts are the upstream file the acquisition pinned."""
    pinned = {entry["path"]: entry for entry in packets.acquisition(source)["files"]}
    entry = pinned[name]
    return (
        len(rebuilt) == entry["bytes"]
        and hashlib.sha256(rebuilt).hexdigest() == entry["sha256"]
    )


# --------------------------------------------------------------------------------------
# The decision
# --------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Walls:
    """Four walls per square, each decided over the square's four vertices."""

    certified: int
    violated: int
    undecided: int
    #: The least clearance over every square and wall, at the working scale.
    least: Iv
    least_square: int


@dataclass(frozen=True, slots=True)
class Decision:
    """Everything decided about one pose at the last precision tried."""

    digits: int
    tried: tuple[int, ...]
    #: The pose's own extent, the least side of a square containing it.
    side: Iv
    pairs_total: int
    pairs_pruned: int
    separated: int
    touching: int
    overlapping: tuple[tuple[int, int], ...]
    undecided: tuple[tuple[int, int], ...]
    least_gap: Iv
    least_gap_pair: tuple[int, int]
    frame: Walls
    #: The translated pose's walls against `bound`, the side this pose proves.
    walls: Walls
    bound: str
    #: Whether the pose fits a square of the printed side, and of the claimed side.
    printed: str
    claimed: str | None

    @property
    def scale(self) -> int:
        return 10**self.digits

    @property
    def verdict(self) -> str:
        """``REFUSED`` on a proved overlap or a refuted side, ``VERIFIED`` when every pair
        is proved disjoint and every wall holds, ``UNDECIDED`` otherwise."""
        if self.overlapping or self.claimed == REFUTED:
            return REFUSED
        settled = not self.undecided and self.walls.violated == self.walls.undecided == 0
        return VERIFIED if settled and self.claimed in {None, CERTIFIED} else UNDECIDED


def _vertices(x: int, y: int, cosine: Iv, sine: Iv) -> list[tuple[Iv, Iv]]:
    """Twice each vertex ``c + s1 e1/2 + s2 e2/2``, with ``e1 = (cos, sin)`` and ``e2``
    its quarter turn, so that no halving rounds."""
    doubled_x, doubled_y = Iv(2 * x, 2 * x), Iv(2 * y, 2 * y)
    corners = []
    for first in (1, -1):
        for second in (1, -1):
            along = cosine if first == 1 else neg(cosine)
            across = sine if second == 1 else neg(sine)
            along_y = sine if first == 1 else neg(sine)
            across_y = cosine if second == 1 else neg(cosine)
            corners.append(
                (sub(add(doubled_x, along), across), add(add(doubled_y, along_y), across_y))
            )
    return corners


def _walls(
    corners: Sequence[Sequence[tuple[Iv, Iv]]], offset: tuple[int, int], doubled_side: int
) -> Walls:
    """Each square's four walls in ``[0, side]^2`` after subtracting ``offset``, doubled."""
    certified = violated = undecided = 0
    lowest = highest = None
    least_square = 0
    for index, square in enumerate(corners, start=1):
        xs = [x.lo - offset[0] for x, _ in square], [x.hi - offset[0] for x, _ in square]
        ys = [y.lo - offset[1] for _, y in square], [y.hi - offset[1] for _, y in square]
        for low, high in (xs, ys):
            for clearance in (
                Iv(min(low), min(high)),
                Iv(doubled_side - max(high), doubled_side - max(low)),
            ):
                if clearance.lo >= 0:
                    certified += 1
                elif clearance.hi < 0:
                    violated += 1
                else:
                    undecided += 1
                if lowest is None or clearance.lo < lowest:
                    lowest, least_square = clearance.lo, index
                if highest is None or clearance.hi < highest:
                    highest = clearance.hi
    assert lowest is not None
    assert highest is not None
    return Walls(certified, violated, undecided, halve(Iv(lowest, highest)), least_square)


def _twice_gap(
    axis: tuple[Iv, Iv], shift: tuple[int, int], other: tuple[Iv, Iv], scale: int
) -> Iv:
    """Twice the gap between two squares' projections on one square's unit edge normal.

    ``axis`` is that square's own edge direction, on which it projects to half-width
    ``1/2``; ``other`` is the second square's ``(cos, sin)``, and ``shift`` the exact
    centre displacement to it.
    """
    ax, ay = axis
    cosine, sine = other
    distance = add(scale_by(ax, shift[0], scale), scale_by(ay, shift[1], scale))
    along = add(mul(ax, cosine, scale), mul(ay, sine, scale))
    across = sub(mul(ay, cosine, scale), mul(ax, sine, scale))
    reach = add(magnitude(along), magnitude(across))
    twice = magnitude(distance)
    return sub(Iv(2 * twice.lo - scale, 2 * twice.hi - scale), reach)


def _pair(first: tuple[int, int, Iv, Iv], second: tuple[int, int, Iv, Iv], scale: int) -> Iv:
    """The best of the four edge-normal gaps, twice over, as an enclosure of their max."""
    x1, y1, c1, s1 = first
    x2, y2, c2, s2 = second
    forward, backward = (x2 - x1, y2 - y1), (x1 - x2, y1 - y2)
    gaps = (
        _twice_gap((c1, s1), forward, (c2, s2), scale),
        _twice_gap((neg(s1), c1), forward, (c2, s2), scale),
        _twice_gap((c2, s2), backward, (c1, s1), scale),
        _twice_gap((neg(s2), c2), backward, (c1, s1), scale),
    )
    return Iv(max(gap.lo for gap in gaps), max(gap.hi for gap in gaps))


def decide_at(pose: Pose, digits: int, claimed: Fraction | None = None) -> Decision:
    """Decide one pose at one fixed-point scale; `decide` escalates the digits."""
    scale = 10**digits
    squares: list[tuple[int, int, Iv, Iv]] = []
    for x, y, theta in pose.squares:
        centre = (Fraction(x) * scale, Fraction(y) * scale)
        if any(value.denominator != 1 for value in centre):
            raise ValueError(f"centre ({x}, {y}) has more than {digits} decimal places")
        cosine, sine = cos_sin(theta, pose.unit, scale)
        squares.append((int(centre[0]), int(centre[1]), cosine, sine))
    reach = 2 * scale * scale
    separated = touching = pruned = 0
    overlapping: list[tuple[int, int]] = []
    undecided: list[tuple[int, int]] = []
    least_lo = least_hi = None
    least_pair = (0, 0)
    for i, first in enumerate(squares):
        for j in range(i + 1, pose.n):
            second = squares[j]
            dx, dy = second[0] - first[0], second[1] - first[1]
            # Exact on the printed centres: at least sqrt(2) apart, the discs of radius
            # sqrt(2)/2 that hold the squares meet at most in a point.
            if dx * dx + dy * dy >= reach:
                pruned += 1
                continue
            gap = _pair(first, second, scale)
            if gap.lo >= 0:
                separated += 1
                # Exactly touching only when the gap is the point zero; a lower end of
                # zero alone would also count a true gap below the working precision.
                if gap.lo == 0 == gap.hi:
                    touching += 1
            elif gap.hi < 0:
                overlapping.append((i + 1, j + 1))
            else:
                undecided.append((i + 1, j + 1))
            if least_lo is None or gap.lo < least_lo:
                least_lo, least_pair = gap.lo, (i + 1, j + 1)
            if least_hi is None or gap.hi < least_hi:
                least_hi = gap.hi
    corners = [_vertices(x, y, cosine, sine) for x, y, cosine, sine in squares]
    xs = [x for square in corners for x, _ in square]
    ys = [y for square in corners for _, y in square]
    extents = [
        Iv(
            max(v.lo for v in values) - min(v.hi for v in values),
            max(v.hi for v in values) - min(v.lo for v in values),
        )
        for values in (xs, ys)
    ]
    side = halve(Iv(max(e.lo for e in extents), max(e.hi for e in extents)))
    printed = Fraction(pose.side)
    shown = places(pose.side)
    bound_units = max(int(printed * 10**shown), _ceil_div(side.hi * 10**shown, scale))
    offset = (min(v.lo for v in xs), min(v.lo for v in ys))
    return Decision(
        digits=digits,
        tried=(digits,),
        side=side,
        pairs_total=pose.n * (pose.n - 1) // 2,
        pairs_pruned=pruned,
        separated=separated,
        touching=touching,
        overlapping=tuple(overlapping),
        undecided=tuple(undecided),
        least_gap=halve(Iv(least_lo or 0, least_hi or 0)),
        least_gap_pair=least_pair,
        frame=_walls(corners, (0, 0), _exact(2 * printed * scale)),
        walls=_walls(corners, offset, _exact(2 * Fraction(bound_units, 10**shown) * scale)),
        bound=_decimal(bound_units, shown),
        printed=_fits(side, printed, scale),
        claimed=None if claimed is None else _fits(side, claimed, scale),
    )


def _exact(value: Fraction) -> int:
    if value.denominator != 1:
        raise ValueError(f"{value} is not on the working scale")
    return value.numerator


def _fits(side: Iv, claimed: Fraction, scale: int) -> str:
    """Whether the pose fits a square of side ``claimed``: whether its extent is at most it."""
    limit = claimed * scale
    if side.hi <= limit:
        return CERTIFIED
    if side.lo > limit:
        return REFUTED
    return UNDECIDED


def _decimal(units: int, shown: int) -> str:
    """``units`` of the ``shown``-th decimal place, exactly: a string is never rounded."""
    return format(Decimal(f"{units}E-{shown}"), "f")


def _settled(decision: Decision) -> bool:
    return (
        not decision.undecided
        and decision.frame.undecided == 0
        and UNDECIDED not in {decision.printed, decision.claimed}
    )


def decide(
    pose: Pose, claimed: Fraction | None = None, *, digits: Sequence[int] = DIGITS
) -> Decision:
    """Decide a pose at the first precision that settles it, or report what stays open."""
    floor = max(places(value) for square in pose.squares for value in square[:2])
    floor = max(floor, places(pose.side))
    tried: list[int] = []
    decision = None
    for working in digits:
        tried.append(max(working, floor))
        decision = decide_at(pose, tried[-1], claimed)
        if _settled(decision):
            break
    assert decision is not None
    return replace(decision, tried=tuple(tried))


# --------------------------------------------------------------------------------------
# Receipts
# --------------------------------------------------------------------------------------


def _scientific(value: Fraction, rounding: str) -> str:
    """Six significant digits, rounded in the direction given."""
    if value == 0:
        return "0"
    context = Context(prec=6, rounding=rounding)
    quotient = context.divide(Decimal(value.numerator), Decimal(value.denominator))
    return f"{quotient:.5e}"


def outward(value: Iv, scale: int, offset: Fraction = Fraction(0)) -> list[str]:
    """An enclosure minus ``offset``, printed to six digits and rounded outward."""
    return [
        _scientific(Fraction(value.lo, scale) - offset, ROUND_FLOOR),
        _scientific(Fraction(value.hi, scale) - offset, ROUND_CEILING),
    ]


def exact_decimal(end: int, digits: int) -> str:
    """An enclosure's end exactly, at the scale's own digits."""
    return format(Decimal(f"{end}E-{digits}"), "f")


def row(source: packets.Source, n: int) -> dict[str, Any]:
    """One receipt row: the pose's provenance and everything decided about it."""
    started = time.monotonic()
    path = source.fact(n)
    pose = read_pose(path)
    name, rebuilt = upstream_bytes(source, pose)
    matches = rebuilds_upstream(source, name, rebuilt)
    decision = decide(pose)
    scale = decision.scale
    printed = Fraction(pose.side)
    return {
        "n": n,
        "printed_side": pose.side,
        "angle_unit": pose.unit,
        "input": {
            "facts": path.relative_to(ROOT).as_posix(),
            "upstream_file": name,
            "upstream_bytes_rebuilt": matches,
        },
        "digits": decision.digits,
        "digits_tried": list(decision.tried),
        "side_enclosure": [
            exact_decimal(decision.side.lo, decision.digits),
            exact_decimal(decision.side.hi, decision.digits),
        ],
        "side_minus_printed": outward(decision.side, scale, printed),
        "printed_side_fits": decision.printed,
        "verified_value": decision.bound,
        "units_above_printed": int(
            (Fraction(decision.bound) - printed) * 10 ** places(pose.side)
        ),
        "exact_route": _exact_route(source, n, decision),
        "frame": {
            "fits_printed_side_as_placed": _frame_verdict(decision.frame),
            "least_wall_clearance": outward(decision.frame.least, scale),
            "least_wall_square": decision.frame.least_square,
        },
        "pairs": {
            "total": decision.pairs_total,
            "pruned_by_circles": decision.pairs_pruned,
            "decided_by_axes": decision.pairs_total - decision.pairs_pruned,
            "separated": decision.separated,
            "touching_exactly": decision.touching,
            "overlapping": [list(pair) for pair in decision.overlapping],
            "undecided": [list(pair) for pair in decision.undecided],
            "least_gap": outward(decision.least_gap, scale),
            "least_gap_squares": list(decision.least_gap_pair),
        },
        "walls": {
            "total": 4 * pose.n,
            "certified": decision.walls.certified,
            "against_side": decision.bound,
        },
        "verdict": decision.verdict,
        "wall_seconds": round(time.monotonic() - started, 2),
    }


def _exact_route(source: packets.Source, n: int, decision: Decision) -> dict[str, Any] | None:
    """The exact route's result beside this one, for comparison only; ``None`` when the
    exact route has not certified the case, since nothing here depends on it."""
    try:
        exact = packets.certification(source).get(n)
    except FileNotFoundError:
        return None
    if exact is None:
        return None
    scale = decision.scale
    exact_side = Fraction(exact["certified_side"])
    return {
        "verified_value": exact["verified_value"],
        "agrees": exact["verified_value"] == decision.bound,
        "certified_side_minus_enclosure": [
            _scientific(exact_side - Fraction(decision.side.hi, scale), ROUND_FLOOR),
            _scientific(exact_side - Fraction(decision.side.lo, scale), ROUND_CEILING),
        ],
    }


def _frame_verdict(walls: Walls) -> str:
    if walls.violated:
        return REFUTED
    return CERTIFIED if walls.undecided == 0 else UNDECIDED


# --------------------------------------------------------------------------------------
# Negative controls
# --------------------------------------------------------------------------------------


def shifted(pose: Pose, square: int, shift: str) -> Pose:
    """The pose with one square moved right by an exact decimal ``shift``."""
    rows = list(pose.squares)
    x, y, theta = rows[square - 1]
    rows[square - 1] = (str(Decimal(x) + Decimal(shift)), y, theta)
    return replace(pose, squares=tuple(rows))


def control_rows(source: packets.Source, n: int, square: int) -> list[dict[str, Any]]:
    """Mutations of one retained pose, each of which must be refused.

    A side ``1e-15`` below the pose's own extent must be refuted; one square moved right
    by ``1e-6`` must produce a proved overlap; and the angles read as degrees instead of
    the radians the source declares must be refused too, which is the unit mistake this
    route is built to catch.
    """
    pose = read_pose(source.fact(n))
    decision = decide(pose)
    shrunk = Fraction(decision.side.lo, decision.scale) - Fraction(1, 10**15)
    cases: list[tuple[str, Pose, Fraction | None]] = [
        ("side-shrunk-1e-15", pose, shrunk),
        (f"square-{square}-shifted-1e-6", shifted(pose, square, "1e-6"), None),
        ("angles-read-as-degrees", replace(pose, unit="degrees"), None),
    ]
    rows = []
    for name, mutated, claimed in cases:
        decision = decide(mutated, claimed)
        rows.append(
            {
                "control": name,
                "n": n,
                "digits": decision.digits,
                "claimed_side": None if claimed is None else "the extent's lower end - 1e-15",
                "claimed_side_fits": decision.claimed,
                "overlapping_pairs": len(decision.overlapping),
                "first_overlaps": [list(pair) for pair in decision.overlapping[:4]],
                "verdict": decision.verdict,
            }
        )
    return rows


#: The pose each packet's controls mutate, and the square moved: the exact route's own
#: choice where the packet has one (``n = 68`` square 31, and ``n = 208`` square 2 in the
#: 3 October packet); at ``n = 211``, square 80, the left square of the closest pair the
#: source reports (zero-based 79 and 81), which moving right closes.
CONTROL_CASES = {
    **{source.id: source.control for source in packets.CERTIFIED if source.control is not None},
    packets.DE_WINTER.id: (211, 80),
}


def controls(source: packets.Source) -> dict[str, Any]:
    n, square = CONTROL_CASES[source.id]
    return {
        "tool": TOOL,
        "facts": source.fact(n).relative_to(ROOT).as_posix(),
        "expectation": "every control is refused",
        "controls": control_rows(source, n, square),
    }


# --------------------------------------------------------------------------------------
# Writing and replaying
# --------------------------------------------------------------------------------------


def _row_unit(unit: tuple[str, int]) -> dict[str, Any]:
    source_id, n = unit
    return {"source": source_id, **row(packets.BY_ID[source_id], n)}


def _units(
    sources: Sequence[packets.Source], numbers: set[int] | None
) -> list[tuple[str, int]]:
    units = [
        (source.id, n)
        for source in sources
        for n in sorted(packets.cases(source))
        if numbers is None or n in numbers
    ]
    return sorted(units, key=lambda unit: -unit[1])


def _map(
    function: Callable[[tuple[str, int]], dict[str, Any]],
    units: list[tuple[str, int]],
    workers: int,
) -> list[dict[str, Any]]:
    if workers <= 1:
        return [function(unit) for unit in units]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(function, units))


def header(source: packets.Source) -> dict[str, Any]:
    return {
        "tool": TOOL,
        "method": "interval-certified",
        "arithmetic": (
            "decimal fixed-point intervals with outward rounding; cos and sin by Taylor "
            f"polynomials with the Lagrange remainder, {GUARD} guard digits"
        ),
        "digits_schedule": list(DIGITS),
        "shared_with_exact_route": list(SHARED),
        "source": source.id,
    }


def dump(record: Mapping[str, Any]) -> str:
    """The record as JSON with one line per case row, so a packet stays diffable."""
    lines = ["{"]
    items = list(record.items())
    for index, (key, value) in enumerate(items):
        comma = "," if index < len(items) - 1 else ""
        if key in {"cases", "controls"}:
            lines.append(f"  {json.dumps(key)}: [")
            lines.extend(
                f"    {json.dumps(entry)}" + ("," if position < len(value) - 1 else "")
                for position, entry in enumerate(value)
            )
            lines.append(f"  ]{comma}")
        else:
            lines.append(f"  {json.dumps(key)}: {json.dumps(value)}{comma}")
    lines.append("}")
    return "\n".join(lines) + "\n"


def receipt(source: packets.Source) -> Path:
    return source.receipts / RECEIPT


def control_receipt(source: packets.Source) -> Path:
    return source.receipts / CONTROLS


def _write(path: Path, record: Mapping[str, Any]) -> None:
    with atomic_output_file(path) as temporary:
        temporary.write_text(dump(record), encoding="utf-8")


def certify(sources: Sequence[packets.Source], numbers: set[int] | None, workers: int) -> None:
    rows = _map(_row_unit, _units(sources, numbers), workers)
    for source in sources:
        mine = {
            entry["n"]: {key: value for key, value in entry.items() if key != "source"}
            for entry in rows
            if entry["source"] == source.id
        }
        if not mine:
            continue
        path = receipt(source)
        previous = (
            {entry["n"]: entry for entry in json.loads(path.read_text("utf-8"))["cases"]}
            if path.is_file()
            else {}
        )
        merged = {**previous, **mine}
        _write(path, {**header(source), "cases": [merged[n] for n in sorted(merged)]})
        for n in sorted(mine):
            entry = mine[n]
            print(
                f"{source.id} n={n}: {entry['verdict']} at {entry['digits']} digits, side "
                f"{entry['side_minus_printed']} from printed, {entry['wall_seconds']} s"
            )
        if CONTROL_CASES[source.id][0] in mine:
            _write(control_receipt(source), controls(source))
            print(f"{source.id}: interval negative controls written")


def _comparable(entry: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in entry.items() if key not in {"wall_seconds", "source"}}


def check(
    sources: Sequence[packets.Source], numbers: set[int] | None, workers: int
) -> list[str]:
    """Decide every case and control again; each must be what its receipt records."""
    problems: list[str] = []
    fresh = _map(_row_unit, _units(sources, numbers), workers)
    for source in sources:
        recorded = {
            entry["n"]: entry
            for entry in json.loads(receipt(source).read_text("utf-8"))["cases"]
        }
        if set(recorded) != set(packets.cases(source)):
            problems.append(f"{source.id}: the interval receipt does not cover every case")
        for entry in (entry for entry in fresh if entry["source"] == source.id):
            n = entry["n"]
            if n not in recorded or _comparable(recorded[n]) != _comparable(entry):
                problems.append(f"{source.id} n={n}: decided differently from its receipt")
            if entry["verdict"] != VERIFIED:
                problems.append(f"{source.id} n={n}: {entry['verdict']}")
            if not entry["input"]["upstream_bytes_rebuilt"]:
                problems.append(f"{source.id} n={n}: the facts do not rebuild the pinned file")
            exact_route = entry["exact_route"]
            if exact_route is not None and not exact_route["agrees"]:
                problems.append(f"{source.id} n={n}: the exact route's value differs")
            print(f"  {source.id} n={n}: {entry['verdict']} ({entry['wall_seconds']} s)")
        if numbers is None or CONTROL_CASES[source.id][0] in numbers:
            stored = json.loads(control_receipt(source).read_text("utf-8"))
            again = controls(source)
            if stored != again:
                problems.append(f"{source.id}: the interval controls differ from their receipt")
            if any(entry["verdict"] != REFUSED for entry in again["controls"]):
                problems.append(f"{source.id}: an interval control was not refused")
    return problems


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name, text in (("certify", "decide and write receipts"), ("check", "decide again")):
        command = commands.add_parser(name, help=text)
        command.add_argument("--source", choices=tuple(s.id for s in packets.CERTIFIED))
        command.add_argument("--n", type=int, action="append")
        command.add_argument("--workers", type=int, default=1)
    args = parser.parse_args(argv)
    chosen = [packets.BY_ID[args.source]] if args.source else list(packets.CERTIFIED)
    numbers = set(args.n) if args.n else None
    if args.command == "certify":
        certify(chosen, numbers, args.workers)
        return 0
    problems = check(chosen, numbers, args.workers)
    for problem in problems:
        print(f"FAIL {problem}", file=sys.stderr)
    if problems:
        return 1
    print("upper-bound intervals: every case and control decided as its receipt records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
