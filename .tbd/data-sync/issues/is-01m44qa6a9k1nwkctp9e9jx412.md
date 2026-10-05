---
type: is
id: is-01m44qa6a9k1nwkctp9e9jx412
title: "PR #336 A3 (Low): the author's machine policy is hard-coded."
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m44qa2mz6hseqc8b10neq6b3
created_at: 2026-10-05T00:27:11.560Z
updated_at: 2026-10-05T00:27:11.560Z
---
https://github.com/jlevy/squares/pull/336#pullrequestreview-5408660754

**A3 (Low): the author's machine policy is hard-coded.**
- `supervise_windows.py:794` refuses whenever `--min-available-gib` is below 8 and only allows tightening, so a host with under 8 GiB free can never use the tool.
- The review threshold (default 12, line 763) always fires before the stop threshold (default 16, line 757), so the 16 GiB stop is unreachable by default.

Authorized maintenance only. Disposition requires evidence and exact-head CI; no research follow-up reserved.
