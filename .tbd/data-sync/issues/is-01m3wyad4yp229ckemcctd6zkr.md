---
type: is
id: is-01m3wyad4yp229ckemcctd6zkr
title: "Import wand125: s(77) = 9 (#279)"
kind: task
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-01-result-import-first-application.md
labels:
  - packing
  - result-import
dependencies: []
parent_id: is-01m3wvgebtkjqb3km59h7768zx
created_at: 2026-10-01T23:55:43.131Z
updated_at: 2026-10-02T00:17:33.593Z
---
Result import process from stage 1. New optimality entry; s(78) = 9 follows by monotonicity, a second route beside T-064. Certificate directory first published at bd4de4f6, retained at 1a25a5e. Same checksum-file defect as #280. The cover replaces 84 points on loaded lines by segments of length 2/1000, a shape the reviewed s21, s45 and s60 covers do not have: the review checks whether either checker depends on the earlier shape. Cheapest complete replay zmx2 --d4 --pair-points, up to about 5 thread-hours.

## Notes

2026-10-01: W1 research-survey, correctness focus. Objective: stages 2 and 3 of the result import process (retain, record as reported). Artifact: a pull request stacked on jlevy/squares#290, branch claude/import-2026-10-01-requests. Check: validate_schemas, check_source_coverage, check_results, packing-validate --records.
