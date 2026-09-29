---
type: is
id: is-01m3p6krj8zr6a0956x7de4xfv
title: Investigate unchanged frontend timing drift on PR 246
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m3nzy6gqfv60whzzvww0ffa0
created_at: 2026-09-29T09:05:57.319Z
updated_at: 2026-09-29T09:05:57.319Z
---
Hosted run36546217991 at45eaf8e75 passed all three frontend functional steps, but the tier took134.86s against recorded85.25s:1.58x exceeds the1.5x regression threshold while remaining below the150s absolute ceiling. Workbench browser behavior took134.85s; browser floor54.34s; liveness24.61s. The preceding run36544631396 passed frontend, and the intervening commit changed only the document scanner, its test and review prose. Preserve this failure and measure workload/runner variance before changing budgets or adding retries. This is separate from the inherited Session161 record blocker; all final-head functional checks passed.
