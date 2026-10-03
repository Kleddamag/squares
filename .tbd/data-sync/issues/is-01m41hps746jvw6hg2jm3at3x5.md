---
type: is
id: is-01m41hps746jvw6hg2jm3at3x5
title: Delete imported replay and transfer branches after checking the beads that cite their commits
kind: task
status: open
priority: 2
version: 1
labels:
  - session-169
  - owner-decision
dependencies: []
parent_id: is-01m41cx3q2pckpmsmmwq1rsngz
created_at: 2026-10-03T18:51:29.380Z
updated_at: 2026-10-03T18:51:29.380Z
---
Lane D measured 76 session and replay branches without a PR holding 60.6 MB unique (mostly transfer/), which every default clone and full-history CI job fetches. Beads cite 26 of their commits (20 on claude/optimistic-gauss-uzmcl2; one each on four replay branches, result-import-process and nice-fermi-v8fhi2), so those citations need re-pointing or the branches keeping. Deleting remote branches is irreversible from a clone's point of view; owner decision. GitHub storage drops only after GitHub's own maintenance.
