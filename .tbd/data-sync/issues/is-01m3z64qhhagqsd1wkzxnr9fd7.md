---
type: is
id: is-01m3z64qhhagqsd1wkzxnr9fd7
title: "H-264 per-state exclusion pilot: 17-owner kernel on residue states (lane K2)"
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-02T20:50:54.641Z
updated_at: 2026-10-02T22:46:26.878Z
---
Session 168. Two residue states (F1 distance 6, N1 distance 4) ran as 17-cell patterns through the kernel at 32 bins: both certified stalls at the 45-minute cap after rounds 3-4 (receipts h-F1.json, h-N1.json in the session scratchpad, not committed). A 2-hour N1 run is in flight. Falsifier: fewer than half of 10-20 sampled orbits close within 2 CPU-hours each. Next: commit the receipts to X048-session-168-pilots, decide H-264, and feed the cost-reduction lanes.

## Notes

2026-10-02 22:50 UTC. N1 (distance 4) CLOSED whole: PASS_CERTIFIED_CLOSED in 3,723 s, 82 steps, 2,624 rows (2-hour ceiling). First per-state exclusion of a residue state. Receipts in packing/campaign/explorations/X048-session-168-pilots/handoff/k2/ (h-sample, h-F1 and h-N1 stalls at the 45-minute cap, h-N1-2h). Seed and node committed in X048-session-168-pilots/certificates/N1-state-pending/ (83783ab29), not admitted. K2 resumed at 22:45: (1) --check-saved plus verify_n17_kernel_certificate on N1; (2) rank 1 of the F1 plan, the octagon core and a W7 re-run at 32 and 16 rows; (3) N1 at the smaller size to set the per-state unit cost. The H-264 sample of 10 to 20 orbits waits on (3).
