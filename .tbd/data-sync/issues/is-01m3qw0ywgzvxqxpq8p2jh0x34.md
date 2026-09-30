---
type: is
id: is-01m3qw0ywgzvxqxpq8p2jh0x34
title: Validate and simplify the n11 proof before a dedicated explainer
kind: task
status: open
priority: 2
version: 6
spec_path: docs/project/reviews/review-2026-09-29-n11-optimality.md
labels:
  - n11
dependencies:
  - type: blocks
    target: is-01m3qw1d6z2hnprytp2r49qe4f
parent_id: is-01m3qw8b5q2xgjp85cxx24134c
created_at: 2026-09-30T00:39:24.303Z
updated_at: 2026-09-30T13:18:45.321Z
---
Prerequisite gate for the requested new n=11 explainer paper. Do not begin simplification work until the current proof validation has completed for the exact theorem and certificate selected for exposition. Record the theorem, source revision, complete domain/census evidence, audited mathematical premises, V/C levels and remaining limitations. Distinguish the established T-037 global bound from T-059 exact row-minimum equality and independent rectangle coverage; one does not certify the others. Then make a bounded effort to simplify and streamline the validated argument: reduce unnecessary dependencies and case distinctions, expose the essential geometric and counting lemmas, and compare clearer equivalent formulations. Use Astra max for hard mathematical review and Sol for supporting implementation. Revalidate every mathematically material simplification with focused controls and complete evidence where required. Acceptance: reviewed proof dependency map, recorded simplification attempts and outcomes (including no safe simplification found), a frozen supported argument, and explicit readiness for exposition. This gate must close before any drafting or figure implementation for the new paper.

## Notes

Validation prerequisite completed 2026-09-30: T-060 exact global equality confirmed at S5/V4/C5, final composition eaad8f14 with all2180 exclusions and ten capture nodes accepted. Integration finishes under think-3i74. Next independent slice may simplify the frozen accepted proof; the explainer remains blocked on this simplification disposition, not merely on CI.
