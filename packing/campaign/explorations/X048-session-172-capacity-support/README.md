# Session 172: the frozen raw binary graph supports every row

All **96 live owner-angle rows** have freshly replayed (same implementation, no search)
complete six-owner supports.
The one preregistered capacity completion attempt closes whole-row deletion by this
exact binary network on the saved B16-bin/2-round state.
It does not establish actual geometric poses, feasibility of a packing or global
optimality.

Baseline `1a7f2ad99abfd3394c99080fcaffb70021b01b82`; frozen parent PR 307
`1525d4e03b891d6cbc9a7c0bb3fd1880765cfb65`. Existing cold-checked B objects were reused;
no producer, kernel, capture/Flag2, standing-checker or admission path changed.
[D1/D2](../X048-session-171-raw-row-support/README.md) remain frozen.

## Protocol and result

Same raw 2,522 atoms, accepted strict cores, sorted-owner `universal_collision`
predicate and forward-MRV order.
All 57 D2 selections were rebuilt from exact provenance and checked through the ordinary
budgeted cache: 329 unique seed pairs, all 69 D2 rows retained.
The retained selections begin with that exact 57 selection prefix.
Search covered missing rows only.
CLI default 50,000 remains; this one target explicitly declared 250,000.

| Quantity | Actual |
| --- | ---: |
| Supported rows / complete selections | 96 / 79 |
| Unique exact pairs / DFS nodes | 62,361 / 154 |
| Protocol wall / CPU | 17.0085522 s / 17.015625 s |
| Whole Job wall / observed worker peak | 20.328 s / 156,405,760 B |
| Fresh replay selections / exact pairs | 79 / 1,185 |

The coordinator’s separate replay reconstructed atoms and directly tested every
selection without DFS/cache.
`PASS_REPLAYED_ALL_ROWS`: 0.4501 s protocol, 3.687 s Job, 153,677,824 B worker.
No unsupported row or exclusion was claimed.
All Job receipts report Job 0 and confirmed tree cleanup.
Per-process working-set observations and Job committed memory are separately labelled in
[the summary](receipts/result-summary.json).

Each clique is a full solution of the frozen binary network, whose edges mean only that
universal collision was not proved.
Sound AC/PC or complete reasoning on these unchanged atoms/predicates must preserve it.
A witness touching each row therefore prevents whole-row deletion.
This does not say every raw atom is supported or that pairwise choices have a common
realisable pose; stronger geometry is a different model.

## Bounds and controls

Frozen target ceilings: 250,000 unique pairs, 100,000 nodes, 180 protocol seconds, 512
MiB worker; Job 240 s, available RAM>=8 GiB. Inventory 4,096 atoms/six owners/128 rows,
input 64 MiB decompressed and packet 4 MiB. No limit was changed after measurement.
All rows were supported well before capacity; no further target or cap ladder followed.

51 focused tests passed in 2.94 s; Ruff/types clean.
Controls retain the earlier exact finite-model, seed/provenance and guard regressions,
plus default/invalid/high-cap parsing and actual search/partial/final limit propagation.
The `endpoint6` state’s 24 rows and its exact endpoint survive; 15 selections were
freshly replayed with 225 pairs.

Planning extrapolated ~68 s at 250k and 20–40 MiB additional cache memory from D2’s 50k
measurement. These were estimates.
Completion at 62,361 pairs means 250k runtime and memory were not measured; no scaling
guarantee or cold speedup is inferred.

## Retained witnesses and replay

[B packet](receipts/B-support-packet.json),
[fresh replay](receipts/B-independent-replay.json) and endpoint packets retain exact
piece/domain/core/source references.
Compact copies were checked JSON-equal to local pretty originals.
Receipt hashes identify canonical JSON content.
Large inputs and local full/partial/Job logs remain outside Git.
Tool identity is this publication’s revision plus
`packing/devtools/probe_n17_raw_row_support.py`.

From `packing/`, using explicit Python 3.14 and supplied saved-object paths:

```powershell
$ProjectPython = (Resolve-Path '.venv/Scripts/python.exe').Path
$InputObjects = 'PATH/TO/SAVED-OBJECTS'
$ColdReceipt = 'PATH/TO/COLD-RECEIPT.json'
$D2Packet = 'PATH/TO/D2_B-support-packet.json'
$Out = 'PATH/TO/E_OUT.json'
& $ProjectPython -m devtools.probe_n17_raw_row_support $InputObjects --checked-receipt $ColdReceipt --strategy forward-mrv --seed-packet $D2Packet --max-pairs 250000 --output $Out
& $ProjectPython -m devtools.probe_n17_raw_row_support $InputObjects --checked-receipt $ColdReceipt --verify $Out --output 'PATH/TO/REPLAY.json'
```

The frozen target additionally used the declared local Job supervisor.
Disposition: retire-success for this exact whole-row route.
Any next work must compare a genuinely different unowned mechanism or a useful
standalone capability at a new W3 gate.

Source/evidence hosted fast certification passed at
`ef8c425472302905c93cf49a9182e06f218b07d2`; final metadata CI is observed separately.
The first suite-D run passed 2030 tests but exceeded the unchanged 131 s ceiling at
132.94 s. The unchanged failed-job rerun passed at 123.45 s; required aggregation
refused mixed-attempt wall accounting.
A coherent unchanged full-workflow rerun passed.
No tests, source or thresholds were altered.
Session 172’s actual administrative end and earlier native cutoff stay unchanged.

A valid cold receipt may be transported or regenerated for the same saved seed and node.
Its timing, host and other metadata are not part of input identity; seed/node content
and the stalled-state checks remain mandatory.
Historical receipts stay historical evidence.

Every run needs a cold saved-check receipt for the saved seed and node:
`--checked-receipt` is a required argument, and the probe refuses a receipt whose seed
or node digest differs from the objects it is given.

The same search and replay on Linux, from `packing/` with the project’s Python 3.14
environment:

```sh
SAVED_OBJECTS="PATH/TO/SAVED-OBJECTS"
COLD_RECEIPT="PATH/TO/VALID-COLD-RECEIPT.json"
D2_PACKET=campaign/explorations/X048-session-171-raw-row-support/receipts/D2_B-support-packet.json
OUT="PATH/TO/E_OUT.json"
uv run --frozen --all-extras --group dev python -m devtools.probe_n17_raw_row_support \
  "$SAVED_OBJECTS" --checked-receipt "$COLD_RECEIPT" --strategy forward-mrv \
  --seed-packet "$D2_PACKET" --max-pairs 250000 --output "$OUT"
uv run --frozen --all-extras --group dev python -m devtools.probe_n17_raw_row_support \
  "$SAVED_OBJECTS" --checked-receipt "$COLD_RECEIPT" \
  --verify campaign/explorations/X048-session-172-capacity-support/receipts/B-support-packet.json \
  --output "PATH/TO/NEW-REPLAY.json"
```

Commits cited in this record that are not in this branch’s history resolve at the tag
`archive/guzhou-review-a-333` (Guzhou’s original nine-session branch); those from PR 307
and PR 325 also resolve at `refs/pull/325/head`. The references are provenance only; no
code reads them (`OR-18`). “Fresh replay” here means the same implementation re-run in a
separate process without search; receipt names ending in `-independent-replay.json`
predate that wording.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
