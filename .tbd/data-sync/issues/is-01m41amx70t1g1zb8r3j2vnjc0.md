---
type: is
id: is-01m41amx70t1g1zb8r3j2vnjc0
title: "Register: a declared superseded_by field, whole or in part, with its checks"
kind: task
status: open
priority: 2
version: 6
labels: []
dependencies: []
parent_id: is-01m41amwkn2j6r6jh6de7as7fb
created_at: 2026-10-03T16:48:07.904Z
updated_at: 2026-10-04T01:03:48.087Z
---
Schema field superseded_by on a result: a list of {result, extent: whole|part, what, since}. Checks: the named result exists, is not the entry itself, was registered no earlier, shares an n in scope; extent part requires what; a bound (kind in BOUND_KINDS) does not declare it, since its supersession is derived, unless the derivation agrees.

## Notes

State 2026-10-04 00:55 UTC: in jlevy/squares#315 at 6c5036895, merged with main at d303e9ef8 and re-pinned; hosted CI running on the head (green at 03833707a); local push gate passes but for the two sandbox-only tests. Reviewed by a strong-tier agent (think-rf21). Closes when #315 merges.
