---
type: is
id: is-01m3v8nsb2pc6hz0b4ynz6jcvg
title: "Result filters: a 'Current best only' checkbox, on by default on the homepage and off on the Results page"
kind: task
status: in_progress
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T08:18:12.953Z
updated_at: 2026-10-01T09:47:51.441Z
---
Owner, 2026-10-01: add a filter for 'current best only' as a checkbox, checked on the homepage overview but not on the all results page. In the shared filter bar (result_filters, table.js, FilterDefaults): one checkbox that shows only rows whose standing is current best; composes with the other filters; default on in RECENT_DEFAULTS and off in RESULTS_DEFAULTS; rows hidden by it stay in the HTML; the count follows; a query preset; whether the Standing select stays beside it or the checkbox replaces it is decided from how the bar reads.

## Notes

Implemented on claude/site-polish-2-filter at 9036d7c04 (worktree overview-fixes, not pushed). Checkbox 'Current best only' in result_filters after Standing; FilterDefaults.current_best, True in RECENT_DEFAULTS, False in RESULTS_DEFAULTS. Current best = standing in {current best; current best, reported} (overview_sections.is_current_best), row attribute data-best. Composes by AND with Standing (narrows, never sets); table.js unchanged (existing flag filter). Homepage default 15 -> 6 of 61; results page 61 (23 when checked). Query preset best=true|false. No reset control exists in the bar; none added.
