---
type: is
id: is-01m3xrx6p081zyj7efn8tjkqw0
title: "Import wand125: linear point/segment certificates s(101) >= 257/25 and s(83) >= 187/20 (#294)"
kind: task
status: open
priority: 2
version: 4
labels:
  - result-import
  - packing
dependencies:
  - type: blocks
    target: is-01m3yrzkz80qd1wv5sjr0kkkv0
parent_id: is-01m3yrdxte02c7bnygkke34ct4
created_at: 2026-10-02T07:40:22.080Z
updated_at: 2026-10-02T17:01:38.803Z
---
Result import process, I. New certificate kind: point masses + uniform segments + rectangles, D4, mass n - 1/100000, checked by code/unified_linear_verify.cpp (the verifier of mixed_n50_L735), 201 net angles. n101 at af1db07, n83 at 0c35d90; n82 (9.32) announced. Stage 2 packet, stage 3 entry V0/C0, stage 4 replay + review (new checker: review needed). Compared with Green G_10 = 10.2467.

## To finish (validation backlog, 2026-10-02)

T-073 (linear certificates at n = 83 and 101..105, V0/C1). From packing/: `.venv/bin/python3 -m devtools.audit_wand125_linear linear-replay n101 --range A-B --work W --workers 4` over all 201 angles (`linear-plan n101 --parts 4`), likewise n83, then `linear-merge n101`, `linear-merge n83`, and `linear-control n101 --work W`, each merged receipt keeping each direction's least lower bound (finding LC-4). Packet resources/web/wand125-linear-certificates-2026-10-02/. Expected CPU: 8.1 (n101) and 23.0 (n83) CPU-hours by `linear-price`. Refutes: an angle unified_linear_verify.cpp refuses, or a replay not matching the shipped record. Moves the rung: both merged receipts recorded as replayed-here entries derive V3/C3. mixed_n83_L937 (think-r7yt) raises n = 83's reported value; T-073 stays true as stated. Run `uv run --frozen --all-extras --group dev python -m devtools.check_results`.
