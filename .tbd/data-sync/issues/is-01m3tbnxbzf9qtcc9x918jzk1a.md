---
type: is
id: is-01m3tbnxbzf9qtcc9x918jzk1a
title: Math inside sans text is sans math on every site surface
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-30T23:51:28.382Z
updated_at: 2026-09-30T23:51:28.382Z
---
Owner, 2026-09-30: math within a sans context is sans math. think-g63b (4cfb962e6) set math in the face of the text around it via host_math_init.js isSansContext; audit every sans context on the built site (cards and their notes, chips, tables, popovers, nav, captions, the Visualize and case pages) in the preview, list any formula still typeset in the serif inside sans text, and fix the face detection or markup so none remains; add a check that walks the pages.
