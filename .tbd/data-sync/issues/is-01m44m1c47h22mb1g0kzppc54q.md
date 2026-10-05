---
type: is
id: is-01m44m1c47h22mb1g0kzppc54q
title: "Enforce OR-18: ceiling on added blob size and a scan for Git-history reads and blob-id gates in tools"
kind: task
status: open
priority: 2
version: 3
labels: []
dependencies: []
created_at: 2026-10-04T23:29:56.870Z
updated_at: 2026-10-05T07:13:28.166Z
---
OR-18 (jlevy/squares#345) states the rule but nothing fails a PR that breaks it. Add (1) a branch check that refuses added blobs over a few MB unless listed with a reason, and (2) a scan of packing/devtools and packing/src for git show/rev-parse REV:path reads and Git blob-id or commit gates on results. Existing frozen evidence is exempt per OR-16.

## Notes

Known violation on main: packing/devtools/check_n17_core_stress.py _frozen_bytes compares inputs via git show REV:path (found during the #347 rebuild).

2026-10-05 (PR 347 Review B, B5). The check_n17_core_stress.py site is lines 1554-1556 (_frozen_bytes on FROZEN_ROOT_REF, FROZEN_ENDPOINT_REF and FROZEN_FEATURE_REF, imported at line 47); it is main's code, carried unchanged into PR 347, whose body defers it to this bead.
