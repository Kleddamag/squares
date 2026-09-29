---
type: is
id: is-01m3q99abfyys0pkhy5w7g8m3j
title: Keep unused n32 inventory out of negative-control worker snapshots
kind: bug
status: open
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m3nzy6gqfv60whzzvww0ffa0
created_at: 2026-09-29T19:11:55.236Z
updated_at: 2026-09-29T19:14:53.155Z
---
The recovery push measured 170,442,934 snapshot source bytes against the fixed 160 MiB cap. Audit the retained n=32 one-spare inventory (3,344,052 bytes) as generated research output with no registered mutation-control consumer, then prune it from worker copies while keeping the repository artifact and regression coverage.

## Notes

Independent Sol cross-review found no lost mutation target or checker input. Inventory has only recorded-command/prose references; tests recompute n32 rather than load it. Focused regression proves absence from snapshot/copy-back and byte-identical preservation of a needed agenda-040 sibling. Two tests pass, Ruff and BasedPyright clean. Final integrated push gate pending; cap remains 160 MiB. Structural headroom work stays think-t1lk.
