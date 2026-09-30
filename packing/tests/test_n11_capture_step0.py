"""Focused complete-step kernel and compression refusal controls."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction as Q

import pytest

from devtools import check_n11_capture_step0 as step0


def test_step_kernel_requires_all_row_planes_and_exact_compression() -> None:
    kernel = [(Q(), Q()), (Q(1), Q()), (Q(1), Q(1)), (Q(), Q(1))]
    step = {
        "common_owned_kernel": [[str(x), str(y)] for x, y in kernel],
        "compression_source_hull": [[str(x), str(y)] for x, y in kernel],
        "inner_grid_compression": {
            "denominator": 1,
            "directions": 4,
            "vertices": [["0", "0"]],
            "witnesses": [{"indices": [0], "weights": ["1"], "point": ["0", "0"]}],
        },
    }
    planes = [(Q(1), Q(), Q(1)), (Q(-1), Q(), Q()), (Q(), Q(1), Q(1)), (Q(), Q(-1), Q())]
    assert step0.check_kernel(step, [(Q(), Q())], planes) == [(Q(), Q())]

    with pytest.raises(ValueError, match="kernel outside"):
        step0.check_kernel(step, [(Q(), Q())], [*planes, (Q(1), Q(), Q(1, 2))])
    wrong_witness = deepcopy(step)
    wrong_witness["inner_grid_compression"]["witnesses"][0]["weights"] = ["1/2"]
    with pytest.raises(ValueError, match="compression weights"):
        step0.check_kernel(wrong_witness, [(Q(), Q())], planes)
