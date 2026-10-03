---
type: is
id: is-01m41crc9rnphq77swdexdmgtx
title: "Merge #292, #298, #311 into main bottom-up once each is green and mergeable"
kind: task
status: open
priority: 1
version: 15
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
updated_at: 2026-10-03T17:27:11.136Z
---
Merge commits, not squash or rebase (think-fqut: GitHub's stacked merge rebases children). After each merge, retarget and check the next PR is still mergeable; refresh its CI.
