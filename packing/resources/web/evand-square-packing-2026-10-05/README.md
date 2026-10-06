# Evan Daniel’s Exact Optima of the Register’s Packings, `square-packing` at 5 October 2026, Retrieved 2026-10-05

This packet records `s12/search/exact/` of
[evand/square-packing](https://github.com/evand/square-packing) at the commit that adds
it: an exact-contact solver, run on this register’s known-best witness at every count
`n = 1` to `324`, and the exact rational certificate of `s(n) ≤ S'` it writes for 321 of
them. At 48 counts `S'` lies below the side the register reported, by `3.5e-13` to
`5.0e-11`: the exact optimum of the same packing, Francisco Couzo’s at 46 counts and Joost
de Winter’s at `n = 126` and `211`, with the slack of its binary64 pose removed.
Evan Daniel asked for those 48 to be registered on
[jlevy/squares#375](https://github.com/jlevy/squares/issues/375). Its Frontier key is
**[evand exact optima 2026-10-05]**, the result is registered as T-098, and the import bead
is `think-t6ok`. At 77 more counts the certified side lies just above the printed one and
lowers the verified ceiling; the author asked for nothing from those, and the owner decided
to register them as T-101 (provisionally T-118 until merged, `think-70bh`;
[The 77 Ceiling Counts](#the-77-ceiling-counts)).

The certificate for `n = 17` is held by the owner for the `n = 17` work on other branches
(`think-x4v4`). It is not retained, not pinned by digest and not replayed here, and neither
are the solver’s `n = 17` input and test-set outputs; the commit pins the whole tree, them
among it.

## Source and Pin

| Field | Value |
| --- | --- |
| Revision | `13ee36e5807727d12a5da36b9b90a96bdba272bf`, committed 2026-10-05T20:54:59Z (“Exact-contact solver for unit-square packings, and exact certificates for every record in jlevy’s register”) |
| Follows | `7ff3b2113532889708a3baa4d56bc44294022e63`, retained in [`../evand-square-packing-2026-10-04/`](../evand-square-packing-2026-10-04/README.md); the one commit between, `ab2bf47`, adds a working note on the algebraic degree of `s(n)` and is a read in [`intake-watch.yaml`](../../../campaign/intake-watch.yaml) |
| Author | Evan Daniel; the commit is co-authored by Claude Opus 5.5 |
| Credit | The batch README says the packings are their finders’ (named in `results.md`), that the inputs are this register’s `witnesses/known-best/n-N.yaml` (“Register data: CC BY 4.0, Joshua Levy, the squares project”), and the issue that the method is David Ellsworth’s analytic minimisation, reimplemented as a high-precision KKT Newton solve with the rational certificate added |
| AI assistance | On #375 the author wrote that “the solver, verifiers and this batch were written with Claude (Anthropic) as a coding and research agent, directed and reviewed by me”; the batch README says both checkers “were written by the same author and agent as the solver” |
| Licence | MIT (`LICENSE` and `s12/LICENSE`, Evan Daniel), pinned here as identical to the earlier packet’s copies |
| Retrieved | 2026-10-05T22:08Z, a blobless clone, `main` at this commit then and at 22:22Z |
| Retained here | The 48 improving certificates `batch/certs/n-N.cert` (1.6 MB) and, from 6 October, the 77 that lower a verified ceiling (2.0 MB), both checkers `verify_cert.py` and `verify_cert2.py`, the solver `exactsolve.py` and its `geom.py`, the drivers `verify_all.sh` and `reproduce.sh`, `batch/results.md`, the source’s per-count report `batch/results.json` (stored compressed) and both READMEs |
| Pinned by digest only | The other 195 certificates, all 320 solver inputs, the solver’s seven-input test set and its outputs, the batch’s scripts that read the register and build its tables, and `candidates_all.json`: 555 files, 4.3 MB, listed with their reasons in [`acquisition/sources.json`](acquisition/sources.json) |
| Left out | `batch/certs/n-17.cert`, `batch/inputs/n-17.txt`, `inputs/site17.txt` and `results/site17.*`, held |

`python -m devtools.acquire_source evand-square-packing-2026-10-05 --checkout PATH` writes
the retained tree, the subtree manifest and the acquisition record from a checkout at the
pin, from [`acquisition/declaration.json`](acquisition/declaration.json); `--check`
re-derives them from the packet alone. `results.md`, `results.json` and
`s12/search/exact/README.md` are retained byte for byte and so keep their `n = 17` rows,
which nothing here reads.

## What the Source Claims

- **48 upper bounds.** For each count below, `s(n) ≤ S'`, `S'` the side of an exact
  rational certificate `n-N.cert`: `n` unit squares, each a rational centre `(x, y)` and a
  rational `t = tan(θ/2)`, so that `(c, s) = ((1 − t²)/(1 + t²), 2t/(1 + t²))` holds
  exactly, inside a box of rational side `S'`. The solver takes the register’s binary64
  pose to a nearby exact KKT point of minimizing the side, at 80 digits, scales it by
  `1 + 10⁻²⁰`, rounds the centres to `10⁻³⁵` and the rotations to rational tangents, and
  rounds the side up. Eleven of the 48 inputs are the witness after the source’s
  unpublished SLP squeeze, which matters only for reproducing the solve.
- **273 more certificates** at the counts that do not improve, each `1e-20` to `1e-14`
  above the printed side, offered as an independent exact replay of the existing upper
  bounds with nothing asked to be registered. `n = 105, 130` and `292` are not certified.
- **Numerical, not by interval proof:** 315 of the 321 exact points are KKT local minima,
  44 of the 48 among them, and `n = 177, 211, 263` and `272` of the 48 are certified bounds
  only. The source names an interval-Newton enclosure as the next step.

## Replayed Here

**Decided here, independently re-implemented.**
`devtools.evand_exact_certificates check` reads each certificate strictly (a header
`n S`, exactly `n` rows `x y t`, rational literals only; the source’s parser ignores rows
past `n`, this one refuses them) and converts it without rounding: `(c, s)` from `t` as
above, a rational centre-and-basis witness for `sqpack.witness.exact_verify`, and the
corners `(x + c a − s b, y + s a + c b)`, `a, b = ±1/2`, for
`devtools.check_rational_witness_independent`, which shares no geometry or verification
code with `sqpack`. Their common mode is that parse and the map from `t` to `(c, s)`.
Both accept all 48, with least wall clearance `5e-21` and least pair gap about `1e-20`
at every count, and every one of the 320 certificates the packet pins, read from a checkout at the
pin: 2,820 CPU seconds on two workers, 802 of them for the 48
([`receipts/first-party-check.json`](receipts/first-party-check.json)).
Neither decider imports or copies the source’s code; the converter’s author read the
source’s checkers first, to confirm the corner convention, as the module states.

**The source’s checkers, reproduced.** `source-replay` runs `verify_cert.py` and
`verify_cert2.py` as retained, under CPython 3.14.7, as separate processes, holding each
to its exit status and to a last line beginning `VALID`. Both accept all 320 certificates
(202 CPU seconds on two workers; 54 for the 48), and `verify_cert.py` reports a least wall
clearance of `5e-21` and a least pair separation of `1e-20` at each improving count
([`receipts/source-replay.json`](receipts/source-replay.json)).

**Against the register.** `compare` reads, at each improving count, the bounds the
record held before this import from the sources that held them: the latest certified
packet’s printed side and verified value (T-056, T-057 or T-092), or at `n = 126` the
Kingbird catalogue’s side and the grid ceiling `12`. Every `S'` lies below both, by
`3.5e-13` (`n = 211`) to `5.0e-11` (`n = 270`) under the printed side. Matched square for
square to the known-best witness by nearest centre, one to one at every count, the
largest centre displacement is at most `1.441e-3`, rounded up. Of the 1,543 squares that move by more than
`1e-8`, 358 are ones the source lists as carrying no force, which its solver moves to give
them clearance; the other 1,185, at 24 counts that include all eleven squeezed inputs,
move by at most `4.2e-5` (at `n = 263`, where the source reports 40 zero modes). Every
other square moves by at most `9.2e-9`
([`receipts/register-comparison.json`](receipts/register-comparison.json)). So each
certificate is the register’s packing, made exact, and not a new arrangement.

**Controls.** `controls` makes three altered copies of each of the 48 certificates and
puts each to all four checkers
([`receipts/negative-controls.json`](receipts/negative-controls.json)). One square of the
tightest pair is moved along the closing normal by the pair’s exact gap, `1e-20`, plus one
unit of the side’s denominator (`1e-30` to `8e-29`): refused by all four at every count.
The box is shrunk by its least top or right clearance, `5e-21`, plus that unit: refused by
all four. The box shrunk by the unit alone is accepted by all four, as it must be, since
every clearance is about `5e-21`: the certificate has that much room, and “one unit of
the rational” is not a tight control here. The run took 3,276 s of wall time on two
workers.

**The source’s own driver.** `verify_all.sh` reports a failure from its first leg only if
`verify_cert.py`’s last line fails `grep -q VALID`, which `INVALID` also matches. Run as
retained on the overlapped `n = 68` control, it prints `verify_cert2 FAIL` and exits 1, and
never `verify_cert FAIL`, although `verify_cert.py` printed `INVALID` and exited 1. The
batch’s `summarize.py`, which wrote the ✓✓ column of `results.md` and is pinned here by
digest only (4,926 bytes, sha256 `79c8ab9c…`, read from the checkout at the pin), has the
same test. Its line 32 reads, verbatim:

```python
    return ('VALID' in a.stdout.splitlines()[-1] if a.stdout else False, b.returncode == 0)
```

So the source’s claim that both checkers accept every certificate rests, for
`verify_cert.py`, on a test an `INVALID` verdict passes; run here and held to its exit
status, `verify_cert.py` does accept all 320.

**Open and closed.** The source’s checkers require every square strictly inside the open
box and every pair strictly apart; this repository’s two accept contact, which is still
sound for `s(n)`, closed squares with disjoint interiors in the closed box. A certificate
with an exact contact would pass here and fail there. None of these does: every clearance
is about `5e-21` and every gap about `1e-20`, and both pairs of checkers accept all 320.
The overlap controls move a square whose walls stay strictly clear (least clearance
`1.07e-20`), so each of their refusals is for the overlapping pair.

**A reproduction sample.** `reproduce` runs the source’s solver, `exactsolve.py` as
retained, on the pinned inputs of `n = 68, 102, 126, 211` and `270` (the smallest count, a
squeezed input, de Winter’s two packings, one a certified bound only, and the largest
gap), with one BLAS thread, under CPython 3.14.7, numpy 2.5.2 and scipy 1.17.1: 178 CPU
seconds in all on two workers ([`receipts/reproduction-sample.json`](receipts/reproduction-sample.json)).
None of the five regenerated certificates is byte for byte the retained one, which is the
test `reproduce.sh` applies. Each has exactly the retained side `S'`; its squares differ
from the retained ones at 1 to 46 places, the centres by at most `2.5e-24` and the
tangents `t` by at most `3.3e-24`, far inside the `1e-20` gaps; and this repository’s two
checkers accept each. So the solve reproduces the bound here and
not the bytes. At each of the five counts the source reports exact flat motions or free
squares, positions the contacts do not fix, where the solver’s floating-point linear
algebra and LP solves choose; that the differences come from there, and from library
versions, is likely and not shown. The source does not state its environment.

From `packing/`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.evand_exact_certificates check --workers 2
uv run --frozen --all-extras --group dev python -m devtools.evand_exact_certificates source-replay
uv run --frozen --all-extras --group dev python -m devtools.evand_exact_certificates controls --workers 2
uv run --frozen --all-extras --group dev python -m devtools.evand_exact_certificates compare
uv run --frozen --all-extras --group dev python -m devtools.evand_exact_certificates check --check
```

The first two take `--certs` to read a checkout’s 320 certificates; `reproduce --inputs`
takes a checkout’s `batch/inputs/`.

## The 48 Counts

Generated by
`uv run --frozen --all-extras --group dev python -m devtools.evand_exact_certificates table`.
“Printed side” is the side the record held before this import, from the certified packet
named, or the Kingbird catalogue’s at `n = 126`; `S'` is shown to 19 decimals, rounded up.
“Moved squares” counts the squares whose centre or rotation differs from the known-best
witness’s by more than `1e-8`, and how many of them the source lists as free.

| n | Finder | Printed side | Certified side `S'` | Below by | Source's report | Moved squares |
| --- | --- | --- | --- | --- | --- | --- |
| 68 | Francisco Couzo (T-056) | `8.798795237222592` | `8.7987952372182839027…` | `4.31e-12` | KKT local min | 4 (4 free) |
| 102 | Francisco Couzo (T-056) | `10.607174680178947` | `10.6071746801760511255…` | `2.90e-12` | KKT local min | 69 (21 free) |
| 103 | Francisco Couzo (T-056) | `10.703516755580015` | `10.7035167555725420088…` | `7.47e-12` | KKT local min | 72 (6 free) |
| 106 | Francisco Couzo (T-056) | `10.822908044141968` | `10.8229080441328475552…` | `9.12e-12` | KKT local min | 39 (9 free) |
| 110 | Francisco Couzo (T-056) | `10.996783396634358` | `10.9967833966315916397…` | `2.77e-12` | KKT local min | 2 (2 free) |
| 123 | Francisco Couzo (T-056) | `11.601384658385687` | `11.6013846583759755644…` | `9.71e-12` | KKT local min | 45 (14 free) |
| 126 | Joost de Winter (catalogue) | `11.77473513240654` | `11.7747351323878328426…` | `1.87e-11` | KKT local min | 2 (2 free) |
| 131 | Francisco Couzo (T-056) | `11.954916830219048` | `11.9549168302161244102…` | `2.92e-12` | KKT local min | 0 |
| 132 | Francisco Couzo (T-056) | `11.991327887694469` | `11.9913278876915014117…` | `2.97e-12` | KKT local min | 1 (1 free) |
| 152 | Francisco Couzo (T-056) | `12.830718800982252` | `12.8307188009766099550…` | `5.64e-12` | KKT local min | 28 (3 free) |
| 154 | Francisco Couzo (T-056) | `12.931663721169976` | `12.9316637211668470194…` | `3.13e-12` | KKT local min | 58 (0 free) |
| 155 | Francisco Couzo (T-056) | `12.955619592137850` | `12.9556195921344524381…` | `3.40e-12` | KKT local min | 35 (3 free) |
| 156 | Francisco Couzo (T-056) | `12.982082698520427` | `12.9820826985168931021…` | `3.53e-12` | KKT local min | 0 |
| 172 | Francisco Couzo (T-056) | `13.618988956935731` | `13.6189889568993984290…` | `3.63e-11` | KKT local min | 81 (13 free) |
| 177 | Francisco Couzo (T-056) | `13.822979734183507` | `13.8229797341694486003…` | `1.41e-11` | bound only | 8 (2 free) |
| 180 | Francisco Couzo (T-056) | `13.927888140501693` | `13.9278881404980963392…` | `3.60e-12` | KKT local min | 0 |
| 181 | Francisco Couzo (T-056) | `13.953748821957927` | `13.9537488219544024981…` | `3.52e-12` | KKT local min | 52 (0 free) |
| 182 | Francisco Couzo (T-056) | `13.974090713124822` | `13.9740907131214390072…` | `3.38e-12` | KKT local min | 1 (1 free) |
| 199 | Francisco Couzo (T-056) | `14.618988956907218` | `14.6189889568993984291…` | `7.82e-12` | KKT local min | 3 (0 free) |
| 206 | Francisco Couzo (T-056) | `14.860158663395859` | `14.8601586633919032369…` | `3.96e-12` | KKT local min | 41 (41 free) |
| 207 | Francisco Couzo (T-056) | `14.893954634242480` | `14.8939546342372273884…` | `5.25e-12` | KKT local min | 171 (32 free) |
| 208 | Francisco Couzo (T-092) | `14.926534459703511` | `14.9265344596994232470…` | `4.09e-12` | KKT local min | 0 |
| 209 | Francisco Couzo (T-092) | `14.953939011860642` | `14.9539390118571223629…` | `3.52e-12` | KKT local min | 3 (3 free) |
| 210 | Francisco Couzo (T-056) | `14.973001116591412` | `14.9730011165876257420…` | `3.79e-12` | KKT local min | 2 (2 free) |
| 211 | Joost de Winter (T-057) | `14.99796070496771500150` | `14.9979607049673615652…` | `3.53e-13` | bound only | 0 |
| 228 | Francisco Couzo (T-092) | `15.604602454552252` | `15.6046024545460569672…` | `6.20e-12` | KKT local min | 9 (9 free) |
| 236 | Francisco Couzo (T-056) | `15.872219025616040` | `15.8722190256072828784…` | `8.76e-12` | KKT local min | 148 (34 free) |
| 237 | Francisco Couzo (T-056) | `15.911191683008479` | `15.9111916830017830311…` | `6.70e-12` | KKT local min | 112 (13 free) |
| 238 | Francisco Couzo (T-056) | `15.931725503598480` | `15.9317255035913282338…` | `7.15e-12` | KKT local min | 24 (0 free) |
| 239 | Francisco Couzo (T-056) | `15.953819333484685` | `15.9538193334807799155…` | `3.91e-12` | KKT local min | 3 (3 free) |
| 240 | Francisco Couzo (T-056) | `15.969685337536875` | `15.9696853375307803361…` | `6.09e-12` | KKT local min | 3 (3 free) |
| 241 | Francisco Couzo (T-056) | `15.988132439537539` | `15.9881324395249908486…` | `1.25e-11` | KKT local min | 3 (3 free) |
| 259 | Francisco Couzo (T-056) | `16.602568490497649` | `16.6025684904933645154…` | `4.28e-12` | KKT local min | 21 (16 free) |
| 263 | Francisco Couzo (T-092) | `16.742270262031791` | `16.7422702620250576838…` | `6.73e-12` | bound only | 35 (0 free) |
| 268 | Francisco Couzo (T-056) | `16.878814821018413` | `16.8788148210067647248…` | `1.16e-11` | KKT local min | 7 (7 free) |
| 269 | Francisco Couzo (T-056) | `16.905967058598858` | `16.9059670585838409115…` | `1.50e-11` | KKT local min | 120 (20 free) |
| 270 | Francisco Couzo (T-056) | `16.937810329390629` | `16.9378103293409541103…` | `4.97e-11` | KKT local min | 2 (0 free) |
| 271 | Francisco Couzo (T-056) | `16.950820792633813` | `16.9508207926249587865…` | `8.85e-12` | KKT local min | 81 (0 free) |
| 272 | Francisco Couzo (T-092) | `16.968165867864400` | `16.9681658678521583329…` | `1.22e-11` | bound only | 6 (6 free) |
| 273 | Francisco Couzo (T-056) | `16.983925962660670` | `16.9839259626504043162…` | `1.03e-11` | KKT local min | 9 (9 free) |
| 297 | Francisco Couzo (T-056) | `17.740417287548325` | `17.7404172875438018512…` | `4.52e-12` | KKT local min | 21 (18 free) |
| 301 | Francisco Couzo (T-056) | `17.846667192848074` | `17.8466671928434897832…` | `4.58e-12` | KKT local min | 10 (10 free) |
| 302 | Francisco Couzo (T-056) | `17.885993892536710` | `17.8859938925304106667…` | `6.30e-12` | KKT local min | 140 (21 free) |
| 303 | Francisco Couzo (T-092) | `17.924341009860250` | `17.9243410098511283732…` | `9.12e-12` | KKT local min | 47 (18 free) |
| 304 | Francisco Couzo (T-056) | `17.934650018395903` | `17.9346500183906817242…` | `5.22e-12` | KKT local min | 3 (3 free) |
| 305 | Francisco Couzo (T-056) | `17.952959459023539` | `17.9529594590155279629…` | `8.01e-12` | KKT local min | 16 (0 free) |
| 306 | Francisco Couzo (T-092) | `17.963438139777139` | `17.9634381397640028537…` | `1.31e-11` | KKT local min | 2 (2 free) |
| 307 | Francisco Couzo (T-056) | `17.981030548643712` | `17.9810305486333106963…` | `1.04e-11` | KKT local min | 4 (4 free) |

## The 77 Ceiling Counts

At the other counts each certified side lies above the side the record prints, and #375
offered those certificates as an independent exact replay of the existing upper bounds,
asking for nothing to be registered from them.
The owner decided on 6 October 2026 to act on them where they lower a verified ceiling
(`think-70bh`); they are registered as T-101, provisionally T-118 until merged.

**Which counts.** A certificate of a printed side carries the verified upper bound at the
larger of the printed side and its own side rounded up at the printed precision, with
that decimal’s fraction as the exact form: the rule the record applies to Francisco
Couzo’s packings (T-056) and to the catalogue’s packings at `n = 69, 83, 87` (T-088,
T-089). `devtools.apply_exact_ceilings survey` computes that value at each of the 272
counts the receipts decide beside the 48 and the held `n = 17`, and selects those where
it lies strictly below the verified ceiling the record held: 77 counts from `n = 28` to
`300`, every one of them the Kingbird catalogue’s packing
([`receipts/ceiling-survey.json`](receipts/ceiling-survey.json)). The ceiling had been the
integer grid at 74 of them, above the printed side by up to `0.464`, and at
`n = 69, 83, 87` the rounded-up sides of exact certificates of a parse of the catalogue’s
pictures. The one other count whose ceiling trailed its report, `n = 29`, keeps it: its
interval-certified bound (`E-n029-interval-certified-upper`) lies `5e-21` below the
certificate’s side.

**What they carry.** Each certified side lies `1.2e-16` to `9.8e-15` above the printed
one, and at all 77 the printed side has fourteen decimals, so each verified upper bound is
the printed side plus one unit of its last place.
At the 22 counts whose catalogue side is a decimal alone, that agrees with the report at
the precision the record compares them.
At the other 55 the catalogue also gives the side as a closed form, and the certificate’s
side lies `7.6e-20` to `1.8e-19` above it, its outward rounding, so those 55 keep a ceiling
section and a `mathematics` blocker, the ceiling now `1e-14` above the printed side
instead of up to `0.464`.
Forty-nine of those forms are irrational, which no rational certificate reaches.
The other six, at `n = 50, 171, 198, 230, 261` and `293`, are rational (`53/7` at
`n = 50`), and an exact certificate of the packing at that side would reach them, a
rational one where the packing’s exact point is rational.
At `n = 50` the source’s own exact point appears to be such a rational one: with its
scaling by `1 + 10^-20` undone, its side is `53/7` rounded up, and of the 44 squares it
does not list as free, every one has tangent `0` or `1/3` (a 3-4-5 rotation) to within
`1e-30`, and 42 have centres on a grid of `1/350` to within `3e-36`. The other two,
squares 24 and 25 (0-based), sit `8e-17` off that grid along their own 3-4-5 edge
direction, so the snapped packing at `53/7` is not yet decided
(`test_n50_certificate_is_53_over_7_on_a_rational_grid_scaled_outward` holds these
figures; the review’s EC-1, `think-l8gt`).

**The same packings.** Matched square for square with the known-best witness, every
certificate lies within `7.1e-4` of it; of the 416 squares that move by more than `1e-8`,
332 are ones the source lists as free, and the other 84 move by at most `1.2e-7`. Four of
the 77, `n = 127, 129, 260` and `299`, were solved from the witness after the source’s
unpublished SLP squeeze.

**Replayed, retained and controlled.** The run of 5 October decided all 77 with the rest,
by both checkers here (838 of its 2,820 CPU seconds) and by the source’s two (59 of 202),
with least wall clearance `5e-21` and least pair gap about `1e-20` at each.
On 6 October the 77 were retained from a second clone at the pin, byte for byte the
pinned and decided ones, and `controls --ceilings` made the three controls of each, as
for the 48 ([`receipts/negative-controls-ceilings.json`](receipts/negative-controls-ceilings.json)):
one square of the tightest pair moved along the pair’s best separating face axis by that
axis’s gap, about `1e-20`, plus one unit of the side’s denominator (`1e-30` to `1.6e-28`),
and the box shrunk by its least top or right clearance, about `5e-21`, plus that unit, are
refused by all four checkers at every count; the box shrunk by the unit alone is accepted
by all four, as it must be. Every moved square stays at least `0.71` inside the walls, so
each overlap refusal is for the pair. The overlap is chosen by the independent checker’s
own pair gap, so that checker’s refusal of it is circular; the mutant is invalid
regardless, since its edge normals are rational unit vectors and a negative gap on every
face axis means the two interiors meet. The run took 4,696 s of wall time on two workers under
the shared machine’s load; it recorded no CPU time.

Generated by
`uv run --frozen --all-extras --group dev python -m devtools.apply_exact_ceilings table`.
“Earlier ceiling” is the verified upper bound before this import, and `S'` is shown to 19
decimals, rounded up.

| n | Printed side | Closed form | Earlier ceiling | Certified side `S'` | Above printed by | Verified upper bound | Agrees |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 28 | `5.82444461667405` | — | `6` (grid) | `5.8244446166740592971…` | `9.30e-15` | `5.82444461667406` | yes |
| 37 | `6.59861960924436` | — | `7` (grid) | `6.5986196092443601163…` | `1.16e-16` | `6.59861960924437` | yes |
| 39 | `6.81072208306864` | — | `7` (grid) | `6.8107220830686488518…` | `8.85e-15` | `6.81072208306865` | yes |
| 41 | `6.92669309446880` | — | `7` (grid) | `6.9266930944688022317…` | `2.23e-15` | `6.92669309446881` | yes |
| 50 | `7.57142857142857` | `7 + (4/7)` | `8` (grid) | `7.5714285714285714287…` | `1.43e-15` | `7.57142857142858` | no |
| 51 | `7.70079923541701` | — | `8` (grid) | `7.7007992354170117236…` | `1.72e-15` | `7.70079923541702` | yes |
| 53 | `7.82287565553229` | `(13/2) + (1/2)sqrt(7)` | `8` (grid) | `7.8228756555322952954…` | `5.30e-15` | `7.82287565553230` | no |
| 54 | `7.84666719284348` | `7 - (1/2)sqrt(2) + sqrt(1 + sqrt(2))` | `8` (grid) | `7.8466671928434897831…` | `9.78e-15` | `7.84666719284349` | no |
| 55 | `7.94577100750391` | — | `8` (grid) | `7.9457710075039129791…` | `2.98e-15` | `7.94577100750392` | yes |
| 69 | `8.82719465572973` | — | `8.82719465572975` (T-088) | `8.8271946557297389151…` | `8.92e-15` | `8.82719465572974` | yes |
| 70 | `8.88166675700900` | — | `9` (grid) | `8.8816667570090046250…` | `4.62e-15` | `8.88166675700901` | yes |
| 71 | `8.94407155757031` | — | `9` (grid) | `8.9440715575703155067…` | `5.51e-15` | `8.94407155757032` | yes |
| 83 | `9.63475764863108` | — | `9.63475764863195` (T-089) | `9.6347576486310820294…` | `2.03e-15` | `9.63475764863109` | yes |
| 87 | `9.83881526994826` | — | `9.83881526994915` (T-089) | `9.8388152699482622604…` | `2.26e-15` | `9.83881526994827` | yes |
| 88 | `9.88815305375857` | — | `10` (grid) | `9.8881530537585723829…` | `2.38e-15` | `9.88815305375858` | yes |
| 101 | `10.53553390593273` | `7 + (5/2)sqrt(2)` | `11` (grid) | `10.5355339059327376222…` | `7.62e-15` | `10.53553390593274` | no |
| 104 | `10.70710678118654` | `10 + (1/2)sqrt(2)` | `11` (grid) | `10.7071067811865475246…` | `7.52e-15` | `10.70710678118655` | no |
| 107 | `10.84666719284348` | `10 - (1/2)sqrt(2) + sqrt(1 + sqrt(2))` | `11` (grid) | `10.8466671928434897831…` | `9.78e-15` | `10.84666719284349` | no |
| 108 | `10.92591939016138` | — | `11` (grid) | `10.9259193901613875107…` | `7.51e-15` | `10.92591939016139` | yes |
| 109 | `10.94974746830583` | `6 + (7/2)sqrt(2)` | `11` (grid) | `10.9497474683058326710…` | `2.67e-15` | `10.94974746830584` | no |
| 122 | `11.53553390593273` | `8 + (5/2)sqrt(2)` | `12` (grid) | `11.5355339059327376222…` | `7.62e-15` | `11.53553390593274` | no |
| 124 | `11.65685424949238` | `6 + 4 sqrt(2)` | `12` (grid) | `11.6568542494923801954…` | `1.95e-16` | `11.65685424949239` | no |
| 125 | `11.70710678118654` | `11 + (1/2)sqrt(2)` | `12` (grid) | `11.7071067811865475246…` | `7.52e-15` | `11.70710678118655` | no |
| 127 | `11.82287565553229` | `(21/2) + (1/2)sqrt(7)` | `12` (grid) | `11.8228756555322952954…` | `5.30e-15` | `11.82287565553230` | no |
| 128 | `11.82509196821368` | — | `12` (grid) | `11.8250919682136870293…` | `7.03e-15` | `11.82509196821369` | yes |
| 129 | `11.88130621809000` | — | `12` (grid) | `11.8813062180900030634…` | `3.06e-15` | `11.88130621809001` | yes |
| 145 | `12.53553390593273` | `9 + (5/2)sqrt(2)` | `13` (grid) | `12.5355339059327376222…` | `7.62e-15` | `12.53553390593274` | no |
| 146 | `12.60090777851301` | — | `13` (grid) | `12.6009077785130182403…` | `8.24e-15` | `12.60090777851302` | yes |
| 147 | `12.65685424949238` | `7 + 4 sqrt(2)` | `13` (grid) | `12.6568542494923801954…` | `1.95e-16` | `12.65685424949239` | no |
| 148 | `12.65685424949238` | `7 + 4 sqrt(2)` | `13` (grid) | `12.6568542494923801954…` | `1.95e-16` | `12.65685424949239` | no |
| 149 | `12.70710678118654` | `12 + (1/2)sqrt(2)` | `13` (grid) | `12.7071067811865475246…` | `7.52e-15` | `12.70710678118655` | no |
| 150 | `12.77817459305202` | `5 + (11/2)sqrt(2)` | `13` (grid) | `12.7781745930520227686…` | `2.77e-15` | `12.77817459305203` | no |
| 151 | `12.82287565553229` | `(23/2) + (1/2)sqrt(7)` | `13` (grid) | `12.8228756555322952954…` | `5.30e-15` | `12.82287565553230` | no |
| 153 | `12.88166675700900` | — | `13` (grid) | `12.8816667570090046250…` | `4.63e-15` | `12.88166675700901` | yes |
| 170 | `13.53553390593273` | `10 + (5/2)sqrt(2)` | `14` (grid) | `13.5355339059327376222…` | `7.62e-15` | `13.53553390593274` | no |
| 171 | `13.57142857142857` | `13 + (4/7)` | `14` (grid) | `13.5714285714285714288…` | `1.43e-15` | `13.57142857142858` | no |
| 173 | `13.65685424949238` | `8 + 4 sqrt(2)` | `14` (grid) | `13.6568542494923801954…` | `1.95e-16` | `13.65685424949239` | no |
| 174 | `13.70710678118654` | `13 + (1/2)sqrt(2)` | `14` (grid) | `13.7071067811865475246…` | `7.52e-15` | `13.70710678118655` | no |
| 175 | `13.77817459305202` | `6 + (11/2)sqrt(2)` | `14` (grid) | `13.7781745930520227686…` | `2.77e-15` | `13.77817459305203` | no |
| 176 | `13.82287565553229` | `(25/2) + (1/2)sqrt(7)` | `14` (grid) | `13.8228756555322952954…` | `5.30e-15` | `13.82287565553230` | no |
| 178 | `13.84666719284348` | `13 - (1/2)sqrt(2) + sqrt(1 + sqrt(2))` | `14` (grid) | `13.8466671928434897831…` | `9.78e-15` | `13.84666719284349` | no |
| 179 | `13.89534106997649` | — | `14` (grid) | `13.8953410699764907318…` | `7.32e-16` | `13.89534106997650` | yes |
| 197 | `14.53553390593273` | `11 + (5/2)sqrt(2)` | `15` (grid) | `14.5355339059327376222…` | `7.62e-15` | `14.53553390593274` | no |
| 198 | `14.57142857142857` | `14 + (4/7)` | `15` (grid) | `14.5714285714285714288…` | `1.43e-15` | `14.57142857142858` | no |
| 200 | `14.65685424949238` | `9 + 4 sqrt(2)` | `15` (grid) | `14.6568542494923801954…` | `1.95e-16` | `14.65685424949239` | no |
| 201 | `14.70710678118654` | `14 + (1/2)sqrt(2)` | `15` (grid) | `14.7071067811865475246…` | `7.52e-15` | `14.70710678118655` | no |
| 202 | `14.72792206135785` | `2 + 9 sqrt(2)` | `15` (grid) | `14.7279220613578554394…` | `5.44e-15` | `14.72792206135786` | no |
| 203 | `14.77817459305202` | `7 + (11/2)sqrt(2)` | `15` (grid) | `14.7781745930520227686…` | `2.77e-15` | `14.77817459305203` | no |
| 204 | `14.82287565553229` | `(27/2) + (1/2)sqrt(7)` | `15` (grid) | `14.8228756555322952954…` | `5.30e-15` | `14.82287565553230` | no |
| 205 | `14.82445114612408` | — | `15` (grid) | `14.8244511461240882237…` | `8.22e-15` | `14.82445114612409` | yes |
| 226 | `15.53553390593273` | `12 + (5/2)sqrt(2)` | `16` (grid) | `15.5355339059327376222…` | `7.62e-15` | `15.53553390593274` | no |
| 227 | `15.57106781186547` | `(17/2) + 5 sqrt(2)` | `16` (grid) | `15.5710678118654752442…` | `5.24e-15` | `15.57106781186548` | no |
| 229 | `15.65685424949238` | `10 + 4 sqrt(2)` | `16` (grid) | `15.6568542494923801954…` | `1.95e-16` | `15.65685424949239` | no |
| 230 | `15.68292682926829` | `15 + (28/41)` | `16` (grid) | `15.6829268292682926831…` | `2.68e-15` | `15.68292682926830` | no |
| 231 | `15.70710678118654` | `15 + (1/2)sqrt(2)` | `16` (grid) | `15.7071067811865475246…` | `7.52e-15` | `15.70710678118655` | no |
| 232 | `15.77817459305202` | `8 + (11/2)sqrt(2)` | `16` (grid) | `15.7781745930520227686…` | `2.77e-15` | `15.77817459305203` | no |
| 233 | `15.77817459305202` | `8 + (11/2)sqrt(2)` | `16` (grid) | `15.7781745930520227686…` | `2.77e-15` | `15.77817459305203` | no |
| 234 | `15.82287565553229` | `(29/2) + (1/2)sqrt(7)` | `16` (grid) | `15.8228756555322952955…` | `5.30e-15` | `15.82287565553230` | no |
| 235 | `15.82660563342856` | — | `16` (grid) | `15.8266056334285680698…` | `8.07e-15` | `15.82660563342857` | yes |
| 257 | `16.53553390593273` | `13 + (5/2)sqrt(2)` | `17` (grid) | `16.5355339059327376222…` | `7.62e-15` | `16.53553390593274` | no |
| 258 | `16.57106781186547` | `(19/2) + 5 sqrt(2)` | `17` (grid) | `16.5710678118654752442…` | `5.24e-15` | `16.57106781186548` | no |
| 260 | `16.65685424949238` | `11 + 4 sqrt(2)` | `17` (grid) | `16.6568542494923801954…` | `1.95e-16` | `16.65685424949239` | no |
| 261 | `16.68292682926829` | `16 + (28/41)` | `17` (grid) | `16.6829268292682926831…` | `2.68e-15` | `16.68292682926830` | no |
| 262 | `16.70710678118654` | `16 + (1/2)sqrt(2)` | `17` (grid) | `16.7071067811865475246…` | `7.52e-15` | `16.70710678118655` | no |
| 264 | `16.77817459305202` | `9 + (11/2)sqrt(2)` | `17` (grid) | `16.7781745930520227686…` | `2.77e-15` | `16.77817459305203` | no |
| 265 | `16.77817459305202` | `9 + (11/2)sqrt(2)` | `17` (grid) | `16.7781745930520227686…` | `2.77e-15` | `16.77817459305203` | no |
| 266 | `16.82306208283780` | — | `17` (grid) | `16.8230620828378046464…` | `4.65e-15` | `16.82306208283781` | yes |
| 267 | `16.84666719284348` | `16 - (1/2)sqrt(2) + sqrt(1 + sqrt(2))` | `17` (grid) | `16.8466671928434897832…` | `9.78e-15` | `16.84666719284349` | no |
| 290 | `17.53553390593273` | `14 + (5/2)sqrt(2)` | `18` (grid) | `17.5355339059327376222…` | `7.62e-15` | `17.53553390593274` | no |
| 291 | `17.53553390593273` | `14 + (5/2)sqrt(2)` | `18` (grid) | `17.5355339059327376222…` | `7.62e-15` | `17.53553390593274` | no |
| 293 | `17.63414634146341` | `17 + (26/41)` | `18` (grid) | `17.6341463414634146344…` | `4.63e-15` | `17.63414634146342` | no |
| 294 | `17.65685424949238` | `12 + 4 sqrt(2)` | `18` (grid) | `17.6568542494923801954…` | `1.95e-16` | `17.65685424949239` | no |
| 295 | `17.70710678118654` | `17 + (1/2)sqrt(2)` | `18` (grid) | `17.7071067811865475246…` | `7.52e-15` | `17.70710678118655` | no |
| 296 | `17.70710678118654` | `17 + (1/2)sqrt(2)` | `18` (grid) | `17.7071067811865475246…` | `7.52e-15` | `17.70710678118655` | no |
| 298 | `17.77817459305202` | `10 + (11/2)sqrt(2)` | `18` (grid) | `17.7781745930520227686…` | `2.77e-15` | `17.77817459305203` | no |
| 299 | `17.82287565553229` | `(33/2) + (1/2)sqrt(7)` | `18` (grid) | `17.8228756555322952955…` | `5.30e-15` | `17.82287565553230` | no |
| 300 | `17.82412338847854` | — | `18` (grid) | `17.8241233884785434711…` | `3.47e-15` | `17.82412338847855` | yes |

## Review

A separately prompted adversarial review of the import, on 2026-10-06
([review](../../../../docs/project/reviews/review-2026-10-06-evand-exact-optima.md)),
found the bound $s(n) \le S'_n$ at the 48 counts sound as reasoned and as the receipts
record it, and ended `defect-open` on one blocking finding: n = 126 kept the
catalogue’s conjectured optimum `11.77473513240654`, `1.9e-11` above the ceiling the
certificate now verifies (EX-1). The layer now clears that conjecture, and
`sqpack.assurance` refuses a decimal conjecture that exceeds its record’s verified
ceiling by more than half a unit in its last place; the check is one-sided and does not
compare the conjecture with the verified floor. The ten other findings were wording,
rounding and receipt fields, none blocking.

A second separately prompted reviewer checked those fixes the same day
([fix check](../../../../docs/project/reviews/review-2026-10-06-evand-exact-optima-fix-check.md))
and ended `defects-resolved`: EX-1 to EX-3, EX-5 to EX-8 and EX-10 resolved, EX-4, EX-9
and EX-11 partly, with seven new findings, none blocking. Since then:

- **EX-4.** The T-098 notes give the reproduction’s tangent differences (FX-1).
- **EX-11.** The layer reads each count’s second-order report beside its status and
  refuses a KKT count whose report is not positive definite modulo exact flat motions;
  all 44 read “strict modulo k exact flat motions (PD on the rest of null(J_A))”, and a
  test holds them (FX-3).
- **The guard.** Its tests now cover both sides of the half-unit band (FX-4).
- **This section and the receipts.** The largest centre displacement is the receipt’s
  `1.441e-3` (FX-2); `summarize.py`’s test line is quoted above with its digest (FX-7);
  this section names what remains (FX-5), and T-098 records both reviews (FX-6).
- **EX-9 stays partly resolved.** Each record’s body says its known-best witness is the
  finder’s binary64 pose at the finder’s larger side and that the certificate witnesses
  $S'$, but the front matter still lists that witness under the reported value $S'$,
  where the atlas writes it for every count; think-5n3o holds the choice.

Neither reviewer could execute code, so no certificate has yet been decided by code
that shares nothing with the tools under review; a second adversarial review that runs
its own decider is what `next_rung` asks for.

### The Review of T-101

Both reviews, stored as their reviewers wrote them, name the entry by its provisional
id, T-118.

A separately prompted adversarial review of the 77 on 2026-10-06
([review](../../../../docs/project/reviews/review-2026-10-06-evand-exact-ceilings.md)),
whose session refused the project interpreter, found the bound and each rounded-up
ceiling to follow from the receipts, the selection and the handling of `n = 29, 69, 83`
and `87` right, and all 125 retained certificates byte for byte the pinned and decided
ones. It ended `defect-open` on one blocking finding, EC-1: the record said no rational
certificate reaches a catalogue closed form, which is false at the six rational ones.
That is reworded in T-101, the blockers and this README.
The six other findings were wording and one missing refusal:

- **EC-2.** `n = 29`’s ceiling is described as its interval-certified bound, not as an
  enclosure of the optimum.
- **EC-3.** `survey` refuses a certificate whose side is not above a closed form, and a
  test holds every gap positive.
- **EC-4.** T-101’s rationale says the 22 ceilings reach the report to one unit of its
  last place.
- **EC-5.** T-088 and T-089 say they are superseded as ceilings, their packings still the
  best known and reported.
- **EC-6.** T-101’s notes name the two rows of the import runbook’s table the entry
  departs from.
- **EC-7.** The overlap control is described as a move along the best separating axis,
  and the independent checker’s refusal of it as circular.

A second separately prompted reviewer checked those fixes the same day
([fix check](../../../../docs/project/reviews/review-2026-10-06-evand-exact-ceilings-fix-check.md)),
also without the project interpreter, and ended `defects-resolved`, with four new
findings, none blocking, handled after it:

- **FC-1.** At the five rational counts other than `n = 50` the record no longer says a
  rational certificate would reach the side, only an exact one, rational where the
  packing’s exact point is.
- **FC-2 and FC-4.** `n = 50`’s grid structure is held by a test, and its two squares
  `8e-17` off the grid are named above.
- **FC-3.** The survey receipt no longer carries a digest column that nothing checked;
  `evand_exact_certificates.is_decided` ties each retained certificate to the decided one.
- **The older wording of EC-7** went from T-101’s claim and the control’s docstring too;
  the controls receipt keeps it as the run wrote it.

## Not Done Here

- **Local optimality.** That each exact point is a KKT local minimum is the source’s
  numerical evidence, recorded as reported. It bears on the packings, not on `s(n)`.
- **The other 195 certificates.** They are replayed with the rest and move no case here:
  at each, the certified side rounded up at the printed precision lies at or above the
  verified ceiling the record already holds.
- **The 55 closed-form sides.** At the ceiling counts whose catalogue side is a closed
  form, the verified upper bound trails it by less than `1e-14`. Reaching it needs an
  exact algebraic certificate of the packing at the 49 irrational sides, and an exact
  certificate at the six rational ones, rational where the packing’s exact point is
  (`think-l8gt`).
- **`n = 17`**, held (`think-x4v4`).

## Compressed Files

The source’s `results.json` runs past 1,000 lines, so it is stored as deterministic gzip
made by `gzip -9n`, with no file name or timestamp in the header.
The table gives the Git blob and SHA-256 of the decompressed bytes.
Readers take the plain path and decompress through
`devtools.retained_data.read_retained_bytes`; `gunzip -k` restores the plain file for a
manual read.

| Stored | Origin | Git blob (decompressed) | SHA-256 (decompressed) |
| --- | --- | --- | --- |
| `square-packing/s12/search/exact/batch/results.json.gz` | upstream | `26705e49fbdc9584343a188720006b423f4c0231` | `cf2ef90c06d95bbfd3ab0468d7ad6248365db8198975959003ba55c20ea466ba` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
