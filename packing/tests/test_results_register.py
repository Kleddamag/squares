"""The results register's rungs are earned: the derivation and its refusals.

`epistemics.md` owns the vocabulary; `devtools/check_results.py` is its
executable form. These tests pin the derivation ladder on synthetic atoms, the
live register's health, and the refusal directions a control also exercises:
a rung claimed past its atoms, and an understatement with no composition note.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

from devtools import backfill_registered, check_results, render_results
from devtools.check_results import (
    derive_confirmation,
    derive_verification,
    repository_file_problem,
    verification_relation,
)
from sqpack.yamlio import safe_load

MACHINE_ENTRY = {
    "method": "exact-algebraic",
    "certificate": "somewhere.py",
    "replay": "uv run --frozen python -m somewhere",
    "replay_status": "passed",
    "origin": "audited-here",
}


def test_the_live_register_is_healthy() -> None:
    assert check_results.main() == 0


def test_confirmation_ladder_on_synthetic_atoms() -> None:
    assert derive_confirmation([]) == "C0"
    read_only = {
        "external_review": {
            "state": "informally-verified",
            "date": "2026-08-31",
            "reviewed_by": "reviewer",
            "note": "Read the argument; did not rederive its case split.",
        },
        "origin": "external",
    }
    assert derive_confirmation([read_only]) == "C1"
    assert derive_confirmation([{**read_only, "origin": "independently-external"}]) == "C1"
    assert derive_confirmation([{**read_only, "origin": "replayed-here"}]) == "C0"
    assert (
        derive_confirmation(
            [{**read_only, "external_review": {"state": "informally-verified"}}]
        )
        == "C0"
    )
    replayed = {
        "origin": "replayed-here",
        "replay": "uv run replay",
        "replay_status": "passed",
        "method": "numerical-f64",
    }
    assert derive_confirmation([replayed]) == "C2"
    assert derive_confirmation([{**replayed, "replay": None}]) == "C0"
    assert derive_confirmation([dict(MACHINE_ENTRY)]) == "C3"
    # Two machine proofs of the same method are still C3: independence is
    # between mechanisms.
    assert derive_confirmation([dict(MACHINE_ENTRY), dict(MACHINE_ENTRY)]) == "C3"
    interval = dict(MACHINE_ENTRY, method="interval-certified")
    assert derive_confirmation([dict(MACHINE_ENTRY), interval]) == "C4"
    assert derive_confirmation([dict(MACHINE_ENTRY)], review_ready=True) == "C5"
    assert derive_confirmation([replayed], review_ready=True) == "C2"
    # The world's machine proof raises V, never C.
    external_machine = dict(MACHINE_ENTRY, origin="external")
    assert derive_confirmation([external_machine]) == "C0"


def test_verification_ladder_on_synthetic_atoms() -> None:
    assert derive_verification([]) == "V0"
    numeric = {"method": "numerical-f64", "precision": {"rounding": "nearest"}}
    assert derive_verification([numeric]) == "V1"
    published = {"method": "published-proof", "proof": {"theorem": "T"}}
    assert derive_verification([published]) == "V3"
    audited = {"method": "proof-audited", "proof": {"theorem": "T"}}
    assert derive_verification([audited]) == "V3"
    assert derive_verification([dict(MACHINE_ENTRY, origin="external")]) == "V4"
    assert derive_verification([{"method": "proof-assistant-checked"}]) == "V5"


def test_v2_bridges_only_an_unavailable_proof() -> None:
    assert verification_relation("V2", "V0") == "supported"
    assert verification_relation("V2", "V1") == "supported"
    assert verification_relation("V2", "V3") == "understated"
    assert verification_relation("V2", "V4") == "understated"


def test_result_paths_must_name_repository_files() -> None:
    assert repository_file_problem("epistemics.md") is None
    assert repository_file_problem("packing") == "does not name a file"
    assert repository_file_problem("/etc/passwd") == (
        "must be a normalized repository-relative path"
    )
    assert repository_file_problem("../outside") == (
        "must be a normalized repository-relative path"
    )


def test_a_reversed_scope_range_is_refused(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    poisoned = _changed_result(tmp_path, "T-007", scope={"n_min": 100, "n_max": 4})
    monkeypatch.setattr(check_results, "RESULTS", poisoned)
    assert check_results.main() == 1
    assert "T-007: scope range is reversed: 100 > 4" in capsys.readouterr().out


def test_results_renderer_escapes_a_pipe_in_a_claim(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    register = _poisoned_register(
        tmp_path,
        "      Sixteen points make [0, 4426213/1000000]^2 unavoidable",
        "      Sixteen points | make [0, 4426213/1000000]^2 unavoidable",
    )
    monkeypatch.setattr(render_results, "RESULTS", register)
    row = next(
        line for line in render_results.render().splitlines() if line.startswith("| T-001 ")
    )
    assert r"Sixteen points \| make" in row
    assert len(re.findall(r"(?<!\\)\|", row)) == 8


def _poisoned_register(tmp_path: Path, old: str, new: str) -> Path:
    text = check_results.RESULTS.read_text(encoding="utf-8")
    assert text.count(old) == 1
    target = tmp_path / "results.yaml"
    target.write_text(text.replace(old, new), encoding="utf-8")
    return target


def _changed_result(tmp_path: Path, result_id: str, **changes: object) -> Path:
    register = safe_load(check_results.RESULTS.read_text(encoding="utf-8"))
    record = next(result for result in register["results"] if result["id"] == result_id)
    record.update(changes)
    target = tmp_path / "results.yaml"
    target.write_text(
        yaml.safe_dump(register, sort_keys=False, allow_unicode=True, width=96),
        encoding="utf-8",
    )
    return target


def test_c5_is_earned_by_a_mapped_review_artifact(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    promoted = _changed_result(
        tmp_path,
        "T-004",
        confirmation="C5",
        review_artifact=(
            "docs/project/reviews/"
            "review-2026-08-31-overnight-run-verification-determinations.md"
        ),
    )
    monkeypatch.setattr(check_results, "RESULTS", promoted)
    assert check_results.main() == 0


def test_c5_refuses_a_mapped_document_that_is_not_a_review(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    promoted = _changed_result(
        tmp_path,
        "T-004",
        confirmation="C5",
        review_artifact="epistemics.md",
    )
    monkeypatch.setattr(check_results, "RESULTS", promoted)
    assert check_results.main() == 1
    assert "not a non-superseded review" in capsys.readouterr().out


def test_an_inflated_rung_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    poisoned = _poisoned_register(
        tmp_path,
        "    verification: V3\n    confirmation: C1\n    significance:\n"
        "      score: 3\n      rationale: >-\n        A published exact value",
        "    verification: V3\n    confirmation: C4\n    significance:\n"
        "      score: 3\n      rationale: >-\n        A published exact value",
    )
    monkeypatch.setattr(check_results, "RESULTS", poisoned)
    assert check_results.main() == 1
    assert "T-006: declares C4" in capsys.readouterr().out


def test_an_unexplained_understatement_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # T-004 sits at its derived C3; dropping it to C2 with no composition note
    # must fail in the sandbagging direction.
    poisoned = _poisoned_register(
        tmp_path,
        "    verification: V4\n    confirmation: C3\n    significance:\n"
        "      score: 3\n      rationale: >-\n"
        "        As far as the archived corpus shows, the first machine verification of",
        "    verification: V4\n    confirmation: C2\n    significance:\n"
        "      score: 3\n      rationale: >-\n"
        "        As far as the archived corpus shows, the first machine verification of",
    )
    monkeypatch.setattr(check_results, "RESULTS", poisoned)
    assert check_results.main() == 1
    assert "T-004: understates C3 as C2" in capsys.readouterr().out


def test_v0_cannot_hide_machine_verification_behind_notes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    poisoned = _changed_result(
        tmp_path,
        "T-004",
        verification="V0",
        notes="Deliberately poisoned declaration for the regression.",
    )
    monkeypatch.setattr(check_results, "RESULTS", poisoned)
    assert check_results.main() == 1
    assert "T-004: understates V4 as V0" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("kind", "value"),
    [
        ("hypothesis", "H-999"),
        ("agenda_cell", "BC-999"),
        ("session", "session-999"),
        ("experiment", "exp-999"),
    ],
)
def test_a_dangling_produced_by_id_is_refused(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    kind: str,
    value: str,
) -> None:
    """The join from a result back to the campaign is a reference, so it can dangle.

    Before `produced_by` existed the join ran through prose -- a `by:` line, cell ids
    in `next_rung` -- and nothing could resolve it. A field that resolves to nothing
    would be the same prose with a colon in front of it.
    """
    poisoned = _changed_result(tmp_path, "T-017", produced_by={kind: value})
    monkeypatch.setattr(check_results, "RESULTS", poisoned)
    assert check_results.main() == 1
    assert f"T-017: produced_by.{kind} names {value}, which is not a recorded" in (
        capsys.readouterr().out
    )


def test_produced_by_resolves_every_kind_of_campaign_record(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    known = check_results.campaign_ids()
    assert {"H-060", "H-061"} <= known["hypothesis"]
    assert {"BC-150", "BC-152", "BC-161"} <= known["agenda_cell"]
    assert {"session-083", "session-085"} <= known["session"]
    assert {"exp-058", "exp-059"} <= known["experiment"]
    linked = _changed_result(
        tmp_path,
        "T-017",
        produced_by={
            "hypothesis": "H-061",
            "agenda_cell": "BC-161",
            "session": "session-085",
            "experiment": "exp-058",
        },
    )
    monkeypatch.setattr(check_results, "RESULTS", linked)
    assert check_results.main() == 0


def test_a_previously_published_result_names_its_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A result by others without its source would be credit restated nowhere."""
    register = safe_load(check_results.RESULTS.read_text(encoding="utf-8"))
    record = next(result for result in register["results"] if result["id"] == "T-032")
    record.pop("attribution")
    target = tmp_path / "results.yaml"
    target.write_text(yaml.safe_dump(register, sort_keys=False, allow_unicode=True))
    monkeypatch.setattr(check_results, "RESULTS", target)
    assert check_results.main() == 1
    assert "T-032: a previously-published result names its source in attribution" in (
        capsys.readouterr().out
    )


def test_a_novel_result_is_this_projects_and_names_no_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    claimed = _changed_result(
        tmp_path,
        "T-017",
        attribution={"source_keys": ["[evand square-packing 2026]"], "published": "2026-08-25"},
    )
    monkeypatch.setattr(check_results, "RESULTS", claimed)
    assert check_results.main() == 1
    assert "T-017: an apparently-novel result is this project's" in capsys.readouterr().out


def test_an_attribution_key_resolves_in_the_bibliography(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    dangling = _changed_result(
        tmp_path,
        "T-032",
        attribution={"source_keys": ["[nobody 2026]"], "published": "2026-09-20"},
    )
    monkeypatch.setattr(check_results, "RESULTS", dangling)
    assert check_results.main() == 1
    assert "T-032: attribution names [nobody 2026], which bibliography.yaml lacks" in (
        capsys.readouterr().out
    )


def test_a_recent_result_by_others_needs_its_sources_lineage() -> None:
    record = {
        "id": "T-999",
        "novelty": "previously-published",
        "attribution": {"source_keys": ["[a]", "[b]"], "published": "2026-09-01"},
    }
    sources = {"[a]": {"lineage": "independent"}, "[b]": {}}
    assert check_results.attribution_problems(record, sources) == [
        "T-999: [b] has no lineage, which a result by others published since 2026-08-22 needs"
    ]
    record["attribution"]["published"] = "2026-08-21"
    assert check_results.attribution_problems(record, sources) == []


def test_a_recent_case_lower_bound_is_covered_for_its_own_n() -> None:
    """The entry that covers a case must cite its evidence and name its `n`.

    A monotone consequence is part of the result it follows from, so the scope carries
    it; an entry that cites the evidence at another `n` does not cover this one.
    """
    evidence = {"E-x": {"novelty": "previously-published", "source_key": "[s]"}}
    sources = {"[s]": {"dated": "2026-09-28"}}
    cases = {27: {"E-x"}, 28: {"E-x"}}
    narrow = [{"evidence": ["E-x"], "scope": {"n_values": [27]}}]
    assert check_results.coverage_problems(narrow, evidence, sources, cases) == [
        "n-028: its lower bound cites E-x, and no registered result citing it covers n = 28"
    ]
    wide = [{"evidence": ["E-x"], "scope": {"n_min": 27, "n_max": 28}}]
    assert check_results.coverage_problems(wide, evidence, sources, cases) == []
    sources["[s]"]["dated"] = "2026-08-21"
    assert check_results.coverage_problems(narrow, evidence, sources, cases) == []


def test_a_sources_credit_and_lineage_agree() -> None:
    """`lineage` is typed so no tool parses `credit`; the two must still say one thing.

    A source that builds on this project or credits it is printed "X after ..., Levy";
    an independent one never names this project. The four `n = 17` keys the W8 audit
    of 2026-09-29 found without that credit would have failed here.
    """
    bibliography = safe_load(check_results.BIBLIOGRAPHY.read_text(encoding="utf-8"))
    for source in bibliography["sources"]:
        lineage = source.get("lineage")
        if lineage is None:
            continue
        names_project = "Levy" in (source.get("credit") or "")
        assert names_project == (lineage != "independent"), source["key"]


def _dropped_field(tmp_path: Path, result_id: str, field: str) -> Path:
    register = safe_load(check_results.RESULTS.read_text(encoding="utf-8"))
    record = next(result for result in register["results"] if result["id"] == result_id)
    record.pop(field)
    target = tmp_path / "results.yaml"
    target.write_text(
        yaml.safe_dump(register, sort_keys=False, allow_unicode=True, width=96),
        encoding="utf-8",
    )
    return target


def test_a_result_without_a_headline_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A table row reads the headline, so a result with none would be a blank cell."""
    monkeypatch.setattr(check_results, "RESULTS", _dropped_field(tmp_path, "T-017", "headline"))
    assert check_results.main() == 1
    assert "T-017: states no headline" in capsys.readouterr().out


def test_a_headline_longer_than_a_table_cell_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """The failure a headline invites: the claim's first sentence pasted in whole."""
    register = safe_load(check_results.RESULTS.read_text(encoding="utf-8"))
    claim = next(result for result in register["results"] if result["id"] == "T-017")["claim"]
    first_sentence = " ".join(str(claim).split()).split(". ")[0]
    assert len(first_sentence) > check_results.HEADLINE_LIMIT, "premise: the sentence is long"
    pasted = _changed_result(tmp_path, "T-017", headline=first_sentence)
    monkeypatch.setattr(check_results, "RESULTS", pasted)
    assert check_results.main() == 1
    assert f"T-017: headline is {len(first_sentence)} characters, over the 100" in (
        capsys.readouterr().out
    )


def test_a_headline_states_only_numbers_its_claim_does() -> None:
    """A headline may cut the claim's decimal short, marked, but never round or add one.

    Rounding `3.810025...` up to `3.810026` would overstate a lower bound in the one cell
    a reader sees; a truncation marked with an ellipsis stays true.
    """
    record = {
        "id": "T-999",
        "claim": "s(11) >= 38100*sqrt(8100042893309449)/899996306539 = 3.810025723614703.",
    }
    assert check_results.headline_problems({**record, "headline": "`s(11) ≥ 3.8100257…`"}) == []
    assert check_results.headline_problems({**record, "headline": "`s(11) ≥ 3.810026`"}) == [
        "T-999: headline states 3.810026, which its claim does not"
    ]
    assert check_results.headline_problems({**record, "headline": "`s(11) ≥ 3.8100257`"}) == [
        "T-999: headline states 3.8100257, which its claim does not"
    ]
    assert check_results.headline_problems({**record, "headline": "`s(12) ≥ 3.8100257…`"}) == [
        "T-999: headline states 12, which its claim does not"
    ]


def test_a_result_by_others_carries_no_established_date(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Its date is its source's, in `attribution.published`; a second would disagree."""
    dated_twice = _changed_result(tmp_path, "T-032", established="2026-09-20")
    monkeypatch.setattr(check_results, "RESULTS", dated_twice)
    assert check_results.main() == 1
    assert "T-032: a result by others is dated by attribution.published" in (
        capsys.readouterr().out
    )


def test_a_result_of_this_project_names_the_day_it_was_established(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    undated = _dropped_field(tmp_path, "T-017", "established")
    monkeypatch.setattr(check_results, "RESULTS", undated)
    assert check_results.main() == 1
    assert "T-017: a result of this project names the day it was established" in (
        capsys.readouterr().out
    )


def test_an_established_date_lies_within_the_projects_record() -> None:
    """Not before the project began, not after the register was last reviewed, and real."""
    record = {"id": "T-999", "established": "2026-08-22"}
    assert check_results.established_problems(record, "2026-09-29") == []
    assert check_results.established_problems(
        {**record, "established": "2026-08-21"}, "2026-09-29"
    ) == ["T-999: established 2026-08-21 is before 2026-08-22, when this project's work began"]
    assert check_results.established_problems(
        {**record, "established": "2026-09-30"}, "2026-09-29"
    ) == ["T-999: established 2026-09-30 is after the register's last review, 2026-09-29"]
    assert check_results.established_problems(
        {**record, "established": "2026-09-31"}, "2026-09-29"
    ) == ["T-999: established 2026-09-31 is not a date"]


def test_every_result_names_the_day_it_was_registered(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """This project's and others' alike: the overview's table sorts by it."""
    for result_id in ("T-017", "T-032"):
        unregistered = _dropped_field(tmp_path, result_id, "registered")
        monkeypatch.setattr(check_results, "RESULTS", unregistered)
        assert check_results.main() == 1
        assert f"{result_id}: states no registered date" in capsys.readouterr().out


def test_a_registration_day_follows_the_result_and_precedes_the_review() -> None:
    """Not before the project, the result's own date or after the last review, and real."""
    ours = {"id": "T-999", "established": "2026-09-01", "registered": "2026-09-02"}
    assert check_results.registered_problems(ours, "2026-09-29") == []
    assert check_results.registered_problems(
        {**ours, "registered": "2026-08-31"}, "2026-09-29"
    ) == ["T-999: registered 2026-08-31 is before it was established, 2026-09-01"]
    assert check_results.registered_problems(
        {**ours, "registered": "2026-09-30"}, "2026-09-29"
    ) == ["T-999: registered 2026-09-30 is after the register's last review, 2026-09-29"]
    assert check_results.registered_problems(
        {**ours, "registered": "2026-02-30"}, "2026-09-29"
    ) == ["T-999: registered 2026-02-30 is not a date"]
    theirs = {
        "id": "T-998",
        "attribution": {"source_keys": ["[X]"], "published": "2026-09-20"},
        "registered": "2026-09-19",
    }
    assert check_results.registered_problems(theirs, "2026-09-29") == [
        "T-998: registered 2026-09-19 is before it was published, 2026-09-20"
    ]
    old = {**theirs, "attribution": {"source_keys": ["[X]"], "published": "1979"}}
    assert (
        check_results.registered_problems({**old, "registered": "2026-08-31"}, "2026-09-29")
        == []
    )
    assert check_results.registered_problems(
        {**old, "registered": "2026-08-21"}, "2026-09-29"
    ) == ["T-998: registered 2026-08-21 is before 2026-08-22, when this project's work began"]


def test_the_registration_backfill_adds_one_line_and_nothing_else() -> None:
    """After `established` on this project's results, after `headline` on others'."""
    text = (
        "results:\n"
        "  - id: T-001\n"
        '    headline: "`s(17) ≥ 4`"\n'
        "    established: '2026-08-31'\n"
        "    claim: >-\n"
        "      s(17) >= 4.\n"
        "  - id: T-002\n"
        '    headline: "`s(46) ≥ 7`"\n'
        "    claim: s(46) >= 7.\n"
        "  - id: T-003\n"
        '    headline: "`s(5) ≥ 2`"\n'
        "    registered: '2026-09-01'\n"
        "    claim: s(5) >= 2.\n"
    )
    days = {"T-001": "2026-08-31", "T-002": "2026-09-02", "T-003": "2026-09-03"}
    written = backfill_registered.with_registered(text, days)
    assert written.splitlines() == [
        *text.splitlines()[:4],
        "    registered: '2026-08-31'",
        *text.splitlines()[4:8],
        "    registered: '2026-09-02'",
        *text.splitlines()[8:],
    ]
    assert backfill_registered.with_registered(written, days) == written


def test_the_registration_backfill_matches_a_result_not_only_its_id() -> None:
    """On 2026-09-21 a merge renumbered one of two `T-031`s; an id alone would misdate it."""
    current = {
        "id": "T-032",
        "scope": {"n_values": [17]},
        "attribution": {"source_keys": ["[R012]"], "published": "2026-09-20"},
    }
    assert backfill_registered.same_result({**current, "attribution": None}, current)
    assert not backfill_registered.same_result({**current, "id": "T-031"}, current)
    assert not backfill_registered.same_result(
        {**current, "scope": {"n_values": [11]}}, current
    )
    other = {**current, "attribution": {"source_keys": ["[Other]"], "published": "2026-09-20"}}
    assert not backfill_registered.same_result(other, current)


def test_the_overview_template_is_in_the_reader_tier(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A `T-NNN` the overview's prose names must be a registered result, as in README."""
    template = next(
        path for path in check_results.READER_TIER if path.name == "overview-article.md"
    )
    poisoned = tmp_path / template.name
    poisoned.write_text(
        template.read_text(encoding="utf-8") + "\nSee T-999.\n", encoding="utf-8"
    )
    tier = tuple(poisoned if path == template else path for path in check_results.READER_TIER)
    monkeypatch.setattr(check_results, "READER_TIER", tier)
    assert check_results.main() == 1
    assert "overview-article.md: mentions unknown result T-999" in capsys.readouterr().out
