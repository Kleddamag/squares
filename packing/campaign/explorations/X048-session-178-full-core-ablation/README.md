# Full-interval augmentation explains71of72fixed tuple losses

冻结E79组选取中，全区间octagon增强已使71组丢失；H的半区间增强使72组丢失，
额外仅E索引58。全部96个全区间核心均严格有效、包含旧核心且有正面积增长，
并精确包含于两个H半区间核心（192项包含关系）。独立回放重新核验1047对判定。
这是固定样本的机制分解：没有replacement search、DFS或整个网络等价结论。

Same original2522pieces and center domains. Full core is hull(old core plus the
octagon over the original complete interval); halves and domains are not split.
All79tuples are classified in source-index/ascending-owner-pair order. A loss has
one exact true collision witness; a survivor has all15false pairs. Full losses F71
are a subset of independently certified J72; all H7survivors survive the weaker
full model. Additional halving loss is precisely index58. Equality of complete
networks was not measured.8surviving E tuples cover21sample parent rows,75unknown;
B's separately established60enhanced-parent supports remain intact. D21does not
replace B60. No tuple loss is parent-row unsupportedness, admission or optimality.

ONE target1047uncached rational calls,2.187575s,154226688B overall worker peak,
inside1185calls/45s/512MiB/Job60. Fresh independent replay directly reconstructs
full cores from old+octagon, rebuilds Hchildren, checks all96strict growth/192nesting
and repeats1047original rational calls without importing the new diagnostic:
2.055424s/159236096B. It independently derives F71, additional58 and positive21.
Endpoint15tuples/24parents all survive225calls, and a newprocess replay checks225.
26focused controls3.31s/Ruff/types/embedded-script check pass. Five retained Jobs
end empty with cleanup confirmed. OS peaks can miss short-lived unsampled children.

[Opt-in diagnostic](../../../devtools/probe_n17_full_core_ablation.py),
[controls](../../../tests/test_n17_full_core_ablation.py), [summary](receipts/result-summary.json)
and [fresh independent receipt](receipts/independent-replay.json). Raw E/H/G/J and
all prior inputs/results/archives stay immutable. Historical cold checks were reused;
no new producer or coldcertificate verification ran. Source identity is Git revision
and path; generated SHA fields are canonical JSON content, not pretty-file bytes.

From packing/, supply preserved B objects/coldreceipt (existing Iarchive transports
them) and choose a new output. Use your explicit existing project interpreter:
```powershell
$ProjectPython = (Resolve-Path '.venv/Scripts/python.exe').Path
$SavedObjects = (Resolve-Path 'YOUR_B_OBJECT_DIRECTORY').Path
$ColdReceipt = (Resolve-Path 'YOUR_B_COLD_RECEIPT.json').Path
$Source = 'campaign/explorations/X048-session-172-capacity-support/receipts/B-support-packet.json'
$Baseline = 'campaign/explorations/X048-session-174-core-refinement/receipts/B-baseline-replay.json'
$Halves = 'campaign/explorations/X048-session-174-core-refinement/receipts/B-enhanced-packet.json'
$Certificate = 'campaign/explorations/X048-session-177-cached-collision/receipts/J-fixed-tuple-certificate.json'
$Ablation = 'campaign/explorations/X048-session-178-full-core-ablation/receipts/B-ablation-packet.json'
& $ProjectPython -m devtools.probe_n17_full_core_ablation $SavedObjects `
  --checked-receipt $ColdReceipt --source-packet $Source --baseline-replay $Baseline `
  --refinement-packet $Halves --conflict-certificate $Certificate `
  --verify $Ablation --output 'YOUR_NEW_REPLAY.json'
```
Expected PASS_REPLAYED_FIXED_SAMPLE/1047freshpairs/F71/additional58/positive21.
Replay verifies fixed classification/provenance; runtime fields are excluded from
comparison while its packet_sha256 binds the entire original packet. No benchmark
claim. The measurement CLI omits --verify; the one target is already spent.

A final test-only fixture repair isolates the reused H memory sampler as well as
the new sampler from historical shared-pytest peaks; production guards and the
measured source remain unchanged.26controls pass again3.75s/Ruff. This later
administrative CI preparation is outside the single native cutoff.

Source/evidence `c6972548e98ec356a8d408e9b34518be87a6cf36` is observed terminal19pass/36skip
and all3requiredSUCCESS. Final metadata CI is observed separately. One native privacy aggregate is a live/boundary lower bound; later
publication/CI is excluded. Another project needs a new W3/ownership/resource gate.

<!-- This document follows common-doc-guidelines.md. -->
