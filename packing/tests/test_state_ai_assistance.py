# ruff: noqa: RUF001 -- the records under test are prose with curly apostrophes.
"""The sentence a case record owes a source that says AI assisted its work.

`devtools.state_ai_assistance` finds the paragraph that describes the source's result and
appends the source's statement to it. The rules are tested over small hand-written
records, and the committed records are held to having every statement they owe, less a
named list that only shrinks.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from devtools import state_ai_assistance as assistance
from sqpack.yamlio import safe_load

REPO = Path(__file__).resolve().parents[2]

WAND125 = assistance.STATEMENTS[0]
TOKOHARU = assistance.STATEMENTS[1]

#: Records still owing a statement. Empty since the n = 68 to 95 records took their
#: wand125 sentence on 2026-09-29, and it may only stay empty: a record added here is a
#: statement not made.
PENDING: frozenset[str] = frozenset()


def _record(front: str, body: str) -> str:
    return f"---\n{front}\n---\n{body}"


INTAKE = """# `s(42)` — open

**External intake, 2026-09-28.** wand125’s
rectangle-density source reports `s(42) >= 679/100`,
accepted by Tokoharu’s unchanged interval checker.

| a table | naming wand125 |
| --- | --- |

```
wand125 in a code block
```

Open.
"""


def test_prose_paragraphs_leave_out_headings_tables_code_and_comments() -> None:
    _, lines = assistance.split_record(_record("x: 1", INTAKE))
    texts = [paragraph.text for paragraph in assistance.paragraphs(lines)]
    assert texts == [
        (
            "**External intake, 2026-09-28.** wand125’s rectangle-density source reports "
            "`s(42) >= 679/100`, accepted by Tokoharu’s unchanged interval checker."
        ),
        "Open.",
    ]


def test_the_statement_is_appended_to_the_paragraph_that_describes_the_source() -> None:
    text = _record("sources:\n  - key: '[wand125 rectangle bounds 2026-09-28]'", INTAKE)
    stated = assistance.state(text)
    assert (
        "accepted by Tokoharu’s unchanged interval checker.\n" + WAND125.sentence + "\n\n| a"
    ) in stated
    assert assistance.state(stated) == stated


def test_a_checker_run_on_someone_else_s_certificate_is_not_its_author_s_result() -> None:
    """Tokoharu's checker accepted wand125's certificate; that paragraph owes wand125 only."""
    text = _record("sources:\n  - key: '[Tokoharu density 2026]'", INTAKE)
    _, lines = assistance.split_record(text)
    assert [
        (statement, paragraph)
        for statement, paragraph, _ in assistance.owed("[Tokoharu density 2026]", lines)
    ] == [(TOKOHARU, None)]
    assert assistance.state(text) == text


def test_a_record_that_does_not_cite_the_source_owes_nothing() -> None:
    text = _record("sources: []", INTAKE)
    assert assistance.state(text) == text


def test_a_marker_already_in_the_paragraph_is_the_statement_made() -> None:
    said = INTAKE.replace(
        "unchanged interval checker.",
        "unchanged interval checker.\nParts had AI assistance under human direction.",
    )
    text = _record("sources:\n  - key: '[wand125 point bounds 2026]'", said)
    assert assistance.state(text) == text


def test_every_committed_record_makes_the_statements_it_owes() -> None:
    missing, _ = assistance.report(assistance.records(None))
    assert {label.split(":", 1)[0] for label in missing} <= PENDING


def _bibliography() -> list[dict]:
    return safe_load(assistance.BIBLIOGRAPHY.read_text(encoding="utf-8"))["sources"]


def test_every_statement_quotes_its_source_where_the_source_says_it() -> None:
    """The quote is the source's own words, in the retained file the entry names."""
    stated = [source for source in _bibliography() if source.get("ai_assistance")]
    assert stated, "premise: the bibliography records statements"
    for source in stated:
        said = source["ai_assistance"]
        quote = " ".join(said["quote"].split())
        assert quote in " ".join(said["statement"].split()), source["key"]
        where = REPO / said["where"]
        assert where.is_file(), f"{source['key']}: {said['where']} is not retained"
        text = " ".join(where.read_text(encoding="utf-8").split())
        assert quote in text, f"{source['key']}: {said['where']} does not say {quote!r}"


def test_the_statements_are_read_from_the_bibliography() -> None:
    """One home: every key a statement names carries it there, word for word."""
    by_key = {source["key"]: source for source in _bibliography()}
    for statement in assistance.STATEMENTS:
        for key in statement.keys:
            assert assistance.said(by_key[key]) == (statement.sentence, statement.marker)


def test_a_statement_with_no_anchor_is_refused_rather_than_left_unsaid() -> None:
    sources = [
        *_bibliography(),
        {
            "key": "[Somebody 2026]",
            "ai_assistance": {"statement": "It says AI helped.", "quote": "AI helped"},
        },
    ]
    with pytest.raises(ValueError, match=r"\[Somebody 2026\]: AI assistance stated"):
        assistance.load_statements(sources)
