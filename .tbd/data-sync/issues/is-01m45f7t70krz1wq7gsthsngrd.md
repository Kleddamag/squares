---
type: is
id: is-01m45f7t70krz1wq7gsthsngrd
title: "Import wand125: mixed_n67_L848 (6c0842e) and mixed_n84_L9411 (a541afb) posted on #282 on 5 October"
kind: task
status: in_progress
priority: 2
version: 3
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
hold: null
hold_until: null
created_at: 2026-10-05T07:25:19.455Z
updated_at: 2026-10-05T07:44:28.460Z
started_at: 2026-10-05T07:44:28.460Z
---
Two certificates posted on jlevy/squares#282 after T-090 (8aa6a10) and T-091 (797bdf6) were packeted, with no owning bead until now (found by the stack-357 bead bookkeeper on 2026-10-05): s(67) >= 212/25 = 8.48 (mixed_n67_L848, wand125/square-packing-bounds 6c0842e, comment 2026-10-05T06:06:49Z; supersedes their mixed_n67_L8475 = 8.475 of 2475d08) and s(84) >= 9411/1000 = 9.411 (mixed_n84_L9411, a541afb, 2026-10-05T06:07:23Z; supersedes mixed_n84_L94075 = 9.4075 of c9c6be0). Same kind and verifier as mixed_n84_L940; the source reports a full 201-angle replay from the bundle on a fresh Ubuntu 24.04 machine. Run the import runbook stages 1-3 (claim map against the record, packet at the later pin, register or extend a T-NNN at V0), queue the stage-4 replay with the others, and fold the acknowledgement into think-7gop / think-aygi. The superseded mixed_n67_L8475 (2475d08) and mixed_n84_L94075 (c9c6be0) fall in the 14 posts from b321ac9 to 3554616 that T-090 covers (think-e6ss), so these two raise T-090 entries at n = 67 and 84 rather than open new counts.
