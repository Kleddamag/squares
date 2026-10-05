---
type: is
id: is-01m44qz48kr4zse36ykc4v9hfb
title: "Homepage: link evand's Square Packing Atlas site and its open-problems page"
kind: task
status: in_progress
priority: 2
version: 3
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
hold: null
hold_until: null
created_at: 2026-10-05T00:38:37.587Z
updated_at: 2026-10-05T01:12:31.395Z
started_at: 2026-10-05T00:41:16.239Z
---
Owner request: the evand site and https://evand.github.io/square-packing/problems.html are linked from the project homepage (packing/devtools/overview_sections.py OTHER_PROJECTS / templates/overview-article.md), re-rendered.

## Notes

Homepage: packing/devtools/templates/overview-article.md, Other Square Packing Projects intro now links https://evand.github.io/square-packing/ and https://evand.github.io/square-packing/problems.html (cards are links themselves, so the links are prose). evand card note in overview_sections.OTHER_PROJECTS updated: n = 21, 32, 45, 60, s(k^2-3)=k k>=6, s(k^2-4)=k awaiting replay. Commit 6d48ab842 on claude/ecstatic-pascal-pothtx-evand; render_overview ran clean; tests/test_overview.py, test_site_project_tallies.py pass (291).
