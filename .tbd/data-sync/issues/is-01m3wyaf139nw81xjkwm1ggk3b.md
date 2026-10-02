---
type: is
id: is-01m3wyaf139nw81xjkwm1ggk3b
title: "Import wand125: 34 rectangle-density lower bounds raised since T-046 (#281)"
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
created_at: 2026-10-01T23:55:45.056Z
updated_at: 2026-10-02T00:17:34.302Z
---
Result import process from stage 1. New lower-bound entry for the 34 counts, under a key for the 1a25a5e release; T-046 keeps its claim. Needs a third Packet in audit_wand125_rectangles and a third Registration in apply_wand125_rectangles. Complete replay 148.5 upstream CPU-h, about 230 worker-hours here. Land the 21 stranded receipts first (think-0rrj, think-20mv): 14 are of certificates this issue raises and all 21 still beat the verified bound.

## Notes

2026-10-01: W1 research-survey, correctness focus. Objective: stages 2 and 3 of the result import process (retain, record as reported). Artifact: a pull request stacked on jlevy/squares#290, branch claude/import-2026-10-01-requests. Check: validate_schemas, check_source_coverage, check_results, packing-validate --records.
