---
type: is
id: is-01m41djpvwrf0tc3tqyp1cnh43
title: "Page metadata: audit OpenGraph, Twitter and head metadata on every published page"
kind: task
status: open
priority: 2
version: 7
labels: []
dependencies: []
parent_id: is-01m41d7edgm9wc99zdrkaa5ehy
created_at: 2026-10-03T17:39:21.596Z
updated_at: 2026-10-04T02:18:45.045Z
---
Owner, 2026-10-03: https://jlevy.github.io/squares/papers/n11-optimality-review.html shows no OpenGraph image or details when shared. Audit every page the Pages build publishes (site pages, papers, the explainer, forwarders, case records, result fragments excluded as not pages): title, description, canonical, og:title/description/type/url/site_name/locale/image (+alt, width, height, type), twitter card tags, and favicon; list what each lacks.

## Notes

State 2026-10-04 02:20 UTC: jlevy/squares#319 at 5216f82e8, green; reviewed (think-u3ew): nothing blocking, two should-fix (forwarders' preview name and type from their destination; the deploy check run on the assembled site) and two nits being fixed in its worktree before push.
