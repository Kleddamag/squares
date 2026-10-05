---
type: is
id: is-01m44rf2h2wkr59cemx47w986q
title: "A deferred catalogue intake had no owning bead: n = 69, 83, 87 sat five days as pending_catalogue_intake while the frontier called the older sides best known"
kind: bug
status: open
priority: 1
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
created_at: 2026-10-05T00:47:20.098Z
updated_at: 2026-10-05T00:47:20.098Z
---
Root cause (2026-10-05): the 2026-09-30 refresh (a897e4031, 1d4020e9f, b8502282d) correctly held the three September 2026 sides as pending intake, and plan-2026-10-01-result-status.md listed 'Register the three catalogue intakes', but no open bead owned the work (only a closed bead's notes mention it). check_requests --backlog reads only GitHub issues and register entries, and check_source_coverage accepts a pending entry indefinitely, so nothing surfaced it. Fix: every pending_catalogue_intake entry names an open bead and a recorded date, the checker refuses one without it, and the sweep reports pending intakes with their age.
