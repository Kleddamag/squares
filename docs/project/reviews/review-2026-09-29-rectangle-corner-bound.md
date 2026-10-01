# Rectangle Corner Bound and Pending-Box Review

The per-rectangle corner minimum is a sound lower bound for the existing native
rectangle-density verifier.
It can improve the common-core bound without changing the admitted density, angular net,
target, or packing argument.
This review derives that bound and checks the implementation’s handling of incomplete
work. It does not establish complete native verification of a retained external
certificate.

This is a GPT-6 Astra review at max thinking for **think-wjb2**, within **think-bmf3**.
The implementation lane owns source and tests; the reviewer owns this document.
The review applies the tbd engineering, code-review, Python, testing, golden-testing,
error-handling and filesystem guidance.
The earlier [native contract review](review-2026-09-29-native-rectangle-contract.md)
owns the unchanged D4 reduction, angle-net bridge, exact clipping and mass-admission
argument. The
[implementation plan](../specs/active/plan-2026-09-29-native-rectangle-verification.md)
owns the predeclared target comparison and the remaining whole-certificate work.

## Bound and Proof

Fix a convex rectangle $R$, an oriented square $Q$ centered at the origin, and a center
box $X$ with vertices $v_1,\ldots,v_4$. Write $A_i=R\cap(Q+v_i)$ and $m=\min_i |A_i|$,
where $|\cdot|$ denotes area.
For every $z\in X$,

$$
|R\cap(Q+z)|\ge m.
$$

If $m=0$, nonnegativity proves the assertion, including empty or tangent corner
intersections. Otherwise all $A_i$ have positive area.
Express $z=\sum_i\lambda_i v_i$, with $\lambda_i\ge0$ and $\sum_i\lambda_i=1$. Convexity
of $R$ and $Q$ gives

$$
\sum_i\lambda_i A_i\subseteq R\cap(Q+z).
$$

The planar Brunn–Minkowski inequality therefore gives

$$
|R\cap(Q+z)|^{1/2}
\ge\sum_i\lambda_i |A_i|^{1/2}
\ge m^{1/2}.
$$

This is the rectangle-square instance of Gardner’s
[Theorem 12.1](https://faculty.gardner.wwu.edu/gorizia12.pdf), which states concavity on
the support of the overlap function.
It does not require concavity after extending that function by zero outside its support.
Repeated vertices handle a center box that degenerates to a segment or point.

For the finite admitted density $f=\sum_j\rho_j 1_{R_j}$, each $\rho_j$ is nonnegative.
Consequently

$$
\int_{Q+z} f\ge
\sum_j\rho_j\min_{v\in\operatorname{vertices}(X)}|R_j\cap(Q+v)|.
$$

Each minimum must be taken before summing.
No theorem here treats the full density as log-concave, and none is needed.
The square’s orientation stays fixed throughout one center box; this bound does not
replace the angular-net argument.

Let $P$ be the old common-core polygon.
Since $P\subseteq Q+v$ at every corner, $|R_j\cap P|\le\min_v|R_j\cap(Q+v)|$ term by
term. The new bound therefore dominates the old bound mathematically.
Taking their maximum is safe, and returning the old bound immediately when it already
reaches the target is also safe.

## Analytic Controls

The new improvement control has $L=4$, $B=1/2$, source rectangle $[1/10,39/10]^2$, and
weight $1444/25$. Its D4 images coincide.
The expanded density is exactly $4$, and its mass is $1444/25<58$. At
$(\cos\theta,\sin\theta)=(3/5,4/5)$ and centers in $X=[2,3]^2$, every checking square
lies entirely inside that rectangle: its extent in either coordinate is $7/20$. Coverage
is therefore exactly $4B^2=1$ throughout $X$. The common-core half-widths are both
$-9/20$, so its polygon is empty and its bound is zero.
The corner bound is exactly one.
This is a local geometric control; it does not prove this candidate covers its entire
admissible center domain.

The minimum-of-total trap uses two density-one rectangles, $[3/4,5/4]\times[3/4,5/4]$
and $[7/4,9/4]\times[3/4,5/4]$, an axis-aligned square of side $1/2$, and the center
segment $[1,2]\times\lbrace1\rbrace$. Each endpoint square captures area $1/4$ from one
rectangle. The midpoint square touches both rectangles only along edges, so its captured
area is zero.
Taking the minimum of endpoint total coverage would incorrectly claim $1/4$
everywhere. Taking the minimum separately for each rectangle gives zero.
This control exercises the bound primitive; its two-rectangle density is not a
D4-admitted packing certificate.

The preexisting asymmetric-orbit control checks a distinct eight-image orbit, rational
rotation, common-core containment inequalities and the exact captured mass.
Together these controls distinguish geometric identities from output snapshots.
They do not constitute a proof by sampling; the proof above supplies the universal
center-box statement.

## Implementation and Receipt Contract

The reviewed additions are in
[`rectangle_density.py`](../../../packing/src/sqpack/rectangle_density.py),
[`verify_rectangle_density.py`](../../../packing/devtools/verify_rectangle_density.py),
and
[`compare_rectangle_density_bounds.py`](../../../packing/devtools/compare_rectangle_density_bounds.py).

`_corner_minimum` constructs the four translated squares, clips each density rectangle
against each square exactly, takes that rectangle’s least area, and then adds its
weighted contribution.
It uses the existing rational clipping primitive.
`corner-min` is an explicit verifier mode; `common-core` remains the default.
Admission and the complete 201-angle acceptance rule are unchanged.

Pending-box capture is optional and applies to the rotated subdivision search.
The axis direction retains its exact event-grid procedure and records its stopping cause
without fabricating a box frontier.
Retention is limited by the total requested node budget across angles.
It refuses an oversized request instead of returning a truncated frontier that resembles
a complete one.

The reviewed early exits preserve the following accounting:

- At a node or time limit between nodes, all queued boxes remain unresolved, together
  with previously retained depth-capped leaves.
- If the deadline interrupts a corner sum, its current box and every queued box remain
  unresolved. An incomplete sum is never used to certify that box.
- A depth-capped leaf keeps its exact coordinates, depth and cause while traversal
  continues elsewhere.
- A coverage counterexample keeps the exact point and value.
  Previously unresolved leaves and the other queued boxes remain counted; the box
  containing the decisive counterexample is no longer pending work.

The comparison command requires a retained common-core frontier receipt, reruns that
angle, and matches its exact result before evaluating both bounds on the same boxes.
Its receipt binds candidate bytes, library source, comparison-tool source, the input
receipt and settings; it checks those bytes again before reporting.
It directly refuses a corner bound below the common-core bound.
It separately reports full frontier retention and completion of the bound comparisons.
Its result is always `DIAGNOSTIC_ONLY`, even when every retained box reaches the target.
The pending-box format has no replay or proof-aggregation authority.

The time ceiling is cooperative.
Exact arithmetic already in progress can finish after a clock check.
The corner loop adds checks between rectangles; this is not a hard per-operation
wall-time guarantee.
The full source-bound node census and the number of completed comparisons must therefore
accompany elapsed time.

## Review Findings and Evidence

The initial theorem comment claimed translation concavity without restricting its
support. The implementation lane corrected the comment to separate positive corner
overlaps from the trivial zero-minimum case.
The computation itself was already sound.
The reviewer also requested the exact midpoint assertion in the counterexample control,
a complete analytic run through the public `corner-min` mode, and a forced interruption
showing that the current box remains unresolved.
Those controls are present in the reviewed test source.

No new unsound acceptance path was found in the bound or pending-box logic reviewed
here. This is a bounded source review, not a formal verification of the program.
The implementation lane reported 18 focused tests passing, with Ruff and BasedPyright
clean. The coordinator independently ran the behavioral suite and CLI goldens: 21 tests
passed in 1.63 seconds.
These are execution reports from those lanes; the mathematical reviewer inspected their
test code without duplicating the run.
The reviewer did not duplicate those executions or run the target experiment.
The reviewer inspected the retained result and checked that the current library,
comparison tool and frontier-receipt hashes match the identities recorded there.

## Frozen Comparison Result

The
[new frontier receipt](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/native-n11-frontier-2026-09-29.json)
retains all nine boxes left by the common-core n11 traversal: angle 1, 100 nodes, 46
accepted leaves, depth limit 20 and a node-limit stop.
The
[comparison receipt](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/native-n11-bound-comparison.json)
reproduces that frontier, compares all nine boxes and reports 1.420 seconds with no
timeout. The direct corner bound is at least the common-core bound in every case.
It is strictly greater in three cases, but closes no box whose common-core bound was
below one. **The predeclared usefulness criterion was not met.**

| Queued boxes | Count | Effect of the corner bound |
| --- | --- | --- |
| Common-core bound already at least one | 4 | Three strict improvements; all four were already provable by the old bound |
| Common-core bound below one | 5 | Every corner bound equals the old bound; no additional threshold crossing |

Queued boxes were unresolved because the traversal had not processed them.
They were not all boxes on which the old bound had failed.
In particular, this result does not mean that none of the nine boxes can be proved.
It means the stronger bound added no threshold crossing on this fixed frontier.
Closing diagnostic boxes also does not create a complete angle or certificate receipt.

The historical
[100-node receipt](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/native-n11-bounded.json)
remains a separate record.
The new receipts add exact frontier and comparison evidence; they do not replace its
outcome or promote the packing claim.

The separately selected
[1,000-node receipt](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/native-n11-angle1-1000-nodes.json)
is also `INCONCLUSIVE`: 1,000 visited nodes, 428 accepted leaves and all 78 unresolved
boxes retained. The terminal cause is `node_limit`, but the retained causes matter: 67
boxes were already processed and stopped at depth 20; 11 boxes remained queued when the
node limit stopped traversal.
Increasing only the node limit at the same depth limit would leave those 67 failed
leaves unresolved. No coverage counterexample was reported.
The receipt records a 30-second ceiling but no elapsed time; it cannot support an exact
wall-time claim.

## Next Whole-Certificate Slice

The frozen first target is the retained Tokoharu n11 rectangle certificate at
$L=381/100$, angle 1, threshold 1, with the old traversal capped at 100 nodes and depth
20\. A useful comparison must preserve the complete retained frontier, show the direct
inequality `corner_min_bound >= common_core_bound` on every completed box, and close at
least one previously unresolved box within the selected 30-second comparison.
Checking only `max(common, corner) >= common` would be tautological.
A timeout, an incomplete comparison, and a completed comparison with no threshold
crossing have different dispositions and must remain distinguishable.

The next selected question is the cost of the existing common-core traversal on that one
angle.
The coordinator separately preregistered **think-rrwv**: the same input, angle and
target, a fixed 1,000-node cap, depth limit 20, a 30-second ceiling, and complete
pending-box retention.
That run did not complete the angle.
It measured both unfinished traversal and a depth-resolution limit, without retesting or
relaxing the failed corner-bound criterion.
No larger rerun follows automatically.

Record total nodes, accepted leaves, unresolved leaves, exact reported bound and elapsed
time.
Neither the 100-node rate nor a local frontier improvement predicts the cost of all
201 angles.
If this traversal identifies persistent hard boxes, further bound development
should address joint rectangle coverage or a justified subdivision rule.
The corner calculation already gives the exact minimum of each individual rectangle’s
overlap on a fixed box: the proof supplies the lower bound and a minimizing corner
attains it. A stronger bound on that same box must therefore exploit relations among
rectangles, or refine the box, rather than merely tighten those separate minima.

Complete external acceptance then requires the same admitted candidate and source
identity, exactly angles 0 through 200, a verified result for each angle, zero
unresolved work, and the strict mass and net-containment premises.
The existing whole-certificate path is preferable to adding resume or shard aggregation
during this slice; either would introduce another completeness contract needing review.
Success would establish independent native coverage for that specific rectangle
certificate.
It would not replay other target counts, verify the distinct T-059 point and
threshold-charge format, or establish that format’s global counting premises.

## Separate T-059 Admission Review

The reviewer also inspected
[`check_general_pose_tree_census.py`](../../../packing/devtools/check_general_pose_tree_census.py)
and its focused tests for **think-pgrx**. This is a different certificate format.
The wrapper checks equality with the pinned 12,028-row reference and independently
evaluates each supplied witness.
Its direct evaluator preserves the source’s point indexing: sorted unique D4 images
within each input orbit, concatenated in input order.
It uses the same closed-square inequalities, integer weight units, and one feature
weight whenever the required number of distinct sites is captured.
The witness must lie in the row’s open center domain.
These formulas match the pinned source contract.

The source branch search supplies the claimed minimum and its lower-bound argument.
The independent direct evaluator checks attainment at a reported point.
Attainment alone supplies an upper bound on the true minimum; it does not independently
prove minimality. The wrapper now states this distinction explicitly.
Complete row equality also does not, by itself, prove the packing theorem.

Review fixes include forcing isolated unoptimized Python, pinning both retained inputs,
binding the first-party wrapper source, bounding range and rational parsing before
allocation, rejecting false exact witnesses, preserving incomplete timeout outcomes, and
refusing output collisions before execution and at atomic publication.
The hostile-environment fixture uses an explicit exception because an assertion would
itself disappear under the optimization setting it is meant to test.
A publication race test verifies that competing evidence is preserved.
The implementation lane reported ten focused tests passing with Ruff and BasedPyright
clean.

The reviewed wrapper has no whole-packing acceptance path.
It distinguishes complete row equality, proper subsets and legacy unbound inventory.
The provenance fields in a retained journal describe a trusted recorded execution;
revalidating that journal does not rerun the source’s full branch search.
The review found no mathematical mismatch in the direct witness evaluator for the pinned
input.

The
[fresh bound sample](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/n11-bound-sample-portable.jsonl)
and its
[summary](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/n11-bound-sample-portable-summary.json)
record rows 0, 6014 and 12027: three matching source minima and three independent exact
witness attainments.
The result is `PARTIAL_ROW_EQUALITY`, with 12,025 rows missing, sample minimum
1,000,047,518 units, and no global-minimum or packing-bound assertion.
The selected process completed; the full row census did not.
Full replay and reuse of previously checked global premises are distinct evidence
questions. The reconciliation below resolves the latter for this pinned input.

The final journal omits machine-specific input paths; its input and implementation
hashes retain the binding, while the writer receives protected paths directly.
The original sample and wrapper remain in commit `754a0342c` as historical evidence.
A fresh three-row run binds the portable journal to the corrected wrapper.

## Reusing the Existing T-037 Global Premises

**think-4t1e** reconciles the new T-059 row checker with the already retained proof of
T-037. The certificate is identical: the wrapper’s mandatory input pin, the original
source replay and the complete native parent-core receipt all name SHA-256
`57e9927da5c13f42dd8bcbf8f08c84363635fece626657ee63a810c61cd44458`. The reviewer checked
that hash against the retained
[`global-certificate.json`](../../../packing/resources/web/external-square-certificates-2026-09-22/kleddamag-11/global-certificate.json).
These are Kleddamag’s point and threshold charges at $L=191/50$ and $A=764/775$. They
are separate from the Tokoharu rectangle density at $L=381/100$ used in the inconclusive
probes above.

The [source mathematical review](review-2026-09-22-kleddamag-n11-mathematics.md) and
[native parent-core review](review-2026-09-22-native-n11-parent-core.md) already
discharge the following obligations for those exact bytes.
The present review checked their mapping to
[`validate_parent_core`](../../../packing/src/sqpack/fractional/parent_core.py), the
threshold-token budget and the retained receipts.

| Obligation | Reusable proof and evidence |
| --- | --- |
| Cover every parent orientation | The 12,028 intervals form a contiguous partition from zero to half-tangent $207107/500000$, whose square plus twice itself exceeds one. Weighted D4 symmetry folds each parent independently into this covered range. |
| Cover every legal center | The parent margin is $h(u)=A(1+2u-u^2)/(2(1+u^2))$. Its only interior stationary point is a maximum, so each row’s union of center domains is $[r,L-r]^2$ with $r=\min(h(a),h(b))$. The native search encloses that full domain. |
| Put each closed core strictly inside its parent | Four vertex-projection quadratics are minimized over every row, including interior minima. The recorded minimum numerator is $1/10^{12}>0$. Quarter-turn symmetry supplies the other parent axis. |
| Bound total charge on disjoint cores | Nonnegative point charges are counted once; each $k$-of-`m` feature contributes at most $\lfloor m/k\rfloor$ times its weight. Strict core containment makes the closed cores disjoint even when parent boundaries touch. The exact budget is $10999479944/10^9$. |
| Prove complete coverage at the required charge | The historical native decision certifies all 12,028 rows at $\Gamma=999962528/10^9$, with zero stalls, exhausted budgets or refutations. The source’s complete event-cell sweeps provide a distinct coverage method. |
| Transfer coverage to the strict packing bound | The exact gap is $11\Gamma-M=107864/10^9>0$. Scaling gives $L/A=31/8$; compactness and attainment make the exclusion a strict lower bound $s(11)>31/8$. |

The
[complete native receipt](../../../packing/campaign/agent-sessions/session-153-native-full.json)
records 136,081,500 resolved boxes and `accepted=true`, from clean commit
`c183cc9abe93eedcb268a5390cdd1cdc6e7bbb39`. The
[retained reconciliation](../../../packing/campaign/agent-sessions/session-153-native-reconciliation.json)
binds that certificate, the row journal and 19 proof-input Git blobs.
The reviewer compared all 19 paths against that commit; none differs in the current
working tree. This review reused the historical execution and its proof review.
It did not rerun the coverage search, the exact premise checker or the reconciliation
command. The original review’s receipt-authentication limitations still apply.

The [claim register](../../../packing/frontier/results.yaml) already records **T-037 at
V4/C4** on this composition of evidence.
The global orientation, containment, symmetry, budget and strict-transfer premises are
therefore available for reuse; they are not newly unresolved merely because the T-059
wrapper intentionally lacks a packing-acceptance path.
No new result promotion or additional confirmation method follows from this
reconciliation.

**T-059 remains a different, incomplete claim:** wand125’s checker is reported to
reproduce every exact row minimum and attaining witness.
The complete native run proves sufficient lower bounds at $\Gamma$; it need not find
those exact minima. For example, its row 12027 lower bound is 1,000,030,057 units,
whereas the exact reference minimum and newly replayed source minimum are 1,000,047,518.
Both exceed $\Gamma$, but their distinction matters.
The new bound journal contains only three rows, leaving 12,025 unreplayed there.
The remaining T-059 work is complete source-bound row equality and the checker-specific
minimum-search audit, not reconstruction of an already retained global packing proof.

## Two-Level Refinement Readiness

The next bounded diagnostic, **think-gfpf**, applies the unchanged common-core bound to
two further subdivision levels of the 67 retained depth-20 leaves.
The reviewer inspected
[`refine_rectangle_density_frontier.py`](../../../packing/devtools/refine_rectangle_density_frontier.py)
and its [focused tests](../../../packing/tests/test_rectangle_density_refinement.py)
before target execution.
This review found no remaining mathematical or admission blocker to that selected
diagnostic. It does not authorize a complete certificate claim or a larger replay.

Each longest-side bisection produces two closed rectangles whose union is the parent and
whose interiors are disjoint.
The tool checks their exact coordinates and depth, not merely their count or total area.
Two bisections produce exactly four children.
For a child center box $Y\subseteq X$, the common-core polygon for $X$ is contained in
the common-core polygon for $Y$. Nonnegative density therefore makes each child bound at
least its parent’s. If every child’s bound reaches one, every center in the parent has
sufficient coverage.
One successful child does not establish that conclusion.

The analytic control uses $L=4$, $B=1/2$, density 16 on $[1,3]^2$, weight 64 and count
65\. At $(\cos\theta,\sin\theta)=(4/5,3/5)$, every checking square centered in
$[15/8,17/8]^2$ lies inside the density rectangle, so its actual coverage is four.
The parent’s common-core half-width is $3/40$, giving bound $9/25$. After two bisections
each child’s half-width is $13/80$, giving bound $169/100$. The test checks these exact
values and drives the real four-child aggregation, replacing only the angle lookup with
the specified rational rotation.
It is a local geometric control, not full-net acceptance of that density.

Before refinement, the command reruns the common-core traversal and matches the retained
frontier’s exact boxes, counts, input and settings.
It selects the expected 67 depth-capped leaves from all 78 pending boxes.
It binds and rechecks the candidate, frontier receipt, native checker, refinement
command and shared comparison helper.
Binding the helper matters because that module supplies admission checks.
The native verifier source is unchanged by this slice.

Review fixes added the helper’s source identity, a bounded receipt read before JSON
parsing, refusal of an empty expected census, and expected parent/child counts that
remain visible when execution is incomplete.
Bounds are checked against the deadline before and after evaluation.
A bound finishing after the deadline is discarded; an interrupted parent retains its
completed children without being counted as closed.
Only four completed sufficient bounds close a parent.

The frozen criterion requires all 67 parents and 268 child bounds, direct
child-to-parent bound monotonicity, and at least one closed parent, within the selected
cooperative 30-second ceiling.
Complete output is always `DIAGNOSTIC_ONLY`; a complete zero-closure result is negative
for this two-level refinement.
A timeout is `PARTIAL_DIAGNOSTIC`, and identity, partition or monotonicity failures
refuse. The other 11 queued boxes and the other net directions remain outside this local
conclusion. In particular, the depth-1 queued box covers half the initial domain.
Local success would supply no complete-angle cost estimate.

The implementation lane reported nine focused tests passing in 0.11 seconds, with Ruff
and BasedPyright clean.
A public-command mutation control changes a stand-in comparison helper during replay and
confirms refusal at the final source-identity check.
The mathematical reviewer inspected those controls and the final source without
duplicating their execution.
No retained target refinement had been run at this readiness checkpoint, and this
section records no measured target outcome or new packing proof.

## Two-Level Refinement Result

The subsequently selected
[first target receipt](https://github.com/jlevy/squares/blob/43c66ec86/packing/resources/web/wand125-tools-2026-09-29/receipts/native-n11-depth22-refinement.json)
is `DIAGNOSTIC_ONLY`, with outcome `LOCAL_CLOSURE_OBSERVED`. It completed all 67
selected parents and 268 child bounds, closed 15 parents, and recorded 7.713767125
seconds including frontier replay, with no timeout.
**The predeclared local usefulness criterion was met.**

The reviewer independently checked the receipt’s exact rational arithmetic and census.
Its replayed frontier equals the retained 1,000-node frontier; its parents are exactly
the 67 depth-capped leaves, without duplicates.
Every parent bound is below one.
Each parent’s four depth-22 boxes form its exact partition, every child bound is at
least its parent’s, and each closure flag agrees with all four child bounds reaching
one. The candidate, native checker, refinement tool, shared comparison helper and input
receipt hashes all match their recorded identities.
The reviewer did not rerun the target or independently recompute its clipping bounds.

The remaining 52 parents each have at least one child whose lower bound is insufficient;
this is not a coverage counterexample.
The original 11 queued boxes also remain outside the selected refinement, including the
depth-1 box covering half the initial domain.
The result demonstrates useful local subdivision on this fixed set of leaves.
It neither replaces the original inconclusive angle verdict nor combines diagnostics
into a complete proof, estimates whole-angle cost, or permits an automatic larger run.
The other net directions and complete external-certificate acceptance remain open.

### Final Source Formatting and Reproduction

The repository-wide format check required a formatting-only change after this review.
Commit `43c66ec86` retains the reviewed tool and first receipt.
The coordinator checked that formatting left the tool’s parsed Python AST unchanged,
then repeated the same bounded diagnostic to bind the final source bytes.
The
[final receipt](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/native-n11-depth22-refinement.json)
records 8.994228833 seconds and the same complete 67/268 census and 15 closures.
Its entire decoded result matches the first receipt except elapsed time and the tool’s
source hash. This is a reproduction for final-source binding, not a larger experiment or
a new Astra review. The native checker and mathematical algorithm are unchanged.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
