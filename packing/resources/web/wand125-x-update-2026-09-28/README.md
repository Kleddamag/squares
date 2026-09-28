# wand125 Update on X, Supplied 2026-09-28

This packet keeps two messages from wand125 (X: `@wand_125`, GitHub: `wand125`) to the
project owner, and a byte capture of the lower-bound table they link.
Its citation key is **[wand125 X update 2026-09-28]**.

The messages report results this repository has not yet taken in, and list the tools
wand125 built for them.
Nothing here is registered.
Each claim below is a pointer to the source to acquire and replay, not evidence for a
bound; the follow-up beads under `think-1an7` own the intake.

## Source

| Field | Value |
| --- | --- |
| Author | wand125, whose rectangle-density work builds on Tokoharu’s solver and verifier |
| Channel | X (Twitter); the first message is addressed to Joshua Levy |
| Supplied | 2026-09-28, pasted by the owner into a session in two parts; no status URL or publication time was given |
| Messages | [`supplied-messages.txt`](supplied-messages.txt), the supplied text unedited |
| Linked table | `claude.ai/artifact/TUa8v1nJWbQpKAokfLMTJy`, “Who Holds Each Lower Bound”, retained as [`acquisition/lower-bound-table-2026-09-28.html`](acquisition/lower-bound-table-2026-09-28.html) |
| Table SHA-256 | `560ec3d6bc2d2e52aee378c789e3008b9ae252d282ee62681fa8db57bbfc5837`, in [`acquisition/lower-bound-table-2026-09-28.sha256`](acquisition/lower-bound-table-2026-09-28.sha256) |
| Linked repositories | [wand125/square-packing-bounds](https://github.com/wand125/square-packing-bounds) (certificates); [wand125/square-packing-density-bounds](https://github.com/wand125/square-packing-density-bounds) (fork of Tokoharu’s solver) |

The table was read on 2026-09-28 at about 23:31 UTC through the Artifact tool, which
saved the page as served; the retained file is those bytes.
Besides the artifact runtime’s scripts, the page carries bilingual English and Japanese
prose, a 100-row table and two charts.

## What the Messages Report

Each row gives the claim as stated, what this repository recorded on 2026-09-28 (its
state at `510dab45`), and the bead that owns it.

| Claim | Register on 2026-09-28 | Bead |
| --- | --- | --- |
| evand proves `s(21) = 5` | Reported and verified `5000/1001` from **[evand square-packing 2026]** at `167d842c`; upper bound the `5 × 5` grid | `think-l6la` |
| evand proves `s(45) = 7` | Reported `1391/200` (wand125 rectangles), verified `6.830952` (Nagamochi); upper bound the `7 × 7` grid; this project’s own `k = 7` transfer was planned as `BC-396` (`think-0g4t`) | `think-l6la` |
| wand125’s point-only route to `s(21) = 5` from evand’s support, no priority claimed, with a Lean 4 reduction to `minSide 21 = 5` from one capture hypothesis (`point_n21_L5/`) | Not retained | `think-ifsv` |
| Rectangle-density bounds improve most counts from `n = 18` to `95`, e.g. `s(37) ≥ 6.425` and `s(91) ≥ 9.645` | 44 certificates from `n = 18` to `78` retained at `ad43d29`; reported at `n = 37` is `32/5`, at `n = 91` Nagamochi’s `9.602325`; only `n = 27` and `31` replayed, `28` by monotonicity | `think-kg79`, `think-20mv` |
| `s(50) ≥ 7.35`: coverage reaches `1.0000000005`, below the `1.0001` margin `verify.cpp` requires, so the certificate ships with its own verifier and a replay bundle | Reported `7.317426` (Green, via **[Friedman DS7]**), verified `7.082763` (Nagamochi) | `think-nnlg` |
| `s(50) ≥ 7.40` (`certificates/mixed_n50_L740`), from Green’s approach for the `N = k² + 1` family, passing 201 angles and a full replay with the same verifier | As above | `think-nnlg` |
| Next targets `n = 65` (Green `8.2900`) and `n = 82` (Green `9.2667`) | Reported Green’s `8.289966` and `9.266734`; `BC-394` (`think-pr2b`) plans this project’s own `n = 82` and `n = 50` ladders | `think-nnlg` |

The known-best PDF draws each open case’s verified lower bound, which is why it shows
`5000/1001` at `n = 21` and Nagamochi’s value at `n = 45` while wand125’s certificates
sit in the reported lane. `think-knrl` asks whether the figure should also draw reported
bounds awaiting replay.

## The Retained Table

The page lists, for `n = 1` to `100`, a lower bound, exact form, holder, year, best
packing, packer, gap and previous holder.
It attributes 49 rows to “this work + tokoharu”, meaning wand125’s certificates built
with Tokoharu’s solver.

Three things about it matter before it is used:

- **Its rows are newer than its stated data state.** The footer says the bounds were
  read from this repository at `db3f5f3` (2026-09-25) with wand125’s 26 September
  certificates added, but the rows already give `s(21) = 5` and `s(45) = 7` to evand and
  `37/5` at `n = 50`.
- **It credits a bound at `n = 17` that this repository has not seen:**
  `233009/50000 = 4.660180` to Guzhou0806, “was 4.6400 (Kleddamag)”, above the register’s
  verified `466001/100000`. The footer still cites Guzhou0806’s R052 at `462003/100000`,
  so the page disagrees with itself; `think-mqd7` finds the source.
- **Its “this work” is wand125’s.** The page is written in the first person by the
  table’s authors, so “this work” and “here” refer to wand125’s repositories, not to
  this one.

`think-insq` owns the row-by-row reconciliation against the case records.

## Tools and Techniques

The first message closes with seven groups of tools, most not yet public.
They are in [`supplied-messages.txt`](supplied-messages.txt) as written.
Two bear directly on this repository’s own ladders:

- **A ceiling on any certificate.** With core side `B`, no certificate reaches
  `L ≥ B · UB(n)`, because the best known packing scaled by `B` holds `n` disjoint cores.
  wand125 caps ladder targets there.
- **Inheritance by mass.** A certificate whose total mass is below `k` also bounds every
  count `k` and above, which the September 27 packet already applies at `n = 77`.

`think-v2lv` evaluates the transfer and speed-up techniques for adoption, and
`think-64le` compares Tokoharu’s and wand125’s solver with this repository’s certificate
tools and chooses a path forward.
`think-unkw` runs the documentation and atlas refresh once the intakes land.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
