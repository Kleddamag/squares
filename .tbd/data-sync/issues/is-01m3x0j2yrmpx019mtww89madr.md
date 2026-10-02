---
type: is
id: is-01m3x0j2yrmpx019mtww89madr
title: "Recent Results on the Overview: slim to the essentials and the table, with the detail on the Results page"
kind: task
status: open
priority: 2
version: 6
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3x0j1s4a1908p5zep249cd6
created_at: 2026-10-02T00:34:51.991Z
updated_at: 2026-10-02T05:25:30.703Z
---
Owner: 'the same for the New Results section on the overview, let's slim it down to the essentials and the table that is now there, but put more of the details on the results page itself. And integrate things so we don't state things repeatedly or give too much verbosity.' The Overview keeps a short lead and the existing table with its See all results action; the moved detail is integrated into the Results page's own introduction rather than appended.

## Notes

2026-10-02 08:20 UTC, follow-up draft PR #302 at edb0acc09 (claude/recent-results-lead, origin/main 8dbd2a77b merged): done, every gate run after the merge. Recent Results is one 88-word paragraph before its table (T-060, T-043, T-065 linked to rows; n = 21, 32, 45 to case records; the star legend; one filter sentence); README's recent-progress block is unshared (SHARED_BLOCKS is project-intro alone). Post-merge: focused non-browser tests 545 passed; browser site tests 305 passed through tests/site_browser.py; records 38/38; edit 53/53 (252.6 s, reported); browser floor 2/2; basedpyright 0/0/0; full preview_site clean; four shots of the Overview at 1280/390 light/dark clean, under attic/shots-lead. Hosted run at edb0acc09 pending; hand-back to the coordinator follows.
