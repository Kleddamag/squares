---
type: is
id: is-01m3nxpjnz3e1wq82nh7vtgsbk
title: "Coverage gate blind spots: sources with no 'dated' and sources missing from bibliography.yaml are treated as not recent"
kind: bug
status: open
priority: 2
version: 1
labels:
  - packing
  - results-register
dependencies: []
parent_id: is-01m3nrt5zy2g6dpegq1fbczpzg
created_at: 2026-09-29T06:30:12.414Z
updated_at: 2026-09-29T06:30:12.414Z
---
devtools.check_results.coverage_problems dates a case lower bound's evidence by its bibliography 'dated'. Sources without 'dated' (Goebel 1979, Kearney-Shiu 2002, Stromquist 2003, Bentz 2016, Friedman DS7) need a year fallback, and cited keys absent from bibliography.yaml ([Friedman DS7], [Ellsworth SVG], [GitHub n17 certificates 2026], [MacIver 2026 n17], [Kingbird n=5 SVG], [Kingbird n=29 SVG], [Schadt n=29 repository], [T-017]) cannot be dated at all; two are 2026 sources. Fail on an undatable key instead of passing silently, and add the missing keys. Found by the backfill agent, Session 161.
