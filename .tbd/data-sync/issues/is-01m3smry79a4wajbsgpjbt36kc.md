---
type: is
id: is-01m3smry79a4wajbsgpjbt36kc
title: Make complete n11 case-2095 regression respect the bounded test worker budget
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3sken298psm0jfn7tmbcqp9
created_at: 2026-09-30T17:11:10.312Z
updated_at: 2026-09-30T17:21:46.339Z
---
Deferred checkpoint36746969192 at6a307f6a4: full generic case2095 test returned INCOMPLETE with max_seconds30 and workers3 while running inside the parallel slow lane. Preserve all160 rows, five complete steps, source binding and no-partial-credit assertions; diagnose scheduling and existing reviewed efficient options before changing a finite deadline. Only tests may change; accepted checker/source and proof receipts remain fixed. Sol repairs, Astra reviews; use one targeted execution and keep the expiration refusal control.

## Notes

Fixed in ebbfec10e, test-only. Same pinned 2095 source/seed/audit now replays with the already-reviewed shared sequential exact checker, one worker, finite 60-second clock, all five steps and 160 rows plus empty pending inventory and written-receipt equality. Positive and real deadline/source-tamper controls: 3 passed in 34.48 seconds (positive 34.15 seconds). Ruff/BasedPyright clean. Astra max approved test SHA d651f66dd8e42f70a7d2006edf7c55b7f64a845435f71aabd86d5eddfb45af77. Accepted production checkers and receipts unchanged. Await publication/current-head normal CI.
