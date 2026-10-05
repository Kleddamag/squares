---
type: is
id: is-01m32dtsk35safvs7ney6xv5fp
title: Retain the Kleddamag n=17 artifact under the archive convention
kind: task
status: closed
priority: 1
version: 4
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m32dt0p76c4bvp3amxtmyt2p
child_order_hints:
  - is-01m32f1hew684z85fk6c5d9g2x
hold: null
hold_until: null
created_at: 2026-09-21T16:47:19.139Z
updated_at: 2026-10-05T05:35:35.241Z
started_at: 2026-10-05T05:34:33.044Z
closed_at: 2026-10-05T05:35:35.241Z
close_reason: "Adopted: E-n017-kleddamag-461300-99853-source-replay, its review of 2026-09-21 and the retained packet; n-017.md now carries the whole Kleddamag-to-Guzhou chain."
resolution: null
duplicate_of: null
---
Retain the external source following the convention the existing n=17 intake used (packing/resources/web/n17-weighted-certificates-2026-09-20/ with receipts), not an invented one: directory naming, receipts, hashing, the archive annotation census in packing/resources/README.md, and whatever .flowmarkignore requires for archived source.

Currently the clone lives only in the gitignored attic, so it is not retained at all and would not survive the container.
