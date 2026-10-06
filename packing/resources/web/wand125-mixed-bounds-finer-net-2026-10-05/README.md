# wand125 Mixed-Rectangle Certificates of Later 5 October 2026, Pinned at `43050ed`

This packet pins the two certificate directories that
[wand125/square-packing-bounds](https://github.com/wand125/square-packing-bounds) added
on 5 October 2026 after the [morning packet’s](../wand125-mixed-bounds-2026-10-05/README.md)
pin `a541afb`:

- `mixed_n66_L843`, for $s(66) \ge 843/100$, posted in a comment on
  [jlevy/squares#282](https://github.com/jlevy/squares/issues/282#issuecomment-5990620723);
- `mixed_n18_L470`, for $s(18) \ge 47/10$, registered in its own issue,
  [jlevy/squares#366](https://github.com/jlevy/squares/issues/366).

Both are rectangle-density lower bounds of the kind and checker of the earlier mixed
certificates. `mixed_n18_L470` is the source’s first on a net of its own: core side
$B = 999/1000$ and 416 half-angle tangents of step $1/1001$, where every earlier mixed
certificate has $B = 9977/10000$ and the standard net of 201 tangents of step
$83/40000$. Its proposed Frontier key is **[wand125 mixed bounds finer net 2026-10-05]**.
The claims below are stated as the source states them.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/wand125/square-packing-bounds> |
| Revision | `43050edc5bdf5116fc5a073283128edd6749946b`, branch `main`, tree `4acb80ac0575403194e1c55c61a442aae2d19f81`; the head when retrieved, and the revision #366 names |
| Committed | 2026-10-05T09:21:25Z |
| Author | wand125, building on Tokoharu’s format and verifier, as for the other mixed certificates |
| Licence | MIT. The root `LICENSE` reads “Copyright (c) 2026 wand125” and is byte-identical to the [September 27 packet’s copy](../wand125-rectangle-certificates-2026-09-27/wand125-rectangles/LICENSE) |
| Retrieved | 2026-10-05T17:10Z: a blobless clone of the whole history, checked out sparsely at this revision. `git ls-remote` listed one branch, `main` at this revision, and no tag |
| Pinned subtree | 35 files, 40,621,100 bytes: the two claim directories and the three root files, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) |
| Retained here | 9 files, 536,631 bytes upstream, under [`square-packing-bounds/`](square-packing-bounds/), byte-identical to the pinned files after decompression |

**The revisions.** The source’s `main` moved from `a541afb`, the morning packet’s pin,
through two commits, each adding one certificate directory and one section of the root
README:

| Claim | Directory | Commit | Request |
| --- | --- | --- | --- |
| $s(66) \ge 843/100$ | `certificates/mixed_n66_L843` | `d73ce20d6650b333f299daf348ac179399190c10` | [#282, 08:11:44Z](https://github.com/jlevy/squares/issues/282#issuecomment-5990620723) |
| $s(18) \ge 47/10$ | `certificates/mixed_n18_L470` | `43050edc5bdf5116fc5a073283128edd6749946b`, 09:21:25Z | [#366, 09:22:35Z](https://github.com/jlevy/squares/issues/366) |

`mixed_n66_L843` is unchanged at the pin since `d73ce20`: its directory has the tree
`00c62d27717dbce989372514f89560a8946b3abe` at both commits. The intake pass of 5
October read `d73ce20` and held it for this import (bead `think-4qit`).

## Credit and AI Assistance, as the Source States Them

The root README at the pin is retained. Between the two pins it gains one section per
certificate and nothing else, so its Attribution section still opens “The method is not
ours.”, crediting Walter Stromquist, Hiroshi Nagamochi, Sam Burns, Gustavo Massaccesi
and this repository, and its Status section still says “Parts of this work were produced
with AI assistance under human direction.”

- **The two certificates.** Each directory README calls the checker “the verifier
  shipped here, `code/mixed_rotated_verify.cpp`”, the same checker as for
  `mixed_n87_L939` and `mixed_n65_L835`. Each says the certificate is not in Tokoharu’s
  format because its least oblique bound is below the $1.0001$ his `verify.cpp`
  requires. Each says the candidate was built from scratch at its side from a structured
  initial measure (“bands at integer distances from the walls”) and repaired against
  counterexamples on the full net.
- **The finer net.** `mixed_n18_L470`’s README and #366 state the argument: “D4 symmetry
  reduces orientations to `[0, π/4]`, and `B(1 + 1/1001) < 1`. So every unit square, at
  any orientation, contains a closed core of side `B` at a net angle, strictly in its
  interior.”
- **The pre-publication replays.** Each README says the full replay was run again from
  the tarball on a fresh Ubuntu 24.04.5 machine with g++ 13.3.0, Python 3.12.3 and NumPy
  2.5.3, after checking the tarball’s SHA-256 and all its file hashes. The `mixed_n18_L470`
  bundle’s own `bundle.json` records the run that made it on macOS 26.2 (arm64) with
  Python 3.14.7 and NumPy 2.5.3. This was not checked.
- **#366’s second check.** The issue reports a copy of this repository’s `sqverify_fast`
  “changed in one place to read the declared proof net”, verifying all 416 directions,
  with corrupted net declarations refused and the masses scaled by $0.985$ refused in
  five directions. The patch was not requested; this repository’s change was written
  apart from it ([`sqverify_fast/INDEPENDENCE.md`](../../../sqverify_fast/INDEPENDENCE.md)).

## What Is Retained

Retained byte-identical at their upstream paths: the root `README.md`, and from each of the
two claim directories `README.md`, `candidate.json`, `certificate.json` and
`manifest.json`.

Pinned by digest only:

| Upstream path | Bytes | SHA-256 |
| --- | ---: | --- |
| `LICENSE` | 1,064 | `c0dd43e7892932c81335f74a2fdbf1a98f5977bab14c0c4c30e3abcc97c34904` |
| `.gitignore` | 132 | `0a31c24fe622ff8b4b012fbf790686063a84da3dd306d47e7283aad434653308` |
| `certificates/mixed_n66_L843/n66-L8.43-proof-bundle.tar.gz` | 29,342,935 | `be0b8476ce0c2a886a1ff30a04c6301e084d826b9bce18584ac654ffffcf9ce2` |
| `certificates/mixed_n18_L470/n18-L4.7-proof-bundle.tar.gz` | 10,663,098 | `6c30eb7337e622371c865f5be9c52609ec319c39728784b5f6d9e1e342111873` |

`LICENSE` is retained byte-identical by the September 27 rectangle packet; a retained
`.gitignore` would act on this repository’s tree. Each tarball is a complete proof bundle,
and each digest is the one its directory’s README states. Each directory’s ten `code/`
files and its `requirements.txt` are byte-identical to the files of the same name in
`mixed_n50_L740/`, which the
[September 28 packet](../wand125-point-and-mixed-2026-09-28/README.md) retains, and are
pinned by digest in the subtree list. So `mixed_n18_L470` is decided by the same driver
and the same checker, `89b674a6…`, as every earlier mixed certificate. Its net is not
built into them; the candidate declares it. Neither directory carries a
`completion-audit.json` at the pin.

[`acquisition/declaration.json`](acquisition/declaration.json) declares the scope and the
pinned-only rules, and [`acquisition/sources.json`](acquisition/sources.json) records the
pin and every pinned-only file with its size, digest, reason and, where one exists, the
retained copy with the same bytes.
From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source \
  wand125-mixed-bounds-finer-net-2026-10-05 --checkout CHECKOUT
```

rebuilds the retained files and both acquisition files from a checkout at the pinned
revision, and with `--check` in place of `--checkout CHECKOUT` re-derives the packet from
its manifest without one.

## The Claims, as the Source States Them

| Name here | Claim | Rectangles | Core $B$ | Net | Source’s comparison, in its README | Least oblique bound recorded (index) | Axis cells, minimum |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| `n66-L843` | $s(66) \ge 843/100$ | 713 | $9977/10000$ | step $83/40000$, 201 nodes | its earlier `mixed_n66_L842` (8.42), and Green’s reported 8.2900… | $1.0000000007136982$ (157) | 21,622,500, $1.0051859714394813$ |
| `n18-L470` | $s(18) \ge 47/10$ | 136 | $999/1000$ | step $1/1001$, 416 nodes | its rectangle certificate `rect_n18_L4695` (4.695) | $1.000000000165181$ (161) | 725,904, $1.0174496711115353$ |

The source’s READMEs round two figures up: `mixed_n18_L470`’s gives its least oblique
bound as “1.0000000002” for the $1.000000000165181$ its certificate records, and
`mixed_n66_L843`’s gives Green’s value as “8.2900…” for $2\sqrt 2 + 71/13 =
8.2899656\ldots$ (finding DN-9 of the
[5 October review](../../../../docs/project/reviews/review-2026-10-05-wand125-declared-net-n18-n66.md)).
The records here cite the exact values.

Both are rectangle densities with no point mass: each `candidate.json` has an empty
`points` list and a `scaling_factor` of `1`. Each has total mass $n - 1/100000$ and
coverage threshold $1$. Each `certificate.json` has status
`ALL_ANGLES_VERIFIED_AND_REPLAYED`, with an `ANGLE_RESULT_REPLAYED` record at every
oblique node and `AXIS_CERTIFICATE_REPLAYED` at the axis.

`mixed_n18_L470`’s candidate declares its net as `"proof_net": {"step": "1/1001",
"last": 415}`. Its `manifest.json` and `certificate.json` restate it with the containment
facts:

- the last tangent is $415/1001$, and $t^2 + 2t - 1 = 1054/1002001 > 0$ there, so the net
  reaches past $\tan(\pi/8)$;
- $B(1 + D) = 500499/500500$, a margin of $1/500500$ below $1$.

[`sqverify_fast/SOUNDNESS.md`](../../../sqverify_fast/SOUNDNESS.md#declared-nets), lemma
N0, proves that these premises carry the argument to a declared net, with the per-bin
centre domain at the declared half-step $1/2002$.

## The Exact Audit and the Pre-Replay Checks

**`n66-L843`.** From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_point_and_mixed \
  mixed-audit wand125-mixed-bounds-finer-net-2026-10-05 --check
```

recomputes [`receipts/mixed-audit.json`](receipts/mixed-audit.json) from the retained bytes,
with the checks the [4 October packet](../wand125-mixed-bounds-2026-10-04/README.md)
describes, and passes. Its side exceeds Green’s DS7 value at $n = 66$ (Theorem 9,
$k = 8$, from $n = 65$, enclosed to 60 digits) and Nagamochi’s $1 + \sqrt{51}$.
`mixed-fetch` on the pinned tarball found the pinned SHA-256 and size, and all 621
entries of `files-sha256.json` matching with nothing unlisted. The unpacked candidate,
certificate, manifest and `code/` are the retained or `mixed_n50_L740` files, and the
shipped driver’s preconditions hold. Every one of the 200 oblique inputs encloses the
exact candidate recomputed here, and every record is `ANGLE_VERIFIED` with an empty
frontier at $\gamma = 1$. Its output is
[`receipts/n66-L843/fetch.json`](receipts/n66-L843/fetch.json).

**`n18-L470`.** The audit tool takes the standard net and core $9977/10000$ as fixed, so
no row of it names this certificate. Its exact premises are decided by the admission of
this repository’s clean-room verifier, `sqverify-fast`, which reads the declared net and
checks every premise of lemma N0 in exact rationals:

- the mass is exactly $1799999/100000 < 18$, with every row a nonnegative mass on a
  nondegenerate rectangle inside $[0, 47/10]^2$;
- the declared net reaches past $\pi/4$, and its last tangent is at most $1/2$;
- $B(1 + D) < 1$, and so is format M’s tangent form.

The pinned tarball has the pinned SHA-256 and size. All 1,266 entries of its
`files-sha256.json` match, and nothing is unlisted. Its `proof/candidate.json`,
`proof/certificate.json` and `proof/manifest.json` are byte-identical to the retained
files; its ten `code/` files are the `mixed_n50_L740` copies; and its `proof/verify.cpp`
has the checker’s SHA-256 `89b674a6…`.

## Prices

| Name here | Oblique nodes | Source’s oblique seconds | Source’s CPU-hours | `mixed-price` CPU-hours |
| --- | ---: | ---: | ---: | ---: |
| `n66-L843` | 120,072,600 | 58,309 | 16.2 | 15.5 |
| `n18-L470` | 37,874,941 | 9,819 | 2.7 | not priced: the tool’s rate model assumes the standard net |

The source’s seconds are each bundle’s own record of its oblique run, summed over its
`proof/net*/result.json`.

## Replaying the Certificates

**`n66-L843`: a sample.** The complete replay is priced above at 15.5 CPU-hours, more
than the importing lane’s budget, so the source’s own checker was replayed here at 12 of
the 201 directions by the audit tool’s `mixed-replay`, at one worker under `nice`, on 5
October 2026 from 18:52 to 20:56 UTC:

```sh
# from packing/, one command per range
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_point_and_mixed \
  mixed-replay n66-L843 --range 156-157 --work W --workers 1 --tarball TARBALL
```

The ranges are 0–1 (the axis and the first oblique direction), 24–25, 100–101, 147–148
and 156–157 (the pairs holding the two least recorded bounds, at 148 and 157), and
199–200 (the last). Every direction was `REPLAYED`, returning the certificate’s own
record, in 4,628 CPU-seconds against the source’s 3,741 on the same directions. The
receipts are [`receipts/n66-L843/range-*/`](receipts/n66-L843/). A sample is a
diagnostic: it decides no other direction, and `mixed-merge` has not been run.

**`n18-L470`: the bundle’s own driver, in full.** The pinned tarball was unpacked twice.
One copy is the shipped run, which `audit_wand125_declared_net bundle` binds to the
packet. In the other, the bundle’s driver ran as its README says, at two workers under
`nice`, with CPython 3.14.7, NumPy 2.5.2 and c++ 13.3.0, from 17:16 to 21:40 UTC on 5
October 2026:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 code/verify_mixed_full_proof.py proof --workers 2
```

It exited zero with `ALL_ANGLES_VERIFIED_AND_REPLAYED` at 416 of 416 nodes, in 4.40
hours of wall time on a host at load 7 to 17; its CPU time was not recorded, the
runner’s process times not reaching the driver’s pooled workers. From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_declared_net \
  compare --shipped SHIPPED --fresh RUN --meta RUN_META
```

printed `FULL_REPLAY_MATCHES_SHIPPED`: the driver’s progress counts 416 of 416 nodes, its
binary is in the copy, all 416 records were written during the run and equal the shipped
ones and the retained certificate’s, the rewritten certificate equals the retained one
as a mapping, and the other 848 shipped files are unchanged. The receipts are
[`receipts/n18-L470/full/`](receipts/n18-L470/full/): `compare.json`, and the runner’s
`run.meta` and the driver’s `run.stdout`.

**`sqverify-fast`.** This repository’s clean-room verifier, with lemma N0 for the
declared net, verified both certificates at every direction of their nets on 5 October:
`n18-L470` at 416 directions in 168 CPU-seconds and `n66-L843` at 201 in 2,167, recorded
in the [Milestone B census](../../../benchmarks/measure-verifier/census-mixed/README.md).
No rung rests on those runs.

On 6 October `n66-L843` was decided again at all 201 directions by the binary of the
crate source that the census route’s review accepted, without the declared-net change:
`VERIFIED`, 117,253,700 nodes, least certified bound $1.0000000006737138$ at index 122,
2,105 CPU-seconds at two threads, the same verdict, node total and least bound as the
run of 5 October, whose census row it replaces. Two mutants were refused at index 122.
On the 12 directions above it took 129 CPU-seconds where the source’s checker took
4,628. The evidence entry `E-n066-wand125-mixed-843-sqverify-fast-replay` states it, and
it is the complete replay here on which the verified lower bound at $n = 66$ rests. The
verifier was written without opening the source’s checker and shares no code with it,
so this is an independent decision of coverage by the same method, not a reproduction of
the source’s records.

## Limitations

- **Coverage is decided by the source’s C++ alone** for the source’s own runs; the replays
  and `sqverify-fast` runs here are recorded separately. At $n = 18$ the bundle’s own
  driver was replayed in full; at $n = 66$ only a sample of 12 directions has been
  replayed with the source’s checker, and the complete replay here is `sqverify-fast`’s.
- **No source audit.** Neither directory carries the source’s `completion-audit.json`, so
  nothing the source publishes binds a certificate to its tarball but the README’s digest
  and the commit. The binding here is the pinned tree’s digest and each bundle’s own file
  list.
- **The bundles are pinned and not held.** A replay needs each tarball from the source at
  the pinned revision, with the digest above.

## Compressed Files

The four upstream data files of more than 1,000 lines, the two candidates and the two
certificates, are stored as deterministic gzip made by `gzip -9n`, with no file name or
timestamp in the header. The table gives the Git blob and SHA-256 of the decompressed
bytes, which are the file’s blob and digest at the pinned commit; each SHA-256 is also
the one [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) pins.
The repository’s readers take the upstream path and decompress through
`devtools.retained_data.read_retained_bytes`, and
`python -m devtools.retained_data check PACKET` re-derives every row.

Before running any of the source’s own programs on this packet, restore the exact upstream
tree from the repository root:

```sh
find packing/resources/web/wand125-mixed-bounds-finer-net-2026-10-05 -name '*.gz' -exec gunzip -k {} +
```

The restored plain files are untracked, so remove them afterwards; while both copies are
present, the acquisition check reports each as retained twice.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `square-packing-bounds/certificates/mixed_n18_L470/candidate.json.gz` | upstream | `5da1be4a1ae08b96b478e991cf10fa91124b9032` | `44eb3741c7529430e729fb1d5398b62f249ee66102f174dd6cac0e7303ba9d67` |
| `square-packing-bounds/certificates/mixed_n18_L470/certificate.json.gz` | upstream | `b9383b5d5aeb48c99f1e867257c477080c51625d` | `90200d8fe0a3b6da6e0b463fef799b0ffcb7849c1f4cdb7cc6bc7dc029792c60` |
| `square-packing-bounds/certificates/mixed_n66_L843/candidate.json.gz` | upstream | `b4ef1a38ae1b6447ee1cbbf04e634b977f12b767` | `7d358bcad6a30954a44e9fd5f909df8df8fac573b348be30d901444393e77a11` |
| `square-packing-bounds/certificates/mixed_n66_L843/certificate.json.gz` | upstream | `1199ff996a3689a7feb8cdac0e3dfdf52f52d20a` | `80e78bf3a3367d983c81dd16dfe226b6c3af665ba37d77b05bec100ea29a071a` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
