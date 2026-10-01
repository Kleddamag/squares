---
type: is
id: is-01m3v4ewvx1nfff15khk2s9taz
title: Recalibrate suite-B cost baseline after fast hosted runner
kind: bug
status: in_progress
priority: 2
version: 4
labels: []
dependencies: []
parent_id: is-01m1v56q9h4rvk2tcp2dt9sqyr
created_at: 2026-10-01T07:04:32.877Z
updated_at: 2026-10-01T07:08:40.254Z
---
PR paper head e37362ff9, hosted packing run 36827494079 job 110256353794: suite B ran 2,381 passing tests; 59.83 s reference-shape tier wall failed stale rule against one-reading 104.65 s baseline from run 36739024277 job 109968163416 (2,380 tests). Reconcile both complete observations with geometric mean and a justified tighter absolute ceiling; keep cost policy and proof tests unchanged.

## Notes

Committed and pushed as 751ef78a4 on PR261. Static budget declaration and 55 focused tests passed (0.87s); both observed hosted walls accepted with unchanged policy. Await final hosted checks.
