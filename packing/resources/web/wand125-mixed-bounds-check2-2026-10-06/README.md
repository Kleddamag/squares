# wand125 Check2 and Finer-Net Certificates for Ten Counts, Pinned at `2fad66e`

This packet pins the ten certificate directories that
[wand125/square-packing-bounds](https://github.com/wand125/square-packing-bounds) added
on 6 October 2026 in ten commits after the
[6 October finer-net packet’s](../wand125-mixed-bounds-finer-net-2026-10-06/README.md)
pin `65e408c`. Each is a rectangle-density lower bound on a net its candidate declares,
in the format of `mixed_n18_L4704` (T-099):

- `mixed_n29_L581`, for $s(29) \ge 581/100$, a complete proof bundle checked by the C++
  checker of every earlier mixed certificate, as T-099 and T-100 are;
- nine **check2** certificates, for $s(18) \ge 941/200$, $s(19) \ge 193/40$,
  $s(20) \ge 981/200$, $s(26) \ge 1109/200$, $s(27) \ge 11287/2000$,
  $s(28) \ge 1147/200$, $s(30) \ge 11767/2000$, $s(39) \ge 133/20$ and
  $s(41) \ge 271/40$, which ship no C++ records. Each is checked instead by the source’s
  adaptation of this repository’s `sqverify_fast` to a declared net
  ([What Check2 Changes](#what-check2-changes)).

None of the ten was posted on an issue here: the intake pass that read `2fad66e` found
them. Their proposed Frontier key is **[wand125 mixed bounds check2 2026-10-06]**. The
claims below are stated as the source states them.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/wand125/square-packing-bounds> |
| Revision | `2fad66e02f54a492835dc41ac37a9184e1e7a662`, branch `main`, tree `39ea18ce37bfdf42cf154decc33a18979fe3c16d`; the head when retrieved, and still the head when this packet was written |
| Committed | 2026-10-06T07:26:49Z, “Mixed certificate: s(41) >= 271/40 = 6.775 (finer angle net, check2 bundle)” |
| Author | wand125, building on Tokoharu’s format and verifier, as for the other mixed certificates; the commits’ author name is Hiroaki Hosono |
| Licence | MIT. The root `LICENSE` reads “Copyright (c) 2026 wand125” and is byte-identical to the [September 27 packet’s copy](../wand125-rectangle-certificates-2026-09-27/wand125-rectangles/LICENSE) |
| Retrieved | 2026-10-06T07:47Z: a blobless clone of the whole history, checked out sparsely at this revision. `git ls-remote` listed one branch, `main` at this revision |
| Pinned subtree | 181 files, 44,445,588 bytes: the ten claim directories and the three root files, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) |
| Retained here | 113 files, 1,682,378 bytes upstream, under [`square-packing-bounds/`](square-packing-bounds/), byte-identical to the pinned files after decompression |

**The revisions.** The source’s `main` moved from `65e408c` through ten commits, each
adding one certificate directory and one section of the root README, and changing
nothing else. The times are the commits’ own, in UTC.

| Claim | Directory | Commit | Committed | Form |
| --- | --- | --- | --- | --- |
| $s(29) \ge 581/100$ | `certificates/mixed_n29_L581` | `8cc13bf` | 04:14:30Z | proof bundle |
| $s(20) \ge 981/200$ | `certificates/mixed_n20_L4905` | `6109d76` | 05:34:08Z | check2 |
| $s(26) \ge 1109/200$ | `certificates/mixed_n26_L5545` | `f2fa814` | 05:34:20Z | check2 |
| $s(27) \ge 11287/2000$ | `certificates/mixed_n27_L56435` | `80fe70c` | 05:34:30Z | check2 |
| $s(28) \ge 1147/200$ | `certificates/mixed_n28_L5735` | `3d28e02` | 05:34:41Z | check2 |
| $s(30) \ge 11767/2000$ | `certificates/mixed_n30_L58835` | `caafcdf` | 06:11:37Z | check2 |
| $s(18) \ge 941/200$ | `certificates/mixed_n18_L4705` | `85951fd` | 07:23:46Z | check2 |
| $s(19) \ge 193/40$ | `certificates/mixed_n19_L4825` | `73b71eb` | 07:23:52Z | check2 |
| $s(39) \ge 133/20$ | `certificates/mixed_n39_L665` | `0683139` | 07:26:42Z | check2 |
| $s(41) \ge 271/40$ | `certificates/mixed_n41_L6775` | `2fad66e` | 07:26:49Z | check2 |

The root README’s sections for `mixed_n18_L4705` and `mixed_n19_L4825` say each
supersedes the certificate above it, `mixed_n18_L4704` (T-099) and `mixed_n19_L48229`
(T-100).

## Credit and AI Assistance, as the Source States Them

The root README at the pin is retained. Since `65e408c` it gains the ten sections and
nothing else, so its Attribution section still opens “The method is not ours.”,
crediting Walter Stromquist, Hiroshi Nagamochi, Sam Burns, Gustavo Massaccesi and this
repository, and its Status section still says “Parts of this work were produced with AI
assistance under human direction.”

- **The measures.** Each directory README says its candidate was built from scratch at
  the stated side from a structured initial measure (“bands at integer distances from
  the walls”), searched under the $n$ budget with the declared core and net, and
  repaired against low-coverage witnesses on the full net until every net angle passed.
  Each check2 directory’s `provenance/search-notes.md` says the same, and that the
  search is “Numerical only; floating-point LP and sampling” and not trusted by the
  checker.
- **`mixed_n29_L581`.** Its README names the checker “the verifier shipped here,
  `code/mixed_rotated_verify.cpp`”, the same checker as for `mixed_n87_L939` and
  `mixed_n65_L835`, and says its least oblique bound, $1.0000000009$, is below the
  $1.0001$ Tokoharu’s `verify.cpp` requires, so the certificate is not in his format.
  It says the bundle’s full replay “was run where the certificate was made”.
- **The check2 certificates.** Each README calls the check “the independent
  second-system check” and its checker “the independently implemented `sqverify_fast`
  (jlevy/squares, adapted to read the declared net; source digest `ab6e33e164db`)”. The
  receipt says it was “built from the certificate specification only, without reading
  the search code”, and `check2/src/SPEC.md` says it “was written from the certificate
  data and a prose description of the certificate, without reading the code that
  produced the certificates.” The independence claimed is from the source’s own search
  and C++ checker; the checker is this repository’s crate
  ([What Check2 Changes](#what-check2-changes)).
- **The pre-publication checks.** Every README reports a second run of the adapted
  verifier before publication, “on a fresh Ubuntu 24.04.5 LTS (x86_64), Rust 1.98.0
  machine”, after checking the tarball’s digest and its file hashes, with
  `verification/prepublication-receipt.json` as its record in each check2 directory.
  `mixed_n29_L581`’s README reports the same run, 416 of 416 directions in 584
  seconds, with no retained receipt.
- **Earlier bundles.** Each check2 README says: “Bundles published before 2026-10-06
  (n18 L=4.70, n18 L=4.704, n19 L=4.8229) carry the full per-angle record of a shipped
  C++ verifier plus its replay (about 24 CPU hours per certificate). Bundles from
  2026-10-06 on carry the second-system check above instead (minutes per certificate);
  their candidates are in the same format and can still be run through the shipped
  verifier of the earlier bundles.”

## What Check2 Changes

**The format does not change.** Each check2 `candidate.json` is format M as T-099’s is:
rectangle rows `{rectangle, mass}` averaged over the container’s eight symmetries, an
empty `points` list, a core side `B`, a total mass of $n - 1/100000$, and a
`proof_net {step, last}`. The candidate digest each README and receipt states is the
source’s semantic digest, SHA-256 of the compact, key-sorted JSON of `n`, `L`, `B`,
`rectangles`, `points`, `total_mass` and `proof_net`; the audit recomputes it.
`mixed_n18_L4705` and `mixed_n19_L4825` declare a net finer than any before: core
$4999/5000$ and 2073 half-angle tangents of step $1/5002$.

**The checker changes.** A check2 bundle carries no per-node C++ record and no
`code/` directory. In their place it carries:

- `check2/receipt.json`, the source’s run of `sqverify-proof-net` at every node of the
  declared net, `VERIFIED` at threshold one, with the verifier’s own summary;
- `check2/run.jsonl.gz`, that run’s per-direction log;
- `check2/control.json` and a control log, the same run on the candidate with every mass
  scaled by $197/200$, `REFUSED`;
- `check2/src/`: the verifier as a `git archive` tarball,
  `sqverify-proof-net-fe12e036c.tar.gz`, described as “`packing/sqverify_fast` of
  jlevy/squares at commit fe12e036c (branch wand125/sqverify-proof-net)”; the script
  `fine_net_check.sh` that runs it; `REPRODUCE.md` and `SPEC.md`; and the crate’s own
  `SOUNDNESS.md` and `INDEPENDENCE.md`.

`SPEC.md` §5 describes the verifier as this repository’s `sqverify_fast` with “one
change: a format M candidate that declares `proof_net {step, last}` takes the step and
the direction count last + 1 from it”, with the net premises checked as before.
`UPSTREAM_COMMIT` names `42534d959d668c5e03839dc87f9e628fa4fc2d83`, which this
repository does not hold: a fetch of it was refused (“not our ref”). The two pinned
documents are this repository’s own files by their bytes: the adapted crate’s
`SOUNDNESS.md` is the Git blob of `packing/sqverify_fast/SOUNDNESS.md` at `b2c98e3bd`
(3 October), and its `INDEPENDENCE.md` that of `packing/sqverify_fast/INDEPENDENCE.md`
at `61acc9dcb` (3 October). Both precede `f007d7afd` (5 October), where this
repository’s crate gained its own declared net and lemma N0, so the adapted crate’s
soundness document has no declared-net lemma, though `SPEC.md` says its lemmas “are
stated for a general step D”. The comparison was by digest; neither file was opened.

**What that means here.**

- **sqverify_fast’s admission is untouched.** Nothing in the bundles changes this
  repository’s crate. A check2 candidate is a format M certificate with a declared net,
  which `main`’s crate (`source_sha256` `d97758bb…`) reads with its own declared-net
  code, written apart from the source’s patch.
- **The declared-net review’s scope covers the new net.** The soundness re-review of 6
  October accepted `d97758bb…` for format M on a declared net whose premises lemma N0
  states, for any step and up to $2^{16}$ nodes. The $1/5002$ net has 2073 nodes and
  meets every premise (the table under [The Claims](#the-claims-as-the-source-states-them)),
  so no new review of the crate is needed for it. The audit here holds each premise
  exactly.
- **The source’s check is not independent of this repository’s verifier.** The program
  that decides a check2 bundle at the source is a copy of this repository’s crate with
  one change. A `sqverify-fast` replay here therefore re-implements the producer’s
  check, sharing its components, rather than confirming it with a second
  implementation. It is recorded as `shared-components`, the shared component being the
  `sqverify_fast` crate, all of it but the declared-net reader, and not as
  `independent-implementation`, as T-099 and T-100’s replays are. The sharing runs the
  other way from the definition’s usual case: the producer adapted this repository’s
  code, not the reverse, and the replay is much closer to a reproduction than the label
  alone says. `mixed_n29_L581` is recorded as T-099 and T-100 are,
  `independent-implementation`, because the claim the source publishes rests on its C++
  records; the source’s pre-publication run of its copy of the crate on that candidate
  publishes no receipt.
- **The source’s C++ checker still applies.** Every check2 candidate is in the format
  `code/mixed_rotated_verify.cpp` (`89b674a6…`) reads, and that checker shares no code
  with `sqverify_fast`. It is the producer’s own code, though, so a run of it here is a
  reproduction with the producer’s code of a check the producer did not run, never an
  independent confirmation; its value is diversity against the crate. `cpp-sample` runs
  it at chosen nodes of each, from the retained `mixed_n50_L740` code
  ([Replaying the Certificates](#replaying-the-certificates)).

## What Is Retained

Retained byte-identical at their upstream paths: the root `README.md`; from each claim
directory `README.md` and `candidate.json`; from `mixed_n29_L581`, `certificate.json` and
`manifest.json`; and from each check2 directory `bundle.json`, `files-sha256.json`,
`check2/receipt.json`, `check2/control.json`, `check2/src/REPRODUCE.md`,
`check2/src/SPEC.md`, `check2/src/UPSTREAM_COMMIT`, `check2/src/fine_net_check.sh`,
`provenance/search-notes.md` and `verification/prepublication-receipt.json`.

Pinned by digest only:

| Upstream path | Bytes | Why |
| --- | ---: | --- |
| `LICENSE` | 1,064 | retained byte-identical by the September 27 packet |
| `.gitignore` | 132 | a retained `.gitignore` would act on this repository’s tree |
| `certificates/mixed_n29_L581/n29-L5.81-proof-bundle.tar.gz` | 38,874,443 | the complete proof bundle; SHA-256 `057d3df36634f062d6eaad37d5c3195bb2c0adfcd7ba7ce6e149d8333be9dc56`, the digest its README states |
| `certificates/*/n*-check2-bundle.tar.gz`, 9 files | 174,603 to 307,607 each | each check2 bundle as one tarball, whose other files the directory holds; digests in the [table of prices](#prices) |
| `certificates/mixed_n29_L581/code/*`, 10 files, and `requirements.txt` | | byte-identical to the retained `mixed_n50_L740` copies |
| `certificates/*/check2/*.jsonl.gz`, 18 files | | upstream gzip files, which the archive cannot retain beside its own compression: the run and control logs, which `bundle` reads from the tarball |
| `certificates/*/check2/src/sqverify-proof-net-fe12e036c.tar.gz`, 9 copies | 69,540 each | the source’s adaptation of this repository’s `sqverify_fast`, one tarball with SHA-256 `e495f9bf14dc5ca20d8890aa0601183b8b955b94580c4e99ddffa64254371e81` in every bundle |
| `certificates/*/check2/src/SOUNDNESS.md` and `INDEPENDENCE.md`, 9 copies of each | | the adapted crate’s copies of this repository’s documents, kept with the crate they document |

The adapted crate is pinned by digest so that the record says what the source
published, and it is not retained, so that no copy of it sits in this tree beside the
crate whose own declared-net change was written apart from it
([`sqverify_fast/INDEPENDENCE.md`](../../../sqverify_fast/INDEPENDENCE.md), Declared
Nets). The importing lane digested it in the scratch clone and in each unpacked bundle,
and did not open it.

[`acquisition/declaration.json`](acquisition/declaration.json) declares the scope and the
pinned-only rules, and [`acquisition/sources.json`](acquisition/sources.json) records the
pin and every pinned-only file with its size, digest, reason and, where one exists, the
retained copy with the same bytes.
From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source \
  wand125-mixed-bounds-check2-2026-10-06 --checkout CHECKOUT
```

rebuilds the retained files and both acquisition files from a checkout at the pinned
revision, and with `--check` in place of `--checkout CHECKOUT` re-derives the packet from
its manifest without one.

## The Claims, as the Source States Them

| Name here | Claim | Rectangles | Core $B$ | Net | Source’s comparison | Least oblique bound recorded (index) | Axis bound recorded |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| `n18-L4705` | $s(18) \ge 941/200$ | 324 | $4999/5000$ | step $1/5002$, 2073 nodes | its `mixed_n18_L4704` (4.704); the directory, its `mixed_n18_L470` (4.7) | $1.0000000000680034$ (1234) | $1.016430568872826$ |
| `n19-L4825` | $s(19) \ge 193/40$ | 341 | $4999/5000$ | step $1/5002$, 2073 nodes | its `mixed_n19_L48229` (4.8229); the directory, its `rect_n19_L48175` (4.8175) | $1.0000000001230112$ (1021) | $1.0036436971903462$ |
| `n20-L4905` | $s(20) \ge 981/200$ | 327 | $1999/2000$ | step $1/2006$, 832 nodes | its `rect_n20_L49` (4.9) | $1.000000000154736$ (679) | $1.0046418452468053$ |
| `n26-L5545` | $s(26) \ge 1109/200$ | 477 | $1999/2000$ | step $1/2006$, 832 nodes | its `rect_n26_L55325` (5.5325) | $1.0000000003495713$ (241) | $1.0032441151223488$ |
| `n27-L56435` | $s(27) \ge 11287/2000$ | 439 | $1999/2000$ | step $1/2006$, 832 nodes | its `rect_n27_L5635` (5.635) | $1.0000000000168654$ (632) | $1.0033571274334194$ |
| `n28-L5735` | $s(28) \ge 1147/200$ | 531 | $999/1000$ | step $1/1001$, 416 nodes | its `rect_n28_L57225` (5.7225) | $1.0000000000381999$ (48) | $1.0019493780352478$ |
| `n29-L581` | $s(29) \ge 581/100$ | 505 | $999/1000$ | step $1/1001$, 416 nodes | its `rect_n29_L57975` (5.7975) | $1.000000000892745$ (364) | 11,309,769 cells, $1.003704246326725$ |
| `n30-L58835` | $s(30) \ge 11767/2000$ | 402 | $1999/2000$ | step $1/2006$, 832 nodes | its `rect_n30_L5875` (5.875) | $1.0000000000570795$ (347) | $1.0055878584856262$ |
| `n39-L665` | $s(39) \ge 133/20$ | 600 | $999/1000$ | step $1/1001$, 416 nodes | its `rect_n39_L6635` (6.635) | $1.0000000001966394$ (394) | $1.002333722755048$ |
| `n41-L6775` | $s(41) \ge 271/40$ | 376 | $999/1000$ | step $1/1001$, 416 nodes | its `rect_n41_L676` (6.76) | $1.0000000000604714$ (409) | $1.004989715377397$ |

For `n18-L4705` and `n19-L4825` the comparison column gives the root README’s, which
says each supersedes the 6 October finer-net certificate, and then that of the
directory’s README and `bundle.json`, which compare with the certificate before it: the
bundle-level comparisons predate the root README’s (finding FN-6 of the review).

The check2 bounds are the source’s `sqverify-proof-net` run log’s, read by `bundle`;
`n29-L581`’s are its C++ records’, read by `audit`. All ten are rectangle densities with
no point mass, total mass $n - 1/100000$ and coverage threshold $1$. The candidates of
`n18-L4705` and `n26-L5545` have no `scaling_factor` field and the others a
`scaling_factor` of `1`, with a `scaling_source_digest` equal to the semantic digest.

The three nets, with lemma N0’s premises as the audit recomputes them:

| | step $1/5002$, $B = 4999/5000$ | step $1/2006$, $B = 1999/2000$ | step $1/1001$, $B = 999/1000$ |
| --- | --- | --- | --- |
| last tangent $t$ | $1036/2501$ | $831/2006$ | $415/1001$ |
| $t^2 + 2t - 1$, positive past $\tan(\pi/8)$ | $367/6255001$ | $497/4024036$ | $1054/1002001$ |
| $B(1 + D)$ | $25009997/25010000$ | $4011993/4012000$ | $500499/500500$ |
| margin below 1 | $3/25010000$ | $7/4012000$ | $1/500500$ |
| format M’s tangent form $B(1 + D/(1 - D^2/4))$ | $500400014977/500400075000$ | $32192229833/32192286000$ | $1335998331/1336001000$ |

[`sqverify_fast/SOUNDNESS.md`](../../../sqverify_fast/SOUNDNESS.md#declared-nets), lemma
N0, proves that these premises carry the argument to a declared net, with the per-bin
centre domain at the declared half-step. The last bin of the $1/5002$ net, from
$4143/10004$, still holds orientations below $\tan(\pi/8)$, which the audit checks for
every net.

## The Exact Audit and the Bundle Binding

From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_declared_net \
  audit --certificate n20-L4905 --check
```

and the same for each name in the table recompute `receipts/<name>/audit.json` from the
retained bytes, and pass. For every certificate:

- the mass is exactly $n - 1/100000$, with every row a nonnegative mass on a
  nondegenerate rectangle inside $[0, L]^2$;
- lemma N0’s five premises hold on the declared net, and its last bin holds an
  orientation.

For `n29-L581`, as for T-099: the net blocks of `manifest.json` and `certificate.json`
are those recomputed here, one candidate digest is stated throughout, and every node has
a replay record at threshold one. For each check2 certificate:

- `bundle.json` states this claim, net, mass and candidate, and the net block recomputed
  here;
- the semantic digest recomputed here is the one `bundle.json` and the receipt state;
- `check2/receipt.json` has the digest `bundle.json` states, and reports every node of
  this net verified at threshold one, by a run that read this side, core, step, node
  count and mass;
- the run’s own record of the bytes it read, its summary’s `input_sha256`, is the
  published `candidate.json` for `n18-L4705` only. The other eight logged runs read a
  file whose bytes are not published, named by its digest in the tool’s
  `UNPUBLISHED_RUN_INPUTS` and in each audit receipt’s `run_input`, with the same side,
  core, net, count and mass (finding FN-1 of the
  [6 October review](../../../../docs/project/reviews/review-2026-10-06-wand125-check2-ten-certificates.md)).
  Any other input is refused;
- `check2/control.json` reports the control refused, with every mass scaled by
  $197/200$ and, where it names one, this candidate’s file;
- `verification/prepublication-receipt.json` reports every node verified by the same
  build, on the published bytes, with its control refused;
- every file `files-sha256.json` lists is the directory’s, by its bytes or its pin,
  apart from the bundle’s own `README.md`, which is shorter than the directory’s.

None of it decides coverage.

`bundle --tarball` unpacks each pinned tarball afresh, refusing it unless it has the
pinned SHA-256 and size, and binds it to the packet. For `n29-L581`, as for T-099: all
1,266 entries of its `files-sha256.json` match, its candidate, certificate and manifest
are the retained files, its ten `code/` files are the retained `mixed_n50_L740` copies,
its `proof/verify.cpp` is the checker `89b674a6…`, and every oblique record and input
is lemma N0’s at its node with rectangle lines enclosing the expanded candidate. For
each check2 bundle:

- all 15 entries of its `files-sha256.json` match and nothing is unlisted; the list is
  the retained one; and every listed file but the bundle’s `README.md` is the
  directory’s, nine by their retained bytes and five by their pins, the adapted crate’s
  tarball compared by digest only;
- the run log holds one record per net node, each `verified` at threshold one with a
  certified lower bound of at least one, the axis by the exact vertex sweep and every
  oblique node by branch and bound, and ends with the summary the receipt states;
- the control log ends `REFUSED` on this side, core, net and threshold, with every mass
  scaled by exactly $197/200$, and its refused directions and witnesses below threshold
  are those `control.json` states;
- every exact witness of the control log lies in its node’s per-bin domain, and its
  logged capture is the one `check_sqverify_fast.mixed_exact`, an evaluator written apart
  from the crate, computes on the published candidate scaled by $197/200$, below one:
  277 witnesses in all, so each control is a provably invalid measure (finding FN-2 of the
  review).

The receipts are `receipts/<name>/bundle.json`. A check2 binding shows what the
source’s run printed; it decides no coverage, and the run it describes is of a copy of
this repository’s verifier, on the published bytes for `n18-L4705` and on unpublished
ones for the other eight. The source’s pre-publication runs read the published bytes and
publish no log, and every control witness evaluates exactly on the published measure:
what remains unbound is which file the eight logged runs read, and the replay here reads
the published bytes.

## Prices

| Name here | Tarball | Bytes | SHA-256 | Source’s run |
| --- | --- | ---: | --- | --- |
| `n18-L4705` | `n18-L4.705-check2-bundle.tar.gz` | 307,607 | `187115fc5297ced03df2c8b2a9cecd77d35da59a254608607facbf2d5e6238f2` | 2,878 CPU seconds, 6 threads, x86_64 Linux |
| `n19-L4825` | `n19-L4.825-check2-bundle.tar.gz` | 292,199 | `7b4f000c3aa87db233cdf9214127db6556d573a8fdedc4d7422f59a2b22e8c52` | 2,981 direction seconds, 4 threads, arm64 macOS |
| `n20-L4905` | `n20-L4.905-check2-bundle.tar.gz` | 202,312 | `aa6721222289fcacf2dd5a9704a089b18f52aaa36cce7622e6d9036123a926cb` | 1,515 direction seconds, 4 threads, arm64 macOS |
| `n26-L5545` | `n26-L5.545-check2-bundle.tar.gz` | 207,412 | `3f8ebbe903a8b6f7d1e12d23d48b6d3a91ea026d3fa143732e91f5a18ce43838` | 4,231 direction seconds, 4 threads, arm64 macOS |
| `n27-L56435` | `n27-L5.6435-check2-bundle.tar.gz` | 208,184 | `33b2a44054f2c69f1da41473fb6412ab599c8597e06a81dd5fa2158408f6fda2` | 2,898 direction seconds, 4 threads, arm64 macOS |
| `n28-L5735` | `n28-L5.735-check2-bundle.tar.gz` | 181,502 | `202dc8de02d0e42bbf6d551a4ae3f1e3c71ef3cb3d4cc97785fdaac39a8a95cc` | 1,459 direction seconds, 4 threads, arm64 macOS |
| `n29-L581` | `n29-L5.81-proof-bundle.tar.gz` | 38,874,443 | `057d3df36634f062d6eaad37d5c3195bb2c0adfcd7ba7ce6e149d8333be9dc56` | 152,187 oblique seconds of the C++ checker, 42.3 CPU-hours |
| `n30-L58835` | `n30-L5.8835-check2-bundle.tar.gz` | 212,146 | `8a629510d1702e41432c95a82e18123471cefc92c1ce5ab797c08e658b49549a` | 5,760 direction seconds, 4 threads, arm64 macOS |
| `n39-L665` | `n39-L6.65-check2-bundle.tar.gz` | 189,653 | `ac1bba6e28dd3c647d003ed8bdfa087c4157a4d01530635676b7822b76a97faa` | 4,845 direction seconds, 4 threads, arm64 macOS |
| `n41-L6775` | `n41-L6.775-check2-bundle.tar.gz` | 174,603 | `59bd9ff55f9b0bd29eea919dd7c19135e7d34673d9fd43ca2c5a46c618fa73e3` | 2,014 direction seconds, 4 threads, arm64 macOS |

A check2 run’s seconds are its summary’s: the sum of the per-direction seconds, and its
CPU seconds where the host recorded them. On arm64 macOS the summary records the CPU as
$-0$, so the direction seconds are the price. The pre-publication runs on an x86_64
host took 490 to 1,411 wall seconds per certificate. `n29-L581`’s C++ run is
priced from its bundle’s own records, summed over its `proof/net*/result.json`.

## Replaying the Certificates

**`sqverify-fast`.** This repository’s clean-room verifier, built from `main`’s crate
at `34e87a86b` (`source_sha256` `d97758bb…`, binary `567a0fd5…`, rustc 1.98.0), decided
all ten at every node of their declared nets on 6 October 2026, from 07:51 to 16:56 UTC,
at one thread under `nice` on the shared four-core host at load 5 to 16, with the census
tool as merged at `f342dff82` and this packet added to its list, recorded in the
[Milestone B census](../../../benchmarks/measure-verifier/census-mixed/README.md):

```sh
# from packing/
uv run --frozen --all-extras --group dev python -m devtools.sqverify_fast_census --family mixed \
  --binary BINARY --out benchmarks/measure-verifier/census-mixed --threads 1 --only mixed_n20_L4905
uv run --frozen --all-extras --group dev python -m devtools.sqverify_fast_census --family mixed \
  --binary BINARY --out benchmarks/measure-verifier/census-mixed --control --only mixed_n20_L4905
```

| Name here | Directions | Boxes | Least certified bound (index) | CPU seconds | Census control | Equal to the source’s run log |
| --- | ---: | ---: | --- | ---: | --- | --- |
| `n18-L4705` | 2073 | 352,045,748 | $1.0000000000680034$ (1234) | 2,884.7 | `CONTROLS_REFUSED` at 1234 | nodes at 2072 of 2072, bounds at 2073 of 2073 |
| `n19-L4825` | 2073 | 355,934,320 | $1.0000000001230112$ (1021) | 2,841.2 | `CONTROLS_REFUSED` at 1021 | nodes at 2072 of 2072, bounds at 2073 of 2073 |
| `n20-L4905` | 832 | 139,374,489 | $1.000000000154736$ (679) | 1,420.5 | `CONTROLS_REFUSED` at 679 | nodes at 831 of 831, bounds at 832 of 832 |
| `n26-L5545` | 832 | 234,384,519 | $1.0000000003495713$ (241) | 2,235.6 | `CONTROLS_REFUSED` at 241 | nodes at 831 of 831, bounds at 832 of 832 |
| `n27-L56435` | 832 | 215,026,151 | $1.0000000000168654$ (632) | 2,824.1 | `CONTROLS_REFUSED` at 632 | nodes at 831 of 831, bounds at 832 of 832 |
| `n28-L5735` | 416 | 114,964,701 | $1.0000000000381999$ (48) | 1,540.9 | `CONTROLS_REFUSED` at 48 | nodes at 415 of 415, bounds at 416 of 416 |
| `n29-L581` | 416 | 126,796,081 | $1.0000000000094453$ (298) | 1,632.3 | `CONTROLS_REFUSED` at 298 | not comparable: its source records are the C++ checker’s |
| `n30-L58835` | 832 | 251,711,359 | $1.0000000000570795$ (347) | 3,890.8 | `CONTROLS_REFUSED` at 347 | nodes at 831 of 831, bounds at 832 of 832 |
| `n39-L665` | 416 | 182,222,199 | $1.0000000001966394$ (394) | 3,869.8 | `CONTROLS_REFUSED` at 394 | nodes at 415 of 415, bounds at 416 of 416 |
| `n41-L6775` | 416 | 114,365,213 | $1.0000000000604714$ (409) | 2,135.3 | `CONTROLS_REFUSED` at 409 | nodes at 415 of 415, bounds at 416 of 416 |

Every row is `VERIFIED`: every direction verified, summary `VERIFIED`, exit 0, and the
exact capture at the least-bound leaf’s centre at least one. 25,275 CPU seconds in all,
7.0 CPU-hours. Each census control verified the original at the least-bound leaf’s
direction and refused there every mass scaled by $99/100$ and every mass scaled so that
the leaf’s centre captures at most $1 - 10^{-6}$, each with an exact capture below one
that an evaluator written apart from the crate computes again. The rows are the complete
replays on which T-108 to T-117 rest. For `n29-L581`, decided at the source by the C++
checker, the replay is independent of the producer’s checker. For the nine check2
certificates it is not: the source decided them with its copy of this crate, and
`compare-census` finds the census rows equal to the source’s run logs at every direction,
node counts and bounds alike ([What Check2 Changes](#what-check2-changes)). They are
recorded as re-implemented sharing the producer’s components.

**The source’s C++ checker.** On 6 October 2026 `cpp-sample` ran the source’s C++
checker, `89b674a6…`, built and driven by the source’s own functions from the retained
`mixed_n50_L740` code, at two nodes of each check2 candidate: the least-bound node of the
source’s run log and its last node, at one worker under `nice`. Every node returned
`ANGLE_VERIFIED` at threshold one, with no frontier and no witness, each record holding
lemma N0’s tangent and per-bin domain and each input enclosing the expanded candidate:

```sh
# from packing/
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_declared_net \
  cpp-sample --certificate n20-L4905 --tarball TARBALL --work W --nodes 679,831 --workers 1
```

| Name here | Node | C++ status | C++ lower bound | C++ nodes | CPU seconds | check2’s lower bound there |
| --- | ---: | --- | --- | ---: | ---: | --- |
| `n18-L4705` | 1234 | `ANGLE_VERIFIED` | $1.0000000050433526$ | 185,673 | 136.3 | $1.0000000000680034$ |
| `n18-L4705` | 2072 | `ANGLE_VERIFIED` | $1.0000000479163114$ | 232,227 | 193.6 | $1.0000000480646534$ |
| `n19-L4825` | 1021 | `ANGLE_VERIFIED` | $1.0000004432449892$ | 183,303 | 141.7 | $1.0000000001230112$ |
| `n19-L4825` | 2072 | `ANGLE_VERIFIED` | $1.0000013259288083$ | 226,665 | 196.9 | $1.000000096803216$ |
| `n20-L4905` | 679 | `ANGLE_VERIFIED` | $1.0000004964172489$ | 210,793 | 181.4 | $1.000000000154736$ |
| `n20-L4905` | 831 | `ANGLE_VERIFIED` | $1.0000003740633827$ | 243,315 | 218.8 | $1.0000002351042394$ |
| `n26-L5545` | 241 | `ANGLE_VERIFIED` | $1.00000005320659$ | 228,431 | 128.9 | $1.0000000003495713$ |
| `n26-L5545` | 831 | `ANGLE_VERIFIED` | $1.0000000285447033$ | 435,321 | 391.0 | $1.0000001372085743$ |
| `n27-L56435` | 632 | `ANGLE_VERIFIED` | $1.000000106018499$ | 321,565 | 275.2 | $1.0000000000168654$ |
| `n27-L56435` | 831 | `ANGLE_VERIFIED` | $1.0000000466948722$ | 431,655 | 385.3 | $1.0000000438623011$ |
| `n28-L5735` | 48 | `ANGLE_VERIFIED` | $1.0000002610373988$ | 186,639 | 90.9 | $1.0000000000381999$ |
| `n28-L5735` | 415 | `ANGLE_VERIFIED` | $1.0000000851369437$ | 409,407 | 412.7 | $1.0000000146721826$ |
| `n30-L58835` | 347 | `ANGLE_VERIFIED` | $1.0000006813531397$ | 305,195 | 194.0 | $1.0000000000570795$ |
| `n30-L58835` | 831 | `ANGLE_VERIFIED` | $1.0000002315296308$ | 425,157 | 316.9 | $1.0000000024559188$ |
| `n39-L665` | 394 | `ANGLE_VERIFIED` | $1.000000031004648$ | 762,267 | 713.5 | $1.0000000001966394$ |
| `n39-L665` | 415 | `ANGLE_VERIFIED` | $1.0000000246206686$ | 789,781 | 726.7 | $1.0000000102061601$ |
| `n41-L6775` | 409 | `ANGLE_VERIFIED` | $1.0000001768444517$ | 475,593 | 314.9 | $1.0000000000604714$ |
| `n41-L6775` | 415 | `ANGLE_VERIFIED` | $1.0000002617844366$ | 477,177 | 326.9 | $1.0000002104724752$ |

The C++ bounds are the checker’s own and differ from `sqverify-fast`’s, a different
subdivision of the same domain. The 18 nodes took 5,346 CPU seconds; at their rate a
complete C++ run would take from about 29 CPU-hours (`n28-L5735`) to 97 (`n19-L4825`)
per certificate. The receipts are `receipts/<name>/cpp-sample/`. The review of 6 October
ran the same command at node 1234 of `n18-L4705` and node 409 of `n41-L6775`, with the
same records. Each sample is the producer’s own code at two nodes, a check that shares
no code with `sqverify-fast`, and decides those nodes only.

`sample` replayed `n29-L581`’s shipped records at nodes 0, 1, 364 and 415, the axis and
the least-bound node among them, with the source’s per-node functions after the full
driver’s preconditions: each returned the shipped record, in 855 CPU seconds, 0.71 of the
bundle’s own seconds on the same nodes, which prices the complete oblique replay at about
30 CPU-hours
([`receipts/n29-L581/sample/`](receipts/n29-L581/sample/)).

## Limitations

- **The check2 coverage evidence at the source is a copy of this repository’s
  verifier.** Its runs show that the producer’s check passed; they are not a second
  implementation beside `sqverify-fast`, whose rows equal them.
- **No complete run of the C++ checker exists for the check2 candidates.** The source
  ran none, and the samples here decide only their nodes.
- **Eight of the nine check2 run logs read an unpublished file** (finding FN-1 of the
  review); the replay here reads the published bytes.
- **The bundles are pinned and not held.** A replay needs each tarball from the source at
  the pinned revision, with the digest above.

## Compressed Files

The eleven upstream data files of more than 1,000 lines, the ten candidates and
`mixed_n29_L581`’s certificate, are stored as deterministic gzip made by `gzip -9n`,
with no file name or timestamp in the header. The table gives the Git blob and SHA-256
of the decompressed bytes, which are the file’s blob and digest at the pinned commit;
each SHA-256 is also the one
[`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) pins. The
repository’s readers take the upstream path and decompress through
`devtools.retained_data.read_retained_bytes`, and
`python -m devtools.retained_data check PACKET` re-derives every row.

Before running any of the source’s own programs on this packet, restore the exact upstream
tree from the repository root:

```sh
find packing/resources/web/wand125-mixed-bounds-check2-2026-10-06 -name '*.gz' -exec gunzip -k {} +
```

The restored plain files are untracked, so remove them afterwards; while both copies are
present, the acquisition check reports each as retained twice.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `square-packing-bounds/certificates/mixed_n18_L4705/candidate.json.gz` | upstream | `521ae5e6e38eaae1938a344c6bc7e00ebe724759` | `9eac284b32b9a387ed9c4c6aebf9ba7727d7ce5bce919cc627bc01e3af1e6ddc` |
| `square-packing-bounds/certificates/mixed_n19_L4825/candidate.json.gz` | upstream | `252b2da2106377b8461f181de02d1726b42bb9a1` | `f6b0c354e66563005b0fad7663a6c77172af549dd9feaa3284115c12e43ff063` |
| `square-packing-bounds/certificates/mixed_n20_L4905/candidate.json.gz` | upstream | `8e20b048e5e9cbc7f81cb37875125389b65f4dbb` | `45a17658c3881fb18c6e2f60fa4979bb54a7099ff5f3812de95f2f1140f7fbf0` |
| `square-packing-bounds/certificates/mixed_n26_L5545/candidate.json.gz` | upstream | `9b936ed9a37a3794e6076ac0f9f0fcae2aa6488d` | `842bee847fcb1f6aa67fb58dbbe865e1b111028af71a64684b879ce1832fc119` |
| `square-packing-bounds/certificates/mixed_n27_L56435/candidate.json.gz` | upstream | `e920c9e48bf8cc3b1132ccff2a42fadd9a561a39` | `210af2260ecd6945dc2490d30418990a1fd174f322be59a6c6a2b03902a61a71` |
| `square-packing-bounds/certificates/mixed_n28_L5735/candidate.json.gz` | upstream | `a0998460c10494180aa49fd72d1f148165ddc230` | `8438a806e1864cd11ae89d9505069e8bffaae8a4d5f9a3705e46268ee827e1de` |
| `square-packing-bounds/certificates/mixed_n29_L581/candidate.json.gz` | upstream | `28b6a8cf0c534d2f9bd409ecf472977351af5b3e` | `f7fe2036784e0fa08bde367ce728adbebc58c3abdbbd55f634f1f9ea3dd59d5d` |
| `square-packing-bounds/certificates/mixed_n29_L581/certificate.json.gz` | upstream | `24bf9944e9a5569197396523de8bba9f12005a1a` | `9969202614745f2992e46c78c138bb69204f2516dc7978695a952c0cb4e7a77a` |
| `square-packing-bounds/certificates/mixed_n30_L58835/candidate.json.gz` | upstream | `31d28ad7b30350043e497c398682203af819c47d` | `32f2e77d7871e2ef41e026077816544a9c69de3bd5be12fa742f21986e74cba2` |
| `square-packing-bounds/certificates/mixed_n39_L665/candidate.json.gz` | upstream | `cd03a066c55ab8ac0a044cb7ad644291f45a407b` | `c05781e733ad0b83769d7944ca0ed8b214f9a6c49bf5a46db7fa19c2c325746a` |
| `square-packing-bounds/certificates/mixed_n41_L6775/candidate.json.gz` | upstream | `c2d8729ffa88064b7524b1cc7f79f20508a79ba5` | `854e8b34748919ef55dcff67ded76b51be6b2860bc874e3adb5c572d1897382e` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
