---
type: is
id: is-01m3yrf5bp4ngk5a0a4tprhz2r
title: "T-046 leftovers: replay the 28 September rectangle certificates n = 51, 57, 58, 72, 73, 91 (n = 37 only if T-069's n37 fails)"
kind: task
status: open
priority: 2
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m3yrdxte02c7bnygkke34ct4
created_at: 2026-10-02T16:51:56.405Z
updated_at: 2026-10-02T16:51:56.405Z
---
Dispatched to runners r1 (n72 workers 3, n91) and r2 (n73 workers 2, n51, n57+n58); transfer dirs wand125-rect-sept28-r1-*/-r2-* on branches claude/replay-wand125-rect-oct1-r1/-r2. Merge with audit_wand125_rectangles --packet 2026-09-28 --merge, then records. About 24 CPU-h.
