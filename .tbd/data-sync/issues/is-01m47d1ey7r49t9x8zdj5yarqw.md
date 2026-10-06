---
type: is
id: is-01m47d1ey7r49t9x8zdj5yarqw
title: "sqverify-fast: the crate in the tree is not the reviewed source; re-review the declared-net diff or pin the replay build"
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-10-06T01:25:23.015Z
updated_at: 2026-10-06T01:25:23.015Z
---
f007d7afd and 910b6b12c (the declared-net change, lemma N0; 910b6b12c never reviewed) mean a build of packing/sqverify_fast/ today has a source_sha256 outside REVIEWED_SOURCES, so the census --evidence template ('cargo build --release in sqverify_fast/') and T-094's replay entries describe a build the route review did not accept. T-097's replay ran the reviewed binary (af0871c0, source 7c49cf79, as at e020eb1e2). Either: a soundness re-review of the declared-net diff that adds its source digest to REVIEWED_SOURCES, or make the replay command name a build of the reviewed source (e.g. a git worktree at e020eb1e2). Until then every further carry of the route (T-082, T-090, T-091) must use a reviewed-source build.
