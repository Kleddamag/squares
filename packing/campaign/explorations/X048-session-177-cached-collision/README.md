# Exact cached collision: agreement, first-use NO-GO

371对固定关系的四种判定路径完全一致，并通过独立有理数回放；
但缓存首次使用成本未达事先冻结的门槛。原路径0.574571s，
准备加首次缓存调用0.680193s，约1.184倍，绝对节省为−0.105622s。
按合同停止adapter-search路线，不调参重测，也不启动matched search。

The fixed corpus comes from B's44compatible selections (660pair occurrences) and
J's298certified collision witnesses. Canonical sorted-owner dedup gives371queries:
281compatible/90collision pairs. Every exact raw-piece/half/domain/core/interval
reference is bound to the same5044enhanced atoms; input/model/B/J identities are pinned.
This is an answer-equivalence and descriptive cost measurement, not new geometry,
parent-row coverage, admission or search speedup. B60supports/36unknown remain unchanged.

| Fixed pass | Seconds | Scope |
| --- | ---: | --- |
| Rational reference |0.574571 | One371query pass |
| Integer uncached |0.427637 | Same ordered exact queries |
| Cache setup |0.409464 | Snapshots and preparation of all5044atoms |
| Initially-empty cached pass |0.270728 | One cache over whole corpus, not reset per query |
| Cached first-use total |0.680193 | Setup plus first pass; failed80percent/0.1s criterion |
| Same-cache repeated pass |0.117992 | Separately descriptive; no search speedup inference |

All four ordered answer arrays agree exactly with expected classes. Overall protocol
2.691652s,1484primitive calls and186671104B sampled OS worker peak; common geometry/
corpus build0.859364s is reported separately. The process peak covers combined
work and is not an isolated per-backend peak. Outer Job observations are retained
separately and can miss short-lived unsampled workers. First/warm caches both hold
181facet entries and1897domain-minimum entries; preparation covers5044atoms.

The one preregistered attempt has ceilings958distinctqueries/4096primitivecalls/
30s/512MiB/Job45. No guard changed and no second profile ran. Fresh independent
replay rebuilt all5044children and the B/Jcorpus using unchanged H/raw functions,
then made371original rational calls; no new adapter/profile implementation was
imported. It verifies values/provenance, not performance statistics. Three scientific
Jobs end0/cleanuptrue/noerrors.25focused tests/Ruff/types pass, including point/
segment, true/false, domain/core mutation, unexpected refusal, pre/post resource
guards, failed-answer omission and strict boolean replay grammar.

[Opt-in adapter/profile](../../../devtools/probe_n17_cached_collision.py),
[controls](../../../tests/test_n17_cached_collision.py) and
[compact receipts](receipts/result-summary.json) retain the result.
The adapter snapshots input geometry, rejects mutation/foreign atoms, keeps fresh
per-inventory caches, propagates unexpected errors and applies pre/post guards.
Kernel, producer, raw/H/A/B diagnostics and default workflows remain unchanged.

Published packets and Jcertificate copy are semantically equal to local originals;
canonical content hashes are not pretty-file byte hashes. The Jcertificate is
historical evidence copied unchanged, not a new tuple-level negative investigation.
Public independent receipt is explicitly a derived summary; original local receipt
remains intact. Git revision/path names source. No cold checker or producer reran.

From packing/, use an explicit existing project interpreter and the preserved B
objects/coldreceipt (transported by the unchanged Iarchive):
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
Expected PASS_FRESH_MIXED_CORPUS,371fresh rational checks. This replay never runs
cached backends or benchmarks. The original measurement command omits --verify;
this project has already used its one target and does not authorize a repeat.

The one measured source is Git `a60cfc611` at the probe path above. Hosted validation
then identified a naming collision: `Guard.evaluate` in Python controls was treated
as browser script code. The identifier-only repair renames it to `check_pair` and
its own call sites;25controls, embedded-script check, Ruff and types pass. The profile
was not rerun and no timing claim is made for the renamed head.

Source/evidence certification pending under think-5sya; exact-head CI is observed
separately. One native privacy aggregate is a lower bound; later publication/CI
after its cutoff is excluded with operator-declared branch attribution. A new
distinct research mechanism needs a new W3/ownership/resource/soundness contract.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
