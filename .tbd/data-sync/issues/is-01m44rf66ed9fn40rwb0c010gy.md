---
type: is
id: is-01m44rf66ed9fn40rwb0c010gy
title: "On-request intake pass: one entry point (make intake) and a runbook section, Running an Intake Pass, an agent follows when the owner says 'run the intake'"
kind: task
status: in_progress
priority: 2
version: 6
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
hold: null
hold_until: null
created_at: 2026-10-05T00:47:23.854Z
updated_at: 2026-10-05T01:31:31.365Z
started_at: 2026-10-05T00:49:42.865Z
---
Owner request 2026-10-05, revised the same day: no schedule (no cron, no weekly cadence in code or docs). The whole sweep-and-import pass is invoked on request: make intake runs devtools.intake_sweep, and packing/campaign/result-import.md's Running an Intake Pass gives the exact steps and a self-contained agent prompt. Network the pass needs: github.com, kingbird.myphotos.cc, evand.github.io, pypi.org.

## Notes

2026-10-05: owner revised the request the same day: no schedule. Delivered as make intake plus result-import.md, Running an Intake Pass, with the self-contained prompt under The Prompt (935a42c2f).
