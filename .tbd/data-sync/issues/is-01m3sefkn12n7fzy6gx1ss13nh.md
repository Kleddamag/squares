---
type: is
id: is-01m3sefkn12n7fzy6gx1ss13nh
title: Add a third behavioral CI shard with complete required coverage
kind: feature
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3rkt99p9bxh8csj2v58nh9p
created_at: 2026-09-30T15:21:13.110Z
updated_at: 2026-09-30T15:51:51.956Z
---
Latest source-bound CI at b6c97667b ran suite A156.19/168s and B165.06/154s: combined321.25s against322s leaves no safe headroom. Add suite-c using the existing deterministic cost partition, full exactly-once file coverage, required aggregator and explicit same-or-tighter per-shard budgets. Preserve verified-tree source classification, dependency selection, failure propagation and all fast tests. Sol scheduler and CI wiring lanes work concurrently; Astra audits coverage. Focused contracts then hosted confirmation; no broad local proof reruns or timing-limit relaxation.

## Notes

Run36739024277 at84dc39d7e: all7958behavioral tests pass with7skips; A65.67s/B104.65s/C88.59s. A fails stale-fast baseline, frontend helper omits suite_c selector. Sol repairs both and removes pending-C machinery; Astra approves retaining frozen historical planningweights168/154/154 while tightening liveA ceiling131 (B/C154). Mathematical/Rust and Pages checks pass; final-head CI pending.
