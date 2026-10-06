# wand125 Mixed-Rectangle Certificates for n = 83, 85, 87, 91, 92 and 96, Pinned 2026-10-02

This packet pins six certificate directories of
[wand125/square-packing-bounds](https://github.com/wand125/square-packing-bounds) at its
commit of 2 October 2026 at 15:16 UTC, for five comments of that afternoon on
[jlevy/squares#282](https://github.com/jlevy/squares/issues/282): six rectangle-density
lower bounds, $s(83) \ge 937/100$, $s(85) \ge 473/50$, $s(87) \ge 237/25$,
$s(91) \ge 97/10$, $s(92) \ge 39/4$ and $s(96) \ge 249/25$. They are of the kind and
checker of the two in the [`52af997` packet](../wand125-mixed-bounds-2026-10-02/README.md),
the one in the [`7975030` packet](../wand125-mixed-bounds-n76-2026-10-02/README.md), the
five in the [October 1 packet](../wand125-point-and-mixed-2026-10-01/README.md) and the
$s(50) \ge 37/5$ certificate in the
[September 28 packet](../wand125-point-and-mixed-2026-09-28/README.md).

Two of the six supersede certificates this record already holds at the same count:
`mixed_n85_L946` the `52af997` packet’s `mixed_n85_L942`, and `mixed_n92_L975` the
October 1 packet’s `mixed_n92_L969`. A third, `mixed_n83_L937`, is above the linear
$s(83) \ge 187/20$ of the
[linear packet](../wand125-linear-certificates-2026-10-02/README.md). The six were
committed in four revisions between 11:38 and 15:16 UTC and are pinned together at the
last, which holds all six unchanged. Its proposed Frontier key is
**[wand125 mixed bounds afternoon 2026-10-02]**. The claims below are stated as the
source states them.
All six were replayed here in full on 2 and 3 October, every direction matching the
source’s record. Before any replay, what was checked is SHA-256 digests, Git blob ids, the exact premises the audit below
recomputes from the retained bytes, and every check the replay makes before its first
angle, run on each pinned tarball.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/wand125/square-packing-bounds> |
| Revision | `b00fc70f1904e9b1b567afee056d347f911209e8`, branch `main`, tree `03f0999d13d1c1462d15471908b43628f38bb01d`; the head when retrieved, and the revision the last request names |
| Committed | Authored and committed 2026-10-02T15:16:36Z, 00:16 on 3 October by the author’s clock (`+09:00`). The commit’s author name is Hiroaki Hosono |
| Author | wand125, building on Tokoharu’s format and verifier, as for the other mixed certificates |
| Licence | MIT. The root `LICENSE` reads “Copyright (c) 2026 wand125”, is unchanged since `1a25a5ed` and is byte-identical to the [September 27 packet’s copy](../wand125-rectangle-certificates-2026-09-27/wand125-rectangles/LICENSE) |
| Retrieved | 2026-10-02T16:53Z: a depth-1 clone of `main` at this revision. Commit dates and the history of each directory are from a blob-filtered clone of the whole history fetched in the same session. `git ls-remote` listed one branch and no tag |
| Pinned subtree | 105 files, 95,503,159 bytes: the six claim directories and the three root files, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256). The whole tree of 3,167 files is pinned file by file in the [2026-10-02 rectangle packet](../wand125-rectangle-certificates-2026-10-02/acquisition/upstream-tree.sha256) |
| Retained here | 30 files, 1,086,472 bytes upstream and 176,477 bytes as stored, under [`square-packing-bounds/`](square-packing-bounds/), byte-identical to the pinned files after decompression |

**The revisions.** The source’s `main` moved from `0c35d909`, the
[linear packet](../wand125-linear-certificates-2026-10-02/README.md)’s pin, through ten
commits on 2 October, each of which also changes the root README:

| Commit | Committed (UTC) | Changes | Pinned by |
| --- | --- | --- | --- |
| `06eeb40c` | 05:58:20 | adds `rect_n59_L79375`, `rect_n77_L894` and `rect_n93_L973` | the [2026-10-02 rectangle packet](../wand125-rectangle-certificates-2026-10-02/README.md), the first two |
| `7d770221` | 08:25:06 | adds `rect_n70_L86275` | the rectangle packet |
| `23e22840` | 09:27:11 | re-hashes the bundles of eleven earlier mixed certificates and withdraws `mixed_n50_L7318` | [What `23e2284` Changed](#what-23e2284-changed) |
| `c5454ae0` | 10:44:29 | adds `mixed_n96_L992`, $s(96) \ge 248/25$ from 195 rectangles | nothing: `mixed_n96_L996` supersedes it |
| `028b9155` | 11:38:12 | adds `mixed_n85_L946` | this packet |
| `58f153f8` | 12:33:44 | adds the linear `mixed_n82_L932` | the [linear $n = 82$ packet](../wand125-linear-n82-2026-10-02/README.md) |
| `4318bdf9` | 13:37:33 | adds `rect_n20_L49`, `rect_n42_L68275`, `rect_n91_L96475` and `rect_n93_L9735` | the rectangle packet |
| `6e4e9786` | 13:49:30 | adds `mixed_n87_L948`, `mixed_n91_L970` and `mixed_n92_L975` | this packet |
| `25c421d5` | 14:46:34 | adds `mixed_n83_L937` | this packet |
| `b00fc70f` | 15:16:36 | adds `mixed_n96_L996` | this packet |

Each directory here has exactly one commit, with equal author and committer dates:

| Claim | Directory | First commit | Committed (UTC) |
| --- | --- | --- | --- |
| $s(83) \ge 937/100$ | `certificates/mixed_n83_L937` | `25c421d57f29320aa0b57c06645d6bac917c8ed1` | 2026-10-02T14:46:34Z |
| $s(85) \ge 473/50$ | `certificates/mixed_n85_L946` | `028b915515f9970ece02e51e079e0fb1e87589e6` | 2026-10-02T11:38:12Z |
| $s(87) \ge 237/25$ | `certificates/mixed_n87_L948` | `6e4e97863ecf9c8f3814a0d9420aa2af629564d7` | 2026-10-02T13:49:30Z |
| $s(91) \ge 97/10$ | `certificates/mixed_n91_L970` | `6e4e97863ecf9c8f3814a0d9420aa2af629564d7` | 2026-10-02T13:49:30Z |
| $s(92) \ge 39/4$ | `certificates/mixed_n92_L975` | `6e4e97863ecf9c8f3814a0d9420aa2af629564d7` | 2026-10-02T13:49:30Z |
| $s(96) \ge 249/25$ | `certificates/mixed_n96_L996` | `b00fc70f1904e9b1b567afee056d347f911209e8` | 2026-10-02T15:16:36Z |

The requests are the comments on issue 282 posted
[at 11:38:35Z](https://github.com/jlevy/squares/issues/282#issuecomment-5951548018)
($n = 85$),
[at 13:49:57Z](https://github.com/jlevy/squares/issues/282#issuecomment-5953839070)
($n = 87$, 91 and 92),
[at 14:46:58Z](https://github.com/jlevy/squares/issues/282#issuecomment-5954944553)
($n = 83$) and
[at 15:16:57Z](https://github.com/jlevy/squares/issues/282#issuecomment-5955463430)
($n = 96$). The comment
[at 10:46:15Z](https://github.com/jlevy/squares/issues/282#issuecomment-5950682288)
asked for `mixed_n96_L992`, which the last one supersedes.

## Credit and AI Assistance, as the Source States Them

The tree’s attribution files are unchanged since the
[`52af997` packet](../wand125-mixed-bounds-2026-10-02/README.md#credit-and-ai-assistance-as-the-source-states-them),
and so is what the root README says there: its Attribution section opens “The method is
not ours.” and credits Walter Stromquist, Hiroshi Nagamochi, Sam Burns, Gustavo
Massaccesi and this repository, and its Status section says “Parts of this work were
produced with AI assistance under human direction.”

- **The six certificates.** Each directory README calls the checker “the verifier shipped
  here, `code/mixed_rotated_verify.cpp`, the same checker as for `mixed_n87_L939`” and
  `mixed_n65_L835`, and says the certificate is not in Tokoharu’s format because its least
  oblique bound is below the $1.0001$ his `verify.cpp` requires. Each says the candidate
  was built from scratch at its side from a structured initial measure and repaired
  against counterexamples on the full net, and five name the certificate they supersede;
  the `route` of each `completion-audit.json` says the same.
- **The pre-publication replays.** Each README says the full 201-angle replay was run
  again from the bundle on a fresh Ubuntu 24.04 machine with only the README’s
  requirements installed. The $n = 83$ and $n = 85$ READMEs add that it ran on a copy of
  the bundle that “differs only in the provenance line of `bundle.json`”, the line
  `23e2284` made relative. This was not checked.
- **The commits.** Each of the four commit messages ends with a co-author trailer naming
  an AI assistant.

## What Is Retained

Retained byte-identical at their upstream paths, from each of the six directories:
`README.md`, `candidate.json`, `certificate.json`, `completion-audit.json` and
`manifest.json`.

Pinned by digest only:

| Upstream path | Bytes | SHA-256 | Why not retained |
| --- | ---: | --- | --- |
| `README.md` | 49,934 | `23a1fa07abc80b5e8d25ea46e2fc609a5173746985eff2018cfb2611b9b499df` | Retained byte-identical by the [2026-10-02 rectangle packet](../wand125-rectangle-certificates-2026-10-02/wand125-rectangles/README.md), pinned at the same revision |
| `LICENSE` | 1,064 | `c0dd43e7892932c81335f74a2fdbf1a98f5977bab14c0c4c30e3abcc97c34904` | Retained byte-identical by the September 27 rectangle packet |
| `.gitignore` | 132 | `0a31c24fe622ff8b4b012fbf790686063a84da3dd306d47e7283aad434653308` | A retained `.gitignore` would act on this repository’s tree; the October 1 packet quotes it |
| `certificates/mixed_n83_L937/n83-L9.37-proof-bundle.tar.gz` | 29,567,366 | `cbf81b21c271b4297036d71eae4948eacabece39fd14d092757a3a5748b9c9c7` | Complete proof bundle |
| `certificates/mixed_n85_L946/n85-L9.46-proof-bundle.tar.gz` | 22,008,842 | `d518b3a95c337361f58d66f520b1fe91ca2e41ffb37bdbb53c7c3235e7ec768c` | Complete proof bundle |
| `certificates/mixed_n87_L948/n87-L9.48-proof-bundle.tar.gz` | 10,985,416 | `c77d8ea193dc345feda1a6000f7e893c861f8f65ca922fb6270689129dd54d28` | Complete proof bundle |
| `certificates/mixed_n91_L970/n91-L9.70-proof-bundle.tar.gz` | 10,533,804 | `56174c72cae492ad957efba93810e5d671702ae3fe0496ef2d78e501aa6e9934` | Complete proof bundle |
| `certificates/mixed_n92_L975/n92-L9.75-proof-bundle.tar.gz` | 11,901,503 | `1f61a64007a9fdc99158c220529d55c8c54da28dca08680720dc9ab8373b5cd3` | Complete proof bundle |
| `certificates/mixed_n96_L996/n96-L9.96-proof-bundle.tar.gz` | 9,136,906 | `5fc6195b1ba4d1e609acf7b2108bcef93869d463ebfe0542d401137a23818b6f` | Complete proof bundle |
| `certificates/mixed_*/code/*` | 231,684 in 60 | each in the subtree list | Each is byte-identical to the file of the same name in `mixed_n50_L740/code/`, which the [September 28 packet](../wand125-point-and-mixed-2026-09-28/README.md) retains |
| `certificates/mixed_*/requirements.txt` | 6 in each of 6 | `e09f656c130b9c08b2c5ab7187c891295e449ed77febea2a6ceee9cc98ccb0fc` | Byte-identical to `mixed_n50_L740/requirements.txt` in the same packet |

Each tarball digest is also the one its directory’s README and `completion-audit.json`
state, and each audit’s `certificate_sha256` is the digest of the retained
`certificate.json`. Each tarball’s `proof/candidate.json`, `proof/certificate.json` and
`proof/manifest.json` are the retained files, and its `code/` is the retained
`mixed_n50_L740/code/`, as `mixed-fetch` below establishes.

[`acquisition/declaration.json`](acquisition/declaration.json) declares the scope and
the pinned-only rules, and [`acquisition/sources.json`](acquisition/sources.json)
records the pin and every pinned-only file with its size, digest, reason and, where one
exists, the retained copy with the same bytes.
From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source \
  wand125-mixed-bounds-afternoon-2026-10-02 --checkout CHECKOUT
```

rebuilds the retained files and both acquisition files from a checkout at the pinned
revision, and with `--check` in place of `--checkout CHECKOUT` re-derives the packet from
its manifest without one. The tool is
[`devtools/acquire_source.py`](../../../devtools/acquire_source.py).

## The Claims, as the Source States Them

| Claim | Directory | Rectangles | Source’s comparison | Least oblique bound recorded | Axis minimum |
| --- | --- | ---: | --- | --- | --- |
| $s(83) \ge 937/100$ | `mixed_n83_L937` | 728 | $92667/10000$, “inherited Green n82 9.266733” | $1.0000000002030356$ at index 165 | $1.0063110587189603$ |
| $s(85) \ge 473/50$ | `mixed_n85_L946` | 525 | $92667/10000$, “inherited Green n82 9.266733” | $1.0000000021147502$ at index 182 | $1.0025322687268394$ |
| $s(87) \ge 237/25$ | `mixed_n87_L948` | 299 | $92667/10000$, “record n87 9.46 via n85 9.46 monotonicity” | $1.0000000089739896$ at index 176 | $1.013387013743792$ |
| $s(91) \ge 97/10$ | `mixed_n91_L970` | 288 | $1929/200$, “record n91 9.645” | $1.0000000003906073$ at index 191 | $1.005778849360574$ |
| $s(92) \ge 39/4$ | `mixed_n92_L975` | 324 | $969/100$, “our published n92 9.69” | $1.0000000022907243$ at index 191 | $1.008723611315222$ |
| $s(96) \ge 249/25$ | `mixed_n96_L996` | 279 | $248/25$, “our published n96 9.92 (Nagamochi reference 9.8882, unproven)” | $1.0000000030392873$ at index 122 | $1.0056403520432675$ |

All six are rectangle densities with no point mass (each `candidate.json` has an empty
`points` list and a `scaling_factor` of `1`), of total mass $n - 1/100000$, with core side
$B = 9977/10000$, 201 net half-angles of step $83/40000$ and coverage threshold $1$, as
for every earlier mixed certificate. Each `certificate.json` has status
`ALL_ANGLES_VERIFIED_AND_REPLAYED`, and its `replay_scope` says the oblique replay is
“not a separate independent oblique implementation”. The source’s comparisons are its own
earlier values at $n = 91$, 92 and 96, and at $n = 83$, 85 and 87 Green’s reported
$9.2667\ldots$ for $n = 82$ to $85$ (Friedman DS7, Theorem 9 with $k = 9$).

## The Exact Audit and the Pre-Replay Checks

From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_point_and_mixed \
  mixed-audit wand125-mixed-bounds-afternoon-2026-10-02 --check
```

recomputes [`receipts/mixed-audit.json`](receipts/mixed-audit.json) from the retained
bytes and imports no source code.
For each certificate it requires every retained file to have its pinned digest; the
count, side, core and rectangle count stated; nonnegative masses inside the container,
of total exactly $n - 1/100000$; the candidate digest, recomputed by the source’s rule,
equal in the manifest, the certificate, the source’s audit and the statement; the net
record equal to the containment facts recomputed here; the checker `89b674a6…` and
`code/` the retained $n = 50$ copy; a replay record at threshold $1$ for each of the 201
angles; and the source audit’s certificate and tarball digests.

All six pass. Each side exceeds Green’s DS7 value at its count, enclosed to 60 digits,
and Nagamochi’s $1 + \sqrt{n - 2\lfloor\sqrt n\rfloor + 1}$. None of it decides coverage.

On 2 October `mixed-fetch` was run on each pinned tarball, read from the depth-1 clone
at the pinned commit. Each has the pinned SHA-256 and size; each unpacked bundle matches
all 621 entries of its `files-sha256.json` with nothing unlisted, and its candidate,
certificate, manifest, `code/`, `proof/verify.cpp` and `requirements.txt` are the
retained or `mixed_n50_L740` files; the shipped driver’s preconditions hold on its own
code; every one of the 200 oblique inputs encloses the exact candidate recomputed here
(5,824, 4,200, 2,392, 2,304, 2,592 and 2,232 rectangle images); and every record is
`ANGLE_VERIFIED` with an empty frontier at $\gamma = 1$. The bundles record the source’s
own oblique runs as 44,833, 27,379, 7,758, 7,792, 6,744 and 8,827 seconds, in the order
of the table above. Each run’s output is its certificate’s `receipts/NAME/fetch.json`,
for instance [`receipts/n83/fetch.json`](receipts/n83/fetch.json); the `bundle` field
names the scratch directory it was unpacked in.

## Replaying the Certificates

All six have been replayed here; see the next section. The source’s check is its driver
`code/verify_mixed_full_proof.py`, run from the unpacked tarball.
`devtools.audit_wand125_point_and_mixed` runs the same check split by net angle, as for
the earlier mixed packets. The tool names the six `n83`, `n85-L946`, `n87`, `n91`,
`n92-L975` and `n96`: a count an earlier certificate already names takes its side as
well. One command per batch:

```sh
# from packing/, one range per session; 0 is the axis direction
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_point_and_mixed \
  mixed-replay n83 --range 0-86 --work /tmp/wand125-n83 --workers 4 --via git \
  --stop-after-hours 1.6
# when every range has run
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_point_and_mixed \
  mixed-merge n83
```

Receipts go to `receipts/NAME/range-AAA-BBB/` as each angle finishes, and a rerun
replays only what has not passed.
`mixed-price` scales the rate of the three angles timed on 2 October by each
certificate’s own node counts: about 16.0 CPU-hours for $n = 83$, 8.3 for $n = 85$, and
2.0, 1.6, 1.9 and 1.6 for $n = 87$, 91, 92 and 96. `mixed-plan NAME --parts K` gives K
ranges of equal estimated cost; for $n = 83$ four parts are 0–86, 87–135, 136–171 and
172–200, about 4 CPU-hours each, and for $n = 85$ two are 0–134 and 135–200. On a busier
guest $n = 50$’s complete replay took twice its estimate.

## Complete Replays Here, 2 and 3 October 2026

The six certificates were replayed over all 201 directions in `mixed-replay` runs of four
workers on shared 4-core x86-64 Linux containers (Intel Xeon at 2.1 or 2.8 GHz, `c++`
13.3.0 at `-O2 -ffp-contract=off -fno-fast-math`, one BLAS and OpenMP thread,
`PYTHONOPTIMIZE` unset), each run bound to the pinned tarball, and `mixed-merge` printed
`FULL_REPLAY_MATCHES_SHIPPED`: every direction returned the record the certificate holds,
the axis direction its cells and integer minimum and each oblique direction its node
count and lower bound. $n = 83$ ran as the four ranges of `mixed-plan n83 --parts 4` in
two sessions and $n = 85$ as two ranges; the others ran whole.

| Certificate | Directions | Least oblique bound (index) | Axis cells, minimum | CPU-hours | Receipts |
| --- | ---: | --- | --- | ---: | --- |
| `mixed_n83_L937` | 201 | $1.0000000002030356$ (165) | 21,808,900, $1.0063110587189603$ | 16.26 | [`receipts/n83/`](receipts/n83/) |
| `mixed_n85_L946` | 201 | $1.0000000021147502$ (182) | 12,694,969, $1.0025322687268394$ | 9.74 | [`receipts/n85-L946/`](receipts/n85-L946/) |
| `mixed_n87_L948` | 201 | $1.0000000089739896$ (176) | 2,866,249, $1.013387013743792$ | 2.66 | [`receipts/n87/`](receipts/n87/) |
| `mixed_n91_L970` | 201 | $1.0000000003906073$ (191) | 2,748,964, $1.005778849360574$ | 2.35 | [`receipts/n91/`](receipts/n91/) |
| `mixed_n92_L975` | 201 | $1.0000000022907243$ (191) | 3,560,769, $1.008723611315222$ | 2.67 | [`receipts/n92-L975/`](receipts/n92-L975/) |
| `mixed_n96_L996` | 201 | $1.0000000030392873$ (122) | 1,420,864, $1.0056403520432675$ | 2.43 | [`receipts/n96/`](receipts/n96/) |

Each `merged.json` is the merged verdict, and `mixed-merge NAME --check` re-derives it;
`mixed-audit wand125-mixed-bounds-afternoon-2026-10-02 --check` reads all six as
`FULL_REPLAY_MATCHES_SHIPPED`. The runs replay the source’s own checker and per-angle
functions, so they confirm the source’s runs rather than deciding coverage a second way.
The checker’s controls are the $n = 37$ ones of the
[October 1 packet](../wand125-point-and-mixed-2026-10-01/README.md#controls-for-the-mixed-checker),
made with the same checker bytes and compile; no mutation of these certificates was run
with the source’s checker.

## The Independent Decisions, 3 and 6 October 2026

`sqverify-fast`, this repository’s clean-room measure verifier, decided all six retained
candidates at all 201 net directions in its census of 3 October 2026, from the reviewed
crate source `9985c465…`, and on 6 October `devtools.sqverify_fast_census --control`
refused two mutants of each at its least-bound direction: every mass scaled by 99/100,
and a near-threshold scaling. The receipts are in
[`benchmarks/measure-verifier/census-mixed/`](../../../benchmarks/measure-verifier/census-mixed/README.md),
and each certificate’s evidence entry `E-…-sqverify-fast-replay` states its run.
The verifier shares no code with the source’s checker and runs the same method, so these
are a second implementation beside the replays above, not a second method, and they move
no rung.

## What `23e2284` Changed

The source’s commit `23e22840` (2026-10-02T09:27:11Z) says it removes local paths from
the proof bundles and records and withdraws `mixed_n50_L7318`, and that “Certificates,
candidates and proofs are unchanged.” Each of the eleven re-hashed tarballs was read
here at its parent `7d770221` and at `23e22840`, and unpacked: each holds the same 622
members, and only two differ, `bundle.json`, whose `source_run` changes from an
absolute path on the author’s machine to a relative one, and `files-sha256.json`,
whose one changed entry is `bundle.json`’s digest. The certificates are `mixed_n37_L644`,
`mixed_n50_L740`, `mixed_n65_L835`, `mixed_n66_L842`, `mixed_n76_L894`,
`mixed_n84_L940`, `mixed_n85_L942`, `mixed_n87_L939`, `mixed_n87_L940`,
`mixed_n90_L960` and `mixed_n92_L969`. The same commit rewrites the tarball digest in
each of their READMEs and `completion-audit.json` files, the `bundle` path in
`mixed_n50_L740/completion-audit.json`, and the command paths in three files of
`point_n21_L5/acceptance/`, with the digests that cite them.

Every packet here that pins one of those tarballs pins it at a revision before
`23e2284`, with the old digest, and that digest is the bytes at `7d770221`. Those
revisions remain in the source’s history, so `--via git` still fetches them, and no
retained file, receipt or claim changes. The six bundles of this packet were built after
`23e2284` and record relative paths. `mixed_n50_L7318` was never registered here.

## Where the Requests and the Retained Files Differ

- **The comparison value is below Green’s bound.** At $n = 83$, 85 and 87 the
  `completion-audit.json` compares with $92667/10000$ and states `improvement_lower` as
  $1033/10000$, $1933/10000$ and $2133/10000$. $9.2667$ is below Green’s
  $9.26673353\ldots$, so none of the three is a lower bound on the improvement, as at
  $n = 84$ and 85 in the `52af997` packet. The bounds themselves are unaffected.
- **Nagamochi’s value as a reference.** The $n = 96$ audit calls Nagamochi’s
  $1 + \sqrt{79} = 9.8882\ldots$ “unproven”, and the root README and the comments call his
  closed form “a reference value” and cite
  [jlevy/squares#295](https://github.com/jlevy/squares/issues/295), which reports that
  the lemma behind it is false. This record holds that bound as verified at $n = 96$.
  The comparison facts in the audit receipt state it, and no claim here rests on it.
- **The record at $n = 87$.** The `compared_note` at $n = 87$ calls 9.46 “the record”, by
  monotonicity from the $n = 85$ certificate of this packet; this record holds 9.41 at
  $n = 87$ until that certificate is registered.
- **The comparison notes.** The `compared_note` at $n = 83$ names a “published rectangle”
  value of 9.15 and at $n = 85$ one of 9.2325, which no retained packet and no case record
  holds.

## Limitations

- **The replays are the source’s own checker and one independent implementation.**
  Coverage is decided by the source’s C++ and by `sqverify-fast`, which share the
  method; neither is a second method.
- **The bundles are pinned and not held.** A replay needs each tarball from the source at
  the pinned revision, with the digest above. `--via git` fetches it by Git; the raw-file
  address has been refused by a session proxy before.

## Compressed Files

Twelve upstream data files of more than 1,000 lines are stored as deterministic gzip made
by `gzip -9n`: the six candidates and the six certificates. Each has no file name or
timestamp in its header.
The table gives the Git blob and SHA-256 of the decompressed bytes, which are the file’s
blob and digest at the pinned commit; each SHA-256 is also the one
[`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) pins.
The repository’s readers take the upstream path and decompress through
`devtools.retained_data.read_retained_bytes`, and
`python -m devtools.retained_data check PACKET` re-derives every row.

Before running any of the source’s own programs on this packet, restore the exact
upstream tree from the repository root:

```sh
find packing/resources/web/wand125-mixed-bounds-afternoon-2026-10-02 -name '*.gz' -exec gunzip -k {} +
```

The restored plain files are untracked, so remove them afterwards; while both copies are
present, the acquisition check reports each as retained twice.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `square-packing-bounds/certificates/mixed_n83_L937/candidate.json.gz` | upstream | `cf2f3db2199b36f33e98094a4889055e0507449b` | `00b58230f08fa4dcd3671b3be5c6f1cb262db248b9e9a7d2563b1a497845f113` |
| `square-packing-bounds/certificates/mixed_n83_L937/certificate.json.gz` | upstream | `be841ffee5485ebb50556b784a345447b68b70e8` | `efbb5f80502a18a2478a77d40747bdb5397a6c3776d5b0986a7e841ec3eabd1b` |
| `square-packing-bounds/certificates/mixed_n85_L946/candidate.json.gz` | upstream | `36605812bee93a9f5cd3680c3e35657fb230b909` | `e0b3c193bc5f09de74e5d5657539398837edc7a8a99c74aa1e4b673e7e67c5fc` |
| `square-packing-bounds/certificates/mixed_n85_L946/certificate.json.gz` | upstream | `d97d4089ae03b8675e3148f56334bfb592f84aee` | `fcf31940d5cff05116e2631d14289e3a2c8d9f5a4f5b805870fd5d9f12eed5f8` |
| `square-packing-bounds/certificates/mixed_n87_L948/candidate.json.gz` | upstream | `df00718bb002e5bf5cfcc8ce0ee0f364e553708e` | `d0afb6ca0ddb4038d97cd2e95513e3dd0d46e18b4f5c8e1eed9c3e543a427b89` |
| `square-packing-bounds/certificates/mixed_n87_L948/certificate.json.gz` | upstream | `a3405fdd002d65473a123bb4f98980a594c89f29` | `2a27d2cfe82cbe35c2c7a45d659524b1f408877c0c86be496195696e5d5aea0b` |
| `square-packing-bounds/certificates/mixed_n91_L970/candidate.json.gz` | upstream | `a472b3b196052bd33fb171fb5083b2c933b7e353` | `469ff2ebdf7aca6b5052f4025bd7e1f1d7aa1d3edc4a6c3dadfbdc28a67f3261` |
| `square-packing-bounds/certificates/mixed_n91_L970/certificate.json.gz` | upstream | `ddf44981bf43c50c6f422abefc5e9a0d927c85a0` | `552405d3912b46be608cb1b4299ee63c1f5bba59de691673b094eabadaea7cb8` |
| `square-packing-bounds/certificates/mixed_n92_L975/candidate.json.gz` | upstream | `3756a5455bf0f9838c060cf6c21f9c0e837b1550` | `22679fc4b83af56c438131050c9c96abfc5880f2b2dd46099b3b400a90a62454` |
| `square-packing-bounds/certificates/mixed_n92_L975/certificate.json.gz` | upstream | `3ab5d0b1e775a4fa23af02e47fa357624112ed8e` | `156507faaf5f94427cebb76d80b3d93f170ce60a73ae5c95016d5c7495840b55` |
| `square-packing-bounds/certificates/mixed_n96_L996/candidate.json.gz` | upstream | `134f48940aef1cd7c11e4eb4779ccb0d05edcd86` | `ae2eda591561f74ebb81735470e8b623f8a8f5afbe3531026517b3fc1d0826f1` |
| `square-packing-bounds/certificates/mixed_n96_L996/certificate.json.gz` | upstream | `94121383ce1861f251427721835d102fb2cf9453` | `dd16ead7d61ced57b5369dbde0928ead95a827c7d8b0293ce0678aadca964f59` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
