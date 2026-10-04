---
type: is
id: is-01m424tye0ptksxhthdgqc60k3
title: The typecheck tier's 111 s wall ceiling sits inside hosted-runner variance
kind: task
status: open
priority: 2
version: 2
labels:
  - ci
dependencies: []
parent_id: is-01m41cx3q2pckpmsmmwq1rsngz
created_at: 2026-10-04T00:25:48.735Z
updated_at: 2026-10-04T00:37:30.092Z
---
Hosted typecheck tier walls (basedpyright alone, --jobs 1) read on 3-4 October 2026 across eight branches: 59.6, 80.7, 81.4, 81.8, 93.8, 96.2, 98.8, 104.0, 105.2, 105.7, 106.6, 107.5, 108.2, 108.2, 108.9, 110.9, 114.9 and 115.2 s against a 111 s ceiling (recorded 76.5 s). The same Python tree read 107.5 s and then 115.2 s on consecutive runs (PR 305 at d56b9f503 and 0952efb57, which differ only in a Markdown record), so the breaches are runner variance, not code: the distribution is bimodal near 80 and 105-115 s. Each breach costs a re-run, and a partial re-run then makes check_pr_wall unmeasurable, which fails packing-required. Decide: re-derive the ceiling from these readings under gate-budgets.yaml's rule, make the typecheck wall advisory like the PR wall (think-g4n9), or reduce basedpyright's cost.

## Notes

2026-10-04: the full re-run of PR 305's run 37164605808 (attempt 3, same commit 0952efb57) read 70.67 s, 44.5 s below the breaching attempt's 115.20 s.
