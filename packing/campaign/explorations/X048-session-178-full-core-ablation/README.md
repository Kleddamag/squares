# Full-interval augmentation explains 71 of 72 fixed tuple losses

Among the frozen 79 E selections, full-interval octagon augmentation loses 71, while
half-interval augmentation loses 72; only E index 58 is additional.
All 96 full-interval cores are strictly valid, contain their old cores and gain positive
area. Each is exactly contained in both H half-interval cores (192 containment checks).
Independent replay made 1,047 fresh predicate calls.
This is fixed-sample mechanism separation, with no replacement search, DFS or
whole-network equivalence claim.

Same original 2522 pieces and center domains.
Full core is hull(old core plus the octagon over the original complete interval); halves
and domains are not split.
All 79 tuples are classified in source-index/ascending-owner-pair order.
A loss has one exact true collision witness; a survivor has all 15 false pairs.
Full losses F71 are a subset of independently certified J72; all H7 survivors survive
the weaker full model.
Additional halving loss is precisely index 58. Equality of complete networks was not
measured. 8 surviving E tuples cover 21 sample parent rows, 75 unknown; B’s separately
established 60 enhanced-parent supports remain intact.
D21 does not replace B60. No tuple loss is parent-row unsupportedness, admission or
optimality.

ONE target 1047 uncached rational calls, 2.187575 s, 154226688 B overall worker peak,
inside 1185 calls/45 s/512 MiB/Job 60. Fresh independent replay directly reconstructs
full cores from old+octagon, rebuilds H children, checks all 96 strict growth/192
nesting and repeats 1047 original rational calls without importing the new diagnostic:
2.055424 s/159236096 B. It independently derives F71, additional 58 and positive 21.
Endpoint 15 tuples/24 parents all survive 225 calls, and a new process replay checks
225\. 26 focused controls 3.31 s/Ruff/types/embedded-script check pass.
Five retained Jobs end empty with cleanup confirmed.
OS peaks can miss short-lived unsampled children.

[Opt-in diagnostic](../../../devtools/probe_n17_full_core_ablation.py),
[controls](../../../tests/test_n17_full_core_ablation.py),
[summary](receipts/result-summary.json) and
[fresh independent receipt](receipts/independent-replay.json).
Raw E/H/G/J and all prior inputs/results/archives stay immutable.
Historical cold checks were reused; no new producer or cold certificate verification
ran. Source identity is Git revision and path; generated SHA fields are canonical JSON
content, not pretty-file bytes.

From packing/, supply preserved B objects/cold receipt (existing I archive transports
them) and choose a new output.
Use your explicit existing project interpreter:
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

On Linux, from `packing/` with the project’s Python 3.14 environment.
Every run requires the cold saved-check receipt (`--checked-receipt`) for the same saved
seed and node:

```sh
SAVED_OBJECTS="YOUR_B_OBJECT_DIRECTORY"
COLD_RECEIPT="YOUR_B_COLD_RECEIPT.json"
SOURCE="campaign/explorations/X048-session-172-capacity-support/receipts/B-support-packet.json"
BASELINE="campaign/explorations/X048-session-174-core-refinement/receipts/B-baseline-replay.json"
HALVES="campaign/explorations/X048-session-174-core-refinement/receipts/B-enhanced-packet.json"
CERTIFICATE="campaign/explorations/X048-session-177-cached-collision/receipts/J-fixed-tuple-certificate.json"
ABLATION="campaign/explorations/X048-session-178-full-core-ablation/receipts/B-ablation-packet.json"
uv run --frozen --all-extras --group dev python -m devtools.probe_n17_full_core_ablation "$SAVED_OBJECTS" \
  --checked-receipt "$COLD_RECEIPT" --source-packet "$SOURCE" --baseline-replay "$BASELINE" \
  --refinement-packet "$HALVES" --conflict-certificate "$CERTIFICATE" \
  --verify "$ABLATION" --output "YOUR_NEW_REPLAY.json"
```
Expected PASS_REPLAYED_FIXED_SAMPLE/1047 fresh pairs/F71/additional 58/positive 21.
Replay verifies fixed classification/provenance; runtime fields are excluded from
comparison while its packet_sha256 binds the entire original packet.
No benchmark claim. The measurement CLI omits --verify; the one target is already spent.

A final test-only fixture repair isolates the reused H memory sampler as well as the new
sampler from historical shared-pytest peaks; production guards and the measured source
remain unchanged.26 controls pass again 3.75 s/Ruff.
This later administrative CI preparation is outside the single native cutoff.

Source/evidence `c6972548e98ec356a8d408e9b34518be87a6cf36` is observed terminal 19
pass/36 skip and all 3 required SUCCESS. Final metadata CI is observed separately.
One native privacy aggregate is a live/boundary lower bound; later publication/CI is
excluded. Another project needs a new W3/ownership/resource gate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
