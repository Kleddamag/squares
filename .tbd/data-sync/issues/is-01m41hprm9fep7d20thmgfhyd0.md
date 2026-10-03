---
type: is
id: is-01m41hprm9fep7d20thmgfhyd0
title: "Set a policy for bulk retained data: report bytes per PR, move files of 1 MB or more out of git, use xz"
kind: task
status: open
priority: 2
version: 1
labels:
  - session-169
  - owner-decision
dependencies: []
parent_id: is-01m41cx3q2pckpmsmmwq1rsngz
created_at: 2026-10-03T18:51:28.776Z
updated_at: 2026-10-03T18:51:28.776Z
---
Lane D measured 250 MB of the 389 MB added across refs in the week to 3 Oct as gzip certificates, receipts and transfer shards. Proposal: CI reports the packed bytes a PR adds; files of 1 MB or more go to release assets, a data repository or LFS with their digest recorded; new archives use xz. Trade-offs: offline clones lose the data, readers need a fetch, it runs against the self-contained-repository convention, LFS adds quota and CI bandwidth. Owner decision; relates to devtools.retained_data and plan-2026-10-01-release-assets-on-demand.md.
