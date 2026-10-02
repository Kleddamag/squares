---
type: is
id: is-01m3wyad4yp229ckemcctd6zkr
title: "Import wand125: s(77) = 9 (#279)"
kind: task
status: in_progress
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-10-01-result-import-first-application.md
labels:
  - packing
  - result-import
dependencies: []
parent_id: is-01m3yrdxte02c7bnygkke34ct4
created_at: 2026-10-01T23:55:43.131Z
updated_at: 2026-10-02T16:53:07.746Z
---
Result import process from stage 1. New optimality entry; s(78) = 9 follows by monotonicity, a second route beside T-064. Certificate directory first published at bd4de4f6, retained at 1a25a5e. Same checksum-file defect as #280. The cover replaces 84 points on loaded lines by segments of length 2/1000, a shape the reviewed s21, s45 and s60 covers do not have: the review checks whether either checker depends on the earlier shape. Cheapest complete replay zmx2 --d4 --pair-points, up to about 5 thread-hours.

## Notes

2026-10-01: stages 2 and 3 are in draft PR jlevy/squares#292 (branch claude/import-2026-10-01-requests, commit 2b7191461), stacked on #290. Stage 4 not started. The T-id is provisional until #292 is on main; quote it to no author before then.

2026-10-02 (stage 4, PR #298): full --pair-points sweep on cloud runner session_01XNF82uVWu1g5o9eCCX2zYL, branch claude/replay-n77-full (halves x0-44, x45-89, driver devtools.replay_evand_zmx2); d4 --pair-points queued locally after B. Cover audit clean (100 segments of 1/500, not 84; 68 points became one segment, 16 at crossings became two). Review: no blocking defect.
