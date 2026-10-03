# wand125 Rectangle-Density Certificates Pinned 2026-10-01

This packet pins
[wand125/square-packing-bounds](https://github.com/wand125/square-packing-bounds) at
`1a25a5e`, which raised 34 of the 50 standing rectangle-density certificates that the
[September 28 packet](../wand125-rectangle-certificates-2026-09-28/README.md) pinned at
`39d8ecc` and added three counts, `n = 87`, 90 and 93. It keeps this repository’s exact
preflight of all 53 standing certificates.
Its Frontier key is **[wand125 rectangle bounds 2026-10-01]**, and the request to
register the certificates is
[jlevy/squares#281](https://github.com/jlevy/squares/issues/281).

The two earlier packets stay as the records at `ad43d29` and `39d8ecc`, under
**[wand125 rectangle bounds 2026]** and **[wand125 rectangle bounds 2026-09-28]**, with
their receipts. This packet retains only what is new at `1a25a5e` and reads everything
else from them. The same revision also added the covers for `s(59) = 8` and `s(77) = 9`,
a point-only `s(61) = 8` bundle and seven mixed rectangle-measure certificates.
None is in Tokoharu’s format; they are taken in separately, in the packet
`wand125-point-and-mixed-2026-10-01`, and this packet pins them by digest only.

## Source and Pin

| Field | Value |
| --- | --- |
| Address | <https://github.com/wand125/square-packing-bounds> |
| Revision | `1a25a5ed745fdd905a52f48fcc48150a0669032d`, branch `main`, tree `d9a5b5e0b32f01eb643c7f701d081b45d0be9a1d` |
| Committed | 2026-10-01T21:10:40Z, stamped `2026-10-02T06:10:40+09:00` in the commit; the 37 certificates new or raised since `39d8ecc` arrived in 15 commits from 2026-09-29T00:29Z to 2026-10-01T15:50Z |
| Retrieved | 2026-10-02T00:18:25Z, a depth-1 clone whose `main` was this revision |
| Requested | jlevy/squares#281, opened by wand125 on 2026-10-01T21:13:37Z |
| Licence | MIT, copyright wand125 2026, byte-identical to the September 27 packet’s [`LICENSE`](../wand125-rectangle-certificates-2026-09-27/wand125-rectangles/LICENSE) |
| Tags, releases, submodules, Git LFS | none: `git ls-remote` lists only `refs/heads/main`, the GitHub API listed no tags and no releases at 2026-10-02T00:28Z, and the tree has no `.gitmodules` or `.gitattributes` |
| Upstream tree | 2,897 files, 1,075 MB, each pinned by SHA-256 in [`acquisition/upstream-tree.sha256`](acquisition/upstream-tree.sha256) |
| Retained here | 149 files under [`wand125-rectangles/`](wand125-rectangles/), byte-identical to the pinned tree after decompression ([Compressed Files](#compressed-files)) |
| Read from the earlier packets | 71 files, byte-identical to the pinned tree: 48 from the September 28 packet and 23 from the September 27 packet |

The clone has no history, so every commit date here is from the GitHub commits API, read
within the hour after retrieval.
The Claims table gives the first commit of each new certificate directory; each of the
37 directories has exactly one commit.

Every one of the 2,295 files pinned at `39d8ecc` is in this tree with the same digest,
except three: the top-level `README.md`, `point_n21_L5/README.md` and
`point_n21_L5/lean/README.md`. The source added 602 files and removed none.
[`acquisition/sources.json`](acquisition/sources.json) records the pin, the file counts,
the referenced files by packet and the claim list.
`python -m devtools.audit_wand125_rectangles --packet 2026-10-01 --acquire CHECKOUT`
rebuilds both acquisition files and the retained subset from a clean checkout at the
pinned revision. It first derives the standing certificate of every count from the
checkout’s candidates and refuses to run unless that set is the tool’s pinned table.

## Credit and AI Assistance

The source has no `CREDITS`, `NOTICE` or `AUTHORS` file.
Its attribution files are `LICENSE` and `point_n21_L5/UPSTREAM-LICENSE.txt`, which is
Evan Daniel’s MIT text for the point-only bundle and does not bear on these
certificates. Credit is in the README, retained here as
[`wand125-rectangles/README.md`](wand125-rectangles/README.md):

- **The method** (lines 749–773, “Attribution”): the README opens the section with “The
  method is not ours.”
  It credits Walter Stromquist, Hiroshi Nagamochi, Sam Burns and Gustavo Massaccesi, and
  this repository for row generation, column generation and branch and bound.
  It claims the search runs and the certificates.
- **The checker** (lines 314–358, “Checking them”): `verify.cpp` and `run_verify.py` are
  Tokoharu’s, unchanged, and the README says nothing in the checker’s mathematics is
  wand125’s. It claims the driver, the machine time, the fixed-support route, the
  scaling step and the choice of parent certificates.
- **AI assistance** (line 801, “Status”): parts of the work were produced with AI
  assistance under human direction.
  The same section says none of the certificates has been peer reviewed.

Issue 281 states the credit the same way: solver and checker Tokoharu’s, certificates
and ladder wand125’s.

## What Is Retained

The tree has 317 rectangle certificate directories, one per rung of each count’s ladder.
The evidence for a count is its standing (highest) certificate:
`certified_candidate.json` (the exact side, shrink, rectangles and rational weights),
`certificate_metadata.json` (exact mass and input digest), and the upstream accepting
run’s `verification_summary.json` and `verified_angles.jsonl`.

- **Retained here**: the source `README.md`, which changed, and those four files for the
  37 standing certificates that are new or raised since `39d8ecc`.
- **Read from the September 28 packet**: the four files of 12 standing certificates
  unchanged since `39d8ecc`, at `n = 21`, 37, 51, 52, 57, 58, 60, 67, 71, 72, 73 and 91.
- **Read from the September 27 packet**: `LICENSE`, `requirements.txt` and the five
  files of `docs/`, and the four files of the 4 standing certificates unchanged since
  `ad43d29`, at `n = 18`, 32, 45 and 61.
- **Pinned by digest only**, because the audit regenerates it: `certificate_input.txt`,
  40 MB across the 37 new certificates, which is the candidate as outward-rounded
  binary64 intervals and must hash to the recorded SHA-256.
- **Pinned by digest only**, because this repository already holds the bytes:
  `verify.cpp` and `run_verify.py`, byte-identical in every certificate directory to
  Tokoharu’s copies (SHA-256 `a75140df…` and `7bce2467…`).
- **Pinned by digest only**, because no claim here rests on it: the lower rungs, 29 of
  them published since `39d8ecc`; the matching certificates; the ten point certificates
  and `src/`; and the `point_n21_L5/`, `point_n45_L7/`, `point_n61_L8/`,
  `certificates/mixed_n*`, `certificates/k2m5_n59_L8` and `certificates/k2m4_n77_L9`
  bundles, which are the other packet’s.

The audit tool reads a file held by an earlier packet from that packet’s
`wand125-rectangles/` directory and requires the digest this pin’s tree manifest records
for it.

## Where the Request and the Source Differ

Issue 281 differs from the pinned tree in two statements and in its scope.
The packet follows the tree.

- **No rectangle directory carries a tarball.** The issue says each directory holds the
  candidate, the checker’s input and summary, and a tarball.
  Each of the 37 directories holds seven files: the four retained here,
  `certificate_input.txt`, `verify.cpp` and `run_verify.py`. The only archives in the
  tree are the ten `certificates/mixed_n*` proof bundles and, under `point_n21_L5/`, a
  bundle in 14 parts and two gzipped JSON files.
- **The revision is dated 1 October in UTC.** The issue dates `1a25a5e` 2 October.
  The commit is 2026-10-01T21:10:40Z; its own stamp is 06:10 on 2 October at `+09:00`.
  This packet is named for the UTC date.
- **The issue lists 34 of the 37 certificates.** It leaves out `n = 59`, 77 and 78,
  where it points to exact values: `s(59) = 8` and `s(77) = 9` in issues 280 and 279,
  and 9 at `n = 78`. The three rectangle certificates are standing at this revision, at
  `3173/400`, `3573/400` and `1793/200`, and are retained with the rest.

The 34 rows the issue does list agree with the tree in directory and side, and its
“T-046” column agrees with the `39d8ecc` table.
The source README’s own standing table still gives Nagamochi’s bound as the previous
record at `n = 59` and 77, beside the exact values the same revision claims.

## Claims

Each standing certificate proves `s(n) >= L`: its exact mass is strictly below `n`, and
every rotated, translated unit square captures mass at least one.
“Rectangles” counts the positive-weight orbit representatives; the checker sees eight
images of each. “First commit” is the UTC date and the commit that added the directory.

| `n` | Certificate | Side | Mass | Rectangles | Since `39d8ecc` | First commit |
| --- | --- | --- | --- | --- | --- | --- |
| 18 | `rect_n18_L4695` | `939/200` = 4.695 | `1799/100` = 17.99 | 199 | unchanged |  |
| 19 | `rect_n19_L48175` | `1927/400` = 4.8175 | `1899/100` = 18.99 | 309 | raised from `963/200` by 0.0025 | 2026-10-01, `03bb2d1` |
| 20 | `rect_n20_L48975` | `1959/400` = 4.8975 | `1999/100` = 19.99 | 229 | raised from `979/200` by 0.0025 | 2026-10-01, `62b4945` |
| 21 | `rect_n21_L49875` | `399/80` = 4.9875 | `20999/1000` = 20.999 | 116 | unchanged |  |
| 26 | `rect_n26_L55325` | `2213/400` = 5.5325 | `2599/100` = 25.99 | 260 | raised from `553/100` by 0.0025 | 2026-09-30, `3d76b48` |
| 27 | `rect_n27_L5635` | `1127/200` = 5.635 | `2699/100` = 26.99 | 242 | raised from `28/5` by 0.035 | 2026-09-30, `d42ea71` |
| 28 | `rect_n28_L57225` | `2289/400` = 5.7225 | `2799/100` = 27.99 | 243 | raised from `143/25` by 0.0025 | 2026-09-30, `d42ea71` |
| 29 | `rect_n29_L57975` | `2319/400` = 5.7975 | `2899/100` = 28.99 | 223 | raised from `579/100` by 0.0075 | 2026-10-01, `62b4945` |
| 30 | `rect_n30_L5875` | `47/8` = 5.875 | `2999/100` = 29.99 | 261 | raised from `1173/200` by 0.01 | 2026-10-01, `62b4945` |
| 31 | `rect_n31_L59525` | `2381/400` = 5.9525 | `3099/100` = 30.99 | 235 | raised from `1187/200` by 0.0175 | 2026-10-01, `03bb2d1` |
| 32 | `rect_n32_L595` | `119/20` = 5.95 | `3199/100` = 31.99 | 135 | unchanged |  |
| 37 | `rect_n37_L6425` | `257/40` = 6.425 | `3699/100` = 36.99 | 304 | unchanged |  |
| 38 | `rect_n38_L6545` | `1309/200` = 6.545 | `3799/100` = 37.99 | 402 | raised from `327/50` by 0.005 | 2026-10-01, `ece1bad` |
| 39 | `rect_n39_L6635` | `1327/200` = 6.635 | `3899/100` = 38.99 | 517 | raised from `663/100` by 0.005 | 2026-10-01, `95d739f` |
| 40 | `rect_n40_L67` | `67/10` = 6.7 | `3999/100` = 39.99 | 480 | raised from `1339/200` by 0.005 | 2026-10-01, `03bb2d1` |
| 41 | `rect_n41_L676` | `169/25` = 6.76 | `4099/100` = 40.99 | 461 | raised from `1351/200` by 0.005 | 2026-09-30, `d42ea71` |
| 42 | `rect_n42_L6815` | `1363/200` = 6.815 | `4199/100` = 41.99 | 439 | raised from `679/100` by 0.025 | 2026-10-01, `98d30ff` |
| 43 | `rect_n43_L68875` | `551/80` = 6.8875 | `4299/100` = 42.99 | 472 | raised from `1373/200` by 0.0225 | 2026-10-01, `95d739f` |
| 44 | `rect_n44_L69425` | `2777/400` = 6.9425 | `4399/100` = 43.99 | 435 | raised from `1387/200` by 0.0075 | 2026-10-01, `ece1bad` |
| 45 | `rect_n45_L6955` | `1391/200` = 6.955 | `4499/100` = 44.99 | 227 | unchanged |  |
| 51 | `rect_n51_L74425` | `2977/400` = 7.4425 | `5099/100` = 50.99 | 448 | unchanged |  |
| 52 | `rect_n52_L7535` | `1507/200` = 7.535 | `5199/100` = 51.99 | 581 | unchanged |  |
| 53 | `rect_n53_L76075` | `3043/400` = 7.6075 | `5299/100` = 52.99 | 643 | raised from `1519/200` by 0.0125 | 2026-09-30, `4bb00e7` |
| 54 | `rect_n54_L76725` | `3069/400` = 7.6725 | `5399/100` = 53.99 | 616 | raised from `3067/400` by 0.005 | 2026-10-01, `98d30ff` |
| 55 | `rect_n55_L77125` | `617/80` = 7.7125 | `5499/100` = 54.99 | 557 | raised from `771/100` by 0.0025 | 2026-09-30, `4bb00e7` |
| 56 | `rect_n56_L77825` | `3113/400` = 7.7825 | `5599/100` = 55.99 | 633 | raised from `777/100` by 0.0125 | 2026-09-30, `60c3c87` |
| 57 | `rect_n57_L7835` | `1567/200` = 7.835 | `5699/100` = 56.99 | 615 | unchanged |  |
| 58 | `rect_n58_L789` | `789/100` = 7.89 | `5799/100` = 57.99 | 590 | unchanged |  |
| 59 | `rect_n59_L79325` | `3173/400` = 7.9325 | `5899/100` = 58.99 | 583 | raised from `198/25` by 0.0125 | 2026-10-01, `ca444dc` |
| 60 | `rect_n60_L794` | `397/50` = 7.94 | `5999/100` = 59.99 | 410 | unchanged |  |
| 61 | `rect_n61_L796` | `199/25` = 7.96 | `6099/100` = 60.99 | 375 | unchanged |  |
| 66 | `rect_n66_L8385` | `1677/200` = 8.385 | `6599/100` = 65.99 | 721 | raised from `67/8` by 0.01 | 2026-09-29, `b62c5ab` |
| 67 | `rect_n67_L8455` | `1691/200` = 8.455 | `6699/100` = 66.99 | 785 | unchanged |  |
| 68 | `rect_n68_L851` | `851/100` = 8.51 | `6799/100` = 67.99 | 774 | raised from `1699/200` by 0.015 | 2026-10-01, `ca444dc` |
| 69 | `rect_n69_L8585` | `1717/200` = 8.585 | `6899/100` = 68.99 | 914 | raised from `343/40` by 0.01 | 2026-10-01, `f2f6245` |
| 70 | `rect_n70_L8625` | `69/8` = 8.625 | `6999/100` = 69.99 | 859 | raised from `431/50` by 0.005 | 2026-10-01, `f2f6245` |
| 71 | `rect_n71_L8685` | `1737/200` = 8.685 | `7099/100` = 70.99 | 871 | unchanged |  |
| 72 | `rect_n72_L874` | `437/50` = 8.74 | `7199/100` = 71.99 | 931 | unchanged |  |
| 73 | `rect_n73_L878` | `439/50` = 8.78 | `7299/100` = 72.99 | 905 | unchanged |  |
| 74 | `rect_n74_L88475` | `3539/400` = 8.8475 | `7399/100` = 73.99 | 886 | raised from `221/25` by 0.0075 | 2026-10-01, `458bf41` |
| 75 | `rect_n75_L89` | `89/10` = 8.9 | `7499/100` = 74.99 | 815 | raised from `889/100` by 0.01 | 2026-09-29, `1c6018c` |
| 76 | `rect_n76_L8925` | `357/40` = 8.925 | `7599/100` = 75.99 | 809 | raised from `223/25` by 0.005 | 2026-09-30, `d42ea71` |
| 77 | `rect_n77_L89325` | `3573/400` = 8.9325 | `7699/100` = 76.99 | 621 | raised from `891/100` by 0.0225 | 2026-10-01, `458bf41` |
| 78 | `rect_n78_L8965` | `1793/200` = 8.965 | `7799/100` = 77.99 | 924 | raised from `1791/200` by 0.01 | 2026-09-30, `3d76b48` |
| 86 | `rect_n86_L9365` | `1873/200` = 9.365 | `8599/100` = 85.99 | 659 | raised from `1871/200` by 0.01 | 2026-09-29, `b62c5ab` |
| 87 | `rect_n87_L941` | `941/100` = 9.41 | `8699/100` = 86.99 | 691 | new | 2026-10-01, `98d30ff` |
| 88 | `rect_n88_L94775` | `3791/400` = 9.4775 | `8799/100` = 87.99 | 687 | raised from `189/20` by 0.0275 | 2026-10-01, `ca444dc` |
| 89 | `rect_n89_L9565` | `1913/200` = 9.565 | `8899/100` = 88.99 | 926 | raised from `191/20` by 0.015 | 2026-09-29, `e30e1a7` |
| 90 | `rect_n90_L95775` | `3831/400` = 9.5775 | `8999/100` = 89.99 | 764 | new | 2026-10-01, `f2f6245` |
| 91 | `rect_n91_L9645` | `1929/200` = 9.645 | `9099/100` = 90.99 | 859 | unchanged |  |
| 93 | `rect_n93_L97225` | `3889/400` = 9.7225 | `9299/100` = 92.99 | 830 | new | 2026-10-01, `98d30ff` |
| 94 | `rect_n94_L9805` | `1961/200` = 9.805 | `9399/100` = 93.99 | 876 | raised from `1959/200` by 0.01 | 2026-09-29, `b62c5ab` |
| 95 | `rect_n95_L98518` | `49259/5000` = 9.8518 | `9499/100` = 94.99 | 880 | raised from `49209/5000` by 0.01 | 2026-09-29, `b62c5ab` |

Of the 53, 16 are unchanged, 34 are raised, by `0.0025` to `0.035`, and 3 are new.
Six of the 37 were first committed on 29 September, nine on 30 September and 22 on 1
October.

Five of the 37 are below a bound registered separately when this packet was written, so
the reported lane of their case records does not take them: the source’s own covers for
`s(59) = 8` and `s(77) = 9`, Evan Daniel’s `s(78) = 9`, and the source’s mixed
certificates `421/50` at `n = 66` and `48/5` at `n = 90`. The other 32 raise the
reported lower bound of their count.

### Bounds by Inheritance of Mass

A certificate of mass below `k` refutes `k` squares, so it also bounds every larger
count. Carried upward from the table, each count below takes the strongest smaller-count
certificate:

| Counts | From | Bound |
| --- | --- | --- |
| 22–25 | `rect_n21_L49875` | `399/80` = 4.9875 |
| 32–36 | `rect_n31_L59525` | `2381/400` = 5.9525, above the direct `119/20` at `n = 32` |
| 46–50 | `rect_n45_L6955` | `1391/200` = 6.955 |
| 62–65 | `rect_n61_L796` | `199/25` = 7.96 |
| 79–85 | `rect_n78_L8965` | `1793/200` = 8.965 |
| 92 | `rect_n91_L9645` | `1929/200` = 9.645 |

None of these beats what the register holds.
The integer bound is stronger at 22–25, 32–36, 46–49, 62–64 and 79–81, wand125’s mixed
certificates at `n = 50`, 65 and 92, and Green’s DS7 value at 82–85. The counts 77, 87,
90 and 93, which took a transfer at `39d8ecc`, now have a direct certificate that is
stronger.

## How the Certificates Were Made

The method and checker are Tokoharu’s, reviewed on 2026-09-22 in the
[density mathematics review](../../../../docs/project/reviews/review-2026-09-22-tokoharu-density-mathematics.md)
and, for sides up to `1791/200`, in the
[checker-scaling review](../../../../docs/project/reviews/review-2026-09-27-wand125-rectangle-scaling.md).
The 37 new certificates go past both: sides to `49259/5000 = 9.8518` and up to 926
rectangle orbits (`n = 89`). The scaling review found no premise of the checker that
depends on the side, the count or the rectangle number except through running time.
It did not run these certificates.

As at the earlier pins, every candidate’s weights were multiplied by one exact rational
factor before the recorded run.
Each candidate records it under `scaling_experiment`, as `factor_exact` with its source
and target masses. All 37 new certificates have mass `n - 1/100`, the one at `n = 27`
included, whose predecessor had `n - 1/1000`; across the 37 the factors lie between
1.00004 and 1.04329. The checker reads the scaled data, and the preflight checks the
scaled mass exactly, so scaling bears only on how a certificate was found.

## Receipts

The audit tool is
[`devtools/audit_wand125_rectangles.py`](../../../devtools/audit_wand125_rectangles.py);
`--packet 2026-10-01` selects this packet.
It reuses the exact preflight of `devtools/audit_tokoharu_density.py`, with each
certificate’s own pinned side, and requires the candidate’s own `n` to be the pinned
count.

- [`receipts/controls/rect_n41_L676.json`](receipts/controls/rect_n41_L676.json): the
  stage-4 controls of 2 October. Tokoharu’s `verify.cpp`, compiled with `run_verify.py`’s
  exact command, accepts `rect_n41_L676` at direction 32, its least recorded bound
  (66,387 nodes, matching the upstream row), and refuses two mutated copies there: every
  weight scaled by 99/100, and the heaviest orbit at a witness centre deleted, whose exact
  coverage falls to 0.99269 and 0.73652. `tests/test_wand125_checker_controls.py` holds
  them.
- [`receipts/preflight/audit.json.gz`](receipts/preflight/audit.json.gz): the exact
  preflight of all 53 standing certificates, the 16 unchanged ones read from the earlier
  packets. For each, the regenerated input matches the published SHA-256, every interval
  encloses its exact datum, the axis-event partition is complete, orbit normalization
  preserves mass, and the exact mass is below `n`. All 53 pass, in 68 s on one core; the
  16 unchanged entries equal those of the September 28 receipt.
- [`receipts/replay/audit.json.gz`](receipts/replay/audit.json.gz) and one directory per
  certificate: the complete 201-direction replays of 2 October 2026 of 30 of the 37
  certificates retained here, every one except `rect_n66_L8385`, `rect_n77_L89325`,
  `rect_n78_L8965`, `rect_n86_L9365`, `rect_n87_L941`, `rect_n90_L95775` and
  `rect_n59_L79325`, whose counts are held above them by mixed certificates or exact
  values. Each ran Tokoharu’s unchanged `verify.cpp` through `run_verify.py` with one
  worker, in sixteen cloud batches (`claude/replay-wand125-rect-oct1-r1` to `-r4`, four
  each), about 143 hours of wall in all. `audit_wand125_rectangles --packet 2026-10-01
  --merge` folded the batches’ receipts in, checking each case against this packet’s
  preflight, the published input digest and the reviewed checker digest, and every
  replay reproduced the upstream accepting run’s nodes, leaves and lower bound angle by
  angle. The transfer branches are not merged. None of the source’s other programs was
  run in making this packet; the earlier packets’ replay receipts remain, and are of the
  certificates those packets retain.

The preflight proves every obligation except global rotated coverage, which the external
checker decides; for the 30 replayed certificates the replay decides it with the
source’s checker (`E-wand125-rectangle-2026-10-01-source-replay`, T-074).

`python -m devtools.apply_wand125_rectangles --packet 2026-10-01 --replay-plan` lists
the standing certificates whose replay would raise a verified lower bound, largest rise
first, each costed by its upstream per-angle CPU time: 50 certificates and about 214 CPU
hours in all, of which the 37 retained here are about 167. Each is replayed into the
packet that retains it, from `packing/` with the project CPython 3.14 environment and a
C++17 `g++` on `PATH`:

```bash
.venv/bin/python3 -m devtools.audit_wand125_rectangles --packet 2026-10-01 \
  --out resources/web/wand125-rectangle-certificates-2026-10-01/receipts/replay \
  --resume --replay --workers 2 --n 38 --n 54
.venv/bin/python3 -m devtools.apply_wand125_rectangles --packet 2026-10-01
```

A certificate unchanged since an earlier pin takes that packet’s `--packet` date and
`receipts/replay` instead, so it is promoted under the evidence entry that already
covers it. The first promotion from this packet’s own receipt needs a replay entry,
`E-wand125-rectangle-2026-10-01-source-replay`, in `frontier/evidence.yaml`;
`apply_wand125_rectangles` stops and names it until it exists.

## Compressed Files

The 37 candidates retained here, `certified_candidate.json` in each certificate
directory, are over 1,000 lines each, and so is the preflight receipt.
Each is stored as deterministic gzip made by `gzip -9n`, with no file name or timestamp
in the header, following the [R052 packet](../n17-guzhou-r052-2026-09-25/README.md).
The table gives the Git blob and SHA-256 of the decompressed bytes, which for an
upstream file are its blob and digest at the pinned commit and for the receipt are the
bytes this repository wrote.
The audit tool writes a receipt plain and removes a stale compressed copy; a receipt
that has grown past 1,000 lines is compressed afterwards with
`python -m devtools.retained_data compress --origin receipt PACKET FILE`, which prints
its table row. The repository’s readers take the upstream path and decompress
transparently through `devtools.retained_data.read_retained_bytes`, and
`python -m devtools.retained_data check PACKET` re-derives every row.
Each upstream SHA-256 is also the one
[`acquisition/upstream-tree.sha256`](acquisition/upstream-tree.sha256) pins, and
`devtools.audit_wand125_rectangles` checks the retained subset against that manifest
through the decompressed bytes.

Before running any of the source’s own programs on this packet, restore the exact
upstream files from the repository root, in all three packets, since this one reads the
unchanged certificates from the other two:

```sh
find packing/resources/web/wand125-rectangle-certificates-2026-09-27 \
  packing/resources/web/wand125-rectangle-certificates-2026-09-28 \
  packing/resources/web/wand125-rectangle-certificates-2026-10-01 -name '*.gz' -exec gunzip -k {} +
```

The restored plain files are untracked, so remove them afterwards; while both copies are
present, the repository’s readers require them to agree.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `wand125-rectangles/certificates/rect_n19_L48175/certified_candidate.json.gz` | upstream | `0d65d64cc8f4c157b8f648bc69b665b70d218b0b` | `6a7646be9b8214d03509ba7529a5d9f89c76a19fbbfd1df07c1063762a683775` |
| `wand125-rectangles/certificates/rect_n20_L48975/certified_candidate.json.gz` | upstream | `44d13aa0e2f3f089fc6a06a4a8110d07a54db172` | `f830089a983d58e56a024759e0ddcd585fb1ae805cd14c55486e86da4979bf3f` |
| `wand125-rectangles/certificates/rect_n26_L55325/certified_candidate.json.gz` | upstream | `e39c67220e0c2063a231eb01e03e96ca8f3ecf50` | `a39bb5cef04fc85f1a2d61e065467ec51001f3293c8b2e0f6971a2e8dbab283f` |
| `wand125-rectangles/certificates/rect_n27_L5635/certified_candidate.json.gz` | upstream | `ab21208a0acd5e2d07f1c38cbedb254cc3cedfec` | `aa3a00166c6da9866478c830714c762fae9ff61098d40fe573c6bbd7f9602ec1` |
| `wand125-rectangles/certificates/rect_n28_L57225/certified_candidate.json.gz` | upstream | `51e019d595bef4aa448f71b32428b5614030b65d` | `36f57cf4bb1f6a8c88a55f764fccb5bd0dd0ecbca6133b6162e585d7f6f04c2e` |
| `wand125-rectangles/certificates/rect_n29_L57975/certified_candidate.json.gz` | upstream | `f5561d598114b29911e2dd32ecddb407c27ba9ba` | `0adb6346322f5365358b40522f4c1105c8a385589373dfb05fc4d9309f372d13` |
| `wand125-rectangles/certificates/rect_n30_L5875/certified_candidate.json.gz` | upstream | `d2cff6b6c45b843d97b8c7bb71d16b0de17c419d` | `8cc5c3b4585d098b413e7f14cd5ef6c52681494ddba8d8f3b222eec78b2e8a52` |
| `wand125-rectangles/certificates/rect_n31_L59525/certified_candidate.json.gz` | upstream | `a091ce3604d1891c8820a92224df42f3b0ca77e3` | `35639ebee56ec0bf0ed64e032467788929ae7e7b7f17328c8a86d425465ebfc9` |
| `wand125-rectangles/certificates/rect_n38_L6545/certified_candidate.json.gz` | upstream | `1db32bd46e1f5678c192ef68c394abc268fdf92d` | `756b36bd45e338bde65372d5ea852ddac77d314dc1e5bbe69cc45349d021cd1a` |
| `wand125-rectangles/certificates/rect_n39_L6635/certified_candidate.json.gz` | upstream | `451e6e166b4e482cc6f16571493c8c9ee2504295` | `8ddeed397919a0edf1ac3e240353fd0f94580e95065912b78073cf89cecd6733` |
| `wand125-rectangles/certificates/rect_n40_L67/certified_candidate.json.gz` | upstream | `0e1862ef0eb10565f0c2ae661ef11b889b727543` | `71011d0356dd179c6e7e6e02c9a064ff30f6f13844016ce3b97463bf7ef53dc0` |
| `wand125-rectangles/certificates/rect_n41_L676/certified_candidate.json.gz` | upstream | `6f663857f1b0023b9c3c1fd81b5060ecdfbc6bda` | `9569eea96209774dd49d856c3e172b4e4e4fac87bb3530563cf80c5258f25078` |
| `wand125-rectangles/certificates/rect_n42_L6815/certified_candidate.json.gz` | upstream | `5cc0a3f6bdec7447577cd0c0de7c0a2e58fd4dc1` | `1d9a29d5f42312747f635f40b79548ebc42ac8595692eb8e5dbe171d7ae4131c` |
| `wand125-rectangles/certificates/rect_n43_L68875/certified_candidate.json.gz` | upstream | `ea86ca81b9d03d5f9134d2d51f1b3cf72bda9da0` | `175b75f3fff6135510c9ebae0acb1477eccc899e526df511141a78c749e9c9b4` |
| `wand125-rectangles/certificates/rect_n44_L69425/certified_candidate.json.gz` | upstream | `7660272a37448e65f05bf3209d35e451a3a45057` | `e5ddc7fb129a10bc6b8aa507d083f352608a85c3d4df81407af100f5c4c2797a` |
| `wand125-rectangles/certificates/rect_n53_L76075/certified_candidate.json.gz` | upstream | `1490ac45a7673a7a8fcf6ae32ed483d04a44097f` | `380cd3274ca9cdb1478174cfdff076e7f8c55dfe8c3e9054072a8a97548e9bd3` |
| `wand125-rectangles/certificates/rect_n54_L76725/certified_candidate.json.gz` | upstream | `2da2c00942f497b9ea50409c53983b885a8a786e` | `3e1969fdc116e6977dcd2c0b83eabf19c278ca83afcaaf1b713f80b25b0ad768` |
| `wand125-rectangles/certificates/rect_n55_L77125/certified_candidate.json.gz` | upstream | `60aa20325fa460f32dfee4ced1501c666db8c600` | `ca72b76c9b0b5cad6fba396caf2db96185b299b32f5a98902adac06a4d06f4a9` |
| `wand125-rectangles/certificates/rect_n56_L77825/certified_candidate.json.gz` | upstream | `16b214d0525bb02759ffd54d03afe594b8a29048` | `ed8829d53c9c02a2f3ad2f797209caade1804a62b635887fcbdfd99c5c04fe1f` |
| `wand125-rectangles/certificates/rect_n59_L79325/certified_candidate.json.gz` | upstream | `59a8fd4e517e0bad8fb7005c5b63b903af469947` | `61ffbaf3c4252b3f50ac23df45fcb00c99026cb4679ba0b2b49a5440df6ed0c7` |
| `wand125-rectangles/certificates/rect_n66_L8385/certified_candidate.json.gz` | upstream | `3f6feb20136b962be6f2d53368b9273d39ddb6f8` | `541d35f25c09bbbf76a60331da6265af0104b822b100087730d2672262788bd3` |
| `wand125-rectangles/certificates/rect_n68_L851/certified_candidate.json.gz` | upstream | `9d93fb8e45009b91f646099a458f5746f529b455` | `42751c3c3988b38f8d13bbda0b5d628fcd672c95665316c05d43a9efdd2858c0` |
| `wand125-rectangles/certificates/rect_n69_L8585/certified_candidate.json.gz` | upstream | `30fa3eea65287c3b5773610753aab2a075b808a7` | `452e196b7afd4e0ddb87485bb567130c6eb232579e95a10fc6ac30cb69e55846` |
| `wand125-rectangles/certificates/rect_n70_L8625/certified_candidate.json.gz` | upstream | `b86f625f795838ec3e369e3f8bdd6d2ffdd56ae8` | `b365dfbf639e15822393843f18ba8048e8e73a18490fff899553a9fc433b288a` |
| `wand125-rectangles/certificates/rect_n74_L88475/certified_candidate.json.gz` | upstream | `12ab9966c33ccf9adb070fcfff6959866ea3069d` | `77b725c5f3a55a326ba054dc7794c69d7015e4a21b6e609ca38d876b0b8760fd` |
| `wand125-rectangles/certificates/rect_n75_L89/certified_candidate.json.gz` | upstream | `dccbb3bf19d118662dc4842eab5d5ed058cd343f` | `4fe94b6fb9b50e2751cb2d623b5c3158ed6be9e29f9ceb69bc0c4009c3bef43e` |
| `wand125-rectangles/certificates/rect_n76_L8925/certified_candidate.json.gz` | upstream | `00da8dd9fdaad366067211a8aad5d0b6680f5538` | `afaf4ec2ae874b27c73120fbf87db8b0a02e1fad5b352ab76969edf14562d0da` |
| `wand125-rectangles/certificates/rect_n77_L89325/certified_candidate.json.gz` | upstream | `b647ad18f96c1a1462385ed121ab43d148c05932` | `354f6f20b93a3306b95f7c6e0298102bbca3e0187c983d03784729258ee87c3c` |
| `wand125-rectangles/certificates/rect_n78_L8965/certified_candidate.json.gz` | upstream | `b51ca88148ea169efdb49257097edd64778ea43f` | `b9157aca1e875aa0daff222f4e0a079efb75e6b0580d675aa0068671d4a73b2b` |
| `wand125-rectangles/certificates/rect_n86_L9365/certified_candidate.json.gz` | upstream | `551f142737d7437cad9ab3421f2eb11c37c31530` | `f43953057c6e87127b03018adf5de58c50dcb51a62eed300acb65b2890b613ec` |
| `wand125-rectangles/certificates/rect_n87_L941/certified_candidate.json.gz` | upstream | `3daea5d8410f64a679f63aaf84360532fc401890` | `b0d6b0bc29a113585f2165a718742d19518d79276ce99f7b6796f032b8884edf` |
| `wand125-rectangles/certificates/rect_n88_L94775/certified_candidate.json.gz` | upstream | `2514b9146bffc49086aef8ed22022fb8a61784c3` | `0fb795534a4a4e162a3b824a3705fc8514959754eace3a313776e976e770b757` |
| `wand125-rectangles/certificates/rect_n89_L9565/certified_candidate.json.gz` | upstream | `2e1511a65543649b50bbdb24a77e46524deb3507` | `651ce91428609e22efd40a43c5132b61fb35dcad03827041138bbc5105ff8059` |
| `wand125-rectangles/certificates/rect_n90_L95775/certified_candidate.json.gz` | upstream | `aec009851ae63be39bee4cc183b0dada1a69c253` | `063d490544cfc984ed127c84f85b350a4bb6b3e509f7357a76cc3cab1b00fd46` |
| `wand125-rectangles/certificates/rect_n93_L97225/certified_candidate.json.gz` | upstream | `454ae8fbccad76caf80f31bc060de55ec57925ac` | `a6b02a88d4e95e8823a432c9ae6dc57c40a4f70d2046d61f4a827e06dd0ec0d0` |
| `wand125-rectangles/certificates/rect_n94_L9805/certified_candidate.json.gz` | upstream | `8dd2c3028e6b04cd1ab3391b7b7db8d31d658d1d` | `5f4e7bf572dca33dc929846af75b7ed4447978309683251e2d2d2defcf531c72` |
| `wand125-rectangles/certificates/rect_n95_L98518/certified_candidate.json.gz` | upstream | `3f0f156717c1998fc656651a90462f71cf478f88` | `cd70e6eab2fc136b04c9225a2c101cb2b55be1119ba93146245dac3a064d275d` |
| `receipts/preflight/audit.json.gz` | receipt | `5eb49297f7075b5b5a2d02cc8bd707e51cddec56` | `5391bc60ee502401ac2b37e82b350413dffe5a4ddaad3bd4c5b05a8dd797bf73` |
| `receipts/replay/audit.json.gz` | receipt | `9d464296a65aca764420e85110bb8849724a0f5d` | `a3a04836844267ed2b8fe782ed7eade166205bc3f7892b067cb3987eb30d6c99` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
