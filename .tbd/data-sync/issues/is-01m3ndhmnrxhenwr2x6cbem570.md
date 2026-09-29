---
type: is
id: is-01m3ndhmnrxhenwr2x6cbem570
title: "Watch other researchers' repositories systematically: an external-source registry, a drift check, and a survey step in the research workflows"
kind: task
status: open
priority: 1
version: 1
labels:
  - packing
  - process
  - research
  - tooling
dependencies: []
parent_id: is-01m3n5wh72rsqd2z97m8v1vv4q
created_at: 2026-09-29T01:47:53.399Z
updated_at: 2026-09-29T01:47:53.399Z
---
Owner direction, 2026-09-29: research here should reference other people's repositories as a matter of course, so the record covers the latest tools and results in the field. Session 161 found the upstream repositories had moved past what the owner had been told (evand's s(21)/s(45) bundles, wand125's point-only and s(50) certificates, Guzhou0806's R067/R068, and now wand125/square-packing-tools), and the solver comparison had to report tools as unpublished that appeared hours later. Build (OR-1): (1) a registry of external repositories and their role (certificates, solvers, checkers, tables), e.g. packing/resources/external-sources.yaml under a softschema contract, seeded with evand/square-packing, wand125/square-packing-bounds, wand125/square-packing-density-bounds, wand125/square-packing-tools, tokoharu/square-packing-density-bounds, Kleddamag/11-squares-certified-bound, Kleddamag/17-squares-certified-bound, Guzhou0806/n17-square-packing, Guzhou0806/N17, Mira's and Fort's n17 repositories, sam-bee/squarl, and the non-GitHub sources the archive already tracks; each entry names its retained packet and pinned revision from acquisition/sources.json; (2) a devtool (e.g. devtools.check_external_sources) that asks each remote for its current head (git ls-remote), lists commits since the retained pin with their subjects, and flags new repositories linked from their READMEs; network-dependent, so an on-demand and session-start check rather than a CI gate; (3) a step in the W1 research-survey and W10 review-planning contracts (SYNOPSIS workflow entry contracts, packing/campaign/review-planning-oversight.md) to run it and dispose each new item as a bead; (4) decide with the owner whether this becomes an operating rule (OR-18). Also add a Related Work section to the solver comparison's successor documents that cites these repositories.
