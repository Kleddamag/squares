---
type: is
id: is-01m44rf2h2wkr59cemx47w986q
title: "A deferred catalogue intake had no owning bead: n = 69, 83, 87 sat five days as pending_catalogue_intake while the frontier called the older sides best known"
kind: bug
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
created_at: 2026-10-05T00:47:20.098Z
updated_at: 2026-10-05T01:31:27.858Z
started_at: 2026-10-05T00:49:40.017Z
---
Root cause (2026-10-05): the 2026-09-30 refresh (a897e4031, 1d4020e9f, b8502282d) correctly held the three September 2026 sides as pending intake, and plan-2026-10-01-result-status.md listed 'Register the three catalogue intakes', but no open bead owned the work (only a closed bead's notes mention it). check_requests --backlog reads only GitHub issues and register entries, and check_source_coverage accepts a pending entry indefinitely, so nothing surfaced it. Fix: every pending_catalogue_intake entry names an open bead and a recorded date, the checker refuses one without it, and the sweep reports pending intakes with their age.

## Notes

2026-10-05, branch claude/ecstatic-pascal-pothtx-process: b8f94a3ec makes pending_catalogue_intake require bead + recorded (schema and check_source_coverage.deferral_errors), deferred-conflict claims require bead, and check_bead_tree fail any deferral whose bead is not live (pending intakes, deferred conflicts, open issues' answer_bead, intake-watch reads with a bead). The three live entries name think-s1xt, recorded 2026-09-30; the Kingbird lane deletes them (merge: take the deletion). 935a42c2f adds the postmortem (docs/project/postmortems/postmortem-2026-10-05-orphaned-catalogue-intake.md) and D-519. Other lists checked: register activity (30-day expiry already), validation backlog (6 of 10 below V3/C3 name no bead; listed by the sweep, not failed), certification_pending (already bead-bound), superseded entries (settled). Leave open for the coordinator's merge.
