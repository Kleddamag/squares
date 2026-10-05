# Two refined rows preserve all frozen certificates in2623 atoms

The fixed sample retains all 72 tuple-loss certificates, seven surviving selections and
the current 44 selections supporting 60 parent rows.
Only rows (18, 13) and (19, 5) are halved, at original-piece cost 62 + 39 = 101. The
actual mixed inventory has 2,522 + 101 = 2,623 atoms, versus 5,044 in the full H model.
Independent replay rebuilt all cores and 64 candidate subsets and made 735 fresh pair
checks.

The minimum is restricted to J58’s retained seven-edge library and its six candidate
parent rows, with original-piece cost and lexicographic row-list tie break.
It is not a global geometry or producer refinement minimum.
Full cores augment the original complete interval; selected rows use both frozen H half
cores. Every original raw piece and its center-domain polygon is retained with distinct
full/half refs.

All71 D full-loss witnesses are freshly tested on every actual mixed endpoint variant.
Four selected J58 half-pair conflicts cover all 64assignments. The first seven B cliques
bind exactly to H7 and their original E indices; all 44 projected B cliques receive660
fresh directed pair checks and cover60 parents (36 unknown).
The exact E79 classification is preserved:72fixed losses and seven survivors.
There is no new support search, whole-network equivalence, unsupported-row, common
realizable pose, admission or global lower-bound claim.
Atom count alone does not establish a memory or speed improvement.
Oldproducer/kernel/H/A/B/C/D modules and all archived inputs remain unchanged.

ONE measurement:735uncachedcalls/2.763400 s/157941760 B actual worker peak.
Independent replay:735 fresh calls/2.038573 s/164585472 B; imports neither new E nor D
runner. Each limit remains1024 calls/45 s/512 MiB/outer Job60 with8 GiB free-memory
guard. 32 controls 3.62 s/Ruff/types/embedded-script pass.
Both controlled Jobs and target/ independent Jobs report active 0, cleanup true and no
errors.
OS sampling can miss short-lived children; receipts do not claim perfect tree RSS
maxima.

[Packet](receipts/B-mixed-packet.json),
[independent replay](receipts/independent-replay.json) and
[summary](receipts/result-summary.json).
Canonical packet content SHA:
`13b1b32ab23b4c85048ae13646bd7eb7fa7f05e66b1054713aafc854486c41a6`. Generated hashes
identify canonical JSON content, not pretty-file bytes.
Source identity is this Git revision and devtools/probe_n17_selective_halving.py.
Coldchecker evidence is historical; no producer or cold certificate rerun occurred.

From packing/, use your existing project interpreter and saved B objects/cold receipt
(the immutable I archive transports inputs); choose a new output:
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
Expected PASS_REPLAYED_FIXED_CERTIFICATES/735 fresh pairs/2623 atoms/60 positive
parents. Fresh replay rechecks all retained certificates; runtime fields are excluded
from scientific comparison and fresh semantic checks establish packet content.
Legacy digest fields remain historical bookkeeping and are not reuse gates.
The measurement CLI omits --verify; this project’s one target is already spent.

Source/evidence `e2fe7aa8ccbcd3e8121d0c01d1bc93ec9f05855b` is observed terminal 19
pass/36 skip and all 3 requiredSUCCESS. Final metadata CI is observed separately.
One native privacy aggregate is a live/boundary lower bound; later publication/CI is
excluded. Further work needs a new scoped value/ownership gate.

A valid cold receipt may be transported or regenerated for the same saved seed and node.
Its timing, host and other metadata are not part of input identity; seed/node content
and the stalled-state checks remain mandatory.
Historical receipts stay historical evidence.

POSIX replay, from `packing/` with the existing Python 3.14 environment:

```sh
SAVED_OBJECTS="PATH/TO/SAVED-B-OBJECTS"
COLD_RECEIPT="PATH/TO/VALID-COLD-RECEIPT.json"
R=campaign/explorations
uv run --frozen --all-extras --group dev python -m devtools.probe_n17_selective_halving \
  "$SAVED_OBJECTS" --checked-receipt "$COLD_RECEIPT" \
  --source-packet "$R/X048-session-172-capacity-support/receipts/B-support-packet.json" \
  --baseline-replay "$R/X048-session-174-core-refinement/receipts/B-baseline-replay.json" \
  --refinement-packet "$R/X048-session-174-core-refinement/receipts/B-enhanced-packet.json" \
  --conflict-certificate "$R/X048-session-177-cached-collision/receipts/J-fixed-tuple-certificate.json" \
  --full-packet "$R/X048-session-178-full-core-ablation/receipts/B-ablation-packet.json" \
  --full-replay "$R/X048-session-178-full-core-ablation/receipts/independent-replay.json" \
  --support-packet "$R/X048-session-176-owner-priority/receipts/B-support-packet.json" \
  --verify "$R/X048-session-179-selective-halving/receipts/B-mixed-packet.json" \
  --output "PATH/TO/NEW-REPLAY.json"
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
