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

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
