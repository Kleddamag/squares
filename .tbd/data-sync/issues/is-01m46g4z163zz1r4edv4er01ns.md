---
type: is
id: is-01m46g4z163zz1r4edv4er01ns
title: "Import squarepacker #363: s(12) >= 7943/2000 (v1.1 at 98ffe37/7a96bec), replay and review to the verified lane"
kind: task
status: in_progress
priority: 1
version: 4
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m46g4yac7ewc22drc7twjhy5
hold: null
hold_until: null
created_at: 2026-10-05T17:00:29.093Z
updated_at: 2026-10-05T18:30:03.248Z
started_at: 2026-10-05T17:06:28.130Z
---

## Notes

2026-10-05 18:30Z, lane A (think-3kd9), stage 4 in progress.

- Daniel's verify (7d6f46d blobs, overflow checks, binary 60279b2c) at N = 96000: VERIFIED,
  least 10000050/10^7 at k = 0, every line = source log; 4,671 s wall, 3,439 CPU-s (commit bb2bd87d5).
- Controls: verify single bins 0/30000 and native rows 0/30000 refuse both (receipts committed).
- Review: separately prompted (claude -p --agent tbd-strong --model claude-opus-5-5), stored byte for
  byte at docs/project/reviews/review-2026-10-05-s12-v11-certificate.md (commit 075ac4ad3); no blocking
  finding; it computed nothing (tool permissions refused execution, its F1). T-095 at V0/C1.
- Native parent-core --case s12-v11 --all --workers 2 started 18:27Z at 3ddd47d3a (pid 16828); at the
  current load ~1.8 rows/s, about 6 h wall, ~5 CPU-h. indep_check N = 96000/192000 and its two
  controls follow it (2-thread cap). The verified-lane move waits for the native decision.
