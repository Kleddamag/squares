---
type: is
id: is-01m3rb0sr8p2xn3m96v3cs96cx
title: Decouple rectangle diagnostics and partition the PR review surface
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies:
  - type: blocks
    target: is-01m3rb0t4zqdze43drjkx9cqx2
parent_id: is-01m3ra1hjvn4bdh3h13aggqgvb
created_at: 2026-09-30T05:01:27.687Z
updated_at: 2026-09-30T05:04:27.446Z
---
Extract strict frontier receipt admission so comparison and refinement do not import each other's CLI; preserve native rectangle acceptance as separate from n11 proof modules. Partition review into proof logic, evidence intake, rectangle tools, and CI/efficiency ownership. Decide actual PR split from dependency map with no force-push or history rewrite in planning; preserve existing reviewed checkpoints and comments. Do not gate morning proof on cleanup.
