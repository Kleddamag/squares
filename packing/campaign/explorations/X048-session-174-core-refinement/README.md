# Fixed-witness half-interval/octagon sensitivity

Combined exact core enhancement retains checked support for 18/96 parent rows in B; 78
remain unknown.
Of 79 retained E tuples, 7 have a compatible child assignment and 72 lose
known support in this bounded enumeration.
This is sensitivity evidence, not exhaustive unsupportedness of any parent row.
No replacement raw-atom search ran.

Each rational chart interval is split at its rational midpoint.
Child core is `hull(original core union octagon_core(child interval))`; exact
`strict_core` accepts each whole child interval and old-core containment is checked.
All 192 child cores have positive exact area growth; twice-area gain ranges
approximately 0.090376..0.160106. Center domains/piece identities stay frozen.
This combines halving and octagon augmentation; it does not isolate their effects or
measure adaptive producer/domain refinement.
Existing geometry is read-only.

| Evidence | Measured result | Limit/interpretation |
| --- | --- | --- |
| B target | 1460 unique refined pairs, 4619 assignments, 5.116 s protocol/9.047 s Job | 4740 pairs/5056 assignments/30 s/512 MiB; no guard |
| Independent B replay | 7 tuples, 105 fresh checks, 18 parent rows/18 observed child rows, 0.417 s protocol/3.687 s Job | Certifies retained support/coverage; not enumeration loss or search statistics |
| Endpoint control | 24/24 parent rows, 15 tuples, 90 unique pairs; 225 fresh replay checks | Exact angle-containing children preserve the endpoint witness |
| Focused controls | 29 tests 2.94 s; Ruff/types clean | Split/containment, identity/tampering, finite exhaustive graphs, guards/cache and endpoint enclosures |

B worker peak 153608192 B, independent replay 154959872 B. Every retained Job ends empty
with confirmed cleanup/no errors.
Child coverage is an observed lower bound: enumeration stops at the first compatible
assignment per original tuple.
Unknown child rows are never called unsupported.
Loss among fixed tuples cannot exclude alternative raw pieces, even when all 64 choices
of that tuple were tried.

The source is [the new diagnostic](../../../devtools/probe_n17_core_refinement.py) and
[its controls](../../../tests/test_n17_core_refinement.py).
[Small receipts](receipts/result-summary.json) and exact retained packets record
generated geometry provenance.
`content_sha256` hashes canonical JSON, not pretty/minified file bytes; published
minified packets are semantically identical to preserved local originals.
Baseline B uses G’s fresh same-E-packet 1185-pair replay, with packet and input identity
strictly bound. Endpoint baseline and cold-check receipts remain historical; no cold
checker reran.

From this PR’s `packing/`, choose explicit existing interpreter/input paths:
```powershell
$ProjectPython = (Resolve-Path .venv/Scripts/python.exe).Path
$SavedObjects = (Resolve-Path 'YOUR_B_OBJECT_DIRECTORY').Path
$ColdReceipt = (Resolve-Path 'YOUR_B_COLD_RECEIPT.json').Path
$Source = 'campaign/explorations/X048-session-172-capacity-support/receipts/B-support-packet.json'
$Baseline = 'campaign/explorations/X048-session-174-core-refinement/receipts/B-baseline-replay.json'
$Packet = 'campaign/explorations/X048-session-174-core-refinement/receipts/B-enhanced-packet.json'
& $ProjectPython -m devtools.probe_n17_core_refinement $SavedObjects `
  --checked-receipt $ColdReceipt --source-packet $Source --baseline-replay $Baseline `
  --verify $Packet --output 'YOUR_NEW_REPLAY.json'
```

On Linux, from `packing/` with the project’s Python 3.14 environment.
Every run requires the cold saved-check receipt (`--checked-receipt`) for the same saved
seed and node:

```sh
SAVED_OBJECTS="YOUR_B_OBJECT_DIRECTORY"
COLD_RECEIPT="YOUR_B_COLD_RECEIPT.json"
SOURCE="campaign/explorations/X048-session-172-capacity-support/receipts/B-support-packet.json"
BASELINE="campaign/explorations/X048-session-174-core-refinement/receipts/B-baseline-replay.json"
PACKET="campaign/explorations/X048-session-174-core-refinement/receipts/B-enhanced-packet.json"
uv run --frozen --all-extras --group dev python -m devtools.probe_n17_core_refinement "$SAVED_OBJECTS" \
  --checked-receipt "$COLD_RECEIPT" --source-packet "$SOURCE" --baseline-replay "$BASELINE" \
  --verify "$PACKET" --output "YOUR_NEW_REPLAY.json"
```
Expected `PASS_REPLAYED_PARTIAL_SUPPORT`: 18 parent rows/7 tuples/105 fresh pairs.
Replay reconstructs original source atoms, exact child cores and every retained edge
without enumeration/cache.
Omitting `--verify` reproduces only the frozen bounded fixed-tuple diagnostic; no
automatic research continuation is prescribed.

Baseline certified PR 333 revision 2bada1a; parent PR 307 at 1525d4e03 unchanged.
Open K2/P2 adaptive producer/539-orbit work stays untouched.
A compatible selection is a full solution of this exact binary abstraction; edges mean
only that universal collision was not established.
No common realizable pose, feasible packing, new exclusion or global proof follows.18
supported parents cannot be deleted completely by sound solution-preserving reasoning on
this exact enhanced graph; the other 78 are unknown.
The earlier 96 row result applies to its earlier cores, not arbitrary stronger geometry.

Root accepted source soundness and fresh independent retained-support replay.
Hosted source/evidence certification passes at
`40fe5f5bf62e6b37488e4d899e555de3bb9a0a5c`; final metadata CI is observed separately.
Native usage is one declared privacy aggregate/lower bound; later publication/CI and
pre-start setup are excluded.
No further H target follows.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
