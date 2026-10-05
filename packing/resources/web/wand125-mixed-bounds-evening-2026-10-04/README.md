# wand125 Mixed-Rectangle Certificates of 4 October 2026, Pinned at `797bdf6`

This packet pins the 12 certificate directories that
[wand125/square-packing-bounds](https://github.com/wand125/square-packing-bounds) added
on 4 October 2026 from 07:51 to 19:03 UTC, from `mixed_n91_L97625` to `mixed_n58_L7935`,
at the commit that added the last of them, and the two it added earlier that morning,
`mixed_n86_L9503` and `mixed_n69_L862`, which are unchanged here. Each of the 14 was
posted in its own comment on [jlevy/squares#282](https://github.com/jlevy/squares/issues/282)
between 07:04 and 19:04 UTC. They are rectangle-density lower bounds of the kind and
checker of the [certificates of 3 and 4 October](../wand125-mixed-bounds-2026-10-04/README.md),
at $n = 53$, 54, 58, 69, 70, 71, 73, 76, 86, 87, 88, 90, 91 and 94.
Its proposed Frontier key is **[wand125 mixed bounds evening 2026-10-04]**.
The claims below are stated as the source states them.

Twelve of the 14 are at counts where an earlier mixed certificate of this source is
retained, and each states a larger side and names the one it supersedes:
`mixed_n58_L7935` over `mixed_n58_L7905`, `mixed_n69_L862` over `mixed_n69_L8612`,
`mixed_n70_L86575` over `mixed_n70_L86475`, `mixed_n71_L8721` over `mixed_n71_L8705`,
`mixed_n73_L8813` over `mixed_n73_L8809`, `mixed_n76_L8965` over `mixed_n76_L896`,
`mixed_n86_L9503` over `mixed_n86_L950`, `mixed_n87_L958` over `mixed_n87_L955`,
`mixed_n88_L962` over `mixed_n88_L96125`, `mixed_n90_L973` over `mixed_n90_L9725`,
`mixed_n91_L97625` over `mixed_n91_L975` and `mixed_n94_L995` over `mixed_n94_L994`.
`mixed_n53_L76275` and `mixed_n54_L7685` are the source’s first mixed certificates at their
counts, each above its own rectangle certificate there.

**Two of the 14 are retained in the earlier packet.** `mixed_n86_L9503` (`683264c`) and
`mixed_n69_L862` (`8aa6a10`) were posted before the
[4 October packet](../wand125-mixed-bounds-2026-10-04/README.md) was pinned at `8aa6a10`,
and that packet retains them, with their exact audit and pre-replay receipts. Here they are
pinned by digest at `797bdf6`, and the acquisition check compares each retained file with
that packet’s copy byte for byte; their tarballs have the digests it pins. The other 14
certificates of that packet are not part of this import.

What was checked here is SHA-256 digests, Git blob ids, the exact premises the audit below
recomputes from the retained bytes, and every check the replay makes before its first
angle, run on each pinned tarball. Nothing was replayed: no direction of any of the 14 has
been decided here.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/wand125/square-packing-bounds> |
| Revision | `797bdf6e10eba5f9dccca9da06f8352e81ba9dde`, branch `main`, tree `2f4a2d442ea6c8568f8bd2f6a4a9f5b483157d37`; the head when retrieved, and the revision the last request names |
| Committed | Authored and committed 2026-10-04T19:03:58Z, 04:03 on 5 October by the author’s clock (`+09:00`) |
| Author | wand125, building on Tokoharu’s format and verifier, as for the other mixed certificates |
| Licence | MIT. The root `LICENSE` reads “Copyright (c) 2026 wand125” and is byte-identical to the [September 27 packet’s copy](../wand125-rectangle-certificates-2026-09-27/wand125-rectangles/LICENSE) |
| Retrieved | 2026-10-05, about 00:44Z: a blobless clone of the whole history, checked out sparsely at this revision. `git ls-remote` listed one branch and no tag |
| Pinned subtree | 227 files, 307,605,128 bytes: the 14 claim directories and the three root files, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) |
| Retained here | 49 files, 2,646,691 bytes upstream, under [`square-packing-bounds/`](square-packing-bounds/), byte-identical to the pinned files after decompression |

**The revisions.** The source’s `main` moved from `8aa6a10`, the 4 October packet’s pin,
through 14 commits. Twelve each add one certificate directory and change the root README,
and nothing else. The other two are outside this packet’s scope and are not retained:
`3f063bd` changes only `certificates/k2m4_n77_L9`, the $s(77) = 9$ cover of
[the 1 October packet](../wand125-point-and-mixed-2026-10-01/README.md), adding its run
logs and a full replay record and hardening its `verify.sh`, the cover unchanged; and
`781afb3` changes only `point_n21_L5`, the $s(21) = 5$ certificate of
[the 28 September packet](../wand125-point-and-mixed-2026-09-28/README.md), removing
absolute machine paths from its records and correcting its lemma-code map, the certificate
unchanged by its message. Each claim directory is unchanged at the pin since the commit
below:

| Claim | Directory | Commit | Committed (UTC) | Request |
| --- | --- | --- | --- | --- |
| $s(53) \ge 3051/400$ | `certificates/mixed_n53_L76275` | `62ff7b2cc66d0062d4a171d9a03259ff0dde61ff` | 2026-10-04T15:22:09Z | [15:22:20Z](https://github.com/jlevy/squares/issues/282#issuecomment-5981531224) |
| $s(54) \ge 1537/200$ | `certificates/mixed_n54_L7685` | `d62b47f76638eca10b14d09cbbe53522b2d2781d` | 2026-10-04T13:34:30Z | [13:34:40Z](https://github.com/jlevy/squares/issues/282#issuecomment-5980542490) |
| $s(58) \ge 1587/200$ | `certificates/mixed_n58_L7935` | `797bdf6e10eba5f9dccca9da06f8352e81ba9dde` | 2026-10-04T19:03:58Z | [19:04:09Z](https://github.com/jlevy/squares/issues/282#issuecomment-5983355904) |
| $s(69) \ge 431/50$ | `certificates/mixed_n69_L862` | `8aa6a10b3b8f165d39c85b68982fed1de086516c` | 2026-10-04T07:17:29Z | [07:17:40Z](https://github.com/jlevy/squares/issues/282#issuecomment-5977636184) |
| $s(70) \ge 3463/400$ | `certificates/mixed_n70_L86575` | `4df6bccc26acaa2e6743b43dd2444a6240ab0afd` | 2026-10-04T17:59:55Z | [18:00:05Z](https://github.com/jlevy/squares/issues/282#issuecomment-5982829543) |
| $s(71) \ge 8721/1000$ | `certificates/mixed_n71_L8721` | `5d095211fa8c9f4c44082f271596d9d3f33e2462` | 2026-10-04T11:24:57Z | [11:25:11Z](https://github.com/jlevy/squares/issues/282#issuecomment-5979433224) |
| $s(73) \ge 8813/1000$ | `certificates/mixed_n73_L8813` | `23e75daea7d5df39c95f66610ca975cfbf89df1d` | 2026-10-04T14:48:43Z | [14:48:52Z](https://github.com/jlevy/squares/issues/282#issuecomment-5981239835) |
| $s(76) \ge 1793/200$ | `certificates/mixed_n76_L8965` | `a2cbd0f10520c66bc3312b295061a853bd44e85a` | 2026-10-04T09:06:27Z | [09:06:36Z](https://github.com/jlevy/squares/issues/282#issuecomment-5978370513) |
| $s(86) \ge 9503/1000$ | `certificates/mixed_n86_L9503` | `683264c35764a1c759914ff19ac82d25ce5fa1ca` | 2026-10-04T07:03:48Z | [07:04:00Z](https://github.com/jlevy/squares/issues/282#issuecomment-5977545188) |
| $s(87) \ge 479/50$ | `certificates/mixed_n87_L958` | `98bb26633ca74d84dcb2329921054f35952479a0` | 2026-10-04T12:19:39Z | [12:19:52Z](https://github.com/jlevy/squares/issues/282#issuecomment-5979851892) |
| $s(88) \ge 481/50$ | `certificates/mixed_n88_L962` | `9a26e8db59bfc04264afa1746b7032dc3abdd4b3` | 2026-10-04T16:05:53Z | [16:06:03Z](https://github.com/jlevy/squares/issues/282#issuecomment-5981908116) |
| $s(90) \ge 973/100$ | `certificates/mixed_n90_L973` | `324c1899896cddf7e042c189aa6b3aa4f64d58e8` | 2026-10-04T09:19:39Z | [09:19:49Z](https://github.com/jlevy/squares/issues/282#issuecomment-5978461213) |
| $s(91) \ge 781/80$ | `certificates/mixed_n91_L97625` | `02f981ad27f7acdf986a53f8d0b00cc31564238c` | 2026-10-04T07:51:33Z | [07:51:44Z](https://github.com/jlevy/squares/issues/282#issuecomment-5977856616) |
| $s(94) \ge 199/20$ | `certificates/mixed_n94_L995` | `8a81f65e22f226a8b2e85aca9a0354c22eb05f2e` | 2026-10-04T15:21:27Z | [15:21:43Z](https://github.com/jlevy/squares/issues/282#issuecomment-5981525788) |

## Credit and AI Assistance, as the Source States Them

The root README at the pin is retained. Its Attribution section opens “The method is not
ours.” and credits Walter Stromquist, Hiroshi Nagamochi, Sam Burns, Gustavo Massaccesi
and this repository, and its Status section says “Parts of this work were produced with
AI assistance under human direction.”, as at the 4 October packet’s pin; between the two
pins the root README gains one section per certificate and nothing else.

- **The 12 certificates.** Each directory README calls the checker “the verifier shipped
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
- **The commits.** Each of the 14 commit messages ends with a co-author trailer naming an
  AI assistant.

## What Is Retained

Retained byte-identical at their upstream paths: the root `README.md`, and from each of the
12 claim directories `README.md`, `candidate.json`, `certificate.json` and
`manifest.json`.

Pinned by digest only, from the 14 claim directories:

| Upstream path | Bytes | SHA-256 |
| --- | ---: | --- |
| `LICENSE` | 1,064 | `c0dd43e7892932c81335f74a2fdbf1a98f5977bab14c0c4c30e3abcc97c34904` |
| `.gitignore` | 132 | `0a31c24fe622ff8b4b012fbf790686063a84da3dd306d47e7283aad434653308` |
| `certificates/mixed_n53_L76275/n53-L7.6275-proof-bundle.tar.gz` | 20,679,843 | `8ad91b2f66a1820bb34d7b602a9e70cc90d4d46001029560b1dbf65a6c394482` |
| `certificates/mixed_n54_L7685/n54-L7.685-proof-bundle.tar.gz` | 14,726,624 | `cb7ba0c801ca4872c0dcbcb020ab03c696939cb9b3d1a565e680d629ccd61e59` |
| `certificates/mixed_n58_L7935/n58-L7.935-proof-bundle.tar.gz` | 23,811,454 | `64b3906371e29b20fdfec1846e4c6d4420bf12a190fa7ca88f3bb366dad2c805` |
| `certificates/mixed_n69_L862/n69-L8.62-proof-bundle.tar.gz` | 22,932,912 | `3408beebaa3f6301d3cf4d13cd80d4834ed0d6f41dd7f5dd326175099ca015b5` |
| `certificates/mixed_n70_L86575/n70-L8.6575-proof-bundle.tar.gz` | 21,232,906 | `5e9d7b0b8ee7ac03d9039bde31c8f8c02b9c272573c81550a5061a0a2b1f2a47` |
| `certificates/mixed_n71_L8721/n71-L8.721-proof-bundle.tar.gz` | 22,323,926 | `b44d6a377c363e527a8fed5f47585d785f0cc187ab07100f4f8ca7d735ae99c1` |
| `certificates/mixed_n73_L8813/n73-L8.813-proof-bundle.tar.gz` | 18,989,101 | `1be9a7fd92d360a0d558c14c08ce67ecc01c131db3afce90e4e80d9c774cf3a0` |
| `certificates/mixed_n76_L8965/n76-L8.965-proof-bundle.tar.gz` | 11,918,563 | `2e2cf21c4aac16d3cf9e3a76dc093b62ee5b3040dffeb3224e2bf5af04f4ac9c` |
| `certificates/mixed_n86_L9503/n86-L9.503-proof-bundle.tar.gz` | 21,587,707 | `8752a3e5e9349b6e5a2dccfd1eec1af01f521e5d3e070f53f50a827935966ab3` |
| `certificates/mixed_n87_L958/n87-L9.58-proof-bundle.tar.gz` | 24,859,047 | `d5a5c75538169af5955c5180d5e2965b443c201758e09930319d01232c91c7ea` |
| `certificates/mixed_n88_L962/n88-L9.62-proof-bundle.tar.gz` | 23,003,472 | `af5e3ec714cf9e0f72657c2c9cfea55e5b7fb931d80de23d522f351d5b92e89b` |
| `certificates/mixed_n90_L973/n90-L9.73-proof-bundle.tar.gz` | 21,824,125 | `0040519809a1ddee976129a3b2448c24dd1f5681738d59b66e705d75105583c1` |
| `certificates/mixed_n91_L97625/n91-L9.7625-proof-bundle.tar.gz` | 17,633,045 | `23cccb32c5cec0591e3de9277eae7fa9dc28674839ffaca57959e656d7619a6a` |
| `certificates/mixed_n94_L995/n94-L9.95-proof-bundle.tar.gz` | 38,451,298 | `1a02b7c3d49a8070a97be334a3194d28629c2199958a9c503b8d2ed3dacc666f` |

`LICENSE` is retained byte-identical by the September 27 rectangle packet; a retained
`.gitignore` would act on this repository’s tree. Each tarball is a complete proof bundle,
and each digest is the one its directory’s README states. Each directory’s ten `code/`
files and its `requirements.txt` are byte-identical to the files of the same name in
`mixed_n50_L740/`, which the
[September 28 packet](../wand125-point-and-mixed-2026-09-28/README.md) retains, and are
pinned by digest in the subtree list. No directory of the 14 carries a
`completion-audit.json` at the pin. The `README.md`, candidate, certificate and manifest of
`mixed_n69_L862` and `mixed_n86_L9503` are pinned by digest only, byte-identical to the
copies the 4 October packet retains, which the acquisition check compares.

[`acquisition/declaration.json`](acquisition/declaration.json) declares the scope and the
pinned-only rules, and [`acquisition/sources.json`](acquisition/sources.json) records the
pin and every pinned-only file with its size, digest, reason and, where one exists, the
retained copy with the same bytes.
From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source \
  wand125-mixed-bounds-evening-2026-10-04 --checkout CHECKOUT
```

rebuilds the retained files and both acquisition files from a checkout at the pinned
revision, and with `--check` in place of `--checkout CHECKOUT` re-derives the packet from
its manifest without one.

## The Claims, as the Source States Them

| Name here | Claim | Rectangles | Source’s comparison, in its README | Least oblique bound recorded (index) | Axis cells, minimum |
| --- | --- | ---: | --- | --- | --- |
| `n53` | $s(53) \ge 3051/400$ | 505 | its rectangle certificate `rect_n53_L76075` (7.6075) | $1.0000000008724097$ (144) | 11,075,584, $1.0027812868265755$ |
| `n54` | $s(54) \ge 1537/200$ | 364 | its rectangle certificate `rect_n54_L76725` (7.6725) | $1.000000000441897$ (130) | 5,784,025, $1.0035007233937916$ |
| `n58-L7935` | $s(58) \ge 1587/200$ | 543 | its earlier certificate `mixed_n58_L7905` (7.905) | $1.0000000000544693$ (197) | 13,645,636, $1.0038605675365069$ |
| `n69-L862` | $s(69) \ge 431/50$ | 547 | its earlier certificate `mixed_n69_L8612` (8.612) | $1.0000000022127755$ (163) | 12,687,844, $1.0024591768578492$ |
| `n70-L86575` | $s(70) \ge 3463/400$ | 513 | its earlier certificate `mixed_n70_L86475` (8.6475) | $1.0000000012817085$ (52) | 11,029,041, $1.003788998037493$ |
| `n71-L8721` | $s(71) \ge 8721/1000$ | 529 | its earlier certificate `mixed_n71_L8705` (8.705) | $1.0000000000794815$ (155) | 12,089,529, $1.0041688505547262$ |
| `n73-L8813` | $s(73) \ge 8813/1000$ | 462 | its earlier certificate `mixed_n73_L8809` (8.809) | $1.000000000257511$ (59) | 9,174,841, $1.0055622862385354$ |
| `n76-L8965` | $s(76) \ge 1793/200$ | 312 | its earlier certificate `mixed_n76_L896` (8.96) | $1.0000000071639858$ (195) | 3,272,481, $1.0080659385288$ |
| `n86-L9503` | $s(86) \ge 9503/1000$ | 533 | its earlier certificate `mixed_n86_L950` (9.5) | $1.00000000053539$ (195) | 11,648,569, $1.005655662978928$ |
| `n87-L958` | $s(87) \ge 479/50$ | 594 | its earlier certificate `mixed_n87_L955` (9.55) | $1.0000000002556373$ (129) | 14,348,944, $1.0044705977715256$ |
| `n88-L962` | $s(88) \ge 481/50$ | 562 | its earlier certificate `mixed_n88_L96125` (9.6125) | $1.0000000001523959$ (182) | 12,439,729, $1.0075198562530931$ |
| `n90-L973` | $s(90) \ge 973/100$ | 525 | its earlier certificate `mixed_n90_L9725` (9.725) | $1.0000000003386997$ (151) | 11,242,609, $1.0063623824958494$ |
| `n91-L97625` | $s(91) \ge 781/80$ | 438 | its earlier certificate `mixed_n91_L975` (9.75) | $1.00000000007525$ (179) | 7,711,729, $1.0019646623662337$ |
| `n94-L995` | $s(94) \ge 199/20$ | 853 | its earlier certificate `mixed_n94_L994` (9.94) | $1.0000000002976601$ (134) | 29,430,625, $1.0031738677875834$ |

All 14 are rectangle densities with no point mass (each `candidate.json` has an empty
`points` list and a `scaling_factor` of `1`), of total mass $n - 1/100000$, with core side
$B = 9977/10000$, 201 net half-angles of step $83/40000$ and coverage threshold $1$, as for
every earlier mixed certificate. Each `certificate.json` has status
`ALL_ANGLES_VERIFIED_AND_REPLAYED`. Each README compares with the source’s own earlier
value at its count. That is the value the record reported there before this import at the
twelve counts other than $n = 88$ and 94; there the record reported the source’s
`mixed_n88_L960` ($48/5$) and `mixed_n94_L992` ($248/25$), and the certificates of earlier
that day that the READMEs name, $769/80$ and $497/50$, are retained in the 4 October packet
and not registered.

## The Exact Audit and the Pre-Replay Checks

From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_point_and_mixed \
  mixed-audit wand125-mixed-bounds-evening-2026-10-04 --check
```

recomputes [`receipts/mixed-audit.json`](receipts/mixed-audit.json) for the 12 from the
retained bytes and imports no source code, with the checks the 4 October packet describes:
pinned digests; the count, side, core and rectangle count stated; nonnegative masses inside
the container, of total exactly $n - 1/100000$; the candidate digest by the source’s rule,
equal in the manifest, the certificate and the statement; the net record equal to the
containment facts recomputed here; the checker `89b674a6…` and `code/` the retained
$n = 50$ copy; a replay record at threshold $1$ for each of the 201 angles; and each
tarball bound by its digest at the pinned tree, which `acquire_source` bound to its Git
blob at the pinned commit, with the size the acquisition record pins, no
`completion-audit.json` in the directory, and the claim, the tarball’s name and its digest
stated in the README. All 12 pass. Each side exceeds Green’s DS7 value at its count,
enclosed to 60 digits, and Nagamochi’s $1 + \sqrt{n - 2\lfloor\sqrt n\rfloor + 1}$, and the
centre domains are recomputed at the oblique nodes. `mixed_n69_L862` and
`mixed_n86_L9503` pass the same audit in the 4 October packet’s receipt. None of it decides
coverage.

On 5 October `mixed-fetch` was run on each of the 12 pinned tarballs, read from the
checkout at the pinned commit, in 2.5 minutes of wall time in all. Each has the pinned
SHA-256 and size; each unpacked bundle matches all 621 entries of its `files-sha256.json`
with nothing unlisted, and its candidate, certificate, manifest and `code/` are the retained
or `mixed_n50_L740` files; the shipped driver’s preconditions hold on its own code; every
one of the 200 oblique inputs encloses the exact candidate recomputed here; and every
record is `ANGLE_VERIFIED` with an empty frontier at $\gamma = 1$. Each run’s output is its
certificate’s `receipts/NAME/fetch.json`; the `bundle` field names the scratch directory it
was unpacked in. The receipts for `n69-L862` and `n86-L9503` are the 4 October packet’s.

| Name here | Rectangle images checked | Oblique nodes | Source’s oblique seconds | Source’s CPU-hours | `mixed-price` CPU-hours | Planned CPU-hours |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `n53` | 4,040 | 80,696,352 | 33,491 | 9.30 | 7.4 | 8.3 |
| `n54` | 2,912 | 86,248,776 | 33,629 | 9.34 | 5.7 | 6.4 |
| `n58-L7935` | 4,344 | 84,183,576 | 40,827 | 11.34 | 8.2 | 9.2 |
| `n69-L862` | 4,376 | 108,821,066 | 51,135 | 14.20 | 10.8 | 12.1 |
| `n70-L86575` | 4,104 | 118,708,596 | 46,401 | 12.89 | 11.0 | 12.3 |
| `n71-L8721` | 4,232 | 114,091,518 | 45,935 | 12.76 | 10.9 | 12.2 |
| `n73-L8813` | 3,696 | 116,555,688 | 44,434 | 12.34 | 9.7 | 10.9 |
| `n76-L8965` | 2,496 | 50,978,010 | 14,404 | 4.00 | 2.8 | 3.1 |
| `n86-L9503` | 4,264 | 95,514,032 | 32,601 | 9.06 | 9.2 | 10.3 |
| `n87-L958` | 4,752 | 107,739,744 | 44,625 | 12.40 | 11.6 | 13.0 |
| `n88-L962` | 4,496 | 106,388,036 | 35,713 | 9.92 | 10.8 | 12.1 |
| `n90-L973` | 4,200 | 123,232,842 | 51,540 | 14.32 | 11.7 | 13.1 |
| `n91-L97625` | 3,504 | 120,868,018 | 45,589 | 12.66 | 9.6 | 10.7 |
| `n94-L995` | 6,824 | 115,335,002 | 59,040 | 16.40 | 17.5 | 19.6 |

The source’s seconds are the bundle’s own record of its oblique run, 160.9 CPU-hours for
the 14. `mixed-price` scales the rate of the three angles timed on 2 October by each
certificate’s node counts and rectangles, 136.9 CPU-hours. The planned column is that
estimate times 1.119, the ratio of measured to estimated CPU-hours over the 14
complete replays already merged in this record (`observed_ratio`), 153.3 CPU-hours in
all: 130.9 for the 12 this packet holds, and 22.4 for `n69-L862` and `n86-L9503`.

## Replaying the Certificates

The source’s check is its driver `code/verify_mixed_full_proof.py`, run from the unpacked
tarball. `devtools.audit_wand125_point_and_mixed` runs the same check split by net angle,
as for the earlier mixed packets, and names the 12 as in the tables above: a count an
earlier certificate already names takes its side as well.

```sh
# from packing/: one command per range; 0 is the axis direction
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_point_and_mixed \
  mixed-replay n94-L995 --range 0-67 --work /tmp/wand125-n94-L995 --workers 4 --via git
# when every range of a certificate has run
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_point_and_mixed \
  mixed-merge n94-L995
```

Receipts go to `receipts/NAME/range-AAA-BBB/` as each angle finishes, and a rerun replays
only what has not passed.
`mixed-shard wand125-mixed-bounds-evening-2026-10-04 --runners 6` splits the 12 across
six hosts of four workers; at eight it leaves one host 16 per cent above the mean, at six
2 per cent:

| Runner | Planned CPU-hours | Wall hours at 4 workers | Ranges, run in this order |
| --- | ---: | ---: | --- |
| r1 | 22.3 | 5.6 | `n73-L8813` 0–134, `n73-L8813` 135–200, `n90-L973` 136–200, `n94-L995` 167–200 |
| r2 | 22.1 | 5.5 | `n58-L7935` 133–200, `n87-L958` 0–138, `n88-L962` 138–200, `n94-L995` 0–78 |
| r3 | 21.6 | 5.4 | `n53` 0–137, `n88-L962` 0–137, `n90-L973` 0–135, `n94-L995` 79–126 |
| r4 | 22.1 | 5.5 | `n58-L7935` 0–132, `n71-L8721` 137–200, `n87-L958` 139–200, `n94-L995` 127–166 |
| r5 | 21.0 | 5.3 | `n54` 0–200, `n71-L8721` 0–136, `n76-L8965` 0–200, `n91-L97625` 137–200 |
| r6 | 21.8 | 5.5 | `n53` 138–200, `n70-L86575` 0–137, `n70-L86575` 138–200, `n91-L97625` 0–136 |

Each runner runs its `mixed-replay` commands one after another, then commits and pushes
its receipts; `mixed-merge NAME` is run for each certificate once every range of it has
arrived. `n69-L862` and `n86-L9503` are replayed once, under their 4 October packet
names, and their receipts go to that packet: a seventh host running `mixed-replay
n69-L862 --range 0-200` and `mixed-replay n86-L9503 --range 0-200` carries 22.4 planned
CPU-hours, about 5.6 wall hours at four workers, unless that packet’s own replay runs them
first. No replay has been launched.

## Limitations

- **Nothing is replayed.** Coverage is decided by the source’s C++ alone, and no direction
  of any of the 14 has been run here.
- **No source audit.** No directory of the 14 carries the source’s `completion-audit.json`,
  so nothing the source publishes binds a certificate to its tarball but the README’s
  digest and the commit. The binding here is the pinned tree’s digest and, after
  `mixed-fetch`, the bundle’s own file list and its proof files.
- **The bundles are pinned and not held.** A replay needs each tarball from the source at
  the pinned revision, with the digest above. `--via git` fetches it by Git.

## Compressed Files

The 24 upstream data files of more than 1,000 lines, the 12 candidates and the 12
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
find packing/resources/web/wand125-mixed-bounds-evening-2026-10-04 -name '*.gz' -exec gunzip -k {} +
```

The restored plain files are untracked, so remove them afterwards; while both copies are
present, the acquisition check reports each as retained twice.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `square-packing-bounds/certificates/mixed_n53_L76275/candidate.json.gz` | upstream | `8d137ca2a4b88676df9ae5414cc914475ff64127` | `fe21d3717240bd7ab0d1e72a38dd859b09af04f9975099ebb0da2ca8d60cc8d9` |
| `square-packing-bounds/certificates/mixed_n53_L76275/certificate.json.gz` | upstream | `f0f7451af7fb643843db4254cb27da07c0f5e80e` | `2de77f57f3cf671f34944c33d4d702d7f4da29efe8daa846b5a375e15eaf6708` |
| `square-packing-bounds/certificates/mixed_n54_L7685/candidate.json.gz` | upstream | `244d4a79f98fbb89ba4df0c9fececca56d790ef7` | `3b6e8bfbde4af5a5bd999d49202244956daaadf21a1d66ec7352e2edbe1be774` |
| `square-packing-bounds/certificates/mixed_n54_L7685/certificate.json.gz` | upstream | `a92dc212633e7668132c3a67f43d5020be654a46` | `e701760c1d0f718d8c7c59324126866f69ca402b02710b14b975b736fdc644db` |
| `square-packing-bounds/certificates/mixed_n58_L7935/candidate.json.gz` | upstream | `544d314211a25c10464e0a05c70b0ef769c3ed35` | `f7ebc067411c3893e690e0ecec94e95be1932ca8bbb0d88236b8fcf879d1ffcc` |
| `square-packing-bounds/certificates/mixed_n58_L7935/certificate.json.gz` | upstream | `32ece94689b16947b9e48b5da0df83260fd4bb91` | `ff459ed0317fe21a06ddc0e792c287045a0bf972352074c395072550460dd5ac` |
| `square-packing-bounds/certificates/mixed_n70_L86575/candidate.json.gz` | upstream | `9f1431ac2f382715da03dd8373316733470c7ac9` | `50f7475132be75733fea922480a7be5173e1e0c5ce9695e249b649d51911a27c` |
| `square-packing-bounds/certificates/mixed_n70_L86575/certificate.json.gz` | upstream | `d6901eb02028abb1b30d0473c6311ad15a88ecd2` | `91c11f49fb8c6370928475f7dd93c87951f34cd0d28417e398f145acf8a5f582` |
| `square-packing-bounds/certificates/mixed_n71_L8721/candidate.json.gz` | upstream | `42cfd39165b13d2baca110b77013bf8b2296cd5c` | `e4b71029357e7d4a772bd5fe68aac3d6b60f0a1186fbc48597652812a0805074` |
| `square-packing-bounds/certificates/mixed_n71_L8721/certificate.json.gz` | upstream | `75379b6a0c684dca4ef90f6d8f30baa437d3104c` | `c772e798f8c788aca65b24abc93683ccdcf36696979b5aa2962f5054a1f14b48` |
| `square-packing-bounds/certificates/mixed_n73_L8813/candidate.json.gz` | upstream | `6b21533bf2d3259949a2d199fcef3f4a6ac57429` | `464f6a0b04bc84f6cefb851def257e37855140a080c04ff7fa8c42428494df38` |
| `square-packing-bounds/certificates/mixed_n73_L8813/certificate.json.gz` | upstream | `0c68daea4426c24560494f39e7e84123eb8683b1` | `5365891e3e8282c7af257b5b215cb1fc379c25b4af49e6656f114e386521b8b7` |
| `square-packing-bounds/certificates/mixed_n76_L8965/candidate.json.gz` | upstream | `bd9161c90d57c2fbd3e3ad388f18b2347ef270a7` | `11e9d3012222bfc225284d3090876c2c6c55c74233193cc317ad632fa19ccd1e` |
| `square-packing-bounds/certificates/mixed_n76_L8965/certificate.json.gz` | upstream | `4b28059d8beee2b03edf99c2ceb36e3e98b9bef5` | `df4084717029f4fb2b9d0f037995cfe3543736e084ab3d28feaea7413575e7b7` |
| `square-packing-bounds/certificates/mixed_n87_L958/candidate.json.gz` | upstream | `7e773e58de32dc0b6ef0a3d212ce51450acc720c` | `ae1d392ca4d638b4a9390a0224c15cb6839a2e3c19b03f2fed7426e12dc95c9f` |
| `square-packing-bounds/certificates/mixed_n87_L958/certificate.json.gz` | upstream | `98de33f256ea2864c08a0b8844286da7fce0f05a` | `02b9fa90d26dae1412bea7effa4f16449c9895132a2aaeb7989a28bcc56c4da3` |
| `square-packing-bounds/certificates/mixed_n88_L962/candidate.json.gz` | upstream | `b0543a40dd853e558efe44453d737ecbe5cf9158` | `663b5d99b69e39c8deb8b1adb9f9e0f197b243038a0a5cc125a94de0dfdf7620` |
| `square-packing-bounds/certificates/mixed_n88_L962/certificate.json.gz` | upstream | `b4365f1fd230b05aaaf8437655bce29b7f99c334` | `02444bae576e34e9c4431197224949f7baf31c2e67036d832ed31f05b1718b21` |
| `square-packing-bounds/certificates/mixed_n90_L973/candidate.json.gz` | upstream | `e658e106bafd25d94e33e43ef331fdbbc9435ebe` | `4cecdd2c2a6c2132f9167853f6417b7f33001e57cf35667e2d6553ba14cc0ddc` |
| `square-packing-bounds/certificates/mixed_n90_L973/certificate.json.gz` | upstream | `ad2e34b6b9211c839f030f398491b0eeeafc9fa3` | `9d32a31eb7098404a66b663a0c3b99ee536ed5a0925b227bedbf9c5798451dc0` |
| `square-packing-bounds/certificates/mixed_n91_L97625/candidate.json.gz` | upstream | `d72c4cd773a0789f5f028dc23ac73552aad74d63` | `22a128c2f0a991ee68bfab0845cff204cdca28789e4f8ca5a7a56301dc28e2c2` |
| `square-packing-bounds/certificates/mixed_n91_L97625/certificate.json.gz` | upstream | `a8e626560550c56c11fd6818bd349ae275ff965d` | `a238c338f5dc5b832a761d7b54d211726e6a4bdb88364f6c8234da97647e1609` |
| `square-packing-bounds/certificates/mixed_n94_L995/candidate.json.gz` | upstream | `c9ed3393bc3da71755c6125c1a3abad0b2a08dc7` | `64d819536a9994172b1f7a7b2095e7b40e420a09efa7441d459e73191a20667a` |
| `square-packing-bounds/certificates/mixed_n94_L995/certificate.json.gz` | upstream | `a273c16ef6e280545498dac5d94895cb9766589d` | `65322f0cd597f37a3a4ebd4ae6ab1cad5541b804071be878ca748cb2de6e34c7` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
