# Enhanced-model replacement supports

The full raw-piece support search added 23 parent supports, each freshly replayed (same
implementation, no search): the enhanced model has 41 of 96 parent rows supported, with
55 unknown. All seven H selections covering 18 rows are retained.
The one search reached its 100,000-pair ceiling; its budget was not increased and the
search was not repeated.
These are positive supports in a finite binary network, not common realizable poses or a
global proof.

All 2522 original pieces receive two half-interval enhanced cores, giving 5044 atoms.
The original center domain and parent(owner, row) remain fixed; 192 half rows are
distinct from 96 parents.
Cores use the unchanged H construction:
`hull(old core union octagon_core(half interval))`, accepted by exact whole-child
`strict_core` with old-core containment.
Each reference includes original piece, source interval/domain/core identity, raw atom
index, half and enhanced core identity.
No piece is dropped, no child domain is recomputed and no adaptive producer runs.

| Evidence | Measured result | Boundary |
| --- | --- | --- |
| ONE B search | 26 cliques, 41 parents (+23), 100000 unique pairs, 134 DFS nodes | INCOMPLETE pair guard; 55 unknown, no unsupported candidate |
| Cost | 157.625 s protocol/160.797 s Job; 170758144 B OS worker peak | 180 s/512 MiB protocol; 240 s outer Job; no guard relaxation |
| Fresh B replay (same implementation, no search) | 26 cliques, 390 fresh pairs; 41 parents/1.417 s | Rebuilds all 5044 children afresh using unchanged H builder; exact H7 prefix/input/model identity |
| Endpoint | 148 raw/296 children, 24 parents, 15 seeds; 225 fresh replay pairs | Explicit full endpoint angle enclosure lies in selected child interval |
| Controls | 36 tests 3.36 s; Ruff/types clean | Finite exhaustive assignments, half identity, strict growth, provenance, seeds, caps, failures and direct replay |

All 7 B seeds are freshly validated and charged 65 unique queries before any coverage is
recorded. Deterministic forward-MRV uses unchanged LazySupports.
Pre/post query time/memory checks prevent failed queries entering its cache.
An all-owner clique is a full solution of this exact binary network, whose edges mean
collision was not proved.
Such a clique prevents whole-parent deletion under AC/PC in this model.
Search failure, budget exhaustion and 55 unknown parents imply no unsupportedness.
All Jobs end empty with confirmed cleanup/no errors.
OS peaks may miss short-lived children; protocol and outer Job limits are separate.
Original B–J/G/I remain frozen.

[New diagnostic](../../../devtools/probe_n17_enhanced_row_support.py),
[focused controls](../../../tests/test_n17_enhanced_row_support.py) and
[compact receipts](receipts/result-summary.json) retain this bounded outcome.
Published packet JSON is semantically equal to local pretty originals.
`content_sha256` denotes canonical JSON content, not serialized file bytes.
Input/cold-check identities bind historical saved objects; no cold checker reran.
Baseline repository revision is 14d131c8aaf2ac94239755f8438ab7d5e0192ef4; the new source
is introduced by this PR’s subsequent publication revision.

From `packing/`, use an explicit existing project interpreter and saved B objects
(transported by the preserved I bundle if needed):
```powershell
$ProjectPython = (Resolve-Path '.venv/Scripts/python.exe').Path
$SavedObjects = (Resolve-Path 'YOUR_B_OBJECT_DIRECTORY').Path
$ColdReceipt = (Resolve-Path 'YOUR_B_COLD_RECEIPT.json').Path
$Source = 'campaign/explorations/X048-session-172-capacity-support/receipts/B-support-packet.json'
$Baseline = 'campaign/explorations/X048-session-174-core-refinement/receipts/B-baseline-replay.json'
$Refinement = 'campaign/explorations/X048-session-174-core-refinement/receipts/B-enhanced-packet.json'
$Packet = 'campaign/explorations/X048-session-175-enhanced-support/receipts/B-support-packet.json'
& $ProjectPython -m devtools.probe_n17_enhanced_row_support $SavedObjects `
  --checked-receipt $ColdReceipt --source-packet $Source --baseline-replay $Baseline `
  --refinement-packet $Refinement --verify $Packet --output 'YOUR_NEW_REPLAY.json'
```

On Linux, from `packing/` with the project’s Python 3.14 environment.
Every run requires the cold saved-check receipt (`--checked-receipt`) for the same saved
seed and node:

```sh
SAVED_OBJECTS="YOUR_B_OBJECT_DIRECTORY"
COLD_RECEIPT="YOUR_B_COLD_RECEIPT.json"
SOURCE="campaign/explorations/X048-session-172-capacity-support/receipts/B-support-packet.json"
BASELINE="campaign/explorations/X048-session-174-core-refinement/receipts/B-baseline-replay.json"
REFINEMENT="campaign/explorations/X048-session-174-core-refinement/receipts/B-enhanced-packet.json"
PACKET="campaign/explorations/X048-session-175-enhanced-support/receipts/B-support-packet.json"
uv run --frozen --all-extras --group dev python -m devtools.probe_n17_enhanced_row_support "$SAVED_OBJECTS" \
  --checked-receipt "$COLD_RECEIPT" --source-packet "$SOURCE" --baseline-replay "$BASELINE" \
  --refinement-packet "$REFINEMENT" --verify "$PACKET" --output "YOUR_NEW_REPLAY.json"
```
Expected `PASS_REPLAYED_PARTIAL_SUPPORT`, 41 parents/26 cliques/390 fresh pairs.
Replay performs no DFS or cached pair lookup and recomputes coverage from exact refs.
It certifies retained positive support; it does not certify search
exhaustion/statistics.

Initial source CI found a stale test-file cost inventory: shard 4 exceeded the existing
10% unrecorded-file limit (14/135); 2094 tests passed and the inventory guard failed.
The official recorder refused that failed cohort.
Costs were regenerated from the complete successful 14d131 hosted cohort/run 37186951080
attempt 1, preserving all ceilings and policy.
Recorded files increased 522 to 557; the new A file remains honestly unrecorded.
Seven focused partition/record/real-tree controls pass.
Two Windows subprocess collection controls hit host ancestor-permission limits; their
full supported-host gate remains required.
No costs were invented, no failed status was edited and no tests or thresholds were
weakened. See[repair receipt](receipts/CI-cost-repair.json).

This attempt ends at its preregistered cap.
No automatic capacity or ordering ladder follows.
Any next project needs a new W3/ownership/resource contract.
Repaired source/evidence `217b571669986590937a7b8d85af0b018103dd60` has terminal 19
pass/36 skip and all 3 required SUCCESS. Final metadata CI is observed separately; no
new A target follows.
Native usage is one privacy aggregate/lower bound; later finalization and CI after its
cutoff are excluded, with declared branch association.

Commits cited in this record that are not in this branch’s history, including the
probes’ `BASE_REVISION` values, resolve at the tag `archive/guzhou-review-a-333`
(Guzhou’s original nine-session branch).
The references are provenance only; no code reads them (`OR-18`). “Fresh replay” here
means the same implementation re-run in a separate process without search; receipt names
ending in `-independent-replay.json` predate that wording.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
