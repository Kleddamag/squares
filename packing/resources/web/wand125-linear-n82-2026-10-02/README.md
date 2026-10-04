# wand125 Linear Certificate for n = 82, Pinned 2026-10-02

This packet pins one certificate directory of
[wand125/square-packing-bounds](https://github.com/wand125/square-packing-bounds) at its
commit of 2 October 2026 at 15:16 UTC, for one registration request: $s(82) \ge 233/25$,
in [a comment on jlevy/squares#294](https://github.com/jlevy/squares/issues/294#issuecomment-5952428928)
posted at 2026-10-02T12:34:09Z. The same author’s
[jlevy/squares#308](https://github.com/jlevy/squares/issues/308), opened at 14:06:26Z,
reports that the published argument for Green’s DS7 Theorem 9 does not establish it for
$k \ge 4$, and names this certificate among those above Green’s value $G_9$ that do not
rest on it. $n = 82$ is the count where this record’s reported lower bound is still
Green’s.

The certificate is of the kind and checker of the two in the
[linear packet](../wand125-linear-certificates-2026-10-02/README.md): a *linear* measure
of point masses, uniform segments and uniform rectangles, checked by
`code/unified_linear_verify.cpp`. Every file of its `code/` is byte for byte the linear
packet’s copy or the September 28 packet’s, the checker included. The directory was first
committed at `58f153f8`; this packet pins it at `b00fc70f`, the head when retrieved, with
the [six mixed certificates](../wand125-mixed-bounds-afternoon-2026-10-02/README.md) and
the [rectangle packet](../wand125-rectangle-certificates-2026-10-02/README.md) of the same
revision. Its proposed Frontier key is **[wand125 linear n82 2026-10-02]**. The claim
below is stated as the source states it.
It was replayed here in full on 3 October 2026, every direction returning the
certificate’s record. Before that, what was checked is SHA-256 digests, Git blob ids,
the exact premises the audit below recomputes from the retained bytes, and every check the
replay makes before its first angle, run on the pinned tarball.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/wand125/square-packing-bounds> |
| Revision | `b00fc70f1904e9b1b567afee056d347f911209e8`, branch `main`, tree `03f0999d13d1c1462d15471908b43628f38bb01d`; the head when retrieved |
| Committed | Authored and committed 2026-10-02T15:16:36Z, 00:16 on 3 October by the author’s clock (`+09:00`). The commit’s author name is Hiroaki Hosono |
| Author | wand125, building on Tokoharu’s format and on the method the root README credits |
| Licence | MIT. The root `LICENSE` reads “Copyright (c) 2026 wand125”, is unchanged since `1a25a5ed` and is byte-identical to the [September 27 packet’s copy](../wand125-rectangle-certificates-2026-09-27/wand125-rectangles/LICENSE) |
| Retrieved | 2026-10-02T16:53Z: a depth-1 clone of `main` at this revision, with commit dates from a blob-filtered clone of the whole history fetched in the same session. `git ls-remote` listed one branch and no tag |
| Pinned subtree | 23 files, 48,039,284 bytes: the claim directory and the three root files, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256). The whole tree of 3,167 files is pinned file by file in the [2026-10-02 rectangle packet](../wand125-rectangle-certificates-2026-10-02/acquisition/upstream-tree.sha256) |
| Retained here | 5 files, 378,774 bytes upstream and 75,114 bytes as stored, under [`square-packing-bounds/`](square-packing-bounds/), byte-identical to the pinned files after decompression |

**The revisions.** `58f153f8` (2026-10-02T12:33:44Z) adds
`certificates/mixed_n82_L932` (20 files) and 14 lines of root README, the section “n =
82: a linear certificate past Green’s bound”. The directory has exactly that one commit, with
equal author and committer dates, so it is the same at the pin. The other nine commits
between the [linear packet](../wand125-linear-certificates-2026-10-02/README.md)’s pin
`0c35d909` and `b00fc70f` are listed in the
[mixed packet’s README](../wand125-mixed-bounds-afternoon-2026-10-02/README.md#source-and-pin).

| Claim | Directory | First commit | Committed (UTC) |
| --- | --- | --- | --- |
| $s(82) \ge 233/25$ | `certificates/mixed_n82_L932` | `58f153f833a97d8b71630e9ff10b6d00999a0998` | 2026-10-02T12:33:44Z |

## Credit and AI Assistance, as the Source States Them

The tree’s attribution files are unchanged since the
[`52af997` packet](../wand125-mixed-bounds-2026-10-02/README.md#credit-and-ai-assistance-as-the-source-states-them):
the root README’s Attribution section opens “The method is not ours.” and credits Walter
Stromquist, Hiroshi Nagamochi, Sam Burns, Gustavo Massaccesi and this repository, and its
Status section says “Parts of this work were produced with AI assistance under human
direction.” The directory README calls the checker “the verifier of `mixed_n83_L935` and
`mixed_n101_L1028`”, and says that “Green’s bound is a reported value: the published
argument behind it does not establish Theorem 9 for k >= 4.” The `route` of its
`completion-audit.json` names a “strict linear loop” with “three exact-witness repairs”
and a replay “resumed on MAD with per-angle persistence … plus a reverse-order helper,
merged”. The commit message ends with a co-author trailer naming an AI assistant.

## What Is Retained

Retained byte-identical at their upstream paths, from
**`certificates/mixed_n82_L932/`**: `README.md`, `candidate.json`, `certificate.json`,
`completion-audit.json` and `manifest.json`.

Pinned by digest only:

| Upstream path | Bytes | SHA-256 | Why not retained |
| --- | ---: | --- | --- |
| `README.md` | 49,934 | `23a1fa07abc80b5e8d25ea46e2fc609a5173746985eff2018cfb2611b9b499df` | Retained byte-identical by the [2026-10-02 rectangle packet](../wand125-rectangle-certificates-2026-10-02/wand125-rectangles/README.md), pinned at the same revision |
| `LICENSE` | 1,064 | `c0dd43e7892932c81335f74a2fdbf1a98f5977bab14c0c4c30e3abcc97c34904` | Retained byte-identical by the September 27 rectangle packet |
| `.gitignore` | 132 | `0a31c24fe622ff8b4b012fbf790686063a84da3dd306d47e7283aad434653308` | A retained `.gitignore` would act on this repository’s tree; the October 1 packet quotes it |
| `certificates/mixed_n82_L932/n82-L9.32-proof-bundle.tar.gz` | 47,542,670 | `296d8f09f6d9a49ecb7ee3438b31585788403044b4a60644a4ef93262476506f` | Complete proof bundle |
| `certificates/mixed_n82_L932/code/` `endpoint_cells.py`, `score.py` and the four `mixed_*` files | 26,592 in 6 | each in the subtree list | Byte-identical to the file of the same name in `mixed_n50_L740/code/`, which the [September 28 packet](../wand125-point-and-mixed-2026-09-28/README.md) retains |
| `certificates/mixed_n82_L932/code/` the seven linear files | 40,092 in 7 | each in the subtree list | Byte-identical to the `mixed_n101_L1028/code/` copies the [linear packet](../wand125-linear-certificates-2026-10-02/README.md) retains |
| `certificates/mixed_n82_L932/requirements.txt` | 26 | `f210d815b23165d825358001c5b3fb3aa3070e9ad931302c6180e2436a09c6c2` | Byte-identical to the `mixed_n101_L1028` copy in the same packet |

**The checker is the one already reviewed.** The directory’s `code/` has the same 13
files as `mixed_n101_L1028/code/` and `mixed_n83_L935/code/`, each with the same Git
blob; `unified_linear_verify.cpp` is blob `b1503a45`, SHA-256 `0249726a…`, the
`source_sha256` of the manifest, the certificate, the source’s audit and all 202 copies of
`verify.cpp` in the bundle. There is nothing to diff.

The tarball digest is also the one the directory’s README and `completion-audit.json`
state, and the audit’s `certificate_sha256` is the digest of the retained
`certificate.json`. As for the other linear certificates, the bundle holds no `code/` and
no file list of its own.

[`acquisition/declaration.json`](acquisition/declaration.json) declares the scope and
the pinned-only rules, and [`acquisition/sources.json`](acquisition/sources.json)
records the pin and every pinned-only file with its size, digest, reason and retained
copy. From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source \
  wand125-linear-n82-2026-10-02 --checkout CHECKOUT
```

rebuilds the retained files and both acquisition files from a checkout at the pinned
revision, and with `--check` in place of `--checkout CHECKOUT` re-derives the packet from
its manifest without one.

## The Claim, as the Source States It

| Claim | Directory | Measure (orbits) | Total | Checks the source reports |
| --- | --- | --- | --- | --- |
| $s(82) \ge 233/25$ | `mixed_n82_L932` | 86 points, 222 segments, 774 rectangles | $8199999/100000$ | `code/unified_linear_verify.cpp` at all 201 net angles, the axis included, 153,579,479 nodes |

The candidate has schema `point_line_rectangle_v1`, core side $B = 9977/10000$ and the
201-node net of step $83/40000$, as for the other linear certificates; the
[linear packet](../wand125-linear-certificates-2026-10-02/README.md#the-claims-as-the-source-states-them)
describes the format and what the checker proves at each angle.

**The measure is $n = 83$’s, shrunk.** Its 1,082 primitives are those of
`mixed_n83_L935` in the same order and of the same kinds, and every coordinate of each is
that certificate’s scaled by exactly $932/935$, the ratio of the sides. The masses were
solved again: their ratios to $n = 83$’s run from $0.72$ to $1.04$, against $0.98795$
for the totals. So the two measures share their support and not their weights, and each
is checked on its own.

The certificate has status `ALL_LINEAR_ANGLES_VERIFIED_AND_REPLAYED`, records each angle as
`LINEAR_ANGLE_REPLAYED` with its input’s digest and node count, and its `replay_scope`
says the replay uses “the SAME outward-rounded implementation. Not an independent second
algorithm or proof-assistant formalization.” Its source audit states Green’s value as an
interval of about 90 digits, `green_interval`; `green_upper` is that interval’s upper end,
and `improvement_lower` is $233/25$ less it, $0.0532664\ldots$, so a true lower bound on
the margin.

## The Exact Audit and the Pre-Replay Checks

From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_linear \
  linear-audit --packet wand125-linear-n82-2026-10-02 --check
```

recomputes [`receipts/linear-audit.json`](receipts/linear-audit.json) from the retained
bytes and imports no source code, with every check the
[linear packet](../wand125-linear-certificates-2026-10-02/README.md#the-exact-audit-and-the-pre-replay-checks)
lists: the pinned digests; the schema, count, side, core and orbit counts; every
primitive inside the container, nondegenerate and of nonnegative mass, with total exactly
$n - 1/100000$; the D4 images, recomputed here in the source’s order, invariant under
both generators; the candidate digest `5ddb7ed3…`, recomputed by the source’s rule, equal
in the statement, the manifest, the certificate and the source’s audit; the net record
equal to the containment facts recomputed here and a positive $E$ at every angle; the
checker `0249726a…` and every file of `code/` a retained copy at its pin; a
`LINEAR_ANGLE_REPLAYED` record for each of the 201 angles; and the source audit’s
certificate and tarball digests, with its Green upper bound the upper end of its own
interval.

It passes. The least centre half-width is at index 200, $3.9545\ldots$. The side exceeds
Green’s DS7 value at $n = 82$, enclosed to 60 digits, and Nagamochi’s $1 + \sqrt{65}$,
and the source’s `green_upper` is above Green’s value. None of it decides coverage.

On 2 October `linear-fetch` was run on the pinned tarball, read from the depth-1 clone at
the pinned commit. It has the pinned SHA-256 and size; the bundle has exactly the 810
files of its shape; its candidate, certificate and manifest are the retained files, every
angle’s `candidate.json` is the top-level one, and all 202 copies of `verify.cpp` are the
pinned checker; its summary records 201 angles verified. The shipped code assembled from
the retained copies passes the replay driver’s preconditions, and every one of the 201
inputs encloses the exact candidate recomputed here: 6,192 rectangle, 688 point and
1,776 segment images. The receipt is [`receipts/n82/fetch.json`](receipts/n82/fetch.json).
The bundle records the source’s own run as 118,941.6 seconds.

## Replaying the Certificate

It has been replayed here in full; see the next section. The source’s check is
`code/replay_linear_bundle.py`,
run on the unpacked bundle beside `code/`. `devtools.audit_wand125_linear` runs the same
check split by net angle, as for the other linear certificates:

```sh
# from packing/, one range per session
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_linear \
  linear-replay n82 --range 0-51 --work /tmp/wand125-n82 --workers 4 --via git \
  --stop-after-hours 1.6
# when every range has run
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_linear \
  linear-merge n82
```

Receipts go to `receipts/n82/range-AAA-BBB/` as each angle finishes, and a rerun replays
only what has not passed.

**What a replay costs.** No angle of this certificate was timed here. Its measure has
$n = 83$’s 1,082 primitives and image counts, and $n = 83$’s angle 50 ran here at 0.53 ms
a node against the source’s 0.48 ms; at that rate its 153,579,479 nodes are about 22.6
CPU-hours, and about 26 when scaled as `linear-price` scales $n = 83$’s estimate from
nodes to the source’s angle-by-angle seconds. The bundle’s own 33.0 hours are 0.77 ms a
node, 40 per cent above $n = 83$’s 0.55 ms; the source audit says the run was resumed and
merged across machines, so its seconds are not one host’s, and `linear-price` lists them
without an estimate. `linear-plan n82 --parts 6` gives six ranges of equal node count, 0–51,
52–90, 91–123, 124–152, 153–178 and 179–200, each about 4 CPU-hours here.

## The Complete Replay, 3 October 2026

The six ranges of `linear-plan n82 --parts 6` ran on 3 October 2026, one `linear-replay`
run of four workers each, on two runners of shared 4-core x86-64 Linux containers (Intel
Xeon at 2.1 or 2.8 GHz, `c++` 13.3.0, Python 3.14.7, one BLAS and OpenMP thread,
`PYTHONOPTIMIZE` unset), each bound to the pinned tarball. `linear-merge n82` printed
`FULL_REPLAY_MATCHES_SHIPPED`: every one of the 201 directions, the axis included,
returned the record the certificate holds, its status, input digest and node count.

| Certificate | Directions | Ranges | Axis CPU-seconds | CPU-hours | Receipts |
| --- | ---: | ---: | ---: | ---: | --- |
| `mixed_n82_L932` | 201 | 6 | 105.4 | 30.74 | [`receipts/n82/`](receipts/n82/) |

[`receipts/n82/merged.json`](receipts/n82/merged.json) is the merged verdict, and
`linear-merge n82 --check` re-derives it. The runs replay the source’s own checker and
replay functions, so they confirm the source’s run rather than deciding coverage a second
way. The certificate’s per-direction records carry no least lower bound, so the receipts
cannot keep one (finding LC-4 of the linear certificates’ review). The 30.7 CPU-hours
here sit between this packet’s estimate of about 26 and the bundle’s 33.0.

## Where the Request and the Retained Files Differ

- **The bundle’s name.** The `bundle` field of `completion-audit.json` is
  `n82-L9.32-proof-bundle.tar.gz`, the tarball’s file name; the other linear audits give
  the directory inside it, `n101-L10.28-proof-bundle`. The audit here accepts either.
- **What the replay needs.** The README asks for NumPy, SciPy, Numba and HiGHS. As for
  the other linear certificates, the replay path imports only the standard library and
  needs a C++17 compiler.
- **Where the second replay ran.** The request and the README say the full replay was run
  from the published tarball on a fresh Ubuntu 24.04 machine. This was not checked.

## Limitations

- **The replay is the source’s own checker.** Coverage is decided by the source’s C++
  alone; the replay confirms its run and is not a second method.
- **No control of its own.** The checker’s negative control is the linear packet’s, at
  $n = 101$; this certificate shares the checker byte for byte.
- **The bundle is pinned and not held.** A replay needs the tarball from the source at
  the pinned revision, with the digest above.

## Compressed Files

Two upstream data files of more than 1,000 lines are stored as deterministic gzip made by
`gzip -9n`: the candidate and the certificate. Each has no file name or timestamp in its
header. The table gives the Git blob and SHA-256 of the decompressed bytes, which are the
file’s blob and digest at the pinned commit; each SHA-256 is also the one
[`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) pins.
The repository’s readers take the upstream path and decompress through
`devtools.retained_data.read_retained_bytes`, and
`python -m devtools.retained_data check PACKET` re-derives every row.

Before running any of the source’s own programs on this packet, restore the exact
upstream tree from the repository root:

```sh
find packing/resources/web/wand125-linear-n82-2026-10-02 -name '*.gz' -exec gunzip -k {} +
```

The restored plain files are untracked, so remove them afterwards; while both copies are
present, the acquisition check reports each as retained twice.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `square-packing-bounds/certificates/mixed_n82_L932/candidate.json.gz` | upstream | `a442aec8a2a10372844831af959dde718c9ba904` | `e4ea1beb57ed9545612e55afc6c9ca9d9d5b07e17dd375b45448c3ff4273c51d` |
| `square-packing-bounds/certificates/mixed_n82_L932/certificate.json.gz` | upstream | `ba2fcd702db1f20990a12d74c17b6abf751412ff` | `f795efe5a8e0e60bcc02bb00e8c65f5d9bf45a6349cd2afe555432513facdc61` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
