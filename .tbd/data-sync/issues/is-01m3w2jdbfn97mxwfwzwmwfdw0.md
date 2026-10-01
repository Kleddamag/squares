---
type: is
id: is-01m3w2jdbfn97mxwfwzwmwfdw0
title: "n = 11 optimality paper: font weight and math match the original explainer"
kind: task
status: in_progress
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T15:50:45.346Z
updated_at: 2026-10-01T16:04:27.618Z
---
Owner, 2026-10-01: 'investigate font weight and math consistency. The page here looks good, it is the original: https://jlevy.github.io/squares/explainer.html but the page here https://jlevy.github.io/squares/n11-optimality/t-060-explainer.html' (message cut off; the second page is the one that looks wrong). Compare the two live pages and the local builds in a browser: body, heading, caption, table and footnote font families, weights, sizes and line heights; whether the same font files load at the same weights (a missing weight is synthesized or falls back); inline and display math faces, sizes and weights (KaTeX fonts, math in sans contexts, math in headings and tables, bold math), and code-versus-math spans. Report every difference with computed values and screenshots, find the cause (the paper's own renderer and stylesheet against the shared paper-type.css), fix it at the shared layer so the two cannot drift, and pin with a browser test.

## Notes

Owner added 2026-10-01: the optimality paper 'has thinner looking math. We should be rigorously consistent about all the ways we format text and content.' and 'The explainer page is the main approach.' Agent on claude/n11-paper-type; the explainer is the reference.
