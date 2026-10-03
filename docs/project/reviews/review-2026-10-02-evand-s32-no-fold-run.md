# Proof Review: Evan Daniel’s `s(32)` Cover Certified Without the D4 Fold, and What the Checkers Share

Reviewed 2026-10-02 from the retained packets and a read-only clone of the source, by
Claude (AI review; model unstated) at maximum thinking effort, as review lane R2 of the
W2 phase that is stage 4 of the
[result import](../../../packing/campaign/result-import.md) for Evan Daniel’s comment of
1 October on
[jlevy/squares#238](https://github.com/jlevy/squares/issues/238#issuecomment-5923097530)
(bead `think-48e1`). The lane was prompted separately from the replay lane and shares no
context with it; this document was written without sight of any replay result.
It covers `T-051` ($s(32) = 6$, `V3/C3`), to which the import is an evidence update and
no new entry: the run is registered as `E-n032-evand-zmx2-full-sym-report`, and what is
owed is a review of the run’s mathematics and a rewrite of the entry’s account of what
its two checkers share.

The $s(32)$ theorem itself was reviewed on
[27 September](review-2026-09-27-evand-s32-s12.md) and `zmx2`’s lemma layer on
[28 September](review-2026-09-28-evand-s21-s45-mixed-covers.md) (§5) and, for point
covers under `--pair-points`, in
[the point-only review](review-2026-09-28-wand125-point-only-s21-s45.md) (§3.3). This
review reuses them and adds what is new: the mirrored atom assignment (Lemma A), the run
that rests on it, and the author’s answer on provenance.
It is evidence for the coordinator, not a verdict of record.

**In one line:** Lemma A is stated and proved in the source and the proof is right, for
a point cover in particular; the `--full --pair-points --sym-atoms` run decides the
unfolded covering statement over 28,800 closed root boxes that tile the whole pose space
twice, using no property of the cover; so once that run is replayed here, the D4 fold
leaves the common mode of `T-051`’s two checkers, and what remains shared is the author
and agent, the point-in-square formulation, which `zmx2`’s author was permitted to take
from `zeromargin.py`, the pose parametrisation and the branch-and-bound architecture.
No blocking defect; one retention gap and two stale sentences in the record.

## 1. What Was Reviewed

| Field | Value |
| --- | --- |
| The comment | retained verbatim as [`issue-238-author-2026-10-01.json`](../../../packing/resources/web/evand-square-packing-2026-10-01/issue-238-author-2026-10-01.json), created `2026-10-01T01:49:14Z` |
| Source pin | `08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5`; the `s32` directory is the same Git tree at `2bf33bc3`, which the comment names |
| Cover | `s32_closed_cover_6.txt`, sha256 `a0d2d38fc9a585a166b9e06c5069fdae9bdce44ca9fb64dda75abcc99e3c2144`, 13,085 points, total $31.71350535386 < 32$ (the 27 September review §4; digest recomputed here from the 26 September packet) |
| The run | `certificates/s32/zmx2_full_sym/`: `manifest.txt`, `run.out`, `roots.log.xz`; the log decompresses to 3,261,664 bytes, 28,801 lines, sha256 `3b867c39…` as the manifest says; made `2026-10-01T00:22:43Z`, 6 threads, 1,938 s wall, 11,592 CPU-s |
| Checker | `zmx2.rs` at sha256 `92a4cfe87b4e33d57ce132c9c517eded3fe62b4a5a2151b5ba250b8ee329fe64`, Git blob `8ce809d6…`, 77,198 bytes, the file at commit `e4af291c` (`git cat-file` in the clone; digest recomputed); binary `ed31d3ee…`, rustc 1.91.1 |
| Lemma A | `search/ZMX2.md` §4.9, with §4.10 and §12, at the pin |
| Later commits | `6383ad8` “Claims audit: verification scopes, checker independence…” and `4e11002` “Checker-independence wording…”, both 2026-10-01, after the pin |

Read in full: the comment; the three run files; `ZMX2.md` §§1 to 7, 10 to 12; the diff
of `zmx2.rs` between `6b7f0f79` (the retained 28 September file) and `92a4cfe8` (252
lines: `build_lines`, `AtomSets`, `Cover.alt`, `segment_bound`, the flags, the log
header), and in the new file `parse_cover`, `reflect_y`, `check_d4`, `cmd_cert`,
`family_bound`, `single_bound`, `pair_bound`, `pt_conds`, `line_atoms`; the `s32`
`README.md` and `verify.sh` at the pin; the two later commits as diffs; the register
entry `T-051` and its five evidence entries; and the earlier reviews.
No scratch instrument was needed beyond the root-tiling check of
`/tmp/claude-0/…/scratchpad/r2/roots_cover.py`, written for the companion review and run
on this log too.

## 2. Verdict

**The run is sound and does what the author says.** Its verdict is the statement “every
closed unit square in $[0, 6]^2$, at every centre and every angle, captures weight at
least 1”, decided directly: no invariance of the cover is assumed, checked or used.
Its one new ingredient, Lemma A, is proved in `ZMX2.md` §4.9 and the proof is correct;
the code does what the lemma says (§4 below).
It therefore answers the gap this project found on 29 September (152 boxes left
uncertified by `zmx2 --full --pair-points` at the $\pm 90^\circ$ images of one germ),
and the author’s diagnosis, that the gap was the atom assignment and not a missing
mirror of Lemma Z, is right (§4.3).

**The evidence account should change as the import proposes**, once the run is replayed
here: the fold leaves what the two checkers share, and the shared point-test lineage
enters it, in the author’s own words.
What the rewrite must not say is that the two checkers are now independent: for a point
cover the point-in-square test is the primitive that does most of the work, and it is
one formulation implemented twice (§5).

**Findings:** one retention gap (F1, non-blocking, with its remedy), the brief that
governed what `zmx2`’s author could read is not public (F2, note), the bundle’s own
check only re-reads the log (F3, note), and two sentences in the record that the replay
will make false (F4, non-blocking).
**None is blocking.**

## 3. What the Run Certifies

`zmx2 cert s32_closed_cover_6.txt --full --pair-points --sym-atoms`, log header
`mode=full atoms=pairpts+sym depth=40 … region=x0-59,y0-59,bins0-3`. From `cmd_cert` and
the log:

- **Roots.** Centre cells of pitch $\tfrac{1}{10}$ over $[0, 6]^2$ ($60 \times 60$)
  times four bins of $u = \tan(\theta/2)$ of width $\tfrac18$ over $[0, \tfrac12]$, for
  two passes: $60 \times 60 \times 4 \times 2 = 28{,}800$. The log holds 28,800 `ROOT`
  lines with distinct ids, 14,400 in each pass, whose boxes tile $[0, 6]^2 \times [0,
  \tfrac12]$ in each pass; 11,268,760 boxes, 5,507,496 certified leaves, 141,284 empty,
  0 uncertified, 0 capped, max depth 29 (`roots_cover.py`; the totals equal the
  manifest’s).
- **Passes.** Pass 0 is the cover; pass 1 is the cover reflected by $y \mapsto 6 - y$
  (`reflect_y`, exact on the integer coordinates), over the same boxes.
  The reflection sends $Q(c, \theta)$ to $Q(\rho c, 90^\circ - \theta)$ and preserves
  admissibility, so pass 1 at $\theta \in [0^\circ, 53.13^\circ]$ is the cover at
  $[36.87^\circ, 90^\circ]$; with the square’s $90^\circ$ periodicity the two passes
  reach every angle (`ZMX2.md` §7, “`--full`”). This uses the same elementary identity
  as the fold’s reflection step and none of the fold’s premises: not the invariance of
  the cover, which `--full` neither checks nor needs, and not the quarter-turn reduction
  of the centre.
- **A box.** $L(B) = P(B) + \Lambda(B) \le \mu(Q)$ for every admissible pose of $B$ (the
  Main property), with $P$ the exact weight of the ordinary points certainly in $Q$
  (Lemma P) and $\Lambda$ the line bound; `--pair-points` makes every abscissa or
  ordinate that has a partner point exactly one unit away a line of atoms, so that the
  pair lemma Z can close the germs of a point cover (the point-only review, §3.3); a
  leaf is certified when $L(B) \ge 1$ in integer bound units, or `EMPTY` by Lemma E;
  closed halves cover the parent.
- **The statement.** Every admissible closed unit square in $[0, 6]^2$ captures weight
  $\ge 1$: the unfolded `S32CheckerCover` of the Lean file, with the region $[0, 3]^2$
  and the fold replaced by $[0, 6]^2$ and the mirror.
  With `not_packs_of_cover` (kernel-checked) this is $s(32) \ge 6$.

The common mode this run removes is therefore exactly the fold: `zeromargin.py` still
certifies the $[0, 3]^2 \times [0, \tfrac12]$ region and relies on `d4_reduction`, which
is kernel-checked for this cover (`S32Data.d4Inv`) and so is no trust item on that side;
`zmx2` now relies on nothing of the kind.

## 4. Lemma A

### 4.1 The statement, and what the flag changes

Without the flag a point is an atom of the first line in a fixed list that exists at its
coordinates: vertical grid or segment line $x$, horizontal grid or segment line $y$,
vertical partner line $x$, horizontal partner line $y$ (rule $A_V$, `ZMX2.md` §4.5); a
point on none of them is an ordinary point.
The mirrored rule $A_H$ tries the horizontal line before the vertical at each rank.
Writing $\Lambda_A(B)$ for the line bound under rule $A$, the `--sym-atoms` bound is
$P(B) + \Lambda_{A_V}(B)$ when that reaches 1, and otherwise
$P(B) + \max(\Lambda_{A_V}(B),
\Lambda_{A_H}(B))$.

**Lemma A** (§4.9): for $A \in \lbrace A_V, A_H \rbrace$ and every admissible pose of
$B$, $P(B) + \Lambda_A(B) \le \mu(Q)$; hence the `--sym-atoms` bound has the Main
property.

### 4.2 The proof, re-derived against the code

The source’s proof has three parts, and each is a fact about the code as well as about
the mathematics.

1. **The ordinary points are the same under both rules.** A point is an atom under
   either rule iff its $x$ is in `vpos` or `vpart` or its $y$ in `hpos` or `hpart`; the
   rules differ only in the order the four memberships are tried.
   `build_lines(pm, raw_segs, &sets, lc, hfirst)` is called twice with the same position
   sets and the same `BTreeMap` of aggregated points, and `build_cover` then asserts
   `pts2 == pts` with a release-mode `assert!`, aborting without a verdict if it ever
   failed. So $P(B)$, the inherited certain-in weight and the candidate lists of `cert`,
   which refer to ordinary points only, mean the same thing in both bounds.
2. **Each line bound is valid for any finite set of atoms on the line.** `family_bound`
   takes the line list as an argument and holds no cache; `line_atoms(ctx, fb, l)`
   decides each atom’s four conditions from its own position by `pt_conds` (Lemma P per
   $G_k$, exact `i128`) and Lemma W at a wall; `single_bound` counts an atom when all
   four hold; `pair_bound` counts a conditional $a$-atom iff $y \ge z$ and a conditional
   $b$-atom iff $y \le z + u_0^G$ with $u_0^G = \lfloor u_0 G \rfloor \le uG$,
   enumerates as candidates the two ends of the $\zeta$-range, the five chord ends, the
   breakpoints of both lines, the $a$-atom positions and the $b$-atom positions minus
   $u_0^G$, and at each takes the smaller of the two one-sided limits $A(z) + B(z^-)$
   and $A(z^+) + B(z)$, which is $\le \Phi(z)$ because $A$ is nonincreasing and $B$
   nondecreasing in $z$. Nothing in Lemmas S, Z, W or H, or in their code, refers to
   which other points are atoms of the line, or of any line.
   For a point cover every $F$ is constant, $\Phi$ is a step function, and the infimum
   over the closed $\zeta$-range is attained at a candidate’s one-sided limit, which is
   what the code evaluates; this is the closedness argument of the point-only review
   (§3.3), unchanged by the choice of rule.
3. **Disjointness.** Under either rule every point of positive weight is an atom of
   exactly one line or ordinary (`o ∈ {0, 1, 2}` in `build_lines`), so $\mu = \mu_{ord}
   + \sum_\ell \nu_\ell$ is a decomposition into nonnegative measures, with $\nu_\ell$
   the line’s density plus the atoms the rule gives it (for a point cover, the atoms
   alone). Lemma DP’s partition of the active lines into singles and adjacent pairs
   gives $\sum$ group bounds $\le \sum_\ell \nu_\ell(Q)$, and $P(B) \le \mu_{ord}(Q)$.
   So $P(B) + \Lambda_A(B) \le \mu(Q)$ for each rule, and the larger of two lower bounds
     is a lower bound: `segment_bound` returns
     `sb.max(segment_bound_lines(…, vl2, hl2))`.

Two further things checked: `reflect_y` calls `build_cover`, so pass 1’s reflected cover
carries its own `alt` and the mirrored bound is available in both passes (the §12
diagnosis found the gap in both, and the run closed both); and the `--log` resume is
keyed on the header, which carries `+sym`, so a log from a run without the flag cannot
be resumed into one with it (the manifest says `0 already done`).

### 4.3 Why both rules are needed, and why Lemma Z needs no mirror

The rules are exchanged by the rotations by $\pm 90^\circ$, which swap vertical and
horizontal lines; $A_V$ alone is not rotation-invariant, so an invariant cover can be
closed at a germ and not at its rotated image, and a `--d4` sweep never sees the image.
The source’s diagnosis (§12): at the deepest uncertified leaf near $(5.498, 1.501,
0.179^\circ)$ the missing mass is the point $(5.001, 1.999)$, the rotated image of the
pair $(1.999, 0.999)$, $(0.999, 0.999)$; both lie on the vertical partner line $x =
5.001$ and on the horizontal partner lines $y = 1.999$, $y = 0.999$; $A_V$ made them
atoms of $x = 5.001$, where at this germ $d \approx \tfrac12$ and the pair $(4.001,
5.001)$ cannot count them, while the horizontal pair that Lemma Z closes there carried
no atoms. With the mirrored rule alone the picture is exactly mirrored: the fundamental
cells fail and the rotated cells verify.
That is the behaviour of an assignment, not of a lemma.

§4.10 shows why no mirrored Lemma Z exists to be missing: as $\theta \to 0^+$ the chord
of a vertical line differs from the bounded $[L_2, H_2]$-chord only for lines cut from
below by the left edge ($d \to \tfrac12$) and from above by the right edge ($d \to
-\tfrac12$), which are exactly Lemma Z’s $a$ and $b$ with $H1_b = \zeta + u$; the
opposite combination is the picture at $\theta \to 90^{\circ -}$, which the checker
meets only as $\theta \to 0^+$ of the reflected cover.
I re-derived the expansions $f_1 = (d - \tfrac12)/(2u) + O(u)$ and $f_2 = (d +
\tfrac12)/(2u) + O(u)$ from Lemma C and agree.
Soundness does not depend on this remark; completeness at germs does.

### 4.4 Without the flag nothing changes

`segment_bound` computes the mirrored bound only when `have + sb < target`, and `alt` is
`None` when the two rules give the same lines, which `info --sym-atoms` reports.
So for the mixed covers of $s(21)$, $s(45)$ and $s(60)$ without `--pair-points` the flag
is inert, and the source reports their censuses unchanged root for root (`ZMX2.md` §12,
table); the author’s statement that the bundles’ `verify.sh` reproduce their shipped
censuses from the new source is a claim the replay of `T-062` will test for $s(60)$. For
$s(32)$ under `--d4 --pair-points --sym-atoms` the census changes from 1,405,342 to
1,395,462 boxes, as it should where the mirrored bound certifies a box earlier.

## 5. What the Two Checkers Share Now

The author’s answer to ask 2 is the first statement of record about provenance: `zmx2`
was written to be independent of `zm_mixed.py` only, and its brief
(`tasks/s21-finish/xcheck.md`, not public) allowed reading `zeromargin.py`,
`ZEROMARGIN.md`, `RUNG2.md` and `zmcheck`’s `main.rs` for point primitives, so “Lemma P
should be read as derived from `zeromargin.py`’s $G_0$–$G_3$”. The later commits put the
same into the source: `6383ad8` rewrites “two independently written checkers” as
“separately written … sharing the point-test formulation” in every bundle README and on
the site, says of `zmcheck` that it was “written from `zeromargin.py`’s lemmas, so the
point-test formulation is common”, and adds to the $s(21)$ and $s(60)$ READMEs that “an
error in that formulation would be common to both”; `4e11002` makes the same change in
`FORMAT.md` and the bounds data.

For `T-051`, after the replay of this run, the two decisions of the covering statement
are `zeromargin.py --d4` (exact, 7,200 roots of the fundamental region, with the fold
kernel-checked) and `zmx2 --full --pair-points --sym-atoms` (interval-certified, 28,800
roots of the whole space, no fold).
They share:

- the author and the AI agent, and the statement decided;
- the point-in-square formulation, $G_0$ to $G_3$ with the corner-and-vertex rule for a
  box, one design in two arithmetics, which for a point cover is the primitive that
  decides most leaves; the formulation is kernel-checked on the `zeromargin.py` side
  (`lemmaA`, `polyOk_quad`), which bounds, and does not remove, the common mode;
- the pose parametrisation ($u = \tan(\theta/2)$, closed root boxes, the admissibility
  exemption) and branch and bound with closed halves;
- the reduction from the cover to the bound, which is kernel-checked and so no trust
  item.

They no longer share the fold, the region, or any symmetry premise.
They never shared the germ mechanism (chains against Lemma Z’s pair programme), the
arithmetic, or the parsers.
With `--sym-atoms` the `zmx2` side rests on Lemma A where the `--d4` side rested on the
fold; Lemma A is `zmx2`’s own and a theorem of §4, and nothing in `zeromargin.py`
corresponds to it.

The author offers a pair that “doesn’t depend on `zmx2` at all”: `zeromargin.py` and
`zmcheck` on the second cover `s32_shift_v1.txt`, each certifying every root of the
fundamental region. That pair shares the same point-test lineage, by the author’s own
account of `zmcheck`, and both halves of it use the fold; it removes `zmx2`’s interval
arithmetic from the basis and nothing else, so it is not a stronger basis than
`zeromargin.py` with this run on either axis, and it is for a different cover than the
one in Lean. The strongest basis the author names, the hypothesis-free `s32_eq_6` of
`S32Lower.lean` (5,990 chunk theorems decided by `decide +kernel`, opt-in, 13.8 CPU-h by
the source’s account, reported since 28 September), would remove both checkers from the
trust base and is a separate import (`think-e8qx`), not part of this one.

## 6. Findings

Severity is blocking, non-blocking, or note.
**None is blocking.**

### F1. The checker source that made the record is retained in no packet (non-blocking)

The manifest names `zmx2.rs` sha256 `92a4cfe8…` at `e4af291c`; the 1 October packet
retains the pin’s `1cd4dcbd…`, a diff of 1,786 lines later (area densities,
`--first-order`), and the 28 September packet the earlier `6b7f0f79…`, which has no
`--sym-atoms`. The runbook’s stage 2 asks that the packet retain every checker the
certificate needs. The remedy is one file: Git blob
`8ce809d617d239dcc40032e97b780a82bd4fb851`, 77,198 bytes, from the source’s history,
added to the 1 October packet with a manifest row that names its commit.
Until then the replay can build it from the clone and must say so; building the pin’s
`1cd4dcbd` instead is a test of the author’s claim that the later changes are inert
without their flags, and the receipt must name which source was built.

### F2. The brief is not public (note)

The statement of what `zmx2`’s author could read rests on the comment, retained
verbatim, and now on the source’s READMEs after `6383ad8`; `tasks/s21-finish/xcheck.md`
is in no public revision.
The record should cite the comment and say the brief was not seen.
The plan’s reply already asks for it.

### F3. The bundle’s own check re-reads the log (note)

`certificates/s32/verify.sh` at the pin reads `zmx2_full_sym/roots.log.xz` and asserts
28,800 distinct roots over both passes with none uncertified; it does not rerun the
sweep. The replay here is the first fresh run of this command outside the source.

### F4. Two sentences in the record that a passing replay will make false (non-blocking)

`E-n032-evand-closed-cover-zmx2-replay` says “The fold cannot be dropped from `zmx2`’s
side”, which was true of `zmx2` without the flag and should read so after the replay.
`E-n032-evand-closed-cover-source-run` says the two entries “together put `T-051` at
`C4`”, which the ladder change of 30 September has already made stale.
`T-051`’s composition says “That run has not been replayed here, so the fold stays in
the common mode as this record has confirmed it”, which is the sentence the replay
retires. Proposed wording is in the lane’s report.

## 7. What the Replay Must Show

For the evidence account of `T-051` to be rewritten with the fold removed from the
common mode, the replay lane must retain receipts showing:

- `zmx2 cert certificates/s32/s32_closed_cover_6.txt --full --pair-points --sym-atoms
  --threads T --log OUT`, from the retained bytes, printing `VERIFIED` with the log
  header `mode=full atoms=pairpts+sym depth=40 node_cap=20000000 kappa=1.5 K=30
  region=x0-59,y0-59,bins0-3`, 28,800 roots, 11,268,760 boxes, 5,507,496 certified,
  141,284 empty, 0 uncertified, 0 capped, max depth 29, and its census equal to the
  shipped `zmx2_full_sym/roots.log` root for root (the source’s
  `search/zmx2_census_cmp.py`, or `devtools.audit_evand_mixed_covers compare-zmx2` once
  it reads this mode); the source’s figure is 11,592 CPU-s on 6 threads.
- Which `zmx2.rs` was built (F1) and its digest, `rustc -vV` with the target triple,
  that `RUSTFLAGS` was unset, the binary digest, the host’s architecture.
- As the control that the flag is what closes the gap: the same command without
  `--sym-atoms` ending `NOT VERIFIED` with 152 boxes uncertified, 38 in each of the four
  roots near $(0.5, 4.5)$ and $(5.5, 1.5)$, which is the retained result of 29 September
  (`receipts/s32_zmx2_full_pairpoints.log` in the 28 September packet) and need not be
  rerun if that receipt is cited.
- Two mutated covers refused with the flag on, held by a test.
  The author’s own are the natural pair: the cover weakened by $0.0125$ at either of the
  decisive points $(5.001, 1.999)$ and $(5.001, 0.999)$, refused at the germ with an
  exact violating pose of mass $0.998413$ (`ZMX2.md` §12). A refusal on an exactly
  scaled cover (the 27 and 28 September reviews’ method) is an acceptable substitute for
  one of the two.

On those receipts the import adds a verified entry beside the report
(interval-certified, replayed here, `relationship_to_generator: same-implementation`),
and `T-051`’s `composition` and `limitations` take the wording of §5.

## 8. Rung, Significance and Credit

Under [`epistemics.md`](../../../epistemics.md):

- `T-051` stays at **`V3/C3`**: the import adds evidence of the same kind, machine
  replay of the source’s own checker with a mapped review, and changes neither rung.
  What it changes is the composition note, which rung 4’s reviewers and oversight record
  will read. Rung 4 still needs a second adversarial review by a distinct reviewer and a
  human oversight record; rung 5 the source’s hypothesis-free Lean theorem built and
  reviewed.
- **Significance:** `S4`, unchanged; the claim has not changed, and an evidence update
  does not rescore it.

**Credit.** The run, the lemma and the flag are Evan Daniel’s (`evand`),
computer-assisted under human direction as `CREDITS.md` says; the gap it closes was
found by this project’s replay of 29 September, which the source credits in `ZMX2.md`
§12 and the `s32` README.

**Licence.** MIT (`LICENSE` under `s12/`).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
