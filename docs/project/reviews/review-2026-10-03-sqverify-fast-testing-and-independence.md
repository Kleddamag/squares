# sqverify-fast: Adversarial Testing and Independence Audit

`sqverify-fast` ([`packing/sqverify_fast`](../../../packing/sqverify_fast/README.md)) is
the clean-room verifier for measure-capture lower-bound certificates at the
201-direction net. This review tries to break it two ways: by feeding it certificates
that an exact computation shows to be false, and by auditing its claim to be an
independent implementation.
It does not check the mathematics of
[SOUNDNESS.md](../../../packing/sqverify_fast/SOUNDNESS.md); another reviewer does.

**Testing: accept.** 9,726 runs on certificates with an exact witness below the
threshold, the smallest deficit $3.9 \times 10^{-121}$ of the threshold, gave 9,726
refusals and no acceptance.
6,772 probes found no centre or box bound above the exact capture, and no disagreement
between the crate’s exact evaluator and this review’s. Three defects were found, none of
which lets a false certificate through: the release audit raises false alarms on slivers
with extreme densities (TI-1); `gzip` input with trailing data is admitted although the
repository’s Python loader refuses it (TI-2); and format L’s fixed net can be overridden
by `certificate.D` metadata (TI-3).

**Independence: accept, with the record to be corrected.** No identifier, constant,
limit, message or structure in the crate could only have come from `verify.cpp`,
`mixed_rotated_verify.cpp` or `unified_linear_verify.cpp`.
`relationship_to_generator: independent-implementation` is justified by the code.
The record departs from the specification’s clean-room protocol in ways it mostly
discloses (TI-4), and git cannot establish the separation it asserts (TI-5).

**Overall: accept.** No defect affects a verdict on any retained certificate, and none
is blocking.

The reviewer is Claude (adversarial AI review, testing and independence), separately
prompted as review lane RB on 2026-10-03, with no context shared with the implementing
lane W2. It registers nothing and moves no bound.

## Scope and Evidence

The subject is the crate at commit `717e4f8ca`: `src/` (4,146 lines with the two
documents), INDEPENDENCE.md and the eight commits that touch it, `d86714e0b` through
`16434721f`. The release binary was built from that commit with the pinned toolchain.

The testing tool is
[`devtools/attack_sqverify_fast.py`](../../../packing/devtools/attack_sqverify_fast.py),
written for this review and kept so that the run can be repeated.
Its ground truth is exact and does not come from the crate: the D4 expansion, the point
and segment capture and the axis-direction minimum are its own, and rectangle capture is
`sqpack.rectangle_density.exact_intersection_area`. It shares no code with
`devtools.check_sqverify_fast`. Three seeds (11, 12, 13) ran for 45 minutes each on four
cores, about 2.3 CPU hours in all, from `packing/`:

```bash
.venv/bin/python3 -m devtools.attack_sqverify_fast --seed 11 --budget-seconds 2700 \
    --out benchmarks/measure-verifier/review-2026-10-03-attack
```

The per-run logs are retained as `attack-seed{11,12,13}.jsonl.gz` in
[`benchmarks/measure-verifier/review-2026-10-03-attack/`](../../../packing/benchmarks/measure-verifier/review-2026-10-03-attack/),
with the reproducer for TI-1.

For the independence audit, the three checkers were read as this lane’s brief allows.
`verify.cpp` exists in eight identical copies (sha256 `a75140df…`) under
`external-square-certificates-2026-09-22/`; `mixed_rotated_verify.cpp` (`89b674a6…`) is
in `mixed_n50_L740/code/` and `unified_linear_verify.cpp` (`0249726a…`) in
`mixed_n101_L1028/code/`. The history was read with `git log`, `git show` and
`git merge-base`, and the specification from W1’s branch at `6c5ff1430`.

## How a False Certificate Was Built

A witness is a centre where the measure’s exact capture lies below the threshold, so a
verifier that accepts must be wrong.
Each run builds one and asks for the witness’s direction alone, with `--confirm` and a
budget of two million boxes:

1. **Pinning.** Take a measure and a centre $c$ near its minimum, compute the exact
   capture $F(c)$, and multiply every weight by a dyadic rational $k \le T(1 -
   \varepsilon)/F(c)$. The capture at $c$ is then exactly below $T$ by at least
   $\varepsilon T$. Here $\varepsilon$ ranges over $10^{-6}$, $10^{-12}$, $2^{-53}$,
   $2^{-80}$ and $2^{-200}$, far below anything binary64 resolves.
2. **The exact axis minimum.** At direction zero a rectangle measure’s capture is
   bilinear on each cell of the event grid, so its minimum over the whole domain $[B/2,
   L - B/2]^2$ is attained at a grid vertex and is computed exactly.
   Scaling then puts it at $T$ exactly, and at $T(1 - 2^{-k})$ for $k$ = 20, 52, 60, 120
   and 400.

Witnesses are drawn from the whole domain, not just the quadrant the verifier searches,
so lemma C1’s reduction is exercised too.
Format M witnesses lie in both the per-bin and Tokoharu domains.

| Family | What it attacks | Runs | Refused | Accepted |
| --- | --- | ---: | ---: | ---: |
| `axis-exact` | the vertex sweep at a minimum $2^{-20}$ to $2^{-400}$ below $T$ | 5,670 | 5,670 | 0 |
| `pinned` | random T, M and L measures: slivers to $10^{-15}$, densities to $10^{10}$, coordinates midway between adjacent binary64 values $\pm 10^{-40}$, edges on $0$ and $L$ | 1,363 | 1,363 | 0 |
| `edge-atoms` | a point or segment exactly on, or $10^{-40}$, $2^{-60}$ or $10^{-15}$ beyond, a square’s edge or corner | 1,332 | 1,332 | 0 |
| `retained` | `rect_n32_L595`, `mixed_n37_L644` and `mixed_n101_L1028`: pinned at the verifier’s own least-bound box, one orbit or point dropped, or one orbit moved by $10^{-30}$, $2^{-52}$ or $10^{-12}$ | 1,361 | 1,361 | 0 |
| total |  | 9,726 | 9,726 | 0 |

The refusals break down as 6,014 axis-sweep refusals, 3,082 counterexample candidates,
574 budget exhaustions and 56 audit failures.
No run timed out, and no generated certificate was refused at admission.
In 3,712 runs `--confirm` evaluated the stopping pose exactly, and the crate’s rational
value equalled this review’s every time.
When the minimum was set exactly equal to the threshold, all 1,134 axis runs refused.
The claim was then true, so refusing is a matter of completeness, and is expected of a
search that needs a positive margin.

The `differential` and `edge-atoms` probes compare `--probe` with the exact capture at
6,772 centres over 2,692 random measures, with boxes of half-width $10^{-9}$ to
$10^{-2}$. The crate’s exact capture equalled this review’s at every centre.
No centre bound exceeded the exact capture, and no box bound exceeded the least exact
capture at the box’s centre and three random rational points in it.
The edge-atom probes include points on a corner, which the closed square counts, and
points $10^{-40}$ outside it, which it must not count.

Admission was given 24 hand-made inputs.
It refused, with exit 2, mass equal to $n$, $B(1 + D) = 1$, a rectangle $10^{-30}$ past
the edge, a negative weight of $-10^{-300}$, `NaN`, an exponent of $10^{6}$, a count or
side that disagreed with the request or the metadata, a threshold below one, a wrong
`total_mass`, a degenerate rectangle, a bad format L net, a format M `points` entry, a
zero-length segment, a duplicate key nested inside `certificate`, and trailing text
after the JSON. It admitted mass $n - 10^{-30}$ and a weight of `-0`, both correctly.
It also admitted the four inputs that TI-2 and TI-3 describe.

## Testing Findings

### TI-1 — Low: the release audit raises false alarms on slivers with extreme densities

56 refusals were `audit-failed`, a verdict that says the search’s bookkeeping is wrong
and that nothing it accepted can be trusted.
In all 20 cases examined, the bookkeeping was right and the audit’s own recomputation
was the looser bound.

`full_centre_bound` takes each rectangle’s area as the area of its inner representable
rectangle $[x_1^\uparrow, x_2^\downarrow] \times [y_1^\uparrow, y_2^\downarrow]$ times
$\rho^-$. For a sliver $10^{-15}$ wide, the outward and inward roundings remove a large
share of its width, and a density of $10^{10}$ magnifies that loss.
The incremental path counts a sliver that lies wholly inside the square by its exact
mass enclosure, so it stays tight.

The reproducer `audit-false-alarm-018.json.gz` (format M, direction 200) shows the gap
at its widest. At the stopping centre the incremental bound is $2.29231199129079$, the
exact capture is $2.29231199129080$, and the full recomputation gives $1.76412594$.
`AUDIT_TOLERANCE` is $10^{-9}(1 + |F|)$ and so cannot tell this from a real error.
In every case examined the incremental bound was at or below the exact capture.

The same effect makes `--probe`’s `centre_lower_bound` loose on such inputs.
Over the rectangle-only formats its gap to the exact capture had a median of
$9 \times 10^{-10}$ to $2 \times 10^{-9}$, but a 90th percentile of $0.015$ to $0.034$,
against the roughly $10^{-11}$ that SOUNDNESS.md’s R2 note leads one to expect on
ordinary data. Also, 41 of the 3,082 `counterexample-candidate` verdicts were not
counterexamples at the reported centre: the heuristic’s $10^{-9}$ margin assumes R2’s
accuracy.

The effect on soundness is none, since every one of these outcomes is a refusal.
The cost is completeness and diagnosis on extreme inputs, and the audit cannot tell
looseness from corruption.
The fix is to compare the audit with a tolerance scaled by $\sum \rho^+ \cdot
\mathrm{ulp}$ of the boundary rectangles.
Or the full recomputation could use the inside/outside shortcut for rectangles it can
classify, keeping the classification-free recomputation only for the boundary list.

### TI-2 — Low: gzip input with trailing members or bytes is admitted

`certificate::read_json` decodes with `flate2::read::GzDecoder`, which stops after the
first gzip member. A retained candidate with a second gzip member appended, or with the
bytes `garbage` appended, is admitted and verified as the first member alone.
Python’s `gzip`, which `sqpack.rectangle_density.load_candidate` and the census use,
refuses both (`JSONDecodeError`, `BadGzipFile`). The receipt’s `input_sha256` covers the
whole file, so it binds bytes that another reader of the record refuses.

The effect on soundness is none: what is verified is a valid certificate, and the
theorem holds for it.
Still, it is the reader disagreement that the crate’s duplicate-key refusal exists to
prevent. The fix is to read with `MultiGzDecoder` and refuse a second member, or to
refuse any bytes left after the first member.

### TI-3 — Low: format L’s fixed net can be overridden by metadata

SOUNDNESS.md says admission refuses “a format L `net` other than step $83/40000$ and
last index $200$”. Admission does check the `net` block, but the step and count it then
uses come from `certificate.D` and `certificate.angle_count` when those are present.
A format L candidate with the required `net` block and `"certificate": {"D": "9/20",
"angle_count": 3}` is admitted, and with $B = 1/2$ is reported `VERIFIED` over three
directions, with `"D": "9/20"` in its premises.

The effect on soundness is none: the theorem holds for any net whose premises admission
checks. But the documented constraint does not hold, and a census that reads only
`status` would count a three-direction run as a 201-direction one.
The fix is to refuse `certificate.D` or `angle_count` that disagrees with the format’s
net, and to refuse any override for formats L and M.

There is an observation for the mathematics reviewer here, not a finding of this review.
Format M’s domain $\rho(a_r)$ with $a_r = t_r - D/2$ reads as bins of half-width $D/2$
in $t$. Within such a bin, the angle can differ from $\theta_r$ by up to
$2\arctan(D/2)$, whose tangent $D/(1 - D^2/4)$ exceeds $D$. If the per-bin argument
assigns orientations that way, N3 needs $B(1 + D/(1 - D^2/4)) <
1$, not the $B(1 + D) < 1$ that admission checks.
At $D = 83/40000$ the two limits are $0.99792929449$ and $0.99792929671$. Every retained
certificate has $B = 0.9977$, so no retained verdict is affected, and with metadata
overrides the gap could widen.

## Independence Findings

### What the code shows

No trace of the three checkers was found.
The checkers share one kernel (`verify.cpp:15-96`); the crate differs from it in every
mechanism that matters:

- **Rounding.** The checker widens with `nextafter`. The crate takes a branch-free step
  of $2^{-52}|x|$ plus a tiny term (`interval.rs`, its own lemma I1) and encloses
  constants from exact rationals by exact comparison (`exact.rs`).
- **Area.** The checker clips a polygon, takes the hull and shrinks it by $1 - 10^{-9}$.
  The crate integrates a concave section by trapezoids over up to 14 nodes
  (`rotated.rs:539-603`).
- **Derivative.** The checker’s `slice` uses $A_1 = B/(2s)$, $k_1 = -c/s$; the crate
  takes the minimum of nine affine terms (`rotated.rs:609-628`).
- **Search.** Only the crate classifies rectangles as inside, outside or boundary with
  slack, inherits lists and derivative bounds, audits, and evaluates exactly at the
  depth limit.
- **Direction zero.** `verify.cpp` loops over a grid the certificate supplies; the crate
  builds its own event grid and sweeps it exactly.
- **Limits.** The checker uses $10^7$ nodes, a $2^{-45}$ floor and, in the linear
  checker, a $2^{-40}$ floor and an anisotropy cap of 4. The crate uses $5 \times 10^7$
  nodes, depth 60, 4,096 deep boxes and 32 exact centres.

None of the checkers’ distinctive constants or messages appears in the crate: `1e-14`,
`0x1p-45`, `UNRESOLVED`, `ANGLE_VERIFIED`, `REGION_*`.

What is shared, each with its classification:

| Shared item | Classification |
| --- | --- |
| $83/40000$, 201 directions, $10001/10000$, exact $c$ and $s$ from $t = rD$, the JSON keys | the certificate format |
| the quadrant $[L/2, L - a_r]^2$ | the mathematics (quarter turn), stated in the allowed reviews |
| the bound $F(c_0) - G_x d_x - G_y d_y$ with edge-length differences as the derivatives | the mathematics, in the allowed Tokoharu review |
| a section of the rotated square as $\min(\cdot) - \max(\cdot)$ of its edges | the geometry. The checker uses it for edge lengths, the crate to integrate area |
| splitting along the axis with the larger penalty; a depth-first stack; bisection at the midpoint | common practice |
| helper names `dn` and `up` | a common abbreviation; the scaling review the record discloses also uses `up(…)` |
| the segment bound: clip the parameter to both strips, prove the two ends inside, appeal to convexity, mass uniform in $\lambda$ | the mathematics of the allowed section of the linear review, which states that a sub-segment counts when both its ends do. The four-step order of the comments is close to `unified_linear_verify.cpp:83-96`, and the record reads that review without line ranges outside 86–161 (see TI-4) |
| `1e-9` as a tolerance | a common value, derived afresh in lemma F2 for a different purpose |

The label `relationship_to_generator: independent-implementation` is justified.

### TI-4 — Low: the record departs from the specification’s clean-room protocol

The specification (`plan-2026-10-02-independent-measure-verifier.md` at `6c5ff1430`, on
W1’s branch) sets the protocol in §2.2–§2.4. The record departs from it four ways:

1. **A review read in full.** The record says the scaling review was read “in full”,
   including its sections on fixed-width types, floating-point constants and hard
   limits, which describe `verify.cpp`’s constants with line numbers.
   §2.2 allows only “The Net and the Box Argument at Side 9” and “The Monotone
   Transfers”. The record discloses this and states that nothing was used; the code bears
   that out.
2. **Tokoharu review sections outside the allowance.** Lines 1–194 and 225–318 include
   “Scope and Evidence” and “Exact Preconditions and Replay Results”, which §2.2 does
   not list. The latter describes controls that alter `src/verify.cpp`. Disclosed.
3. **Replay receipts read.** §2.3 forbids “replay receipts and logs under
   `packing/resources/web/**/receipts/`, which hold the checkers’ raw output”.
   The record lists reads of `receipts/replay/audit.json`, `receipts/controls/*.json`,
   and `merged.json`, `summary.json`, `directions.jsonl` and `control.json` under
   `receipts/`. The census tool reads them as a matter of course.
   These hold verdicts, counts and timings, not code, so the risk is small, but the
   record does not call this a departure.
4. **No machine-readable record.** §2.4 requires `independence-record.yaml` at the
   crate’s root, with the commit range, the spec versions read, and each lane’s sessions
   and harness. The crate has only the prose INDEPENDENCE.md, which names no spec version
   and no session.

The record also says “No passage quoting or paraphrasing checker code line by line was
read”. For the linear review it names lines 86–161, the allowed section, and gives no
range for the “atom bounds” it read.
The section “The Checker, Function by Function” (lines 162–290) paraphrases
`segment_lower` line by line.
The record should state the exact ranges read, or soften the sentence.

The fix is to write `independence-record.yaml` per §2.4, and to list items 1–3 as
departures with the reason for each.
Alternatively, amend §2.3 to allow summary fields of receipts, which the census needs.

### TI-5 — Note: git cannot establish the separation the record asserts

All eight crate commits carry the trailer `Claude-Session:
https://claude.ai/code/session_01HbQD6XX8UwXyhUcQ7fCG46`. The same trailer is on 143
commits in all, among them commits that wrote and changed the checker drivers the
protocol forbids the implementer to read: `audit_wand125_rectangles.py`,
`audit_wand125_point_and_mixed.py`, `audit_wand125_linear.py` (`121588baf`, `2038c32f9`,
`2d7197185`) and `replay_evand_zmx2.py` (`27abc4500`). The trailer names the
coordinating session, not the lane, so git cannot tell the implementer’s commits from
the coordinator’s; this review’s own commits carry it too.
No crate commit touches a forbidden file.
The specification is on W1’s branch (`origin/claude/lane-w1-verifier-spec`), and was
added and then removed on this line (`d86714e0b`, `abf0a592b`) so that the forbidden
files it links stay off W2’s branch.
The crate’s first commit already holds the whole crate and INDEPENDENCE.md, so the
history does not show the order of reading.
The chronology it does show is consistent: the spec at 17:17, the crate at 19:26,
Milestone B after Milestone A.

So the separation rests on the implementer lane’s context isolation and on the
coordinator relaying nothing code-level (§2.1). Neither is recorded.
That is why §2.4’s per-lane sessions and harness matter.
The lane’s prompt, or a digest of it, would let a later auditor check the coordinator’s
side.

## Claims by Evidential Status

- **Computationally verified here.** 9,726 certificates, each with an exact witness
  below the threshold, were refused.
  No `--probe` bound exceeded the exact capture, and the crate’s exact capture equalled
  this review’s at 6,772 centres and 3,712 confirmed poses.
  TI-1 to TI-3 reproduce from the retained inputs.
- **Read here.** No checker-specific identifier, constant, limit, message or structure
  is in the crate. TI-4 and TI-5 rest on the record, the specification and git.
- **Not checked.** The mathematics of SOUNDNESS.md, the retained certificates beyond the
  directions sampled, and the continuous-angle formats D and P, which the crate does not
  implement. Random testing cannot rule out a defect in a region the generators do not
  reach. The largest such regions are measures with thousands of orbits and directions
  near 200 with many segments.

## Disposition

| Finding | Severity | Blocking | Suggested owner |
| --- | --- | --- | --- |
| TI-1 audit false alarms on extreme slivers | Low | no | `think-gpe0` lane W2 |
| TI-2 gzip trailing data admitted | Low | no | `think-gpe0` lane W2 |
| TI-3 format L net overridable by metadata | Low | no | `think-gpe0` lane W2 |
| TI-4 record departs from §2.2–§2.4 | Low | no | `think-3ok2` |
| TI-5 git cannot show lane separation | Note | no | `think-3ok2` |

Verdicts: testing **accept**, independence **accept**, overall **accept**.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
