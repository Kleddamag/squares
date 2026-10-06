"""Interval re-check of the numerical chain behind Ryu's k^2 - M(k) >= 0.033 log k.

Sungjoon Ryu's preprint "Packing k^2 - c unit squares: s(k^2 - c) = k for all large k"
(version 1.1, retained in
``packing/resources/web/squarepacker-k2-minus-c-2026-10-05/k2-minus-c/paper/``) proves
its Theorem 1.1 with explicit constants. This module re-decides every numerical
inequality of the chain that turns the lemmas' stated inputs into the theorem's
constants: Lemma 4.13's ``A``, the numbers in the proofs of Lemmas 5.2 and 5.4 that give
``g0 = 0.49998``, the bracket ``< 30.147`` and the factor ``0.99977`` of Section 6, the
constant ``0.033`` for every ``k >= 2``, the formula for ``k >= 10^13``, the threshold
``log k > 120.24`` for ``c = 4`` of Remark 7.4, and the constant ``0.027`` of Remark 7.5,
which the analytic ``K_w = 13`` of Lemma 4.9 gives without the computer.

The inputs are read from the preprint's text, not from the author's ``verify_v10.py``:
the overlap bound (Lemmas 4.9 and 4.10), ``Q* = 0.32`` (Proposition 4.5), and the
parameters Sections 5 and 6 fix. A step whose quantities are rational is decided in
exact ``Fraction`` arithmetic; a step with a root, a logarithm or a trigonometric
function is decided on ``mpmath`` intervals at 60 significant digits, and holds only when
the intervals decide it. It checks the arithmetic of the chain, not the lemmas that
supply its inputs.

Run from ``packing/``::

    uv run --frozen --all-extras --group dev python -m \\
        cases.asymptotic.ryu_k2_minus_c_constants [--overlap 13] [--json OUT.json]
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath

#: mpmath's interval context. Its functions are attached at run time, so it is typed
#: as Any here.
iv: Any = mpmath.iv

#: Exact rationals, the short name the chain below is written in.
F = Fraction

DIGITS = 60

#: The constants the preprint states for each overlap bound: Lemma 4.10's
#: computer-assisted 9 (Theorem 1.1) and Lemma 4.9's analytic 13 (Remark 7.5), as
#: (A, bracket, kappa).
STATED: dict[int, tuple[str, str, str]] = {
    9: ("10.6067", "30.147", "0.033"),
    13: ("12.7476", "36.212", "0.027"),
}


@dataclass(frozen=True)
class Check:
    """One inequality of the chain, where the preprint states it, and its verdict."""

    name: str
    pinpoint: str
    holds: bool
    value: str


def _i(value: str | int | F):
    """The interval of a decimal string, an integer or a fraction."""
    if isinstance(value, F):
        return iv.mpf(value.numerator) / iv.mpf(value.denominator)
    return iv.mpf(value)


def _show(value) -> str:
    if isinstance(value, F):
        return f"{float(value):.12g} (exact {value})"
    return str(iv.nstr(value, 12))


def _below(lhs, rhs) -> bool:
    """Whether ``lhs < rhs``: exactly for fractions, for every point of intervals."""
    if isinstance(lhs, F) and isinstance(rhs, F):
        return lhs < rhs
    return bool((_promote(lhs) - _promote(rhs)).b < 0)


def _at_most(lhs, rhs) -> bool:
    if isinstance(lhs, F) and isinstance(rhs, F):
        return lhs <= rhs
    return bool((_promote(lhs) - _promote(rhs)).b <= 0)


def _promote(value):
    return _i(value) if isinstance(value, F) else value


def check_constants(
    overlap: int = 9,
    *,
    q_star: str = "0.32",
    a_bound: str | None = None,
    bracket_bound: str | None = None,
    kappa: str | None = None,
) -> tuple[Check, ...]:
    """Every inequality of the chain for the overlap bound ``overlap``.

    The stated ``A``, bracket and ``kappa`` default to the preprint's for 9 and 13; a
    caller may pass others, as the controls do, to see a check refuse them. The
    thresholds of Remarks 7.3 and 7.4 are checked for 9 only, where the preprint states
    them.
    """
    iv.dps = DIGITS
    stated = STATED.get(overlap, STATED[9])
    a_text, bracket_text, kappa_text = (
        a_bound or stated[0],
        bracket_bound or stated[1],
        kappa or stated[2],
    )
    checks: list[Check] = []

    def record(name: str, pinpoint: str, value, *, holds: bool) -> None:
        checks.append(Check(name, pinpoint, holds, _show(value)))

    q, k_w = F(q_star), F(overlap)
    theta_max, theta_1 = F("3e-6"), F("1e-5")
    c_col, delta, eps, omega_0, w_0 = F(2), F("1e-5"), F("2e-3"), F("2e-4"), F("1.08e-5")
    s_min, k_2 = F("7.9e5"), F(10) ** 13
    a_stated, bracket_stated, kappa_stated = F(a_text), F(bracket_text), F(kappa_text)
    lead, offset, g_0 = F("0.99977"), F("0.3819"), F("0.49998")
    sqrt2 = iv.sqrt(_i(2))
    c_line = 2 * sqrt2

    # Lemma 4.13: A := 4 sqrt(K/Q*)/(2 - 3e-6) < the stated bound, and A >= 2.
    a_value = 4 * iv.sqrt(_i(k_w / q)) / _i(2 - theta_max)
    record(
        f"A = 4 sqrt({overlap}/Q*)/(2 - 3e-6) < {a_text}",
        "Lemma 4.13",
        a_value,
        holds=_below(a_value, a_stated),
    )
    record("A >= 2", "Lemma 4.13, last step", a_value, holds=_at_most(F(2), a_value))
    margin = theta_1 * (2 - theta_1) / 40 - q * theta_max * (2 - theta_max) / 4
    record(
        "theta_1(2 - theta_1)/40 >= Q* theta_max(2 - theta_max)/4",
        "Lemma 4.13",
        margin,
        holds=margin >= 0,
    )

    # Lemma 5.2, at the least scale s = 7.9e5 and alpha = alpha(s) = 1/(Cs).
    alpha = 1 / (c_col * s_min)
    record(
        "alpha(s) = 1/(Cs) <= 6.33e-7 for s >= 7.9e5",
        "Lemma 5.2",
        alpha,
        holds=alpha <= F("6.33e-7"),
    )
    x = _i("1e-3")
    sec_ratio = (1 / iv.cos(x) - 1) / (x * x)
    record(
        "(sec x - 1)/x^2 <= 0.50001 at x = 1e-3",
        "Lemma 5.2",
        sec_ratio,
        holds=_at_most(sec_ratio, F("0.50001")),
    )
    drift = F("0.50001") * (1 + alpha / s_min) / (c_col**2 * s_min)
    record(
        "0.50001(1 + alpha/s)/(C^2 s) < 1.59e-7", "Lemma 5.2", drift, holds=drift < F("1.59e-7")
    )
    record(
        "delta + 1.59e-7 <= 1.0159e-5",
        "Lemma 5.2",
        delta + F("1.59e-7"),
        holds=delta + F("1.59e-7") <= F("1.0159e-5"),
    )
    upper_ramp = F("1.0159e-5") + F("6.33e-7")
    record(
        "1.0159e-5 + 6.33e-7 <= 1.0792e-5 < w_0 = 1.08e-5",
        "Lemma 5.2",
        upper_ramp,
        holds=upper_ramp <= F("1.0792e-5") < w_0,
    )
    alpha_max = _i("6.33e-7")
    gap = iv.cos(alpha_max) - iv.sin(alpha_max)
    record(
        "cos alpha - sin alpha > 1 - 6.4e-7",
        "Lemma 5.2",
        gap,
        holds=_below(1 - F("6.4e-7"), gap),
    )

    # Lemma 5.4: |B_Z| < 0.500018, so g_0 = 0.49998.
    tan_ratio = iv.tan(alpha_max) / alpha_max
    record(
        "tan alpha < 1.000001 alpha",
        "Lemma 5.4",
        tan_ratio,
        holds=_below(tan_ratio, F("1.000001")),
    )
    widen = F("3.02") * delta * F("1.000001")
    record("3.02 delta 1.000001 <= 3.04e-5", "Lemma 5.4", widen, holds=widen <= F("3.04e-5"))
    rho = iv.cos(alpha_max) + iv.sin(alpha_max)
    b_z = _i("2.01") * alpha_max + (1 + (alpha_max + rho) / _i(s_min)) * _i(
        1 + F("3.04e-5")
    ) / (_i(c_col) * gap)
    record(
        "|B_Z| <= 2.01 a + (1 + (a + rho)/s)(1 + 3.04e-5)/(C(cos a - sin a)) < 0.500018",
        "Lemma 5.4",
        b_z,
        holds=_below(b_z, F("0.500018")),
    )
    room = 1 - F("6.4e-7") - F("0.500018")
    record("1 - 6.4e-7 - 0.500018 > g_0 = 0.49998", "Lemma 5.4", room, holds=g_0 < room)

    # Section 6 at k = 10^13; each bound is monotone in k on k >= 10^13. y_0 = sqrt(k)/4.
    y_0 = iv.sqrt(_i(k_2)) / 4
    y_0_squared = k_2 / 16
    record(
        "y_0 = sqrt(k)/4 >= 790569 >= 7.9e5", "Section 6", y_0, holds=_at_most(F(790569), y_0)
    )
    alpha_line = 1 / (c_line * y_0)
    record(
        "alpha'(y_0) = 1/(C' y_0) <= 4.48e-7",
        "Section 6",
        alpha_line,
        holds=_at_most(alpha_line, F("4.48e-7")),
    )
    alpha_col = 1 / (_i(c_col) * y_0)
    record(
        "alpha(y_0) = 1/(C y_0) <= 6.33e-7",
        "Section 6",
        alpha_col,
        holds=_at_most(alpha_col, F("6.33e-7")),
    )
    record(
        "C'(1 - epsilon) > C",
        "Section 6",
        c_line * _i(1 - eps),
        holds=_below(c_col, c_line * _i(1 - eps)),
    )
    eta = F("0.50001") * (k_2 - 1) / (8 * y_0_squared)
    record(
        "eta(y) <= 0.50001 (k - 1)/(8 y_0^2) <= 1.00002",
        "Section 6",
        eta,
        holds=eta <= F("1.00002"),
    )
    eta_integral = F("0.50001") * k_2 / (8 * y_0_squared)
    record(
        "integral over H of eta dy/d(y) <= 0.50001 k/(8 y_0^2) = 1.00002",
        "Section 6",
        eta_integral,
        holds=eta_integral <= F("1.00002"),
    )
    two_log = 2 * iv.log(_i(2 * (1 - eps)))
    record(
        "2 log(2(1 - epsilon)) > 1.38229",
        "Section 6",
        two_log,
        holds=_below(F("1.38229"), two_log),
    )
    ratio = (1 - 6 / _i(k_2)) / (1 + 8 / iv.sqrt(_i(k_2)))
    record(
        "(1 - 6/k)/(1 + 8/sqrt k) > 1 - 2.6e-6 for k >= 10^13",
        "Section 6",
        ratio,
        holds=_below(1 - F("2.6e-6"), ratio),
    )
    shift = two_log + 2 * iv.log(_i(1 - F("2.6e-6")))
    record(
        "l(H) >= h_0 (log k + 1.38228)", "Section 6", shift, holds=_at_most(F("1.38228"), shift)
    )
    factor = (1 - omega_0) * (1 - 2 * w_0)
    record("(1 - omega_0) h_0 >= 0.99977", "Section 6", factor, holds=lead <= factor)
    terms_hold = (
        _at_most(1 / (_i(omega_0) * y_0), F("6.33e-3"))
        and _at_most(_i("2.01") / (_i(eps) * y_0), F("1.272e-3"))
        and _at_most(alpha_col / _i(delta), F("0.0633"))
    )
    record(
        "1/(omega_0 y_0) <= 6.33e-3, 2.01/(eps y_0) <= 1.272e-3, alpha(y_0)/delta <= 0.0633",
        "Section 6",
        alpha_col / _i(delta),
        holds=terms_hold,
    )
    bracket = (
        _i("6.33e-3")
        + (c_line / 2) * _i(a_stated)
        + _i(c_col * (1 + F("1.272e-3")))
        / (c_line * _i(g_0 * (1 - eps)))
        * _i(a_stated + F("0.0633"))
    )
    record(
        f"bracket with A < {a_text} is < {bracket_text}",
        "Section 6",
        bracket,
        holds=_below(bracket, bracket_stated),
    )
    shifted = lead * F("1.38228") - F("1.00002")
    record(
        "0.99977 * 1.38228 - 1.00002 >= 0.3819", "Section 6", shifted, holds=offset <= shifted
    )

    # Theorem 1.1: kappa for every k >= 2. Below 10^13 the trivial W >= 1 of Corollary
    # 3.3 carries it; from 10^13 the formula F(k) = (0.99977 log k + 0.3819)/bracket,
    # whose ratio to log k decreases to 0.99977/bracket as the offset is positive.
    log_k2 = iv.log(_i(k_2))
    record(
        f"for 2 <= k < 10^13: {kappa_text} log k < 1, the trivial W >= 1 of Corollary 3.3",
        "Section 6, first line",
        _i(kappa_stated) * log_k2,
        holds=_below(_i(kappa_stated) * log_k2, F(1)),
    )
    limit = lead / bracket_stated
    record(
        f"for k >= 10^13: F(k)/log k > 0.99977/{bracket_text} > {kappa_text}",
        "Section 6, Remark 7.3",
        limit,
        holds=kappa_stated < limit and offset > 0,
    )

    if overlap == 9:
        # Remarks 7.3 and 7.4, and the issue: s(k^2 - c) = k once F(k) > c, W being an
        # integer, so W >= c + 1 and c*(k) >= c.
        threshold_1 = _i((bracket_stated - offset) / lead)
        record(
            "F(k) > 1 already for log k > (bracket - 0.3819)/0.99977, below log 10^13",
            "Remark 7.3",
            threshold_1,
            holds=_below(threshold_1, log_k2),
        )
        threshold_4 = (4 * bracket_stated - offset) / lead
        record(
            "c = 4: F(k) > 4 for log k > (4 bracket - 0.3819)/0.99977, in (log 10^13, 120.24)",
            "Remark 7.4",
            threshold_4,
            holds=threshold_4 < F("120.24") and _below(log_k2, threshold_4),
        )
        slope = bracket_stated / lead
        record(
            "for c >= 2: (bracket c - 0.3819)/0.99977 <= 30.16 c - 0.38",
            "Remark 7.4",
            slope,
            holds=slope <= F("30.16") and -offset / lead <= F("-0.38"),
        )
    return tuple(checks)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument(
        "--overlap",
        type=int,
        choices=sorted(STATED),
        default=9,
        help="the overlap bound: 9 (Lemma 4.10) or 13 (Lemma 4.9)",
    )
    parser.add_argument("--json", type=Path, default=None, help="write the checks here")
    args = parser.parse_args(argv)
    checks = check_constants(args.overlap)
    for check in checks:
        verdict = "OK  " if check.holds else "FAIL"
        print(f"{verdict} [{check.pinpoint}] {check.name} ({check.value})")
    passed = all(check.holds for check in checks)
    print(
        f"{'ALL HOLD' if passed else 'SOME FAIL'}: {sum(c.holds for c in checks)}/{len(checks)}"
    )
    if args.json is not None:
        payload = {
            "overlap": args.overlap,
            "digits": DIGITS,
            "passed": passed,
            "checks": [asdict(check) for check in checks],
        }
        args.json.write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
