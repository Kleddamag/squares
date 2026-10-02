"""The n11 ownership kernel, parametrised by a frame so that it runs on n11 and n17.

The kernel's arithmetic is copied from the frozen native n11 checkers under
`packing/devtools/`, which stay byte-pinned by their receipts and are never edited. What
was a module constant there (the cap, the field side and scale, the cells, the symmetry
group, the state size) is a `Frame` here; everything else is the same exact rational
arithmetic in the same order. `docs/project/reviews/` holds the adaptation spec
(`review-2026-10-02-n17-kernel-adaptation-spec.md`).

Lifted so far, from `check_n11_optimality_field_mask0.py`:

* `geometry`: clipping, areas, the half-angle chart, quadratic envelopes;
* `sweep`: the exact vertical-sweep union cover;
* `ownership`: strict capture of a field point over a cell and every angle;
* `counting`: the row envelope and strict core, the majority median strip, one row of
  the counting mode, the row partition, the containment-plus-symmetry transfer, and the
  packet replay;
* `frame`: frames, symmetry actions and orbit representatives;
* `n11` and `n17`: the two frame adapters.

The method control is `devtools/check_hull_kernel_mask0.py`, which replays n11's mask-0
field packet through this package and refuses unless it matches the frozen checker and
its retained receipt exactly.
"""

from sqpack.hull_kernel.counting import (
    CountingPacket,
    MajorityFeature,
    counting_row,
    partition_rows,
    replay_counting_packet,
    row_envelope,
    transferred_states,
)
from sqpack.hull_kernel.frame import Frame, SymmetryAction, make_frame, orbit_representatives
from sqpack.hull_kernel.geometry import Budget, IncompleteError, RefusalError
from sqpack.hull_kernel.ownership import ownership
from sqpack.hull_kernel.sweep import exact_union_cover

__all__ = [
    "Budget",
    "CountingPacket",
    "Frame",
    "IncompleteError",
    "MajorityFeature",
    "RefusalError",
    "SymmetryAction",
    "counting_row",
    "exact_union_cover",
    "make_frame",
    "orbit_representatives",
    "ownership",
    "partition_rows",
    "replay_counting_packet",
    "row_envelope",
    "transferred_states",
]
