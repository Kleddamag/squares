---
type: is
id: is-01m3sgmwq57x96mhx3j4j722xy
title: Evaluate an exact derivative bound on the frozen rectangle frontier
kind: task
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3rcka78kmcccpetknr2mswh
created_at: 2026-09-30T15:59:03.395Z
updated_at: 2026-09-30T16:06:39.125Z
---
W5 support for finishing the independent native rectangle verifier. Astra first checks the independently derived edge-chord derivative enclosure and its axis/boundary/cancellation obligations. If sound, implement a bounded diagnostic on every box in the retained fixed-work n11 frontier. Before measuring, freeze inputs and require exact controls, old/new lower bounds, midpoint coverage, newly closed/unresolved IDs, CPU/wall separation and no silent truncation. Adopt only with useful threshold closures and measured cost justification; a partial probe never establishes full external acceptance or C++ parity. Keep this separate from completed T-060 validation and run it alongside final PR integration.

## Notes

Astra approved the exact derivative enclosure and mandatory controls before implementation. Preregistered diagnostic in docs/project/reviews/review-2026-09-30-rectangle-derivative-bound.md. Sol implements isolated Python reference and complete-frontier diagnostic; another Sol scopes a Rust extension, pending measured usefulness. No production adoption or speed claim yet.
