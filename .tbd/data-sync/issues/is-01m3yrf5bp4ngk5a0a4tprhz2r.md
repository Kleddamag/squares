---
type: is
id: is-01m3yrf5bp4ngk5a0a4tprhz2r
title: "T-046 leftovers: replay the 28 September rectangle certificates n = 51, 57, 58, 72, 73, 91 (n = 37 only if T-069's n37 fails)"
kind: task
status: open
priority: 2
version: 3
labels:
  - result-import
dependencies:
  - type: blocks
    target: is-01m3yrzkz80qd1wv5sjr0kkkv0
parent_id: is-01m3yrdxte02c7bnygkke34ct4
created_at: 2026-10-02T16:51:56.405Z
updated_at: 2026-10-02T17:01:28.008Z
---
Dispatched to runners r1 (n72 workers 3, n91) and r2 (n73 workers 2, n51, n57+n58); transfer dirs wand125-rect-sept28-r1-*/-r2-* on branches claude/replay-wand125-rect-oct1-r1/-r2. Merge with audit_wand125_rectangles --packet 2026-09-28 --merge, then records. About 24 CPU-h.

## To finish (validation backlog, 2026-10-02)

T-046 (wand125's rectangle bounds of 27 and 28 September, V0/C0). After the runners finish: `.venv/bin/python3 -m devtools.audit_wand125_rectangles --packet 2026-09-28 --out resources/web/wand125-rectangle-certificates-2026-09-28/receipts/replay --merge <run dirs>`, then `--check`, then the records (apply_wand125_rectangles; each count that passes is registered again as replayed, as T-045 and T-070 were). About 24 CPU-hours. Refutes: verify.cpp refusing a direction, or a regenerated input whose digest differs from the upstream run's; the count is then recorded with replay_status failed. Moves the rung: T-046 itself reaches V3/C3 only when every one of its standing certificates has a passing replay; the 16 that T-068 raises would otherwise hold it at V0, so record that decision (replay them, or let the replayed entries carry those counts). C1 comes sooner, by recording the 2026-09-27 scaling review as external_review on the report entries. Run `uv run --frozen --all-extras --group dev python -m devtools.check_results`.
