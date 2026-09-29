#!/usr/bin/env python3
"""Clock a CI gate's hosted jobs against `devtools/gate-budgets.yaml`, as a tier is clocked.

`OR-17` exists because of a number nothing read. `deep-gate.yml` and
`test_deep_gate_workflow.py` price the exhaustive tier at 1943.05s -- the figure that
refused its promotion into `--fast` -- and on 2026-09-21 the job that runs it cost 2674s
on two complete runs of PR 208. That is 1.38x, under the 1.5x that fails a local tier,
and nobody saw it: `sqpack.gate_budgets` judges `packing-validate`'s own wall, and a
hosted job's wall was judged by nothing at all. A tier does not become unbounded by being
deferred.

So this is the same register and the same four rules, pointed at a workflow run instead
of a subprocess. It reads one run's jobs from the GitHub API and reports, per job:

* **the wall** the reviewer waits for, from the job starting to the job completing;
* **the queue** before it, which the gate's wall includes and the job's does not;
* **the split** of that wall into setup and work, by the same `setup_steps` patterns
  `check_pr_wall` classifies a pull-request job's steps with. This is what makes a
  verdict actionable rather than a complaint: on run 35579234418 `exhaustive-tier` spent
  22s of its 2674s on checkout and toolchain, so its gap against the declared step time
  is the step, not the runner.

Each wall then goes through `gate_budgets.judge_ci_job`, which is `judge`'s own
`band_findings` -- ceiling, drift, stale -- with the gate's declared `drift_ratio` in
place of the policy's. The gate's entry says what spread that band was chosen against.

**Reporting is the default and it is deliberate.** A gate declared `enforcement:
reporting` measures, diagnoses and prints every failure and still exits 0, because a
false red on a 45-minute pre-merge gate costs another 45 minutes to clear and teaches
people to stop reading it. `--enforce` is the switch, and the gate's `tracking_bead` is
the work that earns it.

From `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.check_ci_gate_walls \
        --gate deep-gate --run-id 35579234418

To record a baseline, measure several runs at once and paste the block it prints:
    ... check_ci_gate_walls --gate deep-gate --sample --recent 6
    ... check_ci_gate_walls --gate deep-gate --sample --run-id A --run-id B

In CI, the run and repository come from the environment:
    uv run --frozen --all-extras --group dev python -m devtools.check_ci_gate_walls \
        --gate deep-gate

`--dump` prints the trimmed API payload a verdict was computed from.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from devtools.check_pr_wall import (
    Client,
    WallError,
    WallPolicy,
    github_token,
    load_walls,
    trim,
)
from sqpack.gate_budgets import (
    BUDGETS,
    BudgetError,
    CiGate,
    Register,
    Verdict,
    ci_declaration_problems,
    judge_ci_job,
    load,
    render,
)


class GateWallError(Exception):
    """The API cannot supply what a verdict needs."""


RECENT_EVENTS: dict[str, tuple[str, ...]] = {
    "deep-gate": ("pull_request", "workflow_dispatch"),
    "post-merge": ("push", "schedule", "workflow_dispatch"),
}
RECENT_PAGE_SIZE = 30
RECENT_PAGE_LIMIT = 2
RECENT_CANDIDATE_LIMIT = 60
RECENT_SAMPLE_LIMIT = 20
RECENT_JOB_LIMIT = 100
HEAD_SHA = re.compile(r"[0-9a-f]{40}\Z")


@dataclass(frozen=True)
class JobWall:
    """One hosted job's wall, with the queue before it and its setup/work split."""

    name: str
    runner: str
    conclusion: str | None
    queue_seconds: float | None
    setup_seconds: float
    work_seconds: float
    wall_seconds: float | None
    steps: tuple[tuple[str, float], ...]

    @property
    def overhead_seconds(self) -> float | None:
        """Wall that is neither the work steps nor the queue: setup, teardown, finalise."""
        if self.wall_seconds is None:
            return None
        return self.wall_seconds - self.work_seconds


@dataclass(frozen=True)
class GateRun:
    """One workflow run of a gate: its jobs, and the wall a reviewer waited through."""

    run_id: int
    head_sha: str
    conclusion: str | None
    jobs: tuple[JobWall, ...]
    wall_seconds: float | None
    critical_job: str | None

    def job(self, name: str) -> JobWall | None:
        return next((job for job in self.jobs if job.name == name), None)


def _instant(value: object) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def _span(start: object, end: object) -> float | None:
    begun, finished = _instant(start), _instant(end)
    if begun is None or finished is None or finished < begun:
        return None
    return (finished - begun).total_seconds()


def _runner(job: dict[str, Any]) -> str:
    """The label the job asked for, which is the only shape the jobs API reports."""
    labels = [str(label) for label in job.get("labels") or []]
    return labels[0] if labels else "unknown"


def job_wall(job: dict[str, Any], policy: WallPolicy) -> JobWall:
    """One job's wall and its split, classified by the register's own setup patterns."""
    setup = work = 0.0
    steps: list[tuple[str, float]] = []
    for step in job.get("steps") or []:
        name = str(step.get("name", ""))
        seconds = _span(step.get("started_at"), step.get("completed_at")) or 0.0
        if policy.is_setup(name):
            setup += seconds
        else:
            work += seconds
            steps.append((name, seconds))
    return JobWall(
        name=str(job["name"]),
        runner=_runner(job),
        conclusion=job.get("conclusion"),
        queue_seconds=_span(job.get("created_at"), job.get("started_at")),
        setup_seconds=setup,
        work_seconds=work,
        wall_seconds=_span(job.get("started_at"), job.get("completed_at"))
        if job.get("status") == "completed"
        else None,
        steps=tuple(steps),
    )


def measure(
    run: dict[str, Any], jobs: Sequence[dict[str, Any]], gate: CiGate, policy: WallPolicy
) -> GateRun:
    """The gate's wall, from the run starting to its last gating job completing.

    The declared jobs define the endpoint. A workflow may contain another surface beside
    the gate -- `packing-validation` has both post-merge workers and macOS portability --
    and letting an unrelated job extend this wall would measure a different contract.
    The aggregate is retained in the table but excluded from the endpoint because it has
    no ceiling and runs only after every declared prerequisite.
    """
    counts = Counter(str(job.get("name", "")) for job in jobs)
    missing = [name for name in gate.ids if counts[name] == 0]
    duplicates = [name for name in gate.ids if counts[name] > 1]
    if missing or duplicates:
        details: list[str] = []
        if missing:
            details.append(f"missing declared jobs: {', '.join(missing)}")
        if duplicates:
            details.append(f"duplicate declared jobs: {', '.join(duplicates)}")
        raise GateWallError(
            f"run {run.get('id')} cannot measure {gate.id}: {'; '.join(details)}"
        )

    retained = [job for job in jobs if str(job.get("name", "")) in {*gate.ids, gate.aggregate}]
    walls = [job_wall(job, policy) for job in retained]
    gating = [job for job in walls if job.name in gate.ids]
    start = _instant(run.get("run_started_at") or run.get("created_at"))
    ends = [
        _instant(job.get("completed_at"))
        for job in retained
        if str(job.get("name", "")) in gate.ids and job.get("completed_at")
    ]
    finished = [end for end in ends if end is not None]
    complete = len(finished) == len(gate.ids) and all(
        job.wall_seconds is not None for job in gating
    )
    wall = (max(finished) - start).total_seconds() if start and complete else None
    endpoint = (
        max(
            (
                job
                for job in retained
                if str(job.get("name", "")) in gate.ids
                and _instant(job.get("completed_at")) is not None
            ),
            key=lambda job: (
                _instant(job.get("completed_at")) or datetime.min.replace(tzinfo=UTC)
            ),
            default=None,
        )
        if complete
        else None
    )
    return GateRun(
        run_id=int(run["id"]),
        head_sha=str(run.get("head_sha", ""))[:8],
        conclusion=run.get("conclusion"),
        jobs=tuple(walls),
        wall_seconds=wall,
        critical_job=str(endpoint["name"]) if endpoint is not None else None,
    )


def verdicts(
    register: Register, gate: CiGate, measured: GateRun, *, enforce: bool = False
) -> list[Verdict]:
    """One verdict per declared job, plus the gate's whole wall.

    Driven by the register rather than by the run, so a job that stopped reporting is a
    verdict saying its wall is unmeasurable rather than a silently missing row.
    """
    found: list[Verdict] = []
    for budget in gate.jobs:
        job = measured.job(budget.id)
        if job is None or job.wall_seconds is None:
            found.append(
                Verdict(
                    tier=budget.id,
                    wall_seconds=0.0,
                    status="unknown",
                    ceiling_seconds=budget.ceiling_seconds,
                    measured_seconds=budget.measured_seconds,
                    notes=(
                        (
                            f"run {measured.run_id} reports no finished {budget.id!r} "
                            "job, so its band was not applied"
                        ),
                    ),
                )
            )
            continue
        found.append(
            judge_ci_job(
                register,
                gate.id,
                budget.id,
                wall_seconds=job.wall_seconds,
                steps=job.steps,
                runner=job.runner,
                enforce=enforce,
            )
        )
    if measured.wall_seconds is not None:
        found.append(
            judge_ci_job(
                register,
                gate.id,
                "wall",
                wall_seconds=measured.wall_seconds,
                steps=tuple(
                    (job.name, job.wall_seconds)
                    for job in measured.jobs
                    if job.wall_seconds is not None
                ),
                runner=gate.reference.runner,
                enforce=enforce,
            )
        )
    else:
        found.append(
            Verdict(
                tier="wall",
                wall_seconds=0.0,
                status="unknown",
                ceiling_seconds=gate.wall.ceiling_seconds,
                measured_seconds=gate.wall.measured_seconds,
                notes=(
                    (
                        f"run {measured.run_id} has no complete declared-job inventory, "
                        "so its gate wall was not measured"
                    ),
                ),
            )
        )
    return found


def _seconds(value: float | None) -> str:
    return "  --  " if value is None else f"{value:6.0f}s"


def render_run(gate: CiGate, measured: GateRun, found: Sequence[Verdict]) -> list[str]:
    """The per-job table, then each verdict's own lines from `gate_budgets.render`."""
    headline = (
        f"== the {gate.id} gate on run {measured.run_id} ({measured.head_sha}, "
        f"{measured.conclusion}) =="
    )
    lines = [headline, f"{'job':24}{'wall':>8}{'queue':>8}{'setup':>8}{'work':>8}"]
    # Slowest first, because the top row is the one that set the gate's wall.
    lines.extend(
        f"{job.name:24}{_seconds(job.wall_seconds)}{_seconds(job.queue_seconds)}"
        f"{_seconds(job.setup_seconds)}{_seconds(job.work_seconds)}"
        for job in sorted(measured.jobs, key=lambda item: -(item.wall_seconds or 0.0))
    )
    lines.append(
        f"{'-- the gate wall':24}{_seconds(measured.wall_seconds)}"
        f"  run start to the last gating job, critical: {measured.critical_job}"
    )
    for verdict in found:
        lines.append(f"  {verdict.tier}:")
        lines.extend(f"  {line}" for line in render(verdict))
    if gate.reports_only:
        lines.append(
            f"  note: this gate reports rather than enforces under {gate.tracking_bead}"
        )
    return lines


def _geometric_mean(values: Sequence[float]) -> float:
    return math.exp(sum(math.log(value) for value in values) / len(values))


def render_sample(gate: CiGate, runs: Sequence[GateRun], *, today: str) -> list[str]:
    """The register block to paste, as the geometric mean of the readings and the spread.

    The mean rather than the maximum for the reason `policy.drift_ratio` gives: a record
    at the top of its band starves the stale rule by as much as it feeds the drift rule,
    and `D-472` is the entry. The spread is printed beside it because a hosted band has
    to be argued against the runner's own variance rather than a local tier's.
    """
    where = ", ".join(f"run {run.run_id} ({run.head_sha})" for run in runs)
    lines = [f"# {gate.id}: {len(runs)} readings, {where}"]
    for name in (*gate.ids, "wall"):
        present = [
            reading
            for reading in (_reading(run, name) for run in runs)
            if reading is not None and reading > 0
        ]
        if not present:
            lines.append(f"  {name}: no finished reading in these runs")
            continue
        mean = _geometric_mean(present)
        spread = max(present) / min(present)
        lines.extend(
            [
                f"- id: {name}",
                f"  measured_seconds: {mean:.1f}",
                f"  measured_on: {today}",
                f"  spread: {spread:.2f}",
                f"  # readings: {', '.join(f'{value:.0f}' for value in present)}",
            ]
        )
    return lines


def _reading(run: GateRun, name: str) -> float | None:
    """One run's wall for one declared name, where `wall` means the gate's own."""
    if name == "wall":
        return run.wall_seconds
    job = run.job(name)
    return job.wall_seconds if job else None


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Hold a CI gate's hosted jobs to the ceilings in gate-budgets.yaml."
    )
    parser.add_argument("--gate", default="deep-gate", help="the gate's id in the register")
    parser.add_argument("--run-id", type=int, action="append", default=[])
    parser.add_argument("--recent", type=int, help="sample this many recent runs")
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", "jlevy/squares"))
    parser.add_argument("--register", type=Path, default=BUDGETS)
    parser.add_argument("--sample", action="store_true", help="print a record from many runs")
    parser.add_argument("--dump", action="store_true", help="print the API payload read")
    parser.add_argument(
        "--enforce",
        action="store_true",
        help="fail on a band the register's `enforcement: reporting` would merely print",
    )
    return parser


def _candidate_time(run: dict[str, Any]) -> float:
    """A sortable run start, with malformed candidates placed last for rejection."""
    instant = _instant(run.get("created_at") or run.get("run_started_at"))
    if instant is None or instant.tzinfo is None:
        return float("-inf")
    return instant.timestamp()


def _recent_candidates(
    client: Client, gate: CiGate, events: Sequence[str]
) -> list[dict[str, Any]]:
    """Read a bounded window for every admitted event and merge it by global recency."""
    workflow = Path(gate.file).name
    by_id: dict[int, dict[str, Any]] = {}
    for event in events:
        for page_number in range(1, RECENT_PAGE_LIMIT + 1):
            payload = client.get(
                f"actions/workflows/{workflow}/runs?event={event}&status=success"
                f"&per_page={RECENT_PAGE_SIZE}&page={page_number}"
            )
            if not isinstance(payload, dict) or not isinstance(
                payload.get("workflow_runs"), list
            ):
                raise GateWallError(
                    f"GitHub returned a malformed recent-run page for {gate.id}/{event}"
                )
            page = payload["workflow_runs"]
            for candidate in page:
                if not isinstance(candidate, dict):
                    raise GateWallError(
                        f"GitHub returned a malformed recent run for {gate.id}/{event}"
                    )
                identifier = candidate.get("id")
                if type(identifier) is not int or identifier <= 0:
                    raise GateWallError(
                        f"GitHub returned a recent run without a positive integer id for "
                        f"{gate.id}/{event}"
                    )
                previous = by_id.get(identifier)
                if previous is None or _candidate_time(candidate) > _candidate_time(previous):
                    by_id[identifier] = candidate
            if len(page) < RECENT_PAGE_SIZE:
                break
    return sorted(by_id.values(), key=_candidate_time, reverse=True)[:RECENT_CANDIDATE_LIMIT]


def _candidate_jobs(client: Client, run_id: int) -> list[dict[str, Any]] | None:
    """Read one bounded job page; a larger inventory is incompatible with this gate."""
    payload = client.get(
        f"actions/runs/{run_id}/jobs?filter=latest&per_page={RECENT_JOB_LIMIT}&page=1"
    )
    if not isinstance(payload, dict):
        raise GateWallError(f"GitHub returned a malformed jobs page for run {run_id}")
    total = payload.get("total_count")
    jobs = payload.get("jobs")
    if type(total) is not int or total < 0 or not isinstance(jobs, list):
        raise GateWallError(f"GitHub returned a malformed jobs page for run {run_id}")
    if total > RECENT_JOB_LIMIT:
        return None
    if total != len(jobs) or any(not isinstance(job, dict) for job in jobs):
        raise GateWallError(f"GitHub returned an incomplete jobs page for run {run_id}")
    return jobs


def _compatible_recent_run(
    run: dict[str, Any], jobs: Sequence[dict[str, Any]], gate: CiGate, events: Sequence[str]
) -> bool:
    """Whether a successful run has the gate's current, complete job topology."""
    if (
        run.get("event") not in events
        or run.get("conclusion") != "success"
        or HEAD_SHA.fullmatch(str(run.get("head_sha", ""))) is None
        or _candidate_time(run) == float("-inf")
    ):
        return False
    names = Counter(str(job.get("name", "")) for job in jobs)
    required = (*gate.ids, gate.aggregate)
    if any(names[name] != 1 for name in required):
        return False
    selected = [job for job in jobs if str(job.get("name", "")) in required]
    return all(
        job.get("status") == "completed"
        and job.get("conclusion") == "success"
        and _span(job.get("started_at"), job.get("completed_at")) is not None
        for job in selected
    )


def _recent_payloads(
    client: Client, gate: CiGate, count: int
) -> list[tuple[dict[str, Any], list[dict[str, Any]]]]:
    """Find exactly ``count`` compatible readings inside a bounded discovery window."""
    if not 1 <= count <= RECENT_SAMPLE_LIMIT:
        raise GateWallError(
            f"--recent must be between 1 and {RECENT_SAMPLE_LIMIT}, got {count}"
        )
    events = RECENT_EVENTS.get(gate.id)
    if events is None:
        raise GateWallError(
            f"gate {gate.id!r} has no declared recent-run event surface; use --run-id"
        )
    accepted: list[tuple[dict[str, Any], list[dict[str, Any]]]] = []
    for run in _recent_candidates(client, gate, events):
        identifier = int(run["id"])
        jobs = _candidate_jobs(client, identifier)
        if jobs is not None and _compatible_recent_run(run, jobs, gate, events):
            accepted.append((run, jobs))
            if len(accepted) == count:
                return accepted
    named_events = ", ".join(events)
    raise GateWallError(
        f"requested {count} compatible recent {gate.id} runs, found {len(accepted)} "
        f"within the bounded {RECENT_CANDIDATE_LIMIT}-candidate window for "
        f"{named_events}; pass explicit --run-id values to inspect older runs"
    )


def _recent_run_ids(client: Client, gate: CiGate, count: int) -> list[int]:
    """Expose the admitted ids for focused discovery contracts."""
    return [int(run["id"]) for run, _jobs in _recent_payloads(client, gate, count)]


def _run_ids(arguments: argparse.Namespace, client: Client, gate: CiGate) -> list[int]:
    if arguments.run_id:
        return [int(value) for value in arguments.run_id]
    if arguments.recent is not None:
        return _recent_run_ids(client, gate, int(arguments.recent))
    live = os.environ.get("GITHUB_RUN_ID")
    if live:
        return [int(live)]
    raise GateWallError(
        "no run to measure: pass --run-id, or --recent N, or run inside a workflow"
    )


def _payloads(
    arguments: argparse.Namespace, client: Client, gate: CiGate
) -> list[tuple[dict[str, Any], list[dict[str, Any]]]]:
    """Fetch explicit/live runs normally, but reuse bounded recent-run admission bytes."""
    if arguments.run_id:
        identifiers = [int(value) for value in arguments.run_id]
    elif arguments.recent is not None:
        return _recent_payloads(client, gate, int(arguments.recent))
    else:
        identifiers = _run_ids(arguments, client, gate)
    return [(client.run(run_id), client.jobs(run_id)) for run_id in identifiers]


def _require_sample_payloads(
    payloads: Sequence[tuple[dict[str, Any], Sequence[dict[str, Any]]]], gate: CiGate
) -> None:
    """Refuse a pasteable baseline unless every supplied run matches the current gate."""
    events = RECENT_EVENTS.get(gate.id)
    if events is None:
        raise GateWallError(
            f"gate {gate.id!r} has no declared sample event surface; use ordinary --run-id"
        )
    for run, jobs in payloads:
        if not _compatible_recent_run(run, jobs, gate, events):
            raise GateWallError(
                f"run {run.get('id')} is not a complete successful {gate.id} reading "
                "at the current event and job topology"
            )


def _selected(arguments: argparse.Namespace) -> tuple[Register, CiGate]:
    """The register and the gate asked for, or the reason neither can be had."""
    try:
        register = load(arguments.register)
    except BudgetError as error:
        raise GateWallError(str(error)) from error
    gate = register.ci_gate(str(arguments.gate))
    if gate is None:
        known = ", ".join(entry.id for entry in register.ci_gates) or "none"
        raise GateWallError(f"no gate {arguments.gate!r} ({known})")
    return register, gate


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        register, gate = _selected(arguments)
    except GateWallError as error:
        print(f"check_ci_gate_walls: {error}", file=sys.stderr)
        return 2
    problems = ci_declaration_problems(register)
    for problem in problems:
        print(f"  DECLARATION: {problem}")
    client = Client(str(arguments.repo), github_token())
    try:
        policy = load_walls().policy
        payloads = _payloads(arguments, client, gate)
        if arguments.sample and not arguments.dump:
            _require_sample_payloads(payloads, gate)
        measured = (
            []
            if arguments.dump
            else [measure(run, jobs, gate, policy) for run, jobs in payloads]
        )
    except (GateWallError, WallError, OSError) as error:
        print(f"check_ci_gate_walls: {error}", file=sys.stderr)
        return 2
    if arguments.dump:
        for run, jobs in payloads:
            print(json.dumps(trim(run, jobs), indent=2))
        return 0
    if arguments.sample:
        today = datetime.now(UTC).date().isoformat()
        print("\n".join(render_sample(gate, measured, today=today)))
        return 0
    failed = False
    for run in measured:
        found = verdicts(register, gate, run, enforce=bool(arguments.enforce))
        print("\n".join(render_run(gate, run, found)))
        failed = failed or any(verdict.failed for verdict in found)
    if problems:
        return 2
    return 1 if failed and arguments.enforce else 0


if __name__ == "__main__":
    raise SystemExit(main())
