---
type: is
id: is-01m41hprm9fep7d20thmgfhyd0
title: "Set a policy for bulk retained data: report bytes per PR, move files of 1 MB or more out of git, use xz"
kind: task
status: open
priority: 2
version: 4
labels:
  - session-169
  - owner-decision
dependencies: []
parent_id: null
created_at: 2026-10-03T18:51:28.776Z
updated_at: 2026-10-04T01:09:57.394Z
---
Lane D measured 250 MB of the 389 MB added across refs in the week to 3 Oct as gzip certificates, receipts and transfer shards. Proposal: CI reports the packed bytes a PR adds; files of 1 MB or more go to release assets, a data repository or LFS with their digest recorded; new archives use xz. Trade-offs: offline clones lose the data, readers need a fetch, it runs against the self-contained-repository convention, LFS adds quota and CI bandwidth. Owner decision; relates to devtools.retained_data and plan-2026-10-01-release-assets-on-demand.md.

## Notes

2026-10-04 01:05 UTC: moved out from under think-gmef to the top level. think-gmef was closed at 00:37 UTC with this bead open, and an open bead under a closed parent fails check_bead_tree (D-025's first invariant) in every pull request's validate job (jlevy/squares#315 at 6c5036895). Kept open as the owner decision it is; re-parent it wherever it belongs.
