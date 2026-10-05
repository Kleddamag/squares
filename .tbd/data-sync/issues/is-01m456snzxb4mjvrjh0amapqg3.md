---
type: is
id: is-01m456snzxb4mjvrjh0amapqg3
title: Rebuild Guzhou's n17 stack (PRs 325, 333, 351, 352) onto PR 347 without PR 307's dumps and certify it
kind: task
status: open
priority: 1
version: 1
assignee: claude
labels: []
dependencies: []
created_at: 2026-10-05T04:57:47.773Z
updated_at: 2026-10-05T04:57:47.773Z
---
PR 307 was closed and rebuilt as PR 347 without its 112.5 MB of certificate dumps (OR-18). PRs 325, 333, 351 and 352 sit on PR 307's history, so merging any of them would bring the dumps into main. Rebuild each as a claude/ branch by cherry-picking Guzhou's commits (authorship preserved) onto PR 347, re-render the records, verify Guzhou's Review A fixes and finish what is left, open the replacements as a formal stack, drive CI green, then comment on and close the originals as authorized. The rebuilt sessions stay certification_pending on this bead until a hosted fast gate passes on the rebuilt history.
