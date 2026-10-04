---
type: is
id: is-01m42sq21x618qdyrwkz6bfdwe
title: "#323: retarget to main, catch up, re-pin, regenerate, green CI"
kind: task
status: open
priority: 1
version: 2
labels: []
dependencies:
  - type: blocks
    target: is-01m42sq2jz809z5ccym3jj0qwy
parent_id: is-01m42sq026mszrdm4fwf5r8g8y
created_at: 2026-10-04T06:30:41.469Z
updated_at: 2026-10-04T06:30:42.015Z
---
After #305 merges: retarget base to main, merge main, resolve the DATA_REVISION conflict in packing/src/sqpack/release.py by re-pinning, regenerate composite-figure.json and bound-citations.json with their writers, run check_retained_json and --records, hosted CI green. Review pass per pr-review-requirements.
