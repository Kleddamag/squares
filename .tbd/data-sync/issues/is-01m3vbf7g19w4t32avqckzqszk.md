---
type: is
id: is-01m3vbf7g19w4t32avqckzqszk
title: Replay evand finite family premise and reconcile the conditional Lean reduction
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-01-post-optimality-w3-session.md
labels: []
dependencies: []
parent_id: is-01m3v9vq36ykk2jdzce75req44
created_at: 2026-10-01T09:07:03.806Z
updated_at: 2026-10-02T08:03:30.353Z
---
Oct1 source pin 08e8a5f reports s(k^2-3)=k for every k>=6. Register source assertions separately from acceptance. Acquire missing finite-cover inputs, audit exact zero-tilt and positive-tilt/area bounds, complete pose/root coverage and record-to-Lean mapping; replay Valid7 with a selected bounded gate or independent implementation. Lean reduction alone does not discharge Valid7. Scope and next commands in review-2026-10-01-evand-mathematical-transfer.md. Do not schedule the 81000 CPU-second source sweep blindly.

## Notes

2026-10-02: a second, independently written exact checker for Valid7 (wand125/valid7-independent-check, #296) is retained in packing/resources/web/wand125-valid7-independent-check-2026-10-02/; its verify.sh (record check, 2,300 sampled leaves, three mutants) passes here, records-v1 pinned by digest. Remaining for T-064: a full replay of one Valid7 checker, a review of the independent checker's method, and the Lean reduction's build with its axiom receipt.
