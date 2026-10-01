---
type: is
id: is-01m3w446qmzxptdghpen35k717
title: "Results tables: a wider n column that wraps, and a narrower Result column that wraps cleanly"
kind: task
status: in_progress
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T16:17:56.961Z
updated_at: 2026-10-01T17:01:59.242Z
---
Owner, 2026-10-01: 'the results table still has issues with column width. the n column should be wider and wrap so values like T-056 with many n values don't take up a ton of vertical space. the result column could be narrower and wrap cleanly to make room'. The n cell of a result covering many cases (T-056, T-044, T-007) is one value per line today; it should set its values inline, wrapping within a wider column (ranges collapsed where consecutive). The Result column gives up the width: it is held to 411 px by four unbreakable formulas, so those must break cleanly (at relation and operator boundaries, or scroll inside the cell). This also answers think-b245 (tables scrolling sideways at 1024 and 768). Measure with measure_site_pages columns before and after; test_site_result_columns pins it.

## Notes

2026-10-01, branch claude/site-polish-4-columns, commit 70366bb27 (not pushed). n cell: each count or range is a nowrap box (overview_sections.case_list); a cell of five values or more wraps and asks for --site-cases-measure (24ch, column 225 px), narrowing to half that before the table scrolls; shorter lists stay on one line and the column is as narrow as its lists where no long list shows (85 px on the overview as it opens). Result: floor now its 18rem (288 px); a quotient of more than 24 digits sets its solidus as \mathbin{/} (overview_data.breakable_quotients), widest math piece 395 -> 249 px; summary formulas set in the line, so no line starts with a comma. Measured with every row showing, both pages: 1280 n 96->225, Result 480->358, T-056 row 386->165 px (15->6 lines), no scroll; 1024 scroll 63->0, Result 411->288, n 156; 768 scroll 319->221. Cost: Results-page table height at 1280 6213->6689 px, at 1024 6872->8162. The 1024 fit has 36 px of slack if the Rungs column widens. Pinned in tests/test_site_result_columns.py (55 pass); measure_site_pages columns reports split, cuts, wrapped, stranded, piece.
