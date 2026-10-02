---
type: is
id: is-01m3wyaf139nw81xjkwm1ggk3b
title: "Import wand125: 34 rectangle-density lower bounds raised since T-046 (#281)"
kind: task
status: in_progress
priority: 2
version: 9
spec_path: docs/project/specs/active/plan-2026-10-01-result-import-first-application.md
labels:
  - packing
  - result-import
dependencies:
  - type: blocks
    target: is-01m3yrzkz80qd1wv5sjr0kkkv0
parent_id: is-01m3yrdxte02c7bnygkke34ct4
created_at: 2026-10-01T23:55:45.056Z
updated_at: 2026-10-02T17:01:33.770Z
---
Result import process from stage 1. New lower-bound entry for the 34 counts, under a key for the 1a25a5e release; T-046 keeps its claim. Needs a third Packet in audit_wand125_rectangles and a third Registration in apply_wand125_rectangles. Complete replay 148.5 upstream CPU-h, about 230 worker-hours here. Land the 21 stranded receipts first (think-0rrj, think-20mv): 14 are of certificates this issue raises and all 21 still beat the verified bound.

## To finish (validation backlog, 2026-10-02)

T-068 (34 raised rectangle bounds, V0/C1). Per count, on runners: `.venv/bin/python3 -m devtools.audit_wand125_rectangles --packet 2026-10-01 --replay --n N --workers W --out DIR`, then `--merge DIR...` into resources/web/wand125-rectangle-certificates-2026-10-01/receipts/replay and `--check`, controls with `--control --n N`, then apply_wand125_rectangles. Expected CPU: 148.5 CPU-hours at the source; about 158 CPU-hours here for the 30 certificates left after dominance. Refutes: verify.cpp refusing a direction, or an input digest differing from the upstream run's; that count is recorded with replay_status failed. Moves the rung: each passing count is registered again as replayed (T-045 and T-070 precedent) and T-068 derives V3/C3 when all 34 pass. Run `uv run --frozen --all-extras --group dev python -m devtools.check_results`.

## Notes

2026-10-01: stages 2 and 3 are in draft PR jlevy/squares#292 (branch claude/import-2026-10-01-requests, commit 2b7191461), stacked on #290. Stage 4 not started. The T-id is provisional until #292 is on main; quote it to no author before then.

2026-10-02 (PR #298): the 21 stranded receipts (b02,b04,b07,b08,b09) merged by audit_wand125_rectangles --merge (commit f5003d1da); apply raises the verified bound at 34 counts; register update in progress. T-068 replays: 30 certificates after dominance (66, 86, 87, 90 skipped if F/G verify), ~158 CPU-h; batch launch waits on the speed-up lane P1. Review docs/project/reviews/review-2026-10-02-wand125-rectangle-bounds-t068.md: no defect.
