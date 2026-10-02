# wand125 Rectangle Certificates of 1 October: Review of T-068

The 34 raised rectangle-density certificates that `T-068` registers are the certificate
kind reviewed on 22 September (Tokoharu’s method and checker) and 27 September
(wand125’s certificates at sides up to $8.955$), and nothing in the method has changed:
the checker is Tokoharu’s `verify.cpp`, byte for byte, the net, core and margins are the
same exact rationals, and the only new quantities are sizes and running times.
Every retained file of the 37 new or raised certificates is internally consistent, the
exact first-party preflight passes for all of them, and the request on issue 281 agrees
with the register at every one of its 66 numbers.
No defect was found, blocking or otherwise, in the mathematics, the checker or the
record. The 34 values stand as reported until the complete 201-direction replay of each
certificate passes here; this review names what that replay must show.
The draft significance score `S3` is confirmed.

This is the review lane of stage 4 of the result import process for import E
(`think-6ei5`), written by Claude (model Fable, extra-high thinking effort), separately
prompted as lane R3 with no shared context with the replay lane, on 2026-10-02. It
registers nothing and moves no bound.

## Scope and Evidence

The claim is `T-068`: wand125/square-packing-bounds at
[`1a25a5ed`](https://github.com/wand125/square-packing-bounds/tree/1a25a5ed745fdd905a52f48fcc48150a0669032d)
reports a higher standing rectangle-density certificate at each of 34 counts from
$n = 19$ to $95$, each proving $s(n) \ge L$ for the side $L$ in its directory name.
The evidence entry is `E-wand125-rectangle-2026-10-01-report`, whose scope has 37
counts: the 34, and $n = 59$, 77 and 78, where the same revision’s exact covers and Evan
Daniel’s $s(78) = 9$ are higher, so the register entry leaves them out.
The packet is
[`wand125-rectangle-certificates-2026-10-01`](../../../packing/resources/web/wand125-rectangle-certificates-2026-10-01/README.md).

Read in full: the packet README and its acquisition record; the 37 retained
`certified_candidate.json`, `certificate_metadata.json`, `verification_summary.json` and
`verified_angles.jsonl`; the retained source README’s “Checking them” and “Attribution”
sections; `T-045` to `T-048` and `T-068` with their evidence entries; the case records
`n-090.md` and `n-093.md`; issue 281; the
[density mathematics review](review-2026-09-22-tokoharu-density-mathematics.md), the
[checker-scaling review](review-2026-09-27-wand125-rectangle-scaling.md) and the
[n = 50 mixed-verifier review](review-2026-09-28-wand125-n50-mixed-verifier.md); and
`devtools/audit_wand125_rectangles.py` around its `CASES_2026_10_01` table and
`audit_case`.

Run here, on one core of x86-64 Linux with the project CPython 3.14.7, as
`scratchpad/r3/checks.py` (exact rationals, no source program executed):

- the preflight receipt `receipts/preflight/audit.json.gz` read back: 53 cases, every
  one `PASS`, and for the 37 new ones the input digest, mass and node count equal to the
  retained metadata and summary;
- for each of the 37 directories: the summary status, 201 angle cases, target
  $10001/10000$, checker digest `a75140df…`, the input digest in three places, the 201
  per-angle rows $r = 0..200$ each `verified`, their node and leaf sums and minimum
  printed bound equal to the summary, every printed bound at or above `up(10001/10000)`,
  the candidate’s own $n$, $L$, $B$, `rhs`, the exact mass as the sum of the weight
  strings, and the scaling factor as the quotient of its recorded masses;
- the net and smoothing identities, and the comparison of issue 281’s 34 rows with the
  claims of `T-046` and `T-068`.

## The Argument From Certificate to Bound

A certificate for count $n$ at side $L$ is a list of rectangles $R_j \subset [0, L]^2$
with nonnegative rational weights $w_j$. Expanding each through the eight symmetries of
the container with density $w_j / (8 |R_j|)$ per image gives a $D_4$-invariant density
$g \ge 0$ on $[0, L]^2$ of exact total mass $M = \sum_j w_j$. Each of the 37 here has
$M = n - 1/100$, recomputed from the weight strings.

The checker certifies, for every one of the 201 net directions
$\theta_r = 2 \arctan(83 r / 40000)$, that every closed square of side $B = 9977/10000$
at orientation $\theta_r$ whose centre lies in $[L/2,\ L - B(c_r + s_r)/2]^2$ captures
mass at least $10001/10000$. Quarter-turn rotations carry any legal centre into that
quadrant without changing the orientation class, so this is every legal $B$-square at
that direction.

Between net points the argument is exact containment, not interpolation.
An orientation $\theta \in [0, \pi/4]$ (the diagonal reflection folds the rest) has a
nearest net half-angle within $D/2$, $D = 83/40000$, so
$\tan(|\theta - \theta_r|/2) \le D/2$, and the concentric $B$-square at $\theta_r$ has
axis half-width at most $B(1 + D)/2$ in the frame of the unit square at $\theta$. Since
$B(1 + D) = 399908091/400000000 < 1$, that core lies strictly inside the unit square;
with smoothing, the margin $B(1 + D) + 3\varepsilon = 399968091/400000000 < 1$ at
$\varepsilon = 1/20000$ does the same for the mollified density.
The net reaches past $\pi/4$ because $t_{200}^2 + 2 t_{200} - 1 = 89/40000 > 0$. All
three were recomputed here and are the values the preflight records for all 37.

Hence every unit square placed in the container captures at least $1$ (indeed
$10001/10000$). Packed unit squares have disjoint interiors, the density has no mass on
boundaries, so $n$ of them would need $n \le M < n$. The bound is $s(n) \ge L$; by
compactness it is strict, which the source does not claim.

**Angle zero.** At $r = 0$ the coverage of a translated axis-aligned core is a product
of two piecewise-affine overlap lengths, bilinear on every cell of the event grid
$\lbrace a \pm B/2, d \pm B/2 \rbrace \cap [L/2, L - B/2]$ over all expanded rectangle
edges, so its minimum is at a grid vertex; the checker evaluates every vertex in
interval arithmetic in one process (up to $11{,}594{,}025$ vertices here, at $n = 93$),
and the preflight rebuilds the event set from all four edges and requires the input to
list exactly it.

**Scaling.** Every candidate’s weights were multiplied by one exact rational before the
recorded run, recorded as `scaling_experiment.factor_exact`; the 37 factors run from
$1.0000409862\ldots$ ($n = 19$) to $1.0432875130\ldots$ ($n = 93$), each the quotient of
its recorded target and source masses.
Multiplying every weight by $f > 0$ multiplies every coverage value and the mass by $f$;
the checker read the scaled data and the preflight checks the scaled mass, so the factor
is search provenance and enters the proof nowhere.

**Transfers.** `T-068` uses none: each count has its own certificate.
The $n = 31$ certificate’s mass $3099/100 < 32$ also gives $s(32) \ge 2381/400$, which
the evidence entry notes and Daniel’s $s(32) = 6$ supersedes.

## Hypotheses the Checker Assumes

1. The interval endpoints in `certificate_input.txt` enclose the exact candidate, and
   the file is the one the accepting run hashed.
   Discharged exactly by the preflight: it regenerates the input from the candidate,
   requires the published `input_sha256`, and checks every endpoint against its
   rational.
2. The rectangle list is the complete $D_4$ expansion with multiplicity, and
   $M = \sum w_j < n$, with $n$ the directory’s count and the candidate’s own `n`.
   Discharged by the preflight (the candidate-`n` check is WSC-1 of the 27 September
   review, now at `audit_wand125_rectangles.py:658`).
3. The axis-event list is exactly the breakpoint set.
   Discharged by the preflight.
4. $B(1 + D) < 1$, the smoothing margin and the net’s reach.
   Discharged exactly, above.
5. $L^2 > 2B^2$, so the centre domain is nonempty.
   Trivial at $L \ge 1927/400$.
6. Binary64 IEEE 754 with round-to-nearest, no fused multiply-add and no fast-math; the
   compile line is fixed in `run_verify.py` and the binary asserts the rounding mode.
   Trusted, with `stod`’s exact hexadecimal parsing and `nextafter`.
7. The inscribed-polygon area bound (every vertex proved inside both shapes, strict
   convexity proved), the signed edge-length derivative enclosure and the leaf
   inequality $F \ge F(x_0, y_0) - G_x d_x - G_y d_y$: prose, reviewed on 22 September;
   nothing in them depends on $L$ or the rectangle count.
8. All 201 directions finish `verified` under the $10^7$-node and $2^{-45}$-depth
   limits; the runner refuses otherwise, and the per-angle rows show it.
   This is what the replay decides.
9. The theorem is about closed unit squares with disjoint interiors in the closed
   container, and rectangle boundaries carry no mass.
   Prose.

## The Checker’s Trust Boundary

The 37 directories pin `verify.cpp` and `run_verify.py` by digest to Tokoharu’s copies
retained with the
[22 September packet](../../../packing/resources/web/external-square-certificates-2026-09-22/tokoharu-density/README.md)
(`a75140df…`, `7bce2467…`), and the audit tool refuses a directory whose digest differs.
The checker decides coverage at the 201 directions and nothing else: it trusts the orbit
list, the axis events and the input intervals it reads (DENS-2), and the search driver’s
`globally_verified`, `status` and `scaling_experiment` fields are never read by the
intake. Everything outside coverage is decided by the preflight in exact arithmetic.

What this checker shares with wand125’s `mixed_rotated_verify.cpp` of `T-069` is the
whole interval kernel: `diff -u` of the two retained files leaves the interval type and
its `nextafter` roundings, `readI`, `area_lower`, `slice` and the rectangle struct
unchanged, and every change is in `bound`’s interface and in `main` (the threshold,
domain and limits), as the
[mixed-verifier review](review-2026-09-28-wand125-n50-mixed-verifier.md) tabulates.
A kernel defect would therefore reach both families; the 28 September re-read of that
kernel at threshold $1$, and the one-sided exact control it ran, are evidence for this
family too.

## What Changed Since 27 September

Nothing in the checker, the net, the core, `rhs` or the format.
The sizes grew:

| Quantity | 27 September review, 44 certificates | The 37 here |
| --- | ---: | ---: |
| Side $L$ | $939/200$ to $1791/200$ | $1927/400$ to $49259/5000 = 9.8518$ |
| Positive orbit representatives | 135 to 812 | 223 ($n = 29$) to 926 ($n = 89$) |
| Expanded rectangles | 1,080 to 6,496 | up to 7,408 ($n = 89$) |
| Axis events per coordinate | 826 to 2,325 | up to 3,405 ($n = 93$) |
| Axis vertices | up to 5,405,625 | up to 11,594,025 ($n = 93$) |
| Largest node count at one $r \ge 1$ | 237,591 | 196,631 ($n = 94$); cap $10^7$ |
| Longest single direction | 6,114 s ($n = 55$, $r = 0$) | 19,593 s ($n = 70$, $r = 0$); 19,156 s at $n = 93$ |
| Upstream wall time per certificate | 495 s to 13,737 s | 1,219 s to 19,593 s |
| Smallest printed leaf bound | $1.0001000003$ | $1.0001000000786207$ ($n = 26$) |
| Weight scaling factor | $1.00052$ to $1.02659$ | $1.00004$ to $1.04329$ |

The side stays in the binade $[8, 16)$ the 27 September review already analysed, so one
ulp is still $2^{-49}$ and no constant of the checker moves; the smallest printed leaf
bound is a branch-and-bound artefact that sits just above `up(10001/10000)`
$= 1.0001000000000002$, as before.
Every mass is now $n - 1/100$, the $n = 27$ certificate included, whose predecessor had
$n - 1/1000$.

Two statements are new in the source: the README’s “Checking them” section now says
every standing certificate was replayed before publication on a second machine from the
published files, with the input regenerated and the node count equal; and the
`scaling_experiment` record carries the source and target masses.
The retained summary is one run, so the second-machine statement is the source’s; the
replay here is what decides.

## Where Issue 281 and the Record Differ

- **The table agrees exactly.** All 32 values in the issue’s “T-046” column equal the
  `T-046` claim, and all 34 “now” values equal the `T-068` claim and the directory sides
  (checked as rationals).
  The raises are $1/400$ to $7/200$.
- **No directory carries a tarball.** The issue says each holds “the candidate, the
  checker’s input and summary, and the tarball”; each holds seven files and no archive.
  The input is pinned by digest and regenerated, which is stronger than retaining it.
- **The revision’s date.** The issue dates `1a25a5e` 2 October; the commit is
  2026-10-01T21:10:40Z and the packet is named for the UTC date.
- **34 of 37.** The issue leaves out $n = 59$, 77 and 78 on purpose, pointing to the
  exact values; the packet retains and preflights them, and `T-068` excludes them.
- **$n = 93$.** The issue’s “above Nagamochi’s $F(93) = 9.7178\ldots$” is right:
  $3889/400 = 9.7225 > 1 + \sqrt{76} = 9.7177978\ldots$, the case’s verified lower
  bound.

None of these touches a bound.

## Findings

No blocking finding.

### R3E-1 — Low: the axis direction now runs for up to 5.4 hours in one process

WSC-2 of the 27 September review, with a new maximum: at $n = 70$ the $r = 0$ process
took 19,593 s upstream, and at $n = 93$ 19,156 s, against 6,114 s before.
It is cost, not soundness, but a replay whose per-certificate wall ceiling is below that
will refuse a correct certificate at the axis step.

### R3E-2 — Note: the source’s second-machine replay cannot be seen from the record

The source README and the issue say each standing certificate was replayed on a second
machine with the same node count.
The directory retains one `verification_summary.json`, so the record can cite the
statement but not check it; the replay here supplies what it cannot.

### R3E-3 — Note: three retained certificates are outside the claim

`rect_n59_L79325`, `rect_n77_L89325` and `rect_n78_L8965` pass the same preflight and
stay in the evidence entry’s scope.
They prove bounds below values registered elsewhere and need no replay for `T-068`.

## Claims by Evidential Status

- **Proved here in exact arithmetic:** the net, smoothing and reach identities; every
  mass equal to $n - 1/100$ from the weight strings; every scaling factor equal to its
  recorded quotient; the agreement of the issue’s 66 numbers with the register; the
  internal consistency of all 37 summaries, metadata and per-angle rows.
- **Computationally verified by the source, re-read here:** the exact preflight of all
  53 standing certificates (`PASS`), run by the registering lane on macOS arm64 with
  CPython 3.14.7 and retained in the packet.
- **Reviewed by reading:** that the method, checker and constants are those of 22 and 27
  September, and that no new premise depends on the side, the count or the rectangle
  number.
- **Asserted by the source, not verified here:** complete coverage at the 201 directions
  for all 37 certificates.
  They stay reported until the replay passes.

## What the Replay Must Show

For `V3/C3` on `T-068`, by the runbook’s stage 4:

- A complete 201-direction replay of each of the 34 certificates, run by
  `audit_wand125_rectangles --packet 2026-10-01 --replay`, which repeats the preflight
  (the regenerated input must hash to the published `input_sha256`) and then runs the
  retained `run_verify.py` and `verify.cpp`, read before they are run.
  Each direction must reproduce the retained row’s node count, leaf count and printed
  bound; the 27 September review’s reasons for bit-identical reproduction across
  compilers hold unchanged.
- Receipts under `receipts/replay/` of this packet, committed on the bead’s branch when
  each run ends, and a replay evidence entry
  `E-wand125-rectangle-2026-10-01-source-replay` of the shape of
  `E-wand125-rectangle-source-replay`, which `apply_wand125_rectangles` names before it
  moves a verified lane.
- Two mutated certificates refused by the retained checker path, held by a test; the
  existing `test_wand125_rectangle_audit.py` controls must be shown to cover this
  packet.
- The cost beside the source’s figure: the per-angle seconds of the 34 sum to 148.5
  CPU-hours upstream (167.5 for all 37), which is the figure the plan carries; the 27
  September replay ran at about 1.2 times upstream on x86-64. Set each certificate’s
  wall ceiling above its $r = 0$ time (R3E-1).
- No sample or fast tier counts; a direction that stops at the node or depth cap is
  `UNRESOLVED` and the certificate is refused.

The replay adds a confirming machine replay of the source’s own checker, not a second
method: global coverage would still be decided by Tokoharu’s C++ alone, so the entry’s
`composition` should say so, as `T-045`’s does.

## Significance

`S3` confirmed.
Against its neighbours: `T-045` and `T-046` are `S3` for the same kind of
certificate at the same counts, and `T-047` holds the family’s `S4` for the technique.
These are raises of $0.0025$ to $0.035$ at 32 counts the record already held from the
same generator, with two new counts, one of which ($n = 93$) passes Nagamochi’s closed
form; substantive case results, no new technique and no disputed value.

## Disposition

`T-068` is accepted by this review with no defect open: `C1` once this document is
recorded as `external_review` on `E-wand125-rectangle-2026-10-01-report`
(`informally-verified`, 2026-10-02) and listed in the entry’s `reviews`, with the
document mapped as a retained review in `document-map.yaml`; `V3/C3` when the replay
above passes. The reply on issue 281 can carry R3E-1 and R3E-2 as remarks, and the
tarball point the packet README already makes.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
