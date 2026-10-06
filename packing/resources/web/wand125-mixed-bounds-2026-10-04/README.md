# wand125 Mixed-Rectangle Certificates of 3 and 4 October 2026, Pinned at `8aa6a10`

This packet pins the 16 certificate directories that
[wand125/square-packing-bounds](https://github.com/wand125/square-packing-bounds) added
from 3 October 2026 19:33 UTC to 4 October 07:17 UTC, from `mixed_n93_L988` to
`mixed_n69_L862`, at the commit that added the last of them. Each was posted in its own
comment on [jlevy/squares#282](https://github.com/jlevy/squares/issues/282). They are
rectangle-density lower bounds of the kind and checker of the
[22 certificates of 3 October](../wand125-mixed-bounds-2026-10-03/README.md), at
$n = 42$ to 44, 51, 56, 57, 67, 69, 72, 75, 84, 86, 88 and 93 to 95.
Its proposed Frontier key is **[wand125 mixed bounds 2026-10-04]**.
The claims below are stated as the source states them.

Nine of the 16 are at counts where an earlier mixed certificate of this source is
retained, and each states a larger side and names the one it supersedes:
`mixed_n51_L747` over `mixed_n51_L746`, `mixed_n69_L862` over `mixed_n69_L8612`,
`mixed_n75_L894` over `mixed_n75_L892`, `mixed_n84_L94075` over `mixed_n84_L940`,
`mixed_n86_L9503` over `mixed_n86_L950`, `mixed_n88_L96125` over `mixed_n88_L960`,
`mixed_n93_L988` over `mixed_n93_L986`, `mixed_n94_L994` over `mixed_n94_L992` and
`mixed_n95_L9965` over `mixed_n95_L996`. The other seven are the source's first mixed
certificates at their counts, each above its own rectangle certificate there.

**The pin moved once before merge.** This packet was first written at `3554616`
(4 October 06:09 UTC), which held the first 14. The source then added `mixed_n86_L9503`
and `mixed_n69_L862`, and since no copy of the packet had merged, it was written again
from a checkout at `8aa6a10`, the head that added the last of them, rather than opened as
a second packet. The 14 earlier directories and the 23 below are byte for byte the same at
both pins.

The packet also retains, at the same pin, the source's answer to review findings OC-1 and
OC-2 on the 22 certificates of 3 October: commit `150939e` removes `completion-audit.json`
from those 22 directories and from `mixed_n96_L996`, and the two README lines that name
it, and changes nothing else in them.

What was checked here is SHA-256 digests, Git blob ids, the exact premises the audit below
recomputes from the retained bytes, and every check the replay makes before its first
angle, run on each pinned tarball. On 6 October `sqverify-fast`, this repository’s
clean-room measure verifier, decided the 16 retained candidates at all 201 net directions
([the independent replays](#the-independent-replays)); the source’s own checker has not
been run here on any of the 16.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/wand125/square-packing-bounds> |
| Revision | `8aa6a10b3b8f165d39c85b68982fed1de086516c`, branch `main`, tree `303cd9d2b594cb62827313c1ca281809a3ce8249`; the head when retrieved, and the revision the last request names |
| Committed | Authored and committed 2026-10-04T07:17:29Z, 16:17 on 4 October by the author’s clock (`+09:00`) |
| Author | wand125, building on Tokoharu’s format and verifier, as for the other mixed certificates |
| Licence | MIT. The root `LICENSE` reads “Copyright (c) 2026 wand125” and is byte-identical to the [September 27 packet’s copy](../wand125-rectangle-certificates-2026-09-27/wand125-rectangles/LICENSE) |
| Retrieved | 2026-10-04, about 07:21Z: a full clone of the whole history, fetched again and checked out at this revision. `git ls-remote` listed one branch and no tag |
| Pinned subtree | 627 files, 732,550,416 bytes: the 16 claim directories, the 23 directories `150939e` changed and the three root files, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) |
| Retained here | 88 files, 3,485,437 bytes upstream, under [`square-packing-bounds/`](square-packing-bounds/), byte-identical to the pinned files after decompression |

**The revisions.** The source’s `main` moved from `2aff2076`, the 3 October packet’s pin,
through 19 commits. Sixteen each add one certificate directory and change the root README,
and nothing else. `150939e` removes `completion-audit.json` from 27 directories, the 23
named below and four of the 16 (`mixed_n44_L69725`, `mixed_n56_L78025`,
`mixed_n84_L94075` and `mixed_n93_L988`, whose first commits carried one), with the two
README lines that name it. `c56b9b7` changes only `certificates/k2m5_n59_L8`, the
$s(59) = 8$ cover of
[the 1 October packet](../wand125-point-and-mixed-2026-10-01/README.md), and `1ebd484`
only `point_n45_L7`, the $s(45) = 7$ cover of
[the 28 September packet](../wand125-point-and-mixed-2026-09-28/README.md); this packet
retains neither. Each claim directory is unchanged at the pin since the commit below, but
for that removal:

| Claim | Directory | Commit | Committed (UTC) | Request |
| --- | --- | --- | --- | --- |
| $s(42) \ge 2739/400$ | `certificates/mixed_n42_L68475` | `aa26adf88f888b84f4822b01ac78285bee952517` | 2026-10-04T05:26:19Z | [05:26:28Z](https://github.com/jlevy/squares/issues/282#issuecomment-5976921462) |
| $s(43) \ge 2763/400$ | `certificates/mixed_n43_L69075` | `eaed02b46ebce92825c6bcbe8369fb98a85cc050` | 2026-10-04T03:40:51Z | [03:41:00Z](https://github.com/jlevy/squares/issues/282#issuecomment-5976238731) |
| $s(44) \ge 2789/400$ | `certificates/mixed_n44_L69725` | `83010fa645edcba0086ecd545b872de08d1ba25c` | 2026-10-03T20:48:15Z | [20:48:25Z](https://github.com/jlevy/squares/issues/282#issuecomment-5973344259) |
| $s(51) \ge 747/100$ | `certificates/mixed_n51_L747` | `0e0bdeac8c69a230293d652ab91a35092084f6fb` | 2026-10-04T02:40:13Z | [02:40:22Z](https://github.com/jlevy/squares/issues/282#issuecomment-5975862606) |
| $s(56) \ge 3121/400$ | `certificates/mixed_n56_L78025` | `cf451aa6f1928f5d9bdfa02db90d370f5b4a4104` | 2026-10-03T20:48:42Z | [20:48:53Z](https://github.com/jlevy/squares/issues/282#issuecomment-5973347580) |
| $s(57) \ge 3149/400$ | `certificates/mixed_n57_L78725` | `bc7272005a81fe368f04eeecf452dc2d0181c24a` | 2026-10-04T03:17:25Z | [03:17:35Z](https://github.com/jlevy/squares/issues/282#issuecomment-5976097725) |
| $s(67) \ge 339/40$ | `certificates/mixed_n67_L8475` | `2475d0850b87ad25797a26f66c6b0b9043db5772` | 2026-10-04T02:38:55Z | [02:39:06Z](https://github.com/jlevy/squares/issues/282#issuecomment-5975854641) |
| $s(69) \ge 431/50$ | `certificates/mixed_n69_L862` | `8aa6a10b3b8f165d39c85b68982fed1de086516c` | 2026-10-04T07:17:29Z | [07:17:40Z](https://github.com/jlevy/squares/issues/282#issuecomment-5977636184) |
| $s(72) \ge 219/25$ | `certificates/mixed_n72_L876` | `c44fd6ff63bac2d9177f4328674ee866a6db55d7` | 2026-10-04T03:04:04Z | [03:04:14Z](https://github.com/jlevy/squares/issues/282#issuecomment-5976012739) |
| $s(75) \ge 447/50$ | `certificates/mixed_n75_L894` | `35b83e75c1250f31033ec82f79d57aafb41533db` | 2026-10-04T02:40:37Z | [02:40:49Z](https://github.com/jlevy/squares/issues/282#issuecomment-5975865370) |
| $s(84) \ge 3763/400$ | `certificates/mixed_n84_L94075` | `c9c6be03b595bd1e9b5181424332dedb5bb9c526` | 2026-10-03T22:03:41Z | [22:03:52Z](https://github.com/jlevy/squares/issues/282#issuecomment-5973933178) |
| $s(86) \ge 9503/1000$ | `certificates/mixed_n86_L9503` | `683264c35764a1c759914ff19ac82d25ce5fa1ca` | 2026-10-04T07:03:48Z | [07:04:00Z](https://github.com/jlevy/squares/issues/282#issuecomment-5977545188) |
| $s(88) \ge 769/80$ | `certificates/mixed_n88_L96125` | `92b1a7e430a7e104f00c935eac59fc7f7846b39e` | 2026-10-04T02:39:20Z | [02:39:30Z](https://github.com/jlevy/squares/issues/282#issuecomment-5975857134) |
| $s(93) \ge 247/25$ | `certificates/mixed_n93_L988` | `b321ac9ad166bf68cd5f19eeaa8b4884537acce3` | 2026-10-03T19:33:34Z | [19:33:45Z](https://github.com/jlevy/squares/issues/282#issuecomment-5972753544) |
| $s(94) \ge 497/50$ | `certificates/mixed_n94_L994` | `3c7c57a8e65364322d976303b0292147ed20d51f` | 2026-10-04T02:39:46Z | [02:39:57Z](https://github.com/jlevy/squares/issues/282#issuecomment-5975860050) |
| $s(95) \ge 1993/200$ | `certificates/mixed_n95_L9965` | `3554616889186f10bff4f14a3e7e194546fc9fca` | 2026-10-04T06:09:45Z | [06:09:55Z](https://github.com/jlevy/squares/issues/282#issuecomment-5977194758) |

## Credit and AI Assistance, as the Source States Them

The root README at the pin is retained. Its Attribution section opens “The method is not
ours.” and credits Walter Stromquist, Hiroshi Nagamochi, Sam Burns, Gustavo Massaccesi
and this repository, and its Status section says “Parts of this work were produced with
AI assistance under human direction.”, as at the 3 October packet’s pin; between the two
pins the root README gains one section per certificate and nothing else.

- **The 16 certificates.** Each directory README calls the checker “the verifier shipped
  here, `code/mixed_rotated_verify.cpp`”, the same checker as for `mixed_n87_L939` and
  `mixed_n65_L835`, and says the certificate is not in Tokoharu’s format because its least
  oblique bound is below the $1.0001$ his `verify.cpp` requires. Each says the candidate
  was built from scratch at its side from a structured initial measure (“bands at integer
  distances from the walls, as in the Green-series certificates”) and repaired against
  counterexamples on the full net.
- **The pre-publication replays.** Each README says the full 201-angle replay was run
  again from the tarball on a fresh Ubuntu 24.04.5 machine with g++ 13.3.0, Python 3.12.3
  and NumPy 2.5.3, after checking the tarball’s SHA-256 and all its file hashes. This was
  not checked.
- **The commits.** Each of the 16 commit messages, and that of `150939e`, ends with a
  co-author trailer naming an AI assistant.

## What Is Retained

Retained byte-identical at their upstream paths: the root `README.md`; from each of the
16 claim directories `README.md`, `candidate.json`, `certificate.json` and
`manifest.json`; and the `README.md` of each of the 23 directories `150939e` changed.

Pinned by digest only, from the 16 claim directories:

| Upstream path | Bytes | SHA-256 |
| --- | ---: | --- |
| `LICENSE` | 1,064 | `c0dd43e7892932c81335f74a2fdbf1a98f5977bab14c0c4c30e3abcc97c34904` |
| `.gitignore` | 132 | `0a31c24fe622ff8b4b012fbf790686063a84da3dd306d47e7283aad434653308` |
| `certificates/mixed_n42_L68475/n42-L6.8475-proof-bundle.tar.gz` | 17,616,206 | `85be7723ccc80d9cfa1b987645642d07121e7c39f973a054d4792375b7eacf06` |
| `certificates/mixed_n43_L69075/n43-L6.9075-proof-bundle.tar.gz` | 14,474,874 | `d00555a224874da9fc0951c50295ee82d4feb7f4740259ec6a36b1424fcf025f` |
| `certificates/mixed_n44_L69725/n44-L6.9725-proof-bundle.tar.gz` | 16,301,347 | `016e64f3b921144c1ae12068db173b2c40e8f9b069aa01b49924e77fb681a5af` |
| `certificates/mixed_n51_L747/n51-L7.47-proof-bundle.tar.gz` | 19,602,681 | `dafc391aec096f27b474c9db03cfea816e24562fc3be2b13d5f1304f4f4273cb` |
| `certificates/mixed_n56_L78025/n56-L7.8025-proof-bundle.tar.gz` | 18,280,962 | `e363ae926d722f24784b300e6d2238d897647af2aa233bebac0dfea68b3da2ce` |
| `certificates/mixed_n57_L78725/n57-L7.8725-proof-bundle.tar.gz` | 22,186,683 | `4e8df55581814f05bf4a60887bdb7b3e005a09265d22e994e262b826711f8612` |
| `certificates/mixed_n67_L8475/n67-L8.475-proof-bundle.tar.gz` | 19,409,082 | `c8f49ba971abba068fa51a61ef8c2e421ba812c4640660474d42bb3f930654a1` |
| `certificates/mixed_n69_L862/n69-L8.62-proof-bundle.tar.gz` | 22,932,912 | `3408beebaa3f6301d3cf4d13cd80d4834ed0d6f41dd7f5dd326175099ca015b5` |
| `certificates/mixed_n72_L876/n72-L8.76-proof-bundle.tar.gz` | 20,039,614 | `36a739ae22aba2dc51726cec1710b9bca83d9c80f87fe7285c267175aa4d6db9` |
| `certificates/mixed_n75_L894/n75-L8.94-proof-bundle.tar.gz` | 25,606,631 | `a576f4183b0367c2e31ae1f6c8cc806c2d40aea5cb4053f6027eabbb2531bcba` |
| `certificates/mixed_n84_L94075/n84-L9.4075-proof-bundle.tar.gz` | 23,518,582 | `01274b160a5b525918cd35fc54362c08d088d6c1e698b98a947908844f0c0b66` |
| `certificates/mixed_n86_L9503/n86-L9.503-proof-bundle.tar.gz` | 21,587,707 | `8752a3e5e9349b6e5a2dccfd1eec1af01f521e5d3e070f53f50a827935966ab3` |
| `certificates/mixed_n88_L96125/n88-L9.6125-proof-bundle.tar.gz` | 20,227,627 | `ca813e22e2756bb71bd69f5b594d349798c0f28da60c0f4b4395d7cde49e2c55` |
| `certificates/mixed_n93_L988/n93-L9.88-proof-bundle.tar.gz` | 20,653,208 | `974382765bbb24e3ad3af98f1c67941f4e2f59ab62da67fe5656c819e6dd69cf` |
| `certificates/mixed_n94_L994/n94-L9.94-proof-bundle.tar.gz` | 26,509,834 | `1de580505be19101eee65c6d11425876b08d8cd6a1da2a04c427a2cfba231780` |
| `certificates/mixed_n95_L9965/n95-L9.965-proof-bundle.tar.gz` | 18,404,631 | `1397341b2303d6cafb701ef4449e8baa07c87d8ec944c5d9473891ea0e680698` |

`LICENSE` is retained byte-identical by the September 27 rectangle packet; a retained
`.gitignore` would act on this repository’s tree. Each tarball is a complete proof bundle,
and each digest is the one its directory’s README states. Each directory’s ten `code/`
files and its `requirements.txt` are byte-identical to the files of the same name in
`mixed_n50_L740/`, which the
[September 28 packet](../wand125-point-and-mixed-2026-09-28/README.md) retains, and are
pinned by digest in the subtree list. No directory of the 16 carries a
`completion-audit.json` at the pin, so none is retained.

From the 23 directories `150939e` changed, everything but the README is pinned by digest
only: the candidate, certificate and manifest are byte-identical to the copies the
[3 October packet](../wand125-mixed-bounds-2026-10-03/README.md) retains (the
[afternoon packet of 2 October](../wand125-mixed-bounds-afternoon-2026-10-02/README.md)
for `mixed_n96_L996`), which the acquisition check compares byte for byte, and each tarball
has the digest the earlier packet pins.

[`acquisition/declaration.json`](acquisition/declaration.json) declares the scope and the
pinned-only rules, and [`acquisition/sources.json`](acquisition/sources.json) records the
pin and every pinned-only file with its size, digest, reason and, where one exists, the
retained copy with the same bytes.
From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source \
  wand125-mixed-bounds-2026-10-04 --checkout CHECKOUT
```

rebuilds the retained files and both acquisition files from a checkout at the pinned
revision, and with `--check` in place of `--checkout CHECKOUT` re-derives the packet from
its manifest without one.

## The Claims, as the Source States Them

| Name here | Claim | Rectangles | Source’s comparison, in its README | Least oblique bound recorded (index) | Axis cells, minimum |
| --- | --- | ---: | --- | --- | --- |
| `n42` | $s(42) \ge 2739/400$ | 431 | its rectangle certificate `rect_n42_L68275` (6.8275) | $1.00000000038929$ (151) | 8,294,400, $1.0028835196743096$ |
| `n43` | $s(43) \ge 2763/400$ | 358 | its rectangle certificate `rect_n43_L68875` (6.8875) | $1.0000000005367042$ (157) | 5,832,225, $1.0041643070776043$ |
| `n44` | $s(44) \ge 2789/400$ | 399 | its rectangle certificate `rect_n44_L69425` (6.9425) | $1.0000000003387242$ (65) | 6,953,769, $1.0045516914701675$ |
| `n51-L747` | $s(51) \ge 747/100$ | 489 | its earlier certificate `mixed_n51_L746` (7.46) | $1.0000000014730677$ (111) | 10,666,756, $1.008708130978039$ |
| `n56` | $s(56) \ge 3121/400$ | 453 | its rectangle certificate `rect_n56_L77825` (7.7825) | $1.0000000002061535$ (1) | 8,720,209, $1.0049777014201027$ |
| `n57` | $s(57) \ge 3149/400$ | 532 | its rectangle certificate `rect_n57_L7835` (7.835) | $1.0000000005590681$ (194) | 12,752,041, $1.0052281611253358$ |
| `n67` | $s(67) \ge 339/40$ | 485 | its rectangle certificate `rect_n67_L8455` (8.455) | $1.0000000001997127$ (199) | 10,131,489, $1.007364912414975$ |
| `n69-L862` | $s(69) \ge 431/50$ | 547 | its earlier certificate `mixed_n69_L8612` (8.612) | $1.0000000022127755$ (163) | 12,687,844, $1.0024591768578492$ |
| `n72` | $s(72) \ge 219/25$ | 488 | its rectangle certificate `rect_n72_L874` (8.74) | $1.000000000255855$ (138) | 9,634,816, $1.0052632530569092$ |
| `n75-L894` | $s(75) \ge 447/50$ | 589 | its earlier certificate `mixed_n75_L892` (8.92) | $1.000000000242291$ (194) | 14,569,489, $1.0035068984112805$ |
| `n84-L94075` | $s(84) \ge 3763/400$ | 569 | its earlier certificate `mixed_n84_L940` (9.4) | $1.000000000096838$ (75) | 14,386,849, $1.0054208378418148$ |
| `n86-L9503` | $s(86) \ge 9503/1000$ | 533 | its earlier certificate `mixed_n86_L950` (9.5) | $1.00000000053539$ (195) | 11,648,569, $1.005655662978928$ |
| `n88-L96125` | $s(88) \ge 769/80$ | 502 | its earlier certificate `mixed_n88_L960` (9.6) | $1.0000000000855427$ (92) | 10,080,625, $1.005555488215099$ |
| `n93-L988` | $s(93) \ge 247/25$ | 501 | its earlier certificate `mixed_n93_L986` (9.86) | $1.0000000007671606$ (184) | 10,660,225, $1.0038863181990088$ |
| `n94-L994` | $s(94) \ge 497/50$ | 630 | its earlier certificate `mixed_n94_L992` (9.92) | $1.0000000019115551$ (166) | 14,130,081, $1.0023446755279655$ |
| `n95-L9965` | $s(95) \ge 1993/200$ | 480 | its earlier certificate `mixed_n95_L996` (9.96) | $1.000000000398967$ (23) | 7,257,636, $1.0078342043789137$ |

All 16 are rectangle densities with no point mass (each `candidate.json` has an empty
`points` list and a `scaling_factor` of `1`), of total mass $n - 1/100000$, with core side
$B = 9977/10000$, 201 net half-angles of step $83/40000$ and coverage threshold $1$, as for
every earlier mixed certificate. Each `certificate.json` has status
`ALL_ANGLES_VERIFIED_AND_REPLAYED`. Each README compares with the source’s own earlier
value at its count, which is the value the record reported there before this import.

## The Exact Audit and the Pre-Replay Checks

From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_point_and_mixed \
  mixed-audit wand125-mixed-bounds-2026-10-04 --check
```

recomputes [`receipts/mixed-audit.json`](receipts/mixed-audit.json) from the retained
bytes and imports no source code, with the checks the 3 October packet describes, but for
the source’s audit, which this revision does not publish: pinned digests; the count,
side, core and rectangle count stated; nonnegative masses inside the container, of total
exactly $n - 1/100000$; the candidate digest by the source’s rule, equal in the manifest,
the certificate and the statement; the net record equal to the containment facts
recomputed here; the checker `89b674a6…` and `code/` the retained $n = 50$ copy; and a
replay record at threshold $1$ for each of the 201 angles.
In place of the source audit’s certificate and tarball digests, each tarball is bound by
its digest at the pinned tree, which `acquire_source` bound to its Git blob at the pinned
commit: the acquisition record must pin that digest with its size, the pinned tree must
hold no `completion-audit.json` in the directory, and the README must state the claim,
the tarball’s name and its digest. All 16 pass. Each side exceeds Green’s DS7 value at its
count, enclosed to 60 digits, and Nagamochi’s $1 + \sqrt{n - 2\lfloor\sqrt n\rfloor + 1}$,
and the centre domains are recomputed at the oblique nodes. None of it decides coverage.

On 4 October `mixed-fetch` was run on each pinned tarball, read from the checkout at the
pinned commit. Each has the pinned SHA-256 and size; each unpacked bundle matches all 621
entries of its `files-sha256.json` with nothing unlisted, and its candidate, certificate,
manifest and `code/` are the retained or `mixed_n50_L740` files; the shipped driver’s
preconditions hold on its own code; every one of the 200 oblique inputs encloses the exact
candidate recomputed here; and every record is `ANGLE_VERIFIED` with an empty frontier at
$\gamma = 1$. That binding of each bundle to the retained certificate is what the source’s
audit used to state. Each run’s output is its certificate’s `receipts/NAME/fetch.json`;
the `bundle` field names the scratch directory it was unpacked in.

| Name here | Rectangle images checked | Oblique nodes | Source’s oblique seconds | Source’s CPU-hours | `mixed-price` CPU-hours | Planned CPU-hours |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `n42` | 3,448 | 84,154,248 | 42,566 | 11.82 | 6.5 | 7.3 |
| `n43` | 2,864 | 94,327,372 | 49,474 | 13.74 | 6.1 | 6.8 |
| `n44` | 3,192 | 61,963,016 | 37,241 | 10.34 | 4.4 | 4.9 |
| `n51-L747` | 3,912 | 73,294,118 | 30,183 | 8.38 | 6.5 | 7.2 |
| `n56` | 3,624 | 95,233,978 | 46,179 | 12.83 | 7.8 | 8.7 |
| `n57` | 4,256 | 92,644,514 | 42,783 | 11.88 | 8.9 | 9.9 |
| `n67` | 3,880 | 80,893,626 | 32,939 | 9.15 | 7.1 | 8.0 |
| `n69-L862` | 4,376 | 108,821,066 | 51,135 | 14.20 | 10.8 | 12.1 |
| `n72` | 3,904 | 120,543,194 | 60,713 | 16.86 | 10.6 | 11.9 |
| `n75-L894` | 4,712 | 120,119,252 | 53,422 | 14.84 | 12.7 | 14.2 |
| `n84-L94075` | 4,552 | 92,867,418 | 33,695 | 9.36 | 9.5 | 10.6 |
| `n86-L9503` | 4,264 | 95,514,032 | 32,601 | 9.06 | 9.2 | 10.2 |
| `n88-L96125` | 4,016 | 110,846,936 | 50,354 | 13.99 | 10.1 | 11.3 |
| `n93-L988` | 4,008 | 71,180,134 | 27,670 | 7.69 | 6.4 | 7.2 |
| `n94-L994` | 5,040 | 82,482,752 | 37,807 | 10.50 | 9.3 | 10.4 |
| `n95-L9965` | 3,840 | 59,167,032 | 19,990 | 5.55 | 5.0 | 5.6 |

The source’s seconds are the bundle’s own record of its oblique run, 180.2 CPU-hours in
all. `mixed-price` scales the rate of the three angles timed on 2 October by each
certificate’s node counts and rectangles, 130.8 CPU-hours in all. The planned column is
that estimate times 1.119, the ratio of measured to estimated CPU-hours over the 14
complete replays already merged in this record (`observed_ratio`), 146.3 CPU-hours in all.
The source’s seconds run further above the estimate here than for the 3 October
certificates (1.38 times, against 1.24), most at $n = 42$ to 44, so budget wall time toward
the source’s figure.

## Replaying the Certificates

The source’s check is its driver `code/verify_mixed_full_proof.py`, run from the unpacked
tarball. `devtools.audit_wand125_point_and_mixed` runs the same check split by net angle,
as for the earlier mixed packets, and names the 16 as in the tables above: a count an
earlier certificate already names takes its side as well.

```sh
# from packing/: one command per range; 0 is the axis direction
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_point_and_mixed \
  mixed-replay n72 --range 0-106 --work /tmp/wand125-n72 --workers 4 --via git
# when every range of a certificate has run
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_point_and_mixed \
  mixed-merge n72
```

Receipts go to `receipts/NAME/range-AAA-BBB/` as each angle finishes, and a rerun replays
only what has not passed.
`mixed-shard wand125-mixed-bounds-2026-10-04 --runners 8` splits the packet across eight
hosts of four workers:

| Runner | Planned CPU-hours | Wall hours at 4 workers | Ranges, run in this order |
| --- | ---: | ---: | --- |
| r1 | 19.0 | 4.8 | `n43` 0–200, `n67` 0–138, `n75-L894` 102–156, `n93-L988` 0–132 |
| r2 | 18.1 | 4.5 | `n42` 135–200, `n72` 161–200, `n75-L894` 0–101, `n88-L96125` 138–200 |
| r3 | 18.1 | 4.5 | `n42` 0–134, `n69-L862` 112–163, `n75-L894` 157–200, `n95-L9965` 0–200 |
| r4 | 18.1 | 4.5 | `n44` 0–200, `n51-L747` 135–200, `n67` 139–200, `n88-L96125` 0–137 |
| r5 | 18.2 | 4.5 | `n51-L747` 0–134, `n56` 136–200, `n57` 0–133, `n84-L94075` 133–200 |
| r6 | 18.2 | 4.6 | `n56` 0–135, `n57` 134–200, `n84-L94075` 0–132, `n93-L988` 133–200 |
| r7 | 18.3 | 4.6 | `n69-L862` 164–200, `n72` 0–106, `n86-L9503` 0–134, `n94-L994` 129–200 |
| r8 | 18.3 | 4.6 | `n69-L862` 0–111, `n72` 107–160, `n86-L9503` 135–200, `n94-L994` 0–128 |

Each runner runs its `mixed-replay` commands one after another, then commits and pushes
its receipts; `mixed-merge NAME` is run for each certificate once every range of it has
arrived. No replay of the source’s checker has been launched.

## The Independent Replays

On 6 October 2026 `devtools.sqverify_fast_census --family mixed` ran `sqverify-fast` on
each retained `candidate.json.gz` at all 201 net directions, at the threshold the
certificate declares, and then refused two mutants of each at its least-bound direction.
All 16 are `VERIFIED`; the receipts are in
[`benchmarks/measure-verifier/census-mixed/`](../../../benchmarks/measure-verifier/census-mixed/README.md),
and each certificate’s evidence entry `E-…-sqverify-fast-replay` states its run.
The build is main’s crate source `d97758bb…`, which the
[soundness review of 6 October](../../../../docs/project/reviews/review-2026-10-06-sqverify-fast-declared-net-soundness.md)
accepted for standard-net certificates; all 16 are on the standard net.

| Certificate | Nodes | Least certified bound (index) | CPU seconds | Threads |
| --- | ---: | --- | ---: | ---: |
| `mixed_n42_L68475` | 77,174,084 | $1.0000000002195921$ (87) | 1,672 | 2 |
| `mixed_n43_L69075` | 85,750,510 | $1.0000000000794018$ (67) | 1,598 | 2 |
| `mixed_n44_L69725` | 55,337,350 | $1.0000000003233136$ (176) | 1,176 | 2 |
| `mixed_n51_L747` | 72,129,554 | $1.000000000916658$ (137) | 1,040 | 1 |
| `mixed_n56_L78025` | 83,847,974 | $1.0000000002764038$ (179) | 1,597 | 2 |
| `mixed_n57_L78725` | 84,325,748 | $1.0000000000104121$ (184) | 1,816 | 1 |
| `mixed_n67_L8475` | 75,088,660 | $1.0000000006600718$ (183) | 1,299 | 1 |
| `mixed_n69_L862` | 92,221,320 | $1.000000000173938$ (11) | 2,198 | 2 |
| `mixed_n72_L876` | 93,877,670 | $1.000000000071343$ (87) | 2,259 | 2 |
| `mixed_n75_L894` | 102,689,438 | $1.000000000005104$ (198) | 2,705 | 2 |
| `mixed_n84_L94075` | 83,220,602 | $1.0000000005252527$ (117) | 1,494 | 2 |
| `mixed_n86_L9503` | 82,400,840 | $1.00000000020883$ (179) | 1,458 | 1 |
| `mixed_n88_L96125` | 91,617,282 | $1.000000000448649$ (193) | 1,788 | 2 |
| `mixed_n93_L988` | 56,860,974 | $1.0000000008842913$ (116) | 1,317 | 1 |
| `mixed_n94_L994` | 66,819,374 | $1.0000000001238274$ (171) | 1,912 | 2 |
| `mixed_n95_L9965` | 47,780,470 | $1.0000000013097659$ (96) | 1,054 | 2 |

They took 7.3 CPU-hours in all, at one thread while the shared four-core host was
heavily loaded and at two once it was freer. The verifier was written without opening
the source’s checker and shares no code with it, so these are independent decisions of
coverage by the same method, not reproductions of the source’s records. The source’s
checker remains unreplayed here; the range commands above would add that reproduction.

## The Answer to Findings OC-1 and OC-2

The [review of the 3 October certificates](../../../../docs/project/reviews/review-2026-10-03-wand125-october-3-certificates.md)
found that the `improvement_lower` of two of their `completion-audit.json` files is not a
lower bound on the margin (OC-1), and that six compare with values no published
certificate holds (OC-2). `150939e` is the source’s answer. Its message reads “Their
improvement figures compared with superseded or unpublished values (jlevy/squares#282,
review of T-082, OC-1 and OC-2). Each README’s own comparison, taken from the published
record, is unchanged, as are the certificates, the bundles and their hashes.”

That is what the pinned tree shows. In each of the 22 directories of 3 October and in
`mixed_n96_L996`, the files at `8aa6a10` are the files at `2aff2076` (at `b00fc70f` for
`mixed_n96_L996`) less `completion-audit.json`; the README loses the two lines that list
it and is otherwise unchanged; and the candidate, certificate, manifest, tarball, `code/`
and `requirements.txt` keep their digests. The acquisition check compares the candidate,
certificate and manifest with the earlier packets’ copies, and
`tests/test_wand125_mixed_rectangles.py` compares every digest of the two subtree lists.
The 3 October packet keeps the removed audits as they were published there.

## Limitations

- **The source’s checker is not replayed.** Coverage was decided here by `sqverify-fast`
  alone; the source’s C++ and its axis tables have not run on any of the 16.
- **No source audit.** The source’s `completion-audit.json` no longer exists for any of
  the 16, so nothing the source publishes binds a certificate to its tarball but the
  README’s digest and the commit. The binding here is the pinned tree’s digest and, after
  `mixed-fetch`, the bundle’s own file list and its proof files.
- **The bundles are pinned and not held.** A replay needs each tarball from the source at
  the pinned revision, with the digest above. `--via git` fetches it by Git.

## Compressed Files

The 32 upstream data files of more than 1,000 lines, the 16 candidates and the 16
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
find packing/resources/web/wand125-mixed-bounds-2026-10-04 -name '*.gz' -exec gunzip -k {} +
```

The restored plain files are untracked, so remove them afterwards; while both copies are
present, the acquisition check reports each as retained twice.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `square-packing-bounds/certificates/mixed_n42_L68475/candidate.json.gz` | upstream | `168529a390759f7969af8432144a8c86d03df361` | `95da4dbf1f4bb72a24388c291468f11fb94154909d663cbf7c127ceecc6e6cfd` |
| `square-packing-bounds/certificates/mixed_n42_L68475/certificate.json.gz` | upstream | `a5f3f8925bd2191723a10aefd87aa7c3ae0268ea` | `206d6d005aa6adf2b40cc41987b00cc7f609bf3079892130e29beeca1e35e6b0` |
| `square-packing-bounds/certificates/mixed_n43_L69075/candidate.json.gz` | upstream | `b5150f6bf13ea4583c1d0731edea8cdc3f98f37f` | `b74817ddc92d4ef3675615df8842dd2b5b833da37a176652b61dfccdfee23426` |
| `square-packing-bounds/certificates/mixed_n43_L69075/certificate.json.gz` | upstream | `670673ebbbfbc4655e0043b83a6c24bb62586ea1` | `899d2f142a5300d2ffff21746d533f4c28092f61106c0f8b840eae08b701a688` |
| `square-packing-bounds/certificates/mixed_n44_L69725/candidate.json.gz` | upstream | `0a8f90f448337b12eabed01b394fcc5491d18461` | `8f495ceba269db0d1de58ef746dc06c0a31eb51f9ef023bf1f1f38b582374f2f` |
| `square-packing-bounds/certificates/mixed_n44_L69725/certificate.json.gz` | upstream | `3c961e49dc6db2ad16013a26f40613c62b852cdd` | `15b992a4c42216ba1d47b6d5c2431f5baf52daed78123e16e1b84720e4d50fd7` |
| `square-packing-bounds/certificates/mixed_n51_L747/candidate.json.gz` | upstream | `b7dc4669132118d7d32db58c26bc3a774be3ffc1` | `21fc48aab3ab7aaae02421135e63fde33ac1a8c8acaaff90a04f4eb6f2de5f93` |
| `square-packing-bounds/certificates/mixed_n51_L747/certificate.json.gz` | upstream | `f55951c4e65e826a42193a424700f2f433b24f44` | `262bd316eff47b970c257493ee3ea99fd6d57b36e9790cbfac97acb3172e7ac4` |
| `square-packing-bounds/certificates/mixed_n56_L78025/candidate.json.gz` | upstream | `43af92f2d3ae8e61ce9dc72b64f0aa65bba98e3e` | `9755c84ffb727f047277a2862ce002bd556bb5d77697e1f50f2949958392f517` |
| `square-packing-bounds/certificates/mixed_n56_L78025/certificate.json.gz` | upstream | `cac5a7c90aa0c8aee50c403d446cbf5868be140b` | `5687e287bfb8b043cddccceb63a20815037fba559f1d64c8295749616c246652` |
| `square-packing-bounds/certificates/mixed_n57_L78725/candidate.json.gz` | upstream | `65768569cdbf5c564a8c8daf40fb537a0d5ba959` | `50c34cd8476ab90e42ef1e64d7ca6ffb6e918d1d72632ce0c9621748d4625e7b` |
| `square-packing-bounds/certificates/mixed_n57_L78725/certificate.json.gz` | upstream | `a96b09469ba3979fa5a74dfdd08979699d80e659` | `132acfe567cf6455104a63c63d285ed9e04c793c70878c9d3d542cf1048dfe4d` |
| `square-packing-bounds/certificates/mixed_n67_L8475/candidate.json.gz` | upstream | `c55b3a10ced589f4df89af6153440822cda71239` | `ac26408ee16d9a5d72870199d939131774a40c83db813201671e01e75d3ae9a7` |
| `square-packing-bounds/certificates/mixed_n67_L8475/certificate.json.gz` | upstream | `5716ee1c7dae614f5de5e1138e5cd8a941ac6289` | `5e19cfe2b9fde087a0fda86759549607358cf75d3427e1e0b490f193e726e017` |
| `square-packing-bounds/certificates/mixed_n69_L862/candidate.json.gz` | upstream | `2e39b063455a27464a6305d12dee273e1253a6eb` | `3f90303fe70daa9fa92efa1c0e9f78e678d8b0a41a7cf977f71eb735c884ef38` |
| `square-packing-bounds/certificates/mixed_n69_L862/certificate.json.gz` | upstream | `dc7178be3f25d8375d77476a35a64f2aee240f82` | `5f791a3148d2a177701c57f8e9d2e24f86ca97f00ead45ffeec5f209930327b2` |
| `square-packing-bounds/certificates/mixed_n72_L876/candidate.json.gz` | upstream | `daa53a49d58e7ec3245de3d9f529df247d875e18` | `bd27a8887aa27c9e09ac7196ba05bb1bbc07553b632c42500790092251ffab03` |
| `square-packing-bounds/certificates/mixed_n72_L876/certificate.json.gz` | upstream | `806b97b74dca928d753430079b70bab1e5ad770b` | `7d30feb35737a40eee496ca3d94b664d9ad8eb133014b33df69fadd7018c21ac` |
| `square-packing-bounds/certificates/mixed_n75_L894/candidate.json.gz` | upstream | `f6875ff808038adcd7e1464d289b4e7eff7a9328` | `7dad25cbd2a7b60c796a46cd9a7b4b9d2cb1d88519deef3e6721e0102a56d596` |
| `square-packing-bounds/certificates/mixed_n75_L894/certificate.json.gz` | upstream | `1e4c1b92ce8b9797227aea3c906a72753eda8679` | `ef288f9c84b2c8ecabc4a51a0b86ef271fa817090a46a1df2056d8c7750f19bc` |
| `square-packing-bounds/certificates/mixed_n84_L94075/candidate.json.gz` | upstream | `b2f9fac4638185f6f36cc18c9c83b06337f10bce` | `2dd49b9a57e9386a65d3ed231d689d9660eea65f634286102a6e59b8ea89aafc` |
| `square-packing-bounds/certificates/mixed_n84_L94075/certificate.json.gz` | upstream | `161ba8b46f5ab75070164acd162722ca7fb5c0db` | `1b33f32333bb5fe629d29b0b9b3a93aae40f3d5bbaecc52f9f576e590a44c12b` |
| `square-packing-bounds/certificates/mixed_n86_L9503/candidate.json.gz` | upstream | `f9dc8fc0815cc040728c67f0724caaf59816542e` | `e3b897b9f009a295d5bac45ec3cf95abe790a8fcf7e9762f0a6144ea43150254` |
| `square-packing-bounds/certificates/mixed_n86_L9503/certificate.json.gz` | upstream | `a3e64e56fc4b8414dbcce0b19974f01a0aa91664` | `9bd69d3eddbd7debe9a07006c0c1f6f46d03cddf20ca4a44a2a54e8608a79b96` |
| `square-packing-bounds/certificates/mixed_n88_L96125/candidate.json.gz` | upstream | `3d910cd6421272852a6b26c35c7bcf4b70d078a1` | `9ea8fc4d9f2cc58e3829ff3f71212c3503337c6260ab0e7d41f77077c2ef68c0` |
| `square-packing-bounds/certificates/mixed_n88_L96125/certificate.json.gz` | upstream | `2cb2bee5dc662e244c4c5b1ca6d31df243f44fef` | `3dff02f73c3c6926cb96a783e8be2f8aa9a05f4d6d16ff9e2894c03d360c84e8` |
| `square-packing-bounds/certificates/mixed_n93_L988/candidate.json.gz` | upstream | `ff3c5d9299c2f039d199e36804f5f54e75ec1b88` | `e14a405894add77229b02ad41016c4949b0853408019086242fef5bb12ac1b8c` |
| `square-packing-bounds/certificates/mixed_n93_L988/certificate.json.gz` | upstream | `da61c6bdeefda5c32048f9b3e267b992b5cac579` | `02ffd10e3be3db985414ce8127c640e2f3a837a631828ab003a2c01611334a9e` |
| `square-packing-bounds/certificates/mixed_n94_L994/candidate.json.gz` | upstream | `96d745ef59cc3748bc73908bf93e071e7091d361` | `a1c76954188e35a72407d31921c8a74745194f4f9da04c8e54be9274d75d3247` |
| `square-packing-bounds/certificates/mixed_n94_L994/certificate.json.gz` | upstream | `2920025f2f59931e5ab34644d5e0497025e9d28b` | `719b2b05f3693a0585461af792f9d4269a7d4ced7ae24d4c54f4a3020f57e9f5` |
| `square-packing-bounds/certificates/mixed_n95_L9965/candidate.json.gz` | upstream | `5592e15ed90b4e258f89b298f123a285933ce896` | `d4a35ff32b6d5a2985b854c5a09a8c7596db6550c8e784a52a41e579e33de1e1` |
| `square-packing-bounds/certificates/mixed_n95_L9965/certificate.json.gz` | upstream | `08700c9fc3c8fa32045d36b26f2f9ac6b046f6fe` | `a4f9998b50d0ce124a5ad58776137d340d4cb8932c6c1b421d3505449c4e09ba` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
