---
type: is
id: is-01m41hjrm7a3vdmbhtbyj9rq71
title: "Import wand125's 22 certificates posted on #282 on 3 October (mixed_n95_L996 … mixed_n69_L8612)"
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
created_at: 2026-10-03T18:49:17.703Z
updated_at: 2026-10-06T07:50:59.174Z
started_at: 2026-10-06T07:50:57.086Z
---
Found by the final-reply lane: check_requests --github lists 22 comments on #282 after 2 Oct 15:16 UTC carrying new mixed rectangle-measure certificates. None is retained, reviewed or registered. Runbook stages 1-3 (retain, preflight, blind review, register at V0), then replay runners as for T-075. Also check whether their Green comparisons use proper upper enclosures (audit finding MX-2/AF-1). #282 stays open for these.

## Notes

2026-10-06 07:50Z lane R4 of think-wyf4 (worktree squares-lanes/r4, branch claude/ecstatic-pascal-pothtx-r4 from ebf232767): owner released the hold under think-3ok2. None of T-082's 22 or T-090's 16 is in the 149-certificate census (census-mixed has none from the 10-03 or 10-04 packets), so all 38 need sqverify-fast rows. Built sqverify-fast at main's reviewed crate source d97758bb (binary 567a0fd5, rustc 1.98.0), the binary of T-099/T-100. Running the census then --control, one certificate at a time, largest verified-bound gain first: T-090's 16 (12 with a gain, n = 93, 57, 51, 86, 75, 72, 69, 42, 44, 43, 56, 95; then n = 84, 67, 88, 94, dominated by T-094 and T-091). 1 thread while process group 8378 runs, then 2.
