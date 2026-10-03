---
type: is
id: is-01m3xrx7fwv86ykdkyqcrrx762
title: "Import wand125: independent second checker for Valid7 (T-064) (#296)"
kind: task
status: open
priority: 2
version: 3
labels:
  - result-import
  - packing
dependencies: []
parent_id: is-01m3wvgebtkjqb3km59h7768zx
created_at: 2026-10-02T07:40:22.908Z
updated_at: 2026-10-03T17:36:39.381Z
---
Result import process, K. wand125/valid7-independent-check (MIT), records in release records-v1; verify.sh fetches records, checks SHA-256, reruns check_record.py (RECORD OK) and three mutant tests; 156,800 roots over the whole pose space, exact rationals, written from FORMAT.md only (READ_LOG.md). About 626 core-hours to regenerate. Register action: evidence update to T-064 (no new entry), with the replay of the record check; T-064 claim text and next_rung per #296's suggestions after review. Also s(78) = 9 second route via s(77) = 9 (T-067).

## Notes

2026-10-03 06:05 wand125 independent Valid7 checker with --guard-d1: w5 DONE, shards 13-14 all VERIFIED (claude/replay-valid7-w5 @8cfcb5aa; 0 uncertified, 0 counterexamples). w4: 10_1-10_3, 11_1 VERIFIED; 11_2, 12_1 left (@2e8570b0). w3: shards 7, 8 and 9_1 VERIFIED; 9_2, 9_3 left (@1e6ec98c; 8_3 receipt shows already-done 0 after a relaunch overwrote the partial receipt, record rebuilt in full). w2: shard 4, 5_1, 5_2 VERIFIED; 5_3, shard 6 left (@02eb2c1e). w1: shard 1, 2_1 VERIFIED; 2_2 resumed, then 2_3, shard 3 (@c7e4c660). When all finish, the records lane merges w1-w5 receipts as independent-implementation evidence on T-064.
2026-10-03 17:40 Valid7 independent checker (--guard-d1): w3 DONE (shards 7-9, nine runs VERIFIED exit 0; claude/replay-valid7-w3; also pushed a stray sync.sh helper, drop it at merge), w4 DONE (shards 10-12, six runs VERIFIED; claude/replay-valid7-w4), w5 DONE (13-14). w2: runs 1-7 done, shard 6 run 3 (last) running. w1: shards 1-2 done, shard 3 resumed (181/448 roots at the 2 h cut). After all pass: merge w1-w5 receipts as independent-implementation evidence on T-064, in the follow-up branch after the stack lands (scope freeze).
