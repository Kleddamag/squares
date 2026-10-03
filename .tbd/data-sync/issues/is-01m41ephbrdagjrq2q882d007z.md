---
type: is
id: is-01m41ephbrdagjrq2q882d007z
title: Measure what drives the repository's growth, and what would slow it
kind: task
status: in_progress
priority: 2
version: 2
labels:
  - session-169
dependencies: []
parent_id: is-01m41cx3q2pckpmsmmwq1rsngz
created_at: 2026-10-03T17:58:55.608Z
updated_at: 2026-10-03T17:58:56.438Z
---
Owner concern, 2026-10-03: the repository is growing large (about 912 MB packed). Measured for PR 305: its whole history packs to 6.40 MB over main and a single squashed commit to 5.87 MB, so squashing saves about 0.5 MB and would break session-168's certified gate ancestry and about 30 recorded commit references; the PR's bytes are its content (regularized views 2.9 MB packed, already gzip and no smaller as plain YAML; SVG drawings 1.4 MB). Measure the whole repository: packed bytes by path family over all history and for the current tree, growth by month, the largest single objects, which families redraw or rewrite often, what a default clone, a shallow clone and the Pages sparse checkout transfer; then rank the options by bytes saved and cost: slimmer SVG encoding (each square written twice with 28-digit coordinates), compact layouts, packet storage (devtools.retained_data), moving bulky archives out, a squash-merge policy for data-heavy PRs, partial-clone guidance, and whatever else the numbers show. Read-only; the owner decides.
