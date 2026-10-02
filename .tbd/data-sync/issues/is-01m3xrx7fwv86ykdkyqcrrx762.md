---
type: is
id: is-01m3xrx7fwv86ykdkyqcrrx762
title: "Import wand125: independent second checker for Valid7 (T-064) (#296)"
kind: task
status: open
priority: 2
version: 1
labels:
  - result-import
  - packing
dependencies: []
parent_id: is-01m3wvgebtkjqb3km59h7768zx
created_at: 2026-10-02T07:40:22.908Z
updated_at: 2026-10-02T07:40:22.908Z
---
Result import process, K. wand125/valid7-independent-check (MIT), records in release records-v1; verify.sh fetches records, checks SHA-256, reruns check_record.py (RECORD OK) and three mutant tests; 156,800 roots over the whole pose space, exact rationals, written from FORMAT.md only (READ_LOG.md). About 626 core-hours to regenerate. Register action: evidence update to T-064 (no new entry), with the replay of the record check; T-064 claim text and next_rung per #296's suggestions after review. Also s(78) = 9 second route via s(77) = 9 (T-067).
