---
type: is
id: is-01m45ey9dgaxd6105x6jc3snpz
title: "PR #347 B2 (Medium): regenerate the PR body from the head"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m45ex3dssa31jvkkz9bzpc6e
created_at: 2026-10-05T07:20:07.343Z
updated_at: 2026-10-05T07:20:07.343Z
---
Review B finding B2 on jlevy/squares#347 (https://github.com/jlevy/squares/pull/347#pullrequestreview-5411026138), at head 9d2f05582. The body no longer describes the branch: it says #307 stays open (closed 2026-10-05); the cost line says 13 commits / 780 blobs / 25.4 MB (now 25 commits, 4 merges, 821 blobs not on main, 31.8 MB, largest 2.0 MB); it links certificates/hosted-data.yaml (now packing/hosted/n17-x048-session-168-certificates.yaml), tag data-n17-... (now data/n17-x048-session-168-certificates-v1), and calls the hosted-data tool its own PR (merged as #349); Changes by Purpose still describes the minimal reader with a TODO (the census reads load_manifest/require since 8ff730a5c); bead table says 88 flagged classes (records say 87). Not mentioned: sqpack.hosted_data changes (require(..., repo=), the 403 upload message; 210515271, 85cd702c9), development.md's egress note, the merges of #349 and #353, the register change (B4), the operating-rules change (B3). Validation is at 4c246fd3b only. Fix: regenerate cost, manifest path, tag and state, 87 flags, infrastructure and register changes, and validation at the current head. Related: think-wcqs (Session 168 close, PR description).
