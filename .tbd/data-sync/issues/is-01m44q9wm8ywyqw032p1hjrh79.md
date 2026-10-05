---
type: is
id: is-01m44q9wm8ywyqw032p1hjrh79
title: "PR #333 A2 (Medium): durable docs are not in English, and numbers are glued to words."
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m44q9st2e0jh0h0cztp6hnv8
created_at: 2026-10-05T00:27:01.639Z
updated_at: 2026-10-05T00:27:01.639Z
---
https://github.com/jlevy/squares/pull/333#pullrequestreview-5408660716

**A2 (Medium): durable docs are not in English, and numbers are glued to words.**
- The READMEs for sessions 175–179 contain Chinese paragraphs (lines 3–5 or 3–6 in each, plus line 30 in session 175's).
- Numbers glued to words run through the new READMEs and session records and leak into SYNOPSIS titles, for example "explains71of72fixed tuple losses" and "in2623atoms".
- **Fix:** translate the paragraphs and re-space the numbers throughout.

Authorized maintenance only. Disposition requires evidence and exact-head CI; no research follow-up reserved.
