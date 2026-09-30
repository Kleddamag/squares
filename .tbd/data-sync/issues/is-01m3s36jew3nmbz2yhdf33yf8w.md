---
type: is
id: is-01m3s36jew3nmbz2yhdf33yf8w
title: Index pinned near-capture source in one parse for replay
kind: task
status: in_progress
priority: 0
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3rp1yjrw96h7yy6azcahx2w
created_at: 2026-09-30T12:04:02.651Z
updated_at: 2026-09-30T12:28:30.150Z
---
Measure and implement one-pass, source-hash-bound extraction of the 121 ordered near-capture steps, header, and final state into external scratch. Keep every original field; verify input hash before/after and indexed record integrity. Use indexed reads only after independent review, with no cached PASS premise or source mutation. Compare extraction time to repeated jq and retain a reproducible cost receipt.

## Notes

Astra-approved indexer SHA94075042 frozen in cf4a45327. Fresh build_and_open binds fixed source to derived stream in memory; forged rewritten stream+index refused in focused controls (5 pass). Actual pinned near source 185,901,535 bytes/121 steps indexed once: jq10.019s, scan2.280s, total12.617s; compact receipt capture-near-index/result.json SHA7ce0a9e4, no proof acceptance. Remaining: integrate fresh index within near geometric checker after r111 accepted, pin helper, verify before/after, retain complete geometric receipt. Repeated jq step0 parse observed2.62s; index avoids 121 full parses.
