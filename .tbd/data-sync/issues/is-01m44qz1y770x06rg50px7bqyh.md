---
type: is
id: is-01m44qz1y770x06rg50px7bqyh
title: "Recapture the Kingbird catalogue after 2026-09-30 and diff it (blocked: kingbird.myphotos.cc denied by session egress policy)"
kind: task
status: in_progress
priority: 2
version: 3
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
hold: null
hold_until: null
created_at: 2026-10-05T00:38:35.207Z
updated_at: 2026-10-05T23:38:44.392Z
started_at: 2026-10-05T22:38:05.362Z
---
The latest capture is 2026-09-30; evand's mirror (site/www/data at 7cc5af6) is the same date. Recapture with the retained-capture tooling, run devtools.diff_kingbird_catalogue --before, and list any count where the catalogue moved. Needs kingbird.myphotos.cc allowed in the environment's network policy.

## Notes

Recaptured 2026-10-05 22:39:12Z by devtools.capture_kingbird_catalogue (attic/intake/kingbird-2026-10-05): same bytes as the 2026-09-30 capture (SHA-256 b99c3265...), same Last-Modified (Thu, 24 Sep 2026 15:18:52 GMT); diff_kingbird_catalogue: 0 counts changed, 0 below the record. source-coverage kingbird-current reviewed -> 2026-10-05 in bc4cd4311. Older-packings page recaptured (dated 2026-09-24). 98 retained witnesses compared with their live pictures (receipt known-best-packings/receipts/kingbird-2026-10-05-pictures.json). Nothing to import; n = 17 not involved.
