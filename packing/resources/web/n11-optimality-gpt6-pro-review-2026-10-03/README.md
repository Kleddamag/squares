# GPT-6 Pro Evidence Pack for the Eleven-Square Optimality Review

This packet retains the evidence archive that GPT-6 Pro delivered with its
[unified adversarial review](../../../../docs/project/reviews/review-2026-10-03-n11-optimality-adversarial-gpt6-pro.md)
of the tentative proof that Trump’s eleven-square packing is optimal.
The review’s Appendix B.4 and B.5 describe the archive.
It holds the review’s new reconciliation checkers with their pinned source closures,
their exact recorded results, a canonical row dictionary for the local isolation proof,
both input reviews (A and B), and Review B’s earlier supplement preserved byte for byte.

Retention registers the evidence; it discharges no proof obligation by itself.
Neither archived driver replays the global proof, and both say so in their output.
The source proof and this project’s independent checks are in the
[2026-09-29 packet](../n11-optimality-2026-09-29/README.md).

## Provenance

| Field | Value |
| --- | --- |
| Archive | `n11-optimality-unified-review-evidence.zip`, 6,086,828 bytes, SHA-256 `7a2122ffd677f1c0ab1ac8db5ce8c90783d24b19f6b363f90659abc9cc7be589` |
| Members | 202 files, 42,734,989 bytes uncompressed, all under `n11-unified-review-evidence/`; `unzip -t` reports no CRC errors |
| Produced by | GPT-6 Pro, as the evidence pack for the review linked above |
| Supplied by | The repository owner, uploaded to a Claude Code session at 2026-10-03T05:58:40Z |
| Archive manifest | `manifest.json`, schema `n11-unified-review-evidence-v1`, 186 entries, SHA-256 `9d71dd35d3812a1ce781ba3ffc9dbc68816cd34908bb787e90a1a40db9b17720` |
| Source pins | `jlevy/squares@ea0a3b19a70085683c3b65946cded03ffe4e2415` and `Queuingtheorydotcom/11SquaresOptimal@f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c` |
| Prior supplement | `prior-supplement/`: the 144 members of Review B’s `n11-optimality-review-supplement.zip` (SHA-256 `4f9065c61fa188b74d124912f4213677492b21330e3753c89d34214395bb7536`); its source manifest has 118 entries and SHA-256 `be0e69e6b03832be13fa0b03af9b45063e096917e6c1c665cff3447561be4965` |

The archive’s own `README.txt` is retained and is the authority on what its drivers
claim. Its manifest deliberately leaves out 16 members: itself, `manifest.sha256`, and
the 14 files under the top-level `fresh-results/`, which record the producer’s relocated
run. [`provenance.json`](provenance.json) covers all 202 members: size, SHA-256 and Git
blob, whether the archive manifest lists it, and where it is stored here or why it is
not.

## What Was Checked Here

The archive’s SHA-256, byte size, member count and uncompressed size equal the review’s
Appendix B.5. Every one of the 186 manifest entries was recomputed, size and SHA-256,
with no mismatch. `manifest.json` hashes to the value in `manifest.sha256` and in the
review, and the 16 unlisted members are exactly the manifest’s declared exclusions.

| Identity named by the review | Archive path | SHA-256 |
| --- | --- | --- |
| Portable reconciliation checker | `reconciliation_local_checks.py` | `ab5f84a9fa9c8506975e91ad8d7c0aae3ed62867509f2a259846a11b06614123` |
| Exact local result | `recorded-results/reconciliation-local-check-results.json` | `32d58ca2510440f3ce8f82dd775596fa4f9f672e04edb7ee596000c276920430` |
| Canonical row dictionary | `recorded-results/reconciliation-local-canonical-rows.json` | `8f4f426d1746eb0825ee67363506ab864e5b6ca4b6d4b28a0317fcdb2151454c` |
| Weighted packet | `prior-supplement/local-isolation-audit/weighted.json` | `ffe9f89d40a9538ec9a10d8700999f05483d0ccfad17b84d430590da7dd65889` |
| Focused rectangle | `prior-supplement/local-isolation-audit/focused.json` | `9a9cf4e0fdcb1b1d226b9c07ec08d08cbbc572749cec9bc09cf3cd92bd4d88f3` |
| Review A, 36,874 bytes | `source-reviews/report-A.md` | `e911c70cd3e1834661e0d07a0fca358022c797e59487dbaa0ee8bf3635dc7438` |
| Review B, 59,547 bytes | `source-reviews/report-B.md` | `e5333e518b2e872f1786981dbb501da3a261d1072ee4169b26e86f2260db07d1` |
| Reviewed article snapshot, 153,686 bytes | `prior-supplement/reviewed-paper.md` | `428da02fd5b99a6133736113e564097e9281aae213076265f968ceefd4bd3d68` |

All fifteen `jlevy/squares` source copies, under `squares/` and
`prior-supplement/local-isolation-audit/sq/`, are byte-identical to their blobs at
`ea0a3b19`, a commit in this repository’s history. The publisher modules under
`original/` were not compared with the publisher’s tree here; the manifest pins their
hashes.

Each retained file was compared with the extracted archive bytes when `provenance.json`
was written, after decompression for the gzip copies.
[`restore.sh`](restore.sh) then rebuilt all 202 members byte for byte from this packet
and the objects the 2026-09-29 packet retains. The rebuilt tree passed both
`--hashes-only` checks and the full default driver.

## Replays Run Here

uv 0.12.22 created a virtual environment outside the bundle on CPython 3.12.3 (the
producer tested 3.12.14) and installed `requirements.txt`: NumPy 2.3.5, SciPy 1.17.0,
SymPy 1.14.0 and mpmath 1.3.0. Each driver ran with `-B`, invoked by absolute path from
`/tmp`, in this session’s Linux container on 2026-10-03.

| Command | Status | Time here | Producer’s time |
| --- | --- | ---: | ---: |
| `verify_reconciliation.py --hashes-only` | `PASS_HASHES_ONLY`, 186 identities | 0.2 s | |
| `verify_reconciliation.py` | `PASS_NEW_RECONCILIATION_CHECKS`, three stages | 55.6 s | 42.563 s |
| `verify_reconciliation.py` on the tree `restore.sh` rebuilt | `PASS_NEW_RECONCILIATION_CHECKS` | 53.9 s | |
| `verify_review.py --hashes-only` on a copy of `prior-supplement/` | `PASS_HASHES_ONLY`, 118 identities | 0.15 s | |
| `verify_review.py` on that copy, as the archive README prescribes | `PASS_REVIEW_SUPPLEMENT_COMPONENTS`, all eleven stages | 38.5 s | 29.269 s |
| `verify_review.py` on a copy with its `fresh-results/` removed | `PASS_REVIEW_SUPPLEMENT_COMPONENTS` | 38.1 s | |

No driver refused. The local-reconciliation stage takes almost all of the default
driver’s time: 54.3 s here against the producer’s 41.6 s.

The default driver compares its outputs with the recorded results itself.
Beyond that, its two coverage results, their logs and the canonical dictionary came out
byte-identical to the archived `fresh-results/`; the local result differs from the
recorded one only in its `seconds` field.
With `fresh-results/` removed, the prior driver regenerated 23 of its 25 archived
outputs; the other two, the producer’s run transcript and negative-control record, do
not come from the driver.
Sixteen came out byte-identical. The other seven differ only in timing: the `seconds`
fields, the interpreter version in the summary, and timing lines in three logs.

Two refusal controls behaved as documented: `python -O` raised “This mathematical checker
refuses Python -O/-OO.”, and a copy with one byte appended to Review A gave
`REFUSED: Input identity mismatch: source-reviews/report-A.md` with exit status 2.

The transcripts, summaries and controls are in
[`receipts/replay-2026-10-03/`](receipts/replay-2026-10-03/).
Their scope is the archive’s: the summaries record `whole_global_proof_replayed`,
`global_optimality_proved`, `field_geometry_rerun` and `d4_trace_regenerated` as false.
The default driver does not run the prior driver, rerun field certificates, regenerate
the D4 trace, or check Review A’s new dual vectors, which were not supplied.
The prior driver’s field stage checks the 44-certificate selection against the 59
recorded field receipts without rerunning their geometry.

## Where the Cited Numbers Live

Paths are relative to `n11-unified-review-evidence/`. A file the table names without
`.gz` is stored here as `NAME.gz` when it is over 1,000 lines (see
[Compressed Files](#compressed-files)). “Local result” is
`recorded-results/reconciliation-local-check-results.json`; “dictionary” is
`recorded-results/reconciliation-local-canonical-rows.json`.

| Quantity | Value | Where |
| --- | --- | --- |
| Simplified two-radius local maximum | `237880431895517578125000/249999999158632916515561` ≈ 0.9515217307843866, at branch 105, coordinate 31, sign −1 | Local result `$.configurations.simple.unweighted` (`value`, `float`, `at`). The prior supplement’s two implementations give the same value: `prior-supplement/fresh-results/simplified-local-result.json` `$.worst_dual_ratio` and `$.worst_coordinate`, with `$.worst_dual_ratio_less_than` = `20/21`, and `prior-supplement/fresh-results/second-review-simplified-local-result.json` `$.worst_ratio` and `$.worst_at` |
| Direct weighted residual maximum, published radii | 0.6765052045373554, at (12, 6, −1) | Local result `$.configurations.published.weighted.float` and `.at`; exact value in `.value` |
| Direct weighted residual maximum, simplified radii | 0.9515217276118025, at (8, 31, −1) | Local result `$.configurations.simple.weighted.float` and `.at`. This maximum is at branch 8; branch 105 is where the conservative ratio peaks |
| Tightened-curvature control | 0.6764635933318807 (conservative residual) and 0.6764635896668644 (direct weighting) | Local result `$.configurations.tight.unweighted.float` and `$.configurations.tight.weighted.float` |
| Signed residuals checked | 8,448 | Local result `$.fresh_b_signed_residuals_checked` |
| Distinct derivative rows | 56 | Local result `$.distinct_row_keys`; dictionary `$.rows`, 56 entries; second implementation `$.distinct_row_gradients` |
| Branches and rows per branch | 128 branches of 42 rows | Local result `$.branches` and `$.rows_in_every_branch`; dictionary `$.branches` |
| Common rows, rank and nullity | 30 rows, exact rank 25, nullity 8, free columns 20, 21, 23, 26, 28, 29, 31, 32 | Local result `$.common_rows`, `$.common_exact_rank`, `$.common_nullity`, `$.common_free_coordinates`; dictionary `$.common_row_ids`, `$.common_pivot_columns`, `$.common_free_columns` |
| $e_{21}$ in the null space | The basis vector with a single entry 1 at column 21 | Dictionary `$.common_nullspace_basis[1]`. Checked here: only rows 18–25 have a column-21 coefficient, and none of them is common |
| Smallest unavailable-feature margin | 0.005897503722317347, above 1/200 | `prior-supplement/fresh-results/simplified-local-result.json` `$.minimum_feature_margin_float` |
| D4 incidence counts | 999: 168 immediate, 47 propagated, 1 survivor; 1462: 198, 17, 1; 1659: 196, 20, 0; maximum operations 19, 15, 7; 648 records | `prior-supplement/fresh-results/d4-incidence-consumer.json` `$.summary.<case>` (`initial_contradictions`, `propagated_contradictions`, `survivors`, `maximum_operations`) and `$.records_checked`; same counts in `prior-supplement/recorded-results/d4-propagation-summary.json`. The two survivors are the `$.cases` entries of `prior-supplement/d4-propagation-traces.json` whose `terminal.type` is `survives`: source 999 with target indices [1, 1, 0], and 1462 with [0, 2, 4] |
| Forced D4 regions | $R(1,1,11,4)\subseteq[23/50,27/50]\times[0,11/100]$ and $R(2,5,6,9)\subseteq[11/25,14/25]\times[23/100,7/25]$; distance bound 1989/2500 | `prior-supplement/fresh-results/d4-independent-geometry.json` `$.region13_box`, `$.region26_and57_box` and `$.simple_distance_bound_using_U_lt_4`. Overlay regions 13, 26 and 57 carry labels [1, 1, 11, 4], [2, 5, 6, 9] and [5, 2, 6, 9] in the overlay object `845b5f74…` (`$.regions[i].labels`), which this packet omits as already retained |
| Minimum field selection | 43 mandatory certificates covering 1,903 cases; residual case 1456; 44 certificates cover all 1,904; angle rows 24,373 to 17,963; ownership checks 5,877 to 4,233; 71 top-level baseline certificates | `prior-supplement/fresh-results/field-subset-verification.json` `$.mandatory_certificates`, `$.mandatory_union`, `$.residual_case`, `$.minimum_sufficient_field_certificates`, `$.recorded_field_case_union`, `$.original_angle_rows`, `$.selected_angle_rows`, `$.original_ownership_points`, `$.selected_ownership_points`, `$.sufficient_top_level_baseline_certificates`. `prior-supplement/fields/minimal-44-field-manifest.json` repeats them at top level |
| The certificate for case 1456 | `59db0f81…` (167 angle rows) chosen over `7722afef…` (389) | `prior-supplement/fields/minimal-44-field-manifest.json` `$.certificates[26]` and `$.certificates[49]` (`source_sha256`, `selected`, `angle_rows`); these are the only two certificates whose `case_ids` contain 1456 |
| Omittable retained field sources | `68426a0d…` (mask 1925), `72e06f08…` (mask 246), `a323908f…` (mask 1802) | `prior-supplement/fields/minimal-44-field-manifest.json` `$.certificates[13]`, `[17]` and `[30]`, each `selected: false`; stated in `source-reviews/report-B.md` line 305. Checked here: the 44 selected certificates are among the 47 field sources whose receipts the 2026-09-29 packet retains, and these three are exactly the remainder |
| Interval-predicate enumeration | 12,180 cases; 616 historical false accepts, all singleton targets; no other historical error; no corrected-predicate error | `recorded-results/reconciliation-coverage-check.json` `$.enumeration` (`cases`, `old_false_accept_singleton`, `old_false_accept_nondegenerate`, `old_false_reject`, `corrected_errors`), grid in `$.finite_test_grid`. The archived and the regenerated `fresh-results/reconciliation-coverage-check.json` are byte-identical to it |

## Retained and Omitted Files

The packet keeps 196 of the 202 members at their archive paths under
[`n11-unified-review-evidence/`](n11-unified-review-evidence/), unedited: 126 as plain
files and 70 as deterministic gzip, following the
[resources convention](../../README.md) for data files over 1,000 lines.
The gzip copies are the 59 field receipts, the three manifests, both copies of the
canonical dictionary and six prior-supplement results. Source code and Markdown stay
plain.

The retained Python stays as `.py`. `packing/pyproject.toml` names `resources` in Ruff’s
`extend-exclude` and in BasedPyright’s `exclude`, so nothing under `packing/resources/`
is linted or type-checked; the 2026-09-29 packet keeps `source/VERIFY.py` the same way.
No `.py.txt` renaming or new exclusion was needed. `.flowmarkignore` excludes
`packing/resources/web/`, and the document map excludes its Markdown, so the retained
reviews and the article snapshot keep their bytes.

Six members are omitted. Each is byte-identical, after decompression, to an object this
repository already retains, and `restore.sh` rebuilds each from that object.

| Omitted member | Bytes | SHA-256 | Retained copy |
| --- | ---: | --- | --- |
| `prior-supplement/local-isolation-audit/weighted.json` | 11,017,145 | `ffe9f89d40a9538ec9a10d8700999f05483d0ccfad17b84d430590da7dd65889` | `n11-optimality-2026-09-29/receipts/local-dual-residual/objects/ffe9f89d….gz` |
| `prior-supplement/local-isolation-audit/focused.json` | 103,426 | `9a9cf4e0fdcb1b1d226b9c07ec08d08cbbc572749cec9bc09cf3cd92bd4d88f3` | `n11-optimality-2026-09-29/receipts/local-dual-residual/objects/9a9cf4e0….gz` |
| `geometry-audit/df7938d9….json` | 773,471 | `df7938d9ba27095a38fabe45f8b26b259a2cc896c2ae4aac6bae874f417adc4e` | `n11-optimality-2026-09-29/receipts/d4-independent/objects/df7938d9….gz` |
| `prior-supplement/squares/packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/objects/df7938d9….json` | 773,471 | `df7938d9ba27095a38fabe45f8b26b259a2cc896c2ae4aac6bae874f417adc4e` | the same object |
| `prior-supplement/squares/packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/objects/845b5f74….json` | 132,395 | `845b5f748843dd60fa7e290a5ea1a304da4e439ae229bd73a841aec816f4e700` | `n11-optimality-2026-09-29/receipts/d4-independent/objects/845b5f74….gz` |
| `prior-supplement/fields/A1-baseline.json` | 122,029 | `04fa1ebb37f5dace29946224fe8c7c5d8a1bedb4fa860c65b359f4200415de57` | `n11-optimality-2026-09-29/receipts/case-census/objects/04fa1ebb….gz` |

Only the weighted packet exceeds 2 MB. The omitted members total 12,921,937 bytes.
The retained members occupy 5,202,526 stored bytes, and the packet as a whole, with this
README, `provenance.json`, `restore.sh` and the replay receipts, occupies
5,370,723 bytes.

## Restoring the Archive Tree

`restore.sh` copies the retained tree to a new directory, decompresses the gzip copies,
rebuilds the six omitted members, and checks every member’s size and SHA-256 against
`provenance.json`. Run it from the repository root, then follow the archive’s own
`README.txt` in the restored tree:

```bash
out="$TMPDIR/n11-evidence"
mkdir "$out"
bash packing/resources/web/n11-optimality-gpt6-pro-review-2026-10-03/restore.sh \
    "$out/n11-unified-review-evidence"
uv venv "$out/env" --python 3.12
uv pip install --python "$out/env/bin/python" -r "$out/n11-unified-review-evidence/requirements.txt"
"$out/env/bin/python" -B "$out/n11-unified-review-evidence/verify_reconciliation.py"
cp -a "$out/n11-unified-review-evidence/prior-supplement" "$out/prior-supplement-replay"
"$out/env/bin/python" -B "$out/prior-supplement-replay/verify_review.py"
```

Keep the environment and any replay copy outside the restored bundle: the default
driver refuses an inventory with extra files in it. Its new outputs go to the bundle’s
top-level `fresh-results/`, which its inventory check excludes.

## Compressed Files

Seventy retained members of more than 1,000 lines are stored as deterministic gzip made
by `gzip -9n`, with no file name or timestamp in the header. The table gives the Git blob
and SHA-256 of each decompressed file, which are the archive member’s bytes; the SHA-256
also matches `provenance.json` and, for members the archive manifest lists, that
manifest. `devtools.retained_data check` re-derives every row.

| Stored file | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `n11-unified-review-evidence/fresh-results/local/reconciliation-local-canonical-rows.json.gz` | upstream | `0c56faa3177629d58edb5cf4ca56d7dd7e3f2054` | `8f4f426d1746eb0825ee67363506ab864e5b6ca4b6d4b28a0317fcdb2151454c` |
| `n11-unified-review-evidence/manifest.json.gz` | upstream | `ba6f7a1e3b506fdb00367416ca07e39026818a5f` | `9d71dd35d3812a1ce781ba3ffc9dbc68816cd34908bb787e90a1a40db9b17720` |
| `n11-unified-review-evidence/prior-supplement/fields/minimal-44-field-manifest.json.gz` | upstream | `b9ad056e36a2bc4391d87e3e9e489cbdd66ec939` | `5d8a75cecd374177dfa8004c6e5783a222a458dc993f810e82999c009672d226` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/0400213ea154cc697817f43332a4f247032130b704124df860dc91d2d5c135a6.json.gz` | upstream | `14c706ef651b0de5fd663e309e6610fd1e009352` | `7b0e1a7ada98cd3f779b9362b84a86025ce7e46491ac25bbd66a954dc7a51b65` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/0528d7f823c62ecbe034f2e212ebf2c2cd630a7f55cf9fe8721c6c066446bb25.json.gz` | upstream | `5e875d0337475264e8f7237cb11c71e5a1a3986e` | `06723ee5f5a45cb5a4e047ce541855c79ba8176bcdb8b48313c97619cd27f408` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/068d10ddb9fa6b699090541a407169092180289fd1f34457d9bc4f16885d1ba1.json.gz` | upstream | `0a209e003df76d9480ea1574c9996aa1bf9b5a0d` | `423674dd8eb430009375e4000171d3acfdc4a36055ceefba49359c5cc0bc181c` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/0af81517e9a1421f7ee445f8f6542f8491e1a921dde472b908d6786ce8d6619d.json.gz` | upstream | `9b61f17fcaec5c9da6cb1d6fc12ca30319e1c46c` | `a3de13b9c9b62d0f35bab1db8b5ba3fc4b43abb806cc728a7ee1737b435cd4eb` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/0c6bb3cd6cadd805d3a7a9360585cfe91d097891dbf767dbea9ad9975d9386cf.json.gz` | upstream | `e3832ab83c11a5ac8831434a30f383735db534a1` | `982d677e7d00155b106f2f6c1b06cddef1a71f8a0097d1c01f0ef2465f6aa21e` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/0d8969a1574ef04dd823c6bf7f518fface05b7ac4db621fe5ee222ad7c1ced5d.json.gz` | upstream | `75e8705bab0f26e0b0824c80fe7717be41ea214e` | `3c9d130a6bc943c8397fe1a53895e80878ff1f28abb9cff907434e7598b03803` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/0f0d0bcc7b997f2ee77719ae7e19106d024f4df43c3fb6cda47d6d0f21060f3b.json.gz` | upstream | `e8e1c4b07a9b8a766b794a650cab8b8a0a347503` | `5f84998531b6a59e73500ac8f60c4a57699f26b373f94b7a75aba407692fc8ff` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/14164a3d91117055000ae78cd15a4e8ad5d6bb2c27ce24ff080605b873a93340.json.gz` | upstream | `939227db651f28b455ba1a1126b0cddcc1f8e0d7` | `aaa5ae1f13f27d4f90aac6e244a9ad2342038fd81b4d6d989d4bd65b57d88cef` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/180ffde477b16dc7bc0df47612f5232b42a0a138870e67c197dc0b3976381ca7.json.gz` | upstream | `0c93750ba6bf35476f65c4076d976aef26d49f44` | `f24a59a9547b7d4395ed283930a56d8d120ff314999002861394c9596d5ac2e4` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/1d5a197212d1a89530aadb9859645066b3fbc50beb48132833042a15e9b4ffac.json.gz` | upstream | `d48dd1509e2ca44582b299fe07901d586cf4aad4` | `009c0f0670e55e1878bc64f1663a6339e3905e30aef08495a0713115110dff6d` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/1ea6e9f0d84b117f1fb202df4ab265fd2c9b185892181f976fdf3bdeeb4cc4ca.json.gz` | upstream | `a49035d5d243bfce022cd278e1b80bfa3c8a0b3e` | `a58a3092f463b2a8cc84b350ee4857d0ccc7492b87f2e131423de0419ba0c313` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/2d1019d65eb4b4a6ba1ca776b00388f905a3f7dd4432ad9d02525f0a0f65a591.json.gz` | upstream | `be97df8af5c011d4f58155f8265805d9b3e7d827` | `9cea0c51bb4a6d928e6fc81a5cf73cab7ba427cdf356faeb9cb0f9f19ac00a55` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/2dfb2c28000d876b8727f7586f3dc6129235d8dab96e8927a33f6799c6eae4cf.json.gz` | upstream | `59ca0d8382586056e2bfbd98fc0e8d54e011ba8d` | `77c5623de13b1da701f4017e085fa2c85a8fa58169d40433ba360831c978c4d0` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/2ee184f832a24833c348d322c4ee8741f361f3f97d4b8b0faf54974d93e981b9.json.gz` | upstream | `0e72279c909c3fc07ba51a69e3ac2653be86f693` | `214f92b090c7fb468b012ed34bc64534498f0a9f340e671f163967862d0b008f` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/3492cd05d8c2fd1a2aadd84c93a09c4a509171e830b7b42c5a2f049f4f11e0d3.json.gz` | upstream | `a9fa54ea79d40cae9c9a9a306a0d8c891b644625` | `ffa316a41bbcf3ff8173ea0c54f1ed907603dbbcfba0759a9f417275e9bc4b0d` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/3777fe136bcf07e09369f81d06572777e42bc805878d5d8b204463b9363d061b.json.gz` | upstream | `2ff9685b1eaa794b121cac10c38f64ed62984a91` | `5ed342bddc729829ef122a337f45403bc666a3b5a4aedb98a47664e77b6ad0b0` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/3a8330d505e6c087a4d333343977a57677f1ac449d44f8c9194a0870404e739d.json.gz` | upstream | `8111a873d9c7345b06a107f92c123f7713566652` | `85da6787d64f706da9906cdc1e27d45383ed68b0c724e12ab520aa8d814f5cd9` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/3c8f34fdd79a173d26688d932db6a6da12095da17ff7fd6210960df3efaa6bef.json.gz` | upstream | `da76c1a4ac47b097442987285a75f6eddcf464f5` | `05a0b0b2d3884debd7f813b2b584f3b207d2470c8c25a84a8cfb7ef4f17e0795` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/3f5244e99383236309fc46104e65493e86695f671d087e0fd898b617a711a6a3.json.gz` | upstream | `31fab7e07a942fd4742cb84015370778953c4b8e` | `c1aeba791e98abe8c5ead8defb6dd82184fb745b2f5fa17093314eead5d08d87` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/420fa162bb3e54fd11fab58c14606a8e38312bca9dd198ee7fb7eeddd2b715db.json.gz` | upstream | `6b58186f88d82be0d8e75ad8f5b8502d6b0cc7c0` | `9438ad3bea584dbb2631fd73b4b03fd5e7fa84d78d729f7d0d92c475c2b802b9` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/435016c091de76ee0ce06ce531442231744c6b4bb66b00e99d55e3ea4d700172.json.gz` | upstream | `ed7fb62466667977a76b239126d1e40ae8c07feb` | `186bc6f6bf7d836891b651426ea7ba975f71115948149c1bbdaaa9c3fbbc507d` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/4aca103f9d71dad6792f19c0cdd13c84f96bb1e4d7154bf843d7ea62ae009d17.json.gz` | upstream | `6a5a241c9609209efd17e1276c3e3088e62befe9` | `e182dff986e1c47a963105137ec522c5dcc36366c5fafe942c25bc5d808fc2a3` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/5263924bc441ffb869b6d6d4f68e17acd1b0282468868c367e59238231931751.json.gz` | upstream | `025efa9e37ccaa0d4f3c97a6baa07e5758ea2912` | `3e05908f817c969df35e0e7554c9ec9d1e201a89dbfc94554d99bb887771b7b4` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/53f4bdc08254539a17fb0e3245f9d2b6954bacb7a7d1032c66b06a79e2e4ed22.json.gz` | upstream | `6447f466963ecda02c06bdb776d51247015a98fc` | `6da785df7725817b7297d89c2b0e13dfeeb4de0dff6a83786ce30522670463ee` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/59088bfcda01e7942b8299f3f3847313cba5d7e66a0d39e1c6c3d715c3e8b23e.json.gz` | upstream | `fab24bf76ac35344d47e4d69b0c48b7a2ac4c18c` | `73a1b7301e73ad7a8e2683b76b6ae599071036cda331553b89c4bd526bfcdb34` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/59db0f81f262d5cbe27607cd6a45d464caeb8981645bed45d03b81b30d82dc65.json.gz` | upstream | `b901ae4591dfa51d01f182ee0d692ff658d73825` | `297a4b34b17cbbc1f87997c67da04620d20278f676ae9de10125969b7dfe28e2` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/5ba7c24f6a6680d1ea319c2be9e2c8349b93a6ee73d78b951c70620d8379a54c.json.gz` | upstream | `53c6a6d77ac588a7d8c196c946582ac93901c2ba` | `c00064448e107247a0e763ac5e72d9a4a99820d90c6c85f24f2179cbd13e8d7b` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/5ea191acf7c9d8c7010695cf52cc73935f028f2379eab0e52dfbea2a268712b0.json.gz` | upstream | `b2249c8651907f52a3276902dd477fce9a4a7851` | `0a450476e094cbfc148265d294b7954deaec2758f434103c9764fe3870660e37` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/60c4f297c6b5ba092237b1de5a514b8e9ab22d002bfa51cea28b35c6a7d25a07.json.gz` | upstream | `edcfc5208cccd0878832289d80217c60fe2457ca` | `f67d2a81732f6e1f0ac61d98ef9c4e183e58be1c518bb6af2af06bbbe72b9517` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/68426a0d6d8cb642e9a895c7e3e4e354cb854c5af0e401ac4bf8cb8baef8b455.json.gz` | upstream | `c3d518bfb07c739a42c2a3f46600c4879cab5225` | `3d12a749f80be6406ef78d56eb83aab2ba201968d99588b6a0b505f0165c4820` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/6d0f397ca92f7ab7e7a20a0e6aadc2a704367a1cfd3e267f323615bf14042a83.json.gz` | upstream | `3169489cd09a87655668b2dbd8786e0a262315f7` | `2e6eae7ebb872633b3cd0542967b932747f47a74e748d566444d2e9604ee5cd9` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/6dbff97401d93002720395f4e290c02011875f6db4cef1de5996d7d00ff96461.json.gz` | upstream | `8e5eb6773f2f6e0d4a078ce6239dc4521369d6db` | `858175fcba6cc298f86eedc8088fb1d63d21287c2d4580e816d8b8032d0ab15a` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/6fbef8702e626172653ac8117f74551ac6fa05947fd05b668b6d3e7c712a1d47.json.gz` | upstream | `fed28ba2a8f8600d6d7b04a94278a1ab3a47290f` | `3e8118f7d2befdd73e2ac817769efb24c494f6e6c080ac0522691720c9c81c59` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/72e06f08ab0775ec073aa444ac9b698b1ef6746351b5d40435d4a03db231db6b.json.gz` | upstream | `6d20e83b62b05548a2d64a19a05edfa8db1f4353` | `20e0d0fc825f2817201deccb01ea4559f9f8c7947fae49bb5a682b00602d7d45` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/7722afef52e705f7fa74bfa350f132cb9405737677bffac02e476256c87eefd8.json.gz` | upstream | `c47341ab928bd28db2f46f95bd986d474b8262ef` | `dabc80d9de41f6aa973ecfe8d2d88d156fb9420d15e3e67b8b0873444f8bc441` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/7a3ca229b12679663c555df872f1684beb1aeabeaf7907195c310e1dc50f79d3.json.gz` | upstream | `ca786e39062696d01b0d4e696a8876e3fc22d6fb` | `0ff11636c56f26f2b003d20bdc22842f889fb5c7c750837c654d982d607ac256` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/7c943483704ba054294a5d866ec4815f1df9ba4d23a505503a2a88b198e98878.json.gz` | upstream | `e3e55e223a8a8095f701792694c9cf3227f2518a` | `2d3fbaf8e8397636610a5764845b5d359f8dcac1e4542f1823400d3bc5806cfc` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/7fc70fa2373eb159f5739749da59a98ab5e29c2dfadcb5accc5c113e329a5f4c.json.gz` | upstream | `7ff33dbf0ce1f489a0eedfe48d9c09a702fc8e99` | `5cf5a0ccc4d8863f60da8a80378401ce78acc0c717d9d7433903a3cf96b326cc` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/875599dc2563dc877ebc6f1ffcb1afc519659644d0c1707d55046ae897c2f19e.json.gz` | upstream | `8efdc6f5b5c4f4318a04b2245c4ef29204aefa4c` | `fa13a079510a37a6c3bbe1e54c61749c860ee34c60bbcc06e0dd75afd41f9b4c` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/8ac3b7c4093a06354850e4d804f250196ff0505bfc411ac05f4f78cbacec5734.json.gz` | upstream | `dda5277848d72986d3d5dc308e210d0e52d92557` | `1f232d9d6af6891e990bed91c31abbcea2fdb15644dcd1c4bfc14429536b76b3` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/8f5f52a74e3827eef7df30fe4c38eec13e650d380623d5e183a82770b9482fca.json.gz` | upstream | `434a6dc475e90af9abbcc2e6de692732c448b446` | `ef727dd65ea9469571c5d9d403fcfcab55089a25ce73c46ac2d6c7db2adbe352` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/9289222e000a515d80fff8d43e86779b57908e1912900127f4f5de82cae4c385.json.gz` | upstream | `d33471c582a6151adc1b8e19692675beb943b6b2` | `e1a90669e5757bf87377a761aa8b2730ffca2055bdcb91004751b3b70916fbfb` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/958e9c2fcec10e781ca6ba779221d99a27d99f2a4709b03c085349b4b1f96e46.json.gz` | upstream | `27cb30f39c87f59ebd7a82a27c9365922070b9fd` | `346e0624174d6c7aab75cb161954c3b058293a7f0cca49c6088ba3e929660a17` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/9a777a1701cb23e63b5aec586f0650057888e18038bc037ba15f2747d9ea2f8d.json.gz` | upstream | `d49a19eacb56fbfa50f608ab14b61f291f762cc6` | `38669b181a3342e755b673a482e3ffecc325df64c20dd900e2156e8f7af9802d` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/9bd8a1dd184fad2d05b7da7d6b2f63e65c5cde34676f772d77120b895478203e.json.gz` | upstream | `a49953ec0ab1985a421ed5bb075e592e1bc7f34a` | `8cc6483824a7b0be79489ca85a7a8107532a53aa33aafad93a3892d9e023fbcd` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/a323908f1c75407dd57042df054434401df05fdf9332bc5c71271cd54869890d.json.gz` | upstream | `bc0b2d908c7b25a0887e47e73ff9297be0a44757` | `62ea28581c98707e19176a0e1b7767433ba375c39b81a88badc378a30bab1783` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/a3db9c32afc077c15daf11e8c9e2e7f632d452f982398fa86a766f9d1dea4043.json.gz` | upstream | `9f34d8a2d179aebef36d57af02178ff0f47c6627` | `8f042c36fe5de1995f6c0e982f08e201cfd7cf11fd9a19c7f96057f28e4fdca4` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/a53b4fa93314099f56e992ebcc087124e2152dcb05bbda8cb01eb7561212b5ff.json.gz` | upstream | `3c338c818213c26eadd21f8ed6d1ec48d696617d` | `91150cd98b4fd84701b5396409d33abe67074ac878216a8c070a449796bdfb73` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/abb9e2630154ac98f3fffd3df3bbe528b2d33fc4988728c388fbbd621b2aaab9.json.gz` | upstream | `bd751c26ea3ea864500067f9af51734a278cbca1` | `da08ad525e3adc1ff0ad52f7c330f056e93562ebde0a42a3124190eb73940bed` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/b5aa82fdfe5f20b227ad319ef2fd2f53aeff61f25a06b326ddc47c6115506c2b.json.gz` | upstream | `c93b0aeb18e6e5e2481df29bf8860547399ac350` | `feecf6965b57095af931dec9ace3d57ea6901974d04f097c41a9cd9fa39c994c` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/b7522bbd6b128f227c7bafafe29c6f4abf0a33eca5cedd122d7fe7a0df93e754.json.gz` | upstream | `adaabbe02fd470041ab8ebc7f290c27382e56761` | `0eda76646e31afa5524e8d82ae8319db96111e74e87c7d8c25b4d13d47593f06` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/bc698e18151bfc83c244c4a2559772c5e28e03ace331d6dea5fbb6ac1d82e78e.json.gz` | upstream | `402e0acdf6ef5179c3541a563f7e0eceedb94f5f` | `9912a24009b522ef2019b986386d7eb63a58ec97ec92903a1ed8ad41840902e8` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/bf57de8cf853d8d46313fb2eea4372269cbd329946a9ee9e21da31f6e458db00.json.gz` | upstream | `69a1f0539114859a9101f51ec142e9efee49f756` | `35180b18bac028d35d8b91da370ac7ac754e751190fa2ec46eeead4965dd9130` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/c284ab20f0db93dde0b020d14ceac838f1fb140b7d002ee22b7402488a0cf16b.json.gz` | upstream | `fc3c6e74ea4f56d7360a58467ba471474b2b5708` | `7a4d12338ef14dd74edc13c129f0c54fe924d4b94e355d7ae7482ac6b7bb7d48` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/d2526dbf35f225ec92c36f5a78551b2ef4bbfdf8840c9097c10fbc6a248d6dc3.json.gz` | upstream | `a115b96b7f4a10fe6654cbee5d78f3c34c0df985` | `f0fadcd2e47812f89cdd5074d66222fd1baa075f99f7fa7127753239b89db8e7` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/e9d0c40c2a37fee0df7a212313c1f1d43d57653da92fa86940ff00d15ebb943b.json.gz` | upstream | `839191ad3e0af84ddb89398a69d43a35a3a44da0` | `b318d730a6e1a3a2f6bb9e4ad4aacc9b485d4e4ccaacff12bce565af658fc9a8` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/eed2e83e499e986530c2ea8ed6f916a93a6323239650b4eeb5b0a2199e78f6d1.json.gz` | upstream | `cbcce9551e62aac556ff61bd054d7e42003d483f` | `10c73695b9b297b56f005406e5c608b22e795656547bf4119f5a62130af908cb` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/ef0003f22625807b08c17065b7374d92782c07dc39cb0bfc13fe0e1487978015.json.gz` | upstream | `001eccede5e79532177cb9a6f8f58a841e8324b9` | `01eecb4c8608c41af0b2ae96ceec577364cbfa5bed8228177c158fb40447bf0a` |
| `n11-unified-review-evidence/prior-supplement/fields/receipts/f57335c9dc626bd124ee5b0b9903ba7575123f5162aa8ba633f55bfe24fec7d8.json.gz` | upstream | `22cf65eab25d70d22b3002b9ab92e4c5864e134c` | `2adfe050dea9565fd5d232550f937dd6b5aebac122a836ab877cd72e901b5802` |
| `n11-unified-review-evidence/prior-supplement/fresh-results/independent-exact-witness-result.json.gz` | upstream | `6fb8a535f0c9f75bf744857bd7be33ee1740ca9f` | `aa428ecaf637304e8817939d4db586660eea65fc4466e479ebda3ef3ea06cbdf` |
| `n11-unified-review-evidence/prior-supplement/recorded-results/all-59-field-replay-summary.json.gz` | upstream | `91a6a49e63447eb31ddd9501268a7d55573e62ee` | `fa58c01435a9d4e6d0648b925d37c1545d86b8b5b939738164571240b9269d39` |
| `n11-unified-review-evidence/prior-supplement/recorded-results/case-census-fresh.json.gz` | upstream | `df57dfdd36197afb82cea6d5b5945051be0a9004` | `ec33ed3bd967b3aafeaf67729bbbdd7a76d4c467647fb0e214ce77b71a2e78a6` |
| `n11-unified-review-evidence/prior-supplement/recorded-results/independent-exact-witness-result.json.gz` | upstream | `6fb8a535f0c9f75bf744857bd7be33ee1740ca9f` | `aa428ecaf637304e8817939d4db586660eea65fc4466e479ebda3ef3ea06cbdf` |
| `n11-unified-review-evidence/prior-supplement/recorded-results/published-local-replay-result.json.gz` | upstream | `2841e5f22cc7f994b279d21520d768fdaeeb4882` | `b6f045903b070f8deb1a85aae18b1e87f5e4b919c3157ba8eb3acf167c470b23` |
| `n11-unified-review-evidence/prior-supplement/recorded-results/root-generic2095-replay.json.gz` | upstream | `b2a1e3cda449f836a5b459da43aeafacfeb2de11` | `89b07e072ce08bb21d39c96f53bf866008eceaaa0fdc8b725c707d9944db576b` |
| `n11-unified-review-evidence/prior-supplement/source-manifest.json.gz` | upstream | `e22918d1b3f03c0f53442ef7aa8bfb24f055c1d6` | `be0e69e6b03832be13fa0b03af9b45063e096917e6c1c665cff3447561be4965` |
| `n11-unified-review-evidence/recorded-results/reconciliation-local-canonical-rows.json.gz` | upstream | `0c56faa3177629d58edb5cf4ca56d7dd7e3f2054` | `8f4f426d1746eb0825ee67363506ab864e5b6ca4b6d4b28a0317fcdb2151454c` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
