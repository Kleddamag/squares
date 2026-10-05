---
type: is
id: is-01m46g4zqq75w7rn8e3j3fgrpr
title: "Import wand125 #366 s(18) >= 47/10 (finer net, 43050ed) and think-4qit s(66) >= 843/100 (d73ce20): sqverify_fast reads a declared net, replay, review"
kind: task
status: in_progress
priority: 1
version: 4
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m46g4yac7ewc22drc7twjhy5
child_order_hints:
  - is-01m471mzy4w6jycg53h50v68zc
hold: null
hold_until: null
created_at: 2026-10-05T17:00:29.815Z
updated_at: 2026-10-05T22:06:20.098Z
started_at: 2026-10-05T17:06:29.900Z
---

## Notes

2026-10-05 18:55 lane B (branch claude/ecstatic-pascal-pothtx-wand-net, worktree /home/user/squares-lanes/wand-net):
- 045d9ff95 packet wand125-mixed-bounds-finer-net-2026-10-05 at 43050ed (mixed_n66_L843 from d73ce20, mixed_n18_L470 on a declared net); n66-L843 row in the audit tool, mixed-audit + mixed-fetch pass; d73ce20 intake-watch read removed.
- f007d7afd sqverify_fast reads a format M proof_net (lemma N0 in SOUNDNESS.md, tests/declared_net.rs, check_sqverify_fast declared-net group); measure verifier Rust gate green.
- 52d8e8bd7 T-096 (n18) and T-097 (n66) at V0/C0 (provisional ids), audit_wand125_declared_net, check_standing holds C0/C1 superseded entries to the reported lane (T-046).
- 5216fdb7c census: sqverify-fast VERIFIED n18 at 416 dirs (168 CPU-s) and n66 at 201 (2167 CPU-s).
In flight: n18 bundle driver full replay (2 workers, started 17:16Z, ETA ~22Z); n66 sample replay of 12 directions via mixed-replay (1 worker); separate review (claude -p) in /home/user/squares-lanes/rev-wand-net.
