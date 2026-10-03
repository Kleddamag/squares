---
type: is
id: is-01m41cwdw4nr7wrkpgz02j7yzd
title: "Import #316: evand's s(k² − 4) = k for every k ≥ 5 (external certificate + Lean reduction)"
kind: task
status: open
priority: 1
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m41csdc2gp36ry5p6n7c2x2y
created_at: 2026-10-03T17:27:11.491Z
updated_at: 2026-10-03T19:08:50.191Z
---
New registration request opened 2026-10-03 17:19 UTC by evand, not yet tracked in result-requests.yaml. Runbook stages 1-3 now (acknowledge, retain with acquire_source, register as reported at V0 with a request entry), then stage 4 replays like T-064's Valid7 (qx2/zmx2 family) and the Lean build. Related: think-0g4t (BC-396 transfer to n = 45, the k = 7 member).

## Notes

2026-10-03 19:15 PR #322 opened (claude/import-316-k2m4 @c28ba66c9): T-081 Daniel's s(k^2-4)=k for k>=5 at V0/C1, S4; packet evand-square-packing-2026-10-03 at 2eb1545; verify.sh passes (18 s); bentz4_of_validTilt9 built (standard axioms); replay plan 14 shards, 226.48 recorded CPU-h. Seven Valid9 runners (claude/valid9-r1..r7, sessions 01QWRcePjvFnBQ2gribQA1Tp, 01N1Tt8yvrsJHjdY63edJh4L, 01VQFKbxTY477HmkhYYF1Zro, 01Nr8hpjuK3LcH8ypbTU62jJ, 01QSx8AQS6sk1cHSYC7bZHUK, 01K3CtmjUv1YzkZ7q9swhiXg, 01494iN8U2s54TUTCLxkSCDH) running shards 1-14 since 18:30. After all: merge runner branches, plan_valid9_replay compare, record replay → V3/C3, final reply on #316 tagging @evand.
