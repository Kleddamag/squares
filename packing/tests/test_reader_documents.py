"""The overview's Read Further cards: which documents, in what order, titled and linked how.

The cards are read from the document map, so these tests hold the map's reader documents
to the groups the overview shows them in, and a fixture map to the ordering rules where
the real one has no example of a case (two reports on one date, a missing summary).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from devtools import reader_documents, site_kit
from devtools.check_documentation import states_a_bound
from devtools.reader_documents import (
    DEFAULT_BRANCH,
    RENDER_INPUTS,
    REPO,
    REPORTS,
    RESULTS,
    START,
    ReaderDocument,
    document_url,
    documents_from,
    load_map,
    report_date,
    shown_paths,
    title,
)


@pytest.fixture(scope="module")
def cards() -> tuple[ReaderDocument, ...]:
    return reader_documents.reader_documents()


def _groups(cards: tuple[ReaderDocument, ...], group: str) -> list[ReaderDocument]:
    return [card for card in cards if card.group == group]


def test_the_cards_come_in_three_groups_in_the_order_the_overview_shows(
    cards: tuple[ReaderDocument, ...],
) -> None:
    """Start here, then results and policy, then every research report."""
    groups = [card.group for card in cards]
    assert groups == sorted(groups, key=("start", "results", "reports").index)
    assert [card.path for card in _groups(cards, "start")] == list(START)
    assert [card.path for card in _groups(cards, "results")] == list(RESULTS)
    assert START == ("README.md", "TUTORIAL.md", "SYNOPSIS.md")
    assert RESULTS == (
        "packing/frontier/RESULTS.md",
        "packing/frontier/STATUS.md",
        "epistemics.md",
        "conventions.md",
    )
    assert len({card.path for card in cards}) == len(cards)


def test_every_research_report_is_a_card(cards: tuple[ReaderDocument, ...]) -> None:
    """Every report under `docs/project/research/` has a card, and nothing else there does."""
    on_disk = {path.relative_to(REPO).as_posix() for path in (REPO / REPORTS).glob("*.md")}
    reports = _groups(cards, "reports")
    assert {card.path for card in reports} == on_disk
    assert len(reports) == 20


def test_reports_stand_maintained_first_then_newest_first(
    cards: tuple[ReaderDocument, ...],
) -> None:
    """A dated record is labeled as one, with the date its file name carries."""
    lifecycles = {entry["path"]: entry["lifecycle"] for entry in load_map()["documents"]}
    reports = _groups(cards, "reports")
    for card in reports:
        assert card.date == report_date(card.path)
        assert card.dated is (lifecycles[card.path] == "retained")
    order = [(card.dated, card.date or "") for card in reports]
    assert [dated for dated, _ in order] == sorted(dated for dated, _ in order)
    for dated in (False, True):
        dates = [date for flag, date in order if flag is dated]
        assert dates == sorted(dates, reverse=True)
    assert any(card.dated for card in reports)
    assert not all(card.dated for card in reports)
    for card in (*_groups(cards, "start"), *_groups(cards, "results")):
        assert card.date is None
        assert card.dated is False


def test_a_card_links_github_on_the_default_branch_and_the_tutorial_links_its_page(
    cards: tuple[ReaderDocument, ...],
) -> None:
    """A reader lands on the document as it is now; the tutorial is a page of the site."""
    tutorial = next(item.href for item in site_kit.NAV_ITEMS if item.key == "tutorial")
    assert tutorial == "tutorial.html"
    for card in cards:
        if card.path == "TUTORIAL.md":
            assert card.url == tutorial
        else:
            assert card.url == f"https://github.com/jlevy/squares/blob/main/{card.path}"
    assert DEFAULT_BRANCH == "main"
    assert document_url("README.md") == f"{site_kit.REPO_URL}/blob/main/README.md"


def test_a_card_is_titled_by_its_documents_first_heading(
    cards: tuple[ReaderDocument, ...],
) -> None:
    titles = {card.path: card.title for card in cards}
    assert titles["README.md"] == "The Squares Project"
    assert titles["packing/frontier/STATUS.md"] == "Current Square-Packing Frontier"
    for card in cards:
        assert card.title == title(REPO / card.path)
        assert card.title
        assert not card.title.startswith("#")


def test_a_cards_summary_is_the_maps_and_states_no_bound(
    cards: tuple[ReaderDocument, ...],
) -> None:
    summaries = {entry["path"]: entry.get("summary") for entry in load_map()["documents"]}
    for card in cards:
        assert card.summary == summaries[card.path]
        assert states_a_bound(card.summary) is None, (card.path, card.summary)


def test_every_document_a_card_reads_is_a_render_input(
    cards: tuple[ReaderDocument, ...],
) -> None:
    """A card's title is read from its document, so the document is an input of the page."""
    for card in cards:
        path = REPO / card.path
        assert any(
            path == declared or path.is_relative_to(declared) for declared in RENDER_INPUTS
        )
    for declared in RENDER_INPUTS:
        assert declared.exists(), declared


def test_the_shown_paths_are_the_fixed_documents_and_the_mapped_reports() -> None:
    document_map = load_map()
    shown = shown_paths(document_map)
    assert shown[: len(START) + len(RESULTS)] == (*START, *RESULTS)
    assert all(path.startswith(REPORTS) for path in shown[len(START) + len(RESULTS) :])


# ---------------------------------------------------------------------------
# A fixture map, for what the real one has no example of.
# ---------------------------------------------------------------------------


def _entry(
    path: str, lifecycle: str = "maintained", summary: str | None = "Covers it."
) -> dict:
    entry: dict[str, Any] = {
        "path": path,
        "role": "research-report" if path.startswith(REPORTS) else "orientation",
        "authority": "supporting",
        "lifecycle": lifecycle,
    }
    if summary is not None:
        entry["summary"] = summary
    return entry


def _fixture(tmp_path: Path, reports: list[dict]) -> dict:
    for entry in [*(_entry(path) for path in (*START, *RESULTS)), *reports]:
        document = tmp_path / entry["path"]
        document.parent.mkdir(parents=True, exist_ok=True)
        document.write_text(
            f"---\ntitle: front matter\n---\n```\n# not a heading\n```\n# {document.stem}\n",
            encoding="utf-8",
        )
    return {"documents": [*(_entry(path) for path in (*START, *RESULTS)), *reports]}


def test_reports_on_one_date_stand_in_path_order(tmp_path: Path) -> None:
    reports = [
        _entry(f"{REPORTS}research-2026-09-01-b.md"),
        _entry(f"{REPORTS}research-2026-09-09-old.md", lifecycle="retained"),
        _entry(f"{REPORTS}research-2026-09-01-a.md"),
        _entry(f"{REPORTS}research-2026-08-01-z.md"),
        _entry(f"{REPORTS}research-2026-09-05-new.md"),
    ]
    cards = documents_from(_fixture(tmp_path, reports), repo=tmp_path)
    assert [card.path.removeprefix(REPORTS) for card in cards if card.group == "reports"] == [
        "research-2026-09-05-new.md",
        "research-2026-09-01-a.md",
        "research-2026-09-01-b.md",
        "research-2026-08-01-z.md",
        "research-2026-09-09-old.md",
    ]
    assert [card.dated for card in cards if card.group == "reports"] == [False] * 4 + [True]
    assert cards[0].title == "README"


def test_a_shown_document_without_a_summary_is_refused(tmp_path: Path) -> None:
    reports = [_entry(f"{REPORTS}research-2026-09-01-a.md", summary=None)]
    with pytest.raises(ValueError, match="needs a summary"):
        documents_from(_fixture(tmp_path, reports), repo=tmp_path)


def test_a_fixed_document_the_map_does_not_record_is_refused(tmp_path: Path) -> None:
    document_map = _fixture(tmp_path, [])
    document_map["documents"] = [
        entry for entry in document_map["documents"] if entry["path"] != "epistemics.md"
    ]
    with pytest.raises(ValueError, match="does not record"):
        documents_from(document_map, repo=tmp_path)


def test_a_report_without_a_dated_name_is_refused() -> None:
    with pytest.raises(ValueError, match="research-YYYY-MM-DD-"):
        report_date(f"{REPORTS}notes.md")


def test_a_document_without_a_heading_cannot_title_a_card(tmp_path: Path) -> None:
    document = tmp_path / "untitled.md"
    document.write_text("```\n# in a fence\n```\n## a second-level heading\n", encoding="utf-8")
    with pytest.raises(ValueError, match="no level-one heading"):
        title(document)
