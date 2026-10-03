# wand125 Certificates of the Afternoon of 2 October: Review of Six Mixed Bounds, the Linear `s(82) ≥ 233/25` and Seven Rectangle Rungs

Between 05:58 and 15:16 UTC on 2 October wand125/square-packing-bounds published
fourteen certificates this record had not retained, all pinned here at `b00fc70f`: six
rectangle densities checked at coverage one (`n = 83`, 85, 87, 91, 92 and 96), one
linear measure of points, segments and rectangles (`n = 82`), and seven raised rungs in
Tokoharu’s rectangle format (`n = 20`, 42, 59, 70, 77, 91 and 93). None brings a new
checker. Every file of every `code/` directory, and every `verify.cpp` and
`run_verify.py`, has the Git blob of a copy this record retains and has already
reviewed: `mixed_rotated_verify.cpp` (`89b674a6…`) for the six, read on 28 September and
again on 2 October; `unified_linear_verify.cpp` (`0249726a…`) for `n = 82`, read on 2
October; and Tokoharu’s `verify.cpp` (`a75140df…`) for the rungs, read on 22 and 27
September and again on 2 October.
There is nothing to diff, and this review re-derives only what the new measures add:
their sizes, structure and records.

Every exact premise that can be read from the retained files holds for all fourteen, and
every check a replay makes before its first angle passed on the seven pinned tarballs.
No blocking defect was found.
Seven non-blocking findings are recorded: a comparison value below Green’s at three
counts, as on the morning of 2 October; three notes on the source’s records; a note on
Nagamochi’s value; one on the order of registration; and the re-hash of `23e2284`, which
changes no retained byte or claim.
All fourteen values stand as reported until each complete replay passes here.
`S3` is proposed for each of the three entries the import registers.

This is the review of stage 4 of the result import for the afternoon’s requests on
jlevy/squares#282 and #294 and the source’s unrequested rectangle rungs, written by an
AI agent as lane V of the import on 2026-10-02, after retaining the packets and running
the preflights and before any replay.
It was not prompted separately from the retaining lane, so it is a review of the
mathematics and the records, blind to the replay and not to retention.
It registers nothing and moves no bound.

## Scope and Evidence

| Claim | Directory | First commit (UTC) | Measure | Mass | Nodes the source records |
| --- | --- | --- | --- | --- | ---: |
| $s(83) \ge 937/100$ | `mixed_n83_L937` | `25c421d5`, 14:46:34 | 728 rectangles | $8299999/100000$ | 122,070,074 oblique |
| $s(85) \ge 473/50$ | `mixed_n85_L946` | `028b9155`, 11:38:12 | 525 rectangles | $8499999/100000$ | 87,731,796 oblique |
| $s(87) \ge 237/25$ | `mixed_n87_L948` | `6e4e9786`, 13:49:30 | 299 rectangles | $8699999/100000$ | 37,506,392 oblique |
| $s(91) \ge 97/10$ | `mixed_n91_L970` | `6e4e9786`, 13:49:30 | 288 rectangles | $9099999/100000$ | 30,125,436 oblique |
| $s(92) \ge 39/4$ | `mixed_n92_L975` | `6e4e9786`, 13:49:30 | 324 rectangles | $9199999/100000$ | 32,377,010 oblique |
| $s(96) \ge 249/25$ | `mixed_n96_L996` | `b00fc70f`, 15:16:36 | 279 rectangles | $9599999/100000$ | 31,529,330 oblique |
| $s(82) \ge 233/25$ | `mixed_n82_L932` | `58f153f8`, 12:33:44 | 86 points, 222 segments, 774 rectangles | $8199999/100000$ | 153,579,479 |
| $s(20) \ge 49/10$ | `rect_n20_L49` | `4318bdf9`, 13:37:33 | 254 rectangle orbits | $1999/100$ | 20,862,964 |
| $s(42) \ge 2731/400$ | `rect_n42_L68275` | `4318bdf9`, 13:37:33 | 479 | $4199/100$ | 28,399,704 |
| $s(59) \ge 127/16$ | `rect_n59_L79375` | `06eeb40c`, 05:58:20 | 604 | $5899/100$ | 38,103,520 |
| $s(70) \ge 3451/400$ | `rect_n70_L86275` | `7d770221`, 08:25:06 | 883 | $6999/100$ | 38,607,528 |
| $s(77) \ge 447/50$ | `rect_n77_L894` | `06eeb40c`, 05:58:20 | 663 | $7699/100$ | 35,716,875 |
| $s(91) \ge 3859/400$ | `rect_n91_L96475` | `4318bdf9`, 13:37:33 | 915 | $9099/100$ | 35,649,266 |
| $s(93) \ge 1947/200$ | `rect_n93_L9735` | `4318bdf9`, 13:37:33 | 879 | $9299/100$ | 45,473,527 |

The packets are
[`wand125-mixed-bounds-afternoon-2026-10-02`](../../../packing/resources/web/wand125-mixed-bounds-afternoon-2026-10-02/README.md),
[`wand125-linear-n82-2026-10-02`](../../../packing/resources/web/wand125-linear-n82-2026-10-02/README.md)
and
[`wand125-rectangle-certificates-2026-10-02`](../../../packing/resources/web/wand125-rectangle-certificates-2026-10-02/README.md).
The import registers the six mixed bounds, $s(82)$, and the rungs at $n = 20$, 42 and
70; the rungs at $n = 59$ and 77 are below the exact values $8$ and $9$ this record
already verifies, and those at $n = 91$ and 93 below the same revision’s mixed bounds.

Read in full: the fourteen directory READMEs, the seven `manifest.json` and
`completion-audit.json` files, the root README’s sections on these certificates and its
Attribution and Status sections, the commit messages from `06eeb40c` to `b00fc70f`,
issue 282’s comments of the afternoon, issue 294’s comment on $n = 82$, issues 295 and
308, and the three packet READMEs and receipts.
Read again, for what they assume: the
[28 September review of the mixed verifier](review-2026-09-28-wand125-n50-mixed-verifier.md),
the
[2 October review of the mixed bounds](review-2026-10-02-wand125-mixed-rectangle-bounds.md),
the
[2 October review of the linear certificates](review-2026-10-02-wand125-linear-certificates-and-n76.md),
the
[2 October review of the rectangle rungs](review-2026-10-02-wand125-rectangle-bounds-t068.md)
and the [density mathematics review](review-2026-09-22-tokoharu-density-mathematics.md).

Run here, with the project CPython 3.14.7 on x86-64 Linux, and no source program:

- the three audits that write the packets’ receipts, `mixed-audit`, `linear-audit` and
  the rectangle preflight, each from the retained bytes;
- `mixed-fetch` and `linear-fetch` on each of the seven pinned tarballs, read from a
  depth-1 clone at `b00fc70f`, which import the shipped Python driver to repeat its
  preconditions and run no checker;
- a comparison of each of the eleven bundles `23e2284` re-hashed, unpacked at its parent
  and at `23e2284`, member by member; and
- exact structural counts of the seven new measures (walls, orbits, the $n = 82$ support
  against $n = 83$’s).

No angle was replayed, and no checker was compiled.

## The Argument From Certificate to Bound

The argument is the one the earlier reviews re-derived, and nothing in it depends on the
side, the count or the number of primitives except through running time.
For a nonnegative measure $\mu$ on the container $[0, L]^2$ of total mass $M < n$:

1. **Containment.** With $B = 9977/10000$ and the 201 half-angle tangents
   $t_r = r \cdot 83/40000$, $B(1 + 83/40000) = 399908091/400000000 < 1$ and
   $(1 + t_{200})^2 - 2 = 89/40000 > 0$, so every unit square in the container, at any
   orientation, holds in its open interior a closed core of side $B$ at the nearest net
   angle. These are the `net` blocks of all fourteen certificates, recomputed by the
   audits.
2. **Coverage.** At each net angle every such core has $\mu \ge 1$. This is what each
   checker decides over a centre domain at each angle: Tokoharu’s full domain for the
   rungs at threshold $10001/10000$; for the mixed checker the per-node domain
   $[L/2, L - \rho]$, where $\rho$ is the half axis extent of the unit square at the
   lower end of the node’s bin, which contains every centre Tokoharu’s domain admits
   (the audit recomputes the eliminated width at all 200 oblique nodes, least
   $1.2050 \times 10^{-4}$, the same for all six since it depends on $B$ and the net
   alone), with angle zero by integer tables; for the linear checker one quadrant
   $[L/2, L/2 + E_r]^2$, which the measure’s quarter-turn invariance extends to the
   whole domain.
3. **Count.** The cores chosen in the $n$ squares of a packing are disjoint, so
   $n \le \sum \mu(C_i) \le M < n$, a contradiction; so $s(n) \ge L$, and the same
   certificate bounds every larger count.

Each measure is $D_4$-invariant by construction, since every format stores orbit
representatives that the shipped `expand`, `validate` or Tokoharu’s `density` expand to
eight images; the linear audit checks the invariance on the images, and every audited
input encloses the expanded images in the source’s order.

## What Is New in the Measures

**The six rectangle densities.** No point mass, `scaling_factor` $1$, total
$n - 1/100000$, every rectangle strictly inside the container and of positive mass.
The sides reach $249/25 = 9.96$, above the largest mixed side reviewed so far, $969/100$
at $n = 92$, and the orbit counts run from 279 to 728, against 317 to 832 for the
earlier certificates; the side enters the checker only through the input’s header and
the domain, which the audits recompute.
The least distance from a rectangle to a wall is $0.0010$ at $n = 91$ and $0.0011$ at
$n = 87$, and $0.10$ to $0.37$ elsewhere; none touches a wall, so no boundary convention
is exercised. Between 5 and 30 orbits per certificate lie on a symmetry axis or the
diagonal and have fewer than eight distinct images; each still carries eight copies of a
mass of one eighth. The densest rectangles, up to $5{,}992$ per unit area at $n = 85$,
are small rectangles carrying nearly point-like mass, which the area bound treats as any
other rectangle. The READMEs say each was built from scratch from a structured initial
measure with bands at integer distances from the walls; in the final measures between 0
and 30 of the coordinates of each certificate sit at an integer distance from a wall, so
the repair moved most of them.
None of this bears on soundness.
The least recorded oblique bounds are between $1 + 2.0 \times 10^{-10}$ ($n = 83$) and
$1 + 9.0 \times 10^{-9}$ ($n = 87$), as close to one as the earlier certificates’; the
threshold is exactly one and the leaf test outward-rounded, so closeness costs nodes and
not soundness. The axis minima are between $1.0025$ ($n = 85$) and $1.0134$ ($n = 87$).

**The linear measure at $n = 82$.** Its 1,082 primitives are those of `mixed_n83_L935`,
the certificate the linear review read for $n = 83$, in the same order and of the same
kinds, and every coordinate is that certificate’s times exactly $932/935$, the ratio of
the sides, so its 222 segments have the same directions (80 horizontal, 57 vertical, 85
oblique) and the general segment path is exercised as it was there.
The masses were solved again: no mass is equal, their ratios run from $0.72$ to $1.04$,
and the total’s is $8199999/8299999 = 0.98795\ldots$. So the two certificates share
their support and not their weights; each is checked on its own, and the earlier
review’s reading of the checker applies unchanged.
The least centre half-width is $3.9545\ldots$ at index 200. The source audit names three
exact-witness repairs and a run resumed and merged across machines; the merged records
are what the certificate holds, and the replay here decides them afresh.

**The seven rungs.** Positive orbit counts from 254 to 915 and sides up to $1947/200$,
both within what the 1 October certificates reached ($49259/5000$ and 926); masses
$n - 1/100$ after one exact scaling factor each, between $1.00009$ and $1.03993$, which
the checker reads as data.
The preflight regenerates each checker input from the candidate and matches the
published SHA-256, checks every interval’s enclosure, the axis-event partition, the
orbit normalization and the mass: all 53 standing certificates pass, the 46 unchanged
ones with entries equal to the 1 October receipt’s.

## Hypotheses the Checkers Assume

The lists of the
[mixed](review-2026-10-02-wand125-mixed-rectangle-bounds.md#hypotheses-the-checker-assumes)
and
[linear](review-2026-10-02-wand125-linear-certificates-and-n76.md#hypotheses-the-checker-assumes)
reviews apply unchanged; for each, what binds it here:

1. **The input encloses the expanded exact measure.** `mixed-fetch` and `linear-fetch`
   checked all 200 oblique inputs of each mixed bundle and all 201 of the linear one
   against the candidate recomputed here; the rectangle preflight regenerates each
   input.
2. **Mass, geometry, counts, digests.** The three audits, from the retained bytes.
3. **$D_4$ invariance.** By construction, and checked on the images by the linear audit.
4. **Containment and the domains.** The `net` blocks and centre domains, recomputed.
5. **The kernels.** Binary64 round-to-nearest without contraction or fast-math, under
   the shipped compile lines; unchanged bytes, reviewed before.
6. **Every angle finishes.** Each bundle’s records show empty frontiers at $\gamma = 1$,
   and the replay must reproduce them.
7. **Assertions on.** The source’s acceptance checks are `assert`s and its C++ exits
   zero on an unresolved angle; the replay tools refuse to run with assertions off and
   the merges require it of every run.

## The Trust Boundary

As before, coverage is decided by the source’s C++ alone: the mixed checker for the six,
with angle zero by `verify_axis_certificate.py`’s integer tables; the linear checker for
$n = 82$, angle zero included; Tokoharu’s checker for the rungs.
The replays here run the same code on the same inputs, so they reproduce the source’s
computation and are not a second algorithm; `C4` is not available from them.
What the three share is the rectangle area kernel (`area_lower` and `slice`), which is
Tokoharu’s byte for byte in all three checkers, and the net and containment arithmetic.
What this repository adds independently is the exact premises, the input binding and the
structural counts above.

## Where the Requests and the Record Differ

- **The comparison values.** At $n = 83$, 85 and 87 the source compares with
  $92667/10000$, below Green’s $9.26673353\ldots$; at $n = 91$, 92 and 96 with its own
  earlier values ($1929/200$, $969/100$, $248/25$), each below the new side; at $n = 82$
  with the upper end of a 90-digit enclosure of Green’s value.
- **The record at $n = 87$** is 9.41 until the $n = 85$ certificate is registered; the
  source’s note calls its own 9.46 “the record”.
- **The second replays.** Each README says the full replay was run again on a fresh
  Ubuntu 24.04 machine; this is not checkable here, and the replay here decides.
- **Dependencies.** The linear README asks for NumPy, SciPy, Numba and HiGHS; its replay
  path needs the standard library and a C++17 compiler, as the linear review found.

## Findings

No blocking finding.

### AF-1 — Low, in the source: `improvement_lower` at $n = 83$, 85 and 87 is not a lower bound

Each is measured from $92667/10000$, below Green’s value, so $1033/10000$, $1933/10000$
and $2133/10000$ overstate the margins, which are $0.10326646\ldots$, $0.19326646\ldots$
and $0.21326646\ldots$. The bounds are unaffected.
This is the morning’s MX-2 at three more counts, and the reply on issue 282 should say
so once.

### AF-2 — Note, in the source: comparison notes that name values nothing holds

The $n = 83$ and 85 notes name “published rectangle” values of 9.15 and 9.2325, which no
packet and no case record holds, as the morning’s notes at $n = 84$ and 85 did.

### AF-3 — Note: the source calls Nagamochi’s value unproven

The $n = 96$ audit calls Nagamochi’s $1 + \sqrt{79} = 9.8882\ldots$ “unproven”, and the
root README and the comments call his closed form a reference value, citing issue 295,
which reports that the lemma behind it is false.
This record holds that value as the verified lower bound at $n = 96$ and at many other
counts. The certificate does not rest on it, and its replay would give $n = 96$ and, by
mass, $n = 97$ a verified bound that does not.
This review takes no position on issue 295, which is its own import.

### AF-4 — Note, in the source: the $n = 82$ audit names its bundle by the tarball

Its `bundle` field is `n82-L9.32-proof-bundle.tar.gz` where the other linear audits name
the directory inside; harmless, and the audit here accepts either.

### AF-5 — Note: two pre-publication replays ran on an earlier copy of the bundle

The $n = 83$ and 85 READMEs say their fresh-machine replays ran on a copy that “differs
only in the provenance line of `bundle.json`”. No program in `code/` reads
`bundle.json`, and each published bundle’s `files-sha256.json` binds its bytes, so the
published proof files are what that replay read.
The replay here decides in any case.

### AF-6 — Note, for the record: register the mixed entry before the rectangle rungs

The rungs at $n = 91$ and 93 raise what the record reports today, $1929/200$ and
$3889/400$, but the same revision’s mixed $s(91) \ge 97/10$ and $s(92) \ge 39/4$, which
carries to $n = 93$, are stronger.
Registered first, the mixed entry leaves the rungs nothing to write there; registered
after, the rectangle registration would write $3859/400$ and $1947/200$ and the mixed
one overwrite them the same day.
The rungs at $n = 59$ and 77 write nothing either way.

### AF-7 — Note: `23e2284` changes no retained byte or claim

The source’s commit re-hashed the bundles of eleven mixed certificates this record pins,
saying the certificates, candidates and proofs are unchanged.
Each bundle was unpacked here at `7d770221` and at `23e2284`: both hold the same 622
members, and only `bundle.json`, whose `source_run` became a relative path, and the one
entry of `files-sha256.json` that names it differ.
Every packet that pins one of these bundles pins it at a revision before `23e2284`, with
the digest of the bytes at `7d770221`; the revisions remain in the source’s history, so
the replays fetch the pinned bytes as before, and no receipt, case value or claim moves.
The withdrawn `mixed_n50_L7318` was never registered.
The commit’s path edits in `point_n21_L5/acceptance/` change the digests those files
quote of each other and leave the M1 linkage digests unchanged: `6efc5fe5…`, and the
compressed `0d93072b…` that the $s(21)$ audit binds.

## Claims by Evidential Status

- **Recomputed here in exact arithmetic:** the containment and domain identities; each
  measure’s count, side, core, orbit counts, containment, nonnegativity and mass; the
  candidate digests; the linear $D_4$ invariance; the 201 records of each mixed and
  linear certificate; the comparisons with Green’s and Nagamochi’s values; the
  regenerated inputs of the seven rungs; the $n = 82$ support as $n = 83$’s scaled.
- **Checked on the pinned tarballs:** the pins, the bundles’ file lists and bindings to
  the packets, the drivers’ preconditions, and the enclosure of every input by the exact
  candidate (1,401 inputs).
- **Reviewed by reading:** that every checker is a reviewed one byte for byte, and that
  nothing in the new measures meets a premise those reviews left open.
- **Asserted by the source, not verified here:** every directional coverage statement of
  the fourteen certificates.

## What the Replays Must Show

For `V3/C3` on each entry, with the repository’s range drivers, each tarball fetched at
`b00fc70f` by `--via git`, assertions on and one BLAS thread, every direction passing
only because the shipped function returned the certificate’s own record, and the
receipts committed as each range ends:

| Certificate | Tool name | Tarball (bytes) | Expect | Ranges | Estimate here |
| --- | --- | --- | --- | --- | --- |
| `mixed_n83_L937` | `n83` | `cbf81b21…` (29,567,366) | 122,070,074 nodes, least $1.0000000002030356$ at 165, axis $1.0063110587189603$ over 21,808,900 cells | 0–86, 87–135, 136–171, 172–200 | 16.0 CPU-h |
| `mixed_n85_L946` | `n85-L946` | `d518b3a9…` (22,008,842) | 87,731,796; $1.0000000021147502$ at 182; $1.0025322687268394$ over 12,694,969 | 0–134, 135–200 | 8.3 |
| `mixed_n87_L948` | `n87` | `c77d8ea1…` (10,985,416) | 37,506,392; $1.0000000089739896$ at 176; $1.013387013743792$ over 2,866,249 | 0–200 | 2.0 |
| `mixed_n91_L970` | `n91` | `56174c72…` (10,533,804) | 30,125,436; $1.0000000003906073$ at 191; $1.005778849360574$ over 2,748,964 | 0–200 | 1.6 |
| `mixed_n92_L975` | `n92-L975` | `1f61a640…` (11,901,503) | 32,377,010; $1.0000000022907243$ at 191; $1.008723611315222$ over 3,560,769 | 0–200 | 1.9 |
| `mixed_n96_L996` | `n96` | `5fc6195b…` (9,136,906) | 31,529,330; $1.0000000030392873$ at 122; $1.0056403520432675$ over 1,420,864 | 0–200 | 1.6 |
| `mixed_n82_L932` | `n82` | `296d8f09…` (47,542,670) | 153,579,479 nodes, the most at index 199 (1,178,525) | 0–51, 52–90, 91–123, 124–152, 153–178, 179–200 | about 26 |

The rungs replay whole, each with its 201 directions under Tokoharu’s runner:
`rect_n42_L68275`, `rect_n70_L86275` and `rect_n20_L49`, whose upstream per-angle times
sum to 5.25, 3.56 and 1.36 CPU-hours, each reproducing the published node count, leaf
count and least leaf bound of every direction.
The checkers’ negative controls are on file for all three checkers ($n = 37$ mixed,
$n = 101$ linear, $n = 41$ rectangle), and the bytes are the same; running
`mixed-control n96` and `linear-control n82`, both cheap, would put a control on a
certificate of this release.

## Significance

`S3` proposed for each of the three entries.
The six mixed bounds are further sizes from the generator and checker of `T-069`,
`T-071` and `T-072`, each past Green’s reported value at its count and past what the
record reports there, by $0.02$ at $n = 83$ to $0.072$ at $n = 96$, where it is the
first certificate in this record above Nagamochi’s value.
$s(82)$ is the certificate of `T-073`’s kind at the one count from 82 to 85 where the
record’s reported value is still Green’s, which issue 308 reports the published argument
does not establish for $k \ge 4$. The three rungs raise reported bounds by $0.0025$ to
$0.0125$, as `T-068` did.
Substantive case results; no new technique, and no disputed value resolved.

## Disposition

All fourteen certificates are accepted by this review with no defect open.
For each entry the import registers, `C1` once this document is recorded as
`external_review` on its report entries (`informally-verified`, 2026-10-02) and listed
in the entry’s `reviews`, with the document mapped as a retained review; `V3/C3` when
the replays above pass.
The reply on issue 282 should carry AF-1, and the reply on issue 294 can note AF-4.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
