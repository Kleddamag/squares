---
type: is
id: is-01m45f2cc9keebdd7yjqd81wtg
title: "PR #355 B1 (Medium): name archive/guzhou-review-a-333 in the X048-session-170 README as the home of the cited provenance commits"
kind: task
status: in_progress
priority: 1
version: 2
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m45f2ak71t5b3h9evk65mwjt
hold: null
hold_until: null
created_at: 2026-10-05T07:22:21.449Z
updated_at: 2026-10-06T08:09:49.898Z
started_at: 2026-10-06T08:09:49.898Z
---
Review B finding B1 on jlevy/squares#355 (https://github.com/jlevy/squares/pull/355#pullrequestreview-5411026555), at head 018ee13c5. The records and receipts cite 10 commits not in this history: three resolve at refs/pull/325/head; seven (1a7f2ad99, 4ffb5729a, 526a6c3a3, 58af8cded, ee7e0161b, ef8c42547, f0b94b047) resolved only from branch guzhou/review-a-backup-333. Done: tag archive/guzhou-review-a-333 -> 9a1143ab9 now preserves them (all seven verified ancestors of the tag on 2026-10-05). Remaining: the README line in X048-session-170 saying where the cited commits resolve (refs/pull/325/head and the tag), being added by the cascade lane. Close when that commit is on the layer head.
