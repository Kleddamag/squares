---
type: is
id: is-01m3tj1ahf1j0sthhhdqd9fzys
title: Include newly cited provenance files in T-060 publication checkout
kind: bug
status: in_progress
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m3tf1nb0x65ybpkdj2d9y7gs
created_at: 2026-10-01T01:42:33.767Z
updated_at: 2026-10-01T01:44:02.152Z
---
Draft PR261 hosted optimality job failed because source-citation admission requires the retained kingbird provenance SVG and Kleddamag README, but sparse checkout only includes the n11 proof packet. Add the two exact archive files, declare render inputs and guard article archive citations against future omission. Keep the archive sparse; rerun only affected publication/scope checks.

## Notes

Hosted job110178312979 failed source-link admission for retained kingbird SVG. Root added exact kingbird SVG and Kleddamag README sparse patterns/push paths plus ARCHIVED_CITATION_SOURCES render inputs. Sol adds article-citation coverage guard and focused Pages contract tests. No geometry/proof change.
