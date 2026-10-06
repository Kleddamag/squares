#!/usr/bin/env python3
"""Machine-check Proposition 5.1 of Karakuş 2026: the strip measure gives a square more than 1.

Karakuş (arXiv:2609.37410v1, Section 5) fixes `a >= 2`, `b >= 3`, `R = [0, a] x [0, b]`
and the measure `mu` with area density 1 on `H = [0, a] x [1, b - 1]`, line density 1/2 on
`L- = [0, a] x {1}` and `L+ = [0, a] x {b - 1}`, and mass 1/2 at each point of
`W = {(j, 4/5), (j, b - 4/5) : j = 1, ..., ceil(a) - 1}`. Proposition 5.1: every closed
square `S` in `R` of side `1 < lambda <= 101/100` has `mu(S°) > 1`. With the total
`mu(R) = ab - (a + 1 - ceil a)` it gives Theorem 1.1 and so `T-083` and the lower half of
`T-084`. The paper proves it by hand; this program decides it by an exact branch and bound
over the square's pose, written from the paper's Section 5 and nothing else (the source
publishes no code).

It confirms Proposition 5.1's statement by its own decomposition, not the paper's proof of
it. The paper splits by the height of the square's centre and uses Lemma 5.2 and (5.8);
this program splits by which strip lines meet the open square and never evaluates Lemma
5.2, which, with the paper's three strip cases, remains read and is not load-bearing here.

**Reduction to the vertical profile.** A square's
pose is its orientation `theta`, its side `lambda` and the height `z0` of its lowest
vertex; `S° lies in (0, a) x (0, b)`, so `S°` meets `L-` in its whole open chord at
`y = 1`, and its area in `H` is its area between `y = 1` and `y = b - 1`. The open chord
at `y = 4/5` is an interval inside `(0, a)`; when it is longer than one it contains an
integer `j` with `1 <= j <= ceil(a) - 1`, so a point of `W`. Hence

    mu(S°) >= F = area(S between 1 and b - 1) + 1/2 l(1) + 1/2 l(b - 1)
                  + 1/2 [l(4/5) > 1] + 1/2 [l(b - 4/5) > 1],

where `l(y)` is the length of the open chord at height `y`: a function of the vertical
profile alone, which depends on `theta` only through `m = min(cos, sin)`,
`M = max(cos, sin)`, `p = mM` and `h = m + M`, so `theta` ranges over `[0, pi/4]`.
Measured from the lowest vertex, the chord is `w(v) = min(v/p, lambda/M, (lambda h - v)/p)`
on `0 < v < lambda h` and zero elsewhere (it is zero on a tangent line, where the open
square misses the line), and for `lambda > 1` it exceeds one exactly when
`p < v < lambda h - p`, since `lambda/M >= lambda > 1`. Write `C(v)` for the area below
relative height `v` and `E(v) = -C(v) + w(v)/2`. Which lines cut `S°` splits the poses:

- *neither line cuts*: `S` lies in `H` and `F >= lambda^2 > 1`;
- *only `y = 1` cuts*, at relative height `0 < u <= 1` (`u <= 1` is `z0 >= 0`): then
  `F = lambda^2 + E(u) + 1/2 [p < u - 1/5 < lambda h - p]`. **Part A** decides `F > 1`.
- *only `y = b - 1` cuts*: the reflection `y -> b - y` maps `R` and `mu` to themselves and
  this case to the previous one (the top `<= b` is `u <= 1` there);
- *both cut*: since `b - 2 >= 1`, both cut heights lie within `lambda h - 1 <= 3/7` of
  the square's ends, and the central symmetry of `S` gives
  `F >= lambda^2 + E(u1) + E(lambda h - u2)`. **Part B** decides `E(v) >= 0` for
  `0 < v <= 3/7`, so `F >= lambda^2 > 1`. This is where `lambda <= 101/100` is used:
  `(1 + 3/7)^2 >= 2 (101/100)^2` is checked exactly.

Theorem 1.1 then follows by Karakuş's scale-and-sum, which is also by hand: a packing of
`M` unit squares in an `a' x b'` rectangle, `a' < a`, `b' < b`, scaled by some
`1 < lambda <= 101/100` with `lambda a' < a` and `lambda b' < b`, has disjoint open squares
in `R`, so `M < sum mu(S_i°) <= mu(R)`.

**The cells.** On `[0, lambda m]` (L), `[lambda m, lambda M]` (P) and
`[lambda M, lambda h]` (T) the profile is linear and

    E_L = v (1 - v) / (2p),   E_P = (lambda/M)(1/2 - v + lambda m/2),
    E_T = (g^2 + g)/(2p) - lambda^2,  g = lambda h - v.

`check_identities` derives them with sympy from the profile, with every other identity
the decisions use.

**Arithmetic and boxes.** The orientation is `theta = 2 atan(tau)`,
`cos = (1 - tau^2)/(1 + tau^2)`, `sin = 2 tau/(1 + tau^2)`, so a rational `tau` gives an
exact rational square; `tau` runs over `[0, 5/12]`, which contains `tan(pi/8)`. On
`[0, sqrt 2 - 1]` the quantities `m`, `p`, `h` increase and `M` decreases in `tau`, and
past it they turn (`m` and `M` swap), so a `tau` interval's enclosures are its endpoint
values, or the endpoint values and `1/sqrt 2`, `1/2`, `sqrt 2` (by rational bounds) when
it contains `sqrt 2 - 1`; `check_identities` verifies the derivative signs this uses.
Every bound below is a `Fraction`: nothing rounds and nothing floats.

A box is a product of closed intervals in `tau`, `lambda in [1, 101/100]` and the cut
height. For each cell the box may reach, the cell's `E` is bounded below over the box with
the cut height clamped to the cell; `E_lo` is the least of these, and `W_lo` is 1 when
`p < u - 1/5 < lambda h - p` holds over the whole box. Including `lambda = 1` in a box is
sound because every bound used holds at each `lambda > 1` of the box. A box is discharged
by the first rule that holds:

- *margin*: `lambda_lo^2 + E_lo + W_lo/2 > 1`, so `F > 1`;
- *area*: `E_lo + W_lo/2 >= 0`, so `F >= lambda^2 > 1`;
- *corner* (part A, only inside `tau <= 5/384`, `u >= 63/64`): the box reaches no cell L,
  `W = 1` throughout and `u <= 1`. There `F - 1 = Phi + (lambda/M)(1 - u)` in cell P,
  with `2M Phi = (h - 1) + delta (4M + 2m - 1) + delta^2 (2M + m)`, `lambda = 1 + delta`;
  and in cell T, `2p (F - 1) >= (h - 1)^2/2 + delta h (h (2 + delta) - 1)`. Both are
  positive for `delta > 0`. This is where the bound is tight: at `theta = 0`, `u = 1`,
  `F - 1 = (lambda - 1)(lambda + 1/2)` vanishes with `lambda - 1`, so no box containing
  that pose can be closed by enclosures alone.

Otherwise the box is bisected across its widest side relative to the root, the first such
side on a tie, so the cover is a deterministic binary tree. The certificate is that tree
in preorder, one character per node (`S` split, `m` margin, `a` area, `c` corner), which
`verify_tree` walks from the root again, recomputing every box and re-deciding every leaf
by its named rule. Part B's tree is the single leaf `a`.

**Controls.** Three mutations of the measure must be refused, each with an exact witness
pose whose `F` is at most one under the mutation and above one under Karakuş's measure:
point mass 49/100, line density 49/100, and the point rows at height 3/5. The certifier
also confirms the closed-form profile against exact polygon geometry at fixed rational
poses (`profile_spot_checks`).

**What is decided, and what is read.** The trees decide two inequalities, which the
receipt records as `decides`: part A, `lambda^2 + E(u) + 1/2 [p < u - 1/5 < lambda h - p] > 1`
for `lambda > 1` and `0 < u <= 1`; and part B, `E(v) >= 0` for `0 < v <= 3/7`. Everything
that turns them into the register's claims is read, not machine-checked, and the receipt
lists it as `premises`:

1. the closed form (5.3) as the tilted square's chord function, which
   `profile_spot_checks` confirms exactly at 212 poses and the test at 195 more;
2. `mu(S°) >= F`: the open square lies in `(0, a) x (0, b)`, and an open interval longer
   than one inside `(0, a)` holds an integer `1 <= j <= ceil(a) - 1`;
3. the four-way split by which strip lines meet the open square (it is connected), the
   reflection `y -> b - y`, and the central symmetry `C(lambda h - x) = lambda^2 - C(x)`,
   `w(lambda h - x) = w(x)`;
4. the soundness of the rules as coded, a review obligation, which the test samples
   against exact geometry and against a deliberately unsound rule;
5. Theorem 1.1's scale-and-sum: additivity over disjoint open squares, and
   `mu(R) = ab - Delta(a)`;
6. for `T-083`, Corollary 6.2's step from `nu(t, t) < N` to `s(N) >= t`;
7. for `T-084`, Corollary 6.1 at `a = b = k >= 3`, where `Delta(k) = 1`.

The program also restates Corollary 6.2's algebra at every nonsquare `8 <= N <= 324`:
`t = 1/2 + sqrt(N - k + 1/4)` has `k < t <= k + 1` and `t >= 3`, and the sympy identity
gives `t^2 - Delta(t) = N`. Given `k = floor(sqrt N)` the two inequalities hold for every
nonsquare `N >= 8`, so they guard the transcription and carry no evidence beyond that
identity (the lesson of D-518); that the case records state these values is
`devtools.check_nagamochi_bounds`'s.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m \\
        devtools.check_karakus_strip_measure [--update]

Without `--update` it replays the retained certificate (walks both trees and re-decides
every leaf), reruns the search and every other check, and compares everything with the
retained receipt; with it, it searches, re-decides the fresh trees and writes the receipt.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from collections import Counter
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
RECEIPT = (
    ROOT
    / "campaign/series/series-000-smoke-and-calibration/results/karakus-strip-measure"
    / "receipt.json"
)
SCHEMA = "karakus-strip-measure/1"
BEAD = "think-dw1o"

#: The square's orientation is `theta = 2 atan(tau)`; `5/12 > tan(pi/8) = sqrt 2 - 1`.
TAU_MAX = Fraction(5, 12)
LAMBDA_MIN = Fraction(1)
#: Proposition 5.1's ceiling on the side, `lambda <= 101/100`.
LAMBDA_MAX = Fraction(101, 100)
#: Part A's cut heights: `0 < u <= 1` is `z0 >= 0`.
PART_A_V = Fraction(1)
#: Part B's cut depths: at most `lambda h - 1 <= 101 sqrt 2/100 - 1 < 3/7`.
PART_B_V = Fraction(3, 7)
#: The corner box, where the corner rule may close a box: `tau <= TAU_MAX/32`, `u >= 63/64`.
CORNER_TAU = TAU_MAX / 32
CORNER_V = Fraction(63, 64)
SQRT2_LO = Fraction(14142135, 10**7)
SQRT2_HI = Fraction(14142136, 10**7)
#: A box that has not closed after this many bisections refuses the claim.
MAX_DEPTH = 60

#: What turns the two decided inequalities into the register's claims: read, not
#: machine-checked (the module statement's list, and the review of 2026-10-06).
PREMISES = (
    "The closed form (5.3) is the tilted square's chord function; spot-checked exactly.",
    (
        "mu(S°) >= F: the open square lies in (0, a) x (0, b), and an open interval longer "
        "than one inside (0, a) holds an integer 1 <= j <= ceil(a) - 1."
    ),
    (
        "The four-way split by which strip lines meet the connected open square, the "
        "reflection y -> b - y, and the central symmetry C(lambda h - x) = lambda^2 - C(x), "
        "w(lambda h - x) = w(x), which carry parts A and B to Proposition 5.1."
    ),
    (
        "The rules as coded are sound: a review obligation, sampled by the test against "
        "exact geometry and a deliberately unsound rule."
    ),
    (
        "Theorem 1.1's scale-and-sum: additivity over disjoint open squares, and "
        "mu(R) = ab - Delta(a)."
    ),
    "For T-083, Corollary 6.2's step from nu(t, t) < N to s(N) >= t.",
    "For T-084, Corollary 6.1 at a = b = k >= 3, where Delta(k) = 1.",
    (
        "Lemma 5.2, (5.8) and the paper's three strip cases are not used: this decomposition "
        "is the program's own, and they remain read."
    ),
)

HALF = Fraction(1, 2)
ZERO = Fraction(0)
ONE = Fraction(1)

Box = tuple[Fraction, Fraction, Fraction, Fraction, Fraction, Fraction]


class StripMeasureError(AssertionError):
    """A premise, identity, leaf or control that the check refutes."""


def _require(condition: bool, message: str) -> None:  # noqa: FBT001 -- an assertion helper
    if not condition:
        raise StripMeasureError(message)


@dataclass(frozen=True)
class Measure:
    """The strip measure's three weights, so that the controls can mutate them.

    `line` is the density on `y = 1`, `point` the mass of each point of `W`, and `offset`
    the depth of the point row below the line (`1/5`: the row is at `y = 4/5`).
    """

    line: Fraction = HALF
    point: Fraction = HALF
    offset: Fraction = Fraction(1, 5)


KARAKUS = Measure()


def _check_premises() -> None:
    _require(SQRT2_LO**2 < 2 < SQRT2_HI**2, "the rational bounds on sqrt 2 are wrong")
    _require(TAU_MAX**2 + 2 * TAU_MAX - 1 >= 0, "tau does not reach tan(pi/8)")
    _require(TAU_MAX < 1, "tau leaves [0, 1], where cos and sin are monotone")
    _require(
        (1 + PART_B_V) ** 2 >= 2 * LAMBDA_MAX**2,
        "part B's depth does not reach lambda h - 1 at the largest side",
    )


# -- the orientation's enclosures --------------------------------------------------------


def cos_sin(tau: Fraction) -> tuple[Fraction, Fraction]:
    """`cos theta` and `sin theta` at `theta = 2 atan(tau)`, exactly."""
    d = 1 + tau * tau
    return (1 - tau * tau) / d, 2 * tau / d


@dataclass(frozen=True)
class Orientation:
    """Enclosures of `m = min(c, s)`, `M = max(c, s)`, `p = cs`, `h = c + s` over tau."""

    m: tuple[Fraction, Fraction]
    big_m: tuple[Fraction, Fraction]
    p: tuple[Fraction, Fraction]
    h: tuple[Fraction, Fraction]


def orientation(t0: Fraction, t1: Fraction) -> Orientation:
    """Exact enclosures over `[t0, t1]`, from monotonicity on each side of `sqrt 2 - 1`.

    `tau^2 + 2 tau - 1 <= 0` is `tau <= sqrt 2 - 1`. Before it `m = s` and `p`, `h` rise
    while `M = c` falls; after it `m = c` and `p`, `h` fall while `M = s` rises.
    """
    c0, s0 = cos_sin(t0)
    c1, s1 = cos_sin(t1)
    p0, p1 = c0 * s0, c1 * s1
    h0, h1 = c0 + s0, c1 + s1
    if t1 * t1 + 2 * t1 - 1 <= 0:
        return Orientation((s0, s1), (c1, c0), (p0, p1), (h0, h1))
    if t0 * t0 + 2 * t0 - 1 >= 0:
        return Orientation((c1, c0), (s0, s1), (p1, p0), (h1, h0))
    return Orientation(
        (min(s0, c1), SQRT2_HI / 2),
        (SQRT2_LO / 2, max(c0, s1)),
        (min(p0, p1), HALF),
        (min(h0, h1), SQRT2_HI),
    )


# -- lower bounds over a box -------------------------------------------------------------


@dataclass(frozen=True)
class Bounds:
    e_lo: Fraction
    w_lo: int
    cells: frozenset[str]


def gain_lower(o: Orientation, box: Box, measure: Measure) -> tuple[Fraction, frozenset[str]]:
    """A lower bound on `E(v) = -C(v) + line * w(v)` over the box, and the cells it reaches."""
    _, _, l0, l1, v0, v1 = box
    m0, m1 = o.m
    big0, big1 = o.big_m
    p0, p1 = o.p
    h0, h1 = o.h
    alpha = measure.line
    bounds: list[Fraction] = []
    cells: set[str] = set()
    if v0 <= l1 * m1:
        # Cell L: E = v (2 alpha - v) / (2p), concave in v.
        cells.add("L")
        hi = min(v1, l1 * m1)
        if v0 >= 0 and 2 * alpha - hi >= 0:
            bounds.append(v0 * (2 * alpha - hi) / (2 * p1))
        else:
            num = min(v0 * (2 * alpha - v0), hi * (2 * alpha - hi))
            if num >= 0:
                bounds.append(num / (2 * p1))
            elif p0 > 0:
                bounds.append(num / (2 * p0))
            else:
                bounds.append(Fraction(-(10**9)))
    if v1 >= l0 * m0 and v0 <= l1 * big1:
        # Cell P: E = (lambda/M)(alpha - v + lambda m / 2).
        cells.add("P")
        x = alpha - min(v1, l1 * big1) + l0 * m0 / 2
        bounds.append(l0 / big1 * x if x >= 0 else l1 / big0 * x)
    if v1 >= l0 * big0 and v0 <= l1 * h1:
        # Cell T: E = (g^2 + 2 alpha g) / (2p) - lambda^2, g = lambda h - v >= 0.
        cells.add("T")
        g = max(ZERO, l0 * h0 - min(v1, l1 * h1))
        bounds.append((g * g + 2 * alpha * g) / (2 * p1) - l1 * l1)
    _require(bool(bounds), f"box {box} reaches no cell")
    return min(bounds), frozenset(cells)


def row_lower(o: Orientation, box: Box, measure: Measure) -> int:
    """1 when the open chord at the point row is longer than one over the whole box."""
    _, _, l0, _, v0, v1 = box
    p1 = o.p[1]
    return int(p1 < v0 - measure.offset and v1 - measure.offset < l0 * o.h[0] - p1)


def bounds(box: Box, measure: Measure, *, rows: bool) -> tuple[Orientation, Bounds]:
    o = orientation(box[0], box[1])
    e_lo, cells = gain_lower(o, box, measure)
    w_lo = row_lower(o, box, measure) if rows else 0
    return o, Bounds(e_lo, w_lo, cells)


def margin_rule(box: Box, b: Bounds, measure: Measure) -> bool:
    return box[2] * box[2] + b.e_lo + measure.point * b.w_lo > 1


def area_rule(b: Bounds, measure: Measure) -> bool:
    return b.e_lo + measure.point * b.w_lo >= 0


def in_corner(box: Box) -> bool:
    return box[1] <= CORNER_TAU and box[4] >= CORNER_V


@dataclass(frozen=True)
class CornerBounds:
    """Lower bounds over a box on the corner rule's coefficients (see `corner_rule`)."""

    k0: Fraction
    k1: Fraction
    q0: Fraction
    bracket: Fraction
    t1: Fraction


def corner_bounds(o: Orientation, measure: Measure) -> CornerBounds:
    """`K0`, `K1`, `q = h - 1`, `point q + 2 line + 2 point - 2` and `T1`, bounded below."""
    alpha, beta = measure.line, measure.point
    m0 = o.m[0]
    big0, big1 = o.big_m
    h0 = o.h[0]
    q0 = h0 - 1
    return CornerBounds(
        k0=(2 * beta - 1) * (big0 if 2 * beta - 1 >= 0 else big1) + h0 + 2 * alpha - 2,
        k1=2 * (2 * big0 + m0) + 2 * alpha - 2,
        q0=q0,
        bracket=beta * q0 + 2 * alpha + 2 * beta - 2,
        t1=2 * h0 * (q0 + alpha),
    )


def corner_rule(o: Orientation, box: Box, b: Bounds, measure: Measure) -> bool:
    """`F > 1` for every `lambda > 1` of a box with `W = 1`, `u <= 1` and no cell L.

    Cell P: `F - 1 = Phi + (lambda/M)(1 - u)` and, with `lambda = 1 + delta`,
    `2M Phi = K0 + K1 delta + K2 delta^2`, `K0 = (2 point - 1) M + h + 2 line - 2`,
    `K1 = 2(2M + m) + 2 line - 2`, `K2 = 2M + m`. Cell T: `g >= lambda h - 1 >= 0` and
    `2p (F - 1) >= T0 + T1 delta + T2 delta^2` with `q = h - 1`,
    `T0 = q (point q + 2 line + 2 point - 2)`, `T1 = 2h (q + line)`, `T2 = h^2`.
    `K0, T0 >= 0` and `K1, T1 > 0` make both positive for `delta > 0`.
    """
    if b.w_lo != 1 or box[5] > 1 or "L" in b.cells:
        return False
    c = corner_bounds(o, measure)
    if "P" in b.cells and (c.k0 < 0 or c.k1 <= 0):
        return False
    return not ("T" in b.cells and (c.q0 < 0 or c.bracket < 0 or c.t1 <= 0))


def decide(box: Box, part: str, measure: Measure) -> str | None:
    """The rule that closes the box, or None."""
    o, b = bounds(box, measure, rows=part == "A")
    if part == "A" and margin_rule(box, b, measure):
        return "m"
    if area_rule(b, measure):
        return "a"
    if part == "A" and in_corner(box) and corner_rule(o, box, b, measure):
        return "c"
    return None


# -- the cover ---------------------------------------------------------------------------


def root_box(part: str) -> Box:
    v_max = PART_A_V if part == "A" else PART_B_V
    return (ZERO, TAU_MAX, LAMBDA_MIN, LAMBDA_MAX, ZERO, v_max)


def split(box: Box, root: Box) -> tuple[Box, Box]:
    """Bisect the widest side relative to the root; the first such side on a tie."""
    t0, t1, l0, l1, v0, v1 = box
    widths = (
        (t1 - t0) / (root[1] - root[0]),
        (l1 - l0) / (root[3] - root[2]),
        (v1 - v0) / (root[5] - root[4]),
    )
    k = widths.index(max(widths))
    if k == 0:
        mid = (t0 + t1) / 2
        return (t0, mid, l0, l1, v0, v1), (mid, t1, l0, l1, v0, v1)
    if k == 1:
        mid = (l0 + l1) / 2
        return (t0, t1, l0, mid, v0, v1), (t0, t1, mid, l1, v0, v1)
    mid = (v0 + v1) / 2
    return (t0, t1, l0, l1, v0, mid), (t0, t1, l0, l1, mid, v1)


@dataclass(frozen=True)
class Cover:
    part: str
    tree: str
    max_depth: int

    def summary(self) -> dict[str, Any]:
        counts = Counter(self.tree)
        return {
            "nodes": len(self.tree),
            "leaves": len(self.tree) - counts["S"],
            "by_rule": {
                name: counts[code]
                for code, name in (("m", "margin"), ("a", "area"), ("c", "corner"))
                if counts[code]
            },
            "max_depth": self.max_depth,
            "tree": self.tree,
        }


@dataclass(frozen=True)
class Refusal:
    """A box that would not close, and, when its centre already scores at most one, that
    pose and its exact value: a counterexample to the claim for the measure searched."""

    part: str
    box: Box
    witness: tuple[Fraction, Fraction, Fraction] | None = None
    value: Fraction | None = None


def _centre_violation(
    box: Box, measure: Measure
) -> tuple[tuple[Fraction, Fraction, Fraction], Fraction] | None:
    """The box's centre pose and its `F`, when `F <= 1` there (part A's poses only)."""
    pose = ((box[0] + box[1]) / 2, (box[2] + box[3]) / 2, (box[4] + box[5]) / 2)
    if pose[1] <= 1 or pose[2] <= 0:
        return None
    value = point_value(*pose, measure)
    return (pose, value) if value <= 1 else None


def search(
    part: str, measure: Measure = KARAKUS, max_depth: int = MAX_DEPTH
) -> Cover | Refusal:
    """Depth-first branch and bound; the first box that will not close refuses the claim.

    Before a part-A box is split, its centre is scored exactly; a centre at or below one
    refuses at once, with that pose as the counterexample.
    """
    root = root_box(part)
    out: list[str] = []
    deepest = 0
    stack: list[tuple[Box, int]] = [(root, 0)]
    while stack:
        box, depth = stack.pop()
        deepest = max(deepest, depth)
        rule = decide(box, part, measure)
        if rule is not None:
            out.append(rule)
            continue
        if part == "A" and (found := _centre_violation(box, measure)) is not None:
            return Refusal(part, box, *found)
        if depth >= max_depth:
            return Refusal(part, box)
        out.append("S")
        low, high = split(box, root)
        stack.append((high, depth + 1))
        stack.append((low, depth + 1))
    return Cover(part, "".join(out), deepest)


def walk_tree(part: str, tree: str) -> Iterator[tuple[str, Box]]:
    """Each node of a preorder tree with the box it stands for, rebuilt from the root.

    The walk is iterative, so it holds one pending box per open level; the tree must end
    exactly where the cover does.
    """
    root = root_box(part)
    position = 0
    pending: list[Box] = [root]
    while pending:
        box = pending.pop()
        _require(position < len(tree), f"part {part}: the tree ends before the cover does")
        code = tree[position]
        position += 1
        yield code, box
        if code == "S":
            low, high = split(box, root)
            pending.append(high)
            pending.append(low)
    _require(position == len(tree), f"part {part}: the tree runs past the cover")


def leaf_holds(part: str, code: str, box: Box, measure: Measure = KARAKUS) -> bool:
    """Whether the leaf closes by the rule its code names."""
    o, b = bounds(box, measure, rows=part == "A")
    if code == "m":
        return part == "A" and margin_rule(box, b, measure)
    if code == "a":
        return area_rule(b, measure)
    if code == "c":
        return part == "A" and in_corner(box) and corner_rule(o, box, b, measure)
    message = f"part {part}: unknown leaf code {code!r}"
    raise StripMeasureError(message)


def verify_tree(part: str, tree: str, measure: Measure = KARAKUS) -> Counter[str]:
    """Walk a preorder tree from the root box again and re-decide every leaf by its rule."""
    seen: Counter[str] = Counter()
    for code, box in walk_tree(part, tree):
        seen[code] += 1
        if code != "S":
            _require(
                leaf_holds(part, code, box, measure),
                f"part {part}: leaf {box} does not close by rule {code!r}",
            )
    return seen


# -- exact point values, for the controls and the spot checks ----------------------------


def point_value(tau: Fraction, lam: Fraction, u: Fraction, measure: Measure) -> Fraction:
    """`F = lambda^2 + E(u) + point [p < u - offset < lambda h - p]`, exactly, at one pose."""
    c, s = cos_sin(tau)
    m, big, p, h = min(c, s), max(c, s), c * s, c + s
    _require(0 < u < lam * h, "the cut must be strictly inside the square")
    area, chord = profile(m, big, lam, u)
    r = u - measure.offset
    row = int(p < r < lam * h - p)
    return lam * lam - area + measure.line * chord + measure.point * row


def profile(
    m: Fraction, big: Fraction, lam: Fraction, v: Fraction
) -> tuple[Fraction, Fraction]:
    """`C(v)` and `w(v)` from the closed form (5.3) and its integral, at `0 < v < lambda h`."""
    p, h = m * big, m + big
    if v <= lam * m:
        return v * v / (2 * p), v / p
    if v <= lam * big:
        return lam / big * (v - lam * m / 2), lam / big
    g = lam * h - v
    return lam * lam - g * g / (2 * p), g / p


def square_vertices(tau: Fraction, lam: Fraction) -> tuple[tuple[Fraction, Fraction], ...]:
    """The square of side `lambda` at `theta = 2 atan(tau)`, lowest vertex at the origin."""
    c, s = cos_sin(tau)
    return (
        (ZERO, ZERO),
        (lam * c, lam * s),
        (lam * (c - s), lam * (s + c)),
        (-lam * s, lam * c),
    )


def _polygon_below(
    vertices: tuple[tuple[Fraction, Fraction], ...], y: Fraction
) -> tuple[Fraction, Fraction]:
    """Area of the convex polygon below `y`, and the length of its chord at `y`, exactly."""
    clipped: list[tuple[Fraction, Fraction]] = []
    on_line: list[Fraction] = []
    n = len(vertices)
    for i in range(n):
        (x1, y1), (x2, y2) = vertices[i], vertices[(i + 1) % n]
        if y1 <= y:
            clipped.append((x1, y1))
        if y1 == y:
            on_line.append(x1)
        if (y1 - y) * (y2 - y) < 0:
            x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            clipped.append((x, y))
            on_line.append(x)
    twice = sum(
        (
            clipped[i][0] * clipped[(i + 1) % len(clipped)][1]
            - clipped[(i + 1) % len(clipped)][0] * clipped[i][1]
            for i in range(len(clipped))
        ),
        ZERO,
    )
    chord = max(on_line) - min(on_line) if on_line else ZERO
    return abs(twice) / 2, chord


def spot_poses() -> Iterator[tuple[Fraction, Fraction, Fraction]]:
    """Fixed rational poses across every cell, both sides of `tan(pi/8)` and both lambdas."""
    for tau in (
        Fraction(1, 97),
        Fraction(1, 9),
        Fraction(2, 7),
        Fraction(2, 5),
        Fraction(5, 12),
    ):
        for lam in (Fraction(1001, 1000), LAMBDA_MAX):
            for k in range(1, 24):
                yield tau, lam, Fraction(k, 17)


def profile_spot_checks() -> int:
    """The closed form against exact polygon geometry, and the row rule against the chord.

    The poses must reach all three cells, both sides of `pi/4` and both row outcomes, so
    that a narrower set cannot pass unnoticed.
    """
    checked = 0
    reached: Counter[str] = Counter()
    for tau, lam, v in spot_poses():
        c, s = cos_sin(tau)
        _require(c * c + s * s == 1, f"tau={tau}: not a rotation")
        m, big = min(c, s), max(c, s)
        if not 0 < v < lam * (m + big):
            continue
        area, chord = _polygon_below(square_vertices(tau, lam), v)
        _require(
            profile(m, big, lam, v) == (area, chord),
            f"tau={tau}, lambda={lam}, v={v}: the closed form disagrees with the polygon",
        )
        p, h = m * big, m + big
        _require(
            (chord > 1) == (p < v < lam * h - p),
            f"tau={tau}, lambda={lam}, v={v}: the row rule disagrees with the chord",
        )
        reached["L" if v <= lam * m else "P" if v <= lam * big else "T"] += 1
        reached[f"row {chord > 1}"] += 1
        reached[f"past pi/4 {s > c}"] += 1
        checked += 1
    for key in ("L", "P", "T", "row True", "row False", "past pi/4 True", "past pi/4 False"):
        _require(reached[key] > 0, f"the spot checks never reach {key}")
    return checked


# -- identities ----------------------------------------------------------------------------


def check_identities() -> list[str]:
    """Every algebraic identity the rules use, by sympy, with what it establishes."""
    import sympy as sp  # noqa: PLC0415 -- only this check needs the symbolic extra

    m, big, lam, v, t, d, alpha, beta, tau = sp.symbols(
        "m M lambda v t delta alpha beta tau", positive=True
    )
    p, h = m * big, m + big
    checked: list[str] = []

    def zero(expr: Any, name: str) -> None:
        _require(sp.expand(sp.numer(sp.together(expr))) == 0, f"identity fails: {name}")
        checked.append(name)

    c_l = sp.integrate(t / p, (t, 0, v))
    zero(c_l - v**2 / (2 * p), "C_L is the integral of v/p")
    c_p = c_l.subs(v, lam * m) + sp.integrate(lam / big, (t, lam * m, v))
    zero(c_p - lam / big * (v - lam * m / 2), "C_P continues C_L along the plateau lambda/M")
    c_t = c_p.subs(v, lam * big) + sp.integrate((lam * h - t) / p, (t, lam * big, v))
    zero(c_t - (lam**2 - (lam * h - v) ** 2 / (2 * p)), "C_T continues C_P to lambda^2")
    zero((lam * m / p) - lam / big, "the profile is continuous at lambda m")
    zero((lam * h - lam * big) / p - lam / big, "the profile is continuous at lambda M")
    g = lam * h - v
    zero(-c_l + alpha * v / p - v * (2 * alpha - v) / (2 * p), "E_L")
    zero(-c_p + alpha * lam / big - lam / big * (alpha - v + lam * m / 2), "E_P")
    zero(-c_t + alpha * g / p - ((g**2 + 2 * alpha * g) / (2 * p) - lam**2), "E_T")
    # The corner rule, cell P.
    phi = lam**2 - 1 + beta + lam / big * (alpha - 1 + lam * m / 2)
    zero(
        lam**2 - 1 + beta + lam / big * (alpha - v + lam * m / 2) - (phi + lam / big * (1 - v)),
        "cell P: F - 1 = Phi + (lambda/M)(1 - u)",
    )
    k0 = (2 * beta - 1) * big + h + 2 * alpha - 2
    k1 = 2 * (2 * big + m) + 2 * alpha - 2
    k2 = 2 * big + m
    zero((2 * big * phi).subs(lam, 1 + d) - (k0 + k1 * d + k2 * d**2), "cell P: 2M Phi")
    # The corner rule, cell T; 2p = h^2 - 1 is m^2 + M^2 = 1.
    hh = sp.symbols("h", positive=True)
    q = hh - 1
    g0 = (1 + d) * hh - 1
    two_p = hh**2 - 1
    t0 = q * (beta * q + 2 * alpha + 2 * beta - 2)
    zero(
        g0**2
        + 2 * alpha * g0
        - (1 - beta) * two_p
        - (t0 + 2 * hh * (q + alpha) * d + hh**2 * d**2),
        "cell T: 2p (F - 1) at g = lambda h - 1",
    )
    zero(
        lam**2
        + (g**2 + 2 * alpha * g) / (2 * p)
        - lam**2
        + beta
        - 1
        - (g**2 + 2 * alpha * g - 2 * p * (1 - beta)) / (2 * p),
        "cell T: F - 1 = (g^2 + 2 line g - 2p (1 - point)) / (2p)",
    )
    zero(2 * m * big - ((m + big) ** 2 - (m**2 + big**2)), "2p = h^2 - (m^2 + M^2)")
    # The orientation's parametrization and its monotone pieces.
    c = (1 - tau**2) / (1 + tau**2)
    s = 2 * tau / (1 + tau**2)
    zero(c**2 + s**2 - 1, "(cos, sin) is a rotation")
    zero(sp.diff(c, tau) * (1 + tau**2) ** 2 + 4 * tau, "cos falls on tau > 0")
    zero(sp.diff(s, tau) * (1 + tau**2) ** 2 - 2 * (1 - tau**2), "sin rises on [0, 1)")
    zero(
        sp.diff(c + s, tau) * (1 + tau**2) ** 2 + 2 * (tau**2 + 2 * tau - 1),
        "h rises exactly while tau^2 + 2 tau - 1 < 0",
    )
    zero(
        sp.diff(c * s, tau) * (1 + tau**2) ** 3
        - 2 * (tau**2 + 2 * tau - 1) * (tau**2 - 2 * tau - 1),
        "p rises exactly while tau^2 + 2 tau - 1 < 0 (tau^2 - 2 tau - 1 < 0 on [0, 1])",
    )
    zero(
        c - s - (1 - 2 * tau - tau**2) / (1 + tau**2),
        "cos >= sin exactly while tau^2 + 2 tau - 1 <= 0",
    )
    # Corollary 6.2's root: (t - 1/2)^2 = N - k + 1/4 gives t^2 - t + k = N.
    n, k = sp.symbols("N k", positive=True)
    root = sp.Rational(1, 2) + sp.sqrt(n - k + sp.Rational(1, 4))
    zero(root**2 - root + k - n, "Corollary 6.2: t^2 - (t - k) = N")
    return checked


# -- the corollaries' algebra ----------------------------------------------------------------


def corollary_checks() -> dict[str, Any]:
    """Corollary 6.2's algebra at every nonsquare `8 <= N <= 324`, and at `N = k^2 - 1`.

    With `k = floor(sqrt N)` and `q = N - k + 1/4`, `t = 1/2 + sqrt q`. `(k - 1/2)^2 < q <=
    (k + 1/2)^2` is `k < t <= k + 1`, so `Delta(t) = t - k`; `q >= 25/4` is `t >= 3`, so the
    square `[0, t]^2` meets `a >= 2`, `b >= 3`; and `t^2 - Delta(t) = N` is the identity
    `check_identities` verifies. At `N = k^2 - 1` the root is `k` exactly. These restate the
    algebra and cannot fail for a correct `k` (see the module statement).
    """
    general: list[int] = []
    for n in range(8, 325):
        k = math.isqrt(n)
        if k * k == n:
            continue
        q = Fraction(n - k) + Fraction(1, 4)
        _require((k - HALF) ** 2 < q <= (k + HALF) ** 2, f"N={n}: t is not in (k, k + 1]")
        _require(q >= Fraction(25, 4), f"N={n}: t < 3, below the measure's b >= 3")
        general.append(n)
    families: list[int] = []
    for k in range(3, 19):
        n = k * k - 1
        q = Fraction(n - (k - 1)) + Fraction(1, 4)
        _require(q == (k - HALF) ** 2, f"k={k}: Corollary 6.2 is not exactly k at k^2 - 1")
        families.append(n)
    return {
        "note": (
            "These restate the paper's algebra: given k = floor(sqrt N) they hold for every "
            "nonsquare N >= 8, and carry no evidence beyond the sympy identity "
            "t^2 - (t - k) = N. The case records' values are check_nagamochi_bounds's."
        ),
        "T-083": {"n_values": len(general), "first": general[0], "last": general[-1]},
        "T-084": {"n_values": families},
    }


# -- controls ---------------------------------------------------------------------------------


@dataclass(frozen=True)
class Control:
    name: str
    measure: Measure
    witness: tuple[Fraction, Fraction, Fraction]


#: Mutations of the measure, each with a pose the mutation scores at most one. The first two
#: are the axis-parallel square of side 1001/1000 on the floor; the third is tilted, with
#: its point row too low to catch.
CONTROLS = (
    Control(
        "point mass 49/100",
        Measure(point=Fraction(49, 100)),
        (ZERO, Fraction(1001, 1000), ONE),
    ),
    Control(
        "line density 49/100",
        Measure(line=Fraction(49, 100)),
        (ZERO, Fraction(1001, 1000), ONE),
    ),
    Control(
        "point rows at height 3/5",
        Measure(offset=Fraction(2, 5)),
        (Fraction(2, 5), Fraction(1001, 1000), Fraction(17, 20)),
    ),
)


def run_controls() -> list[dict[str, Any]]:
    """Each mutation is refused, and its witness scores at most one under it, above one here."""
    records: list[dict[str, Any]] = []
    for control in CONTROLS:
        outcome = search("A", control.measure)
        if not isinstance(outcome, Refusal):
            message = f"control {control.name}: the certifier accepted"
            raise StripMeasureError(message)
        found = None
        if outcome.witness is not None and outcome.value is not None:
            _require(
                outcome.value == point_value(*outcome.witness, control.measure) <= 1,
                f"control {control.name}: the search's counterexample does not score <= 1",
            )
            found = {
                "tau": str(outcome.witness[0]),
                "lambda": str(outcome.witness[1]),
                "u": str(outcome.witness[2]),
                "value": str(outcome.value),
            }
        tau, lam, u = control.witness
        mutated = point_value(tau, lam, u, control.measure)
        true = point_value(tau, lam, u, KARAKUS)
        _require(mutated <= 1, f"control {control.name}: the witness scores {mutated} > 1")
        _require(true > 1, f"control {control.name}: Karakuş's measure scores it {true} <= 1")
        records.append(
            {
                "name": control.name,
                "certifier": "refused",
                "found_by_search": found,
                "witness": {"tau": str(tau), "lambda": str(lam), "u": str(u)},
                "mutated_value": str(mutated),
                "karakus_value": str(true),
            }
        )
    return records


# -- driver -----------------------------------------------------------------------------------


def certify(*, verify: bool) -> dict[str, Any]:
    """Search both parts and run every other check; the receipt body.

    `verify` re-decides the fresh trees; a replay instead re-decides the retained ones and
    requires the fresh ones to equal them.
    """
    _check_premises()
    parts: dict[str, Any] = {}
    for part in ("A", "B"):
        outcome = search(part)
        if isinstance(outcome, Refusal):
            message = f"part {part}: the box {outcome.box} does not close"
            raise StripMeasureError(message)
        if verify:
            verify_tree(part, outcome.tree)
        parts[part] = outcome.summary()
    return {
        "schema": SCHEMA,
        "bead": BEAD,
        "source": "Karakuş 2026, arXiv:2609.37410v1, Section 5, Proposition 5.1",
        "statement": (
            "For a >= 2, b >= 3 and the strip measure mu, every closed square in "
            "[0, a] x [0, b] of side 1 < lambda <= 101/100 has mu(interior) > 1."
        ),
        "decides": {
            "part_A": (
                "lambda^2 + E(u) + 1/2 [p < u - 1/5 < lambda h - p] > 1 for every "
                "orientation, 1 < lambda <= 101/100 and 0 < u <= 1, where u is the height of "
                "y = 1 above the lowest vertex, E(v) = -C(v) + w(v)/2, C the area below and w "
                "the open chord at relative height v, m = min(cos, sin), M = max(cos, sin), "
                "p = mM and h = m + M"
            ),
            "part_B": "E(v) >= 0 for every orientation, 1 < lambda <= 101/100 and 0 < v <= 3/7",
        },
        "premises": list(PREMISES),
        "parameters": {
            "tau": ["0", str(TAU_MAX)],
            "lambda": [str(LAMBDA_MIN), str(LAMBDA_MAX)],
            "part_a_cut": ["0", str(PART_A_V)],
            "part_b_depth": ["0", str(PART_B_V)],
            "corner": {"tau_max": str(CORNER_TAU), "u_min": str(CORNER_V)},
            "line_density": str(KARAKUS.line),
            "point_mass": str(KARAKUS.point),
            "row_offset": str(KARAKUS.offset),
            "max_depth": MAX_DEPTH,
        },
        "parts": parts,
        "identities": check_identities(),
        "profile_spot_checks": profile_spot_checks(),
        "corollaries": corollary_checks(),
        "controls": run_controls(),
    }


def replay(receipt: dict[str, Any]) -> None:
    """Re-decide the retained trees leaf by leaf, independent of the search."""
    for part, record in receipt["parts"].items():
        seen = verify_tree(part, record["tree"])
        _require(sum(seen.values()) == record["nodes"], f"part {part}: node count differs")


VOLATILE = frozenset({"recorded_utc", "cpu_seconds"})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Machine-check Proposition 5.1 of Karakuş 2026 (the strip measure)."
    )
    parser.add_argument("--update", action="store_true", help="write the receipt")
    args = parser.parse_args(argv)
    started = time.process_time()
    retained: dict[str, Any] | None = None
    if not args.update:
        loaded: dict[str, Any] = json.loads(RECEIPT.read_text(encoding="utf-8"))
        replay(loaded)
        leaves = ", ".join(
            f"part {part} {record['leaves']} leaves" for part, record in loaded["parts"].items()
        )
        print(f"replayed the retained certificate, every leaf re-decided: {leaves}")
        retained = loaded
    body = certify(verify=retained is None)
    cpu = time.process_time() - started
    if retained is None:
        body["recorded_utc"] = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        body["cpu_seconds"] = round(cpu, 1)
        RECEIPT.parent.mkdir(parents=True, exist_ok=True)
        text = json.dumps(body, indent=2, ensure_ascii=False) + "\n"
        RECEIPT.write_text(text, encoding="utf-8")
        print(f"wrote {RECEIPT.relative_to(ROOT)}")
    else:
        stable = {key: value for key, value in retained.items() if key not in VOLATILE}
        _require(body == stable, "the fresh run differs from the retained receipt")
        print("the fresh search, identities, spot checks, corollaries and controls match it")
    a, b = body["parts"]["A"], body["parts"]["B"]
    print(
        f"Proposition 5.1: part A closed by {a['leaves']} leaves {a['by_rule']}, depth "
        f"{a['max_depth']}; part B by {b['leaves']} leaf; {len(body['identities'])} "
        f"identities, {body['profile_spot_checks']} spot checks, "
        f"{body['corollaries']['T-083']['n_values']} values of (6.1), "
        f"{len(body['controls'])} controls refused; {cpu:.1f}s CPU"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
