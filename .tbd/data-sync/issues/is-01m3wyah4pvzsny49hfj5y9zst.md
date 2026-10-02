---
type: is
id: is-01m3wyah4pvzsny49hfj5y9zst
title: "Import wand125: mixed rectangle-measure certificates at n = 37, 65, 66, 90, 92 (#282)"
kind: task
status: in_progress
priority: 2
version: 7
spec_path: docs/project/specs/active/plan-2026-10-01-result-import-first-application.md
labels:
  - packing
  - result-import
dependencies: []
parent_id: is-01m3yrdxte02c7bnygkke34ct4
created_at: 2026-10-01T23:55:47.217Z
updated_at: 2026-10-02T16:53:19.295Z
---
Result import process from stage 1. New lower-bound entry for five counts; T-048 keeps its claim. Tarballs (125 MB) pinned by digest and not retained, as for n = 50. audit_wand125_point_and_mixed is hard-coded to n = 50 and needs a certificate parameter. Complete replay 45 to 90 CPU-h. T-048 own replay sits unmerged on claude/replay-wand125-n50-l740-local (think-nnlg). A rolling request: n = 82 to 85 are announced.

## Notes

2026-10-01: stages 2 and 3 are in draft PR jlevy/squares#292 (branch claude/import-2026-10-01-requests, commit 2b7191461), stacked on #290. Stage 4 not started. The T-id is provisional until #292 is on main; quote it to no author before then.

2026-10-02 (PR #298): audit_wand125_point_and_mixed generalised (mixed-audit/fetch/replay/merge/price), all seven certificates' premises pass; replays of n37,n65,n66,n90,n92 and G's n84,n85 running on cloud runners m1-m3 (branches claude/replay-wand125-mixed-m1..m3), ~66 CPU-h estimated. Review docs/project/reviews/review-2026-10-02-wand125-mixed-rectangle-bounds.md: no blocking defect.
