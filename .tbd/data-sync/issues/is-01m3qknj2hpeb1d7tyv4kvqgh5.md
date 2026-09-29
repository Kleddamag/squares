---
type: is
id: is-01m3qknj2hpeb1d7tyv4kvqgh5
title: Make CI wall recent-run sampling aware of gate event surfaces
kind: task
status: in_progress
priority: 2
version: 6
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
labels: []
dependencies: []
parent_id: is-01m3p5wj25knm7rbx0g4a4tpvg
created_at: 2026-09-29T22:13:22.127Z
updated_at: 2026-09-29T22:30:26.416Z
closed_at: 2026-09-29T22:22:35.132Z
close_reason: Event-aware recent sampling now bounds discovery, admits only complete current-topology runs, reuses admitted payloads, and refuses insufficient compatible samples; focused tests and independent review passed.
resolution: null
duplicate_of: null
---
Post-merge live wall reporting and explicit --run-id work, but --sample --recent discovers successful pull_request runs only. Add event-aware discovery for push/schedule/workflow_dispatch while preserving exact declared-job/source-topology admission. Until then use explicit run IDs for post-merge baseline measurements; do not claim automatic recent sampling works for this surface.

## Notes

Integrated at 902b959b4 and independently reviewed through a2b8e696c. Recent sampling has gate-specific event surfaces, globally deduplicated bounded discovery, exact successful current-topology admission, retained payload reuse, and explicit insufficiency refusal. Focused evidence: 29 tests passed; Ruff/format and BasedPyright clean; native_sol review found no blocker. Ordinary explicit run inspection remains available. Keep in progress until the integrated tree passes published CI.
