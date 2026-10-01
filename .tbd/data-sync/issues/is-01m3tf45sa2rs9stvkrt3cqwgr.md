---
type: is
id: is-01m3tf45sa2rs9stvkrt3cqwgr
title: Match n11 paper presentation exactly to the previous explainer
kind: task
status: in_progress
priority: 1
version: 8
delegate: sol
labels: []
dependencies:
  - type: blocks
    target: is-01m3tfk55tdjnvapbh1330qw7e
  - type: blocks
    target: is-01m3tfk7z8s0pr9jv0kksvzh6y
  - type: blocks
    target: is-01m3tfkatddsz86ee870exr3e0
  - type: blocks
    target: is-01m3tfkczqspdb8hp17z6252h9
parent_id: is-01m3tf1nb0x65ybpkdj2d9y7gs
created_at: 2026-10-01T00:51:41.465Z
updated_at: 2026-10-01T01:00:00.368Z
---
User requires identical look and feel to prior explainer: format chips (HTML/PDF/Markdown), title metadata formatting, typography, spacing, colors and shared style conventions. Delegate separate implementation agent to compare original shell/article/CSS and new paper, reuse components where practical, and perform side-by-side visual checks. Preserve original-proof provenance as first prose and preserve math. Keep corrections on draft branch; no publication until feedback integrated.

## Notes

User clarified repeatedly: every styling element must match the prior explainer, including font sizes/design tokens, metadata/chips, typography, margins, colors, figures/tables and print. Clean website integration with shared design system, no page-specific workaround styles. Dedicated Sol agent explainer_style_sol owns renderer/shell/CSS/tests; root owns article provenance/metadata. Require measured side-by-side parity.
