# Proof Review: Guzhou0806’s R071, `s(17) > 18641771/4000000 = 4.66044275`

Reviewed 2026-10-05 from the retained packet
[`n17-guzhou-r071-2026-09-30`](../../../packing/resources/web/n17-guzhou-r071-2026-09-30/README.md),
pinned at `8c11f696`, by an AI agent: the review lane of the 2026-10-05 stage 4 of the
result import for `T-093`, prompted separately from the lane that retained the packet
and registered `T-093` and from the lane replaying its certificate, sharing no context
with either and blind to the replay.
The model is `claude-opus-5-5` at the tbd-strong tier, whose configured reasoning
setting is xhigh.

This is the stage-4 review of `T-093`: Guzhou0806 / N17 project’s R071 claim
$s(17) > 18641771/4000000 = 4.66044275$, registered at `V0/C0` with draft significance
`S2`. It continues the
[2026-09-28 review of R067 and R068](review-2026-09-28-n17-guzhou-r067-r068.md), which
read the same charge and the same two checkers for `T-042` and `T-043`. It registers
nothing and moves no bound.

**In one line:** R071’s C027 certificate is R068’s charge, byte for byte, run at a
parent side smaller by a relative $5.9 \times 10^{-7}$ with every strict core rebuilt
over a catalogue of 5,114 angle intervals that refines R068’s 4,991 and R070’s 5,107; no
mathematical defect was found; every premise re-derives here in exact arithmetic by code
sharing nothing with the source, and an independent exact sweep returns the source’s
minimum core charge at 227 sampled rows, while reproducing R068’s and R070’s published
ledgers, cell counts included, at 20 control rows; the source retains no row of its own
sweep, so the bound rests on the complete paired replay, after which `V3/C3` is right
and `S2` is confirmed.

## 1. What Was Reviewed

| Field | R068 (`T-043`) | R070 (no entry) | R071 (`T-093`) |
| --- | --- | --- | --- |
| Commit | `815b1626`, 2026-09-28T12:44:22Z | `8988d933`, 2026-09-29T07:56:05Z | `8c11f696`, 2026-09-30T22:53:43Z |
| Claim | $116511/25000 = 4.66044$ | $46604427/10000000 = 4.6604427$ | $18641771/4000000 = 4.66044275$ |
| Package | `R068-C010/accepted/4.66044/` | `R070-4.6604427/` | `R071-C029/bounds/c027/` |
| Certificate SHA-256 | `cf70f74d…` | `8438cae4…` | `15b6bf6a…` |
| Parent side $A$ in $L = 4613/1000$ | $115325/116511$ | $46130000/46604427$ | $18452000/18641771$ |
| Angle intervals | 4,991 | 5,107 | 5,114 |
| Budget $M$, units of $10^{-9}$ | 17,000,448,944 | the same | the same |
| Requested minimum | 1,000,026,409 | the same | the same |
| Reported least core charge $\Gamma$ | 1,000,026,844 | 1,000,026,844 | 1,000,026,844 |
| $17\Gamma - M$ | 7,404 | 7,404 | 7,404 |
| Least strict core margin | $1.0000007 \times 10^{-12}$ | $1.0002300 \times 10^{-12}$ | $1.0001596 \times 10^{-12}$ |
| Row records | two C++ and two Node partitions | four and four | none; a completion summary |
| Replayed here | in full, 28 and 29 September | no | no |

Read in full: in `certificates/R071-C029/`, `BOUND_PROOF.md`, `GEOMETRY_PROOF.md`,
`README.md`, `ATTRIBUTION.md`, `PUBLICATION_STATUS.json`, `REPRODUCIBILITY.md`,
`run_public.js`, `check_package.js`, `history/c027/C027_GLOBAL_THEOREM.json` and every
field of `bounds/c027/certificate.json`; in `certificates/R070-4.6604427/`, `PROOF.md`,
`GEOMETRIC_RESULTS.md`, `README.md`, `ATTRIBUTION.md`, `PUBLICATION_STATUS.json`,
`REPRODUCIBILITY.md`, the certificate, its `THEOREM.json` and `INPUTS.json` and its
eight published ledgers; the source’s root `README.md`, `NOTICE.md`, `CITATION.cff`,
`CHANGELOG.md` and `.github/workflows/r071.yml`; the packet README, its acquisition
records and its receipts, the CI run record among them; and, from the R068 packet, the
launcher `replay.js` and Kleddamag’s `reference/verify_global_variable.js` again, with
the certificate fields `verify.cpp` reads.
On the record side: `T-093`, `T-043`, `T-039`, `T-041` and `T-042`;
`E-n017-guzhou-r071-report`, `E-n017-guzhou-r068-report` and
`E-n017-guzhou-r068-source-replay`; the case record
[`n-017.md`](../../../packing/frontier/n-017.md); the verifier rows
`V-guzhou-n17-verify-cpp`, `V-kleddamag-n17-verify` and `V-audit-guzhou-r068`; the keys
`[Guzhou0806 n17 R071]` and `[Guzhou0806 n17 R070]` and their rows in the resources
README; the coverage entry `guzhou-n17-r071-2026`; and `devtools.audit_guzhou_r071`, the
`compare` function of `devtools.audit_guzhou_r068` it calls, and the test list of
`test_guzhou_r071_packet.py`.

**The checkers are R068’s bytes.** Each package pins its sixteen
`project/base/upstream/` files by digest only.
Their digests in the packet’s subtree manifest equal the SHA-256 of the R068 packet’s
retained copies, computed here: `verify.cpp` `3ba09554…`, `native_geometry.hpp`
`ade0091a…`, `replay.js` `1125e596…`, `reference/verify_global_variable.js` `c2209186…`
and the twelve notices.
R068’s `CMakeLists.txt` and `probe.cpp` are not in R071’s package and are not needed:
`run_public.js` compiles `verify.cpp` directly.
These are the programs the 2026-09-28 review read line by line and this repository’s
replay of R068 ran. The one checker-side file that is new is `run_public.js`, R071’s
launcher, read here (§7).

**Run here**, under the project interpreter (CPython 3.14.7, `Fraction` and `int`; NumPy
`int64` for the sweep’s value array only), from scratch scripts that import nothing from
the source or from this repository’s tools and are not retained:

- `premises.py`, the exact premises of all three certificates, 3.6 CPU-seconds;
- `rowsweep.py`, an exact sweep of one row with a direct evaluation of the original
  predicates at the argmin cell, about 1.3 CPU-seconds a row: 20 control rows of R068
  and R070 and 227 rows of R071;
- `corner.py`, the charge of a certified core at a legal corner centre for every one of
  the 5,114 rows of R071, 44 CPU-seconds, and the open charge of the parent R070’s
  obstruction names.

The source’s complete replay was not run; it is the replay lane’s. The whole review used
about 6 CPU-minutes on one core.

## 2. Verdict

**No mathematical defect was found.** The argument from the C027 certificate to
$s(17) > 18641771/4000000$ is R068’s, which is Kleddamag’s $4.66001$ argument, with a
new parent side. The new side, the refined chain and the rebuilt cores touch five
premises and nothing else: the target identity, the chain, each core’s strict
containment, each envelope, and the exact sweep.
The first four re-derive exactly here at every one of the 5,114 rows.
The sweep is the one the source retains no row of; this review’s independent sweep
returns $1{,}000{,}026{,}844$ at every one of 227 sampled rows, the 14 rows R071 adds
among them, and the charge of a certified core at a legal corner centre equals it at all
5,114 rows, so no row’s minimum lies above it.
The verdict is **sound as stated, conditional on the complete paired replay** passing
with the values in §8.

Nothing found here would make it wrong to move n = 17’s verified lower bound to
$18641771/4000000$ and raise `T-093` to `V3/C3` once that replay is recorded as
replayed-here evidence.
Nine findings are recorded in §14, and none blocks.
Five are non-blocking: the missing rows, which the replay discharges (RF-1); three
corrections to the record’s wording and registry rows (RF-3 to RF-5); and a control the
replay lane must add (RF-6). Four are notes.
`S2` is confirmed (§12).

## 3. The Argument From Certificate to Bound

**Theorem (R071).** Let $s(17)$ be the least side of a closed square containing
seventeen closed unit squares with pairwise disjoint interiors, each at any orientation,
boundary contact allowed.
Then $s(17) > 18641771/4000000$.

The reduction, the charging argument, the strict cores, the Möbius-expanded event sweep,
the boundary argument and the compactness step are those of §3 of the
[4.640020 review](review-2026-09-27-n17-kleddamag-4640020.md) and §3 of the 2026-09-28
review. `BOUND_PROOF.md` states the same steps in the same words as R068’s and R070’s
`PROOF.md`, with $A = L/T = 18452000/18641771$ and 5,114 intervals.
It differs from R070’s only in the paragraph on the records, which cites a completion
summary where R070 cites complete ledgers, and in a closing note that the old partitions
are missing and CI was not observed.

| # | Step | Status here | Touched by R071’s parent side or cores |
| --- | --- | --- | --- |
| 1 | D4 invariance from complete orbits with one weight each; a parent at $\theta \in (\pi/4, \pi/2)$ is reflected alone across the container diagonal | Proved; completeness re-derived for all 7,048 rule images and 2,621 point orbits | No: the charge is R068’s byte for byte |
| 2 | Rational half-angle parameterisation, $c(u) = (1 - u^2)/(1 + u^2)$, $s(u) = 2u/(1 + u^2)$ | Proved | No |
| 3 | A gapless chain from $0$ to $207107/500000$, where $u^2 + 2u - 1 = 309449/250000000000 > 0$, so past $\tan(\pi/8)$ | Verified here; every R068 and R070 endpoint is an endpoint | Yes: 123 more intervals than R068, the same two ends |
| 4 | Strict core containment at both endpoints, $A - B h > 0$ | Verified here exactly at every row; least margin $1.0001596 \times 10^{-12}$ | Yes: every core side is new |
| 5 | The endpoint check holds over the whole interval | Proved in the 2026-09-28 review; checked here exactly at five interior points of every row | The lemma is unchanged; its hypotheses are re-checked |
| 6 | $[r, L - r]^2$ holds every legal parent centre, $r = A \min_{u \in \{a, b\}} (c(u) + s(u))/2$ | Proved there; checked here at five interior points of every row | The lemma is unchanged; $r$ is new with $A$ |
| 7 | Capture is a closed rectangle in core coordinates; Möbius inversion makes each rule a signed sum of rectangles | Proved; the identity re-checked for all 86 patterns | No |
| 8 | Signed accumulators exact: absolute mass below $2^{50}$ | $176{,}068{,}082{,}656 \approx 2^{37.4}$, re-derived | No |
| 9 | The exact minimum over every open cell meeting the envelope, at every interval | The source’s three-partition summary reports $\Gamma$; no row record exists; 227 rows reproduced here; complete replay pending | Yes: every row’s cells are new |
| 10 | Boundary and event centres by upper semicontinuity of the monotone closed-capture charge | Proved | No |
| 11 | Capacity one for all 86 rule patterns, and the budget $M$ | Re-derived here | No |
| 12 | Counting, then scaling and compactness for the strict inequality | Proved | Only through the value $T$ |

**Why steps 5 and 6 carry over unchanged.** The two proofs in §3 of the 2026-09-28
review use no property of $A$, $B$ or $t$ beyond the endpoint checks themselves.
Step 5: with $\delta(u) = \theta(t) - \theta(u)$ monotone in $u$, the endpoint checks
`dot > 0` and `|cross| ≤ dot` put $\delta(a)$ and $\delta(b)$, hence all of
$\delta([a, b])$, in $[-\pi/4, \pi/4]$, where
$\cos \delta + |\sin \delta| = \sqrt{2} \sin(|\delta| + \pi/4)$ increases with
$|\delta|$, so its maximum over the interval is $h$, and $A - B h > 0$ puts the closed
core strictly inside the open parent at every angle of the interval.
Step 6: a parent at angle $\theta$ has legal centres
$[A(\cos\theta + \sin\theta)/2, L - A(\cos\theta + \sin\theta)/2]^2$, and
$\cos\theta + \sin\theta$ is concave on $[0, \pi/2]$, so its minimum over the interval
is at an endpoint and $[r, L - r]^2$ contains every legal centre.
R071 changes $A$, so it changes $r$ and every margin, and both are recomputed here; the
lemmas themselves are R068’s and need no new proof.
The citation for both remains §3 of the 2026-09-28 review, as its F2 asked.

**The counting.** Each certified core is closed and lies strictly inside its open
parent, so seventeen parents with disjoint interiors have pairwise disjoint cores.
A site then lies in at most one core, and the winning subsets a rule captures in
different cores are disjoint, so a rule fires in at most its capacity of cores, which is
one for every pattern here; the total charge of the seventeen cores is at most $M$. Each
core carries at least its row’s minimum, at least $\Gamma = 1{,}000{,}026{,}844$ as
reported, so $17\Gamma \le M$, which fails by $17\Gamma - M = 7{,}404$. The requested
threshold alone would do: $17 \times 1{,}000{,}026{,}409 - M = 9 > 0$. A packing of
seventeen unit squares in a square of side $S \le T$, scaled by $L/S$, gives squares of
side at least $A$, each holding a concentric parent of side $A$ at its own orientation,
so none exists at any $S \le T$; centres and orientations range over a compact set and
the conditions are closed, so $s(17)$ is attained, and $s(17) > T$.

## 4. Hypotheses the Checkers Assume

Each is what the 2026-09-28 review listed for R068; for each, what binds it for R071.

1. **The certificate is the one reviewed.** `replay.js` hashes it before and after the
   run and every partition must name the same digest; `run_public.js` asserts
   `15b6bf6a…`. Recomputed here from the retained bytes.
2. **The site order.** Rule `sets` index the physical sites in one order: each point
   orbit’s distinct D4 images, sorted by $x$ then $y$, appended in orbit order.
   Both checkers use it, and so does this review’s sweep, which reproduces R068’s and
   R070’s published rows with it, cell counts included.
3. **Complete D4 orbits with one weight each.** Checked by both checkers; re-derived
   here for all 889 rule orbits (exact tuples for winning-subset rules, coefficient-site
   multisets for threshold rules) and all 2,621 point orbits, 20,860 distinct sites in
   the closed container.
4. **Capacities.** The budget counts $\lfloor \sum a_i / k \rfloor$ per threshold image
   and one per winning-subset image, whose masks are pairwise intersecting; the C++
   checker also proves by dynamic programming that each exact capacity is at most the
   claimed one. Re-derived here: exact capacity and formula capacity are one for all 86
   patterns, and $M = 17{,}000{,}448{,}944$ from the orbits.
5. **Exact accumulation.** Absolute signed mass $176{,}068{,}082{,}656 < 2^{50}$, so the
   Node checker’s `Float64Array` segment tree and the C++ `int64` one are exact.
6. **The chain and the representatives.** $a_0 = 0$, $a_{i+1} = b_i$, $a < b < 1$, the
   last endpoint past $\tan(\pi/8)$; every $t$ is its interval’s exact midpoint and
   satisfies $t^2 + 2t - 1 \le 0$, which the C++ sweep requires ($C \ge S$).
7. **The geometry contract at both endpoints**, `dot > 0`, `|cross| ≤ dot`, $0 < B < A$,
   $A - Bh > 0$, $B(c(t) + s(t))/2 \le r < L/2$; checked exactly here at every row.
   The two lemmas of §3 extend the endpoint checks to the interval (prose, proved).
8. **The cells.** The minimum is taken over the open cells meeting the closed vertical
   extent of the rotated envelope in each open slab; degenerate rectangles are skipped
   and coincident ones merged, which changes no value on an open cell; boundary centres
   are covered by upper semicontinuity (prose, proved).
9. **Closed containment, interior disjointness, boundary contact allowed**: the envelope
   is the closed $[r, L - r]^2$ and capture is closed.
10. **The launcher’s comparison.** `replay.js` requires both checkers’ processes to exit
    0, every partition’s range, status, budget, threshold and digest, row-by-row
    equality of minimum and cell count, every row at or above the requested threshold,
    and $17\Gamma - M > 0$, before it writes `THEOREM.json`.
11. **The meaning of `minimum_units`.** In the certificate it is the requested threshold
    $\lceil M/17 \rceil = 1{,}000{,}026{,}409$; in `THEOREM.json` and the C027 summary
    it is the least row minimum, $\Gamma$. F3 of the 2026-09-28 review carries over.

## 5. What Changed From `T-043`

**The charge is unchanged.** The parsed `point_orbits` and `threshold_orbits` of R071
equal R068’s, as do `L`, both denominators, `budget_units` and `minimum_units`: 2,621
point orbits over 20,860 sites, four of them weighted ($11{,}734$ each, R068’s added
orbit at $(1.34, 1.34)$), and 889 rule orbits of 7,048 images and 86 patterns.
The `research_provenance` block is R070’s and R068’s, with the same two point-orbit
changes from Kleddamag’s baseline and `"prior_full_geometry_acceptance_reused": false`.

**The parent side** is $A = 18452000/18641771$, so $L/A = 18641771/4000000$ exactly.
$A_{\mathrm{R068}}/A_{\mathrm{R071}} = 18641771/18641760$, a relative shrink of
$5.9 \times 10^{-7}$. The bound rises by $11/4000000 = 2.75 \times 10^{-6}$ over R068,
$1/20000000$ over R070.

**The intervals.** R070 keeps every R068 endpoint: 4,888 intervals kept, 101 bisected
exactly, one cut into 5 and one into 12, giving 5,107. R071 keeps every R070 endpoint
and bisects seven intervals exactly, giving 5,114; over R068 that is 4,885 kept, 104
bisected, one in 5 and one in 16. The seven fall in two groups: R070 rows 3143, 3145,
3146 and 3149, near $\theta = 38.66^\circ$ in the narrowest part of the catalogue,
become R071 rows 3143–3144, 3146–3149 and 3152–3153; R070 rows 4193, 4243 and 4294, near
$\theta = 42.25^\circ$ to $42.29^\circ$, become R071 rows 4197–4198, 4248–4249 and
4300–4301. Every representative is still its interval’s midpoint.
The narrowest rows, 3146 to 3149, are $207107/16777216000000 \approx 1.2 \times 10^{-8}$
wide in half-angle, $1/16384$ of the base width.

**The cores.** All 5,100 intervals R071 shares with R070 keep their core’s angle and
take a strictly smaller core side; none keeps its core, and no core side is R070’s
scaled by $A_{\mathrm{R071}}/A_{\mathrm{R070}}$. The margins $A - Bh$ run from
$1.0001596 \times 10^{-12}$ (row 2647) to $1.9999311 \times 10^{-12}$, where R068’s ran
from $1.0000007 \times 10^{-12}$ to $1.0002021 \times 10^{-12}$; $B/A$ reaches
$0.999999989$ at the narrowest rows.
In exact arithmetic a positive margin of any size is a proof, as F4 of the 2026-09-28
review said of R068’s.

**“All 5111 core intervals rebuilt.”** The certificate’s `source` string gives 5,111
where it holds 5,114 intervals.
What the bytes show: the four bisections near $38.66^\circ$ give both halves one core
side each, and the three near $42.25^\circ$ to $42.29^\circ$ give each half its own;
R070’s 5,107 intervals plus the first four are 5,111. That is consistent with an
intermediate catalogue of 5,111 intervals, every core rebuilt, to which the three later
bisections were added without the string changing; it is not proved by the bytes, and
nothing else in the packet mentions 5,111. It does not matter to the bound: neither
checker reads `source` (the C++ front-end reads `L`, `A`, `normalized_target`, the two
denominators, the orbits, `budget_units`, `minimum_units` and `entries`, and the Node
checker the same fields but the weight denominator), the summary and `run_public.js`
both count 5,114, and every one of the 5,114 rows is checked above.
The certificate’s `created_utc` is likewise a label: it reads `2026-10-01`, while the
summary of the run over these bytes is stamped `2026-09-30T18:01:29.899Z`, so it is the
author’s local date in UTC+8.

## 6. Evidence Re-Derived Here

**Premises** (`premises.py`, all three certificates).
The SHA-256 of each; $L/A$ equal to each target; the charge of R070 and R071 equal to
R068’s; D4 expansion to 20,860 distinct sites, four weighted, all in the closed
container; every rule orbit the exact D4 image set of its first member; the 86 patterns,
each of exact capacity one by dynamic programming over minimal winning sets and of
formula capacity one; the Möbius identity for each; $M$ equal to `budget_units`; the
requested minimum equal to $\lceil M/17 \rceil$; the absolute mass; every row’s six
contract inequalities, and the containment and envelope at five interior points of every
row; every chain gapless from 0 and past $\tan(\pi/8)$; every representative a midpoint
at or below $\tan(\pi/8)$; the refinements R068 ⊂ R070 ⊂ R071 of the endpoint sets, with
the piece counts of §5; and the core comparisons of §5. Controls: R068’s least margin,
$952933981168979477888243189701088457479269241/952933310781657455908355581458029346772069241 \times 10^{-12}$,
is the value the 2026-09-28 review and R068’s C++ ledger give; R070’s,
$2841821827556535860368883518555127286690306535927/2841168301217205113722798488244261580337539919330750000000000$,
is the value R070’s published C++ header gives.
R071’s least margin is
$$
\frac{15923658553101702964643878656034963576202697}{15921117963709509270343578017641703022637690727500000000}
\approx 1.0001595736 \times 10^{-12},
$$
at row 2647, the value the replay’s fresh C++ header must report.

**The sweep** (`rowsweep.py`). Sites, core side and envelope corners on one integer grid
per row, in coordinates rotated to the core; each Möbius term’s capture rectangle; an
`int64` value array over the vertical cells, updated slab by slab; the minimum over the
open cells meeting the closed vertical extent of the rotated envelope; then the argmin
cell’s midpoint mapped back to the container and the charge evaluated there from the
original closed predicates in `Fraction`s, site by site and rule by rule.

- *Controls.* R068 rows 0, 3117, 3119 and 4990, and R070 rows 0, 1000, 2000, 2553 (a
  partition start), 3000, 3143, 3145, 3146, 3149, 4000, 4193, 4243, 4294 (the seven R071
  bisects), 4336 (R070’s least margin), 5000 and 5106: at all 20 the minimum **and the
  cell count** equal both published ledgers, and the direct evaluation equals the
  minimum.
- *R071.* 227 rows, 278.5 CPU-seconds: every 25th row from 0 to 5100; the 14 rows R071
  adds; row 2647, the least margin; rows 1704 and 3409, which start the second and third
  partitions of the source’s three-partition run, and 2556 and 2557, either side of the
  two-partition split the replay uses, with their neighbours 1705 and 3410; and rows 1
  and 5113. At every one the minimum is $1{,}000{,}026{,}844$, and the direct evaluation
  at the argmin cell returns it.
  The JSON array of `[interval, minimum, cells]` triples for all 227 rows in row order,
  with no whitespace, has SHA-256
  `2b8ebed93219c140b0562bdf8de25c93457a899a2ec14aa60aac68cfdf71b7de`, and the cells sum
  to 100,338,354,491. The rows that matter most:

| R071 row | Why sampled | Cells |
| --- | --- | ---: |
| 0 | first | 416,302,717 |
| 1704, 1705 | start of the source’s second partition | 450,194,257; 450,164,973 |
| 2556, 2557 | either side of the two-partition split | 439,904,029; 439,902,613 |
| 2647 | least containment margin | 439,418,109 |
| 3143, 3144 | halves of R070 row 3143 | 436,767,945; 436,767,945 |
| 3146, 3147 | halves of R070 row 3145, the narrowest rows | 436,767,945; 436,767,945 |
| 3148, 3149 | halves of R070 row 3146, the narrowest rows | 436,767,949; 436,767,941 |
| 3152, 3153 | halves of R070 row 3149 | 436,767,945; 436,767,937 |
| 3409, 3410 | start of the source’s third partition | 434,312,933; 434,311,165 |
| 4197, 4198 | halves of R070 row 4193 | 434,392,537; 434,392,369 |
| 4248, 4249 | halves of R070 row 4243 | 434,385,825; 434,385,765 |
| 4300, 4301 | halves of R070 row 4294 | 434,384,237; 434,384,361 |
| 5113 | last | 435,195,593 |

Every row in the table has minimum $1{,}000{,}026{,}844$. Across the 227 rows the core
captures 351 to 406 sites at the argmin cell, as at R068.

**The corner** (`corner.py corner`, all 5,114 rows of R071). For each row the certified
core, side $B$ at angle $\theta(t)$, is centred at $(r + 10^{-9}, r + 10^{-9})$, a legal
centre for the endpoint angle that sets $r$, and its charge is evaluated on the original
closed predicates. That charge bounds the row’s true minimum from above.
It is exactly $1{,}000{,}026{,}844$ at every one of the 5,114 rows.
So no row’s minimum lies above the reported $\Gamma$; with the source’s report that none
lies below it, every row sits at $\Gamma$, which is what the replay’s ledger should
show. At the 227 sampled rows the corner attains the minimum, as the 2026-09-28 review
found for R068. The check runs one way only: a row whose true minimum were lower would
pass it.

**R070’s obstruction parent** (`corner.py obstruction`). At $T' = 186417711/40000000$,
the parent of side $L/T'$ at half-angle $350755760770591/10^{15}$ centred at
$(1915223443770787, 695624205775549)/10^{15}$ is legal, with $2.1 \times 10^{-11}$ to
spare at the bottom wall.
Its open interior holds 1,426 sites and fires 474 of the 7,048 rule images, and its open
charge is exactly $999{,}880{,}603$, so $17F - M = -2{,}478{,}693$: the source’s
figures, all of them.
At R071’s side the same pose crosses the bottom wall by $3.7 \times 10^{-9}$ and is not
legal, so it does not bear on R071 itself (RF-7 says what it does bear on).

None of this decides R071: 227 of 5,114 rows is a sample, and the corner check runs one
way only.
What it does is test the certificate where R071 differs from R068, at every row
it adds, with an instrument that reproduces published ledgers exactly, and find nothing.

## 7. The Trust Boundary

**The deciding programs** are the source’s own two, run by its own launcher:
Guzhou0806’s `verify.cpp` (`3ba09554…`, its front-end “adapted from Kleddamag’s MIT
general-rule checker”, its geometry backend `native_geometry.hpp`, Guzhou0806’s R052
kernel) and Kleddamag’s `reference/verify_global_variable.js` (`c2209186…`), both run by
`replay.js` (`1125e596…`) under `run_public.js`. The 2026-09-28 review read the C++
checker and the launcher in full, and the 4.640020 review the Node checker line by line;
the bytes are unchanged, so this review read again only the Node checker, the launcher
and the fields the C++ front-end takes from the certificate.
`run_public.js` is new and was read here.
Its `bound` path requires `check_package.js`, which checks every `MANIFEST.json` entry’s
size and digest (so the sixteen pinned upstream files must be restored from the R068
packet and the `.gz` files decompressed), compiles `verify.cpp` at `-O3 -std=c++17`,
runs `replay.js` at two partitions, and asserts the `THEOREM.json` status, target,
interval count, minimum, budget, surplus and certificate digest.
It decides nothing itself.

**What the two share, and the relation.** Both decide the certificate by the same
event-cell method: the same certificate format and site order, the same Möbius
expansion, a slab sweep over a lazy segment tree, the same cell selection and the same
safe-integer guard. They differ in language, arithmetic library and author, and the C++
adds the capacity check.
The launcher that runs and compares them is the source’s. So the replay is **reproduced
with the producer’s code**: `relationship_to_generator:
same-implementation`, as for `E-n017-guzhou-r068-source-replay`, with one method and two
implementations. `devtools.audit_guzhou_r071 compare` is a premise check and sets no
relation.
This review’s sweep is a third implementation of the same method that shares no
code; it decides 227 rows and is not retained, so it supports the reading and is no part
of the rung.

**What is trusted.** The two lemmas of §3 (prose, proved), the closed-capture semantics,
the compiler and Node runtime, and the source’s certificate as the statement checked.
What the checkers decide: every premise of §4 that is computational, and the exact
minimum of every row.
Nothing in R071 asks a reader to trust R070: its certificate is self-contained, and
`"prior_full_geometry_acceptance_reused": false` says no earlier acceptance was reused.

## 8. The Missing Records, the Source’s CI, and What the Replay Must Show

**The completion summary.** `C027_GLOBAL_THEOREM.json` reports
`PASS_COMPLETE_CPP_AND_BIGINT_EXCLUSION` for the certificate’s digest over 5,114
intervals, budget 17,000,448,944, minimum 1,000,026,844, surplus 7,404, six processes (a
C++ and a BigInt checker on each of three partitions) exiting 0 in 1,694.142 s, and as
checker and launcher digests Kleddamag’s BigInt checker and `replay.js` as the R068
packet retains them; its executable digest `8f4d59ac…` is the source’s own build, the
one its R068 and R070 runs record.
What it supports: that the source ran the paired launcher over this certificate and that
the launcher wrote a passing theorem, which by §4 item 10 implies row-by-row agreement
if the launcher ran as published.
What it does not support: any row’s minimum or cell count, which C++ build ran, or any
of it here. `BOUND_PROOF.md`, `README.md` and `REPRODUCIBILITY.md` say so plainly: the
C027 partition records “remain missing”, the summary “does not imply current CI
success”, and the public launcher “must regenerate and compare them row by row”.
The source also says that 276 historical C020 files are missing and that an external
sealed-archive audit cited by its C029 documents was not received; neither bears on
C027.

**The source’s CI.** Run 36788162356 of `r071.yml` on `8c11f696`, retrieved through the
GitHub API on 5 October, concluded `success`; its `replay (bound)` job ran
`run_public.js bound` on a GitHub-hosted runner with Node 22 and the distribution’s
`g++` and Boost in 16 min 43 s, and every step succeeded.
That supports one more thing: that the source’s own code, in a run its publisher did not
watch, regenerated the rows and passed `run_public.js`’s assertions, so a complete C++
and BigInt ledger of R071 was written, and the packet reads the artifact `r071-bound` as
holding it. It is the source’s replay, under a workflow in the source’s repository, with
outputs this session could not fetch (the artifact host refused the egress); the
artifact expires on 29 December 2026. It is not a replay here and not a third party’s,
and the register’s `V0` with `replay_status: not-attempted` reads it rightly.

**What the complete replay here must show** for the exit, beyond exit 0 and the receipts
committed:

| Quantity | Value |
| --- | --- |
| `node check_package.js` | `PASS_BYTES_ONLY`, with the pinned upstream files restored from the R068 packet and checked against their digests |
| `REPLAY.json` | `PASS_R071_C027_GLOBAL_REPLAY` |
| `THEOREM.json` | `PASS_COMPLETE_CPP_AND_BIGINT_EXCLUSION`, target `18641771/4000000`, intervals 5114, budget `17000448944`, minimum `1000026844`, surplus `7404`, certificate `15b6bf6a…`, reference `c2209186…`, launcher `1125e596…`; the executable is a local build and differs from `8f4d59ac…` |
| Fresh ledgers | two C++ and two BigInt partitions, rows 0–2556 and 2557–5113, each naming the certificate digest, budget and requested threshold `1000026409` |
| Row agreement | `audit_guzhou_r071 compare R071 FRESH --published FRESH`: 0 mismatches over $4 \times 5{,}114$ rows, minimum and cell count |
| C++ header | `sites` 20860, `signed_terms` 49208, `minimum_strict_margin` the fraction in §6 |
| Least row minimum | `1000026844`; if any row is higher, `intervals_at_minimum` and `next_minimum_units` say so, and nothing here depends on the ledger being flat |
| This review’s sample | the 227 sampled rows of §6 equal in minimum and cell count, by the triples digest given there |
| Controls | two mutated certificates refused by both checkers, and a test that holds them (RF-6) |

## 9. R070, and the Results That Carry No Bound

**R070’s handling is right.** R070 was published on 29 September, superseded by R071 on
30 September, and retained with it on 5 October.
It is the base R071’s certificate names (`base_sha256`), its four C++ and four BigInt
partitions agree row by row (the packet’s receipt; this review’s sweep reproduces 16 of
its rows exactly), and it was never replayed here.
Under the claim table of
[`result-import.md`](../../../packing/campaign/result-import.md) and the scope rule of
[`epistemics.md`](../../../epistemics.md#results-by-others), a result by others enters
the register when its bound is or was a case’s reported or verified bound, or when it
has been or is queued to be replayed or reviewed here.
R070’s bound never was: the case’s reported lower bound went from R068 to R071 in one
import. It is not queued for replay, since R071’s replay covers it, and it is below the
standing reported bound and asks for no work, so it stays in the packet and the case
record, as the register’s note for `T-093` says.
This review reads R070’s certificate and ledgers as R071’s base and as a control of its
instrument; it does not review R070 as a claim, and records no verdict on it.
One contingency: if R071’s replay fails, R070 is the next candidate for the verified
field (RF-8).

**R070’s `GEOMETRIC_RESULTS.md` carries no bound.** Its same-budget overlay upgrades 319
orbits (2,552 images) to winning-subset rules whose winning sets have pairwise
intersecting convex hulls, with capacity one by the hull argument, and checks that the
enhanced charge dominates the original everywhere with the same budget; it inherits the
$4.6604427$ conclusion and says it “does not claim a separate full centre scan” or a
higher target. Its obstruction fixes one parent at $T' = 186417711/40000000 =
4.660442775$ and shows that within one class of fixed-weight enhancements that parent’s
charge cannot rise; the source says this blocks a uniform per-parent proof in that class
and nothing wider, and is neither an upper bound on $s(17)$ nor whole-dictionary
infeasibility. Both readings are faithful.
What the obstruction does say about R071, recomputed here, is RF-7: R071 sits within
$1/40000000$ of the reach of this charge.

**R071’s conditional joint geometry carries no bound.** `GEOMETRY_PROOF.md` (C028 and
C029) fixes $T = 9321/2000 = 4.6605$ and one first-anchor box: centre midpoint
$(1915223443770787, 695624205775549)/10^{15}$ with half-widths $1/50$, half-angle
$350755760770591/10^{15}$ with half-width $1/100$, the pose of R070’s obstruction
parent.
For legal anchors in that box it covers the parents that avoid a 16-point grid by
18 components of capacity one, finds 17 conflict edges and 2 forced holes, bounds the
number of such parents by $V_{\max} \le 11$, and exhibits a partial packing family with
nine, so $9 \le V_{\max} \le 11$; eight component pairs are unknown, the single-avoider
branch keeps 16 components, and other anchors are not covered.
The source says it “does not prove s(17)>4.6605” and “cannot be converted into a global
exclusion”, and `PUBLICATION_STATUS.json` has `"c029_new_global_bound": false`. Its
scope is a conditional case analysis at one target inside one box; it proves no bound on
$s(17)$, and this review did not check its mathematics beyond its scope statements.
Nothing in the record overstates it: `T-093` does not mention it; the evidence entry,
the case record, the coverage entry, the bibliography row and the packet README each
call it conditional, at $9321/2000$, inside one first-anchor box, and not a bound.
The packet README’s “bounds the number of avoiding parents by $9 \le V_{\max} \le 11$”
is the source’s own statement.

## 10. Credit and the AI Statement

Read against the package’s own files:

- **The result.** R071’s `ATTRIBUTION.md`: the improvements to $4.6604427$ and the
  retained $4.66044275$ “belong to AI-assisted research in the Guzhou0806/N17 project;
  they are not new results of Kleddamag”.
  `T-093` credits Guzhou0806 / N17 project, as do the evidence entry, the case record
  and the bibliography key.
- **Kleddamag.** “The original 4.66001 framework, proof and independent JavaScript
  checker originate from the pinned Kleddamag commit.”
  `T-093` says the package credits Kleddamag “for the 4.66001 framework, proof and
  BigInt checker”, and the evidence entry “for the 4.66001 charge, proof and BigInt
  checker”. Faithful: the checker is the JavaScript BigInt one, and the charge is the
  4.66001 charge with Guzhou0806’s two point-orbit changes, which `T-093`’s first
  paragraph states as “the charge of R068”.
- **The lineage.** The package retains the twelve upstream notices R068 retained, byte
  for byte, crediting Mira-acc/17squares, Guzhou0806’s R038 and Joshua Levy’s squares
  project. The bibliography’s `credit: Guzhou0806 after Kleddamag, Mira, Levy` and
  `short_credit` are R068’s, and the claim’s parenthesis, “Kleddamag building on Squares
  Project (Joshua Levy), Mira and Guzhou0806”, names every link the source names, as
  [epistemics.md](../../../epistemics.md#parallel-projects-and-their-credit) asks.
  The `ATTRIBUTION.md` adds that “Nagamochi’s measure, chelokot’s repair/compensation
  proof and Lean work, and other upstream algorithms retain their original attribution”,
  without saying what in the package rests on them; the certificate’s provenance names
  only Kleddamag’s commit and the source’s own C007 and C009 steps, so the credit line
  rightly does not add them, and the bibliography note quotes the sentence (RF-9).
- **The AI statement.** The source’s terms are “AI-assisted research” (R071) and
  “AI-assisted work in the Guzhou/N17 project” (R070). The register says the package
  “discloses AI assistance”, the case record that its publisher “discloses AI
  assistance”, and the bibliography note quotes the source.
  That meets the rule that a register entry or case record say so in the source’s own
  terms.
- **No further claims.** The package claims no world record, priority, optimality, Lean
  formalization or human peer review, and says that agreement of two implementations is
  neither formalization nor independent human peer review.
  No record says otherwise.
- **The date.** `attribution.published: 2026-09-30` is the UTC date of `8c11f696`
  (22:53:43Z), the first commit holding `bounds/c027/certificate.json`. The certificate
  did not exist at R070’s commit (2026-09-29T07:56:05Z): the run over its bytes is
  stamped 2026-09-30T18:01:29Z, its digest appears in none of R070’s files, and its own
  creation date is 1 October in UTC+8, after 16:00 UTC on 30 September.
  The source gives no publication date of its own, so the rule of result-import’s stage
  3 takes the commit’s UTC date.
  The bibliography’s `dated: 2026-09-30` agrees.

## 11. Claims by Evidential Status

- **Proved, and carried over unchanged from the 2026-09-28 review:** the reduction, D4
  folding, the two lemmas of §3, the Möbius rectangles, upper semicontinuity at
  boundaries, capacities, the counting and compactness.
- **Recomputed here in exact arithmetic, every row:** the target identity; the charge’s
  equality with R068’s; orbits, sites, capacities, budget, requested minimum, absolute
  mass; the chain, its ends and refinements; every core’s containment margin and
  envelope, at the endpoints and at five interior points.
- **Decided here by an independent exact sweep, 227 of 5,114 rows:** each sampled row’s
  minimum is $1{,}000{,}026{,}844$, with its cell count; the same instrument reproduces
  20 published rows of R068 and R070 exactly.
- **Bounded above here, every row:** the charge of a certified core at a legal corner
  centre.
- **Asserted by the source, not verified here:** the exact minimum at the other 4,887
  rows, the completion summary, and the CI run’s outputs.
- **Research material, no bound:** R070’s overlay and obstruction, R071’s conditional
  geometry.

## 12. Significance

**`S2` confirmed.** The score is of the claim as it would stand after a passing replay:
the case’s verified lower bound, $2.75 \times 10^{-6}$ above `T-043`. Compared with the
nearest entries:

- `T-042` (R067, `S2`) is the same construction, Kleddamag’s charge unchanged with a
  finer catalogue and rebuilt cores at a smaller parent, and R071 is that construction
  again on R068’s charge, adding no orbit, rule, weight or method.
- `T-043` (R068, `S3`) moved the bound by $43/100000$, 156 times R071’s step, and
  changed the charge: it moved one site orbit and added a weighted point orbit.
- `T-039` (R052, `S3` “at the low end”), the precedent the draft weighs, moved the bound
  by $0.000229$, 83 times R071’s step, by adding three-of-five groups to the
  architecture it continued; it held the verified field for two days.

What R071 would add to `T-043` is the same theorem with the constant raised in its
seventh significant digit, $0.018\%$ of the gap from R068 to Bidwell’s $4.67553009$.
Holding the verified field is a fact about the frontier, and
[epistemics.md](../../../epistemics.md#significance-and-novelty) scores the claim, not
the frontier. The obstruction of RF-7 adds that this is the end of the recipe, not an
opening.
A citable detail that changes no theorem in substance: `S2`. A reader who weighs
the verified field above the size of the step would score `S3` by `T-039`; the score
gates nothing.

## 13. The Rung

Under the ladder in force since 2026-09-30:

- **Now, once this review is recorded:** `V0/C1`. The review is a qualifying read of the
  reported evidence (`external_review.state: informally-verified`), and a read of a
  recorded claim is the one case where `C` may exceed `V`. The status reads *reviewed*.
- **When the complete replay passes and is recorded** as `origin: replayed-here`,
  `method: exact-algebraic`, with the certificate, the replay command and
  `replay_status: passed`: `V3/C3`, and the verified lower bound of n = 17 moves to
  $18641771/4000000$ with `T-043` superseded.
  Its `relationship_to_generator` is `same-implementation`, listing
  `V-guzhou-n17-verify-cpp` and `V-kleddamag-n17-verify` as deciders and the audit as a
  premise check (RF-5). `C3` also needs a control path (RF-6).
- **Not `V4/C4`.** Rung 4 needs two retained adversarial AI reviews by distinct
  reviewers whose latest verdict accepts the claim, and a retained human oversight
  record, on the confirming side for `C4`. This review is one adversarial AI review with
  `relation: project`; `T-043` stands at `V3/C3` for want of the same, and its own
  2026-09-28 review is not in its `reviews` (its `next_rung` leaves that to the owner).
  A second reviewer of another model family or a separately prompted lane, and the
  owner’s oversight record, would raise both.
- **Not a second method.** One event-cell method, two implementations; the native
  parent-core route still cannot read the winning-subset and weighted features, so
  `T-043`’s `next_rung` on that applies unchanged.

## 14. Findings

Severity is blocking, non-blocking or note.
**None is blocking.**

### RF-1 — Non-blocking: no row of C027’s sweep can be read here

The source retains a completion summary of its three-partition run and says its
partition records are missing; its CI regenerated the rows in an artifact this session
could not fetch. Until the replay here, every row’s minimum but the 227 sampled here is
the source’s statement.
This is why `V0/C0` is right now and why the replay, not this review, moves the bound.
Discharged by the replay.
If the replay lane can fetch the `r071-bound` artifact before 29 December 2026, its rows
are a second comparison, not a substitute.

### RF-2 — Note: the certificate’s `source` string and `created_utc` are labels

“All 5111 core intervals rebuilt” where the certificate holds 5,114 intervals, and
`created_utc: 2026-10-01` for a certificate verified on 30 September UTC. Neither
checker reads either field; the bytes are consistent with an intermediate catalogue of
5,111 intervals (§5); the record already quotes the string without relying on it.
Nothing to change; a reply may mention it once.

### RF-3 — Non-blocking, in the record: the summary does not name the executable R068’s replay here ran

`E-n017-guzhou-r071-report` says the summary names, “as checker, launcher and
executable, the bytes R068’s replay here ran”.
It names the BigInt checker and the launcher R068’s replay ran, and the executable
digest `8f4d59ac…` of the source’s own build, which its R068 and R070 runs record;
R068’s replay here built `cf761bb5…`. `T-093`’s “naming the checker bytes T-043’s replay
ran” and the case record’s “names the checker bytes R068’s replay here ran” are right
for the BigInt checker and the launcher only, and the summary names no C++ source digest
at all. `devtools.audit_guzhou_r071 summary` reports it correctly
(`executable_is_r068_and_r070_runs`). Correct the sentence when the exit rewrites the
claim.

### RF-4 — Non-blocking, in the record: “minimum core charge 1000026844 on every interval”

`T-093` says the source reports that minimum “on every interval”.
The source reports the least row minimum over all 5,114 intervals (`minimum_units` in
the summary; “actual Γ=1000026844” in `BOUND_PROOF.md`), which bounds every row from
below and says nothing of a flat ledger; R068’s and R070’s ledgers are flat, and every
row sampled here is at that value, but R071’s source does not say so.
Say “a least core charge of 1000026844 over all 5,114 intervals”, or state the replay’s
own count at the exit.
In the same claim, “on Kleddamag’s charge” in the credit paragraph is looser than the
first paragraph’s “on the charge of R068”; the case record’s “on R068’s continuation of
Kleddamag’s $4.66001$ charge” is the exact form.

### RF-5 — Non-blocking, in the registry: the BigInt checker that runs has no version entry

`V-kleddamag-n17-verify` lists the digests and paths of Kleddamag’s Python `verify.py`,
which no Guzhou0806 launcher runs; the program `replay.js` runs is
`reference/verify_global_variable.js`,
`c22091862df631f8cfd1f1bb8e5013f0b9c216f20be268fcd7104768919c49b7`, retained in the R068
packet, and the row records neither its digest nor its path.
`V-guzhou-n17-verify-cpp` records `verify.cpp` at `815b1626` only, and neither row
records `replay.js` (`1125e596…`) or R071’s `run_public.js` (`45f6ef8e…`);
`devtools.audit_guzhou_r071` is not registered.
Stage 4 asks the replay entry to name every program it runs with the digest that ran and
the retained path of its source.
The gap is `T-043`’s too; close it at this exit.

### RF-6 — Non-blocking, for the replay lane: no mutated-certificate control holds these checkers

Stage 4 asks that two mutated certificates be refused by every checker that accepted the
original, and that a test hold them.
`test_guzhou_r071_packet.py` mutates a published row and a summary, and
`test_guzhou_r068_packet.py` a row and a partition; neither feeds a mutated certificate
to either checker, and R067’s twelve controls are a receipt without the script that made
them. Before `C3`, run two through both checkers, for instance one core side raised past
$A/h$ at one row (refused as `strict core`) and one rule weight raised so the recomputed
budget differs from `budget_units` (refused as `exact budget`), and hold the refusals in
a test.

### RF-7 — Note: R071 is at the end of this charge

R070’s obstruction gives a parent at $T' = 186417711/40000000$, $1/40000000$ above R071,
whose open charge is below $M/17$. Recomputed here (§6): the parent is legal at $T'$ and
its open charge is exactly $999{,}880{,}603$, against $M/17 = 1{,}000{,}026{,}408.47$.
Every core inside it charges no more, and a legal parent shrunk about its centre stays
legal and charges no more, so this fixed charge cannot prove any $T \ge T'$ by
per-parent counting, whatever the cores.
If R071’s replay passes, the reach of the charge lies in
$[18641771/4000000, 186417711/40000000)$, an interval of width $2.5 \times 10^{-8}$. Any
further step needs a new charge, a reweighting, or an argument across parents, which is
what R071’s conditional geometry starts on the same pose.
This sharpens F5 of the 2026-09-28 review and is why §12 reads R071 as the end of a
recipe. It is a fact about the method, not a bound on $s(17)$.

### RF-8 — Note: R070 is the fallback if R071’s replay fails

R070’s certificate is self-contained, its published ledgers are complete and agree, and
its bound is $27/10000000$ above `T-043`. If R071’s replay fails, R070’s replay, priced
the same, is the next step for the verified field, and R070 then needs a register entry
of its own under the scope rule.
Nothing is needed while R071’s replay is pending.

### RF-9 — Note: the attribution names Nagamochi and chelokot without a part

R071’s `ATTRIBUTION.md` says Nagamochi’s measure and chelokot’s repair/compensation
proof and Lean work retain their attribution, and does not say what in the package rests
on them. The C027 certificate’s provenance names neither, so the credit line is right
without them.
If a reply is sent, it may ask which part of the package uses them, so that
the credit of a later result built on that part is read from the source.

## 15. For the Records Lane

**`reviews:` entry for `T-093`:**

```yaml
reviews:
  - path: docs/project/reviews/review-2026-10-05-guzhou-r071.md
    kind: adversarial
    reviewer: AI agent, the review lane of the 2026-10-05 stage 4 for T-093, prompted separately from the registering and replay lanes with no shared context, blind to the replay; claude-opus-5-5, tbd-strong tier (configured reasoning xhigh)
    reviewer_kind: ai
    relation: project
    date: '2026-10-05'
    scope: >-
      Guzhou0806 / N17 project's R071 C027 certificate for s(17) > 18641771/4000000, pinned at 8c11f696, against T-043's charge and checker bytes: the argument from certificate to bound with every hypothesis the two checkers assume; the charge, budget, capacities, chain, every strict core margin and envelope re-derived in exact arithmetic by code sharing nothing with the source; an independent exact sweep at 227 rows, the 14 rows R071 adds among them, with 20 control rows of R068 and R070 matching their published ledgers; the corner charge at every row; what changed from R068 and R070; the missing C027 records and the source's CI; R070's handling and the results that carry no bound; credit, the AI statement and the date; blind to the replay.
    verdict: accepted
```

**`external_review` on `E-n017-guzhou-r071-report`:**

```yaml
external_review:
  state: informally-verified
  date: '2026-10-05'
  reviewed_by: AI agent, the review lane of the 2026-10-05 stage 4 for T-093 (claude-opus-5-5, tbd-strong tier), separately prompted, blind to the replay; docs/project/reviews/review-2026-10-05-guzhou-r071.md
  note: >-
    No mathematical defect. The C027 certificate is R068's charge byte for byte at parent
    side 18452000/18641771 with every strict core rebuilt over 5,114 intervals refining
    R068's 4,991 and R070's 5,107; the charge, budget 17000448944, capacity one of all 86
    patterns, the chain, every core margin (least 1.0001596e-12) and envelope were
    re-derived in exact arithmetic by code sharing nothing with the source, and the two
    prose steps are the lemmas proved in the 2026-09-28 review, unchanged. An independent
    exact sweep returned minimum 1000026844 at 227 sampled rows, the 14 new rows among
    them, and reproduced 20 published rows of R068 and R070 with their cell counts; the
    charge at a legal corner centre bounds every row from above. Unchecked here: the
    exact minimum at the other 4,887 rows, which the source's missing C027 records and
    unobserved CI do not supply and the complete paired replay must decide. RF-1 to RF-9,
    none blocking.
```

**Significance:** keep `score: 2` and `scored: '2026-10-05'`; set `by` to
`think-1qms stage-4 review lane, review-2026-10-05-guzhou-r071 (repository)`, and take
§12 for the rationale.

**On recording this review:** `T-093` moves to `V0/C1`, so the `notes` sentence “C0
because nothing here has read the mathematics” changes with it, and the status reads
*reviewed*.

**At the exit, after the replay passes:** add the replayed-here evidence with the values
of §8 and its programs (RF-5); add the control (RF-6); rewrite `T-093`’s `claim`,
`notes` and `next_rung` together, correcting RF-3 and RF-4; move the case record’s
verified lower bound to $18641771/4000000$; and cite §3 of the 2026-09-28 review beside
`BOUND_PROOF.md` in the evidence’s `pinpoints`, as `E-n017-guzhou-r068-source-replay`
does, with this review as its `audit_record`. If the replay fails: record it with
`replay_status: failed`, leave the verified field at `T-043`, and take RF-8.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
