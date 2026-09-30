---
type: is
id: is-01m3snf059ca48fjmqh0vrb7e8
title: Expose pre-push slow selection and reuse unaffected checkpoint evidence
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3ra1hjvn4bdh3h13aggqgvb
created_at: 2026-09-30T17:23:13.186Z
updated_at: 2026-09-30T17:23:13.186Z
---
The final two-test repair on PR246 selected 55 reachable test files with -m not exhaustive_exact, including slow atlas rebuilding whose successful checkpoint evidence was already retained. --list exposed only reachable behavioral tests, not actual files/markers/cost. Root stopped the redundant run after inspecting processes. Add a reviewable selection/expected-cost dry-run and an explicit way to reuse unaffected checkpoint evidence or select only changed nodes, without hiding required coverage. Preserve current deliberate slow-lane policy and ensure every omitted obligation is covered by bound prior evidence. This is efficiency follow-up, not a mathematical T060 gap.
