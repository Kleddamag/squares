# Joost de Winter’s `square-packing-211`, Retrieved 2026-09-29

This packet records
[JoostdeWinter/square-packing-211](https://github.com/JoostdeWinter/square-packing-211),
which reports 211 unit squares packed in a square of side `14.99796070496771500150`.
That is the first packing of 211 squares below the `15 × 15` grid on record: the Kingbird
catalogue, retained here and live on 29 September 2026, pictures no packing for
`n = 211`. Its Frontier key is **[de Winter n211 2026-09-16]**, and the result is
registered as T-057.

It is a different source from the same author’s ResearchGate report of August 2026,
**[De Winter 2026]**, whose coordinates could not be retrieved and which is recorded in
[`../de-winter-improved-packings-2026/`](../de-winter-improved-packings-2026/README.md).

## Source and Pin

| Field | Value |
| --- | --- |
| Revision | `702df9bb3b1e7fe13279a61a1fa89722aa2d496a`, tree `7216964baa956748913ce20f5f2790a803354921`, the second of two commits |
| Committed | 2026-09-16T10:00:56+02:00, which is 2026-09-16T08:00:56Z; author and committer clocks agree. The first commit, `7d000e1a`, three minutes earlier, holds only the README |
| Author | Joost de Winter, read from the commit metadata: the repository has no LICENSE and its 84-byte README names no author |
| Credit | The source names no prior work and says nothing about AI assistance |
| Licence | None published |
| Retrieved | 2026-09-29, a full clone |
| Retained here | Derived facts and metadata only: [`facts/n-211.yaml`](facts/n-211.yaml), the 211 centres and angles carried verbatim as a Witness/v2 witness, and [`acquisition/sources.json`](acquisition/sources.json), which pins the three upstream files by SHA-256 |
| Not retained | `n211__record.json`, `n211__record.svg` and `README.md`, the upstream bytes, under the [known-best retention policy](../known-best-packings/README.md): with no licence, no raw asset is kept (`raw_asset_retained: false`) |

## The Claim

`n211__record.json` gives the side, and for each square its centre and angle in radians
as 21-significant-digit decimals, with the origin at the lower-left corner.
It also records:

- a verification summary: every unit square inside, every pair of interiors disjoint,
  checked in outward interval arithmetic at 80 decimal digits over 22,155 pairs and 844
  wall inequalities, with least wall clearance `1.000005e-14` and least separating-axis
  gap `2.10001e-14`;
- a previous side for this count, `14.99879247655475100150`, under the key
  `previous_verified_s`, which the record does not attribute to anyone; and
- the method, in the author’s words: “Full-packing adaptive search followed by
  grouped-angle local refinement and interval-verified decimal export.”

No interval boxes or checker are published, so the author’s interval claim cannot be
replayed as such.

## Certified Here

`python -m devtools.upper_bound_packets certify --source de-winter-square-packing-211`
promotes the retained facts to an exact rational packing
(`packing-witness promote --strategy robust-rational --max-side-increase 1e-9`, in
process) and decides every pair and wall over `ℚ` twice: once in the promotion’s exact
separating-axis test, and once in `devtools.check_rational_witness_independent`, which
shares no code with it.
The source’s clearances survive rounding its poses to rationals at centre dilation 1:
the certificate’s side is `74989803524838470007/5000000000000000000`, `2.1e-14` below the
printed side, so the verified upper bound is the printed side itself.
The certificate is committed as deterministic gzip at
[`packing/witnesses/de-winter-2026/n-211-rational.yaml.gz`](../../../witnesses/de-winter-2026/n-211-rational.yaml.gz);
`gunzip -k` restores the YAML that `packing-witness verify` reads.
[`receipts/certification.json`](receipts/certification.json) records its digests, side
and both verdicts, and the negative controls that both checkers refuse are recorded in
the [Couzo packet](../franciscouzo-square-packing-2026-09-27/receipts/negative-controls.json).

Replay, from `packing/`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_packets \
  check --replay --source de-winter-square-packing-211
```

which regenerates the certificate from the facts, requires its bytes to equal the
committed one, and decides it again with the independent checker.
It took under ten seconds here.

## What It Shows

With the catalogue’s packings at `n = 241, 273` and `307`, found by M.Z. Arslanov, S.A.
Mustafin and Z.K. Shangitbayev in March 2019 and marked there as showing
`s(n² − n + 1) < n` for `n = 16, 17, 18`, this packing shows the same for `n = 15`.
For `k = 6…14`, at `n = 31, 43, 57, 73, 91, 111, 133, 157` and `183`, the best known
packing on record is still the grid, and for `k = 2…5` the grid is optimal:
`s(3) = 2`, `s(7) = 3`, `s(13) = 4` and `s(21) = 5`.
Nothing here bears on optimality: the verified lower bound at `n = 211` is untouched.

[`receipts/live-catalogue-2026-09-29.json`](receipts/live-catalogue-2026-09-29.json)
records that the live catalogue fetched on 29 September 2026 still lists no packing for
`n = 211`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
