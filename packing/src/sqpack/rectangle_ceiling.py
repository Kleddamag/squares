"""Exact ceilings on what a rectangle-density certificate can prove (T-058).

A rectangle-density certificate for ``n`` at container side ``L`` is a nonnegative,
D4-invariant density ``g`` on ``[0, L]^2`` of total mass ``M``, together with a check
that every closed side-``B`` square ("core") whose orientation lies in the checked net
and which lies inside ``[0, L]^2`` captures mass at least one. The net is the 201
directions ``(cos, sin) = ((1 - t^2), 2t) / (1 + t^2)`` with ``t = r D``,
``D = 83/40000``, ``r = 0..200``; D4 invariance extends the check to their reflections
and quarter turns. :mod:`sqpack.rectangle_density` is this repository's implementation
of that contract; its centre domain is the full legal domain ``[h, L - h]^2``.

**Ceiling lemma.** If ``[0, L]^2`` contains ``n`` net cores with pairwise disjoint
interiors, no such certificate at any side ``L' >= L`` has ``M < n``. The cores lie in
``[0, L']^2``, so each captures at least one; ``g`` is a bounded density, so core
boundaries carry no mass and ``M >= n``.

A :class:`CeilingCertificate` is exactly that finite object: ``n`` cores with rational
centres and net orientations, so its containment and disjointness are decided here in
exact rational arithmetic. Nothing about the packing that suggested it is trusted; a
witness is used only to place the cores.

The general ceiling follows from the same lemma. Every orientation is within
``arctan D`` of the net, since consecutive half-angles differ by
``arctan(D / (1 + r(r+1)D^2)) <= arctan D`` and ``t_200`` passes ``tan(pi/8)``. A core
turned by ``|delta| <= arctan D`` from a square fits inside the concentric square of
side ``B(cos delta + sin delta) <= B(1 + D)/sqrt(1 + D^2) < B(1 + D) = ALPHA``. So a
packing of ``n`` unit squares at side ``U`` scaled by ``ALPHA`` yields a ceiling at
``ALPHA * U``, and one whose orientations all lie in the net yields ``B * U``.
:func:`premise_checks` decides each numeric premise of that argument exactly.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

import mpmath as mp

from sqpack.rectangle_density import ANGLE_COUNT, ANGLE_STEP
from sqpack.witness import materialize_witness

CORE_SIDE = Fraction(9977, 10000)
ALPHA = CORE_SIDE * (1 + ANGLE_STEP)
#: Relative enlargements tried, in order, when placing cores from a numerical witness.
#: Zero is tried first so an exact axis-aligned witness yields exactly ``B * U``.
SLACKS = (Fraction(0), *(Fraction(1, 10**k) for k in range(12, 3, -1)))
_CENTRE_DIGITS = 30
_SIDE_DIGITS = 15


class CeilingError(ValueError):
    """A ceiling certificate is malformed and cannot be decided."""


@dataclass(frozen=True)
class Core:
    """A side-``B`` core at net direction ``index``, reflected when ``reflected``."""

    x: Fraction
    y: Fraction
    index: int
    reflected: bool


@dataclass(frozen=True)
class CeilingCertificate:
    n: int
    side: Fraction
    core_side: Fraction
    cores: tuple[Core, ...]


@dataclass(frozen=True)
class CeilingReport:
    status: str
    reasons: tuple[str, ...]

    @property
    def verified(self) -> bool:
        return self.status == "VERIFIED"


def net_orientation(index: int, *, reflected: bool = False) -> tuple[Fraction, Fraction]:
    """Return the exact rational direction of a net angle or of its reflection."""

    if isinstance(index, bool) or not isinstance(index, int) or not 0 <= index < ANGLE_COUNT:
        raise CeilingError(f"net index {index!r} is outside 0..{ANGLE_COUNT - 1}")
    tangent = index * ANGLE_STEP
    denominator = 1 + tangent * tangent
    cosine = (1 - tangent * tangent) / denominator
    sine = 2 * tangent / denominator
    return cosine, -sine if reflected else sine


def premise_checks() -> dict[str, bool]:
    """Decide the numeric premises of the general ceiling argument exactly."""

    d = ANGLE_STEP
    endpoint = (ANGLE_COUNT - 1) * d
    return {
        # ALPHA is the reviewed factor B(1 + D).
        "alpha_is_399908091_over_400000000": Fraction(399908091, 400000000) == ALPHA,
        # tan(theta_200 / 2) >= tan(pi/8) = sqrt(2) - 1, so the net reaches 45 degrees.
        "net_reaches_45_degrees": endpoint * endpoint + 2 * endpoint - 1 >= 0,
        # tan of every half-gap, D / (1 + r(r+1)D^2), is at most D.
        "every_half_gap_at_most_arctan_d": all(
            d / (1 + r * (r + 1) * d * d) <= d for r in range(ANGLE_COUNT - 1)
        ),
        # The worst containment factor (1 + D)/sqrt(1 + D^2), squared, is below (1 + D)^2.
        "sharp_factor_below_alpha": (1 + d) ** 2 / (1 + d * d) < (1 + d) ** 2,
        # A net core fits in a unit square, which the lower-bound direction also needs.
        "alpha_below_one": ALPHA < 1,
        # Every net direction is an exact unit vector.
        "net_directions_are_unit": all(
            c * c + s * s == 1 for c, s in (net_orientation(r) for r in range(ANGLE_COUNT))
        ),
    }


def _half_extent(
    core_side: Fraction, cosine: Fraction, sine: Fraction, axis: tuple
) -> Fraction:
    ux, uy = axis
    return core_side * (abs(ux * cosine + uy * sine) + abs(-ux * sine + uy * cosine)) / 2


def _interiors_disjoint(core_side: Fraction, first: Core, second: Core) -> bool:
    """Separating-axis test: interiors are disjoint iff some edge normal separates them."""

    a = net_orientation(first.index, reflected=first.reflected)
    b = net_orientation(second.index, reflected=second.reflected)
    for cosine, sine in (a, b):
        for axis in ((cosine, sine), (-sine, cosine)):
            gap = abs(axis[0] * (second.x - first.x) + axis[1] * (second.y - first.y))
            reach = _half_extent(core_side, *a, axis) + _half_extent(core_side, *b, axis)
            if gap >= reach:
                return True
    return False


def verify_ceiling(certificate: CeilingCertificate) -> CeilingReport:
    """Decide containment and pairwise interior-disjointness exactly."""

    reasons: list[str] = []
    n, side, core_side = certificate.n, certificate.side, certificate.core_side
    if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
        raise CeilingError("n must be a positive integer")
    if not all(isinstance(v, Fraction) for v in (side, core_side)):
        raise CeilingError("side and core side must be exact rationals")
    if not 0 < core_side < 1 or side <= 0:
        raise CeilingError("invalid side or core side")
    if len(certificate.cores) != n:
        reasons.append(f"has {len(certificate.cores)} cores, not n = {n}")
    extents: list[tuple[Fraction, Fraction, Fraction, Fraction]] = []
    for position, core in enumerate(certificate.cores):
        if not (isinstance(core.x, Fraction) and isinstance(core.y, Fraction)):
            raise CeilingError(f"core {position} centre is not exact")
        cosine, sine = net_orientation(core.index, reflected=core.reflected)
        half = core_side * (abs(cosine) + abs(sine)) / 2
        box = (core.x - half, core.y - half, core.x + half, core.y + half)
        if box[0] < 0 or box[1] < 0 or box[2] > side or box[3] > side:
            reasons.append(f"core {position} leaves the container")
        extents.append(box)
    order = sorted(range(len(extents)), key=lambda i: extents[i][0])
    for offset, i in enumerate(order):
        for j in order[offset + 1 :]:
            if extents[j][0] >= extents[i][2]:
                break
            if extents[j][1] >= extents[i][3] or extents[i][1] >= extents[j][3]:
                continue
            if not _interiors_disjoint(core_side, certificate.cores[i], certificate.cores[j]):
                reasons.append(f"cores {min(i, j)} and {max(i, j)} overlap")
    return CeilingReport("REFUSED" if reasons else "VERIFIED", tuple(reasons))


@dataclass(frozen=True)
class Placement:
    """How a witness was turned into a certificate, for the receipt."""

    certificate: CeilingCertificate
    worst_factor: str
    aligned: bool
    slack: Fraction


def _nearest_net(angle: Any) -> tuple[int, bool, Any]:
    """Nearest net orientation to ``angle`` (radians, any value), with its discrepancy."""

    quarter = mp.pi / 2
    reduced = angle - quarter * mp.floor(angle / quarter)
    best: tuple[int, bool, Any] | None = None
    for index in range(ANGLE_COUNT):
        theta = 2 * mp.atan(index * mp.mpf(ANGLE_STEP.numerator) / ANGLE_STEP.denominator)
        for reflected, target in (
            (False, theta),
            (True, quarter - theta),
            (False, theta + quarter),
        ):
            delta = reduced - target
            if best is None or abs(delta) < abs(best[2]):
                best = (index, reflected and index > 0, delta)
    assert best is not None
    return best


def _round_up(value: Any, digits: int) -> Fraction:
    scale = 10**digits
    return Fraction(int(mp.ceil(value * scale)), scale)


def _nearest(value: Any, digits: int) -> Fraction:
    scale = 10**digits
    return Fraction(int(mp.nint(value * scale)), scale)


def _side(witness: Mapping[str, Any], approximate: Any) -> Fraction:
    try:
        return Fraction(str(witness["side"]))
    except ValueError:
        return _round_up(approximate, _CENTRE_DIGITS)


def place_cores(
    witness: Mapping[str, Any], *, slacks: Sequence[Fraction] = SLACKS
) -> Placement | None:
    """Place net cores from a witness and return the first exactly verified placement.

    Each square's core takes its nearest net orientation; all centres are scaled about
    the container centre by ``B * max(cos delta + sin delta) * (1 + slack)``. The
    witness is only a guide, so a numerical witness costs at most a little slack.
    """

    squares, approximate_side = materialize_witness(witness, digits=60)
    mp.mp.dps = 60
    n = len(squares)
    centres = []
    orientations = []
    worst = mp.mpf(1)
    aligned = True
    for corners in squares:
        cx = sum(point[0] for point in corners) / 4
        cy = sum(point[1] for point in corners) / 4
        angle = mp.atan2(corners[1][1] - corners[0][1], corners[1][0] - corners[0][0])
        index, reflected, delta = _nearest_net(angle)
        if abs(delta) > mp.mpf(10) ** -40:
            aligned = False
            worst = max(worst, mp.cos(abs(delta)) + mp.sin(abs(delta)))
        centres.append((_nearest(cx, _CENTRE_DIGITS), _nearest(cy, _CENTRE_DIGITS)))
        orientations.append((index, reflected))
    side = _side(witness, approximate_side)
    for slack in slacks:
        if aligned and slack == 0:
            scale = CORE_SIDE
            container = CORE_SIDE * side
        else:
            scale = _round_up(
                CORE_SIDE * worst * (1 + mp.mpf(slack.numerator) / slack.denominator), 20
            )
            container = _round_up(
                mp.mpf((scale * side * (1 + slack)).numerator)
                / (scale * side * (1 + slack)).denominator,
                _SIDE_DIGITS,
            )
        half_side, half_container = side / 2, container / 2
        cores = tuple(
            Core(
                half_container + scale * (x - half_side),
                half_container + scale * (y - half_side),
                index,
                reflected,
            )
            for (x, y), (index, reflected) in zip(centres, orientations, strict=True)
        )
        certificate = CeilingCertificate(n, container, CORE_SIDE, cores)
        if verify_ceiling(certificate).verified:
            return Placement(certificate, str(mp.nstr(worst, 25)), aligned, slack)
    return None


def grid_certificate(n: int) -> CeilingCertificate:
    """Cores of the first ``n`` cells of the ``k x k`` grid, ``k = ceil(sqrt n)``, at ``B``."""

    if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
        raise CeilingError("n must be a positive integer")
    k = math.isqrt(n - 1) + 1
    cores = tuple(
        Core(
            CORE_SIDE * (2 * (cell % k) + 1) / 2,
            CORE_SIDE * (2 * (cell // k) + 1) / 2,
            0,
            reflected=False,
        )
        for cell in range(n)
    )
    return CeilingCertificate(n, CORE_SIDE * k, CORE_SIDE, cores)


def certificate_document(certificate: CeilingCertificate) -> dict[str, object]:
    """A lossless JSON form; :func:`certificate_from_document` reads it back."""

    return {
        "n": certificate.n,
        "L": str(certificate.side),
        "B": str(certificate.core_side),
        "D": str(ANGLE_STEP),
        "cores": [
            [str(core.x), str(core.y), core.index, core.reflected] for core in certificate.cores
        ],
    }


def certificate_from_document(document: Mapping[str, Any]) -> CeilingCertificate:
    if Fraction(document["D"]) != ANGLE_STEP:
        raise CeilingError("certificate net step does not match the checked net")
    cores = []
    for row in document["cores"]:
        x, y, index, reflected = row
        if not isinstance(reflected, bool):
            raise CeilingError("reflection flag must be a boolean")
        cores.append(Core(Fraction(x), Fraction(y), index, reflected))
    return CeilingCertificate(
        document["n"], Fraction(document["L"]), Fraction(document["B"]), tuple(cores)
    )
