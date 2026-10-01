# ruff: noqa: RUF001 -- the fixtures quote case-record prose, whose typography uses curly
# apostrophes and the minus sign.
"""Reader-facing prose credits a source and links it, and carries no audit mechanics.

On 2026-10-01 the register's claim for `s(32) = 6` read "certified at commit c8b36419 on
26 September 2026 by the author's clock", twenty-four claims ended "An externally
produced, previously published result, not peer reviewed; no new first-party mathematics
is claimed", and forty-four case records dated a commit to the minute and the timezone.
`devtools.check_prose_ceremony` answers that. These tests rebuild each shape as a
synthetic register or document in `tmp_path`, never as an edit to a live record, and then
hold the live tree to the rule once.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from devtools import check_prose_ceremony as ceremony

#: The claim the owner quoted, as the register held it.
OWNERS_EXAMPLE = (
    "s(32) = 6. The lower half is Evan Daniel's weighted closed cover in "
    "evand/square-packing, certified at commit c8b36419 on 26 September 2026 by the "
    "author's clock: 13,085 D4-invariant rational points of [0,6]^2."
)
DISCLAIMER = (
    "An externally produced, previously published result, not peer reviewed; no new "
    "first-party mathematics is claimed."
)


def kinds(text: str) -> set[str]:
    return {kind.name for kind, _ in ceremony.scan(text)}


def words(text: str) -> list[str]:
    return [match.group(0) for _, match in ceremony.scan(text)]


def test_the_owners_example_is_three_kinds_of_ceremony() -> None:
    assert kinds(OWNERS_EXAMPLE) == {"commit-or-digest", "commit-phrase", "clock"}
    assert "c8b36419" in words(OWNERS_EXAMPLE)


def test_the_disclaimer_sentence_is_found_whole() -> None:
    assert kinds(DISCLAIMER) == {"disclaimer"}
    assert len(words(DISCLAIMER)) == 4


@pytest.mark.parametrize(
    "sentence",
    [
        "s(32) = 6: the lower half by Evan Daniel's closed cover of 26 September 2026.",
        (
            "Evan Daniel, [evand/square-packing](https://github.com/evand/square-packing/tree/"
            "167d842cd27ba1451cb2833773ea930c80b9e65b/s12), building on Burns."
        ),
        (
            "The source is at https://github.com/Kleddamag/17-squares-certified-bound/tree/"
            "a499e2c739ce7853fa04c8bcdc85caf1c2b01b37 and nowhere else."
        ),
        "Total weight 3171350535386/10^11 = 31.713505354 < 32 on budget 16998427356.",
        "The record is campaign/resource-usage/agent-a5ada27ae702ebba4.yaml, defaced or not.",
        "Pinned at the solver's floor of 1e-10, the wall clock gate reports when CI ran.",
        "It was replayed here in full, each sweep reproducing the ledger byte for byte.",
    ],
)
def test_plain_credit_links_numbers_and_paths_are_not_ceremony(sentence: str) -> None:
    assert words(sentence) == []


@pytest.mark.parametrize(
    ("sentence", "kind"),
    [
        ("unchanged at the pinned revision `f3c5a52` of 27 September 2026", "commit-or-digest"),
        ("the retained covering (SHA-256 876820dde8d55c72) charges", "digest-word"),
        ("is dated 23 September 2026 at 01:35 UTC and was committed again", "clock"),
        ("committed on 23 September 2026 at 22:45 UTC−6", "clock"),
        ("independent of either repository’s clocks; the issue gives no side", "clock"),
        ("is dated 23 September 2026 by his clock, before Casson’s", "clock"),
        (
            "the v1.0.0 release at commit `a499e2c739ce7853fa04c8bcdc85caf1c2b01b37`",
            "commit-phrase",
        ),
        ("a packet of 6,142,946 bytes in 55 files", "packet-bytes"),
        ("with its receipt retained and hash-bound", "digest-word"),
        ("It is externally proposed and source-backed, a blog post", "disclaimer"),
    ],
)
def test_each_kind_of_ceremony_is_found(sentence: str, kind: str) -> None:
    assert kind in kinds(sentence)


def _register(tmp_path: Path, **fields: object) -> Path:
    record = {
        "id": "T-001",
        "headline": "`s(32) = 6`",
        "claim": "s(32) = 6.",
        "significance": {"rationale": "An exact value for a case that was open."},
        "next_rung": "V5 by a proof-assistant port.",
        # Structured fields: a revision here is where it belongs.
        "artifacts": ["packing/resources/web/evand-square-packing-2026-09-26/c8b36419.json"],
        "attribution": {
            "source_keys": ["[evand square-packing 2026]"],
            "published": "2026-09-26",
        },
    }
    record.update(fields)
    path = tmp_path / "results.yaml"
    path.write_text(
        yaml.safe_dump({"results": [record]}, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return path


def test_register_prose_fields_are_read_and_structured_fields_are_not(tmp_path: Path) -> None:
    clean = _register(tmp_path)
    assert ceremony.register_findings(clean, tmp_path) == []

    dirty = _register(
        tmp_path,
        claim=OWNERS_EXAMPLE,
        notes="The exp143 source is Git blob cc66f06ddd3f7cc52d8a06d30a3920ba8e992c19.",
        significance={"rationale": DISCLAIMER},
    )
    found = {
        (finding.where, finding.kind) for finding in ceremony.register_findings(dirty, tmp_path)
    }
    assert ("T-001 claim", "clock") in found
    assert ("T-001 claim", "commit-or-digest") in found
    assert ("T-001 notes", "commit-or-digest") in found
    assert ("T-001 significance.rationale", "disclaimer") in found
    assert all(where.startswith("T-001 ") for where, _ in found)


def test_a_long_paragraph_of_several_sentences_is_a_wall(tmp_path: Path) -> None:
    sentence = "The certificate is an exact nonnegative rational density on rectangles. "
    wall = sentence * 14
    assert len(wall) > ceremony.PARAGRAPH_CHARS
    (problem,) = ceremony.walls(_register(tmp_path, claim=wall))
    assert problem.startswith("T-001 claim: paragraph 1 of 1 runs to ")

    # The same words in two paragraphs are no longer a wall.
    broken = sentence * 7 + "\n" + sentence * 7
    assert ceremony.walls(_register(tmp_path, claim=broken)) == []

    # Every prose field is held to it, not only the claim.
    (problem,) = ceremony.walls(_register(tmp_path, next_rung=wall))
    assert problem.startswith("T-001 next_rung: ")


def test_one_long_sentence_is_not_a_wall(tmp_path: Path) -> None:
    statement = (
        "Every packing of eleven unit squares " + "in a square container, " * 40 + "is rigid."
    )
    assert len(statement) > ceremony.PARAGRAPH_CHARS
    assert ceremony.walls(_register(tmp_path, claim=statement)) == []


CASE_RECORD = """---
title: s(103) — square packing case
packing:
  n: 103
  reported_lower_bound:
    value: '10.2'
    note: Rectangle-density certificate reported in the retained source at 39d8ecc.
  priority_notes:
  - claim: s(103) <= 10.70377984436967189, Griffin Casson's packing
    published: griffcass/square-packing 82661bc, committed 2026-09-24T04:45:20Z
  resources:
  - key: '[evand square-packing 2026]'
    url: https://github.com/evand/square-packing/tree/167d842cd27ba1451cb2833773ea930c80b9e65b
---
# `s(103)` — open

Francisco Couzo’s packing is dated 26 September 2026 and unchanged at the pinned
revision `f3c5a52` of 27 September 2026.

```
git checkout f3c5a52
```
"""


def test_a_case_record_is_read_in_its_body_and_its_notes_only(tmp_path: Path) -> None:
    record = tmp_path / "n-103.md"
    record.write_text(CASE_RECORD, encoding="utf-8")
    found = ceremony.document_findings(record, repo=tmp_path)
    assert [(finding.where, finding.words) for finding in found] == [
        ("front matter packing.reported_lower_bound.note", "39d8ecc"),
        ("line 18", "f3c5a52"),
    ]
    assert CASE_RECORD.split("\n")[17].startswith("revision `f3c5a52`")


SECTIONED = """# Synopsis

Kleddamag’s release of 21 September 2026 proves the bound.

## Handoff Record

PR 193 merged its records as `4ad98e90`.

## The Problem

Both passes ran on clean commit `c183cc9ab`.

## The Cell Decomposition

Frozen at commit `6e21c4ca`.
"""


def test_only_a_documents_named_spans_are_read(tmp_path: Path) -> None:
    document = tmp_path / "SYNOPSIS.md"
    document.write_text(SECTIONED, encoding="utf-8")
    spans = (
        ("# Synopsis", "## Handoff Record"),
        ("## The Problem", "## The Cell Decomposition"),
    )
    found = ceremony.document_findings(document, spans, tmp_path)
    assert {finding.words for finding in found} == {"c183cc9ab", "clean commit"}
    assert {finding.where for finding in found} == {"line 11"}

    # A renamed heading must not silently stop a section being read.
    with pytest.raises(SystemExit, match="no heading '## The Lay of the Land'"):
        ceremony.document_findings(document, (("## The Lay of the Land", "## End"),), tmp_path)


def test_an_allowlist_entry_excuses_one_sentence_and_goes_stale() -> None:
    finding = ceremony.Finding(
        "epistemics.md",
        "line 98",
        "digest-word",
        "hash-bound",
        "performed here, with its receipt retained and hash-bound, is a replay",
    )
    kept = ceremony.Allowed("epistemics.md", "receipt retained and hash-bound", "the predicate")
    stale = ceremony.Allowed("README.md", "four stale cached-audit digests", "no longer said")
    elsewhere = ceremony.Allowed("README.md", "receipt retained and hash-bound", "wrong file")
    assert ceremony.unexcused([finding], [kept, stale]) == ([], [stale])
    assert ceremony.unexcused([finding], [elsewhere]) == ([finding], [elsewhere])


def test_the_live_tree_carries_no_ceremony(capsys: pytest.CaptureFixture[str]) -> None:
    assert ceremony.main([]) == 0, capsys.readouterr().err
    assert "reader prose carries no audit mechanics" in capsys.readouterr().out


def test_a_removed_hash_can_be_looked_up_in_its_structured_home() -> None:
    """The revision the owner's example named is still in the packet that retained it."""
    homes = ceremony.retained("c8b36419")
    assert "packing/resources/web/evand-square-packing-2026-09-26/README.md" in homes
    report, homeless = ceremony.retention_report(
        ["c8b36419", "0123456789abcdef0123456789abcdef"]
    )
    assert homeless == ["0123456789abcdef0123456789abcdef"]
    assert "NOT RETAINED outside prose" in report
