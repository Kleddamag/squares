---
type: is
id: is-01m3wjqha7v5vqk2x99ncj5940
title: "Atlas: a Grid | Triangle toggle, with the perfect squares n = k^2 down the triangle's right edge and an animated transition"
kind: feature
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T20:33:10.469Z
updated_at: 2026-10-01T20:33:14.586Z
---
Owner, 2026-10-01: 'a toggle (same style as the Film | Workbench toggle on the visualize tab) that lets you choose between Grid | Triangle for the atlas visualization. The current visualization is a grid, but we should have a triangle where the numbers match the structure of the perfect packings of n = k^2 along the right edge. It should toggle between. There should be a nice, clean transition, too, where the blocks move into the right place in a fast and efficient way. This can be done separately as a new bead on a new branch.' Triangle: row k holds n = (k-1)^2 + 1 … k^2, that is 2k - 1 cells, right-aligned so 1, 4, 9, 16, … run down the right edge. Own branch and PR.
