# wand125 Mixed-Rectangle Certificates of 5 October 2026, Pinned at `a541afb`

This packet pins the two certificate directories that
[wand125/square-packing-bounds](https://github.com/wand125/square-packing-bounds) added
on 5 October 2026 at 06:06 and 06:07 UTC, `mixed_n67_L848` and `mixed_n84_L9411`, at the
commit that added the second. Each was posted in its own comment on
[jlevy/squares#282](https://github.com/jlevy/squares/issues/282) seconds after its
commit. They are rectangle-density lower bounds of the kind and checker of the
[certificates of 4 October](../wand125-mixed-bounds-evening-2026-10-04/README.md), at
$n = 67$ and 84. Its proposed Frontier key is **[wand125 mixed bounds 2026-10-05]**.
The claims below are stated as the source states them.

Both are at counts where an earlier mixed certificate of this source is retained, and
each states a larger side and names the one it supersedes: `mixed_n67_L848` over
`mixed_n67_L8475` and `mixed_n84_L9411` over `mixed_n84_L94075`, both of the
[4 October packet](../wand125-mixed-bounds-2026-10-04/README.md).

What was checked here is SHA-256 digests, Git blob ids, the exact premises the audit below
recomputes from the retained bytes, and every check the replay makes before its first
angle, run on each pinned tarball. On 5 October `sqverify-fast`, this repository’s
clean-room measure verifier, decided both retained candidates at all 201 net directions
([the independent replays](#the-independent-replays)); the source’s own checker has not
been run here.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/wand125/square-packing-bounds> |
| Revision | `a541afbe7826ff75f6d3848e10279fd524d55af3`, branch `main`, tree `95cfb20f47f713f8d8c340f487dd5069961e0e77`; the head when retrieved, and the revision the last request names |
| Committed | Authored and committed 2026-10-05T06:07:08Z, 15:07 on 5 October by the author’s clock (`+09:00`) |
| Author | wand125, building on Tokoharu’s format and verifier, as for the other mixed certificates |
| Licence | MIT. The root `LICENSE` reads “Copyright (c) 2026 wand125” and is byte-identical to the [September 27 packet’s copy](../wand125-rectangle-certificates-2026-09-27/wand125-rectangles/LICENSE) |
| Retrieved | 2026-10-05T07:36Z: a blobless clone of the whole history, checked out sparsely at this revision. `git ls-remote` listed one branch and no tag |
| Pinned subtree | 35 files, 51,185,977 bytes: the two claim directories and the three root files, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) |
| Retained here | 9 files, 563,684 bytes upstream, under [`square-packing-bounds/`](square-packing-bounds/), byte-identical to the pinned files after decompression |

**The revisions.** The source’s `main` moved from `797bdf6`, the
[evening packet’s](../wand125-mixed-bounds-evening-2026-10-04/README.md) pin, through two
commits. Each adds one certificate directory and one section of the root README, and
nothing else. Each claim directory is unchanged at the pin since the commit below:

| Claim | Directory | Commit | Committed (UTC) | Request |
| --- | --- | --- | --- | --- |
| $s(67) \ge 212/25$ | `certificates/mixed_n67_L848` | `6c0842ed5d54025d049322bde43a9dc13029e595` | 2026-10-05T06:06:37Z | [06:06:49Z](https://github.com/jlevy/squares/issues/282#issuecomment-5989043109) |
| $s(84) \ge 9411/1000$ | `certificates/mixed_n84_L9411` | `a541afbe7826ff75f6d3848e10279fd524d55af3` | 2026-10-05T06:07:08Z | [06:07:23Z](https://github.com/jlevy/squares/issues/282#issuecomment-5989049022) |

## Credit and AI Assistance, as the Source States Them

The root README at the pin is retained. Its Attribution section opens “The method is not
ours.” and credits Walter Stromquist, Hiroshi Nagamochi, Sam Burns, Gustavo Massaccesi
and this repository, and its Status section says “Parts of this work were produced with
AI assistance under human direction.”, as at the evening packet’s pin; between the two
pins the root README gains one section per certificate and nothing else.

- **The two certificates.** Each directory README calls the checker “the verifier shipped
  here, `code/mixed_rotated_verify.cpp`”, the same checker as for `mixed_n87_L939` and
  `mixed_n65_L835`, and says the certificate is not in Tokoharu’s format because its least
  oblique bound is below the $1.0001$ his `verify.cpp` requires. Each says the candidate
  was built from scratch at its side from a structured initial measure (“bands at integer
  distances from the walls, as in the Green-series certificates”) and repaired against
  counterexamples on the full net.
- **The pre-publication replays.** Each README says the full 201-angle replay was run
  again from the tarball on a fresh Ubuntu 24.04.5 machine with g++ 13.3.0, Python 3.12.3
  and NumPy 2.5.3, after checking the tarball’s SHA-256 and all its file hashes, and each
  comment on #282 says the same. This was not checked.
- **The commits.** Both commit messages end with a co-author trailer naming an AI
  assistant.

## What Is Retained

Retained byte-identical at their upstream paths: the root `README.md`, and from each of the
two claim directories `README.md`, `candidate.json`, `certificate.json` and
`manifest.json`.

Pinned by digest only:

| Upstream path | Bytes | SHA-256 |
| --- | ---: | --- |
| `LICENSE` | 1,064 | `c0dd43e7892932c81335f74a2fdbf1a98f5977bab14c0c4c30e3abcc97c34904` |
| `.gitignore` | 132 | `0a31c24fe622ff8b4b012fbf790686063a84da3dd306d47e7283aad434653308` |
| `certificates/mixed_n67_L848/n67-L8.48-proof-bundle.tar.gz` | 21,960,517 | `2b45da24c08eeb539af72e5d1ff5267984190f1a00ce38de5f46a94b4d53d6d0` |
| `certificates/mixed_n84_L9411/n84-L9.411-proof-bundle.tar.gz` | 28,583,340 | `d38233d75efba438ab2807480d871f247f07c310628a223b0e76ed1e6ae59f80` |

`LICENSE` is retained byte-identical by the September 27 rectangle packet; a retained
`.gitignore` would act on this repository’s tree. Each tarball is a complete proof bundle,
and each digest is the one its directory’s README states. Each directory’s ten `code/`
files and its `requirements.txt` are byte-identical to the files of the same name in
`mixed_n50_L740/`, which the
[September 28 packet](../wand125-point-and-mixed-2026-09-28/README.md) retains, and are
pinned by digest in the subtree list. Neither directory carries a `completion-audit.json`
at the pin.

[`acquisition/declaration.json`](acquisition/declaration.json) declares the scope and the
pinned-only rules, and [`acquisition/sources.json`](acquisition/sources.json) records the
pin and every pinned-only file with its size, digest, reason and, where one exists, the
retained copy with the same bytes.
From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source \
  wand125-mixed-bounds-2026-10-05 --checkout CHECKOUT
```

rebuilds the retained files and both acquisition files from a checkout at the pinned
revision, and with `--check` in place of `--checkout CHECKOUT` re-derives the packet from
its manifest without one.

## The Claims, as the Source States Them

| Name here | Claim | Rectangles | Source’s comparison, in its README | Least oblique bound recorded (index) | Axis cells, minimum |
| --- | --- | ---: | --- | --- | --- |
| `n67-L848` | $s(67) \ge 212/25$ | 536 | its earlier certificate `mixed_n67_L8475` (8.475) | $1.0000000005520073$ (83) | 13,454,224, $1.0064534322049679$ |
| `n84-L9411` | $s(84) \ge 9411/1000$ | 686 | its earlier certificate `mixed_n84_L94075` (9.4075) | $1.0000000003743108$ (127) | 20,738,916, $1.0020008331669186$ |

Both are rectangle densities with no point mass (each `candidate.json` has an empty
`points` list and a `scaling_factor` of `1`), of total mass $n - 1/100000$, with core side
$B = 9977/10000$, 201 net half-angles of step $83/40000$ and coverage threshold $1$, as for
every earlier mixed certificate. Each `certificate.json` has status
`ALL_ANGLES_VERIFIED_AND_REPLAYED`. Each README compares with the source’s own earlier
value at its count, which is the value the record reported there before this import
(T-090), and with Green’s reported value as a reference.

## The Exact Audit and the Pre-Replay Checks

From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_point_and_mixed \
  mixed-audit wand125-mixed-bounds-2026-10-05 --check
```

recomputes [`receipts/mixed-audit.json`](receipts/mixed-audit.json) for the two from the
retained bytes and imports no source code, with the checks the
[4 October packet](../wand125-mixed-bounds-2026-10-04/README.md) describes: pinned
digests; the count, side, core and rectangle count stated; nonnegative masses inside the
container, of total exactly $n - 1/100000$; the candidate digest by the source’s rule,
equal in the manifest, the certificate and the statement; the net record equal to the
containment facts recomputed here; the checker `89b674a6…` and `code/` the retained
$n = 50$ copy; a replay record at threshold $1$ for each of the 201 angles; and each
tarball bound by its digest at the pinned tree, which `acquire_source` bound to its Git
blob at the pinned commit, with the size the acquisition record pins, no
`completion-audit.json` in the directory, and the claim, the tarball’s name and its digest
stated in the README. Both pass. Each side exceeds Green’s DS7 value at its count
(Theorem 9, $k = 8$, from $n = 65$, and $k = 9$, from $n = 82$), enclosed to 60 digits, and
Nagamochi’s $1 + \sqrt{n - 2\lfloor\sqrt n\rfloor + 1}$, and the centre domains are
recomputed at the oblique nodes. None of it decides coverage.

On 5 October `mixed-fetch` was run on each of the two pinned tarballs, read from the
checkout at the pinned commit, in 37 seconds of wall time in all. Each has the pinned
SHA-256 and size; each unpacked bundle matches all 621 entries of its `files-sha256.json`
with nothing unlisted, and its candidate, certificate, manifest and `code/` are the retained
or `mixed_n50_L740` files; the shipped driver’s preconditions hold on its own code; every
one of the 200 oblique inputs encloses the exact candidate recomputed here; and every
record is `ANGLE_VERIFIED` with an empty frontier at $\gamma = 1$. Each run’s output is its
certificate’s `receipts/NAME/fetch.json`; the `bundle` field names the scratch directory it
was unpacked in.

| Name here | Rectangle images checked | Oblique nodes | Source’s oblique seconds | Source’s CPU-hours | `mixed-price` CPU-hours | Planned CPU-hours |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `n67-L848` | 4,288 | 93,610,234 | 33,475 | 9.30 | 9.1 | 10.2 |
| `n84-L9411` | 5,488 | 118,544,320 | 43,006 | 11.95 | 14.6 | 16.4 |

The source’s seconds are the bundle’s own record of its oblique run, 21.2 CPU-hours for
the two. `mixed-price` scales the rate of the three angles timed on 2 October by each
certificate’s node counts and rectangles, 23.7 CPU-hours. The planned column is that
estimate times 1.119, the ratio of measured to estimated CPU-hours over the complete
replays already merged in this record (`observed_ratio`), 26.5 CPU-hours in all.

## Replaying the Certificates

The source’s check is its driver `code/verify_mixed_full_proof.py`, run from the unpacked
tarball. `devtools.audit_wand125_point_and_mixed` runs the same check split by net angle,
as for the earlier mixed packets, and names the two `n67-L848` and `n84-L9411`, since an
earlier certificate already names each count.

```sh
# from packing/: one command per range; 0 is the axis direction
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_point_and_mixed \
  mixed-replay n84-L9411 --range 0-73 --work /tmp/wand125-n84-L9411 --workers 4 --via git
# when every range of a certificate has run
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_point_and_mixed \
  mixed-merge n84-L9411
```

Receipts go to `receipts/NAME/range-AAA-BBB/` as each angle finishes, and a rerun replays
only what has not passed.
`mixed-shard wand125-mixed-bounds-2026-10-05 --runners 2` splits the two across two hosts
of four workers, about 13.3 planned CPU-hours and 3.3 wall hours each:

| Runner | Planned CPU-hours | Wall hours at 4 workers | Ranges, run in this order |
| --- | ---: | ---: | --- |
| r1 | 13.2 | 3.3 | `n67-L848` 108–162, `n84-L9411` 74–116, `n84-L9411` 150–176, `n84-L9411` 177–200 |
| r2 | 13.3 | 3.3 | `n67-L848` 0–107, `n67-L848` 163–200, `n84-L9411` 0–73, `n84-L9411` 117–149 |

Each runner runs its `mixed-replay` commands one after another, then commits and pushes
its receipts; `mixed-merge NAME` is run for each certificate once every range of it has
arrived. No replay has been launched.

## The Independent Replays

On 5 October 2026 `devtools.sqverify_fast_census --family mixed` ran `sqverify-fast` on
each retained `candidate.json.gz` at all 201 net directions, at the threshold the
certificate declares, and then refused two mutants of each at its least-bound direction.
Both are `VERIFIED`; the receipts are in
[`benchmarks/measure-verifier/census-mixed/`](../../../benchmarks/measure-verifier/census-mixed/README.md),
and the evidence entries `E-n067-wand125-mixed-848-sqverify-fast-replay` and
`E-n084-wand125-mixed-9411-sqverify-fast-replay` state them.

| Name here | Nodes | Least certified bound (index) | CPU seconds, two threads |
| --- | ---: | --- | ---: |
| `n67-L848` | 91,535,166 | $1.000000000605981$ (77) | 1,388 |
| `n84-L9411` | 110,704,136 | $1.000000000102596$ (111) | 1,878 |

The verifier was written without opening the source’s checker and shares no code with
it, so these are independent decisions of coverage by the same method, not
reproductions of the source’s records. The source’s checker remains unreplayed here; the
range commands above would add that reproduction.

## Limitations

- **The source’s checker is not replayed.** Coverage was decided here by `sqverify-fast`
  alone; the source’s C++ and its axis tables have not run on either certificate.
- **No source audit.** Neither directory carries the source’s `completion-audit.json`, so
  nothing the source publishes binds a certificate to its tarball but the README’s digest
  and the commit. The binding here is the pinned tree’s digest and, after `mixed-fetch`,
  the bundle’s own file list and its proof files.
- **The bundles are pinned and not held.** A replay needs each tarball from the source at
  the pinned revision, with the digest above. `--via git` fetches it by Git.

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
find packing/resources/web/wand125-mixed-bounds-2026-10-05 -name '*.gz' -exec gunzip -k {} +
```

The restored plain files are untracked, so remove them afterwards; while both copies are
present, the acquisition check reports each as retained twice.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `square-packing-bounds/certificates/mixed_n67_L848/candidate.json.gz` | upstream | `3cd6ce6de282b3bd09a1aa0f4c5076e0282688a7` | `d6393c7c3f8cf4de10c4cbd7696e4cfa10561aed7ed06b0c0cd891b3291bf037` |
| `square-packing-bounds/certificates/mixed_n67_L848/certificate.json.gz` | upstream | `b5227cbb10d8213a6a41f8ea23f3a35ec38f11c7` | `3d5f7948a30305412e8247c24fcd64a878de4c97f6c34eb4cf00d570c4a5f2f7` |
| `square-packing-bounds/certificates/mixed_n84_L9411/candidate.json.gz` | upstream | `089b3f71caceeb9e2f8e734a5440b30142fa9add` | `10ad1ed9844965dbee72708a73047602d27e5b6fc9dfdbb4d5cf6cb7daca8b9c` |
| `square-packing-bounds/certificates/mixed_n84_L9411/certificate.json.gz` | upstream | `cb87bf212cd4d7413143735cbdf7d13851580cd1` | `11673fc5a6409ee20672bdf39fb46b742856e44a69f77fe0173258773e018c86` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
