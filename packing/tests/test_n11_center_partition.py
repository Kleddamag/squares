"""Case credit requires both terminal branches and a fully joined frontier."""

from copy import deepcopy

import pytest

from devtools.check_n11_center_partition import admit_complete


def test_both_complete_branches_required() -> None:
    valid = {
        "nodes_completed": 8,
        "branches_completed": ["le", "ge"],
        "current_node": None,
        "current_branch": None,
        "current_step": None,
        "current_row": None,
        "pending_row_indices": [],
    }
    admit_complete(valid)
    for field, value in (
        ("nodes_completed", 7),
        ("branches_completed", ["le"]),
        ("current_row", 0),
        ("pending_row_indices", [1]),
    ):
        invalid = deepcopy(valid)
        invalid[field] = value
        with pytest.raises(ValueError, match="incomplete"):
            admit_complete(invalid)
