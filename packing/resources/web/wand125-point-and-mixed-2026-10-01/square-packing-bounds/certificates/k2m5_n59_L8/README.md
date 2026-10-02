# s(59) = 8 (computer-assisted; not yet independently reviewed)

Let `s(n)` be the least side of a square that holds `n` non-overlapping unit squares with
arbitrary orientations. This directory contains a measure certificate for

```
s(59) >= 8,   hence   s(59) = 8   (the 8x8 grid packs 64 >= 59 squares).
```

This is the case `k = 8` of the `k^2 - 5` series. `s(60) = 8` (the case `k = 8` of the `k^2 - 4` series)
is due to Evan Daniel; with this certificate the value of `s(59)` is settled as well.
The previous best lower bound for `s(59)` was `793/100 = 7.93`.

**Status.** The certificate passes three sweeps by two independently written checkers, listed below.
It has not been reviewed by anyone outside this project and has not been formalised in Lean.

## The argument

`n59_mixed_cover_8.txt` defines a finite nonnegative measure `mu` on the container `[0,8]^2`.
It uses Evan Daniel's "mixed 1" format: point masses plus axis-parallel segments, each segment
carrying its mass uniformly along its length. The certificate needs two facts:

1. Every closed unit square (any position and orientation) inside `[0,8]^2` has `mu >= 1`.
2. The total mass is `1474762899 / 25000000 = 58.99051596 < 59`.

In a packing of 59 unit squares in a square of side `L < 8`, scale the packing up to side 8.
The squares get larger, so each enlarged square contains a closed unit square with mass `>= 1`.
The enlarged squares are interior-disjoint, so the total mass would be `>= 59`, a contradiction.
Hence `s(59) >= 8`.

The cover is invariant under the dihedral group D4 of the container. Exact invariance is checked
by `zmx2 d4` (and also by the cover reader). The `--d4` sweeps rely on this invariance; the
`zmx2 --full` sweep does not.

- Points: 26,308
- Segments: 5,240 (length `1/50`, on the 14 interior lattice lines `x, y in {1, ..., 7}`)
- Coordinate unit: `1/D = 1/1000`
- Weight unit: `1/W = 10^-8`
- SHA256: `6f4d2b64f9a88ae49546f05fa28752382f9ebfa8b7f8b6e6c6f1a8e693177e19`

## Construction

The cover was produced with Evan Daniel's line-cover linear program (`s12/search/line_cover.py` in
[evand/square-packing](https://github.com/evand/square-packing), MIT licence), run unchanged in
substance at container side 8, i.e. the recipe of his `s(60) = 8` cover, but pushed further:

1. **Columns and warm start.** Point columns on a `0.05` lattice plus the support of Evan Daniel's
   `s(60)` cover (`s12/certificates/s60/s60_mixed_cover_8.txt`, SHA256
   `2d0e456ea86cceeadc92d9f8fa7d468ba570a16d00d7343ebfbfb0b3b3b12a41`); segment columns of length
   `1/50` on the interior lattice lines. Initial rows from the poses where that cover is tightest, the
   tile-germ family and a uniform family of poses.
2. **Cutting-plane rounds** (his phase A: lattice separation, polishing, point pricing). After a cloud
   preemption the run was restarted from its round-5 cover, with the poses that `zmx2` could not
   certify on the round-4 and round-5 covers added as permanent rows. The restarted run used a local
   copy of `line_cover.py` that only adds saving the row set each round and reading extra rows from a
   file between rounds; the LP model is unchanged.
3. **Exact threshold.** For each round cover, the smallest scale factor `f*` at which `zmx2 --d4`
   verifies it was found by bisection. The LP value saturated near `58.435` and `f*` near `1.0086`, so
   `58.435 * 1.0086 < 59` with a little room.
4. **Scaling.** The round cover (LP value `58.4352`, `f*` in `(1.0085157, 1.0085938]`) was multiplied by
   `2019/2000 = 1.0095`, weights rounded up on the unit `10^-8`. The margin over `f*` is about `0.09 %`.

The first comment line of the cover file is a working note; it is kept so that the file hash matches
the hashes recorded in the logs and manifests.

## Checks

All sweeps were run on the file in this directory (same SHA256). Logs are included.

| check | command | result | roots | uncertified | time |
|---|---|---|---|---|---|
| zmx2, D4-reduced | `zmx2 cert COVER --d4` | `VERIFIED-D4` | 6,400 | 0 | 123 s wall / 243 s CPU, 9,844,124 boxes |
| zmx2, unreduced | `zmx2 cert COVER --full` | `VERIFIED` | 51,200 | 0 | 981 s wall / 1,944 s CPU, 79,108,328 boxes |
| zm_mixed, exact rationals, depth 24 | `zm_mixed.py cert COVER --d4 --cert-mode --disj --chain-from 0 --depth 24 --pitch 1/20 --ubins 16` | 6 boxes uncertified, all in one root `R` | 102,400 | 6 | 76,108 s wall / 455,030 s CPU (6 processes), 1,514,784 boxes |
| zm_mixed, the root `R` alone, depth 34 | same, plus `--depth 34 --cx-lo 27/20 --cx-hi 7/5 --cy-lo 13/10 --cy-hi 27/20 --u-lo 1/4 --u-hi 9/32` | `VERIFIED-D4 (PARTIAL)` | 1 | 0 | 3,259 s, 13,767 boxes, max depth 26 |

Here `R = [27/20, 7/5] x [13/10, 27/20] x {u in [1/4, 9/32]}` (`theta = 2 arctan u`, about `28.1°`-`31.4°`).

- **zmx2 sweeps.** `zmx2` is a Rust checker that encloses chord endpoints in floating-point intervals.
  The unreduced sweep checks every root without using the symmetry.
- **zm_mixed sweeps.** `zm_mixed.py` works in exact rational arithmetic, with the settings Evan Daniel
  used for his `s(60)` mixed cover. Because the margin is thin (`0.09 %` over `f*`), its depth limit 24
  was not enough in one root of the D4 region: the depth-24 run certifies the other 102,399 roots and
  lists 6 uncertified boxes, all inside `R`. A second run of the same checker, restricted to `R` and
  with depth limit 34, certifies `R` with no uncertified box (it needed depth 26). Together the two runs
  cover the whole D4 region. The depth-24 run's own verdict line therefore reads `NOT VERIFIED`; that
  is expected, and `verify.sh --zm` checks that its 6 boxes lie in `R`.

The logs were written on cloud machines; the paths in them are those machines' working directories.

Logs:
- `zmx2_d4/run.log`
- `zmx2_full/run.log`
- `zm_mixed_d4/run.log`, `zm_mixed_d4/manifest.json` (all roots, depth 24)
- `zm_mixed_root/run.log`, `zm_mixed_root/manifest.json` (root `R`, depth 34)

Each manifest records the SHA256 of the input and of the three checker files.

### Checkers used (not bundled)

Both checkers are Evan Daniel's, from [evand/square-packing](https://github.com/evand/square-packing)
(MIT licence, see `s12/LICENSE` there). They are not copied here. `verify.sh` fetches them at the
pinned commit `b91d70b6ed314624c1434b628a9c7bf9a132c743` and checks these SHA256 values:

| file | SHA256 |
|---|---|
| `s12/verify2/src/bin/zmx2.rs` | `6b7f0f79466bf25c9a85f8fe2f3866de734935f0521ea188136818c2fb5b3fed` |
| `s12/search/zm_mixed.py` | `ee3e2915349b8795128417bca6414b205d526db9f01f88cd4cd32c32e8d760ac` |
| `s12/search/mixed_cover.py` | `bb89de15ecf5821dd7e1a36ebab8a50d792a406b7fb0f5cb38059f99ef74aae5` |
| `s12/search/zeromargin.py` | `640fe453c1a32f4aa580ca2b1261c6406923a4d7c131f65604a432c7fc2086ab` |

Later upstream commits change `zmx2.rs` and `zm_mixed.py`. Use the pinned commit.

`zmx2` needs Rust 1.86 or newer to build.

## Reproducing

Requirements:
- `git`;
- Python 3 with `numpy`;
- Rust >= 1.86 (`cargo`; set `CARGO=...` to pick a toolchain).

```sh
sh verify.sh /path/to/new/workdir 8             # hashes, exact total, D4, zmx2 --d4
sh verify.sh /path/to/new/workdir 8 --full      # also zmx2 --full
sh verify.sh /path/to/new/workdir 8 --zm        # also both zm_mixed runs (about 127 CPU-hours)
```

`verify.sh` does the following, in order:
1. checks `SHA256SUMS`;
2. clones the upstream repository and checks out the pinned commit;
3. checks the checker hashes;
4. computes the exact total with the upstream reader and asserts that it is `< 59`;
5. builds `zmx2` and checks D4 invariance;
6. runs the requested sweeps and checks their summaries.

For the zmx2 sweeps it also checks that the per-root log has exactly the expected number of
distinct roots, each with `uncert 0` and `capped 0`.

It prints `N59_COVER_VERIFIED` only if every step passes.

## Files

| file | content |
|---|---|
| `n59_mixed_cover_8.txt` | the cover (mixed 1 format) |
| `verify.sh` | reproduction script |
| `zmx2_d4/run.log` | zmx2 `--d4` sweep log |
| `zmx2_full/run.log` | zmx2 `--full` sweep log |
| `zm_mixed_d4/run.log`, `zm_mixed_d4/manifest.json` | zm_mixed sweep over all roots, depth 24 |
| `zm_mixed_root/run.log`, `zm_mixed_root/manifest.json` | zm_mixed sweep of the root `R`, depth 34 |
| `SHA256SUMS` | hashes of the files above |

## Attribution

This result is built directly on Evan Daniel's work:
- the linear-program recipe (`line_cover.py`), the cover format and both checkers are his
  ([evand/square-packing](https://github.com/evand/square-packing), MIT licence);
- the warm start and part of the column set come from his `s(60) = 8` cover.

The decision to apply the recipe to the `k^2 - 5` case, the additional rounds that brought the
exact threshold below `59 / LP`, the restart with `zmx2`-uncertified poses as rows, and the runs
recorded here are ours.
