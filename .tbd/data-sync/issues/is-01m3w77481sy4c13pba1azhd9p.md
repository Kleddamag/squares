---
type: is
id: is-01m3w77481sy4c13pba1azhd9p
title: "Frontier table: the packing icon in its own unnamed first column, slightly larger; cells vertically centred; the case number bold; Recent further left"
kind: task
status: in_progress
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T17:11:58.454Z
updated_at: 2026-10-01T19:04:59.269Z
---
Owner, 2026-10-01: 'in the frontier table https://jlevy.github.io/squares/frontier.html put the small icon on the far left, don't put it below the number. make it slightly bigger and then make sure everything is laid out cleanly and within each cell most results should be vertically centered'; 'the number of the record itself should always be bold'; 'the icon could be in its own unnamed column to left of the n'; 'and let's move recent column further left'.

## Notes

Owner added 2026-10-01: 'also in the frontier table the reported lower should have decimals as well as fractions etc so it's easier to read'.

2026-10-01, implemented on claude/site-polish-4-frontier (not pushed, no PR): 1254d79d1 (renderer, site.css, tests, probe), c8009450d (paper-design.md, Frontier table), e3b0ab5c6 (merge of origin/main at 3e5322f93). Columns are now: drawing (no visible heading, aria-label Packing), n (bold), Recent, Status, Best known packing, Verified upper, Reported lower, Verified lower, Gap, Records. Drawing 41.6 px -> 48.9 px (two lines of table text). Body cells vertical-align middle. Closed-form bounds and non-integer gaps carry a decimal from the exact form (exact_decimal), 267 cells. Table fits its 1200 px track at a 1280 window (was 1281.6, 81.6 past). frontier.html 4,168,556 -> 4,183,093 bytes; ceiling 4,194,304, so 11,211 bytes of room remain (was 25,748, not the ~92 KB think-k8xp assumed). Unused KPress data-col/data-col-index attributes are 128,050 bytes of the page: the lever for think-k8xp. Not done: no phone card layout exists for this table (it scrolls sideways at 390); print still clips the table's right columns, as before.
