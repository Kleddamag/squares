# wand125 Certificates of 3 October: Review of 22 Mixed Rectangle-Measure Bounds From `n = 51` to `n = 96`

Between 02:49 and 17:58 UTC on 3 October wand125/square-packing-bounds published 22
rectangle densities checked at coverage one, at $n = 51$, 52, 55, 58, 69 to 71, 73 to 76
and 86 to 96, all pinned here at `2aff2076`. Six raise a certificate of the same source
that this record already verifies at the same count ($n = 76$, 87, 90, 91, 92 and 96);
the other sixteen are the source’s first mixed certificates at their counts.
None brings a new checker.
Every file of every `code/` directory, and every `requirements.txt`, has the SHA-256 and
the Git blob of the `mixed_n50_L740` copy the 28 September packet retains, so the
checker is `mixed_rotated_verify.cpp` (`89b674a6…`), read on 28 September and again on 2
October. There is nothing to diff, and this review re-derives what the new measures add:
their sizes, structure, comparisons and records.

Every exact premise that can be read from the retained files holds for all 22, every
check a replay makes before its first angle passed on the 22 pinned tarballs, and the
two directions replayed here from regenerated inputs returned the certificates’ own
records. No blocking defect was found.
Five non-blocking findings are recorded: an `improvement_lower` that is not a lower
bound at two counts, as MX-2 and AF-1 found at five; comparison notes that name values
no published certificate held; MV-1, which stands and was observed here; a correction to
MV-2, whose case the shipped drivers cannot reach; and small README matters.
All 22 values stand as reported until each complete replay passes here.
`S3` is proposed for `T-082`.

This is the review of stage 4 of the result import for the 22 requests of 3 October on
jlevy/squares#282, written on 2026-10-03 by an AI agent prompted separately from the
lane that retained the packet and drafted `T-082`, working from that lane’s brief and
the retained files; model unstated.
It was written after retention and the pre-replay checks and before any replay, so it is
a review of the mathematics and the records, blind to the replay and not to retention.
It registers nothing and moves no bound.

## Scope and Evidence

| Claim | Directory | Commit (UTC) | Rectangles | Mass | Oblique nodes the source records |
| --- | --- | --- | ---: | --- | ---: |
| $s(51) \ge 373/50$ | `mixed_n51_L746` | `06a1e9d6`, 07:48:12 | 446 | $5099999/100000$ | 69,985,426 |
| $s(52) \ge 151/20$ | `mixed_n52_L755` | `3d365c47`, 06:30:51 | 455 | $5199999/100000$ | 74,571,040 |
| $s(55) \ge 966/125$ | `mixed_n55_L7728` | `2d22930c`, 10:37:10 | 303 | $5499999/100000$ | 77,422,814 |
| $s(58) \ge 1581/200$ | `mixed_n58_L7905` | `7bcfef5e`, 08:26:30 | 319 | $5799999/100000$ | 36,266,794 |
| $s(69) \ge 2153/250$ | `mixed_n69_L8612` | `2aff2076`, 17:58:33 | 556 | $6899999/100000$ | 99,544,986 |
| $s(70) \ge 3459/400$ | `mixed_n70_L86475` | `13188dd1`, 16:17:10 | 495 | $6999999/100000$ | 100,441,798 |
| $s(71) \ge 1741/200$ | `mixed_n71_L8705` | `044c1271`, 16:14:04 | 471 | $7099999/100000$ | 100,569,226 |
| $s(73) \ge 8809/1000$ | `mixed_n73_L8809` | `b780f588`, 16:30:42 | 450 | $7299999/100000$ | 100,339,538 |
| $s(74) \ge 3547/400$ | `mixed_n74_L88675` | `ce653063`, 15:58:27 | 505 | $7399999/100000$ | 90,044,046 |
| $s(75) \ge 223/25$ | `mixed_n75_L892` | `216e4b4a`, 06:44:51 | 340 | $7499999/100000$ | 39,920,680 |
| $s(76) \ge 224/25$ | `mixed_n76_L896` | `3d2089e8`, 12:59:30 | 341 | $7599999/100000$ | 45,154,982 |
| $s(86) \ge 19/2$ | `mixed_n86_L950` | `bbb78b2e`, 04:27:40 | 509 | $8599999/100000$ | 94,779,600 |
| $s(87) \ge 191/20$ | `mixed_n87_L955` | `239e95fe`, 04:40:33 | 509 | $8699999/100000$ | 86,412,558 |
| $s(88) \ge 48/5$ | `mixed_n88_L960` | `bf23abf3`, 08:24:06 | 443 | $8799999/100000$ | 92,907,150 |
| $s(89) \ge 193/20$ | `mixed_n89_L965` | `b1dc461d`, 05:16:14 | 416 | $8899999/100000$ | 109,970,334 |
| $s(90) \ge 389/40$ | `mixed_n90_L9725` | `4a4f2f81`, 10:48:48 | 571 | $8999999/100000$ | 110,810,810 |
| $s(91) \ge 39/4$ | `mixed_n91_L975` | `ee10b727`, 08:59:53 | 457 | $9099999/100000$ | 128,561,314 |
| $s(92) \ge 977/100$ | `mixed_n92_L977` | `5baaec27`, 12:47:42 | 345 | $9199999/100000$ | 37,604,722 |
| $s(93) \ge 493/50$ | `mixed_n93_L986` | `e11387ec`, 05:03:43 | 443 | $9299999/100000$ | 94,366,242 |
| $s(94) \ge 248/25$ | `mixed_n94_L992` | `caabf77f`, 03:13:50 | 488 | $9399999/100000$ | 57,370,560 |
| $s(95) \ge 249/25$ | `mixed_n95_L996` | `99332265`, 02:49:42 | 438 | $9499999/100000$ | 53,447,460 |
| $s(96) \ge 997/100$ | `mixed_n96_L997` | `1695131c`, 17:24:51 | 376 | $9599999/100000$ | 72,598,690 |

The packet is
[`wand125-mixed-bounds-2026-10-03`](../../../packing/resources/web/wand125-mixed-bounds-2026-10-03/README.md).
The import registers all 22 as `T-082`, drafted at `332e732b` with this review’s fields
left open. Each directory has exactly one commit, which adds it and changes the root
README and nothing else, and each was announced in its own comment on issue 282 within a
minute. Each of the 22 commit messages ends in a trailer naming an AI assistant as
co-author, followed in the last eight, from `5baaec27`, by a session-link trailer; the
root README’s Status section says parts of the work were produced with AI assistance
under human direction.

Read in full: the 22 directory READMEs, `manifest.json` and `completion-audit.json`
files; the root README’s 22 new sections, its Attribution and Status sections and its
diff from `b00fc70f`; the 22 commit messages; the 22 comments of 3 October on issue 282;
the packet README, `acquisition/` records and receipts; the draft `T-082` and its 22
report entries; and the retained `mixed_n50_L740/code/` files the drivers run
(`mixed_net_audit.py`, `mixed_density_check.py`, `mixed_rotated_verify.py`,
`verify_mixed_full_proof.py`, `verify_rotated_result.py`, `verify_axis_certificate.py`,
and `main` of `mixed_rotated_verify.cpp`), with the audit functions `mixed_certificate`,
`green_facts`, `n50_net`, `n50_centre_domains`, `driver_preconditions` and
`replay_runtime`. Read again, for what they assume: the
[28 September review of the mixed verifier](review-2026-09-28-wand125-n50-mixed-verifier.md),
the
[2 October review of the mixed bounds](review-2026-10-02-wand125-mixed-rectangle-bounds.md)
and the
[2 October review of the afternoon certificates](review-2026-10-02-wand125-afternoon-certificates.md).

Run here, with the project CPython 3.14.7 on x86-64 Linux:

- `mixed-audit wand125-mixed-bounds-2026-10-03 --check` (`RECEIPT_MATCHES`),
  `devtools.retained_data check` on the packet (no problem reported) and
  `devtools.acquire_source wand125-mixed-bounds-2026-10-03 --check`
  (`PACKET_MATCHES_ITS_CONTRACT`), each from the retained bytes;
- `mixed-price` and `mixed-shard wand125-mixed-bounds-2026-10-03 --runners 8`;
- exact comparisons of each side, each `compared_with` and each `improvement_lower` with
  what the record reported before this import (the case records at the packet’s commit
  `8b881c38`), with Green’s value and with Nagamochi’s
  $1 + \sqrt{n - 2\lfloor\sqrt n\rfloor + 1}$, and of the decimals the READMEs quote;
- exact structural counts of the 22 measures from the retained candidates (walls,
  densities, orbits, coordinate denominators, and a pairwise comparison of supports);
- on the 22 unpacked bundles, read and not modified: the SHA-256 of each tarball against
  the pin, `files-sha256.json` of $n = 96$ in full, the shipped `centre_domains` on each
  bundle’s candidate, and the domain, `E`, index and threshold of each of the 4,400
  angle manifests against it;
- the retained checker compiled with the shipped compile line (g++ 13.3.0), and two
  directions replayed from inputs regenerated by the shipped `export`: index 2 of
  `mixed_n92_L977`, its cheapest direction (116,503 nodes), and index 79 of
  `mixed_n73_L8809`, the least bound of the 22; plus one input with the threshold raised
  (OC-3); and
- in the source’s history (a blob-filtered clone with every commit), the tree at the pin
  and a search of every added or deleted path for certificates at the values the
  comparison notes cite.

No complete replay was run: two of the 4,422 directions were.

## The Argument From Certificate to Bound

The argument is the one the earlier reviews re-derived, and nothing in it depends on the
side, the count or the number of rectangles except through running time.
For a nonnegative measure $\mu$ on the container $[0, L]^2$ of total mass $M < n$:

1. **Containment.** With $B = 9977/10000$ and the 201 half-angle tangents
   $t_r = r \cdot 83/40000$, $B(1 + 83/40000) = 399908091/400000000 < 1$,
   $(1 + t_{200})^2 - 2 = 89/40000 > 0$, and the last bin reaches below $\pi/4$,
   $(1 + \tfrac{399}{2}\cdot\tfrac{83}{40000})^2 - 2 = -4544311/6400000000 < 0$. So
   every unit square in the container, at any orientation, holds in its open interior a
   closed core of side $B$ at the net angle its orientation is assigned to.
   These are the `net` blocks of all 22 manifests and certificates, recomputed by the
   audit.
2. **Coverage.** At each net angle every such core has $\mu \ge 1$. At node $r \ge 1$
   the checker decides it over the centre domain $[L/2, L - \rho(a_r)]^2$, where
   $a_r = t_r - D/2$ and $\rho(a) = (1 + 2a - a^2)/(2(1 + a^2))$ is the half axis extent
   of a unit square at half-angle $a$: the union of the admissible centres over the
   node’s bin, folded into one quadrant by a quarter turn, with orientations above
   $\pi/4$ sent back by the diagonal reflection, which fixes that quadrant.
   It omits a strip of width $\rho(a_r) - B(c_r + s_r)/2 \ge 1.2050 \times 10^{-4}$ of
   Tokoharu’s domain, the same for all 22 since it depends on $B$ and the net alone, and
   its half-side $E_r = L/2 - \rho(a_r)$ is at least $3.0229$ at the smallest side here,
   $L = 373/50$. Angle zero is decided by integer tables over $[L/2, L - 1/2]^2$.
3. **Count.** The cores chosen in the $n$ squares of a packing are disjoint, so
   $n \le \sum \mu(C_i) \le M = n - 1/100000 < n$, a contradiction; so $s(n) \ge L$, and
   the same certificate bounds every larger count.

Each measure is $D_4$-invariant by construction: `expand` maps every stored rectangle to
its eight images, each of density $m/(8|R|)$. No point mass is present (`points` is
empty and `point_mass` is `0` in every certificate), every `scaling_factor` is $1$ and
every `scaling_source_digest` is the candidate’s own digest, and every audited input
encloses the expanded images, 2,424 to 4,568 per certificate, in the source’s order.

## What Is New in the Measures

**Sizes.** The sides run from $373/50$ to $997/100 = 9.97$, the largest side of any
rectangle density checked at coverage one here, past $249/25$; the rectangle counts from
303 to 571, within the 279 to 832 of the earlier certificates.
The oblique node totals run from 36.3 million ($n = 58$) to 128.6 million ($n = 91$),
the most of any rectangle density here, and 1.773 billion in all; the largest single
direction is 936,567 nodes ($n = 91$, index 200), under the node limit of 3,000,000
every manifest sets.

**Geometry.** Every rectangle lies strictly inside the container, with positive mass
(the least $4.0 \times 10^{-5}$, at $n = 71$) and least side $1.0 \times 10^{-3}$. The
least distance to a wall is $0.0010$ at $n = 74$, 86 and 89 and up to $0.28$ elsewhere;
none touches a wall, so no boundary convention is exercised.
Between 0 and 26 orbits per certificate lie on a symmetry axis or the diagonal and have
fewer than eight distinct images; each still carries eight copies of a mass of one
eighth.

**Density.** The densest rectangles reach 279,195 per unit area at $n = 51$, and above
150,000 at $n = 52$, 69, 71 and 91, about 47 times the afternoon’s densest: rectangles
about $10^{-3}$ on a side near the points $(1, 2)$ and $(1, 1)$, each carrying $0.2$ to
$0.6$ of mass, close to point masses in effect.
The area bound treats them as any other rectangle; they cost nodes and not soundness.

**Construction.** Each README says the measure was built from scratch from a structured
initial measure with bands at integer distances from the walls; in the final measures
between 0 and 23 coordinates of each certificate sit at an integer distance from a wall,
so the repair moved most of them.
Two pairs share a rectangle count, $n = 86$ and 87 at 509 and $n = 88$ and 93 at 443,
and share no rectangle: neither is one support scaled, as $n = 82$’s was from
$n = 83$’s.

**Minima.** The least recorded oblique bounds lie between $1 + 1.4 \times 10^{-10}$
($n = 86$) and $1 + 6.2 \times 10^{-9}$ ($n = 75$), except $n = 73$’s
$1 + 4.4 \times 10^{-11}$ at index 79, as near one as `mixed_n90_L960`’s
$1 + 4.2 \times 10^{-11}$; the threshold is exactly one and the leaf test
outward-rounded, so closeness costs nodes and not soundness, and MV-4’s point stands.
The axis integer minima are $1.0011$ ($n = 87$) to $1.0100$ ($n = 51$), over 3,489,424
($n = 96$) to 13,271,449 ($n = 90$) cells, and no table needs an exact patch.
The tables’ coordinate denominators reach $1.575 \times 10^{20}$ ($n = 73$) and
$6.3 \times 10^{19}$ ($n = 75$), above the $1.68 \times 10^{19}$ the mixed review read
at $n = 65$; as there, the denominator never enters the `int64` products, the
coordinates being scaled in Python integers and the products bounded by the guard
$(\sum w)\,2^{32} < 2^{63}$.

None of this bears on soundness.

## Hypotheses the Checker Assumes

The list of the
[mixed review](review-2026-10-02-wand125-mixed-rectangle-bounds.md#hypotheses-the-checker-assumes)
applies unchanged; for each, what binds it here:

1. **The input encloses the expanded exact measure.** The retaining lane’s `mixed-fetch`
   checked all 200 oblique inputs of each bundle, 4,400 in all, against the candidate
   recomputed by this repository’s tool, and the two inputs regenerated here by the
   shipped `export` are byte-identical to the shipped ones.
2. **Mass, nonnegativity, geometry, digests.** The audit, from the retained bytes;
   `--check` reproduces its receipt.
3. **The threshold.** $\Gamma = 1$ in every one of the 4,400 angle manifests, read from
   the input, with the leaf test `lower >= gamma.h`.
4. **$E$, $c_r$ and $s_r$.** Exact rationals enclosed in Python and read from the input;
   each manifest’s $E$ equals $L/2 - \rho(a_r)$ recomputed here.
5. **The per-node domain lemma and the fold.** Prose; the rational instances are
   recomputed at all 200 oblique nodes, and the domains are paired with the right angles
   (OC-4).
6. **The kernel.** Binary64 round-to-nearest without contraction or fast-math, under the
   compile line fixed in `compile_verifier`; the C++ asserts are live, since that line
   sets no `NDEBUG`. Unchanged bytes, reviewed before.
7. **Assertions on.** The source’s acceptance checks are `assert`s and its C++ exits
   zero on an unresolved angle (OC-3); the repository’s replay refuses to run with
   assertions off.
8. **Every angle finishes.** Each bundle’s records show an empty frontier at every angle
   under the node limit and the $2^{-40}$ floor; the replay must reproduce them.
9. **The axis tables’ integer arithmetic.** The guard is independent of the denominator,
   as above.
10. **Closed squares, disjoint interiors, boundaries without mass.** Prose.

## The Trust Boundary

As before, coverage at the 200 oblique directions is decided by the source’s C++ alone,
angle zero by `verify_axis_certificate.py`’s integer tables, and everything else by
exact arithmetic in `expand`, `net_certificate`, `centre_domains` and this repository’s
audit. The replays here run the same code on the same inputs, so they reproduce the
source’s computation and are not a second algorithm; `C4` is not available from them.
The rectangle area kernel (`area_lower` and `slice`) is Tokoharu’s byte for byte, so the
rectangle rungs of `T-068` and its successors share it with these 22. What this
repository adds independently is the exact premises, the input binding, the structural
counts and the comparisons above.

## Where the Requests and the Record Differ

- **The comparison values.** Every `compared_with` is an exact rational equal to what
  its note names, and none is Green’s value, so a rounded Green value, the cause of MX-2
  and AF-1, cannot recur; but at $n = 88$ and 93 it is below the bound standing there
  (OC-1), and at six counts it names a value no certificate held when it was written
  (OC-2). At the other fourteen the source’s improvement equals the margin over the
  record.
- **The checker’s name.** The READMEs say the checker is the one of `mixed_n87_L939` and
  `mixed_n65_L835`, the root README that of `mixed_n96_L996`, and the comments that of
  `mixed_n84_L940`: the same bytes in every case (OC-5).
- **The second replays.** Each README says the full replay was run again from the
  tarball on a fresh Ubuntu 24.04.5 machine with g++ 13.3.0, Python 3.12.3 and NumPy
  2.5.3. Each bundle’s `bundle.json` places the proof run on macOS x86-64 with Python
  3.10.18 and NumPy 2.2.6, and the $n = 52$ route says the run was moved to another
  machine after preemptions.
  None of this is checkable here, and the replay here decides.
- **Monotonicity in the comments.** The comments on $n = 86$, 87 and 89 say they give
  $s(87), s(88) \ge 9.5$, $s(88) \ge 9.55$ and $s(90) \ge 9.65$; each is right, and each
  was overtaken the same day by the batch’s own certificate at that count.
- **The gap at $n = 95$.** The comment’s “the gap to the best known packing (side 10) is
  now 0.04” is right against the record’s upper bound; at $n = 96$ it is now $0.03$.
- **The packet README.** Its sentence that every comparison is “the source’s own earlier
  value at that count” is right about where the values come from and misses OC-1, and
  its list of six comparison values no certificate at the pin holds is right count by
  count, though two of them now follow by monotonicity (OC-2).

## Findings

No blocking finding.

### OC-1 — Low, in the source: `improvement_lower` at $n = 88$ and 93 is not a lower bound

The $n = 88$ audit compares with $3791/400 = 9.4775$ (“record n88 9.4775”), the source’s
rectangle rung, and states $49/400 = 0.1225$. The record reported $237/25$ there, from
`mixed_n87_L948` by monotonicity (`T-075`), and `mixed_n87_L955`, published 3 h 44 min
earlier, gives $191/20$; the directory README and the comment name that $9.55$
themselves. The $n = 93$ audit compares with $973/100$ (“record n93 9.73”) and states
$13/100$; the record reported $39/4$ there, from `mixed_n92_L975` by monotonicity
(`T-075`), which the README names, and the source’s own `rect_n93_L9735` is also above
$9.73$. So both figures overstate the margins: over the record before this import they
are $3/25 = 0.12$ and $11/100 = 0.11$, and over the source’s own tree at the pin $1/20$
(over $191/20$) and $9/100$ (over `mixed_n92_L977`’s $977/100$). The bounds are
unaffected, and the READMEs’ comparisons are right.
The draft report entries already state $0.12$ and $0.11$; they should also say the
source’s `improvement_lower` is not a lower bound, as the entries for MX-2 and AF-1 at
$n = 83$, 84, 85 and 87 do, and the packet README’s comparison paragraph should say so.
This is MX-2 and AF-1 at two more counts, with a superseded rung in place of a rounded
Green value, and the reply on issue 282 should say so once.

### OC-2 — Note, in the source: comparison notes that name values no published certificate held

Six audits compare with a value their note calls “our certified”: $8639/1000$ at
$n = 70$, $87/10$ at 71, $48/5$ at 89, $97/10$ at 90, $247/25$ at 94 and $248/25$ at 95.
No certificate at those counts with those values appears anywhere in the source’s
history up to the pin, whose only deleted directory is the withdrawn `mixed_n50_L7318`.
Two of the values now hold by monotonicity: `mixed_n88_L960`, published 3 h 8 min after
the $n = 89$ certificate, gives $48/5$ at $n = 89$, and `mixed_n94_L992`, 24 minutes
after the $n = 95$ certificate, gives $248/25$ at $n = 95$; the other four remain
unpublished. Each value lies above what the record reported, so each stated improvement
understates the margin over the record ($17/2000$ against $1/50$ at $n = 70$, $1/200$
against $1/50$ at 71, $1/20$ against $17/200$ at 89, $1/40$ against $1/8$ at 90, $1/25$
against $23/200$ at 94, and $1/25$ against $541/5000$ at 95) and remains a lower bound
on it.
Two further notes give the record’s earlier values, $9.46$ at $n = 87$ and $9.645$
at 91, where it reported $237/25$ and $97/10$ by `T-075`; the compared values there are
right. This is AF-2’s kind; nothing in the record rests on these values.

### OC-3 — Note: MV-1 stands on these bytes, and was observed

`mixed_rotated_verify.cpp` still writes `ANGLE_UNRESOLVED` (line 139) and falls off the
end of `main` with exit status zero, where Tokoharu’s returns 3; and the acceptance
checks of `verify_mixed_full_proof.py` (10), `verify_rotated_result.py` (4) and
`verify_axis_certificate.py` (20) are still `assert` statements.
On the retained checker compiled here, the shipped direction-2 input of `mixed_n92_L977`
with $\Gamma$ raised to $11/10$ returned `ANGLE_UNRESOLVED` after 76 nodes, with a
76-box frontier at the $2^{-40}$ floor, and exit status 0. Under `python -O` the driver
would skip line 33’s status and frontier check and the replay’s record comparison, and
could write `ALL_ANGLES_VERIFIED_AND_REPLAYED` over an unresolved angle.
The repository’s replay refuses to start with assertions off (`replay_runtime`) and
passes a direction only when the shipped function returned the certificate’s own record,
so the replay path is safe and a consumer that trusts exit codes is not.
Non-blocking, as on 28 September; there is nothing new to tell the author.

### OC-4 — Note, correcting MV-2: the shipped drivers cannot reach the misalignment

MV-2 said a net with a skipped node would silently pair angles with the wrong domains,
because `centre_domains` skips a node with no assigned orientation (`continue` at
`mixed_net_audit.py:60`) and the drivers index its list by net index.
Such a net never reaches that index.
`net_certificate` refuses any net whose last node has
$(1 + (\mathit{last} - \tfrac12)\,\mathit{step})^2 \ge 2$ (line 28), and since
$a_j = \max(0, (j - \tfrac12)\,\mathit{step})$ does not decrease with $j$, that is
exactly the condition under which line 60 would skip some node.
Both positional uses call it first with the same step and last: `export` at line 32 and
the full-proof driver at line 21, as does this repository’s `driver_preconditions`. So
the hazard remains only for a direct caller of `centre_domains`. For these 22 it is
ruled out twice over: none declares a `proof_net`, so the net is the default one, whose
last bin gives $-4544311/6400000000 < 0$; and on each unpacked bundle the shipped
`centre_domains` returned 201 records with index equal to position, and each of the
4,400 angle manifests carries the domain of its own net index, equal to the one
recomputed here. The receipt’s `centre_domains.nodes` of 200 is the constant `N50_LAST`,
and the widths beside it are recomputed by index, so that field alone shows nothing
about alignment and should not be cited for it.

### OC-5 — Note, in the source: README details

All 22 READMEs name `mixed_n87_L939`, superseded at its count by four later
certificates, and `mixed_n65_L835` as the certificates sharing the checker (MX-4); each
explains “not in tokoharu’s format” by the threshold alone and not the per-node domain
(MV-3). Seven quote Nagamochi’s value rounded at the fourth place before an ellipsis, at
$n = 69$, 70, 73, 89, 92, 93 and 96 (“$9.7178\ldots$” for $9.71779\ldots$), each above
the true value by less than $5 \times 10^{-5}$; the other thirteen truncate, and Green’s
“$7.3174\ldots$” at $n = 51$ and 52 is the truncation of $7.31742601\ldots$, Theorem 9
at $k = 7$ from $n = 50$. The $n = 73$ README’s “lowest is `1.0000000000`” is
$1.000000000044086$ printed to ten places.
Every name a README cites is a directory in the tree at the pin, and each “622 files”
and “621 file hashes” is right: the hash list covers every other file.

## Claims by Evidential Status

- **Recomputed here in exact arithmetic:** the containment and domain identities; each
  measure’s count, side, core, rectangle count, containment, nonnegativity and mass; the
  candidate digests; the comparisons of each side and each source value with the record,
  with Green’s value (by enclosure) and with Nagamochi’s (by squaring); the 22 margins
  over the record before this import.
- **Checked on the pinned tarballs:** the pins, the bundles’ file lists and bindings to
  the packet, the driver’s preconditions, and the enclosure of every input by the exact
  candidate (4,400 inputs), by the retaining lane’s `mixed-fetch`, whose receipts were
  read here; and here, on the same unpacked bundles, the tarball digests, the alignment
  of all 4,400 domains and the axis tables’ metadata.
- **Replayed here:** two directions, index 2 of `mixed_n92_L977` and index 79 of
  `mixed_n73_L8809`, each from an input regenerated by the shipped `export` and
  byte-identical to the shipped one, each returning the certificate’s status, nodes,
  leaves, lower bound and empty frontier.
- **Reviewed by reading:** that every checker file is a reviewed one byte for byte; that
  `net_certificate` precedes every positional use of `centre_domains`; and that nothing
  in the new measures meets a premise those reviews left open.
- **Asserted by the source, not verified here:** the other 4,420 directional coverage
  statements, and the pre-publication replays.

## What the Replays Must Show

For `V3/C3` on each count, with the repository’s range drivers (`mixed-shard` gives the
ranges for eight runners), each tarball fetched at `2aff2076` by `--via git` (the
pre-replay receipts record it as supplied from the sparse checkout), assertions on and
one BLAS thread, every direction passing only because the shipped function returned the
certificate’s own record, and the receipts committed as each range ends:

| Certificate | Tool name | Tarball (bytes) | Expect | Planned CPU-h |
| --- | --- | --- | --- | ---: |
| `mixed_n51_L746` | `n51` | `0729dce3…` (17,762,923) | 69,985,426 nodes; $1.0000000003200482$ at 107; axis $1.009964249145509$ over 9,048,064 | 6.3 |
| `mixed_n52_L755` | `n52` | `f9f12c57…` (18,083,771) | 74,571,040; $1.0000000004141971$ at 170; $1.0061071116246354$ over 8,862,529 | 6.9 |
| `mixed_n55_L7728` | `n55` | `cf91a3fe…` (11,738,199) | 77,422,814; $1.0000000014125006$ at 114; $1.0076941602220786$ over 3,837,681 | 4.8 |
| `mixed_n58_L7905` | `n58` | `d11b4d3f…` (12,665,333) | 36,266,794; $1.0000000036417236$ at 109; $1.0070002486141336$ over 4,239,481 | 2.3 |
| `mixed_n69_L8612` | `n69` | `0468c96a…` (23,034,012) | 99,544,986; $1.0000000003818312$ at 180; $1.0028461704678193$ over 12,482,089 | 11.2 |
| `mixed_n70_L86475` | `n70` | `fa020a0c…` (20,534,888) | 100,441,798; $1.000000002986998$ at 112; $1.0037504910100976$ over 10,771,524 | 10.0 |
| `mixed_n71_L8705` | `n71` | `a94ffa64…` (19,541,252) | 100,569,226; $1.0000000001991776$ at 177; $1.007609519559992$ over 9,418,761 | 9.6 |
| `mixed_n73_L8809` | `n73` | `17668509…` (18,622,834) | 100,339,538; $1.000000000044086$ at 79; $1.0046099418362586$ over 8,952,064 | 9.1 |
| `mixed_n74_L88675` | `n74` | `edc1ff84…` (21,560,855) | 90,044,046; $1.000000001545537$ at 17; $1.0053919510575358$ over 11,553,201 | 9.1 |
| `mixed_n75_L892` | `n75` | `75330dd3…` (13,193,154) | 39,920,680; $1.000000006207448$ at 177; $1.0042340709582527$ over 4,206,601 | 2.7 |
| `mixed_n76_L896` | `n76-L896` | `85cc7e1e…` (13,101,923) | 45,154,982; $1.0000000015320276$ at 7; $1.0052760168457555$ over 3,783,025 | 3.1 |
| `mixed_n86_L950` | `n86` | `1f72d911…` (20,392,942) | 94,779,600; $1.0000000001438667$ at 171; $1.0061406086120193$ over 10,562,500 | 9.7 |
| `mixed_n87_L955` | `n87-L955` | `f8f4a19d…` (20,745,923) | 86,412,558; $1.0000000015515935$ at 13; $1.0011071121810646$ over 10,426,441 | 8.9 |
| `mixed_n88_L960` | `n88` | `7e4305f1…` (17,386,081) | 92,907,150; $1.0000000014645312$ at 185; $1.0065197740201668$ over 7,096,896 | 8.3 |
| `mixed_n89_L965` | `n89` | `75e1549d…` (16,339,426) | 109,970,334; $1.0000000007032546$ at 186; $1.003735180782793$ over 6,507,601 | 9.2 |
| `mixed_n90_L9725` | `n90-L9725` | `1744a7d6…` (23,740,402) | 110,810,810; $1.0000000003009648$ at 194; $1.003701651702754$ over 13,271,449 | 12.8 |
| `mixed_n91_L975` | `n91-L975` | `fa6f3a9c…` (18,509,656) | 128,561,314; $1.0000000008354386$ at 119; $1.0042708355544132$ over 8,450,649 | 11.8 |
| `mixed_n92_L977` | `n92-L977` | `6e7bbb35…` (13,136,629) | 37,604,722; $1.0000000055876297$ at 156; $1.002664031677061$ over 4,347,225 | 2.6 |
| `mixed_n93_L986` | `n93` | `10e608e2…` (18,020,286) | 94,366,242; $1.0000000019291797$ at 183; $1.0051573923000485$ over 8,139,609 | 8.4 |
| `mixed_n94_L992` | `n94` | `b866b117…` (19,188,976) | 57,370,560; $1.0000000002005007$ at 191; $1.0052232564352899$ over 8,300,161 | 5.6 |
| `mixed_n95_L996` | `n95` | `1f7b67cd…` (16,003,775) | 53,447,460; $1.0000000006841734$ at 186; $1.005856765307342$ over 5,175,625 | 4.6 |
| `mixed_n96_L997` | `n96-L997` | `486bad8c…` (13,477,300) | 72,598,690; $1.0000000012288544$ at 157; $1.0085332557761764$ over 3,489,424 | 5.4 |

The plan totals 162.4 CPU-hours: `mixed-price` gives 145.1, scaled by the observed ratio
1.119 of the complete replays already merged.
The source’s own oblique seconds total 179.3 CPU-hours, and the two directions run here
took 1.37 and 1.22 times the source’s seconds for them, so budget wall time toward the
source’s figure. The checker’s negative control is on file from $n = 37$, and the bytes
are the same; `mixed-control n76-L896`, whose default direction (index 7, 133,697 nodes)
is the cheapest of the release, would put a control on one of these certificates.
The raised-threshold run of OC-3 observes the exit status and is not a control.

Each count’s verified value moves to the certificate’s side when its own replay passes.
The values increase strictly with $n$ within each run of counts (51–52, 69–71, 73–76,
86–96), so a count whose replay fails keeps the larger of its standing verified value
and the replayed value one count below.
The six entries these certificates supersede in the verified lane (`T-072` at $n = 76$,
`T-075` at 87, 91, 92 and 96, `T-069` at 90) keep their claims and scores.

## Significance

`S3` proposed for `T-082`. The 22 bounds are further sizes from the generator and
checker of `T-069`, `T-071`, `T-072` and `T-075`, at counts from 51 to 96. Each is above
what the record reported before this import, by $1/100$ ($n = 96$) to $1/8$ ($n = 90$),
by more than $0.1$ at $n = 88$, 90, 93, 94 and 95; six replace this source’s own
verified mixed values, and at $n = 76$, 95 and 96 the new values are within $0.04$,
$0.04$ and $0.03$ of the sides 9, 10 and 10 of the best known packings, without settling
any count. Substantive case results; no new technique, and no disputed value resolved.

## Disposition

All 22 certificates are accepted by this review with no defect open.
For `T-082`, `C1` once this document is recorded as `external_review` on its 22 report
entries (`informally-verified`, 2026-10-03) and listed in the entry’s `reviews` with
verdict `accepted`, with the document mapped as a retained review; `V3/C3` for each
count when its replay passes.
The reviewer, for that entry: an AI agent prompted separately from the lane that
retained the packet and drafted `T-082`, blind to any replay and not to retention, model
unstated.
The $n = 88$ and 93 report entries and the packet README should carry OC-1, and
the reply on issue 282 should carry OC-1 once, with OC-2 beside it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
