---
type: is
id: is-01m41amx70t1g1zb8r3j2vnjc0
title: "Register: a declared superseded_by field, whole or in part, with its checks"
kind: task
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m41amwkn2j6r6jh6de7as7fb
created_at: 2026-10-03T16:48:07.904Z
updated_at: 2026-10-03T23:02:44.824Z
---
Schema field superseded_by on a result: a list of {result, extent: whole|part, what, since}. Checks: the named result exists, is not the entry itself, was registered no earlier, shares an n in scope; extent part requires what; a bound (kind in BOUND_KINDS) does not declare it, since its supersession is derived, unless the derivation agrees.

## Notes

State 2026-10-03 23:10 UTC: in jlevy/squares#315 at dc7a9acf4 (merged with main at 0ca18df47, re-pinned); MERGEABLE, hosted CI running on the head; no GitHub review yet, final agent review think-rf21 running. Closes when #315 merges.
