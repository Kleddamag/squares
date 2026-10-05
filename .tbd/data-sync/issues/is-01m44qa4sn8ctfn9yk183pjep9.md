---
type: is
id: is-01m44qa4sn8ctfn9yk183pjep9
title: "PR #336 A1 (Medium): no gate exercises the native path."
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
created_at: 2026-10-05T00:27:10.005Z
updated_at: 2026-10-05T02:30:53.819Z
started_at: 2026-10-05T02:30:53.819Z
---
https://github.com/jlevy/squares/pull/336#pullrequestreview-5408660754

**A1 (Medium): no gate exercises the native path.**
- All the FFI and Job-object lifecycle code (`devtools/supervise_windows.py`, about 821 lines of ctypes) is covered only by 3 Windows-only tests, which skip on Linux (`tests/test_supervise_windows.py:136`).
- The acceptance evidence is the author's local receipts. This conflicts with OR-13.
- **Fix:** add a small `windows-latest` CI job for the 3 native tests (about 3 s), or state explicitly that native acceptance is not gated.

Authorized maintenance only. Disposition requires evidence and exact-head CI; no research follow-up reserved.
