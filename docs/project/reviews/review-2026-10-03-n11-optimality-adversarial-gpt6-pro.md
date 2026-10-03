# Unified adversarial review of the tentative optimality proof for eleven squares

> **Reviewer:** GPT-6 Pro, reconciling two of its own reviews of the paper and the
> proof. **Received:** 3 October 2026, from the owner; filed here verbatim apart from
> this note and the footer, under the date it was received.
> Its findings are dispositioned in the integration record that cites it.

**Review and reconciliation date:** 3 October 2026 (UTC).\
**Subject:** *A Review of the Optimality Proof of the Trump Packing of 11 Squares*,
draft v0.1.0, revised 1 October 2026, and the proof materials it cites.\
**Priorities:** correctness; simplicity of the proof; clarity of presentation.\
**Inputs reconciled:** `n11-optimality-adversarial-review-gpt-6-pro-1.md` (**Review A**,
the subsequently supplied review) and `n11-optimality-adversarial-review-gpt-6-pro-2.md`
(**Review B**, the earlier review produced in this conversation).

This document contains the consolidated findings, their mathematical justification, the
disposition of differences between the reviews, and the recommended repairs.
It replaces neither the source proof nor its large computational certificates.
Exact source identities, the available verification archive, and reproduction
instructions are recorded below so that a claim about a computation can be distinguished
from the computation itself.

## Contents

- [1. Assessment](#1-assessment)
- [2. Reconciliation decisions](#2-reconciliation-decisions)
- [3. Claim, parameters, and evidence scope](#3-claim-parameters-and-evidence-scope)
- [4. First priority: correctness and verification](#4-first-priority-correctness-and-verification)
- [5. Second priority: simplifications](#5-second-priority-simplifications)
- [6. Third priority: clarity and presentation](#6-third-priority-clarity-and-presentation)
- [7. Suspected objections that were resolved](#7-suspected-objections-that-were-resolved)
- [8. Recommended acceptance and integration work](#8-recommended-acceptance-and-integration-work)
- [Appendix A. Exact parameters and conventions](#appendix-a-exact-parameters-and-conventions)
- [Appendix B. Reproduction and evidence identities](#appendix-b-reproduction-and-evidence-identities)
- [Appendix C. Complete finding crosswalk](#appendix-c-complete-finding-crosswalk)
- [Appendix D. Source register](#appendix-d-source-register)

## 1. Assessment

**Neither review establishes a counterexample or a fatal mathematical error in the
audited optimality argument.** Their positive mathematical conclusions are compatible.
The exact attaining configuration, the rational-cap-to-exact-endpoint deduction, the
nonlinear local isolation method, the field-capacity argument, and the use of
simultaneous closed symmetry views withstand the objections examined here.
Review B additionally supplies available exact evidence for several substantial
simplifications of the final symmetry bridge, local rectangle, and field-certificate
selection. [R1][r1], [R2][r2], [R4][r4], [R9][r9], [R11][r11]

There are, however, concrete issues worth correcting before presenting the project as a
clean, independently reproducible executable proof:

1. **The short expositions omit the pointwise angular-row invariant needed to justify a
   branch restriction at a seam.** The stronger invariant is established by the
   inspected implementation and stated in the longer project review.
   The article and original proof should expose it directly.
2. **A historical coverage predicate really does falsely accept some singleton
   intervals.** Its use in a complete positive-area convex-domain sweep has a valid
   closure argument, and inspected degenerate-domain paths use separate checking.
   That restricted protection should be explicit; the defective predicate should not be
   reused as a general closed-interval checker.
3. **Four publisher final-state digest bindings are stale, and some fresh child
   admissions depend on historical parent-receipt bytes.** These are reproducibility
   defects, already disclosed by the project.
   They require checked rebinding and a corrected immutable release.
4. **The original proof omits the field-charge lemma that the review’s citation appears
   to attribute to it.** The reconstructed field rule itself is sound and all 59
   supplied field certificates were freshly checked in Review B.
5. **Several logical interfaces need more precise statements:** conjunctions within
   separating features, ownership over valid packings, the owner-to-witness bijection,
   angle units, and the distinction between retained composition and fresh geometric
   execution.

These findings have different classifications.
A missing hypothesis in an exposition, a defective helper used under a restrictive
contract, a stale digest, and an unexecuted global obligation should not all be
described as an invalid proof step.
The sections below identify the relevant distinction in each case.

**The central remaining assurance limitation is unchanged:** neither report, nor this
reconciliation, freshly executes the complete global exclusion and capture corpus.
Review B checked substantially more global geometry than Review A, but still did not
rerun the other 275 nonfield exclusions or the whole capture graph.
A successful retained-evidence composer does not fill that execution gap.
The combined report supports the audited mathematics and several concrete replacement
components; it does not claim a new complete independent execution of the global proof.
[R3][r3], [R4][r4], [R16][r16]

## 2. Reconciliation decisions

### 2.1 The two main boundary findings are different

Review A’s C1 concerns a **spatial singleton interval** passed to a historical coverage
helper. Review B’s C1 concerns an **angular singleton intersection** dropped when
restricting a family of pose rows to a closed branch.
Both findings survive, but their justifications and remedies differ.

- The spatial helper needs a correct singleton test, or a rigorously enforced
  full-dimensional sweep contract together with separate point/segment handling.
- The angular restriction needs a pointwise invariant ensuring that the retained
  adjacent row already encloses every genuine seam pose.

A closure argument for positive-area polygons does not by itself justify deleting an
angular row. Conversely, the pointwise angular invariant does not repair an incorrect
standalone interval predicate.

### 2.2 The reported local ratios are not conflicting measurements

The following quantities come from different certificate configurations:

| Configuration | Stated maximum | Evidence status |
| --- | ---: | --- |
| Published radii and published rational duals, replayed in Review B | Approximately `0.6765052082025971` | Available exact replay and result |
| Review A’s newly generated duals on the published radii | Approximately `0.6764635896702756` | Reported in A; its computational bundle was not supplied with the Markdown |
| Review A’s proposed coordinate-weighted residual, using its new computation | Approximately `0.676463589644483` | Reported in A; the lemma is checked here, but these particular certificate results remain unavailable |
| Review B’s enlarged two-radius box and six coarser curvature constants, using existing duals | Approximately `0.9515217307843866` | Two available exact implementations agree |

All are below one. A larger ratio for a larger rectangle with coarser bounds is expected
and is compatible with a simpler proof.
The small difference between the first two entries cannot be assigned to any one cause
without A’s weights and bound-generation code.
Different duals, curvature enclosures, and residual conventions can change the value.
It would be incorrect to call this a numerical contradiction or to attribute the entire
difference to replacing an unweighted residual by a weighted one.

Likewise, A’s reported unavailable-feature upper bound near `−0.012636021136276269` and
B’s simplified-box positive exclusion margin near `0.005897503722317347` describe
different enclosures.
They have consistent signs for the same conclusion: the corresponding unavailable
feature cannot become available.

### 2.3 Review A’s new local certificate claims need an attribution boundary

Only A’s Markdown was supplied for this reconciliation.
Its referenced archive, new dual weights, audit programs, result files, and manifest
were not attached. Accordingly:

- Its exact local numerical maximum, new dual generation, verify-only local replay, and
  seven local mutation tests are retained as **A-reported observations**, not as
  computations independently replayed here.
  Its 12,180-case interval experiment has now been independently reproduced against the
  pinned functions, with the same counts.
- All 33 radii printed in A were checked against the pinned pose-inclusion result.
  They match exactly and are contained in B’s independently checked two-radius
  rectangle.
- A’s weighted-residual lemma is mathematically valid.
  Its general conclusion does not depend on trusting its reported numerical run.
- Local isolation on A’s published rectangle is already supported by B’s available
  computations, including a separately reconstructed proof on a larger rectangle.
  The missing A bundle limits verification of A’s particular implementation and
  new-certificate claim; it does not leave the local theorem dependent on that claim.

A also used mutable `main` URLs for the review-side repository.
B identified an immutable review-side revision.
This reconciliation uses B’s pinned corpus when checking A’s source claims.
Agreement with that corpus is not proof that every file A saw on `main` was
byte-identical.

### 2.4 The uniqueness question can be resolved conditionally

A asks whether the capture proposition really includes $S=T$. B says that the stated
premises do, and therefore imply uniqueness up to container symmetries and relabeling.
The pinned original proof explicitly uses $S\le T$ in its endpoint and inclusion
statements; its complete capture audit also states that scope.
The inspected root imposes no additional branch assumptions, and the pose-inclusion
calculation does not require $S<T$. [R2][r2], [R10][r10], [R18][r18]

Thus B’s **conditional corollary follows from the same universal global premises used
for optimality**. The article’s weaker choice to claim only optimality is not an error.
The reconciliation resolves A’s scope question positively at the level of the inspected
statements and admissions.
It does not transform the unexecuted parts of the global chain into a fresh verification
of uniqueness.

### 2.5 A’s caution about deletion does not contradict B’s reductions

A says its audit established no deletions of global cases or capture nodes and warns
that keeping only the local rows common to every branch cannot replace the branch
census. Both cautions are correct within their scope.

B supplies additional evidence that A did not obtain:

- Its **44-field selection preserves all 1,904 field-excluded case conclusions**; it
  deletes redundant certificates within a fixed family, not coverage obligations.
- Its simplified **final D4 bridge** replaces a particular search argument.
  It does not remove earlier baseline-dependent symmetry exclusions or the global
  capture premise.
- Its **two-radius local proof retains all 128 branches and all 88 unavailable-feature
  exclusions**. It does not rely on the common rows alone.

The reductions are therefore retained, with their exact dependency limits.
Neither review justifies deleting arbitrary capture nodes or treating a smaller
top-level certificate list as a complete smaller source closure.

## 3. Claim, parameters, and evidence scope

### 3.1 The mathematical claim

Let $s(11)$ be the least side length of a square containing eleven independently rotated
unit squares with disjoint interiors.
Boundary contact is permitted.
Write $D_4$ for the eight rotations and reflections preserving a square container.
The claimed optimum is $s(11)=T$, where

$$
P(u)=5u^8-10u^7-2u^6+14u^5+12u^4-6u^3+2u^2+2u-1,
$$

$u$ is the unique root in $(9/25,37/100)$, and

$$
T=\frac{6u+4}{1+2u-u^2}
=3.87708359002281417730789706010096270637645566846\ldots.
$$

The rational cap, field scale, and aligning quarter-turn are

$$
U=\frac{387708359002281417731}{10^{20}},\qquad
B=\frac{191/50}{U},\qquad Q(x,y)=(-y,x).
$$

Exact comparison gives $T<U$, with

$$
U-T=2.1029398990372936235443315368374\ldots\times10^{-21}.
$$

The decimal is explanatory.
The proof needs the exact sign.
In field coordinates the cap side is $191/50$ and every small square has side $B$; this
is a change of units, not an eleven-unit-square packing of side $191/50$. [R1][r1],
[R2][r2], [R12][r12]

### 3.2 The logical obligations

| Obligation | Mathematical role | Dependency that must remain visible |
| --- | --- | --- |
| Exact witness | Establishes attainment at $T$ | Algebraic root, containment, unit geometry, and pair separation |
| Sixteen-cell cover | Gives exhaustive center classifications | Closed cells of physical diameter strictly below one |
| Exclusion ensemble | Removes 2,180 of 2,184 canonical cases | Valid geometric transitions, field budgets, and exact case unions |
| Earlier conditional D4 exclusions | Removes cases 2175 and 2176 at the relevant earlier stage | The stated earlier 1,931-case baseline, not the later final conclusion |
| Final D4 bridge | Forces a view with case 438 from the four remaining cases | The established exclusion set and simultaneous closed-view geometry |
| Capture | Sends every admitted case-438 packing into the retained near state | Complete closed branch coverage and all transition ancestry |
| Pose inclusion | Sends that near state’s poses into the local rectangle | Exact owner map, frame conversion, angle conversion, and source-state binding |
| Local isolation | Forces the labeled packing in that rectangle to equal the witness at fixed $T$ | Complete local feature alternatives and strict nonlinear inequalities |
| Endpoint deduction | Excludes $S<T$ and conditionally yields uniqueness at $S=T$ | The universal capture/inclusion scope for $S\le T$ |

The geometric center-cover proposition is independent of the later exclusion union even
when a file named for a D4 result packages both.
Separating those receipts would make the dependency structure easier to inspect.
[R4][r4], [R8][r8], [R11][r11]

### 3.3 What the available computations establish

The following table records execution, not merely source inspection.
“Review B” refers to the existing audit and preserved results; this reconciliation does
not claim to have repeated every prior run.

| Component | Available executed evidence | Limit |
| --- | --- | --- |
| Exact witness and endpoint | Independent rational-field reconstruction; 88 edge/orthogonality checks; 44 vertices; 176 wall inequalities; all 55 square pairs; 14 contacting and 41 strictly separated pairs; both spans equal $T$ | Establishes attainment and endpoint arithmetic, not global capture |
| Algebraic parameter | Root isolation, defining-polynomial identities, and irreducibility checks for the parameter and side polynomials | Irreducibility explains the algebraic degree; isolation and signs do the geometric work |
| Cover and final symmetry geometry | All 16 cells, 220 closed overlay regions, and all 1,572 original distance bans; separate boundary-line reconstruction | Includes eight singleton overlay regions |
| Earlier conditional symmetry cuts | Independent exact necessity calculations for 2175 and 2176 | Conditional on the earlier 1,931-case baseline |
| Fields | All 59 field certificates, 24,373 complete angle rows, 5,877 ownership checks, and exact 1,904-case union | Does not establish the remaining nonfield exclusions |
| Nonfield example | Complete case 2095: five updates and 160 closed rows | One of 276 nonfield exclusions; the other 275 were not freshly replayed in B |
| Selected capture | 130 strict seed points; 69 rows; 28 common-kernel vertices; seven compressed points | Selected seed/update work, not the complete capture graph |
| Final pose inclusion | 136 live rows and 1,542 vertices, with exact roles and frame/angle checks | Conditional on the retained near state’s full ancestry |
| Published local theorem | 112 features, 24 available and 88 unavailable; 512 raw choices; 128 matrices; all 8,448 signed-coordinate checks | Fixed-$T$ local conclusion only |
| Simplified local theorem | Two exact implementations; the second rebuilds 1,936 elementary values and gradients | Same global premises remain necessary |
| Retained final composition | Complete inventory and source/state joins; accepted with no pending obligations | Output explicitly has geometry rerun false |
| Diagnostic controls | 23 boundary/child/composition tests; eight generic tests; six invalid field inputs refused; 6,000 range-tree operations and 12,951 extra-direction checks | Tests supplement the soundness arguments; they do not prove the checker rules by themselves |

Review A independently reports matching witness, feature, branch, and elementary-mask
counts, plus a newly generated local dual set.
Its available mathematical text was fully reviewed; its unavailable machine artifacts
are not added to the “available executed evidence” column.

The elementary mask count has a short proof: $\binom{16}{11}=4,368$. The half-turn pairs
labels as $i\leftrightarrow15-i$, so an invariant subset has even size.
No eleven-label mask is fixed.
There are therefore 2,184 half-turn representatives.
This combinatorics is separate from checking the physical cell diameters and the
geometric involution.

## 4. First priority: correctness and verification

### C1. State the pointwise invariant required at angular seams

**Classification:** substantive omission in the short expositions; the inspected
construction establishes the needed stronger invariant.
**Location:** the article’s pose-preservation discussion, original `PROOF.md` section 5,
and `conditional_view` in the child-capture consumer.
[R1][r1], [R2][r2], [R6][r6], [R7][r7]

The statement “every true pose belongs to the union of the closed rows” is insufficient
for the branch restriction implemented by the consumer.
Suppose the rows are

$$
[0,1/2]\times\{A\},\qquad [1/2,1]\times\{B\},\qquad A\ne B.
$$

A pose at angle parameter $1/2$ and center $A$ belongs to their union.
Restricting to $t\ge1/2$ and discarding the first row’s singleton angular intersection
leaves only the second row and loses that pose.
Review B exercised the actual restriction function on this example.

The example does not satisfy the stronger invariant that the real proof maintains.
The necessary statement is

$$
\forall\text{ valid packings under the current assumptions},\quad
\forall r,\quad t_i\in I_r\Longrightarrow p_i\in D_r,
$$

together with coverage of the complete allowed angular range by the row intervals.
Thus **every applicable row** encloses the actual center, including both rows at a
common closed endpoint.

Initial wall envelopes have this property.
A new interval lies in a specified predecessor interval; necessary cuts, uniformly
forbidden regions, exact residual coverage, and outward compression preserve every
actual center on that interval.
The chronological project review already states this stronger pointwise property.
The short article and original proof should import it.
[R4][r4], [R7][r7]

**Repair:** give the quantified invariant and its short induction.
Explain that a singleton intersection can be omitted only when the retained adjacent row
already carries the endpoint guarantee.
The inspected checker refuses an unsupported wholly singleton angular branch.
Spatial points and segments require their own exact treatment; this angular argument
does not authorize discarding them.

**Acceptance check:** retain a regression showing that union-only data are not a
sufficient contract, and verify the actual seed/transition interface against the
pointwise statement.
Do not present the artificial two-row example as an accepted-certificate counterexample.

### C2. Correct the historical singleton-interval predicate and document its restricted use

**Classification:** genuine, already documented helper defect; no demonstrated false
acceptance of an actual complete proof certificate.
**Location:** `covers_vertical` in `check_n11_optimality_field_mask0.py`, the corrected
fast cover kernel, and the point/segment coverage helper.
[R8][r8], [R15][r15], [R17][r17]

For target interval $[1,1]$ and alleged cover interval $[0,0]$, the historical
recurrence initializes its cursor at 1. The interval below it does not advance the
cursor, yet a test that the cursor has reached the target’s upper endpoint succeeds.
The target is not covered.

A positive-area triangular target can have such a singleton as an endpoint slice.
Therefore, “the target polygon has positive area” does **not** make every individual
call to the interval helper correct.

The complete positive-area **convex-domain** sweep nevertheless has a separate soundness
argument for this specific defect.
At every abscissa strictly inside the target’s horizontal projection, its vertical slice
has positive length.
The historical singleton false-accept mechanism does not occur on such a target
interval. The complete arrangement sweep checks the relevant interior interval
configurations. Their covered slices are dense in the target, and a finite union of
closed covering regions contains their limits.
Hence it contains the boundary as well.
This is the project’s documented closure argument, and it is valid under the full sweep
contract. [R4][r4], [R15][r15]

This argument requires a complete arrangement sweep, a full-dimensional convex target,
and finitely many closed covering regions.
It is not a theorem about an arbitrary call to the old predicate, an arbitrary nonconvex
domain with isolated components, or a finite sample of angles or slices.

“Historical” does not mean unused: the frozen reference helper remains in the pinned
field/capture code, and the generic sequential path defaults to that reference backend.
The inspected call sites enforce the full-cover contracts or explicitly refuse/dispatch
degeneracies.
The three inspected field row builders have an additional protection: every
covering region is clipped to the query domain, so a nonempty regional slice at a
singleton target must be that same singleton.
The demonstrated below-target trigger cannot arise on those field calls.
Capture/generic forbidden regions may extend outside the domain and use the general
sweep/closure defense.

The inspected families are the mask-0 and mask-202 field consumers, the general field
runner’s **unweighted union-cover branch**, capture root pilot/continuation, transition
pilot, step 0, root-node checker (also used by child workers), and fresh/sequential
generic consumers. The separate weighted-cover kernel is not included in this
singleton-predicate analysis.
A consumer’s refusal of an unsupported zero-area domain is a refusal to certify it, not
a proof that the domain is empty.
[R8][r8], [R17][r17]

**Repair:** use the corrected interval rule for new releases, explicitly handle
singleton targets, and preserve the separate exact dispatch for zero-area spatial
domains. A singleton $[a,a]$ is covered precisely when some supplied closed interval
contains $a$. A segment must be covered as a closed one-dimensional set.
Keep frozen historical bytes for provenance, while directing new callers to the
corrected contract.

**Acceptance checks:** directly refuse $[1,1]\subseteq[0,0]$; accept a genuinely covered
singleton and a closed seam; reject a strictly positive rational gap, however small;
reject malformed interval endpoints.
The new exact enumeration reproduces A’s 12,180 cases and 616 historical false
acceptances, all on singleton targets, with zero corrected errors.
The triangle’s full historical cover is refused, and the point/segment controls accept
exact seams and reject gaps of $10^{-50}$. Inspect each relevant call site’s domain and
sweep assumptions. This audit does not exhaustively certify every historical variant or
trace whether an actual retained capture probe exercised the defective branch.

### C3. Repair the four stale publisher digest bindings

**Classification:** confirmed release/reproducibility defect, already disclosed.
It is not a new geometric counterexample.
[R3][r3], [R4][r4], [R5][r5]

| Leaf | Publisher’s final-state digest prefix | Observed final-state digest prefix |
| --- | --- | --- |
| Far 15 | `3b7f1ea0` | `9e28b092` |
| Far 13 | `f83eb23c` | `87482985` |
| Far 2 | `7551646f` | `11d4a28e` |
| Near | `81002706` | `a6d45c0c` |

For the near leaf, Review B verified the pinned object at 27,653,954 compressed bytes
and 185,901,535 decoded bytes, parsed the final state, and recomputed its canonical
digest. It matches the observed value, not the publisher’s stated value.
That is a fresh source-identity check, not a replay of that node’s geometric ancestry.

The reviewed alternative proof package is a chain of separately observed component
executions with checked joins.
It should not be described as a successful run of the unchanged publisher driver.

**Repair:** publish a new immutable release, an old-to-new binding report, and a fresh
transcript. Verify every replacement against the mathematical state and its provenance.
Do not change a digest merely because an adjacent JSON field says PASS, and do not
disable identity checks to make a runner complete.

**Acceptance check:** a clean checkout plus verified input acquisition runs the
advertised proof command without editing digests by hand and identifies which primitive
geometry it actually executed.

### C4. Separate semantic parent admission from incidental receipt bytes

**Classification:** confirmed replay-interface defect, already disclosed.
[R3][r3], [R4][r4], [R6][r6]

Some child consumers admit a byte-exact retained parent result containing timings and
other execution data.
A fresh parent may establish the same mathematical state and produce different bytes.
The current retained composer is not an automatic reviewed route for rebinding that new
execution.

Two identities should remain distinct:

- **Mathematical state and admission:** assumptions, allowed angle intervals, center
  domains, owned hulls, owner roles, frame and scale, applicable proof rule,
  rule/checker version, and successfully checked ancestry.
- **Execution provenance:** exact receipt bytes, timing, machine details, logs, and
  serialization of the particular run.

**Repair:** define deterministic semantic serialization and a checked admission rule for
fresh verified parents.
Preserve execution hashes as provenance.
A compact state hash alone must not bypass checking the transition that established the
state; equality of selected geometric fields is not an unrestricted substitute for
admissibility.

**Acceptance checks:** two independently executed parents with different timing bytes
can feed the same child after successful semantic admission.
A changed center domain, closed endpoint, owner map, scale, inherited condition, or rule
version must be refused or explicitly reverified under the documented rule.
Perform the resulting run from a relocated directory with no undeclared cache.

### C5. Supply the missing original field-charge lemma and repair the citation

**Classification:** omitted mathematical explanation and inaccurate citation
description; the reconstructed rule and the checked field instances survive.
[R1][r1], [R2][r2], [R4][r4], [R8][r8]

The article’s field footnote describes original `PROOF.md` section 5 as supplying field
charges and transfer.
That section supplies geometric ownership/exclusion machinery, but not the
median-projection charge definition, capacity proof, or strict weighted-budget rule.
Section 12 mentions the 59 fields and transfer without filling that omission.

The review itself and the independent field acceptance analysis do provide the missing
mathematics. Review B freshly checked all 59 supplied field certificates and their
1,904-case union.
This is therefore a defect in the cited exposition and attribution, not
an uncovered failing field certificate.

**Repair:** add a standalone lemma defining the charge, proving its capacity, explaining
whole-angle lower-charge verification, stating the required-owner condition for
transfer, and concluding contradiction from a strict excess over the global budget.
Correct the footnote to identify where the reconstructed argument actually appears.
The ten-triangle formulation in S5 offers a shorter equivalent definition.

### C6. Preserve all four inequalities within each separation feature

**Classification:** compressed logical exposition in the article; original section 7 and
the inspected local consumers have the correct structure.
[R1][r1], [R2][r2], [R9][r9]

For a contacting pair, one of eight separating features must hold, and a feature holds
only if all four of its corner inequalities hold:

$$
\bigvee_{f=1}^{8}\left(\bigwedge_{k=1}^{4}g_{f,k}(h)\ge0\right).
$$

This explains both key operations.
One corner with a strictly negative upper bound disables the entire feature.
A selected available feature contributes its necessary zero-at-the-witness corner
inequalities to a branch, along with the tied wall inequalities.
The resulting necessary systems give 512 raw feature choices and 128 distinct branch
matrices.

Dropping initially positive or noncontact constraints weakens the necessary system; it
does not discard any feasible packing.
Dropping a conjunct from the definition of the physical separation feature without
explaining the subsequent necessary-system relaxation would be confusing and potentially
misleading.

**Repair:** print the logical formula, explain the relaxation, and retain both branch
completeness and the 88 unavailable-feature checks.
Identical derivatives do not imply identical nonlinear functions; every shared
derivative row must carry the maximum applicable curvature bound.

### C7. Quantify ownership over valid packings

**Classification:** ambiguous wording in the original proof; the review article already
uses the correct valid-packing formulation.
[R1][r1], [R2][r2], [R7][r7]

An owned hull must lie strictly inside its owner’s square in every **valid packing
satisfying the current assumptions**. It need not lie inside every artificial pose
retained by a deliberately loose outer approximation.

Review B found a concrete distinction in candidate round 1, owner 2, row 0, at $t=1/64$:
seed owned point 6 lies outside an artificial square at residual polygon 0, vertex 1.
Its field-frame body coordinate exceeds $B/2$ by approximately `0.00244463249635`. That
artificial pose violates the true wall constraint.
It is not a valid-packing counterexample.

**Repair:** replace the original’s ambiguous “every surviving pose” wording with the
valid-packing quantifier.
Do not silently strengthen the assertion to every point of the outer domain.
Such a strengthening would require different domains or a new proof.

### C8. Make composition scope and implementation independence explicit

**Classification:** assurance boundaries and residual common-mode risk; no particular
wrong geometric result demonstrated by these observations.
[R3][r3], [R9][r9], [R16][r16]

The completion inventory and final composer verify obligation coverage, retained source
identities, and state joins.
They do not rerun every primitive geometry calculation.
A top-level field such as `global_optimality_proved` must be read in that documented
retained-evidence scope.

**Repair:** expose distinct results for input integrity, retained proof composition, and
fresh geometry execution.
A fresh-replay result should derive from computations actually executed or resumed
through a documented admissible mechanism.
Put a short scope statement beside the theorem, not only late in the reproduction guide.

Shared code is a separate issue.
The project local consumer shares construction/derivative source, and several geometric
consumers share clipping, coverage, and collision routines.
Agreement between wrappers is weaker evidence than agreement between separately
implemented primitives.
B’s independently reconstructed witness, boundary-line geometry, and second local
implementation reduce specified common-mode risks; they do not constitute a wholly
independent global kernel.
A reports another independent local implementation, but its bundle is unavailable here.

**Recommended next investment:** implement a small independent global closed-set and
transition kernel, then run it on the bound source objects.
Concentrate on lower-dimensional domains, universal partner quantifiers, pointwise angle
coverage, and conditional ancestry.
Another wrapper around the same arithmetic is a lower-value independence check.
Formal proof-assistant verification is an optional stronger assurance target, not a
prerequisite for a valid computer-assisted proof.
Neither multiple model reviews nor repeated execution alone fulfills a distinct
human-review or formal-verification requirement.

### C9. Publish the exact frame and label interface

**Classification:** an omitted proof-facing interface, correctly handled by the
inspected inclusion consumer.
[R10][r10]

Capture owner labels run through the sixteen-cell inventory; local witness labels run
from 0 to 10. Local center radii are physical lengths and angular radii are radians.
Capture uses the real half-angle coordinate $t_i=\tan(\theta_i/2)$ in the declared
orientation chart, with rational certified row endpoints.
Actual packing angles and their $t_i$ values need not be rational.
These are not interchangeable conventions.

Appendix A supplies the exact role bijection, the 33 published radii, the simpler
replacement radii, and a compact center-cover specification.
The local labels 9 and 10 with doubled angular radii are capture owners 10 and 13,
corresponding to vector coordinates 29 and 32. Print this interface beside pose
inclusion in the article.
Readers should not have to reconstruct it from code before checking whether two
individually correct lemmas compose.

## 5. Second priority: simplifications

The following distinguish checked replacement components from mathematical
reformulations that would still need a new production implementation.
Existing general ideas, including invariant-based organization and the nonlinear local
method, should retain their original attribution.
[R2][r2], [R4][r4], [R19][r19]

### S1. Use one abstract weighted-residual isolation lemma

**Status:** A’s proposed lemma is correct; its use with the available B certificates has
also been checked. This is a clearer statement of the existing nonlinear argument.

Let $r_k>0$ be the coordinate radii.
For a displacement $h$ in the closed rectangle, define

$$
\tau=\max_k\frac{|h_k|}{r_k}\le1.
$$

Suppose each necessary tied inequality in the applicable branch has the Taylor
consequence

$$
A_i h\ge-\frac{\tau^2K_i}{2},
$$

where $K_i\ge0$ is a valid bound on the second directional derivative for directions
with coordinate magnitudes at most $r_k$. For each coordinate $j$ and sign
$\sigma\in\{-1,1\}$, supply a nonnegative vector $\lambda$ and define

$$
e=\lambda^{\mathsf T}A-\sigma e_j^{\mathsf T},\qquad
\eta=\sum_k r_k|e_k|,\qquad
M=\sum_i\lambda_iK_i.
$$

Here $e_j$ is the $j$th coordinate unit vector.
It is sufficient to check

$$
\boxed{\eta+M/2<r_j}
$$

for every signed coordinate in every branch.
Exact upper bounds on $|e_k|$ suffice in place of their exact algebraic values.

For a nonzero $h$, choose a saturated coordinate, $|h_j|=\tau r_j$, and take $\sigma$
opposite to the sign of $h_j$. Multiplying the branch inequalities by $\lambda\ge0$
gives

$$
\tau r_j\le e\cdot h+\tau^2M/2
\le\tau\eta+\tau^2M/2
\le\tau(\eta+M/2)<\tau r_j,
$$

a contradiction.
This argument includes $\tau=1$ and therefore excludes distinct feasible
points on the rectangle’s boundary.
It is a finite nonlinear isolation argument, not merely a tangent-cone calculation.

The straight segment from the witness to $h$ need only remain in the analytic working
box; it need not be a path of feasible packings.
The proof makes no hidden assumption that an endpoint perturbation is connected to the
witness through feasible motions.

If an implementation instead supplies $\sum_k|e_k|\le\varepsilon$ and $R=\max_k r_k$,
then $\eta\le R\varepsilon$. Thus the existing unweighted-residual implementation is a
sufficient conservative instance of the same lemma.
Direct weighting is more natural for unequal physical and angular radii and can reduce
conservatism.

For numerical reporting, distinguish two equivalent acceptance ratios:

$$
d=\frac{\eta+M/2}{r_j}<1,
\qquad
c=\frac{M}{2(r_j-\eta)}<1\quad(\eta<r_j).
$$

Their values are not identical.
The available B checker reports the second form, with its chosen residual upper bound.
This reconciliation explicitly uses that convention when comparing the available exact
computations. A report that prints only “the isolation ratio” should add its formula.

The new direct-residual calculation on B’s fixed weights passes all 8,448
signed-coordinate obligations on both boxes.
With the published curvature bounds, the maximum $c$ changes from approximately
`0.6765052082025971` to `0.6765052045373554`. With the two-radius/six-constant
replacement below, it changes from approximately `0.9515217307843866` to
`0.9515217276118025`. The improvement is small; the principal benefit is a compact,
unit-aware statement of the proof obligation.
These are newly checked computations on **B’s available inputs**, not a replay of A’s
missing dual archive.

### S2. Use two radii, six curvature constants, and one row dictionary

**Status:** B’s simpler local rectangle and curvature bounds have two available exact
implementations. A’s canonical-row packaging proposal is compatible with them.
[R9][r9], [R10][r10]

Set $r=1/256$ and use

$$
|\Delta x_i|,|\Delta y_i|\le r\quad(0\le i\le10),
$$

$$
|\Delta\theta_i|\le r\quad(0\le i\le8),\qquad
|\Delta\theta_9|,|\Delta\theta_{10}|\le2r=1/128.
$$

All 33 published radii are at most their corresponding replacements.
Consequently the checked pose-inclusion result also places the retained near state in
this larger box. Enlarging the box requires a new local proof; B supplies that proof
rather than assuming isolation is monotone under enlargement.

All needed pair-gap Hessian bounds concern the fourteen contacting pairs.
At the witness, a common contact point is within the circumradius $1/\sqrt2$ of each
center, so their center distance is at most $\sqrt2$. Even throughout the larger working
translation box of radius $1/64$ per center coordinate,

$$
\|c_o-c_p\|\le\frac{33}{32}\sqrt2<\frac32,
\qquad
\frac94-2\left(\frac{33}{32}\right)^2=\frac{63}{512}>0.
$$

Use $D=3/2$. Relative center velocity is at most $2\sqrt2r<3r$, and $1/\sqrt2<3/4$. For
an axis-owner angular radius $ar$ and partner radius $br$, with $a,b\in\{1,2\}$, the
bound becomes

$$
K_{\rm pair}\le r^2\left(\frac32a^2+6a+\frac34(a+b)^2\right).
$$

A wall gap has $K_{\rm wall}\le(3/4)a^2r^2$. Only six constants are needed:

| Gap | Angular multipliers | $K/r^2$ |
| --- | --- | ---: |
| Pair | $(1,1)$ | $21/2$ |
| Pair | $(1,2)$ | $57/4$ |
| Pair | $(2,1)$ | $99/4$ |
| Pair | $(2,2)$ | $30$ |
| Wall | $1$ | $3/4$ |
| Wall | $2$ | $3$ |

The order of the pair multipliers matters because the first square supplies the rotating
axis. A shared derivative row still takes the largest bound among its nonlinear aliases.

With the original rational duals and the original conservative residual convention, all
8,448 checks pass with the exact maximum

$$
c_{\max}=\frac{237880431895517578125000}
{249999999158632916515561}
=0.9515217307843866\ldots<\frac{20}{21}<1.
$$

The maximum occurs at branch 105, coordinate 31, sign $-1$. All 88 unavailable features
remain unavailable, with exclusion margins exceeding $1/200$; the smallest is
approximately `0.005897503722317347`. The second implementation reconstructs all 1,936
elementary functions and gradients with separate exact arithmetic before checking
branches, residuals, and margins.

The branch systems contain **56 distinct derivative rows** in total; every one of the
128 branches contains 42 distinct rows.
The relevant tied elementary functions number 62, with six alias groups.
A canonical dictionary of the 56 exact rows, their contributing elementary functions and
maximum curvature bounds, plus ordered branch incidence lists, makes the proof easier to
inspect and reduces repetitive data.
The dictionary does not replace the proof that each nonlinear feature maps to the
appropriate rows.

Preserve the order matching each dual weight vector.
Reordering branch rows without applying the same permutation to the weights would
invalidate their interpretation, even if the unordered row set were unchanged.

**Keep A’s warning about common rows.** Exactly 30 rows occur in every branch.
The reconciliation additionally computed their exact rank as 25 over the endpoint number
field, hence an eight-dimensional linear nullspace.
In particular, column 21, the $x$ displacement of witness square 7, is identically zero
in those common rows, so $e_{21}$ is an explicit null vector.
Keeping only those rows cannot provide the present first-order obstruction in all 33
coordinates.

This nullspace is not a family of actual packing motions, and the inequality cone need
not have dimension eight.
It also does not prove that 128 branches are minimal among all possible arguments.
It shows why simply deleting the noncommon rows is not an established simplification.

### S3. Replace the final D4 search by incidence propagation and one distance bound

**Status:** exact finite certificate and separate geometric reconstruction available.
This replaces the final four-survivor bridge only.
[R11][r11]

After the preceding exclusions, the remaining canonical cases are 438, 999, 1462, and
1659\. Assume no $D_4$ view admits a closed-cell assignment with canonical case 438.
Apply a whole-packing half-turn if necessary so that the initial assignment is the
canonical mask for 999, 1462, or 1659. Each of the other three representative views then
has one of six raw masks: those three canonical masks or their half-turns.
There are $6^3=216$ triples for each initial canonical source, hence 648 combinations.

Use the four normalized views

$$
g_0(x,y)=(x,y),\quad g_1(x,y)=(1-x,y),\quad
g_2(x,y)=(1-y,x),\quad g_3(x,y)=(y,x).
$$

These four views and their compositions with the half-turn exhaust $D_4$. The verified
cell involution accounts for that half-turn without assuming any other symmetry of the
irregular cell cover.

A center determines a closed overlay region with one cell label in each view.
Any actual packing induces the corresponding incidence assignment.
Elementary propagation enforces the bijection between its eleven centers and occupied
labels: an owner with only one possible label reserves it, and a label supported by only
one owner forces that owner.
An empty required domain gives a contradiction.

| Initial canonical case | Immediate contradictions | Further propagation contradictions | Surviving triples | Maximum recorded propagation operations |
| --- | ---: | ---: | ---: | ---: |
| 999 | 168 | 47 | 1 | 19 |
| 1462 | 198 | 17 | 1 | 15 |
| 1659 | 196 | 20 | 0 | 7 |

Write $H$ for label half-turn and $J_i$ for canonical case $i$. The 999 survivor has
other-view masks $(J_{1462},J_{1462},J_{999})$. The 1462 survivor has
$(J_{999},HJ_{999},HJ_{1462})$. Its reflected view therefore has raw mask $J_{999}$.
Composing all views with that reflection preserves the hypothesis that no $D_4$ view
admits 438, so the already established 999 contradiction applies.
No symmetry-equivariant boundary tie-break is needed.

For the 999 survivor, two distinct owners are forced into closed regions

$$
R(1,1,11,4)\subseteq[23/50,27/50]\times[0,11/100],
$$

$$
R(2,5,6,9)\subseteq[11/25,14/25]\times[23/100,7/25].
$$

Here $R(a_0,a_1,a_2,a_3)$ is the intersection requiring label $a_k$ in view $g_k$. The
normalized coordinate differences satisfy $|\Delta x|\le1/10$ and $|\Delta y|\le7/25$.
Since the physical scale is $U-1<3$,

$$
d^2\le(U-1)^2\left((1/10)^2+(7/25)^2\right)
<\frac{1989}{2500}<1.
$$

Every unit square contains an open disk of radius $1/2$. Distinct nonoverlapping squares
therefore have centers at distance at least one.
The forced pair is impossible.
The reflected survivor gives the same contradiction, so some view must be case 438.

The independent geometry calculation reconstructs all sixteen cells and all 220 closed
overlay regions, including the eight singleton regions, and verifies the displayed
enclosures and reflection.
The trace consumer checks every one of the 648 records without regenerating it.

**Scope:** the old 1,572-ban inventory also supports earlier conditional arguments for
cases 2175 and 2176. This final-bridge simplification does not delete that earlier
evidence. Preserve those dependencies unless separately replaced.
Likewise, all prior case exclusions remain premises of this bridge.

The newly written trace consumer itself underwent adverse review: an omitted
terminal-view range check in its first draft was found and corrected before B’s archive
was packaged. Authentic traces already used valid indices and did not change.
The delivered consumer rejects malformed views, omitted/duplicated cases, source
mutations, and optimized Python.
This was a repaired defect in a review helper, not a defect in the published proof.

### S4. Reduce the fixed field-certificate family to a minimum of 44

**Status:** all 59 field geometries were freshly replayed in B; the subset and its
fixed-family minimality were checked exactly.

Let $E_j$ be the checked set of cases excluded by field certificate $j$. Among the 59
supplied certificates, exactly 43 have a case that no other certificate in the family
covers. Each of those certificates is therefore mandatory if the entire supplied field
union is to be retained.
Their union has 1,903 cases, missing only case 1456.

One additional certificate covers 1456. Choosing the 167-row certificate `59db0f81…`
rather than the 389-row alternative `7722afef…` gives 44 certificates covering all 1,904
cases. The 43 mandatory witnesses and the missing case also prove that 43 certificates
cannot suffice within this fixed family.

| Quantity | All 59 supplied certificates | Sufficient 44 |
| --- | ---: | ---: |
| Excluded field cases | 1,904 | 1,904 |
| Complete angle rows | 24,373 | 17,963 |
| Ownership checks | 5,877 | 4,233 |

The already retained independent ensemble uses 47 sources; three can be omitted in a new
sufficient selection: `68426a0d…` for mask 1925, `72e06f08…` for mask 246, and
`a323908f…` for mask 1802. Thus the reduction is fifteen relative to the original 59 and
three relative to the retained 47.

At the original baseline-inventory level, 93 top-level certificates admit a sufficient
71-certificate selection: 44 fields plus 27 generic certificates.
Seven generic case conclusions—644, 1698, 1705, 1745, 1833, 1845, and 2158—are already
included in the field union.

**Limits:** 44 is a minimum for these fixed 59 transfer sets, not for every possible
field construction or mixed proof.
The 71 count is not a 71-file source closure.
Shared ancestors, intermediate ownership data, checker inputs, and downstream bindings
must remain or receive independently checked replacements.
B did not freshly replay all 27 generic certificates.
The compact supplement’s field stage checks the exact selection against the 59 recorded
fresh results; it does not rerun those geometries itself.

Integrate the reduced family as a new manifest, with the same exact case union and
checked transitive dependencies.
Preserve the historical manifest and receipt bytes.

### S5. Explain the five-site field charge using ten convex hulls

**Status:** proved mathematical equivalence and a useful alternative checker design.
No triangle-based production checker has replayed the entire field corpus.

Let $\mathcal P$ be five sites and $K$ a nonempty compact convex core.
Every projection interval of $K$ contains the median projection of $\mathcal P$ if and
only if

$$
K\cap\operatorname{conv}(A)\ne\varnothing
\quad\text{for every }A\subset\mathcal P\text{ with }|A|=3.
$$

There are ten such hulls, which may be triangles, segments, or points.
If $K$ misses one, strict separation puts its three sites beyond one endpoint of a
projection interval of $K$, and therefore puts the median beyond that endpoint.
Conversely, if a median is beyond an endpoint, at least three sites are strictly beyond
it, and their hull misses $K$.

Capacity one follows just as directly.
Two disjoint compact convex cores have a separating line in their gap.
At least three of the five sites lie in one of its two closed halfplanes.
Their hull misses the core strictly on the other side, so the two cores cannot both
satisfy every three-site-hull condition.
In the application the cores lie strictly inside different nonoverlapping squares and
are consequently disjoint.
[R4][r4], [R8][r8]

For a translated core $K=x+K_0$, the charged-center set is

$$
\bigcap_{\substack{A\subset\mathcal P\\|A|=3}}
\left(\operatorname{conv}(A)+(-K_0)\right).
$$

For the **polygonal cores used here**, this is a finite convex-polygon construction.
That qualification improves B’s wording: an arbitrary compact convex $K_0$ need not
produce polygons.

This property does not mean that the core contains three sites.
For example, take

$$
\mathcal P=\{(1/2,0),(0,1/2),(-1/2,0),(0,-1/2),(1/2,1/2)\},
\qquad K=[-3/10,3/10]^2.
$$

$K$ contains none of the five sites.
Nevertheless every three-site subset contains two of the four axial sites; their
midpoint is either the origin or a point $(\pm1/4,\pm1/4)$, hence lies in $K$. Every
three-site hull meets $K$, so it earns the median-projection charge.
This gives a small exact illustration of the distinction both reviews ask the paper to
preserve.

### S6. Derive the endpoint polynomial from one closing contact

**Status:** exact rational-function identity, checked before imposing $P(u)=0$;
independently rederived during reconciliation.
[R2][r2], [R12][r12]

The polynomial is more intelligible when introduced as the closing equation of a
rationally parameterized contact family.
Use the construction and notation in Appendix A. Square 2 is $A(x_0,T-1)$; square 10 is
$F(A(\eta_{\rm c}+2,-\zeta))$. Their separation gap along $n=(-s,c)$ is

$$
g(u)=-s x_0+cT-2c+\zeta+\rho-1
=\frac{P(u)}{2u(1-u^4)(1+2u-u^2)}.
$$

The denominator is positive for $9/25<u<37/100$. Thus $P(u)=0$ closes this specific
contact. The other fifteen zero separating-gap identities in the checked sixteen-entry
contact list hold identically before using $P(u)=0$. Introduce the family, derive this
one equation, isolate the root, and then give the finite feasibility checks.

Root uniqueness also has a short elementary certificate.
Exact endpoint signs are opposite, and termwise derivative bounds give

$$
P'(u)\ge\frac{10398878171521}{2500000000000}>4
\quad\text{on }[9/25,37/100].
$$

The root therefore exists uniquely there.
The available irreducibility calculations additionally confirm degree eight.
Neither the closing equation nor irreducibility replaces the global lower-bound
argument; they explain and validate the attaining construction.

### S7. Finish with a short endpoint lemma and a scoped uniqueness corollary

**Status:** the rigid-map deduction is correct; the inspected global statements admit
$S\le T$. No limiting or compactness argument is required.
[R2][r2], [R10][r10], [R18][r18]

Take a hypothetical packing in side $S\le T$ and place its entire container
concentrically in the cap of side $U$. Apply the container symmetry selected by the
global reduction. Conditional on the complete valid exclusion and capture ensemble, its
poses enter the near state and then the local rectangle under the declared labeling.

For field centers, the conversion to fixed-$T$ physical centers is

$$
p_T=Q^{-1}\left(p_f/B-(U/2,U/2)\right)+(T/2,T/2).
$$

Undoing the scale restores unit squares.
The remaining transformation is rigid and maps the side-$S$ container to

$$
[(T-S)/2,(T+S)/2]^2\subseteq[0,T]^2.
$$

Thus the packing is genuinely feasible in the fixed-$T$ container and lies in the local
rectangle. Local isolation makes it the exact witness.
If $S<T$, the witness’s horizontal span $T$ is already impossible.
The two squares $A(0,0)$ and $A(T-1,0)$ give that span immediately; both coordinate
spans need not be invoked.

An arbitrary packing in the cap $U$ need not become feasible in $T$ under this rigid
transformation. The reason it does here is the premise $S\le T$. Both reviews correctly
identify this distinction.

When $S=T$, a global square symmetry $G$ followed by capture alignment acts as

$$
p\longmapsto(T/2,T/2)+Q^{-1}G\bigl(p-(T/2,T/2)\bigr).
$$

Since $Q^{-1}G\in D_4$, the same universal premises imply uniqueness of the optimal
physical packing up to the eight container symmetries and square relabeling.
Quarter-turn reparameterizations of an individual square represent the same physical
square and should not be counted as additional configurations.

The article may state this corollary with the same evidence scope, or explicitly defer
it. Declining to make the stronger claim does not invalidate its optimality theorem.

## 6. Third priority: clarity and presentation

### 6.1 Organize the main proof by mathematical dependencies

Use three conceptual levels: the general geometric rules, a fully quantified universal
capture proposition, and the endpoint theorem.
Within those levels, a useful five-lemma reading order is:

1. **Attainment:** the exact witness is feasible at $T$, and one closing contact
   explains $P(u)$.
2. **Global exclusion:** the center cover is exhaustive; pointwise pose preservation,
   ownership, and field capacity justify the exact excluded set.
3. **Symmetry:** simultaneous closed-view incidence and one distance obstruction force a
   case-438 view.
4. **Capture and inclusion:** the complete closed partition and verified transitions put
   every surviving packing into the stated rectangle with the exact role and frame map.
5. **Local isolation:** feature completeness, the two-radius box, and the weighted
   residual-curvature lemma leave only the witness at fixed $T$.

Then give the endpoint deduction in one paragraph.
This organization is consistent with the project’s existing simplification
recommendations; it should not be presented as a newly invented proof technique.
Move historical execution chronology, large manifests, code provenance, and rating
history to a verification appendix.
Keep a short execution-scope notice beside the first theorem.
[R19][r19]

The capture proposition should explicitly quantify over every valid packing with
$S\le T$, identify allowed symmetries and relabeling, specify the closed branches, state
the source and target frames, and print the target rectangle.
“All relevant cases passed” is not a substitute for that proposition.

### 6.2 Put the frame legend early

| Object | Meaning and units |
| --- | --- |
| $p$ | Physical center in the side-$U$ cap; each small square has side 1 |
| $z=(p-(1/2,1/2))/(U-1)$ | Normalized center-cover coordinate in $[0,1]^2$ |
| $p_f=Bp$ | Field center; cap side $191/50$, small-square side $B$ |
| $y_i$ in capture branch conditions | Centered physical height of capture owner $i$, using that condition’s declared axis convention |
| $t_i$ | Real half-angle coordinate $\tan(\theta_i/2)$ in the declared orientation chart; certified row endpoints are rational |
| $h_{3k},h_{3k+1}$ | Physical center displacements of local witness label $k$ |
| $h_{3k+2}$ | Angular displacement in radians of local witness label $k$ |
| $p_T$ | Rigidly aligned physical center in the fixed side-$T$ container |

Print the local-to-owner map beside this legend or the inclusion proposition.
Explain that equivalent orientation charts at the axis seam must still enclose the same
physical angle.
The inspected consumer handles the conversions; the article should expose
enough convention to let a reader verify the composition.
[R10][r10]

### 6.3 Include one actual field-certificate example

The mask-0 certificate provides a compact worked example of the difference between a
certificate’s mathematical proposition and a PASS label.
Its source is `14164a3d91117055000ae78cd15a4e8ad5d6bb2c27ce24ff080605b873a93340`. The
initial occupied mask contains labels $\{0,1,2,3,4,5,6,7,8,9,10\}$, and its required
owner set is $\{0,1,2,3,6\}$.

There is one physical five-site median feature of weight 1, with all point weights zero.
Its total capacity budget is 1. The verified per-cell thresholds are 1 in cells 1 and 2
and zero elsewhere. Thus an admitted packing would have total charge at least $1+1=2>1$,
a contradiction.

For a representative row, cell 1, row 0 has the closed half-angle interval $[0,1/64]$.
Its exact domain cover proves that either the inner core activates median feature 931,
or it contains one of three points strictly owned by another occupied square: owner 0
point 5, owner 0 point 6, or owner 2 point 7. In a valid packing the latter alternatives
cause an interior collision.
Consequently the physical feature must be active throughout that legal row and its
charge is at least 1.

The complete checked certificate has 55 ownership points and 136 closed rows—67 for cell
1 and 69 for cell 2—and transfers to 459 canonical cases after allowing the
whole-packing half-turn.
The collision alternatives are logical exclusion devices; they do not add to the
physical budget. This example illustrates an actual checked row.
Its bound input supplies the large exact core and polygon data; this paragraph alone
does not reproduce their geometric coverage calculation.
[R8][r8]

### 6.4 Make the remaining edits concrete

| Article location | Recommended edit | Purpose |
| --- | --- | --- |
| First theorem | State observed component execution, retained composition, and the outstanding complete fresh-run boundary | Prevents reading the theorem’s evidence level from a status label alone |
| Historical introduction | Shorten lower-bound lineage and move detailed tool comparisons into notes | Keeps motivation separate from the equality’s actual premises |
| Center-cover lemma | State that every realized closed-cell assignment in every view is subject to the exclusions | Makes boundary choices and overapproximation legitimate |
| Pose-preservation lemma | Add the pointwise angular invariant and its induction | Matches the branch restriction’s actual contract |
| Coverage discussion | Name the singleton defect, full-dimensional closure defense, and degenerate dispatch separately | Avoids the false assertion that positive area makes every slice nondegenerate |
| Field section | Add the missing capacity/strict-budget lemma and correct the original-proof citation | Makes the cited mathematical argument complete |
| Final symmetry section and Figure 8 | Show the two forced overlay regions and their simple rational boxes | Lets the figure carry the actual simplified contradiction |
| Capture section | Distinguish the four closed mathematical branches from the ten-node execution graph | Separates branch exhaustiveness from ancestry verification |
| Local section | State the OR-of-AND feature logic, abstract isolation lemma, and two-radius box | Makes the local theorem’s hypotheses visible |
| Local appendix | Use the six-entry curvature table and canonical row dictionary | Removes repeated bounds while retaining alias maxima and all unavailable features |
| Inclusion section | Print the role map, radian convention, and centered physical bridge formula | Prevents correct formulas being applied in the wrong frame |
| Numerical appendix | Give exact sites/radii, margin identities or reproducible formulas, and artifact identities | Avoids dependence on rounded displays or reverse-engineering code |
| Reproduction guide | Provide portable explicit input/output commands and separate verification modes | Makes clean reproduction an operationally defined task |
| Status references | Label historical grading epochs and link one authoritative current scope record | Prevents rating-scale migration from looking like mathematical disagreement |

The paper and validation guide use S5/V3/C3, while linked historical acceptance records
use V4/C5. The repository’s policy explains the scale migration.
Preserve historical labels as historical, and provide a short translation or epoch
notice. No rating proves that a checker ran, that its mathematics is sound, or that
distinct human-review requirements were met.
[R3][r3], [R4][r4], [R13][r13]

The retained local replay script contains an author’s mounted path and a
Homebrew-specific timeout command; the underlying checker itself ran successfully in B’s
environment. Preserve that script as history but provide an ordinary portable invocation
with declared dependencies and directories.
[R14][r14]

The earlier review inspected the figures’ mathematical content, captions, and SVG
structure. It did not conduct a browser-based stylesheet or typography audit.
The suggested figure change is mathematical and explanatory, not a claim that a visual
layout defect was observed.

## 7. Suspected objections that were resolved

The following safeguards should survive any shortened exposition:

| Suspected objection | Checked resolution and remaining hypothesis |
| --- | --- |
| $U>T$ leaves an unproved numerical gap | $U$ is a classification cap. The same hypothetical side-$S\le T$ packing is rigidly placed in $T$ after unscaling; the exact sign $T<U$ is checked. |
| Field scaling changes only the container | Both centers and small squares scale by $B$; dividing by $B$ restores physical unit squares. |
| A cell label makes a site owned by its square | Cell membership and strict ownership are different propositions. Ownership needs its own valid-packing proof. |
| A median charge means containing three sites | The charge is projection-based, equivalently intersection with each three-site hull. Section S5 gives an example containing no sites. |
| Closed Minkowski boundaries may exclude legal square contact | The intersecting core and owned hull are both strict inner sets. Their shared point is in both square interiors. Ordinary non-strict containment would not suffice. |
| One favorable partner pose justifies a universal collision | The collision must hold for every live partner row and every possible center in it; the inspected primitive requires nonempty partner coverage. The caller must preserve completeness of that cover. |
| The partner support bound should use a maximum | Intersecting collision regions over possible partner centers produces the minimum support bound appropriate to the universal quantifier. Substituting a maximum uses the wrong quantifier and can make the exclusion unsound. |
| Irregular cover cells must be permuted by every symmetry | Simultaneous closed-cell overlays record independent labels in each view. The proof uses an overinclusive incidence problem, not a nonexistent full symmetry of the original tessellation. |
| Boundary assignments need a symmetry-commuting tie-break | Every actual closed assignment is subject to the exclusions. Independent containing labels in different views still give an included overlay region. |
| Positive-area or sampled coverage automatically proves all boundaries | Complete arrangement/closed-set arguments are needed; lower-dimensional domains use exact point/segment checks. A finite arbitrary sample is insufficient. |
| Local analysis assumes a fixed contact graph or common orientation | Global angles are independent. Locally all relevant separating features are enumerated and all 88 discarded features are excluded on the full rectangle. |
| Infinitesimal rigidity is being used as finite isolation | The curvature and residual bounds apply to an arbitrary nonzero finite displacement, including the rectangle boundary. |
| Equal gradients permit identifying the nonlinear constraints | Only derivative rows are shared; the maximum curvature over all nonlinear aliases is retained. |
| Cases 2175 and 2176 depend circularly on the final exclusions | Their admitted premise is the earlier 1,931-case baseline, explicitly separated from later conclusions. B’s finite necessity checks remain conditional on that baseline. |
| Historical lower-bound papers are unstated numerical premises of equality | They motivate the work; the final exact argument uses its listed present obligations. Their entire historical corpora were not required to derive the endpoint implication. |

As additional historical checking, B ran the standalone T-025 verifier: 181 directions,
584 point atoms, 320 threshold atoms, minimum charge $100000203/100000000>1$, and budget
$685457679/62500000<11$. The separate 1,441-direction T-026 certificate and Kleddamag’s
full lower-bound package were not freshly replayed.
This extra check should remain distinct from the required T-060 proof closure.

## 8. Recommended acceptance and integration work

### 8.1 First: mathematical contracts and a reproducible release

1. State the pointwise angular invariant, spatial-degeneracy contract, feature
   conjunction, and valid-packing ownership quantifier.
   Add the field-capacity/strict-budget lemma to the original proof and correct the
   citation.
2. Pin the article, original proof, checker modules, dependencies, and all input
   objects. Publish the old-to-new report for the four corrected state bindings.
3. Implement checked semantic parent admission while retaining verified transition
   ancestry, conditions, roles, frames, endpoints, and rule identities.
   Test accepted timing variation and refused mathematical mutations.
4. Supply a declared transitive dependency closure and separate commands for integrity,
   retained composition, and fresh geometry.
   Counts of top-level certificates are not counts of required input files.
5. Execute the complete advertised proof from a clean relocated environment with no
   undeclared local cache, after verified input acquisition.
   Report which work was executed, validly resumed, or consumed only as retained
   evidence. Include negative controls for missing cases, wrong states, changed sources,
   and lost endpoints.

These steps target a clean independently reproducible executable release.
The success of B’s smaller component supplement does not already meet the full-global
replay requirement.

### 8.2 Second: adopt the specific checked simplifications

Integrate the final D4 incidence/distance certificate, the two-radius/six-constant local
theorem, and the 44-field manifest as newly identified components.
Recheck the exact case unions, branch assumptions, source-state joins, owner roles,
angle units, and endpoint identities.
Preserve earlier D4 dependencies and shared ancestors.
Keep the historical evidence bytes unchanged.

Use the weighted-residual lemma and canonical row dictionary to simplify the local
exposition. Retain all branch alternatives and negative-feature checks unless a
separately verified argument replaces them.
Explain the polynomial through its closing contact.
The ten-hull characterization is ready as mathematics; a new production checker based on
it still requires implementation and object-backed comparison.

### 8.3 Third: strengthen independent assurance and presentation

An independent global closed-set/transition implementation and bound-object replay would
address a remaining common-mode risk more directly than further wrappers around shared
primitives. A’s absent local archive may also be acquired and checked if its claimed
independent generation is to be counted as available evidence.
Verify its source snapshots, exact weights, acceptance code, and mutations; reconstruct
any local cache from source rather than treating an externally supplied serialized cache
as trustworthy.

Reorganize the article around the mathematical lemmas, print the exact interface tables,
include the worked field row, distinguish mathematical branches from execution nodes,
and translate historical rating labels.
Decide explicitly whether to state the conditional uniqueness corollary.
These changes make the existing argument shorter and easier to audit while keeping its
unresolved execution scope visible.

### 8.4 Standalone handoff for the next implementation agents

This document is the complete review brief.
The earlier reviews are retained as provenance; they do not need to be read to
understand any finding or proposed change.
Paths below are relative to the named repository at the pinned revision in Appendix B.
The article is generated from
`jlevy/squares/packing/devtools/templates/n11-optimality-review-article.md`; update that
source and use the project’s established generation workflow so the published article
and its template agree.

Reproduce the baseline at those pins first.
If integrating into a newer revision, compare the relevant code and proof statements
against this baseline before assuming a finding still applies unchanged.

| Work item | Main targets | Required result and acceptance evidence |
| --- | --- | --- |
| H1. Repair pose and ownership statements | Article template; original `PROOF.md` §5; review-side `check_n11_capture_child_node.py::conditional_view` and root/transition consumers | State the every-applicable-row invariant, justify seam restriction, and limit ownership to valid packings. Preserve the artificial counterexamples as explanations of why the weaker/stronger alternatives fail. No claim that an accepted packing counterexample was found. |
| H2. Consolidate closed coverage | Review-side `check_n11_optimality_field_mask0.py::covers_vertical`, `n11_fast_exact_cover.py`, `n11_indexed_exact_cover.py`, and `check_n11_closed_degenerate_cover.py`; their capture/generic callers | Correct singleton behavior in a newly identified kernel, preserve full-dimensional and degenerate contracts, and run the 12,180 interval controls plus exact point/segment/seam/gap cases. Inspect caller assumptions; retain original historical source bytes. |
| H3. Supply the field proof and example | Original `PROOF.md` §§5/12; article field section; mask-0 and general field consumers | State definition, capacity, whole-angle lower bounds, required-owner transfer, and strict budget. Correct the citation and explain the actual mask-0 $2>1$ example. The exact checked field union stays 1,904 cases. |
| H4. Publish the simplified local component | Article local section and appendices; local isolation/dual consumers; proposed two-radius checker and row dictionary in the evidence archive | State S1/S2, preserve row/weight order and curvature maxima over aliases, check all 128 branches, all 8,448 signed-coordinate obligations, and all 88 unavailable features. Verify that inclusion’s 33 radii lie in the new box. Give new code/data/result identities. |
| H5. Replace the final symmetry bridge | Article symmetry section/Figure 8; proposed incidence consumer and independent geometry in the archive; existing `check_n11_optimality_d4.py` as comparison | Check all 648 records and the 220 closed regions, including eight singletons, then the exact one-pair distance bound. Preserve the earlier baseline-dependent uses of the original distance-ban inventory. |
| H6. Reduce certificate selection | New field/baseline manifests; `minimal-44-field-manifest.json` and `verify_field_subset.py` in the prior supplement | Retain exactly the same 1,904 field conclusions and the relevant 1,931-case baseline. Check 43 mandatory witnesses plus case 1456 and the transitive dependency closure. Do not interpret 71 top-level certificates as permission to delete all other raw inputs. |
| H7. Repair public reproduction | Original runner/publication guide; source-graph bindings; child admissions; `inventory_n11_completion.py`, `check_n11_final_composition.py`, and `n11_composition_joins.py` | Recompute the four changed bindings, implement reviewed semantic parent admission, separate verification modes, and supply a clean relocated full-run command. Timing-only changes are admissible only after checked semantics/ancestry; changed mathematical assumptions are refused or reverified. |
| H8. Complete presentation and endpoint scope | Article template, exact parameter appendix, status links, capture diagram, and endpoint section | Use the five-lemma structure, exact role/frame tables, four-branch versus ten-node distinction, closing-contact equation, and stated $S\le T$ scope. Decide explicitly on uniqueness; preserve its dependence on the complete global ensemble. |

H1–H3 and the source-backed explanatory edits can proceed while the replay interface is
repaired. H4–H6 are specific checked replacements ready for integration with new
identities. A final acceptance claim for a newly reproduced whole proof depends on H7’s
complete execution and all required state joins, not on completion of the editorial work
or the component archive alone.

The evidence archive contains the proposed checkers, the canonical row dictionary, exact
local inputs/results, the field-selection manifest, source-bound coverage controls, and
both original reviews.
Its README distinguishes recorded evidence from commands that perform new checks.
The full large global corpus remains a source-project dependency.
If an implementation changes a mathematical hypothesis, interval endpoint, branch, alias
map, or source-state admission, identify and rerun every downstream obligation affected
by that change rather than retaining an old success status.

## Appendix A. Exact parameters and conventions

### A.1 Construction and square labels

For the root $u$ and endpoint $T$ defined in section 3, put

$$
c=\frac{1-u^2}{1+u^2},\qquad s=\frac{2u}{1+u^2},\qquad
\rho=1-(T-3)c,
$$

$$
\eta_{\rm c}=\frac{(1+\rho)c-1}{s},\qquad
v=c-s,\qquad
\zeta=\frac{T-1}{s}-\rho-\frac{(3+\eta_{\rm c})c}{s},\qquad
x_0=1+\frac2c-\frac{(T-2)s}{c}.
$$

The construction parameter written $\eta$ in the source is denoted $\eta_{\rm c}$ here
to distinguish it from the residual bound in S1. Let $A(a,b)$ be the axis-aligned unit
square with lower-left corner $(a,b)$, and define

$$
F(x,y)=\bigl(1+cx-s(y-\rho),\ 1+sx+c(y-\rho)\bigr).
$$

Because $c^2+s^2=1$, $F$ is a rigid rotation and translation.
The exact construction and its capture roles are:

| Local witness label | Square | Capture owner |
| ---: | --- | ---: |
| 0 | $A(0,0)$ | 3 |
| 1 | $A(T-1,0)$ | 15 |
| 2 | $A(x_0,T-1)$ | 8 |
| 3 | $A(0,T-1)$ | 0 |
| 4 | $A(1,T-1)$ | 4 |
| 5 | $A(0,T-2)$ | 1 |
| 6 | $F(A(0,0))$ | 2 |
| 7 | $F(A(\eta_{\rm c},-1))$ | 11 |
| 8 | $F(A(1,v))$ | 9 |
| 9 | $F(A(\eta_{\rm c}+1,v-1))$ | 10 |
| 10 | $F(A(\eta_{\rm c}+2,-\zeta))$ | 13 |

This specifies the attaining geometry and the role interface needed for the reviewed
local theorem. Feasibility still requires the finite containment and separation checks
recorded in the evidence ledger.
[R10][r10], [R12][r12]

### A.2 The published 33 local radii

Each row lists physical $x$ and $y$ radii and an angular radius in radians, in local
witness-label order.
These values are the ones printed in A and bound by the published pose-inclusion result.
Exact comparison during reconciliation found all 33 equal to the pinned values.
[R10][r10]

| Label | $r_x$ | $r_y$ | $r_\theta$ |
| ---: | ---: | ---: | ---: |
| 0 | $18767167/10000000000$ | $4435327/2000000000$ | $5670363/2500000000$ |
| 1 | $1636033/1000000000$ | $6880181/5000000000$ | $1764113/1000000000$ |
| 2 | $8962451/10000000000$ | $5212397/5000000000$ | $5670363/2500000000$ |
| 3 | $1635053/1000000000$ | $10683139/10000000000$ | $1890121/1250000000$ |
| 4 | $4087019/2500000000$ | $13962901/10000000000$ | $20161291/10000000000$ |
| 5 | $12900283/10000000000$ | $534153/500000000$ | $1890121/1250000000$ |
| 6 | $678279/500000000$ | $4124329/5000000000$ | $35312013/10000000000$ |
| 7 | $11182451/10000000000$ | $3232837/5000000000$ | $8824483/2500000000$ |
| 8 | $9356857/10000000000$ | $8671199/10000000000$ | $7549783/5000000000$ |
| 9 | $293551/400000000$ | $10335557/10000000000$ | $40352153/10000000000$ |
| 10 | $1920157/2500000000$ | $8222903/2500000000$ | $67647473/10000000000$ |

The recommended replacement is $1/256$ for every entry except the angular radii of
labels 9 and 10, which are $1/128$. Every listed entry is no larger than its
replacement. This inclusion alone does not prove isolation of the larger box; the two
exact local checks in S2 establish that additional conclusion.

### A.3 A compact exact sixteen-cell cover specification

All sites below are in normalized center coordinates.
Divide each listed integer pair by $2,000,000$. The remaining eight sites are specified
exactly by $q_{15-i}=(1,1)-q_i$ for $0\le i\le7$.

| Site $i$ | First integer coordinate | Second integer coordinate | Reflected site |
| ---: | ---: | ---: | ---: |
| 0 | 209982 | 265837 | 15 |
| 1 | 746404 | 91006 | 14 |
| 2 | 1267243 | 277512 | 13 |
| 3 | 1731123 | 205608 | 12 |
| 4 | 206181 | 800758 | 11 |
| 5 | 742311 | 625866 | 10 |
| 6 | 1270514 | 832045 | 9 |
| 7 | 1781756 | 671052 | 8 |

Define the closed cell

$$
V_i=\{z\in[0,1]^2:\|z-q_i\|^2\le\|z-q_j\|^2
\text{ for every }j\}.
$$

The inequalities are linear after subtracting squared norms.
Nearest-site existence makes the closed cells cover $[0,1]^2$. The physical map for the
present cap is $p=(1/2,1/2)+(U-1)z$. The exact cell checks establish diameter less than
one after that map, so a cell cannot contain two distinct unit-square centers.
The half-turn sends $V_i$ to $V_{15-i}$. [R11][r11]

For case IDs, enumerate eleven-label subsets lexicographically and replace each by the
lexicographically smaller of itself and its half-turn; sort the resulting distinct masks
and index them **starting at zero**. This fixes the 2,184 canonical indices used in the
report. The cover object also contains a coarser side-upper metadata value
$969271/250000$; the independent check used in the reviewed final bridge directly
verifies the needed geometry at the exact rational cap $U$.

The cover input’s SHA-256 is
`df7938d9ba27095a38fabe45f8b26b259a2cc896c2ae4aac6bae874f417adc4e`; the four-view
overlay input’s is `845b5f748843dd60fa7e290a5ea1a304da4e439ae229bd73a841aec816f4e700`.
The compact specification supplies mathematical data, while the available checker
verifies their claimed cell/overlay properties.

## Appendix B. Reproduction and evidence identities

### B.1 Source snapshots and the two input reviews

| Item | Exact identity |
| --- | --- |
| Original proof repository | `Queuingtheorydotcom/11SquaresOptimal` |
| Original commit | `f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c` |
| Original Git tree | `3fed944c5a0c1dda5e61cb9f45f0dd3d4dc6360c`, independently confirmed from the commit object during reconciliation |
| Review-side repository | `jlevy/squares` |
| Review-side commit used for B and reconciliation | `ea0a3b19a70085683c3b65946cded03ffe4e2415` |
| Exact requested article snapshot | 153,686 bytes; SHA-256 `428da02fd5b99a6133736113e564097e9281aae213076265f968ceefd4bd3d68` |
| Review A input | 36,874 bytes; SHA-256 `e911c70cd3e1834661e0d07a0fca358022c797e59487dbaa0ee8bf3635dc7438` |
| Review B input | 59,547 bytes; SHA-256 `e5333e518b2e872f1786981dbb501da3a261d1072ee4169b26e86f2260db07d1` |

A states that it read the rendered HTML and generating template after its Markdown
transport failed. B obtained the requested Markdown directly.
Template placeholders were not treated as defects in the published article.
A’s review-side `main` references remain mutable provenance; this report does not
retroactively give A an immutable checkout it did not identify.

A describes a single-assistant audit and a repeat execution of the same new checker.
B used six parallel reviewers, with implementation independence claimed only for the
separately identified programs.
Reviewer count itself is not an arithmetic-independence argument.

A reports that binary/LFS acquisition failed through its available route.
B acquired substantial input objects.
This is a difference between audit environments, not evidence that the public data do
not exist.

### B.2 Newly performed reconciliation checks

| Check | Result | Exact scope |
| --- | --- | --- |
| A’s 33 printed radii against pinned inclusion and focused inputs | All equal; all fit in B’s replacement box | Transcription and enclosure check, not replay of A’s new weights |
| Historical and corrected interval predicates | 12,180 cases; 616 historical false accepts, all singleton targets; zero corrected errors | Actual pinned functions compared against an independent endpoint/midpoint oracle |
| Positive-area triangle control | Historical endpoint predicate falsely accepts; full historical sweep refuses at $x=1/2$ | Demonstrates the distinction between helper error and full-cover result |
| Closed seams and $10^{-50}$ gaps | Exact seams accepted and positive gaps refused | Positive-area, point, and segment controls; not an arbitrary-angle sample |
| Pinned cover and listed polygon order | Sixteen reconstructed cells; positive area and convex vertex order checked | Small source-contract check, not a new full overlay/global replay |
| Original publisher V9 small controls | Closed-boundary behavior agrees on the tested cases | Separate original helper executions with recorded imported-source closure |
| Local branch structure | 128 branches of 42 rows; 56-row union; 30-row intersection | Exact reconstruction of the available pinned systems |
| Common-row rank | Rank 25, nullity 8, explicit $e_{21}$ and eight checked basis vectors | Algebraic nullspace, not actual packing motions or a branch-minimality theorem |
| Direct weighted residuals on B’s weights | All 8,448 checks pass on each rectangle | No new dual generation; certified coefficient-wise residual enclosures |
| Closing-contact identity | Exact rational-function identity and $P'>4$ bound rederived | Construction explanation, not new global exclusion |
| Original Git tree | A’s stated tree matches the pinned commit object | Source provenance only |

The interval enumeration uses all 28 closed intervals with endpoints in
$\{-3,-2,-1,0,1,2,3\}$. Cover families contain zero, one, or two such intervals, with
unordered repetition allowed, giving $1+28+\binom{29}{2}=435$ families and
$28\cdot435=12,180$ tests.
This freshly reproduces A’s reported aggregate counts without its missing code.
Finite tests do not replace the general sweep/closure proof.

The controlled local comparison also holds B’s weights and published radii fixed while
tightening only the radical curvature bounds to checked upper bounds on a $10^{15}$
grid. It gives maxima about `0.6764635933318807` using the old residual and
`0.6764635896668644` using direct weighting.
This demonstrates that curvature conservatism can account for essentially the visible
A/B difference. It does not identify A’s missing implementation settings.

### B.3 A’s local execution claims that remain unavailable

A reports 8,448 newly generated rational duals, a verify-only replay without an LP
solve, and maximum exact ratio

$$
\frac{24251087101573907634681435939000000000}
{35849803998164131953538679451950587687}
\approx0.6764635896702756.
$$

It reports a weighted value near `0.676463589644483`, a maximum residual enclosure near
`1.3216954749443503e-11`, and a least favorable unavailable-feature Taylor upper bound
near `−0.012636021136276269`. The displayed fraction has the stated decimal and is less
than one, but that arithmetic fact does not verify the 8,448 missing certificate
instances.

A also reports seven rejected malformed local inputs: missing certificate, duplicate
certificate, negative weight, zeroed dual, changed radius, changed matrix scale, and
changed curvature scale.
Its stated programs import no repository modules, derivative matrices, or publisher dual
weights; SymPy performs algebraic operations, SciPy/HiGHS proposes weights, and
integer/Fraction arithmetic decides acceptance.
These are descriptions of A’s unavailable implementation and executions.
They are not promoted to observed facts by this reconciliation.

Its described archive excludes a local pickle cache, refuses optimized Python, and
explicitly leaves `global_optimality_verified` false.
If that archive is later provided, check the exact sources and weights, reconstruct
required caches, run verify-only acceptance and the advertised controls, and retain its
explicit global-scope limitation.
A second run of the same checker is not a second implementation.

### B.4 The available Review B supplement

The previously delivered `n11-optimality-review-supplement.zip` remains the evidence
package for B’s principal replacement components.
Its full component run was tested from a relocated directory with spaces in its path and
working directory `/tmp`. All eleven stages passed in the recorded 29.269 seconds:

| Stage | Entry point |
| --- | --- |
| Endpoint/cap comparison | `independent_endpoint_check.py` |
| Short cap certificate | `independent_cap_short_certificate.py` |
| Parameter irreducibility | `independent_irreducibility.py` |
| Side-polynomial irreducibility | `independent_side_irreducibility.py` |
| Exact witness | `independent_exact_witness.py` |
| Closing-contact identity | `independent_witness_simplify.py` |
| Read-only final D4 trace | `verify_d4_review.py` |
| Independent D4 geometry | `d4_independent_geometry.py` |
| Simplified local proof, first implementation | `local-isolation-audit/verify_simplified_local.py` |
| Simplified local proof, second implementation | `second_review_simplified_local.py` |
| Minimum 44-field selection | `verify_field_subset.py` |

The driver reports `PASS_REVIEW_SUPPLEMENT_COMPONENTS`. It verifies all 118 immutable
identities before and after execution and leaves the supplied D4 trace unchanged.
ZIP CRC and every archived byte were checked; optimized Python and a modified source
were refused. Its scope is explicitly:

```json
{
  "whole_global_proof_replayed": false,
  "field_geometry_rerun": false,
  "d4_trace_regenerated": false
}
```

The false field-geometry flag describes this compact command, not the earlier all-59
geometric audit. The compact field stage consumes the 59 recorded fresh receipts and
verifies transfer sets, the union, selection, and minimality witnesses.

| Archive item | Value |
| --- | --- |
| Compressed bytes | 5,879,321 |
| Archived files | 144 |
| Uncompressed bytes | 41,223,316 |
| Immutable manifest entries | 118 |
| Archive SHA-256 | `4f9065c61fa188b74d124912f4213677492b21330e3753c89d34214395bb7536` |
| Source-manifest SHA-256 | `be0e69e6b03832be13fa0b03af9b45063e096917e6c1c665cff3447561be4965` |

The archive includes the exact article snapshot as `reviewed-paper.md`. From its
extracted directory, the tested workflow is:

```bash
python3 -m venv ../n11-review-env
../n11-review-env/bin/python -m pip install -r requirements.txt
../n11-review-env/bin/python -B verify_review.py
```

Use the appropriate interpreter path for the platform and keep the environment outside
the supplement.
The tested versions were Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, SymPy
1.14.0, and mpmath 1.3.0. Verification makes no network requests.
`verify_review.py --hashes-only` checks input integrity without mathematical replay.

### B.5 Evidence for this reconciliation

The companion `n11-optimality-unified-review-evidence.zip` supplies the new checkers,
source closures, exact results, and canonical local dictionary.
It also preserves all 144 members of B’s original archive byte-for-byte under
`prior-supplement/`, and both input reviews under `source-reviews/`. The unified
Markdown is delivered separately so it can be handed to the next agents as one complete
review brief.

The default driver runs three new stages: review-side coverage controls, publisher
coverage controls, and local reconciliation on B’s retained weights.
It verifies immutable inputs before and after, compares both coverage JSONs exactly, and
compares the local JSON and canonical dictionary exactly except for the measured local
runtime. All three stages passed from a relocated directory with spaces, invoked from
`/tmp`, in 42.563 seconds.

| Evidence archive item | Verified value |
| --- | --- |
| Filename | `n11-optimality-unified-review-evidence.zip` |
| Compressed bytes | 6,086,828 |
| Archived files | 202 |
| Uncompressed bytes | 42,734,989 |
| Immutable manifest entries | 186 |
| Archive SHA-256 | `7a2122ffd677f1c0ab1ac8db5ce8c90783d24b19f6b363f90659abc9cc7be589` |
| Manifest SHA-256 | `9d71dd35d3812a1ce781ba3ffc9dbc68816cd34908bb787e90a1a40db9b17720` |
| Relocated status | `PASS_NEW_RECONCILIATION_CHECKS` |

All four new entry points refused both `-O` and `-OO`. Changed input or manifest bytes
caused refusal; restoring them restored the integrity check.
ZIP CRC and every archived file were checked.
The historical B archive and all its extracted member bytes remain unchanged.

After extracting the new archive, run from `n11-unified-review-evidence/`:

```bash
python3 -m venv ../n11-unified-review-env
../n11-unified-review-env/bin/python -m pip install -r requirements.txt
../n11-unified-review-env/bin/python -B verify_reconciliation.py
```

The environment belongs outside the immutable bundle.
The wrapper resolves its own path and also works when called by absolute path from
another directory.
New outputs go to top-level `fresh-results/`; `--hashes-only` performs
no mathematical replay.
The README gives direct helper commands and dependency details.

To rerun the prior eleven stages without changing the preserved historical subtree:

```bash
cp -a prior-supplement ../n11-prior-supplement-replay
../n11-unified-review-env/bin/python -B ../n11-prior-supplement-replay/verify_review.py
```

Use the corresponding interpreter and copy commands on other platforms.
The two workflows have different scopes.
The **new default** does not run the prior eleven-stage driver, rerun fields, execute
the full global exclusions or capture graph, regenerate the D4 trace, or verify A’s
unavailable new duals.
The **prior driver** checks its listed component replacements and field selection, with
the limits in B.4. Merely including a recorded result in either archive does not attest
that a new execution of it occurred.

For direct local inspection, the portable checker is `reconciliation_local_checks.py`;
the final exact local result and row dictionary are in `recorded-results/`. The checker
SHA-256 is `ab5f84a9fa9c8506975e91ad8d7c0aae3ed62867509f2a259846a11b06614123`, the exact
result SHA-256 is `32d58ca2510440f3ce8f82dd775596fa4f9f672e04edb7ee596000c276920430`,
and the canonical dictionary SHA-256 is
`8f4f426d1746eb0825ee67363506ab864e5b6ca4b6d4b28a0317fcdb2151454c`. The weighted packet
and focused rectangle have respective SHA-256 values
`ffe9f89d40a9538ec9a10d8700999f05483d0ccfad17b84d430590da7dd65889` and
`9a9cf4e0fdcb1b1d226b9c07ec08d08cbbc572749cec9bc09cf3cd92bd4d88f3`.

## Appendix C. Complete finding crosswalk

This table makes the reconciliation auditable without requiring the reader to compare
two differently numbered reports.
A refers to the supplied pro-1 review; B refers to the earlier pro-2 review.

### C.1 Correctness and assurance

| Source finding | Unified location | Disposition |
| --- | --- | --- |
| A C1: historical singleton predicate | C2; Appendix B.2 | Retained and newly reproduced against pinned functions; restricted whole-cover impact explained |
| B C1: angular seam invariant | C1 | Retained separately; stronger invariant already exists deeper in the repository |
| A C2 and B C2: stale publisher bindings | C3 | Merged; preserve B’s fresh near-object identity check and A’s clean-command acceptance test |
| A C3 and B C2: parent receipt bytes | C4 | Merged; semantic admission retains checked ancestry and all mathematical hypotheses |
| A C4: composer scope | C8; sections 3 and 6 | Retained as an assurance boundary, not an undisclosed geometric verifier failure |
| A C5: shared primitives | C8; section 8 | Retained with component-specific independence and a proposed independent global kernel |
| B C3: original field lemma and citation | C5 | Retained; field rule itself survives and all 59 instances were checked in B |
| B C4: conjunction within features | C6 | Retained, including safe necessary-system relaxation and unavailable-feature logic |
| B C5: ownership versus outer poses | C7 | Retained with the artificial-pose example and valid-packing quantifier |
| B C6 and A E1: roles/frames | C9; section 6.2; Appendix A | Merged into exact role, coordinate, and unit tables |
| A C6 and B resolved objections | Section 7 and S5/S7 | Preserved with strictness, universal-partner, boundary, and dependency hypotheses |
| A source pin and execution limits | Sections 2–3; Appendix B | Preserved; unavailable local archive distinguished from newly reproduced mathematical/control claims |

### C.2 Simplifications

| Source finding | Unified location | Disposition |
| --- | --- | --- |
| A S1: weighted anisotropic lemma | S1 | Retained, proved, and checked on B’s existing weights; ratio convention made explicit |
| A S2: rules/capture/endpoint levels | Section 6.1 | Combined with B’s five-lemma reading order and existing project attribution |
| A S3 and B S6: uniqueness | Section 2.4; S7 | Scope resolved positively for $S\le T$, conditional on the same global premises |
| A S4: canonical row dictionary | S2; Appendix B.2 | Retained; exact 56-row dictionary and ordered incidence now available |
| A S5: do not keep only common rows | S2 | Confirmed; exact rank 25 and explicit null vector strengthen the warning without claiming branch minimality |
| A S5: no global deletions established by A | Section 2.5; S3–S4 | Treated as A’s scope limitation; compatible with B’s additional specific reductions |
| B S1: final D4 incidence and one distance bound | S3 | Retained with all 648 records, closed overlays, survivor counts, and earlier-ban caveat |
| B S2: two radii and six constants | S2 | Retained with exact inequalities, alias maxima, full feature checks, and both implementations |
| B S3: minimum 44 fields and 71 top-level baseline selection | S4 | Retained with fixed-family minimality, exact unchanged union, and source-closure caveat |
| B S4: ten-hull field charge | S5 | Retained; polygonal-core qualification added, alternative production replay still prospective |
| B S5: one closing contact | S6; Appendix A.1 | Retained and independently rederived; exact root uniqueness included |
| A endpoint section and B S6 | S7 | Combined into centered subcontainer deduction; one span suffices; no compactness needed |

### C.3 Presentation, safeguards, and reproducibility

| Source recommendation | Unified location | Disposition |
| --- | --- | --- |
| A E1: complete coordinate legend | Section 6.2 | Added with actual normalized map and physical/radian distinction |
| A E2: exact sites, role map, and radii | Appendix A | Added; missing inline data treated as auditability issue, not missing external proof input |
| A E3 and B status discussion | Section 6.4 | Historical scale migration explained; labels separated from execution/human/formal assurance |
| A E4: propositions before counts and dependency table | Section 3.2; section 6.1 | Added, including earlier-baseline conditions and independent cover geometry |
| A E5: retain key conceptual distinctions | Sections 4 and 7 | Preserved: cell/ownership, median/containment, sampled/closed intervals, enclosure/contradiction |
| A E5: one worked certificate row | Section 6.3 | Added using an actual mask-0 row and exact $2>1$ budget contradiction |
| B figure and main-text edits | Section 6.4 | Retained, including actual forced regions, four branches versus ten nodes, and figure-audit scope |
| B portable commands and three verification modes | C3–C4, C8; Appendix B.4 | Retained; historical platform-specific script remains provenance |
| A acceptance work and B revision order | Section 8 | Combined into contracts/release, checked replacements, then independent assurance/presentation |
| A Appendix A radii | Appendix A.2 | Retained exactly and freshly matched to pinned data |
| A Appendix B claimed bundle and controls | Appendix B.3 | Recorded with availability limits; no unobserved local run promoted to verified evidence |
| B complete supplement and final relocated run | Appendix B.4 | Preserved with commands, versions, hashes, all eleven stages, and exact scope |
| Historical lower bounds | Section 7 | Historical role and B’s T-025 replay retained; T-026/full Kleddamag replay not claimed |
| New-checker self-audit in B | S3; Appendix B.4 | Corrected draft trace-consumer issue and unchanged valid trace explicitly retained |

## Appendix D. Source register

The original proof links below use commit `f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c`;
review-side code and records use `ea0a3b19a70085683c3b65946cded03ffe4e2415`. The live
article URL is paired with its exact snapshot hash in Appendix B. Source citations
identify material inspected; a source-code link is not a claim that every execution path
was run.

### R1. Review article

- [Requested article, with exact snapshot identity in Appendix B](https://jlevy.github.io/squares/papers/n11-optimality-review.md).
- [Pinned generating article template](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/templates/n11-optimality-review-article.md).

### R2. Original mathematical proof

- [PROOF.md](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/PROOF.md).

### R3. Validation and fresh-replay limitations

- [packing/resources/web/n11-optimality-2026-09-29/VALIDATION.md](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/VALIDATION.md).
- [packing/resources/web/n11-optimality-2026-09-29/README.md](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/README.md).

### R4. Mathematical acceptance and dependency contract

- [docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md).

### R5. Publisher source-binding discrepancies

- [packing/resources/web/n11-optimality-2026-09-29/receipts/source-graph/result.json](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/source-graph/result.json).
- [packing/resources/web/n11-optimality-2026-09-29/receipts/capture-ancestry/refusal-result.json](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/capture-ancestry/refusal-result.json).

### R6. Angular branch restriction and boundary controls

- [packing/devtools/check_n11_capture_child_node.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_capture_child_node.py).
- [packing/tests/test_n11_capture_child_node.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/tests/test_n11_capture_child_node.py).

### R7. Pointwise pose preservation and ownership

- [packing/devtools/check_n11_capture_root_pilot.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_capture_root_pilot.py).
- [packing/devtools/check_n11_capture_root_continue.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_capture_root_continue.py).
- [packing/devtools/check_n11_capture_root_node.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_capture_root_node.py).

### R8. Field rules and complete-angle checking

- [packing/devtools/check_n11_optimality_field_mask0.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_optimality_field_mask0.py).
- [packing/devtools/check_n11_optimality_field_mask202.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_optimality_field_mask202.py).
- [packing/devtools/check_n11_optimality_field_runner.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_optimality_field_runner.py).
- [packing/devtools/check_n11_generic_fresh.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_generic_fresh.py).

### R9. Local isolation and exact residuals

- [packing/devtools/check_n11_optimality_local_isolation.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_optimality_local_isolation.py).
- [packing/devtools/check_n11_optimality_local_dual.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_optimality_local_dual.py).
- [packing/resources/web/n11-optimality-2026-09-29/receipts/local-isolation/result.json](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/local-isolation/result.json).
- [src/evidence/research/global-math/FOCUSED-LOCAL-RECTANGLE.md](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/src/evidence/research/global-math/FOCUSED-LOCAL-RECTANGLE.md).

### R10. Pose inclusion, roles, frames, and accepted radii

- [packing/devtools/check_n11_optimality_pose_inclusion.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_optimality_pose_inclusion.py).
- [packing/resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/result.json](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/result.json).

### R11. Center cover and D4 argument

- [packing/devtools/check_n11_optimality_d4.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_optimality_d4.py).
- [packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json).
- [Exact sixteen-cell cover input](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/objects/df7938d9ba27095a38fabe45f8b26b259a2cc896c2ae4aac6bae874f417adc4e.json).
- [Exact four-view overlay input](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/objects/845b5f748843dd60fa7e290a5ea1a304da4e439ae229bd73a841aec816f4e700.json).

### R12. Exact attaining construction

- [packing/cases/trump11/packing.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/cases/trump11/packing.py).
- [packing/cases/trump11/verify_exact.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/cases/trump11/verify_exact.py).

### R13. Verification ratings and historical scale migration

- [epistemics.md](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/epistemics.md).

### R14. Publication and replay interfaces

- [docs/REPRODUCING.md](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/docs/REPRODUCING.md).
- [docs/PUBLICATION.md](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/docs/PUBLICATION.md).
- [packing/resources/web/n11-optimality-2026-09-29/receipts/local-isolation/replay.sh](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/local-isolation/replay.sh).

### R15. Continuous and lower-dimensional scope

- [src/evidence/docs/V9_CONTINUUM_SCOPE_REVIEW.md](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/src/evidence/docs/V9_CONTINUUM_SCOPE_REVIEW.md).
- [packing/devtools/check_n11_closed_degenerate_cover.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_closed_degenerate_cover.py).

### R16. Retained inventory and final composition

- [packing/devtools/inventory_n11_completion.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/inventory_n11_completion.py).
- [packing/devtools/check_n11_final_composition.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_final_composition.py).
- [packing/devtools/n11_composition_joins.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/n11_composition_joins.py).
- [packing/resources/web/n11-optimality-2026-09-29/receipts/final-composition.json](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/final-composition.json).

### R17. Corrected cover kernels and capture transitions

- [packing/devtools/n11_fast_exact_cover.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/n11_fast_exact_cover.py).
- [packing/devtools/n11_indexed_exact_cover.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/n11_indexed_exact_cover.py).
- [packing/devtools/check_n11_capture_transition_pilot.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_capture_transition_pilot.py).
- [packing/devtools/check_n11_capture_step0.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_capture_step0.py).
- [packing/devtools/check_n11_generic_sequential.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_generic_sequential.py).
- [packing/devtools/n11_nonfield_partner.py](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/n11_nonfield_partner.py).

### R18. Universal capture scope at the endpoint

- [src/evidence/research/candidate-capture/audit_complete_capture438.py](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/src/evidence/research/candidate-capture/audit_complete_capture438.py).
- [PROOF.md](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/PROOF.md).

### R19. Earlier expository simplification review

- [docs/project/reviews/review-2026-09-30-n11-expository-simplification.md](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/docs/project/reviews/review-2026-09-30-n11-expository-simplification.md).

[r1]: https://jlevy.github.io/squares/papers/n11-optimality-review.md
[r2]: https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/PROOF.md
[r3]: https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/VALIDATION.md
[r4]: https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md
[r5]: https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/source-graph/result.json
[r6]: https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_capture_child_node.py
[r7]: https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_capture_root_pilot.py
[r8]: https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_optimality_field_mask0.py
[r9]: https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_optimality_local_isolation.py
[r10]: https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_optimality_pose_inclusion.py
[r11]: https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_optimality_d4.py
[r12]: https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/cases/trump11/packing.py
[r13]: https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/epistemics.md
[r14]: https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/docs/REPRODUCING.md
[r15]: https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/src/evidence/docs/V9_CONTINUUM_SCOPE_REVIEW.md
[r16]: https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/inventory_n11_completion.py
[r17]: https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/n11_fast_exact_cover.py
[r18]: https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/src/evidence/research/candidate-capture/audit_complete_capture438.py
[r19]: https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/docs/project/reviews/review-2026-09-30-n11-expository-simplification.md

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
