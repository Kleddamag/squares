# A bounded residual-compatibility diagnostic

Owner: `Guzhou0806-Codex-T0`, bead `think-67ek`, Draft PR #333 above PR #325. The
dependency supplies the process-memory instrument and retained W7 regression fixture.
No producer, standing verifier, certificate grammar or admission rule changes.

**Result:** the frozen two-cover graph cannot remove any of its 192 atoms, even with
complete finite constraint reasoning.
Every atom has a retained compatible six-owner selection, checked directly against the
retained graph. This is a limitation of this finite abstraction, not a feasible square
packing or a new geometric exclusion.

## Question and boundaries

Session 169 retained three W3 candidates: adaptive south-wall refinement (owned by
upstream K2/S2), obsolete producer-memo lifetime (measured and independently delivered),
and residual-piece compatibility.
This continuation takes the third.
The live parent at selection was PR #307 `1525d4e03`; its hull-kernel source was
unchanged from `601bbf110`. Flag2 diagnosis, capture and streamed-verifier review remain
upstream work. One temporary Sol 6.1 xhigh reviewer checked the strategy and
implementation; all implementation and computation were performed by the primary
executor.

The input is pattern B, six owners, 16 angle bins, two producer rounds, envelope cores,
collision enabled, hull limit 16, no adaptive split.
The actual production command used a 180-second total ceiling and one-half producer
share.
Its saved node passed a separate cold saved check with a 120-second ceiling and no
producer import. The graph ceiling is six owners, 32 atoms per owner, 15,360 pair tests,
300 seconds and 512 MiB actual worker peak.
Inputs are limited to 64 MiB decompressed.
Exceeding a guard refuses the protocol; it never drops pieces to make a sample fit.

An atom means one owner’s pose in one angle row and a covering centre polygon.
Its strict core is read from the referenced accepted step and rechecked.
An edge is removed only when exact universal collision proves that the two strict cores
collide for all centres in the domains.
A retained edge is unknown compatibility, not geometric evidence.
Arc consistency deletes unsupported atoms.
Path consistency deletes an edge lacking a common choice for another owner, alternating
with arc consistency until stable.

Acceptance was an extra complete angle-row deletion or abstract contradiction compared
with one convex hull per row, while preserving the explicit known endpoint selection.
Edge deletion alone does not meet that acceptance criterion.

## Three bounded decisions

| Slice | Observation | Outcome and disposition |
| --- | --- | --- |
| B1: one atom per original piece | Owners have 491, 362, 140, 742, 672 and 115 pieces; 2,476,693 raw pairs. Zero pairs tested. | `guard-refused`: retire the unbounded raw expansion; no scientific negative follows. |
| B2: two covering groups per row | The row hull graph has 96 atoms and 3,828 of 3,840 edges. Two-cover has 192 atoms and 14,176 of 15,360 edges; path consistency removes another 163 edges. All 192 atoms and 96 rows survive. | `bounded-negative`: retire this abstraction as a row-deletion improvement on this input. |
| B3: finite support ceiling | All 192 atoms extend to a complete compatible six-owner selection. 1,152 search nodes; every witness directly checked. | `achieved`: retain the finite-model limitation and its witnesses; stronger graph search alone cannot improve this same model. |

B2 was frozen only after the B1 guard result.
For each row, all pieces are sorted by exact mean vertex x coordinate, with original
index as the tie breaker, then split into balanced halves.
Each group’s convex hull contains every vertex of every member piece.
Points and segments are retained.
The two groups may overlap, which only loses precision.
The x-axis rule was frozen before the target; it was not selected from target outcomes.
The receipts retain every group’s original piece indices.

B3 was selected after B2. A deterministic search picks the remaining owner with the
fewest compatible values, under a shared 10,000-node and 60-second ceiling.
It requests one full selection containing each atom.
A ceiling is distinct from exhaustive failure.
The retained packet contains owner domains, the 14,013 surviving edges and all 192
six-atom witnesses. Direct verification checks domain membership, every pair edge,
forced-atom inclusion and complete coverage of the live atoms.
Thus these witnesses are sufficient for the stated finite-model limitation, irrespective
of search order.

| Measured graph process interval | Wall seconds | Worker peak bytes |
| --- | ---: | ---: |
| B1 guard | 0.123 | 152,145,920 |
| B2 row hull | 0.941 | 151,388,160 |
| B2 two-cover | 3.953 | 152,768,512 |
| B3 two-cover plus support search | 3.520 | 151,678,976 |

These are single runs on the same host, not a speed comparison.
Wall starts after imports; peak is the actual Python worker’s high-water working set
including imports. The external Windows Job supervisor separately records full
process-tree wall and CPU. Its root-RSS reading refers to the venv launcher, so it is
not reported as worker memory.
The Job’s committed-memory counter is another metric, not interchangeable with RSS.

## Controls and review

- A three-owner binary odd cycle survives arc consistency and is rejected by path
  consistency. Exhaustive enumeration on twelve small graphs verifies preservation of
  every complete compatible assignment and checks the finite-support search results.
- Exact collision tests distinguish overlap from legal contact.
  Empty domains, degenerate cores and timeouts cannot be silently treated as proved
  impossibility. Search-cap exhaustion cannot be reported as an unsupported atom.
- The retained W7 fixture checks complete group membership and vertex coverage,
  including added point and segment pieces.
- A cold-checked endpoint6, four-bin, one-round state retains its exact six-owner pose
  selection through the two-cover collision graph and propagation.
  All selected atoms and pair edges survive.
  The small-graph mutation control removes a selected atom; the witness check detects
  it. A truncated support witness is also rejected.
- Seventeen focused tests, Ruff and BasedPyright pass.
  The independent reviewer found no soundness defect in the core abstraction; the
  support-search controls additionally compare with exhaustive enumeration.
  None of these controls admits an n17 exclusion.

## Reproduction and limits

Source for B3: `ee7e0161b`. Earlier B1/B2 ran the same atom construction and propagation
before the optional support search was added.
The source and receipts are retained; large producer objects remain outside Git.
The canonical node id is in each receipt.
From `packing/`, using the pinned Python environment, produce B with:

```text
python -m devtools.check_n17_subpattern --pattern B --bins 16 --max-rounds 2 --max-seconds 180 --producer-share 0.5 --save-objects OUT/B --output OUT/B-produce.json
python -m devtools.check_n17_subpattern --check-saved OUT/B --max-seconds 120 --output OUT/B-cold.json
python -m devtools.probe_n17_residual_graph OUT/B --checked-receipt OUT/B-cold.json --mode pieces --output OUT/B-raw.json
python -m devtools.probe_n17_residual_graph OUT/B --checked-receipt OUT/B-cold.json --mode row-hull --output OUT/B-row.json
python -m devtools.probe_n17_residual_graph OUT/B --checked-receipt OUT/B-cold.json --mode two-cover --support-search --output OUT/B-support.json
```

For the positive control, use `--pattern endpoint6 --bins 4 --max-rounds 1`, then the
same cold check and `--mode two-cover --endpoint`. Receipts are in `receipts/`. Keep
producer and checker serial.
The local full validation runner explicitly refuses Windows; hosted required jobs
provide the full fast gate, with actual status recorded in the PR and session.
The diagnostic is not exposed to the standing verifier.

No Flag2 run, broad residue sweep, new proof grammar, frontier admission, parent-branch
edit or merge was performed.
The raw-piece model remains untested.
A finer cover or stronger geometric predicate may behave differently; the finite-support
result does not rule those out.
The next independently scoped work is local worker-memory supervision, before any larger
experiment, not automatic expansion of this target.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
