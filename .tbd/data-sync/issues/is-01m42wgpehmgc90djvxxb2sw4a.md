---
type: is
id: is-01m42wgpehmgc90djvxxb2sw4a
title: "Import wand125: 14+ mixed certificates (#282)"
kind: task
status: in_progress
priority: 1
version: 5
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m41csdc2gp36ry5p6n7c2x2y
hold: null
hold_until: null
created_at: 2026-10-04T07:19:38.704Z
updated_at: 2026-10-05T01:53:55.471Z
started_at: 2026-10-04T07:32:04.027Z
---
Mixed rectangle-measure certificates posted on jlevy/squares#282 from 2026-10-03 19:33Z (14 at upstream 3554616; two more at 6832.. and 8aa6.. after 07:00Z). Stages 1-2 on branch import-282-mixed14 (packet wand125-mixed-bounds-2026-10-04, W7 audit binding by pinned digest). Stage 3 (new T-NNN) waits for jlevy/squares#305. Replays (~124 CPU-h for 14) held with think-wpuu. Separate import needed: c56b9b7 (T-066 F1/F2, #280).

## Notes

2026-10-05: #305 merged 2026-10-04T23:00Z, so stage 3 is unblocked; taken by the follow-up epic think-05m9 (wand125 lane, T-090).
