# Research: Where the Authors’ Measure Checkers Spend Their Time

**Date:** 2026-10-02

**Author:** Claude (agent), lane W1 of `think-gpe0`, for the squares project

**Status:** Complete for one certificate of each net family.
The continuous-angle checker, Daniel’s `zmx2`, was not profiled.

**Tracking:** `think-fcxx`, under `think-gpe0`

**Clean-room status: dirty side, not an implementer input.** This note names the
functions of Tokoharu’s and wand125’s checkers and interprets their profiles.
Under the
[independent verifier’s clean-room protocol](../specs/active/plan-2026-10-02-independent-measure-verifier.md#2-clean-room-protocol),
lane W2 and any later implementer lane do not read it.
What the implementers need from it is restated in that plan’s §3 as targets argued from
clean measurements, and the timings are in
[`timings.json`](../../../packing/benchmarks/results/author-checker-profile-2026-10-02/timings.json).

## Overview

All three checkers spend most of their time in interval arithmetic, and a large share of
it in one library call: every interval endpoint is widened by a call to `nextafter` in
`libm`, which callgrind puts at 62 per cent of the rectangle checker’s instructions, 58
per cent of the mixed checker’s and 45 per cent of the linear checker’s. Interval
multiplication is most of the rest.

The three differ in how many pieces a box touches.
The rectangle and mixed checkers run their area kernel on far fewer rectangles than the
measure holds, about 197 per box of 1,832 for `rect_n20_L48975` and 50 of 2,536 for
`mixed_n76_L894`, so they evidently screen distant rectangles cheaply first (an
inference from the call counts; this note did not read the code for it).
The linear checker evaluates every one of the 7,176 segment images at every box, by the
same count, and its point loop runs once per box over all 2,664 point images.

So the independent verifier’s gain comes from two places, in different proportions per
family: cheaper enclosures (all three), and classification with inheritance (mostly the
linear family, then the rectangle family; little for the mixed one, whose near set is
already about its straddling set).

## What Was Run

[`profile_author_measure_checkers.py`](../../../packing/benchmarks/profile_author_measure_checkers.py),
from `packing/`, with two workers, on the session host (Intel Xeon at 2.1 GHz, four
logical CPUs, shared with other sessions, load average 9 to 32):

```bash
uv run --frozen --all-extras --group dev python -m benchmarks.profile_author_measure_checkers \
  --workers 2 --callgrind-rectangle --scratch <scratch>
```

It builds each checker from the retained packet at its pinned digest under the reviewed
compile line plus `-g` for the timed runs and callgrind, and with `-g -pg -static` for
gprof, so that `libm` is inside the sampled text.
`perf` is not installed on the host.
Every complete timed direction reproduced its recorded node count, and for the rectangle
certificate its leaves and printed bound too.
The attribution runs are on each family’s least direction: the whole of it for the
rectangle checker, which takes no node limit, and bounded prefixes for the other two
(30,000 boxes under gprof and callgrind for the mixed checker; 20,000 under gprof and
5,000 under callgrind for the linear one).
The parsed profiles are in
[`attribution.json`](../../../packing/benchmarks/results/author-checker-profile-2026-10-02/attribution/attribution.json),
and the raw flat profiles and annotations beside it in `attribution/raw/`.

## Findings

### The rectangle checker: near rectangles, each at full cost

On direction 30 of `rect_n20_L48975` (34,887 boxes, run to completion under gprof):

| Function | Share of samples | Calls per box |
| --- | ---: | ---: |
| `operator*(I, I)`, interval multiplication | 43.6 % | 5,910 |
| `nextafter` (`libm`) | 38.7 % | not counted |
| `slice`, one edge’s chord enclosed over the box | 5.6 % | 768 |
| `area_lower`, the certified inscribed-polygon area | 5.6 % | 197 |
| `bound`, the per-box loop | 3.4 % | 1 |
| `operator/(I, I)` | 1.5 % | 1,520 |

Of the 1,832 rectangle images, about 197 per box reach `area_lower` and about 192 get
four `slice` calls each (768 is $4 \times 192$). The locality census of the same
direction, at the scale of the leaves, counts 158 rectangles near the swept core, 111 of
them inside every core of the box and 20 straddling.
So by the counts, the chord work at least is paid for rectangles that are inside
throughout the box, whose chord terms cancel; whether `area_lower` short-circuits those
is not visible in a flat profile.
Either way, the time is almost entirely interval multiplication and endpoint widening.

### The mixed checker: the same kernel, a smaller near set, arithmetic-bound

On the first 30,000 boxes of direction 3 of `mixed_n76_L894`:

| Function | Share of samples | Calls per box |
| --- | ---: | ---: |
| `operator*(I, I)` | 47.5 % | 2,487 |
| `nextafter` (`libm`) | 37.6 % | not counted |
| `area_lower` | 8.7 % | 50.5 |
| `bound` | 1.7 % | 1 |
| `slice` | 1.2 % | 169 |

About 50 rectangles per box reach the area kernel, against 52 straddling and 72 near in
the census. The mixed measure’s near set is already close to its straddling set, so
classification with inheritance buys little here; the gain has to come from cheaper
enclosures and fewer operations per rectangle.
Interval multiplication and widening are 85 per cent of the samples.

### The linear checker: every point and segment at every box

On the first 20,000 boxes of direction 35 of `mixed_n101_L1028`:

| Function | Share of samples | Calls per box |
| --- | ---: | ---: |
| `operator*(I, I)` | 46.5 % | 9,875 |
| `nextafter` (`libm`) | 30.0 % | not counted |
| `segment_lower` | 18.7 % | 7,176 |
| `singular_lower`, the point and segment loop | 4.2 % | 1 |
| `operator/(I, I)` | 0.7 % | 3,200 |

`segment_lower` runs 7,176 times per box, once for every segment image, and
`singular_lower`, which the
[2 October review](../reviews/review-2026-10-02-wand125-linear-certificates-and-n76.md)
reads as testing each point atom over the box, runs once per box.
Neither shows a locality filter in the counts.
The census counts 26 straddling pieces per leaf-scale box out of 9,872. This is the
family where classification with inheritance pays most.

### Instructions per box

Callgrind on the reviewed build (plus `-g`):

| Run | Boxes | Instructions per box | Share in `nextafter` |
| --- | ---: | ---: | ---: |
| Rectangle, direction 30, complete | 34,887 | 2.88 million | 61.9 % |
| Mixed, direction 3, first 30,000 boxes | 30,000 | 1.16 million | 57.7 % |
| Linear, direction 35, first 5,000 boxes | 5,000 | 5.05 million | 44.8 % |

## What This Means for the Independent Verifier

- **Arithmetic, all three families.** Widening by a `libm` call after every interval
  operation is the largest single cost.
  Inline `next_up` and `next_down`, or one widening per compound expression under a
  proved error bound, should cut the arithmetic cost by a factor of several.
  This is the whole of the plausible gain for family M: on the order of 5 to 15 times,
  short of the plan’s thirty-times target unless W2 also reduces the operations per
  rectangle or the node count.
  The plan names family M as the one to watch, without the reason given here.
- **Classification, families T and L.** Family T evaluates about 197 rectangles per box
  in full where about 20 straddle: about ten times less heavy work, before arithmetic,
  so 30 to 50 times overall is plausible.
  Family L evaluates about 9,840 points and segments per box where about 26 straddle;
  with arithmetic, two orders of magnitude or more, until per-box bookkeeping dominates.
- **What the plan may say.** Only the conclusions above, stated as targets and argued
  from the clean census, cross to the implementer side; the function names, call counts
  and shares in this note do not.

## Limits

- One certificate per family and three directions each; the mixed checker’s cost per box
  rises with depth (49 µs over the first 3,000 boxes, 136 µs over 30,000, 227 µs over
  the whole direction), so its 30,000-box callgrind run is a middle-depth sample.
- gprof’s `mcount` adds a call’s worth of overhead to every non-inlined function, which
  inflates the interval operators’ share; callgrind’s instruction counts do not, but
  instructions are not cycles, and a `nextafter` call’s cost in cycles is not measured.
- The host was shared and loaded; CPU times are per process from `wait4`, and the two
  runs of the same directions, an hour apart, agreed within about 5 per cent.

## References

- [The profiling tool](../../../packing/benchmarks/profile_author_measure_checkers.py)
  and its
  [attribution](../../../packing/benchmarks/results/author-checker-profile-2026-10-02/attribution/attribution.json)
- [The independent verifier’s plan](../specs/active/plan-2026-10-02-independent-measure-verifier.md)
- [Exact arithmetic and verifier performance, 30 September](research-2026-09-30-exact-arithmetic-verifier-performance.md)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
