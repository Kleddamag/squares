---
type: is
id: is-01m3wrghxczsftw00my3be7mt3
title: "CI: the three behavioral shards run at their ceilings since the suite grew on 1 October"
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T22:14:13.163Z
updated_at: 2026-10-01T22:14:14.112Z
---
Hosted readings on 2026-10-01 after about 450 tests were added that day: suite_a 113.9 to 132.7 s over ten runs (geometric mean 118.5) against a 131 s ceiling and an 85.03 s record at 2,213 tests (now 2,665); suite_b 91 to 139 s (mean 109.9) against 154; suite_c 90 to 147 s (mean 126.9) against 154. jlevy/squares#277 failed shard A at 132.67 s with every test passing, and needed four full re-runs for runner noise (a PyPI timeout on macOS, partial-rerun refusals, the ceiling). devtools.suite_files packs files by recorded cost and falls back to a path hash for files absent from the record, so the day's new test files are unbalanced. Fix properly: rebuild the per-file cost record from a fresh hosted cohort and repartition; decide between a fourth shard and re-recorded ceilings with attribution (check_gate_budgets' ratchet); keep OR-14's two to two and a half minute surface. Read with: python -m devtools.read_tier_walls --tier suite_a --run-id …
