# Evan Daniel’s `evand/square-packing`, Retrieved 2026-09-28

The second intake of Evan Daniel’s repository of exact computer-assisted lower-bound
certificates for square packing.
Since the [2026-09-27 intake](../evand-square-packing-2026-09-26/README.md) at
`167d842c` it has added two exact values, `s(21) = 5` and `s(45) = 7`, each by a *mixed
cover*: weighted points plus mass spread uniformly along the interior grid lines,
certified at margin zero by two separately written exact checkers.
It has also moved its Lean side forward: a top theorem for `s(21) = 5` from one
computational hypothesis, and, as the source reports, kernel checks of `s(13) = 4` and
`s(32) = 6` with no hypothesis.

Both values close a case in this record, whose upper bounds for `n = 21` and `n = 45`
are the trivial `5 × 5` and `7 × 7` grids.
This packet holds the source bytes that changed or were added since `167d842c` and that
the two proofs and their checks need, the replay receipts, and the record of what was
and was not replayed.
What the repository makes of each claim is in the frontier records and in
[the review](../../../../docs/project/reviews/review-2026-09-28-evand-s21-s45-mixed-covers.md)
written beside this intake, which found no mathematical defect in either.

## Provenance

| Field | Value |
| --- | --- |
| Source | <https://github.com/evand/square-packing> |
| Commit | `6aa82ba457e9eaeaaa3af0833600f27f91a2fce3`, `main` at retrieval |
| Tree | `c9d23e3a60b60e7fb45f5c93663a68040fccc010` |
| Committed | 2026-09-28T09:36:28−06:00 (2026-09-28T15:36:28Z) |
| Retrieved | 2026-09-28, a complete clone of 428 commits |
| Previous intake | `167d842cd27ba1451cb2833773ea930c80b9e65b`, in [`evand-square-packing-2026-09-26/`](../evand-square-packing-2026-09-26/README.md); 28 commits since |
| Licence | MIT, `Copyright (c) 2026 Evan Daniel`; the two `LICENSE` files are unchanged since `167d842c` and retained in the previous packet |
| Write-ups | <https://evand.github.io/square-packing/s21/> and <https://evand.github.io/square-packing/s45/>, retained as `s12/docs/s21.html` and `s12/docs/s45.html` |

The commits that introduced each claim, by the author’s clock:

| Claim or change | Commit | Committed |
| --- | --- | --- |
| Mixed-cover format and reader | `b37ecf27b7d80354ae72707b235465f09661e243` | 2026-09-26T20:54:17−06:00 |
| `zm_mixed.py`, the first exact mixed-cover checker | `443eac0beaf3127ca82e84397aae230d180b8401` | 2026-09-27T00:23:02−06:00 |
| Lean: `s(21) = 5` from the checker statement | `0462eff366b4f8a7e4e3a61d2a9c2f0a7daa2e7a` | 2026-09-27T09:31:17−06:00 |
| `zmx2`, the second exact mixed-cover checker | `5d91695fba1397fbe5ecf8f506d1302064f74b44` | 2026-09-27T10:19:29−06:00 |
| Adversarial audit of `zm_mixed.py` | `14eb9bd7f64da0a2b5eb1b3425ad72fe2c7c734c` | 2026-09-27T12:17:49−06:00 |
| Adversarial audit of `zmx2` | `457f876fbf6e389fbb65603c4b76799ddff70f7a` | 2026-09-27T13:06:55−06:00 |
| `zmx2` parser fix (audit F1) | `dd6f63aa7e9ba2d7a19c46cb9776ee610ddb3c48` | 2026-09-27T13:21:30−06:00 |
| `s(21) = 5` bundle | `086a129af29596892bfea89b9d81616957abcf59` | 2026-09-27T13:56:22−06:00 |
| `s(45) = 7` bundle | `d2001582d05b044965795dbbd7836faa95fe6a44` | 2026-09-27T22:33:10−06:00 |
| Lean: `s(13) = 4` kernel-checked | `6e1223cf7ef2be4c70baaa36c0e7e7197076735a` | 2026-09-27T22:58:50−06:00 |
| Lean: `s(32) = 6` kernel-checked, no hypothesis | `92cc5bb50cae76978ea7b877fcd9aeb24bd85b55` | 2026-09-28T04:31:18−06:00 |
| Corner-deficit route closed | `5f88e29755b36d313e1c0b97d1fc826771080bca` | 2026-09-28T04:31:18−06:00 |

Commit dates are the author’s clock, not publication dates.
The [wand125 X update packet](../wand125-x-update-2026-09-28/README.md) of 2026-09-28
reports both values; this retrieval is the first acquisition of their sources here.

**Credit, as the source states it.** Evan Daniel, building on Sam Burns and Gustavo
Massaccesi. `LICENSE` names **Evan Daniel** as the copyright holder.
`s12/CREDITS.md` says the work was produced with an AI agent, which it names as Claude
(Anthropic), in a single session under human direction, and that nothing in it has been
peer reviewed. Its lineage section is unchanged: the weighted exact-rational method to
Burns and Massaccesi, the unavoidable-set method to Göbel and its development to
Stromquist, Kearney–Shiu, Nagamochi, Bentz and Friedman, and several verification
practices to Mira’s `17squares`. A new section lists parallel 2026 work: this repository
(jlevy, the Squares Project), Kleddamag, Guzhou0806, tokoharu, wand125 and chelokot.

## The Claims

| Claim | Cover | Points | Segments | Total mass | Previous lower bound in this record |
| --- | --- | ---: | ---: | --- | --- |
| `s(21) = 5` | `s12/certificates/s21/s21_mixed_cover_5.txt` | 7,536 | 1,872 | `522368729933/(25·10⁹) = 20.894749197 < 21` | `5000/1001 = 4.995005`, Daniel’s own angle-net certificate |
| `s(45) = 7` | `s12/certificates/s45/s45_mixed_cover_7.txt` | 19,989 | 3,912 | `2238676387/(5·10⁷) = 44.77352774 < 45` | Nagamochi’s general `1 + √34 = 6.830952` (verified); wand125’s `1391/200 = 6.955` (reported) |

**The format.** A mixed cover, `s12/certificates/s21/FORMAT.md`, is a finite measure on
`[0,s]²`: point masses, and masses spread uniformly by length along segments, all
integers over one coordinate and one mass denominator.
Both files use points and axis-parallel segments only, no polygons.
The segments lie on the interior grid lines, `x, y ∈ {1, …, s − 1}`. In `s(21)` they
carry `17.387894139` of the `20.894749197`, in `s(45)` `32.836410640` of the
`44.773527740`.

**What a file asserts, and why it bounds `s(n)`.** Every **closed** unit square
`Q ⊆ [0,s]²`, at every centre and every angle, has `μ(Q) ≥ 1`, a point on the boundary
counting and a segment along an edge counting in full.
If `n` unit squares with disjoint interiors fit in a side `s′ < s`, scaling by `s/s′`
gives `n` pairwise disjoint closed unit squares in `[0,s]²`, so
`n ≤ μ([0,s]²) = total < n`. The line mass is what makes margin zero possible: a square
seated on a grid cell collects its whole boundary’s line mass, and a slightly tilted one
loses part of an edge on one line and gains the complementary part on the parallel line
one unit away.

**The symmetry reduction.** Both covers are exactly invariant under the square’s eight
symmetries, so it suffices to check squares with centre in `[0, s/2]²` and angle
`θ = 2 arctan u`, `u ∈ [0, ½]`, which is `θ ≤ 53.13°`, more than the `45°` needed.

**Novelty, as the source states it.** `s(21) = 5`, with `s(32) = 6`, is “the second
exact value of `s(k² − 4)` for `k ≥ 4`”, and `s(45) = 7` the third.
The source gives `5000/1001`, wand125’s `399/80` and `249/50`, this repository’s
`122/25`, Friedman’s `4.7438` and Nagamochi’s `1 + √14` as the earlier bounds for
`s(21)`, and wand125’s `1389/200` and Nagamochi’s `1 + √34` for `s(45)`. Its site
history adds wand125’s `1391/200` of 2026-09-27. Nothing is claimed for `k ≥ 8`; the
corner-deficit note (below) says one natural route to a general `s(k² − 4) = k` fails.

## The Two Checkers, and What Each Is Trusted For

| Checker | Language | What it certifies | Arithmetic | Trust caveat |
| --- | --- | --- | --- | --- |
| `search/zm_mixed.py`, `--d4 --cert-mode` | Python | Every root box of the D4 region, by adaptive subdivision of pose space `(cₓ, c_y, u)`: 40,000 roots for `s(21)` and 78,400 for `s(45)` (pitch `1/20`, sixteen `u` bins of `1/32`, depth ≤ 24) | Exact `Fraction` and integer tests; floats only choose which exact test to try | The program is not formally verified; its lemmas are proved on paper in `search/ZM_MIXED.md` §2. It imports `zeromargin.py` unchanged, the file pinned by the `s(32)` bundle |
| `verify2/src/bin/zmx2.rs` (`zmx2`) | Rust | The D4 region (`--d4`: 2,500 and 4,900 roots, pitch `1/10`, four `u` bins of `1/8`), and the whole pose space with no symmetry assumed (`--full`: the cover and its mirror `y ↦ s − y`, 20,000 and 39,200 roots) | Exact integers for point containment and all masses; the positions of chord ends, where a grid line crosses the rotated square’s edges, in IEEE-754 binary64 intervals | See below |

**The float caveat of `zmx2`, as its README states it.** `zmx2` “encloses the positions
of chord ends … with IEEE-754 binary64 interval arithmetic, every operation widened
outward by one ulp and the result rounded outward onto an integer grid of pitch
`1/(1000·2³⁰)` (`search/ZMX2.md` §5, Lemma R). So its verdict is a rigorous enclosure
provided the hardware and compiler give correctly rounded `+ − × ÷ √` without
contraction or reordering (IEEE-754 requires the former; Rust guarantees the latter;
x86-64 SSE2).” That is a different kind of trust from `zm_mixed.py`’s, and the source
says so.

**Independence, as the source states it.** `zmx2` was written from the format statement
alone, without reading `zm_mixed.py` or its write-up, with its own parser, lemmas and
arithmetic, including its own derivation of the germ mechanism.
The two share no code.
They differ in their bounding lemmas (for the segments, `zm_mixed.py`’s Lemmas T, L and
R on top of `zeromargin.py`’s chains, against `zmx2`’s pair dynamic programme), in their
arithmetic (rationals, against outward-rounded binary64 on an integer grid) and in the
symmetry assumed (`zmx2 --full` assumes none).
They share the architecture, branch and bound over the pose space `(c, u)` with
inadmissible poses exempt, and the statement they decide.
Whether that makes them two methods for
[`epistemics.md`](../../../../epistemics.md#confirmation)’s `C4` is the register’s call;
the review (§9) argues that it does, with the shared architecture named as the residual
common-mode risk.

**The adversarial audits, as reported.** Both audits are the source’s own, made on
2026-09-27 within the same work, and both are retained:

- `search/ZM_MIXED_AUDIT.md`: no soundness defect; about 115 M exact checks of certified
  component bounds against exact masses at adversarial poses on the `s(21)` cover, none
  violated; three deliberately holed covers each refused at the hole.
  It audited `zm_mixed.py` at `ebf8bbc3…`; the shipped runs use `ee3e2915…`, after the
  audit’s provenance changes, which the source says changed no lemma (commit
  `fe2ac0b1`).
- `search/ZMX2_AUDIT.md`: no defect touching the certificate; one must-fix in the
  parser, unchecked `i128` overflow on crafted input integers, fixed at `dd6f63aa` by
  bounding every input.
  Both shipped `zmx2` runs are by the patched binary, `6b7f0f79…` source.

Nothing specific to the `s(45)` cover was audited separately; its `README.md` says so.
Both checkers accept it.

## What Lean Covers

**`s(21) = 5`: a top theorem from one hypothesis.** `s12/lean/Sqpack/S21.lean` proves

```lean
theorem s21_eq_five_of_checker (h : S21CheckerCover) : minSide 21 = 5
```

with `minSide` and `Packs` those of the `s(32)` development in the previous packet.
Proved in Lean, per `s12/notes/lean-s21.md`: the reduction from any measure to packings
(`packing_le_measure`, `not_packs_of_measure`), the D4 reduction for measures, mixed
covers as measures with a segment’s mass as the push-forward of Lebesgue measure on
`[0,1]`, and, by `decide +kernel` over the transcribed data `S21Data.lean`, the cover’s
exact D4 invariance entry by entry and its total `2089474919732/10¹¹`. The source
reports `lake build` clean against Mathlib `v4.33.1`, no `sorry`, no `native_decide`,
and only `propext`, `Classical.choice` and `Quot.sound`.

Not proved in Lean, as the note says plainly: `S21CheckerCover` itself, which is the
statement both checkers’ D4 runs certify, and that `S21Data.lean` is the certificate
file, which rests on `lean/scripts/gen_s21_data.py --check` and a digest in the file’s
header. That check passed here.

**`s(45) = 7`: no Lean.** There is no `S45Data.lean` and no top theorem.
The reduction from the cover to the packing bound is the `m = 7` case of lemmas proved
in Lean for general side (`not_packs_of_measure`, `d4_reduction_measure_u`), but nothing
about this cover is checked in Lean.
`lean/LADDER.md` scopes a hypothesis-free rung for both mixed covers (segment terms in
the kernel verifier, an estimated 1.5 to 3 thousand lines of Lean and 15 to 40 CPU-hours
of kernel time each) and marks it not started.

**Reported, not verified here: `s(13) = 4` and `s(32) = 6` with no hypothesis.** The
source reports, in `lean/LADDER.md` and the `s(32)` bundle’s `README.md`, two kernel
checks at margin zero by a new generic verifier `ZMTree.lean`, proved sound once
(`ZMTree.sound`), over box trees generated by `lean/scripts/gen_zmtree.py`, with
`zeromargin.py` as an untrusted oracle:

| Theorem | File | Data | Build cost reported |
| --- | --- | --- | --- |
| `s13_eq_4 : minSide 13 = 4` | `Sqpack/S13Lower.lean` | generated, 4 part files, gitignored | 538 s wall, 1,995 CPU-s on 4 cores; 13.2 GB RSS per process |
| `s32_checkerCover : S32CheckerCover`, `s32_eq_6 : minSide 32 = 6` | `Sqpack/S32Lower.lean` | generated, 96 part files (267 MB), gitignored | generation 3,992 s wall on 4 cores; build 13.8 CPU-hours, 3 h 33 min wall 4 at a time; 13.7 to 15.2 GB RSS per part process |

Both are opt-in targets, outside `Sqpack.lean`’s default build, so the source’s own CI
Lean job, which builds the default target and checks `Axioms.lean` for `sorryAx`, does
not build them. Their data files are not in the source repository; `gen_data.sh`
regenerates them. `s32_eq_6` would discharge the one hypothesis of the
`s32_eq_six_of_checker` theorem the previous packet describes, and the source’s `s(32)`
README now says what remains trusted for it is Lean’s kernel, Mathlib and the
statement’s definitions.
None of this was built here; see
[Not Replayed Here](#not-replayed-here-and-what-each-would-take).

The same ladder reports `s(12) ≥ 35/9` and `s(12) ≥ 3920/997` in the default build and
`s(11) ≥ 3040/797` as an opt-in target (26 minutes on 3 cores, 17.6 GB RSS). All three
are below this record’s verified bounds and are retained only as statements.

**The corner-deficit note.** `search/CORNER_DEFICIT.md` asks whether one corner module,
a measure modified only inside `[0,R]²`, could save enough per corner to give
`s(k² − 4) = k` for all large `k` from one certificate, and answers no: the deficit
`D*(R)` is `0` for every `R`, by a short exact argument it labels proved, with float LP
tables as illustration.
It concludes that the savings of the `s(21)`, `s(32)` and `s(45)` covers are not
corner-local. It is retained as the source’s note; its LP program,
`search/corner_deficit.py`, is pinned by digest.

## What Is Retained, and What Is Not

**Retained byte-identical** under `square-packing/`, at their upstream paths: 91 files,
every one changed or added since `167d842c`. Every file’s `git hash-object` equals its
blob at the pinned commit, and [`retained-files.sha256`](retained-files.sha256) lists
their SHA-256 digests.
Nine are stored as deterministic gzip, and for those the identity holds after
decompression ([Compressed Files](#compressed-files)).

- The root `README.md`, and `s12/README.md`, `s12/CREDITS.md` and `s12/verify.sh`.
- The `s(21)` bundle, `s12/certificates/s21/`: the cover, `FORMAT.md`, `README.md`,
  `SHA256SUMS`, `verify.sh`, the `zm_mixed.py` run (`checker/`, the three files that
  ran; `manifest.json`; `roots.jsonl`; `run.log`), and both `zmx2` runs (`manifest.txt`,
  `roots.log`, `run.out`).
- The `s(45)` bundle, `s12/certificates/s45/`, in the same shape, and the `s(32)`
  bundle’s updated `README.md`.
- Checkers: `verify2/src/bin/zmx2.rs`; `search/zm_mixed.py` and `mixed_cover.py`, equal
  to the bundles’ `checker/` copies; the record summarisers `search/s21_records.py` and
  `mixed_records.py`; the run scripts `s21_cert_runs.sh`, `s45_cert_runs.sh` and
  `zmx2_run.sh`, and `zmx2_manifest.txt`.
- Tests and audits: `search/zmx2_tests.sh`, `zmx2_tools.py`, `zmx2_audit/` (nine files),
  `zm_mixed_test.py`, `zm_mixed_audit.py`, `ZMX2_AUDIT.md` and `ZM_MIXED_AUDIT.md`.
- Write-ups: `search/ZM_MIXED.md`, `ZMX2.md`, `S45_COVER.md`, `LINE_COVER.md` and
  `CORNER_DEFICIT.md`; `notes/lean-s21.md`; `docs/s21.html`, `s45.html`, `s13.html` and
  `s32.html`.
- Lean: `Sqpack.lean`, `Axioms.lean`, `LADDER.md`; `MixedMeasure`, `SegTree`, `S21Data`,
  `S21`, `BoxTree`, `ZMTree`, and the five top files `S11Lower`, `S12Lower`,
  `S12WLower`, `S13Lower` and `S32Lower`; the scripts `gen_s21_data.py`,
  `gen_zmtree.py`, `gen_boxtree.py`, `gen_data.sh` and `build_parts.sh`.

**The two packets together.** The files unchanged since `167d842c` that a replay also
needs are in the previous packet, byte-identical at the same paths:
`verify2/Cargo.toml`, `Cargo.lock` and `src/main.rs` for building `zmx2`;
`search/zeromargin.py` and the `s(32)` bundle, whose `checker/zeromargin.py` both new
bundles `cmp` against; the superseded `s21_lower_4.9950.txt`, which the `s(21)`
`SHA256SUMS` still lists; and the Lean project files and the `s(32)` development.
Of the previous packet’s 56 files, 48 equal their blobs at `6aa82ba4`; the other eight
changed since `167d842c`, and this packet retains their new versions at the same paths.
Overlaying this packet’s `square-packing/` on the previous one’s therefore gives the
pinned tree at every path either holds
([Replay From the Packets](#replay-from-the-packets)).

**Pinned by digest only**, each for a reason:

| Upstream path | Bytes | SHA-256 | Why not retained |
| --- | ---: | --- | --- |
| `s12/lean/Sqpack/S12U/{Pts,Part0..3,Cov}.lean` (6 files) | 325,107 | see below | Generated `s(12) ≥ 35/9` box-tree data from a certificate neither packet retains; below this record’s bound |
| `s12/lean/Sqpack/S12W/{Pts,Part0..3,Cov}.lean` (6 files) | 786,341 | see below | The same for `s(12) ≥ 3920/997` |
| `s12/search/line_cover.py` | 45,020 | `3197205d7e6131c42a7722c22b6326be4052358bd475ef10b24fb772be266f43` | The cutting-plane LP that found the covers; not needed to check them |
| `s12/search/corner_deficit.py` | 11,949 | `3e84add2b33466f8efc6dad062f3f55d08be99c042460804e9e5678be7ec7185` | The LP behind the corner-deficit note’s tables |
| `s12/search/m7_zbisect.sh`, `m7_zuncert.py` | 996, 1,258 | `1a62ebf1febb3d5b493c624919df939f85366d82dc1a7849086b73bb24540d32`, `1ac4b89fd9673b4ab4386f448eed7180761b113f12a9935455cc5687b2102cc4` | The threshold bisection of `S45_COVER.md` §10 |
| `s12/.gitignore` | 388 | `7d76257150e43d8760be775637ec388fc397f4e5057d026e3ba0978eba437a2b` | Retained, it would take effect in this repository; it names the gitignored Lean data sets `S11`, `S13` and `S32Z` |
| `.github/workflows/verify.yml` | 2,837 | `11d873e357d7ebf7ee0d39af7dea98e3a77765b7b577ecb56be756466ee83db4` | The source’s CI: fast tier on every push, `zmx2 --full` included and the `zm_mixed.py` re-sweeps excluded, and a Lean job on the default target |
| `.github/workflows/pages.yml` | 1,761 | `ef7a3b865bca68fdad55bd53a1582c18ab1d3a4109a8b6c7a38727e1d0f1a203` | Site deployment |
| `s12/docs/index.html` | 32,217 | `769e4b181f74aca3d154d0f7d695d9375ae9183335c147c02bbd05b1a26d70bf` | The write-ups’ index page |

The generated Lean data, by file:

| File | SHA-256 |
| --- | --- |
| `S12U/Cov.lean` | `32cf39a71b2e90ebd9bdc436b89513feca6afb0d123a07cda578ad2c8a9e39e4` |
| `S12U/Part0.lean` | `ee049c2144ac6bab50532881d54eb3b06ad67dd0ffc7fbe1b2e77f6a0358dd62` |
| `S12U/Part1.lean` | `30902b91597cc87a9a9175212fba3c07160b599a706462f1e2c0016f33ad218c` |
| `S12U/Part2.lean` | `5387df5ed6d5a3988f02b5d42972a89641c34cfcb785fe9e1ba3d5159821b162` |
| `S12U/Part3.lean` | `c0899148fdfa36d4427d98cf47ea25eab71cb0505baec876df65f8064cff3681` |
| `S12U/Pts.lean` | `b51494f412f7a92a5eb2487794439921698d43ac51edab8876e5a2171a9af364` |
| `S12W/Cov.lean` | `d8ce4cf7b400fa552c1d31904ec0aea5ae35f7d5d5ff70bcddd13b1634b9991d` |
| `S12W/Part0.lean` | `0d3a456a0b7b48af61d004248726af937d1735ca3a0bf9b437ed28469c97c83b` |
| `S12W/Part1.lean` | `9f2a562e9b9231629afbb85adeb639c819dc75e034afe20437ed30d7cd69c024` |
| `S12W/Part2.lean` | `96c6a4f6f57798374c597f74be8c17c44ad02d9e5e1c4b734bf7f0d37ea6b11e` |
| `S12W/Part3.lean` | `bfef81b5791b1ab38e2e3b129dee0016ad3640f463f8e9c410e134be166ea80b` |
| `S12W/Pts.lean` | `c9a1119427d272a80b98580365c6b9d3baaabdba43a4136142680e7f708693d5` |

Because `Sqpack.lean` imports `S12Lower` and `S12WLower`, the default `lake build` needs
these files; the `s(21)` target, `lake build Sqpack.S21`, does not.

**Omitted:** the Square Packing Atlas under `site/`, whose eleven changed files are site
data, pages and scripts, and the rest of the repository, which the previous packet
describes. The Atlas data under `site/www/data/` is derived from David Ellsworth’s
catalogue and excepted from the MIT licence by the source.
Nothing retained here falls under that exception.

## Replay Here

Every command ran on 2026-09-28 and 2026-09-29 (UTC), with outputs written outside the
packet: the fast tiers and the point-cover runs from `s12/` of the two packets overlaid
([Replay From the Packets](#replay-from-the-packets)), the other runs from `s12/` of a
scratch export of the source tree at the pinned commit (`git archive`), which the
overlay equals at every path it holds.
`python3` was the project interpreter, `packing/.venv/bin/python3`, CPython 3.14.7 with
numpy 2.5.2; the source’s CI uses 3.13. A first run of each fast tier from the scratch
export resolved `python3` to the interpreter’s base installation without the virtual
environment, which that tier’s standard-library scripts allow, and gave the same
verdicts (`receipts/s{21,45}_bundle_fast_export.log`). `zmx2` was built from the
retained source with cargo and rustc 1.94.1 in 17 s; its binary, SHA-256
`5ee58adea339e1a911712108aeec044d57b268ee3025821397c64c1c6476c39b`, differs from the
source’s `0247012e…`, built by rustc 1.91.1, as a different toolchain’s build must.
The host is a four-core Linux container shared with three other lanes, with load
averages of about 7 to 13 throughout, so every wall below is a contended reading; this
lane held to two threads or processes.
Each receipt under [`receipts/`](receipts/) opens with its command, interpreter, start
time and load, and closes with its exit status, wall and CPU (user plus system, the
command’s descendants included), and [`receipts/replays.json`](receipts/replays.json)
collects them with the verdict lines.

`zmx2` prints a `cpu` figure that is the sum of its roots’ elapsed times, not processor
time, so on a loaded host it overstates CPU; the tables use the measured CPU.

| Check | Command, from `s12/` | Wall | CPU | Result |
| --- | --- | ---: | ---: | --- |
| `s(21)` bundle, fast tier | `NPROC=2 CARGO_BUILD_JOBS=2 sh certificates/s21/verify.sh` | 272 s | 236 s | `s(21) bundle: OK`, with the fresh `zmx2 --full` census identical to the shipped log, root for root; includes building `zmx2` (16 s) |
| `s(45)` bundle, fast tier | `NPROC=2 CARGO_BUILD_JOBS=2 sh certificates/s45/verify.sh` | 544 s | 393 s | `s(45) bundle: OK`, the same |
| `s(21)`, fresh `zmx2 --d4` | `verify2/target/release/zmx2 cert certificates/s21/s21_mixed_cover_5.txt --d4 --threads 2 --log OUT` | 22 s | 28 s | `VERIFIED-D4`: 2,500 roots, 1,826,222 boxes, maximum depth 26, none uncertified |
| `s(21)`, fresh `zmx2 --full` | the same with `--full` | 198 s | 223 s | `VERIFIED`: 20,000 roots, 14,709,448 boxes, maximum depth 27, none uncertified |
| `s(45)`, fresh `zmx2 --d4` | `… cert certificates/s45/s45_mixed_cover_7.txt --d4 --threads 2 --log OUT` | 36 s | 47 s | `VERIFIED-D4`: 4,900 roots, 2,071,984 boxes, maximum depth 24, none uncertified |
| `s(45)`, fresh `zmx2 --full` | the same with `--full` | 311 s | 394 s | `VERIFIED`: 39,200 roots, 16,648,752 boxes, maximum depth 24, none uncertified |
| `s(21)`, `zm_mixed.py` sample | two centre cells, 32 roots; command below | 376 s | 416 s | `VERIFIED-D4 (PARTIAL)` for both cells, 1,510 boxes, none uncertified; every root’s census equal to the shipped record’s |
| `s(45)`, `zm_mixed.py` sample | two centre cells, 32 roots | 315 s | 304 s | `VERIFIED-D4 (PARTIAL)` for both cells, 2,254 boxes, none uncertified; every root’s census equal to the shipped record’s |
| `s(13)` point cover, `zmx2 --d4` | see below | 11 s | 6 s | `VERIFIED-D4`: 1,600 roots, 47,162 boxes, maximum depth 20, none uncertified |
| `s(32)` point cover, `zmx2 --d4 --pair-points` | see below | 2,705 s | 2,313 s | `VERIFIED-D4`: 3,600 roots, 1,405,342 boxes, maximum depth 29, none uncertified |
| Independent audit | `devtools.audit_evand_mixed_covers check --output receipts/audit.json`, from `packing/` | 5 s | 5 s | clean: both covers, all six shipped records, the four fresh `zmx2` logs, the sample and the two point-cover runs ([`receipts/audit.json`](receipts/audit.json)) |

**What the fast tiers check.** Each bundle’s `verify.sh` checks every line of its
`SHA256SUMS`; re-derives the cover’s exact total, its D4 invariance and its
well-formedness with the source’s record parser; for `s(21)`, regenerates the Lean data
and compares it with `S21Data.lean` byte for byte; re-summarises the shipped
`zm_mixed.py` records (header digests equal to the `checker/` files and the cover, the
settings, every root of the D4 region present and certified) and both shipped `zmx2`
logs; for `s(45)`, `cmp`s its three checker files with the `s(21)` bundle’s and
`zeromargin.py` with the `s(32)` bundle’s; runs `zmx2 d4`, the exact invariance check;
and runs a fresh `zmx2 --full`, comparing its census with the shipped
`zmx2_full/roots.log` root for root.

**The fresh `zmx2` runs, root for root.** The four runs above are separate from the fast
tiers’ and keep their logs, compressed, in `receipts/s21_zmx2_{d4,full}_roots.log.gz`
and `receipts/s45_zmx2_{d4,full}_roots.log.gz`. Each started from an empty log
(`0 already
done`). `devtools.audit_evand_mixed_covers` finds each one complete over its region, no
root uncertified or capped, and every one of the 66,600 roots carrying exactly the
source’s census, boxes, certified and empty leaves, uncertified boxes, maximum depth and
cap flag, with the same header line ([`receipts/audit.json`](receipts/audit.json)). The
shipped runs used ten and six threads, these two; the census does not depend on it.

**The `zm_mixed.py` sample.** The complete re-sweeps are 12.9 and 16.5 CPU-hours at the
source, so this lane ran two centre cells of each D4 region, all sixteen `u` bins of
each, with the shipped settings and the partial-region flags:

```sh
python3 search/zm_mixed.py cert certificates/s21/s21_mixed_cover_5.txt --d4 --cert-mode --disj \
  --chain-from 0 --depth 24 --pitch 1/20 --ubins 16 --nproc 2 --progress 4 \
  --cx-lo 7/4 --cx-hi 9/5 --cy-lo 7/5 --cy-hi 29/20 --resume OUT/a.jsonl --manifest OUT/a.json
```

The cells were chosen from the shipped records’ own per-root CPU, one near the mean cell
cost and one at the 99th percentile, because the distribution is heavy-tailed: half the
cells of each region cost under half a second and the dearest over half an hour.

| Case | Cell, `cₓ × c_y` | Source CPU | Boxes | Maximum depth | Wall | CPU here |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `s(21)` | `[7/4, 9/5] × [7/5, 29/20]`, near the mean | 18.6 s | 38 | 5 | 19 s | 25 s |
| `s(21)` | `[19/10, 39/20] × [3/2, 31/20]`, 99th percentile | 295.6 s | 1,472 | 14 | 357 s | 391 s |
| `s(45)` | `[5/2, 51/20] × [67/20, 17/5]`, near the mean | 12.1 s | 60 | 3 | 16 s | 18 s |
| `s(45)` | `[29/20, 3/2] × [9/4, 23/10]`, 99th percentile | 214.6 s | 2,194 | 17 | 300 s | 287 s |

Every one of the 64 roots carries exactly the source’s census, leaf for leaf, with no
uncertified box, and each record file’s header names the same four SHA-256 digests and
the same settings as the shipped run apart from the partial-region bounds
(`devtools.audit_evand_mixed_covers compare-zm-mixed`). By the checker’s own per-root
CPU figures the sample cost 1.32 and 1.33 times the source’s on the same roots, 414.5 s
against 314.2 s for `s(21)` and 301.3 s against 226.7 s for `s(45)`. The records, run
logs and manifests are `receipts/s{21,45}_zm_mixed_sample_{a,b}.*`. A sample is a
control on the replay path, not a decision: `VERIFIED-D4 (PARTIAL)` is the checker’s
word for a restricted region, and the shipped records remain the only complete
`zm_mixed.py` certification until the full re-sweeps below land.

**The previous packet’s point covers, by `zmx2`.** `zmx2` also reads plain point covers,
and the source reports running it on its `s(13)` and `s(32)` covers without shipping
either log (`search/ZMX2.md` §9). Both were run here from the overlay:
`zmx2 cert certificates/rung2/s13_closed_cover_4.txt --d4 --threads 2` and
`zmx2 cert certificates/s32/s32_closed_cover_6.txt --d4 --pair-points --threads 2`, the
option that couples points one unit apart, without which the source reports 38
uncertified boxes on the `s(32)` cover.
Both certify every root of their D4 regions, 1,600 and 3,600, with no uncertified box,
and their totals equal the ones the source reports: 47,162 boxes, 22,136 certified and
2,245 empty leaves, maximum depth 20, for `s(13)`; 1,405,342, 686,886 and 17,585,
maximum depth 29, for `s(32)`. Each is a complete certification of the cover’s D4 region
by a third implementation of the zero-margin method, after `zeromargin.py` and
`zmcheck`; for `s(13)` it is the first repository replay of any checker on the case-free
cover. Neither moves a bound: `s(13) = 4` is Bentz’s, and `s(32) = 6` already stands at
`V4`/`C3` on the `zeromargin.py` re-sweep.
On 29 September the `s(32)` run was recorded as its own evidence entry,
`E-n032-evand-closed-cover-zmx2-replay`, a second method beside the `zeromargin.py`
re-sweep, which raises `s(32) = 6` to `V4/C4` (jlevy/squares#238).

## Replay From the Packets

The fast tiers and the point-cover runs in the table ran from this directory, built from
the two packets alone:

```sh
mkdir OVERLAY
cp -a packing/resources/web/evand-square-packing-2026-09-26/square-packing/. OVERLAY/
cp -a packing/resources/web/evand-square-packing-2026-09-28/square-packing/. OVERLAY/
find OVERLAY -name '*.gz' -exec gunzip -f {} +
cd OVERLAY/s12 && NPROC=2 CARGO_BUILD_JOBS=2 sh certificates/s21/verify.sh
```

The overlay holds 139 files, and every one’s `git hash-object` equals its blob at
`6aa82ba4`. `verify.sh` builds `zmx2` itself; `python3` on `PATH` must be the project
interpreter, and `CARGO_BUILD_JOBS` bounds the build’s parallelism, which cargo
otherwise sets to the core count.
The overlay cannot run the source’s top-level `s12/verify.sh`, which also needs other
`s(12)` certificates, the `s(13)` unavoidable-set checkers and three rejection-test
suites that neither packet retains.

## Full `zm_mixed` Re-sweeps

**Placeholder, to be filled by the coordinator.** The two complete
`zm_mixed.py --d4 --cert-mode` re-sweeps, 12.9 and 16.5 CPU-hours at the source, are
running in separate sessions.
Their receipts will be retained under `receipts/zm-mixed-full-s21/` and
`receipts/zm-mixed-full-s45/`, which this intake leaves unwritten.
From `packing/`, with `N` 21 or 45 and `B` the bundle directory
`resources/web/evand-square-packing-2026-09-28/square-packing/s12/certificates/sN`, the
comparison with the shipped records and the completeness audit are:

```sh
.venv/bin/python3 -m devtools.audit_evand_mixed_covers compare-zm-mixed --case N --records ROOTS.jsonl
.venv/bin/python3 -m devtools.audit_evand_mixed_covers zm-mixed --case N ROOTS.jsonl --checker-dir B/zm_mixed_d4/checker
```

Both read `ROOTS.jsonl` or `ROOTS.jsonl.gz` and exit 0 only when clean.

## Not Replayed Here, and What Each Would Take

The commands are from `s12/` of the overlay, with `python3` the project interpreter.

**The complete `zm_mixed.py` re-sweeps.** Run the checker directly, not through
`verify.sh --full`, whose working directory is a `mktemp` directory removed on exit, so
an interrupted `--full` loses everything:

```sh
mkdir -p OUT/checker && cp search/zm_mixed.py search/mixed_cover.py search/zeromargin.py OUT/checker/
python3 search/zm_mixed.py cert certificates/s21/s21_mixed_cover_5.txt --d4 --cert-mode --disj \
  --chain-from 0 --depth 24 --pitch 1/20 --ubins 16 --nproc P --progress 1000 \
  --resume OUT/roots.jsonl --manifest OUT/manifest.json > OUT/run.log 2>&1
python3 search/s21_records.py zm_mixed OUT certificates/s21/s21_mixed_cover_5.txt
```

For `s(45)`, substitute `certificates/s45/s45_mixed_cover_7.txt` and
`search/mixed_records.py`. **Resume** is `--resume`: the file’s first line is a header
with the SHA-256 of `zm_mixed.py`, `mixed_cover.py`, `zeromargin.py` and the cover, and
every setting that changes what is checked; each finished root appends one line.
Run again with the same file, the checker skips every root already recorded and refuses
a file whose header differs.
`--nproc`, `--progress` and `--manifest` are not in the header, so a resumed leg may
change them. The source’s runs took 12.9 CPU-hours (`s(21)`, 1.4 h on 10 processes) and
16.5 CPU-hours (`s(45)`, 83 minutes on 12). Scaled by the sample’s ratio, a complete
re-sweep on this contended host would take about 61,000 CPU-seconds, 17 CPU-hours, for
`s(21)`, and 79,000, 22 CPU-hours, for `s(45)`: about 8.5 and 11 hours on two workers.
From `packing/`, `devtools.audit_evand_mixed_covers zm-mixed --case N OUT/roots.jsonl`
audits the result and `compare-zm-mixed --case N --records OUT/roots.jsonl` compares it
with the shipped records root for root.

**The source’s test and audit suites.** `search/zmx2_tests.sh` (45 tests, as the source
reports, 45 of 45 passing), `search/zmx2_audit/run_audit.sh`, `search/zm_mixed_test.py`
and `search/zm_mixed_audit.py` were not run.
They test the checkers, not the covers, and are retained so that they can be.

**Lean, blocked here by the network.** The Lean project pins `leanprover/lean4:v4.33.1`
and Mathlib `v4.33.1`. From this session elan, the toolchain archive (570 MB) and
Mathlib’s source are reachable through GitHub, but Mathlib’s build cache, which Mathlib
`v4.33.1` reads from `https://lakecache.blob.core.windows.net/`, is refused by the
session’s egress policy (HTTP 403 to `CONNECT`;
[`receipts/lean_reachability.log`](receipts/lean_reachability.log)). Every `Sqpack`
module imports `Mathlib` whole, 8,311 modules at `v4.33.1`, so without the cache a build
starts with all of Mathlib from source, on the order of tens of CPU-hours, more than a
day on two cores. With the cache reachable, the steps and costs are:

| Target | Command, from `s12/lean` | Reported cost | Here |
| --- | --- | --- | --- |
| `s(21)` top theorem | `lake exe cache get`, then `lake build Sqpack.S21`; `S32Data.lean`, which `S21` imports through `S32`, is regenerated first by `gen_s32_data.py` | `MixedMeasure` about 4 s; `S21Data` and `S21` about 30 s, mostly the kernel evaluating `check_ok`; about 6.6 GB of memory for the Mathlib import | blocked: no cache |
| Default target and axioms | `lake build`, then `lake env lean Axioms.lean`, which imports the whole default target | the source’s CI job builds it under a 45-minute limit; the `S12W` files take up to 10 GB per process | blocked: no cache, and the twelve `S12U`/`S12W` files are pinned by digest only |
| `s13_eq_4` | `lean/scripts/gen_data.sh S13`, then `lake build Sqpack.S13Lower` | 580 CPU-s to generate; 1,995 CPU-s to build; 13.2 GB per process | not attempted: the host has 16 GB shared by four lanes |
| `s32_eq_6` | `lean/scripts/gen_data.sh S32Z`, then `lean/scripts/build_parts.sh S32Z Sqpack.S32Lower 2` | 15,440 CPU-s to generate; 13.8 CPU-hours to build; up to 15.2 GB per process | not feasible on this host |

## Limitations

- **One architecture, one source.** Both checkers are branch and bound over pose space,
  written separately but within the same source’s work, and both audits are the source’s
  own. The complete fresh `zmx2` runs here are a repository replay of one of them; the
  `zm_mixed.py` side has, so far, the shipped records re-summarised and a 64-root sample
  re-executed. This repository’s parent-core interval engine cannot decide a zero-margin
  cover, for the reason the previous packet gives for `s(32)`, and it has no segment
  atom, so no first-party method is available.
- **The float enclosure.** `zmx2`’s full-space runs, the only checks here that do not
  use the symmetry reduction, rest on IEEE-754 binary64 arithmetic being correctly
  rounded on this x86-64 host, as stated above.
  `zm_mixed.py`’s verdicts use no floats, but only a sample of its sweep was re-executed
  here.
- **The Lean side is unbuilt here.** For `s(21)` the kernel checks the reduction and the
  data, not the covering statement; for `s(45)` nothing about the cover is in Lean; the
  hypothesis-free `s(13)` and `s(32)` results are reported, not verified, and their data
  are generated by `gen_zmtree.py` rather than committed to the source repository.
- **Records are the checkers’ own reports.** The audits re-read the shipped records and
  the fresh logs; they re-derive completeness and the census sums, not the certificates
  of individual boxes.
- **`s(45)` has had less scrutiny.** It was not separately audited at the source, and it
  entered the source on 2026-09-28 (UTC), the day of retrieval.

## Retrieval Hashes

The covers’ and checkers’ digests, which the source also pins in its `SHA256SUMS` files
and run manifests. They are digests of the upstream bytes; the covers are stored
compressed ([Compressed Files](#compressed-files)).

| File | SHA-256 |
| --- | --- |
| `s12/certificates/s21/s21_mixed_cover_5.txt` | `8b415ceeb5f20b02c4e338ce2feb21bc206051ef6bc5c7e433bebae2ef39fc23` |
| `s12/certificates/s45/s45_mixed_cover_7.txt` | `5da180d18434ec52a48b05e8ae0ce70453a280dd482df01d997f73bfbc627c6c` |
| `s12/search/zm_mixed.py` | `ee3e2915349b8795128417bca6414b205d526db9f01f88cd4cd32c32e8d760ac` |
| `s12/search/mixed_cover.py` | `bb89de15ecf5821dd7e1a36ebab8a50d792a406b7fb0f5cb38059f99ef74aae5` |
| `s12/search/zeromargin.py` (previous packet) | `640fe453c1a32f4aa580ca2b1261c6406923a4d7c131f65604a432c7fc2086ab` |
| `s12/verify2/src/bin/zmx2.rs` | `6b7f0f79466bf25c9a85f8fe2f3866de734935f0521ea188136818c2fb5b3fed` |
| `s12/lean/Sqpack/S21Data.lean` | `a0632ed93933410c2625c46c307df2deebe501d44c1ce9e2617341bf11e211a3` |

## Compressed Files

Data files of more than 1,000 lines are stored as deterministic gzip made by `gzip -9n`,
with no file name or timestamp in the header, following
[`packing/resources/README.md`](../../README.md): nine upstream files (the two covers,
both `zm_mixed.py` record files, the four `zmx2` root logs and the `s(45)` full run’s
1,573-line `run.out`) and seven of this packet’s receipts.
The table gives the Git blob and SHA-256 of the decompressed bytes, which for an
upstream file are its blob and digest at the pinned commit and for a receipt are the
bytes this repository wrote.
The repository’s readers take the plain path and decompress transparently through
`devtools.retained_data.read_retained_bytes`, and
`python -m devtools.retained_data check PACKET` re-derives every row.
The source’s `SHA256SUMS` files, `verify.sh` scripts and checkers read the plain files,
so restore them before running any of the source’s programs on this packet, from the
repository root:

```sh
find packing/resources/web/evand-square-packing-2026-09-28 -name '*.gz' -exec gunzip -k {} +
```

The restored plain files are untracked, so remove them afterwards; while both copies are
present, the repository’s readers require them to agree.
[Replay From the Packets](#replay-from-the-packets) restores a scratch copy instead.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `receipts/s13_zmx2_d4_roots.log.gz` | receipt | `c3da5a9dac86a2d9b059e2aaa5056e2a35fc0b69` | `47cdcaaec65fd9a2a98be7d17c632ae56c3f059cbb19cf086158ca831fdb59ba` |
| `receipts/s21_zmx2_d4_roots.log.gz` | receipt | `263e03801859d22a39ff477594b93a0abb1712fb` | `9df401f0ef7a0ad1a04116a6a43b66843517d0ddaa42abbbdc13cd3b2819b426` |
| `receipts/s21_zmx2_full_roots.log.gz` | receipt | `13a41837b835746b0eb742c856bcef168d40b00a` | `e9487eeb91a0f3c4e79e0cdec6bf408024b2ed6c8a8aa7a80627ab813691f239` |
| `receipts/s32_zmx2_d4_pairpoints_roots.log.gz` | receipt | `cbe963e8505b617ca179466d01cc3fe2fd6311c8` | `afaaf261142c95466c86c6d6394ec71b0da12a9389cfe80ad20965caa32526a4` |
| `receipts/s45_zmx2_d4_roots.log.gz` | receipt | `21fba95dc5eace70eb85798ca2b4f48811e9cb46` | `5f8f54d0e6e20cb8dfa98de92c5c7161d3ce7bae6c158edcb642403b16b7370c` |
| `receipts/s45_zmx2_full.log.gz` | receipt | `51e798c9e3e90d9d7d01372cd0859fc5ab447b97` | `784f0e4d1e078dd61587ca5a4ff7c2384761c1ac2fb81f6f351a96c0d8841950` |
| `receipts/s45_zmx2_full_roots.log.gz` | receipt | `dfc403ba3a0abd11ecc7649f63f2c6fc941f695d` | `8bf03a678b2a6f3bb609668eff030a006de9775b9aca4ddb6098fab33021a637` |
| `square-packing/s12/certificates/s21/s21_mixed_cover_5.txt.gz` | upstream | `bafe8cc9eb8840485074fb190d3b7da7af1d1b35` | `8b415ceeb5f20b02c4e338ce2feb21bc206051ef6bc5c7e433bebae2ef39fc23` |
| `square-packing/s12/certificates/s21/zm_mixed_d4/roots.jsonl.gz` | upstream | `0b822e048b8e7132914a580a53bd3d40c2dd565d` | `73c643f023425e182debdcdb179363ebba13ba37f973b313195a6b8c51c3d0bb` |
| `square-packing/s12/certificates/s21/zmx2_d4/roots.log.gz` | upstream | `33c707f038546b74bfddfcb5cdd92b947e1b9ff5` | `5f2b81f23794ca6bdd47db62b6d4de7c2b38012a76a9e79416275a8d2f0328e8` |
| `square-packing/s12/certificates/s21/zmx2_full/roots.log.gz` | upstream | `7a8a5e2955c48c39ee7b33448ebe1d52ce1dc3f0` | `66c1d1e9494a8d669230a4aec157e0927c9662921035999b8e9da7e435c43558` |
| `square-packing/s12/certificates/s45/s45_mixed_cover_7.txt.gz` | upstream | `47ae011ce1e883e740f5523caa01c1dc753c2348` | `5da180d18434ec52a48b05e8ae0ce70453a280dd482df01d997f73bfbc627c6c` |
| `square-packing/s12/certificates/s45/zm_mixed_d4/roots.jsonl.gz` | upstream | `371fd03c8651db0a0fffb9669026c38763a262de` | `6dc3ef1a7b395eaa9af6634f66a4557ecda38e00d6eac9c380367662c4dda2fe` |
| `square-packing/s12/certificates/s45/zmx2_d4/roots.log.gz` | upstream | `425315d306dab01d349d2885e5caf76733427979` | `ead2f437121e2763495c857c360c906546bd49187672781298876f639cf66b8f` |
| `square-packing/s12/certificates/s45/zmx2_full/roots.log.gz` | upstream | `8fbf77c61d28104a89c559ed486522ec8d03d451` | `2678a6f9f9ac6a6972f504f5d598f6aa796101756d97ad668269e4961e6b3e3d` |
| `square-packing/s12/certificates/s45/zmx2_full/run.out.gz` | upstream | `d83b327eef67ec4a433d63f693aba50c7d457917` | `2ae28cdeb7721053651ac8e1d0b530fb08e2fdf0ad9dab5573f60960784e35fd` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
