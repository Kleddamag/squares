"""Exact closed-interval cover: is a closed target inside a finite union of closed intervals?

Contract of `covers_closed_interval(target, covers)`:

- Every endpoint is an exact `Fraction` or `int` (`bool` excluded); a float, a NaN, a
  string or any other value raises `ValueError`, as does a pair that is not a 2-tuple
  or 2-list, or one whose low endpoint exceeds its high endpoint.
- A singleton target `[a, a]` is covered iff some supplied closed interval contains
  `a`. A cover lying wholly below `a`, such as `[0, 0]` for `[1, 1]`, does not count.
- A target `[lo, hi]` with `lo < hi` is covered iff the union of the closed covers
  contains every point of it. Closed intervals that touch join (`[0, 1/2]` and
  `[1/2, 1]` cover `[0, 1]`); a positive gap breaks coverage however small it is.
- An empty cover family covers nothing, and the answer is exact: no tolerance.

This supersedes, for new callers, the historical slice predicate `covers_vertical` in
`packing/devtools/check_n11_optimality_field_mask0.py:446-459`. That recurrence starts
its cursor at the target's low end and, after each span that does not start above the
cursor, returns True once the cursor has reached the high end. For a singleton target
the first such span passes that test even when it ends below the point, so `[1, 1]` is
"covered" by `[0, 0]`. Over all 12,180 target/family pairs drawn from the 28 closed
intervals with integer endpoints in -3..3, it makes 616 false accepts, every one on a
singleton target, and no false refusals; on a target of positive length it is exact.
Section C2 of `docs/project/reviews/review-2026-10-03-n11-optimality-adversarial-gpt6-pro.md`
reports the defect.

The historical function stays byte-for-byte as it is. Eight later modules pin that
file by SHA-256 (for example `KERNEL_SHA` in `check_n11_optimality_field_mask202.py:25`
and `check_n11_optimality_field_runner.py:27`, `GEOMETRY_SHA` in
`check_n11_capture_root_pilot.py:33` and `check_n11_generic_fresh.py:33`, and
`GEOMETRY_SOURCE_SHA` in `n11_indexed_exact_cover.py:26`), and 357
retained receipt files under `packing/resources/web/n11-optimality-2026-09-29/receipts/`
record the same digest. Editing it would break the provenance of every result
already produced with it.

Where the historical predicate is still called, and the contract that keeps those
calls sound. Its only caller is the frozen sweep `exact_union_cover`
(`check_n11_optimality_field_mask0.py:495`), which refuses a domain of zero area (:466)
and probes every vertex and edge-crossing abscissa and every midpoint between
consecutive ones (:470-495). At every abscissa strictly inside a positive-area convex
domain's x-projection the slice has positive length, so the old rule is exact there.
Between consecutive events no edges cross, so a midpoint's verdict holds across its
open strip. The checked slices therefore cover a dense subset of the domain, and a
finite union of closed regions contains its limits, the two extreme slices included.
That closure argument (review C2) needs the complete sweep, a full-dimensional convex
domain and finitely many closed convex regions. It does not make an isolated call
correct. Callers of the frozen sweep:

- Field row builders: mask 0 (`check_n11_optimality_field_mask0.py:537`), mask 202
  (`check_n11_optimality_field_mask202.py:220`) and the general runner's unweighted
  branch (`check_n11_optimality_field_runner.py:692`). Each requires a positive-area
  domain (mask0 :522, mask202 :190, runner :644) and clips every region to it with
  `intersect(domain, ...)`, so a region's slice at a singleton target is that singleton
  or empty and the false-accept trigger cannot occur. The runner's weighted branch
  (`weighted_union_cover`, :529) tests points directly and does not use the predicate.
- Capture and generic consumers: root pilot (`check_n11_capture_root_pilot.py:248`,
  area required :237), root continuation (`check_n11_capture_root_continue.py:251`),
  transition pilot (`check_n11_capture_transition_pilot.py:351`), step 0
  (`check_n11_capture_step0.py:128`), root node (`check_n11_capture_root_node.py:240`,
  also reached through `check_row` from `check_n11_capture_child_node.py:544` and
  `check_n11_capture_branch_r1_node.py:99`), generic fresh
  (`check_n11_generic_fresh.py:317`, area required :307) and generic sequential with
  its default `cover_backend="reference"` (`check_n11_generic_sequential.py:336`). Their
  forbidden Minkowski hulls and residual polygons are not clipped to the domain and may
  extend past it, so they rely on the complete-sweep closure argument above. Root
  continuation, transition pilot, step 0, root node and generic sequential send a
  zero-area legal domain to `exact_cover_closed_degenerate`
  (`check_n11_closed_degenerate_cover.py:83`); root pilot and generic fresh refuse it.

Two corrected copies already exist and need no change. `_covers_vertical` in
`packing/devtools/n11_fast_exact_cover.py:90-105` skips spans ending below its cursor
(:98-99) and agrees with the exact oracle on all 12,180 cases;
`n11_indexed_exact_cover.py:118` reuses it. The point/segment helper
`check_n11_closed_degenerate_cover.py:114-121` sweeps the parameter interval `[0, 1]`
with every region interval clipped into it. Its target is never a singleton, even when
the domain is a point.
"""

from __future__ import annotations

from collections.abc import Sequence
from fractions import Fraction

type Interval = tuple[Fraction, Fraction]
type Bounds = tuple[Fraction | int, Fraction | int]


def _endpoint(value: object, role: str) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise ValueError(f"{role} endpoint must be an exact Fraction or int, got {value!r}")


def _interval(pair: object, role: str) -> Interval:
    if not isinstance(pair, tuple | list) or len(pair) != 2:
        raise ValueError(f"{role} must be a pair of endpoints, got {pair!r}")
    low, high = (_endpoint(value, role) for value in pair)
    if low > high:
        raise ValueError(f"{role} has its low endpoint above its high endpoint: {pair!r}")
    return low, high


def covers_closed_interval(target: Bounds, covers: Sequence[Bounds]) -> bool:
    """Return whether the union of the closed `covers` contains the closed `target`."""
    low, high = _interval(target, "target")
    spans = sorted(_interval(span, "cover") for span in covers)
    if low == high:
        return any(start <= low <= stop for start, stop in spans)
    reach: Fraction | None = None  # once set, [low, reach] lies inside the union
    for start, stop in spans:
        frontier = low if reach is None else reach
        if stop < frontier:
            continue
        if start > frontier:
            return False
        reach = stop
        if reach >= high:
            return True
    return False
