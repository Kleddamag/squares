#!/usr/bin/env python3
"""Decide whether a run GitHub starved of hosted runners gets one automatic re-run.

GitHub cancels a queued job it could not hand to a hosted runner, with the annotation
"The job was not acquired by Runner of type hosted even after multiple attempts". The job
has no runner and no steps, and the run goes on without it. `packing-required` and
`pages-required` then fail on that job's `cancelled` result, which is right -- a required
check must not go green on work that never ran -- but the pull request reads red with no
test failed. On 2026-10-05 from about 19:17 UTC, 96 jobs were cancelled this way after 15
to 35 minutes queued (run 37362926042 is the example), and the hand re-runs that followed
were themselves cancelled by the next push.

`.github/workflows/rerun-starved.yml` listens for a completed run of the two gating
workflows and asks this module whether to re-run that run's failed jobs, which include
the cancelled ones, exactly once. Every condition must hold:

* the run was triggered by `pull_request` or `push`;
* it completed with conclusion `failure`;
* it is the run's first attempt, so a re-run is never re-run;
* at least one job was cancelled with an empty or null `runner_name`;
* no newer run of the same workflow exists for the same commit, nor for the same branch
  and event. A re-run joins the run's concurrency group, so re-running an older run on
  a pull request would cancel the newer push's run in progress.

The decision is a pure function of the API's JSON, so the tests drive it with recorded
payloads. The workflow reads the payloads with `gh api` and acts on the answer; nothing
here touches the network.

Usage, in the workflow (the files come from `gh api`, one job or run per line):
    uv run --no-project --python 3.14.7 python packing/devtools/rerun_starved.py \
        --run run.json --jobs jobs.jsonl --runs runs.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

#: The workflows the listener subscribes to, by their `name:`.
WORKFLOWS = ("Packing validation", "Certificate page")
#: The events whose runs gate a pull request or `main`. A dispatch or a schedule is
#: re-run by whoever asked for it.
EVENTS = ("pull_request", "push")


class RerunError(Exception):
    """A payload is missing what the decision reads."""


@dataclass(frozen=True)
class Condition:
    """One rule of the decision, whether it held, and what it was decided from."""

    rule: str
    holds: bool
    detail: str


@dataclass(frozen=True)
class Decision:
    run_id: int
    rerun: bool
    starved: tuple[str, ...]
    conditions: tuple[Condition, ...]


def never_acquired_a_runner(job: Mapping[str, Any]) -> bool:
    """A job GitHub cancelled before any runner took it."""
    return job.get("conclusion") == "cancelled" and not job.get("runner_name")


def _integer(run: Mapping[str, Any], key: str) -> int:
    value = run.get(key)
    if not isinstance(value, int) or isinstance(value, bool):
        raise RerunError(f"run {run.get('id')!r} has no integer `{key}`: {value!r}")
    return value


def _text(run: Mapping[str, Any], key: str) -> str:
    value = run.get(key)
    if not isinstance(value, str) or not value:
        raise RerunError(f"run {run.get('id')!r} has no `{key}`: {value!r}")
    return value


def _newer(candidate: Mapping[str, Any], run: Mapping[str, Any]) -> bool:
    """Whether `candidate` was created after `run`; the run id breaks a tie in seconds."""
    created, mine = str(candidate.get("created_at", "")), str(run["created_at"])
    return created > mine or (created == mine and int(candidate.get("id", 0)) > run["id"])


def newer_runs(run: Mapping[str, Any], runs: Sequence[Mapping[str, Any]]) -> tuple[int, ...]:
    """Runs of the same workflow, created later, for this commit or this branch and event."""
    return tuple(
        sorted(
            {
                int(other["id"])
                for other in runs
                if other.get("id") != run["id"]
                and other.get("path") == run["path"]
                and _newer(other, run)
                and (
                    other.get("head_sha") == run["head_sha"]
                    or (
                        other.get("head_branch") == run["head_branch"]
                        and other.get("event") == run["event"]
                    )
                )
            }
        )
    )


def decide(
    run: Mapping[str, Any],
    jobs: Sequence[Mapping[str, Any]],
    runs: Sequence[Mapping[str, Any]],
) -> Decision:
    """Whether to re-run `run`'s failed jobs once, with every condition and its evidence.

    `jobs` is the first attempt's job list and `runs` the workflow's runs for the same
    commit and branch, which may include `run` itself.
    """
    run_id = _integer(run, "id")
    for key in ("name", "path", "event", "status", "created_at", "head_sha", "head_branch"):
        _text(run, key)
    attempt = _integer(run, "run_attempt")
    starved = tuple(str(job.get("name")) for job in jobs if never_acquired_a_runner(job))
    newer = newer_runs(run, runs)
    conclusion = run.get("conclusion")
    conditions = (
        Condition(
            "the run belongs to a workflow this listener re-runs",
            run["name"] in WORKFLOWS,
            f"`{run['name']}`",
        ),
        Condition(
            "the run was triggered by a pull request or a push",
            run["event"] in EVENTS,
            f"event `{run['event']}`",
        ),
        Condition(
            "the run completed and failed",
            run["status"] == "completed" and conclusion == "failure",
            f"status `{run['status']}`, conclusion `{conclusion}`",
        ),
        Condition(
            "this is the run's first attempt",
            attempt == 1,
            f"attempt {attempt}",
        ),
        Condition(
            "a job was cancelled without ever acquiring a runner",
            bool(starved),
            ", ".join(f"`{name}`" for name in starved) or "none",
        ),
        Condition(
            "no newer run of this workflow exists for this commit or this branch",
            not newer,
            ", ".join(str(other) for other in newer) or "none",
        ),
    )
    return Decision(
        run_id=run_id,
        rerun=all(condition.holds for condition in conditions),
        starved=starved,
        conditions=conditions,
    )


def render(decision: Decision) -> list[str]:
    """The decision as log lines: the verdict, then every condition."""
    verdict = "re-run its failed jobs once" if decision.rerun else "no re-run"
    lines = [f"run {decision.run_id}: {verdict}"]
    lines.extend(
        f"  {'holds' if condition.holds else 'FAILS'}: {condition.rule} ({condition.detail})"
        for condition in decision.conditions
    )
    return lines


def summary_markdown(decision: Decision) -> str:
    """The same decision, for `$GITHUB_STEP_SUMMARY`."""
    heading = "re-running the failed jobs once" if decision.rerun else "not re-running"
    rows = [
        f"### Starved run {decision.run_id}: {heading}",
        "",
        "| Condition | Holds | From |",
        "| --- | --- | --- |",
    ]
    rows.extend(
        f"| {condition.rule} | {'yes' if condition.holds else '**no**'} | {condition.detail} |"
        for condition in decision.conditions
    )
    return "\n".join(rows) + "\n"


def _object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RerunError(f"{path} is not readable JSON: {error}") from error
    if not isinstance(value, dict):
        raise RerunError(f"{path} must hold one JSON object")
    return value


def _lines(path: Path) -> list[dict[str, Any]]:
    """One JSON object per line, which is what `gh api --jq '.jobs[]'` writes."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        raise RerunError(f"{path} is unreadable: {error}") from error
    found: list[dict[str, Any]] = []
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            raise RerunError(f"{path}:{number} is not JSON: {error}") from error
        if not isinstance(value, dict):
            raise RerunError(f"{path}:{number} must be a JSON object")
        found.append(value)
    return found


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Decide whether a run starved of hosted runners is re-run once."
    )
    parser.add_argument("--run", type=Path, required=True, help="the run, as JSON")
    parser.add_argument("--jobs", type=Path, required=True, help="its jobs, one per line")
    parser.add_argument("--runs", type=Path, required=True, help="related runs, one per line")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        decision = decide(
            _object(arguments.run), _lines(arguments.jobs), _lines(arguments.runs)
        )
    except RerunError as error:
        print(f"rerun_starved: {error}", file=sys.stderr)
        return 2
    print("\n".join(render(decision)))
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with Path(output).open("a", encoding="utf-8") as handle:
            handle.write(f"rerun={'true' if decision.rerun else 'false'}\n")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with Path(summary).open("a", encoding="utf-8") as handle:
            handle.write(summary_markdown(decision))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
