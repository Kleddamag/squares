---
type: is
id: is-01m3nqe9wy5qt3wyc6q1my6t8m
title: "Explainer: star caption renders 'since August 2026' while the rule is 22 August on the verified lane; the other-results footnote omits later raises at n = 12 and 17"
kind: bug
status: closed
priority: 1
version: 2
labels:
  - packing
  - documentation
  - wand125-update
dependencies: []
parent_id: is-01m3neehm7hq4apdvzg9925738
created_at: 2026-09-29T04:40:49.822Z
updated_at: 2026-09-29T05:11:46.666Z
closed_at: 2026-09-29T05:11:46.666Z
close_reason: Fixed in b7e421652 on claude/magical-davinci-ueqmu1-docs-refresh
resolution: null
duplicate_of: null
---
packing/devtools/templates/explainer-article.md:195-197 caption uses RECENT_SINCE_MONTH ('August 2026', render_explainer.py:2236); render the exact RECENT_SINCE date and say 'a verified lower bound'. :124-128 and footnote :893-896: note that others have since raised n = 12 (Evan Daniel) and n = 17 (Kleddamag, Guzhou0806). Inventory §3.8.
