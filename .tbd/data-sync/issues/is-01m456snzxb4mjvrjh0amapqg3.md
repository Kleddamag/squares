---
type: is
id: is-01m456snzxb4mjvrjh0amapqg3
title: Rebuild Guzhou's n17 stack (PRs 325, 333, 351, 352) onto PR 347 without PR 307's dumps and certify it
kind: task
status: in_progress
priority: 1
version: 6
assignee: claude
delegate: claude-code@vm
labels: []
dependencies: []
child_order_hints:
  - is-01m45f1jvr8mq9q7q1ajveh3g7
  - is-01m45f2ak71t5b3h9evk65mwjt
  - is-01m45f376m2jqsm1t29jteg8q8
  - is-01m45f3gxdbms4wekyer6s1j9e
hold: null
hold_until: null
created_at: 2026-10-05T04:57:47.773Z
updated_at: 2026-10-05T07:22:58.861Z
started_at: 2026-10-05T04:58:02.944Z
---
PR 307 was closed and rebuilt as PR 347 without its 112.5 MB of certificate dumps (OR-18). PRs 325, 333, 351 and 352 sit on PR 307's history, so merging any of them would bring the dumps into main. Rebuild each as a claude/ branch by cherry-picking Guzhou's commits (authorship preserved) onto PR 347, re-render the records, verify Guzhou's Review A fixes and finish what is left, open the replacements as a formal stack, drive CI green, then comment on and close the originals as authorized. The rebuilt sessions stay certification_pending on this bead until a hosted fast gate passes on the rebuilt history.
