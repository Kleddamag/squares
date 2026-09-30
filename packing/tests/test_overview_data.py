"""The overview's data is the record's, read through the functions the record's views use.

`devtools.overview_data` is the one typed model the overview renders from. These tests
hold it to the views that already render the same record: every register entry is a row
under the heading `RESULTS.md` gives it, the recent results are README's generated lists
in README's order, every credit is `result_credit.credit_line`, the counts are the
declared rungs in `results.yaml`, and a bound keeps its claim's relation. They also hold
the explainer's edition note to the case record, and every link to a permalink at the
build commit that lands on the line it names.
"""

from __future__ import annotations

import dataclasses
import json
import re
from collections import Counter
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import overview_data as data
from devtools import render_explainer, significance
from devtools import render_recent_results as recent
from devtools.build_bound_citations import PROJECT_NAME
from devtools.result_credit import credit_line
from sqpack.release import PUBLICATION_HISTORY
from sqpack.yamlio import safe_load

REPO = data.REPO


@pytest.fixture(scope="module")
def model() -> data.OverviewData:
    return data.load()


@pytest.fixture(scope="module")
def records() -> recent.Records:
    return recent.load_records()


@pytest.fixture(scope="module")
def register() -> list[dict]:
    return safe_load(data.RESULTS.read_text(encoding="utf-8"))["results"]


def _rows(model: data.OverviewData) -> dict[str, data.Result]:
    return {result.id: result for group in model.groups for result in group.results}


def _links(model: data.OverviewData) -> list[data.Link]:
    links: list[data.Link] = []
    for result in _rows(model).values():
        links.extend((*result.records, *result.artifacts, *result.controls))
    for source in model.sources:
        links.extend(source.cases)
        if source.archive is not None:
            links.append(source.archive)
        links.extend(release.archive for release in source.releases if release.archive)
    return links


# --- The register --------------------------------------------------------------------------


def test_every_register_entry_is_a_row_under_exactly_one_heading(
    model: data.OverviewData, register: list[dict]
) -> None:
    listed = [result.id for group in model.groups for result in group.results]
    assert Counter(listed) == Counter(str(record["id"]) for record in register)


def test_the_groups_are_results_md_s_headings_in_its_order(model: data.OverviewData) -> None:
    """The overview's table and `RESULTS.md` call the same `grouped_results`."""
    view = (data.FRONTIER / "RESULTS.md").read_text(encoding="utf-8")
    sections = re.split(r"^#{2,3} ", view, flags=re.MULTILINE)
    by_title = {
        section.split("\n", 1)[0]: re.findall(r"^\| (T-\d{3}) \|", section, re.MULTILINE)
        for section in sections[1:]
    }
    for group in model.groups:
        assert group.title in by_title, group.title
        assert [result.id for result in group.results] == by_title[group.title]
    assert model.groups[0].key == "this-project"
    assert all(result.ours for result in model.groups[0].results)
    assert not any(result.ours for group in model.groups[1:] for result in group.results)


def test_the_recent_results_are_readme_s_generated_lists_in_readme_s_order(
    model: data.OverviewData, records: recent.Records
) -> None:
    readme = recent.README.read_text(encoding="utf-8")
    ours = re.findall(r"^\| \[(T-\d{3})\]", recent.block(readme, recent.NEW), re.MULTILINE)
    others = re.findall(
        r"^\| [^|]+ \| \[(T-\d{3})\]", recent.block(readme, recent.OTHERS), re.MULTILINE
    )
    assert [result.id for result in model.recent_ours] == ours
    assert [result.id for result in model.recent_others] == others
    assert ours == [str(record["id"]) for record in recent.ours(records)]
    assert others == [str(record["id"]) for record in recent.by_others(records)]
    assert all(result.recent for result in (*model.recent_ours, *model.recent_others))


def test_every_credit_is_the_bibliography_s_printed_whole(
    model: data.OverviewData, records: recent.Records
) -> None:
    for result in _rows(model).values():
        record = records.results[result.id]
        if result.ours:
            assert result.credit == PROJECT_NAME
            assert result.lineage == "this-project"
        else:
            assert result.credit == credit_line(record, records.sources)


def test_every_source_s_own_statement_of_ai_assistance_is_shown(
    model: data.OverviewData, records: recent.Records
) -> None:
    """In the source's terms, from the bibliography field the case-record tool also reads."""
    shown = 0
    for result in _rows(model).values():
        keys = (records.results[result.id].get("attribution") or {}).get("source_keys") or []
        stated = [
            " ".join(records.sources[key]["ai_assistance"]["statement"].split())
            for key in keys
            if records.sources[key].get("ai_assistance")
        ]
        if stated:
            shown += 1
            assert result.ai_assistance is not None
            assert all(statement in result.ai_assistance for statement in stated)
        else:
            assert result.ai_assistance is None
    assert shown, "premise: some registered source states AI assistance"


def test_relation_standing_and_holder_are_read_through_readme_s_functions(
    model: data.OverviewData, records: recent.Records
) -> None:
    for result in _rows(model).values():
        record = records.results[result.id]
        assert result.standing == recent.standing(record, records)
        expected = (
            recent.relation(record, records) if recent.is_recent_by_others(record) else None
        )
        assert result.relation == expected
        if result.standing != recent.SUPERSEDED:
            assert result.superseded_by is None
            continue
        assert result.superseded_by
        assert result.superseded_by_results
        for n in result.n_values:
            lane = recent.verified_lane(n, records.cases[n], records)
            assert lane.holder in result.superseded_by


def test_a_reported_result_is_labelled_reported_and_an_exact_value_as_one(
    model: data.OverviewData,
) -> None:
    rows = _rows(model)
    for result in rows.values():
        assert result.reported == (result.verification == "V0")
    assert rows["T-055"].reported
    assert rows["T-055"].exact_value
    assert rows["T-051"].exact_value
    assert not rows["T-051"].reported
    assert not rows["T-037"].exact_value


def test_every_row_carries_its_dates(model: data.OverviewData, register: list[dict]) -> None:
    rows = _rows(model)
    for record in register:
        result = rows[str(record["id"])]
        assert result.registered == str(record["registered"])
        if record.get("attribution"):
            assert result.published == str(record["attribution"]["published"])
            assert result.established is None
        else:
            assert result.established == str(record["established"])
            assert result.published is None


# --- Bounds ------------------------------------------------------------------------------


def test_a_bound_keeps_its_claim_s_relation(model: data.OverviewData) -> None:
    """`T-037` claims `s(11) > 31/8`, strictly, where the case record states only a value."""
    rows = _rows(model)
    kleddamag = rows["T-037"].bound
    assert kleddamag is not None
    assert (kleddamag.relation, kleddamag.exact, kleddamag.decimal) == (">", "31/8", "3.875")
    assert kleddamag.tex == r"s(11) \gt \frac{31}{8}"
    assert kleddamag.value == Fraction(31, 8)
    lead = rows["T-026"].bound
    assert lead is not None
    assert lead.relation == "≥"
    assert lead.value is None
    assert lead.tex == r"s(11) \ge \frac{955000\sqrt{518400042893309449}}{179696714646249}"
    winter = rows["T-057"].bound
    assert winter is not None
    assert winter.relation == "≤"
    assert rows["T-010"].bound is not None
    assert rows["T-010"].bound.tex == r"s(11) \ge 2 + \frac{4}{\sqrt{5}}"


def test_an_entry_that_is_no_single_bound_has_none(model: data.OverviewData) -> None:
    """A rigidity, an exclusion, or a family of cases shows its headline instead."""
    rows = _rows(model)
    for rid in ("T-012", "T-023", "T-031", "T-044", "T-046", "T-056"):
        assert rows[rid].bound is None, rid


def test_decimals_are_cut_never_rounded(model: data.OverviewData) -> None:
    """A lower bound shown rounded up would claim more than the record proves."""
    checked = 0
    for result in _rows(model).values():
        bound = result.bound
        if bound is None:
            continue
        shown = Fraction(Decimal(bound.decimal.removesuffix(recent.ELLIPSIS)))
        if bound.value is not None:
            if bound.decimal.endswith(recent.ELLIPSIS):
                assert shown < bound.value, result.id
            else:
                assert shown == bound.value, result.id
        else:
            form, _ = data.closed_form(bound.exact)
            assert shown <= Fraction(form.approximate) < shown + Fraction(1, 10**4), result.id
        checked += 1
    assert checked > 20


def test_a_claimed_decimal_that_disagrees_with_its_form_fails_the_render() -> None:
    with pytest.raises(ValueError, match="is not the stated"):
        data.claimed_bound("s(11) >= 38100*sqrt(8100042893309449)/899996306539 = 3.9", 11)
    bound = data.claimed_bound("s(11) >= 38100*sqrt(8100042893309449)/899996306539 = 3.81", 11)
    assert bound is not None
    assert bound.decimal == "3.8100…"


def test_a_closed_form_is_read_up_to_the_prose_that_follows_it() -> None:
    assert data.claimed_bound("Bentz: s(46) >= 7 is correct as printed.", 46) == data.Bound(
        46, "≥", "7", "7", r"s(46) \ge 7", Fraction(7)
    )
    six = data.claimed_bound("s(32) = 6. The lower half is a cover.", 32)
    assert six is not None
    assert (six.relation, six.exact) == ("=", "6")
    assert data.claimed_bound("s(11) <= that side.", 11) is None
    assert data.claimed_bound("s(12) >= 99/25", 11) is None


# --- Counts and totals -------------------------------------------------------------------


def test_the_counts_are_the_declared_rungs(
    model: data.OverviewData, register: list[dict]
) -> None:
    """Declared, never re-derived: a composition note may hold a rung below the derived one."""
    declared = {
        "V": lambda record: int(record["verification"][1]),
        "C": lambda record: int(record["confirmation"][1]),
        "S": lambda record: int(record["significance"]["score"]),
    }
    for count in model.rung_counts:
        at = [record for record in register if declared[count.axis](record) == count.rung]
        assert count.ours == sum(not record.get("attribution") for record in at), count
        assert count.others == sum(bool(record.get("attribution")) for record in at), count
    for axis in "VCS":
        counts = [count for count in model.rung_counts if count.axis == axis]
        assert sum(count.ours + count.others for count in counts) == len(register)
        ladder = significance.rungs(axis)
        assert [count.rung for count in counts] == sorted(ladder)
        for count in counts:
            assert count.label == ladder[count.rung].meaning
            assert count.definition == (
                ladder[count.rung].support or ladder[count.rung].meaning
            )


def test_the_atlas_totals_are_the_composite_s(model: data.OverviewData) -> None:
    figure = json.loads(data.COMPOSITE.read_text(encoding="utf-8"))["figure"]
    composite = next(
        item for item in figure["composites"] if item["stem"] == "known-best-1-100"
    )
    totals = composite["totals"]
    assert model.atlas == data.AtlasTotals(
        cases=100,
        proved=totals["proved_optimal"],
        open=100 - totals["proved_optimal"],
        recent_verified_lower=totals["lower_bound_recent_result"],
    )


# --- Notable sources ---------------------------------------------------------------------


def test_every_reviewed_frontier_source_is_a_release_on_exactly_one_card(
    model: data.OverviewData,
) -> None:
    coverage = safe_load(data.COVERAGE.read_text(encoding="utf-8"))["sources"]
    shown = Counter(
        (release.title, release.url, release.reviewed)
        for source in model.sources
        for release in source.releases
    )
    assert shown == Counter(
        (str(source["title"]), str(source["url"]), str(source["reviewed"]))
        for source in coverage
    )
    superseded = {
        (str(source["title"]), source["disposition"] == "superseded-covered")
        for source in coverage
    }
    assert {
        (release.title, release.superseded)
        for card in model.sources
        for release in card.releases
    } == superseded


def test_a_card_credits_its_source_as_the_bibliography_does(
    model: data.OverviewData, records: recent.Records
) -> None:
    registry = {
        entry["id"]: entry
        for entry in safe_load(data.NOTABLE_SOURCES.read_text(encoding="utf-8"))["sources"]
    }
    for card in model.sources:
        entry = registry[card.id]
        cited = [key for key in entry["keys"] if key in records.sources]
        if cited:
            assert card.credit == credit_line(
                {"attribution": {"source_keys": cited}}, records.sources
            )
        else:
            assert card.credit == entry["credit"]
    # Websites and catalogues first, then releases, then repositories.
    rank = {"website": 0, "catalogue": 0, "release": 1, "repository": 2}
    ranks = [rank[card.kind] for card in model.sources]
    assert ranks == sorted(ranks)


# --- The explainer -----------------------------------------------------------------------


def test_the_explainer_s_lead_is_an_earlier_edition_than_the_record(
    records: recent.Records,
) -> None:
    edition = data.explainer_edition()
    assert edition.lead_result == render_explainer.LEAD_RESULT == "T-026"
    case = records.cases[11]["verified_lower_bound"]
    assert edition.current_bound.value == recent.magnitude(case) == Fraction(31, 8)
    assert edition.current_bound.relation == ">"
    assert edition.current_results == ("T-037",)
    assert "Kleddamag" in edition.current_credit
    assert not edition.is_current
    assert "31/8" in edition.note
    assert "Kleddamag" in edition.note
    assert "T-026" in edition.note
    assert "T-037" in edition.note


def test_the_explainer_s_dates_are_read_from_the_publication_history() -> None:
    edition = data.explainer_edition()
    oldest = min(PUBLICATION_HISTORY, key=lambda entry: data.iso_day(entry.first_published))
    assert edition.first_published == data.iso_day(oldest.first_published) == "2026-09-05"
    introduced = next(e for e in PUBLICATION_HISTORY if e.version == edition.edition)
    assert "T-026" in introduced.result_scope
    assert (edition.edition, edition.edition_first_published) == ("v0.4.0", "2026-09-13")


def test_the_note_reads_current_when_the_lead_is_the_verified_bound() -> None:
    edition = data.explainer_edition()
    current = dataclasses.replace(
        edition,
        lead_result="T-037",
        lead_bound=edition.current_bound,
        current_results=("T-037",),
        is_current=True,
    )
    assert "is the current verified lower bound" in current.note
    assert "31/8" in current.note


# --- Links -------------------------------------------------------------------------------


def test_every_record_link_is_a_permalink_at_the_build_commit(model: data.OverviewData) -> None:
    """Never `blob/main`; `tree/` for a directory and `blob/` for a file, as on disk."""
    revision = render_explainer.link_revision()
    prefix = re.compile(
        rf"^{re.escape(render_explainer.REPO_URL)}/(tree|blob)/{revision}/([^#]+)(?:#L\d+)?$"
    )
    links = _links(model)
    assert links
    for link in links:
        match = prefix.match(link.url)
        assert match, link
        kind, path = match.groups()
        target = REPO / path
        assert target.exists(), link
        assert kind == ("tree" if target.is_dir() else "blob"), link


def test_evidence_and_register_links_land_on_the_line_that_opens_the_entry(
    model: data.OverviewData,
) -> None:
    files = {"evidence": data.EVIDENCE, "register": data.RESULTS}
    lines = {
        kind: path.read_text(encoding="utf-8").splitlines() for kind, path in files.items()
    }
    for result in _rows(model).values():
        anchored = [link for link in result.records if link.kind in files]
        assert [link.kind for link in anchored].count("register") == 1
        for link in anchored:
            line = int(link.url.rsplit("#L", 1)[1])
            wanted = link.label if link.kind == "evidence" else result.id
            assert lines[link.kind][line - 1] == f"  - id: {wanted}", link


def test_the_render_inputs_exist_and_include_what_is_read() -> None:
    assert all(path.exists() for path in data.RENDER_INPUTS)
    for path in (data.RESULTS, data.BIBLIOGRAPHY, data.NOTABLE_SOURCES, data.COVERAGE):
        assert path in data.RENDER_INPUTS
    assert data.COMPOSITE in data.RENDER_INPUTS
    assert data.EPISTEMICS in data.RENDER_INPUTS


def test_the_model_is_read_once_and_the_same_every_time() -> None:
    first = data.load()
    assert data.load() is first
    data.load.cache_clear()
    data.explainer_edition.cache_clear()
    assert data.load() == first


def test_nothing_is_read_from_directories_the_pages_checkout_leaves_out(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The Pages jobs check out without `packing/resources/*/` and `packing/campaign/*/`."""
    excluded = (REPO / "packing" / "resources", REPO / "packing" / "campaign")
    opened: list[Path] = []
    original = Path.read_text

    def spy(
        self: Path,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
    ) -> str:
        opened.append(self.resolve())
        return original(self, encoding=encoding, errors=errors, newline=newline)

    monkeypatch.setattr(Path, "read_text", spy)
    data.load.cache_clear()
    data.explainer_edition.cache_clear()
    data.cached_records.cache_clear()
    data.load()
    for path in opened:
        for root in excluded:
            if path.is_relative_to(root):
                assert path.parent == root, f"{path} is under an excluded directory"


def test_a_superseded_upper_bound_names_the_ceiling_s_holder(records: recent.Records) -> None:
    """No upper bound is superseded today, so the lane is exercised on a synthetic entry."""
    entry = {"evidence": ["E-n211-de-winter-exact-replay"], "scope": {"n_values": [211]}}
    named, results = data.superseded_by(entry, records)
    assert results == ("T-057",)
    assert named == "T-057, de Winter"
