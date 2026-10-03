---
type: is
id: is-01m41crc9rnphq77swdexdmgtx
title: "Merge #292, #298, #311 into main bottom-up once each is green and mergeable"
kind: task
status: open
priority: 1
version: 16
labels:
  - merge
dependencies:
  - type: blocks
    target: is-01m3wyajwc1tbyq4f2rbhjhqdh
  - type: blocks
    target: is-01m3ys19bfzkjp4yrp53ndbc8j
  - type: blocks
    target: is-01m3ys1amqty0xqzyhx0avfssz
  - type: blocks
    target: is-01m3ys1by49bhke0fd8twcff5m
  - type: blocks
    target: is-01m3ys1ddgc8ydwg9vk5bpfrkp
  - type: blocks
    target: is-01m3ys1eyvhd71mxr5nec8w8rs
  - type: blocks
    target: is-01m3ys1fz0a6qc5j6vny00wb2p
  - type: blocks
    target: is-01m3ys10dq5xc2gjw4m5dn086t
  - type: blocks
    target: is-01m3ys11k8svw9337p3gsj48rf
  - type: blocks
    target: is-01m3ys13d4m4f3nsy0mq964m19
  - type: blocks
    target: is-01m3ys14zf9kaxrjz44ksfrhmd
  - type: blocks
    target: is-01m3ys167s43cwbqecd86pvw5k
  - type: blocks
    target: is-01m3ys17qmmqsa0pby2rg6x2hk
  - type: blocks
    target: is-01m3xrx8b86kp8t1k6gj71p4ej
parent_id: is-01m41cr1mz526vz5b2a5e4z100
created_at: 2026-10-03T17:24:58.807Z
updated_at: 2026-10-03T17:36:23.438Z
---
Merge commits, not squash or rebase (think-fqut: GitHub's stacked merge rebases children). After each merge, retarget and check the next PR is still mergeable; refresh its CI.

## Notes

2026-10-03 18:00 Owner: stabilize and land now; new imports after. Scope freeze sent to the records lane (#298), SP2 (#311) and the stack-merge lane (#292).
Merge procedure (main is unprotected; delete_branch_on_merge is true, and GitHub restack-rebases children when a base branch is deleted, think-fqut):
1. #292 green → retarget #298's base to main FIRST (gh pr edit 298 --base main), then merge #292 with a merge commit.
2. #298 green against main → retarget #311's base to main FIRST, then merge #298 with a merge commit. Our designated branch is deleted on merge; restart it from main for follow-ups.
3. #311 green → merge with a merge commit.
4. Then final issue replies from main with check_requests --draft N (think-hen3), evand's #316, #256 and #238 first, then close the closeable ones.
Follow-up branch after landing: n82 (T-076), n83 (T-073), T-077, T-046 leftovers, Valid7 w-shards, census evidence (think-3ok2), #316 import (IM316 branch claude/import-316-k2m4), and any newer issues.
