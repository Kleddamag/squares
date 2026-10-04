---
type: is
id: is-01m42xhs1mmqpv12d1j74rrvey
title: Site pages link shared hashed assets (phase 1)
kind: task
status: in_progress
priority: 1
version: 6
delegate: claude-code@vm
labels: []
dependencies:
  - type: blocks
    target: is-01m42xhvh42fy1x77cd5j8c0dc
  - type: blocks
    target: is-01m42xhxk4awqq1jmgzykwdct1
  - type: blocks
    target: is-01m42xhzkhgcrhah1b41gpjxf4
parent_id: is-01m42xfwp06kzm2b390dx1cw17
hold: null
hold_until: null
created_at: 2026-10-04T07:37:42.708Z
updated_at: 2026-10-04T09:22:30.558Z
started_at: 2026-10-04T07:37:53.883Z
---
kpress_page pages (overview job) link assets/ files: site_assets.py bundle, write_site/--check, assert_fetches_only_assets, rebase_links script src, check_published_site.asset_checks, measure faces via inlined_from, docs (paper-design Shared Assets).

## Notes

PR https://github.com/jlevy/squares/pull/341 (draft). Local push gate green apart from the 2 sandbox-only process-group tests.
