# Adversarial review of the tentative optimality proof for eleven squares

**Review date:** October 2, 2026 (America/Los_Angeles).  
**Subject:** *A Review of the Optimality Proof of the Trump Packing of 11 Squares*, draft v0.1.0, last revised October 1, 2026. [S1]  
**Priorities:** correctness; proof simplification; clarity.  
**Disposition:** no fatal mathematical error identified; substantial independent confirmation of the witness and focused local-isolation theorem; no fresh end-to-end global certificate replay in this audit.

## Executive assessment

The central argument survives the mathematical attacks I could substantiate. In particular, the rational-cap/exact-endpoint transition is valid; local isolation is genuinely nonlinear rather than merely infinitesimal; boundary contacts are not automatically discarded; and the symmetry reduction need not assume that the irregular cell cover is invariant under every container symmetry.

The strongest positive result of this review is computational and independent of the project's geometric implementation. I reconstructed the exact witness, derived its elementary gap functions and gradients, enumerated its possible local separating features, and generated **8,448 new rational dual certificates**. All were accepted by exact arithmetic. I also verified that all 88 initially unavailable contact features remain unavailable throughout the stated coordinate rectangle. This establishes a replacement computational proof of the **conditional fixed-T local theorem** on the published radii—not just agreement with a retained PASS flag.

The principal adverse findings concern the proof's executable delivery and trust boundaries. A historical interval predicate has a genuine singleton error, already documented by the project. Its positive-area contract prevents that error from becoming a false full-cover acceptance, and the inspected capture path handles degenerate domains separately. The publisher's stale digest bindings and the independent chain's byte-sensitive parent-receipt admissions remain reproducibility problems. Neither is, by itself, a counterexample to the mathematical theorem. [S5, S13, S4]

**Do not read this report as complete independent verification of global optimality.** I did not acquire and execute the entire global exclusion and capture corpus. Source inspection and a sound abstract inference are not substitutes for that execution.

## 1. Scope, evidence, and independence

### 1.1 What was examined

I followed the review article into the pinned original proof, the focused local note, the witness construction, the geometric coverage and collision kernels, the D4 consumer, the local and pose-inclusion consumers, the completion/composition code, and the review and reproduction records. References below identify the specific files and functions rather than relying on mutable web line numbers.

The upstream proof revision is `f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c`, with recorded tree `3fed944c5a0c1dda5e61cb9f45f0dd3d4dc6360c`. The jlevy review-side files were read from `main` as available during the audit; I did not establish an immutable commit for that entire checkout. This distinction matters for reproducing this review. [S4]

The requested `.md` endpoint was rejected by the browsing transport because of its `text/markdown` content type. I read the corresponding rendered HTML article and its repository template instead. Template placeholders were not treated as defects in the published article.

### 1.2 What actually ran

The accompanying bundle contains newly written programs and exact results. They import **no repository modules**, no publisher derivative matrices, and no publisher dual weights. The coordinate formulas and the 33 rational radii are mathematical inputs transcribed from the cited sources. [S7, S17]

The arithmetic implementation uses rational polynomial representatives in the degree-eight field, a separately checked isolating interval, and rational enclosures. SymPy supplies polynomial irreducibility, root counting, and inverses; SciPy/HiGHS only proposes nonnegative dual weights. Acceptance of the proposed weights uses integer and Fraction arithmetic. Floating-point solver status is never sufficient for acceptance.

No callable subagent service was available in this session. These are multiple computational and mathematical checks by one reviewing assistant, not independent model reviews. Likewise, the second certificate replay is a separate execution of the same new checker, not another independent checker implementation.

### 1.3 What did not run

The following remain outside this audit's fresh computational validation: exact reconstruction of all sixteen cover cells from the bound input object; the full global exclusion inventory with every underlying geometric execution; the complete D4 overlay/search on its source objects; every capture update; and the final captured-pose inclusion on all source vertices and angular rows.

I reviewed the relevant rules and substantial consumer source, but did not execute the large global object-backed corpus. Compressed binary/LFS objects could not be acquired into the execution environment through the available route. The distinction is an audit limitation, not evidence that the public data do not exist.

The earlier threshold and lower-bound papers are historical antecedents, not additional lower-bound premises needed by the stated final implication. Their entire certificate corpora were not re-audited here. The present local theorem was checked directly instead of trusting its ancestry. [S3, S6]

## 2. Independently computed results

### 2.1 Exact witness and elementary combinatorics

The independent reconstruction establishes all of the following:

| Obligation | New computation |
|---|---|
| Algebraic parameter | Irreducible degree-eight defining polynomial; exactly one root in the prescribed rational interval |
| Unit-square geometry | Eleven unit squares; orthogonal unit edge vectors and parallelogram identities |
| Containment | All 44 vertices; all 176 coordinate-wall inequalities |
| Non-overlap | All 55 unordered square pairs, with exact weak separating-axis tests |
| Endpoint facts | Exact opposite-wall span in both coordinates; exact strict inequality T < U |
| Contacts | Fourteen contacting pairs |
| Local elementary functions | 1,936 wall/corner and ordered pair/corner gap functions |
| Contact features | 112 total; 24 available and 88 unavailable at the witness |
| Local alternatives | 512 raw selections; 128 distinct systems, each with 42 rows |
| Elementary mask census | 4,368 eleven-element masks; no half-turn-fixed mask; 2,184 representatives |

The last line verifies the combinatorics of the stated label involution. It does **not** verify that the actual geometric cover has the required diameters or involution; those are separate input-backed geometric obligations.

The resulting endpoint is

\[
T=3.87708359002281417730789706010096270637645566846\ldots,
\]

and the rational cap exceeds it by approximately

\[
U-T=2.1029398990372936235443315368374\times10^{-21}.
\]

These decimal displays are explanatory only. The corresponding sign test was exact.

### 2.2 A new proof of focused local isolation

I derived the gradients directly from rotated corners and moving separating axes. The computation does not accept a supplied tangent matrix as ground truth. Equal derivative rows are identified exactly. Whenever distinct elementary functions share a derivative row, I use the maximum applicable curvature bound, avoiding an unsafe identification of nonlinear functions merely because their first derivatives agree.

For every unavailable feature, at least one corner satisfies an exact negative Taylor upper bound throughout the full rectangle. The least favorable such upper bound in this reconstruction is approximately **−0.012636021136276269**. Thus none of the 88 discarded separating features can activate there.

For each of 128 branches and each of 66 signed coordinate directions, I generated a fresh nonnegative rational weight vector. The maximum exact isolation ratio is

\[
\frac{24251087101573907634681435939000000000}
{35849803998164131953538679451950587687}
\approx 0.6764635896702756<1.
\]

This comfortably passes the strict inequality. The maximum residual enclosure is approximately `1.3216954749443503e-11`; its effect is included, not ignored. A full verify-only pass subsequently recomputed the acceptance conditions without solving any linear program.

The conditional conclusion is precise: **the published rational rectangle contains no distinct feasible labeled packing in the fixed side-T container**. This does not prove that every global packing enters that rectangle. The radii's suitability for capture is a separate geometric assertion.

### 2.3 Adverse controls

Seven deliberately damaged versions of the new local certificate were refused: missing certificate, duplicated certificate, negative weight, zeroed dual, changed radius, changed matrix scale, and changed curvature scale. These controls test the new implementation, not the repository's checkers.

A separate exact interval test exhausted **12,180** one- and two-region inputs on a rational grid. The corrected interval rule agreed with an independent endpoint/midpoint oracle in every case. The modeled historical rule falsely accepted 616 singleton cases and had no errors on nondegenerate target intervals in this finite test. Additional controls retained a closed seam and rejected a strictly positive gap of size `10^-50`.

Finite tests do not prove the general coverage theorem. They reproduce the defect and check the intended boundary semantics; the general non-impact argument appears next.

## 3. First priority: correctness and verification findings

### C1. Genuine historical singleton-predicate error; restricted impact

**Classification:** confirmed, already known; implementation defect and contract hazard, not an established failure of the optimality proof.

**Location:** `check_n11_optimality_field_mask0.py`, `covers_vertical`; corrected handling in `n11_fast_exact_cover.py`; degenerate handling in `check_n11_closed_degenerate_cover.py`. [S9–S11]

Consider target interval `[1,1]` and one alleged covering interval `[0,0]`. The old recurrence initializes its cursor at the target's lower endpoint. An interval wholly below that cursor does not move it; the test that the cursor has reached the target's upper endpoint nevertheless succeeds. The claimed coverage is false.

This can also occur as one endpoint slice of a positive-area triangular domain. It is therefore insufficient to say that positive-area input makes every call to the interval predicate individually correct.

However, **the complete positive-area convex-domain coverage test has a separate protection**. Every vertical slice at an abscissa strictly inside the domain's horizontal projection has positive height. On those slices, the old recurrence does not have the singleton false-accept mechanism. The complete arrangement sweep certifies the interior slices. A finite union of closed covering regions contains their limits, and those limits include the boundary of the convex domain. Consequently, this particular bug does not yield a false whole-domain acceptance under that full contract.

The project's review gives this density argument. I agree with it. The inspected capture transition explicitly dispatches zero-area legal domains to the separate point/segment verifier. [S5, S13]

**Required repair:** retain the frozen historical implementation only as historical evidence; use the corrected predicate in a consolidated release. Make the positive-area/convexity contract explicit, audit all call sites and historical variants, and keep direct singleton and tiny-gap regression tests. Do not silently broaden the old kernel to arbitrary closed domains.

**Limit:** I have not exhaustively checked every historical call site. The defended conclusion is the contract argument and the inspected dispatch—not a blanket certification of every use of that kernel.

### C2. The publisher's unchanged runner is not a clean successful reproduction target

**Classification:** high-priority release/reproducibility defect, already disclosed; not a new geometric counterexample.

The review reports four stale final-state digest bindings in the publisher's packet. Its accepted alternative is a chain of independently observed component executions with checked state joins, not a successful run of the unchanged publisher driver. [S2, “What Was Verified”]

A proof can remain mathematically correct despite obsolete metadata. Nevertheless, the public proof package should not leave readers to discover which literal proof identity fails and which replacement chain is authoritative.

**Required repair:** publish a new immutable release, an explicit old-to-new binding report, and a fresh execution transcript. Each replacement must verify the mathematical state and its provenance; changing a hash because a file says PASS is not an acceptable repair.

**Acceptance test:** a clean checkout plus verified input acquisition executes the advertised public proof command without hand editing digests and reports which geometry was actually rerun.

### C3. Parent receipts couple mathematical admissibility to incidental bytes

**Classification:** high-priority reproducibility/design defect, already disclosed.

Some child consumers admit a byte-exact retained parent result, including timing fields. A fresh execution with an identical mathematical state can therefore be inadmissible. The packet acknowledges that an automatic, reviewed rebinding route remains unfinished. [S4, S22]

The distinction to preserve is:

- a **semantic state identity**: assumptions, coordinate frame, owner roles, intervals, domains, owned hulls, and applicable proof rule;
- an **execution receipt identity**: timings, machine details, logs, and the exact file encoding of one run.

These serve different purposes. A child inference should not depend on an earlier machine reproducing the same timing bytes. Conversely, equality of a small final-state hash must not bypass verification of the transition that established that state.

**Required repair:** deterministic semantic serialization plus a checked admission rule for freshly verified parents. Retain execution hashes as provenance. Explicitly bind rule/checker versions and all hypotheses; do not implement an unqualified “same geometry means acceptable” exception.

**Acceptance test:** two fresh parent executions with different timings can both feed a child after semantic verification; a changed domain, angle endpoint, owner map, scale, or inherited condition is refused.

### C4. The final composer must not be mistaken for a geometry verifier

**Classification:** assurance boundary; the source discloses it. Not a newly found false inference in the composer.

The completion and final-composition programs validate inventories, retained evidence identities, and joins. They do not reproduce all primitive geometric calculations. [S18–S20]

Their successful output is useful, but cannot alone establish that all claimed component executions occurred or that every imported geometric rule is sound. This matters especially when a top-level field has a name such as `global_optimality_proved`.

**Recommended change:** make the output scope unmistakable: “retained proof composition validated” and a separate `fresh_geometry_replayed` field. A full-replay command should derive its top-level result from executions performed or validly resumed under a documented model, not merely from the existence of old JSON files.

**This review's limitation:** I did not perform that full replay. The fact that no mathematical flaw emerged during source review is not a substitute for it.

### C5. Shared geometric primitives limit independence

**Classification:** residual common-mode risk, not evidence of a particular wrong answer.

The project local consumer explicitly shares the construction/derivative source. Other consumers share clipping, coverage, and collision primitives. [S14, S12, S13]

Agreement among consumers can therefore reproduce the same underlying error. The new computation in this bundle directly reduces the local construction/derivative/dual part of that risk. It does not reduce all global geometry risk.

**Recommended next correctness investment:** a small second implementation of the global closed-set geometry and state-transition kernel, followed by object-backed replay. Prioritize degeneracies, quantifier coverage, and conditional ancestry over another wrapper around the same routines. A formal proof assistant is one possible later target, not a prerequisite for a valid computer-assisted proof.

### C6. Suspected gaps that did not survive review

These are important because an adversarial report should not promote plausible-sounding objections into defects.

**Rational cap versus exact T.** Undoing the field scale restores unit physical squares; the remaining map is rigid. A packing from a smaller centered container becomes feasible in the fixed-T container. There is no illicit shrinking of the small squares. Section 4 gives the deduction explicitly.

**Closed forbidden boundaries.** If both the universal row core and an owned hull are strictly inside their respective physical squares, even a shared point on their own boundaries lies in both square interiors. A closed Minkowski-difference exclusion is then justified. Replacing “strictly inside” by ordinary containment would be unsound, but that is not the reviewed rule. [S9, S12]

**Universal partner collisions.** The relevant quantifier is all live partner rows, not one favorable partner pose. The inspected primitive enforces nonempty partner coverage and tests every supplied partner row. Complete partner-cover inheritance remains a separate obligation of its caller. [S13]

**Cell ties and D4.** The correct reduction uses simultaneous closed-cell overlays and an overinclusive assignment search. It does not need arbitrary rotations to permute the original cell polygons. Infeasibility of that overapproximation is sufficient. I found no flaw in this logical reduction or the inspected solver pruning, but did not rerun the object-backed search. [S8]

**Local contact switching.** The new enumeration and negative-feature bounds account for it. A proof using only the witness's apparent contact graph without those checks would be incomplete; that is not what the reconstructed proof does.

**Equal gradients with unequal curvature.** Taking the largest relevant second-derivative bound makes the derivative-system identification safe. Both the inspected consumer and the new checker do so. [S14]

**Conditional symmetry exclusions.** The dependency admitting cases 2175 and 2176 must be the earlier baseline, not the later conclusion they help establish. The inspected completion inventory explicitly treats those premises separately; I did not find the proposed circularity. This is a source/dependency review finding, not an independent replay of those cases. [S18]

## 4. The endpoint deduction, checked independently

Here is the exact composition argument without any limiting process.

Let a hypothetical packing fit in side S < T. Place its entire container concentrically in the rational cap U. Apply the container symmetry selected by the global reduction, which preserves concentric containment. If the global exclusion and capture certificates are valid, its poses enter the captured rectangle after the declared alignment and label assignment.

If field coordinates are used, undo their scale first. Writing the aligning quarter-turn as Q, the physical-to-local transformation is

\[
p_T=Q^{-1}(p_f/B-(U/2,U/2))+(T/2,T/2).
\]

The side-S container becomes

\[
[(T-S)/2,(T+S)/2]^2\subset[0,T]^2.
\]

No small-square edge length changes. The pose-inclusion claim now places a genuine fixed-T feasible packing inside the local rectangle. The new local computation forces it to equal the witness. But the witness has exact horizontal and vertical span T, independently verified here, and cannot fit in side S. Contradiction.

The map and angle conversion in the inspected inclusion consumer agree with this interpretation. In particular, its center comparison is in a consistently centered physical frame; its rational half-angle endpoints are bounded as radian displacements, including the axis-orientation seam. [S16, S20]

**Critical qualification:** an arbitrary packing in U need not become feasible in T under this rigid map. Feasibility in T follows here from S ≤ T. Confusing these two statements would create a false proof, but the actual smaller-container argument does not require that confusion.

## 5. Second priority: simplifications

### S1. Extract one abstract anisotropic isolation lemma

The local calculation can be presented and verified using a single weighted residual instead of a separate unweighted error bound and a largest-radius bound.

For a branch, suppose its necessary tied constraints satisfy

\[
A_i h\ge-\tau^2K_i/2,
\qquad \tau=\max_k |h_k|/r_k\le1.
\]

For each coordinate j and sign σ, choose λ ≥ 0 and define

\[
e=\lambda^\top A-\sigma e_j^\top,
\qquad
\eta=\sum_k r_k|e_k|,
\qquad
M=\sum_i\lambda_iK_i.
\]

It suffices to verify the single strict condition

\[
\boxed{\eta+M/2<r_j.}
\]

Indeed, for a nonzero displacement choose a saturated coordinate and the opposite sign. Then

\[
\tau r_j\le\tau\eta+\tau^2M/2
\le\tau(\eta+M/2)<\tau r_j,
\]

a contradiction. This is the whole nonlinear conclusion once branch completeness and curvature bounds are established.

The weighted residual is no worse than the estimate ε max(r_k). It also directly respects the different units and radii of the coordinates. In the new certificate the maximum ratio changes only slightly, from approximately 0.6764635896702756 to 0.676463589644483; the advantage is conceptual and organizational, not a major numerical improvement.

This is a simplification of the same proof architecture, not a new proof of global capture.

### S2. Separate three levels of argument

A compact organization would distinguish:

1. **Geometric rules:** ownership, whole-angle cores, closed coverage, and safe transitions.
2. **Global capture proposition:** every relevant packing can be transformed and labeled into the specified rectangle.
3. **Endpoint theorem:** exact witness + local isolation + capture imply optimality.

The article already moves in this direction, and the previous simplification review explicitly recommends invariant-based organization. This suggestion should not be credited as a newly discovered geometric method. [S6]

The improvement is to make the intermediate capture proposition a formal statement with all parameters and quantifiers, then move inventories and execution history into its verification appendix. That leaves a short readable proof without hiding a certificate premise.

### S3. There is an apparent uniqueness corollary worth resolving explicitly

Under the **universal capture proposition as stated**, run the argument on a packing with S = T. The rigid transformation preserves the entire side-T container; the packing enters the same local rectangle; local isolation forces the witness.

Thus those premises appear to imply uniqueness of the optimal packing modulo square-container symmetries, square relabeling, and the equivalent quarter-turn parameterizations of each square. The article expressly avoids a separate global uniqueness claim. [S2, endpoint section]

This is not an error in the weaker optimality conclusion. It is a logical consequence to check against the precise scope of every capture admission. Either state the corollary after that scope check, or identify the extra restriction that makes the capture proposition insufficient for S = T. This report does **not** independently certify the corollary without the global replay.

### S4. Publish the local proof with a canonical row dictionary

The new reconstruction contains only **56 distinct derivative rows** across all 128 branches. A small canonical row table, a per-row curvature bound, and branch incidence lists would make the local proof easier to inspect and reduce repeated certificate representation. The new implementation already shares this calculation internally.

This suggestion concerns packaging and reviewability. It does not remove the obligation to connect every nonlinear feature to an allowed branch or to use a safe maximum curvature for aliases.

### S5. Do not simplify away the branch census without a new argument

There are only 30 derivative rows common to every branch, in 33 variables. Those common homogeneous rows necessarily have a nontrivial nullspace. Therefore, merely retaining common rows cannot reproduce the present first-order obstruction to every nonzero motion.

A different nonlinear argument might use fewer branches, but that has not been established here. Nor has this audit established that any global case, capture node, or boundary branch can be deleted. Compressing the exposition is justified; claiming a smaller proof ensemble is not.

## 6. Third priority: clarity and presentation

### E1. Put the coordinate and label conventions in one early table

The most consequential reading risk is not notation density by itself, but applying a correct formula in the wrong frame. An early legend should distinguish physical cap centers, normalized cover coordinates, scaled field coordinates, centered heights, and fixed-T local displacements. It should also distinguish cell-owner labels from witness-square labels, and half-angle t from radian angle displacement.

A suitable table is:

| Symbol or index | Meaning |
|---|---|
| p | Physical center in the cap; the small square has side 1 |
| z | Normalized center-cover coordinate; not the field coordinate |
| p_f = Bp | Field center; small-square side B and container side L |
| y_i in branch conditions | Centered physical height for cell-owner i |
| t_i | Rational half-angle parameter for that owner's orientation |
| h_(3k+2) | Radian angular displacement of witness label k |
| p_T | Rigidly aligned physical center for comparison with the fixed-T witness |

The owner-to-witness role bijection belongs beside the pose-inclusion statement. The checked inclusion source distinguishes these objects correctly; readers should not need to reconstruct its conventions from the code. [S16]

### E2. Make the numerical propositions fully specified in a small appendix

Give the sixteen rational sites or a tiny standalone exact cover specification, the role bijection, and the 33 local radii next to the propositions that use them. Report exact margin identities or reproducible formulas, not only rounded positive displays.

The local radii are reproduced in Appendix A of this report because they are indispensable to specifying the new local computation. The missing inline cover parameters are not a logical gap when a precise external certificate supplies them; they are a barrier to auditing the paper as a mathematical document.

### E3. Separate current status from historical status

The article's current review level and an older simplification record use different grading conventions. The older record should carry a prominent historical-epoch label or point to one authoritative current status record. Otherwise, readers encounter apparently inconsistent assurances without knowing whether the mathematics, verification, or merely the grading system changed. [S1, S6]

No grading label should substitute for a statement of what was executed, independently implemented, or formally proved. This report itself does not automatically fulfill the project's distinct-reviewer or human-oversight requirements.

### E4. State hypotheses before numbers

For every certificate family, lead with its proposition: the admissible input state and assumptions, the rule applied, and the conclusion. Follow that with the exact artifact identity and execution scope. Counts are valuable completeness checks, but “N cases passed” is not the mathematical meaning of those cases.

A particularly useful display would be a dependency table marking unconditional exclusions, exclusions conditional on the earlier baseline, capture transitions, and inclusion. This makes a circularity audit possible without reading a chronological execution diary.

### E5. Keep the safeguards the article already explains well

Preserve the explicit distinctions between a point inside a cell and an owned point inside a square; between median projections and containing a majority of sites; between sampled angles and complete closed intervals; and between a local enclosure and a contradiction. Those are not ornamental qualifications. They prevent incorrect shortened versions of the proof.

For final editorial work, give one worked certificate row with its exact hypotheses and conclusion, then refer back to the invariant. Avoid multiple near-duplicate descriptions that differ only in execution phase names.

## 7. Recommended acceptance work, in priority order

**First:** make the global proof freshly reproducible from a clean, immutable release. Repair stale bindings with checked provenance, separate semantic states from timing-dependent receipts, and record fresh primitive geometry execution. This is the largest remaining gap between this audit and full independent computational confirmation.

**Second:** independently review and replay the global closed-set kernel and conditional capture/exclusion ancestry. The local module now has a materially independent reconstruction; the global geometry deserves comparable attention.

**Third:** adopt the contract-safe coverage regression tests, publish the exact parameter block, and reorganize the proof around capture plus the abstract isolation lemma. Only after those should effort go into deleting cases or further shortening the certificate ensemble.

**Bottom line:** I found no demonstrated fatal flaw in the mathematical optimality argument. I obtained substantial new exact evidence for its witness and local endpoint theorem. The unresolved conclusion of this audit is global certificate execution, not a discovered counterexample or an invalid local argument. The documented packaging defects should be repaired before presenting the proof as a clean independently reproducible executable release.

## Appendix A. Exact local radii used in the new computation

The order is witness label k, then physical x radius, physical y radius, and angular radius in radians. These are transcribed inputs from the published inclusion result [S17]. Their local sufficiency was checked here; their coverage of all captured poses was not.

| k | r_x | r_y | r_theta |
|---|---|---|---|
| 0 | 18767167/10000000000 | 4435327/2000000000 | 5670363/2500000000 |
| 1 | 1636033/1000000000 | 6880181/5000000000 | 1764113/1000000000 |
| 2 | 8962451/10000000000 | 5212397/5000000000 | 5670363/2500000000 |
| 3 | 1635053/1000000000 | 10683139/10000000000 | 1890121/1250000000 |
| 4 | 4087019/2500000000 | 13962901/10000000000 | 20161291/10000000000 |
| 5 | 12900283/10000000000 | 534153/500000000 | 1890121/1250000000 |
| 6 | 678279/500000000 | 4124329/5000000000 | 35312013/10000000000 |
| 7 | 11182451/10000000000 | 3232837/5000000000 | 8824483/2500000000 |
| 8 | 9356857/10000000000 | 8671199/10000000000 | 7549783/5000000000 |
| 9 | 293551/400000000 | 10335557/10000000000 | 40352153/10000000000 |
| 10 | 1920157/2500000000 | 8222903/2500000000 | 67647473/10000000000 |

## Appendix B. Reproduction and interpretation of the new results

See `README.md` in the bundle for exact commands. The bundle includes the newly generated dual weights, all audit programs, positive and negative results, dependency versions, and a SHA-256 manifest. It excludes the local pickle cache; that cache must be reconstructed before verification. Do not load an externally supplied pickle.

The programs use assertions and refuse Python optimization mode. Root/sign comparisons, witness identities, feature margins, and dual acceptance are exact. Numerical solver choices and the displayed numerical common-row rank are not proof premises.

The machine-readable result explicitly sets `global_optimality_verified` to false. That field is intentional, not an unfinished local result.

## Appendix C. Source register

References denote the inspected materials, not a claim that every linked program was executed. The source map JSON duplicates this register in machine-readable form. Review-side `main` URLs are mutable; the upstream original proof and focused note are pinned to the revision stated above.

**[S1] Rendered review article, draft v0.1.0, last revised October 1, 2026.**  
`https://jlevy.github.io/squares/papers/n11-optimality-review.html`

**[S2] Generating article template; read for exact mathematical text.**  
`https://raw.githubusercontent.com/jlevy/squares/main/packing/devtools/templates/n11-optimality-review-article.md`

**[S3] Pinned original mathematical proof.**  
`https://raw.githubusercontent.com/Queuingtheorydotcom/11SquaresOptimal/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/PROOF.md`

**[S4] Retained packet, execution scope and fresh-replay limitations.**  
`https://raw.githubusercontent.com/jlevy/squares/main/packing/resources/web/n11-optimality-2026-09-29/README.md`

**[S5] Chronological census/contract review; especially Compiled Exact Coverage and final acceptance.**  
`https://raw.githubusercontent.com/jlevy/squares/main/docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md`

**[S6] Prior simplification review; compare the scope of claimed simplifications.**  
`https://raw.githubusercontent.com/jlevy/squares/main/docs/project/reviews/review-2026-09-30-n11-expository-simplification.md`

**[S7] Witness coordinate source.**  
`https://raw.githubusercontent.com/jlevy/squares/main/packing/cases/trump11/packing.py`

**[S8] Independent-project D4 checker; source reviewed, object-backed execution not performed here.**  
`https://raw.githubusercontent.com/jlevy/squares/main/packing/devtools/check_n11_optimality_d4.py`

**[S9] Field geometry and historical vertical coverage predicate.**  
`https://raw.githubusercontent.com/jlevy/squares/main/packing/devtools/check_n11_optimality_field_mask0.py`

**[S10] Corrected fast exact coverage kernel.**  
`https://raw.githubusercontent.com/jlevy/squares/main/packing/devtools/n11_fast_exact_cover.py`

**[S11] Closed point/segment domain coverage helper.**  
`https://raw.githubusercontent.com/jlevy/squares/main/packing/devtools/check_n11_closed_degenerate_cover.py`

**[S12] Generic update consumer, including ownership and whole-angle checks.**  
`https://raw.githubusercontent.com/jlevy/squares/main/packing/devtools/check_n11_generic_fresh.py`

**[S13] Capture transition primitives and explicit degenerate-domain dispatch.**  
`https://raw.githubusercontent.com/jlevy/squares/main/packing/devtools/check_n11_capture_transition_pilot.py`

**[S14] Project local-isolation consumer and its shared source declarations.**  
`https://raw.githubusercontent.com/jlevy/squares/main/packing/devtools/check_n11_optimality_local_isolation.py`

**[S15] Project local dual consumer and exact residual arithmetic.**  
`https://raw.githubusercontent.com/jlevy/squares/main/packing/devtools/check_n11_optimality_local_dual.py`

**[S16] Pose-inclusion consumer: coordinate and angle transformations.**  
`https://raw.githubusercontent.com/jlevy/squares/main/packing/devtools/check_n11_optimality_pose_inclusion.py`

**[S17] Published rational radii used as input to this new local proof.**  
`https://raw.githubusercontent.com/jlevy/squares/main/packing/resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/result.json`

**[S18] Completion inventory consumer, including dependency admission.**  
`https://raw.githubusercontent.com/jlevy/squares/main/packing/devtools/inventory_n11_completion.py`

**[S19] Final retained-evidence composer.**  
`https://raw.githubusercontent.com/jlevy/squares/main/packing/devtools/check_n11_final_composition.py`

**[S20] Composition joins: frames, roles, radii and source-state identities.**  
`https://raw.githubusercontent.com/jlevy/squares/main/packing/devtools/n11_composition_joins.py`

**[S21] Pinned focused-rectangle mathematical note.**  
`https://raw.githubusercontent.com/Queuingtheorydotcom/11SquaresOptimal/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/src/evidence/research/global-math/FOCUSED-LOCAL-RECTANGLE.md`

**[S22] Capture child consumer; inspected admission and ancestry mechanisms, not a full execution.**  
`https://raw.githubusercontent.com/jlevy/squares/main/packing/devtools/check_n11_capture_child_node.py`

