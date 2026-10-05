---
type: is
id: is-01m44qa0ckae48eky00fss61fr
title: "PR #333 A7 (Low): single-line receipts."
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
created_at: 2026-10-05T00:27:05.490Z
updated_at: 2026-10-05T00:54:30.342Z
started_at: 2026-10-05T00:54:30.342Z
---
https://github.com/jlevy/squares/pull/333#pullrequestreview-5408660716

**A7 (Low): single-line receipts.**
- Receipts are written as single-line JSON up to 356 KB (`profile-packet.json`).
- That is under the 5,000-line threshold now enforced on main, but against its intent.
- **Fix:** write them with `sqpack.retained_json`, which is on main since jlevy/squares#305.

Authorized maintenance only. Disposition requires evidence and exact-head CI; no research follow-up reserved.
