"""Reading a tier's cost out of a hosted job log, on a recorded excerpt of one.

A record in `gate-budgets.yaml` is a hosted reading, and for nine days the only way to
take one was to open a log and copy a number. Nobody did: `checks` and `sweeps` ran on
every pull request with `measured_seconds: null` from 2026-09-07 to 2026-09-15 while the
gate printed the line to write on every run. `devtools.read_tier_walls` is that reading as
a tool, and this is its parser held to the log it parses -- the `validate` job of run
34997018168, trimmed to the four things a reading is made of: the command, which names the
tier through the CLI's own parser; the step table; the verdict; and the step count that
says which tier the reading is of.
"""

# The hosted-job filter is part of the reader's trust boundary, so it is tested directly.
# ruff: noqa: SLF001
# pyright: reportPrivateUsage=false
from __future__ import annotations

import io
import math
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from typing import Any

import pytest

from devtools import read_tier_walls
from devtools.read_tier_walls import geometric_mean, growth, parse_log, same_shape, step_means
from sqpack import gate_budgets
from sqpack.cli import validate

EXCERPT = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "tier-walls"
    / "validate-34997018168-excerpt.log"
)


def excerpt() -> str:
    return EXCERPT.read_text(encoding="utf-8")


def budget_only_failure() -> str:
    return excerpt().replace(
        "49 of 74 STEPS PASSED (a named tier; this is not the full gate)",
        "THE TIER IS OUTSIDE ITS DECLARED COST BAND:\n"
        "  - the checks tier's recorded cost is stale\n"
        "49 of 74 STEPS PASSED (the budget verdict alone failed)",
    )


def advisory_verdict() -> str:
    """The excerpt as a run whose stale finding was advisory on a pull request."""
    return (
        excerpt()
        .replace(
            "note: no cost is recorded",
            "FAIL (advisory, not enforced): the checks tier ran 135.7s against a recorded "
            "250s, which is 0.54x. The record is stale in the flattering direction\n"
            "2026-09-15T16:48:26.9922197Z   enforcement: the drift and stale rules are "
            "advisory on pull requests under think-aaaa: a reason. Only the ceiling fails a "
            "pull-request run.\n"
            "2026-09-15T16:48:26.9922197Z   note: no cost is recorded",
        )
        .replace(
            "49 of 74 STEPS PASSED (a named tier; this is not the full gate)",
            "THE TIER IS OUTSIDE ITS RECORDED BAND (advisory, not enforced under think-aaaa):\n"
            "  - the checks tier ran 135.7s against a recorded 250s, which is 0.54x\n"
            "49 of 74 STEPS PASSED (a named tier; this is not the full gate)",
        )
    )


def test_the_closing_failure_class_leaves_a_budget_only_reading_readable(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The gate's own hosted rendering, annotations and failure class included, is still
    one budget-only reading of its tier at the reference shape."""
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(tmp_path / "summary.md"))
    summary = validate.RunSummary(
        results=[validate.StepResult("fast behavioral tests, shard A", "passed", 134.0)],
        wall_seconds=134.2,
        selected_count=1,
        total_count=98,
        budget=gate_budgets.Verdict(
            tier="suite_a",
            wall_seconds=134.2,
            status="failed",
            enforced=True,
            ceiling_seconds=131.0,
            measured_seconds=114.58,
            failures=("the suite_a tier ran 134.2s against a 131s ceiling",),
        ),
    )
    stdout = io.StringIO()
    with redirect_stdout(stdout), redirect_stderr(io.StringIO()):
        assert validate._render_text(summary, strict=False) == 1
    log = (
        "##[group]Run uv run --frozen --all-extras --group dev "
        "packing-validate --suite-a --jobs 1 --inner-jobs 1\n" + stdout.getvalue()
    )

    (reading,) = parse_log(log)

    assert (reading.tier, reading.wall_seconds, reading.steps) == ("suite_a", 134.2, "1 of 98")
    assert reading.enforced
    assert reading.budget_only_failure
    assert "FAILURE CLASS: budget verdict alone failed" in log


def test_an_advisory_finding_is_still_a_reading_at_the_reference_shape() -> None:
    """A run whose drift or stale finding was advisory passed at the reference shape, so
    its wall is a reading the mean counts: the band was enforced and the run was judged,
    only the relative verdict was not what failed it."""
    (reading,) = parse_log(advisory_verdict())
    assert reading.enforced
    assert not reading.budget_only_failure
    assert reading.wall_seconds == 135.71


def test_the_tier_and_its_wall_are_read_from_the_log() -> None:
    """The tier comes from the command, not from the job's name.

    A job name is a label someone chose; the command is what ran. `validate` runs
    `--checks`, and the two have never been the same word.
    """
    (reading,) = parse_log(excerpt())
    assert reading.tier == "checks"
    assert reading.wall_seconds == 135.71
    assert reading.enforced
    assert reading.steps == "49 of 74"


def test_a_budget_only_failed_job_remains_a_tier_reading(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Client:
        def jobs(self, _run_id: int) -> list[dict[str, Any]]:
            return [
                {
                    "id": 123,
                    "name": "validate",
                    "status": "completed",
                    "conclusion": "failure",
                }
            ]

    monkeypatch.setattr(read_tier_walls, "_log", lambda _client, _job: budget_only_failure())

    (reading,) = read_tier_walls._collect(Client(), [456], [])  # type: ignore[arg-type]

    assert reading.run == 456
    assert reading.steps == "49 of 74"
    assert reading.budget_only_failure


def test_a_job_read_by_id_carries_its_run_and_attempt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`--job-id` reaches an attempt the latest-attempt view hides, and names it.

    The two readings that failed PR #277 on the ceiling (131.58 s and 132.67 s, run
    36928600491 attempts 1 and 4) sat behind three re-runs; the jobs API answers for a
    job id with its run and attempt, which is what `measured_where` needs to cite it.
    """

    class Client:
        def get(self, path: str) -> dict[str, Any]:
            assert path == "actions/jobs/123"
            return {
                "id": 123,
                "run_id": 456,
                "run_attempt": 2,
                "name": "suite-a",
                "status": "completed",
                "conclusion": "failure",
            }

    monkeypatch.setattr(read_tier_walls, "_log", lambda _client, _job: budget_only_failure())

    (reading,) = read_tier_walls._collect_jobs(Client(), [123], ["checks"])  # type: ignore[arg-type]

    assert (reading.run, reading.attempt, reading.job) == (456, 2, "suite-a")
    assert reading.budget_only_failure
    assert read_tier_walls._collect_jobs(Client(), [123], ["sweeps"]) == []  # type: ignore[arg-type]


def test_an_ordinary_failed_job_is_not_a_tier_reading(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Client:
        def jobs(self, _run_id: int) -> list[dict[str, Any]]:
            return [
                {
                    "id": 123,
                    "name": "validate",
                    "status": "completed",
                    "conclusion": "failure",
                }
            ]

    monkeypatch.setattr(read_tier_walls, "_log", lambda _client, _job: excerpt())

    assert read_tier_walls._collect(Client(), [456], []) == []  # type: ignore[arg-type]


def test_a_reading_off_the_reference_shape_is_not_counted() -> None:
    """The gate itself says when it did not enforce a band, and a mean must respect that.

    Wall time is not comparable across shapes, so a reading the gate reported rather than
    enforced is listed for the reader and left out of the record.
    """
    reported = excerpt().replace(
        "note: no cost is recorded",
        "note: within the declared band, but this run's shape (2 cpus, 2 jobs, 1 inner) is "
        "not the checks tier's reference (4 cpus, --jobs 3 --inner-jobs 1), so the band was "
        "reported and not enforced\n2026-09-15T16:48:26.9922197Z   note: no cost is recorded",
    )
    (reading,) = parse_log(reported)
    assert not reading.enforced


def test_a_scoped_command_is_not_a_tier_reading() -> None:
    """`--only` selects a slice, and a slice has no declared cost (`D-466`)."""
    scoped = excerpt().replace(
        "packing-validate --checks --jobs 3", 'packing-validate --only "lint floor" --jobs 3'
    )
    assert parse_log(scoped) == []


def test_a_removed_tier_syntax_does_not_abort_a_multi_job_log() -> None:
    """Historical suite commands may share a run with current tiers worth reading."""
    obsolete = excerpt().replace("packing-validate --checks", "packing-validate --suite")
    assert parse_log(obsolete) == []


def test_the_step_table_is_read_for_attribution() -> None:
    """A raised record must name what grew, and this is where those numbers come from."""
    (reading,) = parse_log(excerpt())
    assert reading.step_seconds["exact verification"] == 116.00
    assert reading.step_seconds["type floor (basedpyright)"] == 79.22
    assert "TOTAL (wall)" not in reading.step_seconds
    assert len(reading.step_seconds) == 8


def test_growth_pairs_two_groups_of_readings_by_step() -> None:
    """A step outside a run's eight slowest reads as zero there, which bounds it.

    The log prints the eight slowest steps, so a step that was cheap before and dear now
    shows its whole cost as growth, and one that was dear before and cheap now shows its
    whole cost as a fall. That is the right direction to be wrong in for a rule that asks
    what grew, and the tool says so where it prints the table.
    """
    (before,) = parse_log(excerpt())
    (after,) = parse_log(
        excerpt().replace("116.00s  exact verification", "150.00s  exact verification")
    )
    rows = growth([before], [after])
    name, was, now = rows[0]
    assert name == "exact verification"
    assert (was, now) == pytest.approx((116.00, 150.00))
    assert all(earlier == pytest.approx(later) for _, earlier, later in rows[1:])


def test_a_mean_over_readings_is_geometric_and_per_step() -> None:
    """The register's convention: the centre of the band, not one reading and not a max."""
    (one,) = parse_log(excerpt())
    (two,) = parse_log(excerpt().replace("135.71s", "271.42s"))
    assert two.wall_seconds == 271.42
    assert math.isclose(
        geometric_mean([one.wall_seconds, two.wall_seconds]), math.sqrt(135.71 * 271.42)
    )
    means = step_means([one, two])
    assert means["exact verification"] == pytest.approx(116.00)


def test_baseline_attribution_uses_only_the_same_selected_step_shape() -> None:
    """A tier name is not a comparable baseline when the tier selected different work."""
    (matching,) = parse_log(excerpt())
    (different_shape,) = parse_log(excerpt().replace("49 of 74 STEPS", "50 of 75 STEPS"))
    (different_tier,) = parse_log(
        excerpt().replace("packing-validate --checks", "packing-validate --typecheck")
    )
    selected = same_shape(
        [matching, different_shape, different_tier], tier="checks", steps="49 of 74"
    )
    assert selected == [matching]
