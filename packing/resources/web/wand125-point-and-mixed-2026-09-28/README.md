# wand125 Point-Only and Mixed-Rectangle Certificates, Retrieved 2026-09-28

This packet pins three certificate families that
[wand125/square-packing-bounds](https://github.com/wand125/square-packing-bounds) added
on 2026-09-28, none of them in Tokoharu’s rectangle format, and keeps this repository’s
exact audit and replay receipts for them:

- **`s(45) = 7`**, a point-only measure whose capture condition is decided by Evan
  Daniel’s unmodified `zmx2` checker;
- **`s(21) = 5`**, a point-only measure on Daniel’s `s(21)` support, decided by the
  source’s own rational replay, with a Lean 4 reduction of everything but the capture
  computation; and
- **`s(50) ≥ 37/5 = 7.4`**, a rectangle-density measure checked by a research copy of
  Tokoharu’s `verify.cpp` that accepts coverage `≥ 1`, with the two rungs it supersedes,
  `147/20` and `3659/500`.

Its proposed Frontier key is **[wand125 point and mixed bounds 2026-09-28]**. The same
revision’s rectangle-density certificates, in Tokoharu’s format, are in the
[September 28 rectangle packet](../wand125-rectangle-certificates-2026-09-28/README.md),
and the repository’s earlier certificates in the
[September 22](../external-square-certificates-2026-09-22/README.md) and
[September 27](../wand125-rectangle-certificates-2026-09-27/README.md) packets.
Retention registers the claims for review; what the frontier makes of them is decided in
the frontier records.

## Source and Pin

| Field | Value |
| --- | --- |
| Revision | `39d8ecc74d651b54ec977c331c8f2015b442a6c4`, branch `main`, tree `936e2524c09ca137cf9e02dcd955d6737549253b` |
| Committed | Authored 2026-09-28T22:20:47Z and committed 22:20:54Z, by the author’s clock (`+09:00`) |
| Author | wand125, building on Evan Daniel’s work for the point certificates (the `s(21)` support is his, and his `zmx2` decides `s(45)`) and on Tokoharu’s solver and verifier for the `n = 50` densities; the source README says parts of the work were produced with AI assistance under human direction, and the `s(21)` write-up says its code was developed with Codex |
| Licence | MIT; the root `LICENSE` (blob `bbfbff13`) is byte-identical to the [September 27 packet’s copy](../wand125-rectangle-certificates-2026-09-27/wand125-rectangles/LICENSE). `point_n21_L5/UPSTREAM-LICENSE.txt`, retained, is Evan Daniel’s MIT licence for the derived support |
| Retrieved | 2026-09-28T23:41Z, a blob-filtered clone of `main`, sparse over the root `README.md`, `docs/`, `src/` and the five claim directories |
| Pinned subtree | 517 files, the five claim directories with the root `README.md` and `LICENSE`, each pinned by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256); all 517 digests equal those of the sibling packet’s independent full-tree list, which pins the whole 2,295-file tree |
| Retained here | 64 files, 1,367,112 bytes, under [`square-packing-bounds/`](square-packing-bounds/), byte-identical to the pinned files after decompression |

The commits that introduced each claim, all by the author’s clock:

| Claim | Commit | Authored (UTC) |
| --- | --- | --- |
| `s(21) = 5`, staged | `b97c79633cf7c831c84cd28e28a4c6dce62cd2ba` | 2026-09-28T09:58:50Z |
| `s(21) = 5`, with the complete M1 replay record | `d38917c656c12ef1a5571460b0d599658008b436` | 2026-09-28T10:44:48Z |
| `s(50) ≥ 3659/500` | `b08fb24091f97bec6116406253a25c98da1d8fe8` | 2026-09-28T11:18:31Z |
| `s(21) = 5`, Lean 4 reduction | `b64f96e612d3989d52dd0a93ab6530d4ac015345` | 2026-09-28T12:33:33Z |
| `s(50) ≥ 147/20` | `73a51c72dad2b08c86102a3c104d07844688c796` | 2026-09-28T13:10:46Z |
| `s(50) ≥ 37/5` | `75dd09526b2b3757dcc51e732aecf073e73bd8bb` | 2026-09-28T22:16:21Z |
| `s(45) = 7` | `39d8ecc74d651b54ec977c331c8f2015b442a6c4` | 2026-09-28T22:20:47Z |

**Priority, as the source states it.** For both exact values the source says Evan Daniel
published first, with mixed point-and-segment measures, and claims no priority: “Evan
Daniel already published `s(45) = 7` with a mixed point-and-segment measure.
This work does not claim priority for the value; it is a separate route using points
only.”
For `s(21)` it names Daniel’s bundle commit `086a129a…` (2026-09-27T19:56:22Z) and
says the contribution is “this reweighted point certificate and the accompanying
rational verification route”.
The `n = 50` bounds exceed Green’s reported `2√2 + 101/25 + 3√14/25 = 7.3174260…`
(Friedman DS7, Theorem 9), and the source presents them as certificates past that bound.

[`acquisition/sources.json`](acquisition/sources.json) records the pin, the retained and
pinned-only files and the claim list.
From `packing/`,
`.venv/bin/python3 -m devtools.audit_wand125_point_and_mixed acquire CHECKOUT` rebuilds
both acquisition files and the retained subset from a checkout at the pinned revision.
It only reads the checkout: each file’s Git blob is compared with `git ls-tree`, so a
sparse checkout is enough.

## What Is Retained

Retained byte-identical at their upstream paths:

- **`point_n45_L7/`** whole: `cover.txt`, `check_cover.py`, `verify.sh`,
  `provenance.json` and `README.md`;
- **`point_n21_L5/`** except the bundle: the three point files under `certificates/`
  (`upstream-s21-lower-4.9950.txt` is byte-identical to the copy in the
  [evand packet](../evand-square-packing-2026-09-26/README.md)), the runners
  `inspect_certificate.py`, `unpack_bundle.py`, `verify_portable.py` and
  `assemble_portable.py`, `archive-index.json` (which pins every archive part), the
  write-ups `README.md`, `PUBLICATION.md`, `PROOF-LEMMAS.md` and `FORMAT.md`, the
  provenance and acceptance records, and the Lean overlay except its generated data
  file;
- **`certificates/mixed_n50_L740/`** except the tarball: `candidate.json`,
  `certificate.json`, `manifest.json`, `completion-audit.json`, `README.md` and the ten
  files of `code/`; and
- **`certificates/mixed_n50_L735/`** and **`certificates/mixed_n50_L7318/`**, the
  superseded rungs, except their tarballs and, for `L7318`, its `code/`.

Pinned by digest only, each for a reason:

| Upstream path | Bytes | SHA-256 | Why not retained |
| --- | ---: | --- | --- |
| `README.md` | 37,650 | `5f67b9c8da2fcf0249e865ac75d3e62e0c649e4d0e306de595defe75171f74ce` | Retained byte-identical by the [September 28 rectangle packet](../wand125-rectangle-certificates-2026-09-28/README.md) |
| `LICENSE` | 1,064 | `c0dd43e7892932c81335f74a2fdbf1a98f5977bab14c0c4c30e3abcc97c34904` | Retained byte-identical by the September 27 rectangle packet |
| `point_n21_L5/data/bundle.tar.gz.part-000` … `-013` | 463,568,316 in 14 | each in the subtree list and in the retained `archive-index.json` | The replay bundle; 75,130 files, 2.54 GB unpacked |
| `point_n21_L5/verifier-source/**` | 1,321,496 in 421 | each in the subtree list | Readable copies of the bundle’s Python, which `unpack_bundle.py` checks against the bundle |
| `point_n21_L5/acceptance/m1-full-linkage.json.gz` | 5,310,470 | `0d93072b65c1b162e1cba99db64a14b7f85e21f50b98da720247d3234c665f02` | The M1 run’s complete linkage (decompressed `6efc5fe5…`); compared output for output with the replay here |
| `point_n21_L5/acceptance/split-linkage.json.gz` | 5,391,595 | `54a155da8dd177ef9deae35269f92c5af8c35c4a19c220f46bd2526b3b0b59ef` | The split replay’s linkage |
| `point_n21_L5/lean/Sqpack/N21PtsData.lean` | 160,919 | `1e6559c182bb27b648156ed8183064495b9bb4affe296606b3325ce0bbb1376c` | Generated from `n21-original.txt` by the retained `gen_n21pts_data.py`, whose `--check` passed here |
| `certificates/mixed_n50_L740/n50-L7.40-proof-bundle.tar.gz` | 21,752,211 | `90621d1a7ceb27267ef7b4bf3ffb5906f50e259ac28c955ec6679e64c604638f` | 621-file proof bundle: every angle’s input and result, the axis tables |
| `certificates/mixed_n50_L735/n50-L7.35-proof-bundle.tar.gz` | 18,691,881 | `b7e8ac3184738953312946648e889543ad4cefb4901465761203a166363bd387` | The superseded `147/20` bundle, with its own verifier |
| `certificates/mixed_n50_L7318/n50-L7.318-proof-bundle.tar.gz` | 12,829,854 | `239e4ac5c4b756811708ca78140394d1c4d99d56b066b9fd2eafb90f239b06bd` | The superseded `3659/500` bundle |
| `certificates/mixed_n50_L7318/code/*` | 38,614 in 10 | each in the subtree list | Byte-identical to `mixed_n50_L740/code/`, which is retained |

Each tarball digest is also the one the source README states.
The rest of the tree — the rectangle and earlier point certificates, `src/` and `docs/`
— is pinned by the commit and by the September 28 rectangle packet’s full-tree list.

## The Claims

| Claim | Certificate | Measure | Total | Margin | Decided by |
| --- | --- | --- | --- | --- | --- |
| `s(45) = 7` | `point_n45_L7/cover.txt` | 12,645 distinct points, D4-invariant; coordinates over 2,000, weights over `2^49` | `12666371418707823/2^48 = 44.99999100001…` | `45 − total = 2533271697/2^48` | `zmx2 cert --d4 --pair-points`: every closed unit square in `[0,7]²` captures at least `1` |
| `s(21) = 5` | `point_n21_L5/certificates/n21-original.txt` | 4,604 entries, 4,520 positive, D4-invariant | `2624862500021/125000000000 = 20.999…` | `21q − total = 999979/125000000000` with `q = 249987/250000` | The source’s rational replay: every closed unit square in `[0,5]²` captures at least `q` |
| `s(50) ≥ 37/5` | `certificates/mixed_n50_L740/candidate.json` | 553 rectangle orbit representatives, each spread over its eight D4 images; core side `B = 9977/10000` | `4999999/100000` | `1/100000` | `code/mixed_rotated_verify.cpp` at 200 oblique net angles, integer tables at angle zero |
| `s(50) ≥ 147/20` | `certificates/mixed_n50_L735/candidate.json` | 499 rectangles | `4999999/100000` | `1/100000` | Its bundle’s `unified_linear_verify.cpp`; superseded |
| `s(50) ≥ 3659/500` | `certificates/mixed_n50_L7318/candidate.json` | 355 rectangles | `4999999/100000` | `1/100000` | The same checker as `L740`; superseded |

**The point certificates.** Both use the reduction Daniel’s `s(32) = 6` uses: a packing
of `n` unit squares in a side `L < m`, scaled by `m/L`, gives `n` pairwise disjoint
closed unit squares in `[0,m]²`, which would capture at least `n` (or `nq`), more than
the total.
The grid gives the matching upper bound, and monotonicity gives `s(n) = 5` for
`22 ≤ n ≤ 25` and `s(n) = 7` for `46 ≤ n ≤ 49`. At `n = 45` the checker runs Daniel’s
D4-reduced sweep over centres in `[0,7/2]²` and half-angle tangents in `[0,1/2]` at the
closed unit side, so the margin is exactly zero and a boundary point counts.
At `n = 21` the threshold `q < 1` gives a positive margin; the replay covers centres in
`[0,5/2]²` and `t ∈ [0,1/2]` with 5,000 rational root boxes, and discards the 7,052 of
its 38,730 second-stage regions whose lower `t` exceeds `5/12 > tan(π/8)`.

The `s(21)` support is Daniel’s: its 4,604 coordinates are exactly those of his
`s21_lower_4.9950.txt`, in the same order, scaled by `1001/1000` from side `5000/1001`
to side `5`. Only the weights were re-optimised, and the source notes that the scaling
alone transfers no coverage guarantee.

**The Lean reduction for `s(21)`.** `lean/Sqpack/N21Pts.lean` proves
`n21pts_eq_five_of_checker (h : N21PtsCheckerCover) : minSide 21 = 5`, where the one
hypothesis is that every closed unit square in `[0,5]²` with centre in `[0,5/2]²` and
angle `2 arctan t`, `t ∈ [0,5/12]`, has mass at least `q`. The data, total, D4
invariance, normalisation, angle sufficiency, scaling and grid are proved; the source
reports only the axioms `propext`, `Classical.choice` and `Quot.sound`. It builds as an
overlay on Daniel’s unmodified Lean project at `6e1223cf`. The capture computation is
not formalised.

**The `n = 50` certificates.** Each proves that 50 unit squares do not fit in a square
of side `L` by the shrunken-core argument reviewed on 2026-09-22 for Tokoharu’s format:
the measure is D4-symmetric, `B(1 + 83/40000) = 399908091/400000000 < 1` puts a closed
core of side `B` at one of 201 net angles strictly inside every unit square, and every
such core at every admissible centre has measure at least `1` while the total is below
`50`. Every side exceeds Green’s value, compared here in exact rational arithmetic by
squaring twice: `37/5` by more than `0.0825739888`, `147/20` by more than `0.0325739888`
and `3659/500` by more than `0.0005739888`. The `L7318` measure descends from wand125’s
`L = 7.33` rectangle candidate built with Tokoharu’s solver; the `L740` measure was
built directly at `L = 7.4` by the source’s own initialisation, pricing and repair
pipeline.

## The `n = 50` Checker Against `verify.cpp`

`code/mixed_rotated_verify.cpp` (SHA-256 `89b674a6…`, 144 lines) is a modified copy of
Tokoharu’s `src/verify.cpp` (SHA-256 `a75140df…`, 126 lines, retained in the
[September 22 packet](../external-square-certificates-2026-09-22/tokoharu-density/src/verify.cpp)).
A `diff -u` of the two has three hunks.
Lines 1–78 of `verify.cpp` — the interval primitives, `area_lower`, `slice` and the
`Bound` record — are unchanged but for one added header comment, and so are lines 81–94,
the rectangle loop of `bound` with its derivative penalty.
What differs:

1. **Acceptance threshold.** `verify.cpp` accepts a centre box when its lower bound is
   at least `up(10001/10000)`. The copy accepts when it is at least `gamma.h`, the upper
   end of an interval read from its input.
   The Python driver refuses `gamma < 1`, and all 201 records in each of the `L740` and
   `L7318` bundles carry `gamma = 1`, written as the exact binary64 interval `[1, 1]`.
   The review of 2026-09-22 found the `10001/10000` in `verify.cpp` to be “a sufficient
   certificate inequality, not a tolerance”, so this change removes a margin, not a
   correction term; the 2026-09-28 review adds that the margin had bought insurance
   against an undetected over-estimation below `10^-4`.
2. **Angle data from outside.** `verify.cpp` loops over `r = 0…200` itself, computing
   `c` and `s` from the integers `40000² − (83r)²`, `2·40000·83r` and `40000² + (83r)²`
   in interval arithmetic.
   The copy checks one angle per run and reads `L`, `B`, `E`, `c`, `s` and `gamma` from
   the input file as binary64 enclosures that `mixed_rotated_verify.py` writes from
   exact rationals, rounding each endpoint outward by one step where the rational is not
   a double.
3. **Centre domain.** `verify.cpp` computes `E = L/2 − B(c+s)/2`, the core’s own half
   axis extent, so it checks core centres in `[L/2, L − B(c+s)/2]²`. The driver supplies
   `E = L/2 − r_j`, where `r_j = (1 + 2a − a²)/(2(1 + a²))` with
   `a = max(0, t_j − step/2)` is the half axis extent of the containing *unit square* at
   the lower end of node `j`’s bin (`mixed_net_audit.centre_domains`). The strip between
   the two domains is not checked; over the 200 oblique nodes it is between `0.000120`
   and `0.001627` wide.
   At angle zero the axis tables likewise use `[L/2, L − 1/2]²`. This relies on each
   unit square lying in the container, not only its core, and on `r(t)` increasing on
   `[0, tan(π/8)]`. Both domains are the quarter-turn reduction of the full one.
4. **Point atoms.** `bound` adds the weight of every atom that lies in the closed core
   for every centre of the box.
   None of the three certificates has an atom.
5. **Subdivision control.** The node budget comes from the command line (3,000,000 in
   the manifests) and a box stops splitting at half-width `2^-40` (`verify.cpp`:
   `2^-45`, or 10,000,000 nodes, then exit 3). The split axis is capped at aspect ratio
   four. Unresolved boxes are printed as a frontier with status `ANGLE_UNRESOLVED` rather
   than ending the run; the driver accepts an angle only with status `ANGLE_VERIFIED`
   and an empty frontier.
   A `query` mode and a single-region mode are added, and nonnegative densities and atom
   weights are asserted on input.
6. **Angle zero** is not in the C++ at all.
   `verify_axis_certificate.py` re-checks integer tables (floor-rounded weights and
   overlap fractions, 13,205,956 cells for `L740`) against exact event axes it rebuilds
   from the candidate.

The source calls the oblique replay “the same outward-rounded algorithm … not an
independent second implementation”.
The source READMEs name only the first departure from Tokoharu’s format.
The superseded `L735` rung ships a different verifier, `src/unified_linear_verify.cpp`
in its bundle, which keeps Tokoharu’s centre domain.

The soundness of changes 1 and 3 is the subject of the
[2026-09-28 verifier review](../../../../docs/project/reviews/review-2026-09-28-wand125-n50-mixed-verifier.md),
which found both legitimate and no blocking finding; this packet describes and replays
them.

## Replay Here

Every command ran on 2026-09-28 and 2026-09-29 (UTC) on a four-core KVM guest (Intel
Xeon at 2.10 GHz, Linux 6.18.44) shared with three other lanes, whose load average ran
between about 7 and 13, so every wall below is a contended reading.
This lane held to two cores.
The source’s own scripts ran in a scratch copy of the pinned files under CPython 3.14.7
in a virtual environment with the `s(21)` pins, NumPy 2.5.3 and SciPy 1.18.1 (the source
asks for Python 3.12 or later); this repository’s tool ran under the project
interpreter, CPython 3.14.7 with NumPy 2.5.2. `c++` is GCC 13.3.0 and Rust is 1.94.1.
[`receipts/host.json`](receipts/host.json) records them.
Each log under [`receipts/`](receipts/) opens with its command and start time and closes
with its exit status, wall and child CPU time.

| Check | Command | Wall | CPU | Result |
| --- | --- | ---: | ---: | --- |
| All three families, exact | `devtools.audit_wand125_point_and_mixed exact` | 0.6 s | 0.4 s | Every premise below the table; no source code imported |
| `s(45)`, the source’s full check | `sh verify.sh WORK 2` from `point_n45_L7/` | 1,287 s | 1,494 s | `N45_POINT_COVER_VERIFIED`; see below |
| `s(21)`, data | `python inspect_certificate.py` | 0.3 s | 0.3 s | `EXACT_CERTIFICATE_DATA_CHECKED`, output byte-identical to the shipped `certificate-data-check.json` |
| `s(21)`, bundle bytes | `python unpack_bundle.py` | 51 s | 47 s | `BUNDLE_BYTES_VERIFIED`: all 14 parts, the combined archive and 75,130 files, manifest `bb2883c5…` |
| `s(21)`, Lean overlay | every step of `lean/build_lean.sh` before `lake` | 0.3 s | 0.1 s | Daniel’s `Sqpack.lean` has the pinned SHA-256; `gen_n21pts_data.py --check` regenerates `N21PtsData.lean` byte for byte; no `sorry`, `native_decide` or `axiom` in the overlay. `lake build` not run: no Lean toolchain here |
| `s(21)`, the source’s full replay | `python verify_portable.py --workers 2 --out OUT` | 13,773 s | 20,765 s | `FRESH_ALL_DOMAIN_REPLAY_VERIFIED`, every proof file byte-identical to the source’s M1 run; see [Complete Replays](#complete-replays-here-29-september-2026) |
| `s(50)`, bundle bytes | `n50-bundle-check` on a pristine unpacking | 0.5 s | 0.4 s | All 621 entries of `files-sha256.json` match; nothing unlisted |
| `s(50)`, inputs | `n50-inputs` on the same unpacking | 26 s | 18 s | Each of the 200 oblique inputs hashes to the digest its `result.json` records, and every interval in it encloses the exact datum recomputed here |
| `s(50)`, sampled replay | `n50-replay BUNDLE --index 0 --index 1 --index 150 --index 200 --workers 2` | 852 s | 814 s, summed per angle | All four equal the shipped records; see below |
| `s(50)`, the source’s full replay | `python3 code/verify_mixed_full_proof.py proof --workers 3` | 19,507 s | not recorded | `ALL_ANGLES_VERIFIED_AND_REPLAYED`, all 201 directions equal to the shipped records; see [Complete Replays](#complete-replays-here-29-september-2026) |

**`s(45)`.** `verify.sh`, unchanged, ran `check_cover.py`, cloned `evand/square-packing`
at `6e1223cf`, checked `zmx2.rs` against its pinned SHA-256 `6b7f0f79…`, built it with
`cargo build --release` (binary `5ee58ade…`; the source’s macOS build is `4d2e0d3e…`),
confirmed the exact D4 invariance and ran `zmx2 cert cover.txt --d4 --pair-points
--threads 2`. It printed `VERIFIED-D4` for all 4,900 roots of `[0,7/2]² × [0,1/2]` (35
by 35 centre cells, four half-angle bins): 1,295,460 boxes, 629,884 certified and 20,296
empty leaves, none uncertified or capped, maximum depth 38. The box count and depth
equal the source’s reference run, which took 204.4 s on eight threads of an Apple M4
under Rosetta. The sweep took 1,269 s here on two threads; `zmx2`’s own `cpu 2534s` is
summed per-root thread wall time under contention, and the process CPU was 1,494 s
including the build.
The roots log’s digest cannot equal the source’s `roots_sha256`, because each line
carries that root’s milliseconds.
`n45-compare` re-reads the retained logs.

**`s(21)`.** `unpack_bundle.py` rebuilt the 2.54 GB bundle from its 14 parts, checking
every part, the combined archive and all 75,130 files against the manifest.
The complete run, `verify_portable.py --workers 2 --out OUT`, started at
2026-09-29T00:24:41Z. Its stages run in order: the root stage (5,000 root boxes), the
sieve stage (8,758 parents), then two frontier shards of 15,839 required parents each,
then exact assembly.

- The root stage exited zero after 300 s (139 s on the source’s M1). All 5,000 of its
  per-root proof files are byte-identical to the M1 run’s, by the digests the pinned M1
  linkage records; the four stage files that differ, `inputs.json`,
  `portable-reads.json`, `progress.json` and `result.json`, carry absolute paths or
  timings.
- The sieve stage exited zero after 812 s (412 s on the M1), with the 104 supplementary
  repairs the assembler requires.
  All 8,758 of its per-parent proof files are byte-identical to the M1 run’s; the same
  four stage files differ.
- The frontier stage was still running when this packet was first written, and ended the
  same night: both shards exited zero, after 12,626 s and 12,575 s (7,873 s and 7,968 s
  on the M1), and the run ended `FRESH_ALL_DOMAIN_REPLAY_VERIFIED`.
  [Complete Replays](#complete-replays-here-29-september-2026) gives what it printed.

The run must end with `FRESH_ALL_DOMAIN_REPLAY_VERIFIED`. Then, from `packing/`,

```sh
.venv/bin/python3 -m devtools.audit_wand125_point_and_mixed n21-compare OUT \
  --m1-linkage M1 --collect resources/web/wand125-point-and-mixed-2026-09-28/receipts/n21 \
  --out resources/web/wand125-point-and-mixed-2026-09-28/receipts/n21/comparison.json
```

with `M1` the pinned `point_n21_L5/acceptance/m1-full-linkage.json.gz` of a checkout at
`39d8ecc`, compares the certified quantities with `m1-full-replay.json` and each of the
45,446 output files with the M1 run’s, and copies the run’s summary, exit records and
logs beside it. `--stage root --stage sieve` gives the same file comparison for finished
stages of a run still in progress, which is how the two lines above were made.

**`s(50)`, sampled.** The source’s driver has no subset mode, so `n50-replay` repeats
the full driver’s preconditions in order — the candidate digest `fdfaed93…`, symmetry,
net, centre domains, manifest and checker digest `89b674a6…` — and then calls the
shipped per-angle functions unchanged: `verify_axis_certificate.replay` at angle zero
and `verify_rotated_result.replay`, which regenerates the input, requires it to be the
recorded bytes and runs the C++ compiled by the source’s own `compile_verifier`
(`-O2 -std=c++17 -ffp-contract=off -fno-fast-math`). Each angle then has to reproduce
the shipped node count, leaf count, lower bound and empty frontier exactly.

| Index | Here | Shipped | CPU here | Upstream seconds |
| ---: | --- | --- | ---: | ---: |
| 0 (axis) | 13,205,956 cells, integer minimum `1.0084468491077132` | the same | 106 s | 59 |
| 1 | 252,065 nodes, lower `1.0000002481875527` | the same | 72 s | 50 |
| 150 | 486,389 nodes, lower `1.0000000004625813` | the same | 276 s | 184 |
| 200 | 605,563 nodes, lower `1.0000000708015935` | the same | 361 s | 295 |

Index 150 carries the certificate’s least recorded bound and index 200 its slowest
angle.
The sample ran on an unpacking of the pinned tarball; a second, pristine unpacking
of the same tarball matched all 621 listed digests.
The oblique angles took 1.34 times their upstream seconds here, so the 200 oblique
angles, 28,350 upstream seconds, would take about 10.5 CPU-hours: over this lane’s
three-hour ceiling, so the complete replay was not run that day.
It ran on 29 September, by the procedure below.
Every one of the bundle’s 201 records carries `gamma = 1` and status `ANGLE_VERIFIED` or
`AXIS_VERIFIED` with an empty frontier, 80,719,306 oblique nodes in all.

**The complete `L740` replay.** In a scratch directory `S`, with `c++` a C++17 compiler
and `python3` an interpreter with NumPy (the project’s `.venv/bin/python3` will do):

```sh
cd S && sha256sum n50-L7.40-proof-bundle.tar.gz   # 90621d1a7ceb27267ef7b4bf3ffb5906f50e259ac28c955ec6679e64c604638f
mkdir pristine run
tar xzf n50-L7.40-proof-bundle.tar.gz -C pristine
tar xzf n50-L7.40-proof-bundle.tar.gz -C run
cd S/run/n50-L7.40-proof-bundle && c++ --version
env -u PYTHONOPTIMIZE OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  python3 code/verify_mixed_full_proof.py proof --workers 3
```

and, from `packing/`, before and after the run:

```sh
.venv/bin/python3 -m devtools.audit_wand125_point_and_mixed n50-bundle-check S/pristine/n50-L7.40-proof-bundle --out F1
.venv/bin/python3 -m devtools.audit_wand125_point_and_mixed n50-compare S/run/n50-L7.40-proof-bundle --out F2
```

The checklist, from the
[2026-09-28 verifier review](../../../../docs/project/reviews/review-2026-09-28-wand125-n50-mixed-verifier.md):
no `-O` and `PYTHONOPTIMIZE` unset, since every check is an `assert` (its MV-1); the
driver refuses more than three workers; it must end with
`ALL_ANGLES_VERIFIED_AND_REPLAYED`, the axis `replayed.json` with 13,205,956 cells and
integer minimum `1.0084468491077132`, and every per-angle `replayed.json` with the
shipped node count and lower bound.
The first command must print `BUNDLE_FILES_MATCH` for all 621 entries.
The driver rewrites `proof/certificate.json` with `results` in completion order, so
`n50-compare` compares it with the retained certificate field by field, checks every
per-angle `replayed.json` against the shipped `result.json`, and must print
`FULL_REPLAY_MATCHES_SHIPPED`. Budget about 10.5 CPU-hours by the sample above (7.88
upstream), so at least three hours of wall on three idle workers; on the shared host it
took five and a half.

**Not replayed, by decision.** `L735` and `L7318` are superseded by `L740` and were not
replayed; their files are retained and their tarballs pinned.
`L735`’s own route is `python3 audit.py` then `python3 replay.py --workers 3` in the
unpacked `green-n50-L735/` (3.48 CPU-hours upstream); `L7318` takes the `L740` procedure
(1.33 CPU-hours upstream).
The `L7318` README and the source README give its least bound as `1.0000019…`; the
retained certificate’s least recorded bound is `1.0000000069521284` at index 81 (the
exact audit and the review’s MV-5 agree), and 160 of its 201 records are below
`1.0000019`. The `L740` figure, `1.0000000004…` at index 150, is right.

**The exact audit.** `devtools.audit_wand125_point_and_mixed exact` recomputes from the
retained bytes alone, and [`receipts/exact-audit.json`](receipts/exact-audit.json)
records:

- every retained file against the subtree list, through its decompressed bytes;
- `s(45)`: the cover’s digest, 12,645 distinct points with coordinates in `[0,7]`,
  nonnegative weights, exact D4 invariance, and total `12666371418707823/2^48` below 45
  by `2533271697/2^48`;
- `s(21)`: the three point files’ digests, 4,604 distinct entries (4,520 positive), D4
  invariance, total `2624862500021/125000000000`, the normalised file equal to the
  original divided by `q`, `21q − total = 999979/125000000000`, the support equal entry
  for entry to Daniel’s scaled by `1001/1000`, and Daniel’s file equal to the evand
  packet’s copy;
- `s(50)`, each rung: side and core, rectangle count, nonnegative masses in the
  container, total `4999999/100000`, the candidate digest recomputed from the candidate
  for `L740` and `L7318`, the checker digest `89b674a6…` in their manifests, the net
  identities, the per-node strip between the two centre domains, the certificate’s least
  recorded bound, the source audit record bound to the certificate and tarball digests,
  and the exact comparison with Green’s value, including that the source’s own
  `green_upper` is an upper bound.

None of it decides coverage.

## Complete Replays Here, 29 September 2026

Both complete runs ended on 29 September in the session that ran the checks of
[Replay Here](#replay-here), on the host [`receipts/host.json`](receipts/host.json)
records.
Their records came into this packet on 2 October from the transfer branches that
held them, `claude/replay-wand125-n21-point` and `claude/replay-wand125-n50-l740-local`,
and that day each compare step ran on the retained records under the project
interpreter, with its receipt written by `devtools.replay_receipt`.

- **`s(21)`.** `verify_portable.py --workers 2 --out OUT` ran from 00:24:41Z to
  04:14:14Z, 13,773 s of wall and 20,765 CPU-s against the M1’s 8,577 s
  ([`n21_verify_portable.log`](receipts/n21/n21_verify_portable.log)). Every stage
  exited zero, and it printed `FRESH_ALL_DOMAIN_REPLAY_VERIFIED`: 5,000 roots, 8,758
  sieve and 31,678 frontier parents, 7,052 excluded
  ([`result.json`](receipts/n21/result.json)). `n21-compare --collect`, against the
  pinned M1 linkage fetched at `39d8ecc` (SHA-256 `0d93072b…`), printed
  `MATCHES_SOURCE_M1_RECORD` ([`comparison.log`](receipts/n21/comparison.log)): every
  certified quantity agrees with `m1-full-replay.json`, and 45,436 of the 45,446 output
  files are byte-identical to the M1 run’s. The other ten are stage bookkeeping that
  carries absolute paths or timings: `inputs.json`, `portable-reads.json`,
  `progress.json` and `result.json` of the root and sieve stages, and each frontier
  shard’s `result.json`. The run’s own `linkage.json` (22,317,976 bytes, SHA-256
  `646c4369…`) is not retained, as the tool intends;
  [`comparison.json`](receipts/n21/comparison.json) records its digest.
- **`s(50)`.** The shipped `verify_mixed_full_proof.py proof --workers 3`, with
  `PYTHONOPTIMIZE` unset and one BLAS thread, ran on a fresh unpacking of the pinned
  tarball from 01:29:37Z to 06:54:44Z, 19,507 s of wall; its CPU time was not recorded.
  It printed `ALL_ANGLES_VERIFIED_AND_REPLAYED` for 201 of 201 directions
  ([`run.log`](receipts/n50/full/run.log)), with the checker its own `compile_verifier`
  built (`replay-verify`, 54,080 bytes, SHA-256 `e3643cb5…`, by GCC 13.3.0; not
  retained). [`receipts/n50/full/proof/`](receipts/n50/full/proof/) keeps every other
  file the driver wrote.
  `n50-compare`, on those files laid over a fresh unpacking with the binary in place,
  printed `FULL_REPLAY_MATCHES_SHIPPED`
  ([`compare.log`](receipts/n50/full/compare.log)): the rewritten certificate equals the
  shipped one field by field, and the axis record and every oblique node count and lower
  bound equal the shipped ones.
  [`compare.json`](receipts/n50/full/compare.json) is byte-identical to the comparison
  the transfer host wrote on 29 September.
  Each `replayed.json` is also byte-identical to the one the shipped bundle carries,
  since the replay writes the same record; the log, the progress file, the binary and
  the certificate rewritten in completion order (`545de253…`, against the shipped
  `3e96341b…`) are what show the run happened.
- **Controls.** The `n = 50` checker, `mixed_rotated_verify.cpp` (`89b674a6…`), accepts
  the `n = 37` certificate at its least-bound direction and refuses two mutated copies
  there, in `receipts/n37/control.json` of the
  [2026-10-01 packet](../wand125-point-and-mixed-2026-10-01/README.md), held by
  `tests/test_wand125_checker_controls.py`; no mutation of the `n = 50` certificate was
  run.
- **`s(21)` controls.** On 2 October `n21-control` ran the accepting run’s
  `verify_portable.py` (`2cea95ce…`) and `assemble_portable.py` (`88888adc…`), with
  `--workers 2`, on two mutated covers; [`receipts/controls/`](receipts/controls/) holds
  them and `tests/test_wand125_checker_controls.py` regenerates each mutation and checks
  its receipt. Each mutation changes one D4 orbit of eight entries and keeps every entry
  in place, because the proof records index entries by position: `drop-heaviest-point`
  sets the weight at `(0.63, 1)` and its images, `50893799989/10^12` each, to zero, and
  `move-point` moves `(1, 0.7)` and its images by `1/1000`. The closed square `[0, 1]²`
  at angle zero, which holds `1001050000003/10^12` of the original, then holds
  `0.89926…` or `0.90966…`, exactly, below `q = 249987/250000`, so neither mutated cover
  is a certificate. The bundle’s records name the cover by its SHA-256, so the source’s
  own checks would refuse any changed cover by digest before any arithmetic.
  The tool therefore runs each mutation on a hard-linked copy of the pinned bundle
  re-bound to it: the 37,222 records that name the cover’s digest and the manifest are
  rewritten with the new digest, and the Python is not touched (one script that names
  the digest, `n21_L5_refit29_scoped_gate/check.py`, is not on the replay’s path).
  The runner has no subset mode, so each run went to its first failure, and both ended
  in the root-stage witness replay’s own refusal at root 832, the first of the 5,000
  root boxes, in the order the stage runs them, that holds an admissible pose (the
  corner square itself): `ValueError: Insufficient witness mass` for the dropped orbit
  and `ValueError: Point containment not proved: 66` for the moved one, entry 66 being
  `(1, 0.7)` itself. Each run took about six seconds of wall and three of CPU.

## Receipts

- [`receipts/host.json`](receipts/host.json): CPU, cores and toolchain versions.
- [`receipts/exact-audit.json`](receipts/exact-audit.json): the exact audit;
  `exact --check` recomputes it.
- [`receipts/n45/`](receipts/n45/): `verify_sh.log` (the whole run), `run.log` and
  `roots.log.gz` (the `zmx2` output and per-root census), `zmx2_d4.log`,
  `cargo_build.log`, and `comparison.json`, which `n45-compare receipts/n45` rebuilds
  from those logs.
- [`receipts/n21/`](receipts/n21/): `inspect.log`, `unpack.log`, the Lean overlay steps
  (`lean_overlay_prefix.sh`, with this lane’s scratch paths, and its log),
  `stage_comparison.json` (the root and sieve outputs against the M1 run’s, made while
  the frontier ran), and the complete run’s records as `n21-compare --collect` copied
  them: `n21_verify_portable.log`, `run-inputs.json`, `result.json`, each stage’s log
  and exit record (the two frontier logs as `.gz`), and `comparison.json` with its
  receipt `comparison.log`.
- [`receipts/n50/`](receipts/n50/): `bundle_check.json`, `inputs.json` and
  `sample.json`, each with the log of the run that wrote it; and `full/`, the complete
  replay’s `run.log`, `start.txt` and `end.txt`, the driver’s outputs under `proof/`
  (`certificate.json.gz`, `replay-progress.json` and the 201 `replayed.json`), and
  `compare.json` with its receipt `compare.log`.
- [`receipts/controls/`](receipts/controls/): the two `s(21)` controls, each as the
  runner’s receipt `n21_control_KIND.log`, the root stage’s own log
  `n21_control_KIND_root.log`, and `n21_control_KIND.json`: the mutation, the exact
  witness, the re-binding and how the run ended.

The tool is
[`devtools/audit_wand125_point_and_mixed.py`](../../../devtools/audit_wand125_point_and_mixed.py),
and
[`tests/test_wand125_point_and_mixed.py`](../../../tests/test_wand125_point_and_mixed.py)
keeps its fast part true;
[`tests/test_wand125_checker_controls.py`](../../../tests/test_wand125_checker_controls.py)
holds the controls.

## Limitations

- **Coverage rests on each source’s checker.** `zmx2` is Daniel’s, written independently
  of wand125’s search, although the source says `zmx2` also located the weak poses
  during that search. The `s(21)` replay and the `n = 50` driver are wand125’s, and the
  source calls the `n = 50` oblique replay the same algorithm run again.
  None of the three is a second method; each replay here is the source’s program run
  again.
- **The `s(21)` replay** re-executes the bundle’s recorded proof objects with the new
  weights; the lemmas behind them are prose in `PROOF-LEMMAS.md` and were not reviewed
  here.
- **Lean.** The `s(21)` Lean overlay was not built.
  Its data file was regenerated from the certificate and matched, and it was scanned for
  forbidden constructs, but the kernel checks and the axiom report are the source’s.
- **`n = 50`.** The complete replay ran the source’s driver and checker again; the
  angle-zero tables are a second implementation for one direction only.
  The soundness of the threshold and centre-domain changes is the subject of the
  2026-09-28 review, not of this packet.
- **Controls.** The `n = 50` checker’s controls were run on the `n = 37` certificate,
  not on this one. The `s(21)` controls run on a bundle re-bound to each mutated cover,
  which is what lets them reach the replay’s arithmetic; both are refused at the first
  root box that holds a pose, so neither exercises the sieve or frontier stages.
- **Priority.** For `s(21) = 5` and `s(45) = 7` Evan Daniel’s mixed point-and-segment
  proofs came first, and the source claims no priority; these are second, point-only
  routes.

## Compressed Files

Fifteen data files of more than 1,000 lines are stored as deterministic gzip made by
`gzip -9n`: eleven upstream files — the two `n = 21` point files with Daniel’s support
file, the `n = 45` cover, and the `n = 50` candidates, certificates and audit record —
and four receipts, the two `n = 21` frontier-shard logs, the `n = 45` per-root census
and the certificate the complete `n = 50` replay rewrote.
Each has no file name or timestamp in its header, following the
[R052 packet](../n17-guzhou-r052-2026-09-25/README.md).
The table gives the Git blob and SHA-256 of the decompressed bytes, which for an
upstream file are its blob and digest at the pinned commit and for a receipt are the
bytes this repository wrote.
The repository’s readers take the upstream path and decompress transparently through
`devtools.retained_data.read_retained_bytes`, and
`python -m devtools.retained_data check PACKET` re-derives every row.
Each upstream SHA-256 is also the one
[`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) pins.

Before running any of the source’s own programs on this packet, restore the exact
upstream tree from the repository root:

```sh
find packing/resources/web/wand125-point-and-mixed-2026-09-28 -name '*.gz' -exec gunzip -k {} +
```

The restored plain files are untracked, so remove them afterwards; while both copies are
present, the repository’s readers require them to agree.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `receipts/n21/frontier-s0.log.gz` | receipt | `fe34f614c5824ff54dafc0b91e61bd8cd5486e9c` | `34950ceae8c6ed75d70ced698106bcbe7f2b487a194fb79927d9a5b582a041d6` |
| `receipts/n21/frontier-s1.log.gz` | receipt | `2b352fad97f4e4d8aaa7b1382bcc357a6dd88d4e` | `8db8376070249d8c61499a39078cb5111df7437780c0ee0d2592c1bb0880cd0e` |
| `receipts/n45/roots.log.gz` | receipt | `5da0ec48641158ac8100ad99044d472b110f709f` | `45c1c221013b019062b8d43e985886604656f8b4b1ff398853ab32fa2ef505bd` |
| `receipts/n50/full/proof/certificate.json.gz` | receipt | `7a4eedbec1332f3a1e3822afc6e16aaee1888cbb` | `545de253151146e4977a03d8fe3524a9ae83382b51e6fe1d66f825534f260bf0` |
| `square-packing-bounds/certificates/mixed_n50_L7318/candidate.json.gz` | upstream | `7d63faad0fc6ec167d077328fb14955726a7f84c` | `096a3219fb53574af28109d3cae2f6ad39aedb4b85bcf5333010b8dc2fe7a590` |
| `square-packing-bounds/certificates/mixed_n50_L7318/certificate.json.gz` | upstream | `35afd2d15762cea809cf3e670d6bd28955ea769f` | `59c13465a2b1cd12626166879deb292598d1063b0655330a36c608d80212bc4d` |
| `square-packing-bounds/certificates/mixed_n50_L735/candidate.json.gz` | upstream | `93036e5b3a87155f84854d79e0be19ae8d21c18b` | `ddb70daa1878a022585e1a585851a9ef2a92b9f1a1ff749e901e190992eef5cd` |
| `square-packing-bounds/certificates/mixed_n50_L735/certificate.json.gz` | upstream | `f9b64913cf60105689424995f0f2a0e70412a626` | `7feee2c77b2a653a40a87673b7d3842fd7e2056c8174fbf6e644f476cc5d9e38` |
| `square-packing-bounds/certificates/mixed_n50_L735/final-audit.json.gz` | upstream | `0a6e1154203d43e74d09e55e01e4bf50cd697541` | `a65326dfc1d5bb8331900c59fa6d35da7eba9454136b8fab58a721d1f8cabc68` |
| `square-packing-bounds/certificates/mixed_n50_L740/candidate.json.gz` | upstream | `57da13cb221041ba1bd80a81e604b01805ebb973` | `139fc31b9cea47bca7a4240a55077a97b35cbb164cef1d018f2a728a0ca03766` |
| `square-packing-bounds/certificates/mixed_n50_L740/certificate.json.gz` | upstream | `ae9ff15050b4de51006d3e217ddf36211b567caa` | `3e96341b12e4a3db7ba035fc4853d6fa79fd0e531284c2badc313af0290a91d7` |
| `square-packing-bounds/point_n21_L5/certificates/n21-capture-one.txt.gz` | upstream | `57bad49aa526831effbe355dbcdb800e9e902544` | `9f631fbae420e0376ea636a232b7680e937deebe205dc035cfb9c43a3d74b456` |
| `square-packing-bounds/point_n21_L5/certificates/n21-original.txt.gz` | upstream | `2fe4d84942ec2466c697968ce0d30a0d248f02cb` | `84a7dae793f05ff72de52ddcd3058e8518c1f84c461f94d11305adefe6137679` |
| `square-packing-bounds/point_n21_L5/certificates/upstream-s21-lower-4.9950.txt.gz` | upstream | `9718ac85cac9bf3c9d0e7e7cb380f30689aace58` | `c8e8f878205f2da9c213e4a87c06f17c5a759dce7e695e676dd5c50e0994f2ef` |
| `square-packing-bounds/point_n45_L7/cover.txt.gz` | upstream | `ee2017302e596cb85974aa41c4c8d8a3501f58ca` | `f7d706aa07506c351d9c4b76082cc391ae3f1fd20f6759496bd7c601bb0ca192` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
