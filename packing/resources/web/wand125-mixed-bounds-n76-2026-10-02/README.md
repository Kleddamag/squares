# wand125 Mixed-Rectangle Certificate for n = 76, Pinned 2026-10-02

This packet pins one certificate directory of
[wand125/square-packing-bounds](https://github.com/wand125/square-packing-bounds) at its
commit of 2 October 2026 at 01:39 UTC, for one registration request: the rectangle-density
lower bound $s(76) \ge 447/50$, of the same kind as the two in the
[packet of the same morning](../wand125-mixed-bounds-2026-10-02/README.md), the five in
the [October 1 packet](../wand125-point-and-mixed-2026-10-01/README.md) and the
$s(50) \ge 37/5$ certificate in the
[September 28 packet](../wand125-point-and-mixed-2026-09-28/README.md). The request is
[a comment on jlevy/squares#282](https://github.com/jlevy/squares/issues/282#issuecomment-5943989352),
posted at 2026-10-02T01:39:56Z.

It is a packet of its own because its revision is later than the
[`52af997` packet](../wand125-mixed-bounds-2026-10-02/README.md)’s, and a later revision
is a new packet. Both revisions fall on the same UTC date, so this one’s name carries the
count. Its proposed Frontier key is **[wand125 mixed bounds n76 2026-10-02]**. The claim
below is stated as the source states it.
The certificate was not replayed here. What was checked is SHA-256 digests, Git blob
ids, the exact premises the audit below recomputes from the retained bytes, and every
check the replay makes before its first angle, run on the pinned tarball.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/wand125/square-packing-bounds> |
| Revision | `7975030a192607ef27edd1559aee4e98bd93047b`, branch `main`, tree `eda24e306e49a3c1434ce987c131f63142998676`; the revision the request names |
| Committed | Authored and committed 2026-10-02T01:39:38Z, 10:39 on 2 October by the author’s clock (`+09:00`). Its parent is `af1db07b`, which follows `52af997d` |
| Author | wand125, building on Tokoharu’s format and verifier, as for the other mixed certificates |
| Licence | MIT. The root `LICENSE` reads “Copyright (c) 2026 wand125”, is unchanged since `1a25a5ed` and is byte-identical to the [September 27 packet’s copy](../wand125-rectangle-certificates-2026-09-27/wand125-rectangles/LICENSE) |
| Retrieved | 2026-10-02T07:47Z: a blob-filtered clone of `main`, fetched when `main` was at `06eeb40c`, checked out sparse at this revision over the root `README.md`, `LICENSE` and `.gitignore` and the claim directory. `git ls-remote` listed one branch and no tag |
| Pinned subtree | 20 files, 12,186,668 bytes: the claim directory and the three root files, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256). The other 2,948 files of the tree are pinned by the commit alone |
| Retained here | 6 files, 204,212 bytes upstream and 70,496 bytes as stored, under [`square-packing-bounds/`](square-packing-bounds/), byte-identical to the pinned files after decompression |

**What the revision changed.** `git diff --stat af1db07 7975030` lists 18 files: the 17
of the new directory, and the root `README.md`, which gains a 14-line section “n = 76: a
structured certificate past the rectangle ladder”. Against `52af997` the root README also
has the `af1db07` section on $n = 101$, which the
[linear packet](../wand125-linear-certificates-2026-10-02/README.md) covers. No file of
the `52af997` packet’s scope changed.

**Later revisions.** When this packet was retrieved, `main` had moved on to `0c35d90`
(the $n = 83$ linear certificate) and `06eeb40c` (three Tokoharu-format rectangle
certificates, at $n = 59$, $77$ and $93$). Neither changes anything in this packet’s
scope: `git diff 7975030 06eeb40 -- certificates/mixed_n76_L894 LICENSE .gitignore` is
empty.

The directory has exactly one commit, the pinned one, with equal author and committer
dates.

| Claim | Directory | First commit | Committed (UTC) |
| --- | --- | --- | --- |
| $s(76) \ge 447/50$ | `certificates/mixed_n76_L894` | `7975030a192607ef27edd1559aee4e98bd93047b` | 2026-10-02T01:39:38Z |

## Credit and AI Assistance, as the Source States Them

The tree’s attribution files are unchanged since the
[`52af997` packet](../wand125-mixed-bounds-2026-10-02/README.md#credit-and-ai-assistance-as-the-source-states-them),
and so is what it says there: the root README’s Attribution section opens “The method is
not ours.”, and its Status section says “Parts of this work were produced with AI
assistance under human direction.”
The directory README calls the checker “the verifier shipped here,
`code/mixed_rotated_verify.cpp`, the same checker as for `mixed_n87_L939` and
`mixed_n65_L835`”, says the certificate is not in Tokoharu’s format because its least
oblique bound is below the $1.0001$ his `verify.cpp` requires, and says it supersedes the
source’s `rect_n76_L8925`. The `route` of its `completion-audit.json` reads “n76 Green
structured fresh at L8.94 (rectangles), full-net repair, 201-angle verification and
replay.” The commit message ends with the trailer
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## What Is Retained

Retained byte-identical at their upstream paths:

- from **`certificates/mixed_n76_L894/`**: `README.md`, `candidate.json`,
  `certificate.json`, `completion-audit.json` and `manifest.json`; and
- the root **`README.md`** (SHA-256 `9465a8ac…`, 46,229 bytes).

Pinned by digest only:

| Upstream path | Bytes | SHA-256 | Why not retained |
| --- | ---: | --- | --- |
| `LICENSE` | 1,064 | `c0dd43e7892932c81335f74a2fdbf1a98f5977bab14c0c4c30e3abcc97c34904` | Retained byte-identical by the September 27 rectangle packet |
| `.gitignore` | 132 | `0a31c24fe622ff8b4b012fbf790686063a84da3dd306d47e7283aad434653308` | A retained `.gitignore` would act on this repository’s tree; the October 1 packet quotes it |
| `certificates/mixed_n76_L894/n76-L8.94-proof-bundle.tar.gz` | 11,942,640 | `d804bb88f0fa5fd5cfa11aeccb4977f708a015879917c189c6d6511f1bbbef63` | Complete proof bundle |
| `certificates/mixed_n76_L894/code/*` | 38,614 in 10 | each in the subtree list | Each is byte-identical to the file of the same name in `mixed_n50_L740/code/`, which the [September 28 packet](../wand125-point-and-mixed-2026-09-28/README.md) retains |
| `certificates/mixed_n76_L894/requirements.txt` | 6 | `e09f656c130b9c08b2c5ab7187c891295e449ed77febea2a6ceee9cc98ccb0fc` | Byte-identical to `mixed_n50_L740/requirements.txt` in the same packet |

The tarball digest is also the one the directory’s README and `completion-audit.json`
state, and the audit’s `certificate_sha256` is the digest of the retained
`certificate.json`.

[`acquisition/declaration.json`](acquisition/declaration.json) declares the scope and
the pinned-only rules, and [`acquisition/sources.json`](acquisition/sources.json)
records the pin and every pinned-only file with its size, digest, reason and, where one
exists, the retained copy with the same bytes.
From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source \
  wand125-mixed-bounds-n76-2026-10-02 --checkout CHECKOUT
```

rebuilds the retained files and both acquisition files from a checkout at the pinned
revision, and with `--check` in place of `--checkout CHECKOUT` re-derives the packet from
its manifest without one. The tool is
[`devtools/acquire_source.py`](../../../devtools/acquire_source.py).

## The Claim, as the Source States It

| Claim | Directory | Measure | Total | Checks the source reports |
| --- | --- | --- | --- | --- |
| $s(76) \ge 447/50$ | `mixed_n76_L894` | 317 rectangles | $7599999/100000$ | `code/mixed_rotated_verify.cpp` at 200 oblique net angles and integer tables at angle zero; least oblique bound stated $1.0000000005$, axis minimum $1.007513$ |

The measure is a rectangle density with no point mass, at core side $B = 9977/10000$, 201
net half-angles of step $83/40000$ and coverage threshold $1$, as for the other mixed
certificates. Its `certificate.json` has status `ALL_ANGLES_VERIFIED_AND_REPLAYED`, and its
`replay_scope` says the oblique replay is “not a separate independent oblique
implementation”. The source compares it with its own `rect_n76_L8925` ($357/40$) and with
Nagamochi’s $1 + \sqrt{61} = 8.8102\ldots$.

## The Exact Audit and the Pre-Replay Checks

From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_point_and_mixed \
  mixed-audit wand125-mixed-bounds-n76-2026-10-02 --check
```

recomputes [`receipts/mixed-audit.json`](receipts/mixed-audit.json) from the retained
bytes, as for the [`52af997` packet](../wand125-mixed-bounds-2026-10-02/README.md#the-exact-audit),
and imports no source code. It passes. The candidate digest recomputed by the source’s
rule is `f2c25305…`. The least oblique bound recorded is $1.000000000516032$ at index
150, and the axis integer minimum $1.0075130139576551$ over 3,225,616 cells. The side
exceeds Nagamochi’s $1 + \sqrt{61}$ and Green’s Theorem 9 value for $k = 8$, the DS7
envelope’s strongest at $n = 76$. None of it decides coverage.

On 2 October `mixed-fetch n76` was run on the pinned tarball, read by Git from the
pinned commit: its SHA-256 and size are the pinned ones, its 621 listed files match its
`files-sha256.json`, its candidate, certificate, manifest and `code/` are the retained
files, the driver’s preconditions hold, and all 200 oblique inputs enclose the exact
candidate. The bundle’s records give the source’s own oblique run as 12,687 seconds.

## Replaying the Certificate

The certificate has not been replayed.
`devtools.audit_wand125_point_and_mixed` replays it by range, exactly as it does
$n = 84$ and $85$; the
[`52af997` packet](../wand125-mixed-bounds-2026-10-02/README.md#replaying-the-certificates)
describes the steps, the receipts and the exit codes. `mixed-price` estimates
2.2 CPU-hours from the three timed single angles of the mixed certificates, about
33 minutes of wall time at four workers, so one session can run it whole:

```sh
# from packing/, on a four-core runner
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_point_and_mixed \
  mixed-replay n76 --range 0-200 --work /tmp/wand125-n76 --workers 4 --via git
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_point_and_mixed \
  mixed-merge n76
```

`--via git` reads the tarball from a fetch of the pinned commit, which a proxy that
truncates raw-file downloads cannot cut short. The receipts land in `receipts/n76/`.

## Where the Request and the Retained Files Differ

- **The least bound.** The directory README and the request give $1.0000000005$; the
  certificate records $1.000000000516032$. Both are right to the places they give.
- **Files in the bundle.** The README says the tarball holds 622 files and the replay
  checked 621 file hashes; `files-sha256.json` lists the other 621, as at $n = 84$ and
  $85$.
- **Where the second replay ran.** The request says the replay was run again “on a
  separate machine”; the README says it was run again from the tarball and does not say
  where. This was not checked further.

## Limitations

- **Not replayed.** No angle of the 201 was replayed here. Every other statement above is
  read from the retained files, recomputed by the exact audit, checked by `mixed-fetch`,
  or a digest comparison.
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
find packing/resources/web/wand125-mixed-bounds-n76-2026-10-02 -name '*.gz' -exec gunzip -k {} +
```

The restored plain files are untracked, so remove them afterwards; while both copies are
present, the acquisition check reports each as retained twice.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `square-packing-bounds/certificates/mixed_n76_L894/candidate.json.gz` | upstream | `d58f65b9a3f055fb4b7ac769e961f5ffe29e2551` | `ea72baaec46dfced229a854e367c7bf008281b15f4835c2015bb8bb58baf9d21` |
| `square-packing-bounds/certificates/mixed_n76_L894/certificate.json.gz` | upstream | `b1d5ea423a30136144a7ea443f2da259a7de36b4` | `f5b87ee10b9ac66ea6f48075ca671c8a7a61efd4392b2f8f2069c4ea13153d11` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
