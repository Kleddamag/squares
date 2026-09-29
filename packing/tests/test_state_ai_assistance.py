# ruff: noqa: RUF001 -- the records under test are prose with curly apostrophes.
"""The sentence a case record owes a source that says AI assisted its work.

`devtools.state_ai_assistance` finds the paragraph that describes the source's result and
appends the source's statement to it. The rules are tested over small hand-written
records, and the committed records are held to having every statement they owe, less a
named list that only shrinks.
"""

from __future__ import annotations

from devtools import state_ai_assistance as assistance

WAND125 = assistance.STATEMENTS[0]
TOKOHARU = assistance.STATEMENTS[1]

#: Records another lane owns on 2026-09-29, whose wand125 sentence it writes with
#: `--apply`. The list may only shrink: a record added here is a statement not made.
PENDING = frozenset(
    {
        *(f"n-{n:03d}.md" for n in (68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78)),
        *(f"n-{n:03d}.md" for n in (86, 88, 89, 90, 91, 94, 95)),
    }
)


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
