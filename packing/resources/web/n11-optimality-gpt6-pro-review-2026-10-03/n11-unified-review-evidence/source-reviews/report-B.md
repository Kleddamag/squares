# Adversarial review of eleven square optimality

*Correctness findings and independently checked simplifications*

**Review date:** 3 October 2026 (UTC)  
**Companion verification archive:** `n11-optimality-review-supplement.zip`

## Contents

- [1 Assessment](#1-assessment)
- [2 Correctness issues and required repairs](#2-correctness-issues-and-required-repairs)
- [3 Checked simplifications](#3-checked-simplifications)
- [4 Clarity and organization](#4-clarity-and-organization)
- [5 Apparent objections that did not survive checking](#5-apparent-objections-that-did-not-survive-checking)
- [6 Recommended revision order](#6-recommended-revision-order)
- [7 Sources and audit supplement](#7-sources-and-audit-supplement)
- [8 Final reproducibility record](#8-final-reproducibility-record)

## 1 Assessment

**I found no counterexample to the claimed optimum and no fatal mathematical error in the audited proof components.** The exact construction, rational cap, center classification, final symmetry argument, field exclusions, local analysis, and endpoint deduction survived substantial independent checking. The most important mathematical exposition issue is a missing quantifier in the angular-row invariant. The implementation establishes the stronger property that the argument needs, so this is a repairable proof-contract omission rather than a demonstrated invalid packing theorem.

There are also confirmed defects in the public verification package: four stale final-state digest bindings, and a fresh-replay interface that depends on historical parent-receipt bytes. These are already acknowledged by the review paper and validation guide. They prevent treating the public distribution as an unchanged, successfully reproduced, one-command proof package. They do not establish that the separately reviewed component executions or the geometric theorem are false. ([S1](#s1-review-paper), [S2](#s2-original-mathematical-proof), [S3](#s3-validation-scope-and-outstanding-fresh-run-work), [S4](#s4-mathematical-acceptance-and-dependency-contract), [S5](#s5-source-bound-digest-discrepancies))

**The largest positive result of this review is a set of concrete, checked simplifications.** The final symmetry bridge can use one simple distance obstruction after a short incidence calculation. The local theorem can use two dyadic radii and six dyadic curvature constants. The 59 supplied field certificates can be reduced to a minimum 44 within that family. The endpoint polynomial can be explained as the closing equation of one specific contact. These reductions are supported by fresh exact calculations; they are not merely suggestions to try later.

My assessment remains bounded by the work actually performed. This review freshly verifies all 1,904 field-excluded cases and one complete nonfield exclusion, plus selected capture geometry, the complete local system, and the final pose inclusion. It does **not** rerun the other 275 nonfield exclusions or the entire capture graph. Rechecking the retained final composer is an evidence-identity and composition check, not a substitute for those executions. The report therefore supports the soundness of the audited mathematics and identifies concrete repairs, without claiming a new complete end-to-end verification of the global theorem.

### Claim and notation

The claimed theorem is $s(11)=T$: eleven independently rotated unit squares fit in a square of side T, and no smaller square suffices. Boundary contact is allowed. Define

$$
P(u)=5u^8-10u^7-2u^6+14u^5+12u^4-6u^3+2u^2+2u-1,
$$

where u is the unique root in $(9/25,37/100)$. Then

$$
T=\frac{6u+4}{1+2u-u^2}
=3.8770835900228141773078970601\ldots.
$$

The rational cap, field scale, and quarter-turn used below are

$$
U=\frac{387708359002281417731}{10^{20}},
\qquad B=\frac{191/50}{U},
\qquad Q(x,y)=(-y,x).
$$

Here $D_4$ denotes the eight symmetries of the square. The field frame rescales a cap of side U to side $191/50$, so the small squares in that frame have side B. ([S1](#s1-review-paper), [S2](#s2-original-mathematical-proof))

### Review target and method

The target is *A Review of the Optimality Proof of the Trump Packing of 11 Squares*, draft v0.1.0, retrieved from the requested URL. Its stated original-proof revision is `f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c` in `Queuingtheorydotcom/11SquaresOptimal`; its principal Squares Project references are pinned to `ea0a3b19a70085683c3b65946cded03ffe4e2415` in `jlevy/squares`. The retrieved paper contains 153,686 bytes, including embedded SVG, with SHA-256 `428da02fd5b99a6133736113e564097e9281aae213076265f968ceefd4bd3d68`. ([S1](#s1-review-paper), [S2](#s2-original-mathematical-proof))

Six parallel reviewers examined complementary obligations. The review combined mathematical reconstruction, direct source inspection, exact component replay, malformed-input controls, and independent implementations. The strongest independent checks did not import the original geometric arithmetic: the witness was rebuilt with rational polynomial arithmetic; the Voronoi overlay was reconstructed by boundary-line intersections; and the simplified local theorem received a second implementation of all elementary values and gradients. Existing source was also replayed to detect disagreement between independently derived mathematics and the supplied implementation.

The included supplement contains the principal new checkers, exact input data for the proposed symmetry and local replacements, finite field-subset evidence, and audit results. It is a supplement to this review, not a standalone replacement for the entire original global proof.

### What was actually checked

| Obligation | Fresh work in this review | Result and limit |
|:--|:--|:--|
| Exact endpoint and construction | Independent rational-field reconstruction; root isolation; side polynomial; 88 unit-edge and orthogonality identities; 176 scalar containment inequalities; 55 pair separations | All pass; 14 touching and 41 strictly separated pairs; both coordinate spans equal T |
| Rational cap | Independent exact comparison of the algebraic endpoint with U | T is strictly below U; the difference is about 2.10294 times 10 to the minus 21 |
| Center cover and final D4 geometry | All 16 cells, all 220 closed overlay regions, all 1,572 distance bans; separate exact geometry implementation | All pass, including eight singleton overlay regions |
| Earlier conditional D4 cuts | Independent necessity calculations for cases 2175 and 2176 | Pass conditional on the stated 1,931-case baseline; baseline geometry is a separate premise |
| Field exclusions | All 59 supplied field certificates; 5,877 ownership checks; 24,373 complete angle rows; exact transfer sets | All pass; exact union of 1,904 field cases |
| One nonfield exclusion | Complete case 2095; five sequential updates and 160 closed angle rows | Pass; this is one of the other 276 cases |
| Capture seed and first update | 130 strict seed points; 69 angle rows; 28 common-kernel vertices and seven compressed points | Pass; selected update, not the complete capture graph |
| Final pose inclusion | 136 live rows and 1,542 vertices; exact role, angle, and frame checks | Pass for the retained extracted near state; its full ancestry remains a separate obligation |
| Published local theorem | 112 features, 24 available and 88 unavailable; 512 raw choices and 128 branch matrices; all 8,448 signed-coordinate inequalities | All pass; published worst ratio about 0.6765052082 |
| Simplified local theorem | Two independent exact implementations; second reconstructs 1,936 elementary functions and gradients | All 8,448 inequalities and 88 feature exclusions pass with the simpler box and constants |
| Retained global composition | Actual source and receipt identities, complete exclusion inventory and capture joins | PASS with no pending obligations and geometry rerun false; no fresh global geometric claim |
| Adversarial controls | Published boundary, child-node, generic and composition tests; additional field and new-checker mutations | Targeted controls pass; successful tests supplement the mathematical review |

The boundary, child-node, and composition suite completed 23 tests; the generic suite completed eight. Additional field checks rejected six targeted invalid inputs and compared 6,000 signed range-tree operations and 12,951 extra-direction inequalities. These are diagnostic observations, not replacements for the proofs of the checker rules. Counts and detailed outputs are retained in the supplement.

## 2 Correctness issues and required repairs

The findings below distinguish a mathematical failure, an incomplete explanation of a valid implementation, and a publication or replay defect. No finding in this section supplies a packing below T or invalidates a freshly checked geometric certificate.

### C1 State the stronger invariant required at angular seams

**Priority: first. Classification: substantive proof-contract omission in both expositions; actual implementation found sound.**

The review paper says that every true pose belongs to an outer cover made of closed angle rows with center regions. Read literally, this guarantees membership in the union of the rows. The original proof gives essentially the same weaker description in section 5. However, `conditional_view` in the independent child-capture checker skips a row intersection when its angular interval has zero length. A union-only cover does not justify that operation. ([S1](#s1-review-paper), section One Geometric Invariant; [S2](#s2-original-mathematical-proof), section 5; [S6](#s6-closed-angular-branch-restriction))

Here is a minimal exact example. Suppose the stored rows are

$$
[0,1/2]\times\{A\},\qquad [1/2,1]\times\{B\},\qquad A\ne B.
$$

A possible pose at angle parameter $t=1/2$ and center A belongs to their union. Restricting to $t\ge1/2$ and discarding the first row's singleton angular intersection leaves only the second row. That loses the pose at A. We exercised the published pure function on this example and obtained exactly that behavior.

This example is **not** an accepted certificate counterexample. The actual seed and transition induction establishes a stronger statement:

$$
\text{For every valid packing and every row }r,
\quad t_i\in I_r\ \Longrightarrow\ p_i\in D_r.
$$

The quantifier is every applicable row, not merely one row in the union. The row intervals also cover the complete allowed angular range. Initial wall envelopes satisfy the statement pointwise. Every new closed interval lies in a specified predecessor interval; necessary cuts preserve each feasible center; uniformly forbidden regions exclude none; exact residual coverage and outward compression preserve the implication. At a seam, the retained adjacent closed row therefore also contains every actual boundary pose. All actual branch ranges have positive length, and the checker refuses an unsupported wholly singleton range. ([S6](#s6-closed-angular-branch-restriction), [S7](#s7-actual-pointwise-induction))

**Repair.** Add this pointwise row invariant to the Pose-preservation lemma and give the short induction just described. Explain that dropping a singleton angular intersection is safe only because an adjacent retained closed row already covers all actual poses at that endpoint. Keep this separate from the rule for spatial points and segments, which must not be discarded merely because they have zero area.

Suggested replacement text:

> For every valid packing under the current assumptions, each closed angle row containing an owner's angle encloses that owner's center. Adjacent rows consequently both enclose every feasible pose at their common endpoint. A singleton intersection created by a closed branch restriction may be omitted only when a retained adjacent row provides that same endpoint guarantee.

### C2 Repair the public bindings and the fresh parent interface

**Priority: first for a reproducible publication. Classification: confirmed, previously documented release defects; not a refutation of the theorem.**

The source graph records four inconsistent final-state digest bindings in the publisher's packet. The paper correctly acknowledges them. The retained graph gives the following prefixes; full identities are in the cited source and the supplement. ([S3](#s3-validation-scope-and-outstanding-fresh-run-work), [S4](#s4-mathematical-acceptance-and-dependency-contract), [S5](#s5-source-bound-digest-discrepancies))

| Leaf | Publisher claim prefix | Actual state prefix |
|:--|:--|:--|
| Far 15 | 3b7f1ea0 | 9e28b092 |
| Far 13 | f83eb23c | 87482985 |
| Far 2 | 7551646f | 11d4a28e |
| Near | 81002706 | a6d45c0c |

For the near leaf, I freshly downloaded the pinned compressed object, verified its 27,653,954 compressed bytes and 185,901,535 decoded bytes against the supplied hashes, parsed the actual final state, and recomputed its canonical digest. It matches `a6d45c0c…`, not the publisher's `81002706…`. This is a fresh check of the input mismatch, not a geometric replay of that node.

A separate issue affects the independent pipeline. Child consumers bind byte-exact historical parent receipts, including runtime information. A fresh parent can establish the same mathematical state while producing different receipt bytes. The existing retained-evidence composer cannot make that new run composable automatically. The validation guide explicitly identifies the need for reviewed state-equivalence and parent rebinding. ([S3](#s3-validation-scope-and-outstanding-fresh-run-work))

**Repair.** Publish a corrected minimal input closure and a fresh runner. Define a canonical mathematical state containing the owner inventory, frame, closed angular rows, center domains, owned hulls, branch assumptions, and relevant source identities. Bind children to that state and to successful checking of the parent, with timing and other observational metadata stored separately. Verify each changed binding against recomputed source data; do not merely disable the checks or substitute a stored success label.

Then run the corrected package from a clean relocated directory with no undeclared local cache. Preserve separate commands for fresh geometric replay and retained-evidence inspection. The paper's late caveat is accurate, but a brief version should also accompany the first theorem statement.

### C3 Supply the field lemma in the original proof and correct its citation

**Priority: first for mathematical completeness of the cited exposition. Classification: omitted explanation and inaccurate citation description; review's actual field argument found sound.**

The review's field footnote describes original `PROOF.md` section 5 as covering field charges and transfer. That section explains the ownership and geometric-exclusion induction, but does not define the median-projection charge, prove its capacity, or state the strict weighted-budget rule. Section 12 mentions the 59 field certificates and mask transfer without supplying this missing mathematical argument. ([S1](#s1-review-paper), field footnote; [S2](#s2-original-mathematical-proof), sections 5 and 12)

The review itself supplies a valid median-projection argument, and the independent mask-0 acceptance analysis explains the rule. All 59 field instances freshly passed here. Thus the issue is not an uncovered defect in these field certificates. It is a significant omission from the original proof exposition and a misleading description of what its cited section contains. ([S8](#s8-field-rules-and-exact-runner))

**Repair.** Add an explicit field-charge lemma to the original proof: definition, capacity bound, whole-angle lower-charge verification, required-owner condition, and strict excess over budget. Correct the footnote to identify the independent field review and checker as the sources of the reconstructed argument. The ten-triangle formulation in section 3 below is a shorter alternative.

### C4 Preserve the conjunction inside each separation feature

**Priority: mathematical precision. Classification: compressed explanation in the review; original section 7 is explicit and correct.**

For each contacting pair, nonoverlap means that at least one of eight separation features holds. A chosen feature holds only when **all four** corner inequalities hold. The review moves quickly from feature counts to branch matrices without stating this logical structure. It is the reason one negative corner disables a feature, and the reason an available feature contributes its necessary tied rows. ([S1](#s1-review-paper), local section; [S2](#s2-original-mathematical-proof), section 7; [S9](#s9-local-isolation-and-exact-residuals))

**Repair.** State the condition directly:

$$
\bigvee_{f=1}^{8}\ \bigwedge_{k=1}^{4} g_{f,k}(h)\ge0.
$$

Explain that branches choose one still-available feature for each contacting pair. Its zero-at-the-witness corner inequalities, together with the tied wall inequalities, form a necessary system. Dropping positive or noncontact constraints weakens that necessary system and cannot remove a feasible packing. This clarification makes the 112-feature census and 512-to-128 reduction inspectable.

### C5 Define ownership over valid packings rather than artificial outer poses

**Priority: mathematical precision in the cited original. Classification: ambiguous wording; the review paper already uses the correct formulation.**

Original section 5 describes an owned hull as lying inside its square in every surviving pose. If that includes every point of the stored outer approximation, the statement is too strong. Outer approximations deliberately retain artificial poses. The invariant needs ownership only in every valid packing satisfying the current assumptions. ([S2](#s2-original-mathematical-proof), section 5; [S7](#s7-actual-pointwise-induction))

This is a real distinction in the retained data. In candidate round 1, owner 2, row 0, at $t=1/64$, seed owned point 6 lies outside an artificial square: its field-frame body coordinate exceeds $B/2$ by approximately 0.00244463, at residual polygon 0, vertex 1. That artificial pose violates the exact wall constraint; the row's wall envelope merely overapproximates it. It is therefore no counterexample to ownership in valid packings.

**Repair.** Use the review's existing valid-packing wording in the original proof. Do not strengthen it to a claim about every artificial outer pose unless the stored domains are also changed and that stronger property is proved.

### C6 Expose the label and coordinate interfaces

**Priority: proof-facing clarity. Classification: checked implementation interface omitted from the article.**

Capture labels are occupied cell owners, ranging as high as 15. Local coordinates use eleven square labels, 0 through 10. The paper does not print the bijection. Number the Appendix A squares in displayed order and provide the following checked map. ([S10](#s10-pose-inclusion-and-role-bijection))

| Local square | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|:--|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Capture owner | 3 | 15 | 8 | 0 | 4 | 1 | 2 | 11 | 9 | 10 | 13 |

State that the local center radii use physical unit-length coordinates and the angular radii use radians. The field frame scales both centers and square side length by B; the half-angle parameter is not a radian angle. These facts are handled correctly by the checker and should be visible beside the bridge formula. The new dyadic box below makes the radius portion of this interface much easier to state.

## 3 Checked simplifications

### S1 Replace the final D4 search by incidence propagation and one distance bound

**Status: implemented, exactly checked, independently reviewed, and included in the supplement.** This is the most useful simplification of the global exposition.

The original final bridge uses 220 overlay regions and 1,572 distance bans in an exhaustive assignment search. The same final conclusion follows from an elementary incidence calculation and one geometric obstruction. The proof still uses the complete closed overlay; its eight singleton regions remain included. ([S11](#s11-center-cover-and-d4-argument))

Write $J_m$ for canonical mask m and H for the half-turn. Suppose no D4 image admits $J_{438}$. Every closed-cell assignment in every view must then be one of the six raw masks

$$
J_{999},\ J_{1462},\ J_{1659},\ H(J_{999}),\ H(J_{1462}),\ H(J_{1659}).
$$

Canonicalize an identity-view assignment. For each of the three possible canonical source masks, there are only $6^3=216$ possible triples of masks in the other three views. Each view assigns eleven different labels to eleven owners, so the assignment is a bijection. Two elementary propagation rules are enough:

1. If an owner has only one possible label in a view, that label is unavailable to other owners.
2. If a target label can belong to only one owner, that owner must take it.

The exact 648-record certificate checks these rules and contradiction terminals. It eliminates 215 of 216 triples for source 999, 215 of 216 for source 1462, and every triple for source 1659. It uses no search branching. The remaining information is small enough to print in the paper:

| Source mask | Sole surviving transformed-mask triple | Consequence |
|:--|:--|:--|
| $J_{999}$ | $(J_{1462},J_{1462},J_{999})$ | Owner 1 lies in $R_{(1,1,11,4)}$ and owner 2 in $R_{(2,5,6,9)}$ |
| $J_{1462}$ | $(J_{999},H(J_{999}),H(J_{1462}))$ | The reflected view has raw mask $J_{999}$ |
| $J_{1659}$ | None | Incidence contradiction |

Here the four entries of a region label correspond to the paper's views $(x,y)$, $(1-x,y)$, $(1-y,x)$, and $(y,x)$. Exact independent halfplane reconstruction gives the simple rational enclosures

$$
R_{(1,1,11,4)}\subset[23/50,27/50]\times[0,11/100],
$$

$$
R_{(2,5,6,9)}\subset[11/25,14/25]\times[23/100,7/25].
$$

Any two points in these respective regions satisfy $|\Delta x|\le1/10$ and $|\Delta y|\le7/25$. Since $U-1<3$, their physical squared distance satisfies

$$
d^2 < 9\left(\frac1{100}+\frac{49}{625}\right)
=\frac{1989}{2500}<1.
$$

They cannot be centers of two interior-disjoint unit squares: each unit square contains a disk of radius 1/2 at its center, and two such disks have overlapping interiors when their center distance is less than one. This excludes source 999. Source 1462 is then excluded by applying the same argument to its reflected view; the hypothesis that every D4 view avoids 438 is preserved by that change of view. Source 1659 was already incidence-impossible. This proves that some D4 image admits case 438.

The resulting mathematical argument has one easy distance estimate. The finite incidence evidence is approximately 97 KB and takes less than a second to check here, including the independent geometry reconstruction. The supplement binds the source cover, overlay, label conventions, cap, and trace bytes. A second reviewer checked the propagation rules, the group-composition step, invalid-index rejection, closed endpoints, and a relocated minimal package.

**Scope.** This replaces the final four-survivor D4 bridge. The earlier baseline-dependent support arguments for cases 2175 and 2176 also consume the larger distance-ban inventory. Their use does not disappear merely because the final bridge has become smaller. Do not delete the other bans from the whole proof package without separately reducing and checking those earlier arguments.

### S2 Use two dyadic radii and six dyadic curvature constants

**Status: complete exact replay in two implementations, including independently reconstructed elementary derivatives.**

Let $r=1/256$. The local rectangle can be replaced by

$$
|\Delta x_i|,|\Delta y_i|\le r\quad(0\le i\le10),
$$

$$
|\Delta\theta_i|\le r\quad(0\le i\le8),\qquad
|\Delta\theta_9|,|\Delta\theta_{10}|\le2r=1/128.
$$

These are physical center coordinates and radian angular displacements. The exceptional angular coordinates in the 33-vector are 29 and 32. By the checked role map they belong to capture owners 10 and 13. Every original radius is at most its proposed replacement, so the existing pose-inclusion result immediately puts the captured near state inside this larger rectangle. A new local isolation check is necessary for the enlarged box; it has now been performed. ([S9](#s9-local-isolation-and-exact-residuals), [S10](#s10-pose-inclusion-and-role-bijection))

The analytic bounds can also be made much simpler. Every needed pair is one of the 14 contacting pairs. At the exact witness, its center distance is at most $\sqrt2$, because a common contact point is within the circumradius $1/\sqrt2$ of each center. In the working box of coordinate radius $1/64$, translations increase the distance by at most $\sqrt2/32$. Therefore

$$
\|c_o-c_p\|\le\frac{33}{32}\sqrt2<\frac{3}{2},
\qquad
\frac94-2\left(\frac{33}{32}\right)^2=\frac{63}{512}>0.
$$

Thus we may choose $D=3/2$ in the Hessian bound. For a direction bounded by the proposed radii, relative center velocity has norm at most $2\sqrt2\,r<3r$. Also $1/\sqrt2<3/4$. If the axis owner's angular radius is $ar$ and its partner's is $br$, where $a,b\in\{1,2\}$, the paper's Hessian bound becomes

$$
K_{\mathrm{pair}}\le r^2\left(\frac{3}{2}a^2+6a+\frac{3}{4}(a+b)^2\right).
$$

A wall gap has $K_{\mathrm{wall}}\le(3/4)a^2r^2$. Thus all required nonlinear estimates use only six dyadic constants:

| Gap type | Angular multipliers | K/r² |
|:--|:--:|--:|
| Pair | $(1,1)$ | $21/2$ |
| Pair | $(1,2)$ | $57/4$ |
| Pair | $(2,1)$ | $99/4$ |
| Pair | $(2,2)$ | $30$ |
| Wall | $1$ | $3/4$ |
| Wall | $2$ | $3$ |

The order of the pair multipliers matters because the first square supplies the rotating axis. The checker still takes the maximum curvature across elementary functions that have the same gradient. Our independent reconstruction found 56 distinct row gradients and 62 matching elementary functions, including six alias groups. All required pair aliases concern the same 14 contact pairs, which validates the uniform D bound.

The existing rational dual vectors pass all 8,448 residual and nonlinear checks with these coarser constants. The exact worst ratio is

$$
c_{\max}=
\frac{237880431895517578125000}
{249999999158632916515561}
=0.9515217307843866\ldots
<\frac{20}{21}<1.
$$

It occurs at branch 105, coordinate 31, sign minus one. Every unavailable-feature inequality also stays strict: the smallest margin is approximately 0.0058975037223, and all 88 margins exceed $1/200$.

This calculation was independently reproduced from a separate rational-field construction, rebuilding all 1,936 elementary values and gradients, the 24/88 feature census, the 512 raw choices, the 128 reduced matrices, and every residual and margin. The portable proposed checker separately verifies its pinned inputs and shared source modules; it does not trust a previous success receipt.

**Recommended presentation.** State this two-radius local lemma in the main text and put the six-entry curvature table in Appendix B. The dual vectors remain machine-readable proof data. The local branch count and the full capture obligation remain necessary. The replacement changes the local theorem's data and proof receipt, so it should be recorded as a newly checked local lemma rather than silently substituted into historical receipts.

### S3 Reduce the supplied field family to a minimum 44 certificates

**Status: all 59 field certificates freshly replayed; subset and minimality verified by exact finite-set checks.**

The 59 supplied field certificates establish a union of 1,904 case IDs. Exactly 43 certificates are individually mandatory within this family: each has a case ID covered by no other certificate in the family. Their union contains 1,903 cases. The only missing case is 1456, which either of two additional certificates covers. Choosing the 167-row `59db0f81…` certificate instead of the 389-row alternative yields a sufficient 44-certificate subset.

This also proves minimality within the supplied family. Any sufficient subset must include all 43 mandatory certificates and at least one certificate for case 1456. A 43-certificate subset cannot suffice. The supplement lists every selected source hash, every exact transfer set, and a unique-case witness for each mandatory certificate. I independently recomputed the unions and uniqueness witnesses.

| Quantity | All 59 supplied certificates | Sufficient 44 |
|:--|--:|--:|
| Field cases excluded | 1,904 | 1,904 |
| Complete angle rows | 24,373 | 17,963 |
| Ownership-point checks | 5,877 | 4,233 |

The independently retained field ensemble already uses only 47 sources. Three of those can be omitted in a new sufficient manifest: `68426a0d…` for mask 1925, `72e06f08…` for mask 246, and `a323908f…` for mask 1802. The original 93-certificate baseline also has a 71-certificate sufficient selection at the inventory level: 44 field certificates plus 27 generic certificates; seven of its generic exclusions are already covered by the field union. This last observation simplifies selection of proof inputs; this review did not freshly replay all 27 of those generic certificates.

The 71 count describes sufficient top-level certificates. Shared ancestors, checker inputs, and downstream source bindings must still be retained or replaced by independently checked equivalents.

**Scope.** Forty-four is a minimum for these fixed 59 certificates and their checked transfers. It is not a lower bound on how many certificates some new mathematical construction might need. Preserve the original historical manifests, and create a separate reduced manifest whose dependencies and exact exclusion union are checked.

### S4 Explain the field charge through ten triangles

**Status: proved mathematical equivalence; proposed alternative checker design, not a replay of all field certificates through a newly implemented triangle algorithm.**

Let P be the five sites and K a nonempty compact convex core. Every projection interval of K contains the median of P if and only if

$$
K\cap\operatorname{conv}(A)\ne\varnothing
\quad\text{for every }A\subset P\text{ with }|A|=3.
$$

There are only ten such subsets. Their convex hulls may be triangles, segments, or points; the statement covers all three cases.

To prove the forward implication, suppose K misses one three-site convex hull. The two compact convex sets are strictly separable, putting all three selected sites beyond one endpoint of K's projection. The median of all five sites is then beyond that endpoint too, a contradiction. Conversely, if a median lies beyond a projection interval, at least three sites lie strictly beyond that same endpoint. Their convex hull misses K.

Capacity one is equally short. Two disjoint compact convex cores have a separating line with a gap. At least three of the five sites lie in one of its two closed halfplanes. Their convex hull misses the core on the other side. Thus both cores cannot intersect all ten three-site hulls. This is the same capacity used by the paper's median-projection charge.

For a translated fixed core $K=x+K_0$, the charged-center region is exactly

$$
\bigcap_{\substack{A\subset P\\|A|=3}}
\left(\operatorname{conv}(A)+(-K_0)\right).
$$

This is a finite convex-polygon construction and gives a structurally different way to check the median feature. It may improve the exposition and supports an alternative implementation to cross-check the current direction-sector code. It makes no claim that the core contains three of the five sites; that interpretation would be incorrect. ([S8](#s8-field-rules-and-exact-runner))

### S5 Derive the endpoint polynomial from one closing contact

**Status: exact identity independently verified before imposing the endpoint polynomial.**

The paper states the degree-eight polynomial in The Result and gives the placement formulas in Appendix A, without explaining their geometric connection. Let P(u) denote the polynomial defined above. Number the squares in Appendix A from zero. Square 2 is the top axis-aligned square $A(x_0,T-1)$, and square 10 is the final tilted square $F(A(\eta+2,-\zeta))$. Their separation gap along $n=(-s,c)$ is

$$
g(u)=-s x_0+cT-2c+\zeta+\rho-1
=\frac{P(u)}{2u(1-u^4)(1+2u-u^2)}.
$$

The denominator is positive on the specified interval. Hence $P(u)=0$ closes this particular contact. Every other zero separating-gap identity checked in this construction holds as a rational-function identity before using $P(u)=0$. The polynomial's role is therefore quite concrete: it closes the remaining contact in a rationally parameterized contact family. ([S2](#s2-original-mathematical-proof), section 2; [S12](#s12-exact-construction))

The paper could explain the construction in that order: contact family, one closing equation, root isolation, then finite containment and separation checks. This does not replace the global proof; it explains why the attaining configuration has this algebraic endpoint.

Root uniqueness also has a short elementary proof. Exact endpoint signs give a root, while termwise bounds throughout $[9/25,37/100]$ yield

$$
P'(u)\ge\frac{10398878171521}{2500000000000}>4.
$$

The cap comparison is very small but rigorous: $U-T=2.1029398990372936\ldots\times10^{-21}>0$. The independent audit certifies it with rational bounds. A displayed decimal is unnecessary for the proof; the strict rational sign is the relevant fact.

### S6 Shorten the endpoint deduction and consider the uniqueness corollary

The rational-cap argument is correct and can be stated in one compact lemma. Start with a packing in a square of side $S\le T$, centered in the cap U. The global reduction, closed capture, and pose-inclusion checks put an appropriate D4 image in the local rectangle. The exact map from field centers is

$$
p_T=Q^{-1}\left(p_f/B-(U/2,U/2)\right)+(T/2,T/2).
$$

After undoing the field coordinate scale, this is an isometry. It maps the side-S container to the concentric side-S subcontainer of $[0,T]^2$, with all small squares still unit squares. Local isolation forces the construction. For $S<T$, its horizontal span T is already impossible. That span follows immediately from the two displayed squares $A(0,0)$ and $A(T-1,0)$; one coordinate span suffices. No compactness or limiting argument is needed. ([S2](#s2-original-mathematical-proof), sections 3, 8–10)

The stated premises also apply when $S=T$. Original section 9F explicitly uses $S\le T$; the capture root has no additional assumptions; and the pose-inclusion calculation does not depend on a strict inequality $S<T$. For a packing initially in $[0,T]^2$, a global symmetry G followed by capture alignment acts as

$$
p\longmapsto (T/2,T/2)+Q^{-1}G\bigl(p-(T/2,T/2)\bigr).
$$

Because $Q^{-1}G\in D_4$, those premises imply uniqueness of optimal packings up to the eight container symmetries and square relabeling. The paper's decision not to claim global uniqueness is not an error. It is an available corollary that deserves explicit consideration and its own statement of scope. Its evidential basis is exactly the same complete global ensemble as the optimum theorem, not an additional full replay by this review.

## 4 Clarity and organization

The review is careful about strictness, closed boundaries, source identity, and the limits of computation. Those strengths should be preserved. The suggested changes below would make its main argument easier to follow without weakening its verification claims.

### Lead with five mathematical lemmas

The main text can follow this order:

1. **Attainment.** The exact construction is feasible at T, and the final contact explains P(u).
2. **Global exclusion.** The closed center cover is exhaustive; pointwise pose preservation and field capacity justify the exact excluded set.
3. **Symmetry.** The short incidence table and one distance bound force a view with case 438.
4. **Capture.** A complete closed partition sends every surviving case-438 packing into the stated local rectangle after the exact role and frame conversion.
5. **Local isolation.** The dyadic rectangle, feature coverage, and strict dual-curvature inequalities admit only the construction at fixed T.

The smaller-container contradiction is then one paragraph. The large certificate manifests, code provenance, execution history, and ratings belong in a verification appendix, with a concise scope statement beside the theorem. This structure separates the general mathematical rules from the finite data that instantiate them.

### Concrete edits to the article

| Location | Recommended edit | Reason |
|:--|:--|:--|
| First theorem | Add two sentences distinguishing observed component executions, retained-evidence composition, and the outstanding portable fresh runner | Readers should know the exact evidential claim before reaching the final section |
| Historical introduction | Shorten the lower-bound lineage and move tool-specific comparisons to notes | Those bounds motivate the method but are not premises of the equality |
| Center-cover lemma | State that every realized closed-cell assignment in every D4 view must survive the exclusions | Makes independent choices at boundary ties visibly legitimate |
| Pose-preservation lemma | Add the quantified pointwise row invariant and seam rule from C1 | Matches the condition used by the branch checker |
| Field section | Give the missing original lemma and consider the ten-triangle description | Makes capacity and the finite charge region easier to audit |
| Symmetry section and Figure 8 | Show the forced regions from source 999 and their simple enclosing rectangles | The illustration then carries the actual simplified final obstruction |
| Capture section | Keep the four closed mathematical branches separate from the ten-node execution graph | Branch coverage and state ancestry are different obligations |
| Local section | State all four corner inequalities per feature; print the two-radius box | Makes the branch and neighborhood statements concrete |
| Appendix B | Use the six dyadic constants, while retaining maximum-over-aliases and the 88 negative-feature checks | Removes unnecessary pair-specific square roots without dropping a premise |
| Endpoint section | Print the label map and use centered physical coordinates as the main frame | Reduces conversions and prevents owner-index and angle-unit confusion |
| Sources and status | Explain that some linked reviews retain an older rating scale | Prevents readers from mistaking historical labels for conflicting mathematical conclusions |

The last item is a real navigation problem. The paper and validation guide use S5/V3/C3, while linked historical acceptance records use V4/C5. The repository's epistemic policy explicitly explains the scale migration. A short footnote should translate the old labels instead of requiring readers to discover that history. This is not contradictory proof evidence. ([S3](#s3-validation-scope-and-outstanding-fresh-run-work), [S4](#s4-mathematical-acceptance-and-dependency-contract), [S13](#s13-verification-ratings))

The captions and SVG structure were reviewed for mathematical scope, labels, and correspondence with the argument. This work was not a browser-based typography or stylesheet-layout audit of the published webpage. The strongest figure change is conceptual: replace the generic distance-ban illustration with the two regions that actually suffice for the new final D4 proof.

### Make the verification modes operationally clear

The reader needs three separately named operations:

| Operation | What it establishes | What it must not be taken to establish |
|:--|:--|:--|
| Input integrity | Exact source, payload and manifest identities | The truth of geometric assertions inside those files |
| Retained-evidence composition | Coverage of obligations and correct joins among previously reviewed executions | A fresh execution of those geometric checks |
| Fresh proof replay | Actual geometric and algebraic checking of every required instance, followed by composition | Independent formal verification of the mathematical soundness of the checker rules |

The paper already makes these distinctions, but the documentation still intermixes portable checker modules with historical launch scripts. For example, the retained local replay script names an author's mounted scratch path and a Homebrew timeout executable. The checker itself ran successfully here. Supply a machine-independent command that accepts explicit input and output directories, while retaining the historical script as a record of that earlier run. ([S14](#s14-publication-and-replay-interfaces))

For the field layer, separate the foundational cover-geometry receipt from the final D4-reduction receipt. The field runner currently obtains the cover through a pinned conditional D4 receipt. That is not a logical cycle: the geometric cover computation is valid without the exclusion union. A separately named cover receipt would make this independence immediately apparent. ([S8](#s8-field-rules-and-exact-runner), [S11](#s11-center-cover-and-d4-argument))

## 5 Apparent objections that did not survive checking

A systematic adversarial review should record which plausible objections were resolved, so they do not reappear as unsupported claims of a gap.

**Using U greater than T does not leave a numerical gap.** The proof never needs to show that no packing exists at U. The same hypothetical side-S packing is embedded in U for global classification and then rigidly mapped into the T container for the local theorem. The small difference between U and T is included exactly. The local theorem applies only after the smaller container is known to fit in the fixed T frame.

**The field scale does not shrink only the container.** Multiplication by B scales both the container and every small square. Dividing by B restores unit squares before the local argument. L equal to 191/50 is a coordinate scale here, not the asserted optimum for eleven unit squares.

**Boundary ties do not require a symmetry-compatible convention.** Every realized closed assignment is subject to the exclusions. Containing labels may be chosen independently in the four views. Each genuine center therefore yields an included closed overlay region; a deterministic tie-break commuting with D4 is unnecessary.

**Strict Minkowski exclusion is valid even on its boundary.** The common point belongs to two strict inner sets, hence to both square interiors. Contact of the forbidden-center boundary does not correspond to legal square-boundary contact. This would fail without strict inner containment, which the actual core checks enforce.

**An area calculation alone would be insufficient, but the reviewed checks do more.** Lower-dimensional spatial domains have exact point/segment coverage checks. In a full-dimensional closed polygon, dense interior coverage by a finite union of closed covering regions can also establish its boundary by closure. The actual implementation and its continuum-scope explanation use that distinction. ([S15](#s15-continuous-and-lower-dimensional-scope))

**The universal partner-collision support uses a minimum in the correct direction.** The region must force collision for every possible partner pose. Intersecting the collision regions over the partner's center domain produces a minimum support bound. Replacing it with a maximum would reverse the intended quantifier.

**Linear rigidity alone is not being substituted for finite isolation.** The proof controls curvature, eliminates all 88 unavailable features throughout the box, and applies signed-coordinate duals to an arbitrary nonzero finite displacement. The saturated-coordinate argument excludes the boundary of the local rectangle as well as its interior.

**There is no assumed common orientation or hidden contact graph for the hypothetical packing.** The global intervals allow independent angles. Locally, the complete feature census and negative-feature bounds force a checked branch. Omitting noncontact-pair inequalities weakens the necessary system and cannot incorrectly exclude a feasible perturbation.

**Earlier conditional D4 cuts are not justified by the final conclusion.** The necessity checks for cases 2175 and 2176 depend on the original 1,931-case baseline. We independently checked their finite geometric implications conditional on that baseline. The final four-survivor theorem is not used to establish its own exclusion premise.

**Historical lower bounds are not numerical assumptions in the equality proof.** The exact global argument stands on its own listed obligations. As a useful additional check, the standalone historical T-025 verifier freshly passed all 181 directions here: 584 point atoms, 320 threshold atoms, minimum charge $100000203/100000000>1$, and budget $685457679/62500000<11$. The separate 1,441-direction T-026 certificate and Kleddamag's complete lower-bound package were not freshly replayed in this review. Their historical role should remain distinct from the required input closure of T-060.

## 6 Recommended revision order

**First, repair the proof contract.** Add the pointwise angular-row invariant, make the feature conjunction explicit, align the ownership wording with valid packings, and print the role map. Import the field-capacity and strict-budget lemma into the original proof and fix the review's field citation.

**Second, repair publication reproducibility.** Correct the four source-bound final-state digests; define deterministic mathematical parent states; supply the minimal declared dependency closure and a clean fresh runner. Recheck each correction against exact source states and perform a relocated full replay. Keep the retained-evidence composer available with an unambiguous name and scope.

**Third, adopt the checked simplifications as new proof components.** The one-pair final D4 bridge and the two-radius, six-constant local theorem are ready for integration as separately identified checkers and receipts. The minimum 44-field selection is ready for a reduced manifest, subject to the same dependency and exact-union checks. Explain the contact equation behind P(u). The ten-triangle characterization is ready as a mathematical lemma; an alternative production checker still needs implementation and replay if that route is chosen.

**Fourth, tighten the article around the five-lemma structure.** Keep a short verification-scope notice at the front, reduce operational chronology in the main argument, make figures carry the actual simplified geometry, and translate historical status labels in a footnote. Decide explicitly whether to state the uniqueness corollary supported by the accepted scope $S\le T$.

The result of this review is a strengthened basis for assessing the computer-assisted proof, together with concrete smaller replacements for substantial parts of it. Acceptance of the whole equality should continue to refer to the actual complete geometric execution ensemble and its mathematical soundness review. The fresh work in this report is extensive and explicitly scoped; it does not silently promote unexecuted components to independently replayed ones.

## 7 Sources and audit supplement

References to the review paper use section titles, because its embedded SVG makes raw Markdown line counts poor reading locators. Source-code findings additionally name the relevant functions in the report. Every repository link below uses the reviewed commit where applicable.

### S1 Review paper

[A Review of the Optimality Proof of the Trump Packing of 11 Squares](https://jlevy.github.io/squares/papers/n11-optimality-review.md). Retrieved snapshot identity is given in section 1.

### S2 Original mathematical proof

[PROOF.md at the reviewed original revision](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/PROOF.md).

### S3 Validation scope and outstanding fresh-run work

[T-060 validation guide](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/VALIDATION.md).

### S4 Mathematical acceptance and dependency contract

[Census and capture ancestry review](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md), especially Whole-Proof Acceptance, Final Composition Interface, and the complete-execution sections.

### S5 Source-bound digest discrepancies

[Actual source graph](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/source-graph/result.json) and [retained binding refusal](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/capture-ancestry/refusal-result.json). The supplement adds the fresh near-input digest check.

### S6 Closed angular branch restriction

[Child-node checker](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_capture_child_node.py), `angle_domain` and `conditional_view`; [boundary controls](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/tests/test_n11_capture_child_node.py).

### S7 Actual pointwise induction

[Capture root pilot](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_capture_root_pilot.py), [root continuation](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_capture_root_continue.py), and [root-node checker](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_capture_root_node.py).

### S8 Field rules and exact runner

[Mask-0 mathematical consumer](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_optimality_field_mask0.py) and [general field runner](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_optimality_field_runner.py). The capacity review is in S4 under First Independent Field Exclusion.

### S9 Local isolation and exact residuals

[Local isolation checker](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_optimality_local_isolation.py), [dual checker](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_optimality_local_dual.py), and [accepted local result](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/local-isolation/result.json).

### S10 Pose inclusion and role bijection

[Pose-inclusion checker](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_optimality_pose_inclusion.py) and [accepted inclusion result](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/result.json).

### S11 Center cover and D4 argument

[Independent D4 checker](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_optimality_d4.py), [accepted D4 result](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json), and original proof section 6. The new incidence certificate and independent geometry are in the supplement.

### S12 Exact construction

[Placement formulas](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/cases/trump11/packing.py) and [exact witness verifier](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/cases/trump11/verify_exact.py). The independent witness and closing-contact calculation are in the supplement.

### S13 Verification ratings

[Epistemic policy and historical scale migration](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/epistemics.md).

### S14 Publication and replay interfaces

[Original reproduction guide](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/docs/REPRODUCING.md), [publication scope](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/docs/PUBLICATION.md), and [retained local replay script](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/local-isolation/replay.sh).

### S15 Continuous and lower-dimensional scope

[Original continuum-scope review](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/src/evidence/docs/V9_CONTINUUM_SCOPE_REVIEW.md) and [independent point and segment cover checker](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_closed_degenerate_cover.py).

### S16 Final retained-evidence composition

[Composer](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_final_composition.py) and [accepted final composition](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/final-composition.json). This review's fresh composer output has the same accepted scope, with geometry rerun false.

### Supplement contents and limits

The accompanying archive supplies read-only consumption of the new D4 incidence trace, exact reconstruction of its cover and overlay, the two-radius local checker with its required source and data closure, the separately implemented local cross-check, independent endpoint and witness checks, the exact 44-field selection and minimality check, and the principal recorded audit results. Its README gives commands, dependencies, source pins, and a clear scope boundary.

The auxiliary D4 checker underwent its own adversarial review. A missing terminal-view range check in its first draft was found, corrected, and retested before packaging. The authentic incidence traces already used valid indices, so the correction did not change the mathematical survivor table. The delivered version rejects the original malformed-view example, source mutations, missing or duplicated cases, and optimized Python. This was a corrected defect in a newly written review helper, not a defect in the published proof.

Every proposed reduction should enter the project through a new, explicit source-and-result identity. The historical execution evidence should retain its original bytes. Integration should check the same complete exclusion sets, branch assumptions, pose roles, angle units, and exact endpoint as the original argument.

## 8 Final reproducibility record

The complete review supplement was tested after assembly from a relocated directory whose path contained spaces, with the working directory set to `/tmp`. The run used the supplied inputs and installed third-party dependencies, without relying on the original workspace's proof inputs. All eleven stages passed. This final execution record supplements the component-level audit described above.

### Full component run

| Stage | Entry point | Result |
|:--|:--|:--|
| Endpoint and rational cap | `independent_endpoint_check.py` | PASS |
| Short rational cap certificate | `independent_cap_short_certificate.py` | PASS |
| Parameter-polynomial irreducibility | `independent_irreducibility.py` | PASS |
| Side-polynomial irreducibility | `independent_side_irreducibility.py` | PASS |
| Exact attaining witness | `independent_exact_witness.py` | PASS |
| Symbolic closing contact | `independent_witness_simplify.py` | PASS |
| Read-only D4 incidence verification | `verify_d4_review.py` | PASS |
| Independent D4 geometry | `d4_independent_geometry.py` | PASS |
| Simplified local theorem, first implementation | `local-isolation-audit/verify_simplified_local.py` | PASS |
| Simplified local theorem, second implementation | `second_review_simplified_local.py` | PASS |
| Field subset and minimum of 44 | `verify_field_subset.py` | PASS |

The final status was `PASS_REVIEW_SUPPLEMENT_COMPONENTS`. Total recorded elapsed time was **29.269 seconds**. Both local implementations freshly checked all 8,448 signed-coordinate inequalities and all 88 unavailable features; their radii and exact worst ratios agreed. All 118 immutable input identities passed before and after execution, and the supplied D4 trace was unchanged.

The final package also passed ZIP CRC checking and comparison of every archived file with the assembled bundle. Python `-O` and `-OO` were rejected. An altered source file was rejected, and restored source bytes passed.

The successful component run has the following explicit scope:

```json
{
  "status": "PASS_REVIEW_SUPPLEMENT_COMPONENTS",
  "whole_global_proof_replayed": false,
  "field_geometry_rerun": false,
  "d4_trace_regenerated": false
}
```

All 59 field certificates had been geometrically replayed during the review. In this compact supplement, the field stage consumes those 59 recorded fresh results and checks their transfer sets, the 1,904-case union, and the 44-certificate selection and minimality argument. The final supplement run does not repeat the field geometry or the complete global exclusions and capture graph.

### Commands and tested dependencies

The relocated run used Python 3.12.14 and these package versions:

```text
numpy==2.3.5
scipy==1.17.0
sympy==1.14.0
mpmath==1.3.0
```

The two local implementations require these dependencies; the other component entry points use the Python standard library. Verification makes no network requests.

After extracting `n11-optimality-review-supplement.zip`, run from the extracted supplement directory:

```bash
python3 -m venv ../n11-review-env
../n11-review-env/bin/python -m pip install -r requirements.txt
../n11-review-env/bin/python -B verify_review.py
```

Use the corresponding interpreter path on your operating system. Keep the virtual environment outside the supplement directory. The driver resolves its own location, writes new outputs under `fresh-results/`, and leaves the recorded evidence separate. For input integrity checking alone:

```bash
../n11-review-env/bin/python -B verify_review.py --hashes-only
```

That command performs no mathematical replay.

### Archive and snapshot identities

| Item | Value |
|:--|:--|
| Companion archive | `n11-optimality-review-supplement.zip` |
| Archive bytes | 5,879,321 |
| Archived files | 144 |
| Uncompressed bytes | 41,223,316 |
| Immutable files covered by the source manifest | 118 |
| Archive SHA-256 | `4f9065c61fa188b74d124912f4213677492b21330e3753c89d34214395bb7536` |
| Source-manifest SHA-256 | `be0e69e6b03832be13fa0b03af9b45063e096917e6c1c665cff3447561be4965` |

The archive includes the exact reviewed paper as `reviewed-paper.md`: 153,686 bytes, with SHA-256 `428da02fd5b99a6133736113e564097e9281aae213076265f968ceefd4bd3d68`. Its original URL and provenance are recorded in the source manifest. The final successful component run is tied to the final manifest, including that snapshot.
