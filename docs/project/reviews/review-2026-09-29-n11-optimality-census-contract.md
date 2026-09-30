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

The near-state source alone is 27,653,954 compressed bytes and 185,901,535 decoded
bytes. Its index key is
`73ddd73ce616ecb4a74d08c18a17f7eaff044df2111b0e500636b073e43ee970`; its decoded SHA-256
is `491afdaaf411e7fdb4968bdcda7232ea517ead34739d0ae8c7d5570333a981cc`. Select the
remaining source ancestry from B1–B7 before estimating or scheduling that replay.

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

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
