---
type: is
id: is-01m49m120kvhpbtpt0x4jfxdww
title: "Schema: reported_upper_bound.algebraic_source vocabulary, generator support and contract test"
kind: task
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: claude-code@vm
labels:
  - packing
dependencies:
  - type: blocks
    target: is-01m49m12kznje1m608fc5g1akz
  - type: blocks
    target: is-01m12y4vf6c8t5mb3f268nm1kx
parent_id: is-01m49m0enx3qf7mm1kyrra0z10
hold: null
hold_until: null
created_at: 2026-10-06T22:05:58.675Z
updated_at: 2026-10-06T22:06:51.350Z
started_at: 2026-10-06T22:06:51.350Z
---
Add algebraic_source enum {catalogue, derived-from-exact-form, contact-system} to frontier/square-packing-case.schema.yaml, required when algebraic_degree is non-null. generate_frontier_case writes 'catalogue' for catalogue intakes. Contract test refuses a degree without a source and an unknown source. Spec component 1.
