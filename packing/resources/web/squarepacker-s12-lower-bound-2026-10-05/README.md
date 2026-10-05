# squarepacker’s `s(12) ≥ 7943/2000`, v1.1, Pinned 2026-10-05

Ryu Sungjoon (GitHub `squarepacker`) reports `s(12) ≥ 7943/2000 = 3.9715`, which is
`10266889/7898846000`, about `0.0013`, above this record’s verified
`s(12) ≥ 15680000/3949423` (`T-079`).
The certificate keeps Evan Daniel’s 1,736 points of `s12_lower_3.9686.txt` (`T-049`),
dilated to the container `7943/2000` and rounded to the grid `1/4000000` one symmetry
orbit at a time, with new weights found by linear programming: all 223 orbits positive,
total `119974808/10⁷ < 12`.
Daniel’s verifier and the author’s own checker accept it on the angle net `N = 96000`
and refuse it on `N = 24000`; the author’s checker also accepts it on `N = 192000`.
The claim reached this repository as
[jlevy/squares#363](https://github.com/jlevy/squares/issues/363), opened by squarepacker
on 2026-10-05 at 08:43 UTC.

The result is squarepacker’s, after Evan Daniel and after this project’s Route B: the
points, the verifier and the reduction are Daniel’s; keeping his points and re-solving
the weights on a fine net is Route B of this project (`T-079`), whose tool the source
says guided its own scripts; the weights, the search that found them and the
verification runs are squarepacker’s.
This packet holds the v1.1 source at a pinned commit, and the replays and controls run
here. What the record makes of the claim is decided in the frontier records.
The earlier v1.0 release, `s(12) ≥ 31360/7901` (`T-078`), is the
[2 October packet](../squarepacker-s12-lower-bound-2026-10-02/README.md).

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/squarepacker/s12-lower-bound> |
| Revision | [`7a96bec36bc6811c3715ef581598f22ff9b7ba3a`](https://github.com/squarepacker/s12-lower-bound/tree/7a96bec36bc6811c3715ef581598f22ff9b7ba3a), `main` and the lightweight tag `v1.1` when fetched, tree `2bfa3159` |
| Committed | 2026-10-05T08:31:05Z (`17:31:05+09:00` by the author’s clock). Its parent [`98ffe373`](https://github.com/squarepacker/s12-lower-bound/commit/98ffe37334c63df8ab209f1f43f4c5642d5d2ee2), “Add v1.1: s(12) >= 7943/2000”, at 08:26:42Z, adds every v1.1 file; the pin adds only `.zenodo.json` |
| Release | GitHub release `v1.1`, “s(12) >= 7943/2000 (v1.1)”, published 2026-10-05T08:37:31Z with no uploaded assets; its API record is retained as [`github-release-v1.1.json`](github-release-v1.1.json). The Zenodo record below was created three seconds later, and its archive is the tag’s GitHub archive, named for the commit and carrying it as its comment, so the release and the record hold the same 68 files |
| Archive | Zenodo [10.5281/zenodo.23157015](https://doi.org/10.5281/zenodo.23157015), version `v1.1`, “squarepacker/s12-lower-bound: s(12) >= 7943/2000 (v1.1)”, published 2026-10-05 (record created 08:37:34Z), creator “Ryu, Sungjoon”, MIT; concept DOI `10.5281/zenodo.23106581`, the v1.0 record’s; related identifier `https://github.com/squarepacker/s12-lower-bound/tree/v1.1`. Its one file, `squarepacker/s12-lower-bound-v1.1.zip`, 478,011 bytes, has the MD5 Zenodo lists, `096de4f2c604be3d419710610eefb68f`, and SHA-256 `bfaae73d48b69f523396f8cd58ce6fb50cdca4260095392944e872001a2ead7c`; its archive comment is the pinned commit, and its 68 files equal this packet’s manifest byte for byte, the paper PDF (`4da8741d…`) among them ([per-file digests](receipts/zenodo-23157015-archive.sha256)) |
| Retrieved | 2026-10-05T17:07Z, a complete clone; the Zenodo record and its archive at 22:46Z, when the proxy first answered for `zenodo.org` |
| Licence | MIT. `LICENSE` reproduces Daniel’s MIT licence for the material derived from `evand/square-packing` at `7d6f46d9`, which v1.1 extends to `s12_lower_3.9715.txt` and `controls/3.9715/`, and releases the other v1.1 files (`paper/`, `logs/`, `search/`, `tools/`, `.zenodo.json`) under the same terms, copyright Ryu Sungjoon |
| Request | [jlevy/squares#363](https://github.com/jlevy/squares/issues/363) |

**Credit and AI assistance, as the source states them.** The README credits Evan
Daniel with the 1,736 points, the verifier, the reduction and its Lean formalisation;
this project with the idea of keeping Daniel’s points and re-weighting them by linear
programming on a fine angle net (Route B), saying that its `s12_reweight.py` and
Daniel’s `s12/search/tighten.py` guided `tools/search/`, which was written from scratch;
Sam Burns and Gustavo Massaccesi with the weighted-certificate method; and Göbel and
Stromquist with the unavoidable-set method. It names Ryu Sungjoon (`@squarepacker`) as
author and says that “the rescaling, the re-weighting, the verification runs and the
tools in `tools/` were prepared with the help of Claude (Anthropic)”; the issue ends
“Prepared with the help of Claude (Anthropic).” It says the result is computer-assisted
and not peer reviewed, and that “the improvement is small and comes from re-weighting
Daniel’s points, not from a new mathematical idea”.

## What Is Retained

The tree has 68 files, 879,455 bytes. The 46 files v1.1 added or changed are retained
under [`s12-lower-bound/`](s12-lower-bound/), 695,301 bytes, byte-identical after
decompression. Of the 22 pinned by digest only, 21 are v1.0 files v1.1 leaves
unchanged, which the [2 October packet](../squarepacker-s12-lower-bound-2026-10-02/README.md)
already retains and the check compares byte for byte, `tools/indep_check.cpp` among
them; the 22nd is `logs/3.9715/tightscan_N96000.txt.gz`, the source’s per-bin scan at
`N = 96000`, which is itself gzip and so cannot be retained under its own name.
The manifest is [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256)
and the record [`acquisition/sources.json`](acquisition/sources.json), both written by
`devtools.acquire_source` from [`acquisition/declaration.json`](acquisition/declaration.json).

| Upstream path | What it is |
| --- | --- |
| `s12_lower_3.9715.txt` | The certificate, SHA-256 `e2f326b28142cf22402f88357f4c7fe4680a08a32ae785b493adac335bcc2685`, as the issue states (stored as `.gz`) |
| `paper/s12_lower_3.9715.pdf`, `.tex` | The write-up: the reduction, the angle-net lemmas with proofs, the certificate, how the weights were found, the runs, the dependence on the net and the limits of the method |
| `logs/3.9715/` | Every v1.1 run the README tabulates: Daniel’s `verify` with overflow checks at `N = 24000` and `96000`, `indep_check` at `24000`, `48000`, `96000` and `192000`, each with its start and end times |
| `controls/3.9715/` | The two altered certificates (`.gz`) and their outputs from `indep_check` at `N = 96000` and from single bins of `verify` |
| `search/` | The linear-programming and column-generation logs, as JSON lines |
| `tools/indep_scan.cpp`, `tools/indep_dump.cpp`, `tools/exact_pose.py`, `tools/search/` | The checker restricted to a bin range, a lister of near-tight cells, an exact evaluator of actual unit squares, and the search scripts, which the source says hold the paths of the machine they ran on |
| `logs/control_scaled_further_31360_7900_N96000.log`, `logs/exact_pose_*.log` | Added to the v1.0 logs: the `31360/7900` control at `N = 96000` and the two exact-pose checks behind the source’s clarification of #309 |
| `README.md`, `LICENSE`, `SHA256SUMS`, `.zenodo.json` | The claim and its argument, the licence, the author’s digests of every file but these and `paper/`, the archive metadata |

The Zenodo API responses for the record and its files are retained as
[`zenodo-23157015.json`](zenodo-23157015.json) and
[`zenodo-23157015-files.json`](zenodo-23157015-files.json); the archive itself is not,
since its files are the pinned tree’s, and the acquisition record states the
comparison.

From `packing/`,
`uv run --frozen --all-extras --group dev python -m devtools.acquire_source squarepacker-s12-lower-bound-2026-10-05 --check`
re-derives the packet from its manifest.

**Daniel’s files it depends on are already retained.** His certificate is
`s12/certificates/s12_lower_3.9686.txt` and his verifier `s12/verify/`, both in the
[26 September evand packet](../evand-square-packing-2026-09-26/README.md) at `167d842c`.
The source names `7d6f46d9`. In a blobless clone of `evand/square-packing` fetched on
2026-10-05, `git ls-tree 7d6f46d9` gives the certificate as blob `4c3f0bb3` and
`verify/src/main.rs`, `Cargo.toml` and `Cargo.lock` as blobs `0e8035a3`, `7c956f54` and
`946d942c`, which `git hash-object` gives for the retained copies, so they are the bytes
the author ran.

## The Certificate, Derived Exactly

[`devtools.audit_s12_v11_certificate`](../../../devtools/audit_s12_v11_certificate.py)
reads the retained certificate and Daniel’s and decides 21 checks in rational
arithmetic, all passing ([`receipts/preflight.json`](receipts/preflight.json)):

- the digests, and the bytes are the canonical rendering of their integers;
- the header `15886000 4000000 / 4000000 / 10000000 / 1736`, so the container is
  `7943/2000`; the dilation from Daniel’s `15680/3951` is `31382793/31360000`, and the
  advance over `T-079` is `10266889/7898846000`;
- the points are Daniel’s points dilated, matched one to one, each coordinate within
  `11/39200000` of its exact image, as the source states, and the bound is attained. The
  file lists the points in another order than Daniel’s, so the match is found, not read
  from the line numbers;
- every weight is positive, the least `1/10⁷`; the points are distinct and in the closed
  container; the weighted multiset is invariant under the container’s eight symmetries,
  in 223 orbits; and the total is `119974808/10⁷`, a counting gap of `3149/1250000`;
- the closed corner square `[0, 1]²` holds 58 points of total weight `10000050/10⁷`,
  the least captured weight both of the source’s checkers print at `N = 96000`;
- the heaviest orbit, weight `1097369/10⁷` a point, has eight points, two of them in
  `[0, 1]²`, as the source describes its first control; and
- both of the source’s controls are rebuilt here from their descriptions, byte for
  byte: that orbit lowered by `100/10⁷` (`lowered-orbit`, SHA-256 `1c42bbb4…`), and the
  same integers read over `D = 3999600` (`regrid-3999600`, `f1796e27…`), container
  `39715/9999 = 3.9718972`.

The receipt also records the quantities behind the source’s account of why these points
stop near `3.9715`, as facts and not checks. The row of 112 points nearest `x = 1` lies
at `999967/10⁶`, Daniel’s row at `3948/3951` dilated, which is `(141/560)·s` up to the
grid rounding; on the container `s` the test square of bin 0, of side
`σ₀ = 9216000001/9216191999` exactly or `999979/10⁶` as Daniel’s verifier rounds it,
fits between that row and the wall once `(141/560)·s > σ₀`, that is past
`s = 3.9715485` or `3.9715478` for the two.

## Compressed Files

Each is stored as deterministic gzip made by `gzip -9n`, by `devtools.acquire_source`;
the table gives the Git blob and SHA-256 of the decompressed bytes, which are the
upstream blob and digest at `7a96bec3`. The repository’s readers take the upstream path
and decompress transparently through `devtools.retained_data.read_retained_bytes`, and
`python -m devtools.retained_data check PACKET` re-derives every row.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `s12-lower-bound/controls/3.9715/control1_lowered_orbit.txt.gz` | upstream | `1f6b7bd42cb3e236577ce789d9c299a02f4d8c09` | `1c42bbb4cf21ee75d9e13e3947cde199559f5207f71662394ed66eecfd05aad9` |
| `s12-lower-bound/controls/3.9715/control2_scaled_further.txt.gz` | upstream | `cb2cd058164a20872c0321a5e63320ba6249c006` | `f1796e271c6b877692ee06520153636cb7386e331724a720e966ec49c42b8560` |
| `s12-lower-bound/s12_lower_3.9715.txt.gz` | upstream | `77d09032eb6886cf4c61652b1def410295b76428` | `e2f326b28142cf22402f88357f4c7fe4680a08a32ae785b493adac335bcc2685` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
