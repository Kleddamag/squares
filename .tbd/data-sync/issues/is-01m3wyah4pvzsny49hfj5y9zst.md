---
type: is
id: is-01m3wyah4pvzsny49hfj5y9zst
title: "Import wand125: mixed rectangle-measure certificates at n = 37, 65, 66, 90, 92 (#282)"
kind: task
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-10-01-result-import-first-application.md
labels:
  - packing
  - result-import
dependencies: []
parent_id: is-01m3wvgebtkjqb3km59h7768zx
created_at: 2026-10-01T23:55:47.217Z
updated_at: 2026-10-02T00:17:34.962Z
---
Result import process from stage 1. New lower-bound entry for five counts; T-048 keeps its claim. Tarballs (125 MB) pinned by digest and not retained, as for n = 50. audit_wand125_point_and_mixed is hard-coded to n = 50 and needs a certificate parameter. Complete replay 45 to 90 CPU-h. T-048 own replay sits unmerged on claude/replay-wand125-n50-l740-local (think-nnlg). A rolling request: n = 82 to 85 are announced.

## Notes

2026-10-01: W1 research-survey, correctness focus. Objective: stages 2 and 3 of the result import process (retain, record as reported). Artifact: a pull request stacked on jlevy/squares#290, branch claude/import-2026-10-01-requests. Check: validate_schemas, check_source_coverage, check_results, packing-validate --records.
