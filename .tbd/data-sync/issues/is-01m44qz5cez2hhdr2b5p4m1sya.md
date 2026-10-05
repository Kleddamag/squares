---
type: is
id: is-01m44qz5cez2hhdr2b5p4m1sya
title: "Draft and post the replies on #282 and #281 after the follow-up PR merges (stage 7)"
kind: task
status: open
priority: 2
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
created_at: 2026-10-05T00:38:38.734Z
updated_at: 2026-10-05T07:51:17.373Z
---
check_requests --report / --draft from main after the merge.

## Notes

2026-10-05 (intake pass think-i5qd): the four blocks dependencies are removed; think-s1xt, think-07s1, think-8i66 and think-plrl are closed and the follow-up PR (#359) merged at b9a55a51d. What is left: #281 has no reply due (check_requests), and #282's next reply (think-7gop's) should report T-094, which the intake pass on claude/ecstatic-pascal-pothtx-intake3 registers, so it is rendered with check_requests --draft 282 from main once that pass merges, and posted only on the owner's word. Replace think-i5qd below with the pass's pull request (jlevy/squares#N) when it is opened.

blocked_on: think-i5qd
