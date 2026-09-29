---
type: is
id: is-01m3p5wj25knm7rbx0g4a4tpvg
title: Measure and narrow documentation-checker test selection
kind: task
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m3nzy6gqfv60whzzvww0ffa0
created_at: 2026-09-29T08:53:16.996Z
updated_at: 2026-09-29T08:58:20.298Z
---
Observed during PR246 W7 quality follow-up: a narrow check_documentation.py generated-Cargo-output exclusion plus its regression and review prose selects dozens of workbench/certificate/search tests under packing-validate --push, after the previous selected suite already passed2039tests. Measure import/data fanout and preserve true callers and negative-control coverage while avoiding unrelated expensive replays. Do not weaken required test semantics or merely raise ceilings. Evidence: push-rustdoc.log in task scratch and PR246 hosted/local validation comments; full selector command retained in session tools.

## Notes

Bounded W7 audit 2026-09-29, source devtools/reachable_tests.py:90,220-245. Existing select_tests API on exact repair paths returns54/384files; checker-only54, regression-only54, review-prose-only53. All53 prose-selected files contain a raw WALKER_MARKERS substring; all-three minus prose is only packing/tests/test_documentation_links.py. Thus fanout is conservative lexical walker/dynamic-import policy, not actual documentation import closure. Examples: workbench test_capture_and_export.py202/212/385 scans tmp_path output; test_build_site_check.py119 walks tmp_path; n17_weighted_certificate_resume.py104 and parallel.py107/110/159 inspect temporary outputs. Four workbench and four certificate test modules enter this way. Genuine dependencies must remain: test_certificate_citations.py40 walks cases; n17_external_weighted_certificates.py46 dynamically loads fixed retained PACKET source. Recommended first slice: expose per-file selection reasons in reusable selector output, then AST-recognize only provably fixture-local walks (direct pytest tmp_path and conservatively proven aliases) while unknown/repository walks and dynamic imports stay universal. Preserve import closure/text mentions/config/parse fallbacks. Add negatives: real repo walker still selected; alias/unknown receiver remains selected; fixture-local walk is omitted for unrelated prose but selected for changed imported source; fixture-data edits and dynamically loaded packet edits still select true readers. Do not blacklist expensive files or drop walker fallback wholesale. Keep full PR/slow lanes unchanged. No source edits or heavyweight gates run; current push remains independent.
