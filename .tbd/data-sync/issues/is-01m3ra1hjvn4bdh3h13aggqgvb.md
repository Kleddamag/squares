---
type: is
id: is-01m3ra1hjvn4bdh3h13aggqgvb
title: Consolidate proof verification and decouple the validation pipeline
kind: epic
status: in_progress
priority: 1
version: 14
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3qw8b5q2xgjp85cxx24134c
child_order_hints:
  - is-01m3razbt8p1kktnnzvqbdjv74
  - is-01m3razc6hwms10f04btg028vv
  - is-01m3rb0sr8p2xn3m96v3cs96cx
  - is-01m3rb0t4zqdze43drjkx9cqx2
  - is-01m3rbmdd2knptgfj454y4exak
  - is-01m3rkt99p9bxh8csj2v58nh9p
  - is-01m3s6fg7h4a51s61zzk4k37qp
  - is-01m3s98kgj0s9pg4ybk685nc7t
  - is-01m3sk1aq5e7wm2hzghg3wf499
created_at: 2026-09-30T04:44:23.504Z
updated_at: 2026-09-30T16:42:02.261Z
---
User requested audit of ~60000-line PR. At0dda2856e diff vs886b1783a:59419 additions483 deletions240 files,32 binary. Added lines: retained source/receipts30071; sessions/logs/accounting9710 (7212 log lines); implementation/config8153; CI/config1130; tests4804; goldens/fixtures1844; docs/registers3705; atlas text2. Actual n11 checkers4395 and tests991. At least3338 lines duplicate result.json exactly in stdout.json. Three large JSON receipts total15240 lines. Review code duplication and separate mathematical proof audit from earlier rectangle-tools and CI scope; compress bulky raw results/logs deterministically with concise summaries and preserved decoded identities/replay bindings. Do not discard unique evidence, blindly change frozen checker hashes, or weaken independent acceptance. Read-only size audit complete; reduction not yet implemented.

## Notes

Implemented shared field geometry/runner and independently reviewed integer and indexed exact kernels; generic exclusion, capture, local isolation and final composition remain separate contracts. Deterministic compression has removed 93,389 plaintext ledger lines while preserving decoded bytes and acceptance credit. Final composition is implemented with missing-premise refusal and observed-execution disclosure. Current work finishes the remaining proof executions and complete audit; it does not require a blanket verifier rewrite, a new workflow engine, or a PR-history split. The optional Rust rectangle backend is complete but slower on the matched external probe; measured performance follow-up remains think-3cwg and cannot block T-060. Keep the planning baseline in the spec distinct from current acceptance in the mathematical review.

2026-09-30: T-060 and within-PR integration are complete at the previously green 180326e81. The new first-principles overview separates proof execution, evidence composition and CI. The 66c37b255 diagnostic closes think-r97y negatively, with complete retained evidence. Packaging remains focused: think-e2ot for a thin fresh replay entry point, think-nxd8 for shared diagnostic frontier admission, and think-d15x for actual cross-PR merge/ID reconciliation. Accepted proof sources and receipts remain unchanged.
