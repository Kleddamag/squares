---
type: is
id: is-01m44qz1y770x06rg50px7bqyh
title: "Recapture the Kingbird catalogue after 2026-09-30 and diff it (blocked: kingbird.myphotos.cc denied by session egress policy)"
kind: task
status: open
priority: 2
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
created_at: 2026-10-05T00:38:35.207Z
updated_at: 2026-10-05T00:38:35.207Z
---
The latest capture is 2026-09-30; evand's mirror (site/www/data at 7cc5af6) is the same date. Recapture with the retained-capture tooling, run devtools.diff_kingbird_catalogue --before, and list any count where the catalogue moved. Needs kingbird.myphotos.cc allowed in the environment's network policy.
