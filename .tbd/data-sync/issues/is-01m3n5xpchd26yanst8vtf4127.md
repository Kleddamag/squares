---
type: is
id: is-01m3n5xpchd26yanst8vtf4127
title: Reconcile wand125's n <= 100 lower-bound table against the register, row by row, with a devtools check
kind: task
status: open
priority: 2
version: 1
labels:
  - packing
  - wand125-update
  - documentation
dependencies: []
parent_id: is-01m3n5wh72rsqd2z97m8v1vv4q
created_at: 2026-09-28T23:34:39.761Z
updated_at: 2026-09-28T23:34:39.761Z
---
Build (OR-1) a reader for the retained byte capture packing/resources/web/wand125-x-update-2026-09-28/acquisition/lower-bound-table-2026-09-28.html (SHA-256 in the .sha256 beside it) that lists every row whose value, exact form, attribution or best-packing figure disagrees with packing/frontier/n-*.md, separating reported from verified and flagging rows the page marks as inherited from smaller n. Dispose each disagreement: an intake bead, a register correction, or a note that the table is ahead or behind. The page states its data came from this repository at db3f5f3 (2026-09-25) plus wand125's 26 September certificates, but its rows are later (n = 21 and 45 exact, n = 50 at 37/5).
