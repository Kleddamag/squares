# Exact cached collision: agreement, first-use NO-GO

All four predicate paths agree on 371 fixed relations and pass independent rational
replay. Cached first-use cost missed the preregistered gate: the original path took
0.574571 s, while preparation plus the first cached pass took 0.680193 s (about 1.184
times as long; saving −0.105622 s). The adapter-search route was stopped without
retuning, repeating the profile or starting matched search.

The fixed corpus comes from B’s 44 compatible selections (660 pair occurrences) and J’s
298 certified collision witnesses.
Canonical sorted-owner dedup gives 371 queries: 281 compatible/90 collision pairs.
Every exact raw-piece/half/domain/core/interval reference is bound to the same 5044
enhanced atoms; input/model/B/J identities are pinned.
This is an answer-equivalence and descriptive cost measurement, not new geometry,
parent-row coverage, admission or search speedup.
B60 supports/36 unknown remain unchanged.

| Fixed pass | Seconds | Scope |
| --- | ---: | --- |
| Rational reference | 0.574571 | One 371 query pass |
| Integer uncached | 0.427637 | Same ordered exact queries |
| Cache setup | 0.409464 | Snapshots and preparation of all 5044 atoms |
| Initially-empty cached pass | 0.270728 | One cache over whole corpus, not reset per query |
| Cached first-use total | 0.680193 | Setup plus first pass; failed 80 percent/0.1 s criterion |
| Same-cache repeated pass | 0.117992 | Separately descriptive; no search speedup inference |

All four ordered answer arrays agree exactly with expected classes.
Overall protocol 2.691652 s, 1484 primitive calls and 186671104 B sampled OS worker
peak; common geometry/ corpus build 0.859364 s is reported separately.
The process peak covers combined work and is not an isolated per-backend peak.
Outer Job observations are retained separately and can miss short-lived unsampled
workers. First/warm caches both hold 181 facet entries and 1897 domain-minimum entries;
preparation covers 5044 atoms.

The one preregistered attempt has ceilings 958 distinct queries/4096 primitive calls/ 30
s/512 MiB/Job 45. No guard changed and no second profile ran.
Fresh independent replay rebuilt all 5044 children and the B/J corpus using unchanged
H/raw functions, then made 371 original rational calls; no new adapter/profile
implementation was imported.
It verifies values/provenance, not performance statistics.
Three scientific Jobs end 0/cleanup true/no errors.
25 focused tests/Ruff/types pass, including point/ segment, true/false, domain/core
mutation, unexpected refusal, pre/post resource guards, failed-answer omission and
strict boolean replay grammar.

[Opt-in adapter/profile](../../../devtools/probe_n17_cached_collision.py),
[controls](../../../tests/test_n17_cached_collision.py) and
[compact receipts](receipts/result-summary.json) retain the result.
The adapter snapshots input geometry, rejects mutation/foreign atoms, keeps fresh
per-inventory caches, propagates unexpected errors and applies pre/post guards.
Kernel, producer, raw/H/A/B diagnostics and default workflows remain unchanged.

Published packets and J certificate copy are semantically equal to local originals;
canonical content hashes are not pretty-file byte hashes.
The J certificate is historical evidence copied unchanged, not a new tuple-level
negative investigation.
Public independent receipt is explicitly a derived summary; original local receipt
remains intact. Git revision/path names source.
No cold checker or producer reran.

From packing/, use an explicit existing project interpreter and the preserved B
objects/cold receipt (transported by the unchanged I archive):
```powershell
$ProjectPython = (Resolve-Path '.venv/Scripts/python.exe').Path
$SavedObjects = (Resolve-Path 'YOUR_B_OBJECT_DIRECTORY').Path
$ColdReceipt = (Resolve-Path 'YOUR_B_COLD_RECEIPT.json').Path
$Source = 'campaign/explorations/X048-session-172-capacity-support/receipts/B-support-packet.json'
$Baseline = 'campaign/explorations/X048-session-174-core-refinement/receipts/B-baseline-replay.json'
$Refinement = 'campaign/explorations/X048-session-174-core-refinement/receipts/B-enhanced-packet.json'
$Support = 'campaign/explorations/X048-session-176-owner-priority/receipts/B-support-packet.json'
$Certificate = 'campaign/explorations/X048-session-177-cached-collision/receipts/J-fixed-tuple-certificate.json'
$Profile = 'campaign/explorations/X048-session-177-cached-collision/receipts/profile-packet.json'
& $ProjectPython -m devtools.probe_n17_cached_collision $SavedObjects `
  --checked-receipt $ColdReceipt --source-packet $Source --baseline-replay $Baseline `
  --refinement-packet $Refinement --support-packet $Support `
  --conflict-certificate $Certificate --verify $Profile --output 'YOUR_NEW_REPLAY.json'
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
SUPPORT="campaign/explorations/X048-session-176-owner-priority/receipts/B-support-packet.json"
CERTIFICATE="campaign/explorations/X048-session-177-cached-collision/receipts/J-fixed-tuple-certificate.json"
PROFILE="campaign/explorations/X048-session-177-cached-collision/receipts/profile-packet.json"
uv run --frozen --all-extras --group dev python -m devtools.probe_n17_cached_collision "$SAVED_OBJECTS" \
  --checked-receipt "$COLD_RECEIPT" --source-packet "$SOURCE" --baseline-replay "$BASELINE" \
  --refinement-packet "$REFINEMENT" --support-packet "$SUPPORT" \
  --conflict-certificate "$CERTIFICATE" --verify "$PROFILE" --output "YOUR_NEW_REPLAY.json"
```
Expected `PASS_FRESH_MIXED_CORPUS`, 371 fresh rational checks.
This replay never runs cached backends or benchmarks.
The original measurement command omits --verify; this project has already used its one
target and does not authorize a repeat.

The one measured source is Git `a60cfc611` at the probe path above.
Hosted validation then identified a naming collision: `Guard.evaluate` in Python
controls was treated as browser script code.
The identifier-only repair renames it to `check_pair` and its own call sites; 25
controls, embedded-script check, Ruff and types pass.
The profile was not rerun and no timing claim is made for the renamed head.

Source/evidence `3348a22ab85b7514aed09d76c0aa82f4f8b51731` is observed terminal 19
pass/36 skip and all 3 required SUCCESS. Final metadata CI is observed separately.
One native privacy aggregate is a lower bound; later publication/CI after its cutoff is
excluded with operator-declared branch attribution.
A new distinct research mechanism needs a new W3/ownership/resource/soundness contract.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
