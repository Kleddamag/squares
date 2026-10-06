---
type: is
id: is-01m482vcnp34p75qmjdbjqa9qn
title: "Import wand125/square-packing-bounds 8cc13bf..2fad66e: ten mixed finer-net certificates (n = 18, 19, 20, 26, 27, 28, 29, 30, 39, 41), check2 bundles"
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m482krnapg9vxqd91zjrg171
hold: null
hold_until: null
created_at: 2026-10-06T07:46:32.757Z
updated_at: 2026-10-06T08:28:59.984Z
started_at: 2026-10-06T07:47:18.411Z
---
Intake sweep 2026-10-06 08:00Z: head 2fad66e, 10 commits past 65e408c. s(18) >= 941/200 and s(19) >= 193/40 raise T-099 and T-100. Lane R7.

## Notes

R7 progress 2026-10-06T08:35Z (branch claude/ecstatic-pascal-pothtx-r7, worktree /home/user/squares-lanes/r7):
- a7069fd4a packet wand125-mixed-bounds-check2-2026-10-06 at 2fad66e (10 dirs; 113 retained, 68 pinned); audit_check2, bundle_check2, cpp-sample; all 10 audits EXACT_PREMISES_HOLD, all 10 bindings BUNDLE_BOUND_TO_PACKET_AND_NET.
- 183cb1fc6 records T-108..T-117 at V0/C0 (provisional ids; contiguity check fails on the branch alone), eb004e7c5 re-pin.
- check2 = format M unchanged; checker = source's copy of sqverify_fast (sqverify-proof-net fe12e036c, build ab6e33e1), so a sqverify-fast replay is shared-components for the nine check2; T-114 (n29) is a C++ proof bundle, independent as T-099.
- Census running at 1 thread (scratch r7/census-mixed, script r7/scripts/census2.sh); review running in /home/user/squares-lanes/r7-review (claude -p), output scratch r7/review/output.md.
- Pending: C++ samples (cpp-sample on each check2, sample on n29) after PG 8378 exits; census rows -> repo; --evidence entries (shared-components); exit; validation.
