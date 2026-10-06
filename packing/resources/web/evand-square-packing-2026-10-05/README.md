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
**[evand exact optima 2026-10-05]**, the result is registered as T-098 (provisional until
merged), and the import bead is `think-t6ok`.

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
| Retained here | The 48 improving certificates `batch/certs/n-N.cert` (1.6 MB), both checkers `verify_cert.py` and `verify_cert2.py`, the solver `exactsolve.py` and its `geom.py`, the drivers `verify_all.sh` and `reproduce.sh`, `batch/results.md`, the source’s per-count report `batch/results.json` (stored compressed) and both READMEs |
| Pinned by digest only | The other 272 certificates, all 320 solver inputs, the solver’s seven-input test set and its outputs, the batch’s scripts that read the register and build its tables, and `candidates_all.json`: 632 files, 6.2 MB, listed with their reasons in [`acquisition/sources.json`](acquisition/sources.json) |
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

## Not Done Here

- **Local optimality.** That each exact point is a KKT local minimum is the source’s
  numerical evidence, recorded as reported. It bears on the packings, not on `s(n)`.
- **The other 272 certificates.** They are replayed with the rest and move no case here.
  Where a case’s verified ceiling trails its report, one of them could carry the verified
  lane to within `1e-14` of the printed side; that is an import the author did not ask
  for, left to its own bead.
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
