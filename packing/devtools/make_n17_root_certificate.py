"""Produce the fixed H-255 exact rational polynomial-root certificate.

The polynomial and interval kernel is reusable for synthetic controls. The CLI fixes
the H-253 source identity, midpoint and radius; it performs no search or adjustment.
The resulting certificate proves a root in its box only after separate checking.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Self

from devtools.check_n17_contact_chart import SOURCE, SOURCE_ROW_LABELS, load_frozen_source

ZERO, ONE = Q(0), Q(1)
RHO = Q(1, 10**12)
REPO = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Interval:
    lo: Q
    hi: Q

    def __post_init__(self) -> None:
        if type(self.lo) is not Q or type(self.hi) is not Q or self.lo > self.hi:
            raise ValueError("interval endpoints must be ordered exact Fractions")

    @classmethod
    def point(cls, value: Q) -> Self:
        return cls(value, value)

    def __add__(self, other: Interval) -> Interval:
        return Interval(self.lo + other.lo, self.hi + other.hi)

    def __neg__(self) -> Interval:
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other: Interval) -> Interval:
        return self + -other

    def __mul__(self, other: Interval) -> Interval:
        products = (
            self.lo * other.lo,
            self.lo * other.hi,
            self.hi * other.lo,
            self.hi * other.hi,
        )
        return Interval(min(products), max(products))

    def __pow__(self, exponent: int) -> Interval:
        if type(exponent) is not int or exponent < 0:
            raise ValueError("interval power must be a nonnegative integer")
        if exponent == 0:
            return Interval.point(ONE)
        if exponent % 2 == 0:
            values = (self.lo**exponent, self.hi**exponent)
            return Interval(ZERO if self.lo <= 0 <= self.hi else min(values), max(values))
        return Interval(self.lo**exponent, self.hi**exponent)

    def magnitude(self) -> Q:
        return max(abs(self.lo), abs(self.hi))

    def as_json(self) -> list[str]:
        return [str(self.lo), str(self.hi)]


@dataclass(frozen=True)
class Polynomial:
    terms: dict[tuple[int, int], Q]

    def __post_init__(self) -> None:
        for exponents, coefficient in self.terms.items():
            if (
                len(exponents) != 2
                or any(type(power) is not int or power < 0 for power in exponents)
                or type(coefficient) is not Q
            ):
                raise ValueError(
                    "polynomial terms must have nonnegative exponents and exact coefficients"
                )

    @classmethod
    def constant(cls, value: int | Q) -> Self:
        if type(value) not in (int, Q):
            raise ValueError("polynomial constants must be exact integers or Fractions")
        coefficient = Q(value)
        return cls({(0, 0): coefficient} if coefficient else {})

    @classmethod
    def variable(cls, axis: int) -> Self:
        if axis not in (0, 1):
            raise ValueError("polynomial variable axis must be 0 or 1")
        return cls({(1, 0) if axis == 0 else (0, 1): ONE})

    def __add__(self, other: Polynomial | int | Q) -> Polynomial:
        other_poly = other if isinstance(other, Polynomial) else Polynomial.constant(other)
        terms = self.terms.copy()
        for powers, coefficient in other_poly.terms.items():
            terms[powers] = terms.get(powers, ZERO) + coefficient
            if not terms[powers]:
                del terms[powers]
        return Polynomial(terms)

    def __radd__(self, other: Polynomial | int | Q) -> Polynomial:
        return self + other

    def __neg__(self) -> Polynomial:
        return Polynomial({powers: -coefficient for powers, coefficient in self.terms.items()})

    def __sub__(self, other: Polynomial | int | Q) -> Polynomial:
        other_poly = other if isinstance(other, Polynomial) else Polynomial.constant(other)
        return self + -other_poly

    def __rsub__(self, other: Polynomial | int | Q) -> Polynomial:
        other_poly = other if isinstance(other, Polynomial) else Polynomial.constant(other)
        return other_poly - self

    def __mul__(self, other: Polynomial | int | Q) -> Polynomial:
        other_poly = other if isinstance(other, Polynomial) else Polynomial.constant(other)
        terms: dict[tuple[int, int], Q] = {}
        for (i, j), a in self.terms.items():
            for (k, ell), b in other_poly.terms.items():
                powers = (i + k, j + ell)
                terms[powers] = terms.get(powers, ZERO) + a * b
        return Polynomial({powers: value for powers, value in terms.items() if value})

    def __rmul__(self, other: Polynomial | int | Q) -> Polynomial:
        return self * other

    def __pow__(self, exponent: int) -> Polynomial:
        if type(exponent) is not int or exponent < 0:
            raise ValueError("polynomial power must be a nonnegative integer")
        result = Polynomial.constant(1)
        base = self
        power = exponent
        while power:
            if power & 1:
                result = result * base
            base = base * base
            power >>= 1
        return result

    def derivative(self, axis: int) -> Polynomial:
        if axis not in (0, 1):
            raise ValueError("derivative axis must be 0 or 1")
        terms: dict[tuple[int, int], Q] = {}
        for powers, coefficient in self.terms.items():
            if powers[axis]:
                reduced = list(powers)
                reduced[axis] -= 1
                terms[(reduced[0], reduced[1])] = coefficient * powers[axis]
        return Polynomial(terms)

    def evaluate(self, x: Q | Interval, y: Q | Interval) -> Q | Interval:
        if isinstance(x, Interval) != isinstance(y, Interval):
            raise TypeError("polynomial inputs must both be points or intervals")
        if isinstance(x, Interval) and isinstance(y, Interval):
            total = Interval.point(ZERO)
            for (i, j), coefficient in self.terms.items():
                total += Interval.point(coefficient) * (x**i) * (y**j)
            return total
        if isinstance(x, Q) and isinstance(y, Q):
            return sum(
                (coefficient * x**i * y**j for (i, j), coefficient in self.terms.items()), ZERO
            )
        raise TypeError("polynomial inputs must be exact Fractions or intervals")

    def as_json(self) -> list[list[int | str]]:
        return [[i, j, str(coefficient)] for (i, j), coefficient in sorted(self.terms.items())]


def fixed_polynomials() -> tuple[Polynomial, Polynomial]:
    """The two frozen integer polynomials in H-255, built symbolically."""
    t, b = Polynomial.variable(0), Polynomial.variable(1)
    d = 1 + t * t
    e = 1 + b * b
    ell = (1 + t) * d
    n_alpha = (1 - t * t) * (1 - b * b) - 4 * t * b
    pi2 = 2 * t * (1 - t) * (1 - b * b) + (1 - t) ** 2 * ell * b - t * ell * e
    pi3 = (
        (1 - t * t) * d * e**2
        - (1 + t) * d * e * (b * (1 - t * t) + t * (1 - b * b))
        - (1 - t) * (1 - b * b) * n_alpha
    )
    return pi2, pi3


def _point_value(value: Q | Interval) -> Q:
    if not isinstance(value, Q):
        raise TypeError("expected point polynomial evaluation")
    return value


def _interval_value(value: Q | Interval) -> Interval:
    if not isinstance(value, Interval):
        raise TypeError("expected interval polynomial evaluation")
    return value


def certify(
    polynomials: tuple[Polynomial, Polynomial], midpoint: tuple[Q, Q], radius: Q
) -> dict[str, Any]:
    """Build an exact 2D Krawczyk receipt, including strict-failure diagnostics."""
    if (
        len(polynomials) != 2
        or len(midpoint) != 2
        or any(type(value) is not Q for value in midpoint)
        or type(radius) is not Q
        or radius <= 0
    ):
        raise ValueError(
            "expected two exact polynomials, two rational midpoint values and rho>0"
        )
    box = tuple(Interval(value - radius, value + radius) for value in midpoint)
    fm = tuple(_point_value(poly.evaluate(*midpoint)) for poly in polynomials)
    derivatives = tuple(
        tuple(poly.derivative(axis) for axis in range(2)) for poly in polynomials
    )
    jm = tuple(
        tuple(_point_value(poly.evaluate(*midpoint)) for poly in row) for row in derivatives
    )
    determinant = jm[0][0] * jm[1][1] - jm[0][1] * jm[1][0]
    if determinant == 0:
        raise ValueError("singular midpoint Jacobian")
    c = (
        (jm[1][1] / determinant, -jm[0][1] / determinant),
        (-jm[1][0] / determinant, jm[0][0] / determinant),
    )
    identity = tuple(tuple(ONE if i == j else ZERO for j in range(2)) for i in range(2))
    cj = tuple(
        tuple(sum((c[i][k] * jm[k][j] for k in range(2)), ZERO) for j in range(2))
        for i in range(2)
    )
    jc = tuple(
        tuple(sum((jm[i][k] * c[k][j] for k in range(2)), ZERO) for j in range(2))
        for i in range(2)
    )
    if cj != identity or jc != identity:
        raise ValueError("rational inverse identity failed")
    jbox = tuple(
        tuple(_interval_value(poly.evaluate(*box)) for poly in row) for row in derivatives
    )
    matrix = tuple(
        tuple(
            Interval.point(identity[i][j])
            - sum(
                (Interval.point(c[i][k]) * jbox[k][j] for k in range(2)), Interval.point(ZERO)
            )
            for j in range(2)
        )
        for i in range(2)
    )
    row_norms = tuple(sum((cell.magnitude() for cell in row), ZERO) for row in matrix)
    q = max(row_norms)
    correction = tuple(sum((c[i][j] * fm[j] for j in range(2)), ZERO) for i in range(2))
    inclusion = tuple(abs(correction[i]) + radius * row_norms[i] for i in range(2))
    failures = [
        name
        for name, okay in (
            ("contraction", q < 1),
            ("inclusion.0", inclusion[0] < radius),
            ("inclusion.1", inclusion[1] < radius),
        )
        if not okay
    ]
    return {
        "schema": "n17-root-certificate/v1",
        "box": {"midpoint": [str(value) for value in midpoint], "radius": str(radius)},
        "polynomials": [poly.as_json() for poly in polynomials],
        "F_mid": [str(value) for value in fm],
        "J_mid": [[str(value) for value in row] for row in jm],
        "C": [[str(value) for value in row] for row in c],
        "J_box": [[value.as_json() for value in row] for row in jbox],
        "M": [[value.as_json() for value in row] for row in matrix],
        "row_norms": [str(value) for value in row_norms],
        "q": str(q),
        "correction": [str(value) for value in correction],
        "inclusion_bounds": [str(value) for value in inclusion],
        "criterion_passed": not failures,
        "failures": failures,
    }


def fixed_domain(midpoint: tuple[Q, Q], radius: Q) -> tuple[dict[str, list[str]], list[str]]:
    """Enclose all H-255 denominator, angle and side guards on the whole box."""
    t = Interval(midpoint[0] - radius, midpoint[0] + radius)
    b = Interval(midpoint[1] - radius, midpoint[1] + radius)
    one = Interval.point(ONE)
    d, e = one + t**2, one + b**2
    ell = (one + t) * d
    k = one + Interval.point(Q(2)) * t - t**2
    lower = Interval.point(Q(187)) * t**2 - Interval.point(Q(214)) * t + Interval.point(Q(53))
    upper = (
        Interval.point(Q(1169)) * t**2 - Interval.point(Q(1338)) * t + Interval.point(Q(331))
    )
    intervals = {
        "t": t,
        "b": b,
        "D": d,
        "E": e,
        "L": ell,
        "K": k,
        "side_guard_lower": lower,
        "side_guard_upper": upper,
    }
    failures = [
        name
        for name, passed in (
            ("domain.t", t.lo >= Q(36, 100) and t.hi <= Q(37, 100)),
            ("domain.b", b.lo >= Q(33, 100) and b.hi <= Q(34, 100)),
            ("denominator.t", t.lo > 0),
            ("denominator.D", d.lo > 0),
            ("denominator.E", e.lo > 0),
            ("denominator.L", ell.lo > 0),
            ("denominator.K", k.lo > 0),
            ("side_guard_lower", lower.lo >= 0),
            ("side_guard_upper", upper.hi <= 0),
        )
        if not passed
    ]
    return {name: interval.as_json() for name, interval in intervals.items()}, failures


def _git_provenance() -> dict[str, str | bool]:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=REPO, check=True, capture_output=True, text=True
    ).stdout.strip()
    status = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return {"git_commit": head, "git_clean": not status, "git_clean_scope": "tracked"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.parse_args(argv)
    try:
        poses, digest = load_frozen_source(SOURCE)
        midpoint = poses[8].t, -poses[15].t
        result = certify(fixed_polynomials(), midpoint, RHO)
        domain, domain_failures = fixed_domain(midpoint, RHO)
        result["domain"] = domain
        result["failures"].extend(domain_failures)
        result["source"] = {
            "path": SOURCE.relative_to(REPO).as_posix(),
            "sha256": digest,
            "row_to_label": list(SOURCE_ROW_LABELS),
        }
        result["provenance"] = _git_provenance()
        if not result["provenance"]["git_clean"]:
            result["failures"].append("tracked Git files differ from HEAD")
        result["criterion_passed"] = not result["failures"]
    except (OSError, ValueError, TypeError, subprocess.CalledProcessError) as error:
        print(
            json.dumps(
                {
                    "schema": "n17-root-certificate/v1",
                    "criterion_passed": False,
                    "refused": str(error),
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["criterion_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
