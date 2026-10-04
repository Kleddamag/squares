"""Bašić and Slivková's piercing lower bound on s(n), exactly, for every case.

Bašić and Slivková 2018 (`[Basic-Slivkova 2018]`, Discrete Applied Mathematics 247)
bound the piercing number of the open unit squares inside a square of side `x`
(Theorem 7, by an explicit equilateral-lattice piercing set), and no more than that many
unit squares can be packed in the square (Proposition 8). Writing

    m(x) = ⌊(2/√3)(x + 1 - 2√2)⌋,
    B(x) = ⌊x⌋(m(x) + 2)                         if {x} < 1/2,
    B(x) = ⌊x⌋(m(x) + 2) + ⌊(m(x) + 2)/2⌋        if {x} ≥ 1/2,

at most `B(x)` unit squares fit in side `x`, so `s(n) > x` wherever `B(x) ≤ n - 1`.
`B` is a nondecreasing step function, right-continuous, whose steps fall only where `x`
is an integer, a half-integer, or `(√3/2)j + 2√2 - 1` for an integer `j`. The bound
`s(n) ≥ x*(n)` therefore holds at the first such point with `B(x*) ≥ n`, and that point
is computed here exactly, as an algebraic number, with `sympy`. The paper's own use is
Theorem 10, `s(61) ≥ 7√3/2 + 2√2 - 1 ≈ 7.8906`; this tool asks the same question of
every case and compares the answer with each case record's verified lower bound.

Nothing here depends on Nagamochi 2005: the paper cites it only for the values it
reproduces. The theorem is a published proof read here (2026-10-03), not replayed; this
tool replays only its arithmetic.

From `packing/`, with `uv run --frozen --all-extras --group dev` before each:

    python -m devtools.check_piercing_lower_bounds
    python -m devtools.check_piercing_lower_bounds --update
    python -m devtools.check_piercing_lower_bounds --check
"""

from __future__ import annotations

import argparse
import itertools
import math
import sys
from collections.abc import Sequence
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any

import sympy

from devtools.audit_t007_consumers import Surd
from sqpack import retained_json
from sqpack.known_best import KNOWN_BEST_CORPUS

ROOT = Path(__file__).resolve().parents[1]
FRONTIER = ROOT / "frontier"
RESULT = (
    ROOT
    / "campaign"
    / "series"
    / "series-000-smoke-and-calibration"
    / "results"
    / "piercing-lower-bounds.json"
)

SQRT2 = sympy.sqrt(2)
SQRT3 = sympy.sqrt(3)
#: Digits each bound is printed with, rounded down so a printed bound is still a bound.
DIGITS = 12


def surd(value: sympy.Expr) -> Surd:
    """`value` as an exact sum of rational multiples of square roots of integers.

    Every quantity this tool decides is one: the step points are rationals and
    `(√3/2)j + 2√2 - 1`, and `m`, `B` and the printed digits only scale and shift them.
    `radsimp` clears the radicals from denominators, so the expanded value is a sum whose
    terms are `1` or `√r` times a rational, and anything else is refused rather than
    decided in floating point.
    """
    expression = sympy.expand(sympy.radsimp(sympy.expand(sympy.sympify(value))))
    total = Surd()
    for summand in sympy.Add.make_args(expression):
        coefficient, term = summand.as_coeff_Mul()
        radicand = (
            term.base
            if isinstance(term, sympy.Pow) and term.exp == sympy.Rational(1, 2)
            else None
        )
        if not isinstance(coefficient, sympy.Rational) or not (
            term == 1 or isinstance(radicand, sympy.Integer)
        ):
            raise ArithmeticError(f"not an exact surd: {value}")
        part = Surd.rational(Fraction(int(coefficient.p), int(coefficient.q)))
        if isinstance(radicand, sympy.Integer):
            part *= Surd.root(int(radicand))
        total += part
    return total


def exact_sign(value: sympy.Expr) -> int:
    """The sign of `value`, exactly: square roots of distinct squarefree integers are
    linearly independent, so a nonzero sum is separated from zero by refining rational
    enclosures of its radicals (`Surd.sign`), with no tolerance anywhere."""
    return surd(value).sign()


def exact_floor(value: sympy.Expr) -> int:
    """`⌊value⌋` for an algebraic `value`, exactly (`Surd.floor`).

    Neither `sympy.floor` of an unevaluated sum of surds, which can round a value a
    billionth below an integer up to it, nor `nsimplify`, which decides at finite
    precision, is used: `5 - (√2 - 1)^170` is within `10^-64` of 5 and its floor is 4.
    """
    return surd(value).floor()


def m_of(x: sympy.Expr) -> int:
    """`⌊(2/√3)(x + 1 - 2√2)⌋`, the rows of the paper's lattice less two."""
    return exact_floor(2 / SQRT3 * (x + 1 - 2 * SQRT2))


def pierce_bound(x: sympy.Expr) -> int:
    """Theorem 7's bound on the piercing number of the unit squares in side `x`."""
    whole = exact_floor(x)
    rows = m_of(x) + 2
    base = whole * rows
    if exact_sign(x - whole - sympy.Rational(1, 2)) < 0:
        return base
    return base + rows // 2


@cache
def steps(limit: int) -> tuple[sympy.Expr, ...]:
    """Every point in `[2√2 - 1, limit]` where `B` can step, in increasing order.

    Below `2√2 - 1` the lattice has no row to stand on (`m < 0`), and the paper does not
    use the bound there.
    """
    start = 2 * SQRT2 - 1
    points: set[sympy.Expr] = set()
    for k in range(1, limit + 1):
        points.add(sympy.Integer(k))
        points.add(sympy.Rational(2 * k + 1, 2))
    j = 0
    while True:
        point = SQRT3 / 2 * j + start
        if exact_sign(point - limit) > 0:
            break
        points.add(point)
        j += 1
    inside = [
        point
        for point in points
        if exact_sign(point - start) >= 0 and exact_sign(point - limit) <= 0
    ]
    ordered = tuple(sorted(inside, key=lambda point: sympy.N(point, 50)))
    # The sort key is a decimal; the order it gives is then confirmed exactly.
    for left, right in itertools.pairwise(ordered):
        if exact_sign(right - left) <= 0:
            raise ArithmeticError(f"steps {left} and {right} are not strictly increasing")
    return ordered


@cache
def step_values(limit: int) -> tuple[tuple[sympy.Expr, int], ...]:
    """Each step and `B` at it, evaluated once: `B` is nondecreasing, so every case reads
    its bound from this one table rather than walking the steps again."""
    return tuple((point, pierce_bound(point)) for point in steps(limit))


def piercing_bound(n: int, limit: int = 40) -> sympy.Expr:
    """The largest `x` the paper proves `s(n) ≥ x` for: the first step with `B ≥ n`."""
    for point, value in step_values(limit):
        if value >= n:
            return point
    raise ValueError(f"n = {n}: no step of B up to {limit} reaches {n}")


def floor_decimal(value: sympy.Expr, digits: int = DIGITS) -> str:
    """`value` rounded down to `digits` significant digits, as the case records print."""
    if exact_sign(value) <= 0:
        raise ValueError(f"only positive values are printed: {value}")
    # A decimal guess at the magnitude, then corrected exactly: 10^magnitude <= value.
    magnitude = math.floor(math.log10(float(sympy.N(value, 30))))
    while exact_sign(value - sympy.Integer(10) ** magnitude) < 0:
        magnitude -= 1
    while exact_sign(value - sympy.Integer(10) ** (magnitude + 1)) >= 0:
        magnitude += 1
    scale = digits - 1 - magnitude
    floored = exact_floor(value * sympy.Integer(10) ** scale)
    return format(Decimal(floored).scaleb(-scale).normalize(), "f")


def verified_floor(n: int) -> Decimal:
    """The case record's verified lower bound, exactly as the record prints it.

    Until 2026-10-04 this was a float, and the two comparisons in `survey` were float
    comparisons; both are now exact on the printed decimals.
    """
    text = (FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
    front = text.split("---", 2)[1]
    block = front.split("verified_lower_bound:", 1)[1]
    value = block.split("value:", 1)[1].splitlines()[0].strip().strip("'\"")
    try:
        floor = Decimal(value)
    except InvalidOperation as error:
        raise ValueError(f"n = {n}: verified lower bound {value!r} is not a decimal") from error
    if not floor.is_finite():
        raise ValueError(f"n = {n}: verified lower bound {value!r} is not a finite decimal")
    return floor


def survey(numbers: Sequence[int]) -> dict[str, Any]:
    """Each case's piercing bound, and the cases where it beats the verified floor."""
    rows: list[dict[str, Any]] = []
    for n in numbers:
        bound = piercing_bound(n)
        floor = verified_floor(n)
        decimal = floor_decimal(bound)
        rows.append(
            {
                "n": n,
                "bound": str(bound),
                "decimal": decimal,
                "verified_lower": str(floor),
                # The record holds a value rounded down, so the bound holds the floor
                # where its own decimal, rounded down at DIGITS, is the record's, and
                # beats it where it is strictly above. Both are exact decimal comparisons.
                "holds": Decimal(decimal) == floor,
                "improves": Decimal(decimal) > floor,
            }
        )
    return {
        "source_key": "[Basic-Slivkova 2018]",
        "theorem": "Theorem 7 with Proposition 8",
        "cases": rows,
        "holds": [row["n"] for row in rows if row["holds"]],
        "improves": [row["n"] for row in rows if row["improves"]],
    }


def _text(record: dict[str, Any]) -> str:
    return retained_json.dumps(record, ensure_ascii=False)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--update", action="store_true", help="rewrite the retained record")
    mode.add_argument("--check", action="store_true", help="compare with the retained record")
    arguments = parser.parse_args(argv)
    record = survey(range(2, KNOWN_BEST_CORPUS.count + 1))
    text = _text(record)
    if arguments.update:
        RESULT.write_text(text, encoding="utf-8")
        print(f"wrote {RESULT.relative_to(ROOT.parent)}")
    elif arguments.check:
        if not RESULT.is_file() or RESULT.read_text(encoding="utf-8") != text:
            print(f"{RESULT.name} is stale; run with --update", file=sys.stderr)
            return 1
    print(
        f"piercing lower bounds checked for {len(record['cases'])} cases; holds the "
        f"verified floor at n = {record['holds']} and beats it at n = {record['improves']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
