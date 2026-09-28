# wand125 Rectangle Certificates: Does the Reviewed Checker Scale to Side 9?

The premises reviewed on 2026-09-22 for Tokoharu’s three certificates carry unchanged to
wand125’s 44 standing certificates at sides up to $1791/200 = 8.955$ and up to 812
rectangle orbits. Nothing in `verify.cpp`, `run_verify.py` or the repository’s intake
path depends on the side, the count or the number of rectangles except through running
time: every arithmetic step is an outward-rounded binary64 interval whose width scales
with the operands, every absolute constant is either exact or fails safe, and every hard
limit ends the run with a nonzero status rather than a truncated result.
No defect was found in the mathematics, the checker or the intake.
The three verified registrations (n27, n28 by transfer, n31) and the 42 reported ones
stand. Two Low observations are recorded below; neither moves a bound.

This is a read-only review by a Fable max sub-agent acting as the mathematical reviewer
of the coordinator’s 2026-09-27 wand125 intake.
It is evidence for the coordinator: no result row was registered and no bound was moved
by writing it.

## Scope and Evidence

The reviewed source is the packet
[`wand125-rectangle-certificates-2026-09-27`](../../../packing/resources/web/wand125-rectangle-certificates-2026-09-27/README.md),
pinning
[wand125/square-packing-bounds at `ad43d29`](https://github.com/wand125/square-packing-bounds/tree/ad43d29d96d0d9740b34643b5ac3fb960909cf9c).
The checker is Tokoharu’s, retained with the
[September 22 packet](../../../packing/resources/web/external-square-certificates-2026-09-22/tokoharu-density/README.md)
and reviewed in the
[density mathematics review](review-2026-09-22-tokoharu-density-mathematics.md).
The tree manifest records the same `verify.cpp` (SHA-256 `a75140df…`) and
`run_verify.py` (`7bce2467…`) in all 192 certificate directories, and the audit tool
refuses any directory whose digest differs.

Read in full: `verify.cpp` (126 lines) and `run_verify.py`, again, with the new sizes in
mind; `devtools/audit_wand125_rectangles.py`, `devtools/audit_tokoharu_density.py` and
`devtools/apply_wand125_rectangles.py`; the packet README and the source README; the
three evidence entries; the case records n27, n28, n31, n46, n76 and n77; and the
metadata, summaries and per-angle rows of all 44 standing certificates.

Run here, under `/tmp/claude-0/review-wand/` with the project interpreter, on x86-64
Linux with `g++` 13.3.0:

- the exact preflight of n76 and n78 from the retained subset, including provenance over
  the 184 retained files (`PASS`, 1.6 s in all);
- a first-party replay of the largest certificate, n78, at directions $r = 1, 100, 200$
  from the regenerated input (its SHA-256 equals the published `9e0f56cb…`), compared
  field by field with the upstream rows;
- a field-by-field comparison of the retained n27, n31 and n32 replay rows against the
  upstream rows;
- statistics over the 44 certificates (table below), exact-rational checks of the two
  monotone transfers, an exact check of every candidate’s own `n`, `L`, `B` and `rhs`
  against the intake’s pinned table, and `apply_wand125_rectangles --check`, which
  reports no drift between the receipts and the register;
- a measurement of the double rounding error of the checker’s hull cross product at
  coordinates near sides 4.7 to 32.

## What Changes at the New Sizes

| Quantity | Tokoharu’s three | wand125’s 44 |
| --- | ---: | ---: |
| Side $L$ | $381/100$ to $571/100$ | $939/200$ to $1791/200$ |
| Positive orbit representatives | 24 to 83 | 135 (n32) to 812 (n78) |
| Expanded rectangles | 192 to 664 | 1,080 to 6,496 |
| Axis events per coordinate | 146 to 600 | 826 (n21) to 2,325 (n43) |
| Axis vertices ($r = 0$) | 21,316 to 360,000 | 682,276 to 5,405,625 |
| Largest node count at one $r \ge 1$ | — | 237,591 (n21, $r = 199$) |
| Longest single direction | — | 6,114 s (n55, $r = 0$) |
| Upstream wall time | 74 s to 179 s | 495 s to 13,737 s |
| Density $\rho$ range, all cases | — | $2.8 \times 10^{-9}$ to $1.4 \times 10^{5}$ |
| Smallest rectangle dimension | — | $3.2 \times 10^{-4}$ |
| Weight scaling factor | none | $1.00052$ to $1.02659$ |

Every candidate declares $B = 9977/10000$, `rhs` $= 1001/1000$ and the same net
$D = 83/40000$ with 201 directions; every candidate’s own `n` and `L` equal the pinned
table in `audit_wand125_rectangles.CASES`. The per-angle rows account for the summary
totals in all 44 cases, all 201 directions report `verified`, and the smallest printed
leaf bound is $1.0001000003$ (n68). The last figure is a branch-and-bound artefact, not
a margin: a box is accepted the moment its lower bound clears $10001/10000$, so the
least accepted leaf always sits just above the threshold.

## Fixed-Width Types and Overflow

`verify.cpp` has no fixed-size arrays and no compile-time capacity.
The rectangle count `n` and the axis-event count `nc` are `int`, read from the input and
used to size `std::vector`s; their largest values here are 6,496 and 2,325. Node and
leaf counters are `long long`. The axis case counts $nc^2 \le 5{,}405{,}625$ vertices,
and the largest single branch-and-bound direction is 237,591 nodes.
Polygon indices are `size_t` over at most eight vertices.
Python sums the node counts as unbounded integers.

The only integer arithmetic in floating point is the net’s rotation coefficients:
$p = 83r \le 16{,}600$, $q = 40{,}000$, so $p^2 \le 2.76 \times 10^8$,
$q^2 = 1.6 \times 10^9$ and $2pq \le 1.33 \times 10^9$, all exact integers in binary64
by a margin of $2^{22}$. They do not involve the side.

Weights are never summed in the checker; the mass inequality is decided by the preflight
in exact rationals, from the candidate’s weight strings.
The scaled weights are large rationals (denominators of 23 digits), which
`fractions.Fraction` handles exactly; `float(Fraction)` is correctly rounded, and the
preflight checks every emitted interval endpoint against its exact value.
Coverage values inside the checker are of order 1 to 3 and the derivative sums of order
$\rho \times$ length $\le 1.4 \times 10^5$; nothing approaches the binary64 range.

## Floating-Point Constants Relative to the Side

Every interval operation widens by `nextafter` at both ends, so the enclosure is
relative to the operand’s magnitude: at coordinates in $[8, 16)$ one ulp is
$2^{-49} \approx 1.8 \times 10^{-15}$, twice the value at Tokoharu’s sides.
The certified leaf inequality needs the enclosed coverage minus the enclosed derivative
penalty to clear $10001/10000$, a margin the LP left at $10^{-3}$ (its `rhs` is
$1001/1000$, and the scaling step raised every coverage value by a further factor above
one). Interval widths at side 9 are of order $10^{-15}$ times the number of terms, six
orders of magnitude below that margin.

The checker has four absolute constants:

- **`threshold = up(10001/10000)`** — an upward-rounded enclosure of an exact rational,
  independent of the side.
- **`(1 - 1e-9)` vertex shrink** — a relative contraction toward the polygon’s centroid.
  It moves a vertex by $10^{-9}$ times its distance from the centroid, at least
  $1.6 \times 10^{-13}$ for the smallest rectangle here ($3.2 \times 10^{-4}$ across),
  far above one ulp at side 9. Even if it moved nothing, the shrink only prepares the
  approximate polygon; the exact containment postchecks at lines 62 and 64 decide.
- **`1e-14` hull cutoff** — compared against the plain double cross product `cr`. The
  measurement here over 200,000 random triples of points within a unit square of a point
  near side $S$ gives a rounding error of at most $2.6 \times 10^{-16}$ for every $S$ in
  $\{4.7, 5.6, 9, 16, 32\}$: once $S \ge 2$, the coordinate differences are exact
  (Sterbenz) and only the two products round.
  The cutoff stays forty times above the noise at every side in question, and a wrong
  hull can only return area zero, because the interval `cross` at line 68 must be
  strictly positive for every edge before an area is trusted.
- **`0x1p-45` depth floor** — a dyadic on the unit parameter square, so the physical box
  half-width is $2^{-45} E$ with $E = L/2 - a$; it grows with the side, and the
  parameter arithmetic stays exact at every reachable depth as before.

`stod` reads hexadecimal endpoints exactly; a subnormal endpoint would raise
`std::out_of_range` and end the run, not silently flush, and the smallest magnitude in
any input here is $2.8 \times 10^{-9}$.

## Hard-Coded Limits and How They Fail

| Limit | Value | Largest observed | On breach |
| --- | ---: | ---: | --- |
| Nodes per direction, $r \ge 1$ | $10^7$ | 237,591 | `UNRESOLVED`, exit 3 |
| Box half-width in parameter space | $2^{-45}$ | not printed; all resolved | `UNRESOLVED`, exit 3 |
| Directions | $r = 0..200$ | 201 in every run | runner asserts the full set |
| Axis grid | $nc^2$, uncapped | 5,405,625 | none needed; exhaustive by construction |
| Input stream | `assert(in)` after the last token | — | abort, nonzero |

Nothing is truncated.
A breach of the node or depth limit is a nonzero exit that `run_verify.py` raises on,
and the audit tool then refuses the case.
The per-direction node counts at $r \ge 1$ do rise with the side — n27 peaks at 86,945
and n78 at 162,365 — but the largest anywhere is n21’s 237,591, 2.4% of the cap.
The axis case is where the size shows: it is one process evaluating every vertex of the
$nc \times nc$ grid against all expanded rectangles, $2 \times 10^6 \times 6{,}496$
interval products for n78, and it is the whole of the wall time in six cases.
That is cost, not soundness.

One inherited fragility, unchanged from September 22: the divisor-excludes-zero guard,
the rounding-mode check and the input-stream check are `assert`s, live only because the
runner’s fixed compile line does not define `NDEBUG`. The audit tool runs the retained
runner, so the guards are live in every replay here.

## The Net and the Box Argument at Side 9

The angular argument is entirely at unit scale.
The nearest net direction is within $\arctan D$, and the concentric $B$-square at that
direction lies inside the unit square because $B(1 + D) = 399908091/400000000 < 1$; the
smoothing margin $B(1 + D) + 3\varepsilon = 399968091/400000000 < 1$ likewise.
Neither involves $L$. The preflight recomputes both exactly for every certificate, with
the net-endpoint polynomial $t_{200}^2 + 2t_{200} - 1 = 89/40000 > 0$.

The side enters only through the centre domain.
At direction $r \ge 1$ the checker covers $(x, y) = (L/2 + uE, L/2 + vE)$ for
$(u, v) \in [0, 1]^2$, $E = L/2 - a$, which is the quarter-turn fundamental domain of
$[a, L - a]^2$ and contains the centre of every $B$-square whose enclosing unit square
lies in the container.
The leaf inequality $F \ge F(x_0, y_0) - G_x d_x - G_y d_y$ is the fundamental theorem
of calculus along two segments of the box, with $G_x, G_y$ interval enclosures of the
derivative over the whole box.
There is no Lipschitz constant assumed in advance and no margin that grows with $E$: a
larger $E$ makes the initial box physically larger, so the subdivision goes deeper and
the node counts rise, which the table above shows.
At $r = 0$ the coverage is bilinear on each cell of the event grid, its minimum is at a
vertex, and the grid is $\{a \pm B/2, d \pm B/2\} \cap [L/2, L - B/2]$ over all expanded
rectangles, with both domain endpoints; the preflight rebuilds that set from all four
edges and requires the checker input to list exactly it.
None of this changes with $L$.

The first-party replay of n78 at three directions reproduces the upstream rows exactly
on a different compiler, architecture and operating system:

| $r$ | Nodes | Leaves | Printed lower bound | Here | Upstream |
| ---: | ---: | ---: | --- | ---: | ---: |
| 1 | 128,911 | 64,456 | 1.0001005130179181 | 32.4 s | 27.9 s |
| 100 | 139,765 | 69,883 | 1.0001003497583174 | 60.3 s | 50.8 s |
| 200 | 162,325 | 81,163 | 1.0001007138274234 | 84.3 s | 67.3 s |

The retained n27, n31 and n32 replays likewise agree with upstream in nodes, leaves and
printed bound at all 201 directions each.
Bit-identical reproduction is what the reviewed arithmetic predicts — correctly rounded
operations, `nextafter`, exact hexadecimal parsing, no FMA — and its holding at side
8.955 is the direct evidence that the new sizes exercise nothing platform-dependent.

## DENS-1 and DENS-2 at This Intake

DENS-1 is a defect of `push.py`’s admission of a *starting* certificate: the driver
accepts a candidate for the wrong count and stale side metadata, so its own final status
is not a bound decision.
wand125’s tree at `ad43d29` does not contain `push.py` (its `src/` holds the point tools
`certify.py`, `check_with_sqpack.py`, `lp.py`, `verify.py`); the rectangle certificates
were built with Tokoharu’s solver, driven by that `push.py` for the ladder rungs and by
a fixed-support-plus-scaling route for the rest, as the source README describes.
A DENS-1 failure could therefore have put a wrongly labelled parent under a run, or made
the driver announce a bound it had not built.
It cannot change what the published files say, and the intake trusts none of the
driver’s outputs: `globally_verified`, `status` and `TARGET_REACHED` are never read.
The preflight recomputes the mass from the weight strings and requires it below the
pinned $n$, requires the candidate’s $L$ to equal the pinned side, regenerates the
checker input from the candidate so the replayed $L$ is the candidate’s, and binds that
input to the digest the accepting run recorded.
A wrong count or stale side would surface as `mass >= n` or a side mismatch.
All 44 candidates also carry their own `n` and `L` in agreement with the pins (checked
here; see WSC-1).

DENS-2 — the runner is a coverage checker, not a bound verifier — is exactly why the
intake wraps it, and wand125’s README says the same: “The runner does not check the
budget condition.” The scaling step is a matter for the mass check alone: multiplying
every weight by one positive rational multiplies every coverage value by the same
factor, and the checker read the scaled data, so nothing about how the factor was chosen
enters the proof.
All 44 factors lie in $[1.00052, 1.02659]$, so every scaled certificate
covers at least as well as the LP solution it came from.

## The Monotone Transfers

The precise statement: if $n$ unit squares pack in side $L$, the covering argument gives
$n \le M$. A certificate with $M < k$ therefore refutes $k$ squares, so $s(k) > L$; and
$s$ is nondecreasing (delete squares), so $s(m) > L$ for every $m \ge k$. The transfer
runs **upward** in the count and never downward: the n27 certificate says nothing about
$s(26)$. The packet README and the audit tool’s docstring state it in this direction.

- **n27 to n28 (verified lane).** $M = 26999/1000 < 28$, so the replayed n27 certificate
  proves $s(28) \ge 28/5$. It is weaker than n28’s own $1139/200 = 5.695$, which stays
  in the reported lane until its replay runs.
  Correctly registered: `n-028.md` holds verified $28/5$ on
  `E-wand125-rectangle-source-replay` and reported $1139/200$ on
  `E-wand125-rectangle-report`.
- **n76 to n77 (reported lane).** $M = 7599/100 < 77$ and $89/10 > 222/25$, n77’s own
  side; n75’s $889/100$ is smaller, so n76 is the right source, and n78’s $1791/200$
  exceeds $89/10$, so nothing carries further.
  Correctly registered on `E-wand125-rectangle-monotone-report`, with n77’s verified
  lane still Nagamochi’s $8.874007$.
- **Other consequences.** `monotone_bounds` would also carry n21 into 22–25, n32 into
  33–36, n45 into 46–50 and n61 into 62–65; each is superseded by a stronger registered
  bound there (Evan Daniel’s $5000/1001$ and $6$, Bentz’s $s(46) \ge 7$, Nagamochi’s
  $1 + \sqrt{36}$ and $1 + \sqrt{49}$), and `apply_wand125_rectangles` leaves a field
  another source holds at least as high.
  Its `--check` run reports no drift.

## Findings

### WSC-1 — Low: the preflight does not compare the candidate’s own `n` to the pin

`audit_tokoharu_density.preflight` checks the pinned side and `mass < n` for the pinned
$n$, and the metadata’s `L`, `B` and `mass_exact`, but never reads the candidate’s `n`
field. The bound is sound without it — the mass inequality is the operative condition —
and all 44 candidates agree with the pins.
It is the one descriptive field a DENS-1-style mislabel would leave inconsistent, so
requiring `candidate["n"] == n` is a cheap identity check worth adding.

### WSC-2 — Low: the axis direction is one unpartitioned process

At $r = 0$ the runner spawns one `verify 0 0`, which is the whole wall time in six of
the 44 cases (up to 6,114 s at n55) while the other 200 directions share the workers.
Splitting the vertex grid into ranges would cut the per-certificate wall time by a
factor near the worker count with no change to the mathematics.
That is for the replay budget, not the proof; the source is Tokoharu’s and any change
would be a new checker revision to review.

## Claims by Evidential Status

- **Proved here in exact arithmetic**: the net and smoothing margins; the rotation
  coefficients’ exactness; the two monotone transfers; the agreement of every
  candidate’s `n`, `L`, `B`, `rhs` with the pins; every mass below its count (the
  preflight receipt, re-run here for n76 and n78).
- **Computationally verified**: complete 201-direction coverage for n27, n31 and n32,
  bit-identical to upstream; n78 at $r = 1, 100, 200$, bit-identical to upstream.
  These are V4/C3 machine evidence by the reviewed checker, as before.
- **Reviewed by reading**: that no type, constant or limit in `verify.cpp` depends on
  the side, the count or the rectangle number except through running time.
- **Asserted by the source, not verified here**: complete coverage for the other 41
  standing certificates (n78’s remaining 198 directions included).
  Their upstream rows are consistent and their inputs bind to the published digests, and
  they stay reported until their replays pass.

## Disposition

The three verified registrations and the 42 reported ones stand.
For `E-wand125-rectangle-source-replay` the external review can move from `not-reviewed`
to `informally-verified`, dated 2026-09-27, with a note that this review read the
checker again against the new sizes, found no side-, count- or size-dependent premise,
and reproduced n78 at three directions bit for bit; the reported entries need no change.
The review should be added to `docs/project/document-map.yaml` as a retained record
review, as the other 2026-09-27 reviews are.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
