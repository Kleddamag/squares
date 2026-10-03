# Proof Review: wand125’s Point-Only Cover for `s(61) = 8`

**Date:** 2026-10-02. **Lane:** FF of the W2 phase that is stage 4 of the
[result import runbook](../../../packing/campaign/result-import.md), bead `think-hxrz`.
**Scope:** the second route to $s(61) = 8$, registered as `T-063` by monotonicity from
`T-062`. A mathematical read of the argument from the certificate to the claim, the
trust boundary of the checker that decided it, and an account of what the replay did.
No defect was found.
The `zmx2` source was not re-read in this lane; the
[`s(59)` and `s(77)` review](review-2026-10-02-wand125-s59-s77-mixed-covers.md) read it
at the same source hash, `6b7f0f79…`, in full and is relied on for it.

## 1. What Was Reviewed

| Field | Value |
| --- | --- |
| Source | `wand125/square-packing-bounds` at `f8846cec9661773dbd0cc7cbeee7d01ddb12a2b8`, `point_n61_L8/`, retained in [`packing/resources/web/wand125-point-n61-2026-09-30/`](../../../packing/resources/web/wand125-point-n61-2026-09-30/README.md) |
| Claim | $s(61) = 8$ by a $D_4$-invariant point measure on $[0,8]^2$: 15,193 points, total $8584985072679551/2^{47} < 61$ |
| Cover | `cover.txt`, SHA-256 `bcb66c79…0374`, in the plain format of Daniel’s `certificates/FORMAT.md` |
| Checker | `zmx2.rs` `6b7f0f79…3fed` at `evand/square-packing` `6e1223cf`, which the source’s `verify.sh` builds and checks by that digest |
| Replay | [`receipts/`](../../../packing/resources/web/wand125-point-n61-2026-09-30/receipts/) of the packet |

## 2. The Argument, Re-Derived

1. **Reduction.** Suppose 61 unit squares with disjoint interiors fit in $[0,s']^2$ with
   $s' < 8$. Scaling by $8/s' > 1$ puts 61 squares of side above 1 in $[0,8]^2$; the
   concentric closed unit square of each lies in its parent’s interior, so the 61 cores
   are pairwise disjoint as sets.
   If every closed unit square in $[0,8]^2$ captures mass at least 1, then
   $61 \le \sum_i \mu(Q_i) = \mu(\bigcup Q_i) \le \mu([0,8]^2) < 61$, a contradiction.
   Only nonnegativity and additivity of $\mu$ are used, and a point on $\partial Q$
   counts in full, which is the convention `zmx2` implements.
   This is the argument already reviewed for Daniel’s covers, in
   [the $s(59)$ and $s(77)$ review](review-2026-10-02-wand125-s59-s77-mixed-covers.md#33-the-reduction).
2. **From $s(61) \ge 8$ to equality.** The $8 \times 8$ grid packs 64 squares, so
   $s(61) \le 8$.
3. **The data facts, recomputed here** by `devtools.audit_evand_mixed_covers cover
   --case 61` and an independent count, in integers and `Fraction`: the header is
   $s = 8$, $D = 2000$, $W = 2^{49}$, $m = 15193$; there are exactly $m$ distinct point
   rows and no other tokens; every weight is positive (least $28765412/2^{49}$); every
   point lies in $[81/500, 3919/500]^2$, so none is on the container’s boundary; the
   total is $8584985072679551/2^{47} = 60.9999878\ldots$ with slack
   $1716995457/2^{47} \approx 1.2 \cdot 10^{-5}$ below 61; and the measure is invariant
   under $x \mapsto 8 - x$ and $x \leftrightarrow y$, entry by entry.
4. **The fold.** `zmx2 --d4` checks poses with centres in $[0,4]^2$ only.
   That is sufficient exactly because the cover is $D_4$-invariant (item 3), and `zmx2`
   itself re-checks the invariance
   (`D4: measure invariant under x->s-x and x<->y (exact)`).

Neither the source nor this review relies on the search that found the measure; the
source says as much.

## 3. Trust Boundary

| Step | Decided by | Trusts |
| --- | --- | --- |
| Format, nonnegativity, $D_4$ invariance, total $< 61$ | `check_cover.py` (the source’s, run by `verify.sh`); `audit_evand_mixed_covers cover` (this repository’s, own parser) | Python integers and `Fraction`; each parser |
| Every closed unit square captures $\ge 1$ | `zmx2 cert --d4 --pair-points` (Daniel, third party to wand125) | Its interval arithmetic and branch lemmas, from the source reviewed for $s(59)$ and $s(77)$; the root grid derived from the side |
| That the log covers the region | `audit_evand_mixed_covers zmx2` (own parser, recomputes the 6,400 root ids from the side) | The `ROOT` line format as `zmx2` writes it |
| Reduction to $s(61) = 8$ | The argument in section 2 | Nothing else |

The two cover audits share no code with `zmx2`. The only route to the capture condition
that was run is `zmx2`, so a flaw in it would pass here.
`T-062`’s cover was also decided by Daniel’s `zm_mixed.py`, and his `zeromargin.py` and
`zmcheck` report certifying this cover; those are separately written, were run by him,
and were not run here.

## 4. The Replay and the Controls

`zmx2 cert --d4 --pair-points` on the retained cover reports `VERIFIED-D4`: 6,400 of
6,400 roots, 800,042 boxes, maximum depth 30, 0 uncertified, 0 capped, in 256 s on four
cores. The audit finds every root once with the id `zmx2` assigns it.
The box total and depth equal the source’s own run on another machine and Daniel’s. Two
mutated covers, each with one $D_4$ orbit of points removed (the 8 heaviest points, and
the 4 points at $(29/8, 29/8)$), are each refused, with 460 and 452 uncertified boxes.
`tests/test_replay_controls.py` holds both.

## 5. Findings

| # | Finding | Blocking |
| --- | --- | --- |
| 1 | The point mass on the lines $x \in \mathbb{Z}$ or $y \in \mathbb{Z}$ is 39.2 of 60.99999: contacts at integer coordinates are the tight poses, and `zmx2` decides them in closed form. A cover with no margin in those poses would not be certifiable by interval arithmetic; this one has the $1.2 \cdot 10^{-5}$ slack and the source’s scale-down for it. Nothing to correct. | No |
| 2 | The claim README links `../point_n21_L5/UPSTREAM-LICENSE.txt`, outside the packet’s scope; the commit pins it. | No |
| 3 | The value is already proved by `T-062`/`T-063`. This is a second route and changes no standing result. | No |

## 6. Recommendation

Record the replay as evidence for the reported claim with `performed_by: repository` and
`relationship_to_generator: independent-implementation`, the checker being Daniel’s
`zmx2`, external, as wand125’s own `verify.sh` already uses it.
`T-063` gains a sentence naming this route; no new register entry is needed (the
runbook’s “consequence another entry already registers” row).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
