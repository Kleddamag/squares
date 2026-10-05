---
type: is
id: is-01m46g4z163zz1r4edv4er01ns
title: "Import squarepacker #363: s(12) >= 7943/2000 (v1.1 at 98ffe37/7a96bec), replay and review to the verified lane"
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m46g4yac7ewc22drc7twjhy5
hold: null
hold_until: null
created_at: 2026-10-05T17:00:29.093Z
updated_at: 2026-10-05T17:24:05.625Z
started_at: 2026-10-05T17:06:28.130Z
---

## Notes

2026-10-05 17:30Z, lane A (think-3kd9), stage 1-3 done on branch claude/ecstatic-pascal-pothtx-s12.

Claim map (#363, issue body; no comments): one claim, s(12) >= 7943/2000 = 3.9715, certificate
s12_lower_3.9715.txt (SHA-256 e2f326b2...), squarepacker/s12-lower-bound v1.1 (98ffe37 adds it,
7a96bec = tag v1.1 adds .zenodo.json). New entry, provisional T-095 (a later release than T-078's).
Notes, not claims: "why it stops near here" (560/141 sigma_0, LP 12.0052 at 3.97155) and the
#309 clarification (31360/7900 rejection is a net artefact at the reported pose); neither changes T-078.

Retained: packing/resources/web/squarepacker-s12-lower-bound-2026-10-05/ at 7a96bec (commit 3ae63093a),
devtools.audit_s12_v11_certificate (21 exact checks PASS), native case s12-v11 at N = 96000.
Registered: T-095 V0/C0 draft S3 (commit 037f78f15), E-n012-squarepacker-7943-2000-report.

Stage 4 plan (2 threads, nice 10): Daniel's verify (7d6f46d, overflow checks) at N = 96000
(running since 17:09Z), native parent-core all 39,765 rows (pilot 0.4 s/row, ~4.4 CPU-h),
indep_check N = 96000 (+192000), controls on all three, separately prompted review (claude -p,
running since 17:21Z in /home/user/squares-lanes/s12-review).
