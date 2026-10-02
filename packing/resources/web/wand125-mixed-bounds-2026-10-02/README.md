# wand125 Mixed-Rectangle Certificates for n = 84 and 85, Pinned 2026-10-02

This packet pins two certificate directories of
[wand125/square-packing-bounds](https://github.com/wand125/square-packing-bounds) at its
commit of 2 October 2026, for one registration request: two rectangle-density lower
bounds, $s(84) \ge 47/5$ and $s(85) \ge 471/50$, of the same kind as the five in the
[October 1 packet](../wand125-point-and-mixed-2026-10-01/README.md) and the
$s(50) \ge 37/5$ certificate in the
[September 28 packet](../wand125-point-and-mixed-2026-09-28/README.md). The request is
[a comment on jlevy/squares#282](https://github.com/jlevy/squares/issues/282#issuecomment-5943469227),
posted at 2026-10-02T00:47:21Z.

Its proposed Frontier key is **[wand125 mixed bounds 2026-10-02]**. The claims below are
stated as the source states them.
Neither certificate was replayed in full: one oblique angle of each was replayed, to
price the replay. Otherwise what was checked here is SHA-256 digests, Git blob ids and the
exact premises the audit below recomputes from the retained bytes.
Retention registers the claims for review; what the frontier makes of them is decided in
the frontier records.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/wand125/square-packing-bounds> |
| Revision | `52af997dc91c579658f0828bc8304e306ad9d95b`, branch `main`, tree `50c618fe5886240acfdfa24aa97b49ea483b5b79`; the revision the request names |
| Committed | Authored and committed 2026-10-02T00:46:51Z, which is 09:46 on 2 October by the author’s clock (`+09:00`). Its parent is `1a25a5ed`, the revision of the October 1 packets |
| Author | wand125, building on Tokoharu’s format and verifier, as for the October 1 densities |
| Licence | MIT. The root `LICENSE` reads “Copyright (c) 2026 wand125”, is unchanged since `1a25a5ed` (blob `bbfbff13`) and is byte-identical to the [September 27 packet’s copy](../wand125-rectangle-certificates-2026-09-27/wand125-rectangles/LICENSE) |
| Retrieved | 2026-10-02T01:12Z, a blob-filtered clone of `main`, sparse over the root `README.md`, `LICENSE` and `.gitignore` and the two claim directories, when `main` was at this revision. A later `git ls-remote` listed one branch and no tag |
| Pinned subtree | 37 files, 52,143,244 bytes: the two claim directories and the three root files, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256). The other 2,894 files of the tree are pinned by the commit alone |
| Retained here | 11 files, 535,969 bytes upstream and 128,427 bytes as stored, under [`square-packing-bounds/`](square-packing-bounds/), byte-identical to the pinned files after decompression |

**What the revision changed.** `git diff --stat 1a25a5ed 52af997` lists 35 files: the 34
files of the two new directories, and the root `README.md`, which gains a 17-line section
“n = 84, 85: certificates past Green’s bound”. No other file changed, so every file the
October 1 packets pin is unchanged at this revision.

**A later revision exists.** At 2026-10-02T01:23:19Z, after this packet was retrieved, the
source added `af1db07b9516e5d45508bb89481014a65a51d12d`, which adds
`certificates/mixed_n101_L1028` ($s(101) \ge 257/25$, checked by a different verifier,
`unified_linear_verify.cpp`) and 14 lines of root `README.md`, and changes nothing in
this packet’s scope. It is not pinned here: [jlevy/squares#294](https://github.com/jlevy/squares/issues/294)
requests its certificate, which the
[linear packet](../wand125-linear-certificates-2026-10-02/README.md) pins at a later
revision.

Both directories have exactly one commit, the pinned one, with equal author and committer
dates. The dates come from the clone’s full history.

| Claim | Directory | First commit | Committed (UTC) |
| --- | --- | --- | --- |
| $s(84) \ge 47/5$ | `certificates/mixed_n84_L940` | `52af997dc91c579658f0828bc8304e306ad9d95b` | 2026-10-02T00:46:51Z |
| $s(85) \ge 471/50$ | `certificates/mixed_n85_L942` | `52af997dc91c579658f0828bc8304e306ad9d95b` | 2026-10-02T00:46:51Z |

## Credit and AI Assistance, as the Source States Them

The tree’s only attribution files are `LICENSE` and `point_n21_L5/UPSTREAM-LICENSE.txt`,
Evan Daniel’s MIT licence.
It has no credits, notice, authors or citation file, so credit is read from the READMEs.

- **The root README** keeps the Attribution section the October 1 packet quotes, which
  opens “The method is not ours.”
  and credits Walter Stromquist, Hiroshi Nagamochi, Sam Burns and Gustavo Massaccesi,
  and this repository, for the method.
  Its Status section still says: “Parts of this work were produced with AI assistance
  under human direction.”
- **The two certificates.** Each directory README calls the checker “the verifier shipped
  here, `code/mixed_rotated_verify.cpp`, the same checker as for `mixed_n87_L939` and
  `mixed_n65_L835`”, and says the certificate is not in Tokoharu’s format because its
  least coverage bound is below the $1.0001$ his `verify.cpp` requires.
  Issue 282 says the format and base checker are Tokoharu’s and the measures and the
  modified checker wand125’s.
  The `route` of the $n = 84$ `completion-audit.json` reads “n84 fresh Green
  initialization at L9.4 (rectangles), full-net repair, 201-angle verification and
  replay.”, and the $n = 85$ one the same at L9.42.
- **The commit.** Its message ends with the trailer
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## What Is Retained

Retained byte-identical at their upstream paths:

- from each of **`certificates/mixed_n84_L940/`** and **`certificates/mixed_n85_L942/`**:
  `README.md`, `candidate.json`, `certificate.json`, `completion-audit.json` and
  `manifest.json`; and
- the root **`README.md`** (SHA-256 `a64f9132…`, 44,990 bytes), which differs from the
  44,137-byte copy the October 1 packet retains by the added section.

Pinned by digest only:

| Upstream path | Bytes | SHA-256 | Why not retained |
| --- | ---: | --- | --- |
| `LICENSE` | 1,064 | `c0dd43e7892932c81335f74a2fdbf1a98f5977bab14c0c4c30e3abcc97c34904` | Retained byte-identical by the September 27 rectangle packet |
| `.gitignore` | 132 | `0a31c24fe622ff8b4b012fbf790686063a84da3dd306d47e7283aad434653308` | A retained `.gitignore` would act on this repository’s tree. It is unchanged since `1a25a5ed`, and the October 1 packet quotes its patterns |
| `certificates/mixed_n84_L940/n84-L9.40-proof-bundle.tar.gz` | 27,162,456 | `723f167b569835d8aa6f2dfb9eb61d99f5199a2a94f78a4edf9039b7eaf7f080` | Complete proof bundle |
| `certificates/mixed_n85_L942/n85-L9.42-proof-bundle.tar.gz` | 24,366,383 | `c61c51087753ffa9eb57a03b08e5f4aae4439f877ef54386d133f425d389150a` | Complete proof bundle |
| `certificates/mixed_*/code/*` | 77,228 in 20 | each in the subtree list | Each is byte-identical to the file of the same name in `mixed_n50_L740/code/`, which the [September 28 packet](../wand125-point-and-mixed-2026-09-28/README.md) retains |
| `certificates/mixed_*/requirements.txt` | 6 in each of 2 | `e09f656c130b9c08b2c5ab7187c891295e449ed77febea2a6ceee9cc98ccb0fc` | Byte-identical to `mixed_n50_L740/requirements.txt` in the same packet |

Each tarball digest is also the one its directory’s README and `completion-audit.json`
state, and each audit’s `certificate_sha256` is the digest of the retained
`certificate.json`.
Each tarball’s `proof/candidate.json`, `proof/certificate.json` and `proof/manifest.json`
are the retained files, and its `code/` is the retained `mixed_n50_L740/code/`, as
`mixed-fetch` below establishes.

[`acquisition/declaration.json`](acquisition/declaration.json) declares the scope and
the pinned-only rules, and [`acquisition/sources.json`](acquisition/sources.json)
records the pin and every pinned-only file with its size, digest, reason and, where one
exists, the retained copy with the same bytes.
From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source \
  wand125-mixed-bounds-2026-10-02 --checkout CHECKOUT
```

rebuilds the retained files and both acquisition files from a checkout at the pinned
revision. It only reads the checkout and compares each file’s Git blob with
`git ls-tree`. With `--check` in place of `--checkout CHECKOUT` it needs no checkout: it
re-derives from this packet that every retained file has the digest the subtree list
records, that every pinned-only file named as identical to a retained copy is, and that
the record is complete.
The tool is [`devtools/acquire_source.py`](../../../devtools/acquire_source.py).

## The Claims, as the Source States Them

| Claim | Directory | Measure | Total | Checks the source reports |
| --- | --- | --- | --- | --- |
| $s(84) \ge 47/5$ | `mixed_n84_L940` | 661 rectangles | $8399999/100000$ | `code/mixed_rotated_verify.cpp` at 200 oblique net angles and integer tables at angle zero; least oblique bound stated $1.0000000009$, axis minimum $1.008338$ |
| $s(85) \ge 471/50$ | `mixed_n85_L942` | 587 rectangles | $8499999/100000$ | The same; least oblique bound stated $1.0000000017$, axis minimum $1.013817$ |

Both are rectangle densities with no point mass (each `candidate.json` has an empty
`points` list), with core side $B = 9977/10000$, 201 net half-angles of step
$83/40000$ and coverage threshold $1$, as for $n = 50$ and the October 1 five.
Each `certificate.json` has status `ALL_ANGLES_VERIFIED_AND_REPLAYED`, and its
`replay_scope` says the oblique replay is “not a separate independent oblique
implementation”.
The source compares both with Green’s reported $2\sqrt2 + (247 + 12\sqrt2)/41 = 9.2667\ldots$
for $n = 82$ to $85$ (Friedman DS7, Theorem 9 with $k = 9$).

## The Exact Audit

From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_point_and_mixed \
  mixed-audit wand125-mixed-bounds-2026-10-02 --check
```

recomputes [`receipts/mixed-audit.json`](receipts/mixed-audit.json) from the retained
bytes and imports no source code.
For each certificate it requires every retained file to have its pinned digest; the
count, side, core and rectangle count stated; nonnegative masses inside the container,
of total exactly $n - 1/100000$; the candidate digest, recomputed by the source’s rule
(`58dabcb4…` and `b95a0bb4…`), equal in the manifest, the certificate, the source’s
audit and the statement; the net record equal to the containment facts recomputed here;
the checker `89b674a6…` and `code/` the retained $n = 50$ copy; a replay record at
threshold $1$ for each of the 201 angles; and the source audit’s certificate and tarball
digests.

Both pass. The least oblique bounds recorded are $1.0000000008975796$ at index 175 and
$1.0000000017271347$ at index 44, and the axis integer minima $1.0083383947166207$ and
$1.013816765469528$. Each side exceeds Green’s Theorem 9 value for $k = 9$, enclosed to
60 digits, and Nagamochi’s $1 + \sqrt{67}$ and $1 + \sqrt{68}$.
None of it decides coverage.

The same command checks two things it does not write to the receipt, which stays a
function of the retained bytes. Given `--tarball FILE`, it checks a downloaded tarball
against the pin. And it merges whatever replay receipts `receipts/n84/` and
`receipts/n85/` hold, refusing a run not bound to the pinned tarball or an angle that
returned another record, and reports how far each replay has got.

## Replaying the Certificates

Both certificates have since been replayed in full; the next section records the runs.
The source’s check is its driver `code/verify_mixed_full_proof.py`, run from the unpacked
tarball. `devtools.audit_wand125_point_and_mixed` runs the same check split by net
angle, so that one certificate can be shared across sessions, one command per batch:

```sh
# from packing/, one range per session; 0 is the axis direction
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_point_and_mixed \
  mixed-replay n84 --range 0-79 --work /tmp/wand125-n84 --workers 4 --stop-after-hours 5
# when every range has run
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_point_and_mixed \
  mixed-merge n84
```

`mixed-replay` downloads the tarball at the pinned revision from the raw-file address,
`https://github.com/wand125/square-packing-bounds/raw/52af997dc91c579658f0828bc8304e306ad9d95b/`
followed by the upstream path, then from `raw.githubusercontent.com`, where that address
redirects, then by Git. It refuses the file unless its SHA-256 and size are the pinned
ones, unpacks it afresh, checks all 621 entries of its `files-sha256.json` and binds its
candidate, certificate, manifest and code to this packet and the September 28 copy before
importing any of it, repeats the driver’s preconditions in order, binds each oblique
input of the range to the candidate by an independent enclosure check, compiles the
shipped C++ with the shipped `compile_verifier`, and then calls the shipped per-angle
replay functions unchanged. An angle passes only if the function returns exactly the
record the retained `certificate.json` holds for it.

Each angle’s receipt is appended to `receipts/n84/range-AAA-BBB/directions.jsonl` and
synced, and the range’s `summary.json` rewritten, as soon as the angle finishes, so a
session can commit and push `receipts/` at any moment. Run again after an interruption,
the same command replays only the angles with no passing row. It exits 0 when its range
is complete, 3 when angles remain and none was refused, and 1 on a refusal. Disjoint
ranges write disjoint directories, so sessions’ receipts merge without conflict;
`mixed-merge` requires all 201 angles to have passed on runs bound to the pinned tarball.
`mixed-plan n84 --parts K` gives K ranges of equal estimated cost, with their commands.

**What a replay costs.** The shipped `compile_verifier` builds the checker with
`c++ -O2 -std=c++17 -ffp-contract=off -fno-fast-math`. Net index 100 of each
certificate was replayed alone, with `--workers 1`, on 2 October on a 4-core KVM guest
(Intel Xeon at 2.10 GHz) whose other three cores were busy: 195.8 CPU-seconds for
$n = 84$ and 182.0 for $n = 85$, each returning the certificate’s record. The receipts
are [`receipts/n84/range-100-100/`](receipts/n84/range-100-100/) and
[`receipts/n85/range-100-100/`](receipts/n85/range-100-100/). With index 100 of
$n = 65$ (237.1 s), they put a checker node at $6.42 \times 10^{-7}$ CPU-seconds per
rectangle of the measure, all three within 3 per cent. `mixed-price` scales that by each
certificate’s own node counts: about 11.7 CPU-hours for $n = 84$ and 10.2 for $n = 85$,
or 3 and 2.5 hours of wall time at four workers. On a busier guest, $n = 50$’s complete
replay took twice its estimate, so a session should allow for that.

## Complete Replays Here, 2 October 2026

Each certificate was replayed over all 201 directions in two `mixed-replay` runs of four
workers on shared 4-core x86-64 Linux containers (Intel Xeon, `c++` 13.3.0, one BLAS
and OpenMP thread, `PYTHONOPTIMIZE` unset), each run bound to the pinned tarball, and
`mixed-merge` printed `FULL_REPLAY_MATCHES_SHIPPED`: every direction returned the record
the certificate holds, the axis direction its cells and integer minimum and each oblique
direction its node count and lower bound.

| Certificate | Directions | Least oblique bound (index) | Axis cells, minimum | CPU-hours | Receipts |
| --- | ---: | --- | --- | ---: | --- |
| `mixed_n84_L940` | 201 | $1.0000000008975796$ (175) | 18,198,756, $1.0083383947166207$ | 12.29 | [`receipts/n84/`](receipts/n84/) |
| `mixed_n85_L942` | 201 | $1.0000000017271347$ (44) | 15,784,729, $1.013816765469528$ | 9.77 | [`receipts/n85/`](receipts/n85/) |

Each `merged.json` is the merged verdict, and `mixed-merge NAME --check` re-derives it.
The runs replay the source’s own checker and per-angle functions, so they confirm the
source’s runs rather than deciding coverage a second way.
The checker’s controls are the $n = 37$ ones of the
[October 1 packet](../wand125-point-and-mixed-2026-10-01/README.md#controls-for-the-mixed-checker),
made with the same checker bytes and compile; no mutation of these two certificates was
run.

## Where the Request and the Retained Files Differ

- **The comparison value is below Green’s bound.** Each `completion-audit.json` compares
  with `92667/10000` and states `improvement_lower` as $1333/10000$ and $1533/10000$.
  $9.2667$ is below Green’s $9.26673353\ldots$, so neither figure is a lower bound on the
  improvement: the margins are $0.13326646\ldots$ and $0.15326646\ldots$. The root
  README’s “by `0.133` and `0.153`” is right to the places it gives.
- **The least bound at $n = 84$.** The directory README gives $1.0000000009$, rounded;
  the root README and the request give $1.0000000008\ldots$, truncated. The certificate
  records $1.0000000008975796$.
- **Files in the bundle.** Each README says the tarball holds 622 files and that the
  second replay checked 621 file hashes. Both are right: `files-sha256.json` lists the
  other 621.
- **Where the second replay ran.** The request says each full replay was run again from
  the published tarball on a separate machine.
  The READMEs say it was run again from the tarball and do not say where.
  Inside each tarball, `bundle.json` records the replay on macOS 26.2 on arm64 under
  Python 3.12.2 and NumPy 1.26.4, and the manifests name candidates under `/opt/sp/runs/`;
  that is consistent with the request and was not checked further.
- **The comparison notes.** Each `compared_note` names a “published rectangle” value,
  $9.2225$ at $n = 84$ and $9.2325$ at $n = 85$, which no retained packet and no case
  record here holds. This record reports Green’s $9.2667\ldots$ at both counts, by
  monotonicity from $n = 82$.
- **Neighbouring counts.** The READMEs link `mixed_n87_L939`, which is in the tree at
  this revision and below the source’s rectangle certificate at $n = 87$; it is not
  retained here.

## Limitations

- **One implementation.** The complete replays run the source’s checker, so coverage is
  decided by one C++ program; the axis tables are a second implementation for one
  direction only. Every other statement above is read from the retained files,
  recomputed by the exact audit, or a digest comparison.
- **The bundles are pinned and not held.** A replay needs the tarballs from the source at
  the pinned revision; each must have the digest above.
  On 2 October the session’s egress policy refused the raw-file address
  `github.com/wand125/square-packing-bounds/raw/…` with a 403 and allowed
  `raw.githubusercontent.com` and Git, which is why `mixed-replay` tries all three.

## Compressed Files

Four upstream data files of more than 1,000 lines are stored as deterministic gzip made
by `gzip -9n`: the two candidates and the two certificates.
Each has no file name or timestamp in its header.
The table gives the Git blob and SHA-256 of the decompressed bytes, which are the file’s
blob and digest at the pinned commit; each SHA-256 is also the one
[`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) pins.
The repository’s readers take the upstream path and decompress through
`devtools.retained_data.read_retained_bytes`, and
`python -m devtools.retained_data check PACKET` re-derives every row.

Before running any of the source’s own programs on this packet, restore the exact
upstream tree from the repository root:

```sh
find packing/resources/web/wand125-mixed-bounds-2026-10-02 -name '*.gz' -exec gunzip -k {} +
```

The restored plain files are untracked, so remove them afterwards; while both copies are
present, the acquisition check reports each as retained twice.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `square-packing-bounds/certificates/mixed_n84_L940/candidate.json.gz` | upstream | `9c9ad0cfe6d0fc25c991bd0861e7260f395bbfcb` | `5d9e8e601fdd1490c870a38512a8893a14b901a713b5e0c4ab430de04b95c53b` |
| `square-packing-bounds/certificates/mixed_n84_L940/certificate.json.gz` | upstream | `4f4995db590e07fce974f94559bb6d08b08dae53` | `a663ffe2b346626b6c34e13d07ad2b94ee83ad6174c8821cd02b15f221bb0917` |
| `square-packing-bounds/certificates/mixed_n85_L942/candidate.json.gz` | upstream | `fb14c56a1c9d8431afbbb7cef950a0b518e77c64` | `b512d94ddfc755c9d3972a175b8a002b8496e932bb8e14e7f1cc961ea4d2e7fe` |
| `square-packing-bounds/certificates/mixed_n85_L942/certificate.json.gz` | upstream | `4a687795e25c76d11328b5e15769c0f8e35f4baf` | `13599f60c73cde0b1608d1628c20903097fb9b3ebee8363f4cebed880280b02f` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
