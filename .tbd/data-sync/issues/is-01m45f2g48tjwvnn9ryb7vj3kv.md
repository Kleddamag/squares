---
type: is
id: is-01m45f2g48tjwvnn9ryb7vj3kv
title: "PR #355 B4 (Low): 'independently replayed' describes a same-implementation replay (Session 172)"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m45f2ak71t5b3h9evk65mwjt
created_at: 2026-10-05T07:22:25.287Z
updated_at: 2026-10-05T07:22:25.287Z
---
Review B finding B4 on jlevy/squares#355 (https://github.com/jlevy/squares/pull/355#pullrequestreview-5411026555), at head 018ee13c5. Examples: 'independently replayed complete six-owner selections' (X048-session-172-capacity-support/README.md:3) and the *-independent-replay.json receipts. These are fresh, search-free replays that use the same predicate code; in this repository's evidential vocabulary 'independent' means a separate implementation. Fix: 'freshly replayed (same implementation, no search)', or state what the replay shares with the producer. Same finding on #356 (B3) and #360 (B3).
