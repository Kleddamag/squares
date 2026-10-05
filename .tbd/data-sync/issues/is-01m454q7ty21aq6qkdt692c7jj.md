---
type: is
id: is-01m454q7ty21aq6qkdt692c7jj
title: "Stage 4 for T-088 and T-089: exact rational certificates for n = 69, 83, 87, receipts, controls and a separate review"
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
hold: null
hold_until: null
created_at: 2026-10-05T04:21:30.590Z
updated_at: 2026-10-05T04:50:15.076Z
started_at: 2026-10-05T04:23:01.170Z
---

## Notes

2026-10-05 lane stage4, branch claude/ecstatic-pascal-pothtx-stage4 (not pushed). Replay lane committed 0c0559fe1: devtools.catalogue_upper_bounds promotes witnesses/known-best/n-069/083/087 with upper_bound_packets' robust-rational settings (36 digits, <= 1e-9), certificates in witnesses/kingbird-2026/, receipts in resources/web/known-best-packings/receipts/ (kingbird-2026-09-certification.json, -negative-controls.json). Results: n=69 dilation 1+1e-15, certified 8.8271946557297478..., +1.78e-14 over printed, verified 8.82719465572975 (2 units); n=83 dilation 1+1e-13 (1e-15 leaves 1 pair overlapping), 9.6347576486319454..., +8.65e-13, verified 9.63475764863195 (87 units); n=87 dilation 1+1e-13 (13 pairs), 9.8388152699491448..., +8.85e-13, verified 9.83881526994915 (89 units). check --replay: all VERIFIED (regenerated identical, independent checker, exact_verify), ~14 s. Two controls on n=69 (side -1e-15, square 1 +1e-6) refused by both checkers; tests/test_catalogue_upper_bounds.py re-decides them. Review lane: separately prompted tbd-strong (claude -p --agent tbd-strong, claude-opus-5-5, effort xhigh) in detached worktree /home/user/squares-lanes/stage4-review at 0c0559fe1, writing docs/project/reviews/review-2026-10-05-kingbird-intake-n69-n83-n87.md. Exit (records, rungs, renders, atlas, pin) waits on its verdict.
