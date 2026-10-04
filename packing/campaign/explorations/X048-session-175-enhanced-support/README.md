# Enhanced-model replacement supports

完整 raw-piece 搜索新增23个经独立回放的父行支持：相同增强模型现有41/96行支持，
55行未知。原H的7组/18行全部保留。此次唯一搜索达到100000次关系检查上限；
没有扩大预算或再次搜索。结果是有限二元网络的正支持，不是真实共同位姿或全局证明。

All2522 original pieces receive two half-interval enhanced cores, giving5044atoms.
The original center domain and parent(owner,row) remain fixed;192half rows are
distinct from96parents. Cores use the unchanged H construction:
`hull(old core union octagon_core(half interval))`, accepted by exact whole-child
`strict_core` with old-core containment. Each reference includes original piece,
source interval/domain/core identity, raw atom index, half and enhanced core identity.
No piece is dropped, no child domain is recomputed and no adaptive producer runs.

| Evidence | Measured result | Boundary |
| --- | --- | --- |
| ONE B search |26cliques,41parents(+23),100000unique pairs,134DFS nodes | INCOMPLETE pair guard;55unknown, no unsupported candidate |
| Cost |157.625s protocol/160.797s Job;170758144B OS worker peak |180s/512MiB protocol;240s outer Job; no guard relaxation |
| Independent B replay |26cliques,390fresh pairs;41parents/1.417s | Rebuilds all5044children independently using unchanged H builder; exact H7prefix/input/model identity |
| Endpoint |148raw/296children,24parents,15seeds;225fresh replay pairs | Explicit full endpoint angle enclosure lies in selected child interval |
| Controls |36tests3.36s; Ruff/types clean | Finite exhaustive assignments, half identity, strict growth, provenance, seeds, caps, failures and direct replay |

All7B seeds are freshly validated and charged65unique queries before any coverage
is recorded. Deterministic forward-MRV uses unchanged LazySupports. Pre/post query
time/memory checks prevent failed queries entering its cache. An all-owner clique
is a full solution of this exact binary network, whose edges mean collision was
not proved. Such a clique prevents whole-parent deletion under AC/PC in this model.
Search failure, budget exhaustion and55unknown parents imply no unsupportedness.
All Jobs end empty with confirmed cleanup/no errors. OS peaks may miss short-lived
children; protocol and outer Job limits are separate. Original B–J/G/I remain frozen.

[New diagnostic](../../../devtools/probe_n17_enhanced_row_support.py),
[focused controls](../../../tests/test_n17_enhanced_row_support.py) and
[compact receipts](receipts/result-summary.json) retain this bounded outcome.
Published packet JSON is semantically equal to local pretty originals.
`content_sha256` denotes canonical JSON content, not serialized file bytes.
Input/cold-check identities bind historical saved objects; no cold checker reran.
Baseline repository revision is14d131c8aaf2ac94239755f8438ab7d5e0192ef4;
the new source is introduced by this PR's subsequent publication revision.

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
Expected PASS_REPLAYED_PARTIAL_SUPPORT,41parents/26cliques/390fresh pairs.
Replay performs no DFS or cached pair lookup and recomputes coverage from exact refs.
It certifies retained positive support; it does not certify search exhaustion/statistics.

This attempt ends at its preregistered cap. No automatic capacity or ordering ladder
follows. Any next project needs a new W3/ownership/resource contract. Source/evidence
hosted certification is initially pending under think-wh57; exact-head CI is observed
separately. Native usage is one privacy aggregate/lower bound; later finalization and
CI after its cutoff are excluded, with declared branch association.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
