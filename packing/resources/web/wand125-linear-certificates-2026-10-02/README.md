# wand125 Linear Certificates for n = 101 and 83, Pinned 2026-10-02

This packet pins two certificate directories of
[wand125/square-packing-bounds](https://github.com/wand125/square-packing-bounds) at its
commit of 2 October 2026 at 05:26 UTC, for two registration requests:
$s(101) \ge 257/25$, in [jlevy/squares#294](https://github.com/jlevy/squares/issues/294)
(opened 2026-10-02T01:24:48Z), and $s(83) \ge 187/20$, in
[its comment of 05:27](https://github.com/jlevy/squares/issues/294#issuecomment-5946131807).
The issue also announces $n = 82$ at $9.32$, which no revision publishes yet.

The certificates are of a kind this record has not registered: *linear* measures of point
masses, uniform segments and uniform rectangles, checked by
`code/unified_linear_verify.cpp`. The source first used that checker for its superseded
$s(50) \ge 147/20$ rung, `mixed_n50_L735`, whose bundle the
[September 28 packet](../wand125-point-and-mixed-2026-09-28/README.md) pins; the rectangle
densities of the [`52af997`](../wand125-mixed-bounds-2026-10-02/README.md) and
[`7975030`](../wand125-mixed-bounds-n76-2026-10-02/README.md) packets use another.
Its proposed Frontier key is **[wand125 linear certificates 2026-10-02]**. The claims below
are stated as the source states them.
Neither certificate was replayed in full: one angle of each was replayed, to price the
replay. Otherwise what was checked is SHA-256 digests, Git blob ids, the exact premises
the audit below recomputes from the retained bytes, and every check the replay makes
before its first angle, run on each pinned tarball.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/wand125/square-packing-bounds> |
| Revision | `0c35d909764997ead04dfd90081c9fe9af8d07f2`, branch `main`, tree `907e5a02198be072d44e5cfc3ab8ebd2f1d01c4a`; the revision the $n = 83$ request names, and the first that holds both certificates |
| Committed | Authored and committed 2026-10-02T05:26:52Z, 14:26 on 2 October by the author’s clock (`+09:00`). Its parent is `7975030a`, the [$n = 76$ packet](../wand125-mixed-bounds-n76-2026-10-02/README.md)’s revision |
| Author | wand125, building on Tokoharu’s format and on the method the root README credits |
| Licence | MIT. The root `LICENSE` reads “Copyright (c) 2026 wand125”, is unchanged since `1a25a5ed` and is byte-identical to the [September 27 packet’s copy](../wand125-rectangle-certificates-2026-09-27/wand125-rectangles/LICENSE) |
| Retrieved | 2026-10-02T07:47Z: a blob-filtered clone of `main`, fetched when `main` was at `06eeb40c`, checked out sparse at this revision over the root `README.md`, `LICENSE` and `.gitignore` and the two claim directories. `git ls-remote` listed one branch and no tag |
| Pinned subtree | 43 files, 74,678,515 bytes: the two claim directories and the three root files, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256). The other 2,945 files of the tree are pinned by the commit alone |
| Retained here | 19 files, 785,224 bytes upstream and 200,259 bytes as stored, under [`square-packing-bounds/`](square-packing-bounds/), byte-identical to the pinned files after decompression |

**What the revisions changed.** `af1db07b` (2026-10-02T01:23:19Z), the parent of
`7975030a`, adds `certificates/mixed_n101_L1028` (20 files) and a 14-line root README
section “n = 101: a linear certificate past Green’s bound”. `0c35d909` adds
`certificates/mixed_n83_L935` (20 files) and a 13-line section on $n = 83$; it changes
nothing else, so `git diff af1db07 0c35d90 -- certificates/mixed_n101_L1028` is empty.
The pin is the later commit because it holds both directories, $n = 101$’s unchanged.

**A later revision exists.** `06eeb40c` (2026-10-02T05:58:20Z), the head when this packet
was retrieved, adds three Tokoharu-format rectangle certificates, `rect_n59_L79375`,
`rect_n77_L894` and `rect_n93_L973`, and changes the root README’s table to match. It
changes nothing in this packet’s scope. No request names it; it is not pinned here.

| Claim | Directory | First commit | Committed (UTC) |
| --- | --- | --- | --- |
| $s(101) \ge 257/25$ | `certificates/mixed_n101_L1028` | `af1db07b9516e5d45508bb89481014a65a51d12d` | 2026-10-02T01:23:19Z |
| $s(83) \ge 187/20$ | `certificates/mixed_n83_L935` | `0c35d909764997ead04dfd90081c9fe9af8d07f2` | 2026-10-02T05:26:52Z |

Each directory has exactly that one commit, with equal author and committer dates.

## Credit and AI Assistance, as the Source States Them

The tree’s attribution files are unchanged since the
[`52af997` packet](../wand125-mixed-bounds-2026-10-02/README.md#credit-and-ai-assistance-as-the-source-states-them):
the root README’s Attribution section opens “The method is not ours.” and credits Walter
Stromquist, Hiroshi Nagamochi, Sam Burns, Gustavo Massaccesi and this repository, and its
Status section says “Parts of this work were produced with AI assistance under human
direction.” Issue 294 calls these “our certificates of a second kind”. Each directory
README calls the checker “the verifier of `mixed_n50_L735`”, and the checker’s own header
reads “Research verifier for rectangle, point and uniform line-segment measures.” All
three commits, `af1db07b`, `7975030a` and `0c35d909`, end with the trailer
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## What Is Retained

Retained byte-identical at their upstream paths:

- from each of **`certificates/mixed_n101_L1028/`** and **`certificates/mixed_n83_L935/`**:
  `README.md`, `candidate.json`, `certificate.json`, `completion-audit.json` and
  `manifest.json`;
- from **`certificates/mixed_n101_L1028/`** also `requirements.txt` and the seven files of
  `code/` that no other packet holds: `unified_linear_verify.cpp`,
  `unified_linear_verify.py`, `unified_linear_full_verify.py`, `unified_measure.py`,
  `replay_linear_bundle.py`, `radial_measure.py` and `trimmed_core.py`; and
- the root **`README.md`** (SHA-256 `51d5aeae…`, 46,790 bytes).

Pinned by digest only:

| Upstream path | Bytes | SHA-256 | Why not retained |
| --- | ---: | --- | --- |
| `LICENSE` | 1,064 | `c0dd43e7892932c81335f74a2fdbf1a98f5977bab14c0c4c30e3abcc97c34904` | Retained byte-identical by the September 27 rectangle packet |
| `.gitignore` | 132 | `0a31c24fe622ff8b4b012fbf790686063a84da3dd306d47e7283aad434653308` | A retained `.gitignore` would act on this repository’s tree; the October 1 packet quotes it |
| `certificates/mixed_n101_L1028/n101-L10.28-proof-bundle.tar.gz` | 27,507,146 | `c32bba42686b9b27268a770c6505d9e8e0804bf0bb169848cecfb622775efdd5` | Complete proof bundle |
| `certificates/mixed_n83_L935/n83-L9.35-proof-bundle.tar.gz` | 46,291,647 | `ca8bf31319a02ee58d978e3de3a86289c4893a2c68eead34e72f22841e111705` | Complete proof bundle |
| `certificates/mixed_*/code/` `endpoint_cells.py`, `score.py` and the four `mixed_*` files | 26,592 in 6, in each directory | each in the subtree list | Byte-identical to the file of the same name in `mixed_n50_L740/code/`, which the [September 28 packet](../wand125-point-and-mixed-2026-09-28/README.md) retains |
| `certificates/mixed_n83_L935/code/` the seven linear files | 40,092 in 7 | each in the subtree list | Byte-identical to the `mixed_n101_L1028/code/` copies retained here |
| `certificates/mixed_n83_L935/requirements.txt` | 26 | `f210d815b23165d825358001c5b3fb3aa3070e9ad931302c6180e2436a09c6c2` | Byte-identical to the `mixed_n101_L1028` copy retained here |

The two directories’ `code/` are byte-identical, 13 files each. Twelve of the thirteen,
`unified_linear_verify.cpp` among them, are also byte-identical to the file of the same
name in `src/` of the `mixed_n50_L735` bundle, which was read from that pinned tarball for
this comparison; `replay_linear_bundle.py`, the replay-only driver, is new. The checker’s
SHA-256, `0249726ab1e67dc481e0c53f43b524902a48f95d051b1b08865a3cf3ef89a06d`, is the
`source_sha256` of the `L735` manifest, of both new manifests and certificates, and of
every `verify.cpp` in both new bundles.

Each tarball digest is also the one its directory’s README and `completion-audit.json`
state, and each audit’s `certificate_sha256` is the digest of the retained
`certificate.json`. The bundles hold no `code/` and no file list of their own: the
source’s README unpacks each beside its directory’s `code/`.

[`acquisition/declaration.json`](acquisition/declaration.json) declares the scope and
the pinned-only rules, and [`acquisition/sources.json`](acquisition/sources.json)
records the pin and every pinned-only file with its size, digest, reason and retained
copy. From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source \
  wand125-linear-certificates-2026-10-02 --checkout CHECKOUT
```

rebuilds the retained files and both acquisition files from a checkout at the pinned
revision, and with `--check` in place of `--checkout CHECKOUT` re-derives the packet from
its manifest without one. Two of its rules name this packet’s own `mixed_n101_L1028`
copies, which a rebuild reads before it rewrites them, so a rebuild into an empty packet
directory needs one run without those two rules first.

## The Claims, as the Source States Them

| Claim | Directory | Measure (orbits) | Total | Checks the source reports |
| --- | --- | --- | --- | --- |
| $s(101) \ge 257/25$ | `mixed_n101_L1028` | 333 points, 897 segments, 4 rectangles | $10099999/100000$ | `code/unified_linear_verify.cpp` at all 201 net angles, the axis included, 55,222,823 nodes |
| $s(83) \ge 187/20$ | `mixed_n83_L935` | 86 points, 222 segments, 774 rectangles | $8299999/100000$ | The same, 137,090,913 nodes |

Each candidate has schema `point_line_rectangle_v1`: a list of primitives, each a point,
a segment or a rectangle with exact rational geometry and the total mass of its eight D4
images, so the symmetry is built into the format. Segment mass is uniform along its
length. The core side is $B = 9977/10000$ and the net 201 half-angle tangents of step
$83/40000$, as for the rectangle certificates. At each angle the checker proves, with
outward-rounded interval arithmetic and a branch and bound over centre boxes, that every
closed core of side $B$ centred in $[L/2, L/2 + E]^2$, where $E = (L - B(c + s))/2$, has
measure at least $1$; by the measure’s quarter-turn symmetry that quadrant stands for the
whole centre domain. Points count when they are in the closed core, segments by the
length inside, rectangles by the area inside. Unlike the rectangle densities’ checker, it
has no separate axis program: angle zero is one more input.

Each `certificate.json` has status `ALL_LINEAR_ANGLES_VERIFIED_AND_REPLAYED`, records each
angle as `LINEAR_ANGLE_REPLAYED` with its input’s digest and node count, and its
`replay_scope` says the replay uses “the SAME outward-rounded implementation. Not an
independent second algorithm or proof-assistant formalization.” The source compares
$n = 101$ with Green’s $G_{10} = 2\sqrt2 - 1 + (810 + 18\sqrt5)/101 = 10.2467\ldots$
(DS7, Theorem 9 with $k = 10$) and $n = 83$ with Green’s $9.2667\ldots$ for
$n = 82$ to $85$ ($k = 9$).

## The Exact Audit and the Pre-Replay Checks

From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_linear \
  linear-audit --check
```

recomputes [`receipts/linear-audit.json`](receipts/linear-audit.json) from the retained
bytes and imports no source code. For each certificate it requires every retained file to
have its pinned digest; the schema, count, side and core stated; the stated point,
segment and rectangle orbit counts; every primitive inside the container, nondegenerate
and of nonnegative mass, with total exactly $n - 1/100000$; the D4 images, recomputed here
in the source’s order, invariant under both generators; the candidate digest, recomputed by
the source’s rule (`933aa468…` and `159f4c9e…`), equal in the statement, the manifest,
the certificate and the source’s audit; the net record equal to the containment facts
recomputed here, and a positive $E$ at every angle; the checker `0249726a…` and every file
of `code/` a retained copy at its pin; a `LINEAR_ANGLE_REPLAYED` record for each of the
201 angles; and the source audit’s certificate and tarball digests.

Both pass. The least centre half-widths are at index 200, $4.4345\ldots$ and
$3.9695\ldots$. Each side exceeds Green’s DS7 value at its count, enclosed to 60 digits,
and Nagamochi’s $1 + \sqrt{82}$ and $1 + \sqrt{66}$. None of it decides coverage.

On 2 October `linear-fetch` was run on each pinned tarball, read by Git from the pinned
commit. Each has the pinned SHA-256 and size; each bundle has exactly the 810 files of
its shape (six at the top, four in each of the 201 angle folders); its candidate,
certificate and manifest are the retained files, every angle’s `candidate.json` is the
top-level one, and all 202 copies of `verify.cpp` are the pinned checker; its summary
records 201 angles verified. The shipped code assembled from the retained copies passes
the replay driver’s preconditions, and every one of the 201 inputs encloses the exact
candidate recomputed here: 32 rectangle, 2,664 point and 7,176 segment images for
$n = 101$, and 6,192, 688 and 1,776 for $n = 83$. The bundles record the source’s own
runs as 31,304 and 75,686 seconds.

## Replaying the Certificates

The $n = 101$ certificate has been replayed here in full, on 2 October 2026; the $n = 83$
certificate has not. The source’s check is
`code/replay_linear_bundle.py`, run on the unpacked bundle beside `code/`.
`devtools.audit_wand125_linear` runs the same check split by net angle, through the mixed
certificates’ range driver, one command per batch:

```sh
# from packing/, one range per session
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_linear \
  linear-replay n101 --range 0-100 --work /tmp/wand125-n101 --workers 4 --via git
# when every range has run
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_linear \
  linear-merge n101
```

`linear-replay` obtains the tarball at the pinned revision (with `--via git`, from a fetch
of the pinned commit), refuses it unless its SHA-256 and size are the pinned ones, unpacks
it afresh, binds the bundle as above, rebuilds `code/` from the retained copies, repeats
the replay driver’s preconditions, binds each input of the range to the candidate, builds
the checker with the shipped `compile_verifier`
(`c++ -O2 -std=c++17 -ffp-contract=off -fno-fast-math`), and calls the shipped
`replay_angle` unchanged. An angle passes only if that function returns exactly the
record the retained `certificate.json` holds for it. Receipts are written to
`receipts/n101/range-AAA-BBB/` as each angle finishes; a rerun replays only what has not
passed, and the exit codes are the mixed driver’s. `linear-plan NAME --parts K` gives K
ranges of equal node count with their commands.

**What a replay costs.** One angle of each was replayed alone, with `--workers 1`, on
2 October on a 4-core KVM guest (Intel Xeon at 2.10 GHz) whose load average stood near
20: index 150 of $n = 101$ took 123.8 CPU-seconds against the source’s 133.3, and index
50 of $n = 83$ took 273.3 against 249.6, each returning the certificate’s record. The
receipts are [`receipts/n101/range-150-150/`](receipts/n101/range-150-150/) and
[`receipts/n83/range-050-050/`](receipts/n83/range-050-050/). A node’s cost depends on the
measure’s mix and on the angle: the source’s own seconds per node at $n = 83$ rise from
0.42 ms below index 20 to 0.60 ms above 150. So `linear-price` scales the source’s seconds
for each whole run by the ratio on the sampled angle: about 8.1 CPU-hours for $n = 101$
and 23.0 for $n = 83$, or 2.0 and 5.8 hours of wall time at four workers. On a four-core
runner that is one batch for $n = 101$ and three for $n = 83$, the ranges
`linear-plan n83 --parts 3` gives, 0–90, 91–152 and 153–200, of about 6.7, 8.0 and
8.3 CPU-hours. The longest single angle is $n = 101$’s axis, about 20 minutes.

**The negative control.** `linear-control n101` ran on 2 October at net index 35, the
oblique angle with the fewest recorded nodes (76,875). A witness centre found there and
evaluated exactly is covered $1.00200\ldots$ by the measure. The original, exported by
the shipped `export`, was accepted with the stored result; both mutations, every mass
scaled by $99/100$ and the segment orbit contributing most at the witness dropped, leave
the witness covered $0.99198\ldots$ and $0.95298\ldots$, and the checker refused both,
stopping unresolved at its depth floor. The receipt is
[`receipts/n101/control.json`](receipts/n101/control.json); the three runs took 45
CPU-seconds.

## The Complete Replay of $n = 101$, 2 October 2026

`linear-replay n101 --range 0-200` ran on 2 October 2026 in one run of four workers on a
shared 4-core x86-64 Linux container (Intel Xeon at 2.10 GHz, `c++` 13.3.0, one BLAS and
OpenMP thread, `PYTHONOPTIMIZE` unset), bound to the pinned tarball, after index 150 had
been replayed alone to price it. `linear-merge n101` printed
`FULL_REPLAY_MATCHES_SHIPPED`: every one of the 201 directions, the axis included,
returned the record the certificate holds, its status, input digest and node count.

| Certificate | Directions | Runs | Axis CPU-seconds | CPU-hours | Receipts |
| --- | ---: | ---: | ---: | ---: | --- |
| `mixed_n101_L1028` | 201 | 2 | 949.5 | 7.69 | [`receipts/n101/`](receipts/n101/) |

[`receipts/n101/merged.json`](receipts/n101/merged.json) is the merged verdict, and
`linear-merge n101 --check` re-derives it. The run replays the source’s own checker and
replay functions, so it confirms the source’s run rather than deciding coverage a second
way. The certificate’s per-direction records carry no least lower bound, so the receipts
cannot keep one (the review’s finding LC-4); acceptance at each direction is the
checker’s own verdict. With the control above, it puts $s(101) \ge 257/25$, and by mass
$s(102)$ to $s(105)$, in the verified lane (T-080).

## Where the Request and the Retained Files Differ

- **The margin at $n = 83$.** The directory README and the root README say $9.35$ exceeds
  Green’s $9.2667\ldots$ “by more than `0.0833`”, and `completion-audit.json` gives
  `improvement_lower` as $833/10000$ against `compared_with` $92667/10000$. That value is
  below Green’s $9.26673353\ldots$, so the margin is $0.08326646\ldots$, which is less
  than $0.0833$. The bound itself is unaffected. At $n = 101$ the comparison value is an
  upper enclosure of $G_{10}$, and the stated margin, more than $0.0332637$, is right:
  it is $0.03326373\ldots$.
- **Where the second replay ran.** The request and the READMEs say the full replay was
  run from the published tarball “on a separate machine”. This was not checked.
- **What the replay needs.** The READMEs ask for NumPy, SciPy, Numba and HiGHS. The replay
  path imports none of them, only the standard library, and needs a C++17 compiler.

## Limitations

- **Neither certificate was replayed in full.** Two angles of 402 were replayed, each
  returning the certificate’s record; that decides nothing about the others.
- **The bundles are pinned and not held.** A replay needs each tarball from the source at
  the pinned revision, with the digest above.
- **One control.** Only $n = 101$ has a negative control; $n = 83$’s shares its checker.

## Compressed Files

Four upstream data files of more than 1,000 lines are stored as deterministic gzip made
by `gzip -9n`: the two candidates and the two certificates. Each has no file name or
timestamp in its header. The table gives the Git blob and SHA-256 of the decompressed
bytes, which are the file’s blob and digest at the pinned commit; each SHA-256 is also the
one [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) pins.
The repository’s readers take the upstream path and decompress through
`devtools.retained_data.read_retained_bytes`, and
`python -m devtools.retained_data check PACKET` re-derives every row.

Before running any of the source’s own programs on this packet, restore the exact
upstream tree from the repository root:

```sh
find packing/resources/web/wand125-linear-certificates-2026-10-02 -name '*.gz' -exec gunzip -k {} +
```

The restored plain files are untracked, so remove them afterwards; while both copies are
present, the acquisition check reports each as retained twice.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `square-packing-bounds/certificates/mixed_n101_L1028/candidate.json.gz` | upstream | `c379fc651b753a623ef52989e26f11e0e98c570c` | `022f87cada5e3cfb27525d09b07d0c2c4274fc9ebd8f117985e5a042b3241ac9` |
| `square-packing-bounds/certificates/mixed_n101_L1028/certificate.json.gz` | upstream | `6f40afbfb5f12afcec79fc4065679ab8a91b5fa2` | `443e0e1b5422e5f81e25a4a52b7a49479a326977c93f67ca5a6a049f0b18c316` |
| `square-packing-bounds/certificates/mixed_n83_L935/candidate.json.gz` | upstream | `db9052627e70a8716bb1affcc87fe24c56e6f57a` | `e15f9a4de81ab5e737c4c4d70ac54552744ae65229f961a58e516fcb2fa52065` |
| `square-packing-bounds/certificates/mixed_n83_L935/certificate.json.gz` | upstream | `5bcebedcf58b68edb47a0ee496f3140470b8142d` | `ae29a32388626af4933293536d6cbd867cc6592ce64ab61a8271343cce3b898b` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
