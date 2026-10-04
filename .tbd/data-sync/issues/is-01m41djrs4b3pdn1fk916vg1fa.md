---
type: is
id: is-01m41djrs4b3pdn1fk916vg1fa
title: "Deploy check: every published page carries complete link-preview metadata"
kind: task
status: open
priority: 2
version: 8
labels: []
dependencies: []
parent_id: is-01m41d7edgm9wc99zdrkaa5ehy
created_at: 2026-10-03T17:39:23.555Z
updated_at: 2026-10-04T02:55:21.491Z
---
Hold every published page to the metadata contract in a test and in check_published_site, so a page added later cannot ship without a preview; forwarders state what they carry by rule.

## Notes

Merged in jlevy/squares#319 (ebe5415a7) without its review's fixes; those are in jlevy/squares#334 (forwarders from their page's record; publish checks the assembled site). Closes when #334 merges.
