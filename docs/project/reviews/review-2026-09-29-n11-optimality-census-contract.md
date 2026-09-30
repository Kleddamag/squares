# Eleven-Square Optimality: Census and Capture Ancestry Contract

The next bounded checks for **T-060** establish whether the published case lists and
capture dependencies cover the claimed domain.
They support the independent proof review under `think-3i74`; they do not change the
reported theorem’s S5/V0/C1 classification or the verified lower bound.
The [source review](review-2026-09-29-n11-optimality.md) records the theorem, completed
symmetry check, and remaining geometric obligations.

This contract uses `Queuingtheorydotcom/11SquaresOptimal` at commit
`f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c`. The relevant published consumers are
[`verify_recorded_proof.py`](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/src/evidence/code/verify_recorded_proof.py),
[`baseline_reconstruct.py`](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/src/evidence/research/finalization/baseline-portable/baseline_reconstruct.py),
[`verify_returned.py`](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/src/evidence/code/verify_returned.py),
and
[`audit_complete_capture438.py`](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/src/evidence/research/candidate-capture/audit_complete_capture438.py).
Their source code defines the proposed obligations below; reading that code does not
accept the supplied certificate instances.

## What Each Check Establishes

| Scope | Acceptance means | Obligations still open |
| --- | --- | --- |
| Case census | Independently reconstructed mask universe and exact membership, assignment, and family unions agree with the selected metadata. | Every geometric exclusion and conditional transfer. |
| Reported capture ancestry | Published receipts describe a complete branch partition and consistent dependency graph. | The graph’s agreement with the large source objects and every geometric implication. |
| Source capture ancestry | Hash-verified source objects establish the actual parent graph, assumptions, root identity, and final-state bindings. | Exact geometric validity of the transformations and exclusions at those nodes. |
| Component mathematical acceptance | Independent checks prove the named transfer, exclusion, local-isolation, or inclusion implication over its entire stated domain. | Other components and final composition. |
| Global acceptance | Construction, all exclusions, symmetry, capture, local isolation, and their connecting implications have been accepted together. | No unresolved obligation needed for $s(11)=T$. |

Receipts must state the checked scope and set `global_optimality_proved: false` until
the last row is satisfied.
A census receipt should use an explicit status such as `PASS_CASE_CENSUS_ONLY` and
`geometry_verified: false`. Missing inputs, a stopped run, or partial coverage produces
an incomplete result.
A failed check identifies the specific invalid premise.
A valid packing of eleven unit squares in a container of side below $T$ refutes the
claimed lower bound.
A gap in the published proof leaves the optimum unresolved unless further reasoning
settles it.

## Small Payload Packages

All paths in the next tables are decoded paths relative to the publisher’s package.
The retained
[content index](../../../packing/resources/web/n11-optimality-2026-09-29/source/data/INDEX.json.gz)
maps a path through `files[path]` to an object entry.
Resolve that entry’s `object`, `sha256`, and `bytes` fields.
**The index key is not necessarily the decoded SHA-256.** The compressed sizes below
come from the pinned Git LFS pointers and are declared sizes, not measured download
costs. Verify both the compressed LFS identity and the decoded SHA-256 and length when
acquiring a payload.

### Case Census

The five objects total **100,541 compressed bytes and 833,308 decoded bytes**. The
center cover already acquired for the independent symmetry check supplies the shared
cover identity; independently enumerate the masks again in the census consumer.

| ID | Decoded path | Compressed bytes | Decoded bytes |
| --- | --- | ---: | ---: |
| A1 | `evidence/research/PHASE3_FRESH_REPLAY_RESULT.json` | 26,100 | 122,029 |
| A2 | `evidence/results/prior-union/PRIOR_UNION_RESULT.json` | 25,401 | 270,956 |
| A3 | `evidence/inputs/returned-replay-plan.json` | 45,515 | 401,045 |
| A4 | `evidence/inputs/CASE_ASSIGNMENTS.json` | 2,762 | 37,021 |
| A5 | `evidence/results/returned/SUMMARY.json` | 763 | 2,257 |

### Candidate 438 Ancestry

The seven objects total **19,590 compressed bytes and 91,760 decoded bytes**. They
support receipt-level checks and selection of source payloads.
They cannot establish what is inside an unacquired source object.

| ID | Decoded path | Compressed bytes | Decoded bytes |
| --- | --- | ---: | ---: |
| B1 | `evidence/inputs/candidate-composition-pins.json` | 1,991 | 5,892 |
| B2 | `evidence/research/candidate-capture/complete-capture438-audit.json` | 5,232 | 20,536 |
| B3 | `evidence/research/candidate-capture/root14-independent-audit.json` | 2,948 | 30,071 |
| B4 | `evidence/research/candidate-capture/far15y-independent-audit.json` | 1,713 | 4,160 |
| B5 | `evidence/research/candidate-capture/far13-independent-audit.json` | 2,335 | 7,513 |
| B6 | `evidence/research/candidate-capture/far2-independent-audit.json` | 2,596 | 10,638 |
| B7 | `evidence/research/candidate-capture/near1024-independent-audit.json` | 2,775 | 12,950 |

## Exact Exclusion Census

Construct the ordered universe independently:

$$
\mathcal C=\operatorname{sorted}\{\min(J,\tau J):J\subset\{0,\ldots,15\},\ |J|=11\},
\qquad \tau J=\operatorname{sorted}\{15-j:j\in J\}.
$$

There must be 4,368 raw masks and 2,184 representatives.
Case IDs are zero-based indices into this exact ordering.
Check the full arrays against the cover rather than accepting their counts alone.
All domain-bearing premises must use $U=387708359002281417731/10^{20}$, $L=191/50$, and
$B=L/U$.

Require the following exact sets and source identities:

- A1 supplies 1,931 distinct baseline exclusions and 253 complementary cases.
  Its certificate inventory has 59 field and 34 generic entries.
  Count each certificate once; overlapping case support from different certificates is
  permitted.
- A2 preserves the entire baseline set and adds exactly 76 distinct cases outside it.
  Its 76 extension entries each name their single case and source audit.
  Their union with the baseline must equal its 2,007-case exclusion list.
- A3 has exactly 173 distinct case entries.
  Each case has one declared job, source, root, archive, and submitted audit; its job
  assignment must agree with A4. Record duplicate assignments explicitly rather than
  silently converting every list to a set.
  A5’s completed list must equal those 173 cases and its unresolved list must be empty
  before accepting the complete reported census.
- The returned set is disjoint from the 2,007 prior cases.
  Their union must equal $\{0,\ldots,2183\}\setminus\{438,999,1462,1659\}$. Reconstruct
  the four actual masks from the universe and compare them with the symmetry component’s
  inputs.

Refuse out-of-range or noninteger IDs, duplicate entries in lists that claim distinct
case coverage, omitted cases, inconsistent mask arrays, changed cap or cover,
conflicting source bindings, and a completion flag paired with an unresolved case.
Report the precise missing, unexpected, or duplicated IDs.
A published `PASS` string is data to compare, not the reason a case is excluded.

### Conditional Transfers and Dependency Direction

The first substantive successor to the census independently reconstructs the transfer
sets of the 59 field certificates.
For a packet with required owners $O$, checked positive cells $P$, cell thresholds
$q_i$, and global charge budget $b$, its counting argument excludes a mask $J$ only when

$$
O\subseteq J\quad\text{and}\quad\sum_{i\in P\cap J}q_i>b.
$$

Apply this rule to each representative and its half-turn.
Use only thresholds whose whole-cell, whole-angle lower charge has been proved by the
packet’s geometry; the transfer calculation remains conditional until those proofs are
accepted. Equality with the budget does not exclude a mask.
Refuse lost support owners, an unproved positive threshold, or a claimed transferred
case outside the recomputed set.

The field union must have 1,904 cases.
The 34 generic certificates must each exclude their one complete mask with no branch
assumption or local-guard condition; exactly 27 are new beyond the field union.
Their union is the baseline’s 1,931 cases.
The baseline replay manifest and the field packets are additional inputs to this
successor, to be selected after the first census identifies their exact references.

Preserve the direction of every conditional premise.
The necessary $D_4$ cuts used by some of the 76 extensions depend on the **253 survivors
of the original baseline**. Their support queries and resulting halfplanes must be
justified from that earlier set.
The later four-candidate symmetry result cannot be used to prove those earlier
exclusions. A dependency graph must expose any such cycle.

### Coverage Classes and the Non-Field Frontier

Set arithmetic over the pinned A1–A3 inventories separates the remaining algorithms:

| Class | Certificates or entries | Distinct cases contributed |
| --- | ---: | ---: |
| A1 fields | 59 | 1,904 |
| A1 generic, outside the field union | 34 total, seven overlapping fields | 27 |
| A2 extensions, outside A1 | 76 | 76 |
| A3 returned jobs, outside A1 and A2 | 173 | 173 |
| Complete reported exclusion union |  | 2,180 |

Thus completing every field still leaves **276 non-field exclusions**, as well as the
separate symmetry and candidate-capture obligations.
These are case counts, not fractions of the mathematical proof or estimates of its
remaining cost.
Count completed field receipts by their exact case-ID union; a timeout or
unsupported field contributes no IDs.

The retained
[field coverage inventory](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/field-batch-a/field-coverage-inventory.json)
now closes that entire 1,904-case field union using 46 complete distinct packets.
An independent reread checked every listed receipt’s decoded identity, checker and
packet bindings, successful geometry flag, empty pending lists, and exact per-packet A1
transfer set, then recomputed the union.
Those receipts contain 18,855 checked rows and 4,464 ownership checks.
The inventory SHA-256 is
`768b7110548ce9200d1a8887e417985d79109e5987ff8e0b2b7dd998976d260e`. This closes every
field-covered case without claiming that all 59 overlapping source certificates were
individually completed.
The 276 non-field cases and the remaining candidate-capture implications are still open.

The A2 inventory contains 72 `direct_v9` entries, two
`necessary_D4_cuts_and_independent_geometry` entries, one `native_cached_v9`, and one
`native_cached_v4_center_partition`. Each requires the geometric dependency closure
appropriate to that method.
A reported one-node audit may still depend on an unproved root or cached state.
The two conditional symmetry cuts must retain the earlier-baseline dependency described
above.

Case 1723 is the smallest A1 generic-only terminal payload by decoded size.
Its terminal and fresh audit total 293,355 compressed bytes and 1,736,892 decoded bytes:

| Input | Pinned package path | Compressed bytes | Decoded bytes |
| --- | --- | ---: | ---: |
| Terminal source | `evidence/research/phase3/work/phase3/generic/mask1723-collision-followup-v5.json` | 287,501 | 1,707,879 |
| Fresh audit | `evidence/research/phase3-fresh-generic/17-mask1723-collision-followup-v5.json` | 5,854 | 29,013 |

The source index key and decoded SHA-256 are
`4819cd7a7eb95a411288c42c108c33ae0bc83f36f445c97bcd53e9831cba3cf0`; its compressed
SHA-256 is `8afe4fe10a03878a05bfe24fff4b6598e005124870a67ec59d15a3b5458a8f83`. The audit
index key is `b960a0232ce72ccce555c073b5c92d9aa87cab7125682e64d16975cc3a4abe3e`, its
decoded SHA-256 is `49de61eb2c2caae8558d634c8b93825304b64fb4256f8183fcba5bab285c92ae`,
and its compressed SHA-256 is
`53f8d7476c7cb1e2df2e6a1901512e68990aee60cfe43190d74242dd46d830df`. Inspect these two
objects before selecting further inputs: their size does not include unresolved
ancestors and does not establish the cheapest complete replay.
The audit supplies references and proposed geometry, not accepted ownership or a
contradiction. Completing this case would add one exclusion beyond the entire field
union.

Reusing a field through a larger container symmetry requires an independently checked
permutation of the complete closed cover and transformed ownership and charge premises.
Only the already checked whole-packing half-turn is presently part of field transfer.

### Source-Bound Non-Field Recipes

The maintained
[recipe builder](../../../packing/devtools/prepare_n11_nonfield_manifest.py) now freezes
all 276 non-field cases in a
[compact manifest](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/nonfield-manifest/manifest.json.gz),
with a readable
[summary](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/nonfield-manifest/summary.json).
Each recipe binds its canonical mask, seed, proposed ordered ancestry, exact cap, source
and audit identities, and individual index/LFS object sizes and hashes.
A3 member recipes also match the indexed archive members and assigned jobs; their
individual blobs can be acquired without downloading a ZIP. Ten focused controls cover
omissions, duplicate ancestors, wrong identities and sizes, unsafe member paths, and
unsupported member types.

The recipes comprise 273 sequential wall-seed cases, one closed center-partition case
(1383), and two cases requiring earlier-baseline symmetry cuts (2175 and 2176). Case
1839’s cached source is listed with all four proposed ancestors, so the consumer can
replay them rather than accept the cache’s verdict.
Published audit order supplies a proposed dependency list; actual source-parent edges,
inherited predicates, and geometric transitions still require independent acceptance.
The manifest’s geometry, actual-parent, and global-proof flags are all false.

The 924 unique declared proof objects total 2,121,265,805 compressed bytes and
10,063,719,433 decoded bytes.
These are inventory sizes, not a download request or a replay-cost estimate.
The final build read 285 small metadata objects in 12.13 seconds and retained a
186,249-byte compressed manifest.
Select bounded source closures from this inventory before scheduling geometry.

Inspecting complete ancestry changes the first-pilot choice from terminal-size ranking.
Case 2095 has one fresh node with five sequential 32-row updates and no self-hull cuts,
partner covers, branch predicate, or guard.
Its first row and complete 77-point, 352-row wall seed are checked as diagnostics; no
case exclusion follows from that pilot.
Case 2135 is a small follow-on: one fresh node, six eight-row updates, and 75 seed
points. Its complete declared closure, including cover and audit, is 492,515 compressed
bytes and 3,168,742 decoded bytes.
It additionally requires self-hull center cuts, but no partner-cover or branch adapter.

The shared transition contract starts from independently accepted strict owned hulls
$H_j$, a complete closed angular partition, and accepted outer center domains.
For every row, prove the proposed core $Q$ lies strictly inside every physical square
orientation in that row; then $H_j-Q$ forbids the querying square’s center for each
other occupied owner $j$. Prove that the complete legal center domain is covered by
those forbidden regions and the proposed closed residual polygons, preserving points and
segments.
New ownership points must lie in every translate $z+Q$ for all residual centers
$z$; exact facet minima and convex-combination witnesses establish this implication.
Each sequential update consumes the preceding accepted state, and acceptance of an
exclusion requires a complete empty pose cover for an occupied square.
Normalize accepted polygons before later clipping; equal convex hulls do not justify
clipping an unnormalized source vertex sequence.

For a proposed self-owned-hull cut $n\cdot c\le h$, set $E=h-\min_{p\in H}n\cdot p$. For
each pair of signs $\sigma_1,\sigma_2\in\{-1,1\}$, define $A=\sigma_1n_x+\sigma_2n_y$
and $D=\sigma_1n_y-\sigma_2n_x$. Require $(E-BA/2)-BDt+(E+BA/2)t^2\ge0$ throughout the
row’s closed half-angle interval.
Checking endpoints and any interior quadratic minimum proves the full physical square’s
support is at most $E$, making the center cut necessary.
This uses an upper bound on the full square; the smaller strict collision core cannot
supply that bound.

### The Three Special Adapters

Case 1383 reuses the generic transition kernel under two explicit center assumptions.
Its pinned tree proposes five unguarded ancestors followed by an owner-13 split at
centered unit height $4/3$, with two further nodes on the lower branch and one on the
upper branch. From the same accepted parent state, fork the closed conditions
$y_{13,f}\le B(U/2+4/3)$ and $-y_{13,f}\le-B(U/2+4/3)$. Their union is exhaustive and
includes equality on both sides.
Verify actual parent edges, exact inherited assumptions, seed, case, scale, and child
state bindings before replaying each branch.
Both leaves must independently reach contradiction; do not merge ownership points
derived under different branch assumptions.
The eight-node inventory and its 36,600 reported rows remain proposals until those
source objects are read and replayed.
This case has no declared dependency on the baseline exclusion set.

Cases 2175 and 2176 add 72 and 73 necessary center halfplanes, respectively.
Their published support premise is the exact 1,931-case A1 baseline, identified by
snapshot `bc3563a0c9955a561f99cbefe7278e027feff085ff6d97bc338e347f97514545`, with 253
canonical survivors.
Using only the accepted field union and case 2095 leaves 26 A1 exclusions unaccepted.
Matching a count of 1,931, accepting unrelated extensions, or using the later four-case
symmetry conclusion cannot supply those missing premises.

A separate independent support check may instead use any explicitly admitted exclusion
set $E$, with canonical survivor set $S=\mathcal C\setminus E$ and both raw half-turn
orientations of each survivor.
For the field union and case 2095, this means 279 canonical and 558 raw masks.
Reuse the reviewed cover, complete 220-region overlay, and 1,572 strict distance bans
from the [D4 checker](../../../packing/devtools/check_n11_optimality_d4.py), while
parameterizing its finite search by $S$ and a forced owner-region assignment.
For each proposed plane, exhaustively exclude every owner region having an offending
vertex; other regions may remain conservatively retained without a feasibility claim.
Every retained normalized vertex $v$, including singleton regions, must satisfy
$n\cdot B(\tfrac12(1,1)+(U-1)v)\le h$. A timeout leaves a region unexcluded.
The publisher’s planes may fail under the larger survivor set, in which case their
necessity remains unproved.

Bind the retained overlay and distance objects explicitly: the special recipes list
publisher support receipts but do not include those receipts’ full geometry input
closure.
Recomputing support avoids treating the publisher’s supported hulls as premises.
Only after all source constraints are proved necessary may a complete conditional
generic contradiction exclude its case.
Record the exact exclusion dependencies and reject cycles or reliance on the target’s
own conclusion.

### First Independent Field Exclusion: Mask 0

`think-fi4w` takes the first substantive geometric slice after the case census.
The selected packet is
`evidence/research/phase3/work/phase2/mask0-minimized-packet.json`, decoded SHA-256
`14164a3d91117055000ae78cd15a4e8ad5d6bb2c27ce24ff080605b873a93340`. It has 28,065
decoded bytes and 3,749 compressed bytes; its compressed LFS SHA-256 is
`0759a9f56e0035713996287fa2bd540c29ad60820da5da40250136375442f832`. The packet has five
rational sites, zero point weights, and one majority-hull feature using all five sites
with threshold three and weight one.
Its total budget is one.
Cells 1 and 2 have required charge one; the other cell thresholds are zero.
The conditional owner set is $O=\{0,1,2,3,6\}$, whose five groups contain 55 owned-point
proposals.

The A1 audit `evidence/research/phase3-fresh-fields/04-mask0-minimized-packet.json`
supplies proposed angle intervals.
Its index key is `2b99103ea70889c86e094fa8cface28d3e48e9040de5cad34caa1c975422a85e`,
decoded SHA-256 `1a56056ad4d19786e41e248f0ef60866ad2021370e9ef809faa471fb679f8a54`, and
decoded size 201,961 bytes.
The compressed object has 29,707 bytes and LFS SHA-256
`156102cf720236023cf5ec86cc697a5d6d2615fcf0eaa82336574be49d8856a2`. Use its
`independent_row_proofs` intervals as proposals; its coverage, ownership, and `PASS`
fields are not mathematical premises.
A new proof that reconstructs every domain and covers both complete angle charts needs
no producer replay as a mathematical premise.

**Owned points.** For each of the 55 used points, prove strict interior membership in
every unit square with center in its owner’s cell and contained in $[0,U]^2$. The
unit-coordinate cell is $C_i=\tfrac12(1,1)+(U-1)V_i$, where $V_i$ is the validated
normalized cover polygon, and the point is $p=p_f/B$. The bound
$\max_{v\in\operatorname{vertices}(C_i)}\lVert p-v\rVert^2<1/4$ is sufficient.
Otherwise, cover $t\in[0,1]$ by closed rational intervals $[a,b]$ and use

$$
c(t)=\frac{1-t^2}{1+t^2},\quad s(t)=\frac{2t}{1+t^2},\quad
h=\frac{\min(c(a)+s(a),c(b)+s(b))}{2}.
$$

Clip $C_i$ to $[h,U-h]^2$, which contains every legal center in the interval.
At every resulting vertex $v$, bound the body projections $c(t)(p_x-v_x)+s(t)(p_y-v_y)$
and $c(t)(p_y-v_y)-s(t)(p_x-v_x)$ using $c(t)\in[c(b),c(a)]$ and $s(t)\in[s(a),s(b)]$.
Both absolute bounds must be strictly below $1/2$. Preserve singleton and segment
domains; an empty domain is vacuous.
Refine unresolved intervals within selected depth and wall ceilings.
No point is accepted until its entire closed chart is covered.
Unused owner groups need no ownership proof for this specialized certificate.

**Angle rows and strict cores.** For each proposed row $[a,b]$ of cells 1 and 2,
reconstruct $t=(a+b)/2$, $(c,s)=(c(t),s(t))$, and

$$
f=\max_{z\in\{a,b\}}\bigl(c\,c(z)+s\,s(z)+\lvert c\,s(z)-s\,c(z)\rvert\bigr),
\quad q=\frac{B-10^{-12}}{f},
\quad H=\frac L2-\frac B2\min_{z\in\{a,b\}}(c(z)+s(z)).
$$

Require $0<q<B$ and $qf<B$. Check the full-angle quadratic inequalities from the pinned
`audit_wall_mask_chain_v3.py`: the two core-support inequalities on $[a,t]$ and $[t,b]$,
and the legal-wall width inequality on $[a,b]$. Endpoint sampling is insufficient.
The midpoint-oriented square of side $q$ must lie strictly inside every parent square
represented by the row.
Rebuild the field center domain from $(B/2,B/2)+(L-B)V_i$, intersect it with
$[L/2-H,L/2+H]^2$, and rotate it by the negative midpoint angle about $(L/2,L/2)$.

**Closed domain coverage.** Rotate the five feature sites and used owned points into the
same axes. The majority feature’s region consists of centers $x$ satisfying

$$
\lvert n\cdot x-\operatorname{median}_{j=1}^{5}(n\cdot p_j)\rvert
\le\frac q2(\lvert n_x\rvert+\lvert n_y\rvert).
$$

Check the coordinate-axis normals and every nonzero perpendicular to a site pair.
Between consecutive such directions, the median site and signs in the square’s support
function are fixed, so these inequalities are linear in the normal.
The other allowed cover regions are closed axis boxes of radius $q/2$ around owned
points of $O\setminus\{i\}$. Those boxes represent collisions with other occupied
squares; they add nothing to the physical charge budget.

Prove that the union contains the entire closed center domain for every row.
A rational slab and endpoint-chain consumer can provide an implementation distinct from
the publisher’s field polygon-subtraction checker.
The existing first-party closed-polygon consumer accepts rectangles and capped polygon
inventories; it cannot be applied unchanged to these arbitrary convex domains.
The accepted symmetry checker’s rational hull and clipping primitives are reusable, with
their source identity retained.
Preserve points, segments, touching boundaries, and tiny positive gaps.
An unsupported degenerate domain or exhausted event budget yields an incomplete result.

**Counting conclusion.** The majority feature has capacity one across disjoint strict
inner cores: two such cores have a strictly separating direction, whereas both being
charged would place the same median projection inside disjoint projection intervals.
An owned-point collision is impossible in a legal packing, so full row coverage forces
each of cells 1 and 2 to receive the majority charge.
Their combined charge two exceeds the budget one.
Require a complete, gap-free closed angle cover of $[0,1]$ for each cell before claiming
this contradiction.

Apply the owner-support and strict-budget transfer rule to every canonical mask and its
whole half-turn. The expected sets have 453 direct representatives and 459 after the
half-turn; compare all IDs with A1. An ownership-only or partial-row result proves no
mask exclusion. The full component may prove these 459 exclusions while retaining
`global_optimality_proved: false`.

Profile one owned-point proof and one complete positive row before selecting the full
run. Record checked point and row identities, remaining angular coverage by cell, exact
refusal reasons, polygon or slab counts, and wall and CPU costs.
These measurements determine later batching and parallel execution; the input size does
not establish a runtime bound.

## Candidate 438 Capture Contract

The case mask is `(0,1,2,3,4,8,9,10,11,13,15)`. The claimed capture partitions its
domain into four closed leaves.
Here $y_{15}$ is the owner’s centered unit-coordinate height and $t_i$ is its half-angle
parameter in $[0,1]$.

| Leaf | Assumptions | Required conclusion |
| --- | --- | --- |
| Far 15 | $y_{15}\le5/4$ | Contradiction |
| Far 13 | $y_{15}\ge5/4$, $t_{13}\le147/512$ | Contradiction |
| Far 2 | $y_{15}\ge5/4$, $t_{13}\ge147/512$, $t_2\le183/512$ | Contradiction |
| Near | $y_{15}\ge5/4$, $t_{13}\ge147/512$, $t_2\ge183/512$ | Inclusion in the independently accepted local isolation rectangle |

Both sides of each cut include equality.
Check the partition as predicates over the full real height and closed angular domains;
a floating-point sample of the leaves is insufficient.
The field-coordinate center cut must have normal $(0,\pm1)$ and bound $\pm B(U/2+5/4)$
with the correct sign.

Check the receipt graph first, then confirm these properties against acquired source
objects:

1. **Root.** Bind the exact case, cover, cap, scale, and ownership seed.
   The root has no branch assumptions.
   Every owner has a complete root induction through round 14. A round count without the
   eleven owner identities is insufficient.
2. **Nodes and premises.** Match the published inventory of ten distinct geometry source
   nodes and 24 bound premises.
   Multiple receipts may refer to the same node; the node’s metadata must agree
   everywhere. The four far/near audits and any cached premise audits must have no
   unresolved dependency.
3. **Parent induction.** Every source parent exists at its declared hash and precedes
   its child. Check both the source-node graph and cached-audit graph for cycles.
   A child retains its parent’s assumptions in order and adds at most one branch
   predicate. An unparented source node has no hidden assumption.
   Refuse continuation from a parent already marked contradictory.
4. **Cached premises.** A cached sibling must be present in an accepted earlier audit
   with identical mathematical fields.
   Every selected leaf node belongs to its actual parent ancestry or has such an
   explicit cached premise.
   File existence and a hash alone do not prove the cached geometry.
5. **Geometry domain.** Each accepted induction preserves all owners, complete closed
   angular coverage, and every residual component, including points and segments.
   A far leaf needs a whole-branch contradiction.
   Entering a local guard or stopping with a residual region does not establish that
   contradiction.
6. **Near-state binding.** The final source state and its constraints must agree with
   the near audit and the pose-inclusion input.
   The role assignment is a bijection between the eleven source owners and exact
   construction squares.
   Check all 136 reported live angular rows and 1,542 vertices against the source;
   retain angular endpoints 0 and 1.

The inclusion map is $(x_f,y_f)\mapsto(y_f/B-U/2,\ U/2-x_f/B)$ into centered unit
coordinates. Compare these coordinates with construction centers relative to $T/2$.
Verify every closed angular interval against the appropriate orientation chart.
Once inclusion and local isolation are proved, a centered packing of side $S\le T$
remains feasible after the rigid map into the fixed container of side $T$; the
construction’s opposite-wall contacts exclude $S<T$. The census or ancestry checks alone
do not establish this conclusion.

## Independent Near-State Pose Inclusion

`think-hjne` checks inclusion after the fixed-$T$ local-isolation component under
`think-sw68`. The accepted
[local receipt](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/local-isolation/result.json)
binds the 33 radii through focused input SHA-256
`9a9cf4e0fdcb1b1d226b9c07ec08d08cbbc572749cec9bc09cf3cd92bd4d88f3`. Use those exact
radii and retain the local receipt’s identity in the inclusion output.
The rectangle has center displacements in unit-square coordinates and angle
displacements in radians; each radius lies in $(0,1/64]$.

The two new objects total **27,656,848 compressed bytes and 185,939,439 decoded bytes**:

| Input | Decoded path | Compressed bytes | Decoded bytes |
| --- | --- | ---: | ---: |
| Near trace | `evidence/research/candidate-capture/near-refined1024-240.json` | 27,653,954 | 185,901,535 |
| Role guards | `evidence/research/phase3/current/research/optimality/global_capture/local-capture-guards.json` | 2,894 | 37,904 |

The near trace has index key
`73ddd73ce616ecb4a74d08c18a17f7eaff044df2111b0e500636b073e43ee970`, decoded SHA-256
`491afdaaf411e7fdb4968bdcda7232ea517ead34739d0ae8c7d5570333a981cc`, and compressed LFS
SHA-256 `5d74352c6c05fd4e0ea4d4842915061603669a54205af2a59cf2303051a48949`. The guard’s
index key and decoded SHA-256 are both
`0bc2edf59cbf620258719db7ba50cdf77af749d38dfbef76a131d32353443fb0`; its compressed LFS
SHA-256 is `13b0aa2153484dc689f0c7b48295e91c5ba91b45c0e9c5921c6e7ba1b23866e3`.

Bind the full trace before extracting `final_state`. Check its mask, cap, scale, and
constraints against the corresponding top-level fields.
Require exactly one matching guard for mask 438, symmetry
`{swap: true, reflect_x: true, reflect_y: false}`, a role bijection between labels 0–10
and all eleven owners, and a `label_to_cell` array consistent with those roles.
State cell keys must be exactly the eleven owners.
Each owner must have at least one live row; check every nonempty residual component of
every live row, preserving singleton points, segments, and singleton angle intervals.

For each encoded vertex $(x_f,y_f)$, compute

$$
c=(y_f/B-U/2,\ U/2-x_f/B).
$$

Independently enclose the exact construction center $c_i^*-(T/2,T/2)$ in rational
intervals. For each coordinate, the maximum distance from $c$ to **both** enclosure
endpoints must be at most its accepted radius.
The affine map and convex coordinate bounds extend the vertex check to the whole encoded
polygon. Record all per-owner row and vertex counts; the total must be 136 live rows and
1,542 vertices, with angular endpoints 0 and 1 both present.

For the angular checks, let $[a,b]\subseteq[0,1]$ be a full closed half-angle row and
$[u_-,u_+]$ the independently isolated algebraic root interval.
Verify the exact witness axes: labels 0–5 have axis $(1,0)$, and labels 6–10 have axis
$((1-u^2)/(1+u^2),2u/(1+u^2))$. The inverse quarter-turn preserves square orientations
modulo $\pi/2$. Check these rational upper bounds on the absolute angular displacement:

| Witness orientation | Row condition | Sufficient bound on $\lvert\Delta\theta\rvert$ |
| --- | --- | --- |
| Axis aligned | $b\le1/2$ | $2b$ |
| Axis aligned | $a\ge1/2$ | $2(1-a)/(1+a)$ |
| Slanted | $b<2/3$ | $2\max(\lvert a-u_+\rvert,\lvert b-u_-\rvert)/(1+\min(a,u_-)^2)$ |

Each bound must be at most the corresponding accepted angular radius.
An axis row straddling $1/2$ fails this chart check.
The first bound uses $\arctan t\le t$; the second uses the axis chart
$\tan((\theta-\pi/2)/2)=(t-1)/(t+1)$; the slanted bound follows from the derivative of
$\arctan$ over the interval between $t$ and $u$. These checks include equality endpoints
and apply to the whole angle interval.
A midpoint calculation is insufficient.

The resulting component may report `PASS_POSE_INCLUSION` with
`conditional_on_source_pose_domains: true`. It must retain false capture and global
optimality flags.
Refusal controls should cover a wrong cap or scale, wrong inverse chart
sign, a vertex or angular bound just outside its radius, a missing owner or component,
and a nonbijective role map.
An in-range singleton polygon and singleton angle row must remain admissible.
Geometric ancestry is accepted separately under `think-pgie`; accepting inclusion does
not accept the trace’s pruning history.

## Root Induction and Geometric Transitions

`think-mnd1` remains open for independent geometric acceptance.
Source review of
[`audit_residual_kernel_v2.py`](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/src/evidence/research/phase3/work/phase3/hull/audit_residual_kernel_v2.py)
and
[`audit_capture_portable.py`](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/src/evidence/research/candidate-capture/audit_capture_portable.py)
found no geometric contradiction in the ownership, strict-core, and collision
implications examined.
The supplied instances still require independent replay.
The four published final-state binding defects remain separate from this mathematical
obligation; replacing their hashes does not establish the geometry.

The two adaptive-root inputs have been acquired and checked against both the pinned LFS
identities and decoded identities, totaling **21,258,733 compressed bytes and
136,828,193 decoded bytes**:

| Input | Decoded package path | Compressed bytes | Decoded bytes |
| --- | --- | ---: | ---: |
| Adaptive root | `evidence/research/phase3/work/phase2/conditional/mask438-adaptive.json` | 21,255,326 | 136,801,164 |
| Ownership seed | `evidence/research/phase3/work/phase2/conditional/mask438-seed.json` | 3,407 | 27,029 |

For these two objects the index keys equal their decoded SHA-256 values:

```text
adaptive decoded 5452ed7fe20266ec81749b79c1e00f4e9a2ba75242b25d90b7fb696ca317d40a
adaptive LFS     cf9e5e8d3722587f21ccd746ff4005662a5bf12c1e9e0b47fa32b86a402db9f1
seed decoded     b93be3358f7dfbf063d4109c52fd3bbbbfff9b34cb468c3123598b54cea72a56
seed LFS         ad9c0c9c00c54301dd49b1fcd771d7a9a3a14e894fe904b949fe415dceddf7f2
```

The adaptive payload contains all fourteen rounds, with eleven complete owner updates
per round and 16,551 angular rows.
Its first seven rounds each have 777 rows, the next four each have 1,251, and the last
three each have 2,036. It declares no branch, contradiction, or local-guard capture.
Its `resume` record names an earlier producer checkpoint, but replaying the included
rounds from the seed requires no assumption from that checkpoint.
These are observed source counts, not accepted geometric conclusions.

The root acceptance kernel must establish the following induction:

1. Reconstruct each field-coordinate center cell $W_i=B(1/2+(U-1)V_i)$ from the accepted
   cover cell $V_i$. Check the exact case, cap, scale, and all 130 seed points belonging
   to occupied owners. Every such point must lie strictly inside every legal side-$B$
   square with center in its owner cell.
   The existing exact disk test or closed-angle wall subdivision can establish this.
2. Bind each round’s prior point groups to the preceding accepted state.
   For every owner in that round, use the same prior snapshot for the other owners’
   hulls. The eleven owner updates may run independently; their newly derived points
   become available only after the round finishes.
3. Require each owner’s closed angular rows to partition $[0,1]$. An inherited support
   cut must contain every vertex of the referenced prior residual polygons, and the new
   interval must lie inside that prior interval.
   Reconstruct the legal-wall outer domain.
   Empty inherited residuals may delete an angle only after accepting the referenced
   row.
4. Treat each proposed core $Q$ as geometric input: prove that it is strictly inside
   every side-$B$ square orientation throughout the row.
   For prior owned hulls $H_j$, reconstruct the forbidden center regions $H_j-Q$ for
   occupied owners $j\ne i$. Prove that their union with the proposed residual polygons
   covers the entire closed center domain.
   An uncovered point invalidates this localization certificate; it does not by itself
   exhibit a feasible eleven-square packing.
5. After all angular rows accept, prove each proposed new owned point belongs to $z+Q$
   for every center $z$ in every live residual polygon.
   Linear inequalities need checking at all residual vertices.
   Verify each compressed output point as an exact convex combination of prior owned
   points and accepted new points, with nonnegative coefficients summing to one.
   Bind the reconstructed output groups to the source state.
   Partial angular coverage promotes no points.

The first bounded pilot should check all 130 occupied seed points, profile one row of
round 1 for owner 2, then check that owner’s full 69-row update.
Those rows contain at most six residual polygons each; the update proposes 28 kernel
vertices and seven compressed output points.
Passing this pilot establishes one conditional ownership update.
Acceptance of the full adaptive root requires all 154 owner updates and their state
bindings. Measure exact arithmetic and arrangement work before scheduling the remaining
rows; file size and the publisher’s slab counts do not predict replay time.

The retained
[owner-2 receipt](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-root-pilot/owner2-final-result.json)
now accepts that bounded pilot: all 130 seed points, all 69 rows, and seven exact
compressed ownership points, in 10.947 seconds of checker wall time.
Source review confirms that the proposed core is admitted only after strict quadratic
enclosure throughout each angle interval, the complete legal center domain is covered,
and point or segment residuals remain in the coverage and support calculations.
The shared rational geometry kernel is explicitly bound by SHA-256; this is an
independent reconstruction of the geometric implication using previously reviewed local
primitives.

The first
[round-one join receipt](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-root-round1-attempt1/result.json)
records all eleven owners and 777 rows, producing 100 exact compressed additions and a
reconstructed next prior equal to the source, in 32.518 seconds with three worker
processes. Its source review approves the conditional induction step: every worker uses
the same accepted seed snapshot, new points become available only at the complete join,
and exact convex-combination witnesses justify compression.
Worker receipts bind the same source, prior, checker, and shared kernel; the join
requires every owner exactly once.
Focused refusal controls for missing owners, changed worker bindings, and invalid convex
weights accompany acceptance of this runner.
Neither receipt accepts all fourteen rounds, the later transition tree, candidate
capture, or global optimality; all those verdict flags remain false.

Later-round acceptance is conditional on the preceding independently accepted geometry.
Every current closed angle interval must lie within its cited prior interval, and each
inherited support bound must contain every prior residual vertex, including degenerate
residuals. An excluded prior interval stays explicitly excluded.
A receipt-only chain audit must bind all fourteen aggregate results and owner files back
to the pinned first result and declare the actual local geometric executions as its
premise. Matching status fields and checker hashes cannot establish that execution
occurred. Full root acceptance requires those observed, reviewed executions and their
complete joins; it does not follow from the last round number alone.

The ten later source nodes are already acquired.
Their first node, `root.json` in the local source-graph cache, records a later
fourteen-step transition from the adaptive root.
Its last step is incomplete and leaves the prior recorded state unchanged.
A verifier must preserve that behavior rather than infer that every recorded step makes
progress. For these later transitions, extend the root kernel with these obligations:

- Check self-owned-hull center cuts using support bounds valid throughout each closed
  angular interval. For a proposed core vertex $(x,y)$ and half-angle $t$, strict
  containment follows by proving both quadratics
  $B/2-\sigma x-2\sigma yt+(B/2+\sigma x)t^2>0$ and
  $B/2-\sigma y+2\sigma xt+(B/2+\sigma y)t^2>0$ for each $\sigma\in\{-1,1\}$. Check
  endpoints and every in-interval quadratic minimum exactly.
- Bind every partner pose domain $D_j$ and core $Q_j$ to accepted parent geometry and a
  complete permitted angular partition.
  A proposed universal collision polygon $P$ for query core $Q_i$ must satisfy
  $P\subseteq\bigcap_{y\in D_j}(y+Q_j-Q_i)$ for every partner row.
  For each facet $n\cdot v\le h$ of $Q_j-Q_i$, this is the exact vertex inequality
  $n\cdot p\le h+\min_{y\in D_j}n\cdot y$. Equality is safe because the two cores lie
  strictly inside the physical squares.
- Preserve inherited branch predicates and the closed row-domain cover.
  Check point and segment domains explicitly or refuse them; deleting a zero-area domain
  can lose a legal pose.
  A complete empty pose cover proves a contradiction, while an incomplete step with no
  point promotion leaves its prior state intact.
- Accept a cached state only through an accepted geometric node receipt with identical
  input and output states, assumptions, kernel identity, and acyclic accepted ancestry.
  Published status fields, source hashes, and completed-node inventories establish
  identity and structure; they do not discharge the geometric implication.

The far-branch contradictions, near capture, and final composition remain open until
these root and transition checks accept their complete dependency closure.

## Generic Weighted Field Admission

A pinned manifest may replace hand-written field descriptors without changing the proof
rule. The manifest binds each packet and audit proposal to the source revision, index
key, compressed and decoded identities and sizes, and A1 certificate identity.
Feature indices, ownership counts, and row subdivisions are proposal data; extracting
them supplies no geometric acceptance.

Admit only exact rational sites at the declared scale, nonnegative integer point
weights, and positive integer weighted `majority_hull` features with three, five, or
seven distinct valid site indices.
Reject booleans and floats where integers are required.
Each feature must have threshold $(m+1)/2$ for its odd arity $m$ and a unique atom
identifier.
Recompute the global budget as the sum of point and feature weights and match
the packet’s declaration.
Require at least one charged resource.
Other feature kinds need a separately reviewed capacity proof.

The capacity-one argument is independent of a producer’s feature table.
For $2k-1$ sites and a closed square core $Q$, the majority region consists of centers
$z$ for which $z+Q$ intersects the convex hull of every $k$-subset of sites.
Its inequalities are median projection strips, with core support $r(|n_x|+|n_y|)$ for a
square of half-side $r$ in its own frame.
Square axes and normals perpendicular to site pairs supply all required facet
directions; exact ties and collinear sites remain admissible.
Two disjoint physical square interiors have a separating projection.
The same site median cannot belong to both projected cores when each core lies strictly
inside its physical square, so a majority resource can charge at most one square.
A point resource also has capacity one.
Different resources may share sites; summing their weighted capacities remains valid.

Require exactly sixteen nonnegative integer cell thresholds.
Positive cells may have different thresholds; each row uses its own cell’s value.
Derive the positive cells from all sixteen packet thresholds, never from the cells
present in the audit proposal.
Every positive cell requires a nonempty exact closed partition of $[0,1]$, with no
omitted endpoint, gap, interior overlap, duplicate interval, or extra cell.
Deriving both row counts and positive cells from an incomplete audit would lose this
obligation.
Ownership support must contain distinct valid cells in the packet mask; check
every point used by the geometric argument under that support before transfer.
The cover, cap, scale, and packet-to-audit bindings remain mandatory.

For each row, reconstruct one convex region per physical atom and count its weight once.
An owned-point collision region is an infeasibility alternative and may carry the local
cell threshold in the coverage check; it contributes nothing to the global physical
budget. Check the weighted sum at every exact polygon-edge crossing and vertex abscissa,
between consecutive abscissae, and at every resulting vertical endpoint and open
interval. Affine endpoint order between events proves the complete closed domain.
Closed membership is safe only with the strict whole-angle core and ownership margins
already checked by the geometric kernel.

Owned collision alternatives may be pruned by bounding-box containment when both regions
are intersections of the same closed domain with axis-aligned capture boxes.
If $A=D\cap Q_A$ and $B=D\cap Q_B$, then
$\operatorname{bbox}(A)\subseteq\operatorname{bbox}(B)$ implies $A\subseteq B$. Keep one
representative on equality.
Do not apply that argument to majority regions or discard distinct physical charges.

After complete geometry, recompute applicable canonical masks from occupied support and
a cell-threshold sum strictly greater than the independently derived budget, including
the whole-packing half-turn alternative.
Compare the exact resulting IDs with the pinned A1 certificate set.
Partial, unsupported, or interrupted fields exclude zero cases; aggregate accepted
fields by set union.
Controls must include deletion of an entire positive-cell row group, a missing owner,
budget equality, duplicate atoms, insufficient charge, a closed seam, and a sloped gap
between coarse probes.
Parallel scheduling changes neither these premises nor the complete acceptance rule.

## Bounded Execution and Refusal Controls

Implement the checks in retained tools and exercise only their affected contracts.
Use positive synthetic controls and targeted mutations: omitted or duplicated case,
strict budget equality, lost support owner, wrong cap, missing parent, parent cycle,
dropped inherited constraint, unproved cached sibling, strict instead of closed branch
boundary, omitted degenerate region, and changed near-state identity.
Do not run general repository tests, a full checkpoint, or an atlas rebuild for this
slice.

Before each acquisition, report the selected object count and declared compressed and
decoded sizes from the pinned index.
Acquire the two small packages separately; use their references to select later
payloads. Read large source objects one at a time in verified external scratch.
A reusable extractor may retain compact parent, constraint, and final-state projections,
bound to the full source digest and extractor identity.
Those projections accelerate repeat checks without supplying omitted geometry.

Select the remaining source ancestry from B1–B7 before estimating or scheduling its
replay.

Each run records the source revision, checker and input identities, exact checked and
unresolved IDs, wall time, process CPU time, and the chosen wall ceiling.
Record outer process wall/CPU costs separately from checker phases.
On timeout or missing data, retain the completed census and stop before acceptance;
resume only against unchanged inputs and checker semantics.
These bytes and counts are observations; no runtime or speedup estimate follows from
them.

## Payload Identities

For each table ID, the first value below is the content-index key and the second is the
decoded SHA-256. Resolve the compressed object path from the index and its compressed
identity from the pinned LFS pointer inventory.

```text
A1 60add61f5efc56652a350944ad34cafd19d9c590f058ebaad2d98d8854be9538 04fa1ebb37f5dace29946224fe8c7c5d8a1bedb4fa860c65b359f4200415de57
A2 d3c8a8f207c986462c6c85d399b739fce7841e0adaff6b75801ac171bc319db4 719efa40df07d5cb29874a44483737a4903c82498f18b348fc05b5ad08daa8e6
A3 ba2ba3eae20ffa7b88bbc8e97928a073d7c084d1976211fa16e5e6338860fcc1 ba2ba3eae20ffa7b88bbc8e97928a073d7c084d1976211fa16e5e6338860fcc1
A4 3f5ce8ccd45268a34f567f87897640255ea946dec3e43f1bca161a951806f0d1 03d6e82a9bde1bad6cf6683081cff2b583d7f60fddb2c810c91e071cb4575864
A5 8147c29389e597227ddee71ebacafe7358b0fd6b8e07885fb0e0ff0ab860a3cb 7920ae9fede574c58ea36893724a55911a02f2875dd808f799a99fd3ea0ee18e
B1 4b940a7b89b4fbb51e4231e7595d48adc83e2dfa0ff0f789eafbe03923c46a8d f5c66ab125f7a4695039197ae52b5ce5ee2dd2365142e4cf8488a220f250f5d5
B2 bcd0048d125f5582653de5f2180723fd4962fb2658c8f5034ba1c8f9979881e9 dd192f1a95fe23d0ae63112ef8f6f78ee31ba2f81241c47abf2b48299e430f45
B3 a3e3ebb9bb89be3e430ef7b813efe075f27d069e688228fa54299370cac9d104 8e369168774ba97721ba49efcff2d35cbe5f0d86f3e01a37b419a800e047d7e4
B4 6d654d2518955a5f9ab6c45100904168f37c262e410575a5e1472e8e4716b87d c68188a3ecd68ae865c139347cf5d4234f3e99e69c16709c806f4d307e732689
B5 0053aa7ea7354d2bc9ba2a23d9f53fc50ccb70865f01668a342d40dc5f9d2294 6088857994ed2fae2e5de5f27c0fccbeb7aac668736506fa81b6afdfefeed7e3
B6 6c3ba29494ae83a98531ad8dafc98dd919ba37f230e44ec68d593c5e573dcc81 cc9b3d39e30bcf76a27956a7c453476d9364f6c3d2cc9864d66506ec65306832
B7 8f898b9c197d0ff7ae85266ce8ee2fdc225954d01657a413600ec4c6612ef8c5 4a93b7c841b4380fb0bd481b6d57e595d9f4ae84fe3ce86fc57bad7374c765a3
```

## Fresh Generic Induction and Degenerate Domains

Astra-max review on 2026-09-30 found no mathematical blocker in the supported fresh-wall
induction of the
[generic checker](../../../packing/devtools/check_n11_generic_fresh.py).
For case 2095 it reconstructs all 352 seed rows from the accepted cover and legal-wall
envelopes, proves the 77 seed points strictly owned, and checks five sequential updates
with 32 closed angular rows each.
Every proposed core vertex must satisfy the strict containment quadratics throughout the
complete interval, including its endpoints and any interior minimum.
Convexity then places the entire core strictly inside the physical square.

For another occupied owner’s strictly owned hull $H$ and the query core $Q$, the
reconstructed Minkowski difference $H-Q$ is forbidden: a center there places a point of
$H$ inside both physical square interiors.
The exact sweep must cover the complete legal center domain by these forbidden regions
and the proposed residuals.
If $n\cdot q\le b$ is a core facet, the common-ownership condition is
$n\cdot p\le b+\min_{z\in R}n\cdot z$ over every live residual $R$ in every row.
Its minimum occurs at a residual vertex, including a singleton or segment endpoint.
Thus each promoted point belongs to every possible translate of the strict core.
Exact nonnegative convex-combination witnesses preserve that ownership during
compression.

The row workers consume one frozen predecessor state; the next step receives their
results only after all 32 rows finish.
The checker normalizes accepted polygons before subsequent clipping, validates support
bounds against every residual vertex, and binds the reconstructed final groups and rows
to the source state.
Case 2095 requires independently empty residuals in all 32 rows of terminal owner 11,
then an exact match to its sole A1 generic assignment.
The publisher’s terminal and audit status fields supply no geometric premise.
The seed and one-row diagnostic scopes accept no exclusion.

The accepted
[full result](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/generic-mask2095-intake/full-result.json)
binds checker `e8fcfd02560d09e7a2a5b2622976ab021ef15a4456a2824b37abae926f6ab7d3` and has
SHA-256 `2aa9c3819e4f39d9f4f489a25d1885b2a1c5a6f6c21099f42821d1165d608f88`. It completes
those inventories with no pending row and accepts exactly case 2095 in 23.753 seconds
wall, 5.611 seconds coordinator CPU, and 35.086 seconds child CPU. Eight focused generic
tests pass, including the full replay and refusals for a strict core touching the
physical boundary, a removed necessary residual, a changed predecessor, invalid
compression, tampered source, and expiry.
This adds one case to the accepted 1,904-case field union: 1,905 exclusions are accepted
and 275 non-field exclusions remain open.
The global optimality flag remains false.

The
[degenerate-domain helper](../../../packing/devtools/check_n11_closed_degenerate_cover.py)
correctly extends closed coverage to a legal point or segment.
Write the domain as $z(t)=a+t(b-a)$ for $0\le t\le1$. Pulling back each convex region’s
halfplanes gives exact closed linear intervals in $t$; their intersection is that
region’s intersection with the domain.
Sorted interval union covers the domain exactly when it reaches from zero to one without
a positive gap. Coincident endpoints are retained, and $a=b$ reduces to ordinary point
membership. Point regions use coordinate equalities, segment regions use their line
equality and coordinate bounds, and positive-area regions use their hull facets.
The helper rejects a proposed polygon whose area differs from its hull; consistent local
turns alone would not reject a star traversal.
The continuation keeps the existing sweep for positive-area domains and verifies empty
residuals and strips when the reconstructed legal domain is empty.

The revised
[root continuation](../../../packing/devtools/check_n11_capture_root_continue.py) admits
the earlier rounds through the frozen checker at commit `0f6b1e2d1`, whose SHA-256 is
`dbde306a481333b470f1e2613ff05fd2be65c9711dd135615d65548932cebdd3`. The round-one
checker, pilot, geometry kernel, and fixed round-one result also match their recorded
identities. This source bridge preserves the conditional induction rule.
It does not establish historical execution from a claimed `PASS`: full root acceptance
still requires the observed geometric runs and complete joins of all fourteen rounds,
rooted at the fixed first result.
Even a complete adaptive root leaves the later transition tree, branch capture, and
global composition to be checked.

The accepted
[round-eight result](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-root-round8-final/result.json)
checks all eleven owners and 1,251 rows, with 91 compressed additions and an exact
joined next state, in 76.119 seconds wall.
It binds continuation checker
`17fc81b2b08a80456325b347b3effa25050e4e233d9a984292e0d6339bb64e73` and the reviewed
helper `858c61c3ffa464a12be0fda9a14f802d7d9ea22f9b6aaa2b06c6974f0caa5385`. The first
eight accepted rounds cover 88 owner updates and 6,690 rows; root, capture, and global
verdicts remain false.
Four helper controls exercise closed ties, a positive gap, point and segment regions,
and rejection of area domains or malformed polygons, including a star traversal.
Together with inherited-domain and generic refusal controls, the focused review run
passed fourteen tests in 4.90 seconds; the separate complete generic replay is the
eighth generic test above.

## Complete Adaptive Root Receipt Chain

The fourteen retained, accepted geometric executions now cover 154 owner updates and
16,551 rows, adding 1,060 owned points to the fixed seed state.
The [chain audit](../../../packing/devtools/check_n11_capture_root_chain.py), reviewed
at SHA-256 `fdc46b2178bcfc91b97dfbd1fa45c7ec193cd5778800b31a98461ecc30f66a75`, checks
all 168 aggregate and worker receipt files against the pinned adaptive source.
It starts from the fixed round-one result, reconstructs every common prior and joined
next state, and requires each owner’s complete row count and exact compressed output.
No owner consumes additions from another owner in the same round.
Every joined state equals the next source prior, including the final adaptive output.

The checker revisions are explicit: the fixed first-round checker; `dbde306a…` for
rounds two through seven; `17fc81b2…` for rounds eight through eleven; and
`3eca359a215cde005b79fbd9f7866000f75b48bb3f50ce0b3a3d9b2d9db83b34` for rounds twelve
through fourteen.
The last revision changes only the selected owner ceiling from 30 to 60
seconds and admits the pinned preceding checker revision.
Its geometric operations and the `858c61c3…` degenerate-domain helper are unchanged.
The complete prior checker is retained at commit `cb8e8b8c4` and matches its declared
`17fc81b2…` digest.

The
[chain result](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-root-chain/result.json),
SHA-256 `f10d50e6b34179a6b2fb066d6ade9553057c280f7538ae6e53fe06e639a56d11`, passes in
28.385 seconds and binds final state
`914d6337ee4231fb4980693f8ece49b2d16d0a35b31b6b1f402b627a2dda9d3f`. This is an accepted
receipt-and-state audit conditional on the reported actual geometric executions; a
cached status or hash cannot establish that those executions occurred.
The observed executions and their complete joins support the adaptive root induction.
The audit itself retains false conditional-root, candidate-capture, and global flags.
Transition-tree coverage, branch capture, and final composition remain open.
Focused review controls for revision boundaries, incomplete worker rows, stale prior
bindings, and altered output pass together with the shared generic controls: six tests
in 0.17 seconds, with the full generic replay deselected.

## Shared Single-Node Generic Replay

The [shared checker](../../../packing/devtools/check_n11_generic_sequential.py)
preserves the reviewed fresh-wall induction while admitting the pinned recipe’s bin
count, mask, seed, and A1 or A3 assignment.
The exact full-square support quadratics above justify every added self-hull cut before
it restricts a legal center domain.
Each row starts from its accepted predecessor hull, and parallel rows use the same prior
ownership state until their complete join.
Strict cores, residual coverage, common ownership, compression, and the reconstructed
final state retain the earlier mathematical checks.
The sole terminal exclusion must have empty residuals in every angular row.
The imported generic and geometry kernels are explicitly pinned, and all consumed file
identities must remain unchanged during replay.
A2 assignment, multiple source nodes, partner covers, guarded branches, and degenerate
generic domains remain refused by this adapter.

The accepted
[case-2135 result](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/generic-case2135-pilot/final-result.json)
binds shared checker `820f35f7dfeb5ec9dd0cd276305f3e86a230abfccb94ee2a70463682f69d6e15`
and has SHA-256 `ecd3b2cd820ae92c0770641031a789b25ee9739cdba5f2064232f7b7ace234be`. It
checks 75 owned seed points and 88 seed rows, then all 48 rows in six sequential
updates, finishing with empty residuals in all eight rows of owner 10. No node, step, or
row remains pending.
The receipt accepts exactly case 2135 and keeps global optimality false; its costs are
8.706 seconds wall, 3.779 seconds coordinator CPU, and 11.440 seconds child CPU. An
independent focused run passes eight refusal controls in 3.48 seconds, including a
missing angular row, changed initial state, unjustified domain shrink, invalid
full-square cut, helper-pin mismatch, altered assignment, unsupported ancestry, and
expiry.

## Compiled Exact Coverage

The [compiled sweep](../../../packing/devtools/n11_fast_exact_cover.py), reviewed at
SHA-256 `eb21b1acda671b9f858039d077b0c8a30d035ee5920e083887952bf44b156904`, is sound for
a positive-area convex domain and finitely many closed convex covering regions; covering
regions may also be points or segments.
Callers retain responsibility for that convexity contract.
Its increasing probes activate edges at their left endpoint and remove them strictly
after their right endpoint, preserving closed intersections exactly.
Polygon vertices and overlapping-edge crossings partition the sweep into slabs with
fixed affine endpoint order, so the existing event and midpoint probes remain complete.

The new vertical predicate skips intervals ending below the current cursor before
testing coverage.
This fixes an inherited predicate weakness for a singleton target slice
without changing the frozen historical kernel.
The weakness cannot produce a false full-cover acceptance under the reviewed historical
contract: every slice strictly inside a positive-area convex domain’s horizontal
projection has positive height, so the sweep correctly covers all those slices.
Their closure is the whole domain, and a finite union of closed covering regions
contains their limits.
This argument grants no extension to degenerate domains or nonconvex inputs.
Direct controls now distinguish intervals below or above a singleton from intervals
touching it, preserving equality.

The
[matched benchmark](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/nonfield-manifest/fast-cover-benchmark-final.json)
binds this helper and the unchanged historical sources.
On three rows of case 2095, three repetitions per row preserve the exact event, probe,
and edge counts and measure median CPU speedups of 1.85–1.94, with median 1.89. Those
measurements describe these rows only.

## Adaptive-Root to Capture Input Bridge

The [bridge checker](../../../packing/devtools/check_n11_capture_root_bridge.py),
SHA-256 `2bbddc8f27575eb6a61e0a4f97e0cb71194357fbd6a341ec1d710a6a2c1ae9a5`, verifies
that all eleven initial capture hulls equal the accepted adaptive-root hulls.
Taking those convex hulls preserves strict ownership.
It matches all 2,036 ordered phase-two row references and the first capture step’s 217
references for owner 15, with exact cap, scale, mask, source, and final adaptive-state
bindings. The pilot, round-one, and geometry dependencies are pinned and checked before
and after; canonical-state hashing uses the standard library directly.

The
[final bridge result](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-root-bridge-final2/result.json),
SHA-256 `ba65b7416678f701feee8c027e2b4f9359e9d3324ceee0958fbc8ca30afe309d`, passes in
2.876 seconds. This accepts the input bridge conditional on the accepted root execution
chain. It proves no capture transition and keeps capture and global flags false.
Transition consumers must still resolve every referenced domain from its accepted source
and prove the complete geometric update.
Focused bridge and singleton-slice controls pass in 0.07 seconds.

## Endpoint and Final-Composition Readiness

Static review confirms that the accepted
[local-isolation execution](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/local-isolation/result.json)
already discharges the exact construction and endpoint prerequisites.
Its [checker](../../../packing/devtools/check_n11_optimality_local_isolation.py) invokes
[the witness loader](../../../packing/cases/trump11/isolation_radius.py), which verifies
all eleven unit-square shapes, all 44 vertices against the container, and all 55 pairs
with weak separating axes through the
[exact packing verifier](../../../packing/src/sqpack/verify.py).
The same execution isolates the specified root $u\in(9/25,37/100)$, encloses
$T=(6u+4)/(1+2u-u^2)$ strictly below $U$, and checks exact contacts with both opposite
walls in each coordinate.
The current construction and arithmetic source identities match those retained in the
accepted local receipt.
A separate upper-witness replay is therefore not a missing premise of this composition.

For any putative packing of side $S<T$, centering its container at $(U/2,U/2)$ embeds it
into the cap without changing the unit squares.
Every $D_4$ image preserves that concentric side-$S$ container.
The accepted inclusion map is exactly $Q^{-1}(p_f/B-(U/2,U/2))+(T/2,T/2)$, so it places
the image in $[(T-S)/2,(T+S)/2]^2\subset[0,T]^2$. The same labeled centers and
orientation charts then satisfy the fixed-$T$ local theorem once the near-state ancestry
is proved. That theorem forces the exact construction, whose span $T$ contradicts
containment in side $S<T$. Once the pending exclusion and capture premises are accepted,
the verified witness at $T$ supplies the matching upper bound.
No compactness or limiting argument is needed.

The remaining final implication is conditional: the exact exclusion union must leave
only cases 438, 999, 1462, and 1659; the accepted symmetry lemma must then supply a
case-438 image; and complete capture must bind that image to the already accepted
pose-inclusion and local-isolation states.
Every exclusion assumption and reused ancestry must be discharged without cycles.
The final consumer must preserve these distinct scopes: noncandidate exclusions hold at
$U$, whereas the candidate conclusion excludes sides below $T$. No additional analytic
premise was found in this composition review.

## Repeated Owners and the Coverage Target

Sequential induction may revisit an owner when every prior owned hull still matches the
current accepted state and every row consumes that owner’s current accepted predecessor.
All row results must join before the next promotion.
Removing a one-visit restriction does not weaken those obligations.
An early capability check may refuse unsupported partner covers, guards, or source
grammar before doing the ownership work.

The pinned
[`audit_capture_v9.py`](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/src/evidence/research/phase3/work/phase3/hull/audit_capture_v9.py#L118-L127)
distinguishes two domains: `row.input_domain` is recorded after inherited and self-hull
cuts, while `residual_cover` additionally clips it by the full-angle legal-wall bounds.
Consequently the source input can properly contain the actual coverage target.
A failed attempt to cover the entire source input is not itself a certificate defect.

For independent replay, let $D$ be the accepted predecessor outer domain intersected
with independently necessary wall and self-hull cuts.
The induction already proves that every feasible center lies in $D$. One may therefore
check exact forbidden-plus-residual coverage directly on $D$ while retaining the
compatibility check $D\subseteq\operatorname{conv}(P)$ for the source input $P$.
Validate $P$ as convex and normalize it; retain the positive-area requirement on $D$ in
this adapter. Keep all proposed residual polygons and compute ownership minima and
support bounds over all their vertices, including vertices outside $D$. That
overapproximation makes those subsequent obligations stronger and preserves every legal
pose. This mathematical rule grants no exclusion until a complete source-bound execution
accepts the case.

The reviewed implementation is shared checker
`6294b3eb43727c08635fde1407de6629946e2c2138f6c712150f0b9cf2a8114d`. It defaults to the
reference sweep and optionally uses the pinned compiled sweep, propagating the selected
backend to every row worker and binding its source when used.
The accepted
[case-2129 execution](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/generic-case2129-repeated/attempt-3.json),
SHA-256 `69a65557ab5c8b15f90087ecd20c0faca4a983982adc7a509f983d33c8bcea31`, uses the
reference backend. It checks 70 strict seed points and 88 seed rows, then 18 complete
sequential updates and all 144 rows, including repeated owners.
Terminal owner 10 has empty residuals in all eight rows; no node, step, or row remains
pending. The receipt accepts exactly case 2129 and retains false global optimality.
Its costs are 22.598 seconds wall, 4.269 seconds coordinator CPU, and 43.823 seconds
child CPU. The two earlier refused attempts retain zero credit.

## First Capture Transition Row

The [transition pilot](../../../packing/devtools/check_n11_capture_transition_pilot.py),
SHA-256 `22c5b4d1f23d48bcc4333bd279df41ba022c337109d063073771349b2854b309`, accepts only
root-self step zero, row zero, for owner 15. It reconstructs the accepted phase-two
support domains and checks all 149 partner-10 rows, including the complete closed angle
partition and all 93 live domains.
Self-hull cuts use full-square support bounds, and both query and partner cores lie
strictly inside every physical square throughout their respective angle intervals.

For every live partner domain $D$, the 23-vertex collision region is checked against
every facet $n\cdot v\le h$ of $Q_{10}-Q_{15}$ using
$n\cdot p\le h+\min_{y\in D}n\cdot y$. Thus every proposed query center forces a common
core point for every remaining partner pose.
Even equality gives a point in both physical interiors, so their intersection contains
an open disk and has positive area.
The row then checks its complete legal-domain cover, all common-ownership facets, and
the eight outer support bounds and resulting domain.
No point or segment domain is discarded by area alone.

The
[retained result](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-transition-row0/result.json),
SHA-256 `7a46c8bf3ef348ddcf5061785728a5e507ae2bc3ed70fc991fd3f16e70efeb0d`, completes
34,224 universal facet-vertex inequalities, 44 coverage events, 87 probes, and eight
common-core planes in 5.170 seconds.
Its helper and source identities are checked before and after execution.
This accepts one row’s geometry; it promotes no owned-point compression, complete step,
source node, candidate capture, or global conclusion.

## Closed Lower-Dimensional Generic Domains

The shared checker revision
`19cf2e57a5647125f8760ad4bf69511beff14c049aee15b731ec0184f5f6245f` extends the reviewed
induction to empty, point, and segment legal domains.
It reconstructs the required domain before interpreting source output.
An empty domain retains its exact row identity and angle interval and permits only empty
geometric output. A nonempty point or segment uses the already reviewed closed-interval
cover helper, pinned to
`858c61c3ffa464a12be0fda9a14f802d7d9ea22f9b6aaa2b06c6974f0caa5385` before and after
execution. Strict physical core containment, necessary cuts, source-hint inclusion,
residual support bounds, and same-prior joins retain their previous obligations.
The positive-area sweeps receive only positive-area domains; no zero-area domain is
discarded merely because its area vanishes.

The
[four-case batch](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/nonfield-batch-a1-degenerate/summary.json),
SHA-256 `427fe5214650689ed75c9f4aa78fb6a1950e0c70ab88c06318fb0705c8d484ed`, records
complete executions of cases 1681, 1690, 1692, and 1727 under this exact revision.
The first three each accept 23 sequential updates and 736 rows; the fourth accepts 16
updates and 512 rows.
All four retain exact singleton exclusions, empty pending work, and false
global-optimality flags.
Their compressed and decoded receipt hashes match the batch index.
Together they accept 85 updates and 2,720 rows in a batch wall time of 98.696 seconds.
This accepts those four exclusions conditional on the observed executions; receipt
inspection alone does not replace their geometric replay.

## Special-Adapter Implementation Lemmas

The pinned
[support replay](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/src/evidence/research/global-math/audit_all_overlay_support.py)
and
[direct vertex test](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/src/evidence/research/global-math/overlay_field_halfplanes_v2.py)
confirm a smaller sufficient proof for the 2175/2176 constraints.
Reuse the independently reconstructed 220 closed overlay regions and strict distance
bans. For each source owner, collect the regions having a vertex that violates any
requested plane after the exact map $v\mapsto B((1/2,1/2)+(U-1)v)$. Exhaustively reject
those forced owner-region assignments using all 506 raw masks from the exact 253-case A1
complement. Every other region may remain without a feasibility witness.
Its vertices satisfy every relevant plane, so convexity proves the required center
inequalities without trusting publisher support hulls.

The finite search assigns one region to each of the eleven source owners.
Compatibility requires distinct cell labels in all four views and excludes only
independently strict distance bans.
The cell-diameter lemma makes those distinctness conditions necessary, including at
closed-cell ties.
Each view’s target set consists of allowed masks containing every label
chosen so far; after eleven distinct labels, containment in an eleven-cell target means
equality. Thus this search overapproximates every feasible packing.
It must retain the eight singleton overlay regions, both half-turn orientations of each
canonical survivor, and equality in the proposed planes.
The final bridge’s six-mask search cannot be reused unchanged.
A surviving assignment or interrupted search leaves that region unexcluded.
This lemma remains conditional on accepted executions covering the exact 1,931 A1 IDs,
with no target-case or cyclic dependency.

For 1383, the pinned
[node replay](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/src/evidence/research/phase3/work/phase3/hull/audit_capture_v9.py)
allows successive updates to refine the angular partition.
Validate every row against its exact accepted predecessor reference and closed
containing interval, then require a gap-free full partition before promotion; a fixed
seed-bin count is insufficient.
Apply each inherited center condition to both query and partner domains for its owner.
A final incomplete source step may be ignored only when it promotes no state and the
reported final state equals the state reconstructed from complete updates; skipped rows
must remain explicitly unaccepted.
Both split children consume separate copies of the same accepted parent state, with
their respective closed halfplanes.

A generic leaf may close through a complete empty pose cover or an independently checked
intersection of two accepted strict owned hulls.
A shared point, including a degenerate intersection, lies in both physical interiors and
therefore forces positive-area overlap.
Neither local-guard capture nor points learned on the sibling branch establish such a
contradiction. The source audit supplies these implementation rules; actual large-node
ancestry and branch geometry remain to be read and replayed.
The A2 assignment helper separately checks source/census identity only; its six focused
controls pass in 0.23 seconds and grant no exclusion or baseline geometry.

## First Complete Capture Owner Update

The [complete-step checker](../../../packing/devtools/check_n11_capture_step0.py),
SHA-256 `3e8180817ffedff6406c13e1e98ac5beacad54a2d8bd9695c8a238b4467f78af`, gives all
217 rows the same accepted root hulls and independently checked partner cover.
Their closed angular intervals partition $[0,1]$. Only after every row accepts does the
ordered join test the proposed common kernel against all residual ownership planes and
verify the additions as exact convex combinations of the accepted hull and kernel.
All eleven prior owned hulls recorded for the following step match the resulting state.
The acceptance flag is set only after final source, dependency, and deadline checks.

The
[complete execution](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-step0/result.json),
SHA-256 `8ca86cc3f119c1dc42e14b142d04cf6863934b799b8e8b6818e54830b1d22b78`, checks 149
partner rows, including 93 live domains, and 3,173,632 universal facet-vertex
inequalities. The 217 query rows require 3,546 coverage events and 6,919 probes.
All 1,320 common-core planes accept the 60-vertex kernel and ten compressed additions.
The observed execution takes 64.918 seconds with three workers; the focused kernel and
compression control independently passes in 0.07 seconds.
This accepts the first capture owner update conditional on the accepted root chain and
bridge.
Subsequent updates must still consume the accepted pose rows as well as the owned
hulls.
No complete source node, candidate capture, or global conclusion is accepted here.

## A2 Admission and Remaining Capture Grammar

Shared checker revision
`da09d08d0e2d6c40755a15a9e9b4a47ae874513463acc9fb44e29f5a821afa2b` binds ordinary A2
assignments through helper
`f8135ba45073ad4bda7f66f543454b7484f46cc3fbcee63340afee1dbeac7265`. It pins and rechecks
that helper and the baseline metadata object.
The geometric checker remains restricted to one-node, assumption-free sequential
wall-seed cases; partition and necessary-D4 recipes still refuse.
This admission grants no exclusion until a complete geometric execution accepts the
selected case, and supplies no A1 geometric premise.

A further read-only inspection of all ten capture source objects, each checked against
its
[retained source identity](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/source-graph/result.json),
found the existing transition grammar sufficient: exact predecessor rows, inherited
center and angle conditions, necessary self-hull cuts, strict cores, universal partner
collision regions, residual coverage, and exact ownership compression.
Root-self, r1, r10, r11, and r111 each end with an incomplete step that must not promote
state. Every complete query and partner cover must partition its owner’s entire allowed
closed angle interval.
At a branch threshold, a retained row must cover the endpoint with its own proved center
domain; ignoring a zero-width intersection is justified only when the retained closed
rows still cover that endpoint.
The induction invariant is that each row contains every feasible center at every angle
in its interval.

The three far source leaves all propose `all_parent_poses_forbidden` contradictions.
The final near source instead has `closed: false`, no contradiction, 121 complete
updates, and 136 live final rows.
Its older guard therefore cannot be a required acceptance gate.
Those guard boxes classify producer progress and do not justify any geometric pruning in
the reviewed node rules.
After proving the actual near state, compose directly with the accepted pose-inclusion
result for source `491afdaaf411e7fdb4968bdcda7232ea517ead34739d0ae8c7d5570333a981cc` and
the accepted local-isolation theorem.
Bind the actual final-state digest
`a6d45c0c383496fbffd0934e37d735badecc6d05f1e8346da8c063ee5f44fd80`; the previously
refused publisher leaf digests remain refused.
This source inspection accepts no additional capture transition, but identifies no
additional analytic premise for the remaining composition.

## Generic Partner-Collision Admission

Shared checker revision
`722e654fbf426d9db3a799458c075378814da632b29a23c4b514e24a38a19a7c` admits partner
collisions through the
[partner helper](../../../packing/devtools/n11_nonfield_partner.py), SHA-256
`2928f0371a6442ca405f0d13c01c52022da87a1ef0b8dfaf0ae77613b7987a0d`. Each used partner
cover partitions the complete closed angle interval and resolves its references against
the same accepted predecessor state used by the query rows.
Every live partner domain equals the reconstructed predecessor hull, and its core lies
strictly inside every square throughout that row’s interval.
This profile refuses partner self-hull cuts and empty live families used for collision.

The helper independently proves every proposed collision polygon using the reviewed
universal Minkowski-facet inequalities; publisher status and row counts provide no
geometric premise. Proving collision throughout the larger pre-wall query domain is
conservative. The row cover still targets the independently required legal domain, and
residual ownership and support calculations retain all proposed residual vertices.
Parallel rows receive the same admitted partner covers and accepted prior state.
The checker pins the helper, frozen collision checker, and its dependency closure before
and after execution, then retains the existing complete-state and terminal-contradiction
gates. Seventeen focused controls pass independently in 1.10 seconds, with two selected
slow tests excluded.
This approves the supported one-node implementation; it grants no case exclusion from
the source-shaped 1658 row diagnostic.

## Capture Root-Node Continuation Contract

The [root-node continuation](../../../packing/devtools/check_n11_capture_root_node.py),
reviewed at SHA-256 `7642b10e0ed2021dda95f0f9b5f73f6286f471877c46b3c807760db52f7c910b`,
admits the fixed first-step execution as an explicit premise.
It reconstructs the phase-two support rows once, replaces owner 15 with the accepted
first-step state, and thereafter resolves query and used partner references against the
immediately preceding accepted pose rows.
Each complete update checks its full closed angular cover, common kernel, exact
compression, and following prior hulls before promoting ownership or pose state.
An independently checked complete empty partner cover already contradicts the existence
of that partner, so the dedicated empty-partner rule is sound.

The final partial step must be step 13, cover a proper initial angle interval, and have
no kernel or compression to promote.
The source’s final groups, intervals, references, residuals, and outer domains must
match the state reconstructed from complete updates.
Source, premise, and helper identities and the deadline are checked before final
acceptance. This source review permits the bounded step-one pilot; neither the pilot nor
this review accepts the complete root node, branch tree, or candidate capture.

## Exact Integer Collision Predicates

The [integer collision helper](../../../packing/devtools/n11_integer_collision.py),
SHA-256 `4a1f71cdc96134af1083c84717912b73801b07933a8f7cd2eff8b998b31eab98`, represents
each point as $(X/Z,Y/Z)$ with $Z>0$. Its determinant and lexicographic comparisons
therefore have the exact affine orientation and ordering signs, including differently
scaled representations of the same point.
For successive counterclockwise hull vertices $a,b$, the computed facet coefficients are
the rational facet multiplied by the positive factor $Z_aZ_b$. The minimum center
projection and final region inequality likewise cross-multiply only positive
denominators. Thus the helper proves the same universal Minkowski containment with exact
closed boundary equality, without rational normalization in the inner loop.

Six focused controls independently pass in 0.10 seconds.
They cover random rational hulls with scaled duplicates, every-partner necessity, and
rational oblique facets with signed translated centers and boundary perturbations of
$10^{-60}$. The
[three-row comparison](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-step0/collision-integer-benchmark.json),
SHA-256 `b5b9c1d9eafc11c8e0130ac02f07f63e54c30cdc4eecec830bca2ec36aa5ac37`, records the
same facet-vertex counts and unprofiled kernel CPU speedups from 4.607 to 4.920. Those
measurements give no additional proof credit or whole-replay speed guarantee.
Consumers must still establish strict full-angle core ownership and complete accepted
partner pose covers, and pin this helper and the frozen reference dependency closure.

## Partner Exclusion and Integer Integration Checkpoint

The observed
[1687 execution](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/generic-case1687-partner/pilot-fast.json),
SHA-256 `8566a62979920c37778638a9abbd36b90a4eed503601462bb84d6766a928d8f5`, binds the
reviewed shared checker `722e654f` and partner helper `2928f037`. It accepts 70 strict
seed points, 352 seed rows, and six complete updates containing 192 rows, including
3,055,752 universal collision inequalities.
The terminal owner is 10, no work remains pending, and the only exclusion is 1687. The
observed run takes 296.132 seconds and retains a false global-optimality flag.
This accepts that singleton conditional on the observed source-bound execution.

The optional integer dispatch is approved at shared checker
`79473807be4564af6cb13f8c36ad6517b8f077383707513069bc8a5be933fb5c` with partner helper
`0bfbac5f09e366622ac324a776daa9a51829d3c3fb2aa24ec1a6627f31ea72ae`. The selected integer
helper is hashed, recorded, and checked before dispatch and after replay; serial and
parallel rows retain the same fixed backend and accepted state.
This source review grants no additional exclusion.

The subsequent
[full integer replay](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/generic-case1687-partner/pilot-integer.json),
SHA-256 `f0505c72b7bbe15c50e92ba51f7064f4d50c05837752cd93d69b4600c653f7c1`, binds those
reviewed revisions and the frozen integer helper.
Its seed, six complete updates, 192 rows, and 3,055,752 collision inequalities match the
accepted reference execution.
Every row’s coverage event, probe, and collision count, and every partner-cover count,
also match.
Both executions check the same source final state and exclude only 1687, with
no pending work and a false global flag.
This accepts the integer execution under the same observed-execution premise and adds no
new case ID. Its 151.322-second wall time was measured under different host load and is
not a controlled whole-case speedup.

Capture continuation revision
`2804989aff9414e712855d099aab659bb645f05cd9b2f72259b97a1d22cefcb8` similarly pins the
integer helper and forces every positive diagnostic row limit to stop before promotion.
The observed
[complete step-one calculation](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-root-node-step1-integer/result.json),
SHA-256 `ba2b7a053c6626e3be3af87ca2bd2492b2c276e1df86705a3f3588f4377d03e8`, reaches all
149 rows, 670 partner rows, 4,452,672 collision inequalities, 624 ownership planes,
eight compressed additions, and the following prior-hull equality in 125.824 seconds.
Its whole-node status remains incomplete.
The selected-step stop precedes the checker’s final source recheck, so this result is
observed calculation evidence and requires a separate final binding before reuse as an
accepted step premise.
Both ten-row prefix comparisons perform zero collision inequalities; they establish
diagnostic refusal behavior, not backend timing or nontrivial geometric parity.

## Completed Reviewed-Worktree Batches

Two retained batches ran with shared checker `722e654f` in the frozen worktree at
`33b97fcadfb92be997e655fb24b67e127eb3cb3d`. The
[A3 summary](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/nonfield-batch-a3-reviewed/summary.json),
SHA-256 `25be910a1ae2174890bbb279e091cd66d32e52e14c55fa88e422d346f42cf1d7`, completes
all 32 selected cases, with 489 updates and 15,336 rows.
The
[first A2 summary](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/nonfield-batch-a2-reviewed-1/summary.json),
SHA-256 `b085f9f2dacd6043533d5f9c6babfa3b10b5750ecaeb833d0cc88151d4abfc78`, completes 25
of 26 selected cases, with 268 accepted updates and 17,152 accepted rows.
Case 2174 refuses unsupported partner self-hull cuts and receives no credit.

The audit checked compressed and decoded receipt identities, exact source and assignment
bindings, helper pins, complete ordered step and row inventories, singleton exclusions,
and false global flags.
Every accepted receipt has no pending obligations.
The copied main-checkout summaries retain the audited bytes.
This admits the 57 distinct IDs in these two accepted lists conditional on the observed
reviewed executions; the maintained union must deduplicate them against earlier
evidence. Earlier aborted batches receive no credit.
Neither this receipt audit nor a cached success marker repeats the geometry.

The
[second A2 batch](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/nonfield-batch-a2-reviewed-2/summary.json),
SHA-256 `1a0cd58a21cf572a9428541623be42a93d21b8169a0145bec09569070f68aed1`, completes
all 26 selected cases under the same frozen worktree checker, with 369 updates and
23,616 rows. The
[A1 integer batch](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/nonfield-batch-a1-integer/summary.json),
SHA-256 `860a8fddce125063eb769a7c0b77a2038151b65c267bc53288a423f1365d785e`, completes
1652, 1658, 1776, 1816, 1841, and 1876 under reviewed checker `79473807`. Its 76 updates
contain 2,432 rows and 23,730,928 collision inequalities.
Both batches pass the same source, helper, decoded-receipt, and complete-inventory
checks; all 32 IDs were new to the maintained union at admission.
Their main-checkout copies retain the audited bytes.

## Baseline D4 Cut Implementation Checkpoint

The new [finite-cut consumer](../../../packing/devtools/check_n11_baseline_d4_cuts.py),
SHA-256 `338fb431d381502fa1a9721647f231f1a3e9db73a3c6337c3561e69d16bf5d32`, implements
the forced-owner-region lemma above using the frozen independent cover, overlay, and
strict-distance primitives.
It derives the exact 253-case complement of the pinned 1,931-case metadata and retains
all 506 raw masks. Five focused controls pass in 0.11 seconds, including comparison with
independent enumeration of small finite assignments, strict cut-boundary tests,
interrupted-search refusal, and rejection of count-only baseline admission.
Lint and type checks report no findings.
Independent code review is complete: the affine normalization, strict offending-vertex
test, exhaustive region search, all-view target-mask intersections, closed equality, and
exact baseline-ID premise were checked without a blocking finding.

The observed
[diagnostic execution](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/baseline-d4-cuts/diagnostic.json),
SHA-256 `e4e440c09b69463d42ee4421054dee6e6f5137f95f7a45f9223f8d737bc11d38`, reconstructs
all 220 closed regions and 1,572 strict bans.
For 2175, its 72 proposed planes require rejection of 38 regions, taking 131 search
nodes. For 2176, 73 planes require rejection of 36 regions, taking 115 nodes.
All 74 forced assignments exhaust without a witness in 1.152 seconds overall.
Regions whose vertices already satisfy every requested plane need no feasibility
witness; equality is retained.
The
[post-commit diagnostic](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/baseline-d4-cuts/frozen-diagnostic.json),
SHA-256 `abc56c2b2eb2ee7710ef11bbe087dc7447e1deed584ba2b83147e133e5342e08`, binds the
same frozen implementation committed at `891e4715b` and repeats all 74 obligations in
246 search nodes and 1.066 seconds, with the same limited scope.

No baseline execution inventory was supplied, so necessary-cut and proof-credit flags
remain false and no case is excluded.
The optional inventory admission requires every exact baseline ID and explicitly depends
on reviewed observed executions; a stored inventory is not a geometric replay.
The output lists the precise manifest-bound constraints and their proposed source-node
identities. A later geometric consumer must compare its actual source constraints with
that list before using any admitted cut.
Neither large source node was downloaded or replayed for this finite diagnostic.

## Linked Exclusion and Complete Capture Root State

Shared checker `51c5fcfa802fe9e0ad644efd4bbaa14f132cb4f519e3b3c76ea4ba378686c814` uses
[ancestry helper](../../../packing/devtools/n11_nonfield_ancestry.py)
`f1d113d9d5c382933f3939d7481ecec6e486cc04890f417f7025af8e54264264` to pass the actual
accepted groups and full pose rows between source nodes.
Each child binds its immediate parent hash, seed, owner inventory, group hulls, and
ordered pose references.
Each node’s final state must match its completed updates.
Open checkpoints grant no exclusion; only the last node’s independently checked
contradiction can close the case.
Twenty focused controls pass independently in 0.68 seconds.

The
[1723 execution](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/generic-case1723-chain/pilot-fast-integer.json),
SHA-256 `14b8676358dd4f9c4b71c6b0c329392ce3ee91895d092027f869d739c63b9eda`, binds those
revisions and both exact source nodes.
It accepts 75 strict seed points, 352 seed rows, 32 parent updates and two child
updates, totaling 1,088 rows and 17,848 collision inequalities in 124.721 seconds.
Its complete node/step/row inventory has no pending work, and its only exclusion is
1723\. The maintained inventory now contains every exact ID in the pinned 1,931-case
baseline; this is a union of reviewed observed executions, not an inference from the
total accepted count.

The
[continuous capture root execution](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-root-node-full-integer/result.json),
SHA-256 `0d55007a6c5092c0e276ec4e6a2f8524a32ddc4d527ffa3a930f088ff11bccc4`, binds
reviewed checker `2804989a` and the accepted first-step premise.
Complete updates 1--12 accept 2,185 rows, 28,396,560 collision inequalities, 7,784
ownership planes, and 92 compressed additions.
Partial update 13 checks another 103 rows and 621,568 collision inequalities without
promoting any row or point.
The 891.927-second run reaches exact final-state equality and final source, dependency,
and deadline checks.
It therefore accepts the root node state for subsequent branch induction, resolving the
selected-step receipt’s final-binding limitation.
Capture-tree, candidate-capture, and global flags remain false.

## Refined Partitions and Acquired Special Sources

Shared checker `33e9dad1cc590f97b49a13daa73813f65a80587070f993451a8b235bc21d4014` with
[refinement helper](../../../packing/devtools/n11_nonfield_refinement.py)
`937d36d64bf385d94d8dad9e6de5c1f8c487f07955cdbc826987dd63dea3464c` removes the fixed
seed-bin restriction from later updates.
Each new closed interval lies in its uniquely referenced accepted predecessor interval;
the new intervals form a gap-free full $[0,1]$ cover.
Workers receive those exact predecessors, and final row counts match the accepted rows
of each owner.
A trailing incomplete step in an open ancestor is explicitly skipped, with
no geometric or ownership promotion, and the source final state must still equal the
state from completed updates.
This implementation review grants no further case exclusion.
The acquired 2053 and six-node 1393 sources fit this interval rule; 1393 also needs two
unpromoted partial tails and steps containing up to 512 rows.

The acquired 2175 and 2176 sources exactly match the manifest’s 72 and 73 proposed
planes. Both use ordinary 64-bin wall seeds and one unguarded node, with 13 and 17
complete updates, no collision regions, and terminal empty-owner contradictions.
The [D4 admission helper](../../../packing/devtools/n11_nonfield_d4_admission.py),
SHA-256 `621106a4855da5ca4bbc75985890561e80656cc7fb85dbcea95cf792b965ce28`, is approved
as a source join: it refuses diagnostic or incomplete baseline reports and requires
every actual rational owner/plane triple to match the pinned recipe and newly checked
cut report. Its caller must freshly execute the frozen finite-cut consumer with the
explicitly bound baseline inventory and recheck all dependencies and inputs before case
acceptance. Admitted owner planes restrict query pre-wall and legal domains, and partner
domains when used. Seed ownership, residual coverage, support, compression, and terminal
checks remain required.

The
[acquired 1383 sources](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/nonfield-sources/batch-partition-special.json)
confirm five common ancestors followed by a two-node lower branch and a one-node upper
branch. Both children start from the accepted state of source `b72e9019`, using separate
copies. Their exact closed conditions are $y_{13}\le H$ and $-y_{13}\le-H$, where
$H=B(U/2+4/3)=374956889708307252359863/116312507700684425319300$. These conditions cover
every center, including equality, and must restrict both query and partner domains for
owner 13. The lower branch closes through owner 6’s empty pose cover; the upper branch
closes through owner 11’s. Both branches must accept before excluding 1383; this case
has no baseline-exclusion premise.

All eight actual parent links, initial group hulls and pose references, query and
partner interval ancestry, and complete-only final pose states match the proposed 1383
tree. Its 36,600 source query rows include 120 rows in three incomplete tails; there are
260 complete updates and 132,288 partner rows.
All 12,191 collision regions use the reviewed universal-collision rule, with no empty
partner family. Variable partitions, necessary partner self-cuts, inherited center
planes, and the two-child state join suffice for the observed grammar.
This source audit proves no 1383 transition or exclusion.

## Refined Replay and Special-Adapter Checkpoint

The
[second reviewed A3 batch](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/nonfield-batch-a3-reviewed-2/summary.json),
SHA-256 `675808fdc64b7e9a581b82331db959c2fdafacda6411996822d6a651dcac73b4`, completes
all 32 selected cases under frozen checker `79473807`, with 405 updates, 23,584 rows,
and 21,472 seed rows.
Every compressed and decoded receipt identity, source and assignment binding, helper
pin, ordered row inventory, singleton exclusion, and false global flag passes the
receipt audit. The main-checkout copies retain the worktree bytes.
All 32 IDs were new to the maintained 2,018-case union, taking it to 2,050, conditional
on the observed reviewed executions.
No earlier aborted batch is admitted.

Shared checker `f430580c526c679d0b6a2551799bcec61a3973374fa7d6469064f11c459352cc` and
partner helper `39f58aa5e83438009ca3a01c950f7d2668e37bedfda4cb8e55bd309c79bad850` extend
the reviewed refined-interval rule with independently necessary partner self-cuts.
For every refined closed interval, the frozen quadratic checker bounds all four corners
of the complete physical square against the current accepted owned hull.
The proposed partner domain must equal the accepted predecessor domain intersected with
these proved cuts, including empty, point, and segment results.
Strict partner core containment and same-prior collision checks remain required.
The helper and its dependency closure are bound whenever partner covers are used.
Thirty-two focused controls pass; this implementation review grants no exclusion by
itself.

The
[2053 replay](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/generic-case2053-refined/pilot-fast-integer.json),
SHA-256 `5296d5061231abc7dd6e13892990575b71e45e74ce35d529779dea1de59461f1`, binds those
revisions and refinement helper `937d36d6`. It accepts 69 strict seed points and 88 seed
rows, followed by 11 eight-row parent updates and three sixteen-row child updates.
Its 136 completed rows include 144 partner-cover rows and 54,736 collision inequalities.
Source and assignment identities, both node inventories, every ordered step and row, and
all helper pins match.
The 27.400-second observed execution has no pending or skipped work and excludes exactly
2053, with a false global flag.
This admits that singleton under the observed-execution premise.

The
[full-baseline finite-cut execution](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/baseline-d4-cuts/complete-baseline-cuts.json),
SHA-256 `b71f4c20b3ffef84e21953bad3c4ad77759647eecef8433b62c62f7a122499e7`, binds the
frozen finite-cut checker and the
[immutable baseline inventory](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/baseline-d4-cuts/baseline-execution-inventory.json),
SHA-256 `e581a614d4d3210375059e4fd98bfdae0ebb1ca8ba3078050454b0da208f3c6f`. That
inventory contains every exact baseline ID; its 14 execution-record bindings match the
retained bytes. The fresh 1.416-second calculation exhausts all 74 offending region
assignments in 246 search nodes over all 506 raw survivors.
It therefore admits the 72 and 73 necessary planes conditional on the reviewed baseline
executions. The actual pinned 2175 and 2176 sources also pass the reviewed `621106a4`
source join against this report.
No geometric replay or singleton exclusion follows from the finite-cut calculation
alone; its exclusion list is empty and its global flag false.

The
[special-assignment helper](../../../packing/devtools/n11_nonfield_special_assignment.py),
SHA-256 `a01986779d54a80804b4ed9572c5448aa90e287c1dadae9b6b3f5377233aa4f7`, binds case
and frame metadata, the D4 source and baseline identities, or the 1383 tree, seed,
cover, and every ordered source node.
It deliberately supplies no geometric meaning to publisher success flags.
All three actual audits pass this helper and the unchanged A2 assignment checker.
Seven focused controls pass.

The
[center-partition helper](../../../packing/devtools/n11_nonfield_center_partition.py),
SHA-256 `43d2b8ec9c18911bbc26858f31db8429b2453b21a3a5a07c81daf7c5aa489e9b`, constructs
an immutable plan after checking every actual parent chain, all source IDs, the
unconstrained common prefix, two separate leaf tails, and the exact complementary closed
center planes. The actual eight pinned headers produce the five-node common prefix and
the two-node lower and one-node upper tails described above.
Five focused controls pass.
This helper grants no exclusion: its consumer must independently replay the common
state, copy it for each branch, preserve every inherited condition, and close both
leaves.

## Conditional Capture Branch Review

The [first-row r1 adapter](../../../packing/devtools/check_n11_capture_branch_r1.py),
SHA-256 `f75b7ef718cc301833770128dd2f9b2bab3473b5dd01f59583e70fc2bb84abf9`, binds the
exact reviewed root receipt `0d55007a` before and after its work.
The earlier draft accepted a supplied root receipt without this identity check and was
not admitted. The corrected adapter checks the root-to-child source link, every initial
group and pose reference, and the exact closed condition $-y_{15}\le-B(U/2+5/4)$. It
checks the original current-row identity before adapting only that label for the frozen
root row checker; predecessor references, intervals, and geometry remain intact.

The observed
[r1 first-row execution](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-branch-r1-row0/result.json),
SHA-256 `5d6061c4647d28778380328f784981d6bcfd608662fe3b8c6411019f1aed79ac`, binds the
corrected adapter, root premise, and child source.
It checks nine coverage events, 17 probes, and eight common-core planes in 2.706
seconds. Its complete-step, branch, candidate, and global flags remain false; only this
selected row is admitted.

The [full-r1 adapter](../../../packing/devtools/check_n11_capture_branch_r1_node.py),
SHA-256 `3e1bfc6471acc48ccbbce00a5c546f4f7e1e4e0cdd1bb3ce51247bfc94b10ce1`, is approved
for a bounded replay.
It reapplies the inherited owner-15 center condition to every query and used-partner
view of accepted rows, including rows whose later outer support proposals extend beyond
that condition. Each original current-row identity is checked before the same narrow
label adaptation. All workers use the same accepted prior; every complete closed angular
cover joins before kernel, compression, or state promotion.
The final partial update cannot promote rows or additions.
Exact child constraints are checked before adapting that field for the frozen
final-state checker, and all source, premise, dependency, and deadline checks precede
node acceptance. This source review grants no child-node, tree, candidate, or global
proof credit.

The subsequent
[full r1 execution](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-branch-r1-full/result.json),
SHA-256 `677719a04426aa53a9ebe3bf8d597e78079313eec2e387bc6f4e4655fd5610f4`, binds that
reviewed implementation and the accepted root premise.
Its eight complete updates check 1,585 rows, 4,600 common-core planes, and 63 additions.
Partial update 8 checks 154 further rows and 616 planes without promotion.
The retained result, provenance, stdout, source pins, dependency closure, and ordered
step inventory agree.
Exact final state and final binding checks precede acceptance in 117.128 seconds.
This admits the conditional r1 node state; tree, candidate-capture, and global flags
remain false.

## Further Exclusions and D4 Integration

The
[third reviewed A2 batch](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/nonfield-batch-a2-reviewed-3/summary.json),
SHA-256 `b67859511a7a6d257491bb487f435f14cdf8349fdc25d169bd791fbd3729c8bd`, completes
all 15 selected cases, with 291 updates and 18,624 rows.
The
[third reviewed A3 batch](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/nonfield-batch-a3-reviewed-3/summary.json),
SHA-256 `3be940ab5d88828c595d5cc7dbefd01ac80e7af2d79837b17125e756fc89fd0b`, completes 31
cases, with 501 updates and 32,064 rows.
Both use frozen checker `79473807` and runner `461b6e6a`. Every copied compressed and
decoded receipt, ordered step and row inventory, source and assignment binding, helper
pin, and pending-work flag passes the audit.
The 141 distinct referenced source, seed, and audit objects also match their pinned
compressed identities.
All 46 accepted IDs were new to the 2,051-case union, taking it to 2,097 under the
observed-execution premise.
Case 1875 remains refused and receives no credit from this batch.

Shared checker `d226cb8d2ca971a98eb453971b820bf159bbf59308cf9b0b5908047c1206c1bc` with
partner helper `1722c6e3e93b53885342516f42a2e094991c34fa938f1befef3b947ff8daa0fa` is
approved for bounded D4, complete-ancestry `native_cached_v9`, and producer-flag
replays.
Its D4 path freshly executes frozen checker `338fb431`, admits the actual source
through `621106a4`, and reapplies those exact field-coordinate planes in every query and
partner domain.
Use the reviewed immutable baseline inventory `e581a614`; the cut premise
remains conditional on its observed baseline executions.
The report, inventory, source objects, dependencies, and final constraints are bound
through case acceptance.
Cached labels supply no geometric premise.

The publisher’s `terminal` boolean is unnecessary after independently proving an empty
accepted pose cover over the entire closed angular domain.
The revised final-node check accepts either boolean value while retaining
`closed: true`, the exact last owner and step, complete row coverage, the empty-residual
contradiction, and exact final-state equality.
Open-ancestor admission is unchanged.
A focused control accepts `terminal: false` only with the checked empty cover and
refuses a retained residual.
The old 1875 refusal remains unaccepted until a new frozen execution completes.

## Final Composition Interface

A final obligation consumer must distinguish the mathematical implication from the
premise that the reviewed component executions actually occurred.
Bind full receipt, checker, input, and output-state identities from an explicit accepted
registry; a matching success string or an arbitrary self-supplied receipt is
insufficient. Record `geometry_rerun: false` and the observed-execution premise.
Until every required obligation below is bound, report the exact missing or refused
obligations and grant no global conclusion.
A complete evidence inventory still does not itself replay the geometry; final theorem
acceptance uses the reviewed executions and the composition argument together.

1. **Cap and census.** Require the shared exact $U$, $B$, $L$, cover, and pinned source
   revision. Reconstruct the ordered 2,184 canonical masks and require the exclusion
   union to equal exactly $\{0,\ldots,2183\}\setminus\{438,999,1462,1659\}$. The
   accepted census receipt `98dad854` binds the A1--A5 assignments but contributes no
   geometry. The accepted 1,904-case field union plus all 276 non-field IDs suffice;
   completing redundant overlapping field certificates is unnecessary.
   Each admitted singleton must retain its reviewed execution and complete dependency
   closure.
2. **Conditional exclusions.** The 2175 and 2176 executions must bind freshly checked
   necessary cuts and the independently accepted exact 1,931-case baseline.
   Their later exclusions cannot justify that earlier premise.
   The 1383 execution must close both complementary center branches after the common
   accepted ancestry. Check this dependency graph for cycles; neither metadata-only
   admission nor a partial branch closes a case.
3. **Symmetry.** Bind the independent D4 receipt
   `c4aa4df460593abcb51cd4ebaaf916c78a6a718659bb6b7bf4245e3e67e6c00e`, its exact cover,
   overlay, strict-distance inputs, and three exhausted finite searches.
   Its premise is the complete 2,180-case exclusion union.
   Its conclusion supplies a case-438 image of any remaining packing, including the
   closed cover boundaries.
4. **Root induction.** Bind all 14 observed root rounds, rooted in the fixed first
   result `488f26c0`, through chain audit `f10d50e6`, bridge `ba65b741`, first capture
   step `8ca86cc3`, and complete root-state execution `0d55007a`. Preserve all eleven
   owners, the 154 owner updates, every source-state succession, and the 2,036-row
   initial bridge. The chain audit alone proves no execution occurred.
5. **Capture graph.** Require accepted geometry for every node in the table below, with
   exact parent initial-state equality, retained assumptions, complete closed query and
   partner angular coverage, and no promotion from partial tails.
   Split predicates are the complementary closed conditions at $y_{15}=5/4$,
   $t_{13}=147/512$, and $t_2=183/512$. A singleton threshold remains covered by a
   retained closed row with its own proved domain.
   Each of the three far leaves must independently contradict every pose in its branch.
   The near leaf instead supplies its accepted final state; its `closed: false` marker
   is consistent with that role.

| Node | Exact source SHA-256 | Accepted parent or required conclusion |
| --- | --- | --- |
| Root | `f9e67f28ea951fb5255c89e33b3ff0e1ee663c7011751761c9200441047b66d4` | Fourteen-round adaptive state; receipt `0d55007a` accepted |
| Far 15 | `e25a5de42cb45d9057660bb6d5942f980672e5d6e6b97e361c10931359c2f486` | Root; contradiction under the lower center branch |
| r1 | `63c6e29d75491d51aa9abc404e35eb99bc862456f07bf7aa3c20f7b1c9ea5e52` | Root; receipt `677719a0` accepted under the upper center branch |
| r10 | `58da537ee50dee6f21848f166a4d685961ebae6de4077835e40eef1fc1f89f48` | r1; lower owner-13 angular branch |
| Far 13 | `c86ed9d005dc5b2c347aa89964d7a9305bfe67f3ab3451a6e663a2185dac5fd5` | r10; contradiction |
| Near 13 | `a2f30c9246b770a2da91e45489f7b9343c345c105e00333f7ca67ab66b53db09` | r1; upper owner-13 angular branch |
| r11 | `280b5152e02e0dffd23bafb4dda2fd464ad847ec969c42b903ea266d2f7f974a` | Near 13; continuation |
| Far 2 / r110 | `79e7f3141c9d726b3c1ba9fe6dfdd2fe82692aab1b6cacf51b6860610baa1576` | r11; contradiction under the lower owner-2 angular branch |
| r111 | `db4c60f07a0143ac2edf976f595178903113102de902ac72ddcf863de04d0f7b` | r11; upper owner-2 angular branch |
| Near | `491afdaaf411e7fdb4968bdcda7232ea517ead34739d0ae8c7d5570333a981cc` | r111; accepted final state for pose inclusion |

The
[actual source graph](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/source-graph/result.json),
SHA-256 `cb7ffccf1e3841d44a2dff88549fdee1911805e516f175ef484c5b6e9004b248`, binds these
identities and edges but grants no transition geometry.
Its publisher-audit digest refusal remains valid.
Use the actual final-state digests below, not the inconsistent claimed leaf digests:

| Leaf | Actual canonical final-state SHA-256 |
| --- | --- |
| Far 15 | `9e28b0927cfa568ead95beb35cc3173e3c0466d3175dc47bb6d325939e6f1451` |
| Far 13 | `87482985d0271e404133f1255f1b49e0ba3cf434ce9ce09b6b187f417089948e` |
| Far 2 | `11d4a28e176ed885dbd650854426704ec280b08b275e556765d68c49f4108e6c` |
| Near | `a6d45c0c383496fbffd0934e37d735badecc6d05f1e8346da8c063ee5f44fd80` |

6. **Inclusion and local isolation.** Bind pose-inclusion receipt
   `c5b970458135847f5790f2311e4861faf720924ad7e62f5bafb6d1978743144c` to that exact near
   source and final state, its 136 live rows and 1,542 vertices, the retained extraction
   `d519f3a4`, guard-role input `0bc2edf5`, and exact frame and role bijection.
   Its local-result reference must equal
   `a98623f57017b4f04c8d3a72083caa7d4a6fb5096a79ab1e4dbbf2cd9b35a29d`, with the same 33
   focused radii from `9a9cf4e0`. The local execution covers all 128 branches and 8,448
   strict signed-coordinate inequalities.
   Retain its construction and exact arithmetic source bindings.
   The earlier residual-only profile is not a substitute.
7. **Endpoint and witness.** Use the already reviewed exact construction,
   $T=(6u+4)/(1+2u-u^2)$ for the specified root $u\in(9/25,37/100)$, its verified
   packing, $T<U$, and opposite-wall contacts.
   A putative side $S<T$ embeds concentrically in the cap; the D4 map and the accepted
   inverse frame place the resulting unit squares in a concentric side-$S$ subcontainer
   of the fixed side-$T$ container.
   Capture, inclusion, and local isolation force the construction, whose span $T$ is
   impossible there. The verified packing at $T$ supplies the upper bound.

These obligations suffice for $s(11)=T$ when every required execution and join is
accepted. Exclusions apply at the rational cap $U$; the candidate argument rules out
$S<T$ and does not exclude the valid witness at $T$. At this checkpoint, the remaining
non-field exclusions and eight capture-node executions are still open, so this
composition contract grants no global theorem acceptance.

## Refined and Conditional Exclusion Execution Checkpoint

The
[first refined batch](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/nonfield-batch-refined-1/summary.json),
SHA-256 `4cb4d19f42708ac81eb63d4d5b9b20f20ad9a3af367344d2c45a2ee81d371a40`, accepts
1889, 1950, 1955, 2049, 2050, 2052, 2055, 2056, 2057, and 2174 under frozen checker
`f430580c` and partner helper `39f58aa5`. Its 19 nodes contain 321 complete updates,
4,080 rows, 10,056 partner-cover rows, and 18,728,392 collision inequalities, with no
skipped or pending work.
Every copied compressed and decoded receipt, helper pin, node/step/row inventory,
assignment, and all 39 distinct source-object identities pass the audit.
The ten IDs were new, taking the reviewed union from 2,097 to 2,107.

Three further executions bind reviewed checker `d226cb8d`, frozen at `f00127429`:

| Case | Retained execution | Decoded receipt SHA-256 | Complete updates / rows |
| --- | --- | --- | ---: |
| 2175 | [Replay](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/generic-case2175-complete/replay.json.gz) | `1946b9a11d5a1906c0a25f73383f45ab4bb20689521c19f2ce8eeb89ea1618b5` | 13 / 832 |
| 2176 | [Replay](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/generic-case2176-complete/replay.json.gz) | `3f17e984518a9dc409154c8fd99a027110fa68b9f4045ab7e85119eb1fc77f2d` | 17 / 1,088 |
| 1875 | [Replay](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/generic-case1875-complete/replay.json.gz) | `cf3f99b76601b722e1394db56a940547a350b23df29b10d6dc4f7ebcb59758ab` | 16 / 1,024 |

Each accepts 704 seed rows and its exact singleton exclusion, with complete ordered
inventories, matching source and helper bindings, and false global flags.
The
[2175 cut report](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/generic-case2175-complete/replay-d4-cuts.json),
SHA-256 `842602d8e8abf3712787a870a06f3363518a21658a4bd091534dad81cc53c8c6`, and
[2176 cut report](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/generic-case2176-complete/replay-d4-cuts.json),
SHA-256 `c96c3d139aac3585d2a0e0291c50c2696b03d3ac55b2c177292de83e2175a627`, were freshly
executed within those replays.
They retain the reviewed immutable baseline `e581a614`, exact 1,931 IDs and 506 raw
survivors, all input and dependency identities, and exactly the previously reviewed
per-case constraints and exhausted region searches.
These geometric executions discharge both conditional D4 cases under the accepted
baseline-execution premise.
The 1875 replay independently closes its full empty-owner cover despite the publisher’s
false terminal marker.
Their earlier no-work refusals remain unaccepted.
The union reaches 2,110, leaving 70 non-field exclusions.

## Child-Node and Empty-Row Admission Checkpoint

The
[parameterized child checker](../../../packing/devtools/check_n11_capture_child_node.py),
SHA-256 `ebbc83b0a92913234cd701d53557bab52305d1755727976f283a22d1fc3dbf0f`, is approved
for bounded far-15, r10, and near-13 executions.
Its registry binds each accepted parent’s actual receipt, original checker, source, and
final-state identities.
Copied query and partner views reapply every exact center and angular condition.
Discarding a zero-width row intersection is sound here because the retained
positive-width closed rows still cover the complete allowed interval, including that
endpoint with their own accepted domains.
Singleton or empty angular branches outside this profile refuse.
A terminal node requires an independently empty complete owner cover.

Review found that the earlier draft would reject near-13’s last complete update after
doing its geometry. The corrected path checks that update’s kernel and compression, then
binds its promoted state through exact final-state equality; earlier updates still
require the next prior hull.
Four focused controls pass.
Original row identities and final conditions are checked before the narrow adaptations
for the frozen root primitives.
Final source, parent-premise, dependency, and deadline checks precede node acceptance.
This source review supplies no new capture execution credit.

Shared checker `9047dcbb9957877fe9b44d1bee356349be77cce0727c1195260d5fbb1d3803cf` is
also approved with unchanged partner helper `1722c6e3`. Once accepted predecessor,
independently necessary self-cuts, inherited conditions, and physical walls give an
exactly empty legal domain over the closed row interval, unused pre-wall hints and core
proposals need not be empty.
Every residual, collision, common-core, support, and outer-domain output must still be
empty; the row promotes no ownership point.
A focused control refuses a retained residual in this case.
Selecting the integer backend for a source with no collision regions no longer refuses
admission; the receipt explicitly records the absence of collision work and the row
counts retain zero collision inequalities.
This is no evidence of integer-kernel execution or speed.
Fresh bounded runs are still required before these relaxed admissions add any case ID.

## First Far-Leaf Contradiction and r10 State

The
[far-15 execution](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-child-far15/result.json),
SHA-256 `cda898189d5026234bb6dfd1239dec356a1ea7c1e22504034b02d0c6b692641e`, is accepted
under reviewed child checker `ebbc83b0`. Its exact parent is root receipt `0d55007a`,
its source is `e25a5de4`, and its retained condition is the closed owner-15 lower center
branch.
All eight steps complete, checking 1,585 rows, 6,891 cover events, 13,183 probes,
880 common-core planes, and 31 additions.
The final owner-8 update checks all 259 rows and finds every residual and outer domain
empty, with no addition.
The original final-state digest equals the actual graph digest `9e28b092`. Source,
dependency, parent, ordered execution, final-state, and stdout bindings pass.
This discharges the far-15 branch contradiction only; it neither excludes case 438 nor
completes the capture tree.

The
[r10 execution](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-child-r10/result.json),
SHA-256 `d75b95da3f286f794aa091a4abbddfea22eb264c29530200d19fa6bb8aab517f`, is accepted
under the same checker.
It binds accepted r1 receipt `677719a0`, source `58da537e`, the inherited closed
conditions, and original final-state digest `356e63cb`. Steps 0–11 check 1,908 rows,
13,945 cover events, 27,112 probes, 6,136 common-core planes, and 95 additions.
Step 12 checks 88 rows but adds no point and does not promote its partial state.
The observed 164.074-second execution reaches final-state and dependency checks.
Its conclusion is the conditional r10 state; terminal, capture-tree, candidate, and
global flags remain false.
Neither execution uses partner collision regions.

## Exclusion Execution Checkpoint at 2,143 Cases

The
[fourth reviewed A3 batch](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/nonfield-batch-a3-reviewed-4/summary.json),
SHA-256 `47126cf6c12903b8283b40b1f7647898e2d8195d194633efecc2ec51d77c2500`, accepts
1145, 1259, 1265, 1268, 1270, 1310, 1342, 1416, 1422, 1429, 1439, 1686, 1688, 1693,
1696, 1729, 1783, 1850, 2071, 2072, 2073, 2078, 2098, and 2116. Frozen checker
`79473807` checks 574 complete updates and 35,488 rows after 16,544 seed rows and 1,751
strict seed points. It records 1,708,092 cover events and 3,382,028 probes, with no
partner collision work.
All compressed and decoded receipts, assignments, ordered inventories, helper
identities, and 72 distinct archived input objects pass the audit.
Historical source bytes at `891e4715b` establish the frozen checker and runner
identities after the worktree was reused.
These 24 IDs were new, taking the union from 2,110 to 2,134.

The
[second refined batch](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/nonfield-batch-refined-2/summary.json),
SHA-256 `6009b91fda5095df0b1fb281f94781ce44432e8552c91907dfed4db9f4f9ec4d`, accepts
1335, 1411, 1430, 1484, 1695, 1728, 1810, 1885, and 2069 under frozen checker
`f430580c`, partner helper `39f58aa5`, and refinement helper `937d36d6`. Its 19 accepted
nodes contain 489 complete updates, 13,640 rows, 15,568 partner rows, and 24,518,448
collision inequalities.
The 116 skipped source rows occur only in unpromoted ancestor tails; every accepted
terminal node has its complete required owner cover.
The audit checks the copied receipts byte for byte, both compression identities, exact
source and dependency bindings at `cbc57135`, all 49 distinct input objects, and
complete node/step/row inventories.
The batch’s refusals for 1343, 1716, and 2125 add no ID; later retries require their own
accepted executions.
The nine accepted IDs are new and disjoint from the A3 batch, bringing the reviewed
union to 2,143 of 2,180 required exclusions, with 37 remaining.
These are retained, source-bound execution results under the reviewed geometric
checkers; the receipt audit itself does not rerun their geometry.

## Closed Center-Partition Consumer Review

The
[center orchestrator](../../../packing/devtools/n11_nonfield_center_orchestrator.py),
SHA-256 `cfa62c5c4d3947bf6c9483b5cde9d194305d833d944e6ef467c52876d25fdf9a`, correctly
joins the reviewed case-1383 branch plan.
It checks the five common nodes once, then gives each branch a separate deep copy of the
same accepted groups and pose rows.
Every child must match its exact parent, seed, frame, owner inventory, hulls, and
ordered references. The exact closed center condition is reapplied to every query and
partner domain through shared checker `9047dcbb`. Both terminal leaves must return from
complete independently empty owner covers before the join succeeds.
The helper alone supplies neither source admission nor case credit.

The [standalone consumer](../../../packing/devtools/check_n11_center_partition.py),
SHA-256 `da3c38b75bdf823dbe3ccf3f07d1905b931290d4ca1f9cde0ca5203356f7a5b6`, binds that
orchestrator, plan helper `43d2b8ec`, shared checker `9047dcbb`, and their fourteen
direct dependency identities plus the collision dependency closure.
It admits the exact metadata, cover, tree, seed, audit, and eight source nodes, checks
the strict seed geometry once, and requires both closed terminal branches, all eight
completed nodes, and an empty pending frontier before singleton acceptance.
Input, source, dependency, and deadline checks precede the final status.
Existing output paths and overlaps with inputs refuse.
The actual tree `7a9bf9e6` matches the pinned manifest proposal and retains false
publisher proof flags.
This approves a bounded execution; case 1383 remains unaccepted until its complete
observed replay passes.

The scoped [completion inventory](../../../packing/devtools/inventory_n11_completion.py)
revision `c1cea231` also passes review as incomplete evidence bookkeeping.
Its conditional-D4 join binds immutable baseline `e581a614`, the exact 1,931-case
census, every earlier execution file, and each fresh cut report through its already
reviewed singleton execution.
Cases 1383, 2175, and 2176 cannot enter that premise.
The far-15 parent, actual final-state, and terminal joins are explicit.
Its read-only execution retains false geometry-rerun and global flags; matching records
does not establish that their geometric executions occurred.

## Near-13 State and Four Further Exclusions

The
[near-13 execution](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-child-near13/result.json),
SHA-256 `c6e6f7bca7d19f759445fada136ee9632eb7ed69fa792ee486514bdcd781c1d2`, is accepted
under child checker `ebbc83b0`. It binds r1 receipt `677719a0`, source `a2f30c92`, the
inherited upper center and owner-13 angular conditions, and actual original final-state
digest `b0404ffa`. All 44 updates complete: 7,852 rows, 52,383 cover events, 101,811
probes, 23,592 common-core planes, and 344 additions, with no partner collision work.
The last complete update is bound through the exact final state, as required by the
reviewed source correction.
The 623.328-second execution and its stdout, parent receipt, source, dependency, and
ordered step bindings pass.
This supplies the conditional near-13 state for r11; it proves no terminal
contradiction, completed capture tree, or global theorem.

The isolated child-checker revision
`da027220b6eaea1962410fc786860e6c5c48d05cfe0860ac16ccdcec079c6921` is approved for
far13. It adds exact accepted r10 receipt `d75b95da`, source `58da537e`, final state
`356e63cb`, and the pinned far13 source `c86ed9d0` with 24 steps and terminal owner 10
at step 23. Its parent admission requires the exact
twelve-complete-steps-plus-partial-tail shape.
The geometry, closed-condition inheritance, complete terminal cover, and final
dependency checks are unchanged; this source approval grants no far13 execution credit.

The
[fresh retry batch](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/nonfield-batch-refined-retry/summary.json),
SHA-256 `b16a8c549a6784e4a5fc69a6dd98d808b8d76f8beb1488d43e22575e436d4204`, accepts
1343, 1716, and 2125 under reviewed checker `9047dcbb`. Its six nodes contain 160
complete updates and 3,776 rows.
The 81 skipped rows belong only to unpromoted ancestor tails.
Case 2125 checks 1,176 partner rows and 87,688 collision inequalities; 1343 and 1716
correctly record no collision work.
The
[final single-node batch](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/nonfield-batch-final-single/summary.json),
SHA-256 `7bdcde5281868fb58fadccb40c8b418bc1e22314136b8690cf9f94a1b9e762a1`, accepts 1694
after 37 complete updates and 2,368 rows, with no collision work.
Both audits check every compressed and decoded receipt, exact ordered inventory,
assignment, frozen checker/helper/runner identity, and all 15 distinct archived input
objects.
All four IDs were new, bringing the union to 2,147 of 2,180 required exclusions,
with 33 remaining. Earlier refused runs retain zero credit.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
