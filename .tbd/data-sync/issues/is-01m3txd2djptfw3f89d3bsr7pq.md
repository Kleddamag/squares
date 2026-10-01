---
type: is
id: is-01m3txd2djptfw3f89d3bsr7pq
title: "Result filters: a maximum age in days replaces the date range; the Results page starts with significance and age off"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T05:01:13.007Z
updated_at: 2026-10-01T05:01:13.007Z
---
Owner, 2026-10-01: (1) drop the date range filtering (from and to); have one maximum age in days instead, defaulting to 180. (2) On the standalone Results page, filtering by significance is off and filtering by date is off by default; otherwise its filters are the same as Recent Results on the homepage. So: one filter bar on both tables (think-3pi5) with an Age control (days; empty means no limit); the homepage's Recent Results starts at significance S4 and up and age 180 days; all-results.html starts at significance All and no age limit. Rows hidden by a default stay in the HTML. The no-script and build-time default needs a deterministic reference date (the render's revision date), with the live page measuring age from today.
