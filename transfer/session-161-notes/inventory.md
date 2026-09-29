# W8 inventory: recent lower bounds, their holders and lineage, and where the documents list them

Session 161, read-only. Working tree read on 2026-09-29 at `7837df379` plus the
uncommitted registration in progress (n-021, n-045, n-050, evidence.yaml,
bibliography.yaml, resources/README.md, bound-citations.json already modified;
`packing/frontier/n-017.md` **not yet modified** when read). Every row below treats the
pending registrations as landed:

- `s(17) > 116511/25000 = 4.66044`, Guzhou0806 R068, verified `V4/C3`
  (`E-n017-guzhou-r068-source-replay`, packing/frontier/evidence.yaml:3352), after
  Kleddamag's `466001/100000`; R067 `233009/50000` replayed beside it.
- `s(21) = 5` and `s(45) = 7`, Evan Daniel, mixed covers, verified `V4/C3`, both cases
  `proved`; wand125's point-only routes recorded as second certificates (`s(45)`
  verified `V4/C3`, `s(21)` reported, replay running).
- `s(50) ≥ 37/5`, wand125, reported (replay running).
- wand125's 38 reported rectangle bounds at `39d8ecc` (commit `2c8bda4e`), `n = 21` and
  `28–95`, replays running in batches.

**Definitions used throughout.**

- *Recent* is the record's own rule, not a reading of prose:
  `build_bound_citations.RECENT_SINCE = date(2026, 8, 22)`
  (packing/devtools/build_bound_citations.py:141), applied to the source's
  bibliography `dated`; this project's own new bounds are recent by construction. The
  prose everywhere says "since August 2026" (README.md:47, README.md:64, explainer
  caption via `RECENT_SINCE_MONTH` = "August 2026"), which a reader will take to include
  1–21 August; the 2026 bounds dated 1–21 August (Burns, MacIver, Mira's and Fort's
  sixteen-point sets, anabologyco-maker, Massaccesi) are **not** recent under the rule.
  They are listed separately in §1c so the owner can decide.
- *Lineage class*: **A** this project's own result (a `T-NNN` scored
  `apparently-novel`); **B** builds on this project (the source's own attribution
  credits this project's certificates, data or pipeline, directly or through an
  intermediary it names); **B′** credits this project only as inspiration or second-hand
  and brings its own method (Tokoharu; wand125's `n = 50` density on Tokoharu's
  solver); **C** independent of this project (the source names another lineage and
  lists this project as parallel work). Evidence codes (L-…) are defined in §1b with the
  quotes.
- *Rung*: V/C as the case records and evidence entries state it (external bounds have no
  typed rung; see §4).

## Headline numbers after the pending registrations

Computed from `packing/frontier/n-*.md` (reported and verified lower-bound fields),
`bibliography.yaml` `dated`, and `bound-citations.json` `recent` (verified lane only).
Cross-checked against wand125's own "Who Holds Each Lower Bound" table
(packing/resources/web/wand125-x-update-2026-09-28/acquisition/lower-bound-table-2026-09-28.html),
whose holder summary is "this work + tokoharu 49, Kleddamag 1, Guzhou0806 1, evand 4" = 55,
the same 55 counts (it still shows R067 at `n = 17`).

| Quantity (`n = 1…100`) | Count | The `n` values |
| --- | ---: | --- |
| Cases with a recent lower bound in either lane | **55** | 11, 12, 17–21, 26–32, 37–45, 50–61, 66–78, 86, 88–91, 94, 95 |
| … whose **verified** lower bound is recent (the atlas star) | **27** | 11, 12, 17, 18, 19, 20, 21, 26, 27, 28, 29, 30, 31, 32, 39, 40, 41, 45, 52, 53, 55, 56, 68, 69, 70, 71, 72 |
| … of those 27, this project's (class A) | **3** | 18 (T-030), 19 (T-020), 20 (T-021) |
| … of those 27, proved (star on the card, no lower-bound line drawn) | 3 | 21, 32, 45 |
| … whose recent bound is **reported only** (verified lane older) | **28** | 37, 38, 42, 43, 44, 50, 51, 54, 57–61, 66, 67, 73–78, 86, 88–91, 94, 95 |
| Cases where the strongest recent bound (either lane) is this project's | **0** | wand125's reported bounds sit above T-030/T-020/T-021 at 18, 19, 20 |
| New exact values since 22 August 2026 | **3** | 21, 32, 45 (Evan Daniel, class C) |
| Proved cases `n ≤ 100` | 38 (was 36) | adds 21, 45 |
| Proved / open, `n ≤ 324` | 62 / 262 | |

Strongest-bound holders over the 55 (reported lane, which never trails the verified
one): wand125 49, Evan Daniel 4 (12, 21, 32, 45), Kleddamag 1 (11), Guzhou0806 1 (17).
Verified-lane holders over the 27: wand125 15, Evan Daniel 4, this project 3, Tokoharu 3
(26, 29, 30), Kleddamag 1, Guzhou0806 1. By class, verified lane: A 3, B 17
(Kleddamag, Guzhou0806, wand125), B′ 3 (Tokoharu), C 4 (Daniel). Reported lane: B 50
(wand125 rectangle 48, Kleddamag 1, Guzhou0806 1), B′ 1 (`n = 50`), C 4 (Daniel).

No case above `n = 100` carries a recent lower bound: a scan of `n-101.md … n-324.md`
finds no reported or verified lower bound from a source dated on or after 2026-08-22
(wand125's highest registered count is `n = 95`).

## 1. Every recent lower bound on `s(n)`, `n = 1…100`

### 1a. The table

"Earlier recent bounds" lists every bound at the same `n`, dated 22 August 2026 or
later, that the records carry (case body, evidence, packet, or audit tables) and that is
now superseded, with its class. Source rungs that a packet pins by digest only (e.g.
wand125's intermediate ladder rungs) are not listed individually. Dates are the
source's; `rep` = reported lane, `ver` = verified lane.

| `n` | Reported lower (exact = decimal) | Verified lower (exact = decimal), rung | Holder(s), as the record credits them | Class | Lineage | Earlier recent bounds at this `n` (all superseded) | Proved |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 11 | `31/8` = 3.875, strict | `31/8`, **V4/C4** | Kleddamag ("Kleddamag after Levy") | B | L-KL11 | T-018 `381/100` = 3.81 (09-04, A); T-022 3.8100257 (09-06, A); T-024 3.8166095 (09-09, A); T-025 `191/50` = 3.82 (09-09, A); T-026 3.8264474 (09-09, A); T-033 3.8269975 (09-22, A; still the strongest first-party rung); Tokoharu `381/100` (09-22, B′, replayed `V4/C3`, never above T-026); Daniel `3040/797` = 3.8143036 (found 08-26, published 09-22, C; retained in the evand packet, **not registered in n-011**) | no |
| 12 | `15680/3951` = 3.9686155 | same, **V4/C4** | Evan Daniel ("Daniel after Burns, Massaccesi") | C | L-EVD | T-017 `99/25` = 3.96 (09-04, A; ladder `19/5`…`79/20` below). The Daniel certificate entered his source on 2026-08-25 (packing/frontier/n-012.md:121), before T-017 | no |
| 17 | `116511/25000` = 4.66044, strict | same, **V4/C3** (pending) | Guzhou0806 ("Guzhou0806 after Kleddamag"; continuing Kleddamag's `4.66001` charge) | B (via Kleddamag) | L-GZ68 | T-001 `4426213/1000000` = 4.426213 (08-31, A); T-019 `459/100` = 4.59 (09-04, A); Mira `4613/1000` (09-07, B); R012 `461300/99999` = 4.6130461 = T-032 (09-20, B, V4/C4); Kleddamag v1.0.0 `461300/99853` = 4.6197911 (09-21, B, V4/C3); R038 `461300000000/99974999999` = 4.6141535 (B, reported, not replayed); ahyangyi v1.1.1 ≈ 4.6136817 (09-23, not assessed, not retained); R042 `115325/24963` = 4.6198374, R043 `461300/99851` = 4.6198836 (09-23), R050 `4613000/998509` = 4.6198883 (09-24) (B, publication records, not replayed); R052 `231001/50000` = 4.62002 (09-25, B, V4/C3); R052 continuation `462003/100000` = 4.62003 (09-25 UTC, B, publication record with C++ replay receipts, no evidence entry); Kleddamag v1.1.0 `232001/50000` = 4.64002 (09-26, B, V4/C3); Kleddamag `466001/100000` = 4.66001 (09-27, B, V4/C3); R067 `233009/50000` = 4.66018 (09-28, B, V4/C3, never the case bound) | no |
| 18 | `939/200` = 4.695 (09-26/27) | `4679/1000` = 4.679, **V4/C4** (T-030) | rep: wand125 ("wand125 after Tokoharu, Levy"); ver: Squares Project (Levy) | rep B; ver A | L-W125R; L-A | T-002 4.426213 (08-31, A); T-019 `459/100` (09-04, A); T-027 `467/100` (09-18, A); T-028 `187/40` = 4.675, T-029 `1871/400` = 4.6775 (09-19, A); R012 `461300/99999` in the reported lane from 09-20 (B) | no |
| 19 | `963/200` = 4.815 | `24/5` = 4.8, **V4/C4** (T-020) | rep: wand125; ver: Squares Project (Levy) | rep B; ver A | L-W125R; L-A | T-019 `459/100` (09-04, A) | no |
| 20 | `979/200` = 4.895 | `97/20` = 4.85, **V4/C4** (T-021) | rep: wand125; ver: Squares Project (Levy) | rep B; ver A | L-W125R; L-A | T-020 `24/5` (09-04, A) | no |
| 21 | `5` | `5`, **V4/C3** (complete `zmx2` replay; C4 needs the `zm_mixed.py` re-sweep recorded) | Evan Daniel; second, point-only route by wand125 (reported, replay running) | C; wand125 route C | L-EVD; L-W125X | T-020 `24/5` (09-04, A); T-021 `97/20` (09-05, A); T-034 `122/25` = 4.88 (09-23, A); Daniel `5000/1001` = 4.9950050 (source 09-23, verified 09-27, C, V4/C3); wand125 `997/200` = 4.985 (09-26, B) and `399/80` = 4.9875 (09-28, B), neither cited by the case | **yes** |
| 26 | `553/100` = 5.53 | `1377/250` = 5.508, **V4/C3** | rep: wand125; ver: Tokoharu ("Tokoharu after Levy, wand125") | rep B; ver B′ | L-W125R; L-TOK | wand125 point `109/20` = 5.45 (09-22, B) | no |
| 27 | `28/5` = 5.6 | `28/5`, **V4/C3** | wand125 | B | L-W125R | Tokoharu `1377/250` by monotonicity from `n = 26` (09-22, B′) | no |
| 28 | `143/25` = 5.72 (09-28) | `28/5` by monotonicity from `n = 27`, **V4/C3** | wand125 | B | L-W125R | Tokoharu `1377/250` (monotone, verified 09-22, B′); wand125 `1139/200` = 5.695 (09-27, B) | no |
| 29 | `579/100` = 5.79 (09-28) | `571/100` = 5.71, **V4/C3** | rep: wand125; ver: Tokoharu | rep B; ver B′ | L-W125R; L-TOK | wand125 point `557/100` = 5.57 (09-22, B); wand125 `1157/200` = 5.785 (09-27, B) | no |
| 30 | `1173/200` = 5.865 | `571/100` by monotonicity from `n = 29`, **V4/C3** | rep: wand125; ver: Tokoharu | rep B; ver B′ | L-W125R; L-TOK | — | no |
| 31 | `1187/200` = 5.935 (09-28) | `148/25` = 5.92, **V4/C3** (the 09-27 certificate) | wand125 | B | L-W125R | Tokoharu `571/100` (monotone, verified 09-22, B′) | no |
| 32 | `6` | `6`, **V4/C3** | Evan Daniel | C | L-EVD | wand125 `119/20` = 5.95 (09-26, B; complete replay passed, superseded) | **yes** |
| 37 | `257/40` = 6.425 | `1 + √26` = 6.099020 (Nagamochi 2005, not recent) | wand125 | B | L-W125R | wand125 `32/5` = 6.4 (09-27) | no |
| 38 | `327/50` = 6.54 | `1 + √27` = 6.196152 | wand125 | B | L-W125R | `163/25` = 6.52 (09-27) | no |
| 39 | `663/100` = 6.63 | `13/2` = 6.5, **V4/C3** (point) | wand125 | B | L-W125R; L-W125P | rectangle `331/50` = 6.62 (09-27) | no |
| 40 | `1339/200` = 6.695 | `13/2`, **V4/C3** (point) | wand125 | B | L-W125R; L-W125P | — | no |
| 41 | `1351/200` = 6.755 | `13/2` by monotonicity from `n = 39`, **V4/C3** | wand125 | B | L-W125R; L-W125P | `1349/200` = 6.745 (09-27) | no |
| 42 | `679/100` = 6.79 | `1 + √31` = 6.567764 | wand125 | B | L-W125R | `169/25` = 6.76 (09-27) | no |
| 43 | `1373/200` = 6.865 | `1 + √32` = 6.656854 | wand125 | B | L-W125R | `1371/200` = 6.855 (09-27) | no |
| 44 | `1387/200` = 6.935 | `1 + √33` = 6.744563 | wand125 | B | L-W125R | `277/40` = 6.925 (09-27) | no |
| 45 | `7` | `7`, **V4/C3**; second certificate, wand125 point-only, also **V4/C3** (same `zmx2`) | Evan Daniel; wand125 (second route, no priority claimed) | C; wand125 route C | L-EVD; L-W125X | wand125 rectangle `1391/200` = 6.955 (09-27, B; the case's reported bound until 09-29) | **yes** |
| 50 | `37/5` = 7.4 (09-28; replay running) | `1 + √37` = 7.082763 | wand125 ("wand125 after Daniel, Tokoharu") | B′ | L-W125X | same-day source rungs `3659/500` = 7.318 and `147/20` = 7.35 (not registered) | no |
| 51 | `2977/400` = 7.4425 | `1 + √38` = 7.164414 | wand125 | B | L-W125R | `743/100` = 7.43 (09-27) | no |
| 52 | `1507/200` = 7.535 | `369/50` = 7.38 from the `n = 53` point certificate's mass, **V4/C3** | wand125 | B | L-W125R; L-W125P | `1501/200` = 7.505 (09-27) | no |
| 53 | `1519/200` = 7.595 | `369/50`, **V4/C3** (point) | wand125 | B | L-W125R; L-W125P | `379/50` = 7.58 (09-27) | no |
| 54 | `3067/400` = 7.6675 | `1 + √41` = 7.403124 | wand125 | B | L-W125R | `1533/200` = 7.665 (09-27) | no |
| 55 | `771/100` = 7.71 | `377/50` = 7.54, **V4/C3** (point) | wand125 | B | L-W125R; L-W125P | `77/10` = 7.7 (09-27) | no |
| 56 | `777/100` = 7.77 | `381/50` = 7.62, **V4/C3** (point) | wand125 | B | L-W125R; L-W125P | `194/25` = 7.76 (09-27) | no |
| 57 | `1567/200` = 7.835 | `1 + √44` = 7.633250 | wand125 | B | L-W125R | `39/5` = 7.8 (09-27) | no |
| 58 | `789/100` = 7.89 | `1 + √45` = 7.708204 | wand125 | B | L-W125R | `197/25` = 7.88 (09-27) | no |
| 59 | `198/25` = 7.92 | `1 + √46` = 7.782330 | wand125 | B | L-W125R | `1581/200` = 7.905 (09-27) | no |
| 60 | `397/50` = 7.94 | `1 + √47` = 7.855655 | wand125 | B | L-W125R | `198/25` = 7.92 (09-27) | no |
| 61 | `199/25` = 7.96 (09-27, unchanged) | `1 + √48` = 7.928203 | wand125 | B | L-W125R | — | no |
| 66 | `67/8` = 8.375 | `1 + √51` = 8.141428 | wand125 | B | L-W125R | `1669/200` = 8.345 (09-27) | no |
| 67 | `1691/200` = 8.455 | `1 + √52` = 8.211103 | wand125 | B | L-W125R | `211/25` = 8.44 (09-27) | no |
| 68 | `1699/200` = 8.495 | `841/100` = 8.41 from the `n = 69` point certificate's mass, **V4/C3** | wand125 | B | L-W125R; L-W125P | `423/50` = 8.46 (09-27) | no |
| 69 | `343/40` = 8.575 | `841/100`, **V4/C3** (point) | wand125 | B | L-W125R; L-W125P | `1709/200` = 8.545 (09-27) | no |
| 70 | `431/50` = 8.62 | `171/20` = 8.55, **V4/C3** (point) | wand125 | B | L-W125R; L-W125P | `861/100` = 8.61 (09-27) | no |
| 71 | `1737/200` = 8.685 | `171/20` by monotonicity from `n = 70`, **V4/C3** | wand125 | B | L-W125R; L-W125P | `1729/200` = 8.645 (09-27) | no |
| 72 | `437/50` = 8.74 | `861/100` = 8.61, **V4/C3** (point) | wand125 | B | L-W125R; L-W125P | `1741/200` = 8.705 (09-27) | no |
| 73 | `439/50` = 8.78 | `1 + √58` = 8.615773 | wand125 | B | L-W125R | `437/50` = 8.74 (09-27) | no |
| 74 | `221/25` = 8.84 | `1 + √59` = 8.681146 | wand125 | B | L-W125R | `1763/200` = 8.815 (09-27) | no |
| 75 | `889/100` = 8.89 (09-27, unchanged) | `1 + √60` = 8.745967 | wand125 | B | L-W125R | — | no |
| 76 | `223/25` = 8.92 | `1 + √61` = 8.810250 | wand125 | B | L-W125R | `89/10` = 8.9 (09-27) | no |
| 77 | `223/25` = 8.92, by monotonicity from `n = 76` | `1 + √62` = 8.874008 | wand125 | B | L-W125R | `89/10` by the same transfer (09-27); the direct claims `222/25` = 8.88 (09-27) and `891/100` = 8.91 (09-28) are weaker | no |
| 78 | `1791/200` = 8.955 (09-27, unchanged) | `1 + √63` = 8.937254 | wand125 | B | L-W125R | — | no |
| 86 | `1871/200` = 9.355 (new 09-28) | `1 + √69` = 9.306624 | wand125 | B | L-W125R | — | no |
| 88 | `189/20` = 9.45 (new) | `1 + √71` = 9.426150 | wand125 | B | L-W125R | — | no |
| 89 | `191/20` = 9.55 (new) | `1 + √72` = 9.485281 | wand125 | B | L-W125R | — | no |
| 90 | `191/20`, by monotonicity from `n = 89` | `1 + √73` = 9.544004 | wand125 | B | L-W125R | — | no |
| 91 | `1929/200` = 9.645 (new) | `1 + √74` = 9.602325 | wand125 | B | L-W125R | — | no |
| 94 | `1959/200` = 9.795 (new) | `1 + √77` = 9.774964 | wand125 | B | L-W125R | — | no |
| 95 | `49209/5000` = 9.8418 (new) | `1 + √78` = 9.831761 | wand125 | B | L-W125R | — | no |

Sources for the rows: current values from each case's `reported_lower_bound` and
`verified_lower_bound`; wand125's superseded 09-27 values from `CASES` and its 09-28
values from `CASES_2026_09_28` in packing/devtools/audit_wand125_rectangles.py:80 and
:129; point values from `E-wand125-point-source-replay` (evidence.yaml:7); `n = 17`
history from packing/frontier/n-017.md:261–521 and
evidence.yaml:3191–3510; `n = 21` history from the working-tree n-021.md; T-NNN values
from packing/frontier/results.yaml.

### 1b. Lineage evidence (bibliography `credit` and the source's own words)

| Code | Source(s) | Bibliography `credit` | The source's own words |
| --- | --- | --- | --- |
| L-A | this project | "Squares Project (Levy)" (`PROJECT_NAME`, build_bound_citations.py:126) | results.yaml novelty `apparently-novel` for T-017…T-034 |
| L-KL11 | Kleddamag `s(11)` v1.0.2 | "Kleddamag after Levy" | "This work builds on **Joshua Levy, the squares project** … particularly the T-026 threshold certificate" and "Developed from Levy's T-026 certificate" (resources/web/external-square-certificates-2026-09-22/kleddamag-11/ATTRIBUTION.md:3–5, :13); "Built on @ojoshe’s work, with checker code adapted from @guzhou0806." (…/acquisition/x-kleddamag.txt:30) |
| L-KL17 | Kleddamag `s(17)` v1.0.0, v1.1.0, `4.66001` | "Kleddamag after Levy, Mira, Guzhou0806" on the v1.1.0 and `4.66001` keys; **none** on `[Kleddamag n17 certified bound]` (v1.0.0, bibliography.yaml:78) | "Credit **Joshua Levy, the squares project** … for the weighted-covering, strict-core, event-cell and threshold-budget lineage"; "The numerical support and parent-angle catalogue lineage comes from Mira-acc/17squares" (resources/web/n17-kleddamag-466001-2026-09-27/kleddamag-17-squares-certified-bound/ATTRIBUTION.md:46–48, :9–10) |
| L-GZ68 | Guzhou0806 R067, R068 | "Guzhou0806 after Kleddamag" (bibliography.yaml:125–150) | "The original 4.66001 charge, proof and independent JavaScript checker come from the pinned Kleddamag repository" (…/n17-guzhou-r068-2026-09-28/n17-square-packing/certificates/R068-C010/ATTRIBUTION.md:3); "historical notices for Mira, Joshua Levy and this project are retained in upstream_notices" (…/R067-4.66018/ATTRIBUTION.md:9). Class B through Kleddamag; the credit omits Levy |
| L-GZ52 | Guzhou0806 R052 (and R042–R050, continuation) | **none** (`[Guzhou0806 n17 R052]`, bibliography.yaml:115) | "the methodological lineage also includes Joshua Levy's squares project" (resources/web/n17-guzhou-r052-2026-09-25/n17-square-packing/certificates/R052/SOURCE_NOTICES.md:9) |
| L-GZ12 | Guzhou0806 R012 (T-032) | **none** (`[n17 weighted certificates 2026-09-20]`, authors Guzhou0806, Mira) | "R012 uses the decimal measure derived from **Mira's 17squares** and the weighted-covering lineage of **Joshua Levy, the squares project**" (resources/web/n17-weighted-certificates-2026-09-20/guzhou0806-n17-square-packing/NOTICE.md:5) |
| L-MIRA | Mira `4613/1000` | none (same key) | "The initial 1184-atom measure and its certificate data are by **Joshua Levy, the squares project**" (…/mira-17squares/certificates/lower_bound_4p613/ATTRIBUTION.md:3–4) |
| L-EVD | Evan Daniel (all bounds) | "Daniel after Burns, Massaccesi" | "Two independent families appeared in August 2026 … This work is a direct descendant of the second." / "**Weighted / LP family — what this repo builds on:**" Burns, Massaccesi; this project listed under "**Parallel 2026 work**", with "`s(12) ≥ 99/25` (T-017, 2026-09-04, independently of ours)" (resources/web/evand-square-packing-2026-09-28/square-packing/s12/CREDITS.md:38–41, :73–77); "jlevy/squares reached `99/25 = 3.96` independently on 2026-09-04" (…/s12/README.md:50) |
| L-TOK | Tokoharu | "Tokoharu after Levy, wand125" (bibliography.yaml:189) | "I was inspired to explore square-packing problems by @ojoshe and @wand125." (…/external-square-certificates-2026-09-22/acquisition/x-tokoharu.txt:32); wand125's repository is "a public repository by a different author that this work builds on" (…/tokoharu-density/README.md:13–16); jlevy/squares is credited for row generation, column generation and branch-and-bound only through "that repository's own README" (README.md:170–183). The rectangle-density basis and verifier are his own |
| L-W125P | wand125 point bounds (09-22) | "wand125 after Levy" | "The method is not ours." … "**jlevy/squares** added row generation via a separation oracle, dual-priced column generation, and branch-and-bound as a second Condition 5 decider" (…/wand125-points/README.md:201, :212–214); "Following the generator described in jlevy/squares (2026)" (…/wand125-points/docs/prior-art-method.md:53; the six-element table there attributes elements 4–6 to jlevy/squares) |
| L-W125R | wand125 rectangle bounds (09-27, 09-28) | "wand125 after Tokoharu, Levy" | "nothing in the mathematics is ours. What is ours is the driver, the machine time, the fixed-support route, the scaling step … and the choice of parents"; "The chains for `n = 18`, `19`, `21` and `28` go back to our own point certificates"; "The method is not ours." (resources/web/wand125-rectangle-certificates-2026-09-28/wand125-rectangles/README.md:353–355, :416, :637) |
| L-W125X | wand125 point-only `s(21)`, `s(45)`; mixed `s(50)` | "wand125 after Daniel, Tokoharu" | "wand125, building on Evan Daniel’s work for the point certificates (the `s(21)` support is his, and his `zmx2` decides `s(45)`) and on Tokoharu’s solver and verifier for the `n = 50` densities" (resources/web/wand125-point-and-mixed-2026-09-28/README.md:32); "This work does not claim priority for the value" (:51–53). Point-only routes C (via Daniel); `n = 50` B′ (via Tokoharu), credit omits Levy |

### 1c. Recent results that hold no current bound, and 2026 bounds before the cutoff

Recent, moving no current bound:

- `n = 13`: Evan Daniel's case-free zero-margin closed cover for Bentz's `s(13) = 4`
  (reported, `E-n013-evand-casefree-cover-report`, evidence.yaml:2926), class C.
- `n = 11`: Tokoharu's `381/100` (verified replay, B′) and Daniel's `3040/797` (C,
  retained, unregistered) — in the table's history column.
- `n = 45`: wand125's point-only `s(45) = 7` (verified `V4/C3`, second certificate), and
  `n = 21` point-only (reported) — in the table.
- `n = 17`: second-hand report of Kleddamag's unpublished `4.62001` (not recorded as a
  bound, packing/frontier/n-017.md:496).
- Lean: the record carries Daniel's `s32_eq_six_of_checker` and `s21_eq_five_of_checker`
  and wand125's `n21pts_eq_five_of_checker` as reductions from one hypothesis; the
  source reports hypothesis-free kernel checks of `s(13) = 4` and `s(32) = 6`; none was
  built here. chelokot's Lean archive (kernel-checked known values, per Daniel's
  CREDITS.md:89–93) is not retained.

2026 lower bounds dated before 22 August (not recent under the rule; all superseded;
all at `n = 17`, some also 18):

| Date | Bound | Author | Class |
| --- | --- | --- | --- |
| 07-18 | `89/20` = 4.45, exact sixteen-point capsule | Kim Brandwijk | C |
| 08-06 | `44811/10000` = 4.4811, weighted | Sam Burns | C |
| 08-08 | `(40√2 + 19)/17 + 1/200` ≈ 4.4502084, `s(17)`, `s(18)` (source-reported) | David R. MacIver | C |
| 08-10, 08-11 | 4.450837, 4.468292, sixteen-point subdivision | Mira | C |
| 08-11 | 4.456575, sixteen-point subdivision | Stanislav Fort | C |
| 08-13, 08-16 | 4.57, `9141/2000` = 4.5705, weighted + Lean 4 layer | anabologyco-maker | C |
| 08-21 | `22529/5000` = 4.5058 (registered as T-015/T-016 on 09-03) | Gustavo Massaccesi | C |

## 2. Per source

**This project (class A).** Weighted fractional unavoidable-set certificates found by
its own LP generator (row generation by a Condition-5 separation oracle, dual-priced
column generation), point atoms and then threshold atoms, each certificate decided twice
from frozen bytes (exact event-cell sweep, interval branch and bound), plus exact
dilation-limit corollaries. Since 22 August: `s(11)` from `381/100` (T-018, 09-04) to
3.8269975 (T-033, 09-22); `s(12) ≥ 99/25` (T-017); `s(17)` 4.426213 (T-001) and
`459/100` (T-019); the `n = 18` ladder to `4679/1000` (T-030); `s(19) ≥ 24/5` (T-020);
`s(20) ≥ 97/20` (T-021); `s(21) ≥ 122/25` (T-034); the Stromquist repair (T-010) and
the external registrations T-015/T-016 and T-032. **Holds now:** the verified lane at
`n = 18, 19, 20` (3 of the 27 stars); no case in the reported lane, where wand125's
`939/200`, `963/200`, `979/200` stand above. Its certificates are the starting point of
the Kleddamag (`n = 11`, `17`), Mira, Guzhou0806 and wand125 lines. T-017's claim "the
first lower bound specific to `n = 12` in the retained corpus" is now contradicted by the
retained corpus: Daniel's `15680/3951` entered his source on 2026-08-25.

**Kleddamag (class B).** Parent-core certificates: parent squares of side `A` in a
container of side `L`, a catalogue of rational parent-angle intervals each with its own
strict closed core, point and `k`-of-`m` threshold charges (and, from `v1.1.0`,
weighted-threshold and pairwise-intersecting winning-subset rules), decided by exact
event-cell sweeps in Python rationals and JavaScript BigInt; the bound is `L/A`. Work
produced with OpenAI Codex under Kleddamag's direction. `s(11) > 31/8` (09-22),
developed from T-026's certificate, confirmed here at `V4/C4` by this repository's native
parent-core interval route; at `n = 17`, `461300/99853` (09-21), `232001/50000` (09-26),
`466001/100000` (09-27), each `V4/C3`. **Holds now:** `n = 11` (both lanes). Its
`4.66001` charge is the base of Guzhou0806's R067/R068.

**Guzhou0806 / N17 project (class B).** R012 (09-20) restricted Mira's T-019-derived
measure to real parents (side `99999/100000`, 2,925 parent-angle intervals, legal
parent centres), `461300/99999`, registered as T-032 at `V4/C4`; R038 (reported,
retained, not replayed); R042/R043/R050/R052 and the R052 continuation on Kleddamag's
`v1.0.0` architecture, R052 (`231001/50000`, 09-25) replayed at `V4/C3`; R067
(`233009/50000`) and R068 (`116511/25000`, 09-28) re-core and refine Kleddamag's
`4.66001` charge (R068 adds one four-site point orbit, 4,991 intervals), decided by
Guzhou0806's own C++ checker and Kleddamag's Node BigInt checker; the publisher ran no
local validation. AI assistance disclosed. **Holds now:** `n = 17` (both lanes,
pending), `V4/C3`.

**Mira (class B for the recent bound).** `s(17) ≥ 4613/1000` (09-07): 1,620 atoms
written in this repository's certificate schema, starting from T-019's 1,184 atoms, on
a 2,880-step net; decided here by both stock verifiers. Mira's later support
(`lower_bound_4p614153`) is the numerical support Kleddamag's `n = 17` releases and R038
build on. Mira's 10–11 August sixteen-point subdivision certificates (4.450837,
4.468292) are class C and predate the cutoff. **Holds now:** nothing; ancestor of the
whole current `n = 17` line.

**Stanislav Fort (class C, pre-cutoff).** `s(17) > 4.456575` (11 August), an exact
sixteen-point certificate by dyadic pose-space subdivision, produced by GPT-5.6-Sol; the
author "can't vouch for its correctness" (resources/web/n17-github-certificates-2026/stanislavfort-17squares/README.md:1).
Replayed here under its own checker (`E-n017-fort-point-certificate-replay`). Not recent
under the rule. **Holds now:** nothing.

**Evan Daniel (class C).** Builds on Burns's and Massaccesi's weighted exact-rational
covering method and lists this project as parallel work. Angle-net certificates checked
by a Rust verifier (`s(12) ≥ 15680/3951`, in his source 2026-08-25; `s(21) ≥ 5000/1001`,
09-23; `s(11) ≥ 3040/797`, found 08-26, published 09-22), zero-margin closed covers
decided by exact pose-space subdivision (`s(13) = 4` case-free; `s(32) = 6`, 09-26), and
mixed covers of weighted points plus uniform mass on interior grid-line segments
(`s(21) = 5`, `s(45) = 7`, 09-27/28), each certified by two checkers that share no
code (`zm_mixed.py` exact, `zmx2` binary64 enclosures), with Lean reductions. Produced
with an AI agent under human direction. **Holds now:** `n = 12` (`V4/C4`), and the
exact values `s(21) = 5`, `s(32) = 6`, `s(45) = 7` (each `V4/C3`): 4 cases, 3 of them
closed.

**Tokoharu (class B′).** Generalises wand125's point-mass basis to uniform densities on
axis-aligned rectangles, `D4`-symmetrised, with an outward-rounded interval verifier
(`verify.cpp`) over a 201-direction net; "inspired … by @ojoshe and @wand125", with
this project credited second-hand. `s(26) ≥ 1377/250`, `s(29) ≥ 571/100` (09-22), and
`s(11) ≥ 381/100` (equal to T-018). **Holds now:** the verified lane at `n = 26, 29, 30`
(`V4/C3`); nothing in the reported lane (wand125's certificates, built with his solver,
stand above).

**wand125 (class B; C for the point-only routes; B′ for `n = 50`).** Three bodies of
work. (1) Point certificates (09-15 to 09-22) from the generator described in
jlevy/squares, checked with this project's `sqpack` verifier: `s(39), s(40) ≥ 13/2`,
`s(53) ≥ 369/50`, `s(55) ≥ 377/50`, `s(56) ≥ 381/50`, `s(69) ≥ 841/100`,
`s(70) ≥ 171/20`, `s(72) ≥ 861/100` (and 26, 29, since superseded). (2) Rectangle-density
ladders with Tokoharu's solver and unchanged verifier: 44 standing certificates at
`ad43d29` (09-26/27, `n = 18–78`), 50 standing at `39d8ecc` (09-28, `n = 18–95`, 38 new
or raised, six new counts 86, 88, 89, 91, 94, 95). (3) 09-28: point-only `s(21) = 5`
and `s(45) = 7` on Daniel's support and checker (no priority claimed), and `s(50) ≥ 37/5`
with a threshold-one research copy of Tokoharu's verifier. Tools published 09-29 as
`wand125/square-packing-tools`. **Holds now:** the reported lane at 49 counts (18, 19,
20, 26–31, 37–44, 50–61, 66–78, 86, 88–91, 94, 95); the verified lane at 15 (27, 28,
31; 39, 40, 41, 52, 53, 55, 56, 68, 69, 70, 71, 72); and the second certificate for
`s(45) = 7`.

**Others the records name for a 2026 lower bound.** Sam Burns (4.4811, 08-06, C),
Gustavo Massaccesi (4.5058, 08-21, C; T-015/T-016), anabologyco-maker (`9141/2000`,
08-16, C), Kim Brandwijk (`89/20`, 07-18, C), David R. MacIver (4.4502084, 08-08, C,
source-reported), ahyangyi (≈ 4.6136817, 09-23, not assessed, not retained). None holds
a case. UnitSquare Project (07-29) contributes upper bounds only.

## 3. Document audit

Each item: file:line, current text, whether it is still correct after the pending
registrations, and the proposed replacement. "Omits" items list results the document
should carry under the owner's position.

### 3.1 README.md

1. **README.md:15–17** — "With them come the first lower bounds located in the public
   record for twelve, twenty and twenty-one squares, and bounds for seventeen through
   twenty-one squares that improved on the published ones." **Incorrect.** For twelve,
   Daniel's `15680/3951` entered his source on 2026-08-25 (packing/frontier/n-012.md:121; his README says
   "public 2026-08-26"), before T-017 (2026-09-04). For twenty and twenty-one, the DS7
   audit records size-specific reported bounds (Table 2 lists `6√2 − 4` at `n = 19–20`,
   packing/frontier/n-020.md:139–140; the opaque 4.7438 at `n = 21`, n-021.md:234), and Nagamochi's general
   formula applies to both; T-020's own rationale says the audit "corrects the earlier
   claim that no size-specific bounds had been reported" (packing/frontier/results.yaml:983).
   Replace with: "With them come `s(12) ≥ 99/25`, reached independently of Evan Daniel's
   stronger `15680/3951` (in his repository from 25 August, first seen here on 27
   September), the first proved bounds specific to twenty and twenty-one squares, and
   bounds for seventeen through twenty-one squares that improved on the published ones."
2. **README.md:18–19** — "The bounds for eighteen, nineteen and twenty squares are still
   the verified ones; the others have since been raised by the results below." Correct;
   under the owner's position append: "wand125's reported rectangle bounds, `939/200`,
   `963/200` and `979/200`, stand above all three until their replays run."
3. **README.md:20–24** — "Others have built on these certificates, credited them and
   taken the bounds further, and one has worked in parallel from the same weighted
   method. This repository takes in each result, replays its certificate, reviews its
   mathematics, and registers the bound credited to its authors." The first sentence is
   still true (one parallel author, Evan Daniel; wand125's point-only routes derive from
   his). The second is **inaccurate**: 28 of the 55 recent bounds are registered as
   *reported* before any replay. Replace the second with: "This repository registers
   each claimed bound as reported when it takes the source in, and as verified only
   after a complete replay and a review of its mathematics."
4. **README.md:25–31** (`s(11) > 31/8`, Kleddamag) — correct.
5. **README.md:32–40** — "**`s(17) > 466001/100000 = 4.66001`**, by Kleddamag, building
   on Squares Project (Joshua Levy), Mira and Guzhou0806: [link to 57519bb]. Six
   certificates at seventeen squares trace their support back to T-019’s atoms, and
   this is the strongest; it is the verified lower bound, about `0.0155` below
   Bidwell’s packing." **Stale.** Replace with: "**`s(17) > 116511/25000 = 4.66044`**, by
   Guzhou0806, continuing Kleddamag's `4.66001` charge (Kleddamag building on Squares
   Project (Joshua Levy), Mira and Guzhou0806):
   [Guzhou0806/n17-square-packing R068 at `815b162`](https://github.com/Guzhou0806/n17-square-packing/tree/815b16261f852e389968513eec94b4b9e5b3206d/certificates/R068-C010).
   Eight replayed certificates at seventeen squares trace their support back to T-019’s
   atoms, and this is the strongest; it is the verified lower bound (`V4/C3`), about
   `0.0151` below Bidwell’s packing. Recorded here: the
   [retained copy](packing/resources/web/n17-guzhou-r068-2026-09-28/README.md), the
   [review](docs/project/reviews/review-2026-09-28-n17-guzhou-r067-r068.md) and the
   [case record](packing/frontier/n-017.md)." Count: see §3.10.
6. **README.md:41–43** — "Evan Daniel’s `s(32) = 6`, `s(21) ≥ 5000/1001` and
   `s(12) ≥ 15680/3951`, from Burns’s and Massaccesi’s weighted method, and Tokoharu’s and
   wand125’s density and point bounds for `n = 26` to `72`, are registered the same
   way." **Stale.** Replace with: "Evan Daniel's `s(21) = 5`, `s(32) = 6` and `s(45) = 7`,
   the first exact values of `s(k² − 4)` for `k ≥ 4`, and his `s(12) ≥ 15680/3951`, all
   from Burns's and Massaccesi's weighted method and independent of this project; and
   wand125's and Tokoharu's point and rectangle-density bounds for `n = 18` to `95`,
   `s(50) ≥ 37/5` among them, most still reported pending replay."
7. **README.md:44–48** — "Twenty-six of the lower bounds it shows are recent results,
   proved since August 2026; three of them are this project’s." **Stale count and loose
   date.** Replace with: "Fifty-five of its hundred cases carry a lower bound proved
   since 22 August 2026, twenty-seven of them verified here; three of those are this
   project's, and three are new exact values." Computation in §3.10.
8. **README.md:54–57** (explainer paragraph) — correct.
9. **README.md:64–65** (atlas caption) — "A crimson star marks a recent result, a lower
   bound proved since August 2026" — the star follows the verified lane only and the
   rule is 22 August: "…a verified lower bound proved since 22 August 2026".
10. **README.md:164–165** — correct.
11. **README.md:176–187** (T-019's list of August bounds) — correct as history.
12. **README.md:206–209** — "…and `T-034` has raised `n = 21` again to `122/25`, leaving
    `0.1085`; this `24/5` rung remains current for `n = 19`. Evan Daniel’s certificate at
    `5000/1001`, below, now carries `n = 21`." **Stale.** Replace the last sentence with:
    "Evan Daniel has since proved `s(21) = 5`, below."
13. **README.md:210–220** (T-017) — "the frontier record said in as many words that
    nothing specific to `n = 12` had ever been proved" is true of the record at the time
    but not of the public record; append after "…has since narrowed that to about
    `0.0314`": "; his certificate was in his repository from 25 August, before T-017, and
    T-017 was reached independently of it."
14. **README.md:247–249** (T-021) — "`T-034` has since raised `n = 21` to `122/25`, and
    Evan Daniel’s certificate to `5000/1001`; `97/20` remains current for `n = 20`."
    **Stale.** → "`T-034` has since raised `n = 21` to `122/25`, and Evan Daniel has
    proved `s(21) = 5`; `97/20` remains the verified bound for `n = 20`, below wand125's
    reported `979/200`."
15. **README.md:259** (T-034) — "Evan Daniel’s `5000/1001`, below, has since superseded it
    on that case." → "Evan Daniel's `5000/1001` and then his `s(21) = 5`, below, have
    since superseded it."
16. **README.md:280–281** (T-030) — "The last rung, `T-030` at `4679/1000`, is the current
    survey lower bound" → "…is the current verified lower bound; wand125's reported
    `939/200` stands above it pending replay".
17. **README.md:348–352** — "…and only then registers the bound, with its credit."
    **Inaccurate** (reported registrations). Same fix as item 3.
18. **README.md:354–381** (Evan Daniel) — heading "`s(32) = 6`, `s(21) ≥ 5000/1001` and
    `s(12) ≥ 15680/3951`" and "proves the first exact value of `s(k² − 4)` for any
    `k ≥ 4`" and "…are now the verified lower bounds there, above `T-034` and `T-017`;
    `s(21)` is left within `5/1001` of the grid." **Stale.** Rewrite heading as "**Evan
    Daniel: `s(21) = 5`, `s(32) = 6`, `s(45) = 7` and `s(12) ≥ 15680/3951`.**" and add,
    after the `s(32)` sentences: "On 28 September the same repository proved `s(21) = 5`
    and `s(45) = 7` by *mixed covers* — weighted points plus mass spread along interior
    grid-line segments — each certified at margin zero by two checkers that share no
    code, `zm_mixed.py` in exact arithmetic and the Rust `zmx2` in outward-widened
    binary64 intervals, with a Lean reduction for `s(21)`. Complete `zmx2` sweeps pass
    here for both, registered at `V4/C3`; recording the exact checker's complete
    re-sweep would make them `C4`. With `s(32) = 6` these are the first three exact
    values of `s(k² − 4)` for `k ≥ 4`. Its earlier `5000/1001` for twenty-one squares
    remains valid evidence." Replace "`s(21)` is left within `5/1001` of the grid" with
    "the `s(12)` certificate leaves that case about `0.0314` below the grid".
19. **README.md:383–397** (wand125 rectangles) — "**wand125, building on Tokoharu’s
    rectangle-density method: `n = 18` to `78`.** The rectangle-density certificates of
    26 and 27 September 2026, 44 standing ones, … except at `n = 21` and `n = 32`, where
    Evan Daniel’s bounds are stronger. … about 102 CPU-hours in all, are run."
    **Stale.** Replace with: "**wand125, building on Tokoharu’s rectangle-density
    method: `n = 18` to `95`.** 44 standing certificates of 26 and 27 September and 50 of
    28 September (`39d8ecc`), 38 of them new or raised and six at counts not reached
    before (`n = 86, 88, 89, 91, 94, 95`), were built with Tokoharu's solver and are
    decided by his unchanged interval verifier … Each improves the reported lower bound
    this record held for its count, except at `n = 21`, `32` and `45`, where Evan
    Daniel's exact values are stronger. Complete replays have passed here at `n = 27` and
    `31` … the other counts stay reported until their replays, 47 certificates and about
    134 CPU-hours by the September 28 packet's plan, are run." (plan:
    resources/web/wand125-rectangle-certificates-2026-09-28/README.md:191–194)
20. **README.md:399–413** (Kleddamag `s(11)`) — correct.
21. **README.md:415–434** (Kleddamag `4.66001`) — "It is the verified lower bound for
    seventeen squares, exactly `0.01999` above `v1.1.0` and `0.0155` below Bidwell’s
    packing." **Stale.** → "It was the verified lower bound for seventeen squares from 27
    to 29 September 2026, exactly `0.01999` above `v1.1.0`, and it remains valid
    evidence." Also link the review, now retained, instead of the code path at :431–432.
22. **README.md:501–503** (T-032) — "It was the first external bound registered here and
    is the only one with a `T-NNN` identifier; the later external bounds are recorded in
    their case files." **Incorrect**: T-015 and T-016 (Massaccesi's `4.5058`, registered
    2026-09-03, `previously-published`) are earlier external bounds with `T-NNN`
    identifiers. → "Like T-015 and T-016 before it, it carries a `T-NNN` identifier; the
    external bounds registered since are recorded in their case files."
23. **README.md:518–521** (Survey) — "…and the `n = 11` and `n = 17` rows record
    Kleddamag’s `n = 11` bound and Kleddamag’s `4.66001` `n = 17` bound under Results by
    Others." **Stale.** → "…the `n = 11` row records Kleddamag's `31/8` and the `n = 17`
    row Guzhou0806's `116511/25000`, and the `n = 21`, `32` and `45` rows Evan Daniel's
    exact values, under Results by Others." :523–525 (Tokoharu verified at 26, 29) is
    correct.
24. **Omits** (under the owner's position): a Guzhou0806 R067/R068 bullet at the head of
    the `n = 17` group; a Tokoharu bullet (only the Survey paragraph names him); a
    wand125 point-bounds bullet (the 22 September certificates that hold 12 verified
    counts); a wand125 point-only/mixed bullet (`s(21)`, `s(45)` second routes,
    `s(50) ≥ 37/5`); Daniel's `s(11) ≥ 3040/797` (retained, unregistered); the pre-cutoff
    August bounds as a group (they are only inside the T-019 bullet); a statement of the
    lineage split (§4). Proposed Guzhou0806 bullet: "**Guzhou0806, continuing Kleddamag's
    `4.66001` charge: `s(17) > 116511/25000 = 4.66044`.** The R068 release of 28 September
    2026 keeps that charge's 889 rule orbits, moves one zero-weight site orbit and adds
    one weighted four-site point orbit, over 4,991 angle intervals, with a counting
    surplus of 7,404 units of `10⁻⁹`; its C++ checker is Guzhou0806's own and its BigInt
    checker Kleddamag's. Its publisher ran no local validation; both checkers' complete
    paired replays pass here and agree with the published ledgers on every row, so it is
    the verified lower bound at `V4/C3`, exactly `0.00043` above `4.66001`. R067,
    `233009/50000`, the same day on the unchanged charge, was replayed beside it. AI
    assistance is disclosed."

### 3.2 SYNOPSIS.md

1. **SYNOPSIS.md:108–115** — "The same day `s(17) > 466001/100000 = 4.66001` followed …
   It supplies the verified Frontier bound for `n = 17`, `0.0155` below Bidwell’s packing"
   **Stale.** Change "It supplies" to "It supplied the verified Frontier bound for
   `n = 17` from 27 to 29 September" and add: "Guzhou0806's R068 of 28 September,
   continuing that charge with one added point orbit over 4,991 intervals, proves
   `s(17) > 116511/25000 = 4.66044`, exactly `0.00043` higher; its complete paired
   replay passes here at `V4/C3`, and it supplies the verified bound, `0.0151` below
   Bidwell's packing. R067, `233009/50000`, was replayed beside it."
2. **SYNOPSIS.md:118–123** — "proves `s(32) = 6` … at `V4/C1` until its complete re-sweep
   runs here, and its angle-net certificates `s(12) ≥ 15680/3951` and
   `s(21) ≥ 5000/1001` pass the source’s verifier here at `V4/C3`" **Stale** (the
   re-sweep ran; `s(12)` is `V4/C4`; `s(21)` is now 5). → "proves `s(32) = 6` … at
   `V4/C3` on a complete re-sweep here, and `s(12) ≥ 15680/3951` at `V4/C4`; its
   `s(21) ≥ 5000/1001` was superseded on 28 September by the same author's mixed covers
   proving `s(21) = 5` and `s(45) = 7`, both `V4/C3`."
3. **SYNOPSIS.md:123–126** — "wand125’s 44 rectangle-density certificates for `n = 18` to
   `78` … verified at `n = 27`, `28` by monotonicity, and `31`, and reported at the other
   counts" **Stale count.** → "wand125's rectangle-density certificates, 44 at `ad43d29`
   and 50 standing at `39d8ecc` (`n = 18` to `95`) …"; add "wand125's point-only
   routes to `s(21) = 5` and `s(45) = 7` (the latter verified here as a second
   certificate) and its `s(50) ≥ 37/5` (reported) followed on 28 September."
4. **SYNOPSIS.md:3776** — "| 1–100 | 36 proved, 64 open |" **Stale.** → "38 proved,
   62 open".
5. **SYNOPSIS.md:6504–6507** — "`s(12) >= 99/25` is T-017, the first bound located that
   was proved about twelve squares rather than inherited from eleven" **Incorrect** (see
   3.1 item 1). → "…T-017, reached independently of Evan Daniel's stronger
   `15680/3951`, which was in his repository from 25 August; the case bound is now …".
6. **SYNOPSIS.md:6513–6517** — "…and twenty and twenty-one had never carried a bound of
   their own at all. The `n = 21` case bound is now Evan Daniel’s third-party
   `5000/1001`…" **Incorrect and stale.** → "…and twenty and twenty-one had never carried
   a proved bound of their own. Evan Daniel has since proved `s(21) = 5`
   ([`n-021`](packing/frontier/n-021.md))."
7. **SYNOPSIS.md:6564–6566** — "At `n = 19`, `20` and `21` the ceiling is `5B = 4.9885`,
   so `T-020` has `0.1885` above it at twenty and twenty-one" — historical measurement,
   still true of the method; append "`s(21) = 5` was reached by a mixed cover, a
   certificate of a different shape".
8. **Omits:** R068/R067; Daniel's `s(21) = 5`, `s(45) = 7`; wand125's point-only and
   `n = 50` results; a pointer to a single all-sources table. The dated handoff records
   (SYNOPSIS.md:1158 onward) are session history and need no change.

### 3.3 TUTORIAL.md

- **TUTORIAL.md:92** ("strongest verified lower bound | `31/8 = 3.875`, strict |
  Kleddamag 2026, developed from T-026’s certificate …") and :105–107 — correct.
- :461–465 — correct. No recent-bound or holder statement is stale; the tutorial covers
  `n = 11` only. The link `README.md#results-by-others` (:92) breaks if §4 renames the
  section.

### 3.4 packing/frontier/README.md

1. **:134** — "There are currently 60 proved and 264 open formal cases." → "62 proved and
   262 open".
2. **:385** — "Of the 264 open cases, **239** have Nagamochi’s formula as their verified
   lower bound." → "Of the 262 open cases, **238** …" (gated, see §3.10).
3. **:386–389** — "Seven others … `n = 17` (`466001/100000`) and `n = 21` (`5000/1001`),
   plus the first-party bounds at `n = 18` …" → "Six others use certificates already
   integrated into the register: current external certificate bounds at `n = 11`
   (`31/8`), `n = 12` (`15680/3951`) and `n = 17` (`116511/25000`), plus the first-party
   bounds at `n = 18` (`4679/1000`), `n = 19` (`24/5`) and `n = 20` (`97/20`)."
4. **:389–393** — "Complete interval and exact replays add 18 more external-certificate
   cases: `n = 26,27,28` at `1377/250`; `n = 29,30,31` at `571/100`; …" **Stale since
   2026-09-27** (count right, values wrong). → "…: `n = 26` at `1377/250` and
   `n = 29, 30` at `571/100` (Tokoharu); `n = 27, 28` at `28/5` and `n = 31` at `148/25`
   (wand125's rectangle certificates); `n = 39,40,41` at `13/2`; …" (rest unchanged).
5. **:393–395** — "`n = 32` left the open cases on 2026-09-27 … Within the original
   `n ≤ 100` corpus, the corresponding Nagamochi count is 39." → "`n = 32` left the open
   cases on 2026-09-27, and `n = 21` and `n = 45` on 2026-09-29, when replayed external
   covers proved `s(32) = 6`, `s(21) = 5` and `s(45) = 7`. Within the original `n ≤ 100`
   corpus, the corresponding Nagamochi count is 38."
6. **:399** — "Of the 264 open cases, 119 are still held by the trivial grid." → "Of the
   262 open cases, 117 …" (:400 "The other 145" and :401 "34 non-grid open cases"
   unchanged).
7. **:414–420** (five smallest gaps) — rows 21 and 17 stale. New table: 11 `0.0021`
   (Trump 1979, "carried to `31/8` by Kleddamag after Levy"); 17 `0.0151` (Bidwell,
   "carried to `116511/25000` by Guzhou0806 after Kleddamag"); 12 `0.0314` (grid, "`4² − 4`,
   carried to `15680/3951` by Daniel after Burns, Massaccesi"); 97 `0.0557` (grid,
   `10² − 3`); 78 `0.0627` (grid, `9² − 3`).
8. **:422–426** — "The `n = 17` bound is Kleddamag … All four leaders moved in September
   2026 on third-party weighted certificates, and the `k² − 4` family now has one solved
   member above `k = 3`: `s(32) = 6` …" → "The `n = 17` bound is Guzhou0806's R068,
   continuing Kleddamag's charge (Kleddamag building on Squares Project (Joshua Levy),
   Mira and Guzhou0806). Three of the five leaders moved in September 2026 on others'
   weighted certificates, and the `k² − 4` family now has three solved members above
   `k = 3`: `s(21) = 5`, `s(32) = 6` and `s(45) = 7`, all by Evan Daniel; `s(12)` is the
   open one."
9. **:428–432** — "Next come `n = 78` at `0.0627` and `n = 61` at `0.0718`; with `n = 97`
   they are consecutive unproved members of the family `s(m² − 3) = m`" → "Next comes
   `n = 61` at `0.0718`; with `n = 78` and `n = 97` it is one of three consecutive
   unproved members …".
10. **:437–440** — "Among the cases with a *non-trivial* record, `n = 19` follows `n = 11`
    and `n = 17` at `0.0856`, then `n = 18` at `0.1439`." **Stale since 2026-09-22/27**:
    `n = 27` (`0.1071`) and `n = 26` (`0.1133`) now come before `n = 18`. → "…`n = 19`
    follows `n = 11` and `n = 17` at `0.0856`, then `n = 27` at `0.1071`, `n = 26` at
    `0.1133` and `n = 18` at `0.1439`. First-party certificates moved 17, 18 and 19
    beginning on 2026-09-04; external certificates now carry `n = 11`, `17`, `26` and
    `27`, and wand125's reported rectangle bounds stand above the verified values at
    18 and 19."
11. **Omits:** any count of recent results or of who holds them; a pointer to the
    all-sources table.

### 3.5 packing/frontier/STATUS.md (generated, note only)

Generated by `devtools.render_research_tables`. After n-017 lands and the renderer
runs, row 17 reads `116511/25000` in both lower columns; rows 21, 45 already read
`proved`. It has no holder or recency column; the §4 table would supply one.

### 3.6 packing/atlas/known-best/README.md and FIGURE-PLAYBOOK.md

- The atlas README states no recent bound or holder; the figure itself does.
  `composite-figure.json` is **not yet rebuilt**: it stars 26 cases, shows
  `s(21) ≥ 4.995004`, does not star 45 and shows `s(17) ≥ 4.66001`.
  `bound-citations.json` (working tree) already stars 45, so
  `tests/test_bound_citations.py::test_the_recent_lower_bounds_are_exactly_the_starred_cases`
  **fails now** (run here: extra item 45). Rebuild with
  `build_composite_figure_data --update` and `build_known_best_atlas` after n-017 lands.
- **FIGURE-PLAYBOOK.md:92** — "| `s(n) ≥ …` second line | … shown where `status` is
  `open` | 65 lines; …" **Stale** (composite draws 64 now; 62 after the rebuild) →
  "62 lines".
- **FIGURE-PLAYBOOK.md:93** — "26 cases: `n = 11, 12, 17–21, 26–32, 39–41, 52, 53, 55,
  56, 68–72`, 3 of them (`n = 18, 19, 20`) proved here" → "27 cases: `n = 11, 12, 17–21,
  26–32, 39–41, 45, 52, 53, 55, 56, 68–72`, 3 of them (`n = 18, 19, 20`) proved here;
  the star follows the verified lane, so the 28 cases whose recent bound is reported
  only carry none".

### 3.7 docs/project/research/research-2026-08-22-packing-11-unit-squares.md

1. **:3–12, :35–52** — the dated "Current Summary Through 2026-09-06" (T-022's
   3.8100257) is labelled as dated, so not false, but a reader meets it first. Add after
   :36: "Since then T-033 reached `3.8269975…` (22 September) and Kleddamag's
   `s(11) > 31/8`, developed from T-026's certificate, is the verified bound; see
   [`n-011`](../../../packing/frontier/n-011.md)."
2. **:882** (generated `frontier-open` row 17: "4.66001 | elementary | 0.0155") —
   regenerates to `4.66044 … 0.0151`. The "from" column renders every certificate bound
   (`kind: counting`) as "elementary" (render_research_tables.py:76), which mislabels
   weighted, rectangle-density and mixed-cover certificates (rows 11–95 and solved rows
   21, 32, 45); propose "certificate" for `counting` bounds whose evidence is a
   certificate replay.
3. **:1381** — "No machine-checked `s(n)` theorem is on record." **Stale**: the record
   carries Lean reductions `s32_eq_six_of_checker`, `s21_eq_five_of_checker` (Daniel) and
   `n21pts_eq_five_of_checker` (wand125), and Daniel reports hypothesis-free kernel checks
   of `s(13) = 4` and `s(32) = 6` (none built here). → "Lean reductions of `s(21) = 5` and
   `s(32) = 6` to one computational hypothesis are on record (Evan Daniel, September
   2026), and the source reports kernel checks of `s(13) = 4` and `s(32) = 6`; none has
   been built here."
4. **:2306** — "Neither current verified 459/100 lower bound depends on these artifacts."
   **Stale.** → "No verified lower bound at `n = 17` or `n = 18` depends on these
   artifacts."

### 3.8 packing/devtools/templates/explainer-article.md (source of the generated page)

1. **:56–61** (Frontier update, 22 September, `s(11)`) — correct.
2. **:124–128** — "These include improved lower bounds for `n = 12`, `17`, and
   `19`.[^other-results]" and "…currently includes {{N_PROVED_HERE}} new lower bounds
   proved here." True of the register; under the owner's position append "since raised
   by others at `n = 12` and `17`".
3. **:195–197** (Figure 2 caption) — "A crimson star marks a recent result, a lower bound
   proved since {{RECENT_SINCE_MONTH}}: {{N_STARRED}} of the hundred, {{N_PROVED_HERE}}
   of them here." Counts are derived (render_explainer.py:1918–1932 from
   composite-figure.json totals) and become 27 and 3 on rebuild. `RECENT_SINCE_MONTH`
   renders "August 2026" (render_explainer.py:2236) while the rule is 22 August; render
   `{RECENT_SINCE:%-d %B %Y}` instead, and say "a verified lower bound".
4. **:893–896** (`[^other-results]`) — add "since superseded at `n = 12` by Evan Daniel
   and at `n = 17` by the Kleddamag–Guzhou0806 line".

### 3.9 packing/resources/README.md (Web Sources intro prose)

1. **:462–469** (September 22 packet) and **:471–477** (September 27 wand125 packet, "44
   counts from `n = 18` to `n = 78`") — correct for those packets.
2. **:479–485** — "keeps two messages wand125 sent the owner on X" **Stale**: the packet
   holds three since `7837df37` (supplied-message-3-2026-09-29.txt, announcing
   wand125/square-packing-tools). → "keeps three messages wand125 sent the owner on X
   (two on 28 September, one on 29 September)…". The packet's own README line 3 ("This
   packet keeps two messages") has the same defect.
3. **Omits** an intro paragraph for the 28 September packets (the 50-certificate
   rectangle packet, the point-and-mixed packet, evand 2026-09-28, R068) and any
   statement of lineage; proposed: "Since 22 August 2026 the archive has retained every
   public certificate that moved a lower bound here: those that build on this project's
   certificates or pipeline (Kleddamag, Guzhou0806, Mira, wand125, and Tokoharu through
   wand125) and those independent of it (Evan Daniel, on Burns's and Massaccesi's
   method). Each key's `credit` in `bibliography.yaml` names the lineage."

### 3.10 Counts stated in prose: recomputation and gates

| Where | Current text | After the pending registrations | Computation | Gate |
| --- | --- | --- | --- | --- |
| README.md:46–48 | "Twenty-six … recent …; three of them are this project’s" | 27 verified-lane stars, 3 this project's; 55 in either lane | stars: 11, 12, 17, 18, 19, 20, 21, 26, 27, 28, 29, 30, 31, 32, 39, 40, 41, 45, 52, 53, 55, 56, 68, 69, 70, 71, 72 (= composite 26 + `n = 45`); project: 18, 19, 20; either lane: the headline table | **none** (check_readme.py has no such check; the explainer caption is derived) |
| README.md:35 | "Six certificates at seventeen squares trace their support back to T-019’s atoms" | **eight** replayed and registered (Mira `4613/1000`, R012, Kleddamag v1.0.0, R052, v1.1.0, `4.66001`, R067, R068); thirteen with the five publication records (R038, R042, R043, R050, R052 continuation) | history of the phrase: three on 09-22 (`42fc48fc`), four on 09-25, six on 09-27 (`63368dce`), i.e. it counts certificates with verified evidence entries | none |
| README.md:20–22 | "one has worked in parallel" | still one (Evan Daniel) | L-EVD; wand125's point-only routes derive from Daniel | none |
| README.md:383, :385 | "`n = 18` to `78`", "44 standing ones" | `n = 18` to `95`, 50 standing, 38 new or raised | `CASES_2026_09_28` has 50 entries; `E-wand125-rectangle-2026-09-28-report` scope has 38 | none |
| README.md:392 | "about 102 CPU-hours in all" | 47 certificates, about 134 CPU-hours | 09-28 packet README:191–194 | none |
| README.md:357 | "the first exact value of `s(k² − 4)` for any `k ≥ 4`" | first of three (21, 32, 45) | packing/frontier/n-021.md:130–132 (working tree) | none |
| README.md:501–502 | "the only one with a `T-NNN` identifier" | false: T-015, T-016, T-032 | results.yaml novelty `previously-published` | none |
| README.md:37, SYNOPSIS.md:112 | "`0.0155` below Bidwell’s" | `0.0151` | 4.67553009360455 − 4.66044 = 0.01509009 | none |
| SYNOPSIS.md:120 | "`V4/C1`" (`s(32)`) | `V4/C3` | README.md:363–372; n-032.md:149 | none |
| SYNOPSIS.md:123 | "44 rectangle-density certificates for `n = 18` to `78`" | 50, `n = 18` to `95` | as above | none |
| SYNOPSIS.md:3776 | "36 proved, 64 open" | 38 / 62 | proved `n ≤ 100`: 1–10, 13–16, 21–25, 32–36, 45–49, 62–64, 79–81, 98–100 | none |
| frontier/README.md:134 | "60 proved and 264 open" | 62 / 262 | case `status` counts | none |
| frontier/README.md:385 | "264 … **239**" | 262 / **238** | open cases whose `verified_lower_bound.evidence` is `E-nagamochi-lower` | **`devtools.check_nagamochi_bounds`** (`_README_COUNT`, check_nagamochi_bounds.py:53) — fails now ("README.md says 239 of 264 … the case records say 238 of 262") |
| frontier/README.md:386 | "Seven others" | six | 11, 12, 17, 18, 19, 20 | none |
| frontier/README.md:390 | "18 more external-certificate cases" | 18 (values wrong, see 3.4 item 4) | 26–31, 39–41, 52, 53, 55, 56, 68–72 | none |
| frontier/README.md:395 | "39" (Nagamochi, `n ≤ 100`) | 38 | open `n ≤ 100` on `E-nagamochi-lower` | none |
| frontier/README.md:399 | "264 … 119" (grid) | 262 / 117 | `construction_method: trivial-grid` among open | none |
| frontier/README.md:424 | "one solved member above `k = 3`" | three | 21, 32, 45 | none |
| FIGURE-PLAYBOOK.md:92–93 | "65 lines"; "26 cases …" | 62; 27 cases incl. 45 | composite `lower.shown` for `n ≤ 100` | `test_known_best_atlas` checks drawn lines against the composite, not this prose |
| check_nagamochi_bounds.py:5–6 (docstring), results.yaml:203–204 (T-007) | "95 … 64 … other 31" | 95 / **63** / **32** | operative `n ≤ 100` any status on `E-nagamochi-lower` | **`check_nagamochi_bounds`** — fails now on six phrases (run here); evidence.yaml:1024 is already updated |
| explainer caption | {{N_STARRED}} / {{N_PROVED_HERE}} | 27 / 3 on rebuild | composite totals | `test_bound_citations.py::test_the_recent_lower_bounds_are_exactly_the_starred_cases` (fails now until the composite is rebuilt) |

Other stale text found in passing, outside the listed documents:

- packing/frontier/n-020.md:156–158 — "Since 2026-09-23 the companion `n = 21` carries the
  stronger T-034 certificate at `122/25`…" (now `s(21) = 5`).
- packing/tests/test_audit_ds7_lower_bounds.py:89 pins `(17, "466001/100000", …,
  "4.66001")`, and packing/tests/test_rung_figures.py:700 pins "4.66001, after v1.1.0, R052,
  R012 (T-032)…"; both need the R068 values when n-017 lands.
- bibliography.yaml `credit` gaps that misstate lineage under the "after Levy" encoding:
  `[Kleddamag n17 certified bound]` (v1.0.0) has no credit though its ATTRIBUTION
  credits Levy, Mira and Guzhou0806 → "Kleddamag after Levy, Mira, Guzhou0806";
  `[Guzhou0806 n17 R052]` has none → "Guzhou0806 after Kleddamag, Levy";
  `[n17 weighted certificates 2026-09-20]` has none → "Guzhou0806, Mira after Levy";
  `[Guzhou0806 n17 R068]`/`[R067]` "Guzhou0806 after Kleddamag" omits Levy although the
  owner describes the line as building on this project's threshold lineage →
  "Guzhou0806 after Kleddamag, Levy" (45 characters with year and venue, under the 66
  limit). With R068 the `n = 17` citation line on the atlas and film will otherwise read
  "Guzhou0806 after Kleddamag 2026, GitHub" and no longer name this project.
  `[Tokoharu density 2026]` "Tokoharu after Levy, wand125": his README names wand125's
  repository as the work it builds on and credits this project second-hand; owner to
  decide whether "Tokoharu after wand125, Levy" reads truer.
- results.yaml T-017 (`apparently-novel`, claim "the first lower bound specific to
  `n = 12` in the retained corpus") — the retained corpus now holds Daniel's earlier
  `15680/3951`; owner to decide on re-scoring or an annotation ("found independently of
  …").

## 4. Proposed structure for README's results presentation

**Order.** (1) *New Results* stays this project's own (T-NNN), with the cross-reference
fixes of 3.1. (2) A new section, **Recent Results, All Sources**, opens with one sentence
of totals (55 cases, 27 verified, 3 new exact values, 3 this project's in the verified
lane) and a generated table. (3) *Results by Others* becomes the per-source paragraphs,
grouped by lineage: "Building on this project" (Kleddamag; Guzhou0806; Mira; wand125;
Tokoharu, credited through wand125) and "Independent of this project" (Evan Daniel;
wand125's point-only routes on his supports), then "Earlier in 2026" (the seven
pre-22-August bounds of §1c). Keep the `#results-by-others` anchor or update the links at
README.md:20, :91, :165, :521, SYNOPSIS.md:128, TUTORIAL.md:92.

**Table columns.** `n` · lower bound (exact = decimal; `=` when it closes the case) ·
lane (verified `V4/C…` or reported) · holder, as the bibliography credit prints it ·
lineage (A, B, B′, C) · source date · earlier recent bounds (count, linked to the case
record's history) · case record link. One row per case, 55 rows for `n ≤ 100`; where
the verified lane differs (18, 19, 20, 26, 29, 30, 31, 39–41, 52, 53, 55, 56, 68–72) the
row shows both, as §1a does.

**Can an existing renderer produce it?** Partly.
`devtools.build_bound_citations` already derives, per `n`, the *verified* lower bound's
credit line (`Source.credited`), `recent` (`is_recent`, `RECENT_SINCE`) and
`basis: project | external` (`lower_citation`, build_bound_citations.py:474–509), from
typed fields only. `devtools.render_research_tables` already splices generated
Markdown blocks between `BEGIN/END GENERATED` markers and `--check`s them cell by cell
(`splice`, `extract`, `cells`, render_research_tables.py:324–345). Neither covers the
reported lane, lineage or history. A new generator, `devtools.render_recent_results`,
reusing both, is the smaller change: read each case's `reported_lower_bound` and
`verified_lower_bound`, resolve both source keys through `load_register`, and splice a
`recent-results` block into README.md. It needs three typed inputs the record lacks:

1. **Lineage as data, not prose.** Add `lineage: project | builds-on-project |
   credits-project | independent` (or `builds_on: [..]`) to each bibliography entry;
   the `credit` string cannot be parsed (the module's own rule, "Nothing is read from
   prose", build_bound_citations.py:50–55). A test should hold `credit` and `lineage`
   consistent ("after Levy" iff `builds-on-project`), which would have caught the four
   credit gaps above.
2. **Rung.** Either a typed `rung` on `verified_lower_bound`, or a stated rule computed
   from the verified evidence entries (V4 when each is `exact-algebraic` or
   `interval-certified` with `replay_status: passed`; C4 when two entries of distinct
   `method` include an `independent-implementation`; else C3). The rule reproduces every
   rung in §1a (11 and 12 at C4 by the native parent-core entries; all others C3).
3. **History.** Lower-bound evidence entries carry no value field, so "earlier recent
   bounds" is only in prose and audit tables. Add `value`/`exact_form` to lower-bound
   evidence entries (or a `lower_bound_history` list on the case) if the table should
   carry history; otherwise keep history in the per-source paragraphs and case records.

**Checks to guard it.** The generator's `--check` in the edit tier (cell comparison, as
`render_research_tables` does); a README count check in `check_readme.py` in the shape of
`check_nagamochi_bounds`'s `_README_COUNT` regex, holding "Fifty-five … twenty-seven …
three" to the record (no gate holds today's "Twenty-six"); a test that every
lower-bound `source_key` dated on or after `RECENT_SINCE` appears in the table; and the
existing `test_the_recent_lower_bounds_are_exactly_the_starred_cases`, which ties the
verified-lane subset to the atlas star.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
