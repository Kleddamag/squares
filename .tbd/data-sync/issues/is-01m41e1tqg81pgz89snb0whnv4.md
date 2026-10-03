---
type: is
id: is-01m41e1tqg81pgz89snb0whnv4
title: "After landing: verify the Pages deploy end to end and the new results on the live site"
kind: task
status: open
priority: 1
version: 1
labels:
  - merge
  - site
dependencies: []
parent_id: is-01m41cr1mz526vz5b2a5e4z100
created_at: 2026-10-03T17:47:37.072Z
updated_at: 2026-10-03T17:47:37.072Z
---
Owner, 2026-10-03: double-check everything deploys end to end and is visible on the website. After each merge to main: the 'Certificate page' workflow (pages.yml) run on main passes prepare, build, deploy and verify-deployment (check_published_site). Then on https://jlevy.github.io/squares/: Recent Results and all-results.html show T-066..T-079 with the right rungs and credits (wand125, Evan Daniel, squarepacker, Levy); the frontier shows 77 proved; case records cases/59.html, 60, 61, 77, 78, 97, 12 show the new bounds and the formula-wrap fix; the README intro example reads 5.7975. Record the run id and what was checked.
