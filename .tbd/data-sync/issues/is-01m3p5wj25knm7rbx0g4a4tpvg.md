---
type: is
id: is-01m3p5wj25knm7rbx0g4a4tpvg
title: Measure and narrow documentation-checker test selection
kind: task
status: open
priority: 2
version: 4
labels: []
dependencies: []
parent_id: is-01m3nzy6gqfv60whzzvww0ffa0
created_at: 2026-09-29T08:53:16.996Z
updated_at: 2026-09-29T17:57:48.549Z
---
Observed during PR246 W7 quality follow-up: a narrow check_documentation.py generated-Cargo-output exclusion plus its regression and review prose selects dozens of workbench/certificate/search tests under packing-validate --push, after the previous selected suite already passed2039tests. Measure import/data fanout and preserve true callers and negative-control coverage while avoiding unrelated expensive replays. Do not weaken required test semantics or merely raise ceilings. Evidence: push-rustdoc.log in task scratch and PR246 hosted/local validation comments; full selector command retained in session tools.

## Notes

Session 163 Sol read-only diagnosis: push since4296edce selects65/386 behavioral test files, not the whole suite. Six changed Python paths select56;20 prose/record paths select62; union65. WALKER_MARKERS substring matching adds44 files that are otherwise unreachable. Confirmed false positives include __import__ in an attack string, importlib.metadata.version, tmp_path-only globs and rglob in comments; actual repo walkers must remain covered. Next safe slice: AST/context-aware exclusion of proven non-repo uses, with positive repository/dynamic-import selector controls. Rank actual gate costs before implementing; current buffered log does not attribute elapsed time. No gate weakened.
