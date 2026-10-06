---
type: is
id: is-01m482vcnp34p75qmjdbjqa9qn
title: "Import wand125/square-packing-bounds 8cc13bf..2fad66e: ten mixed finer-net certificates (n = 18, 19, 20, 26, 27, 28, 29, 30, 39, 41), check2 bundles"
kind: task
status: in_progress
priority: 1
version: 4
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m482krnapg9vxqd91zjrg171
hold: null
hold_until: null
created_at: 2026-10-06T07:46:32.757Z
updated_at: 2026-10-06T09:17:43.672Z
started_at: 2026-10-06T07:47:18.411Z
---
Intake sweep 2026-10-06 08:00Z: head 2fad66e, 10 commits past 65e408c. s(18) >= 941/200 and s(19) >= 193/40 raise T-099 and T-100. Lane R7.

## Notes

R7 progress 2026-10-06T09:20Z: review stored (8b57141f2, SHA-256 1d5e1326..., accept all ten, S3); fixes FN-1..FN-7 at 19c99c7ed (FN-1: 8 of 9 check2 run logs read an unpublished input, now named in UNPUBLISHED_RUN_INPUTS; FN-2: 277 control witnesses recomputed exactly with check_sqverify_fast.mixed_exact); T-108..T-117 at V0/C1; re-pin f2f46ab8c. cpp-sample n41 at 409, 415 verified. Census continuing at 1 thread (scratch r7/census-mixed, census2.sh); cpp.sh waits for PG 8378 exit or census end. Census rows identical to the source's check2 run logs at every compared direction (nodes and bounds), as expected for a copy of the crate.
