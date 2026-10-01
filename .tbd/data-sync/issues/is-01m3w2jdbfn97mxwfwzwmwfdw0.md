---
type: is
id: is-01m3w2jdbfn97mxwfwzwmwfdw0
title: "n = 11 optimality paper: font weight and math match the original explainer"
kind: task
status: in_progress
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T15:50:45.346Z
updated_at: 2026-10-01T17:22:12.801Z
---
Owner, 2026-10-01: 'investigate font weight and math consistency. The page here looks good, it is the original: https://jlevy.github.io/squares/explainer.html but the page here https://jlevy.github.io/squares/n11-optimality/t-060-explainer.html' (message cut off; the second page is the one that looks wrong). Compare the two live pages and the local builds in a browser: body, heading, caption, table and footnote font families, weights, sizes and line heights; whether the same font files load at the same weights (a missing weight is synthesized or falls back); inline and display math faces, sizes and weights (KaTeX fonts, math in sans contexts, math in headings and tables, bold math), and code-versus-math spans. Report every difference with computed values and screenshots, find the cause (the paper's own renderer and stylesheet against the shared paper-type.css), fix it at the shared layer so the two cannot drift, and pin with a browser test.

## Notes

Cause found 2026-10-01 (agent interim): the paper's shell inlines explainer-publication.css, whose math rule sets text-rendering: geometricPrecision on .katex and returns it to auto on macOS only under html[data-squares-native-math-metrics]; that attribute is stamped by explainer/native-math-metrics.js, which the explainer's shell carries and the paper's never did. So on macOS Chromium the paper's formulas are rasterised lighter: ink 0.5268 against 0.6318 square em for s(11)=T in light (16.6% less), 25.8% less in dark. Toggling the one property reproduces each page's value. Fix in the worktree: both renderers take the stylesheet and head script as one pair (render_explainer.publication_layer); the paper also now uses the site's math pipeline (the one-mu kern; \top for a sans T drawn from the reader's Times). Not verified in Firefox or WebKit. CI could not see it: on Linux both pages take geometricPrecision; new tests tell the page it is on macOS.
