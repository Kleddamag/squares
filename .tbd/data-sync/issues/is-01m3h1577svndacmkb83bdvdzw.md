---
type: is
id: is-01m3h1577svndacmkb83bdvdzw
title: "BC-393: decide Kleddamag's s(17) > 232001/50000 natively for C4 (v1.1.0 loader, winning-subset atom, cap lift)"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-27-after-4640020-overnight.md
labels:
  - agenda-042
  - n17
dependencies: []
created_at: 2026-09-27T08:54:25.785Z
updated_at: 2026-09-27T08:54:25.785Z
---
Retarget of BC-386 after Kleddamag v1.1.0: load the 4.640020 certificate (280 point orbits; 2-of-3, 3-of-4 with coefficients [2,1,1,1], 3-of-5 and 4-of-7 thresholds; 30 winning-mask intersecting-rule orbits on 7 sites; 2,048 rows) into the parent-core interval route; add the winning-subset atom with its capacity-one lemma reviewed; lift the 8,192-site ceiling behind a byte budget; run all rows on 2 workers, about 1-6 CPU-h. A refusal is a refusal, never a negative.
