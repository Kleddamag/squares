# Owner-priority enhanced parent supports

This attempt added 19 independently replayed parent supports: the enhanced model has 60
of 96 parent rows supported, with 36 unknown.
All 26 A selections covering 41 rows are retained.
The one search stopped at the unique exact pair ceiling.
It establishes no parent-row unsupportedness, common realizable poses or global proof.

The exact H combined half-interval/octagon enhancement, strict core validation, original
center domains and all 2522 raw pieces remain unchanged: 5044 child atoms, 96 parent
rows and 192 half rows.
Stable references include raw piece index and half, with exact original/derived
domain/core/interval identities.
A/H modules are unchanged.
Only the owned LazySupports API gains an optional full row permutation; its default
numeric ordering is unchanged.
Partial, duplicate or invalid permutations refuse.

The schedule derives unique supported-parent counts from the exact A26 references:
owners 17, 18, 19, 22, 10, 8, then numeric rows.
All 96 rows are in the frozen permutation.
All 26 seed cliques are freshly checked from an empty charged cache before coverage; the
seed cost is 182 unique pairs.
No failed query is cached.

| Evidence | Measured result | Scope |
| --- | --- | --- |
| ONE search | 60 parents (+19), 44 cliques, 100000 pairs, 127 DFS nodes | INCOMPLETE; 36 unknown |
| Cost | 142.535 s protocol; 172961792 B worker peak | 100k pairs/100k nodes/180 s/512 MiB; outer Job 240 s |
| Independent replay | 44 cliques, 660 fresh pairs; 1.726 s | Full 5044 inventory, A26 prefix, baseline 41 and new coverage reconstructed |
| Endpoint | 24 parents/15 cliques; 225 fresh replay pairs | Full actual angle enclosure lies in selected child interval |
| Controls | 66 focused tests 2.95 s; Ruff/types pass | Finite exhaustive graphs, default regression, permutations, seeds, provenance and guards |

An all-owner clique is a full solution of this frozen binary constraint network.
Its pair edges mean collision was not proved; they do not prove a common realizable
pose.
Such positive cliques prevent complete parent-row deletion under AC/PC in this same
model. Search exhaustion and budget failure are unverified/unknown.
The search starts from stronger seeds than A (26/41 versus 7/18), so added coverage
cannot be attributed solely to scheduling or called a matched speedup.
No extra numeric baseline was run.
This is one coverage experiment, not default adoption.

[New diagnostic](../../../devtools/probe_n17_scheduled_row_support.py),
[controls](../../../tests/test_n17_scheduled_row_support.py) and
[compact receipts](receipts/result-summary.json) retain the outcome.
Published packets are semantically equal to local pretty originals.
Canonical JSON content hashes identify generated inputs/packets/receipts, not file
serialization bytes.
Public independent receipt is explicitly a derived summary; the original local receipt
is retained. Source identity uses Git revision/path.
Historical cold saved-object checks are reused; no cold checker or producer reruns.
All 5 Jobs end empty with confirmed cleanup/no errors.
OS peaks may miss short-lived children.
Native usage is one privacy aggregate/lower bound; later publication/CI after its cutoff
is excluded, with operator-declared branch association.

From packing/, use an explicit existing project interpreter and saved B objects (the
preserved I archive transports the objects/cold receipt):
```powershell
$ProjectPython = (Resolve-Path '.venv/Scripts/python.exe').Path
$SavedObjects = (Resolve-Path 'YOUR_B_OBJECT_DIRECTORY').Path
$ColdReceipt = (Resolve-Path 'YOUR_B_COLD_RECEIPT.json').Path
$Source = 'campaign/explorations/X048-session-172-capacity-support/receipts/B-support-packet.json'
$Baseline = 'campaign/explorations/X048-session-174-core-refinement/receipts/B-baseline-replay.json'
$Refinement = 'campaign/explorations/X048-session-174-core-refinement/receipts/B-enhanced-packet.json'
$Accepted = 'campaign/explorations/X048-session-175-enhanced-support/receipts/B-support-packet.json'
$AcceptedReplay = 'campaign/explorations/X048-session-175-enhanced-support/receipts/B-independent-replay.json'
$Packet = 'campaign/explorations/X048-session-176-owner-priority/receipts/B-support-packet.json'
& $ProjectPython -m devtools.probe_n17_scheduled_row_support $SavedObjects `
  --checked-receipt $ColdReceipt --source-packet $Source --baseline-replay $Baseline `
  --refinement-packet $Refinement --accepted-packet $Accepted `
  --accepted-replay $AcceptedReplay --verify $Packet --output 'YOUR_NEW_REPLAY.json'
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
ACCEPTED="campaign/explorations/X048-session-175-enhanced-support/receipts/B-support-packet.json"
ACCEPTED_REPLAY="campaign/explorations/X048-session-175-enhanced-support/receipts/B-independent-replay.json"
PACKET="campaign/explorations/X048-session-176-owner-priority/receipts/B-support-packet.json"
uv run --frozen --all-extras --group dev python -m devtools.probe_n17_scheduled_row_support "$SAVED_OBJECTS" \
  --checked-receipt "$COLD_RECEIPT" --source-packet "$SOURCE" --baseline-replay "$BASELINE" \
  --refinement-packet "$REFINEMENT" --accepted-packet "$ACCEPTED" \
  --accepted-replay "$ACCEPTED_REPLAY" --verify "$PACKET" --output "YOUR_NEW_REPLAY.json"
```
Expected retained support: 60 parents/44 cliques/660 fresh pairs.
Replay uses no DFS or pair cache and recomputes parent coverage from exact refs.
It certifies positive selections, not search exhaustion or search statistics.
One attempt ended; no automatic ordering/cap ladder follows.
A further substantive project requires a new W3/ownership/resource contract.
Source/evidence `a647f83f8b37fa65cbc6791064b3704257845802` is observed terminal 19
pass/36 skip and all 3 required SUCCESS. Final metadata CI is observed separately.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
