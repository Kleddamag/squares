# Mathematical Review: Wang–Li `s(11) > 3875000000/999999999` (issue #247)

Reviewed 2026-09-30 from the Zenodo record 23038546 archive, downloaded to a scratch
directory outside the repository, read-only, by an independent adversarial review lane.
It is evidence for the coordinator, not a verdict of record: no register row was written
and no bound was moved by writing it.
The separate retention and replay lane’s directory and receipts were not consulted, so
the numbers below rest on this lane’s own downloads and code.

**In one line:** the bound is Kleddamag’s reviewed `s(11) > 31/8` parent-core
certificate (T-037) with thirteen threshold-orbit weights raised and the parent and
every core shrunk by the same rational factor `λ = 1 − 10⁻⁹`; no mathematical defect was
found, every hypothesis of the counting and transfer theorem was re-derived here for the
new parameters with exact arithmetic by code sharing nothing with the release or with
Kleddamag, 651 of the 12,028 rows, the shrink-sensitive and the historically weakest
rows first, were re-decided here by that code and every one returns exactly
`1000047559`, and the claimed constants are all exact.
The improvement, `31/7999999992 ≈ 3.9 × 10⁻⁹`, is real and is the smallest step the
public `s(11)` ladder has taken; the release itself calls it a proof-of-slack result,
and the register should describe it in those terms.

## 1. What Was Reviewed

| Field | Value |
| --- | --- |
| Source | Zenodo record 23038546, DOI `10.5281/zenodo.23038546`, published 2026-09-29 |
| Creators | Wang Ke and Li Can, Fudan University (no ORCIDs) |
| Issue | jlevy/squares #247, opened 2026-09-29T13:38Z by GitHub user `XiaoLiaoShe`, signed Ke Wang and Can Li |
| Claim | `s(11) > 3875000000/999999999 = 3.875000003875000003875…`, strict |
| Container, parent | `L = 191/50`, `A′ = 190999999809/193750000000 = λ · 764/775`, `L/A′ = 3875000000/999999999` |
| Archive | `n11_wang_li_zenodo_release_2026-09-29_stage10_doi_23038546-1.zip`, 2,495,053 bytes, MD5 `52c82aee798ab94d3733c749eecd70de` (matches Zenodo), SHA-256 `80381e22ab3535cdd113fb35f3a475b1071593af5d809ab65684af46ad98e648` |
| Source certificate | `certificate/global-certificate-original.json`, SHA-256 `57e9927da5c13f42dd8bcbf8f08c84363635fece626657ee63a810c61cd44458`, byte-identical to the repository’s retained Kleddamag v1.0.2 certificate |
| Improved certificate | `certificate/improved-global-certificate.json`, 3,513,169 bytes, SHA-256 `31e10ceb8368cc858e61f45ce7cfee783e8d0c7910893559164810f45439cc34` |

All 39 entries of the archive’s `SHA256SUMS` verify.
Files read line by line: the preprint (`paper/n11_lower_bound_wang_li.tex`; the PDF and
DOCX were text-extracted and compared), `README.md`, `AUTHORS.md`,
`SOURCE_ATTRIBUTION.md`, `THIRD_PARTY_NOTICES.md`, `LICENSE_STATUS.md`, `AUDIT_LOG.md`,
`EXTERNAL_REVIEW_REQUEST.md`, `ZENODO_METADATA.md`, `CITATION.cff`, `MANIFEST.json`,
`verify.py`, the three files under `verifier/independent/`, the three Python files under
`verifier/primary_kleddamag/`, and all nine receipts under `evidence/`. First-party
context: Kleddamag’s retained `PROOF.md` and `VERIFICATION.md`,
[review-2026-09-22-kleddamag-n11-mathematics.md](review-2026-09-22-kleddamag-n11-mathematics.md),
[review-2026-09-22-native-n11-parent-core.md](review-2026-09-22-native-n11-parent-core.md),
`packing/devtools/verify_kleddamag_n11_native.py`, register entry T-037, the
`[Kleddamag n11 2026]` bibliography entry, `packing/frontier/n-011.md`, and
[epistemics.md](../../../epistemics.md).

Scratch instruments written for this review ran outside the repository: `wl_verify.py`
(exact structure, premise and per-row sweep checker, written from the theorem statement,
importing nothing from either release), `run_sample.py` (the sample driver and its
`sample_results.jsonl`), and `containment_quadratic.py` (strict containment by exact
quadratic minimisation, bypassing the endpoint-extremum lemma).
They are not retained here; retention belongs to the intake packet.

## 2. Verdict

**No mathematical defect found.** The reduction is unchanged from the reviewed T-037
argument, every hypothesis holds for the new parameters, and the finite computation is
reproduced exactly on 651 of the 12,028 rows by an implementation sharing no code with
the release, cell count for cell count against the release’s own fresh receipt.
Nothing in the argument is tied to the old numbers.

- **Blocking:** none.
- **Should-fix:** four, in §8: the release’s “independent” verifier never reads the
  frozen improved certificate and passes by equality to hard-coded constants rather than
  by the theorem’s inequality; the archive says nothing about AI assistance while two
  receipts use agent-session vocabulary; the Zenodo licence field and the standalone PDF
  disagree with the archive; and the register description should state the size of the
  step.
- **Rung the repository can state on its own evidence:** `V4/C1` on this review alone;
  `C3` once the replay lane’s complete run of the source sweeps passes on the pinned
  bytes; `C4` only after the native parent-core interval decision
  (`devtools.verify_kleddamag_n11_native`, which is bound to T-037’s certificate hash
  and needs a parameter for the new one) accepts all 12,028 rows.

## 3. The Theorem

**Statement.** Let `L`, `A` be positive rationals.
A *parent* is a closed side-`A` square in `[0, L]²` at any orientation; parents may
touch, their interiors are disjoint.
The certificate supplies a finite D4-invariant set of sites in `[0, L]²` (679 orbits,
5,284 distinct sites), nonnegative integer weights on ordinary sites (66 positive
orbits, 496 sites) and on `k`-of-`m` threshold features (132 two-of-three orbits, 10
two-of-five, 142 three-of-five; 2,220 features in all), and a catalogue of 12,028 rows
`(a, b, t, B)`: for every parent whose folded half-tangent `u` lies in `[a, b]` it
assigns the concentric closed core of side `B` at half-tangent `t`. The charge of a core
`Q` is the weighted count of ordinary sites it holds plus the weight of every threshold
feature of which it holds at least `k` of the `m` sites.

*Budget.* Across pairwise disjoint closed cores an ordinary site pays at most `w` and a
`k`-of-`m` feature at most `⌊m/k⌋ w`, because `q` firing cores hold `q` disjoint
captured subsets of at least `k` sites each, so `qk ≤ m`; the inequalities add even when
features share sites.
Hence `Σ C(Qᵢ) ≤ M` for any disjoint family.
*Transport.* If `B(cos δ + |sin δ|) < A` for every `u ∈ [a, b]`, with
`δ = 2 arctan u − 2 arctan t`, the core lies strictly inside every parent of the row;
and if `C(Q) ≥ Γ` for every legal centre of every row, then eleven parents with disjoint
interiors have eleven pairwise disjoint cores with total charge `≥ 11Γ`.
*Contradiction.* `11Γ > M` excludes eleven parents of side `A` in side `L`, hence eleven
unit squares in side `L/A`. *Strictness.* Feasible packings with container side at most
4 form a compact set on which containment and interior-disjointness are closed
conditions, so the infimum is attained, and exclusion at `L/A` gives `s(11) > L/A`.
*Folding.* The eight symmetries of the container preserve the weighted charge system
(every point orbit is a full D4 orbit, every threshold orbit is a complete set of 4 or 8
images with one weight), so each parent’s orientation is folded into `[0, π/4]`
separately, with no symmetry imposed on the packing.

**Each hypothesis for the new parameters**, all re-derived here with `Fraction`
arithmetic on the frozen improved certificate:

| Hypothesis | How checked here | Result |
| --- | --- | --- |
| Charge system nonnegative | every point weight and orbit weight read as `int ≥ 0` | holds; the thirteen changes are `+1` to `+34344` |
| D4 invariance | orbit of `sets[0]` under the 8 symmetries equals the listed sets, one weight per orbit; point orbits expanded and deduplicated, no site repeated | holds for all 284 charge orbits and 679 point orbits (identical to the source) |
| Sites distinct within a feature, indices in range | asserted per feature | holds |
| Catalogue contiguous from 0, past `tan(π/8)` | `a₀ = 0`, each `a` equals the previous `b`, last `b = 207107/500000` with `b² + 2b − 1 = 309449/250000000000 > 0` | holds (unchanged) |
| Relative angle in `[−π/4, π/4]` | `dot > 0` and `dot ≥ |cross|` at both endpoints, `2 arctan` monotone | holds (depends on `a, b, t` only) |
| Core strictly inside every parent | `A′ − B′·max endpoint width > 0` for all rows; **and independently** by maximising the two exact quadratics `q(u) < 0` on `[a, t]` and `[t, b]`, vertices included, which does not use the endpoint-extremum lemma | holds; minimum endpoint margin `999999999/10²¹ = λ · 10⁻¹²` at row 0; all 12,028 rows also pass the quadratic form, whose supremum of `(1+u²)(BW − A)` is `−999999999/10²¹`, at row 0 |
| Centre envelope `[r, L−r]²` with `r = A′ min(f(a), f(b))/2` | `f(u) = (1+2u−u²)/(1+u²)` has its only stationary point at `u = √2 − 1`, a maximum, so the interval minimum is at an endpoint; sign of `1 − 2u − u²` checked per row | holds for all rows; `H = L/2 − r > 0` everywhere |
| Parent-envelope sanity `B′(c_t + s_t)/2 ≤ r < L/2` | per row | 0 violations in 12,028 |
| `0 < B′ < A′ < L` | per row | holds |
| Accumulation exact | `Σ ordinary weights + Σ |signed rectangle coefficients| < 2⁵⁰` per row | holds on every swept row |
| `11Γ > M` | `11 × 1000047559 − 11000095024 = 428125 > 0` | holds |

**Why scaling parent and cores together is legitimate.** The container and the sites are
untouched; only the two lengths `A` and `B_r` are multiplied by `λ > 0`. The containment
inequality `B W < A` is homogeneous of degree one in `(A, B)`, so it is preserved with
the same relative margin; the folding, the angle range and the catalogue depend only on
`(a, b, t)`. What is not preserved is coverage: a smaller core captures a subset of the
sites the old core captured at the same centre, so each threshold indicator and hence
the charge at every fixed centre is nonincreasing in `B`, and a smaller parent has a
larger legal-centre domain `[r′, L − r′]² ⊇ [r, L − r]²`, so the row minimum is taken
over a superset. Both effects push `Γ` down, never up, which is why the release replays
every row rather than arguing by continuity, and it is right to do so.
The bound `L/A′ = (31/8)/λ` follows exactly as before.

**Why the reweighting is needed first.** In the source certificate the eleven-bin
histogram has its minimum `999962528` on row 11962, only `9,805.8` units above
`M/11 = 999952722.18…`; a shrink that lowered that one row by ten thousand units would
break the counting inequality.
The thirteen increments raise every one of the 12,028 rows (11,981 rows sat at
`1000047518`, now `1000047559`; row 11962 rises by `85,031`) onto a flat plateau at
`1000047559`, while the budget rises by only `615,080`, so the surplus grows from
`107,864` to `428,125` and the slack on every row from `9,805.8` to
`428125/11 = 38,920.5` units.
The shrink by `10⁻⁹` then changes no row minimum at all: the release’s histogram is
still `{1000047559: 12028}`, the 651 rows swept here agree, and the first row to fall,
615, falls only at `λ = 1 − 10⁻⁸` (the ladder in §4).

**Nothing in `PROOF.md` is tied to the old numbers.** The argument is stated for
arbitrary positive rationals `L`, `A`; the tables of `764/775`, the budgets and the
`10⁻¹²` margin are the instantiation, not premises.
The endpoint-extremum lemma (`cos δ + |sin δ|` increases with `|δ|` on `[−π/4, π/4]`)
and the envelope lemma are independent of `A` and `B`. The only hard-coded number on the
verifier path is `L = 191/50` (twice in `exact_mixed.py`), which is unchanged; `A` and
each `B_r` are read from the certificate and rechecked.
The `2⁵⁰` accumulation guard is rechecked with the new weights.

## 4. The Certificate

**Exact diff against Kleddamag’s `global-certificate.json`** (my own field-by-field
comparison):

| Field | Source | Improved |
| --- | --- | --- |
| `A` | `764/775` | `190999999809/193750000000` (`= λ · 764/775` exactly) |
| `minimum_units` | `999962528` | `1000047559` |
| `budget_units` | `10999479944` | `11000095024` |
| `bound` | `31/8` | `3875000000/999999999` |
| `point_orbits` (679) | — | identical |
| `charge_orbits` sets and thresholds (284) | — | identical; 13 weights changed, listed below |
| `entries` `(a, b, t)` (12,028) | — | identical |
| `entries` `B` (12,028) | — | every one exactly `λ · B` |
| `L`, denominators | — | identical |

The file has no duplicate JSON keys and no floating-point literal.

| Orbit | Family | Features | Weight | Increment | Budget delta |
| ---: | --- | ---: | ---: | ---: | ---: |
| 3 | 2-of-3 | 8 | 863818 → 863819 | +1 | 8 |
| 27 | 2-of-3 | 8 | 370820 → 370824 | +4 | 32 |
| 43 | 2-of-3 | 8 | 9293472 → 9293475 | +3 | 24 |
| 51 | 3-of-5 | 8 | 1924284 → 1928668 | +4384 | 35072 |
| 52 | 2-of-5 | 8 | 5679789 → 5679796 | +7 | 112 |
| 130 | 2-of-5 | 8 | 14211519 → 14245863 | +34344 | 549504 |
| 131 | 2-of-5 | 8 | 4083535 → 4083536 | +1 | 16 |
| 174 | 3-of-5 | 8 | 878087 → 881863 | +3776 | 30208 |
| 206 | 2-of-3 | 4 | 19257662 → 19257667 | +5 | 20 |
| 207 | 2-of-3 | 8 | 58655 → 58656 | +1 | 8 |
| 218 | 3-of-5 | 4 | 9486754 → 9486761 | +7 | 28 |
| 232 | 2-of-3 | 8 | 15651 → 15656 | +5 | 40 |
| 259 | 2-of-3 | 8 | 153071 → 153072 | +1 | 8 |
|  |  |  |  |  | **615080** |

**Exact recomputation** (own code, `Fraction` and `int`):

| Quantity | Value |
| --- | --- |
| Budget by family, improved | points `2247714156` (66 orbits, 496 sites); 2-of-3 `3188007732` (1,020 features); 2-of-5 `990221920` (76 features, capacity 2); 3-of-5 `4574151216` (1,124 features) |
| `M` | `11000095024`, equal to the declared value; source `10999479944` likewise |
| `11 Γ` | `11000523149` |
| `11 Γ − M` | `428125` |
| `M/11` | `1000008638 + 6/11`, so each row has `38920 + 5/11` units of slack |
| `L/A′` | `3875000000/999999999`, and `(31/8)/λ` gives the same fraction |
| `L/A′ − 31/8` | `31/7999999992 = 3.875000003875…× 10⁻⁹` |
| Decimal | `3.875000003875000003875000003875…` (period `003875`) |
| Increments | `Γ + 85031`, `M + 615080`, surplus `+ 320261`, as the preprint’s table states |

**Independent row re-decision.** `wl_verify.py` expands the orbits, builds the signed
capture-rectangle expansion of each `k`-of-`m` indicator, sweeps the rotated
centre-domain polygon slab by slab with exact rational edge values, accumulates in a
plain NumPy `int64` array by direct range addition (no segment tree), and takes the
minimum over the legal cells of each slab.
It then evaluates the charge at an interior point of the arg-min cell by a direct count
of captured sites per feature, with no signed expansion, and requires equality; on three
further random legal cells per row it requires the direct count to equal the signed sum.
Rows chosen worst-first: the two bands the preprint names as the first to fail under a
larger shrink (all of 543–574 and 615–626), the nine rows that were lowest or extreme in
the source histogram (0, 1, 3985, 6014, 8844, 9281, 9740, 11962, 12027), and every
twentieth row across the catalogue.

| Selection | Rows | Minimum | Matches fresh receipt (minimum, slabs, cells) |
| --- | ---: | --- | --- |
| Band 543–574, first to fail under a larger shrink | 32 | all `1000047559` | 32 of 32 |
| Band 615–626 | 12 | all `1000047559` | 12 of 12 |
| Source-histogram extremes 0, 1, 3985, 6014, 8844, 9281, 9740, 11962, 12027 | 9 | all `1000047559` | 9 of 9 |
| Every twentieth row, 0 to 12020 | 602 | all `1000047559` | 602 of 602 |
| **Distinct total** | **651** | histogram `{1000047559: 651}` | 651 of 651 |

That is 4,649,917 slabs and 27,639,745,555 represented cells in 637 s, 0.98 s per row on
a loaded machine. The arg-min cell’s direct count equalled the sweep on every row, the
direct count equalled the signed sum on all 1,835 random cells, and the smallest random
cell charge seen was itself `1000047559`.

The same code run on the **source** certificate returns the source’s nonuniform values
(row 0: `1000047518`; 3985: `1000019046`; 8844: `999970079`; 11962: `999962528`; 12027:
`1000047518`, as the 2026-09-22 review’s table and the source receipts give them), so it
is not a checker that returns a plateau regardless of input.

**Sensitivity of the shrink.** On a reconstruction of the reweighted certificate at the
source geometry (`A = 764/775`, source `B_r`, improved weights; equal to the frozen file
after scaling, as checked above), the same code was run at several `λ` on the named
sensitive rows and on control rows:

| `1 − λ` | bound `(31/8)/λ` | row 0 | 543 | 560 | 574 | 600 | 615 | 620 | 626 | 11962 | counting on these rows |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `0` | `3.8750000000` | `1000047559` | `1000047559` | `1000047559` | `1000047559` | `1000047559` | `1000047559` | `1000047559` | `1000047559` | `1000047559` | passes |
| `10⁻⁹` | `3.8750000039` | `1000047559` | `1000047559` | `1000047559` | `1000047559` | `1000047559` | `1000047559` | `1000047559` | `1000047559` | `1000047559` | passes |
| `10⁻⁸` | `3.8750000388` | `1000047559` | `1000047559` | `1000047559` | `1000047559` | `1000047559` | `998920060` | `1000047559` | `1000047559` | `1000047559` | fails on 615 |
| `5 × 10⁻⁸` | `3.8750001938` | `1000047559` | `1000047559` | `1000047559` | `1000047559` | `1000047559` | `998920060` | `998920060` | `998920060` | `1000047559` | fails on 615, 620, 626 |
| `10⁻⁷` | `3.8750003875` | `1000047559` | `1000047559` | `1000047559` | `1000047559` | `1000047559` | `996661034` | `996661034` | `996661034` | `1000047559` | fails on 615, 620, 626 |
| `2 × 10⁻⁷` | `3.8750007750` | `1000047559` | `998920060` | `998920060` | `998920060` | `1000047559` | `996661034` | `996661034` | `996661034` | `1000047559` | fails on 543, 560, 574, 615, 620, 626 |

The threshold is `M/11 = 1000008638.54…`. `λ = 1` and `1 − 10⁻⁹` leave every one of
these rows on the plateau.
At `1 − 10⁻⁸` row 615 drops by `1,127,499` units to `998920060` and the counting
inequality fails; rows 620 and 626 follow at `1 − 5 × 10⁻⁸`, and rows 543, 560 and 574
at `1 − 2 × 10⁻⁷`, which is exactly the preprint’s sentence.
Rows 0, 600 and 11962 are unmoved throughout.
The drops are cliffs rather than drifts — a whole feature leaving the shrunken core —
which is why no continuity argument could have replaced the replay, and why the release
was right to replay every row.

## 5. The Verifiers

**Primary.** `verifier/primary_kleddamag/exact_mixed.py` is byte-identical to
Kleddamag’s retained v1.0.2 file; `integer_sweep.py` differs only by two blank lines and
`replay_parallel.py` by a docstring line and three blank lines.
So the primary replay is Kleddamag’s checker run on the new certificate, and it does
check the theorem’s hypotheses for the new parameters: `validate` reads `A` and every
`B_r` from the file, tests the angle range, strict containment, the envelope, catalogue
contiguity and the `b² + 2b > 1` gap, D4 completeness of every orbit, the `2⁵⁰` guard,
the recomputed budget against the declared one, and `11 · minimum_units > budget_units`
as an inequality; each row then has to reach the certificate’s declared minimum.
It hard-codes only `L = 191/50`. Its decisions are on Python integers and `Fraction`s;
the Numba sweep is `int64` under the checked guard.
This is the reviewed T-037 code path.

**“Independent”.** `independent_core.py` / `independent_scaled_fast.py` /
`run_independent_full.py` is a re-implementation of the same method: rectangle expansion
of the same signed identity, the same integerisation
(`scale = lcm(2D, den(B/2), den(H))`, the same rotated polygon, the same floor/ceiling
bisection), and a range-minimum sweep — a lazy segment tree in pure Python in the audit
module and a Numba block decomposition in the fast module.
Its decisions are on integers and `Fraction`s; no float is on the decision path
(`bound_decimal` occurs only in a receipt).
It shares no source lines with `exact_mixed.py`, but its structure and names follow it
closely, so it is implementation diversity within one method, as Kleddamag’s Python and
JavaScript scanners were, not a different decision procedure.

Four things it assumes rather than checks:

1. **It never reads `improved-global-certificate.json`.** It loads the *source*
   certificate, applies the `weight_deltas` of
   `evidence/reweighted_fullscan_receipt.json`, and multiplies `A` and every `B_r` by a
   hard-coded `λ` in memory.
   `run_independent_full.py` records the improved file’s SHA but does not open it.
   The frozen file is tied to that reconstruction only by `verify.py`’s `integrity()`,
   which compares the two certificates against its own hard-coded `DELTAS` dictionary,
   and never compares the receipt’s `weight_deltas` to either.
   The three copies of the deltas (receipt, `verify.py`, README) do agree with the file
   diff, so nothing is wrong today, but the chain of custody runs through constants
   rather than through the artefact.
2. **Its PASS criterion is equality to a constant, not the theorem’s inequality.**
   `PASS_INDEPENDENT_FULL_REPLAY` requires every row minimum to equal the hard-coded
   `TARGET = 1000047559`; it reports `11·min − budget` but does not test its sign.
   `verify.py --mode full` likewise asserts the two replays’ histograms, minima, budgets
   and surpluses equal each other and the expected constants.
3. **It skips the hypotheses `validate` checks.** It does assert strict containment per
   row and recompute the budget from the orbits, but it does not check D4 completeness
   of the charge orbits, the angle range, catalogue contiguity or the gap, the envelope,
   or the accumulation guard.
   In this release those are checked only by the pinned Kleddamag code.
4. **Its self-test constants come from Kleddamag’s evidence.** `independent_core.main`
   asserts seven source row minima (`0: 1000047518`, `11962: 999962528`, …) taken from
   the source’s receipts; this audit entry point is not invoked by `verify.py`.

Neither verifier uses a trusted precomputed table for the decision; both recompute every
rectangle and cell. `verify.py --mode quick` runs row 0 through both and is a smoke test
only.

**Receipts.** The primary evidence with per-row data is the four fresh quarter receipts
(rows 0–3006, 3007–6013, 6014–9020, 9021–12027, each `3007` rows, histogram
`{1000047559: 3007}`, merged into `primary_full_fresh_12028.json` with 86,299,918 slabs
and 511,649,696,956 cells).
The older `scaledA_full12028_receipt.json` is a merge of two staged runs ("rows 0–5999:
PASS (prior staged exact sweep receipt)") with no per-row data.
The independent receipt carries only aggregates (histogram, min, max, `bad_count = 0`,
659.6 s). My sweep reproduces the fresh receipt’s per-row minimum, slab count and cell
count exactly on every sampled row.

## 6. Claims and Credit

| Claim | Where | Evidence | Status |
| --- | --- | --- | --- |
| `s(11) > 3875000000/999999999 = 3.875000003875…` | issue, abstract, theorem | §3–§4 | supported |
| Improvement `31/7999999992` | issue, §1 | exact | correct |
| 12,028 rows, `bad_count = 0`, histogram `{1000047559: 12028}` | issue, README | fresh quarter receipts (per row) and independent receipt (aggregate); 651 rows re-decided here | consistent |
| Improved certificate SHA-256 `31e10ceb…` | issue, preprint, README | recomputed | correct |
| Surplus `428125` | everywhere | recomputed | correct |
| Source table `999962528 / 10999479944 / 107864` and deltas `+85031 / +615080 / +320261` | preprint §2 | Kleddamag `PROOF.md`, recomputed | correct |
| Thirteen orbits, increments and new weights | preprint §3, README | file diff | correct, and only those |
| Budget unchanged by scaling | preprint §5.1 | budget depends on weights and orbit sizes only | correct |
| Independent replay 659.6 s | preprint §5.2 | receipt `elapsed_seconds = 659.5959` | correct |
| `λ = 1 − 2 × 10⁻⁷` fails on rows 543–574 and 615–626 | preprint §7 | reproduced here at `1 − 2 × 10⁻⁷` on rows 543, 560, 574, 615, 620 and 626, with rows 0, 600 and 11962 unaffected; the ladder also shows row 615 already failing at `1 − 10⁻⁸` | correct; the first cliff is earlier than the sentence suggests |
| Source row 11962 has charge `999962528` | preprint §7 | 2026-09-22 review table; my source-control sweep | correct |
| Strict core margin `λ · 10⁻¹²` | receipts | recomputed | correct |
| “No stronger registered lower bound” on 2026-09-29 | abstract, §8 | `n-011.md` verified lane is `31/8`; the owner’s comment on #247 says stronger results are reported but unconfirmed | correct as dated |

**Provenance and credit.** The release is explicit and consistent.
`SOURCE_ATTRIBUTION.md` calls it “a derivative continuation of **Kleddamag**, *Eleven
unit squares: a certified lower bound* (September 2026)”, records Kleddamag’s statement
that the certificate “was developed from the Squares Project T-026 threshold
certificate” at revision `7ccb679cc0827d10ee80e2cd1988c8a07d65dfdc`, and says “Source
credit does not imply endorsement or coauthorship by Kleddamag, Joshua Levy, the Squares
Project contributors, or Walter Trump.”
`AUTHORS.md` claims authorship “only for the continuation represented here: the 13-orbit
reweighting, the exact common rational parent/core shrink, the derived certificate, and
the verification/release work”.
The preprint’s references are Kleddamag’s repository, “Joshua Levy and collaborators,
The Squares Project”, and Trump’s 1979 packing.
The Zenodo record relates to Kleddamag as `isDerivedFrom` and to jlevy/squares as
`references`. Under the credit rule in epistemics.md the line is therefore **Wang, Li
after Kleddamag, Levy** (the source names no further link), with lineage
`builds-on-project` through Kleddamag, whose own line is
`Kleddamag after Levy, Guzhou0806, Mira`.

**Licence of what they derived from.** Kleddamag’s code is MIT and its certificate data
carries the CC BY 4.0 obligations of this project’s T-026 data (Kleddamag’s
`LICENSING.md`). The archive preserves both: `verifier/primary_kleddamag/` keeps the
upstream MIT notice verbatim, `THIRD_PARTY_NOTICES.md` reproduces the attribution
“Joshua Levy, the squares project (https://github.com/jlevy/squares)”, and the adapted
certificate is “explicitly identified as modified”, as CC BY requires.
The release’s own material is CC BY 4.0 (paper, records) and MIT (its verifier code).
The Zenodo record itself lists only `cc-by-4.0` although `LICENSE_STATUS.md` asks for
both licences to be selected.

**AI assistance.** The archive makes no statement either way: the words “AI”,
“artificial intelligence”, “language model”, “assistant”, “agent” and the names of any
coding tools occur in no file of the release, and the preprint says only “computer-
assisted”.
Two receipts, however, are written in the vocabulary of an agent-tool session:
`scaledA_full12028_receipt.json` records `"rows_6000_12027": "PASS (completed this turn,
exact Fraction geometry; all row minima identical)"`, and the Q1 fresh-replay receipt
says “The process environment continued that same invocation beyond Q1 after a tool
timeout; this staged package intentionally retains only the Q1 subset.”
`ZENODO_METADATA.md` is written as instructions to a human uploader ("Add ORCID
identifiers only if the authors actually have and wish to use them; do not invent
identifiers"). The release also does not repeat the source’s own statement: Kleddamag’s
`AUTHORS.md` says an AI coding agent “developed the mathematical and computational
continuation” under Kleddamag’s direction, which the `[Kleddamag n11 2026]` bibliography
note records. Under epistemics.md the register says what the source says, so a Wang–Li
entry would carry no AI statement unless the authors make one; the owner’s reply on #247
is the place to ask.

## 7. Significance, Honestly

The step is `31/7999999992 ≈ 3.875 × 10⁻⁹`, against a remaining gap to Trump’s packing
of `0.0020836`: it closes `1.9 × 10⁻⁴` per cent of that gap.
The preprint says as much ("deliberately modest numerically", “a proof-of-slack
result”).

**It is a one-parameter family.** With the weights fixed, define `Γ(λ)` as the minimum
row charge after shrinking `A` and every `B_r` by `λ`. By the monotonicity argument in
§3, `Γ(λ)` is nondecreasing in `λ`, so the set of `λ` with `11 Γ(λ) > M` is an interval
`(λ*, 1]`, and every rational `λ` in it yields the strict bound `(31/8)/λ`. The
release’s two data points bracket `λ*`: `1 − 10⁻⁹` passes on all rows and, by the
preprint, `1 − 2 × 10⁻⁷` fails on rows 543–574 and 615–626, which the ladder in §4
reproduces on six of those rows.
The ladder also shows row 615 already failing at `1 − 10⁻⁸`, so
`λ* ∈ [1 − 10⁻⁸, 1 − 10⁻⁹)`. Every member of the family from these exact data therefore
lies in `(3.875, (31/8)/(1 − 10⁻⁸)] = (3.875, 3.8750000388]`: at most ten times the
present step. The chosen `λ` is not the best the data support, only the one with a tidy
decimal; the true `λ*` is computable exactly, since the row minima are piecewise
constant in `λ`, or by bisection with full replays at about ten minutes each.
Going beyond `3.87500004` needs new weights or new geometry, which is a new certificate
of Kleddamag’s kind, not another turn of this step.
The authors say as much in §9 of the preprint.

**Recommendation for the register.** Enter it as the authors’ result under its own
`T-NNN` with attribution `[Wang Li n11 2026]`, `published: 2026-09-29`, headline
`` `s(11) > 3875000000/999999999 = 3.875000003875…` ``, a claim that states the step
`31/7999999992` and that it is T-037’s certificate reweighted on 13 orbits and shrunk by
`λ = 1 − 10⁻⁹`, and significance **S2** by the T-042 precedent ("a citable intermediate
that changes no standing bound" was scored S2 for a `+0.00017` step superseded on its
day). T-037’s S5 rationale, 96 per cent of the gap closed, does not transfer to a
`3.9 × 10⁻⁹` step. If the stronger reported results the owner mentions on #247 are
confirmed first, this entry is exactly T-042’s situation.
README prose should give the exact rational and its distance from `31/8` in the same
sentence, so no reader takes “improved bound” to mean substantive movement; the case
record’s verified lane may move to it once the replay lane’s complete run and this
review are on file, with T-037’s evidence retained as history.

## 8. Findings

### Blocking

None.

### Should-fix

1. **Bind the independent replay to the artefact (authors).** Make
   `independent_scaled_fast.py` read `improved-global-certificate.json`, check the
   hypotheses `exact_mixed.validate` checks, and pass on `11 · min > budget` rather than
   on `min == 1000047559`; have `verify.py` compare the receipt’s `weight_deltas` to the
   file diff. Today every link is a hard-coded constant that happens to agree (§5).
2. **State AI assistance one way or the other (authors, via the issue reply).** The
   receipts’ “completed this turn” and “after a tool timeout” read as an agent harness;
   the policy records the source’s own words, and there are none (§6).
3. **Describe the step honestly in the register (record).** S2, headline with the exact
   rational, claim with the `31/7999999992` step and the λ construction; the T-037 S5
   rationale does not carry over (§7).
4. **Reconcile the Zenodo record with the archive (authors).** The record’s licence
   field lists only CC-BY-4.0 where `LICENSE_STATUS.md` asks for CC-BY-4.0 and MIT, and
   the standalone `n11_lower_bound_wang_li.pdf` on Zenodo (294,739 bytes, SHA-256
   `647dbb77…`) is not the archived, hash-listed PDF (254,473 bytes, SHA-256
   `dee13bfe…`); their extracted text and pdfTeX metadata are identical, so this is a
   packaging difference, not a content one.

### Nits

- The DOCX reference [2] carries a sentence absent from the LaTeX and PDF ("At access
  time the project lists 3.875 < s(11) ≤ 3.877083590022814… and identifies Kleddamag’s
  31/8 certificate as the strongest verified lower bound"); the three formats should say
  the same thing.
- `scaledA_full12028_receipt.json` merges two staged runs and has no per-row data; the
  fresh quarter receipts supersede it and the README could say so.
- The independent receipt has no per-row values, only the aggregate histogram.
- `requirements.txt` pins `numba == 0.65.1` but the README pins no interpreter; the
  pinned wheel may not install on the newest CPython.
- `verify.py --mode full` writes its output under the archive’s own `evidence/`
  directory.
- The issue was opened from a GitHub account (`XiaoLiaoShe`) that names neither author;
  the Zenodo creators and the preprint agree on Wang Ke and Li Can, Fudan University.
- `exact_mixed.py` hard-codes `L = 191/50` in `validate` and again in `geometry`; a
  future certificate with another container would silently need a code change.

## 9. Verified

| Item | Method | Result |
| --- | --- | --- |
| Archive integrity | `sha256sum -c SHA256SUMS`; zip MD5 against Zenodo | 39 of 39 OK; MD5 matches |
| Source certificate identity | `cmp` against the repository’s retained Kleddamag file | byte-identical, SHA-256 `57e9927d…` |
| Improved certificate identity and hygiene | SHA-256; `object_pairs_hook` duplicate-key and float-literal refusal | `31e10ceb…`; clean |
| Field-by-field diff | own code | exactly the fields in §4 |
| `A′ = λA`, `B′_r = λB_r` for all rows | `Fraction` | 12,028 of 12,028 |
| Budget, surplus, ratio, improvement | `Fraction`/`int`, own orbit expansion | all equal to the claimed values |
| Budget delta of the 13 increments | per orbit | `615080` |
| D4 completeness, nonnegativity, distinct sites | own expansion of 679 point and 284 charge orbits | holds |
| Catalogue contiguity, gap, angle range, envelope, parent envelope | per row, `Fraction` | holds, 0 violations |
| Strict containment, endpoint form | per row | min margin `999999999/10²¹`, row 0 |
| Strict containment, quadratic form without the endpoint lemma | `containment_quadratic.py` | 12,028 of 12,028 strictly contained; supremum `−999999999/10²¹` at row 0; envelope endpoint-minimum valid on every row |
| Row minima on the improved certificate | own sweep, worst rows first | 651 rows, histogram `{1000047559: 651}`; 27,639,745,555 cells; 0.98 s per row |
| Arg-min cell cross-check | direct `k`-of-`m` count at an interior point, no signed expansion | equal on every sampled row |
| Random-cell cross-check | direct count equals signed sum | equal on every sampled cell |
| Per-row slab and cell counts | against the fresh primary quarter receipts | equal on every sampled row |
| Source-certificate controls | own sweep on the source file | 5 of 5 nonuniform source values reproduced |
| Shrink sensitivity | own sweep at `λ ∈ {1, 1−10⁻⁹, 1−10⁻⁸, 1−5·10⁻⁸, 1−10⁻⁷, 1−2·10⁻⁷}` | `1` and `1 − 10⁻⁹` pass on all nine rows; `1 − 10⁻⁸` fails on row 615 (`998920060`); `1 − 2 × 10⁻⁷` fails on all six named rows and passes on 0, 600, 11962 |
| Preprint formats | LaTeX read; PDF and DOCX text-extracted and compared | one sentence differs in the DOCX (§8) |
| AI-assistance statements | grep over every file of the archive | none; two agent-session phrases quoted in §6 |

## Disposition

- **Registered** on 2026-09-30 as T-058, at `V4/C4`, `S2`, credited “Wang, Li after
  Kleddamag, Levy” with `lineage: builds-on-project`, as this review recommends.

- **The replays in the intake packet** (`packing/resources/web/wang-li-n11-2026-09-29/`)
  completed and passed:
  - the authors’ full two-implementation mode;
  - Kleddamag’s adapted launcher;
  - this repository’s native interval coverage of all 12,028 rows.

  Every mutated control is refused.

- **The shrink cliff is tighter than this review’s ladder showed.** The packet’s `cliff`
  measurement finds `λ = 1 − 2·10⁻⁹` already failing at row 615, so the admissible
  factors lie in `(1 − 2·10⁻⁹, 1]`, and these data give at most about twice the present
  step.

- **Scaling alone suffices.** A full event-cell sweep of Kleddamag’s unreweighted
  certificate, scaled by `λ = 999999999/1000000000` (the packet’s
  `receipts/scale-only/`), passes with the same minimum 999,962,528 and surplus 107,864,
  so the bound does not need the reweighting.
  This review’s sampled rows could not show it.

- **The should-fix items addressed to the authors** (binding the independent replay to
  the frozen file, the licence field, the standalone PDF, an AI-assistance statement)
  are put to them on jlevy/squares#247.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
