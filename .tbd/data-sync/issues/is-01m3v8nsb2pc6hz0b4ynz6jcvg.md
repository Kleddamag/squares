---
type: is
id: is-01m3v8nsb2pc6hz0b4ynz6jcvg
title: "Result filters: a 'Current best only' checkbox, on by default on the homepage and off on the Results page"
kind: task
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T08:18:12.953Z
updated_at: 2026-10-01T08:18:19.099Z
---
Owner, 2026-10-01: add a filter for 'current best only' as a checkbox, checked on the homepage overview but not on the all results page. In the shared filter bar (result_filters, table.js, FilterDefaults): one checkbox that shows only rows whose standing is current best; composes with the other filters; default on in RECENT_DEFAULTS and off in RESULTS_DEFAULTS; rows hidden by it stay in the HTML; the count follows; a query preset; whether the Standing select stays beside it or the checkbox replaces it is decided from how the bar reads.
