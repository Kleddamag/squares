---
type: is
id: is-01m41cpevn6nbaataejd13t6bk
title: "Register: backfill superseded_by on every result of another kind that a later result implies"
kind: task
status: open
priority: 2
version: 7
labels: []
dependencies: []
parent_id: is-01m41amwkn2j6r6jh6de7as7fb
created_at: 2026-10-03T17:23:55.892Z
updated_at: 2026-10-04T02:18:41.759Z
---
Owner, 2026-10-03: did we backfill all the superseding relationships? Bounds are derived and complete (26). Of the results whose kind is no bound, only T-036 declares one. Audit each (rigidity, case exclusion, restricted optimality, method limit, correction, audit, simplification) against later results; T-023 and T-031 exclude packings at side 96/25 < T, which T-060 implies whole.

## Notes

State 2026-10-04 02:20 UTC: jlevy/squares#315 at 833a5117f is ready to merge: 29 checks pass, 28 skipped by design; mergeable and clean, and merges cleanly into main at fa5133b49. Reviewed (think-rf21) and its fixes checked (think-wizo). Waiting on the owner's merge.
