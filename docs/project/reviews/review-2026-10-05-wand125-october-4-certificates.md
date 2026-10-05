# wand125 Certificates of 3 and 4 October: Review of 28 Mixed Rectangle-Measure Bounds From `n = 42` to `n = 95`

From 19:33 UTC on 3 October to 19:03 UTC on 4 October wand125/square-packing-bounds
published 28 rectangle densities checked at coverage one.
Sixteen, at $n = 42$ to 44, 51, 56, 57, 67, 69, 72, 75, 84, 86, 88 and 93 to 95, are
pinned at `8aa6a10b` and registered as `T-090`; twelve, at $n = 53$, 54, 58, 70, 71, 73,
76, 87, 88, 90, 91 and 94, are pinned at `797bdf6e` and registered as `T-091`. At
$n = 88$ and 94 the evening certificate raises the morning one at the same count.
None brings a new checker: every file of every `code/` directory, and every
`requirements.txt`, has the SHA-256 and the Git blob of the `mixed_n50_L740` copy the 28
September packet retains, so the checker is `mixed_rotated_verify.cpp` (`89b674a6…`),
read on 28 September and on 2 and 3 October.

What is new is procedural.
Since `150939e` the source publishes no `completion-audit.json`, so each tarball is
bound to its certificate by the digest at the pinned tree, the README’s statement of it,
and this repository’s own fetch; and five of the twelve evening bundles record their
proof run on a different platform from the other 23 and from the 22 of 3 October.
Every exact premise that can be read from the retained files holds for all 28, every
check a replay makes before its first angle passed on the 28 pinned tarballs, every
margin and comparison in the records is right in exact arithmetic, and the two
directions replayed here from regenerated inputs returned the certificates’ own records,
one of them recorded on the new platform.
No blocking defect was found.
Five non-blocking findings are recorded: the binding without the source’s audit, judged
sufficient; the change of platform; rounded decimals in the READMEs; two corrections to
the 3 October review’s measurements; and a small inconsistency between the packet
READMEs. All 28 values stand as reported until each complete replay passes here.
`S3` is confirmed for `T-090` and for `T-091`.

This is the review of stage 4 of the result import for the 28 requests of 3 and 4
October on jlevy/squares#282, written on 2026-10-05 by an AI agent prompted separately
from the lane that retained the packets and registered `T-090` and `T-091`, working from
that lane’s brief and the retained files; model unstated.
It was written after retention and the pre-replay checks and before any replay, so it is
a review of the mathematics and the records, blind to the replay and not to retention.
It registers nothing and moves no bound.

## Scope and Evidence

`T-090`, the
[4 October packet](../../../packing/resources/web/wand125-mixed-bounds-2026-10-04/README.md),
pinned at `8aa6a10b` (4 October 07:17:29 UTC):

| Claim | Directory | Commit (UTC) | Rectangles | Mass | Oblique nodes the source records |
| --- | --- | --- | ---: | --- | ---: |
| $s(42) \ge 2739/400$ | `mixed_n42_L68475` | `aa26adf8`, 10/04 05:26:19 | 431 | $4199999/100000$ | 84,154,248 |
| $s(43) \ge 2763/400$ | `mixed_n43_L69075` | `eaed02b4`, 10/04 03:40:51 | 358 | $4299999/100000$ | 94,327,372 |
| $s(44) \ge 2789/400$ | `mixed_n44_L69725` | `83010fa6`, 10/03 20:48:15 | 399 | $4399999/100000$ | 61,963,016 |
| $s(51) \ge 747/100$ | `mixed_n51_L747` | `0e0bdeac`, 10/04 02:40:13 | 489 | $5099999/100000$ | 73,294,118 |
| $s(56) \ge 3121/400$ | `mixed_n56_L78025` | `cf451aa6`, 10/03 20:48:42 | 453 | $5599999/100000$ | 95,233,978 |
| $s(57) \ge 3149/400$ | `mixed_n57_L78725` | `bc727200`, 10/04 03:17:25 | 532 | $5699999/100000$ | 92,644,514 |
| $s(67) \ge 339/40$ | `mixed_n67_L8475` | `2475d085`, 10/04 02:38:55 | 485 | $6699999/100000$ | 80,893,626 |
| $s(69) \ge 431/50$ | `mixed_n69_L862` | `8aa6a10b`, 10/04 07:17:29 | 547 | $6899999/100000$ | 108,821,066 |
| $s(72) \ge 219/25$ | `mixed_n72_L876` | `c44fd6ff`, 10/04 03:04:04 | 488 | $7199999/100000$ | 120,543,194 |
| $s(75) \ge 447/50$ | `mixed_n75_L894` | `35b83e75`, 10/04 02:40:37 | 589 | $7499999/100000$ | 120,119,252 |
| $s(84) \ge 3763/400$ | `mixed_n84_L94075` | `c9c6be03`, 10/03 22:03:41 | 569 | $8399999/100000$ | 92,867,418 |
| $s(86) \ge 9503/1000$ | `mixed_n86_L9503` | `683264c3`, 10/04 07:03:48 | 533 | $8599999/100000$ | 95,514,032 |
| $s(88) \ge 769/80$ | `mixed_n88_L96125` | `92b1a7e4`, 10/04 02:39:20 | 502 | $8799999/100000$ | 110,846,936 |
| $s(93) \ge 247/25$ | `mixed_n93_L988` | `b321ac9a`, 10/03 19:33:34 | 501 | $9299999/100000$ | 71,180,134 |
| $s(94) \ge 497/50$ | `mixed_n94_L994` | `3c7c57a8`, 10/04 02:39:46 | 630 | $9399999/100000$ | 82,482,752 |
| $s(95) \ge 1993/200$ | `mixed_n95_L9965` | `35546168`, 10/04 06:09:45 | 480 | $9499999/100000$ | 59,167,032 |

`T-091`, the
[evening packet](../../../packing/resources/web/wand125-mixed-bounds-evening-2026-10-04/README.md),
pinned at `797bdf6e` (4 October 19:03:58 UTC):

| Claim | Directory | Commit (UTC) | Rectangles | Mass | Oblique nodes the source records |
| --- | --- | --- | ---: | --- | ---: |
| $s(53) \ge 3051/400$ | `mixed_n53_L76275` | `62ff7b2c`, 10/04 15:22:09 | 505 | $5299999/100000$ | 80,696,352 |
| $s(54) \ge 1537/200$ | `mixed_n54_L7685` | `d62b47f7`, 10/04 13:34:30 | 364 | $5399999/100000$ | 86,248,776 |
| $s(58) \ge 1587/200$ | `mixed_n58_L7935` | `797bdf6e`, 10/04 19:03:58 | 543 | $5799999/100000$ | 84,183,576 |
| $s(70) \ge 3463/400$ | `mixed_n70_L86575` | `4df6bccc`, 10/04 17:59:55 | 513 | $6999999/100000$ | 118,708,596 |
| $s(71) \ge 8721/1000$ | `mixed_n71_L8721` | `5d095211`, 10/04 11:24:57 | 529 | $7099999/100000$ | 114,091,518 |
| $s(73) \ge 8813/1000$ | `mixed_n73_L8813` | `23e75dae`, 10/04 14:48:43 | 462 | $7299999/100000$ | 116,555,688 |
| $s(76) \ge 1793/200$ | `mixed_n76_L8965` | `a2cbd0f1`, 10/04 09:06:27 | 312 | $7599999/100000$ | 50,978,010 |
| $s(87) \ge 479/50$ | `mixed_n87_L958` | `98bb2663`, 10/04 12:19:39 | 594 | $8699999/100000$ | 107,739,744 |
| $s(88) \ge 481/50$ | `mixed_n88_L962` | `9a26e8db`, 10/04 16:05:53 | 562 | $8799999/100000$ | 106,388,036 |
| $s(90) \ge 973/100$ | `mixed_n90_L973` | `324c1899`, 10/04 09:19:39 | 525 | $8999999/100000$ | 123,232,842 |
| $s(91) \ge 781/80$ | `mixed_n91_L97625` | `02f981ad`, 10/04 07:51:33 | 438 | $9099999/100000$ | 120,868,018 |
| $s(94) \ge 199/20$ | `mixed_n94_L995` | `8a81f65e`, 10/04 15:21:27 | 853 | $9399999/100000$ | 115,335,002 |

The evening packet also pins `mixed_n86_L9503` and `mixed_n69_L862` unchanged, with
their files compared byte for byte with the 4 October packet’s copies; they are
`T-090`’s. Each directory has one commit, which adds it and changes the root README and
nothing else, but for four of the morning sixteen (`mixed_n44_L69725`,
`mixed_n56_L78025`, `mixed_n84_L94075` and `mixed_n93_L988`), first published with a
`completion-audit.json` that `150939e` removed before the pin.
Each was announced in its own comment on issue 282 within 20 seconds of its commit.
All 33 source commits between `2aff2076` and `797bdf6e` end in a trailer naming an AI
assistant as co-author and a session-link trailer, and the root README’s Status section
says parts of the work were produced with AI assistance under human direction.

Read in full: the 28 directory READMEs, `manifest.json` files and the retained
candidates and certificates; the root README’s 28 new sections and its diffs from
`2aff2076` and `8aa6a10b`, which add those sections and remove nothing; the 33 commit
messages, and the paths and README diff of `150939e`; the 28 comments of 3 and 4 October
on issue 282; both packet READMEs, `acquisition/` records and receipts; `T-090`,
`T-091`, their 28 report entries, the two coverage entries, the lanes and intake
paragraphs of the 26 changed case records, and #282 in `result-requests.yaml`; the audit
tool’s `MixedCertificate`, `_pinned_bundle_facts`, `_source_audit_facts`,
`mixed_certificate`, `mixed_audit`, `green_facts`, `tarball_pin` and `mixed_replay`; and
the retained `mixed_n50_L740/code/` files the drivers run (`mixed_net_audit.py`,
`mixed_density_check.py`, `mixed_rotated_verify.py`, `verify_mixed_full_proof.py`,
`verify_rotated_result.py`, and `main` and the interval type of
`mixed_rotated_verify.cpp`). Read again, for what they assume: the
[28 September review of the mixed verifier](review-2026-09-28-wand125-n50-mixed-verifier.md),
the
[2 October review of the mixed bounds](review-2026-10-02-wand125-mixed-rectangle-bounds.md)
and the
[3 October review of 22 certificates](review-2026-10-03-wand125-october-3-certificates.md).

Run here, with the project CPython 3.14.7 on x86-64 Linux:

- `mixed-audit PACKET --check` on both packets (`RECEIPT_MATCHES` each),
  `devtools.retained_data check` on both (no problem reported) and
  `devtools.acquire_source PACKET --check` on both (`PACKET_MATCHES_ITS_CONTRACT`), each
  from the retained bytes;
- `mixed-price`, `mixed-shard wand125-mixed-bounds-2026-10-04 --runners 8` and
  `mixed-shard wand125-mixed-bounds-evening-2026-10-04 --runners 6`;
- every `fetch.json` receipt of both packets against the audit receipt and the pins
  (status, revision, digest and size, 621 listed files, 10 code files, preconditions,
  200 enclosing inputs of $8 \times$ the rectangle count, 200 `ANGLE_VERIFIED` records
  at $\gamma = 1$, empty frontier, node total and least bound);
- exact comparisons of each side with what the record reported before each import (the
  case records at `7e45c42a`, the merge before the lane, for `T-090`; those plus
  `T-090`’s values for `T-091`), with the next count’s value after both imports, with
  Green’s value (by the audit’s enclosure) and with Nagamochi’s
  $1 + \sqrt{n - 2\lfloor\sqrt n\rfloor + 1}$, and of every margin and figure in the 28
  report entries and the 26 case records;
- exact structural counts of the 28 measures from the retained candidates and
  certificates (rectangle counts, walls, masses, densities, orbits, coordinate
  denominators, supports against the certificates they supersede), with the definitions
  of the 3 October review, checked against its figures (OF-4 gives the two that differ);
- in the source’s history (a blob-filtered clone): the tree at both pins, the paths each
  of the 33 commits touches, the Git blob of every `code/` file and `requirements.txt`
  in the 28 directories at `797bdf6e`, and the README diff of `150939e`;
- all 28 tarballs downloaded by their raw-file address: each has its pinned SHA-256, and
  each bundle’s `bundle.json` names the candidate digest and the platform of its proof
  run; and
- `mixed-fetch n58-L7935` and `mixed-fetch n88-L96125` by `--via git` into scratch space
  (both `BUNDLE_READY`, each tarball’s Git blob equal to the blob at its pin), the
  retained checker compiled with the shipped `compile_verifier` (g++ 13.3.0), and two
  directions replayed with the shipped `verify_rotated_result.replay` from inputs
  regenerated by the shipped `export`: index 197 of `mixed_n58_L7935`, the least
  recorded bound of the 28, and index 92 of `mixed_n88_L96125`, the least of `T-090`’s.

No complete replay was run: two of the 5,628 directions were.

## The Argument From Certificate to Bound

The argument is the one the earlier reviews re-derived; nothing in it depends on the
side, the count or the number of rectangles except through running time.
For a nonnegative measure $\mu$ on the container $[0, L]^2$ of total mass $M < n$:

1. **Containment.** With $B = 9977/10000$ and the 201 half-angle tangents
   $t_r = r \cdot 83/40000$, $B(1 + 83/40000) = 399908091/400000000 < 1$,
   $(1 + t_{200})^2 - 2 = 89/40000 > 0$, and the last bin reaches below $\pi/4$,
   $(1 + \tfrac{399}{2}\cdot\tfrac{83}{40000})^2 - 2 = -4544311/6400000000 < 0$. So
   every unit square in the container, at any orientation, holds in its open interior a
   closed core of side $B$ at the net angle its orientation is assigned to.
   These are the `net` blocks of all 28 manifests and certificates, recomputed by the
   audit; no candidate declares a `proof_net`.
2. **Coverage.** At each net angle every such core has $\mu \ge 1$. At node $r \ge 1$
   the checker decides it over the centre domain $[L/2, L - \rho(a_r)]^2$, where
   $a_r = t_r - D/2$ with $D = 83/40000$ the step, and
   $\rho(a) = (1 + 2a - a^2)/(2(1 + a^2))$ is the half axis extent of a unit square at
   half-angle $a$: the union of the admissible centres over the node’s bin, folded into
   one quadrant by a quarter turn, with orientations above $\pi/4$ sent back by the
   diagonal reflection.
   It omits a strip of width $\rho(a_r) - B(c_r + s_r)/2 \ge 1.2050 \times 10^{-4}$ of
   Tokoharu’s domain, the same for all 28, and its half-side $E_r = L/2 - \rho(a_r)$ is
   at least $2.7166$ at the smallest side here, $L = 2739/400$. Angle zero is decided by
   integer tables over $[L/2, L - 1/2]^2$.
3. **Count.** The cores chosen in the $n$ squares of a packing are disjoint, so
   $n \le \sum \mu(C_i) \le M = n - 1/100000 < n$, a contradiction; so $s(n) \ge L$, and
   the same certificate bounds every larger count.

Each measure is $D_4$-invariant by construction: `expand` maps every stored rectangle to
its eight images, each of density $m/(8|R|)$. No point mass is present (`points` is
empty and `point_mass` is `0` in every certificate), every `scaling_factor` is $1$ and
every `scaling_source_digest` is the candidate’s own digest, and every audited input
encloses the expanded images, 2,496 to 6,824 per certificate.

## What Is New in the Measures

**Counts and sizes.** Nine counts get the source’s first mixed certificate: $n = 42$,
43, 44, 56, 57, 67 and 72 in `T-090` and $n = 53$ and 54 in `T-091`, each above the
source’s best rectangle certificate there.
The other nineteen supersede a mixed certificate of the source at the same count, and
none shares a rectangle with the one it supersedes, before or after scaling by the ratio
of the sides: each was built afresh, as its README says.
The sides run from $2739/400$ to $1993/200$; the rectangle counts from 312 ($n = 76$) to
853 ($n = 94$, `mixed_n94_L995`), the most of any rectangle density this checker has
decided here, past `mixed_n92_L969`’s 832. No two of the 28 share a rectangle count.

**Nodes and tables.** The oblique node totals run from 51.0 million ($n = 76$) to 123.2
million ($n = 90$), 1.444 billion for `T-090` and 1.225 billion for `T-091`; the largest
single direction is 968,259 nodes ($n = 90$, index 199), the most this checker has
recorded for one direction here, and under the node limit of 3,000,000 every manifest
sets. The axis tables run from 3,272,481 cells ($n = 76$) to 29,430,625 ($n = 94$,
`mixed_n94_L995`), the largest here, past `mixed_n65_L835`’s 26,532,801; its tarball,
38.5 MB, is the largest of any bundle this checker decides.

**Geometry.** Every rectangle lies strictly inside the container, with positive mass
(the least $2.9 \times 10^{-6}$, at $n = 54$) and least side $1.0 \times 10^{-3}$. The
least distance to a wall is $0.0010$ at $n = 67$ and $0.0012$ at $n = 71$, and up to
$0.28$ elsewhere; none touches a wall, so no boundary convention is exercised.
Between 0 and 34 orbits per certificate ($n = 94$, `mixed_n94_L994`) lie on a symmetry
axis or the diagonal and have fewer than eight distinct images; each still carries eight
copies of a mass of one eighth.

**Density.** The densest image carries $84{,}457$ per unit area ($n = 51$), from an
orbit of mass $0.90$ on rectangles about $10^{-3}$ on a side near the point
$(0.85, 1.0)$; above $35{,}000$ also at $n = 42$, 43, 56 and 94 (`mixed_n94_L995`).
These are point masses in effect; the area bound treats them as any other rectangle, so
they cost nodes and not soundness.
(Measured as the 3 October review measured it, orbit mass over one image’s area, the
largest is 675,652; see OF-4.)

**Minima.** The least recorded oblique bounds lie between $1 + 5.4 \times 10^{-11}$
($n = 58$, index 197) and $1 + 7.2 \times 10^{-9}$ ($n = 76$), with $n = 91$, 71, 88
(`mixed_n88_L96125`) and 84 also below $1 + 10^{-10}$; the threshold is exactly one and
the leaf test outward-rounded, so closeness costs nodes and not soundness, as on 3
October. The axis integer minima are $1.0020$ ($n = 91$) to $1.0087$ ($n = 51$), and no
table needs an exact patch.
The coordinate denominators reach $9 \times 10^{18}$ ($n = 73$), below the
$1.575 \times 10^{20}$ of `mixed_n73_L8809`; between 0 and 13 coordinates per
certificate ($n = 76$) sit at an integer distance from a wall.

None of this bears on soundness.

## Hypotheses the Checker Assumes

The list of the
[mixed review](review-2026-10-02-wand125-mixed-rectangle-bounds.md#hypotheses-the-checker-assumes)
applies unchanged; for each, what binds it here:

1. **The input encloses the expanded exact measure.** The retaining lanes’ `mixed-fetch`
   checked all 200 oblique inputs of each bundle, 5,600 in all, against the candidate
   recomputed by this repository’s tool; the two runs here repeated that for two
   bundles, and the two inputs regenerated by the shipped `export` are byte-identical to
   the shipped ones.
2. **Mass, nonnegativity, geometry, digests.** The audit, from the retained bytes;
   `--check` reproduces both receipts.
3. **The threshold.** $\Gamma = 1$ in every record the fetch receipts summarize, read
   from the input, with the leaf test `lower >= gamma.h`.
4. **$E$, $c_r$ and $s_r$.** Exact rationals enclosed in Python and read from the input;
   the shipped `replay` asserts the regenerated manifest, with its domain and $E$, equal
   to the saved one.
5. **The per-node domain lemma and the fold.** Prose; the rational instances are
   recomputed at all 200 oblique nodes, and the shipped drivers cannot misalign them
   (OC-4 of the 3 October review).
6. **The kernel.** Binary64 round-to-nearest without contraction or fast-math, under the
   compile line fixed in `compile_verifier`, with the C++ asserts live.
   The kernel uses the four basic operations and `nextafter` and no other library
   function, so its results do not depend on the platform once contraction is off
   (OF-2).
7. **Assertions on.** The source’s acceptance checks are `assert`s and its C++ exits
   zero on an unresolved angle (MV-1, observed on 3 October); the repository’s replay
   refuses to run with assertions off.
8. **Every angle finishes.** Each bundle’s records show an empty frontier at every angle
   under the node limit and the $2^{-40}$ floor; the replay must reproduce them.
9. **The axis tables’ integer arithmetic.** The guard $(\sum w)\,2^{32} < 2^{63}$ is
   independent of the coordinate denominator.
10. **Closed squares, disjoint interiors, boundaries without mass.** Prose.
11. **The tarball is the certificate’s.** New with these packets; bound as OF-1 says.

## The Trust Boundary

As before, coverage at the 200 oblique directions is decided by the source’s C++ alone,
angle zero by `verify_axis_certificate.py`’s integer tables, and everything else by
exact arithmetic in `expand`, `net_certificate`, `centre_domains` and this repository’s
audit. The replays here run the same code on the same inputs, so they reproduce the
source’s computation and are not a second algorithm; `C4` is not available from them.
The rectangle area kernel is Tokoharu’s byte for byte, shared with `T-068` and its
successors. What this repository adds independently is the exact premises, the input
binding, the tarball binding, the structural counts and the comparisons above.
Nothing the source publishes now binds a certificate to its tarball but its README and
its commit; the source’s audit, which used to, decided nothing in the argument.

## Where the Requests and the Record Differ

- **The comparisons.** Each README, root README section and comment compares with a
  published certificate of the source at the same count: the one it supersedes, or its
  best rectangle certificate there.
  For all sixteen of `T-090` that is the value the record reported before the import;
  for `T-091` it is at ten counts, and at $n = 88$ and 94 the comparison is with
  `T-090`’s $769/80$ and $497/50$ of earlier that day, which the evening packet README
  says. With no `completion-audit.json` there is no `improvement_lower`, so OC-1 and OC-2
  of the 3 October review cannot recur.
  Every margin in the 28 report entries and the 26 case records equals the exact
  difference, $3/1000$ ($n = 86$) to $3/80$ ($n = 57$) for `T-090` and $1/250$
  ($n = 73$) to $3/100$ ($n = 58$ and 87) for `T-091`, as the two claims state.
- **The reference values.** Twenty-five READMEs give Nagamochi’s closed form “(a
  reference value, see jlevy/squares#295)” and three Green’s reported bound ($n = 51$,
  67 and 84); in each case the larger of the two at that count.
  Every side exceeds the larger by at least $0.13$ (Nagamochi’s, at $n = 95$); the audit
  decides Green’s by enclosure and Nagamochi’s by squaring, and the record treats
  Nagamochi’s as reported only since `T-085`.
- **Monotonicity.** None carries: at each next count the record reports more after both
  imports, a value of these two entries at fifteen of them and an earlier one at the
  rest.
- **The checker’s name.** The READMEs say the checker is the one of `mixed_n87_L939` and
  `mixed_n65_L835`, the root README that of `mixed_n96_L996`, and the comments that of
  `mixed_n84_L940`: the same bytes in every case.
- **The second replays.** Each README says the full replay was run again from the
  tarball on a fresh Ubuntu 24.04.5 machine with g++ 13.3.0, Python 3.12.3 and NumPy
  2.5.3. Each `bundle.json` places the proof run on macOS: 23 on x86-64 with Python
  3.10.18 and NumPy 2.2.6, as on 3 October, and five of the evening twelve on arm64 with
  Python 3.14.7 and NumPy 2.5.3 (OF-2). None of this is checkable here, and the replay
  here decides.
- **Two packets, two revisions.** `mixed_n86_L9503` and `mixed_n69_L862` are pinned at
  both revisions and registered once, by `T-090`: one row each in the audit tool, one
  evidence entry each, outside `T-091`’s scope, its coverage entry and its replay plan,
  and mapped to `T-090` alone on #282 (`oct4-n86-n69`).
- **Supersession within the day.** At $n = 88$ and 94 the case records report `T-091`’s
  $481/50$ and $199/20$, each intake paragraph for `T-090` says its certificate was
  superseded, and `T-090` keeps its claim, which is about what the source reported.

## Findings

No blocking finding.

### OF-1 — Note: the tarball binding without the source’s audit is sufficient

Up to `2aff2076` each directory carried the source’s `completion-audit.json`, which
named the certificate’s and the tarball’s SHA-256. At these pins none does, and
`devtools.audit_wand125_point_and_mixed` binds a certificate pinned at a revision in
`WITHOUT_SOURCE_AUDIT` instead by the tarball’s digest in the pinned subtree list (which
`acquire_source` bound to the tarball’s Git blob at the pinned commit), by the size the
acquisition record pins, by a pinned tree with no `completion-audit.json` in that
directory, and by a README whose first line is the claim and which names the tarball and
its digest. That is the right shape, for three reasons.
The source’s audit was the source’s own statement and decided nothing in the argument;
what has always bound a bundle to the retained certificate is `mixed-fetch`, which
requires the tarball’s pinned digest and size, the bundle’s 621-entry file list with
nothing unlisted, its candidate, certificate, manifest and `code/` byte-identical to the
retained or `mixed_n50_L740` files, and all 200 inputs enclosing the candidate
recomputed here; the replay repeats it before its first angle.
The rule is two-sided and keyed to the revision, not to whether a file is found: a row
at an earlier revision without an audit is refused, and a row at these revisions whose
tree holds one is refused.
And what is lost with the audit is its comparison figures, which were OC-1’s and OC-2’s
subject. Re-derived here rather than taken from the receipts: all 28 tarballs downloaded
by their raw-file address have their pinned SHA-256, and each bundle’s `bundle.json`
names its candidate’s digest; the two fetched by Git have the Git blob of their pins.
A later revision will need its own entry in `WITHOUT_SOURCE_AUDIT`, and until then its
rows are refused, which is the safe direction.

### OF-2 — Note, in the source: five evening bundles record a new platform

The `bundle.json` of `mixed_n53_L76275`, `mixed_n54_L7685`, `mixed_n58_L7935`,
`mixed_n70_L86575` and `mixed_n88_L962` places the proof run on macOS arm64 with Python
3.14.7 and NumPy 2.5.3; the other 23, and the 22 the 3 October review read, on macOS
x86-64 with Python 3.10.18 and NumPy 2.2.6. No README or comment says so.
It does not bear on soundness: the C++ kernel is compiled with
`-ffp-contract=off -fno-fast-math`, asserts `FE_TONEAREST` and IEC 559 doubles, and
calls no library function but `nextafter`, so a record made on arm64 is the record
x86-64 must return, bit for bit.
Index 197 of `mixed_n58_L7935`, one of the five, was replayed here on x86-64 and
returned that record exactly.
A replay that does not return its record fails visibly; it cannot pass wrongly.
The replay receipts should name the bundle’s platform for these five so that a mismatch,
if one appears, is read with it.

### OF-3 — Note, in the source: rounded decimals in the READMEs

Thirteen of the 28 READMEs quote the reference value rounded at the fourth place before
an ellipsis (“$9.7750\ldots$” for $1 + \sqrt{77} = 9.77496\ldots$), each above the true
value by less than $5 \times 10^{-5}$; the other fifteen truncate.
Nineteen print the least oblique bound rounded up at ten places, as `mixed_n58_L7935`’s
“lowest is `1.0000000001`” for $1.0000000000544693$. The record cites the certificate’s
own values, so nothing rests on the decimals.
This is OC-5’s kind and needs no reply.

### OF-4 — Note, correcting the 3 October review: two measurements

The 3 October review’s “What Is New in the Measures” gives the least mass of its 22
measures as $4.0 \times 10^{-5}$ at $n = 71$; it is $1.19 \times 10^{-5}$ at $n = 73$
(`mixed_n73_L8809`), and $n = 86$, 87 and 88 are also below $4.0 \times 10^{-5}$. Its
densities (279,195 per unit area at $n = 51$) are an orbit’s mass over one image’s area,
eight times the density $m/(8|R|)$ each image carries, which is 34,899 there; the ratio
it draws with the afternoon’s densest is unaffected if both were measured alike.
Neither figure bears on soundness or on any record field, and the review stands
otherwise; this note is the correction, the retained document being left as written.

### OF-5 — Note, in the record: the two packets price `n86-L9503` differently

The 4 October packet plans `n86-L9503` at 10.2 CPU-hours and the evening packet, which
lists it beside its own twelve, at 10.3: the same estimate, 10.29, rounded two ways.
Neither total is affected, since `n69-L862` and `n86-L9503` are replayed once, under the
4 October plan.

## Claims by Evidential Status

- **Recomputed here in exact arithmetic:** the containment and domain identities; each
  measure’s count, side, core, rectangle count, containment, nonnegativity and mass; the
  candidate digests; each side against the record before each import, the next count
  after both, Green’s value (by enclosure) and Nagamochi’s (by squaring); the 28
  margins, and every margin and figure in the report entries and case records.
- **Checked on the pinned tarballs:** the pins, the bundles’ file lists and bindings to
  the packets, the driver’s preconditions and the enclosure of every input by the exact
  candidate (5,600 inputs), by the retaining lanes’ `mixed-fetch`, whose 28 receipts
  were checked here against the audit and the pins; and here, the SHA-256 of all 28
  tarballs and their `bundle.json`, two complete `mixed-fetch` runs, and two tarballs’
  Git blobs.
- **Replayed here:** two directions, index 197 of `mixed_n58_L7935` and index 92 of
  `mixed_n88_L96125`, each from an input regenerated by the shipped `export` and
  byte-identical to the shipped one, each returning the certificate’s status, nodes,
  leaves, lower bound and empty frontier.
- **Reviewed by reading:** that every checker file is a reviewed one byte for byte; that
  the audit tool’s binding without the source’s audit is two-sided and sufficient; and
  that nothing in the new measures meets a premise the earlier reviews left open.
- **Asserted by the source, not verified here:** the other 5,626 directional coverage
  statements, the 28 axis tables among them, and the pre-publication replays.

## What the Replays Must Show

For `V3/C3` on each count, with the repository’s range drivers (`mixed-shard` gives the
ranges), each tarball fetched at its pin by `--via git`, assertions on and one BLAS
thread, every direction passing only because the shipped function returned the
certificate’s own record, and the receipts committed as each range ends:

| Certificate | Tool name | Tarball (bytes) | Expect | Planned CPU-h |
| --- | --- | --- | --- | ---: |
| `mixed_n42_L68475` | `n42` | `85be7723…` (17,616,206) | 84,154,248 nodes; $1.00000000038929$ at 151; axis $1.0028835196743096$ over 8,294,400 | 7.3 |
| `mixed_n43_L69075` | `n43` | `d00555a2…` (14,474,874) | 94,327,372; $1.0000000005367042$ at 157; $1.0041643070776043$ over 5,832,225 | 6.8 |
| `mixed_n44_L69725` | `n44` | `016e64f3…` (16,301,347) | 61,963,016; $1.0000000003387242$ at 65; $1.0045516914701675$ over 6,953,769 | 4.9 |
| `mixed_n51_L747` | `n51-L747` | `dafc391a…` (19,602,681) | 73,294,118; $1.0000000014730677$ at 111; $1.008708130978039$ over 10,666,756 | 7.2 |
| `mixed_n56_L78025` | `n56` | `e363ae92…` (18,280,962) | 95,233,978; $1.0000000002061535$ at 1; $1.0049777014201027$ over 8,720,209 | 8.7 |
| `mixed_n57_L78725` | `n57` | `4e8df555…` (22,186,683) | 92,644,514; $1.0000000005590681$ at 194; $1.0052281611253358$ over 12,752,041 | 9.9 |
| `mixed_n67_L8475` | `n67` | `c8f49ba9…` (19,409,082) | 80,893,626; $1.0000000001997127$ at 199; $1.007364912414975$ over 10,131,489 | 8.0 |
| `mixed_n69_L862` | `n69-L862` | `3408beeb…` (22,932,912) | 108,821,066; $1.0000000022127755$ at 163; $1.0024591768578492$ over 12,687,844 | 12.1 |
| `mixed_n72_L876` | `n72` | `36a739ae…` (20,039,614) | 120,543,194; $1.000000000255855$ at 138; $1.0052632530569092$ over 9,634,816 | 11.9 |
| `mixed_n75_L894` | `n75-L894` | `a576f418…` (25,606,631) | 120,119,252; $1.000000000242291$ at 194; $1.0035068984112805$ over 14,569,489 | 14.2 |
| `mixed_n84_L94075` | `n84-L94075` | `01274b16…` (23,518,582) | 92,867,418; $1.000000000096838$ at 75; $1.0054208378418148$ over 14,386,849 | 10.6 |
| `mixed_n86_L9503` | `n86-L9503` | `8752a3e5…` (21,587,707) | 95,514,032; $1.00000000053539$ at 195; $1.005655662978928$ over 11,648,569 | 10.2 |
| `mixed_n88_L96125` | `n88-L96125` | `ca813e22…` (20,227,627) | 110,846,936; $1.0000000000855427$ at 92; $1.005555488215099$ over 10,080,625 | 11.3 |
| `mixed_n93_L988` | `n93-L988` | `97438276…` (20,653,208) | 71,180,134; $1.0000000007671606$ at 184; $1.0038863181990088$ over 10,660,225 | 7.2 |
| `mixed_n94_L994` | `n94-L994` | `1de58050…` (26,509,834) | 82,482,752; $1.0000000019115551$ at 166; $1.0023446755279655$ over 14,130,081 | 10.4 |
| `mixed_n95_L9965` | `n95-L9965` | `1397341b…` (18,404,631) | 59,167,032; $1.000000000398967$ at 23; $1.0078342043789137$ over 7,257,636 | 5.6 |
| `mixed_n53_L76275` | `n53` | `8ad91b2f…` (20,679,843) | 80,696,352; $1.0000000008724097$ at 144; $1.0027812868265755$ over 11,075,584 | 8.3 |
| `mixed_n54_L7685` | `n54` | `cb7ba0c8…` (14,726,624) | 86,248,776; $1.000000000441897$ at 130; $1.0035007233937916$ over 5,784,025 | 6.4 |
| `mixed_n58_L7935` | `n58-L7935` | `64b39063…` (23,811,454) | 84,183,576; $1.0000000000544693$ at 197; $1.0038605675365069$ over 13,645,636 | 9.2 |
| `mixed_n70_L86575` | `n70-L86575` | `5e9d7b0b…` (21,232,906) | 118,708,596; $1.0000000012817085$ at 52; $1.003788998037493$ over 11,029,041 | 12.3 |
| `mixed_n71_L8721` | `n71-L8721` | `b44d6a37…` (22,323,926) | 114,091,518; $1.0000000000794815$ at 155; $1.0041688505547262$ over 12,089,529 | 12.2 |
| `mixed_n73_L8813` | `n73-L8813` | `1be9a7fd…` (18,989,101) | 116,555,688; $1.000000000257511$ at 59; $1.0055622862385354$ over 9,174,841 | 10.9 |
| `mixed_n76_L8965` | `n76-L8965` | `2e2cf21c…` (11,918,563) | 50,978,010; $1.0000000071639858$ at 195; $1.0080659385288$ over 3,272,481 | 3.1 |
| `mixed_n87_L958` | `n87-L958` | `d5a5c755…` (24,859,047) | 107,739,744; $1.0000000002556373$ at 129; $1.0044705977715256$ over 14,348,944 | 13.0 |
| `mixed_n88_L962` | `n88-L962` | `af5e3ec7…` (23,003,472) | 106,388,036; $1.0000000001523959$ at 182; $1.0075198562530931$ over 12,439,729 | 12.1 |
| `mixed_n90_L973` | `n90-L973` | `00405198…` (21,824,125) | 123,232,842; $1.0000000003386997$ at 151; $1.0063623824958494$ over 11,242,609 | 13.1 |
| `mixed_n91_L97625` | `n91-L97625` | `23cccb32…` (17,633,045) | 120,868,018; $1.00000000007525$ at 179; $1.0019646623662337$ over 7,711,729 | 10.7 |
| `mixed_n94_L995` | `n94-L995` | `1a02b7c3…` (38,451,298) | 115,335,002; $1.0000000002976601$ at 134; $1.0031738677875834$ over 29,430,625 | 19.6 |

The first sixteen are `T-090`’s, planned at 146.3 CPU-hours over eight runners
(`mixed-price` gives 130.8, scaled by the observed ratio 1.119); the source’s own
oblique seconds total 180.2 CPU-hours, 1.38 times the estimate.
The other twelve are `T-091`’s, planned at 130.9 over six runners (116.9 unscaled); the
source’s seconds total 137.7. `mixed_n94_L995` alone is 19.6, with the largest axis
table here. The two directions run here, on a shared host under load, took 587 and 235
seconds against the source’s 337 (on arm64) and 264, so budget wall time toward the
source’s figure. The checker’s negative control is on file from $n = 37$, and the bytes
are the same.

Each count’s verified value moves to the side of the largest certificate at that count
whose own replay passes.
At $n = 88$ and 94 that is `T-091`’s if both pass, and `T-090`’s if only it does.
The values increase strictly with $n$ within each run of counts the two entries cover
(42–44, 53–54, 56–58, 69–73, 75–76, 86–88, 90–91 and 93–95), so a count whose replay
fails keeps the larger of its standing verified value and the replayed value one count
below. The entries these certificates supersede in the verified lane (`T-071`’s
`mixed_n84_L940` at $n = 84$) keep their claims and scores.

## Significance

`S3` confirmed for both.
The 28 bounds are further sizes from the generator and checker of `T-069`, `T-071`,
`T-072`, `T-075` and `T-082`, at counts from 42 to 95. Each was above what the record
reported at its count when it was registered, by $0.003$ to $0.0375$, smaller steps than
`T-082`’s; nine are the source’s first mixed certificates at their counts, and at
$n = 44$, 76 and 95 the new values are within $0.0275$, $0.035$ and $0.035$ of the sides
7, 9 and 10 of the best known packings, without settling any count.
Substantive case results; no new technique, and no disputed value resolved.

## Disposition

All 28 certificates are accepted by this review with no defect open.
For `T-090` and `T-091`, `C1` once this document is recorded as `external_review` on
their 28 report entries (`informally-verified`, 2026-10-05) and listed in each entry’s
`reviews` with verdict `accepted`, with the document mapped as a retained review;
`V3/C3` for each count when its replay passes.
The reviewer, for both entries: an AI agent prompted separately from the lane that
retained the packets and registered `T-090` and `T-091`, blind to any replay and not to
retention, model unstated.
OF-2’s request is for the replay lane.
The reply on issue 282 may mention OF-2 once, since the READMEs describe one platform
and five bundles record another; nothing else here is for the author.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
