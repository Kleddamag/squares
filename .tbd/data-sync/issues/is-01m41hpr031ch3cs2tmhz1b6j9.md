---
type: is
id: is-01m41hpr031ch3cs2tmhz1b6j9
title: Decide how PR 307's 115.5 MB of X048 certificate dumps are stored before it merges
kind: task
status: open
priority: 1
version: 5
labels:
  - session-169
  - owner-decision
dependencies: []
parent_id: null
created_at: 2026-10-03T18:51:28.130Z
updated_at: 2026-10-04T02:41:09.009Z
---
Lane D (think-nkp0) measured PR 307 (busy-goldberg-rouoli) carrying 115.5 MB of X048 pilot certificate dumps (.json.gz node files up to 26 MB each) unique over main. Merged as is, every main clone and every full-history CI job carries them permanently, and the repository passes about 1 GB. Options: a release asset or data repository pinned by digest, keep only summaries in git, or at least xz (28-38% smaller than gzip on the largest archives). GitHub storage holds the PR ref's objects either way. Owner decision; whatever reads the dumps needs a fetch path.

## Notes

2026-10-04 01:05 UTC: moved out from under think-gmef to the top level. think-gmef was closed at 00:37 UTC with this bead open, and an open bead under a closed parent fails check_bead_tree (D-025's first invariant) in every pull request's validate job (jlevy/squares#315 at 6c5036895). Kept open as the owner decision it is; re-parent it wherever it belongs.
2026-10-04 02:50 UTC OWNER DECISION (asked by the import coordinator, session_01HbQD6XX8UwXyhUcQ7fCG46): move the dumps out of git. Publish them as a GitHub release asset pinned by SHA-256, keep summaries and digests in git, and give readers a fetch path. Main's history must not gain the dump blobs, so a later deleting commit is not enough. The owning session (session_014BFGxtvY6cuiHB7LR4LvPj) chooses how, keeping the record's SHA references valid. #307 merges after that; #283, whose commit is in #307's history, lands with it.
