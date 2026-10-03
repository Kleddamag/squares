# Eleven-Square Optimality Paper: Adversarial Review

**Date:** October 3, 2026\
**Reviewer:** Claude Code, one lead session with six parallel sub-reviews; human
oversight pending\
**Subject:** the published paper
[A Review of the Optimality Proof of the Trump Packing of 11 Squares](https://jlevy.github.io/squares/papers/n11-optimality-review.md),
from its
[article source](../../../packing/devtools/templates/n11-optimality-review-article.md),
and the proof it explains\
**Tracking:** none; the `tbd` CLI is not installed in this session

**Disposition:** No mathematical error was found in the paper or in the proof it
explains. Every number the paper states was reproduced, most of them by independent
recomputation from first principles rather than by rereading a receipt.
The paper has one footnote that cites the wrong section of the original proof, one
stated rule that is only a necessary condition for the exclusions it describes, and one
step of the final deduction that silently skips the symmetry image the argument is
about. Each is a wording defect with a one-sentence fix.
The review also found seven simplifications of the exposition that follow from the
accepted premises without new computation, and one simplification that was examined and
found not to be available.

Line numbers below refer to the article source.
The published page was built from commit `ea0a3b19`, which is the commit reviewed; a
fresh render at that commit is byte-identical to the published Markdown.

## Scope and Method

The four reviews of September 30, 2026 ([mathematical][math-review],
[proof reconciliation][reconciliation], [intuition][] and [citations][]) compared the
paper with the original proof and approved it.
This review starts from their dispositions and asks a different question of each
component: not whether the paper matches the proof, but whether the component is true,
by recomputing it another way.

What was done, by component:

- **Endpoint and construction.** Exact arithmetic in $\mathbb Q(u)$ written from scratch
  (polynomials of degree below eight over `Fraction`, inverses by the extended Euclidean
  algorithm modulo the defining polynomial, signs by a rational bracket of width
  $10^{-124}$). Sturm sequences for the root counts.
  The eleven squares rebuilt from Appendix A, all 44 vertices, all 55 pairs, all 112
  separation features and all 512 branch selections classified independently.
- **Center cover and symmetry.** The sixteen cells rebuilt from the retained sites by
  halfplane intersection; diameters, half-turn symmetry, the 2,184 canonical masks, the
  220-region overlay, and all distance bans recomputed with `Fraction`; the three finite
  problems re-solved by an independently written search, with ablations.
- **Exclusions and capture.** The mask-0 field certificate and case 2095 replayed with
  the repository’s checkers; the transfer sets of all 46 accepted field packets
  recomputed from the paper’s rule; the exclusion inventory, census, source graph,
  branch predicates and role map read from the receipts and checker code.
- **Local isolation.** The 1,936 elementary gap functions, their gradients, the feature
  census, the 88 negative-feature margins and all 8,448 dual margins recomputed in
  80-digit arithmetic from the paper’s own formulas, sharing with the repository only
  the retained dual weights, radii and row labels.
  Pose inclusion recomputed with an independent arctangent and chart.
- **Replay.** Every retained replay script that can run in this checkout was rerun and
  diffed against its receipt: exact witness, D4, case census, local isolation and its
  partial control, local dual residuals, pose inclusion against the pinned upstream near
  state, source graph against the pinned upstream capture objects, six field
  certificates, both inventories, the final composer, the T-060 control tests, 64 n = 11
  test files, the paper render, its PDF, `check_documentation` and `make format-check`.
- **Document.** Every relative link and anchor resolved; the published HTML checked for
  unrendered or erroneous mathematics (159 formulas, none failing); figure labels,
  caption facts and phone-width layout inspected in a browser.

Five of the six sub-reviews were cut off by a session rate limit while writing their
reports.
Their scripts and outputs were recovered and rerun by the lead session, which is
why some sections below cite a script rather than a sub-review.
The scripts are in the session scratchpad and are not part of the repository; see
[Follow-Ups](#follow-ups).

Not done here: the 44 remaining field packets, the 276 non-field executions, the
fourteen root rounds and the capture nodes were not replayed, because their 2.1 GB of
source objects are not in the checkout.
Those remain the observed executions that the
[final composition](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/final-composition.json)
binds, as the paper says.

## 1. Correctness

### 1.1 Statements in the Paper That Need Correction

1. **The transfer rule is stated without the half-turn (lines 433–445).** The paper says
   a field certificate “excludes a mask $J$ only when $O\subseteq J$ and
   $\sum_{i\in P\cap J}q_i>b$.” Both checkers apply the rule to $J$ *or to its
   half-turn* (`check_n11_optimality_field_runner.py` lines 730–739;
   `check_n11_optimality_field_mask0.py` lines 585–593), and the census contract says to
   apply it “to each representative and its half-turn.”
   Recomputing the rule as written over all 46 accepted packets reaches 1,666 of the
   1,904 field cases; the other 238 are reached only through the half-turn.
   The rule as the paper states it is sound but does not account for the inventory the
   paper then reports. Fix: “excludes every case whose mask, or its half-turn, satisfies
   …”
2. **Footnote `[^field]` cites the wrong section (line 926).** It links “Original proof,
   §5: field charges and transfer.”
   Section 5 of the original proof has no field-charge text; the words charge, median,
   capacity and site do not occur in it.
   The only field material is §12 ("59 field certificates … transfer … justified by
   containment of the antecedent"), and the five-site charge is documented only in the
   census contract’s mask-0 section.
   Fix: cite §12, or drop the original-proof link.
3. **The final deduction skips the symmetry image (lines 713–718).** The packing that
   capture encloses is the D4 image $g(P)$ supplied by the symmetry lemma, and $Q$ is a
   separate fixed alignment of case 438 with the construction.
   The paper writes only $Q^{-1}$ and “an original side-$S$ container centered inside
   $U$ becomes $[(T-S)/2,(T+S)/2]^2$.” The step is valid because every D4 element about
   $(U/2,U/2)$ maps the concentric container onto itself, and because a quarter-turn
   leaves every orientation unchanged modulo $\pi/2$, so the half-angle values carry
   over. The original proof (§10) and the census contract both state the first fact; the
   paper states neither.
4. **“Some certificates use field coordinates” (line 695) should be “the certificate
   data use field coordinates.”** The field checker, the generic checker, the capture
   headers and pose inclusion all store centers as $p_f=Bp$. The Figure 6 caption (line
   344\) uses “field center coordinates” 350 lines before the term is defined.
5. **The obligations table says “all four closed leaves” (line 759).** The near leaf is
   not closed by a contradiction; its header records `"closed": false`. “Closed” here
   means the branch inequalities are closed, which the table does not say.
6. **“The accepted ten nodes and nine parent edges bind this enclosure to the original
   unconditional case” (lines 567–568).** They do so only together with the
   fourteen-round root chain, the root bridge and the first-step join, which lie outside
   the ten-node source graph (`inventory_n11_completion.py` joins them separately).
   Fix: “Together with the root chain, …”
7. **Two different fourteens (Figure 9 caption, line 555).** “The fourteen root rounds
   precede the descendants shown here.”
   The fourteen adaptive rounds precede the root *node* itself (`capture-root-chain`:
   rounds 1–14, 154 owner updates), and the root node then has another fourteen steps
   (`"steps": 14` in its header).
   “Root round” is never defined; it means one parallel update of all eleven owners
   against a common prior.
8. **Zero-based indices without saying so (Figure 6, line 342).** “Step 1” is the second
   of five updates (the step owners are 6, 10, 7, 14, 11) and “row 17” is
   $[17/32,18/32]$. The paper declares zero-based numbering only for cases (line 262).
9. **“A zero gap is accepted, since it represents legal contact” (line 177).** A zero
   gap on one axis is not contact: squares 0 and 4 have a zero $x$-gap and are 1.877
   apart. Contact is a zero *maximal* gap over the edge normals of both squares; “gap”
   itself is undefined at this point.
10. **The linked reviews report a different verification level.** The paper (lines 121
    and 776) and the register say V3/C3. The linked [whole-proof acceptance][acceptance]
    says “support **V4/C5**,” as does the simplification review.
    Both predate the ladder change of September 30 that the
    [register note](../../../packing/frontier/results.yaml) explains; the paper does not
    say so, and a reader following its links meets both levels.

### 1.2 The Proof and Its Verification Record

No error was found. The following were confirmed by recomputation, with the number that
decides each claim.

| Claim in the paper | Confirmed how | Decisive value |
| --- | --- | --- |
| $u$ is the unique root in $(9/25,37/100)$; $T$ as displayed | Sturm sequence: $p$ is squarefree with two real roots, $-0.546$ and $0.3657693076$; $p'$ has no root in the interval | the 28 displayed decimals of $T$ are exact; next digits 009 |
| $T<U$ | exact sign test | $U-T=2.103\times10^{-21}$ |
| $T$ satisfies the degree-8 side polynomial | exact reduction in $\mathbb Q(u)$ | residual zero; $p$ and the side polynomial are both irreducible, so $\mathbb Q(T)=\mathbb Q(u)$ has degree 8 |
| Appendix A gives eleven unit squares in $[0,T]^2$ spanning $T$ | rebuilt from the paper’s text; matches `packing.py` to $9\times10^{-57}$ | 20 vertex coordinates exactly on walls; smallest nonzero wall slack 0.5486 |
| 55 pairs weakly separated, 14 in contact | own separating-axis test | smallest positive gap $\eta=0.02487$ at pairs (6,9) and (8,10) |
| 16 closed cells of physical diameter below one | cells rebuilt from the sites; exact diameters | largest $(U-1)^2\operatorname{diam}^2=0.9509$ (cell 6); a uniform $4\times4$ grid gives 1.0347 |
| half-turn maps cell $j$ to cell $15-j$; no other D4 element permutes cells | site set tested under all eight elements | invariant only under the identity and the half-turn (0 of 16 cells mapped by the other six) |
| 4,368 masks, 2,184 representatives, the four indices | enumerated | 438, 999, 1462, 1659 are the listed tuples |
| 220 overlay regions, 212 polygons and 8 points | overlay rebuilt | vertex sets identical to the receipt; all 8 points are the center $(1/2,1/2)$ |
| 1,572 strict bans; none at distance one | all pairs recomputed | 1,572 is exactly the set of label-distinct pairs with physical distance below 1; largest banned 0.99587, smallest unbanned 1.00335 |
| the three finite problems are UNSAT | independent search | UNSAT with 1,232, 1,882 and 759 nodes; also UNSAT from the half-turned sources |
| the bans and all four views are needed | ablations | without bans, sources 999 and 1462 become SAT; every proper subset of the views leaves some source SAT |
| $E=\{0..2183\}\setminus\{438,999,1462,1659\}$, 1,904 field and 276 other | inventory and census receipts, disjointness checked | 276 = 27 (A1) + 76 (A2) + 173 (A3); 1,931 = 1,904 + 27 |
| the five-site charge and its transfer | mask-0 replayed (136 rows, 55 owned points, 459 cases); 46 packets’ transfer sets recomputed | every recomputed set equals its receipt |
| ownership depends only on the owner’s cell | `ownership()` in the field checker uses the cell, the walls and the full angle range | transfer to any mask containing $O$ is sound |
| cases 2175 and 2176 rest on the 1,931-case baseline, acyclically | `replay-d4-cuts.json`: `baseline_case_ids` = census baseline; 506 allowed raw masks; all 38 and 36 offending regions UNSAT | neither case is in the baseline (`check_n11_baseline_d4_cuts.py` lines 77–100) |
| case 1383 splits at $y_{13}=4/3$, physical height | field bound $B(U/2+4/3)$ | both branches `PASS`, 8 nodes |
| branch table directions | `keep` fields of the four leaf headers | far15 `y15 le`; far13 `ge, t13 le`; far2 `ge, ge, t2 le`; near `ge, ge, ge` |
| ten nodes, nine edges, fourteen rounds, 136 rows, 1,542 vertices | source-graph, root-chain and pose receipts; pose inclusion recomputed | all 136 rows and 1,542 vertices inside; narrowest slack $2.3\times10^{-12}$ |
| 112 features, 24 available, 88 unavailable, 512 raw, 128 branches, 42 rows | own census from the gap functions | per pair 1,1,1,1,2,2,4,1,1,2,2,2,2,2; 42 = 20 wall rows + 22 pair rows; 128 = 512/4 from the two flush pairs (3,4) and (3,5) |
| 88 features stay unavailable on the rectangle | own Taylor test | smallest margin $0.012636$ |
| 8,448 dual margins, $c_j<1$ | duals rechecked against recomputed gradients and own curvature bounds | worst ratio 0.6768 with a cruder $D_{op}$; receipt 0.6765052082 |
| the curvature bound $K$ holds | derivation of the Hessian; 3,000 random second differences in the rectangle | largest observed $\lvert d^\top Hd\rvert/K=0.997$ |
| radii within the working box | `focused.json` | all 33 radii $\le1/64$; largest 0.00676, smallest 0.00065; two exceed the older uniform $1/248$ |
| omitting non-contacting pairs is harmless | own clearance test | all 41 stay strictly separated across the whole rectangle, clearance $\ge0.0151$; non-tied wall corners clear by 0.548 |
| the frame map and role bijection | algebra; receipt `inverse` string; composition joins | $Q^{-1}(x,y)=(y,-x)$; roles $[3,15,8,0,4,1,2,11,9,10,13]$ |

Replays: every rerun matched its receipt with zero non-timing differences, including the
source graph against freshly fetched upstream capture objects, which reproduced the same
four stale leaf digests the paper reports.
Two field receipts, masks 1155 and 612, bind an older revision of the field runner than
the checkout’s (different `checker_sha256`); the current runner reproduces their results
exactly. This is a provenance note, not a defect.

Three observations about the record that the paper might state:

- **Inclusion is fitted, not loose.** The 33 radii were chosen to fit the captured
  domains: for every owner the required center radii are within $10^{-7}$ of the
  declared ones, and the angular requirement equals the declared radius to six digits.
  The proof is sound either way, but a reader who imagines a comfortable margin is
  wrong; the margin lives in the dual ratio 0.68, not in the box.
- **The branch system is complete, not merely necessary.** The paper says omitting
  non-contacting pairs “cannot discard a feasible packing.”
  The stronger fact holds: no new contact can form anywhere in the rectangle, so the 128
  branches are the whole feasible local structure.
- **The curvature bound is tight.** At 99.7 percent in random probing, $K$ is not
  conservative. That is a feature of the proof, but it means the margins quoted above are
  the only slack there is.

## 2. Simplicity of the Proof

### 2.1 Simplifications Available Now

Each of these follows from the accepted premises and needs no new geometric computation.

1. **One chart.** The construction’s parameter $u$ *is* the half-angle parameter of the
   five tilted squares: $u=\tan(a/2)$ with $a=2\arctan u=40.1819^\circ$ (the
   `packing.py` docstring says so).
   The paper introduces $c=(1-u^2)/(1+u^2)$ at line 162 and $t=\tan(\theta/2)$ with the
   same formulas at line 265 as if unrelated.
   One sentence joins them and makes the angular displacement of a tilted square
   $2\arctan t-2\arctan u$, which is what pose inclusion bounds.
2. **Where the polynomial comes from.** Treating $u$ as a free parameter in Appendix A,
   43 of the 44 zero gaps at the construction vanish identically.
   The one that does not is the contact of square 2, $A(x_0,T-1)$, with square 10, the
   image of $A(\eta+2,-\zeta)$: its gap is exactly
   $p(u)/\bigl(2u(1-u^4)(1+2u-u^2)\bigr)$. So the degree-8 equation is that one contact
   condition, and for $u$ below the root the two squares overlap.
   The paper presents the polynomial as given; this derivation explains it in two lines.
3. **Why four survivors, and why 438.** The four surviving masks are the construction’s
   own center pattern under the eight symmetries: the identity and half-turn give 1462,
   the two axis reflections give 999, the two diagonal reflections give 1659 and the two
   quarter-turns give 438. No construction center is within 0.0079 (normalized) of a
   cell boundary, so these labels are unambiguous.
   Case 438 is captured because it is the quarter-turned construction, which is why the
   alignment $Q$ is a quarter-turn.
   The paper never says this; it is the single most orienting fact about the survivors.
4. **A half-plane form of the charge.** For a convex core and five sites, “the
   projection interval contains the median in every direction” is equivalent to “every
   closed half-plane containing the core contains at least three of the five sites”
   (apply the hypothesis to the two supporting half-planes of each direction).
   Capacity one then takes one line: a strictly separating line gives two disjoint
   closed half-planes, which would hold $3+3>5$ sites.
   The finite test becomes: half-planes bounded by lines parallel to a core side or
   through two sites. This is not “the core contains three sites,” so it respects the
   earlier reviews’ warning.
5. **A shorter transfer rule.** In all 46 accepted packets, $P\subseteq O$ and
   $\sum_{i\in P}q_i>b$ holds on its own.
   The rule therefore reduces to: a certificate with owner set $O$ excludes every case
   whose mask or half-turn contains $O$. The $P\cap J$ generality is never used, and the
   sentence “Neither an equal budget nor an unsupported transfer to a larger mask
   suffices” (line 444) becomes unnecessary.
6. **Treat the field frame as a storage convention.** State the alignment map in
   physical coordinates, $p_T=Q^{-1}(p-(U/2,U/2))+(T/2,T/2)$, and note once that the
   certificate files store $Bp$ with $B=(191/50)/U$. The disclaimer that the frame “is
   not a claim that eleven unit squares fit in a side-$L$ square” then disappears;
   $L=3.82<T$ in any case.
   The branch variables $y_{13}$ and $y_{15}$ are already physical.
7. **Smaller cuts.** “The unique positive real root” identifies $u$ without the
   interval, since $p$ has one positive root.
   The 512 raw selections are a computational detail; the exposition needs only the 128
   branches. The local contradiction can be written without $\tau^2$: from
   $\tau r_j\le\epsilon_j\tau R+\tau^2M_j/2$ divide by $\tau$ and use $\tau\le1$ to get
   $r_j-\epsilon_jR\le M_j/2$, which the margin denies.
   Figure 10 is then optional.

### 2.2 Simplifications Examined and Not Available

- **A symmetric cover.** If the sixteen sites were D4-symmetric, every symmetry would
  permute the cells, the 4,368 masks would fall to about 550 orbits, and the overlay
  machinery would disappear.
  A parameter search over the D4-symmetric sixteen-site families (orbit types $8+8$,
  $8+4+4$, and so on) found none whose cells all have physical diameter below one: the
  best is the $4\times4$ grid at normalized diameter 0.3536 against the required 0.3476,
  and the retained irregular cover achieves 0.3389. A symmetric cover needs more cells,
  and $\binom{20}{11}/8$ already exceeds 2,184 by a factor of ten.
  The irregular cover is a deliberate trade, and the paper could say so with one number:
  a grid cell has physical diameter 1.017.
- **Dropping the baseline dependency of cases 2175 and 2176.** Their necessary
  halfplanes are the only exclusions that depend on another exclusion set.
  Excluding them directly, by a center partition as for case 1383, would remove that
  dependency and the acyclicity obligation with it.
  This needs new geometric computation and is noted for a future revision of the proof,
  not of the paper.

## 3. Clarity of the Presentation

### 3.1 Structure

1. The paragraph on T-060, S5/V3/C3 and the ladder (lines 121–127) sits inside “The
   Result,” between the theorem and the method.
   It belongs in “What Was Verified,” where the same facts are repeated at lines
   776–782.
2. “From Weighted Points to a Global Proof” is lineage, not proof.
   Its second half (the gap between 3.875 and $T$, what the optimality proof adds) is
   the useful part; the rest could move to a footnote.
3. The symmetry lemma is stated as “some square symmetry of every remaining packing
   admits case 438” (line 506). Clearer: “for every remaining packing, some symmetry
   image of it has a valid assignment with mask 438.”
4. The paper never defines $s(11)$ (first used at line 54) and never states that a
   square’s orientation is taken modulo $\pi/2$, which is why $t=1$ and $t=0$ describe
   the same square and why the quarter-turn $Q$ preserves orientations.

### 3.2 Terms Used Before, or Without, Definition

- Never defined: *update*, *step*, *round*, *root round*, *capture graph*, *node*, *live
  row*, *compression*, *common-core inclusion*, *self-containment cut* (a square
  contains its own owned hull, which bounds its center), *seed*, *proposal*, *partner
  row*, *common prior*, *source graph*, *tied* (zero projection gap at the construction,
  not physical contact; read as “touching” it gives 36 rows, not 42), *available*
  (feature), *analytic working box* (line 583), *gap*, *wall contact*.
- Used before definition: *residual* (Figure 6 caption, line 346, defined at 365);
  *field coordinates* (line 344, defined at 695); *feature* (line 139 in the sense of a
  threshold feature, line 614 in the sense of a separation feature).
- Three senses of *field*: the number field $\mathbb Q(u)$ (line 179), a field
  certificate (line 394, never explained as a charge field) and field coordinates (line
  695).
- Notation clashes: $s$ is $\sin a$ at line 162, $s(11)$ is the optimum and $S$ a
  hypothetical side; $c_j$ (line 676) beside $c=\cos a$.
- The general certificate is never described.
  Across the 46 packets the features use three, five or seven sites, 25 packets add
  weighted point charges, budgets range up to 22 and thresholds up to 11. One sentence
  would make “total capacity $b$” concrete: each feature or point charge contributes its
  weight to at most one core, and $b$ is the sum of the weights.

### 3.3 Sentences a Reader Cannot Parse Without the Code

- Line 366: “A larger proposed domain may contain impossible points that those necessary
  cuts already remove.”
  This describes `covering_input_domain`: the proposal must contain the required domain
  (predecessor, walls and cuts intersected), and coverage is checked only on the
  required domain.
- Line 462: “They cannot use the final four-survivor reduction to prove its own
  premise.” The antecedent of “its” is unclear.
  Suggested: “The four-survivor reduction assumes these two exclusions, so their cuts
  may not use it; they rely only on the 253 survivors of the 1,931-case baseline.”
- Line 355: “A stronger collision check compares a proposed pose against another
  square’s entire possible pose cover.”
  The check compares a region of query centers for one angle row, and “stronger” is only
  relative.
- Lines 405–408 say the bounding directions of each sector suffice without saying why no
  sector reaches a half-turn: both axis normals are always among the event directions,
  so every sector lies within one quadrant.
- Line 622: “Each has 42 necessary tied inequalities, including wall inequalities” is
  the first and only use of “tied.”

### 3.4 Figures and Rendering

- All 71 relative links and 19 anchors resolve.
  The six internal fragment links resolve.
  External links were not fetched through the proxy.
- The published HTML typesets all 159 formulas with no error; the caption formulas
  render.
- The caption facts render as 220 regions, 1,572 bans, regions 9 and 12 for the
  illustrated ban, cell 9 for the capacity figure, 32 rows and 5 updates for case 2095,
  and 8,448 margins over 128 branches, all matching the prose.
- On a 375-pixel phone viewport, nine of the eleven figures keep a minimum width of 680
  to 850 pixels and scroll horizontally inside the figure, by the stylesheet’s design.
  A phone reader pans every diagram.
- Fourteen of the 21 figure labels contain glyphs the shipped face lacks (≤, ≥, ⊆, ∩, τ,
  superscript 2 and subscript digits), which the browser draws from a fallback font.
  Every edge label of the capture tree is such a string.
- Figure captions carry disclaimers that belong once in the text ("is not a certificate
  for the displayed schematic," “the drawing does not show three sites inside a core,”
  “not a projection of the 33-dimensional feasible set”).

## What This Review Did Not Establish

- It is a same-method confirmation with independently written arithmetic for the
  endpoint, cover, overlay, search and local components, and receipt reading plus
  checker replay for the exclusions and capture.
  It is not a distinct proof method and not a proof-assistant verification.
- The bulk exclusions and the capture geometry were not rerun; their receipts, joins and
  the final composer were.
- The independent recomputations are one-off scripts in the session scratchpad: exact
  $\mathbb Q(u)$ arithmetic and the construction census (`endpoint/`), the cover, masks,
  overlay, bans and search (`d4/`), the field transfer sets (`exclusions/`), and the
  80-digit local recomputation and pose inclusion (`local/`). They are not retained
  controls.

## Changes That Would Simplify Validation or Prepare a Formal Proof

These go beyond the paper.
Each names what it would remove and what it would cost; none is required for the result
as it stands.

**Validation today.** The fast components replay in about two minutes in this checkout
(D4 1.3 s, census 0.2 s, local isolation 22 s, dual residuals 18 s, pose inclusion 15 s,
composition 3 s), the 46 accepted field packets take about fifteen minutes, and the rest
is the 276 generic exclusions and the capture: the last 32 exclusion cases alone took
5.7 CPU-hours, the near node 303 s and the root node 892 s. A fresh end-to-end replay is
therefore an overnight job, and it cannot yet start from one command, because the child
capture checkers pin their parent receipts byte for byte, timing fields included
(`think-e2ot`).

1. **Bind states, not receipts.** Have every consumer pin a canonical digest of the
   mathematical content it depends on (the parent’s final state, the certificate bytes)
   and put timings in a sidecar.
   A fresh parent would then rebind automatically, the publisher’s four stale digests
   could not recur, and the composer could run the whole ensemble from one command.
   This is the one change that makes the record re-executable rather than only
   re-readable.
2. **Publish the minimal input closure.** The upstream driver materializes all 2,638 LFS
   payloads, 11.3 GB decoded, before its first stage; the non-field manifest already
   names the 924 objects (2.12 GB) those exclusions need, and the field packets add
   little. A standalone release with that closure, the checkers at pinned revisions and
   one runner (`think-22uw`) is what an outside verifier would download.
3. **One certificate language with few rule kinds.** About forty checker and helper
   modules implement roughly a dozen distinct mathematical rules: cover diameter, mask
   census, strict-core quadratics, Minkowski cuts, universal partner collision, residual
   coverage, hull promotion and compression, initial ownership, charge features, mask
   transfer, the D4 overlay search, branch predicates, pose inclusion and the local dual
   argument. Formalization cost scales with the number of rules, not the number of
   instances. The largest saving is in residual coverage, which has four arrangement
   implementations (reference, fast, indexed and degenerate) and an integer backend:
   replace the arrangement check by a triangulation certificate, in which the producer
   supplies triangles, each tagged with the forbidden region or residual containing it,
   and the checker verifies only vertex-in-halfplane facts and that the triangles tile
   the required domain.
   Section 13 of the original proof already allows this substitution.
4. **Drop the field frame from the data.** Convert every stored center to the physical
   cap frame once, so the proof has two frames (normalized cells and physical) instead
   of three, and the inverse map in pose inclusion loses its division by $B$.
5. **State the local theorem at the quarter-turned construction.** The capture target
   and the local pose are then the same labeled object and the alignment $Q^{-1}$
   disappears. The dual certificates transform by a coordinate permutation; the 22-second
   local check would confirm them.
6. **Give the local rectangle slack.** The radii fit the captured domains to within
   $10^{-11}$, so any change upstream breaks inclusion.
   The local certificates have room: with every radius multiplied by 1.2 the worst dual
   ratio is 0.81, by 1.4 it is 0.95, and the 88 feature margins stay positive through
   1.5, where the ratio reaches 1.015 and the argument fails.
   Inflating the radii by 1.3 costs one 22-second rerun and lets a formal inclusion
   proof use coarse rational bounds for the arctangent.
7. **One angle chart.** Doing the local theorem in $t$ rather than radians would make
   every quantity in the proof rational or algebraic and remove the arctangent bounds;
   it needs the curvature constants rederived in the $t$ chart.
8. **Exclude cases 2175 and 2176 directly**, by a center partition as for case 1383,
   removing the only exclusions that depend on another exclusion set, the halfplane
   support theorem behind them, and the acyclicity obligation.
9. **Trim the certificate grammar to what is used.** In all 46 accepted field packets
   $P\subseteq O$ and the charged thresholds exceed the budget on their own, so the
   transfer rule can drop $P$; 13 of the 59 source field certificates are redundant and
   can be left out of a release.
10. **Retain the first-principles recomputations as controls**, so that the endpoint and
    the local theorem’s arithmetic have a second implementation sharing no code with the
    publisher; the shared-primitive caveat then applies only to the geometry rules.

A formalization is best ordered by rule family: the exact witness and local theorem
first (an algebraic number of degree eight, 128 rational linear systems, Taylor bounds),
then the cover, census and D4 overlay (finite rational geometry), then the charge
certificates, then the generic induction, which is the largest, and last the composition
in section 10 of the original proof, which is a few lines of logic.

## Follow-Ups

1. The ten corrections of section 1.1 and the expository simplifications of section 2.1
   were applied to the article in the commit that carries this section, together with
   definitions of the terms section 3.2 lists, each placed before the term’s first use.
   The paper keeps the general transfer rule, which Figure 7 draws, and states the
   half-turn and the reduced form beside it.
2. The verification level is now stated once, in the paper’s closing section, with the
   note that the linked reviews predate the ladder change.
3. Promote two of the scratchpad recomputations to retained controls under
   `packing/devtools/`: the exact $\mathbb Q(u)$ endpoint and census check, and the
   first-principles local recomputation.
   Each would need the project’s Python floor.
4. Register this review against T-060 in the register if the project counts it as the
   second adversarial review the ladder requires; the human oversight record would still
   be missing.

[math-review]: review-2026-09-30-n11-optimality-explainer.md
[reconciliation]: review-2026-09-30-n11-explainer-proof-reconciliation.md
[intuition]: review-2026-09-30-n11-explainer-intuition.md
[citations]: review-2026-09-30-n11-explainer-citations-and-docs.md
[acceptance]: review-2026-09-29-n11-optimality-census-contract.md#whole-proof-acceptance

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
