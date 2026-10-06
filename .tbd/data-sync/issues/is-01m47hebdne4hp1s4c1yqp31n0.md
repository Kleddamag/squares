---
type: is
id: is-01m47hebdne4hp1s4c1yqp31n0
title: "Import wand125 #366: mixed_n18_L4704 (s(18) >= 588/125, 832-node net) and mixed_n19_L48229 (s(19) >= 48229/10000) at 65e408c"
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m47hea1vkqx8h5wzdzcyqs5k
hold: null
hold_until: null
created_at: 2026-10-06T02:42:19.701Z
updated_at: 2026-10-06T03:36:39.522Z
started_at: 2026-10-06T02:45:53.733Z
---

## Notes

2026-10-06 03:40Z, lane R2 progress.

Stages 2-3 done on claude/ecstatic-pascal-pothtx-r2: packet wand125-mixed-bounds-finer-net-2026-10-06 at 65e408c (5046b8c96), T-099 and T-100 registered at V0/C0 (95a96145d), pin 35a148afa.

Stage 4 so far (82b2183a5):
- Source checker, pricing samples at 2 workers: n18 7 nodes, ratio 1.06, full 12.8 CPU-h; n19 7 nodes, ratio 1.14, full 13.4 CPU-h. All nodes matched the shipped records.
- sqverify-fast (main's crate, source_sha256 d97758bb, not in REVIEWED_SOURCES): n18 VERIFIED 832/832, n19 VERIFIED 416/416. Census rows committed; no rung rests on them until think-gcld accepts.
- Controls: source checker and sqverify-fast refuse 99/100 and 1-1e-6 mass mutants at nodes 797 and 37, and three corrupted nets each for its own premise.
- Defect found: census --control on a declared net uses the standard step in check_sqverify_fast.mixed_exact (think-q9gu).

Running: n18 complete replay of the bundle's own driver, 2 workers, started 03:28:44Z, ETA about 11:15Z. Separately prompted review started 03:17Z in /home/user/squares-lanes/r2-review.
