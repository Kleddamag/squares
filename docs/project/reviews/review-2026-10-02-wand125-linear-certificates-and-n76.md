# wand125 Linear Certificates: Review of `s(101) ≥ 257/25`, `s(83) ≥ 187/20` and the Point-and-Segment Checker, with an Addendum on n = 76

The two certificates `mixed_n101_L1028` and `mixed_n83_L935` are of a kind this record
has not registered: a measure of point masses, segments of uniform linear density and
rectangles of uniform density, given in $D_4$ orbits with exact rational geometry, of
total mass $n - 1/100000$, checked at coverage one over one quadrant of the centre
domain at each of 201 net angles by `code/unified_linear_verify.cpp`. The argument from
such a measure to the bound is sound, and the checker’s two new capture bounds, for a
point and for a segment, are lower bounds in the safe direction: a point is charged only
when it lies in the closed core for every centre of the box, and a segment only by the
parameter length between two points each proved inside every such core, which convexity
extends to the whole sub-segment.
The quadrant reduction rests on the measure’s quarter-turn invariance, which the source
never checks and need not, since its `validate` expands every primitive to its eight
$D_4$ images; this repository’s audit checks it on the images, and so did this review.
The angle-zero branch is a rigorous bound of the same shape as the oblique one, with the
left-minus-right derivative enclosed by `axis_slice`. Every exact premise readable from
the retained files holds for both certificates, and no blocking defect was found.
Four non-blocking findings are recorded, one of them the margin at $n = 83$ that the
record already corrects.
The two values stand as reported until the complete replay of each passes here.
`S3` is confirmed for the entry to be registered for $n = 83$ and $n = 101$ to 105.

The $n = 76$ certificate `mixed_n76_L894` is the certificate kind reviewed on 28
September and again on 2 October, with its `code/` byte-identical to the reviewed
checker; its exact premises hold, and `S3` is confirmed for its entry.
The addendum at the end records what was checked.

This is review lane R4 of stage 4 of the result import process, for imports I (issue 294
and its comment) and H (the comment on issue 282), written by Claude (model Fable) at
extra-high thinking effort, raised to maximum for the checker’s argument, separately
prompted as lane R4 with no shared context with the replay lane, on 2026-10-02. It
registers nothing and moves no bound.

## Scope and Evidence

| Claim | Directory | Pin | Orbits | Mass | Nodes the source records |
| --- | --- | --- | --- | --- | ---: |
| $s(101) \ge 257/25 = 10.28$ | `mixed_n101_L1028` | `0c35d909` (first committed at `af1db07b`, 2026-10-02T01:23:19Z) | 333 points, 897 segments, 4 rectangles | $10099999/100000$ | 55,222,823 |
| $s(83) \ge 187/20 = 9.35$ | `mixed_n83_L935` | `0c35d909`, 2026-10-02T05:26:52Z | 86 points, 222 segments, 774 rectangles | $8299999/100000$ | 137,090,913 |
| $s(76) \ge 447/50 = 8.94$ | `mixed_n76_L894` | `7975030a`, 2026-10-02T01:39:38Z | 317 rectangles | $7599999/100000$ | 38,762,302 oblique; 3,225,616 axis cells |

The packets are
[`wand125-linear-certificates-2026-10-02`](../../../packing/resources/web/wand125-linear-certificates-2026-10-02/README.md)
and
[`wand125-mixed-bounds-n76-2026-10-02`](../../../packing/resources/web/wand125-mixed-bounds-n76-2026-10-02/README.md).
The bundles are pinned by digest and not retained; nothing in them was read here beyond
what the packets’ receipts quote.

Read in full: the retained
[`unified_linear_verify.cpp`](../../../packing/resources/web/wand125-linear-certificates-2026-10-02/square-packing-bounds/certificates/mixed_n101_L1028/code/unified_linear_verify.cpp)
(196 lines, SHA-256 `0249726a…`), against Tokoharu’s `verify.cpp` (`a75140df…`) and
wand125’s `mixed_rotated_verify.cpp` (`89b674a6…`) by `diff`; the export and replay
drivers `unified_linear_verify.py`, `unified_linear_full_verify.py`,
`replay_linear_bundle.py` and `unified_measure.py`, and the `interval` and
`net_certificate` functions of the retained `mixed_n50_L740/code/`; the three
certificate READMEs, manifests and completion audits; both packet READMEs, the linear
audit receipt, the two single-angle replay receipts and the $n = 101$ control receipt;
the root README’s sections on $n = 101$ and 83; the audit tool
[`devtools/audit_wand125_linear.py`](../../../packing/devtools/audit_wand125_linear.py)
at its `_orbit`, `d4_invariant`, `linear_certificate`, `check_inputs`,
`_replay_direction`, `mutate_linear` and `linear_control`; the
[28 September review](review-2026-09-28-wand125-n50-mixed-verifier.md) of the mixed
verifier, which read this checker for `mixed_n50_L735` with its point and segment paths
“dead code for this certificate”, and the
[2 October review](review-2026-10-02-wand125-mixed-rectangle-bounds.md) of `T-069`; the
register entries and evidence entries the import drafted.

Run here, on one core of x86-64 Linux with the project CPython 3.14.7, as
`scratchpad/r4/linear_premises.py` and `scratchpad/r4/n76_premises.py` (exact rationals,
80-digit decimals for the square roots, SHA-256; no source program executed):

- for each linear candidate: $n$, $L$, $B$; every primitive inside the closed container,
  nondegenerate, of nonnegative mass; the orbit counts; the mass equal to `total_mass`
  and to $n - 1/100000$; the eight images of every orbit in the source’s order and the
  weighted image multiset invariant under the diagonal reflection and under
  $x \mapsto L - x$ (an implementation written here, not the audit’s); the candidate
  digest by the source’s rule; the net identities; the centre half-width at every index;
  the Green and Nagamochi comparisons; the per-angle records of each certificate;
- for the $n = 76$ candidate: the same premises as the 2 October review’s script, the
  digest, the 201 records, and the SHA-256 of each pinned `code/` file against the
  retained `mixed_n50_L740` copy.

No angle was replayed, and no checker was compiled here.

## The Argument From a Linear Measure to the Bound

**The measure.** The candidate lists orbit representatives.
`validate` (`unified_measure.py:40–65`) refuses any primitive outside $[0, L]^2$, a
reversed or empty rectangle, a zero-length segment, a negative mass, and a `total_mass`
that is not the sum; it then writes, for every primitive of positive mass $m$, its eight
images under `orbit` (lines 18–31: the swap $(x, y) \mapsto (y, x)$ or not, then each of
the four sign choices $x \mapsto L - x$, $y \mapsto L - y$), each with mass $m/8$. Those
eight maps are the dihedral group of the container, so the expanded family $\mu$ is
$D_4$-invariant whatever the listed representatives look like, coincident images
included (28 orbits at $n = 101$ and 25 at $n = 83$ have fewer than eight distinct
images; each still carries eight copies of $m/8$). A point image carries its mass at its
point; a segment image carries its mass uniformly along its length, so a sub-segment of
parameter length $\lambda$ carries $\lambda$ of it; a rectangle image carries density
$m/(8|R|)$. $\mu$ is a finite nonnegative Borel measure of mass $M = n - 1/100000 < n$.
No primitive touches a wall (the least coordinate distance to a wall is $0.1995$ at
$n = 101$ and $0.2052$ at $n = 83$), so no boundary convention of the container is
exercised; 67 and 17 orbits respectively have a point on a symmetry axis.

**Containment.** With $D = 83/40000$, $t_r = rD$, $\theta_r = 2\arctan t_r$ and
$B = 9977/10000$, the identities of the 28 September review were recomputed here:
$t_{200} = 83/200$ and $t_{200}^2 + 2t_{200} - 1 = 89/40000 > 0$, so the net reaches
past $\pi/4$; for $t, t_r \ge 0$, $\tan(|\theta - \theta_r|/2) \le |t - t_r| \le D/2$;
$\cos\delta + \sin\delta = (1 + 2z - z^2)/(1 + z^2) \le 1 + 2z$; and
$B(1 + D) = 399908091/400000000 < 1$, which is the `rotated_side_upper` every manifest
and certificate carries, with `side_margin` $91909/400000000$. So a unit square at any
orientation $\theta \in [0, \pi/4]$ contains, concentric and strictly inside its open
interior, a closed square of side $B$ at the net angle nearest to it.
`net_check` (`unified_measure.py:67–72`) refuses a candidate unless $T \le 1/2$,
$(1 + T)^2 \ge 2$ and $B(1 + D) < 1$, and the replay driver requires the stored `net`
block to equal `net_certificate` recomputed from $B$, $D$ and 200.

**The two folds.** The checker’s domain at net index $r$ is the closed quadrant
$[L/2,\ L/2 + E_r]^2$ with $E_r = (L - B(c_r + s_r))/2$, Tokoharu’s centre domain folded
by a quarter turn, as the 28 September review noted for `L735`. Two facts carry the
rest:

- *Quarter turn.* A core of side $B$ at angle $\theta_r$ centred at $p$, rotated by a
  quarter turn $\rho$ about the container’s centre, is the core at angle
  $\theta_r + \pi/2$ centred at $\rho(p)$, which as a set is the core at angle
  $\theta_r$ centred at $\rho(p)$. The four images of the quadrant under $\rho^k$ are
  the four closed quadrants of $[L/2 - E_r,\ L/2 + E_r]^2 = [a_r,\ L - a_r]^2$,
  $a_r = B(c_r + s_r)/2$, which is every centre at which such a core fits in the
  container, since the core’s extreme coordinates are attained at vertices inside
  $[0, L]^2$. With $\mu(\rho A) = \mu(A)$, coverage at least $1$ on the quadrant is
  coverage at least $1$ on the whole domain at angle $+\theta_r$.
- *Reflection.* A square at orientation $\theta \in (\pi/4, \pi/2)$ is the image under
  $\sigma: x \mapsto L - x$ of a square at orientation $\pi/2 - \theta \in (0, \pi/4)$,
  which contains a core at the nearest $+\theta_r$ with $\mu \ge 1$; $\sigma$ of that
  core is a core at $-\theta_r$ strictly inside the original square, with the same
  measure by $\mu(\sigma A) = \mu(A)$.

Both hypotheses are $\mu$’s invariance under the two generators of $D_4$, true by
construction of `orbit`, checked here on the weighted images, and checked by the audit’s
`d4_invariant` on every run of `linear-audit`. Nothing in the checker or the source’s
drivers checks it; nothing needs to, so long as the input the checker reads is the
expansion, which the replay’s byte comparison of the regenerated input and the audit’s
`check_inputs` (every image enclosed, in the source’s order) both bind.

**The count.** Choose in each of the $n$ closed unit squares of a packing the core just
described.
Cores lie in the squares’ interiors, which are pairwise disjoint, so the cores
are pairwise disjoint closed sets; a point mass on a core’s boundary belongs to that
core alone, and a segment’s length inside the cores is additive.
Each core has $\mu \ge 1$ by the 201 directional statements, so
$n \le \sum_i \mu(C_i) = \mu(\bigcup_i C_i) \le M < n$. The source claims $s(n) \ge L$;
compactness gives the strict inequality, as before.

**Transfer by mass.** $M < n \le n'$ for every $n' > n$, so the same certificate refutes
$n'$ squares in side $L$ with no further step: $s(102), \ldots, s(105) \ge 257/25$,
which the import’s entry states.
Against the record, $257/25$ exceeds Nagamochi’s $1 + \sqrt{86} = 10.2736\ldots$ at
$n = 105$ and falls below $1 + \sqrt{87} = 10.3273\ldots$ at $n = 106$; at $n = 84$ and
85 the record’s $47/5$ and $471/50$ are above $187/20$, so the $n = 83$ certificate
transfers nothing.

## The Checker, Function by Function

### What it shares with Tokoharu’s `verify.cpp`

Extracting the spans and diffing them here: the interval type, `dn`, `up`, the five
operators, `mn`, `mx`, `pos`, `ab`, `readI`, the structs `R` and `P`, `cross`, `cr`,
`area_lower`, `slice` and `Bound` (lines 17–29 and 31–80 of the retained file) are
byte-identical to Tokoharu’s. The oblique part of `bound` (139–153) is Tokoharu’s
`bound` with the interface changes the 28 September review tabulated for the mixed
checker ($E$, $c$, $s$, $\Gamma$ from the input; the atom term) and `main` (156–196) is
the mixed one: node limit from the command line, the $2^{-40}$ floor, JSON status with
exit zero, `query` and `region` modes, the anisotropy cap and tie-break in the split.
Against `mixed_rotated_verify.cpp` the `diff` is exactly: the header comment, the
`Segment` struct, `segment_lower`, `singular_lower`, `axis_slice`, the axis branch at
the top of `bound`, the segment list read in `main`, and the point loop moved from
`bound` into `singular_lower` with its body unchanged.
Tokoharu’s axis vertex loop, which the mixed checker dropped in favour of the integer
tables, is here replaced by the branch inside `bound`; so this checker has no Python
axis program and no NumPy in its proof path.

### Points

`singular_lower` (107–113) forms, for each atom, $p_x = x - X$ and $p_y = y - Y$ as
intervals over the whole outward-rounded box $X \times Y$ (124), and charges the weight
$w^l$ only if $|c\,p_x + s\,p_y|^h \le (B/2)^l$ and
$|{-s}\,p_x + c\,p_y|^h \le (B/2)^l$: the point’s rotated offset from every centre of
the box, for every value in the enclosures, is within the closed core’s half-side.
A pass means the point is in the closed core for every centre of the box; a failure
charges nothing. Each addition is rounded down.
A point on the core’s boundary for some centre of the box is charged nothing until the
box no longer contains such a centre, which is a loss of tightness, never of soundness
(LC-3).

### Segments

`segment_lower` (86–106) has a numeric stage and a proven stage, in the pattern of
`area_lower`:

- *Proposal* (87–100), in plain doubles: shrink the core’s half-side by the box’s
  half-widths rotated into the core’s frame, intersect the segment’s parameter
  $\lambda \in [0, 1]$ with the strip $|a_k + \lambda b_k| \le h_k$ on both axes, and
  inset the result by $\max(10^{-12}, 10^{-8}(\text{hi} - \text{lo}))$. A segment
  parallel to an axis and outside the strip returns $0$. Nothing here is trusted.
- *Proof* (101–104): for $t \in \lbrace \text{lo}, \text{hi} \rbrace$ the point
  $P(t) = (x_0, y_0) + t\,((x_1, y_1) - (x_0, y_0))$ is formed in interval arithmetic
  from the endpoint enclosures and the exact double $t$, its offset from $X \times Y$ is
  tested against $(B/2)^l$ exactly as a point is, and any failure returns $0$.
- *Charge* (105): $\downarrow\!\big(w^l \cdot \downarrow\!(\text{hi} - \text{lo})\big)$.

The core is convex, so if $P(\text{lo})$ and $P(\text{hi})$ are both in the closed core
$C$ at some centre, the whole sub-segment $P([\text{lo}, \text{hi}])$ is in $C$; the
mass on it is $w\,(\text{hi} - \text{lo})$ because uniform arclength density is uniform
in $\lambda$ on a straight segment, which is also how `coefficient` in
`unified_measure.py:89–98` scores a segment exactly.
The proof stage quantifies over every centre of the box, so the charge is a lower bound
on the segment’s contribution throughout the box.
`segment_lower` handles any direction: at $n = 101$ the 897 segment orbits are 896
horizontal and one oblique, at $n = 83$ the 222 are 80 horizontal, 57 vertical and 85
oblique, so the general path is exercised by the second certificate.

### Angle zero

At net index 0 the export writes $c = 1$ and $s = 0$; `interval` (retained
`mixed_rotated_verify.py:16–22`) returns a value that is already a binary64 as a
degenerate pair, so the input reads `0x1p+0 0x1p+0` and `0x0p+0 0x0p+0`, and `bound`
takes the branch at line 125 on `s.l == 0 && s.h == 0`. Had the pair not been
degenerate, the oblique branch would divide by $s$ at line 140 and the divisor assertion
in `operator/` would abort the run; no unsound path exists either way.
In the branch:

- $f$ (131) is $\sum_j \downarrow\!(\rho_j\, w_x\, w_y)^l$ with
  $w_x = (\min(d, c_x + B/2) - \max(a, c_x - B/2))^+$ in intervals over the centre
  enclosure $c_x$, likewise $w_y$: the exact axis-aligned overlap at the centre, rounded
  down.
- The derivative. For $R = [a, d] \times [b, e]$ the almost-everywhere derivative of
  $w_x(x)\,w_y(y)$ in $x$ is
  $\big(\mathbf 1[x - B/2 < a < x + B/2] - \mathbf 1[x - B/2 < d < x + B/2]\big)\,w_y(y)$,
  left edge inside the core’s $x$-extent minus right edge inside, as the four cases of
  $\min(d, x + B/2) - \max(a, x - B/2)$ show.
  `axis_slice` (116–121) encloses one edge’s term over the box: $0$ when the edge is
  outside the extent for every centre, the interval overlap `length` when it is strictly
  inside for every centre, and $[0, \text{length}^h]$ otherwise.
  `fx`, `fy` are the interval sums (132–133), $r_x = \uparrow\!(d_x^h\,|f_x|^h)$.
- The leaf value (137) is $\downarrow\!(\downarrow\!(\downarrow\!(f - r_x) - r_y) +
  \text{singular})$: the fundamental-theorem bound on the rectangle part, whose
  Lipschitz coverage is bounded below on the box by its value at the centre less the
  half-widths times the suprema of the derivatives, plus the point-and-segment term that
  `singular_lower` already quantifies over the whole box.
  The sum of a lower bound on one part and a lower bound on the other is a lower bound
  on $F$.

This is the branch the 28 September review read for `L735`’s axis (230,167 nodes there);
here it did 2,072,307 nodes at $n = 101$, the most of any angle, and 424,193 at
$n = 83$.

### The oblique branch and the combination

Lines 139–153 are Tokoharu’s: `area_lower` at the centre enclosure, `slice` for the
chord of each edge over the box, $r_x$, $r_y$ rounded up, and the leaf
$\downarrow\!(\downarrow\!(\downarrow\!(f - r_x) - r_y) + \text{atom})$ with `atom` now
`singular_lower`. The 22 and 28 September reviews re-derived every step at $\Gamma = 1$
and ran a 72-box exact control on the shared kernel; nothing in those bytes changed.

### Branch and bound, rounding, modes

The root box is the normalised quadrant $(1/2, 1/2, 1/2, 1/2)$ (175); a child is its
parent halved along one axis in exact dyadic doubles, so the boxes partition the
quadrant down to the $2^{-40}$ floor (184), where an unresolved box is pushed back and
the run stops `ANGLE_UNRESOLVED`. The physical box is $L/2 + z\,E$ in intervals with the
exact $E$ enclosed in the input, then widened one `nextafter` each way (124). A leaf is
accepted on `b.lower >= gamma.h` with `gamma` exactly $1$: `export` writes
`interval(F(1))`, a degenerate pair, and the audit’s `check_inputs` requires that line
to be `(1, 1)`. `static_assert` binds IEEE binary64, `fegetround()` is asserted
round-to-nearest, and `compile_verifier` fixes
`-O2 -std=c++17 -ffp-contract=off -fno-fast-math` with no `NDEBUG`, so the divisor and
rounding-mode assertions are live.
`stod` parses the hexadecimal pairs exactly.
`query` and `region` are not in the proof path: `replay_angle` runs the binary with the
input and the stored node count only.
The split heuristic (186–189) chooses axes and nothing else.

## Hypotheses the Checker Assumes

1. **The input encloses the expanded exact measure.** `export` writes every image
   through `interval`, which asserts the enclosure; the replay regenerates each input
   and requires byte equality with the bundle’s; the audit’s `check_inputs` requires
   every interval to enclose the image recomputed here, in the source’s order, with
   `gamma` exactly $1$. Run by the packet on all 201 inputs of each bundle; the replay
   repeats it.
2. **Mass, geometry, counts, digest.** Checked here exactly and by `validate` on every
   path that reads the candidate; `export` and `replay_linear_bundle.py` refuse
   $M \ge n$.
3. **$D_4$ invariance of the expanded family.** By construction of `orbit`; checked here
   and by `d4_invariant`. The quadrant fold needs the quarter turn and the orientation
   fold a reflection; both are prose lemmas whose hypothesis is this invariance.
4. **Containment.** $B(1 + D) < 1$, the reach of the net, the half-angle inequality:
   prose with rational instances recomputed here, refused by `net_check` if false.
5. **The per-angle domain.** $E_r = (L - B(c_r + s_r))/2 > 0$ at every index, least at
   index 200 ($4.4345\ldots$ and $3.9695\ldots$); Tokoharu’s domain, with no strip
   omitted, so MV-2’s indexing concern does not arise.
6. **The rectangle kernel.** `area_lower`, `slice`, the fundamental-theorem bound with
   an almost-everywhere derivative, under binary64 round-to-nearest without FMA or
   fast-math: prose, reviewed on 22 and 28 September; bytes unchanged.
7. **The point and segment bounds.** Convexity of the closed core and uniformity of a
   segment’s mass in its parameter: prose, derived above.
8. **Closed cores in closed squares.** The theorem is about closed unit squares with
   disjoint interiors in the closed container; a core strictly inside its square’s
   interior; cores pairwise disjoint; $\mu$ additive on them.
   Prose.
9. **Every angle finishes.** Empty frontier under the node limit $3{,}000{,}000$ in both
   manifests and the $2^{-40}$ floor; the largest recorded angle is 2,072,307 nodes.
   What the replay decides.
10. **Asserts and exit codes** (MV-1 of 28 September).
    Every acceptance check in the source’s drivers is an `assert`, and the C++ exits
    zero on an unresolved angle.
    The repository’s replay refuses to start with assertions off (`replay_runtime`,
    shared with the mixed tool) and its merge requires `PYTHONOPTIMIZE` unset in every
    run record; anyone running the source’s own command must do the same.
11. **The trusted base.** The compiler at the fixed flags, `stod`, `nextafter`,
    binary64, CPython’s `Fraction` and the reviewed C++ logic; none is proof-assistant
    checked, as the certificate’s `replay_scope` says.

## Where the Requests and the Record Differ

- **The margin at $n = 83$.** The directory README, the root README and
  `improvement_lower` $= 833/10000$ measure from $92667/10000$, below Green’s
  $2\sqrt2 + (247 + 12\sqrt2)/41 = 9.26673353\ldots$; the margin is $0.08326646\ldots$,
  which is not “more than 0.0833”. The packet and the import’s entry already say so.
  At $n = 101$ the comparison is a 90-digit upper enclosure of $G_{10}$ and the margin
  $0.03326373\ldots$ is as the source states; both recomputed here.
- **Dependencies.** Both READMEs ask for NumPy, SciPy, Numba and HiGHS; the replay path
  imports the standard library only and needs a C++17 compiler, as MV-6 found for
  `L735`.
- **The second replay “on a separate machine”** is stated in issue 294 and the READMEs
  and is not checkable here; the replay here decides the matter.
- **Issue 294 announces $n = 82$ at $9.32$**, which no revision publishes; nothing is
  claimed for it.

## Findings

No blocking finding.

### LC-1 — Low, in the source: the $n = 83$ margin over Green is overstated

As above; the bound is unaffected, and the reply on issue 294 should carry it.

### LC-2 — Note: the READMEs state the fold’s conclusion and not its hypothesis

Each README’s Argument says “$D_4$ symmetry reduces orientations to $[0, \pi/4]$” and
“every closed core … has measure $\ge 1$”, and the manifests’ `net.remaining` says
“every admissible centre at every net angle”; none says that the checker covers one
quadrant and that the quarter-turn invariance of the expanded measure carries the rest.
The invariance is true by construction and is checked here; a reader comparing the
checker’s root box with Tokoharu’s domain should be told why they differ.

### LC-3 — Note: a refusal is an unresolved frontier, not a measured deficit

An atom or segment is charged only when captured throughout a box, so at a centre where
the coverage drops below $1$ once a boundary atom is excluded, the branch and bound
cannot close and stops at the depth floor.
That is why the control’s two mutations ended `ANGLE_UNRESOLVED` with a frontier rather
than with a deficit: the C++ reports nothing but the frontier, the source’s `run`
(`unified_linear_verify.py:43–49`) evaluates exact witnesses on sampled frontier boxes
afterwards, and the repository’s control found its own witness exactly instead (coverage
$1.00200\ldots$ at the original, $0.99198\ldots$ and $0.95298\ldots$ at the mutations;
the checker stopped after 78 and 18,933 nodes with 78 and 19 boxes open, against the
original’s 76,875 nodes and none).
A measure whose coverage reaches $1$ at some centre only with an atom on the core’s
boundary could not be certified by this checker even where it is valid; neither
certificate is such a measure, since both record empty frontiers.

### LC-4 — Note: the certificate’s records carry nodes and the input digest only

Each `LINEAR_ANGLE_REPLAYED` record holds `index`, `input_sha256` and `nodes`; the
`lower`, `leaves` and `frontier` the replay compares live in the bundle’s per-angle
`result.json`, bound to the pinned tarball by digest.
The replay here compares them through the shipped `replay_angle`, which is right, but
the merged receipts should retain each certificate’s least accepted `lower` and the
angle it occurs at, as the mixed receipts do, so that the figure is on file without the
bundle.

## Claims by Evidential Status

- **Proved here in exact arithmetic:** the containment identities; the centre half-width
  at all 201 indices of each certificate; the orbit counts, the image counts ($2{,}664$,
  $7{,}176$, $32$ and $688$, $1{,}776$, $6{,}192$), the $D_4$ invariance under both
  generators, the mass $n - 1/100000$ and the candidate digests (`933aa468…`,
  `159f4c9e…`); the 201 replay records of each certificate with distinct input digests
  and the node totals above; the Green and Nagamochi comparisons.
- **Reviewed by reading:** the soundness of the point and segment bounds, of the
  angle-zero branch and of the combination in `bound`; that the shared kernel is
  Tokoharu’s byte for byte; that the quadrant and orientation folds need only the
  invariance proved above; that the source’s drivers bind the input to the candidate.
- **Asserted by the source, not verified here:** the 201 directional statements of each
  certificate, the byte identity of the regenerated inputs beyond the two angles the
  packet replayed, and the contents of the bundles.
- **Checked by the packet lane and relied on here:** every pre-replay check on both
  pinned tarballs, the enclosure of all 402 inputs, the single-angle replays at indices
  150 and 50, and the $n = 101$ control.

## What the Replay Must Show

For `V3/C3` on the entry for $n = 83$ and $n = 101$ to 105:

- Both tarballs fetched at `0c35d909` (`--via git`), hashing to `c32bba42…` (27,507,146
  bytes) and `ca8bf313…` (46,291,647 bytes); each unpacked afresh and bound to the
  packet by `linear-replay`’s preconditions; `code/` assembled from the retained copies,
  never from the bundle.
- Every one of the 201 directions of each certificate replayed by the shipped
  `replay_angle` unchanged, under the shipped compile line with the compiler version
  recorded, with assertions on and `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`; each
  direction passing only because the function returned the certificate’s own record.
  Expect totals of 55,222,823 and 137,090,913 nodes; the axis at $n = 101$ (2,072,307
  nodes, about 20 minutes) and index 200 at $n = 83$ (1,037,823) as the longest.
- `linear-merge` for each, printing a full replay with no missing or refused direction,
  every run bound to the pinned tarball with `PYTHONOPTIMIZE` unset; receipts committed
  as each range ends, in the ranges `linear-plan` gives (one for $n = 101$; 0–90,
  91–152, 153–200 for $n = 83$).
- Two mutated controls refused by the retained path and held by a test: the $n = 101$
  control at index 35 is on file
  ([`receipts/n101/control.json`](../../../packing/resources/web/wand125-linear-certificates-2026-10-02/receipts/n101/control.json),
  `test_the_control_accepts_the_original_and_refuses_both_mutations`); run
  `linear-control n83` as well, since that measure’s mix is different and its
  `drop-top-contributor` mutation may fall on a rectangle or point orbit rather than a
  segment, and keep both receipts.
- The cost beside the source’s: 31,304 and 75,686 seconds upstream; the packet’s pricing
  is 8.1 and 23.0 CPU-hours here.
- The entry’s `composition` should keep saying that coverage is decided by the source’s
  C++ alone: the replay is the same implementation, the point and segment paths have no
  second implementation anywhere, and `C4` is not available from it.

## Significance

`S3` confirmed for the entry to be registered for $n = 83$ and $n = 101$ to 105. Scored
as a claim, these are substantive case results at six counts: past Green’s reported
value at $n = 101$ by $0.0333$ and at $n = 83$ by $0.0833$, and past Nagamochi’s at
$n = 105$; the first linear certificates in this record, and the first results above
Green’s $k = 10$ value.
The nearest entries are `T-048` and `T-069` at `S3`. The kind is new here, but the
technique is Stromquist’s and Nagamochi’s measure argument with Tokoharu’s net and
checker, extended by two capture bounds; the generator is the source’s and is not
retained, no disputed value is resolved, and `S4` would need the kind to be a reusable
technique established here rather than two more sizes from one generator.

## Addendum: $s(76) \ge 447/50$ by `mixed_n76_L894`

The certificate is the kind of `T-048`, `T-069` and `T-071`, read on 28 September and 2
October, and nothing in it differs from those reviews’ object:

- The ten files of its `code/` hash, each, to the retained `mixed_n50_L740` copy
  (checked here from `acquisition/sources.json`), so the checker is `89b674a6…` and the
  axis program is the reviewed `verify_axis_certificate.py`; `source_sha256` in the
  manifest and every oblique record names it.
- The candidate has 317 rectangles inside the container with positive area and
  nonnegative mass, no point, mass $7599999/100000 = 76 - 1/100000$, `scaling_factor`
  $1$ and `scaling_source_digest` equal to its own digest, which recomputes here by the
  source’s rule to `f2c25305…`, the digest the manifest, the audit and all 201 records
  carry.
- The certificate records 200 `ANGLE_RESULT_REPLAYED` angles and one
  `AXIS_CERTIFICATE_REPLAYED`, 38,762,302 oblique nodes, least `lower`
  $1.000000000516032$ at index 150 (the README’s $1.0000000005$ is right to its places),
  and an axis integer minimum of $1.0075130139576551$ over 3,225,616 cells, a margin of
  $0.75$ per cent at angle zero.
- The side exceeds Nagamochi’s $1 + \sqrt{61} = 8.8102\ldots$, the source’s
  `rect_n76_L8925` ($357/40$, `T-068`) by $3/200$, and Green’s $k = 8$ value.
- The hypotheses of the 2 October review hold unchanged: Tokoharu’s format departs only
  in $\Gamma = 1$ and the per-node domain, both reviewed; the net block is the one
  recomputed there; `requirements.txt` is the `L740` one.
  As that review’s MX-5 noted for $n = 65$, where the second replay ran is not checked
  and the replay here decides it.

No defect.
`S3` is confirmed for its entry: a further size from one generator by the kind
of `T-048`, the strongest reported value at $n = 76$ if the replay passes.
For `V3/C3` the replay must do what that review’s list says, with the
`audit_wand125_point_and_mixed` range driver: the tarball `d804bb88…` (11,942,640 bytes)
at `7975030a`, all 621 file hashes, `ALL_ANGLES_VERIFIED_AND_REPLAYED`, the axis cell
count and integer minimum above, every oblique `replayed.json` with the record’s node
count and `lower`, two mutated controls refused, and the cost beside the source’s 12,687
seconds (the packet prices 2.2 CPU-hours).

## Disposition

Both linear certificates are accepted by this review with no defect open: `C1` once this
document is recorded as `external_review` on `E-n083-wand125-linear-935-report` and
`E-n101-wand125-linear-1028-report` (`informally-verified`, 2026-10-02) and listed in
their entry’s `reviews`, with the document mapped as a retained review; `V3/C3` when the
replays above pass. The $n = 76$ certificate is accepted the same way on
`E-n076-wand125-mixed-894-report`. The reply on issue 294 should carry LC-1 and LC-2 to
the author.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
