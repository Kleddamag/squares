---
type: is
id: is-01m44qa72ggesrxb8pvkxfk71h
title: "PR #336 A4 (Low): reporting and private APIs."
kind: task
status: in_progress
priority: 2
version: 2
delegate: graph_gate
labels: []
dependencies: []
parent_id: is-01m44qa2mz6hseqc8b10neq6b3
hold: null
hold_until: null
created_at: 2026-10-05T00:27:12.335Z
updated_at: 2026-10-05T02:30:55.898Z
started_at: 2026-10-05T02:30:55.897Z
---
https://github.com/jlevy/squares/pull/336#pullrequestreview-5408660754

**A4 (Low): reporting and private APIs.**
- Line 647: a root that exits 0 reports `success` even when live descendants are killed at cleanup. Only `active_processes_before_cleanup` records it.
- `process_handle` (line 43) reads CPython's private `Popen._handle`.
- Resume uses the undocumented `NtResumeProcess`.
- All acceptable, but say so in the docs.

Authorized maintenance only. Disposition requires evidence and exact-head CI; no research follow-up reserved.
