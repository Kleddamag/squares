"""The notable-sources registry stays joined to the frontier's sources and the archive.

`devtools.check_notable_sources` refuses a reviewed frontier source that no entry covers
or two do, a credit key that resolves nowhere, a credit written twice, a retained copy that
is missing, and a summary that states a bound. Each refusal is exercised here on a small
synthetic registry, and the committed registry is held to all of them.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from devtools import check_notable_sources as check

COVERAGE = [
    {"id": "alpha-2026", "source_key": "[Alpha 2026]"},
    {"id": "beta-2026", "source_key": "[Beta 2026]"},
]
BIBLIOGRAPHY = ["[Alpha 2026]"]
ARCHIVE = ["[Beta 2026]", "[Gamma site]"]


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    web = tmp_path / "packing" / "resources" / "web"
    (web / "alpha").mkdir(parents=True)
    (web / "gamma.md").write_text("# Gamma\n", encoding="utf-8")
    return tmp_path


def _entry(**changes: Any) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "id": "alpha",
        "title": "alpha",
        "kind": "repository",
        "url": "https://example.org/alpha",
        "keys": ["[Alpha 2026]", "[Beta 2026]"],
        "retained": "packing/resources/web/alpha/",
        "coverage": ["alpha-2026", "beta-2026"],
        "summary": "Alpha's certificates for seventeen squares, with their checkers.",
    }
    entry.update(changes)
    return {key: value for key, value in entry.items() if value is not None}


def _site(**changes: Any) -> dict[str, Any]:
    site: dict[str, Any] = {
        "id": "gamma",
        "kind": "website",
        "keys": ["[Gamma site]"],
        "credit": "Gamma",
        "retained": "packing/resources/web/gamma.md",
        "coverage": None,
        "summary": "Gamma's page on packing unit squares in squares.",
    }
    return _entry(**{**site, **changes})


def _problems(registry: list[dict[str, Any]], repo: Path) -> list[str]:
    return check.problems(registry, COVERAGE, BIBLIOGRAPHY, ARCHIVE, repo)


def test_the_committed_registry_is_joined_to_its_records() -> None:
    assert check.main() == 0


def test_a_well_formed_registry_passes(repo: Path) -> None:
    assert _problems([_entry(), _site()], repo) == []


def test_a_reviewed_frontier_source_on_no_card_is_refused(repo: Path) -> None:
    """The failure the registry exists to prevent: a reviewed source dropping off the page."""
    dropped = _entry(coverage=["alpha-2026"], keys=["[Alpha 2026]"])
    assert _problems([dropped, _site()], repo) == [
        "beta-2026: a reviewed frontier source that no entry covers"
    ]


def test_a_reviewed_frontier_source_on_two_cards_is_refused(repo: Path) -> None:
    twice = _site(keys=["[Gamma site]", "[Beta 2026]"], coverage=["beta-2026"])
    assert _problems([_entry(), twice], repo) == [
        "beta-2026: covered by 2 entries: alpha, gamma"
    ]


def test_a_coverage_id_the_frontier_does_not_record_is_refused(repo: Path) -> None:
    unknown = _entry(coverage=["alpha-2026", "beta-2026", "delta-2026"])
    assert _problems([unknown, _site()], repo) == [
        "alpha: covers delta-2026, which source-coverage.yaml lacks"
    ]


def test_a_covered_source_s_own_key_is_among_the_entry_s_keys(repo: Path) -> None:
    assert _problems([_entry(keys=["[Alpha 2026]"]), _site()], repo) == [
        "alpha: covers beta-2026 but not its key [Beta 2026]"
    ]


def test_a_credit_key_that_resolves_nowhere_is_refused(repo: Path) -> None:
    """A key resolves in the bibliography or, failing that, in the archive index."""
    assert _problems([_entry(), _site(keys=["[Gamma site]", "[Nowhere]"])], repo) == [
        "gamma: [Nowhere] resolves nowhere"
    ]


def test_a_credit_is_read_from_the_bibliography_never_written_again(repo: Path) -> None:
    assert _problems([_entry(credit="Alpha"), _site()], repo) == [
        (
            "alpha: states a credit although [Alpha 2026] is in the bibliography, whose "
            "credit the card prints"
        )
    ]


def test_a_source_the_bibliography_does_not_carry_states_its_credit(repo: Path) -> None:
    assert _problems([_entry(), _site(credit=None)], repo) == [
        "gamma: no key is in the bibliography, so it states its credit"
    ]


@pytest.mark.parametrize(
    ("retained", "problem"),
    [
        (
            "packing/resources/web/missing/",
            "packing/resources/web/missing/ is not a retained directory",
        ),
        (
            "packing/resources/web/missing.md",
            "packing/resources/web/missing.md is not a retained file",
        ),
        (
            "packing/resources/web/alpha",
            "packing/resources/web/alpha is a directory, written without its trailing slash",
        ),
        (
            "packing/resources/web/gamma.md/",
            "packing/resources/web/gamma.md/ is not a retained directory",
        ),
    ],
)
def test_a_retained_copy_that_is_not_there_is_refused(
    repo: Path, retained: str, problem: str
) -> None:
    assert _problems([_entry(retained=retained), _site()], repo) == [f"alpha: {problem}"]


@pytest.mark.parametrize(
    ("summary", "issue"),
    [
        ("Alpha's proof that s(17) is large.", "names s(n) ('s(')"),
        ("Alpha's bound, at least 4.66 for seventeen squares.", "states a value ('4.66')"),
        ("Alpha's bound at 31/8 for eleven squares.", "states a value ('31/8')"),
        ("Alpha's certificate, which is ≥ the grid.", "states a relation ('≥')"),
        ("Alpha's certificates. They are exact.", "is more than one sentence"),
        ("Alpha's certificates", "does not end as a sentence"),
    ],
)
def test_a_summary_is_one_sentence_that_states_no_bound(
    repo: Path, summary: str, issue: str
) -> None:
    assert _problems([_entry(summary=summary), _site()], repo) == [
        f"alpha: its summary {issue}"
    ]


def test_a_summary_may_name_counts_and_years() -> None:
    """Integers are not bounds: `29 unit squares` and `the 2009 edition` are descriptions."""
    assert check.summary_problems("The 2009 edition, with packings of 29 unit squares.") == []


def test_the_archive_index_defines_its_keys_in_bold() -> None:
    text = "| **[Gamma site]** | a page |\n- **[Delta]** and [Not defined]\n"
    assert check.archive_keys(text) == frozenset({"[Gamma site]", "[Delta]"})
