---
type: is
id: is-01m3v99q1pcy16z29xrgfza1vb
title: "Homepage survey: hover keeps the packing's black lines; only the background tint changes"
kind: task
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T08:29:05.970Z
updated_at: 2026-10-01T08:29:08.447Z
---
Owner, 2026-10-01: hover on the survey on the homepage hides the black lines on the graphics. This doesn't look good. Don't do that. Just overlay with the hover background color change as you currently do. Find what the hover rule does to the tile's SVG (an opaque background painted over the strokes, a fill change on the squares, a blend mode, or a z-order overlay) and make the hover tint sit behind or beneath the strokes so every line stays at full black; check the frontier page's grid for the same fault; pin with a browser test that samples a stroke pixel with and without hover.
