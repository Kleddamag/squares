---
type: is
id: is-01m3x26at8m0fw1ew36dnbhaar
title: main's post-merge validate job fails 11 browser layout tests on Linux at 07f014386 (results and frontier tables)
kind: bug
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-02T01:03:23.972Z
updated_at: 2026-10-02T05:00:46.617Z
---
Run 36943941580 (Packing validation on main at 07f014386, the merge of #286 on top of #289), job validate, both attempts: tests/test_site_frontier_table.py::test_the_table_fits_its_track_at_1280_and_scrolls_in_its_wrap_below (table 1210.8 in a 1200 frame) and ten in tests/test_site_result_columns.py (credit 'Queuingtheorydotcom' breaks inside the name at 1024 and 768; a formula ends a line after ', the ...ng of 2' at 1280; a case list measures 232 against 224.8; the table is 938.2 wide at 1024), on index.html and all-results.html. Deterministic: a full re-run failed the same eleven. Not reproduced on macOS: at 07f014386 both files pass locally, 74 passed. The Pages deployment of the same commit succeeded and check_published_site passed 848 of 848, so the live site is not affected; this is the test surface.

What is known. The validate job normally skips these: when a pull-request run passed the exact tree it reuses 73 fast steps. 07f014386's tree was never a PR head (#286 was green at df0ef9f91 before #289 merged, #289 at 4f3b64cd2), so the whole surface ran in validate, with Chromium from 'playwright install --with-deps --only-shell chromium'. The previous main runs (48e7e5aa8, f25a85cb5) were green by reuse, so they say nothing about these tests in that job. Everything is about ten pixels wider than the macOS measurement, which points at text metrics (a face not applied when measured, or a different fallback) rather than at a rule in #286 or #289; neither PR's site.css diff touches the tables.

To decide: (1) whether the PR shards run these two files with a browser at all, or skip them (shard summaries show '6 skipped'); (2) run the two files in the validate job's environment on 48e7e5aa8 to see whether the failure predates #286/#289; (3) if it is the environment, make the validate job and the shards use one browser and font set; if it is the merge, bisect #286 against #289.

A merge whose tree equals a green PR head (a PR that is up to date with main) is reused and stays green, so this does not block such merges, but main shows red until it is fixed.

## Notes

Cause (2026-10-02, in progress on branch claude/validate-layout-tests): the eleven failures are
text metrics, not layout. Playwright's Chromium headless shell hints text at HINTING_FULL by
default (headless/public/headless_browser.h), which on Linux rounds every glyph's advance to
a whole pixel, where CoreText on macOS does not; the n column's 24ch measure read 232 px
(9 px a digit) against 224.8 (8.7), the frontier table 1210.8 in its 1200 track, and the
credit broke inside "Queuingtheorydotcom" at the 184 px floor. The faces are the page's own
web fonts, inlined. No pull-request job runs these two files with a browser: the four shards
install no Chromium (shard A reports "2062 passed, 6 skipped"), the frontend job runs only
check_frontend, and every main run since the pins (903b63a09 to 48e7e5aa8, and 8aaa411dc
after) reused a PR head's tree, so 07f014386 was the first Linux reading. Fix in hand: launch
with --font-render-hinting=none through devtools.preview_site.launch_chromium (identical
numbers on macOS), move the two files out of the quick lane into a fail-closed frontend step
"site table layout in Chromium", a workflow guard, and D-513. The Linux proof is the PR's own
frontend job, pending.
