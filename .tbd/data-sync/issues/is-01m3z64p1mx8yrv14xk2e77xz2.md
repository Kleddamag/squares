---
type: is
id: is-01m3z64p1mx8yrv14xk2e77xz2
title: "Capture pilot 2: lift the live-row cap per the capture-after-pilot review (lane C1)"
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-02T20:50:53.101Z
updated_at: 2026-10-02T22:46:27.313Z
---
Session 168. Pilot 1 (cea300a4) met the capture falsifier (position g=1.000), but review-2026-10-02-n17-capture-after-pilot.md (3f90fc2d) finds it producer-limited by the 24 live-row cap. Pilot 2: max-live 128/256, all live rows bisected to 2^-22, end-angle core, hull cap 48, per-side bounds, widest-row/extent ratio, n11 case-438 contraction control. Falsifier: 3 rounds with widest row < 1/20 of extent and no two-sided extent falling 10%. In-flight uncommitted edits to packing/devtools/pilot_n17_capture.py and its test; runs and receipts in the session scratchpad lanes/c1/p2. Next: integrate receipts into X048-session-168-pilots, record per-round g, decide the capture route.

## Notes

2026-10-02 22:50 UTC. The unfinished rework is packing/campaign/explorations/X048-session-168-pilots/handoff/c1/capture-pilot2-wip.patch (git apply from repo root; clean on 83783ab29). Partial outputs in packing/campaign/explorations/X048-session-168-pilots/handoff/c1/: box1024 at 128 rows reached round 11; the n11 control at 32 rows reached g~0.81 by round 9 (recorded 0.84). C1 resumed at 22:45 on one worker: finish, test, then the n11 control and box1024 at 128 and 256 rows against the review's falsifier.
