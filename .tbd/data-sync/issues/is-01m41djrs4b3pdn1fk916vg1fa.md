---
type: is
id: is-01m41djrs4b3pdn1fk916vg1fa
title: "Deploy check: every published page carries complete link-preview metadata"
kind: task
status: open
priority: 2
version: 7
labels: []
dependencies: []
parent_id: is-01m41d7edgm9wc99zdrkaa5ehy
created_at: 2026-10-03T17:39:23.555Z
updated_at: 2026-10-04T02:18:45.972Z
---
Hold every published page to the metadata contract in a test and in check_published_site, so a page added later cannot ship without a preview; forwarders state what they carry by rule.

## Notes

State 2026-10-04 02:20 UTC: jlevy/squares#319 at 5216f82e8, green; reviewed (think-u3ew): nothing blocking, two should-fix (forwarders' preview name and type from their destination; the deploy check run on the assembled site) and two nits being fixed in its worktree before push.
