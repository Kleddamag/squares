---
type: is
id: is-01m3rdcdbds5nnn4a7czrz9kra
title: "Coordinate the #247 s(11) intake with PR #246's n = 11 optimality work"
kind: task
status: open
priority: 1
version: 5
labels:
  - packing
  - low-n
  - coordination
dependencies: []
created_at: 2026-09-30T05:42:45.356Z
updated_at: 2026-09-30T16:45:00.995Z
---
Two lines of n = 11 work are open at once. This bead keeps them from colliding.

## The two lines

- **jlevy/squares#246**, branch `codex/wand125-tools-review`, a separate agent. It does W7 work on the confirmed global optimality of Trump's eleven-square packing (T-060, S5/V4/C5; P0 `think-3i74`). It also registers wand125's tool claims as T-058 (the `B·UB(n)` ceiling) and T-059 (all 12,028 row minima of Kleddamag's certificate reproduced by wand125's exact `general_pose_tree` checker).
- **jlevy/squares#247 intake**, session 01BwdQAcVk5jwFycxVkLGNaK on branch `claude/determined-goldberg-ura2ed`. Ke Wang and Can Li (Fudan) report `s(11) > 3875000000/999999999`, Zenodo 23038546, CC-BY-4.0. Their certificate is Kleddamag's `global-certificate.json` with 13 threshold-charge orbits reweighted and the parent and core sides scaled by 999999999/1000000000. It improves T-037's 31/8 by 31/7999999992, about 3.9e-9. The intake runs three replays (the authors' two verifiers, Kleddamag's source sweeps, and this repository's native interval parent-core checker) and an independent mathematical review.

## The rules both lines follow

- **IDs.** The current branches collide: #246 uses T-058 to T-060, while #249 uses T-058 for Wang–Li. Contiguous-register validation prevents reserving T-061 in #249 now. Whichever PR merges second renumbers its new entries to follow the first; if #249 is second, Wang–Li becomes T-061. Update every reference and regenerate dependent records.
- **Shared files.** Both lines edit these:
  - `packing/frontier/n-011.md`
  - `packing/frontier/results.yaml`, `evidence.yaml` and `source-coverage.yaml`
  - `packing/resources/README.md`
  - `README.md` and `SYNOPSIS.md`
  - `packing/src/sqpack/release.py` (`DATA_REVISION`)

  #246 also changes `packing/devtools/gate-budgets.yaml`, `run_negative_controls.py` (snapshot cap 160 → 192 MiB) and `packing/src/sqpack/cli/validate.py`, which the #247 intake does not touch. Whichever branch merges second merges main into itself and resolves conflicts there. The #247 intake keeps its `n-011.md` change to one new subsection plus the verified-lower-bound line, so the conflict stays small. `DATA_REVISION` is re-pinned after the merge, never hand-merged.
- **Mathematical overlap.**
  - T-059's `general_pose_tree` row checker is a candidate third route for the Wang–Li certificate: its histogram claims every one of the 12,028 row minima equals 1000047559. Whether that checker accepts the scaled parameters is an open question for the #247 lane's report.
  - T-060 now confirms global optimality at Trump's exact value. Preserve Wang–Li as a separately credited historical lower bound when merging the case records.
  - Preserve the exact equality from T-060 and the earned V4/C4 evidence for the Wang–Li historical bound; do not replace the confirmed optimum with the weaker historical bound during conflict resolution.
- **Tools.** #247 generalises `devtools.verify_kleddamag_n11_native` so it reads the certificate's own container and parent sides, keeping the old certificate's behaviour byte-identical (`packing/devtools/verify_n11_parent_core_native.py` in progress). #246 does not modify that tool.

## Done when

Both PRs are merged with distinct contiguous IDs and complete source credit, `n-011.md` states both lines consistently, and each line's reply (#247 on the issue, #246 in its PR) points at the other where it matters.

## Notes

2026-09-30 correction: check_results requires contiguous register IDs, so T-061 could not be reserved. The Wang–Li result is T-058 on claude/determined-goldberg-ura2ed (jlevy/squares#249, commit 827e70b68). #246 also uses T-058 to T-060. Whichever PR merges second renumbers its new entries to follow the other's; if #249 is second, Wang–Li becomes T-061. The comment on #246 was edited to say so.

2026-09-30 PR246 completion update: T-060 now independently confirms global equality at Trump's exact endpoint, S5/V4/C5, after all2180 exclusions and ten capture nodes plus final Astra-max composition review. Final receipt eaad8f14; PR review https://github.com/jlevy/squares/pull/246#issuecomment-5912106554. The verified lower frontier is being promoted on that evidence. Wang–Li remains a separately credited historical improvement; preserve its intake and generalized native parent-core tool. Current origin/main was fetched and is included; PR249 was still open at the prior check. The later-merging PR must reconcile IDs as above and repin generated artifacts.

2026-09-30 packaging review: independently compared both branches. 36 shared changed paths include claim/evidence/source records, n-011, root reader docs, release pin, explainer renderer/tests, budgets/validate and generated atlas assets. Read-only merge analysis reports 39 text conflict hunks and six binary atlas conflicts. Merge completed PR246 first after its final packaging checks. PR249 remains draft; its own re-sweeps and full dispatch are still declared pending, so do not race or merge its ongoing work. Once its owner is ready, merge updated main into PR249, renumber Wang–Li to the next contiguous ID, preserve exact n11 equality and historical source credit, preserve T006/T056/T057 promotions, compose tooling semantics and the three-shard topology, regenerate artifacts, then repin DATA_REVISION to the merged data commit. Run affected records, release, explainer and atlas checks plus the hosted full checkpoint before its merge. Prior green checks against old main do not certify that combination.
