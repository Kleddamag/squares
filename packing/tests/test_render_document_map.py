"""The synopsis document map takes each document's own title, as the formatter writes it."""

from __future__ import annotations

from pathlib import Path

from devtools import render_document_map

APOSTROPHE = "\N{RIGHT SINGLE QUOTATION MARK}"


def test_a_raw_titles_apostrophe_is_written_as_the_formatter_writes_it(tmp_path: Path) -> None:
    """A review stored as its reviewer wrote it is left raw by the formatter, and its H1
    keeps a straight apostrophe; the synopsis is formatted, so the map writes the
    typographic one, or it would drift from the synopsis on every commit."""
    path = tmp_path / "review.md"
    path.write_text("# Review: wand125's `s(18)` and the authors' 'net'\n\nBody.\n")
    expected = f"Review: wand125{APOSTROPHE}s `s(18)` and the authors' 'net'"
    assert render_document_map.title(path) == expected
    path.write_text(f"# A title{APOSTROPHE}s own typography\n")
    assert render_document_map.title(path) == f"A title{APOSTROPHE}s own typography"
