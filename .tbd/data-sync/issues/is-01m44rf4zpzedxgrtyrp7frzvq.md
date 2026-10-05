---
type: is
id: is-01m44rf4zpzedxgrtyrp7frzvq
title: "devtools.intake_sweep: one command that lists every unimported input across sources"
kind: task
status: in_progress
priority: 1
version: 4
delegate: claude-code@vm
labels:
  - result-import
dependencies:
  - type: blocks
    target: is-01m44rf66ed9fn40rwb0c010gy
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
hold: null
hold_until: null
created_at: 2026-10-05T00:47:22.613Z
updated_at: 2026-10-05T01:31:29.022Z
started_at: 2026-10-05T00:49:41.998Z
---
Combine check_requests --github (unread issues/comments), watched repositories whose head is past their newest retained packet pin, the Kingbird recapture diff (diff_kingbird_catalogue) when a new capture exists, pending_catalogue_intake entries with age and owning bead, queued asks; markdown report + nonzero exit when an item lacks a bead.

## Notes

2026-10-05: 57b05f65f adds devtools/intake_sweep.py (+ tests/test_intake_sweep.py), devtools/capture_kingbird_catalogue.py, campaign/intake-watch.yaml (IntakeWatch/v1), check_requests.backlog_rows and page-by-number gh_fetch (gh --paginate failed through the session proxy), and make intake. Full sweep 13 s on this worktree; first run: 24 items without an owner (15 unread comments on #282/#281, 9 watched repositories past their pins), 7 owned, Kingbird and UnitSquare not checked (kingbird.myphotos.cc denied).
