---
type: is
id: is-01m3qj6hf8hnceh702waazsnhk
title: Give pool-heavy reachable tests an exclusive inner-worker phase
kind: task
status: in_progress
priority: 1
version: 2
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
labels: []
dependencies: []
parent_id: is-01m3p5wj25knm7rbx0g4a4tpvg
created_at: 2026-09-29T21:47:41.413Z
updated_at: 2026-09-29T21:48:27.282Z
---
Exclusive pytest workers with PACK_JOBS=1 still serialize the whole-corpus atlas test, which already uses a deterministic per-case process pool. Retained timings show a 1327.87-second single-node atlas call; current quiet run does not prove its live identity. Preserve all nodes and assertions: identify pool-heavy tests explicitly, run the remainder with bounded xdist and PACK_JOBS=1, then pool-heavy tests without xdist and with the reserved host allocation. Keep explicit resource overrides authoritative. Prove collection union/disjointness and failures/empty-lane behavior; measure the integrated candidate before claiming improvement.
