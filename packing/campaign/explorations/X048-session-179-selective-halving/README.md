# Two refined rows preserve all frozen certificates in2623atoms

冻结样本的72组排除、7组幸存与当前44组/60父行正支持全部保留。
只细分(18,13)、(19,5)两行，原piece代价62+39=101；真实mixedinventory
2522+101=2623，完整H模型为5044。独立重建所有核心、64候选子集并fresh核验735对。

The minimum is restricted to J58's retained seven-edge library and its six candidate
parent rows, with original-piece cost and lexicographic row-list tie break. It is
not a global geometry or producer refinement minimum. Full cores augment the
original complete interval; selected rows use both frozen H half cores. Every
original raw piece and its center-domain polygon is retained with distinct full/half refs.

All71 D full-loss witnesses are freshly tested on every actual mixed endpoint
variant. Four selected J58 half-pair conflicts cover all64assignments. The first
seven B cliques bind exactly to H7 and their original E indices; all44 projected
B cliques receive660fresh directed pair checks and cover60parents (36unknown).
The exact E79 classification is preserved:72fixed losses and seven survivors.
There is no new support search, whole-network equivalence, unsupported-row,
common realizable pose, admission or global lower-bound claim. Atom count alone
does not establish a memory or speed improvement. Oldproducer/kernel/H/A/B/C/D
modules and all archived inputs remain unchanged.

ONE measurement:735uncachedcalls/2.763400s/157941760B actualworker peak.
Independent replay:735freshcalls/2.038573s/164585472B; imports neither new E nor D
runner. Each limit remains1024calls/45s/512MiB/outerJob60 with8GiB free-memory guard.
32controls3.62s/Ruff/types/embedded-script pass. Both controlled Jobs and target/
independent Jobs report active0, cleanuptrue and no errors. OS sampling can miss
short-lived children; receipts do not claim perfect tree RSS maxima.

[Packet](receipts/B-mixed-packet.json), [independent replay](receipts/independent-replay.json)
and [summary](receipts/result-summary.json). Canonical packet content SHA:
`13b1b32ab23b4c85048ae13646bd7eb7fa7f05e66b1054713aafc854486c41a6`.
Generated hashes identify canonical JSON content, not pretty-file bytes. Source
identity is this Git revision and devtools/probe_n17_selective_halving.py.
Coldchecker evidence is historical; no producer or coldcertificate rerun occurred.

From packing/, use your existing project interpreter and saved B objects/coldreceipt
(the immutable Iarchive transports inputs); choose a new output:
```powershell
$ProjectPython = (Resolve-Path '.venv/Scripts/python.exe').Path
$SavedObjects = (Resolve-Path 'YOUR_B_OBJECT_DIRECTORY').Path
$ColdReceipt = (Resolve-Path 'YOUR_B_COLD_RECEIPT.json').Path
$Source = 'campaign/explorations/X048-session-172-capacity-support/receipts/B-support-packet.json'
$Baseline = 'campaign/explorations/X048-session-174-core-refinement/receipts/B-baseline-replay.json'
$Halves = 'campaign/explorations/X048-session-174-core-refinement/receipts/B-enhanced-packet.json'
$Certificate = 'campaign/explorations/X048-session-177-cached-collision/receipts/J-fixed-tuple-certificate.json'
$FullPacket = 'campaign/explorations/X048-session-178-full-core-ablation/receipts/B-ablation-packet.json'
$FullReplay = 'campaign/explorations/X048-session-178-full-core-ablation/receipts/independent-replay.json'
$Supports = 'campaign/explorations/X048-session-176-owner-priority/receipts/B-support-packet.json'
$Mixed = 'campaign/explorations/X048-session-179-selective-halving/receipts/B-mixed-packet.json'
& $ProjectPython -m devtools.probe_n17_selective_halving $SavedObjects `
  --checked-receipt $ColdReceipt --source-packet $Source --baseline-replay $Baseline `
  --refinement-packet $Halves --conflict-certificate $Certificate `
  --full-packet $FullPacket --full-replay $FullReplay --support-packet $Supports `
  --verify $Mixed --output 'YOUR_NEW_REPLAY.json'
```
Expected PASS_REPLAYED_FIXED_CERTIFICATES/735freshpairs/2623atoms/60positiveparents.
Fresh replay rechecks all retained certificates; runtime fields are excluded from
scientific comparison while packet_sha256 binds the complete original packet.
The measurement CLI omits --verify; this project's one target is already spent.

Source/evidence certification pending under think-ns4t; exact-head CI is observed
separately. One native privacy aggregate is a live/boundary lower bound; later
publication/CI is excluded. Further work needs a new scoped value/ownership gate.

<!-- This document follows common-doc-guidelines.md. -->
