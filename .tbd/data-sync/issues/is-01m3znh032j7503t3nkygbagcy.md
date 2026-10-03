---
type: is
id: is-01m3znh032j7503t3nkygbagcy
title: "Compiled exact kernel checker in Rust (lane X1): row cover sweep and collision facets behind the resident protocol"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/reviews/review-2026-10-02-n17-cost-reduction-performance.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-03T01:19:45.250Z
updated_at: 2026-10-03T01:19:45.250Z
---
Owner directive 2026-10-03: pursue primitive tool speedups aggressively and upgrade tooling. Rank 5 of the performance review (estimated 5-10x on the checker's integer parts). Standalone crate and harness in a separate worktree; bar is identical verdicts and counts on W7 and N1 row by row plus refusal of corrupted certificates. Integration as check_n17_subpattern --cover rust after F2's gmpy2 port. Started 2026-10-03 01:15 UTC.
