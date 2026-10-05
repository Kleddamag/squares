---
type: is
id: is-01m44qa1wd6047vfr7fvm0dr8p
title: "PR #333 A9 (Low): lifetime peak RSS."
kind: task
status: in_progress
priority: 2
version: 2
delegate: graph_gate
labels: []
dependencies: []
parent_id: is-01m44q9st2e0jh0h0cztp6hnv8
hold: null
hold_until: null
created_at: 2026-10-05T00:27:07.021Z
updated_at: 2026-10-05T00:54:30.348Z
started_at: 2026-10-05T00:54:30.348Z
---
https://github.com/jlevy/squares/pull/333#pullrequestreview-5408660716

**A9 (Low): lifetime peak RSS.**
- `remaining()` uses lifetime peak RSS, so it refuses forever in any process that ever went over 512 MiB.
- The tests stub it, so this is a reuse hazard, not a CI flake.

Authorized maintenance only. Disposition requires evidence and exact-head CI; no research follow-up reserved.
