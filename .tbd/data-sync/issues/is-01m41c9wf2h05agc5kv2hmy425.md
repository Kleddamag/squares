---
type: is
id: is-01m41c9wf2h05agc5kv2hmy425
title: "Integrity ceremony: remove the digest pins in four n = 11 tools inherited from main"
kind: task
status: open
priority: 3
version: 1
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels:
  - integrity
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-03T17:17:03.841Z
updated_at: 2026-10-03T17:17:03.841Z
---
The merge of origin/main at f864a576a brought in four n = 11 tools written on main before OR-16's amendment reached it. Each hashes its own source or pins digests of retained objects:
- check_n11_optimality_d4_incidence.py (5 sites)
- check_n11_optimality_local_two_radius.py (6)
- select_n11_field_minimum.py (4)
- n11_optimality_overview_figures.py (7, up from 1)
They are recorded in devtools/integrity-ceremony.yaml as inherited. Apply OR-16 as amended: identify by Git revision and path, keep pins only at real boundaries (the publisher's archived objects), and lower the baseline with --update. Coordinate with main, which owns these files, so the change does not fight upstream edits.
