---
type: is
id: is-01m3qj2s8fb8ewx3h334rtqqjf
title: Expose child pytest timings and live worker progress for reachable validation
kind: task
status: in_progress
priority: 1
version: 2
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
labels: []
dependencies: []
parent_id: is-01m3p5wj25knm7rbx0g4a4tpvg
created_at: 2026-09-29T21:45:38.317Z
updated_at: 2026-09-29T21:46:18.520Z
---
The reachable-test wrapper prevents the gate from injecting direct-pytest JUnit and duration receipts. A ten-worker broad run can stall near completion with one CPU-active worker, without enough evidence to distinguish an indivisible test from queued imbalance. Preserve exact selection, markers and assertions. Add maintained child-pytest durations/JUnit plus live start/finish receipts naming run, worker, node and source, with interrupted partial states and focused regression tests. Do not claim that changing xdist scheduling helps until matched workload evidence exists.

## Notes

Sol implementation and independent Sol review are running in the isolated validation-parity checkout while primary candidate 1afb75ca6 finishes its unchanged broad push. Retained Session 152 logs identify a 1327.87-second single atlas-composite test as one possible source of an indivisible tail; current quiet output cannot prove the active node. Keep scheduling unchanged until the new receipts support a diagnosis.
