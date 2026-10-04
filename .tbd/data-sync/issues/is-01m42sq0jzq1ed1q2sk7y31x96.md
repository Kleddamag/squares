---
type: is
id: is-01m42sq0jzq1ed1q2sk7y31x96
title: "#305: merge main (#334), re-pin DATA_REVISION if needed, hosted CI green"
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@vm
labels: []
dependencies:
  - type: blocks
    target: is-01m42sq1hwn811q3t0jfz4dcsj
parent_id: is-01m42sq026mszrdm4fwf5r8g8y
hold: null
hold_until: null
created_at: 2026-10-04T06:30:39.967Z
updated_at: 2026-10-04T06:31:03.851Z
started_at: 2026-10-04T06:31:03.851Z
---
main moved past #305's last green head 498258a9f with #334 (pages/site-head contract, render_case_pages, render_overview, test_overview, test_case_pages). Textual merge is clean; prove the semantic merge: local --records/--edit plus the touched tests, then hosted CI green on the merge head.
