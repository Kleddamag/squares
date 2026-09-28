---
type: is
id: is-01m3n5xmgd6yhd9egf4wv0baq8
title: Re-pin wand125/square-packing-bounds past ad43d29 and take in the new rectangle-density certificates for n = 18 to 95
kind: task
status: open
priority: 1
version: 2
labels:
  - packing
  - wand125-update
  - review
dependencies:
  - type: blocks
    target: is-01m3n5y05cdnsnkspf7e4vg5jp
parent_id: is-01m3n5wh72rsqd2z97m8v1vv4q
created_at: 2026-09-28T23:34:37.837Z
updated_at: 2026-09-28T23:34:49.772Z
---
The September 27 packet (wand125-rectangle-certificates-2026-09-27/) pins 44 standing certificates, n = 18 to 78. wand125 now reports improvements for most n from 18 to 95 (e.g. s(37) >= 6.425 against the retained 32/5, s(91) >= 9.645 against Nagamochi's 9.602325), and the retained table in packing/resources/web/wand125-x-update-2026-09-28/acquisition/ lists 1929/200 at 91, rows at 86, 88-90, 94, 95, and raised values at many retained counts. Extend devtools.audit_wand125_rectangles to the new pin, retain each standing certificate's exact data, run the exact preflight on all, and register the reported bounds with credit (wand125, building on Tokoharu's solver and verifier), including bounds inherited by mass or monotonicity from smaller counts.
