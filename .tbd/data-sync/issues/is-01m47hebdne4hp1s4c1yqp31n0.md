---
type: is
id: is-01m47hebdne4hp1s4c1yqp31n0
title: "Import wand125 #366: mixed_n18_L4704 (s(18) >= 588/125, 832-node net) and mixed_n19_L48229 (s(19) >= 48229/10000) at 65e408c"
kind: task
status: in_progress
priority: 1
version: 4
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m47hea1vkqx8h5wzdzcyqs5k
hold: null
hold_until: null
created_at: 2026-10-06T02:42:19.701Z
updated_at: 2026-10-06T05:30:18.042Z
started_at: 2026-10-06T02:45:53.733Z
---

## Notes

2026-10-06 05:35Z, lane R2 handing back to the coordinator (branch claude/ecstatic-pascal-pothtx-r2, HEAD 830a1222d).

T-099 and T-100 at V0/C1: registered, reviewed (6bc2a8ea7, accepted, S3 confirmed), the review's FN-1 to FN-6 fixed (771013dba).
sqverify-fast rows and census controls for both, made with the merged census tool of f342dff82 (blob c4ea4eb5 = f342dff82's 59a98bec plus this packet), committed 9377a2ae9; no rung moved on this branch.
Source-checker controls, samples (10 nodes of each net) committed.
n18 full replay of the bundle's driver still running detached (process group 8378, started 03:28:44Z, 299/832 at 05:19Z); /proc snapshot ASSERTS_ON committed (cd531fb82). Receipts land in the lane scratchpad full-n18-receipts/. Finish: copy run.meta and run.stdout into receipts/n18-L4704/full/, run audit_wand125_declared_net compare, add E-n018-wand125-mixed-4704-source-replay.
Open: think-q9gu (fixed by R1's 36b52538a, close at merge).
