# Review: The Interval Route for T-056 and T-057 (`devtools.upper_bound_intervals`)

Reviewed 2026-09-30 by an independent adversarial sub-agent, on branch
`claude/determined-goldberg-ura2ed` at `a56f07fcf` (the tool, its test file and the four
receipts), reading the packet README text that `4c9c0fc2f` added on top of it.
Nothing in the repository was modified.
The review’s own scripts (an adversarial trigonometry sweep, two adversarial pose suites
and an independent third computation of all 50 cases) ran from a scratch directory and
are not retained; section 4 describes the third computation.
Every command ran from `packing/` under the project interpreter, one process at a time.

**In one line:** the arithmetic is sound at every line I could attack, the geometry is a
correct three-valued separating-axis decision with an exact broad phase, the route
shares no geometry or arithmetic code with the exact route, and a third computation of
my own (mpmath interval arithmetic at 60 digits, vertex-projection SAT, plain PyYAML)
agrees with all 50 receipts on every extent, every one of the 1,229,925 pairs, the 29
refuted printed sides, the 2, 3 and 2 trailing units, and de Winter’s two clearances.
T-056 and T-057 may be raised to `C4` on this evidence once an evidence entry records
it, with the common mode stated below.

## 1. Verdict

**No blocking finding.** Two should-fix items, both about how the tool is wired rather
than about what it decides: the transcription digest is folded into the mathematical
verdict, and the route cannot run without the exact route’s receipt.
The rung question has a definite answer: by the literal rule in `epistemics.md` (two
`C3` entries with different `method` values) and by the register’s own precedent
(T-009’s `next_rung` names an exact-algebraic confirmation of the same witness as the
way to `C4`; T-051’s composition note reaches `C4` from an exact and an interval replay
with the common mode stated), `interval-certified` beside `exact-algebraic` is a real
method difference here, and a stronger one than the precedent: the two routes decide
different objects.

## 2. What Was Reviewed

| Item | Path |
| --- | --- |
| Tool | `packing/devtools/upper_bound_intervals.py`, 917 lines |
| Tests | `packing/tests/test_upper_bound_intervals.py`, 73 tests, 6.75 s |
| Receipts | `receipts/interval-certification.json` and `receipts/interval-negative-controls.json` in `packing/resources/web/franciscouzo-square-packing-2026-09-27/` and `packing/resources/web/de-winter-square-packing-211-2026-09-16/` |
| Exact route | `packing/devtools/upper_bound_packets.py`, `packing/devtools/check_rational_witness_independent.py`, `sqpack.witness.promote_rational`, `sqpack.verify` |
| Standards | `epistemics.md` (rungs), `operating-rules.md` OR-16, `development.md` “Hashes and Repository-Owned Artifacts”, `tbd guidelines general-coding-rules` “Cryptographic Hash Checks” |
| Prior review | `docs/project/reviews/review-2026-09-29-issue-227-upper-bound-packings.md` |

The replay, `.venv/bin/python3 -m devtools.upper_bound_intervals check`, reported every
case and control as its receipt records, in 6.6 s wall on one worker.
Ruff, `ruff format --check` and BasedPyright are clean on both new files.

## 3. Soundness of the Arithmetic

Read line by line, then attacked with inputs chosen to break a wrong implementation.

**Primitives.** `add`, `sub`, `neg` are exact on scaled integers.
`mul` takes the minimum and maximum of the four end products and rounds them with floor
and ceiling division, which is correct for every sign pattern, including both operands
straddling zero. `scale_by` swaps the ends when the exact factor is negative.
`magnitude` and `halve` round outward.
Evidence: 20,000 random interval pairs at scale `10^6`, all sign patterns, against the
exact rational product range; no enclosure missed its range and none was wider than the
end-product bound plus four units (`trig.log`, “no failures”).

**`pi_enclosure`.** `_arctan_inverse(x)` sums the alternating series for `arctan(1/x)`
with each term rounded outward, stops when a term is at most one unit, and returns the
partial sum widened by that first omitted term plus one unit of slack.
The terms `1/((2k+1) x^(2k+1))` decrease strictly for `x >= 1`, so the
alternating-series bound applies.
Machin’s `16 arctan(1/5) - 4 arctan(1/239)` crosses the ends correctly.
Evidence: contains `pi` at scales `10^1, 10^5, 10^13, 10^52, 10^92`, with widths 80,
116, 188, 652 and 1132 units; at the working scale `10^52` that is `6.5e-50`.

**`_series`.** After the loop has added the degree-`k - 1` term, it computes the next
term `|x|^k / k!` as an outward enclosure and returns the two polynomials widened by its
upper end. Both are the true Taylor polynomials of degree `k - 1` (the missing parity
terms have zero coefficient), every derivative of `cos` and `sin` is bounded by one, so
Lagrange’s bound `|x|^k / k!` applies to both, and the enclosure’s upper end is at least
the true bound. The stop rule, `term.hi * 1000 <= 10^GUARD`, means the remainder is at
most `10^-3` of one working unit.
A negative argument is handled by summing on `|x|` and negating the sine before the
symmetric remainder is added.
No argument reduction is done: the result is sound for any `|x|`, but the width grows
with the size of the largest Taylor term (see nit 2).

**Degrees.** `pi` is enclosed at the guard scale, the radian value’s two ends are
`value * pi.lo / 180` and `value * pi.hi / 180`, sorted (so negative degrees are right),
floored and ceiled to units of the guard scale; the series runs at the lower end, and
both results are widened by the spread, which is correct because `cos` and `sin` are
1-Lipschitz. `rescale` divides out the guard digits with floor and ceiling and clamps to
`[-1, 1]`.

**Adversarial evidence** (`trig_adversarial.py`, 30 angles times 5 scales
`D = 1, 3, 12, 40, 80`, checked against mpmath at 220 digits): `pi/2` printed to 20 and
53 places, `1.57079633331250923` (the data’s largest angle), `-pi/2`, `pi`, `-pi` at 36
places, `2 pi`, `+-6.5`, `20`, `-33.3...`, `100` radians, `1e-30`, `-1e-45`,
`-3.75...E-15` (a data value with a capital exponent), and in degrees `0, 30, 45, 90,
-90, 180, 270, 359.999999999999999999, -135.25, 1e-10, 720.5, -1000`. All 300 enclosures
contain the true value; at `D = 40` every width is one or two units except `100`
radians, which is `8.1e25` units (`8e-15`) and still contains the value.
The data’s angles lie in `[-0.8038, 1.5708]`, all in radians, so nothing in either
packet approaches the loose regime.

## 4. The Geometry

**Vertices.** Twice each vertex is `2c + s1 (cos, sin) + s2 (-sin, cos)`, all four sign
pairs, doubled so that no halving rounds.
Correct.

**The pair test.** On an axis `a` that is one square’s own edge direction, that square
projects to half-width exactly `1/2` (for the true unit vector), the other to
`(|a . e1| + |a . e2|) / 2`, and the centres to `|a . dc|`; `_twice_gap` evaluates
`2|a . dc| - 1 - (|a . e1| + |a . e2|)` on the enclosures.
The axis is an enclosure of the true unit vector, the expression holds at the true
values, and the interval evaluation ranges over a box containing them, so the enclosure
is sound. `_pair` takes `[max lo, max hi]` over the four axes, which encloses the
maximum.

The three-valued verdict is sound at both boundaries:

- *Separated* when some axis’s lower end is at least zero: the two projections meet in
  at most a point, so the interiors are disjoint.
  Boundary contact is allowed, consistent with the repository’s convention, and the
  axis-aligned contacts of a `2 x 2` grid decide as the exact interval `[0, 0]`.
- *Overlapping* when every axis’s upper end is below zero: for two convex polygons with
  disjoint interiors, some edge normal of one of them has a non-negative gap (the
  Minkowski difference has edges parallel to the polygons’ edges and the origin is not
  in its interior), so all four strictly negative proves the interiors meet.
- Neither verdict can be returned wrongly at a boundary, because both are strict sign
  conditions on the ends of an enclosure; anything else escalates.
  An exact tangency that the arithmetic cannot represent stays `UNDECIDED` through 640
  digits, which is a liveness limit, not a soundness one, and none of the 24,014
  axis-decided pairs in the packets is within `1.97e-13` of contact.

**The broad phase.** `dx^2 + dy^2 >= 2 scale^2` on the exact scaled centres is an exact
test of `|dc| >= sqrt 2`; each unit square lies in the closed disc of radius
`sqrt 2 / 2` about its centre, and two such discs with centres at least `sqrt 2` apart
meet in at most a point.
Correct.

**The extent argument.** Translating the true pose by minus its least `x` and `y` puts
every vertex in `[0, extent]^2`, disjointness is translation-invariant, and
`U = max(printed, ceiling of the extent's upper end at the printed places)` is at least
the extent, so `s(n) <= U`. Valid.
Note that the wall check on the translated pose then holds by construction (the offset
is the global minimum lower end; `2 U scale` is at least the extent’s upper end), so
`walls.certified = 4n` in every receipt is a consistency check, not evidence (nit 3).

**Pose-level evidence** (`pose.log`, `pose2.log`):

| Case | Expected | Got |
| --- | --- | --- |
| Axis-aligned pair, centres exactly `(1, 1)` apart (corner contact at `sqrt 2`) | pruned, VERIFIED | pruned, VERIFIED |
| Axis-aligned pair, centres `(0.99999, 0.99999)` apart | REFUSED, not pruned | REFUSED |
| 45-degree diamonds corner to corner, centres `1.41421` apart (overlap `3.6e-6`) | REFUSED | REFUSED |
| Same at `1.4142135623730950` (below `sqrt 2` by `4.9e-17`) | REFUSED | REFUSED |
| Same at `1.4142135623730951` | pruned, VERIFIED | pruned, VERIFIED |
| Corner-to-edge contact at `1 + sqrt 2 / 2`, centre rounded up at 40 places | VERIFIED | VERIFIED at 40 |
| Same, rounded down | REFUSED | REFUSED at 80 (undecided at 40) |
| Axis-aligned pair overlapping by `1e-45` (45-place centre) | REFUSED | REFUSED at 45 |
| Same with a gap of `1e-45` | VERIFIED | VERIFIED at 45 |
| Square at `1.5707963267948966` rad beside an axis-aligned one, centres 1 apart (overlap `3e-17`) | REFUSED | REFUSED |
| Same, centres `1.0000000000000001` apart; and with the angle negated | VERIFIED | VERIFIED, VERIFIED |
| Two squares at 100 rad, `1.001` apart along the rotated edge | VERIFIED | VERIFIED at 40 |
| Pair at 0.5 rad displaced by `(cos, sin)` rounded up and down at 40 places | VERIFIED / REFUSED, undecided at 40 alone | as expected |
| Single diamond, printed side `3.1e-12` below `sqrt 2` | printed refuted, bound `1.41421356238` | as expected |
| Single square at `(-3, -3)` with printed side 1 | frame violated, VERIFIED with bound 1 | as expected |

## 5. Independence and the Method Question

**Code.** The module imports `devtools.upper_bound_packets` and
`sqpack.yamlio.safe_load` and nothing else of the project or of mpmath; it has no
dynamic import. The test pins the import set by AST and the attributes used on `packets`
to records and readers (`Source`, the two sources, `CERTIFIED`, `BY_ID`, `cases`,
`acquisition`, `certification`, the two control constants).
Importing `packets` does load the exact route’s code into the process, but none of it is
called. The geometry, the interval arithmetic and the trigonometry are the tool’s own,
and I found no line in common with `check_rational_witness_independent`, `sqpack.verify`
or `sqpack.witness`.

**What is shared, honestly:**

1. the facts files and the libyaml-backed loader (every value is a quoted string, so the
   loader can only pass them through or fail);
2. the reading of the representation: centre-angle, unit squares, radians.
   The unit was taken from Couzo’s header by the acquisition regex `theta\(rad\)` and
   from de Winter’s `angle_unit` field, once, and both routes trust the facts; the
   interval route’s upstream rebuild is the only later check of that transcription;
3. the mathematics: the separating-axis theorem over the four edge normals and the
   extent argument;
4. the verified-value rule, `max(printed, ceiling at the printed places)`, written
   twice;
5. CPython’s integer arithmetic; and
6. the author lineage: the same agent lineage wrote both routes a day apart.

Item 2 bears on attribution, not on the bound: a pose read with the wrong sign or unit
is still a packing if both routes decide it one, and the bound would still hold; only
the statement “this is the author’s packing” would be wrong.
Items 3 and 4 are the substantive common mode, and this review’s third computation
covers both (Section 6), because it uses a different formulation of the axis test
(projections of all eight vertices, with no unit-vector assumption) and recomputes the
ceiling independently.

**The method difference.** The exact route decides a rational packing whose angles
differ from the printed ones by about `1e-36`; the interval route decides the printed
pose with the true cosine and sine of each printed angle, which are transcendental and
never replaced. Both prove `s(n) <= U` by exhibiting a packing, but they are different
packings decided in different arithmetic by different code.
`epistemics.md` warns that two implementations of the same method stay at `C3`; here the
method values differ, the register already treats an exact and an interval decision of
one witness as `C4` (T-009’s `next_rung`; T-051’s composition note, which states its
common mode as this review does), and the objects differ as well.
That is a real method difference by the repository’s standard.

## 6. Results, Confirmed Independently

`independent_check.py` reads each facts file with plain PyYAML, encloses each decimal in
mpmath’s `iv` at 60 digits (checked to contain the exact decimal; no string needed
widening), takes `iv.cos` and `iv.sin`, builds the eight vertices, encloses the extent,
and decides every pair not pruned by an exact integer broad phase by the separating-axis
test on the vertex projections.
Every comparison with a printed decimal is exact.

| n | Printed side | Extent (mine, 25 digits, a point at this width) | Extent minus printed | Units above | Verified value | Least gap, pair | Frame least clearance, square |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 68 | `8.798795237222592` | `8.798795237222591963278212` | `-3.672e-17` | 0 | printed | `1.998157e-13`, (38, 46) | `-2.33e-17`, 13 |
| 206 | `14.860158663395859` | `14.86015866339586012403306` | `+1.1240e-15` | 2 | `14.860158663395861` | `2.0007357e-13`, (55, 56) | `-1.09e-15`, 167 |
| 259 | `16.602568490497649` | `16.60256849049765113427251` | `+2.1343e-15` | 3 | `16.602568490497652` | `2.0087237e-13`, (116, 117) | `-1.50e-15`, 179 |
| 305 | `17.952959459023539` | `17.95295945902354086517768` | `+1.8652e-15` | 2 | `17.952959459023541` | `2.0116723e-13`, (67, 81) | `-1.87e-15`, 202 |
| 211 | `14.99796070496771500150` | `14.9979607049676940014` exactly | `-2.10001e-14` | 0 | printed | `2.10001e-14` exactly, (80, 82) | `+1.000005e-14` exactly, 66 |

Every figure agrees with the receipt row, whose six-digit outward ranges contain my
values, and with the exact route’s verified value.
The trailing units are confirmed: the ceiling of the extent at fifteen places is 2, 3
and 2 units above the printed side at `n = 206, 259, 305`, and the decimal one unit
below each verified value is exceeded by the extent’s lower end by `1.2e-16`, `1.3e-16`
and `8.7e-16`. De Winter’s reported clearances, `1.000005e-14` at square 65 and
`2.10001e-14` at squares 79 and 81 counted from zero, are reproduced exactly (66, and 80
and 82, from one); the extreme squares are axis-aligned with exact centres, so the
enclosures are points.

Across all 50 counts (`independent_all.log`, 69 s): `printed_side_fits`, the units above
the printed side, the side-minus-printed range and the least-wall square agree at every
count; the 29 refuted counts are exactly the receipts’ 29, with one unit at 26 of them;
and the pairs total 1,205,911 pruned by the broad phase, 24,014 separated on axes, 0
overlapping, 0 undecided, the same totals the Couzo README states, with the least gap
and its pair agreeing at every count.
The exact certificate’s side lies within `3.19e-37` of the interval enclosure at every
count (from the receipts), which is the promotion’s `1e-36` angle rounding showing
through. All 50 cases settled at 40 digits.

## 7. The Upstream-Rebuild Digest (OR-16)

The tool rewrites each pose as the upstream file prints it (Couzo’s three-line header
and `x y theta` rows; de Winter’s JSON with the fields the acquisition record keeps) and
requires the size and SHA-256 that `acquire` took from the raw bytes of the clone at the
pinned revision (`_file_record` hashes `read_bytes()` before any parsing).

**Keep it.** It passes the test in `general-coding-rules`: the two sides are computed
independently (the raw upstream bytes at acquisition; a rebuild from the parsed,
serialised, reloaded facts at replay), the data in between crossed a transformation
whose fidelity is the whole question, the expected value is fixed, retained, and
re-derivable by anyone with the upstream revision, and the failure it detects is named
in the docstring: a digit, a sign, a row or the angle unit transcribed wrongly.
OR-16’s alternative, comparing complete content, is unavailable because the upstream
bytes are not retained; the digest is the only retained link to them, and Git cannot
check the facts against a file it does not hold.
It is not the “same process hashing both sides” case, and not a content hash standing in
for a revision pin, since the revision is pinned too.
Two limits should be understood: it cannot say anything about what the author intended,
only that the facts are the bytes; and it is only as good as the rebuild, so a layout
change in the rebuild (de Winter’s JSON depends on `json.dumps(indent=2)` matching his
formatting) would be a false alarm, not a soundness event, which is one reason for
should-fix 1.

A policy note for the owner, not a defect: since the facts plus the acquisition metadata
rebuild the unlicensed files byte for byte, the packets retain those files’ whole
information content; “not retained” describes the form, not the content.

## 8. Findings

| Severity | Finding |
| --- | --- |
| blocking | None. |
| should-fix | **1. The transcription digest is folded into the mathematical verdict.** `row` sets `verdict = REFUSED` when the rebuild does not match, so a provenance or formatting failure would read as a refuted packing. Report it as its own failure (`check` already has a problems list) and leave `verdict` to the enclosures. |
| should-fix | **2. The route cannot run alone.** `row` reads the exact route’s receipt unconditionally (`packets.certification(source)[n]`), so `certify` fails on a packet the exact route has not certified. For a route whose point is independence, the comparison should be optional. |
| should-fix | **3. No register change accompanies the tool.** The commit adds no evidence entry and moves no rung; Section 10 lists what the `C4` entry needs. |
| nit | **1.** `touching_exactly` counts pairs whose gap’s lower end is exactly zero; a pair with a true gap of about `1e-41` at 40 digits counts as touching (the rounded-up corner-to-edge case). Rename it or define it as “lower end exactly zero”. |
| nit | **2.** No argument reduction and no bound on the angle: sound for any angle, but the width grows with the largest Taylor term (`8e-15` at 100 rad, `D = 40`) and the series is impractical beyond about `10^3` rad. A guard or a reduction modulo `2 pi` with the `pi` enclosure would close it; nothing in either packet needs it. |
| nit | **3.** The translated-pose wall check cannot fail by construction, so the receipts’ `walls.certified = 4n` is not evidence beyond the extent; the docstring could say so. The frame check is the informative one. |
| nit | **4.** `_settled` waits on `frame.undecided` while `verdict` ignores the frame, so a frame clearance within `1e-40` of zero would raise digits for a quantity the verdict does not use. Harmless. |
| nit | **5.** The README’s “the decimal one unit below each verified value is refuted too” is true (Section 6) but is derivable only from the receipt’s 40-digit `side_enclosure`; it is not a recorded field. |
| nit | **6.** The module docstring’s “about ten seconds on one worker” is 6.6 s here; fine. |

## 9. Verified

| Claim | Evidence |
| --- | --- |
| Interval primitives round outward in every sign case | `trig_adversarial.py`: 20,000 random products, scalings, magnitudes, halvings and enclosures against exact rational ranges, no misses |
| `pi` is enclosed | contains `pi` at five scales from `10^1` to `10^92`; width 652 units at the working scale `10^52` |
| `cos` and `sin` are enclosed, including near `pi/2`, negative, tiny and large arguments, and degrees | 300 enclosures at `D = 1, 3, 12, 40, 80` against mpmath at 220 digits, all containing; widths one or two units at `D = 40` except 100 rad |
| Lagrange remainder applied to the right degree for both series | code reading, Section 3; widths above |
| Degrees conversion widened correctly | `-135.25`, `359.999...`, `720.5`, `-1000` degrees all contained |
| Separating-axis formula and three-valued verdict | code reading, Section 4; 15 pose-level cases in `pose.log`, `pose2.log` |
| Broad phase exact and correctly bounded | centres `1.4142135623730950` apart refused, `...951` pruned and verified |
| Touching allowed, overlap refused, escalation works | `2 x 2` grid, `1e-45` gap and overlap, 0.5-rad contact rounded both ways |
| Extent and translation prove `s(n) <= U` | Section 4 |
| Replay and tests pass | `check` in 6.6 s; 73 tests in 6.75 s |
| No shared geometry code; AST test enforces the import and attribute sets; no dynamic imports | Section 5; `grep` for `importlib`, `__import__`, `exec`, `eval`: none |
| All 50 verdicts, extents, 29 refuted sides, trailing units 2/3/2, least gaps and pairs, de Winter’s clearances | `independent.log`, `independent_all.log`; Section 6 |
| README totals 1,205,911 / 24,014, least gap `1.98e-13` at `n = 106` (receipt `1.97856e-13`), frames inside only at 102 and 239, up to `1.87e-15` outside (`-1.86670e-15` at 305), exact side within `3.2e-37` (`3.19e-37`) | receipts and `independent_all.log` |
| Lint and type floor | Ruff, `ruff format --check`, BasedPyright: clean |

## 10. What the `C4` Entry Needs

Each result needs a second evidence entry beside its exact replay, and the checker will
derive `C4` from it:

- `method: interval-certified`, `performed_by: repository`, `origin: replayed-here`,
  `relationship_to_generator: independent-implementation`;
- `certificate:` the retained facts (the object decided) with the receipt beside it,
  since this route publishes enclosures’ ends rather than boxes; `replay:` the `check`
  command for the source; `replay_status: passed`;
- `limitations` stating that the enclosure’s soundness rests on this tool’s own directed
  rounding rather than on a verified library, that the object is the printed pose with
  transcendental trig (not the rational certificate), that the verified value is the
  same rounding rule applied to the extent’s upper end, and the common mode of Section 5
  (facts and loader, the reading of the representation, the separating-axis theorem, the
  ceiling rule, the author lineage);
- `controls:` `receipts/interval-negative-controls.json` and
  `tests/test_upper_bound_intervals.py`;
- and in `results.yaml`, the claim text and `next_rung` of T-056 and T-057 rewritten,
  since both currently say `C4` awaits an interval route, and T-056’s claim should keep
  saying that at `n = 206, 259, 305` the printed side is refuted by the pose in either
  arithmetic.

This review’s own computation (Section 6) is a third decision of all 50 cases by a
different formulation and library; it is kept beside this file and not in the record.

## Disposition

- **Should-fix (1) and (2) and the touching nit were fixed** on 2026-09-30, in the
  commit that registers the route:
  - A failed upstream rebuild is now its own `check` failure, and the verdict comes from
    the enclosures alone.
  - The exact route’s receipt is read only for the comparison column, which is `null`
    when the exact route has not certified a case.
  - A pair counts as touching only when its gap enclosure is exactly the point zero.
  - The receipts were unchanged by these fixes.
- **Should-fix (3):** the evidence entries `E-franciscouzo-2026-09-27-interval-replay`
  and `E-n211-de-winter-interval-replay`, with T-056 and T-057 raised to `C4`, are
  recorded in the same commit.
- **Other nits:** left as they are, and documented here.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
