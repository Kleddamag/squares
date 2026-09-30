# Mathematics Review: Couzo’s 49 Packings and de Winter’s `s(211) < 15` (T-056, T-057)

Reviewed 2026-09-29 by a Fable max sub-agent acting as the mathematical reviewer for the
intake of [jlevy/squares#227](https://github.com/jlevy/squares/issues/227), after the
intake had registered Francisco Couzo’s 49 packings as T-056 and Joost de Winter’s
packing of 211 squares as T-057, both at `V4`/`C3`. This record was written from the
review’s verifier and logs and from the tools, receipts and certificates they checked.
It is an adversarial correctness review of 50 upper bounds on `s(n)`, the least side of
a square containing `n` unit squares with pairwise disjoint interiors, each freely
rotated. It moves no rung.
Priority between Couzo and Griffin Casson, and what each source says about AI
assistance, are recorded in the packets and case records and are outside it.

**In one line:** each of the 50 exact rational certificates is a packing of unit squares
in a square of its own side, decided over `ℚ` by two checkers that share no geometry
code and again by the review’s own verifier, which passes all 50. The certificates are
the sources’ own poses at centre dilation 1, so each proves `s(n)` at most its side with
no scaling argument.
At `n = 206, 259` and `305` the printed side is not certified, and the record says so.
The mathematics is sound as stated.

## 1. What Was Reviewed

| Field | T-056 | T-057 |
| --- | --- | --- |
| Source | [`franciscouzo/square-packing`](https://github.com/franciscouzo/square-packing) | [`JoostdeWinter/square-packing-211`](https://github.com/JoostdeWinter/square-packing-211) |
| Revision | `f3c5a529`, committed 2026-09-27T21:46:41Z | `702df9bb`, committed 2026-09-16T08:00:56Z |
| Counts | 49, from `n = 68` to `307` | `n = 211` |
| Printed sides | 15 decimals, from `binary64` values printed as `%.17e` | 20 decimals, poses at 21 significant digits |
| Retained facts | [`facts/`](../../../packing/resources/web/franciscouzo-square-packing-2026-09-27/facts/), one Witness/v2 file per count | [`facts/n-211.yaml`](../../../packing/resources/web/de-winter-square-packing-211-2026-09-16/facts/n-211.yaml) |
| Certificates | [`packing/witnesses/franciscouzo-2026/`](../../../packing/witnesses/franciscouzo-2026/), 49 files | [`packing/witnesses/de-winter-2026/n-211-rational.yaml.gz`](../../../packing/witnesses/de-winter-2026/n-211-rational.yaml.gz) |
| Receipt | [`receipts/certification.json.gz`](../../../packing/resources/web/franciscouzo-square-packing-2026-09-27/receipts/certification.json.gz) | [`receipts/certification.json`](../../../packing/resources/web/de-winter-square-packing-211-2026-09-16/receipts/certification.json) |
| Packet | [README](../../../packing/resources/web/franciscouzo-square-packing-2026-09-27/README.md) | [README](../../../packing/resources/web/de-winter-square-packing-211-2026-09-16/README.md) |

The tools are
[`devtools.upper_bound_packets`](../../../packing/devtools/upper_bound_packets.py),
which acquires, certifies and checks the packets;
[`sqpack.witness.promote_rational`](../../../packing/src/sqpack/witness.py), the
promotion it calls in process;
[`devtools.check_rational_witness_independent`](../../../packing/devtools/check_rational_witness_independent.py),
the second checker; and
[`devtools.apply_upper_bound_packets`](../../../packing/devtools/apply_upper_bound_packets.py),
which writes the case records from the receipts.

## 2. Verdict

**No mathematical defect found.** Every certificate is a set of `n` exact unit squares
with disjoint interiors inside `[0, S]²` for its rational side `S`, so `s(n) ≤ S`. Each
case’s verified upper bound is `S` rounded up at the printed precision, so it is an
upper bound too.
The promotion that produced the certificates does what its receipt says,
the two checkers that decided them share no geometry or verification code, and both
refuse the two mutations built to fail.
The three counts whose certificate lands more than one unit of the last place above the
printed side are recorded as a conflict and a blocker, not as agreement.
T-057’s novelty holds on the Kingbird catalogue and this record, which is how the record
now states it.

## 3. What an Exact Corner Certificate Proves

A certificate lists a rational side `S` and, for each square, its four corners
`c₀, c₁, c₂, c₃` with rational coordinates.
Three facts are decided over `ℚ`, with no tolerance:

1. **Each square is a unit square.** With edges `eᵢ = cᵢ₊₁ − cᵢ`, `eᵢ · eᵢ = 1`,
   `eᵢ · eᵢ₊₁ = 0`, `e₂ = −e₀` and `e₃ = −e₁`. The four corners are then the vertices,
   in order, of a square of side one.
2. **Each square lies in the container.** Every corner coordinate is in `[0, S]`. A
   square is the convex hull of its corners and the container is convex, so the whole
   square is inside.
3. **No two interiors meet.** For each pair, some direction among the four edge normals
   of the two squares projects them onto intervals that meet at most at an endpoint.
   The line perpendicular to that direction through a point separating the two intervals
   (their common endpoint, when they touch) has each interior strictly on its own side,
   so the interiors are disjoint.
   By the separating-axis theorem for convex polygons, such a direction exists for every
   pair of convex polygons with disjoint interiors, so a valid packing always passes.

Together these say the `n` squares form a packing of unit squares in a square of side
`S`, which is the definition of `s(n) ≤ S`. Nothing is scaled: the object checked is the
packing itself, contact is decided exactly (a gap of zero is allowed, a negative one
refused), and no margin is spent on rounding.
A floating-point check cannot do this at any tolerance, for the reason
[`sqpack.verify.verify_packing`](../../../packing/src/sqpack/verify.py) gives: a
tolerance large enough to accept exact contacts also accepts overlaps smaller than it.

The case records carry the verified value `V`, which is `S` rounded up at the source’s
printed decimals, or the printed side when that is larger
(`upper_bound_packets.verified_value`). Since `S ≤ V`, `s(n) ≤ V`, and `V`’s
`exact_form` is that decimal as a fraction.

## 4. The Robust-Rational Promotion

`packing-witness promote --strategy robust-rational --max-side-increase 1e-9`, which
`upper_bound_packets certify` runs in process with `rational_digits` 36, turns a decimal
centre-and-angle pose into a corner certificate:

- **Centres.** Each coordinate is rounded to 36 significant digits.
  Couzo’s literals carry 18 significant digits and de Winter’s 21, so the rounding
  leaves every centre exactly as the source printed it.
- **Angles.** For each angle `θ`, `t = tan(θ/2)` is computed at 56 digits and rounded to
  36 significant digits, a rational.
  The rotation is `cos = (1 − t²)/(1 + t²)` and `sin = 2t/(1 + t²)`, and then
  `cos² + sin² = ((1 − t²)² + 4t²)/(1 + t²)² = 1` exactly, so the square built from them
  is an exact unit square with rational corners.
  The angle moves by at most about `10⁻³⁶` radians.
- **Side.** The corners are translated so that the least `x` and least `y` are zero, and
  `S` is the largest coordinate that remains: the certificate’s side is its own exact
  extent, not the printed side.
- **Acceptance.** The candidate is kept only if `S` is at most the printed side plus
  `10⁻⁹`, compared as fractions, and the exact separating-axis test passes.
  Otherwise the centres are dilated about the container’s centre by `1 + 10⁻³¹`,
  `1 + 10⁻²⁹`, and so on, and the test repeats.

All 50 were accepted at the first candidate, **centre dilation 1** in every receipt.
Each certificate is therefore the source’s pose, centres unchanged and angles moved by
about `10⁻³⁶`, and its side is that pose’s extent to the same order.
Couzo’s sides moved by between `−1.61e-15` (`n = 268`) and `+2.13e-15` (`n = 259`), and
de Winter’s by `−2.1e-14`, which is his reported clearances surviving the rounding.
The `1e-9` allowance was never approached.

## 5. Two Checkers and Two Refusals

The promotion decides each candidate with `sqpack.verify.verify_packing` over exact
rational signs, and `packing-witness verify` replays that on the committed file.
`devtools.check_rational_witness_independent` decides the committed file again.
It shares no geometry or verification code with `sqpack.witness` or `sqpack.verify` (it
uses the same YAML loader): it re-derives the unit-square tests, takes the least
coordinate slack for containment, and for each pair takes the best gap over the four
edge normals, requiring it to be non-negative.
Both tested every one of the `n(n − 1)/2` pairs, 1,229,925 in all across the 50
certificates, and both report least containment clearance `0`: every certificate touches
its container, as a side equal to the extent must.
The walls were 1,202 s of promotion and 3,393 s of independent checking in all.

Two controls mutate the `n = 68` certificate, and each is refused by both checkers
([`negative-controls.json`](../../../packing/resources/web/franciscouzo-square-packing-2026-09-27/receipts/negative-controls.json)):

| Control | Independent checker | `exact_verify` |
| --- | --- | --- |
| Side cut by `1e-15` | Refused: container penetration `−1/10¹⁵` | Refused |
| Square 31 moved right by `1e-6` | Refused: two overlapping pairs | Refused |

The first shows that a certificate with zero slack fails at the smallest cut the printed
precision can express; the second shows that the pair test sees an overlap.
[`tests/test_upper_bound_packets.py`](../../../packing/tests/test_upper_bound_packets.py)
repeats both on a two-square packing that passes, so the controls are known to fail for
the reason named.

## 6. The Three Trailing Counts

At 20 of Couzo’s counts and at `n = 211` the certificate is at or inside the printed
side, and the verified value is the printed side.
At 26 it is one unit of the fifteenth decimal above, which
`bounds_agree_at_declared_precision` accepts as the same bound.
At three it is more:

| n | Printed side | Certificate minus printed | Verified value | Units above |
| --- | --- | --- | --- | --- |
| 206 | `14.860158663395859` | `+1.124e-15` | `14.860158663395861` | 2 |
| 259 | `16.602568490497649` | `+2.134e-15` | `16.602568490497652` | 3 |
| 305 | `17.952959459023539` | `+1.865e-15` | `17.952959459023541` | 2 |

Since the certificate’s side is the printed pose’s extent (§4), the printed side is
below the extent of the pose the source prints, most likely because the source computed
its side in `binary64`. The pose as printed therefore certifies only the larger value.
The record handles this as it should: `verified_upper_bound` carries the certified
value, `reported_upper_bound` keeps the source’s printed side, and each of the three
case records has a `replay-failure` conflict and a `mathematics` blocker, with a ceiling
section in the body saying that the verified value is neither `s(n)` nor a different
packing.
Closing the gaps needs a pose refined beyond `binary64`, for example by Newton’s
method on the active contacts, or coordinates the source prints at higher precision;
T-056’s `next_rung` says so.

## 7. The Review’s Own Verifier

The review wrote a third checker, `verify.py`, from scratch, and ran it on all 50
committed certificates.
It is kept outside the repository, beside its logs, at
`/tmp/claude-0/…/scratchpad/fable227/`, and shares no code with either checker above or
with the YAML library: it reads the certificate text line by line into
`fractions.Fraction`, then checks

- that the ids are `1…n` and each square is a unit square by the edge tests of §3;
- that every corner lies in `[0, S]²`;
- each pair whose axis-aligned bounding boxes overlap, by the separating-axis test on
  the four edge directions (a pair with separated boxes already has an exact separating
  line); and
- whether the certificate is tight, with some corner at `0` and some at `S`.

**All 50 pass, and all 50 are tight.** It decided the pairs its bounding boxes did not,
from 57 at `n = 106` to 455 at `n = 301`, in at most 0.3 s per certificate.
Its sample sides, from the exact fractions:

| n | Certificate side | Against the printed side |
| --- | --- | --- |
| 102 | `≈ 10.6071746801789459424` | `1.06e-15` below |
| 211 | `74989803524838470007/5000000000000000000` | `2.1e-14` below |
| 206 | as in §6 | `+1.12e-15` |
| 259 | as in §6 | `+2.13e-15` |
| 305 | as in §6 | `+1.87e-15` |

Its log prints each side through `binary64`, so the log’s digits past the sixteenth are
not the certificate’s; the values above are from the fractions.
The review also ran `upper_bound_packets check` and `check_source_coverage`, and both
passed.

## 8. Licence and Retention

Neither Couzo’s nor de Winter’s repository publishes a licence, and neither README names
an author, so each author is read from the commit metadata.
Their packets follow the
[known-best retention policy](../../../packing/resources/web/known-best-packings/README.md#source-packets-derived-facts),
the one the Kingbird catalogue’s packings are held under: a conservative repository
policy, not a legal conclusion.
Each packet keeps only derived facts and metadata: the centres and angles carried
verbatim into Witness/v2 files, and an acquisition record pinning every upstream file by
SHA-256 (all 99 of Couzo’s, with each count’s commit history, and de Winter’s three).
No upstream byte is kept (`raw_asset_retained: false`), and `upper_bound_packets check`
fails if any packet file has the digest of an upstream file the policy does not retain.
The rational certificates are this repository’s own derived objects, committed as
deterministic gzip under `packing/witnesses/`.

Griffin Casson licenses his code MIT and his packings, figures and paper CC BY 4.0, so
[his packet](../../../packing/resources/web/casson-square-packing-2026-09-23/README.md)
keeps 43 of his 109 files byte for byte and pins the rest by digest, and credits him as
the licence asks. None of his packings holds a field, and none was replayed.

## 9. The Scope of T-057’s Novelty

T-057 is previously published: de Winter’s repository published it on 16 September 2026.
What it adds to this record is scoped to the corpus the intake read, the Kingbird
catalogue (the retained capture of 25 August and the live page of 29 September) and this
repository’s case records:

- **211.** Neither the catalogue nor any case record held a packing of 211 squares below
  the `15 × 15` grid; this is the first on either.
- **`s(k² − k + 1) < k`.** The catalogue shows it at `n = 241, 273, 307`
  (`k = 16, 17, 18`), from Arslanov, Mustafin and Shangitbayev’s packings of March 2019.
  With 211 it holds at `k = 15` too.
  The case records at `n = 31, 43, …, 183` (`k = 6…14`) still hold the grid, and the
  grid is optimal at `k = 2…5`, so on the catalogue and this record the smallest `k`
  shown drops from 16 to 15.

No claim is made about sources outside that corpus, and nothing bears on optimality: the
verified lower bound at 211 is Nagamochi’s general bound, untouched.
The margin below 15 is about `0.002`.

## 10. Findings

| Severity | Finding |
| --- | --- |
| none | All 50 certificates pass the promotion’s exact test, the independent checker and the review’s verifier, each at centre dilation 1. |
| none | Every certificate is tight, so the side each proves is its own extent and nothing is padded. |
| minor | At `n = 206, 259, 305` the printed side is not certified; the record carries the certified value with a conflict and a blocker. Correct handling, and T-056’s claim states it. |
| minor, fixed | The receipt’s `units_above_printed` for 211 read `−2100010`, counted in the twentieth decimal. It is now the units the verified value sits above the printed side, `0` at or inside it, and `side_increase` keeps the signed distance. |
| minor, fixed | The ceiling sections printed Decimal’s `2E-15` beside the receipts’ `1.124e-15`; they now print one lowercase form. |
| minor, fixed | T-057’s significance and the 211 case record said the smallest such `k` “is known” to drop to 15, without the scope §9 gives. |
| note | The review’s log prints sides through `binary64`; exact values are taken from the fractions. |

## 11. What Remains

- **`C4`.** Both results need a method-distinct route, such as an interval-certified
  replay of each packing, for example a Krawczyk enclosure of its contact system as
  T-009 did at `n = 29`, recorded as a second evidence entry.
  For T-057, de Winter’s own 80-digit enclosures would serve if he publishes them.
- **The trailing counts.** A refined pose, or higher-precision coordinates from the
  source, is needed before the printed sides at `n = 206, 259, 305` certify.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
