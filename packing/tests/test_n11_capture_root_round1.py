"""Focused refusal controls for the conditional round-one owner join."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q

import pytest

from devtools import check_n11_capture_root_round1 as round1
from devtools import check_n11_optimality_field_mask0 as geometry


def test_compression_rechecks_nonnegative_weights() -> None:
    prior = [(Q(), Q()), (Q(1), Q()), (Q(1), Q(1)), (Q(), Q(1))]
    encoded = [[str(x), str(y)] for x, y in prior]
    base = {
        "compression_source_hull": encoded,
        "inner_grid_compression": {
            "denominator": 1,
            "directions": 16,
            "vertices": [["0", "0"]],
            "witnesses": [{"point": ["0", "0"], "indices": [0], "weights": ["1"]}],
        },
    }
    assert round1.compressed_points(base, prior, []) == [(Q(), Q())]
    bad = {
        **base,
        "inner_grid_compression": {
            **base["inner_grid_compression"],
            "witnesses": [{"point": ["0", "0"], "indices": [0], "weights": ["-1"]}],
        },
    }
    with pytest.raises(ValueError, match="invalid compression weights"):
        round1.compressed_points(bad, prior, [])


def test_join_requires_every_owner_and_distinguishes_resource_stop() -> None:
    with pytest.raises(geometry.IncompleteError, match="incomplete"):
        round1.require_complete_owner_results({})
    results = {
        owner: {"status": "PASS_CONDITIONAL_OWNER_UPDATE"} for owner in round1.pilot.MASK
    }
    round1.require_complete_owner_results(results)
    results[2] = {"status": "INCOMPLETE"}
    with pytest.raises(geometry.IncompleteError, match="incomplete"):
        round1.require_complete_owner_results(results)
    results[2] = {"status": "REFUSED"}
    with pytest.raises(ValueError, match="refused"):
        round1.require_complete_owner_results(results)


def test_worker_refuses_stale_prior_before_geometry(tmp_path) -> None:
    source = tmp_path / "round.json"
    prior = tmp_path / "prior.json"
    output = tmp_path / "worker.json"
    state = [[] for _ in range(16)]
    source.write_text(json.dumps({"round": {"index": 1, "prior_owned_points": state}}))
    stale = [[["0", "0"]] if owner == 0 else [] for owner in range(16)]
    prior.write_text(json.dumps(stale))
    args = argparse.Namespace(
        owner=2,
        max_owner_seconds=1,
        round_source=source,
        round_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        prior_state=prior,
        prior_sha256=hashlib.sha256(prior.read_bytes()).hexdigest(),
        max_events=100,
        worker_output=output,
    )
    assert round1.worker(args) == 2
    result = json.loads(output.read_text())
    assert result["status"] == "REFUSED"
    assert result["error"] == "source prior differs"
