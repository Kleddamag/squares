---
type: is
id: is-01m3wyaaj32r2rm87q4k2e4ax2
title: "Import wand125: s(59) = 8 (#280)"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-10-01-result-import-first-application.md
labels:
  - packing
  - result-import
dependencies: []
parent_id: is-01m3wvgebtkjqb3km59h7768zx
created_at: 2026-10-01T23:55:40.479Z
updated_at: 2026-10-01T23:55:40.479Z
---
Result import process from stage 1. New optimality entry; T-062 and T-063 gain a sentence naming the monotone route. Source wand125/square-packing-bounds at 1a25a5e, checkers Daniel at b91d70b6 (already retained). Triage: verify.sh cannot pass as published (SHA256SUMS lists unpublished logs); the exact evidence is two runs, the main one NOT VERIFIED with 6 boxes, on the checker that predates the zero-width-bin guard. Cheapest complete replay zmx2 --d4 and --full, about 2,200 CPU-s.
