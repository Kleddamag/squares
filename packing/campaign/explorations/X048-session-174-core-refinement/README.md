# Fixed-witness half-interval/octagon sensitivity

Combined exact core enhancement retains checked support for18/96parentrows in B;
78remain unknown. Of79retained E tuples,7have a compatible child assignment and72
lose known support in this bounded enumeration. This is sensitivity evidence, not
exhaustive unsupportedness of any parent row. No replacement raw-atom search ran.

Each rational chart interval is split at its rational midpoint. Child core is
`hull(original core union octagon_core(child interval))`; exact `strict_core`
accepts each whole child interval and old-core containment is checked. All192child
cores have positive exact area growth; twice-area gain ranges approximately
0.090376..0.160106. Center domains/piece identities stay frozen.
This combines halving and octagon augmentation; it does not isolate their effects
or measure adaptive producer/domain refinement. Existing geometry is read-only.

| Evidence | Measured result | Limit/interpretation |
| --- | --- | --- |
| B target |1460unique refined pairs,4619assignments,5.116s protocol/9.047s Job |4740pairs/5056assignments/30s/512MiB; no guard |
| Independent B replay |7tuples,105fresh checks,18parentrows/18observed childrows,0.417s protocol/3.687s Job | Certifies retained support/coverage; not enumeration loss or search statistics |
| Endpoint control |24/24parentrows,15tuples,90unique pairs;225fresh replay checks | Exact angle-containing children preserve the endpoint witness |
| Focused controls |29tests2.94s; Ruff/types clean | Split/containment, identity/tampering, finite exhaustive graphs, guards/cache and endpoint enclosures |

B worker peak153608192B, independent replay154959872B. Every retained Job ends
empty with confirmed cleanup/no errors. Child coverage is an observed lower bound:
enumeration stops at the first compatible assignment per original tuple. Unknown
child rows are never called unsupported. Loss among fixed tuples cannot exclude
alternative raw pieces, even when all64choices of that tuple were tried.

The source is [the new diagnostic](../../../devtools/probe_n17_core_refinement.py)
and [its controls](../../../tests/test_n17_core_refinement.py). [Small receipts](receipts/result-summary.json)
and exact retained packets record generated geometry provenance. `content_sha256`
hashes canonical JSON, not pretty/minified file bytes; published minified packets
are semantically identical to preserved local originals. Baseline B uses G's fresh
same-E-packet1185pair replay, with packet and input identity strictly bound. Endpoint
baseline and cold-check receipts remain historical; no cold checker reran.

From this PR's `packing/`, choose explicit existing interpreter/input paths:
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
Expected `PASS_REPLAYED_PARTIAL_SUPPORT`:18parentrows/7tuples/105fresh pairs.
Replay reconstructs original source atoms, exact child cores and every retained
edge without enumeration/cache. Omitting `--verify` reproduces only the frozen
bounded fixed-tuple diagnostic; no automatic research continuation is prescribed.

Baseline certified PR333 revision2bada1a; parent3071525d4e03 unchanged. Open K2/P2
adaptive producer/539-orbit work stays untouched. A compatible selection is a full
solution of this exact binary abstraction; edges mean only that universal collision
was not established. No common realizable pose, feasible packing, new exclusion or
global proof follows.18supported parents cannot be deleted completely by sound
solution-preserving reasoning on this exact enhanced graph; the other78are unknown.
The earlier96row result applies to its earlier cores, not arbitrary stronger geometry.

Root accepted source soundness and fresh independent retained-support replay.
Hosted source certification is pending under think-0xxc; final metadata CI is
observed separately. Native usage is one declared privacy aggregate/lower bound;
later publication/CI and pre-start setup are excluded. No further H target follows.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
