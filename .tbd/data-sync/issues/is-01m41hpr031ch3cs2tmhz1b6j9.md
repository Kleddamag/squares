---
type: is
id: is-01m41hpr031ch3cs2tmhz1b6j9
title: Decide how PR 307's 115.5 MB of X048 certificate dumps are stored before it merges
kind: task
status: open
priority: 1
version: 1
labels:
  - session-169
  - owner-decision
dependencies: []
parent_id: is-01m41cx3q2pckpmsmmwq1rsngz
created_at: 2026-10-03T18:51:28.130Z
updated_at: 2026-10-03T18:51:28.130Z
---
Lane D (think-nkp0) measured PR 307 (busy-goldberg-rouoli) carrying 115.5 MB of X048 pilot certificate dumps (.json.gz node files up to 26 MB each) unique over main. Merged as is, every main clone and every full-history CI job carries them permanently, and the repository passes about 1 GB. Options: a release asset or data repository pinned by digest, keep only summaries in git, or at least xz (28-38% smaller than gzip on the largest archives). GitHub storage holds the PR ref's objects either way. Owner decision; whatever reads the dumps needs a fetch path.
