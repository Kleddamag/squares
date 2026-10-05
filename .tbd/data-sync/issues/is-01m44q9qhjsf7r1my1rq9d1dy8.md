---
type: is
id: is-01m44q9qhjsf7r1my1rq9d1dy8
title: "PR #325 A4 (Low): frame introspection with no test."
kind: task
status: in_progress
priority: 2
version: 2
delegate: graph_gate
labels: []
dependencies: []
parent_id: is-01m44q74w8x5z0b69hev8yr4d7
hold: null
hold_until: null
created_at: 2026-10-05T00:26:56.434Z
updated_at: 2026-10-05T00:27:47.063Z
started_at: 2026-10-05T00:27:47.063Z
---
https://github.com/jlevy/squares/pull/325#pullrequestreview-5408660666

**A4 (Low): frame introspection with no test.**
- `profile_n17_partner_memo.py:74-75` reads the producer's locals `memo` and `rows` through frame introspection. Renaming either local breaks the tool with a KeyError, and no test covers it.
- **Fix:** add a smoke test on W7 (about 2 s).

Authorized maintenance only. Disposition requires evidence and exact-head CI; no research follow-up reserved.
