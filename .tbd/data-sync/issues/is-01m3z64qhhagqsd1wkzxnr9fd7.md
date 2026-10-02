---
type: is
id: is-01m3z64qhhagqsd1wkzxnr9fd7
title: "H-264 per-state exclusion pilot: 17-owner kernel on residue states (lane K2, in flight)"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-02T20:50:54.641Z
updated_at: 2026-10-02T20:50:54.641Z
---
Session 168. Two residue states (F1 distance 6, N1 distance 4) ran as 17-cell patterns through the kernel at 32 bins: both certified stalls at the 45-minute cap after rounds 3-4 (receipts h-F1.json, h-N1.json in the session scratchpad, not committed). A 2-hour N1 run is in flight. Falsifier: fewer than half of 10-20 sampled orbits close within 2 CPU-hours each. Next: commit the receipts to X048-session-168-pilots, decide H-264, and feed the cost-reduction lanes.
