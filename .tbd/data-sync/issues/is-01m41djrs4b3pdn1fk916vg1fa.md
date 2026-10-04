---
type: is
id: is-01m41djrs4b3pdn1fk916vg1fa
title: "Deploy check: every published page carries complete link-preview metadata"
kind: task
status: open
priority: 2
version: 6
labels: []
dependencies: []
parent_id: is-01m41d7edgm9wc99zdrkaa5ehy
created_at: 2026-10-03T17:39:23.555Z
updated_at: 2026-10-04T01:03:53.593Z
---
Hold every published page to the metadata contract in a test and in check_published_site, so a page added later cannot ship without a preview; forwarders state what they carry by rule.

## Notes

State 2026-10-04 00:55 UTC: in jlevy/squares#319 at 5216f82e8; 29 checks pass, 28 skipped by design; merges cleanly into main at d303e9ef8. No review yet. Closes when #319 merges.
