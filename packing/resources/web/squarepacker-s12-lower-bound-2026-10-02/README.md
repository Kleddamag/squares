# squarepacker’s `s(12) ≥ 31360/7901`, Pinned 2026-10-02

Ryu Sungjoon (GitHub `squarepacker`) reports `s(12) ≥ 31360/7901 = 3.96911783…`,
which is `15680/31216851`, about `0.000502`, above Evan Daniel’s registered
`s(12) ≥ 15680/3951` (`T-049`).
The certificate is Daniel’s 1,736-point weighted certificate `s12_lower_3.9686.txt` with
every coordinate and the container multiplied by `7902/7901` and the weights unchanged.
Daniel’s verifier refuses it on the angle nets `N = 6000` and `12000` and accepts it at
`N = 24000`; the author’s own checker agrees, and also accepts at `48000` and `96000`.
The claim reached this repository as
[jlevy/squares#309](https://github.com/jlevy/squares/issues/309), opened by squarepacker
on 2026-10-02 at 16:57 UTC.

The result is squarepacker’s, after Evan Daniel: the rescaling and its verification on
the finer net are squarepacker’s, and the certificate and the verifier are Daniel’s.
This packet holds the source repository whole at a pinned commit, and the replays and
controls run here.
What the record makes of the claim is decided in the frontier records; the
[review](../../../../docs/project/reviews/review-2026-10-02-s12-rescaled-certificate.md)
gives the argument.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/squarepacker/s12-lower-bound> |
| Revision | [`8c53049025b94bb589ed25a90203f0a34c2945e4`](https://github.com/squarepacker/s12-lower-bound/tree/8c53049025b94bb589ed25a90203f0a34c2945e4), `main` when fetched, tree `9f41baf8` |
| Committed | 2026-10-02T16:45:25Z (`2026-10-03T01:45:25+09:00` by the author’s clock); five commits in all, the first, `be1871bd` at 15:47:37Z, adding the certificate, both checkers and every log |
| Archive | Zenodo [10.5281/zenodo.23106582](https://doi.org/10.5281/zenodo.23106582), version `v1.0`, published 2026-10-02, creator “Ryu, Sungjoon”, MIT; concept DOI `10.5281/zenodo.23106581`. It snapshots tag `v1.0` = `7acf812c`, whose files equal this pin’s except `README.md`, to which the pin adds the DOI line. The archive `squarepacker/s12-lower-bound-v1.0.zip` has the MD5 Zenodo lists, `a76e086aec0dab200e7426d32e5ecdf3`, and its certificate the SHA-256 below |
| Retrieved | 2026-10-02T17:26Z, a complete clone; the Zenodo record and archive at 17:27Z |
| Licence | MIT. `LICENSE` reproduces Daniel’s MIT licence for the material derived from `evand/square-packing` at `7d6f46d9` (the certificate and the controls) and releases `README.md`, `tools/` and `logs/` under the same terms, copyright Ryu Sungjoon |
| Request | [jlevy/squares#309](https://github.com/jlevy/squares/issues/309) |

The Zenodo API response for the record is retained as
[`zenodo-23106582.json`](zenodo-23106582.json); the archive itself is not, since its
files are the pinned tree’s.

**Credit and AI assistance, as the source states them.** The README credits Evan
Daniel with the certificate, the verifier, the reduction and its Lean formalisation,
Sam Burns and Gustavo Massaccesi with the weighted-certificate method, and Göbel and
Stromquist with the unavoidable-set method, and names Ryu Sungjoon (`@squarepacker`) as
author. It says that “the rescaling, the verification runs and `tools/indep_check.cpp`
were prepared with the help of” an AI assistant from Anthropic, which it names.
It says the result is not peer reviewed and that “the improvement is small and comes from
recovering discretisation slack, not from a new mathematical idea”.

## What Is Retained

Every file of the tree, 24 files and 94,729 bytes, under
[`s12-lower-bound/`](s12-lower-bound/), byte-identical after decompression; the
manifest is [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256)
and the record [`acquisition/sources.json`](acquisition/sources.json), both written by
`devtools.acquire_source` from [`acquisition/declaration.json`](acquisition/declaration.json).

| Upstream path | What it is |
| --- | --- |
| `s12_lower_3.969118.txt` | The certificate, SHA-256 `6ad9b0e8257166687f4e861b97f024f4993d7b2125897173b2f5e9f6e2167578`, as the issue states (stored as `.gz`) |
| `tools/indep_check.cpp` | The author’s checker, SHA-256 `21527e8d…` |
| `tools/spot_check.py` | 30,000 random admissible poses evaluated exactly; a sanity check, not a proof |
| `controls/` | Daniel’s 56-point set at its critical and an over-critical container, and the certificate scaled to `31360/7900` (`.gz`) |
| `logs/` | Every run the README tabulates: Daniel’s `verify` at 6000, 12000 and 24000 and with overflow checks, `indep_check` at 6000 to 96000 and at grid `2⁴⁰`, the controls and the spot check |
| `README.md`, `LICENSE`, `SHA256SUMS` | The claim and its argument, the licence, the author’s digests |

From `packing/`,
`uv run --frozen --all-extras --group dev python -m devtools.acquire_source squarepacker-s12-lower-bound-2026-10-02 --check`
re-derives the packet from its manifest.

**Daniel’s files it depends on are already retained.** The certificate it rescales is
`s12/certificates/s12_lower_3.9686.txt` and the verifier is `s12/verify/`, both in the
[26 September evand packet](../evand-square-packing-2026-09-26/README.md) at `167d842c`.
The source names `7d6f46d9`; in a blobless clone of `evand/square-packing` the certificate
is Git blob `4c3f0bb3`, and `verify/src/main.rs`, `Cargo.toml` and `Cargo.lock` are
blobs `0e8035a3`, `7c956f54` and `946d942c`, at both revisions, so the retained copies are
the ones the author ran.

## The Certificate, Derived Exactly

[`devtools.audit_s12_rescaled_certificate`](../../../devtools/audit_s12_rescaled_certificate.py)
reads the retained certificate and Daniel’s and decides 16 checks in rational arithmetic,
all passing ([`receipts/preflight.json`](receipts/preflight.json)): the digests; the
container `31360/7901 = (7902/7901)·(15680/3951)`; point `i` of the new file is point `i`
of Daniel’s with both coordinates times `7902/7901` and the same weight (`X′ = 2X`,
`Y′ = 2Y` over `D′ = 7901`); every weight positive, every point in the closed container,
the weighted set invariant under the container’s symmetries; total `119738036/10⁷ < 12`;
and the source’s `31360/7900` control is the same integers over `7900`.

## Replays Here

On a four-core Linux container shared with other lanes, at load averages of 13 to 30
throughout, so every wall time is contended.
A container restart at about 19:20 UTC killed the first full runs of `verify` and of the
native route; `verify` was rerun whole, and the native route resumed from its journal
of the 1,810 rows it had certified on clean commit `119d1bab`, the same tool code, both
reniced to 10.
Each receipt is written by
`devtools.replay_receipt` (command, working directory, load, exit status, wall and
CPU), and the checkers ran on the certificate restored from this packet’s `.gz`, whose
SHA-256 the receipt’s header names.

| Checker | Built from | Run | Wall | CPU | Result |
| --- | --- | --- | ---: | ---: | --- |
| Daniel’s `verify` (external, the producer’s verifier) | the 26 September evand packet’s `s12/verify/` by cargo 1.97.0 `--release`, target outside the packet; binary SHA-256 `9e79ec32…` | `verify s12_lower_3.969118.txt 12 24000 2 0` | 2,134 s | 982 s | VERIFIED, least captured weight `10000056/10⁷` at bin `k = 0`; every printed line equals `logs/daniel_verify_N24000.log` ([receipt](receipts/daniel-verify-N24000.log)) |
| squarepacker’s `indep_check` (external, the producer’s own checker) | `tools/indep_check.cpp` by g++ 13.3.0 `-O2` ([build](receipts/indep-check-build.log)); binary `e7748f8b…` | `indep_check s12_lower_3.969118.txt 24000` | 289.7 s | 67.7 s | VERIFIED, least `10000056/10⁷` at `k = 0`; every printed line equals `logs/indep_check_N24000.log` ([receipt](receipts/indep-check-N24000.log)) |
| The coarse nets, `indep_check` | as above | `indep_check … 6000` and `… 12000` | 67.1 s, 137.1 s | 16.2 s, 30.9 s | NOT VERIFIED, least `9849809/10⁷` at `k = 976` and `9867834/10⁷` at `k = 362`; both outputs equal the source’s logs ([6000](receipts/nets/indep-check-N6000.log), [12000](receipts/nets/indep-check-N12000.log)) |
| The coarse nets, `verify` | as above | `VERIFY_BINS=970:980 verify … 6000 1 0` and `VERIFY_BINS=355:370 … 12000 1 0` | 3.8 s, 4.5 s | 0.9 s, 1.0 s | FAIL at bins `975..980` and `361..367` with the same values, the bins before them accepted ([6000](receipts/nets/daniel-verify-N6000-bins-970-980.log), [12000](receipts/nets/daniel-verify-N12000-bins-355-370.log)) |
| This repository’s native parent-core route (first party) | [`devtools.verify_evand_angle_net_native`](../../../devtools/verify_evand_angle_net_native.py), case `s12-rescaled`: 1,810 rows on clean commit `119d1bab`, the rest resumed on clean commit `44cf3444`, the tool unchanged between them | `--case s12-rescaled --all --workers 2`, then the same with `--resume` | 4,704 s for the resumed run | 2,856 s for the resumed run; the killed first run’s is not recorded | `PASS_COMPLETE`: all 9,942 rows certified at the threshold `10⁷/10⁷`, 89,403,350 boxes, no stalled box, no exhausted budget, no refutation; the least row bound is the threshold itself, at row 1985 ([receipt](receipts/native-parent-core-N24000.json), [row journal](receipts/native-parent-core-N24000.rows.jsonl.gz), [log](receipts/native-parent-core-N24000.log); the killed first run’s [journal](receipts/native-parent-core-N24000-first-run.rows.jsonl.gz) and [log](receipts/native-parent-core-N24000-first-run.log)) |

The native reader builds the rows `[k/N, (k+1)/N]` of half-tangents, the core side
Daniel’s `σ_k` rounded down to `10⁻⁶`, at `N = 24000`; the case carries its own net and
pin, and Daniel’s `s12` case at `N = 6000` is unchanged.
The overflow-checked build of `verify` the source ran was not repeated here.

## Controls

[`devtools.audit_s12_rescaled_certificate --write-controls`](../../../devtools/audit_s12_rescaled_certificate.py)
writes two mutations, each of which every correct checker must refuse:
`scaled-7901-7900`, side `31360/7900` (SHA-256 `04d7105c…`, byte for byte the source’s
`controls/scaled_further_31360_7900.txt`), and `weights-minus-57`, every weight lowered
by `57/10⁷` (`61b48f23…`), which leaves the pose that attained `10000056/10⁷` at most
`9999999/10⁷`.

| Checker | `scaled-7901-7900` | `weights-minus-57` |
| --- | --- | --- |
| `verify`, a window of bins (`VERIFY_BINS`, which cannot print VERIFIED) | bins `3880..3910`: FAIL at `3893..3899`, least `9849809/10⁷` ([receipt](receipts/controls/daniel-verify-N24000-scaled-7901-7900-bins-3880-3910.log)) | bins `0..15`: FAIL at `0..6`, least `9988604/10⁷` ([receipt](receipts/controls/daniel-verify-N24000-weights-minus-57-bins-0-15.log)) |
| `indep_check`, every bin | NOT VERIFIED, least `9849809/10⁷` at `k = 3894`, as the source’s log ([receipt](receipts/controls/indep-check-N24000-scaled-7901-7900.log)) | NOT VERIFIED, least `9985548/10⁷` at `k = 4154` ([receipt](receipts/controls/indep-check-N24000-weights-minus-57.log)) |
| Native, two rows each | rows `3893` and `3894` refuted, with admissible witnesses of charge `1973359/2000000` and `9849809/10⁷` ([receipt](receipts/controls/native-scaled-7901-7900.json)) | rows `0` and `4154` refuted, each with a witness of charge `39987/40000` ([receipt](receipts/controls/native-weights-minus-57.json)) |

A bin refused in a window is refused in the full sweep, since each bin is computed alone
and one refused bin makes the sweep refuse. `verify` exits `0` whatever its verdict, so
its receipts are read by their verdict lines.
[`tests/test_s12_rescaled_certificate.py`](../../../tests/test_s12_rescaled_certificate.py)
holds every receipt here and regenerates both controls.

## Reproduce

From `packing/`, with `SCRATCH` any directory outside the repository:

```bash
uv run --frozen --all-extras --group dev python -m devtools.audit_s12_rescaled_certificate \
  --output SCRATCH/preflight.json --write-controls SCRATCH/controls
uv run --frozen --all-extras --group dev python -c "from pathlib import Path; \
from devtools.retained_data import read_retained_bytes as r; \
Path('SCRATCH/s12_lower_3.969118.txt').write_bytes(r(Path( \
'resources/web/squarepacker-s12-lower-bound-2026-10-02/s12-lower-bound/s12_lower_3.969118.txt')))"
(cd resources/web/evand-square-packing-2026-09-26/square-packing/s12/verify && \
  CARGO_TARGET_DIR=SCRATCH/verify-target cargo build --release)
SCRATCH/verify-target/release/verify SCRATCH/s12_lower_3.969118.txt 12 24000 2 0
g++ -O2 -o SCRATCH/indep_check \
  resources/web/squarepacker-s12-lower-bound-2026-10-02/s12-lower-bound/tools/indep_check.cpp
SCRATCH/indep_check SCRATCH/s12_lower_3.969118.txt 24000
uv run --frozen --all-extras --group dev python -m devtools.verify_evand_angle_net_native \
  --case s12-rescaled --all --workers 2 --output SCRATCH/native.json
```

## Compressed Files

Upstream files and receipts of more than 1,000 lines are stored as deterministic
`gzip -9n`. Each row gives the Git blob and SHA-256 of the decompressed bytes, as
`devtools.retained_data` produces them.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `s12-lower-bound/s12_lower_3.969118.txt.gz` | upstream | `1ba9daed88559402212afc8ba4e65f2105c59b8d` | `6ad9b0e8257166687f4e861b97f024f4993d7b2125897173b2f5e9f6e2167578` |
| `s12-lower-bound/controls/scaled_further_31360_7900.txt.gz` | upstream | `ceff7e884f59be751723d48de25a0bbdd4bdd11e` | `04d7105c5b6d8b85cd0655f544b5c59163f9a36fa86814601a30c4114d1526f1` |
| `receipts/native-parent-core-N24000.rows.jsonl.gz` | receipt | `d37a30c6fededa188dc7d64cf00e801977c1c8a6` | `15f9a2bb426946ebe20592d0ab94383d57876617876ecf5e65c3e091771ea1ef` |
| `receipts/native-parent-core-N24000-first-run.rows.jsonl.gz` | receipt | `88d64d7ecef96397750b840ece2cc32e77d55974` | `c882fe8d926262368e780b59dc494060bf4ecf3372dc2a4a703fcedb35552636` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
