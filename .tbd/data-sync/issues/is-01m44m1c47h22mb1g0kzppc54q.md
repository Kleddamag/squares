---
type: is
id: is-01m44m1c47h22mb1g0kzppc54q
title: "Enforce OR-18: ceiling on added blob size and a scan for Git-history reads and blob-id gates in tools"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-10-04T23:29:56.870Z
updated_at: 2026-10-04T23:29:56.870Z
---
OR-18 (jlevy/squares#345) states the rule but nothing fails a PR that breaks it. Add (1) a branch check that refuses added blobs over a few MB unless listed with a reason, and (2) a scan of packing/devtools and packing/src for git show/rev-parse REV:path reads and Git blob-id or commit gates on results. Existing frozen evidence is exempt per OR-16.
