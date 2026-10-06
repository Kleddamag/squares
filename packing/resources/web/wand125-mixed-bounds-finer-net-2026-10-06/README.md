# wand125 Finer-Net Certificates for n = 18 and 19, Pinned at `65e408c`

This packet pins the two certificate directories that
[wand125/square-packing-bounds](https://github.com/wand125/square-packing-bounds) added
on 6 October 2026 in one commit after the
[5 October finer-net packet’s](../wand125-mixed-bounds-finer-net-2026-10-05/README.md)
pin `43050ed`:

- `mixed_n18_L4704`, for $s(18) \ge 588/125 = 4.704$, posted in
  [a comment on jlevy/squares#366](https://github.com/jlevy/squares/issues/366#issuecomment-6006625425);
- `mixed_n19_L48229`, for $s(19) \ge 48229/10000 = 4.8229$, posted in
  [a second comment there](https://github.com/jlevy/squares/issues/366#issuecomment-6007234651).

Both are rectangle-density lower bounds of the kind, checker and driver of the earlier
mixed certificates, on a net the candidate declares, as `mixed_n18_L470` (T-096) is.
`mixed_n19_L48229` is on `mixed_n18_L470`’s net: core side $B = 999/1000$ and 416
half-angle tangents of step $1/1001$. `mixed_n18_L4704` is on a finer one: $B = 1999/2000$
and 832 half-angle tangents of step $1/2006$. Its proposed Frontier key is
**[wand125 mixed bounds finer net 2026-10-06]**. The claims below are stated as the
source states them.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/wand125/square-packing-bounds> |
| Revision | `65e408c9fa6bb787b6744c7c479ec19551a15016`, branch `main`, tree `15c56b89f26af0284f4f6ec534913a2cb416d38c`; the head when retrieved, and the revision both comments name |
| Committed | 2026-10-06T00:35:05Z, “Publish finer-net lower bounds for 18 and 19 squares” |
| Author | wand125, building on Tokoharu’s format and verifier, as for the other mixed certificates; the commit’s author name is Hiroaki Hosono |
| Licence | MIT. The root `LICENSE` reads “Copyright (c) 2026 wand125” and is byte-identical to the [September 27 packet’s copy](../wand125-rectangle-certificates-2026-09-27/wand125-rectangles/LICENSE) |
| Retrieved | 2026-10-06T02:47Z: a blobless clone of the whole history, checked out sparsely at this revision. `git ls-remote` listed one branch, `main` at this revision, and no tag |
| Pinned subtree | 70 files, 57,841,419 bytes: the two claim directories, the `verification/` directory and the three root files, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) |
| Retained here | 20 files, 1,464,020 bytes upstream, under [`square-packing-bounds/`](square-packing-bounds/), byte-identical to the pinned files after decompression |

**The revision.** The source’s `main` moved from `43050ed`, the 5 October finer-net
packet’s pin, by this one commit. It adds the two certificate directories, the directory
`verification/sqverify-net`, and one section of the root README, “Finer-net
improvements: n = 18 and 19”, and changes nothing else.

| Claim | Directory | Request |
| --- | --- | --- |
| $s(18) \ge 588/125$ | `certificates/mixed_n18_L4704` | [#366, 2026-10-06T00:36:20Z](https://github.com/jlevy/squares/issues/366#issuecomment-6006625425) |
| $s(19) \ge 48229/10000$ | `certificates/mixed_n19_L48229` | [#366, 2026-10-06T01:11:19Z](https://github.com/jlevy/squares/issues/366#issuecomment-6007234651) |

## Credit and AI Assistance, as the Source States Them

The root README at the pin is retained. Since `43050ed` it gains the one section above
and nothing else, so its Attribution section still opens “The method is not ours.”,
crediting Walter Stromquist, Hiroshi Nagamochi, Sam Burns, Gustavo Massaccesi and this
repository, and its Status section still says “Parts of this work were produced with AI
assistance under human direction.”

- **The two certificates.** Each directory README credits “Tokoharu’s rectangle-measure
  method and base checker; wand125’s measure, core/net adaptation and bundled modified
  checker”. Each says the measure was built from a structured initial measure at the
  stated side and repaired against the full net, and that the numerical search is not
  trusted by the checker.
- **The argument.** Each README states it: “D4 symmetry reduces orientations to [0,
  pi/4]. The exact net endpoint covers this interval, and B(1 + step) < 1. Thus every
  unit square contains a closed net-angle B-core strictly inside it.”
- **The source’s second check.** Each README reports a run of `sqverify-net`, the
  source’s copy of this repository’s `sqverify_fast` “adapted to read the declared
  uniform `proof_net`”, whose source the commit publishes under `verification/`:
  `mixed_n18_L4704` verified at all 832 directions in 388.2 seconds at one thread on
  macOS arm64, with two controls refused: a net declaration of step $1/1001$ at the same
  core, where $B(1 + D) > 1$, and every mass scaled by $9/10$ (the source’s pinned
  inputs, read here as data). `mixed_n19_L48229` verified at all 416, with no control. That copy is pinned here by digest and not retained,
  and was not opened (see [What Is Retained](#what-is-retained)).
- **The source’s replays.** `mixed_n19_L48229`’s README says the bundled checker’s full
  replay was run again before publication on a separate machine, 416 of 416 with “all
  1266 original bundle file hashes matching”, and retains the log
  (`verification/prepublication-replay.txt`). That was the bundle before its path
  metadata was made relative: the pinned tarball lists 1,267 files, and it is bound to
  the replayed one only through the source’s before and after digests, whose before
  archive is not published (finding FN-5 of the
  [6 October review](../../../../docs/project/reviews/review-2026-10-06-wand125-finer-net-n18-n19.md)).
  `mixed_n18_L4704`’s says plainly that no
  such replay was run for it: its evidence is the original complete run, the
  `sqverify-net` run and the publication audit. Neither was checked here.
- **The publication audit.** Each directory’s `publication-audit.json` records that the
  bundle’s absolute path metadata was made relative in 834 files (`mixed_n18_L4704`) and
  417 (`mixed_n19_L48229`), with each file’s digest before and after, and that the
  candidate, certificate and checker code are byte-identical to the audited originals.
  The audit “does not reexecute all geometric checks”.

## What Is Retained

Retained byte-identical at their upstream paths: the root `README.md`; from each claim
directory `README.md`, `candidate.json`, `certificate.json`, `manifest.json`,
`publication-audit.json` and the plain files of `verification/`; and
`mixed_n18_L4704/code/verify_mixed_full_proof.py`.

That driver is the one file of the two `code/` directories that is not byte-identical to
the retained [`mixed_n50_L740`](../wand125-point-and-mixed-2026-09-28/README.md) copy.
It differs in one line, the check on its `--workers` argument, which allows up to 16
workers where the earlier copy allows 3. Every other `code/` file of both directories,
`code/mixed_rotated_verify.cpp` (SHA-256 `89b674a6…`) among them, and each
`requirements.txt`, is byte-identical to the `mixed_n50_L740` file of the same name, so
both certificates are decided by the same checker as every earlier mixed certificate.

Pinned by digest only:

| Upstream path | Bytes | Why |
| --- | ---: | --- |
| `LICENSE` | 1,064 | retained byte-identical by the September 27 packet |
| `.gitignore` | 132 | a retained `.gitignore` would act on this repository’s tree |
| `certificates/mixed_n18_L4704/n18-L4.704-proof-bundle.tar.gz` | 31,800,246 | the complete proof bundle; SHA-256 `a4098f8200686c944d20c4c9458c3412225b1ca06f77423206a3306d03d4a709`, the digest its README states |
| `certificates/mixed_n19_L48229/n19-L4.8229-proof-bundle.tar.gz` | 24,197,004 | the complete proof bundle; SHA-256 `03aeca45921bcb8fd0be2f4869fb98e596cad673758c79022d337b8ad9629c54`, the digest its README states |
| the other 19 `code/` files and both `requirements.txt` | | byte-identical to the retained `mixed_n50_L740` copies |
| `certificates/*/verification/*.json.gz`, 4 files | | upstream gzip files, which the archive cannot retain beside its own compression: the inputs the `sqverify-net` runs and controls read |
| `verification/sqverify-net/`, 21 files | | the source’s adaptation of this repository’s `sqverify_fast` |

`verification/sqverify-net/` is a copy of this repository’s crate changed to read a
declared net. It is pinned by digest so that the record says what the source published,
and it is not retained, so that no copy of it sits in this tree beside the crate whose
own declared-net change was written apart from it
([`sqverify_fast/INDEPENDENCE.md`](../../../sqverify_fast/INDEPENDENCE.md), Declared
Nets). The importing lane fetched its files into a scratch clone to digest them and did
not open them.

[`acquisition/declaration.json`](acquisition/declaration.json) declares the scope and the
pinned-only rules, and [`acquisition/sources.json`](acquisition/sources.json) records the
pin and every pinned-only file with its size, digest, reason and, where one exists, the
retained copy with the same bytes.
From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source \
  wand125-mixed-bounds-finer-net-2026-10-06 --checkout CHECKOUT
```

rebuilds the retained files and both acquisition files from a checkout at the pinned
revision, and with `--check` in place of `--checkout CHECKOUT` re-derives the packet from
its manifest without one.

## The Claims, as the Source States Them

| Name here | Claim | Rectangles | Core $B$ | Net | Source’s comparison | Least oblique bound recorded (index) | Axis cells, minimum |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| `n18-L4704` | $s(18) \ge 588/125$ | 209 | $1999/2000$ | step $1/2006$, 832 nodes | its `mixed_n18_L470` (4.7) | $1.000000001066446$ (797) | 1,623,076, $1.008469823012092$ |
| `n19-L48229` | $s(19) \ge 48229/10000$ | 313 | $999/1000$ | step $1/1001$, 416 nodes | its `rect_n19_L48175` (4.8175) | $1.0000000005351664$ (37) | 4,717,584, $1.0026527162381171$ |

Both are rectangle densities with no point mass: each `candidate.json` has an empty
`points` list and a `scaling_factor` of `1`. Each has total mass $n - 1/100000$ and
coverage threshold $1$. Each `certificate.json` has status
`ALL_ANGLES_VERIFIED_AND_REPLAYED`, with an `ANGLE_RESULT_REPLAYED` record at every
oblique node and `AXIS_CERTIFICATE_REPLAYED` at the axis.

The candidates declare their nets as `"proof_net": {"step": "1/2006", "last": 831}` and
`{"step": "1/1001", "last": 415}`. Each `manifest.json` and `certificate.json` restates
the net with its containment facts:

| | `n18-L4704` | `n19-L48229` |
| --- | --- | --- |
| last tangent $t$ | $831/2006$ | $415/1001$ |
| $t^2 + 2t - 1$, positive past $\tan(\pi/8)$ | $497/4024036$ | $1054/1002001$ |
| $B(1 + D)$ | $4011993/4012000$ | $500499/500500$ |
| margin below 1 | $7/4012000$ | $1/500500$ |
| format M’s tangent form $B(1 + D/(1 - D^2/4))$ | $32192229833/32192286000$ | $1335998331/1336001000$ |

[`sqverify_fast/SOUNDNESS.md`](../../../sqverify_fast/SOUNDNESS.md#declared-nets), lemma
N0, proves that these premises carry the argument to a declared net, with the per-bin
centre domain at the declared half-step, $1/4012$ and $1/2002$.

`mixed_n19_L48229`’s README adds that since $s(18) \le 7/2 + \sqrt 7/2 \approx 4.822876$,
Hämäläinen’s packing, the certificate gives $s(18) < s(19)$. That holds in exact
arithmetic: $(48229/10000 - 7/2)^2 = (13229/10000)^2 = 175006441/100000000$ exceeds
$7/4$.

## The Exact Audit and the Pre-Replay Checks

From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_declared_net \
  audit --certificate n18-L4704 --check
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_declared_net \
  audit --certificate n19-L48229 --check
```

recompute [`receipts/n18-L4704/audit.json`](receipts/n18-L4704/audit.json) and
[`receipts/n19-L48229/audit.json`](receipts/n19-L48229/audit.json) from the retained
bytes, and pass:

- the mass is exactly $n - 1/100000$, with every row a nonnegative mass on a
  nondegenerate rectangle inside $[0, L]^2$;
- lemma N0’s five premises hold on the declared net: the net reaches past $\pi/4$, its
  last tangent is at most $1/2$, $B(1 + D) < 1$, and so is format M’s tangent form;
- the net blocks of `manifest.json` and `certificate.json` are those recomputed here;
- one candidate digest is stated throughout, and every node has a replay record at
  threshold one.

None of it decides coverage.

The pinned tarballs have the pinned SHA-256 and size. `bundle` binds each to the packet:

- every entry of its `files-sha256.json`, 2,515 for `n18-L4704` and 1,267 for
  `n19-L48229`, matches, and nothing is unlisted;
- its `proof/candidate.json`, `proof/certificate.json` and `proof/manifest.json` are
  byte-identical to the retained files, its ten `code/` files are the retained copies,
  and its `proof/verify.cpp` is the checker `89b674a6…`;
- at every oblique node the shipped record’s net index, tangent, bin floor and per-bin
  centre domain are lemma N0’s exactly, and its input’s header encloses the side, core,
  domain half-width, cosine and sine exactly, with threshold one;
- every input’s rectangle lines enclose the eight images of every row of the candidate,
  with their densities, and list no point mass;
- the axis record is at threshold one, with no unresolved cell.

The receipts are [`receipts/n18-L4704/bundle.json`](receipts/n18-L4704/bundle.json) and
[`receipts/n19-L48229/bundle.json`](receipts/n19-L48229/bundle.json).

## Prices

| Name here | Oblique nodes | Source’s oblique seconds | Source’s CPU-hours |
| --- | ---: | ---: | ---: |
| `n18-L4704` | 114,915,109 | 43,585 | 12.1 |
| `n19-L48229` | 75,131,365 | 42,239 | 11.7 |

The source’s seconds are each bundle’s own record of its oblique run, summed over its
`proof/net*/result.json`, on macOS arm64. `mixed_n18_L470` (T-096) recorded 9,819
seconds, and its complete replay here took 4.40 hours of wall time at two workers.

## Replaying the Certificates

**Pricing samples of the source’s checker.** On 6 October 2026 `sample` unpacked each
pinned tarball afresh, bound it, and replayed seven nodes spread over its net with the
source’s per-node functions and its unchanged checker, after the full driver’s
preconditions, at two workers under `nice` on a shared four-core host at load 3 to 7:

```sh
# from packing/
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_declared_net \
  sample --certificate n19-L48229 --tarball TARBALL --work W --nodes 0,1,37,104,208,312,411 --workers 2
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_declared_net \
  sample --certificate n18-L4704 --tarball TARBALL --work W --nodes 0,1,208,416,636,797,831 --workers 2
```

Each node returned the shipped record, the axis included, and each set holds the node
with the least recorded bound (37 and 797) and the slowest or last nodes.

| Name here | Nodes | Axis CPU seconds | Oblique CPU seconds here | Source’s seconds, same nodes | Ratio | Complete oblique replay, priced |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `n18-L4704` | 0, 1, 208, 416, 636, 797, 831 | 5.6 | 408.3 | 386.7 | 1.06 | 12.8 CPU-hours |
| `n19-L48229` | 0, 1, 37, 104, 208, 312, 411 | 19.9 | 639.5 | 559.7 | 1.14 | 13.4 CPU-hours |

The receipts are [`receipts/n18-L4704/sample/`](receipts/n18-L4704/sample/) and
[`receipts/n19-L48229/sample/`](receipts/n19-L48229/sample/). A sample is a diagnostic:
it decides no other node. The
[6 October review](../../../../docs/project/reviews/review-2026-10-06-wand125-finer-net-n18-n19.md)
ran the same command on three more nodes of each, 2, 759 and 830 at $n = 18$ and 198, 414
and 415 at $n = 19$, each returning the shipped record, so ten nodes of each net are
reproduced here with the producer’s code.

**The controls.** `control` binds a fresh copy of each bundle, runs the full driver’s
preconditions, and at the oblique node of the least recorded bound (797 at $n = 18$, 37
at $n = 19$) finds a centre of low capture and evaluates it exactly. Two mass mutants
leave that centre covered below 1, so each is provably invalid there: every mass scaled by
$99/100$, and every mass scaled so that the centre captures exactly $1 - 10^{-6}$. The
source’s export and the checker its `compile_verifier` builds, with the shipped record’s
node limit, accepted each original with its shipped record and stopped both mutants of
each unresolved (`ANGLE_UNRESOLVED`, at the depth floor). Three corrupted net
declarations, each breaking one premise, were refused by the source’s own net check and
by `sqverify-fast`’s admission, each for the premise it breaks:

| Corruption | `n18-L4704` | `n19-L48229` | Source’s refusal | `sqverify-fast`’s refusal |
| --- | --- | --- | --- | --- |
| a coarser step on which a core at a bin’s edge does not fit, the net otherwise sound | step $1/1998$, last 828 | step $1/997$, last 413 | “Core containment is not strict” | “B (1 + D) >= 1” |
| the last node dropped | last 830 | last 414 | “Net does not reach tan(pi/8)” | “the net does not reach past pi/4” |
| an unknown field | `offset` | `offset` | “Invalid proof_net fields” | “a field this reader does not know” |

`control-sqverify-fast` then rebuilt the same two mutants from the retained candidate,
recomputed their captures at the same centre with a first-party exact evaluator, and ran
`sqverify-fast` at the same node: it verified each original and refused each mutant with
an exact capture below 1 (`counterexample-candidate`). The receipts are
`receipts/*/control.json` and `receipts/*/control-sqverify-fast.json`.

**`sqverify-fast`.** This repository’s clean-room verifier, built from `main`’s crate at
`34e87a86b` (`source_sha256` `d97758bb…`, binary `567a0fd5…`, rustc 1.98.0), decided both
certificates at every node of their declared nets on 6 October 2026,
recorded in the
[Milestone B census](../../../benchmarks/measure-verifier/census-mixed/README.md):

| Name here | Directions | Boxes | Least certified bound | CPU seconds |
| --- | ---: | ---: | --- | ---: |
| `n18-L4704` | 832 | 115,091,221 | $1.000000001132137$ | 701.7 |
| `n19-L48229` | 416 | 75,232,113 | $1.000000000833015$ | 512.1 |

The rows were first made on 6 October at 03:12 UTC with the census tool of the base
commit, whose own `--control` could not run on a declared net: its exact evaluator turned
the core by the standard net’s step whatever the candidate declared, so its captures
disagreed with the crate’s (`think-q9gu`). The declared-net soundness review of 6 October
(`think-gcld`) found the same defect (its DR-1), and its fix, `36b52538a`, makes the
evaluator read the declared net. The rows and both census controls were then made again
from 04:48 to 05:03 UTC with that tool, as merged at `f342dff82` (the census tool is
that commit’s file with this packet added to its list, blob `c4ea4eb5`; its
`check_sqverify_fast.py` is that commit’s, blob `e6366726`), at one thread: the same
verdicts, box totals and least bounds, 701.7 and 512.1 CPU seconds. Each census control
verified the original at the least-bound leaf’s direction (797 at $n = 18$, 198 at
$n = 19$) and refused both mutants there, with the crate’s exact capture equal to the
independent evaluator’s. That review accepts the crate source `d97758bb…` for declared
nets; until its acceptance is merged here, no rung rests on these rows.

## Limitations

- **Coverage is decided by the source’s C++ alone** for the source’s own runs; the
  replays and `sqverify-fast` runs here are recorded separately.
- **No source audit binds a replay.** Each directory’s `publication-audit.json` is the
  source’s audit of its metadata and hashes; it re-executes no geometric check. The
  binding here is the pinned tree’s digest and each bundle’s own file list.
- **The bundles are pinned and not held.** A replay needs each tarball from the source at
  the pinned revision, with the digest above.

## Compressed Files

The six upstream data files of more than 1,000 lines, the two candidates, the two
certificates and the two publication audits, are stored as deterministic gzip made by
`gzip -9n`, with no file name or timestamp in the header. The table gives the Git blob
and SHA-256 of the decompressed bytes, which are the file’s blob and digest at the
pinned commit; each SHA-256 is also the one
[`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) pins. The
repository’s readers take the upstream path and decompress through
`devtools.retained_data.read_retained_bytes`, and
`python -m devtools.retained_data check PACKET` re-derives every row.

Before running any of the source’s own programs on this packet, restore the exact upstream
tree from the repository root:

```sh
find packing/resources/web/wand125-mixed-bounds-finer-net-2026-10-06 -name '*.gz' -exec gunzip -k {} +
```

The restored plain files are untracked, so remove them afterwards; while both copies are
present, the acquisition check reports each as retained twice.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `square-packing-bounds/certificates/mixed_n18_L4704/candidate.json.gz` | upstream | `30146dee336a9d4c0b2542f131f2f47d2e2768b7` | `9d8fea08976883f74fb47eda44fb29d1423c1394951cff34c6d7e135ebb818ea` |
| `square-packing-bounds/certificates/mixed_n18_L4704/certificate.json.gz` | upstream | `32a8cb2aa69342baeaa6e1d48b72df4d85d01b23` | `5e817f89882cb7420fb9ff37af71683abec6a27421dac425f715526140964606` |
| `square-packing-bounds/certificates/mixed_n18_L4704/publication-audit.json.gz` | upstream | `276fe9f3b3f144136d6776c49e7044e4ea1c6758` | `f28b0a65d73654d891f1087fac71710d52201067a9e52316ae0987b2aa67b17f` |
| `square-packing-bounds/certificates/mixed_n19_L48229/candidate.json.gz` | upstream | `e2744adf0fd832cb9effa5352ae66365bfa27adf` | `98ab7347d21776d54d45026414e00f89eabbb8747b302e2a00fe539e927d54a7` |
| `square-packing-bounds/certificates/mixed_n19_L48229/certificate.json.gz` | upstream | `5210d981fbf8c05a0a224403e88a74395a8b8884` | `c9ba32792551f4dc5937c5f76f989ca2e940952f10ed75e1a9ec9799b91d9e01` |
| `square-packing-bounds/certificates/mixed_n19_L48229/publication-audit.json.gz` | upstream | `6158ee7183b62bf7a47f94039c7b2d4b8796abe4` | `feeac0b12765799f9dc6d951bb6a9e2fd4a48326ac03c888b7256a469c79e09b` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
