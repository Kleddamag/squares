---
type: is
id: is-01m3rdcdbds5nnn4a7czrz9kra
title: "Coordinate the #247 s(11) intake with PR #246's n = 11 optimality work"
kind: task
status: open
priority: 1
version: 2
labels:
  - packing
  - low-n
  - coordination
dependencies: []
created_at: 2026-09-30T05:42:45.356Z
updated_at: 2026-09-30T11:28:02.642Z
---
Two lines of n = 11 work are open at once. This bead keeps them from colliding.

## The two lines

- **jlevy/squares#246**, branch `codex/wand125-tools-review`, a separate agent. It does W7 work on the claimed global optimality of Trump's eleven-square packing (T-060, V0/C1, S5; P0 `think-3i74`). It also registers wand125's tool claims as T-058 (the `B·UB(n)` ceiling) and T-059 (all 12,028 row minima of Kleddamag's certificate reproduced by wand125's exact `general_pose_tree` checker).
- **jlevy/squares#247 intake**, session 01BwdQAcVk5jwFycxVkLGNaK on branch `claude/determined-goldberg-ura2ed`. Ke Wang and Can Li (Fudan) report `s(11) > 3875000000/999999999`, Zenodo 23038546, CC-BY-4.0. Their certificate is Kleddamag's `global-certificate.json` with 13 threshold-charge orbits reweighted and the parent and core sides scaled by 999999999/1000000000. It improves T-037's 31/8 by 31/7999999992, about 3.9e-9. The intake runs three replays (the authors' two verifiers, Kleddamag's source sweeps, and this repository's native interval parent-core checker) and an independent mathematical review.

## The rules both lines follow

- **IDs.** #246 holds T-058, T-059 and T-060. The #247 result takes **T-061**. Neither line renumbers the other's IDs. If a merge meets a new collision, the later branch takes the next free number and says so in the entry's notes, as T-059's already does.
- **Shared files.** Both lines edit these:
  - `packing/frontier/n-011.md`
  - `packing/frontier/results.yaml`, `evidence.yaml` and `source-coverage.yaml`
  - `packing/resources/README.md`
  - `README.md` and `SYNOPSIS.md`
  - `packing/src/sqpack/release.py` (`DATA_REVISION`)

  #246 also changes `packing/devtools/gate-budgets.yaml`, `run_negative_controls.py` (snapshot cap 160 → 192 MiB) and `packing/src/sqpack/cli/validate.py`, which the #247 intake does not touch. Whichever branch merges second merges main into itself and resolves conflicts there. The #247 intake keeps its `n-011.md` change to one new subsection plus the verified-lower-bound line, so the conflict stays small. `DATA_REVISION` is re-pinned after the merge, never hand-merged.
- **Mathematical overlap.**
  - T-059's `general_pose_tree` row checker is a candidate third route for the Wang–Li certificate: its histogram claims every one of the 12,028 row minima equals 1000047559. Whether that checker accepts the scaled parameters is an open question for the #247 lane's report.
  - If T-060's global optimality is confirmed, `s(11)` is closed at Trump's value. The Wang–Li bound then remains a historical lower bound, and the case record says so.
  - Neither line changes the verified lower bound except through T-061 at its earned rung.
- **Tools.** #247 generalises `devtools.verify_kleddamag_n11_native` so it reads the certificate's own container and parent sides, keeping the old certificate's behaviour byte-identical (`packing/devtools/verify_n11_parent_core_native.py` in progress). #246 does not modify that tool.

## Done when

Both PRs are merged with T-058 to T-061 intact, `n-011.md` states both lines consistently, and each line's reply (#247 on the issue, #246 in its PR) points at the other where it matters.

## Notes

2026-09-30 correction: check_results requires contiguous register IDs, so T-061 could not be reserved. The Wang–Li result is T-058 on claude/determined-goldberg-ura2ed (jlevy/squares#249, commit 827e70b68). #246 also uses T-058 to T-060. Whichever PR merges second renumbers its new entries to follow the other's; if #249 is second, Wang–Li becomes T-061. The comment on #246 was edited to say so.
