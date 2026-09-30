---
type: is
id: is-01m3ra1hjvn4bdh3h13aggqgvb
title: Reduce PR246 review surface while preserving proof evidence
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/reviews/review-2026-09-29-n11-optimality.md
labels: []
dependencies: []
parent_id: is-01m3qw8b5q2xgjp85cxx24134c
created_at: 2026-09-30T04:44:23.504Z
updated_at: 2026-09-30T04:44:23.504Z
---
User requested audit of ~60000-line PR. At0dda2856e diff vs886b1783a:59419 additions483 deletions240 files,32 binary. Added lines: retained source/receipts30071; sessions/logs/accounting9710 (7212 log lines); implementation/config8153; CI/config1130; tests4804; goldens/fixtures1844; docs/registers3705; atlas text2. Actual n11 checkers4395 and tests991. At least3338 lines duplicate result.json exactly in stdout.json. Three large JSON receipts total15240 lines. Review code duplication and separate mathematical proof audit from earlier rectangle-tools and CI scope; compress bulky raw results/logs deterministically with concise summaries and preserved decoded identities/replay bindings. Do not discard unique evidence, blindly change frozen checker hashes, or weaken independent acceptance. Read-only size audit complete; reduction not yet implemented.
