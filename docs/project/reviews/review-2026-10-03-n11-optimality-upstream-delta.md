# Eleven-Square Optimality Proof: The Delta for the Original Contributor

**Date:** October 3, 2026\
**Author:** Claude Code, lead session with Opus sub-agents; human oversight pending\
**Subject:** the computer-assisted proof of
[Queuingtheorydotcom/11SquaresOptimal](https://github.com/Queuingtheorydotcom/11SquaresOptimal/tree/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c),
pinned at `f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c` and [archived here][proof], set
against the Squares Project’s confirmation, its two adversarial reviews of October 3,
and the [explainer paper][paper] at v0.1.3\
**Tracking:** `think-nnrx`;
[jlevy/squares#317](https://github.com/jlevy/squares/issues/317)

**Disposition:** This record is the delta to hand back to the original contributor.
It lists every correction, simplification, explicit interface and retained replacement
component that the confirmation and the two reviews of October 3 produced, and what the
paper now states that the original does not.
Every item names its source in this repository.
Neither review found a counterexample or a fatal error, and the proof’s mathematics
stands. Nothing here claims a new complete fresh run of the global proof: the composer
checks retained joins, the bulk exclusions and the capture geometry were not rerun, and
T-060 stays at S5/V3/C3. Where the reviews disagree with each other or with the
[integration record][integration], the integration record governs, and the record says
so.
Issue [#317](https://github.com/jlevy/squares/issues/317) carries the running summary
of the work to streamline, explain and formalize the result.

## How the Delta Was Produced

| Date | Stage | What it contributed |
| --- | --- | --- |
| September 29 | Confirmation and [whole-proof acceptance][acceptance] | Independent first-party consumers for all 2,180 exclusions and the ten capture nodes; the [final composition][composition]; the [stale leaf digests][stale] found |
| September 30 | Paper v0.1.0 and four exposition reviews ([mathematical][math-review], [reconciliation][], [intuition][], [citations][]) | The field-capacity lemma the original leaves to its checker; the finite-direction reduction; the required coverage domain; a first statement of the seam rule |
| October 3 | The [project’s adversarial review][own-review], applied as v0.1.1 | Every number the paper states reproduced, most by independent recomputation; ten wording defects, seven simplifications, one simplification found unavailable |
| October 3 | [GPT-6 Pro’s unified review][gpt6] and its [integration][], v0.1.2 | Findings C1 to C9 and S1 to S7 dispositioned; four retained components with receipts; the [evidence pack][evidence] retained |
| October 3 | The [receipts register][register], v0.1.3 | The purpose and tier of every receipt; what a receipt is and the three verification depths |

The paper’s versions are recorded in `OPTIMALITY_REVIEW_HISTORY` in
[release.py][history]. The two pull requests that carried the October 3 work are
[jlevy/squares#313](https://github.com/jlevy/squares/pull/313) and
[jlevy/squares#314](https://github.com/jlevy/squares/pull/314).

The status column uses these values:

- **Applied (vX):** the paper states it from version X.
- **Retained:** a checked component beside the accepted one, with its own receipt or
  manifest; it is not a premise of the composed proof and changes no frozen byte.
- **Upstream:** a change for the contributor’s repository; this project never edits the
  archived copy.
- **Deferred:** a bead here names the slice.
- **Recorded:** measured in a review by a script that was not retained as a control.
- **Declined:** not adopted, with the reason.

## What Stands Unchanged

The [project’s review][own-review-confirmed] recomputed most claims with independently
written arithmetic. GPT-6 Pro’s Review B executed further components, listed in
[its section 3.3][gpt6-executed]. These values decide the claims, and each agrees with
the original:

| Claim | Decisive value |
| --- | --- |
| The root and $T$ | $p$ is squarefree with two real roots; the one in the interval is $0.3657693076$; the original’s 28 displayed decimals of $T$ are exact |
| $T<U$ | $U-T=2.103\times10^{-21}$, by an exact sign test |
| The algebraic degree | $p$ and the side polynomial are both irreducible, so $\mathbb Q(T)=\mathbb Q(u)$ has degree 8 |
| The construction | 44 vertices inside, 20 coordinates exactly on walls, 14 contacting pairs, smallest positive gap $0.02487$ |
| The cover | Largest $(U-1)^2\operatorname{diam}^2$ is $0.9509$, in cell 6; the half-turn is the only nontrivial symmetry of the sites |
| The overlay and bans | 220 regions, 212 polygons and 8 points; the 1,572 bans are exactly the label-distinct region pairs whose maximum physical distance is below one; largest banned $0.99587$, smallest unbanned $1.00335$ |
| The three finite D4 problems | Unsatisfiable under an independent search with 1,232, 1,882 and 759 nodes; without the bans, sources 999 and 1462 become satisfiable |
| Field certificates | The transfer sets of all 46 accepted packets match their receipts on recomputation; Review B checked all 59 supplied certificates, 24,373 angle rows and the exact 1,904-case union |
| A generic exclusion | Case 2095 replayed in full by Review B: five updates and 160 closed rows |
| Pose inclusion | All 136 live rows and 1,542 vertices inside the rectangle; narrowest slack $2.3\times10^{-12}$ |
| Local isolation | 88 features stay unavailable, smallest margin $0.012636$; the curvature bound is tight, with $0.997$ the largest observed ratio to it |

## 1. Corrections to Statements

Most items here correct the exposition, the original’s or the paper’s. One concerns this
repository’s own checker, and one the publisher’s release.
None is an invalid proof step.
GPT-6 Pro separates a missing hypothesis in an exposition, a helper defect under a
restrictive contract, and a stale binding ([section 1][gpt6-assessment]), and the items
keep that distinction.

| Item | What the original has | What the delta adds or corrects | Evidence | Status |
| --- | --- | --- | --- | --- |
| Pointwise angular-row invariant and the seam | §5: an outer pose cover “contains every possible center and orientation”, a statement about the union of the rows. | In every valid packing, each row whose closed angle interval contains the actual angle encloses the actual center, and the intervals cover the allowed range. So a branch may drop another row’s single shared endpoint angle, because the retained row already carries the guarantee there. It may never drop a point or segment of a center polygon. Two rows, $[0,1/2]$ and $[1/2,1]$ with different centers, show the union form is not enough. The checkers already enforce the stronger form. | [GPT-6 C1][c1]; [integration, C1][int-correctness]; [reconciliation, seam][recon-falsify] | Applied (v0.1.2); upstream for §5 |
| Ownership over valid packings | §5: an owned hull lies “strictly inside that same square in every surviving pose”. | Ownership is quantified over valid packings under the current assumptions, not over every artificial pose a loose outer cover keeps. Capture round 1, owner 2, row 0 at $t=1/64$ has such a pose: seed point 6 lies outside the artificial square by about $0.00244$ in the field frame. The walls already forbid that pose. No accepted-packing counterexample is claimed. | [GPT-6 C7][c7]; [integration, C7][int-correctness] | Applied (v0.1.2 adds the reason); upstream for §5 |
| Separation features as a disjunction of conjunctions | §7 is correct: all four corners must satisfy the projection inequality. | The paper’s v0.1.0 had compressed this. It now prints $\bigvee_{f=1}^{8}\bigwedge_{k=1}^{4}g_{f,k}(h)\ge0$ and says one negative corner disables the whole feature. | [GPT-6 C6][c6] | Applied (v0.1.2); no upstream change |
| The field-charge lemma and its citation | §5 has no field-charge text. §12 names the 59 field certificates and justifies transfer “by containment of the antecedent”. No charge definition, capacity proof or strict budget rule appears in `PROOF.md` or the README. | The paper states the lemma: the five-site median-projection charge, capacity one by strict separation, the whole-angle lower charge, required-owner transfer, and contradiction from a strict excess over the budget. Its footnote now cites §12 and says the original states no charge lemma. | [GPT-6 C5][c5]; [project review, item 2][own-corrections]; [reconciliation][] | Lemma applied (v0.1.0); citation applied (v0.1.2); upstream for the lemma |
| Transfer through the half-turn | §12 leaves the mask bookkeeping to “the accepted ledger”. | A certificate excludes every case whose mask, or its half-turn, meets the rule. Without the half-turn the 46 accepted packets reach 1,666 of the 1,904 field cases; the other 238 are reached only through it. | [Project review, item 1][own-corrections] | Applied (v0.1.1); upstream as wording |
| Four stale publisher digests | The published leaf audits bind final-state digests far15 `3b7f1ea0`, far13 `f83eb23c`, far2 `7551646f` and near `81002706`. | The canonical digests of the pinned final states are `9e28b092`, `87482985`, `11d4a28e` and `a6d45c0c`. The project found the near mismatch on September 29, then all four. Review B recomputed the near one from the pinned object of 27,653,954 compressed and 185,901,535 decoded bytes. The publisher’s replay compares fresh results with the stale values, so its unchanged driver would refuse. This is a binding defect, not a geometric counterexample. | [Source-graph receipt][source-graph] (full digests); [September 29 review][stale]; [GPT-6 C3][c3] | Disclosed in the paper since v0.1.0; upstream |
| Singleton defect in an interval helper | Not in the original. The defect is in this repository’s frozen consumer, `covers_vertical` in `check_n11_optimality_field_mask0.py`. Review B’s small controls on the publisher’s V9 helper agreed on closed boundaries. | The helper treats $[1,1]$ as covered by $[0,0]$: 616 false acceptances in a 12,180-case control, all on singleton targets, none the other way. Its only caller is the complete union-cover sweep, which refuses zero-area domains. Every interior slice of a positive-area convex domain has positive length, and a finite union of closed regions contains the limits, so the sweep stays sound. A corrected kernel serves new callers; its docstring audits the ten call sites. Not traced: whether a retained receipt exercised the defective branch. | [Kernel][kernel] and [its test][kernel-test]; [GPT-6 C2][c2]; [GPT-6 B.2][gpt6-checks] | Retained (kernel); applied (v0.1.2); 357 receipts bind the frozen bytes, so they stay |
| The mask-0 worked row | No worked certificate row. | Mask 0 needs owners in cells 0, 1, 2, 3 and 6, with 55 owned points. Cells 1 and 2 each carry threshold one against a budget of one, so $2>1$. They have 67 and 69 rows, and the certificate excludes 459 cases. In cell 1, row 0 over $[0,1/64]$, every legal center activates feature 931 or meets a point owned by owner 0 or owner 2. GPT-6 Pro says three points cover the row. The accepted proposal records five regions, the feature and four points, and two points suffice. | [GPT-6 6.3][gpt6-example]; [integration, 6.3][int-clarity] | Applied (v0.1.2), with the proposal’s count |

## 2. Simplifications Established with Evidence

Three of these are retained as checked components, each with its own receipt or
manifest. The rest are exposition, or measurements that show a simplification is not
available.

| Item | What the original has | What the delta adds or corrects | Evidence | Status |
| --- | --- | --- | --- | --- |
| The polynomial is one closing contact; the root is unique | §1 gives $p$, the interval and $T$; it does not derive $p$. | With $u$ free in the placement formulas, every wall contact and 13 of the 14 square contacts hold identically. Square 2, $A(x_0,T-1)$, and square 10, the image of $A(\eta+2,-\zeta)$, have gap $p(u)/(2u(1-u^4)(1+2u-u^2))$, and overlap for smaller $u$. On $[9/25,37/100]$ the derivative $p'$ exceeds 4, so the root there is unique. | [Project review, item 2][own-simplifications]; [GPT-6 S6][s6]; [integration, S6][int-simplifications] | Applied (v0.1.1; uniqueness v0.1.2); upstream, optional |
| One half-angle chart | §2 defines $c$ and $s$ from $u$; §3 defines $t=\tan(\theta/2)$ by the same formulas, unconnected. | $u=\tan(a/2)$ for the common tilt $a$ of the five tilted squares, about 40.18°, so the tilted squares have $t=u$. | [Project review, item 1][own-simplifications] | Applied (v0.1.1) |
| Why four survivors, and why 438 | §4 lists the four masks; §6 reduces them to 438. | The four masks are the construction’s own center pattern under the eight symmetries: identity and half-turn give 1462, the axis reflections 999, the diagonal reflections 1659, the quarter-turns 438. No construction center lies within $0.0079$ of a cell boundary in normalized units. Case 438 is the quarter-turned construction, which is why the alignment $Q$ is a quarter-turn. | [Project review, item 3][own-simplifications] | Applied (v0.1.1) |
| Weighted-residual isolation lemma | §7 bounds the residual by $\epsilon_j$ in the 1-norm and checks $M_j<2(r_j-\epsilon_jR)$ with $R=\max_k r_k$. | With the weighted residual $\eta=\sum_k r_k\lvert e_k\rvert$ the lemma needs only $\eta+M_j/2<r_j$. The original’s check is a conservative instance, since $\eta\le\epsilon_jR$. The two ratios $(\eta+M_j/2)/r_j$ and $c_j=M_j/(2(r_j-\epsilon_jR))$ are different numbers. Direct weighting moves the published maximum $c$ from $0.6765052082$ to $0.6765052045$. | [GPT-6 S1][s1]; [integration, S1][int-simplifications] | Applied (v0.1.2) |
| Two-radius local box | §7: 33 fitted radii inside the working box of radius $1/64$; largest ratio about $0.6765$. | Radius $1/256$ for every coordinate except the angles of squares 9 and 10, coordinates 29 and 32, which get $1/128$. Every accepted radius is at most its replacement; the tightest, square 6’s angle, is at $0.904$. With the repository’s curvature bounds and the accepted duals, all 128 branches and 8,448 margins pass at worst ratio $0.8667$, and the 88 features stay unavailable. GPT-6 Pro’s six constants $K/r^2$, namely 21/2, 57/4, 99/4 and 30 for pairs and 3/4 and 3 for walls, are confirmed exactly and give $0.9515$. | [Checker][two-radius]; [receipt][two-radius-receipt]; [GPT-6 S2][s2]; [integration, S2][int-simplifications] | Retained; the proof’s rectangle stays the fitted one |
| The 56-row derivative dictionary | The row labels live inside the accepted objects. | GPT-6 Pro’s canonical dictionary of the 56 distinct derivative rows, with alias maxima and branch incidence. | [GPT-6 S2][s2]; [evidence pack][evidence] | Declined as a component; the file is kept in the evidence pack |
| Incidence propagation for the final D4 step | §6: an exhaustive bitset search over overlay assignments with 1,572 strict distance bans. | Fix the identity view’s mask and try the 216 assignments of non-438 masks to the other three views, 648 in all. Immediate contradictions, propagation contradictions and survivors are 168, 47, 1 for 999; 198, 17, 1 for 1462; 196, 20, 0 for 1659. In the 999 survivor two owners are forced into $R(1,1,11,4)\subseteq[23/50,27/50]\times[0,11/100]$ and $R(2,5,6,9)\subseteq[11/25,14/25]\times[23/100,7/25]$. Then $(U-1)^2((1/10)^2+(7/25)^2)<1989/2500<1$; the exact vertex bound is $0.704$. The reflection $g_1$ carries the 1462 survivor onto the 999 one. With 438 allowed, the construction’s own assignment survives as a control. | [Checker][incidence]; [receipt][incidence-receipt]; [GPT-6 S3][s3]; [integration, S3][int-simplifications] | Retained; replaces the final search only, and the bans stay the premise of the cuts for cases 2175 and 2176 |
| A minimum of 44 field certificates | §12: the baseline uses 59 field certificates. | Of the 46 field packets accepted here, 44 are mandatory, each the only cover of some case, and their union is all 1,904 field cases. So the minimum is 44 and the selection is unique; it omits masks 246 and 1802. The 44 have 17,963 rows and 4,233 ownership points, against 18,855 and 4,464 for all 46. It is bookkeeping over receipts, and nothing is deleted. | [Selection tool][selection]; [manifest][selection-manifest]; [GPT-6 S4][s4]; [integration, S4][int-simplifications] | Retained, as a reading aid and replay shortcut |
| A shorter transfer rule | §12: transfer by containment of the antecedent. | In all 46 accepted packets the charged cells lie in the owner set, and their thresholds alone exceed the budget. So a certificate excludes every case whose mask, or its half-turn, contains its owner set. | [Project review, item 5][own-simplifications] | Applied (v0.1.1), beside the general rule |
| Three forms of the five-site charge | No charge text. | The median-projection form; the half-plane form, every closed half-plane containing the core holds at least three sites; and the ten-hull form, the core meets the hull of every three sites. Capacity one follows from each in a line. Sites $(\pm1/2,0)$, $(0,\pm1/2)$, $(1/2,1/2)$ and core $[-3/10,3/10]^2$: the core holds no site yet earns the charge. | [Project review, item 4][own-simplifications]; [GPT-6 S5][s5] | Applied (v0.1.1 and v0.1.2); no ten-hull production checker exists |
| Branch completeness | §7: omitting noncontact constraints weakens the system and cannot exclude a feasible packing. | The 41 non-contacting pairs keep clearance at least $0.015$ across the rectangle. So no new contact forms, and the 128 branches are the whole local structure, not only a necessary relaxation. | [Project review, section 1.2][own-review-confirmed] | Applied (v0.1.1) |
| Conditional uniqueness corollary | §8 and §9 state capture for $S\le T$; §10 concludes only $s_{11}=T$. | The same premises cover $S=T$. Every optimal packing is then the construction up to the eight container symmetries and relabeling, conditional on the same exclusion and capture ensemble. The project registers only the optimality statement. | [GPT-6 S7][s7]; [GPT-6 2.4][gpt6-uniqueness] | Applied (v0.1.2) |
| A D4-symmetric cover | §4 uses an irregular sixteen-site cover. | Examined and not available. A search over D4-symmetric sixteen-site families found none with every cell of physical diameter below one. The best, the $4\times4$ grid, has normalized diameter $0.3536$ against the required $0.3476$; the retained cover reaches $0.3389$. A grid cell has physical diameter $1.017$. | [Project review, section 2.2][own-unavailable] | Recorded; one sentence applied (v0.1.1) |
| Keeping only the common rows | 128 branches of 42 rows. | Not available. Exactly 30 rows occur in every branch, of exact rank 25, so their nullspace has dimension 8 and contains $e_{21}$. They cannot give the first-order obstruction in all 33 coordinates. | [GPT-6 S2][s2] | Recorded |
| Radius headroom | The radii fit the captured domains with almost no slack. | With every radius multiplied by 1.2 the worst dual ratio is 0.81, and by 1.4 it is 0.95. At 1.5 the ratio reaches 1.015 and the argument fails, though the 88 feature margins stay positive. The review suggests inflating by 1.3. | [Project review, item 6][own-formal] | Recorded; the two-radius box gives slack of another shape |

## 3. Interfaces Made Explicit

The original defines most of these objects; the paper states them where a reader checks
a join, and generates the numeric tables from the retained receipts so they cannot
drift.

| Item | What the original has | What the delta adds or corrects | Evidence | Status |
| --- | --- | --- | --- | --- |
| Frames and units legend | §3 defines $p$, $p_f=Bp$, $z$, $t$, $L=191/50$ and $B=L/U$ in prose. | One table of seven rows with units, adding the centered physical height $y_i$, the local displacement $h$ (center in physical units, angle in radians) and the aligned center $p_T$. | [GPT-6 C9][c9]; [GPT-6 6.2][gpt6-legend] | Applied (v0.1.2) |
| The role bijection | §8 states the frame map; the label-to-owner map is not printed. | Local labels 0 to 10 map to capture owner cells 3, 15, 8, 0, 4, 1, 2, 11, 9, 10, 13. Labels 9 and 10, with the doubled angular radii, are owners 10 and 13, at coordinates 29 and 32. The table is generated from the role guard, the pose-inclusion result and the focused object, and refuses altered inputs. | [GPT-6 Appendix A.1][gpt6-roles]; [project review, section 1.2][own-review-confirmed] | Applied (v0.1.2) |
| The 33 radii and the sixteen sites | The radii are in the focused receipt; the sites are in the cover object `df7938d9`. | Appendix C prints the 33 radii as exact rationals, physical for centers and radians for angles; the largest is $0.0068$ and the smallest $0.00065$. It prints sites 0 to 7 as integers over 2,000,000, with site $15-i$ equal to $(1,1)$ minus site $i$. | [GPT-6 A.2 and A.3][gpt6-radii]; [integration, 6.4][int-clarity] | Applied (v0.1.2) |
| Four branches against ten nodes | §8 lists the four closed branches. | The paper separates the four closed branches from the ten-node, nine-edge ancestry. It also separates the two fourteens: fourteen root rounds of 154 owner updates precede the root node, which then runs fourteen steps of its own. | [Project review, item 7][own-corrections]; [integration, 6.4][int-clarity] | Applied (v0.1.0 and v0.1.1) |
| The grouping of the exclusions | The README groups the 2,180 exclusions as $1931+76+173$, by provenance. | The paper also groups them as 1,904 field and 276 generic; $276=27+76+173$ and $1931=1904+27$. The composer checks the set equality, not the count. | [Project review, section 1.2][own-review-confirmed] | Applied (v0.1.0) |
| Terms defined before use | Tied, available, live and seed are used without definition. | Each is defined before its first use. A zero gap on one axis is not contact: squares 0 and 4 have a zero $x$-gap and are $1.877$ apart. | [Project review, section 3.2][own-terms] | Applied (v0.1.1) |
| A scope notice beside the theorem | The README cites a completed 23-stage verification; the publication note says the public derivative has had no fresh full geometric replay. | Beside the theorem the paper says the lower bound rests on component computations, each observed and reviewed separately and joined by a composer, with no single fresh run of the whole proof. | [GPT-6 C8][c8] | Applied (v0.1.2) |
| What a receipt is, and three depths | §11 lists the evidence directory and replay scripts. | A receipt records the verdict, the SHA-256 of every input and of the checker, the command and commit, and a replay script. A reader can check object hashes, the composition’s joins in seconds, or a component’s geometry afresh. | [Paper, closing section][paper]; [PR #314](https://github.com/jlevy/squares/pull/314) | Applied (v0.1.3) |
| The receipts register | No counterpart. | 103 receipts, 48.7 MB, by tier: 51 composed (14.0 MB), 8 data (12.2 MB), 2 replacement (87.0 KB), 20 ancestry (22.0 MB), 11 control (57.5 KB), 11 attempt (347.7 KB). It is generated, and a test fails on an undocumented receipt or a stale file. | [Register][register] | Applied (v0.1.3 links it) |
| Verification levels across epochs | Not applicable. | The September reviews record V4/C5 under the ladder before September 30; the register now records S5/V3/C3. The paper states the current level once and explains the change. | [Project review, item 10][own-corrections]; [epistemics][] | Applied (v0.1.1) |

## 4. Reproduction and Release

The replay work is this repository’s. Two rows also concern the publisher’s release:
semantic parent admission, and the minimal input closure an outside verifier would need.

| Item | What the original has | What the delta adds or corrects | Evidence | Status |
| --- | --- | --- | --- | --- |
| Portable replay commands | `VERIFY.py` runs every stage after the full LFS store is decoded, about 11.3 GB. This repository’s earlier `replay.sh` scripts recorded a Mac’s mounted paths and Homebrew `timeout`. | One ordinary command per retained checker, with declared inputs, recorded ceilings and outputs in a new directory outside the tree. Each ran on Linux on October 3 and matched its receipt apart from timing. The older scripts stay as provenance. | [Validation guide][portable]; [GPT-6 6.4][gpt6-edits] | Applied |
| Three verification modes | No counterpart. | Input integrity: every one of the 36 retained objects decodes to its hash. Retained composition: the inventory and the composer, 2.9 s and 3.2 s here. Fresh geometry: one command per checker, local isolation the longest at 22 to 39 s. | [Validation guide][portable] | Applied |
| The composer and the inventories | `verify_recorded_proof.py` and the global result. | The completion inventory reports 2,180 accepted exclusions and none missing. The composer returns `PASS_REVIEWED_COMPONENT_COMPOSITION` with no pending obligations; accept it only with that status, an empty list and exit code zero. It records `geometry_rerun: false`. | [Validation guide][recheck]; [final composition][composition] | Applied |
| The retained components’ replays | No counterpart. | A table of the four components, what each replaces, its checker and receipt, and its replay. The two replay scripts reproduce their results exactly, timings aside, from any directory. | [Retained Replacement Components][replacements] | Applied |
| GPT-6 Pro’s evidence pack | No counterpart. | The archive of 202 files and 6,086,828 bytes, its manifest recomputed with no mismatch. Both drivers pass here, `PASS_NEW_RECONCILIATION_CHECKS` in 55.6 s and `PASS_REVIEW_SUPPLEMENT_COMPONENTS` in 38.5 s. 196 files are kept, 5.4 MB; the other six are byte-identical to objects already retained, and `restore.sh` rebuilds the archive byte for byte. Neither driver replays the global proof. | [Evidence pack][evidence] | Retained |
| What cannot be rerun here | The pinned source states and the LFS store. | Pose inclusion reads the publisher’s near-leaf state, 27,653,954 bytes compressed and 185,901,535 decoded, which this repository does not hold. The bulk exclusions and capture need about 2.1 GB of source objects not in the checkout; the last 32 exclusion cases took 5.7 CPU-hours, the near node 303 s and the root node 892 s. The child capture checkers pin byte-exact parent receipts, timing fields included, so a fresh parent cannot be admitted. | [Validation guide][portable]; [project review][own-formal]; [register][] | Deferred (`think-e2ot`) |
| Semantic parent admission | The publisher’s `replay_candidate.py` compares a fresh result with the historical audit, digest included; this repository’s child checkers pin byte-exact parent receipts. | A deterministic semantic serialization of a node’s state and a checked admission rule, distinct from execution provenance. Two parents that differ only in timing must feed the same child; a changed domain, endpoint, owner map, scale, condition or rule version must be refused or reverified. | [GPT-6 C4][c4]; [integration, C4][int-correctness] | Deferred (`think-if2i`); the open item |
| The minimal input closure | The driver materializes 2,638 LFS payloads, 11.3 GB decoded, before its first stage. | The non-field manifest already names the 924 objects, 2.12 GB, that those exclusions need. A standalone release with that closure, pinned checkers and one runner is what an outside verifier would download. | [Project review, item 2][own-formal]; [validation guide][standalone] | Deferred (`think-22uw`) |

## 5. Open Items for the Contributor

These are the changes the reviews ask of the original repository.
The archived copy here stays unchanged; `think-nnrx` holds them on this side.

| Item | What the original has | What the delta adds or corrects | Evidence | Status |
| --- | --- | --- | --- | --- |
| The stale digests and a corrected release | Four leaf audits bind stale final-state digests, and the replay compares fresh results against them. | Recompute the four bindings from the mathematical states and their provenance. Publish an old-to-new report, a fresh transcript and a new immutable release. Do not change a digest because an adjacent field says PASS. | [GPT-6 C3][c3]; [source-graph receipt][source-graph] | Upstream (`think-nnrx`; `think-gzju` tracks the digests here) |
| The missing charge lemma | §12 names the certificates and the transfer; no lemma. | A standalone lemma: the charge’s definition, capacity one, the whole-angle lower charge, required-owner transfer including the half-turn, and the strict excess over the budget. The paper’s text or the ten-hull form can serve. | [GPT-6 C5][c5]; [paper][] | Upstream |
| The section 5 wording | Union-level pose cover; ownership “in every surviving pose”. | State the row-by-row invariant with its induction and the seam rule, and quantify ownership over valid packings. | [GPT-6 C1][c1]; [GPT-6 C7][c7] | Upstream |
| The role and frame tables | The frame map in §8; the role map only in the data. | Print the local-to-owner map and a frame legend beside the capture bridge. | [GPT-6 C9][c9] | Upstream, optional |
| Three checked simplifications | The fitted rectangle, the bitset D4 search and 59 field certificates. | Adopt the two-radius box, the incidence bridge and the 44-certificate selection. Each has a checker, a receipt or manifest, and tests here. Adoption keeps the premises each names: the 1,572 bans for cases 2175 and 2176, the 2,180 exclusions, and the accepted pose inclusion. | [Retained Replacement Components][replacements]; [GPT-6 8.2][gpt6-adopt] | Upstream; retained here |
| An independent global kernel | Several consumers share clipping, coverage and collision routines. | A small independent closed-set and transition kernel run on the bound source objects. It should concentrate on lower-dimensional domains, universal partner quantifiers, pointwise angle coverage and conditional ancestry. GPT-6 Pro names it the next investment; the project review’s nearest item is keeping its first-principles recomputations as controls. | [GPT-6 C8][c8]; [project review, item 10][own-formal] | Deferred (`think-wbpu`); upstream welcome |

## Where the Sources Differ

| Point | What the sources say | Resolution |
| --- | --- | --- |
| The minimum field selection | GPT-6 Pro: 43 of its 59 certificates are mandatory and miss only case 1456, covered by the 167-row `59db0f81` rather than the 389-row `7722afef`. The integration record: 44 of the 46 accepted here are mandatory, and the selection is unique. | The integration record governs for this repository’s family. The 389-row packet is not retained, so the 167-row one is mandatory. GPT-6 Pro’s third omittable packet, mask 1925, has an incomplete receipt and was never accepted. Both counts are 44. |
| The mask-0 row | GPT-6 Pro: three owned points cover the row. The integration record: the proposal records five regions, and two points suffice. | The integration record governs; the paper states the proposal’s count. |
| The two-radius ratio | GPT-6 Pro: $0.9515$ with its six constants, smallest feature margin $0.0058975$. The receipt: $0.8667$ with the repository’s bounds, margin $0.0059028$. | Different curvature bounds over the same box; both pass, and the integration record confirms the six constants exactly. |
| D4 propagation operations | GPT-6 Pro records at most 19, 15 and 7 operations for 999, 1462 and 1659; the receipt records 12, 15 and 19. | The two count operations differently. The contradiction and survivor counts agree exactly, and neither argument uses the operation counts. |
| Identities behind the closing contact | The project review: 43 of 44 zero gaps vanish identically. GPT-6 Pro: 15 of a 16-entry contact list. | Different lists with the same single closing contact; the paper states every wall contact and 13 of the 14 square contacts. |
| The bound on $p'$ | GPT-6 Pro: a termwise lower bound of $10398878171521/2500000000000$, about 4.16. The integration record: the minimum on the interval exceeds 4.32. | A lower bound and a recomputed minimum; both exceed 4, which is all the argument uses. |
| Review A’s local ratio | Review A reports $0.6764635896702756$ from new duals; its archive was not supplied. | GPT-6 Pro does not count it as evidence, and finds that curvature conservatism can account for the gap. This record does not count it either. |

## Suggestions for the Formalization

These are the lead session’s judgments, ordered so that each step is a closed statement
with its own finite certificate and the trust base shrinks at each step.
Each names the delta item that makes it smaller than the original’s form.

1. **Formalize the endpoint and the construction first.** Everything is in
   $\mathbb{Q}(u)$: the polynomial $p$, the root’s uniqueness on $[9/25, 37/100]$ from
   $p' > 4$ (item 8 above), the 44 vertex containments and 55 pair separations as exact
   sign conditions, $T = (6u+4)/(1+2u-u^2)$, the rational cap $U$, and the opposite-wall
   span that turns $S < U$ into $S < T$. This is the smallest unit, and a proof
   assistant can take it whole with no computation outside exact arithmetic.
2. **State the capture proposition as one quantified sentence** over every valid packing
   with $S \le T$: the allowed symmetries and relabelings, the closed branches, the
   source and target frames, and the target rectangle (GPT-6 Pro’s section 6.1). The
   formal development then needs verified checkers for four closed rules, the pose
   update, ownership, the charge, and the closed cover, and never the search programs
   that proposed the certificates.
3. **Formalize the row-by-row invariant, not the union** (item 1), with the seam rule as
   its corollary and ownership quantified over valid packings (item 2). Formalize the
   corrected closed-interval contract, a singleton covered when some closed interval
   contains it, and prove the full-dimensional closure argument once as a lemma (item
   5). Do not formalize the historical predicate.
4. **Take the incidence-propagation bridge rather than the finite searches** (item 11):
   648 records, 220 closed regions and one distance bound, against 1,572 bans and three
   searches whose unsatisfiability a proof assistant would have to re-derive.
5. **Take the two-radius box and the weighted-residual lemma** (items 9 and 10): uniform
   radii, six rational constants and one abstract lemma replace 33 fitted radii and
   per-pair curvature bounds.
   The 8,448 margin checks remain, but each is a rational inequality with simpler
   inputs, and nothing in the chain uses a float.
6. **Use the ten-hull form of the five-site charge** (item 13): a statement about the
   convex hulls of three points is easier to formalize than the median projection, and
   the two are equivalent.
7. **Take the 44-certificate selection as the field obligation** (item 12), with the
   dependency closure the manifest records, in place of the 59 published certificates.
8. **Define the node state canonically** before formalizing capture: assumptions, angle
   intervals, center domains, owned hulls, roles, frame, scale and rule version, so the
   formal object is a state and a checked transition rather than a receipt’s bytes.
   This is the open item `think-if2i`, and it is also what a one-command fresh run of
   the whole ensemble needs.
9. **Mirror the composition table.** The theorem is the composition of seven
   obligations, the endpoint, the exhaustive classification, the 2,180 exclusions, the
   reduction to case 438, capture, local isolation with inclusion, and the rigid
   embedding; the paper’s closing table lists them with their accepted evidence.
   A formalization should discharge each row separately and compose them last, so that a
   failure in one row names itself.
10. **An independent kernel for the global rules** (`think-wbpu`), an independent
    closed-set and transition checker on the bound source objects, would give the
    distinct-method confirmation the ladder’s higher rungs ask for, and is the natural
    companion to a formal development: the formal checker and the independent kernel can
    be the same program.

The items the contributor can act on without waiting for a formalization are the five in
section 5: the four digests, the section 5 wording, the charge lemma, and the three
simplifications that already carry receipts here.

[proof]: ../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md
[paper]: ../../../packing/devtools/templates/n11-optimality-review-article.md
[history]: ../../../packing/src/sqpack/release.py
[integration]: review-2026-10-03-n11-gpt6-pro-review-integration.md
[int-correctness]: review-2026-10-03-n11-gpt6-pro-review-integration.md#first-priority-correctness-and-verification
[int-simplifications]: review-2026-10-03-n11-gpt6-pro-review-integration.md#second-priority-simplifications
[int-clarity]: review-2026-10-03-n11-gpt6-pro-review-integration.md#third-priority-clarity-and-presentation
[own-review]: review-2026-10-03-n11-optimality-paper-adversarial.md
[own-review-confirmed]: review-2026-10-03-n11-optimality-paper-adversarial.md#12-the-proof-and-its-verification-record
[own-corrections]: review-2026-10-03-n11-optimality-paper-adversarial.md#11-statements-in-the-paper-that-need-correction
[own-simplifications]: review-2026-10-03-n11-optimality-paper-adversarial.md#21-simplifications-available-now
[own-unavailable]: review-2026-10-03-n11-optimality-paper-adversarial.md#22-simplifications-examined-and-not-available
[own-terms]: review-2026-10-03-n11-optimality-paper-adversarial.md#32-terms-used-before-or-without-definition
[own-formal]: review-2026-10-03-n11-optimality-paper-adversarial.md#changes-that-would-simplify-validation-or-prepare-a-formal-proof
[gpt6]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md
[gpt6-assessment]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#1-assessment
[gpt6-executed]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#33-what-the-available-computations-establish
[gpt6-uniqueness]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#24-the-uniqueness-question-can-be-resolved-conditionally
[c1]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#c1-state-the-pointwise-invariant-required-at-angular-seams
[c2]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#c2-correct-the-historical-singleton-interval-predicate-and-document-its-restricted-use
[c3]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#c3-repair-the-four-stale-publisher-digest-bindings
[c4]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#c4-separate-semantic-parent-admission-from-incidental-receipt-bytes
[c5]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#c5-supply-the-missing-original-field-charge-lemma-and-repair-the-citation
[c6]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#c6-preserve-all-four-inequalities-within-each-separation-feature
[c7]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#c7-quantify-ownership-over-valid-packings
[c8]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#c8-make-composition-scope-and-implementation-independence-explicit
[c9]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#c9-publish-the-exact-frame-and-label-interface
[s1]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#s1-use-one-abstract-weighted-residual-isolation-lemma
[s2]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#s2-use-two-radii-six-curvature-constants-and-one-row-dictionary
[s3]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#s3-replace-the-final-d4-search-by-incidence-propagation-and-one-distance-bound
[s4]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#s4-reduce-the-fixed-field-certificate-family-to-a-minimum-of-44
[s5]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#s5-explain-the-five-site-field-charge-using-ten-convex-hulls
[s6]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#s6-derive-the-endpoint-polynomial-from-one-closing-contact
[s7]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#s7-finish-with-a-short-endpoint-lemma-and-a-scoped-uniqueness-corollary
[gpt6-legend]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#62-put-the-frame-legend-early
[gpt6-example]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#63-include-one-actual-field-certificate-example
[gpt6-edits]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#64-make-the-remaining-edits-concrete
[gpt6-adopt]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#82-second-adopt-the-specific-checked-simplifications
[gpt6-roles]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#a1-construction-and-square-labels
[gpt6-radii]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#a2-the-published-33-local-radii
[gpt6-checks]: review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md#b2-newly-performed-reconciliation-checks
[evidence]: ../../../packing/resources/web/n11-optimality-gpt6-pro-review-2026-10-03/README.md
[acceptance]: review-2026-09-29-n11-optimality-census-contract.md#whole-proof-acceptance
[stale]: review-2026-09-29-n11-optimality.md#confirmed-public-replay-binding-defect
[math-review]: review-2026-09-30-n11-optimality-explainer.md
[reconciliation]: review-2026-09-30-n11-explainer-proof-reconciliation.md
[recon-falsify]: review-2026-09-30-n11-explainer-proof-reconciliation.md#attempts-to-falsify-the-reductions
[intuition]: review-2026-09-30-n11-explainer-intuition.md
[citations]: review-2026-09-30-n11-explainer-citations-and-docs.md
[portable]: ../../../packing/resources/web/n11-optimality-2026-09-29/VALIDATION.md#portable-replay-commands
[recheck]: ../../../packing/resources/web/n11-optimality-2026-09-29/VALIDATION.md#recheck-the-retained-execution
[replacements]: ../../../packing/resources/web/n11-optimality-2026-09-29/VALIDATION.md#retained-replacement-components
[standalone]: ../../../packing/resources/web/n11-optimality-2026-09-29/VALIDATION.md#fresh-replay-and-a-standalone-release
[register]: ../../../packing/resources/web/n11-optimality-2026-09-29/receipts/README.md
[composition]: ../../../packing/resources/web/n11-optimality-2026-09-29/receipts/final-composition.json
[source-graph]: ../../../packing/resources/web/n11-optimality-2026-09-29/receipts/source-graph/result.json
[kernel]: ../../../packing/devtools/n11_closed_interval_cover.py
[kernel-test]: ../../../packing/tests/test_n11_closed_interval_cover.py
[incidence]: ../../../packing/devtools/check_n11_optimality_d4_incidence.py
[incidence-receipt]: ../../../packing/resources/web/n11-optimality-2026-09-29/receipts/d4-incidence/result.json
[two-radius]: ../../../packing/devtools/check_n11_optimality_local_two_radius.py
[two-radius-receipt]: ../../../packing/resources/web/n11-optimality-2026-09-29/receipts/local-isolation-two-radius/result.json
[selection]: ../../../packing/devtools/select_n11_field_minimum.py
[selection-manifest]: ../../../packing/resources/web/n11-optimality-2026-09-29/receipts/field-batch-a/minimal-selection.json
[epistemics]: ../../../epistemics.md

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
