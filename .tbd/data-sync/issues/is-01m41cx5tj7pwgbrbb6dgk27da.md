---
type: is
id: is-01m41cx5tj7pwgbrbb6dgk27da
title: Measure whether the atlas's SVG renderings should be committed or drawn at the Pages build
kind: task
status: in_progress
priority: 3
version: 2
labels:
  - session-169
dependencies: []
parent_id: is-01m41cx3q2pckpmsmmwq1rsngz
created_at: 2026-10-03T17:27:36.018Z
updated_at: 2026-10-03T17:29:57.122Z
---
The house atlas commits 324 SVG renderings (52 MB, packing/atlas/known-best/rendering/) and PR 305 adds 51 regularized ones (11 MB). Measure: what reads them (render_overview, the tiles' packing_svg reduction, check_frontend, the Pages partial checkout), how long drawing all of them takes on a hosted runner, what they add to a clone and to the repository's packs, and what a build-time render would cost the Pages critical path (OR-14) and its determinism checks. Recommend keep or change, with the evidence; the change itself is the owner's decision.
