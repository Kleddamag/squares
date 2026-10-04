---
type: is
id: is-01m41cpevn6nbaataejd13t6bk
title: "Register: backfill superseded_by on every result of another kind that a later result implies"
kind: task
status: open
priority: 2
version: 6
labels: []
dependencies: []
parent_id: is-01m41amwkn2j6r6jh6de7as7fb
created_at: 2026-10-03T17:23:55.892Z
updated_at: 2026-10-04T01:03:49.374Z
---
Owner, 2026-10-03: did we backfill all the superseding relationships? Bounds are derived and complete (26). Of the results whose kind is no bound, only T-036 declares one. Audit each (rigidity, case exclusion, restricted optimality, method limit, correction, audit, simplification) against later results; T-023 and T-031 exclude packings at side 96/25 < T, which T-060 implies whole.

## Notes

State 2026-10-04 00:55 UTC: in jlevy/squares#315 at 6c5036895, merged with main at d303e9ef8 and re-pinned; hosted CI running on the head (green at 03833707a); local push gate passes but for the two sandbox-only tests. Reviewed by a strong-tier agent (think-rf21). Closes when #315 merges.
