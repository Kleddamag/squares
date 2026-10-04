---
type: is
id: is-01m44m1dkx2sb29pw359yn4rja
title: "Results tables: drop the Details column, put the record links in the row's popover"
kind: task
status: in_progress
priority: 1
version: 2
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m42xfwp06kzm2b390dx1cw17
hold: null
hold_until: null
created_at: 2026-10-04T23:29:58.396Z
updated_at: 2026-10-04T23:30:01.244Z
started_at: 2026-10-04T23:30:01.244Z
---
Owner request 2026-10-04: the results tables (Recent Results on the overview, all-results.html) carry a Details column of record links (overview_sections.result_head / _records). Remove the column; the row's popover (result_overview.result_popover_html, and the in-page short form result_row writes before the fragment is fetched) carries the links in an appropriate place. Cleaner to read.
