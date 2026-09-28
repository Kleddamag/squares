# Evan Daniel’s `evand/square-packing`, Retrieved 2026-09-27

A third-party repository of exact computer-assisted lower-bound certificates for square
packing: `s(32) = 6` by a zero-margin weighted closed cover with a Lean top theorem,
`s(12) ≥ 15680/3951`, `s(21) ≥ 5000/1001`, `s(11) ≥ 3040/797`, and a case-free proof
of Bentz’s `s(13) = 4`.
It is retained because three of those claims sit above this record’s verified lower
bounds and one of them closes a case. Two of the three replay here in minutes; the
third took 2.6 CPU-hours here, and its complete re-sweep matches the source’s run.

What the repository makes of each claim is in the frontier records and in
[the review](../../../../docs/project/reviews/review-2026-09-27-evand-s32-s12.md) written
beside this intake. This packet holds the source bytes, the replay receipts, and the
record of what was and was not replayed.

## Provenance

| Field | Value |
| --- | --- |
| Source | <https://github.com/evand/square-packing>, formerly `evand/square-packing-12` |
| Commit | `167d842cd27ba1451cb2833773ea930c80b9e65b`, `main` at retrieval |
| Tree | `0ed02f62b37f01ceb02f70463a4b53343c6945ce` |
| Committed | 2026-09-26T19:42:14−06:00 (2026-09-27T01:42:14Z) |
| Retrieved | 2026-09-27, a complete clone of 400 commits |
| Licence | MIT, `Copyright (c) 2026 Evan Daniel`, at the root and again in `s12/` |
| Write-ups | <https://evand.github.io/square-packing/s32/> and <https://evand.github.io/square-packing/s12/> |

The commits that introduced each claim, all by the same author clock:

| Claim | Commit | Committed |
| --- | --- | --- |
| `s(12) ≥ 15680/3951` | `144f4d3fd807936b03741155b79d3b3c393607d4` | 2026-08-25T21:25:24−06:00 |
| `s(11) ≥ 3040/797` | `dfd5b3cdc6d3924e87caa835a71070ea915bedb4` | 2026-08-26T20:23:21−06:00 |
| `s(13) = 4`, case-free | `815a955a4ac8737b786e08686ec428de0da4456b` | 2026-09-12T05:46:15−06:00 |
| `s(21) ≥ 5000/1001` | `0eee6bae487475b00e887908bec39a9ab3943af3` | 2026-09-23T23:08:46−06:00 |
| Lean: `s(32) = 6` from one hypothesis | `55f0fad0cef17f5a1de29183e9c0a21380f97f97` | 2026-09-26T18:22:44−06:00 |
| `s(32) = 6` certified | `c8b364196c8b4fa0c2c1061add32d9a59a93ef19` | 2026-09-26T18:38:24−06:00 |
| `s(32)` bundle and write-up | `6da04ee3b2cdfb07cc7eead44bb075283ca94fa9` | 2026-09-26T19:30:19−06:00 |
| Novelty wording, `k ≥ 4` | `167d842cd27ba1451cb2833773ea930c80b9e65b` | 2026-09-26T19:42:14−06:00 |

Commit dates are the author’s clock, not publication dates.
The repository was renamed from `square-packing-12`, and when its history became public
is not recorded here; this record’s first sight of it is 2026-09-27.

**Credit, as the source states it.** Evan Daniel, building on Sam Burns and Gustavo
Massaccesi. `LICENSE` names **Evan Daniel** as the copyright holder.
`s12/CREDITS.md` says the work was produced with an AI agent in a single session under
human direction, and that nothing in it has been peer reviewed.
It credits the weighted, exact-rational method to Sam Burns and Gustavo Massaccesi, the
unavoidable-set method to Göbel and its development to Stromquist, Kearney–Shiu,
Nagamochi, Bentz and Friedman, and several verification practices to Mira’s
`17squares`. Its literature note on `s(32)` names this repository and wand125’s
rectangle-density certificates as concurrent work.

## The Claims

| Claim | Certificate | Points | Total weight | What decides it |
| --- | --- | ---: | --- | --- |
| `s(32) = 6` | `s12/certificates/s32/s32_closed_cover_6.txt` | 13,085 | `3171350535386/10¹¹ = 31.713505354 < 32` | Zero-margin closed cover of `[0,6]²`, D4-reduced exhaustive subdivision |
| `s(12) ≥ 15680/3951 = 3.968615…` | `s12/certificates/s12_lower_3.9686.txt` | 1,736 | `11.9738036 < 12` | Positive-margin cover over a rational angle net, `N = 6000` |
| `s(21) ≥ 5000/1001 = 4.995004…` | `s12/certificates/s21/s21_lower_4.9950.txt` | 4,604 | `260057/12500 = 20.80456 < 21` | The same, `N = 6000` |
| `s(11) ≥ 3040/797 = 3.814303…` | `s12/certificates/s11_lower_3.8143.txt` | 680 | `10.8146708 < 11` | The same, `N = 6000` |
| `s(13) = 4`, no case analysis | `s12/certificates/rung2/s13_closed_cover_4.txt` | 3,621 | `2591194431/200000000 = 12.955972155 < 13` | Zero-margin closed cover of `[0,4]²` |

The `s(11)` bound is below this record’s verified `31/8`, as the source’s own
literature note says, and is retained here without being registered.

Every certificate is a finite set of rational points with nonnegative rational weights,
one integer triple per line (`s12/certificates/FORMAT.md`).
Each asserts that every closed unit square inside the container, at every centre and
angle, captures weight at least `1`, a point on the square’s boundary counting.

**The positive-margin bounds.** For `s(12)`, `s(21)` and `s(11)` the container is below
the conjectured side, so the claim tolerates a finite angle net.
The Rust verifier `s12/verify/` enumerates rational rotations `θₖ = 2 arctan(k/N)`; a
unit square at any angle in `[θₖ, θₖ₊₁]` contains the concentric square of side
`σₖ = 1/(cos δ + sin δ)` at `θₖ`, and for each `k` the least captured weight over all
centres is computed exactly by an arrangement sweep.
Twelve interior-disjoint unit squares would capture at least `12` without counting a
point twice; the certificate weighs less.
This is the Burns–Massaccesi object this repository’s own `T-017` and `T-034` use,
with a per-bin shrink instead of one fixed `B`.

**The zero-margin covers.** At the container side itself the margin is exactly zero and
an angle net cannot work. Two exact checkers subdivide pose space
`(cₓ, c_y, u = tan(θ/2))` adaptively instead:
`s12/search/zeromargin.py` (Python, `fractions.Fraction`, floats only as pre-filters)
and `s12/verify2/` (`zmcheck`, Rust, exact `i128`). The reduction is the classical one:
a packing of `n` unit squares in a side `s < m`, scaled by `m/s`, becomes `n` squares
of side `m/s > 1` with disjoint interiors in `[0,m]²`, each strictly containing a
concentric closed unit square, so those closed unit squares are pairwise disjoint and
together capture at least `n`.

**`s(32) = 6`, specifically.** The cover is exactly invariant under the symmetries of
the square, weights included, so it suffices to check centres in `[0,3]²` and
`u ∈ [0, ½]`, which is `θ ≤ 53.13°`, more than the `45°` needed.
`zeromargin.py --d4` certifies all 7,200 root boxes of that region, with 164,130 boxes,
maximum depth 27 and no uncertified box, in 2.77 CPU-hours on the source’s machine; one
root needs depth 30.
`zmcheck --d4` certifies 3,595 of its own 3,600 roots in 80.2 CPU-hours; the five it
leaves open are interior tile germs, which `zeromargin.py` closes.
A second cover, `s32_shift_v1.txt` of total weight `31.697940…`, is certified in full by
both: 7,200 of 7,200 roots and 3,600 of 3,600, the latter with the opt-in branch order
`ZM_MIXPAIR=1`.
The upper bound is the `6 × 6` grid minus four squares.

**The Lean top theorem.** `s12/lean/Sqpack/S32.lean` proves

```lean
theorem s32_eq_six_of_checker (h : S32CheckerCover) : minSide 32 = 6
```

where `minSide n = sInf {s | Packs n s}` and `Packs n s` says `n` closed unit squares,
at any centres and angles, lie in `[0,s]²` with pairwise disjoint interiors.
The one hypothesis, `S32CheckerCover`, says that every closed unit square in `[0,6]²`
with centre in `[0,3]²` and angle `2 arctan u`, `u ∈ [0, ½]`, contains cover entries of
total weight at least `1`. That is exactly what the `zeromargin.py` D4 run certifies.
Everything else is proved in Lean: the D4 reduction, the cover’s invariance and total
weight (by `decide +kernel` over the transcribed data, with no `native_decide`), the
scaling argument and the grid packing. The source reports `lake build` clean against
Mathlib `v4.33.1`, no `sorry`, and only the axioms `propext`, `Classical.choice` and
`Quot.sound`.
The checker programs themselves are not formalised; their primitives are, in
`ZeroMargin.lean`.

**Novelty, as the source states it.** “As far as we can find, this is the first exact
value of `s(k² − 4)` for any `k ≥ 4`”; `s(5)`, the `k = 3` member, is Göbel’s 1979
result, where tilting beats the grid. The write-up adds that Friedman’s survey
conjectures that once `s(k² − c) = k` holds for one `k` it holds for every larger one,
which would carry `s(32) = 6` to `s(45) = 7`; that conjecture is not claimed.
It gives the previous best lower bound for `s(32)` as wand125’s `119/20`, from
2026-09-26.

## What Is Retained, and What Is Not

**Retained byte-identical** under `square-packing/`, at their upstream paths: 56 files.
Every file’s `git hash-object` equals its blob at the pinned commit, and
[`retained-files.sha256`](retained-files.sha256) lists their SHA-256 digests.
Seven of them are stored as deterministic gzip, and for those the identity holds
after decompression ([Compressed Files](#compressed-files)).

- The root and `s12/` `LICENSE` and `README.md`, `s12/CREDITS.md`,
  `s12/VERIFICATION.md` and `s12/verify.sh`.
- Certificates: all five above, `certificates/FORMAT.md`, `certificates/SHA256SUMS`,
  `certificates/s21/SHA256SUMS` and `certificates/rung2/README.md`.
- The whole `certificates/s32/` bundle except its two `SUMMARY.txt` files: the second
  cover, the bundle’s `README.md`, `SHA256SUMS` and `verify.sh`, both `zeromargin.py`
  run records (`manifest.json`, the per-root `roots.jsonl` and the checker file that
  ran), and the `zmcheck` sweep summaries.
- Checkers: `xcheck.py`, `verify/` and `verify2/` (Cargo files and `src/main.rs`),
  `search/zeromargin.py` and `search/zm_d4_sweep.py`.
- Lean: `lakefile.toml`, `lean-toolchain`, `lake-manifest.json`, `Sqpack.lean`,
  `Axioms.lean`, the six source files `Basic`, `Chord`, `Cover`, `D4`, `S32` and
  `ZeroMargin`, and `scripts/gen_s32_data.py`.
- Write-ups: `search/S32_EXACT.md`, `search/S21_LB.md`, `notes/lean-s32.md`,
  `notes/literature-s32.md` and `notes/s13-casefree.md`.

**Pinned by digest only**, each for a reason:

| Upstream path | Bytes | SHA-256 | Why not retained |
| --- | ---: | --- | --- |
| `s12/lean/Sqpack/S32Data.lean` | 439,352 | `d26cd11073aef59ebb411586cb3eed18cb37ce250eb770156b16ed43903f22cf` | Generated from the cover by the retained `gen_s32_data.py`, whose `--check` passed here |
| `s12/certificates/s32/zeromargin_d4/SUMMARY.txt` | 1,370,766 | `327b927349655e34c6eb2e1df69f76b6164115d8ddab7ebdf99209acc334b9ab` | Written by `zm_d4_sweep.py summary` from the retained `roots.jsonl` |
| `s12/certificates/s32/zeromargin_d4_shift_v1/SUMMARY.txt` | 1,370,813 | `c1a0fcdaec7cf34b7a2c2063b5e30fa7fe220d3e51e59fb5045273516411c889` | The same, for the second cover |
| `s12/certificates/s21/s21_lower_4.9950.json` | 134,050 | `ea0533bd9de328592f895174d223b58db3587485614de3b29a6980ebfdbfc9ca` | A `points.json` companion of the retained `.txt` |
| `s12/search/s32_sweep.py` | 10,273 | `44332d2bac2037312f5c0e1c2ea1fb5cf2ca89c2f8e2160f718b8fcb19b49232` | The `zmcheck` sweep runner, not run here; a summary string in it trips this repository’s embedded-JavaScript gate, whose allowlist is empty by policy |

**Omitted:** the rest of the repository — the Square Packing Atlas under `site/`, the
other `s(12)` certificates and branch leaves, the search tools and research notes under
`s12/search/` and `s12/notes/`, the rejection-test suites, `.github/`, and `.git/`.
The pinned commit and tree identify all of it.

**Licensing.** The code is MIT-licensed, and the source says so for the whole
repository. The source excepts the Atlas data under `site/www/data/`, derived from David
Ellsworth’s catalogue, which is not retained here.
Nothing retained here falls under that exception.

## Replay Here

Every command ran on 2026-09-27 from `s12/` of a scratch copy of the source tree at the
pinned commit, whose retained files are byte-identical to this packet’s, with outputs
written outside the packet. `python3` resolved to the project interpreter,
`packing/.venv/bin/python3`, CPython 3.14.7 with numpy 2.5.2; the source does not pin an
interpreter. The two Rust checkers were built from the retained sources with cargo
1.94.1 in about 30 s; the source’s own builds are not shipped (review finding F2).
The host is a four-core Linux container shared with other work, whose load average
ran between about 6 and 22, so every wall below is a contended reading, and
this lane held to two workers.
Each receipt under [`receipts/`](receipts/) opens with its command, interpreter, start
time, and closes with its exit status and wall.

| Check | Command, from `s12/` | Wall | Result |
| --- | --- | ---: | --- |
| `s(32)` bundle, fast | `certificates/s32/verify.sh` | 13 s | `s(32) bundle: OK`: every `SHA256SUMS` line, `S32Data.lean` equal to the cover, both shipped run records re-summarised to `D4 RECHECK CLEAN`, two germ roots re-run with identical census |
| `s(32)` full sweep | `zm_d4_sweep.py run --cert certificates/s32/s32_closed_cover_6.txt --depth 24 --nproc 2`, then again with `--deepen 30`, then `summary` | four legs; 9,429 CPU-s in all | `D4 RECHECK CLEAN`: all 7,200 roots certified, 164,130 boxes, maximum depth 27, every census identical to the shipped record; see below |
| `s(12)`, `N = 6000` | `verify/target/release/verify certificates/s12_lower_3.9686.txt 12 6000 2 0` | 256 s | `VERIFIED`, least covered weight `10000056/10⁷` at bin `k = 0` |
| `s(12)`, Python sample | `python3 xcheck.py certificates/s12_lower_3.9686.txt 6000 50 --n 12 -j 2` | 168 s | 50 of 2,486 bins, least `1250007/1250000` at `k = 0`, the same value |
| `s(21)`, `N = 6000` | `verify/target/release/verify certificates/s21/s21_lower_4.9950.txt 21 6000 2 0` | 1,459 s | `VERIFIED`, least covered weight `10000083/10⁷` at bin `k = 684` |
| `s(21)`, Python sample | `python3 xcheck.py certificates/s21/s21_lower_4.9950.txt 6000 684 --n 21 -j 2` | 69 s | bins 0, 684, 1368 and 2052, least `10000083/10⁷` at `k = 684`, the same value and bin |

Every minimum above equals the one the source records, at the same bin.
The sampled `xcheck.py` runs print `sampled bins only -- not a proof` and are recorded as
controls: the verdict on each positive-margin bound rests on the exhaustive `verify` run.

**A method-distinct decision of `s(12)`.** The source’s angle-net test is, row for row,
this repository’s parent-core theorem with parent side `1`: bin `k` is the row
`[k/N, (k+1)/N]` of parent half-tangents with core half-tangent `k/N` and core side
`σₖ`. `packing/devtools/verify_evand_angle_net_native.py` builds those 2,486 rows from
the certificate’s integers without importing source code, proves their premises exactly
with `validate_parent_core`, and decides coverage with the directed-rounding branch and
bound over centre boxes, `verify_parent_core_rows`, which shares nothing with the
source’s arrangement sweep. Run from `packing/` on clean commit `1f262c0d`, it accepted
every row at one unit, 23,409,578 boxes with no stalled box and no refutation, in 752 s
of summed row time on two workers
([`receipts/s12_native_parent_core.json`](receipts/s12_native_parent_core.json), with
its row journal). An earlier complete run, on a clean commit of this branch before its
history was rebuilt, gave the same status and the same 23,409,578 boxes.

**The `s(21)` native decision is an overnight item.** A complete run on a clean commit
of this branch, before its history was rebuilt, was started on 2026-09-27 and stopped by hand at 21:42 UTC, past this lane’s
1.5 CPU-hour budget, with rows 0 to 2,378 of 2,486 decided: every one certified at one
unit, 87,247,713 boxes, no stalled box and no exhausted budget, in 9,695 s of summed row
time on two workers. Its journal is not retained, so nothing here rests on it and
`s(21)` stays at `V4/C3`. The rows cost about 4 to 8 s each, against 0.2 to 0.6 s for
`s(12)`, so the whole run projects to about 2.8 CPU-hours, roughly 1.5 hours on two idle
workers. From `packing/`:

```sh
.venv/bin/python3 -m devtools.verify_evand_angle_net_native --case s21 --all --workers 2 --output OUT.json
```

It must print `PASS_COMPLETE`; `--resume OUT.rows.jsonl` continues an interrupted run
from its journal. A complete pass would give `s(21)` a second method, `V4/C4`, as it did
`s(12)`.

**The `s(32)` re-sweep is complete.** It ran with the same runner (`cc7fa8c7…`),
checker (`640fe453…`), certificate and settings as the shipped run, in four legs on
2026-09-27. The first, from a scratch copy of the source tree, was stopped by hand after
735 roots when the host’s load average passed 20. Its records seeded the other three,
which ran from `s12/` of this packet with one or two workers: two resumptions cut short
when their lane stopped, then a depth-24 pass over the remaining 5,895 roots (2.06
CPU-hours), a `--deepen 30` pass over the one root still open, and `summary`, which
printed `D4 RECHECK CLEAN`: all 7,200 roots certified, with the cover’s exact `D4`
invariance and both digests re-checked. The totals are the source’s: 164,130 boxes,
maximum depth 27, leaves ADM 12,201, CHAIN 70,007 and EMPTY 3,457, none uncertified.
The one root that needs depth 30, `x ∈ [1.5,1.6], y ∈ [0.5,0.6], u ∈ [0,1/16]`,
leaves one box at depth 24 and closes at 30, as in the shipped record.
All valid records took 9,429 CPU-seconds here, against the source’s 9,958.

[`receipts/s32_zeromargin_roots.jsonl.gz`](receipts/s32_zeromargin_roots.jsonl.gz) retains all
7,201 per-root records; its first 735 lines are the first leg’s, byte for byte.
`packing/devtools/compare_evand_s32_sweep.py` compares them with the source’s shipped
records ([`receipts/s32_sweep_comparison.json`](receipts/s32_sweep_comparison.json)):
every record carries the census of the source’s record of the same root at the same
depth, box for box and leaf for leaf, and none differs. The logs are
[`receipts/s32_zeromargin_partial_sweep.log`](receipts/s32_zeromargin_partial_sweep.log)
for the first leg and [`receipts/s32_zeromargin_sweep.log`](receipts/s32_zeromargin_sweep.log)
for the rest. The regenerated `SUMMARY.txt` is not retained; its digest is in the log.
This is a repository replay of the whole region, so the verified `n = 32` field stands
at `V4/C3`. It is the source’s program run again, one method, so it is not `C4`; see
[Routes to `C4`](#routes-to-c4-as-surveyed-on-2026-09-27).
To repeat it, from `s12/` with `OUT` outside the packet and the compressed files
restored ([Compressed Files](#compressed-files)):

```sh
python3 search/zm_d4_sweep.py run --cert certificates/s32/s32_closed_cover_6.txt --out OUT --depth 24 --nproc P
python3 search/zm_d4_sweep.py run --cert certificates/s32/s32_closed_cover_6.txt --out OUT --depth 24 --deepen 30 --nproc P
python3 search/zm_d4_sweep.py summary --out OUT   # must print D4 RECHECK CLEAN
```

It needs about 2.6 CPU-hours. The runner skips roots that already have a record in
`OUT`, so an interrupted run resumes.

**Not replayed here, and what each would take.** The commands are from `s12/`, with
`python3` the project interpreter and the compressed files restored; the CPU figures
are the source’s.

| Check | Command | Cost at the source |
| --- | --- | --- |
| `zeromargin.py` on the second cover | `python3 search/zm_d4_sweep.py run --cert certificates/s32/s32_shift_v1.txt --out OUT --depth 24 --nproc P`, then with `--deepen 30`, then `summary --out OUT` (or `certificates/s32/verify.sh --full` for both covers) | 2.42 CPU-h |
| `zmcheck --d4`, second cover | `ZM_MIXPAIR=1 python3 search/s32_sweep.py run --cert certificates/s32/s32_shift_v1.txt --out OUT --jobs J --threads T`, then `summary --out OUT` | 6.0 CPU-h |
| `zmcheck --d4`, Lean-transcribed cover | the same without `ZM_MIXPAIR` on `certificates/s32/s32_closed_cover_6.txt` | 80.2 CPU-h, 3,595 of 3,600 roots |
| Lean | `gen_s32_data.py` to regenerate `S32Data.lean`, then `cd lean && lake build && lake env lean Axioms.lean` against Mathlib `v4.33.1` | not stated; no Lean toolchain is installed here |
| `s(12)`, `s(21)` at `N = 12000` | `verify/target/release/verify CERT n 12000 T 0` | minutes to an hour |
| Exhaustive `xcheck.py` | `python3 xcheck.py CERT 6000 --all --n n -j J` | 5 min on 32 cores (`s(12)`); 87 min on 12 workers (`s(21)`) |
| `s(13)` case-free cover | `verify2/target/release/zmcheck cert certificates/rung2/s13_closed_cover_4.txt --depth 18 --threads T` | 34 min on 4 threads |

`search/s32_sweep.py` defaults to the source’s `runs/` path, so `--cert` is required, and
its default `--zmcheck` binary is `verify2/target/release/zmcheck`.

## Routes to `C4`, as Surveyed on 2026-09-27

`C4` asks for two complete repository decisions by different methods
([`epistemics.md`](../../../../epistemics.md#confirmation)). Two implementations of one
method stay at `C3`. This survey covers the certificates taken in on 26 and 27
September.

**Daniel’s `s(32)` closed cover: no native point-atom route.** The parent-core theorem
behind the `s(12)` decision proves a strict `s(n) > L` from cores strictly inside their
parents, and `s(32) > 6` is false. At side 6 the thirty-six grid cells are unit squares
with disjoint interiors, so their shrunken cores would each have to capture the
threshold `c`, and `36c ≤ 31.7135…` forces `c ≤ 0.881`, while excluding 32 squares
needs `32c > 31.7135…`, so `c > 0.991`. No threshold satisfies both. The point atoms
would load; the transfer theorem cannot apply. At any side `6 − ε` the route could
prove only `s(32) > 6 − ε`. A second method has to decide closed unit squares at margin
zero, with a boundary point counting. The interval engine never does that, since a site
on a tile edge is never surely inside a box’s core. Two candidates exist, neither built
or priced here:

- a first-party exact zero-margin checker that does not subdivide pose space; and
- a formalisation of the checker premise that the Lean top theorem leaves as a
  hypothesis. The primitives are already in `ZeroMargin.lean`.

`zmcheck` is a second implementation of `zeromargin.py`’s method, so it would add
assurance but not `C4`. It took the source 80.2 CPU-hours and left five roots open on
this cover.

**wand125’s and Tokoharu’s rectangle-density certificates: an area atom first.** They
stand at `C3` on complete replays of Tokoharu’s `verify.cpp`, the unchanged checker,
for wand125’s `n = 27` and `31` (`n = 28` by monotonicity; `n = 32` replayed but
superseded) and for Tokoharu’s own certificates at `n = 11`, `26` and `29`. Their construction is the same
shrunken-core angle net (`B < 1`), so the parent-core transfer carries over. What the
native engine lacks is a rectangle atom: a rectangle contributes its density times the
area of its intersection with the core, and a box needs a directed-rounding lower bound
on that clipped area. The engine carries only point and threshold atoms, so the atom,
its review and the cost are all unbuilt and unpriced. The `C3` replays of the other 41
standing wand125 certificates come first. They are an overnight item of about 102
CPU-hours by the upstream per-angle times, run from `packing/` with
`.venv/bin/python3 -m devtools.audit_wand125_rectangles --out resources/web/wand125-rectangle-certificates-2026-09-27/receipts/replay --resume --replay --workers 2`
and then `devtools.apply_wand125_rectangles`.

**Kleddamag’s `s(17) > 4.640020` and `4.66001`: BC-393.** Both stand at `C3` on two
implementations of one exact event-cell sweep. The native route needs three things:

- a loader for the schema’s `sets`, `coefficients` and `winning_masks`;
- a winning-subset atom in the parent-core and interval routes, taking masks on up to
  12 sites, with its capacity-one lemma reviewed; and
- a lift of the frozen site ceiling to at least 20,856 sites.

The 2026-09-27 review of `4.66001` puts the run at 2,168 rows and about 2 to 12
CPU-hours on two workers. A `C4` rating of `4.640020` would be superseded on arrival, so
BC-393 aims at `4.66001`.

## Retrieval Hashes

The certificates’ digests, which the source also pins in its own `SHA256SUMS` files.
They are digests of the upstream bytes; all the certificates but `s11_lower_3.8143.txt`
are stored compressed ([Compressed Files](#compressed-files)).

| File | SHA-256 |
| --- | --- |
| `s12/certificates/s32/s32_closed_cover_6.txt` | `a0d2d38fc9a585a166b9e06c5069fdae9bdce44ca9fb64dda75abcc99e3c2144` |
| `s12/certificates/s32/s32_shift_v1.txt` | `7598d39a899adbdd2352d8054d98cb3e8818e4e4cd9c7a23830795a8f9847793` |
| `s12/certificates/s12_lower_3.9686.txt` | `75f1cc891a8b8739b92b50c7ddbd85a493efa58cf2e921d58ce4ac7c2dcabe78` |
| `s12/certificates/s21/s21_lower_4.9950.txt` | `c8e8f878205f2da9c213e4a87c06f17c5a759dce7e695e676dd5c50e0994f2ef` |
| `s12/certificates/s11_lower_3.8143.txt` | `0b716e4079b07d333a42412021c970a97c861b933a76261a26cfe63841c55ac9` |
| `s12/certificates/rung2/s13_closed_cover_4.txt` | `ea303acea08cc17a13cecc24d3714c2df409f91eba048cd5546050ed064b53ed` |
| `s12/search/zeromargin.py` | `640fe453c1a32f4aa580ca2b1261c6406923a4d7c131f65604a432c7fc2086ab` |
| `s12/search/zm_d4_sweep.py` | `cc7fa8c70f7a39c5e1e920baa9efdc1af8feb68bc6eeb029dab4a99fc3f77fbe` |

## Compressed Files

Nine data files of more than 1,000 lines: seven upstream files, the five certificates
and the two shipped `zeromargin.py` run records, and two of this packet’s receipts,
the `s(12)` native row journal and the `s(32)` re-sweep records.
Each is stored as deterministic gzip made by `gzip -9n`, with no file name or timestamp
in the header, following the [R052 packet](../n17-guzhou-r052-2026-09-25/README.md).
The table gives the Git blob and SHA-256 of the decompressed bytes, which for an
upstream file are its blob and digest at the pinned commit and for a receipt are the
bytes this repository wrote.
The repository’s readers take the upstream path and decompress transparently through
`devtools.retained_data.read_retained_bytes`, and
`python -m devtools.retained_data check PACKET` (run by
`packing/tests/test_retained_data.py`) re-derives every row.
The seven upstream digests are the ones [`retained-files.sha256`](retained-files.sha256)
and the Retrieval Hashes list. The source’s `SHA256SUMS` files, `verify.sh` scripts,
`zm_d4_sweep.py` and Rust checkers read the plain files.

Before running any of the source’s own programs on this packet, restore the exact
upstream tree from the repository root:

```sh
find packing/resources/web/evand-square-packing-2026-09-26 -name '*.gz' -exec gunzip -k {} +
```

The restored plain files are untracked, so remove them afterwards; while both copies
are present, the repository’s readers require them to agree.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `receipts/s12_native_parent_core.rows.jsonl.gz` | receipt | `aaaf1b72f172e3c3fa97761e6dfc3eab2539e975` | `2dd7388ea9e054da8129b73bbc5da282d624403c6d4a62e9dd82a32b873dbc40` |
| `receipts/s32_zeromargin_roots.jsonl.gz` | receipt | `1003ccf426a47c80e44c272bdc93914648fd906a` | `16366bb7637c0d114667df2a9df7b5913a5b6714af5023287326c57ba47a4e0e` |
| `square-packing/s12/certificates/rung2/s13_closed_cover_4.txt.gz` | upstream | `f5da1b112e08bc6d81db63a7aa6ae2530099677c` | `ea303acea08cc17a13cecc24d3714c2df409f91eba048cd5546050ed064b53ed` |
| `square-packing/s12/certificates/s12_lower_3.9686.txt.gz` | upstream | `4c3f0bb3b2607ad037086e1183324eb4fb7a8d68` | `75f1cc891a8b8739b92b50c7ddbd85a493efa58cf2e921d58ce4ac7c2dcabe78` |
| `square-packing/s12/certificates/s21/s21_lower_4.9950.txt.gz` | upstream | `9718ac85cac9bf3c9d0e7e7cb380f30689aace58` | `c8e8f878205f2da9c213e4a87c06f17c5a759dce7e695e676dd5c50e0994f2ef` |
| `square-packing/s12/certificates/s32/s32_closed_cover_6.txt.gz` | upstream | `ece6239cd96f89c9249a2dd62d5736b2981d647f` | `a0d2d38fc9a585a166b9e06c5069fdae9bdce44ca9fb64dda75abcc99e3c2144` |
| `square-packing/s12/certificates/s32/s32_shift_v1.txt.gz` | upstream | `3c3a7b05b2175246edb7390014126dd41d0c82b5` | `7598d39a899adbdd2352d8054d98cb3e8818e4e4cd9c7a23830795a8f9847793` |
| `square-packing/s12/certificates/s32/zeromargin_d4/roots.jsonl.gz` | upstream | `5cc2c5ad92b53e4f3f7aa20081b9bdbfc95585c6` | `a4feedde1d25335f2c554286fefb76acb2d228664361d6c023fa566082abfb1a` |
| `square-packing/s12/certificates/s32/zeromargin_d4_shift_v1/roots.jsonl.gz` | upstream | `47353f41debc7ee8d89465bc0a83346c7870a9bb` | `04261c4f85140b7062e592884d8a10f4e4bcbd72f1496173eb1c060ed3a0abbc` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
