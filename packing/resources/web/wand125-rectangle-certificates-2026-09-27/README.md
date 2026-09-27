# wand125 Rectangle-Density Certificates Retrieved 2026-09-27

This packet pins the rectangle-density lower-bound certificates that
[wand125/square-packing-bounds](https://github.com/wand125/square-packing-bounds) added
on 2026-09-26 and 2026-09-27, and keeps this repository’s audit and replay receipts for
them. Its Frontier key is **[wand125 rectangle bounds 2026]**.

The same repository’s earlier point certificates, at revision `1398e42`, are in the
[September 22 packet](../external-square-certificates-2026-09-22/README.md) under
**[wand125 point bounds 2026]**. Those remain valid; the rectangle certificates here
supersede them as the strongest bounds at every count both cover.

## Source and Pin

| Field | Value |
| --- | --- |
| Revision | `ad43d29d96d0d9740b34643b5ac3fb960909cf9c`, branch `main`, tree `d1207dcdb98890dee13b461771e04b49df8cf9e2` |
| Author | wand125, building on Tokoharu’s solver and interval verifier; the source README says parts of the work were produced with AI assistance under human direction |
| Licence | MIT, retained as [`wand125-rectangles/LICENSE`](wand125-rectangles/LICENSE) |
| Tags, releases, submodules, Git LFS | none |
| Upstream tree | 1,367 files, each pinned by SHA-256 in [`acquisition/upstream-tree.sha256`](acquisition/upstream-tree.sha256) |
| Retained here | 184 files under [`wand125-rectangles/`](wand125-rectangles/), byte-identical to the pinned tree after decompression ([Compressed Files](#compressed-files)) |

[`acquisition/sources.json`](acquisition/sources.json) records the pin, the file counts
and the claim list.
`python -m devtools.audit_wand125_rectangles --acquire CHECKOUT` rebuilds both files and
the retained subset from a clean checkout at the pinned revision.

## What Is Retained

The source tree is 186 MB, almost all of it certificate directories: 192 of them, one per
rung of each count’s ladder. This packet keeps the evidence for the standing
(highest) certificate at each of the 44 counts and pins the rest by digest.

- The source `README.md`, `LICENSE`, `requirements.txt` and `docs/`.
- For each standing certificate: `certified_candidate.json` (the exact data: side,
  shrink, rectangles and rational weights), `certificate_metadata.json` (exact mass and
  input digest), and the upstream accepting run’s `verification_summary.json` and
  `verified_angles.jsonl`.

Two kinds of file are pinned by digest and not copied:

- **`certificate_input.txt`**, 35 MB across the 44 certificates.
  It is the candidate rewritten as outward-rounded binary64 intervals, so it carries no
  information of its own.
  The audit tool regenerates it from the candidate and requires the SHA-256 that both
  the metadata and the upstream run recorded, so the bytes replayed are the bytes that
  were published.
- **`verify.cpp` and `run_verify.py`**, which are byte-identical in every certificate
  directory to Tokoharu’s copies retained in the September 22 packet (SHA-256
  `a75140df…` and `7bce2467…`). The audit tool runs those retained copies.

Lower rungs, the four matching certificates, the ten point certificates and `src/` at
this revision are pinned by digest only.
`src/` holds the point-certificate search and checker; the rectangle certificates were
built with Tokoharu’s solver, which is not part of this tree.
Leaving out its Python also keeps the change-reachable test selection from treating
foreign modules as repository code.

## Claims

Each standing certificate proves `s(n) >= L`: its mass is strictly below `n`, and every
rotated, translated unit square captures mass at least one.
A certificate of mass below `k` refutes `k` squares too, so it also bounds every larger
count; at `n = 77` the `n = 76` certificate gives `89/10`, stronger than the direct
`222/25`.

| `n` | Certificate | Side | Mass | Rectangles |
| --- | --- | --- | --- | --- |
| 18 | `rect_n18_L4695` | `939/200` = 4.695 | `1799/100` = 17.99 | 199 |
| 19 | `rect_n19_L4815` | `963/200` = 4.815 | `1899/100` = 18.99 | 213 |
| 20 | `rect_n20_L4895` | `979/200` = 4.895 | `1999/100` = 19.99 | 208 |
| 21 | `rect_n21_L4985` | `997/200` = 4.985 | `20999/1000` = 20.999 | 136 |
| 26 | `rect_n26_L553` | `553/100` = 5.53 | `2599/100` = 25.99 | 256 |
| 27 | `rect_n27_L56` | `28/5` = 5.6 | `26999/1000` = 26.999 | 168 |
| 28 | `rect_n28_L5695` | `1139/200` = 5.695 | `2799/100` = 27.99 | 162 |
| 29 | `rect_n29_L5785` | `1157/200` = 5.785 | `2899/100` = 28.99 | 194 |
| 30 | `rect_n30_L5865` | `1173/200` = 5.865 | `2999/100` = 29.99 | 176 |
| 31 | `rect_n31_L592` | `148/25` = 5.92 | `3099/100` = 30.99 | 155 |
| 32 | `rect_n32_L595` | `119/20` = 5.95 | `3199/100` = 31.99 | 135 |
| 37 | `rect_n37_L64` | `32/5` = 6.4 | `3699/100` = 36.99 | 253 |
| 38 | `rect_n38_L652` | `163/25` = 6.52 | `3799/100` = 37.99 | 351 |
| 39 | `rect_n39_L662` | `331/50` = 6.62 | `3899/100` = 38.99 | 420 |
| 40 | `rect_n40_L6695` | `1339/200` = 6.695 | `3999/100` = 39.99 | 453 |
| 41 | `rect_n41_L6745` | `1349/200` = 6.745 | `4099/100` = 40.99 | 386 |
| 42 | `rect_n42_L676` | `169/25` = 6.76 | `4199/100` = 41.99 | 298 |
| 43 | `rect_n43_L6855` | `1371/200` = 6.855 | `4299/100` = 42.99 | 334 |
| 44 | `rect_n44_L6925` | `277/40` = 6.925 | `4399/100` = 43.99 | 335 |
| 45 | `rect_n45_L6955` | `1391/200` = 6.955 | `4499/100` = 44.99 | 227 |
| 51 | `rect_n51_L743` | `743/100` = 7.43 | `5099/100` = 50.99 | 441 |
| 52 | `rect_n52_L7505` | `1501/200` = 7.505 | `5199/100` = 51.99 | 466 |
| 53 | `rect_n53_L758` | `379/50` = 7.58 | `5299/100` = 52.99 | 477 |
| 54 | `rect_n54_L7665` | `1533/200` = 7.665 | `5399/100` = 53.99 | 558 |
| 55 | `rect_n55_L77` | `77/10` = 7.7 | `5499/100` = 54.99 | 572 |
| 56 | `rect_n56_L776` | `194/25` = 7.76 | `5599/100` = 55.99 | 578 |
| 57 | `rect_n57_L78` | `39/5` = 7.8 | `5699/100` = 56.99 | 511 |
| 58 | `rect_n58_L788` | `197/25` = 7.88 | `5799/100` = 57.99 | 544 |
| 59 | `rect_n59_L7905` | `1581/200` = 7.905 | `5899/100` = 58.99 | 484 |
| 60 | `rect_n60_L792` | `198/25` = 7.92 | `5999/100` = 59.99 | 417 |
| 61 | `rect_n61_L796` | `199/25` = 7.96 | `6099/100` = 60.99 | 375 |
| 66 | `rect_n66_L8345` | `1669/200` = 8.345 | `6599/100` = 65.99 | 542 |
| 67 | `rect_n67_L844` | `211/25` = 8.44 | `6699/100` = 66.99 | 716 |
| 68 | `rect_n68_L846` | `423/50` = 8.46 | `6799/100` = 67.99 | 594 |
| 69 | `rect_n69_L8545` | `1709/200` = 8.545 | `6899/100` = 68.99 | 735 |
| 70 | `rect_n70_L861` | `861/100` = 8.61 | `6999/100` = 69.99 | 662 |
| 71 | `rect_n71_L8645` | `1729/200` = 8.645 | `7099/100` = 70.99 | 709 |
| 72 | `rect_n72_L8705` | `1741/200` = 8.705 | `7199/100` = 71.99 | 754 |
| 73 | `rect_n73_L874` | `437/50` = 8.74 | `7299/100` = 72.99 | 752 |
| 74 | `rect_n74_L8815` | `1763/200` = 8.815 | `7399/100` = 73.99 | 732 |
| 75 | `rect_n75_L889` | `889/100` = 8.89 | `7499/100` = 74.99 | 798 |
| 76 | `rect_n76_L89` | `89/10` = 8.9 | `7599/100` = 75.99 | 706 |
| 77 | `rect_n77_L888` | `222/25` = 8.88 | `7699/100` = 76.99 | 545 |
| 78 | `rect_n78_L8955` | `1791/200` = 8.955 | `7799/100` = 77.99 | 812 |

“Rectangles” counts the positive-weight orbit representatives; the checker sees eight
images of each.
Every certificate improves the reported lower bound this register held on 2026-09-27,
but at `n = 21` and `n = 32` Evan Daniel’s separately registered `s(21) >= 5000/1001` and
`s(32) = 6` are stronger, so those two are superseded priors and move neither lane.

## How the Certificates Were Made

The method and checker are Tokoharu’s, reviewed here on 2026-09-22 in the
[density mathematics review](../../../../docs/project/reviews/review-2026-09-22-tokoharu-density-mathematics.md).
wand125 ran Tokoharu’s solver, climbed each count rung by rung, and before each recorded
run multiplied every weight by one exact rational factor that brings the mass to
`n - 1/100` (`n - 1/1000` at `n = 21` and `n = 27`).
The factor is recorded in each candidate under `scaling_experiment`.
Scaling changes only how the certificate was found: the checker reads the scaled data,
and the audit checks its mass exactly.

## Receipts

The audit tool is
[`devtools/audit_wand125_rectangles.py`](../../../devtools/audit_wand125_rectangles.py).
It reuses the exact preflight of `devtools/audit_tokoharu_density.py`, with each
certificate’s own pinned side.

- [`receipts/preflight/audit.json`](receipts/preflight/audit.json): the exact preflight
  of all 44 standing certificates from the retained subset.
  For each, the regenerated input matches the published SHA-256, every interval
  encloses its exact datum, the axis-event partition is complete, orbit normalization
  preserves mass, and the exact mass is below `n`.
- [`receipts/replay/audit.json`](receipts/replay/audit.json): complete 201-direction
  coverage replays of the unchanged checker, with each run’s standard output, summary
  and per-angle rows beside it.
  It lists only the certificates replayed so far.

The full set needs about 102 CPU hours by the upstream per-angle times, so it runs in
batches. From `packing/`, with the project CPython 3.14 environment and a C++17 `g++`
on `PATH`:

```bash
.venv/bin/python3 -m devtools.audit_wand125_rectangles \
  --out resources/web/wand125-rectangle-certificates-2026-09-27/receipts/replay \
  --resume --replay --workers 2 --n 18 --n 19
.venv/bin/python3 -m devtools.apply_wand125_rectangles
```

`--resume` keeps the certificates already accepted in that directory.
`apply_wand125_rectangles` then promotes exactly the replayed counts, and their
monotone consequences, into the verified lane; unreplayed counts keep the reported
entry `E-wand125-rectangle-report`.

## Compressed Files

The 44 standing candidates, `certified_candidate.json` in each certificate directory,
are over 1,000 lines each.
Each is stored as deterministic gzip made by `gzip -9n`, with no file name or timestamp
in the header, following the [R052 packet](../n17-guzhou-r052-2026-09-25/README.md).
The table gives the Git blob and SHA-256 of the decompressed bytes, which for an
upstream file are its blob and digest at the pinned commit and for a receipt are the
bytes this repository wrote.
The repository’s readers take the upstream path and decompress transparently through
`devtools.retained_data.read_retained_bytes`, and
`python -m devtools.retained_data check PACKET` (run by
`packing/tests/test_retained_data.py`) re-derives every row.
Each SHA-256 is also the one [`acquisition/upstream-tree.sha256`](acquisition/upstream-tree.sha256)
pins, and `devtools.audit_wand125_rectangles` checks the retained subset against that
manifest through the decompressed bytes.

Before running any of the source’s own programs on this packet, restore the exact
upstream tree from the repository root:

```sh
find packing/resources/web/wand125-rectangle-certificates-2026-09-27 -name '*.gz' -exec gunzip -k {} +
```

The restored plain files are untracked, so remove them afterwards; while both copies
are present, the repository’s readers require them to agree.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `wand125-rectangles/certificates/rect_n18_L4695/certified_candidate.json.gz` | upstream | `2506ecc97c36f720ad1152377c846b593d5ba209` | `ca83e64dbcf220bac0cce3ce658eee91522d0ba33f5ccb6d286afe7f076b0a2a` |
| `wand125-rectangles/certificates/rect_n19_L4815/certified_candidate.json.gz` | upstream | `0f519d8e10aeb1379f43e0d7ea354d9daacfed2f` | `8276792ac1cc80399842267e65d86e99cad37b65829ee864247ad057f7007f88` |
| `wand125-rectangles/certificates/rect_n20_L4895/certified_candidate.json.gz` | upstream | `28d120eb3897f83ce188a79ce1e2e5f311941d77` | `4b49797fd0a30aa52f212e7b8cd8121be778fafb5d4828ced71fb4aa41d23ebc` |
| `wand125-rectangles/certificates/rect_n21_L4985/certified_candidate.json.gz` | upstream | `678b60fc7ebf119d40a3ddc4b2d885bb72a7ce5d` | `3f6fc8e1a1789726bd93b0a34eb89a7c556bd5dde057300b2281a472e8ebf09d` |
| `wand125-rectangles/certificates/rect_n26_L553/certified_candidate.json.gz` | upstream | `06a03e3a15237c842c6619fb79723f991c7c7bf4` | `e9492bfa6f081f8404880e085badaaf61909ffbeef2d217871002b543e3dca1b` |
| `wand125-rectangles/certificates/rect_n27_L56/certified_candidate.json.gz` | upstream | `9d38abbb73d1265c2b1d01ff65bc0f58eaa78782` | `e0c57af4048ef0a14e8cd2c29d8360abc6c46483edc02652914f94fed18f50d6` |
| `wand125-rectangles/certificates/rect_n28_L5695/certified_candidate.json.gz` | upstream | `8fcc2e9e882aa915a6b51eba1ad056573151dfc1` | `27b43c7407c9bba805c7949699594f922de3eb057bc6979c3e03fc7fd7c75c69` |
| `wand125-rectangles/certificates/rect_n29_L5785/certified_candidate.json.gz` | upstream | `36915fe35e1e55c04016808660ad69781130c359` | `9263d9a7e77e95df7c75b794f1c7ebd6f34601b7c5e428e9cc175ff84839b37b` |
| `wand125-rectangles/certificates/rect_n30_L5865/certified_candidate.json.gz` | upstream | `bd22be7a0c85b0fafa2d570b8ab2cc9cc95b523b` | `403caacad5c80f67a61c8f6420ac6ab2e84b7c17ab49f1e8923ab223b8d17984` |
| `wand125-rectangles/certificates/rect_n31_L592/certified_candidate.json.gz` | upstream | `185f9ae36cc8534073da97aa8b6b955317182c81` | `371b6d9d8d76f31c4b08db05ee6f5042fcfd4ecba63244376fed08e8626daa11` |
| `wand125-rectangles/certificates/rect_n32_L595/certified_candidate.json.gz` | upstream | `9a41c9742973a381aaa912c0658e519184c51d85` | `57292ff69cc1ecb86e3798a6aad859df79c8dcfb78ffe260717a93d9b37f8895` |
| `wand125-rectangles/certificates/rect_n37_L64/certified_candidate.json.gz` | upstream | `4893afafcd79b85040d9be366fae22b9db533318` | `84297a2344e89c8c3b3c5f88bd66a0e3433a747ad019e66f542e3f37dfe95153` |
| `wand125-rectangles/certificates/rect_n38_L652/certified_candidate.json.gz` | upstream | `ce5580a703db0fee070d4aed9465571f6f21951b` | `43f65f0965b21ba63469d445c19e665d2eef175168473b1d9b8f6e6ea51c3b7a` |
| `wand125-rectangles/certificates/rect_n39_L662/certified_candidate.json.gz` | upstream | `a5470636012cda2a5032820f913027702dae18de` | `3c3b07e1f882707e102de9947336e10ec5077c832b7bf0285c91a76a1986c87a` |
| `wand125-rectangles/certificates/rect_n40_L6695/certified_candidate.json.gz` | upstream | `bbd27723d0a09dc23a9af07c65921a342a14de40` | `86cdd9d4864f14020fe4331d1ac90d9d9a0c960a55212a27c4cbe9f517ae8671` |
| `wand125-rectangles/certificates/rect_n41_L6745/certified_candidate.json.gz` | upstream | `bac957d61949975b1b458d4310ff426b95b9800c` | `1d14c9b676dc92259cd1811ea3ddd9a0805f681e2ad47634ca20e64efa3104e8` |
| `wand125-rectangles/certificates/rect_n42_L676/certified_candidate.json.gz` | upstream | `3e7bab62c125d2eb6a25b622c139c8fbe995f385` | `9f8619e3fdb01e6af2e79d814b337ad535656afb6c1e9c77d455ebacb1785785` |
| `wand125-rectangles/certificates/rect_n43_L6855/certified_candidate.json.gz` | upstream | `4395c774ebe41262ed09aa91c93995b8fa55b26c` | `24f7207bcd5103e92cb610a8075086a1f55bb9fc0ee96a08fd1674c52692752d` |
| `wand125-rectangles/certificates/rect_n44_L6925/certified_candidate.json.gz` | upstream | `e323f8978ac7d9e5f6d8ed75529a8c211a3dfea5` | `195104c4f0de64e169f2273fc12fdde131d27b1e9824ed0b1399caf99b8d3e8e` |
| `wand125-rectangles/certificates/rect_n45_L6955/certified_candidate.json.gz` | upstream | `ab749850b9699d0627053a249be7d09d8d7e244c` | `eeca07aa7308c7f88c203127afbdb9193ed081460fdb47f6755882b6747c5890` |
| `wand125-rectangles/certificates/rect_n51_L743/certified_candidate.json.gz` | upstream | `1b8a4326f57af09f516b6432cc9cf958d72cbf0d` | `41e10dc227324b5263b1a7178c7e994245ca52635a1a2218360b2043f0d00460` |
| `wand125-rectangles/certificates/rect_n52_L7505/certified_candidate.json.gz` | upstream | `8c164a2d4524dadf3c47f42bf316d59a5f6368cf` | `53d5ed62c9cad4dbdd0b2dc4802337d635105adc2da56cb02d240dc2aac069ee` |
| `wand125-rectangles/certificates/rect_n53_L758/certified_candidate.json.gz` | upstream | `41c6265ee38a2d4565abe55ca3257eee1da9bd0b` | `fcb29a7cf1d3fc0a222a4bf9baef70c7bf0626ea6a28c5bb84765b041a115bc8` |
| `wand125-rectangles/certificates/rect_n54_L7665/certified_candidate.json.gz` | upstream | `11b8942afbee4a9eb35da71fee7cbee72f62b114` | `82bee0fa9fe15d507859990c716ecdbc1c85d2b1814a077dd5c7fc80048d8a1b` |
| `wand125-rectangles/certificates/rect_n55_L77/certified_candidate.json.gz` | upstream | `330a990e731494f35bc949ffc247d858824dd722` | `8e85f0f0648ae416866502f9779e7846704c39b69710bf3485fe7ee4f44a74fd` |
| `wand125-rectangles/certificates/rect_n56_L776/certified_candidate.json.gz` | upstream | `a6e98793160eaa301c55e9e11310b8c7c0fbf093` | `0f891d33f49f8434dd132fcde5bfb2a98f173bb0ad8f84dc158d08ff420375c0` |
| `wand125-rectangles/certificates/rect_n57_L78/certified_candidate.json.gz` | upstream | `964dd1d7cb1ebbcf44abd422c6a98d8d6c1e8ed6` | `508ce0342f0189b0897bc460fba66e65213ee7141febde95a40ce94e5dbb5df5` |
| `wand125-rectangles/certificates/rect_n58_L788/certified_candidate.json.gz` | upstream | `2b633acc9a840990527f77cf1cdede12459a38a3` | `1b238a5b66bb304ac52b05f77252981c0b67956647e41e330514b1f07f80980b` |
| `wand125-rectangles/certificates/rect_n59_L7905/certified_candidate.json.gz` | upstream | `739735d4386293baeabe7388def58c50afbcdbf8` | `f273831f3a805a39db0a137d7388ed586368ee7c1f3235ac5f3a180c1e21f2a8` |
| `wand125-rectangles/certificates/rect_n60_L792/certified_candidate.json.gz` | upstream | `b56973edd53e2e6f761c666b906ffdf7004088d8` | `88c0f804d3d6baaf4db062c738c34aa512b8ece3b7d0bdf92ddef7fbc12d92ab` |
| `wand125-rectangles/certificates/rect_n61_L796/certified_candidate.json.gz` | upstream | `a788dcc2e23abb581165a5153cbf8b5f58506816` | `a3a62b3cb129674d6e9db0aa5e89aa18b5fd160c48d2a8c176e917b2a788fef6` |
| `wand125-rectangles/certificates/rect_n66_L8345/certified_candidate.json.gz` | upstream | `18dfe47f2e266d21b99c8adae5561bb63c471a21` | `1b47dd0adb002321fb848dbe0afd8e058afd1b95ba0a7c1386c6cc60fd6aa501` |
| `wand125-rectangles/certificates/rect_n67_L844/certified_candidate.json.gz` | upstream | `25e61ca78c1725f9acc01ba8d6b798a091bbb1cc` | `74d4ac49d8ebf3bc73490f48846b491fdddfe4938a19deaaa48df97994dc6676` |
| `wand125-rectangles/certificates/rect_n68_L846/certified_candidate.json.gz` | upstream | `1b0fd68ff5b30d20b0a7fd4712dd1eb5e5f7fdbc` | `b046ca089ad15309fa7bf299599d765e23659a959e542657238e691ade0963fd` |
| `wand125-rectangles/certificates/rect_n69_L8545/certified_candidate.json.gz` | upstream | `4d2ed1394974bab10993f38938cbd93ff0eec885` | `164a61fa9383905902e9642c3dc43a54c442340f3e0fd72d29226af8e0aff9de` |
| `wand125-rectangles/certificates/rect_n70_L861/certified_candidate.json.gz` | upstream | `5c73fa3e521c4117e9825c836faf7ecb8637ec78` | `3fb1adda0fff3a4e192ccd64050d9f1f322af84f3ecca08d6ab7cbc4f02c5827` |
| `wand125-rectangles/certificates/rect_n71_L8645/certified_candidate.json.gz` | upstream | `7efdca413d09fdac1ba21cf060fbf722effff5a5` | `01a89fe3a027dc8f173b9bf5e645d5e6c459fc54090019dc8f26becbe3e3f0da` |
| `wand125-rectangles/certificates/rect_n72_L8705/certified_candidate.json.gz` | upstream | `6e07cbc79c2656735bb75f7536a6322b19df3faf` | `50cdd4ccef59a76abaaa2141379c9a3ce1a9946f3f844c43cf525676fa6c71f6` |
| `wand125-rectangles/certificates/rect_n73_L874/certified_candidate.json.gz` | upstream | `c3989f9a81dda7e727f94d94ce574ad5203c06f0` | `2dbd17ccdb11e74e60bacb65084f076ff97d4fc4533138593f67b9df0e82d558` |
| `wand125-rectangles/certificates/rect_n74_L8815/certified_candidate.json.gz` | upstream | `366ec04558b136b8c32de86d4faf773cf974e790` | `eeaa6ab20c86b46404b84f0210c67d2a095bc118314af43e28148605bbe81229` |
| `wand125-rectangles/certificates/rect_n75_L889/certified_candidate.json.gz` | upstream | `a5be86938691cde88a161222d1ba4f76d861b215` | `d39394a3c5c3b492d0452600fc7e3133052870690d97542c30d32f6c6691198d` |
| `wand125-rectangles/certificates/rect_n76_L89/certified_candidate.json.gz` | upstream | `11e21df4b4f46ae986ff3fa66250f3efc2cd1d08` | `564c3c12f1d3278a44ff127d9c8693785a58dfaf6f8d38aeca3b6802bbef71de` |
| `wand125-rectangles/certificates/rect_n77_L888/certified_candidate.json.gz` | upstream | `813e23b70acd0ebef928209cb8223b5560c148c8` | `301244a417a81aeb702e77b1fbdc8b182d9b76788ac52e9d9e0b4f43b8fb08e9` |
| `wand125-rectangles/certificates/rect_n78_L8955/certified_candidate.json.gz` | upstream | `d73575fcd4f9e6a2d007532ebb6e074ef46ce925` | `6db7bd7575624b262393dc2775c25b905fc830a4418d8332a54d006d019f8c92` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
