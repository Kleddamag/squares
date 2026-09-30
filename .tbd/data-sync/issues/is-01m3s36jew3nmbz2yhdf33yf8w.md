---
type: is
id: is-01m3s36jew3nmbz2yhdf33yf8w
title: Index pinned near-capture source in one parse for replay
kind: task
status: open
priority: 0
version: 1
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3rp1yjrw96h7yy6azcahx2w
created_at: 2026-09-30T12:04:02.651Z
updated_at: 2026-09-30T12:04:02.651Z
---
Measure and implement one-pass, source-hash-bound extraction of the 121 ordered near-capture steps, header, and final state into external scratch. Keep every original field; verify input hash before/after and indexed record integrity. Use indexed reads only after independent review, with no cached PASS premise or source mutation. Compare extraction time to repeated jq and retain a reproducible cost receipt.
