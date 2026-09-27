# Guzhou0806’s R052 Continuation for `s(17)`, Retrieved 2026-09-27

A publication record for Guzhou0806’s continuation of R052, which claims
`s(17) > 462003/100000 = 4.62003`. It is numerically superseded by Kleddamag’s public
`232001/50000 = 4.64002` of 26 September 2026, so it is kept on the precedent the
[R052 packet](../n17-guzhou-r052-2026-09-25/README.md) set for R042, R043 and R050: the
publication record, not the package.
Its new C++ entry was cheap enough to run once here, and the receipts are kept beside
the record.

Retaining it registers no result, moves no bound and makes no review.

## Provenance

| Field | Value |
| --- | --- |
| Source | <https://github.com/Guzhou0806/n17-square-packing> |
| Commit | `6f64e4b206374bd609a0c1a517d5d51d9397dc9c`, `main` at retrieval |
| Tree | `299014b94e1cb0d3f7e11a2d68347047190efca3` |
| Committed | 2026-09-25T16:50:31Z (2026-09-26 00:50 in the author’s `+08:00`) |
| Retrieved | 2026-09-27 |
| Package | `certificates/R052-4.62003/`, 28 files; `MANIFEST.json` `2cdc6f04…2824` |
| Certificate, gzip | `8d19a1c4b7efa911857e9587d6bd18a1c46f1ded5e7e3eada6d5d267fd6b0bca` |
| Certificate, decompressed | `74d884cbb1f9ca0c9684bb940ecd13781db53e6efe7a775d852e15ba618aafe3` |
| Upstream CI | [run 36163391871](https://github.com/Guzhou0806/n17-square-packing/actions/runs/36163391871), all three jobs green, the native job included |

The commit adds the package beside R052’s; `certificates/R052/` is byte-unchanged
between `3bf1095c` and `6f64e4b2`.

**Credit, as the source states it.** The continuation is “produced by Guzhou0806 / N17
project with AI assistance”, continues Kleddamag’s public mixed-certificate
architecture, and was accepted upstream by non-proposer AI review, with no claim of
human peer review, formal proof, priority or optimality.
It repeats R052’s report that Kleddamag holds an unpublished internal `4.62001`.

## The claim

$$
s(17) > \frac{462003}{100000} = 4.62003
$$

The container side stays `L = 4613/1000`; the parent side becomes `A = 461300/462003`.
R052’s sites are moved by `δ/2` toward the nearest wall, with
`δ = 230650/231001 − 461300/462003`, midlines fixed and the other half reflected, so the
resources, `D4` orbits and weights are R052’s own.
Two rows are split four ways, taking R052’s `15,721` rows to `15,727`.

| Quantity | Exact value |
| --- | ---: |
| Total budget `M` | 16990246659579 units of `10⁻¹²` |
| Minimum core charge `Γ` | 999426274093, at rows 15560, 15561 and 15562 |
| `17Γ − M` | 2 units |
| Strict containment inequalities | 62,908, least margin `4613/9240060000000000000` |
| Sites / threshold groups / columns | 18,585 / 4,504 / 2,922 |

`M` and `Γ` are R052’s exactly, so the slack is again only integer rounding.

## What Is Retained, and What Is Not

**Retained byte-identical** under `n17-square-packing/`, at their upstream paths, each
equal to its blob at the pinned commit by `git hash-object`:

| File | Git blob | SHA-256 |
| --- | --- | --- |
| `R052_4p62003_PUBLICATION.json` | `2b36f12f` | `d1fcb33fd97ee4cbec7b64ba89383664663cfb37ba207c6cda91e8f1f0181d92` |
| `verification/R052_4p62003.json` | `0f1dc51d` | `54a14d6f018805e648fe75a1c08344c77b2e43df2904abc3497a405cbcc30fcc` |

The publication record lists the size and SHA-256 of all 39 files the commit adds or
changes, the whole package included; the validation record is the source’s own account
of its Python, BigInt and C++ full runs.

**Not retained:** the package itself, including the `1.2 MB` certificate, the C++ and
Python sources and the BigInt ledger.
The pinned commit and the publication record’s digests identify every byte.
That follows the R042, R043 and R050 precedent for a superseded release.

## Replay Here

Every command ran on 2026-09-27 from the root of a clean clone of the source at
`6f64e4b2`, outside this repository, with outputs in a scratch directory that is not
retained.
The host is a shared Linux container with four cores, running other work at the
same time, so the walls are contended readings.
The interpreter is the project’s CPython 3.14.7; the compiler is Ubuntu’s `g++` 13.3.0
with the distribution’s Boost 1.83 headers.
[`receipts/replays.json`](receipts/replays.json) records each command, start, wall and
exit, and each mode’s directory keeps the source’s own `RESULT.json`, `INPUT.json` and
console output.

```sh
python -X utf8 -B -S certificates/R052-4.62003/verify.py --output OUT/r052c-records
python -X utf8 -B -S certificates/R052-4.62003/verify.py --containment --output OUT/r052c-containment
python -X utf8 -B -S certificates/R052-4.62003/verify_native.py --jobs 1 --output OUT/r052c-native
```

| Mode | Wall | Exit | Status | What it establishes |
| --- | ---: | ---: | --- | --- |
| records | 0.23 s | 0 | `PASS_R052_RECORDS` | Package manifest `2cdc6f04…2824`, certificate identity, the frozen ledger and its per-row minima; no geometry |
| containment | 2.57 s | 0 | `PASS_R052_CONTAINMENT` | Resource closure, budget, and 62,908 endpoint containment inequalities, least margin `4613/9240060000000000000` |
| native-full | 2,358 s | 0 | `PASS_R052_NATIVE_FULL` | Fresh exact centre minimum for all 15,727 rows through the compiled C++ kernel, each equal to the shipped BigInt ledger |

The native mode compiles `src/native_exact.cpp` itself (the build printed nothing),
recomputes every row’s exact centre minimum through the compiled kernel, and requires
each to equal the row of the shipped BigInt ledger before it writes a result.
At one job it took 39 minutes of contended wall; the source’s own run took 6.5 minutes
at four jobs on Windows.

The fresh C++ row ledger has SHA-256 `869596b3…a5f6`, byte-identical to the
`fresh_rows_sha256` of the source’s native run under MinGW `g++` 16.1 on Windows, so two
compilers on two platforms agree on every row’s minimum and cell counts.
The global minimum `999426274093` falls only on rows 15560, 15561 and 15562, as the
source says; the next row is `14,902,677` units above it.

The Python and BigInt full modes were not run here: they are the modes whose method this
record already holds for R052, and the continuation carries no bound.

## What the C++ Replay Does and Does Not Add

The kernel is an exact rectangle-event sweep with a lazy segment tree over rotated
integer coordinates, using Boost’s arbitrary-precision integers for geometry and `int64`
for charges under a checked `2⁵⁰` mass bound.
The row parameters, legal-centre polygon and site table are built by Python adapters
whose five geometry functions the source says are extracted unchanged from its Python
checker, and the `k`-of-`m` groups are expanded into subset rectangles the same way.
The source itself says the C++ and Python paths “share geometric construction lineage
and are not two fully independent proofs”.

So it is a third implementation of the same exact event-cell method, not a
method-distinct decision.
It could not raise R052 from `C3` to `C4` even in principle: it decides this
continuation’s certificate, not R052’s, and the rung needs a check that fails
differently, such as this repository’s interval branch and bound, which refuses R052 at
its engine ceilings.
Both certificates are in any case below Kleddamag’s `4.64002`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
