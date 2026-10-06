"""Focused contracts for the resumable native n=17 search driver."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import copy
from pathlib import Path

import pytest

from devtools import pilot_n17_subpattern_bb as pilot
from devtools import run_n17_bb_parallel as parallel


def _node() -> pilot.Node:
    return pilot.Node(
        angles=((-0.0, 1.0),),
        boxes=((1.0, 2.0, 3.0, 4.0),),
        windows=(),
        depth=7,
        share=0.125,
    )


def _binding() -> dict[str, object]:
    return {
        "pattern": ["cell-a"],
        "design": "test-design",
        "parameters": {"theta0": 0.4, "floor": 1e-6},
    }


def test_node_state_round_trip_preserves_every_float() -> None:
    node = _node()

    restored = parallel._node_from_record(  # noqa: SLF001
        parallel._node_record(node),  # noqa: SLF001
        squares=1,
        pairs=0,
    )

    assert restored == node
    assert restored.angles[0][0].hex() == "-0x0.0p+0"


def test_state_resume_binds_semantics_but_not_code_provenance(tmp_path: Path) -> None:
    state = tmp_path / "state.json"
    binding = _binding()
    document = parallel._state_document(  # noqa: SLF001
        binding=binding,
        queue=[_node()],
        nodes=11,
        closed_share=0.875,
        cpu_seconds=2.0,
        search_cpu_seconds=1.5,
        cpu_seconds_complete=True,
        wall_seconds=3.0,
        hit_floor=False,
        provenance=[{"git_revision": "old"}],
    )
    parallel._atomic_json(state, document)  # noqa: SLF001

    loaded = parallel._load_state(state, binding)  # noqa: SLF001

    assert loaded[:8] == ([_node()], 11, 0.875, 2.0, 1.5, 3.0, True, False)
    assert loaded[8] == [{"git_revision": "old"}]
    with pytest.raises(ValueError, match="different pattern or search settings"):
        parallel._load_state(  # noqa: SLF001
            state,
            {**binding, "pattern": ["cell-b"]},
        )


def test_state_resume_rejects_malformed_nodes_totals_and_queue_mass(tmp_path: Path) -> None:
    state = tmp_path / "state.json"
    binding = _binding()
    valid = parallel._state_document(  # noqa: SLF001
        binding=binding,
        queue=[_node()],
        nodes=11,
        closed_share=0.875,
        cpu_seconds=2.0,
        search_cpu_seconds=1.5,
        cpu_seconds_complete=True,
        wall_seconds=3.0,
        hit_floor=False,
        provenance=[{"git_revision": "old"}],
    )
    malformed = []
    wrong_dimensions = copy.deepcopy(valid)
    wrong_dimensions["queue"][0]["angles"] = []
    malformed.append((wrong_dimensions, "dimensions"))
    nonfinite_share = copy.deepcopy(valid)
    nonfinite_share["queue"][0]["share"] = "nan"
    malformed.append((nonfinite_share, "share must be finite"))
    negative_nodes = copy.deepcopy(valid)
    negative_nodes["nodes"] = -1
    malformed.append((negative_nodes, "nodes must be a nonnegative integer"))
    missing_mass = copy.deepcopy(valid)
    missing_mass["closed_tree_share"] = (0.0).hex()
    malformed.append((missing_mass, "do not account for the root"))
    incomplete_empty = copy.deepcopy(valid)
    incomplete_empty["queue"] = []
    malformed.append((incomplete_empty, "do not account for the root"))

    for document, message in malformed:
        parallel._atomic_json(state, document)  # noqa: SLF001
        with pytest.raises((TypeError, ValueError), match=message):
            parallel._load_state(state, binding)  # noqa: SLF001


def test_certificate_option_is_refused_before_native_loading(tmp_path: Path) -> None:
    with pytest.raises(SystemExit, match="refuses certificates"):
        parallel.main(
            [
                "--native-dir",
                str(tmp_path / "missing-native"),
                "--cells",
                "interior-SW",
                "--workers",
                "1",
                "--max-seconds",
                "1",
                "--state",
                str(tmp_path / "state.json"),
                "--output",
                str(tmp_path / "result.json"),
                "--certificate",
                str(tmp_path / "certificate"),
            ]
        )


@pytest.mark.parametrize(
    ("extra", "message"),
    [
        (["--max-seconds", "nan"], "must be positive"),
        (["--merge-gap", "0.1"], "requires --merge-gap 0"),
    ],
)
def test_invalid_settings_are_refused_before_native_loading(
    tmp_path: Path, extra: list[str], message: str
) -> None:
    arguments = [
        "--native-dir",
        str(tmp_path / "missing-native"),
        "--cells",
        "interior-SW",
        "--workers",
        "1",
        "--max-seconds",
        "1",
        "--state",
        str(tmp_path / "state.json"),
        "--output",
        str(tmp_path / "result.json"),
        *extra,
    ]

    with pytest.raises(SystemExit, match=message):
        parallel.main(arguments)
