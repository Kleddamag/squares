"""Recent CI-wall samples are bounded and match each gate's current event surface."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import argparse
from datetime import UTC, datetime, timedelta
from typing import Any, cast
from urllib.parse import parse_qs, urlsplit

import pytest

from devtools.check_ci_gate_walls import (
    GateWallError,
    _payloads,
    _require_sample_payloads,
    _run_ids,
)
from devtools.check_pr_wall import Client
from sqpack.gate_budgets import BUDGETS, CiGate, load


class _FakeClient:
    def __init__(
        self,
        pages: dict[tuple[str, int], list[dict[str, Any]]],
        jobs: dict[int, list[dict[str, Any]]],
    ) -> None:
        self.pages = pages
        self.jobs = jobs
        self.requests: list[str] = []

    def get(self, path: str) -> object:
        self.requests.append(path)
        query = parse_qs(urlsplit(path).query)
        if "/jobs?" in path:
            run_id = int(path.split("/runs/", 1)[1].split("/", 1)[0])
            selected = self.jobs[run_id]
            return {"total_count": len(selected), "jobs": selected}
        event = query["event"][0]
        page = int(query["page"][0])
        return {"workflow_runs": self.pages.get((event, page), [])}


def _gate(name: str) -> CiGate:
    gate = load(BUDGETS).ci_gate(name)
    assert gate is not None
    return gate


def _run(
    run_id: int,
    event: str,
    started_at: str,
    *,
    head_sha: str = "a" * 40,
) -> dict[str, Any]:
    return {
        "id": run_id,
        "event": event,
        "conclusion": "success",
        "head_sha": head_sha,
        "created_at": started_at,
        "run_started_at": started_at,
    }


def _jobs(gate: CiGate) -> list[dict[str, Any]]:
    return [
        {
            "name": name,
            "status": "completed",
            "conclusion": "success",
            "started_at": "2026-09-29T20:00:00+00:00",
            "completed_at": "2026-09-29T20:01:00+00:00",
        }
        for name in (*gate.ids, gate.aggregate)
    ]


def _arguments(*, recent: int | None, run_ids: list[int] | None = None) -> argparse.Namespace:
    return argparse.Namespace(run_id=run_ids or [], recent=recent)


def _as_client(fake: _FakeClient) -> Client:
    return cast(Client, fake)


def test_post_merge_recent_runs_merge_events_by_recency_and_reject_old_topology() -> None:
    gate = _gate("post-merge")
    valid_older = _run(101, "push", "2026-09-29T20:01:00+00:00")
    stale_newest = _run(102, "schedule", "2026-09-29T20:03:00+00:00")
    valid_newer = _run(103, "workflow_dispatch", "2026-09-29T20:02:00+00:00")
    duplicate_older = dict(valid_older, run_started_at="2026-09-29T19:59:00+00:00")
    pages = {
        ("push", 1): [valid_older],
        ("schedule", 1): [stale_newest],
        ("workflow_dispatch", 1): [valid_newer, duplicate_older],
    }
    jobs = {101: _jobs(gate), 102: _jobs(gate)[:-1], 103: _jobs(gate)}
    client = _FakeClient(pages, jobs)

    payloads = _payloads(_arguments(recent=2), _as_client(client), gate)
    found = [int(run["id"]) for run, _jobs_payload in payloads]

    assert found == [103, 101]
    listing = [request for request in client.requests if "/workflows/" in request]
    assert {parse_qs(urlsplit(request).query)["event"][0] for request in listing} == {
        "push",
        "schedule",
        "workflow_dispatch",
    }
    assert all("event=pull_request" not in request for request in listing)
    assert all(
        request.startswith("actions/workflows/") or "/jobs?" in request
        for request in client.requests
    )


def test_deep_gate_recent_runs_use_only_pr_and_dispatch_and_require_successful_jobs() -> None:
    gate = _gate("deep-gate")
    skipped = _run(201, "pull_request", "2026-09-29T20:02:00+00:00")
    valid = _run(202, "workflow_dispatch", "2026-09-29T20:01:00+00:00")
    skipped_jobs = _jobs(gate)
    skipped_jobs[0] = dict(skipped_jobs[0], conclusion="skipped")
    client = _FakeClient(
        {
            ("pull_request", 1): [skipped],
            ("workflow_dispatch", 1): [valid],
        },
        {201: skipped_jobs, 202: _jobs(gate)},
    )

    found = _run_ids(_arguments(recent=1), _as_client(client), gate)

    assert found == [202]
    listing = [request for request in client.requests if "/workflows/" in request]
    assert {parse_qs(urlsplit(request).query)["event"][0] for request in listing} == {
        "pull_request",
        "workflow_dispatch",
    }
    assert all(
        "event=push" not in request and "event=schedule" not in request for request in listing
    )


def test_recent_sampling_refuses_to_return_a_smaller_compatible_sample() -> None:
    gate = _gate("post-merge")
    valid = _run(301, "push", "2026-09-29T20:01:00+00:00")
    client = _FakeClient({("push", 1): [valid]}, {301: _jobs(gate)})

    with pytest.raises(
        GateWallError,
        match=r"requested 2 compatible.*found 1.*explicit --run-id",
    ):
        _run_ids(_arguments(recent=2), _as_client(client), gate)


def test_recent_sampling_rejects_malformed_identity_and_timestamps() -> None:
    gate = _gate("post-merge")
    bad_run_time = _run(311, "push", "not-a-timestamp")
    bad_head = _run(
        312,
        "schedule",
        "2026-09-29T20:02:00+00:00",
        head_sha="A" * 40,
    )
    bad_job_time = _run(313, "workflow_dispatch", "2026-09-29T20:01:00+00:00")
    malformed_jobs = _jobs(gate)
    malformed_jobs[0] = dict(malformed_jobs[0], completed_at="not-a-timestamp")
    client = _FakeClient(
        {
            ("push", 1): [bad_run_time],
            ("schedule", 1): [bad_head],
            ("workflow_dispatch", 1): [bad_job_time],
        },
        {311: _jobs(gate), 312: _jobs(gate), 313: malformed_jobs},
    )

    with pytest.raises(GateWallError, match=r"requested 1 compatible.*found 0"):
        _run_ids(_arguments(recent=1), _as_client(client), gate)


def test_recent_sampling_bounds_pages_candidates_and_job_inventory_reads() -> None:
    gate = _gate("post-merge")
    pages: dict[tuple[str, int], list[dict[str, Any]]] = {}
    jobs: dict[int, list[dict[str, Any]]] = {}
    origin = datetime(2026, 9, 29, 20, tzinfo=UTC)
    run_id = 400
    for event in ("push", "schedule", "workflow_dispatch"):
        for page in (1, 2):
            candidates: list[dict[str, Any]] = []
            for _ in range(30):
                run_id += 1
                candidates.append(_run(run_id, event, origin.isoformat()))
                jobs[run_id] = []
                origin -= timedelta(seconds=1)
            pages[(event, page)] = candidates
    client = _FakeClient(pages, jobs)

    with pytest.raises(GateWallError, match=r"bounded 60-candidate window"):
        _run_ids(_arguments(recent=1), _as_client(client), gate)

    listing = [request for request in client.requests if "/workflows/" in request]
    inventories = [request for request in client.requests if "/jobs?" in request]
    assert len(listing) == 6
    assert len(inventories) == 60
    assert all(int(parse_qs(urlsplit(request).query)["page"][0]) <= 2 for request in listing)
    assert all("per_page=30" in request for request in listing)
    assert all("per_page=100&page=1" in request for request in inventories)


@pytest.mark.parametrize("count", [0, -1, 21])
def test_recent_sampling_refuses_invalid_counts_before_any_api_read(count: int) -> None:
    client = _FakeClient({}, {})

    with pytest.raises(GateWallError, match="--recent must be between 1 and 20"):
        _run_ids(_arguments(recent=count), _as_client(client), _gate("deep-gate"))

    assert client.requests == []


def test_explicit_run_ids_bypass_recent_discovery_and_admission() -> None:
    client = _FakeClient({}, {})

    found = _run_ids(
        _arguments(recent=-1, run_ids=[17, 12]),
        _as_client(client),
        _gate("post-merge"),
    )

    assert found == [17, 12]
    assert client.requests == []


def test_pasteable_explicit_sample_requires_current_successful_topology() -> None:
    gate = _gate("post-merge")
    run = _run(501, "push", "2026-09-29T20:01:00+00:00")
    jobs = _jobs(gate)

    _require_sample_payloads([(run, jobs)], gate)

    jobs[-1] = dict(jobs[-1], conclusion="skipped")
    with pytest.raises(GateWallError, match="not a complete successful post-merge reading"):
        _require_sample_payloads([(run, jobs)], gate)
