---
type: is
id: is-01m3ra1hjvn4bdh3h13aggqgvb
title: Consolidate proof verification and decouple the validation pipeline
kind: epic
status: in_progress
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3qw8b5q2xgjp85cxx24134c
child_order_hints:
  - is-01m3razbt8p1kktnnzvqbdjv74
  - is-01m3razc6hwms10f04btg028vv
  - is-01m3rb0sr8p2xn3m96v3cs96cx
  - is-01m3rb0t4zqdze43drjkx9cqx2
created_at: 2026-09-30T04:44:23.504Z
updated_at: 2026-09-30T05:04:27.758Z
---
User requested audit of ~60000-line PR. At0dda2856e diff vs886b1783a:59419 additions483 deletions240 files,32 binary. Added lines: retained source/receipts30071; sessions/logs/accounting9710 (7212 log lines); implementation/config8153; CI/config1130; tests4804; goldens/fixtures1844; docs/registers3705; atlas text2. Actual n11 checkers4395 and tests991. At least3338 lines duplicate result.json exactly in stdout.json. Three large JSON receipts total15240 lines. Review code duplication and separate mathematical proof audit from earlier rectangle-tools and CI scope; compress bulky raw results/logs deterministically with concise summaries and preserved decoded identities/replay bindings. Do not discard unique evidence, blindly change frozen checker hashes, or weaken independent acceptance. Read-only size audit complete; reduction not yet implemented.
