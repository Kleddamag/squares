# Adversarial Review: The Re-Weighted $s(12)$ Certificate

Reviewed 2026-10-02 by Claude, as review lane RV of the 2 October result work (bead
`think-4srr`), from branch `claude/lane-rv-s12-review` at the lane under review’s commit
`32cd041c`. This lane did not produce the result; it shares no context with lane BB,
which did, and read lane BB’s tools only to check what they claim.
The coordinating session’s instructions keep model names out of repository files, so the
reviewer is named here by lane; the session record names the model.
This is stage 4 review evidence under
[result import](../../../packing/campaign/result-import.md), not a register change.

The write-up under review is
[s(12) Beyond Rescaling](../research/research-2026-10-02-s12-beyond-rescaling.md).
It claims two bounds:

- **Route B:** $s(12) \ge 15680000/3949423 = 3.9702002\ldots$, from Evan Daniel’s 1,736
  points scaled by $3951000/3949423$ and re-weighted by linear programming.
- **Route A:** $s(12) \ge 1568000/395039 = 3.9692284\ldots$, from Daniel’s certificate
  scaled whole, continuing squarepacker’s rescaling in jlevy/squares#309.

**In one line:** both bounds hold.
The argument from a passing run of Daniel’s verifier to a bound at every angle is sound
at $N = 96000$. This lane checked the certificate exactly with its own tool and reran
Daniel’s verifier over all 39,765 bins: `VERIFIED`, least captured weight
$10000045/10^7$. This repository’s parent-core checker, which shares no code with the
sweep or with the generating LP, certified all 39,765 rows (`PASS_COMPLETE`). Both
mutation controls are refused by both checkers.
No defect is blocking; there are five notes.

## 1. What Was Reviewed

| Field | Value |
| --- | --- |
| Certificate | [`certificate.txt.gz`](../../../packing/cases/n12_beyond_rescaling/certificate.txt.gz), SHA-256 of the decompressed bytes `6823e8e872259a6cf3ed258400bf1a0973e1972ab671e8fdcab25938ca605a66` |
| Route A certificate | [`rescaled-certificate.txt.gz`](../../../packing/cases/n12_beyond_rescaling/rescaled-certificate.txt.gz), `93ccef6363b0814ec34c66e94ac8bc83b707e3f7430955c9ccd9ab250e8ae235` |
| Base certificate | Daniel’s `s12_lower_3.9686.txt` (T-049), `75f1cc89…`, in the [retained packet](../../../packing/resources/web/evand-square-packing-2026-09-26/README.md) at `167d842c` |
| Source verifier | `s12/verify/src/main.rs`, SHA-256 `226ef3f1…`, equal to the packet’s pin |
| First-party checker | [`devtools.verify_evand_angle_net_native`](../../../packing/devtools/verify_evand_angle_net_native.py) over `sqpack.fractional.parent_core` and `parent_core_interval` |
| This lane’s tool | [`devtools.audit_s12_reweighted`](../../../packing/devtools/audit_s12_reweighted.py), with [tests](../../../packing/tests/test_audit_s12_reweighted.py) |
| Lane BB’s tools, read | `devtools.s12_angle_net_rescale`, `devtools.s12_reweight`, and lane BB’s change to the native checker (`803d3643`) |

## 2. From a Passing Run to a Bound at Every Angle

This section re-derives what Daniel’s verifier proves at a given $N$, from its source,
his `certificates/FORMAT.md`, and the [T-049 review](review-2026-09-27-evand-s32-s12.md)
§6.1.

**The counting step.** Let $w_i \ge 0$ be weights on points $p_i \in [0, s]^2$ with
$\sum w_i < 12$, such that every closed unit square $Q \subseteq [0, s]^2$ captures
$\sum_{p_i \in Q} w_i \ge 1$. Suppose twelve unit squares with disjoint interiors fit in
a square of side $s' < s$. Scaling by $s/s' > 1$ puts twelve squares of side $s/s'$ in
$[0, s]^2$, and each contains the concentric closed unit square strictly inside it.
Those twelve closed unit squares are pairwise disjoint and each captures weight at least
1, so $12 \le \sum w_i < 12$. Hence $s(12) \ge s$. The step needs exactly three facts
about the file: weights nonnegative, points in the closed container, total below 12.

**The fold to $[0°, 45°]$.** A square is fixed by rotation through $90°$, so angles
$[0°, 90°)$ suffice.
The reflection in the diagonal of the container maps a square at angle $\theta$ to one
at $90° - \theta$. When the weighted multiset is D4-invariant, a square and its image
capture the same weight, so $[0°, 45°]$ suffices.
The verifier checks the invariance exactly (`check_symmetry`) and sweeps the full range
otherwise.

**The net.** Bin $k$ is $[\theta_k, \theta_{k+1}]$ with $\theta_k = 2\arctan(k/N)$, so
$\cos\theta_k = (N^2 - k^2)/(N^2 + k^2)$ and $\sin\theta_k = 2kN/(N^2 + k^2)$ are
rational. The verifier sweeps bins $0, \ldots, K - 1$ with $K$ least such that
$(K + N)^2 \ge 2N^2$, which is $\theta_K \ge 45°$. At $N = 96000$,
$N(\sqrt 2 - 1) = 39764.57\ldots$, so $K = 39765$: the bins reach past $45°$.

**The shrink lemma.** Let $Q$ be a unit square at $\theta = \theta_k + \varphi$ with
$0 \le \varphi \le \delta_k = \theta_{k+1} - \theta_k$. A concentric square of side
$\sigma$ at angle $\theta_k$ lies in $Q$ exactly when
$\sigma(\cos\varphi + \sin\varphi) \le 1$. The function $\cos\varphi + \sin\varphi$
increases on $[0°, 45°]$, and $\delta_k$ is far below $45°$, so the worst case is
$\varphi = \delta_k$ and $\sigma_k = 1/(\cos\delta_k + \sin\delta_k)$ works.
The verifier computes $\cos\delta_k$ and $\sin\delta_k$ exactly from the two rotations
and rounds $\sigma_k$ down to a multiple of $10^{-6}$, which only shrinks the square.
The shrunken square captures a subset of what $Q$ captures, so a lower bound for it is a
lower bound for $Q$.

**The centres.** $Q$ at angle $\theta$ lies in $[0, s]^2$ exactly when its centre lies
in $[w/2, s - w/2]^2$, $w = \cos\theta + \sin\theta = \sqrt 2 \sin(\theta + 45°)$. That
is concave on the bin, so its least value is at an endpoint.
The verifier takes the smaller endpoint value, rounded down to $10^{-6}$, which makes
the box of centres larger.
In each strip of the sweep the range of centres is computed in floating point and padded
outward by at least $10^{-6}$ of the half-side, which can only add centres.
Every centre of an admissible $Q$ in the bin is therefore among those swept.

**The sweep.** For a fixed angle the captured weight of the closed $\sigma_k$-square is
constant on each cell of the arrangement of lines $u_j = q_j \pm h$ in the bin’s frame.
The verifier takes the exact minimum over the cells in `i128`. A bin passes when that
minimum is at least $W$.

**What the margin does and does not do.** The between-angle step spends geometric slack,
the gap $1 - \sigma_k \approx \delta_k \le 2/N = 2.1 \times 10^{-5}$ of the side, and no
weight. A run that ends `VERIFIED` has shown that the shrunken square captures weight at
least 1 in every bin; with the shrink lemma and the centre box, that holds for every
closed unit square at every angle, not just at net angles.
The least captured weight, $10000045/10^7$, says how close the tightest square came; any
value of at least 1 would prove the bound.
A reader should not read the $4.5 \times 10^{-6}$ weight margin as the safety that
covers angles between net points.
That safety is $\sigma_k < 1$, and it is built into every bin.

**Overflow.** At $N = 96000$ and $D = 3949423$ the sweep’s numerators reach about
$10^{29}$ before its products.
The shipped release profile does not check `i128` overflow, so a wrap could in principle
print a false pass.
Lane BB built the verifier with `overflow-checks` on, and so did this
lane, independently, with `CARGO_PROFILE_RELEASE_OVERFLOW_CHECKS=true` and `--locked`. A
panic in a worker thread reaches `main` through `join().unwrap()` and aborts before any
verdict is printed. The two builds have the same SHA-256, `60279b2c…`.

**Verdict on the argument:** passing at $N = 96000$ with least weight $10000045/10^7$
proves that every closed unit square in $[0, 15680000/3949423]^2$, at every angle,
captures weight at least 1. With the exact checks of §3 that proves Route B’s bound.

## 3. The Certificate, Checked Exactly

[`devtools.audit_s12_reweighted`](../../../packing/devtools/audit_s12_reweighted.py)
imports nothing from lane BB’s tools.
It parses the files itself, in integers and `Fraction`, and wrote
[`review-audit.json`](../../../packing/cases/n12_beyond_rescaling/receipts/review-audit.json).
All 18 checks pass.

| Check | Result |
| --- | --- |
| Digest of the decompressed Route B file | `6823e8e8…`, equal to `claim.json` |
| Header and format | $s = 15680000/3949423$, $D = 3949423$, $W = 10^7$, $m = 1736$; $s_{den}$ divides $s_{num} D$; the bytes are the canonical rendering of what they parse to |
| Weights | nonnegative integers over $W$; 120 are zero |
| Points | all in the closed container, $15680000$ units on a side |
| Total | $14970347/1250000 = 11.9762776$, gap $29653/1250000$ below 12 |
| Container | $15680000/3949423$, equal to Daniel’s $15680/3951$ times $3951000/3949423$ |
| Geometry | each point is Daniel’s, in file order, with both coordinates times 1000 |
| Symmetry | the weighted multiset is D4-invariant, 223 orbits |
| Route A | digest `93ccef63…`; Daniel’s file times 1000 over $3950390$, weights unchanged, total $29934509/2500000$; D4-invariant and in its container |
| Controls | both rebuilt here from their descriptions match the digests in `controls.json` |

All 1,736 weights differ from Daniel’s. The geometry is his and the weights are new,
which is the attribution the write-up gives.

## 4. Replays

| Check | Code | Scope | Outcome | Receipt |
| --- | --- | --- | --- | --- |
| Arrangement sweep, Daniel’s `verify`, overflow-checked build `60279b2c` | external (the producer’s) | all 39,765 bins, $N = 96000$, two threads | `VERIFIED`, least $10000045/10^7$ at bin 0; 1,642 s wall, 2,913 CPU-s | [log](../../../packing/cases/n12_beyond_rescaling/receipts/review-source-verifier-N96000.log) |
| Parent-core interval branch and bound | first-party | all 39,765 rows, $N = 96000$, two workers | `PASS_COMPLETE`: every row certified at the one-unit threshold, 375,934,771 boxes, no stall, no exhausted budget, no refutation; 11,358 row-CPU-s | [receipt](../../../packing/cases/n12_beyond_rescaling/receipts/review-native-complete.json), [row journal](../../../packing/cases/n12_beyond_rescaling/receipts/review-native-complete.rows.jsonl.gz) |
| Control 1, lowered orbit, source verifier at bin 0 | external | bin 0 | least $9999845/10^7$, refused | [log](../../../packing/cases/n12_beyond_rescaling/receipts/review-source-verifier-ctl1.log) |
| Control 2, one step larger, source verifier at bin 7808 | external | bin 7808 | least $9764124/10^7$, refused | [log](../../../packing/cases/n12_beyond_rescaling/receipts/review-source-verifier-ctl2.log) |
| Control 1, native checker | first-party | row 0 | refuted with an exact witness | [receipt](../../../packing/cases/n12_beyond_rescaling/receipts/review-native-ctl1.json) |
| Control 2, native checker | first-party | row 7808 | refuted with an exact witness, upper bound $9793495/10^7$ | [receipt](../../../packing/cases/n12_beyond_rescaling/receipts/review-native-ctl2.json) |

The source replay ran under
[`devtools.replay_receipt`](../../../packing/devtools/replay_receipt.py) from a scratch
copy of the retained crate, built here and not by lane BB’s `build` command.
A single refused bin refuses the whole certificate, because the verdict is the minimum
over all bins. The verifier exits 0 on `NOT VERIFIED`, so its verdict line, not its exit
code, is what decides; each control log shows that line.

**Why the native run matters more here than for T-049.** The re-weighting LP took its
rows from the source verifier’s own `TIGHT_DUMP` cells and was checked by the same
verifier. An optimiser fitted against a checker will exploit any cell that checker
mishandles, and lane BB’s first complete sweep refused six bins that its sampled rows
had missed. Nothing suggests the verifier mishandles a cell; it was read on 27 September
and again here. But the producer’s verifier is not independent of this generator in the
way it is independent of Daniel’s. The parent-core checker decides coverage over centre
boxes with directed rounding.
It shares no code with the sweep or with the LP, and its premise check proves each row’s
core strictly inside every parent of the row in exact rationals, which is the shrink
lemma of §2 proved again.
What the two checkers share is the certificate, the row decomposition with its
$\sigma_k$, and the counting step.

## 5. Findings

Severity is blocking, non-blocking, or note.
**None is blocking.**

### F1. The write-up’s first-party check was a sample (non-blocking, resolved here)

Lane BB’s native run decided 1,034 of 39,765 rows, `PASS_PARTIAL`. Because of the
fitting described in §4, a sample was weaker evidence than it would be for a certificate
produced without reference to the source verifier.
This review’s complete run closes the gap: all 39,765 rows certified, none refuted.
The run was stopped by a container restart after 9,407 rows and resumed from its row
journal. The first part ran on clean commit `32cd041c`, the rest on clean commit
`b1a78984`, and the checker’s code is identical at both; the receipt counts the 9,407
resumed rows and requires every row certified before it says `PASS_COMPLETE`.

### F2. Two statements in the write-up are estimates and should say so (note)

“Only a net finer than about 15000 leaves that much of the shrink unspent” is an
estimate from $1 - \sigma_k \approx 2/N$, and the measured facts are refusal at $12000$
and acceptance at $24000$. “An effective $3.9709$” for Daniel’s column generation is the
same estimate applied to his reported stopping point.
Neither carries any claim.

### F3. The explanation of the unchanged least weight was not checked (note)

The write-up explains why Route A’s least weight equals Daniel’s: the binding square in
bin 0 captures the same 58 points at each scale.
That is consistent with the receipts, but this review did not read the bin-0 dump.
It is an explanation, not a claim.

### F4. The verifier’s header comment says “interior” (note)

`main.rs` line 5 states the claim with atoms “in the interior of $Q$”, while the code,
`FORMAT.md` and the verdict line use the closed square.
Counting fewer points would only make the check stricter, so either reading is sound.
The comment is the source’s, not lane BB’s, and belongs in a note to Daniel, not in this
record.

### F5. The thin reader into the native checker, read (note)

The T-049 evidence entry says the reader that maps Daniel’s integer file onto
parent-core rows had no review of its own.
This review read it, with lane BB’s change to it.
`read_source` admits only digit tokens, so weights and coordinates are nonnegative.
`parse_certificate` checks the header, the point count, the container grid and the upper
coordinate bound, and drops zero-weight points, which is sound.
`sigma` is the source’s `bin_geometry` formula.
`net_rows` stops at the first right end at or above $\tan(\pi/8)$, which gives the
source’s $K$. Lane BB’s change only threads the net and a file path through, and the
receipt records the file’s own digest.
No defect.

## 6. Verdicts

| Claim | Verdict |
| --- | --- |
| Route B, $s(12) \ge 15680000/3949423$ | **Accepted.** Exact audit, a complete source-verifier replay here, a complete first-party parent-core run, both controls refused by both checkers |
| Route A, $s(12) \ge 1568000/395039$ | **Accepted**, as implied by Route B, since $1568000/395039 < 15680000/3949423$. This lane checked the file exactly (§3) but did not replay its sweep; lane BB’s receipt is the only run on it |
| Route B exceeds #309’s $31360/7901$ by about $0.0010824$, and Daniel’s by about $0.0015847$ | Confirmed exactly |
| Both controls are refused | Confirmed, by both checkers, on controls rebuilt here |
| The total is $14970347/1250000 < 12$ and the weights are nonnegative exact rationals | Confirmed |
| “This point set may carry the bound further” | An open question, correctly worded as one |

The register claim is the non-strict $s(12) \ge 15680000/3949423$, the closed-square
form of the counting step.
The native theorem gives the strict $s(12) > 15680000/3949423$, which implies it.

## 7. Attribution

The result is Levy’s, by this project’s re-weighting.
It builds on Evan Daniel’s certificate `s12_lower_3.9686.txt` (T-049), whose 1,736
points it uses unchanged up to scale, and on squarepacker’s rescaling in
jlevy/squares#309, which Route A continues.
The re-weighting, an LP over D4 orbits with rows from the source verifier’s near-tight
cells, is this project’s own step.
Daniel’s verifier, built unmodified from the retained source with overflow checks on, is
the external check; the parent-core checker and the audit tool are first-party.

## 8. Significance, Draft

**`S3`, a substantive case result.** The nearest entry is T-049, scored `S3` for raising
the verified bound at $n = 12$ by $0.0086$. This raises it again by $0.0016$, to within
$0.0298$ of 4. It is the best verified lower bound at $n = 12$ that this repository
knows of. Its geometry is Daniel’s, and the method, a weighted cover re-optimised at a
finer net, is his and Burns’s and Massaccesi’s, so it is not a reusable technique at
`S4`. Daniel’s fractional packing at $3.99$ caps pure point covers well short of 4, so
it does not move the central question at $n = 12$, which would be `S5`. Novelty:
`apparently-novel`, against T-049, #309 and the source packet; no wider literature
search was run for this review.

## 9. For the Records Lane

A result entry, `kind: lower-bound`, $s(12) \ge 15680000/3949423$, attributed as in §7,
draft `S3` with `by` naming this review, and these evidence entries:

| Entry | `performed_by` | `relationship_to_generator` | `origin` | Verifier |
| --- | --- | --- | --- | --- |
| Lane BB’s complete sweep, `route-b-source-verifier.json` | `repository` | `generator` | none, the producing run | Daniel’s `verify`, external |
| This review’s complete sweep, `review-source-verifier-N96000.log` | `repository` | `same-implementation` | `replayed-here` | Daniel’s `verify`, external |
| This review’s parent-core run, `review-native-complete.json` | `repository` | `independent-implementation` | `audited-here` | `devtools.verify_evand_angle_net_native`, first-party |
| This review’s exact audit, `review-audit.json` | `repository` | `independent-implementation` | `audited-here` | `devtools.audit_s12_reweighted`, first-party, well-formedness only |

The source replay is `exact-algebraic` and the native run `interval-certified`, which
gives `C3` with two methods beside the rung.
The controls are `receipts/controls.json` and the four `review-*-ctl*` receipts.
This document goes in the result’s `reviews` as `kind: adversarial`,
`reviewer_kind: ai`, `relation: project`, verdict `accepted`. Route A needs no separate
entry; if one is wanted, it is lane BB’s receipt alone.

## References

- [s(12) Beyond Rescaling](../research/research-2026-10-02-s12-beyond-rescaling.md), the
  write-up under review
- [The case directory](../../../packing/cases/n12_beyond_rescaling/__init__.py), with
  the certificates, claim and receipts
- [T-049 review](review-2026-09-27-evand-s32-s12.md), §6.1
- [Daniel’s packet](../../../packing/resources/web/evand-square-packing-2026-09-26/README.md),
  `s12/certificates/FORMAT.md` and `s12/verify/src/main.rs`
- [Epistemics](../../../epistemics.md), for the rungs and the review record

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
