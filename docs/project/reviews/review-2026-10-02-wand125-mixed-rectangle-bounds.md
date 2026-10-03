# wand125 Mixed Rectangle-Measure Certificates: Review of T-069 and of n = 84, 85

The five certificates `T-069` registers, at $n = 37$, 65, 66, 90 and 92, and the two of
2 October at $n = 84$ and 85, are the certificate kind reviewed on 28 September for
$s(50) \ge 37/5$: a rectangle density of mass $n - 1/100000$ checked at coverage one by
wand125’s research copy of Tokoharu’s `verify.cpp`, with angle zero decided by integer
tables.
The checker is the one reviewed then, byte for byte: every file of `code/` in all
seven directories, at both `1a25a5ed` and `52af997`, hashes to the retained
`mixed_n50_L740` copy.
Every exact premise that can be read from the retained files holds for all seven, each
`candidate_digest` is reproduced here from the candidate, and the per-angle records are
complete and consistent.
No blocking defect was found.
Five non-blocking findings are recorded: a seventh-decimal typo in the Green comparison
that the record copied at $n = 65$, an `improvement_lower` at $n = 84$ and 85 that is
not a lower bound, a stale comparison at $n = 90$, two README inconsistencies, and a
two-machine verification at $n = 65$ that the replay here makes moot.
The seven values stand as reported until the complete replay of each bundle passes here.
`S3` is confirmed for `T-069` and proposed for the $n = 84$, 85 entry to be registered.

This is the review lane of stage 4 of the result import process for imports F
(`think-ye2x`) and G, written by Claude (AI review; model unstated; extra-high thinking
effort), separately prompted as lane R3 with no shared context with the replay lane, on
2026-10-02. It registers nothing and moves no bound.

## Scope and Evidence

The claims are `T-069`, five lower bounds reported at
[`1a25a5ed`](https://github.com/wand125/square-packing-bounds/tree/1a25a5ed745fdd905a52f48fcc48150a0669032d)
on evidence entries `E-n037-wand125-mixed-644-report`, `E-n065-…-835`, `E-n066-…-842`,
`E-n090-…-960` and `E-n092-…-969`, and the $n = 84$, 85 entry to be registered from
[`52af997`](https://github.com/wand125/square-packing-bounds/tree/52af997dc91c579658f0828bc8304e306ad9d95b),
the commit after `1a25a5ed`, announced in a
[comment of 2026-10-02 on issue 282](https://github.com/jlevy/squares/issues/282#issuecomment-5943469227).
The packet for F is
[`wand125-point-and-mixed-2026-10-01`](../../../packing/resources/web/wand125-point-and-mixed-2026-10-01/README.md);
G’s packet is being written by another lane, so its files were read with `git cat-file`
from a read-only clone at `52af997`.

| $n$ | Directory | Claim | Rectangles | Mass | First commit (UTC) |
| ---: | --- | --- | ---: | --- | --- |
| 37 | `mixed_n37_L644` | $s(37) \ge 161/25 = 6.44$ | 350 | $3699999/100000$ | 2026-09-30, `baff9d23` |
| 65 | `mixed_n65_L835` | $s(65) \ge 167/20 = 8.35$ | 787 | $6499999/100000$ | 2026-09-29, `c21d1bd5` |
| 66 | `mixed_n66_L842` | $s(66) \ge 421/50 = 8.42$ | 631 | $6599999/100000$ | 2026-10-01, `1807160d` |
| 90 | `mixed_n90_L960` | $s(90) \ge 48/5 = 9.6$ | 762 | $8999999/100000$ | 2026-10-01, `8038d64d` |
| 92 | `mixed_n92_L969` | $s(92) \ge 969/100 = 9.69$ | 832 | $9199999/100000$ | 2026-10-01, `8038d64d` |
| 84 | `mixed_n84_L940` | $s(84) \ge 47/5 = 9.4$ | 661 | $8399999/100000$ | 2026-10-02, `52af997` |
| 85 | `mixed_n85_L942` | $s(85) \ge 471/50 = 9.42$ | 587 | $8499999/100000$ | 2026-10-02, `52af997` |

Read in full: the seven `README.md`, `candidate.json`, `certificate.json`,
`completion-audit.json` and `manifest.json`; the retained `mixed_n50_L740/code/`
(`mixed_density_check.py`, `mixed_net_audit.py`, `verify_axis_certificate.py`, and the
C++ against Tokoharu’s `verify.cpp` by `diff -u`); the F packet README and the root
README’s diff from `1a25a5ed` to `52af997`; `T-048` and `T-069` with their evidence
entries; the case records `n-037`, `n-065`, `n-066`, `n-084`, `n-085`, `n-090` and
`n-092`; issue 282 and its comment; the
[n = 50 mixed-verifier review](review-2026-09-28-wand125-n50-mixed-verifier.md) and the
[density mathematics review](review-2026-09-22-tokoharu-density-mathematics.md).

Run here, on one core of x86-64 Linux with the project CPython 3.14.7, as
`scratchpad/r3/checks.py` (exact rationals and SHA-256; no source program executed):

- for each of the seven candidates: $n$, $L$, $B$, the empty point list, every rectangle
  inside the container with positive area and nonnegative mass, the mass sum equal to
  `total_mass` and to $n - 1/100000$, `scaling_factor` $= 1$, and the `candidate_digest`
  recomputed by the shipped recipe (SHA-256 of the sorted-key compact JSON of `n`, `L`,
  `B`, `rectangles`, `points`, `total_mass`) equal to the audit’s, the manifest’s, the
  certificate’s, the candidate’s own `scaling_source_digest` and every one of the 201
  per-angle records;
- for each `certificate.json`: status, 201 results indexed $0..200$, the axis record at
  `gamma = 1`, every oblique record `ANGLE_RESULT_REPLAYED` with `lower` $\ge 1$ and its
  index, the least bound, the largest node count against the manifest’s limit, and the
  SHA-256 of the file against the audit’s `certificate_sha256`;
- the net identities, all 201 per-node centre domains, and the Green and Nagamochi
  comparisons to 60 decimal digits.

## The Argument From Certificate to Bound

The density is the $D_4$ expansion of the listed rectangles with density
$m_j / (8|R_j|)$ per image, so $g \ge 0$, is invariant under the container’s symmetries,
and has exact mass $M = \sum_j m_j = n - 1/100000 < n$. No point mass is present
(`points` is empty and `point_mass` is `0` in every certificate), so the atom term of
the checker is dead code here, as at $n = 50$.

At net index $r \ge 1$ the checker proves that every closed $B$-square at
$\theta_r = 2\arctan t_r$, $t_r = 83r/40000$, whose centre lies in
$[L/2,\ L - \rho(a_r)]^2$ captures mass at least $\Gamma = 1$, where $a_r = t_r - D/2$
and $\rho(a) = (1 + 2a - a^2)/(2(1 + a^2))$ is the half-width, in the container’s frame,
of a unit square at half-angle $a$. That domain is the union, over the orientations the
net assigns to node $r$ (half-angles in $[a_r, t_r + D/2]$), of the admissible centres
of a unit square, folded by a quarter turn; it omits a strip of width
$\rho(a_r) - B(c_r + s_r)/2 \ge 1.2 \times 10^{-4}$ of Tokoharu’s domain whose centres
belong to no unit square the bin assigns to $r$. Recomputed here for all 201 indices: no
node is skipped (so the list-position indexing of MV-2 is safe),
$\rho(a_r) \ge B(c_r + s_r)/2$ at every node, and the domain half-side
$E_r = L/2 - \rho(a_r)$ is at least $2.5129$ at the smallest side here, $L = 161/25$.

Containment is as for the standard certificates: $B(1 + D) = 399908091/400000000 < 1$,
$t_{200}^2 + 2t_{200} - 1 = 89/40000 > 0$, and the last bin reaches below $\pi/4$
($a_{200}^2 + 2a_{200} - 1 = -4544311/6400000000 < 0$), all recomputed here and all
equal to the `net` block every manifest and certificate carries.
So a unit square at any orientation contains, strictly inside, a closed $B$-core at the
net angle its orientation is assigned to, with its centre in that node’s domain; the
core captures at least $1$; cores inside the $n$ squares of a packing are disjoint; and
$n \le M < n$ is impossible.
The bound is $s(n) \ge L$.

**Angle zero** is decided by `verify_axis_certificate.py`, not the C++: it rebuilds the
event grid on $[L/2, L - 1/2]$ from all expanded edges and requires the stored axes to
equal it, scales coordinates to integers by the table’s own `coordinate_denominator`,
requires each table entry $f_{ij}$ to satisfy $f_{ij}(x_1 - x_0) \le 2^{16} \ell_{ij}$
with $\ell_{ij}$ the exact overlap, forms the corner coverages as `int64` matrix
products under an overflow guard, takes each cell’s corner minimum, and requires every
cell below $\lceil \Gamma \cdot 2^{56} \rceil$ to be patched by an exact rational
recomputation. The seven integer minima are $1.0031$ ($n = 66$) to $1.0246$ ($n = 92$),
so the axis margin is between $0.31$ and $2.46$ per cent and no patch can be needed; the
cell counts are $5{,}044{,}516$ ($n = 37$) to $26{,}532{,}801$ ($n = 65$).

**Scaling** is not used: every `scaling_factor` is $1$ and each `scaling_source_digest`
is the candidate’s own digest.
The $n = 65$ route’s contraction of a search state by $167/168$, and the stretch of the
$n = 89$ and $n = 91$ rectangle certificates into the $n = 90$ and $92$ candidates, are
how the candidates were found; only the final candidate at the claimed $L$ enters the
checker, and its 201 records carry its digest.

## Hypotheses the Checker Assumes

1. The oblique input files enclose the exact candidate: `export` rounds each rational
   outward and asserts the enclosure; the replay regenerates all 200 files and requires
   byte equality with the shipped ones.
   Not checked here (the bundles are pinned by digest and not retained); the replay
   must.
2. The mass, nonnegativity, geometry and digest of the candidate: checked here exactly,
   and by `expand` on every path that reads the candidate.
3. $\Gamma \ge 1$ read from the input (`export` refuses less), and the leaf test
   `lower >= gamma.h` with `gamma.h` exactly $1$: the theorem needs only $\Gamma \ge 1$
   with $M < n$, and the $10001/10000$ margin of Tokoharu’s format bought insurance
   against an undetected over-estimate, which the 28 September review’s re-read of the
   kernel at $\Gamma = 1$ and its 72-box exact control address.
4. $E$, $c_r$ and $s_r$ per node are exact rationals enclosed in Python and read from
   the input, not formed in C++: an enclosure either way.
5. The per-node domain lemma ($\rho$ increasing on $[0, \pi/4]$, so the bin’s union is
   $[\rho(a_r), L - \rho(a_r)]^2$) and the quarter-turn fold: prose; their rational
   instances are computed here for all 201 nodes.
6. The interval kernel: `area_lower`, `slice`, the derivative enclosure and the leaf
   inequality, under binary64 round-to-nearest without FMA or fast-math, the compile
   line fixed in `compile_verifier`; `stod` and `nextafter` trusted.
   Prose, reviewed on 22 and 28 September; unchanged.
7. The driver’s acceptance checks are `assert` statements and the C++ exits zero on an
   unresolved angle (MV-1): the replay must run without `-O` or `PYTHONOPTIMIZE`, and
   read status and frontier, as `verify_mixed_full_proof.py` does.
8. Every angle finishes with an empty frontier under the node limit ($3{,}000{,}000$ in
   every manifest; the largest recorded angle is $724{,}677$ nodes, at $n = 65$) and the
   $2^{-40}$ depth floor.
   What the replay decides.
9. The axis tables’ `int64` arithmetic cannot overflow: `verify_axis_certificate.py`
   asserts $(\sum w_j) 2^{32} < 2^{63}$ and $f \le 2^{16}$, and the coordinate scaling
   is done in Python integers.
   This was read again here because the candidates’ coordinate denominators are larger
   than at $n = 50$: up to $1.68 \times 10^{19}$ at $n = 65$ and $7.6 \times 10^{18}$ at
   $n = 92$, against $10^{16}$. The denominator $D$ is read from the table’s metadata
   and each scaled coordinate is asserted integral, and $D$ does not enter the `int64`
   products, so the guard is independent of its size.
   The replay should report each certificate’s `coordinate_denominator`.
10. The theorem is about closed unit squares with disjoint interiors in the closed
    container, and rectangle boundaries carry no mass.
    Prose.

## The Checker’s Trust Boundary and What It Shares

`mixed_rotated_verify.cpp` (SHA-256 `89b674a6…`) is Tokoharu’s `verify.cpp`
(`a75140df…`) with the interval type, `readI`, `area_lower`, `slice` and the rectangle
struct unchanged, and every change in `bound`’s interface and `main`: $\Gamma$, $E$,
$c$, $s$ from the input; the atom term; the node limit from the command line and the
$2^{-40}$ floor; `query` and `region` modes; the split heuristic; JSON status with exit
zero.
The `diff -u` run here reproduces the 28 September table line for line, and the ten
Python files beside it are byte-identical to the retained copies, so the trust boundary
is the one that review drew: coverage at 200 oblique directions is decided by this C++,
angle zero by the integer tables, and everything else by exact arithmetic in `expand`,
`net_certificate`, `centre_domains` and this repository’s audit.
The two families, `T-068` and this one, share the kernel; a defect there would reach
both.

## What Changed Since 28 September

Nothing in the code: all 50 files of the five F `code/` directories and the 20 of G, and
the five `requirements.txt`, hash to the `mixed_n50_L740` copies.
The certificate and manifest fields are the same set with the same values of the net
block, the node limit and the two workers.
What is new is in the audits, the READMEs and the sizes:

- `completion-audit.json` compares with a rational `compared_with` and a `compared_note`
  where the previous value is rational ($n = 66$, 90, 92, 84, 85), and with a 90-digit
  `green_upper` where it is Green’s irrational ($n = 37$, 65); `bundle` is now a
  relative name; the `route` notes record a contraction ($n = 65$), a stretch ($n = 90$,
  92), a verification assembled across two machines after a six-hour runner timeout
  ($n = 65$, 181 angles on one and the rest on another, each accepted only as
  `ANGLE_VERIFIED` with an empty frontier and matching digest), and the agents that ran
  the pipeline.
- The READMEs of $n = 66$, 90, 92, 84 and 85 state the axis integer minimum; those of
  $n = 37$ and 65 do not.
- Sides to $969/100$ and 832 rectangles, against $37/5$ and 553; densities from
  $7.2 \times 10^{-4}$ to $2.6 \times 10^{4}$ per unit area ($n = 84$), smallest sides
  $1.0 \times 10^{-3}$ throughout; oblique node totals of $50.2$ million ($n = 37$) to
  $98.5$ million ($n = 84$), against $80.7$ million at $n = 50$.
- The least oblique bounds: $1.000000005449$ ($n = 37$, index 99), $1.00000000036832$
  ($n = 65$, 104), $1.00000000092563$ ($n = 66$, 10), $1.000000000041986$ ($n = 90$,
  122), $1.0000000034450$ ($n = 92$, 172), $1.00000000089758$ ($n = 84$, 175) and
  $1.0000000017271$ ($n = 85$, 44), each a branch-and-bound artefact just above
  $\Gamma$; the $n = 90$ figure is an order of magnitude nearer $1$ than the
  $4.6 \times 10^{-10}$ at $n = 50$, which is why MV-4’s point stands: the shipped
  replay proves determinism, and the direction of the bound rests on the kernel review
  and its control.

## Where the Requests and the Record Differ

- **Comparisons at $n = 37$ and 90** (triage item 8). Issue 282 compares $161/25$ with
  Green’s reported $6.3506\ldots$ and $48/5$ with Nagamochi’s $1 + \sqrt{73} = 9.5440$;
  the record’s reported lane held wand125’s own $257/40 = 6.425$ (`T-046`) and $191/20$
  (`T-046`, now $3831/400$ by `T-068`), so the improvements over the record are $3/200$
  and $9/400$. The audit at $n = 90$ compares with $3827/400 = 9.5675$, the rung
  standing when the measure was made (`rect_n90_L95675` is in the tree); the pin’s
  standing rectangle is $3831/400$ (MX-3).
- **Format, second replay, route.** The packet README lists three more: the issue calls
  the format Tokoharu’s while each README says the certificate is not in his format
  because its least bound is below $1.0001$; the issue places the second replay on a
  separate machine, which the READMEs do not say; and the issue says $n = 65$ was
  generated directly at the target side, while its README and audit say it was
  contracted from a state at $L = 8.40$. None enters the checker.
- **The comment on $n = 84$, 85** agrees with the certificates: 661 and 587 rectangles,
  masses $n - 1/100000$, least bounds $1.0000000008\ldots$ and $1.0000000017\ldots$, and
  the root README’s “by $0.133$ and $0.153$” over Green are right to three decimals.
- **`mixed_n87_L940`.** The issue says it exists and is below `rect_n87_L941`; both are
  in the tree, with `mixed_n87_L939`, and none is claimed.

## Findings

No blocking finding.

### MX-1 — Low, in the record: Green’s value at $n = 65$ is $8.2899656$, not $8.2899658$

$2\sqrt2 + 71/13 = 8.28996558628\ldots$ The $n = 65$ README writes “$8.2899658\ldots$”,
and `T-069`’s claim and `E-n065-wand125-mixed-835-report` copied it.
The source’s own `green_upper` is exact to 59 digits and its `improvement_lower`
$0.0600344137\ldots$ is right, so only the decimal in prose is wrong.
Correct the two record texts to $8.2899656$ and tell the author.

### MX-2 — Low, in the source: `improvement_lower` at $n = 84$ and 85 is not a lower bound

Both audits compare with `compared_with` $= 92667/10000 = 9.2667$, which is below
Green’s $2\sqrt2 + (247 + 12\sqrt2)/41 = 9.26673353324\ldots$ (the value the case
records hold as `E-green-ds7-theorem9-reported-lower`), so the recorded $1333/10000$ and
$1533/10000$ overstate the improvements by $3.4 \times 10^{-5}$; the true values are
$0.13326646\ldots$ and $0.15326646\ldots$ The bounds $47/5$ and $471/50$ are unaffected.
The $n = 84$, 85 entry should state “by more than $0.1332$ and $0.1532$”, and the author
should be told; the $n = 37$ and 65 audits use a proper upper enclosure.

### MX-3 — Note: the $n = 90$ comparison names a superseded rung

`compared_with` $3827/400$ and the README’s “our earlier $9.5675$” are the rung that
stood when the measure was made; at the pin the standing rectangle certificate is
$3831/400 = 9.5775$ (`T-068`), which $48/5$ exceeds by $9/400$. At $n = 92$ the audit’s
$24151/2500 = 9.6604 \ge 1 + \sqrt{75}$ is a proper enclosure and its $37/1250$ a true
lower bound on the improvement; the README’s “$9.645$” and the audit’s “$9.6475$” for
the earlier value differ, as the packet README notes.

### MX-4 — Note: two README inconsistencies

The $n = 66$, 90, 92, 84 and 85 READMEs say the bundle holds 622 files and that 621
hashes were checked (the hash list presumably being the 622nd); the $n = 37$ and 65
READMEs say 621 files.
The same five READMEs name `mixed_n87_L939` as the certificate that uses the same
checker, a rung that `mixed_n87_L940` and `rect_n87_L941` both supersede.
The replay should record each bundle’s file count and the length of `files-sha256.json`.

### MX-5 — Note: the $n = 65$ verification was assembled on two machines

The route says 181 angles verified on one machine and the rest on another after a
timeout, each accepted only as a complete record.
The full replay from the tarball, which the source says it ran, is one run; the replay
here is also one run and decides the matter.

## Claims by Evidential Status

- **Proved here in exact arithmetic:** the net, reach and bin identities; the 201 centre
  domains with $\rho(a_r) \ge B(c_r + s_r)/2$ and $E_r \ge 2.5129$; every mass equal to
  $n - 1/100000$ from the rectangle masses; every candidate digest reproduced; every
  certificate file’s digest equal to its audit’s; the Green and Nagamochi comparisons.
- **Reviewed by reading:** that the seven `code/` directories are the reviewed checker
  byte for byte; that no new premise depends on $L$, the rectangle count or the
  coordinate denominators (hypothesis 9).
- **Asserted by the source, not verified here:** the 200 oblique coverage statements and
  the axis tables of each certificate, the byte identity of the regenerated inputs, and
  the contents of the seven bundles, which are pinned by digest and not retained.

## What the Replay Must Show

For `V3/C3` on `T-069`, and on the $n = 84$, 85 entry once its packet is on `main`:

- The seven tarballs fetched at their pinned commits, each hashing to the digest the
  packet’s `sources.json` (F) or the `completion-audit.json` (G) records; a pristine and
  a working unpacking; every entry of `files-sha256.json` matched; the bundle’s `code/`
  and `candidate.json` byte-identical to the retained copies.
- `env -u PYTHONOPTIMIZE OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3
  code/verify_mixed_full_proof.py proof --workers 3` with a C++17 `c++` whose version is
  recorded, the retained checker read before it is run; it must end
  `ALL_ANGLES_VERIFIED_AND_REPLAYED`.
- The axis `replayed.json` with the cell count and integer minimum below, and every
  per-angle `replayed.json` with the node count and `lower` of the retained
  `certificate.json`; then the generalised `n50-compare` of
  `audit_wand125_point_and_mixed` (plan item 7: the tool takes the certificate as a
  parameter) printing `FULL_REPLAY_MATCHES_SHIPPED`, and its `exact` audit extended to
  these certificates: digest, mass, net, centre domains and the enclosure binding of all
  200 inputs.

| $n$ | Axis cells | Axis integer minimum | Oblique nodes | Largest angle (index) |
| ---: | ---: | --- | ---: | ---: |
| 37 | 5,044,516 | 1.010578471379292 | 50,197,404 | 352,649 (200) |
| 65 | 26,532,801 | 1.005594099748123 | 93,302,968 | 724,677 (200) |
| 66 | 17,530,969 | 1.0031018132438783 | 90,325,926 | 699,617 (200) |
| 90 | 11,812,969 | 1.0187419121321 | 59,985,962 | 400,323 (200) |
| 92 | 12,489,156 | 1.0245720286547386 | 60,700,598 | 395,415 (200) |
| 84 | 18,198,756 | 1.0083383947166207 | 98,464,504 | 724,319 (200) |
| 85 | 15,784,729 | 1.013816765469528 | 97,066,046 | 665,943 (199) |

- Two mutated certificates refused by the retained path, held by a test, and the
  receipts committed when each run ends.
- The cost beside the source’s figure.
  The certificates carry no upstream seconds, so the estimate is by nodes: the $n = 50$
  replay was costed at $10.5$ CPU-hours for $80.7$ million oblique nodes here, about
  $0.13$ CPU-hours per million, which gives about $46$ CPU-hours for the five of F and
  $25$ for G, before the extra per-node cost of 787 to 832 rectangles against 553. The
  plan’s $45$ to $90$ is the right range.
  The $n = 65$ bundle is the largest at $32$ MB.

The replay is a confirming machine replay of the source’s own checker: the axis tables
are a second implementation for one direction and not a second method, so `composition`
should say coverage is decided by the source’s C++ alone, as `T-048`’s notes do.

## Significance

`S3` confirmed for `T-069` and proposed for the $n = 84$, 85 entry.
The nearest entry is `T-048` at `S3`, one count of the same kind past Green’s reported
value; these add five and two counts from the same generator and checker, two past
Green’s values ($n = 65$, and 84 and 85 by $0.133$ and $0.153$, the widest margins over
Green on record) and two past Nagamochi’s closed forms ($n = 90$, 92). Substantive case
results; the technique and the threshold-one checker are `T-048`’s, and no disputed
value is resolved.

## Disposition

`T-069` is accepted by this review with no defect open: `C1` once this document is
recorded as `external_review` on its five report entries (`informally-verified`,
2026-10-02) and listed in the entry’s `reviews`, with the document mapped as a retained
review; `V3/C3` when the replays above pass.
The $n = 84$, 85 entry can cite this review the same way when it is registered, with
MX-2’s correction in its evidence text.
The reply on issue 282 should carry MX-1 and MX-2 to the author.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
