# Soundness of sqverify-fast

This is the proof obligation of the clean-room measure verifier: every lemma the code
relies on, stated and proved, with the code that discharges it.
It was derived from the mathematics of the net-and-shrink argument, not from any
checker’s source; [INDEPENDENCE.md](INDEPENDENCE.md) records what was read.

A verdict of `verified` for all directions of a net, together with the exact admission
premises, proves $s(n) \ge L$. Every other verdict proves nothing.

## The Claim

A certificate gives a side $L$, a shrunk side $B$, a net step $D$ and count $N_\theta$
(here $83/40000$ and $201$), and orbit representatives $R_j = [x_1, x_2] \times [y_1,
y_2]$ with weights $w_j \ge 0$, all exact rationals.
Its density is

$$
g = \sum_j \frac{w_j}{8 |R_j|} \sum_{S \in D_4} \mathbf 1_{S(R_j)},
$$

with $D_4$ the symmetry group of $K = [0, L]^2$. So $g \ge 0$, $g$ is $D_4$-invariant,
and $\int g = M = \sum_j w_j$.

**Theorem.** If $M < n$, $B(1 + D) < 1$, $t_{\max} = (N_\theta - 1) D$ satisfies
$t_{\max}^2 + 2 t_{\max} - 1 > 0$, and for every net index $r$ and every centre $c \in
[a_r, L - a_r]^2$ the closed square $Q_r(c)$ of side $B$, centre $c$ and angle $\theta_r
= 2 \arctan(rD)$ satisfies $\int_{Q_r(c)} g \ge 1$, where $a_r = B(\cos\theta_r +
\sin\theta_r)/2$, then $n$ unit squares do not pack in $K$; hence $s(n) \ge L$.

*Proof.*

1. *Net (N1).* With $t_r = rD$, $\tan\frac{\theta_{r+1} - \theta_r}{2} = \frac{D}{1 +
   t_r t_{r+1}} \le D$, so consecutive net angles differ by at most $2 \arctan D$, and
   every $\varphi \in [0, \theta_{N_\theta - 1}]$ is within $\arctan D$ of a net angle.
   The endpoint condition says $\tan(\theta_{\max}/2) > \sqrt 2 - 1 = \tan(\pi/8)$, so
   $\theta_{\max} > \pi/4$.

2. *Orientation (N2).* A unit square’s angle is defined modulo $\pi/2$; take $\varphi
   \in [0, \pi/2)$. If $\varphi > \theta_{\max}$, reflect the whole configuration in the
   diagonal $y = x$, which maps $K$ to itself, preserves $g$, preserves disjointness,
   and sends $\varphi$ to $\pi/2 - \varphi < \pi/4 < \theta_{\max}$. So assume
   $\varphi \le
   \theta_{\max}$, and let $\theta_r$ be a net angle with $\delta = |\varphi - \theta_r|
   \le \arctan D$.

3. *Shrink (N3).* The concentric square of side $B$ at angle $\theta_r$, seen in the
   unit square’s frame, is rotated by $\delta$; its extent along either of the unit
   square’s axes is
   $B(\cos\delta + \sin\delta) = B \cos\delta (1 + \tan\delta) \le B(1 +
   D) < 1$. So it lies in the open unit square, hence in $K$, and its centre lies in
   $[a_r, L - a_r]^2$, the set of centres whose $B$-square at angle $\theta_r$ lies in
   $K$.

4. *Counting (N4).* The $n$ unit squares have disjoint interiors, so their $B$-squares
   are pairwise disjoint closed sets in $K$. With $g \ge 0$, $n \le \sum_i \int_{Q_i} g
   \le \int_K g \le M < n$, a contradiction.

The code checks every premise but the coverage in exact rationals at admission
(`certificate::admit`): $0 < M < n$; $0 < B < 1$; $B(1 + D) < 1$; the endpoint
polynomial; $t_{\max} < 1$ (so every net angle is below $\pi/2$ and its cosine and sine
are positive); $L^2 \ge 2B^2$ (so $a_r \le L/2$ and the domains are nonempty); and $0
\le x_1 < x_2 \le L$, $0 \le y_1 < y_2 \le L$ for every positive-weight rectangle
(containment is not needed for N4 but is the format’s promise).
Negative weights, duplicate JSON keys, a count or side that disagrees with the request,
and decimal tokens that do not parse exactly are refusals.
Decimal JSON numbers are their literal values, never the nearest binary64. The expansion
multiplies nothing out of order: each image’s exact density is summed when images
coincide, and the expanded total must integrate back to $M$ exactly.

The coverage threshold $T$ defaults to $1$, which is what N4 needs.
A larger $T$ (the authors’ checker uses $10001/10000$) only makes acceptance harder.

## Reduction of Centres

**Lemma C1 (quarter turn).** Let $\rho$ be the rotation by $\pi/2$ about $(L/2, L/2)$.
Then $\rho(Q_r(c)) = Q_r(\rho c)$, since a square is invariant under a quarter turn
about its centre, and $g \circ \rho = g$. So $F_r(c) = \int_{Q_r(c)} g$ satisfies
$F_r(\rho c) = F_r(c)$, and every point of $[a_r, L - a_r]^2$ has an image under a power
of $\rho$ in the closed quadrant $[L/2, L - a_r]^2$. It suffices to check that quadrant.
A reflection would reverse the angle and is not used here.

The search box for $r \ge 1$ is $[\ell, u]^2$ with $\ell \le L/2$ and $u \ge L - a_r$
the outward binary64 roundings, a superset of the quadrant.

## Direction $r = 0$

**Lemma A1 (vertices suffice).** For $\theta = 0$, $F(x, y) = \sum_k \rho_k\,
o^x_k(x)\, o^y_k(y)$ over the expanded rectangles, where $o^x_k(x) = |[x - h, x + h]
\cap [x_1, x_2]|$ with $h = B/2$. Each $o^x_k$ is continuous and affine between
consecutive points of $\{x_1 \pm h, x_2 \pm h\}$. Let $E$ be the set of all such points
in $[L/2, L - h]$ together with both ends.
On each cell of $E \times E$ every term is a product of an affine function of $x$ and
one of $y$, so $F$ is bilinear there, hence a convex combination of its four corner
values: its minimum over the closed quadrant is a minimum over grid vertices.
The event sets are computed and sorted in exact rationals (`axis::verify_axis`).

**Lemma A2 (the column sweep).** With $o^y_k(y) = r(y + h - y_1) - r(y + h - y_2) - r(y
- h - y_1) + r(y - h - y_2)$ and $r(z) = \max(z, 0)$, the column function $G(y) = \sum_k
  a_k o^y_k(y)$ for fixed weights $a_k = \rho_k o^x_k(x)$ is affine between
consecutive events, with slope changes $+a_k, -a_k, -a_k, +a_k$ at $y_1 - h, y_2 - h,
  y_1 + h, y_2 +
  h$. Every in-range breakpoint is itself an event (located by exact binary
search), a breakpoint below the domain belongs to the initial slope, and one above it
never acts. So $G(y_{j+1}) = G(y_j) + \sigma_j (y_{j+1} - y_j)$ with $\sigma_j$ the sum
of steps at or below $y_j$, which the code evaluates in interval arithmetic (lemma I1),
starting from a directly evaluated $G(y_0)$. The verdict compares the least lower
endpoint with the upper end of $T$’s enclosure.

## Directions $r \ge 1$

Write $c = \cos\theta_r$, $s = \sin\theta_r$ (exact rationals, both positive), $h =
B/2$, $u = (c, s)$, $v = (-s, c)$, so $Q(p) = \{q : |u \cdot (q - p)| \le h, |v \cdot (q
- p)| \le h\}$. A box of centres is $C = [x_0 \pm d_x] \times [y_0 \pm d_y]$; the code
takes $x_0$ the rounded midpoint and $d_x$ an upward-rounded half-width, so the real box
  it reasons about contains the box it was given.
  Splitting a box at its rounded midpoint yields two closed boxes whose union is the
  box, so the leaves cover the search box.

**Lemma R1 (classification).** Let $R$ have centre $m$ and half-sizes $(w_x, w_y)$. Put
$\Delta = m - (x_0, y_0)$, $d_u = |u \cdot \Delta|$, $d_v = |v \cdot \Delta|$, $e_u
= c w_x + s w_y$, $e_v = s w_x + c w_y$, $b_u = c d_x + s d_y$, $b_v = s d_x + c d_y$.

- If $d_u + e_u + b_u \le h$ and $d_v + e_v + b_v \le h$, then $R \subseteq Q(p)$ for
  every $p \in C$. For $q \in R$, $p \in C$: $|u \cdot (q - p)| \le d_u + |u \cdot (q -
  m)| + |u \cdot (p - p_0)| \le d_u + e_u + b_u$, and likewise for $v$.
- If $d_u \ge e_u + h + b_u + \tau'$ for some $\tau' > 0$ (or the same along $v$, or the
  axis-aligned extents are separated by $\tau'$), then $R \cap Q(p) = \emptyset$ for
  every $p \in C$, by the same triangle inequality.

Inside rectangles contribute their exact mass $\rho |R|$ at every $p \in C$ and nothing
to the derivative; outside ones contribute nothing.
Both tests are made in plain binary64 with the slack `TAU` $= 10^{-9}$ added against the
decision (lemma F2), and anything not certified either way is a boundary rectangle.
A child box is a subset of its parent, so a parent’s inside and outside verdicts hold
for the child and only the parent’s boundary list is reclassified.

**Lemma R2 (area at the centre).** Fix $p_0$ and $R$ with an inner representable
rectangle $R^- \subseteq R$ (the code takes $[x_1^{\uparrow}, x_2^{\downarrow}] \times
[y_1^{\uparrow}, y_2^{\downarrow}]$ from the tight enclosures).
For $\xi$ in $R^-$’s abscissa range (as offsets from $x_0$), the vertical section of
$R^- \cap Q(p_0)$ has length $\max(0, \eta(\xi))$ where

$$
\eta(\xi) = \min(e, f_1(\xi), f_2(\xi)) - \max(b, g_1(\xi), g_2(\xi)),
$$

$e, b$ are the section’s top and bottom offsets, $f_1 = (h - c\xi)/s$, $f_2 = (h +
s\xi)/c$, $g_1 = (-h - c\xi)/s$, $g_2 = (s\xi - h)/c$. (On the vertical line, $|c\xi +
s\eta| \le h$ and $|-s\xi + c\eta| \le h$ are exactly $g_1 \le \eta \le f_1$ and $g_2
\le \eta \le f_2$.) So $\eta$ is a minimum of nine affine functions and is concave on
all of $\mathbb R$. For any nodes $\xi_0 < \dots < \xi_k$ in the abscissa range and
lower bounds $\lambda_i \le \eta(\xi_i)$,

$$
|R \cap Q(p_0)| \ge \int_{\xi_0}^{\xi_k} \max(0, \eta) \ge \sum_{i \in P} \frac{(\xi_{i+1}
- \xi_i)(\lambda_i + \lambda_{i+1})}{2}
$$

for any set $P$ of pieces with positive summands: on each piece $\max(0, \eta) \ge
\eta$, and the trapezoid underestimates the integral of a concave function.
The bound needs no breakpoint to be located exactly; the code places nodes at the
approximate breakpoints (where two affine pieces cross, and at the zeros of $\eta$) so
the bound is nearly exact, takes $P$ to be the pieces whose summand is positive, and
rounds every step downward (lemma I1). `rotated::area_dn`.

**Lemma R3 (mean value).** $F$ is Lipschitz (translating a square by $\delta$ changes it
by a set of area at most $4B|\delta|$, and $g$ is bounded), so it is absolutely
continuous on every segment.
If $|\partial_x F| \le G_x$ and $|\partial_y F| \le G_y$ almost everywhere on $C$, then
for $p \in C$, along the path $p_0 \to (p_x, y_0) \to
p$ inside $C$,

$$
F(p) \ge F(p_0) - G_x d_x - G_y d_y.
$$

**Lemma R4 (the derivative).** For a rectangle $R = [x_1, x_2] \times [y_1, y_2]$ and a
measurable $S$, $t \mapsto |(R - t e_1) \cap S| = \int_{y_1}^{y_2} |[x_1 - t, x_2 - t]
\cap S_y|\, dy$ is Lipschitz with derivative, for almost every $t$, $\ell(\{x_1 - t\}
\times [y_1, y_2] \cap S) - \ell(\{x_2 - t\} \times [y_1, y_2] \cap S)$, by
differentiating each one-dimensional section and Fubini.
Translating the square by $+t$ is translating $R$ by $-t$ relative to it, so

$$
\partial_x |R \cap Q(p)| = \ell(\text{left edge} \cap Q(p)) - \ell(\text{right edge}
\cap Q(p)),
$$

and $\partial_y$ is bottom minus top.
$\partial F$ is the $\rho$-weighted sum over the boundary rectangles (inside and outside
ones have zero derivative on $C$).

**Lemma R5 (edge lengths over a box).** For the vertical edge $\{a\} \times [b, e]$ and
$p \in C$, with $\omega = a - p_x$, $e' = e - p_y$, $b' = b - p_y$, the length inside
$Q(p)$ is $\max(0, \min_i T_i)$ over

$$
e - b,\ e' + \tfrac hs + \tfrac cs \omega,\ e' + \tfrac hc - \tfrac sc \omega,\
\tfrac hs - \tfrac cs \omega - b',\ \tfrac hc + \tfrac sc \omega - b',\ \tfrac{2h}s,\
\tfrac{2h}c,\ \tfrac hs + \tfrac hc - \tfrac{\omega}{sc},\ \tfrac hs + \tfrac hc +
\tfrac{\omega}{sc},
$$

the nine differences $X - Y$, $X \in \{e', f_1(\omega), f_2(\omega)\}$, $Y \in \{b',
g_1(\omega), g_2(\omega)\}$. Each $T_i$ depends on $p$ only through $\omega$ or $p_y$,
separately, so its interval enclosure over $C$ (with $a, b, e$ enclosed too) is valid,
and $\max(0, \min_i T_i)$ is enclosed by $[\max(0, \min_i T_i^{\mathrm{lo}}), \max(0,
\min_i T_i^{\mathrm{hi}})]$. Horizontal edges are the same with $c$ and $s$ exchanged.
An edge certified inside every square of the box (R1 with $w_x = 0$) has length exactly
$e - b$; one certified outside has length zero.
`rotated::segment_length`, `rotated::edge_length`.

**Acceptance.** A box is accepted when the downward-rounded $F^-(p_0) - G_x d_x - G_y
d_y$, with $F^-$ the sum of inside masses and R2 bounds and $G$ the magnitude of the
interval sum of R4–R5 enclosures, is at least the upper end of $T$’s enclosure.
The receipt’s minimum certified bound is the least accepted value, a lower bound on
$\min F$ over the quadrant.
A box whose centre bound falls below $T - 10^{-7}$ stops the direction as a
counterexample candidate, which is a refusal; `--confirm` evaluates the candidate centre
in exact rationals (`oracle::coverage`). Budgets exhausted are `unresolved`, also a
refusal.

## Floating Point

**Lemma I1 (directed steps).** Let $z$ be real, $x = \mathrm{fl}(z)$ its
round-to-nearest value (finite), $x^+$ and $x^-$ the adjacent binary64 values above and
below $x$, and

$$
\mathrm{up}(x) = \mathrm{fl}\big(x + \mathrm{fl}(\mathrm{fl}(|x| 2^{-52}) +
2^{-1074})\big),\qquad \mathrm{dn}(x) = \mathrm{fl}\big(x -
\mathrm{fl}(\mathrm{fl}(|x| 2^{-52}) + 2^{-1074})\big).
$$

Then $\mathrm{dn}(x) \le z \le \mathrm{up}(x)$. *Proof.* $z \le x^+$: if $z > x^+$, then
$x^+$ would be nearer to $z$ than $x$. Let $g = x^+ - x$, a power of two.
For normal $x$, $g \le 2^{-52}|x|$ (also for $x =
-2^e$, where $g = 2^{e-53}$); rounding is monotone and $g$ is representable, so
$\delta = \mathrm{fl}(|x| 2^{-52}) \ge g$. For zero or subnormal $x$, $g = 2^{-1074}$.
Either way $\mathrm{fl}(\delta + 2^{-1074}) \ge g$, hence $x + \mathrm{fl}(\delta +
2^{-1074}) \ge x^+$, and by monotonicity $\mathrm{up}(x) \ge \mathrm{fl}(x^+) = x^+ \ge
z$. The lower step is symmetric.
The step is branch-free and may land two values out, which costs a few units in the last
place and nothing in soundness.
`interval::tests::steps_reach_the_adjacent_values` checks $\mathrm{up}(x) \ge x^+$ on
special values and 100,000 random bit patterns.
(The first build used `next_up` and `next_down`; experiment exp-005 replaced them.)
Rust neither fuses multiply-adds nor uses x87, so each `+ - * /` is one correctly
rounded IEEE operation.
Every interval operation in `interval.rs` applies I1 to each endpoint.

**Lemma I2 (enclosing rationals).** `exact::enclose` returns the largest binary64 value
at most $q$ and the smallest at least $q$, decided by exact comparisons of $q$ with $\pm
m 2^e$ (`exact::compare`), so the starting approximation’s accuracy does not matter.

**Lemma F2 (classification slack).** The R1 tests and the edge tests are evaluated in
plain binary64 from approximations within two units in the last place of the exact
centre, half-sizes, $c$, $s$ and $h$. Every operand has magnitude below $4L + 4 \le
4004$ (sides are admitted up to `MAX_SIDE` $= 1000$), and each tested quantity is at
most ten operations deep, so by the standard model $|\mathrm{fl}(a \circ b) - a \circ b|
\le 2^{-53} |a \circ b|$ its absolute error is below $30 \cdot 4004 \cdot 2^{-52} <
3 \times 10^{-11}$, far below `TAU`. Decisions near the slack become boundary items,
which R2–R5 handle soundly.

## Tests That Hold the Lemmas

- `rotated_tests::area_lower_bound_is_below_and_close_to_exact`: R2 against exact
  rational clipping on random rectangles and directions, below and within $10^{-9}$.
- `rotated_tests::edge_length_enclosures_contain_exact_lengths_over_the_box`: R5 against
  exact rational edge lengths at the corners and interior points of 2,000 random boxes
  over five directions; a seeded wrong endpoint makes it fail.
- `interval::tests::steps_reach_the_adjacent_values`: I1 on special values and 100,000
  random bit patterns.
- The debug build re-derives every box’s incremental centre bound from the full
  rectangle list (R1’s inheritance) and panics on a difference.
- `devtools/check_sqverify_fast.py` compares, on retained certificates, the probe’s
  centre and box bounds with `sqpack.rectangle_density`’s exact coverage at sampled
  centres and box points, and runs the mutation controls; its `--quick` subset runs in
  the gate step `measure verifier Rust (sqverify-fast)`.
- `devtools/sqverify_fast_census.py` verifies every replayed certificate at all 201
  directions and evaluates, in exact rationals, the capture at the centre of each
  certificate’s least-bound leaf.

## The First Leg on Its Own Segment

**Lemma R7.** In R3’s path $p_0 \to (p_x, y_0) \to p$, the first leg lies on the segment
$S_x = [x_0 \pm d_x] \times \{y_0\}$, so it needs only $G^S_x \ge \sup_{S_x}
|\partial_x F|$; the second leg needs $G_y$ over the whole box.
Hence $F(p) \ge F(p_0) -
G^S_x d_x - G_y d_y$, and with the other order, $F(p) \ge F(p_0) - G_x d_x - G^S_y d_y$;
the larger of the two lower bounds holds.
$G^S_x$ is R5’s enclosure with the centre’s ordinate fixed at $y_0$ (the segment ends’
offsets enclosed with half-width zero), its abscissa still ranging over the box.
Any bound valid on the box is valid on the segment, so each segment bound is also capped
by the box’s. The current build does not use R7: experiments exp-009 and exp-010 found
that it removes about a third of the boxes but costs as much again in enclosures,
eagerly or lazily.

## Inheritance of Derivative Bounds

**Lemma R6.** A bound $G_x \ge \sup_C |\partial_x F|$ proved on a box $C$ holds on every
sub-box $C' \subseteq C$. So a child may apply R3 with its parent’s bounds, and with the
smaller of its parent’s and its own, per axis.
Skipping a box’s own enclosure is only a choice of where to spend work: it never accepts
a box (experiment exp-003).

## The Release Audit

**Lemma A3 (what the audit establishes).** At an audited box the centre bound is
recomputed by R2 over every rectangle, with no classification and no inherited mass.
Inside rectangles enter the incremental sum as their exact mass and the full sum through
R2, which is within rounding of it; boundary and outside rectangles enter both the same
way. So on a correct run the two agree to within `AUDIT_TOLERANCE` (relative $10^{-9}$),
and a disagreement proves the incremental bookkeeping wrong at that box or at an
ancestor whose inside mass it inherits.
The search then stops with `audit-failed`, a refusal.
The audit covers R1’s decisions and their inheritance, not the derivative enclosures,
which `rotated_tests` and the box differential test check.
The audit is sampled (the root and every $K$-th box, $K = 1024$ by default), so a wrong
inside decision is caught when its box or a box in its subtree is audited;
`--audit-every 1` audits every box.
`--inject-fault-at-node N` classifies the first boundary rectangle at box $N$ as inside,
the control of spec §4.2; the controls in `devtools/check_sqverify_fast.py` require the
refusal.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
