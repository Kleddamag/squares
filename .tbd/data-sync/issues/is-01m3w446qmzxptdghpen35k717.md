---
type: is
id: is-01m3w446qmzxptdghpen35k717
title: "Results tables: a wider n column that wraps, and a narrower Result column that wraps cleanly"
kind: task
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T16:17:56.961Z
updated_at: 2026-10-01T16:17:59.981Z
---
Owner, 2026-10-01: 'the results table still has issues with column width. the n column should be wider and wrap so values like T-056 with many n values don't take up a ton of vertical space. the result column could be narrower and wrap cleanly to make room'. The n cell of a result covering many cases (T-056, T-044, T-007) is one value per line today; it should set its values inline, wrapping within a wider column (ranges collapsed where consecutive). The Result column gives up the width: it is held to 411 px by four unbreakable formulas, so those must break cleanly (at relation and operator boundaries, or scroll inside the cell). This also answers think-b245 (tables scrolling sideways at 1024 and 768). Measure with measure_site_pages columns before and after; test_site_result_columns pins it.
