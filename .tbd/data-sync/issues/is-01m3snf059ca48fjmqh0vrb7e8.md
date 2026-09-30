---
type: is
id: is-01m3snf059ca48fjmqh0vrb7e8
title: Expose pre-push slow selection and reuse unaffected checkpoint evidence
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3ra1hjvn4bdh3h13aggqgvb
created_at: 2026-09-30T17:23:13.186Z
updated_at: 2026-09-30T17:36:15.319Z
---
The final two-test repair on PR246 selected 55 reachable test files with -m not exhaustive_exact, including slow atlas rebuilding whose successful checkpoint evidence was already retained. --list exposed only reachable behavioral tests, not actual files/markers/cost. Root stopped the redundant run after inspecting processes. Add a reviewable selection/expected-cost dry-run and an explicit way to reuse unaffected checkpoint evidence or select only changed nodes, without hiding required coverage. Preserve current deliberate slow-lane policy and ensure every omitted obligation is covered by bound prior evidence. This is efficiency follow-up, not a mathematical T060 gap.

## Notes

Observed invocation: packing-validate --push --since6a307f6a4 --jobs4 --inner-jobs2 selected 55 reachable files and launched pytest -m not exhaustive_exact -n7, including slow atlas work; supervisor interrupt exited130 and no child processes remained. Inspect effective worker planning as well as selected files/markers/cost before changing behavior; the current selector deliberately includes reachable slow tests, so do not simply suppress them. Reuse must bind prior evidence and list invalidated obligations explicitly.
