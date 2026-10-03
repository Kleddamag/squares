---
type: is
id: is-01m41hjrm7a3vdmbhtbyj9rq71
title: "Import wand125's 22 certificates posted on #282 on 3 October (mixed_n95_L996 … mixed_n69_L8612)"
kind: task
status: open
priority: 1
version: 3
labels:
  - result-import
dependencies: []
parent_id: is-01m41csdc2gp36ry5p6n7c2x2y
created_at: 2026-10-03T18:49:17.703Z
updated_at: 2026-10-03T22:47:13.177Z
---
Found by the final-reply lane: check_requests --github lists 22 comments on #282 after 2 Oct 15:16 UTC carrying new mixed rectangle-measure certificates. None is retained, reviewed or registered. Runbook stages 1-3 (retain, preflight, blind review, register at V0), then replay runners as for T-075. Also check whether their Green comparisons use proper upper enclosures (audit finding MX-2/AF-1). #282 stays open for these.

## Notes

2026-10-03 20:50 IM282b done: claude/import-282-oct3 @bce32635b, PR #324. T-082 at V0/C1 (S3 proposed), 22 counts n = 51..96, packet wand125-mixed-bounds-2026-10-03 at 2aff2076, all 22 pass exact audit and pre-replay checks; blind review accepted (OC-1 improvement_lower at n = 88, 93 not lower bounds; OC-2 six uncertified comparison values; OC-3 exit 0 on ANGLE_UNRESOLVED; OC-4 corrects MV-2; OC-5 README). Replay plan: 8 runners x 4 workers, ~162 CPU-h (budget 165-225), ranges in the packet README. Runners HELD pending the owner's answer on load (weekly limit warning). Findings to post on #282 once merged.2026-10-03 22:55 PR #324 merged into main at 4949d1439: T-082 at V0/C1, S3 (stages 1-3, blind review accepted, OC-1..OC-5). Findings OC-1/OC-2 posted to @wand125 on #282 (issuecomment-5974294911). Remaining: the 8 replay runners (about 162 CPU-h; held until after the 7 Oct usage reset per owner), mixed-merge per certificate, then a replayed entry moving each count to V3/C3.
