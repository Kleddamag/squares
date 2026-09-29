---
type: is
id: is-01m3nqe98ev7sb8nam5vtsqmth
title: "11-squares research report: dated summary lacks a pointer to the current bound; 'No machine-checked s(n) theorem is on record' and the n = 17/18 dependency sentence are stale"
kind: bug
status: closed
priority: 1
version: 2
labels:
  - packing
  - documentation
  - wand125-update
dependencies: []
parent_id: is-01m3neehm7hq4apdvzg9925738
created_at: 2026-09-29T04:40:49.166Z
updated_at: 2026-09-29T05:11:46.211Z
closed_at: 2026-09-29T05:11:46.211Z
close_reason: Fixed in 2709dca52 on claude/magical-davinci-ueqmu1-docs-refresh
resolution: null
duplicate_of: null
---
docs/project/research/research-2026-08-22-packing-11-unit-squares.md:35-52 (add a pointer: T-033 3.8269975 and Kleddamag's 31/8 is the verified bound), :1381 (Lean reductions of s(21) = 5 and s(32) = 6 are on record; none built here), :2306 ('Neither current verified 459/100 lower bound depends on these artifacts'). Also render_research_tables.py:76 labels every certificate bound 'elementary' in the frontier-open table. Inventory §3.7.
