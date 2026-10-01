# Eleven-Square Optimality: Expository Simplification Review

**Date:** September 30, 2026\
**Reviewer:** Codex, Astra at max reasoning\
**Tracking:** `think-uz2x`, prerequisite to the dedicated n=11 explainer

**Disposition:** The accepted T-060 argument is ready for exposition.
Three consolidations below simplify its presentation while preserving every mathematical
premise and accepted execution.
This bounded review establishes no reduction in the number of cases, branches, rounds,
or required geometric checks.
No proof code, accepted receipt, or frontier value was changed, and no fresh geometric
replay was performed.

## Frozen Theorem and Evidence

For eleven congruent unit squares with independent rotations and pairwise disjoint
interiors, allowing boundary contact,

$$
s(11)=T=\frac{6u+4}{1+2u-u^2},
$$

where $u$ is the unique root in $(9/25,37/100)$ of

$$
5u^8-10u^7-2u^6+14u^5+12u^4-6u^3+2u^2+2u-1=0.
$$

The [T-060 register](../../../packing/frontier/results.yaml) and
[whole-proof acceptance](review-2026-09-29-n11-optimality-census-contract.md#whole-proof-acceptance)
record S5/V4/C5. The external source is `Queuingtheorydotcom/11SquaresOptimal` at
`f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c`. The exact construction is Trump’s.

The [final composition][composition], SHA-256
`eaad8f14cf3404e8abe1bfee18cbd7f12a2fed2094f46f021d4e3bfb3088b141`, binds the reviewed
execution ensemble with no pending obligation.
Its accepted [exclusion inventory][exclusions] is
`498801611757f8ce4557dd105697c4e6c4ab8aa3d460e0306b90bda4657ffe48`. The final receipt
retains the component identities and six-source composition closure; the
[reproduction guide][reproduction] identifies the frozen geometric checkers and their
commands. The logical map below preserves those dependencies rather than replacing that
execution record.

## Proof Dependency Map

| Accepted obligation | Mathematical input and conclusion | Evidence and review |
| --- | --- | --- |
| Exact endpoint and witness | Isolate $u$, verify eleven unit squares at $T$, prove $T<U$, and verify opposite-wall contacts giving span $T$ in both coordinates. | [Endpoint review][endpoint] and [local execution][local] |
| Exhaustive center patterns | Sixteen closed rational Voronoi cells cover the normalized center square. Each physical cell has diameter strictly below one, so it contains at most one center. The 4,368 raw masks reduce by half-turn to 2,184. | [Cover and D4 checker][d4-code] and [case census][census] |
| All noncandidate exclusions | Sound ownership, charge, collision and residual-cover arguments exclude exactly $\{0,\ldots,2183\}\setminus\{438,999,1462,1659\}$ at the same cap $U$: 1,904 field cases and 276 others. | [Complete exclusion inventory][exclusions] and [exclusion acceptance][exclusion-review] |
| Final D4 reduction | Given those exclusions, the closed four-view overlay and strict distance bans force some square symmetry to admit case 438. Reflections and quarter-turns need not permute the original cells. | [D4 execution][d4] and [geometric implication][d4-proof] |
| Case-438 capture | The accepted seed, fourteen root rounds, root bridge and ten capture nodes preserve every feasible pose. Three far leaves contradict feasibility; the near leaf supplies a complete outer enclosure. | [Root chain][root] and [complete capture review][capture] |
| Fixed-$T$ local isolation | At the exact witness, complete feature coverage, Taylor bounds and 8,448 signed-coordinate dual margins exclude every nonzero feasible displacement in the declared 33-coordinate rectangle. | [Local checker][local-code] and [local execution][local] |
| Near-to-local inclusion | The accepted near final state, role bijection, inverse frame and whole-angle bounds place all 136 live rows and 1,542 vertices inside that same local rectangle. | [Pose inclusion][inclusion] and [accepted final-state join][capture] |
| Global equality | A putative side-$S$ packing with $S<T$ embeds in $U$, reduces to case 438 and recenters into the fixed-$T$ local problem. Isolation forces the witness of span $T$, a contradiction. The witness attains $T$. | [Endpoint review][endpoint] and [whole-proof acceptance][whole] |

Two dependencies must remain visible inside the exclusion row.
The necessary D4 cuts for cases 2175 and 2176 start from the complete **1,931-case
baseline**, with 253 canonical survivors; the later four-survivor conclusion cannot
justify them. Case 1383 instead forks the same accepted common state at the closed
owner-13 center split $y_{13}=4/3$ and requires both branches to reach contradiction.
These premises and the exact charge-transfer condition are recorded in the
[census contract][special].

The ten-node capture ancestry is `root → {far15, r1}`, `r1 → {r10, near13}`,
`r10 → far13`, `near13 → r11`, `r11 → {far2, r111}`, and `r111 → near`. The root
includes its accepted first step and continuation.
The three closed splits are at centered height $y_{15}=5/4$, then half-angle parameters
$t_{13}=147/512$ and $t_2=183/512$; each cut includes equality on both sides.
Intermediate continuation nodes remain part of the accepted ancestry even when the
article draws only the four mathematical leaves.

## Three Consolidations and Their Limits

**1. Organize by implication rather than execution history.** Present the dependency map
as a reduction from all packings to one local neighborhood, followed by isolation and
the matching witness.
Put operational stages, retries and receipt inventories in an appendix or linked
reproduction record.
This removes repeated explanations of the same premise without deleting it.
The article review must map every summarized stage back to the complete census,
conditional-cut dependencies, both case-1383 branches and all capture joins.
The outcome is an accepted organizational simplification; no smaller certificate
ensemble was established.

**2. State the ownership invariant once.** For each occupied owner, an outer pose cover
contains every feasible center and orientation, while its owned hull lies strictly
inside its square in every surviving pose.
A strict inner core for a whole angle row makes collision regions safe to exclude even
on their closed boundaries.
A complete cover check retains every remaining pose; points owned in every residual pose
can then be added. Field, generic and capture arguments can refer to this one invariant.
Preserve closed angle endpoints, singleton and segment domains, predecessor identity,
sequential update order and the common prior of parallel updates.
Partial trailing steps promote no state.
Exact compression can replace an owned-hull representation, so the prose must not assert
that stored hulls or vertex lists always grow.

Field counting remains a separate lemma: with required owners $O$, charged cells $P$,
thresholds $q_i$ and budget $b$, transfer to a mask $J$ requires $O\subseteq J$ and
$\sum_{i\in P\cap J}q_i>b$. Collision alternatives consume no physical charge.
The majority feature uses median-projection inequalities and has capacity one across
disjoint strict cores; it must not be illustrated or described as merely containing a
majority of the sites.
The [five-site example][majority] provides a concrete charge-two-versus-budget-one
explanation. This consolidation preserves the existing mathematical rules; a new
general-purpose checker or broader feature class would require its own validation.

**3. Present the endpoint argument together with local isolation.** Keep the algebraic
root, rational cap, exact witness and coordinate conversion in one argument.
With $B=(191/50)/U$ and $Q$ the checked quarter-turn, the map is

$$
p_T=Q^{-1}\!\left(p_f/B-(U/2,U/2)\right)+(T/2,T/2).
$$

A side-$S$ container centered inside $U$ maps to $[(T-S)/2,(T+S)/2]^2$. For $S<T$, its
unchanged unit squares are therefore feasible inside $[0,T]^2$. Capture and inclusion
put them in the local rectangle, where the accepted local theorem forces the exact
witness. Its span $T$ contradicts containment in side $S$. This uses neither a
compactness passage nor a rescaling of the small squares.
It also does not assert that case 438 is impossible in the larger cap $U$.

The local proof can be summarized by its decisive inequality.
For a nonzero displacement $h$, let $\tau=\max_j|h_j|/r_j\le1$ and choose a saturated
coordinate $j$. The dual sign opposes $h_j$; nonnegative weights, residual error
$\epsilon_j$ and row-curvature mass $M_j$ give

$$
\tau r_j\le\epsilon_j\tau R+\frac{\tau^2M_j}{2},\qquad
R=\max_k r_k,\qquad M_j<2(r_j-\epsilon_jR).
$$

Thus $\tau\le c_j\tau^2$ with $c_j<1$, contradicting $0<\tau\le1$. Preserve the strict
positive margin, the nonlinear remainder bound and the complete feature census: 112
features, 88 unavailable throughout the rectangle, and 512 raw choices reduced to 128
derivative branches.
An infinitesimal-rigidity assertion alone would not supply these conclusions.
This is a shorter presentation of the accepted [local argument][local-proof], with no
stronger isolation radius claimed.

## Exposition Readiness and Review Obligations

The bounded assessment found no justified removal of a case, capture round, feature
branch, or boundary condition.
Such a change would require a new implication or a complete replacement certificate and
the corresponding mathematical review and replay.
Global uniqueness, a uniform isolation region replacing the anisotropic rectangle, and a
distinct proof method remain outside this disposition.

The dedicated paper may proceed in this order:

1. State the unrestricted packing problem and exact matching construction.
2. Derive center separation, the closed Voronoi cover and the finite pattern census.
3. Explain ownership and complete pose-cover preservation, then field charge budgets.
4. Account for the exclusion union and the exact D4 reduction.
5. Follow the closed capture splits into the local rectangle.
6. Derive local isolation and finish the concentric smaller-container contradiction.
7. Give a compact checker/evidence map, attribution and reproduction limits.

Review each diagram against the exact quantities it depicts: the center cells are
Voronoi polygons, orientations are independent, and $t=\tan(\theta/2)$ is not an angle
in radians. Label schematic collision or majority examples as schematic.
The article must cite the final accepted review rather than promote an earlier
provisional status or infer geometry from a stored success string.

The [evidence record](../../../packing/frontier/evidence.yaml) retains the source’s
credit and the shared local construction, derivative and arithmetic primitives.
V4/C5 means exact computational verification with a mapped mathematical review and
adverse controls; it supplies neither distinct-method C4 confirmation nor
proof-assistant V5 verification.
The publisher’s four stale final-state digests remain reproducibility defects.
Fresh whole-ensemble automation needs reviewed state-equivalence rebinding of historical
parent receipts; the accepted observed ensemble has no pending mathematical obligation.
T-037’s earlier lower bound, T-059’s separate row-minimum assertion, and
rectangle-density performance work are separate results.

The acceptance condition for `think-uz2x` is satisfied by this frozen dependency map,
the three dispositions and their preserved obligations.
The subsequent paper still requires mathematical review of its prose and figures;
closing this prerequisite does not accept an unwritten article.

[composition]: ../../../packing/resources/web/n11-optimality-2026-09-29/receipts/final-composition.json
[exclusions]: ../../../packing/resources/web/n11-optimality-2026-09-29/receipts/exclusion-inventory.json
[reproduction]: ../../../packing/resources/web/n11-optimality-2026-09-29/README.md#reproducing-the-independent-checks
[endpoint]: review-2026-09-29-n11-optimality-census-contract.md#endpoint-and-final-composition-readiness
[local]: ../../../packing/resources/web/n11-optimality-2026-09-29/receipts/local-isolation/result.json
[d4-code]: ../../../packing/devtools/check_n11_optimality_d4.py
[census]: ../../../packing/resources/web/n11-optimality-2026-09-29/receipts/case-census/result.json
[exclusion-review]: review-2026-09-29-n11-optimality-census-contract.md#complete-exclusion-execution-census
[d4]: ../../../packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json
[d4-proof]: ../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#6-the-exact-d4-reduction-to-case438
[root]: ../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-root-chain/result.json
[capture]: review-2026-09-29-n11-optimality-census-contract.md#accepted-near-state-and-complete-capture
[local-code]: ../../../packing/devtools/check_n11_optimality_local_isolation.py
[inclusion]: ../../../packing/resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/result.json
[whole]: review-2026-09-29-n11-optimality-census-contract.md#whole-proof-acceptance
[special]: review-2026-09-29-n11-optimality-census-contract.md#the-three-special-adapters
[majority]: review-2026-09-29-n11-optimality-census-contract.md#first-independent-field-exclusion-mask-0
[local-proof]: ../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#7-local-contact-analysis-and-the-focused-isolation-rectangle

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
