"""The math-markup migration: classification, rewriting, and the ratchet that holds it."""

# ruff: noqa: RUF001 -- the fixtures are the mathematical Unicode the tool reads.

from pathlib import Path

import pytest

from devtools import check_math_markup, migrate_math
from devtools.migrate_math import (
    Keep,
    analyze,
    classify,
    code_spans,
    kpress_parser,
    load_ledger,
    math_inline,
    migrate,
    to_latex,
    verify_kpress,
)

REPO = Path(__file__).resolve().parents[2]

MATH = {
    "s(11) ≥ 381/100": r"s(11) \ge 381/100",
    "s(11) >= 191/50": r"s(11) \ge 191/50",
    "3.875 < s(11) ≤ 3.8770835…": r"3.875 < s(11) \le 3.8770835\ldots",
    "2 + 4/√5": r"2 + 4/\sqrt{5}",
    "1 + 5sqrt(2)/4": r"1 + 5\sqrt{2}/4",
    "k² − 4": r"k^2 - 4",
    "s(n) ≤ ⌈√n⌉": r"s(n) \le \lceil \sqrt{n} \rceil",
    "ceil(sqrt(n))^2": r"\lceil \sqrt{n} \rceil^2",
    "31/8": "31/8",
    "3.8269975…": r"3.8269975\ldots",
    "n": "n",
    "k": "k",
    "L": "L",
    "α": r"\alpha",
    "a*": r"a^{\ast}",
    "n = 11": "n = 11",
    "4": "4",
    "1e-11": "10^{-11}",
    "2.2e-15": r"2.2 \times 10^{-15}",
    "45°": r"45^{\circ}",
    "θᵢ ∈ [0, π/2)": r"\theta_i \in [0, \pi/2)",
    "oᵢₖ,ₓ": "o_{ik,x}",
    "ℝ^(3n+1)": r"\mathbb{R}^{3n+1}",
    "|O|": r"\lvert O\rvert",
    "{S ≤ U}": r"\lbrace S \le U\rbrace",
    "ℚ(α)": r"\mathbb{Q}(\alpha)",
    "n = 39–41": r"n = 39\text{–}41",
    "2 + ½√2": r"2 + \tfrac{1}{2}\sqrt{2}",
}

IDENTIFIERS = {
    "T-018": "record-id",
    "E-n011-repaired-lower": "record-id",
    "BC-NNN": "placeholder-id",
    "V4": "label",
    "V4/C3": "label",
    "S5": "label",
    "think-07t7": "slug-id",
    "n-011": "slug-id",
    "packing/frontier/n-011.md": "path",
    "README.md": "file",
    "--apply": "flag",
    "uv run --frozen python -m devtools.check_synopsis": "flag",
    "packing-validate": "slug-id",
    "sqpack.fractional": "dotted-name",
    "verified_lower_bound": "word-or-name",
    "ResultsRegister/v1": "path",
    "AgentSession": "word-or-name",
    "9cca493c17ab61d5efb3e1032f32c54a9b87320e": "hash",
    "v0.4.2": "version",
    "status: enforced": "key-value",
    "1.28 ms": "measurement",
    "<figure>": "html",
    "f64": "label",
}

UNCERTAIN = {
    "Feas(s)": "no-math-signal",
    "best_side − standing_best": "snake-name-in-expression",
    "28696526": "long-integer",
    "f1 … f6": "label-in-expression",
    "8^C(n,2)": "ambiguous-superscript",
    "…": "no-operand",
    "0/1/0": "slash-sequence",
    "closure(G) = [C, G, M]": "named-term",
}


@pytest.mark.parametrize(("source", "latex"), MATH.items())
def test_mathematics_is_classified_and_written_as_latex(source: str, latex: str) -> None:
    verdict = classify(source)
    assert verdict.kind == "math", verdict
    assert verdict.latex == latex


@pytest.mark.parametrize(("source", "rule"), IDENTIFIERS.items())
def test_identifiers_stay_code(source: str, rule: str) -> None:
    verdict = classify(source)
    assert verdict.kind == "identifier"
    assert verdict.rule == rule


@pytest.mark.parametrize(("source", "rule"), UNCERTAIN.items())
def test_uncertain_spans_are_left_for_a_person(source: str, rule: str) -> None:
    verdict = classify(source)
    assert verdict.kind == "uncertain"
    assert verdict.rule == rule


def test_the_translator_refuses_what_it_cannot_write() -> None:
    with pytest.raises(migrate_math.UnconvertibleError, match="unpaired-bar"):
        to_latex("|x")
    with pytest.raises(migrate_math.UnconvertibleError, match="named-term"):
        to_latex("area + 1")
    with pytest.raises(migrate_math.UnconvertibleError, match="character"):
        to_latex("a # b")


FIXTURE = """\
# Heading about `n = 11`

The bound `s(11) ≥ 381/100` holds, see `T-018` and `packing/frontier/n-011.md`.
A variable `k` and a command `uv run --frozen pytest`, and [`s(12)`](x.md) in a link.

```text
s(11) >= 381/100 and `n` inside a fence
```

    `31/8` in an indented code block

<!-- BEGIN GENERATED: something (devtools.render_something) -->
The renderer owns `s(13) = 4` here.
<!-- END GENERATED: something -->

| Case | Bound |
| --- | --- |
| `n = 17` | `s(17) > 116511/25000` |

A word`n`touching and a span `s(20)
≥ 97/20` across a line.
"""


def test_the_fixture_converts_only_convertible_math() -> None:
    after, findings = migrate(FIXTURE)
    assert "The bound $s(11) \\ge 381/100$ holds, see `T-018` and" in after
    assert "A variable $k$ and a command `uv run --frozen pytest`" in after
    assert "| $n = 17$ | $s(17) > 116511/25000$ |" in after
    rules = {finding.span.content: finding.rule for finding in findings}
    assert rules["n = 11"] == "math-but-heading"
    assert rules["s(12)"] == "math-but-link-text"
    assert rules["n"] == "math-but-adjacent"
    assert rules["s(20) ≥ 97/20"] == "math-but-line-break"


def test_code_blocks_comments_and_generated_regions_are_never_read() -> None:
    contents = [span.content for span in code_spans(FIXTURE)]
    assert "31/8" not in contents
    assert "s(13) = 4" not in contents
    after, _ = migrate(FIXTURE)
    assert "s(11) >= 381/100 and `n` inside a fence" in after
    assert "    `31/8` in an indented code block" in after
    assert "The renderer owns `s(13) = 4` here." in after


def test_applying_twice_changes_nothing() -> None:
    once, _ = migrate(FIXTURE)
    twice, findings = migrate(once)
    assert twice == once
    assert not any(finding.converts for finding in findings)


def test_kpress_reads_every_conversion_back_as_the_math_written() -> None:
    after, findings = migrate(FIXTURE)
    assert verify_kpress(FIXTURE, after, findings) == []
    assert math_inline(after)[r"s(11) \ge 381/100"] == 1


def test_the_backtick_dollar_form_is_not_math_to_kpress() -> None:
    """Why the tool writes `$...$` and never GitHub's `` $`...`$ `` alternative."""
    assert math_inline("See $`x`$ here.") == {"`x`": 1}
    assert math_inline("See $x$ here.") == {"x": 1}
    assert math_inline("2$x$ and $x$2") == {}


def test_the_kpress_parser_options_are_the_ones_kpress_passes() -> None:
    source = (REPO / "vendor/kpress/src/kpress/format/markdown.py").read_text(encoding="utf-8")
    assert "dollarmath_plugin, allow_space=False, allow_digits=False" in source
    assert kpress_parser().parse("$a$")[1].children[0].type == "math_inline"  # type: ignore[index]


def test_a_leading_span_in_a_cell_ending_in_a_digit_stays_code() -> None:
    """dollarmath reads `src[-1]` before an opening `$` at position 0."""
    table = "| a | b |\n| --- | --- |\n| `μ(K) = 10.86`, below 11 | x |\n"
    assert math_inline("| a | b |\n| --- | --- |\n| $x$, below 11 | y |\n") == {}
    (finding,) = analyze(table)
    assert finding.rule == "math-but-kpress-leading-dollar"
    assert migrate(table)[0] == table


def test_a_table_cell_writes_bars_that_cannot_split_it() -> None:
    table = "| a | b |\n| --- | --- |\n| x | `⌊|S|/k⌋` |\n"
    assert classify("⌊|S|/k⌋").latex == r"\lfloor \lvert S\rvert/k \rfloor"
    # The pipe inside the code span already splits the cell, so the parser and the raw
    # scan disagree and the span is reported rather than rewritten.
    assert migrate(table)[0] == table


def test_kept_spans_stay_code_everywhere_or_only_where_named() -> None:
    text = "The `V` and `C` axes.\n\nFix a cell `C` and a set `S`.\n"
    everywhere = migrate(text, [Keep("V"), Keep("C")])[0]
    assert everywhere == "The `V` and `C` axes.\n\nFix a cell `C` and a set $S$.\n"
    scoped = migrate(text, [Keep("V"), Keep("C", "axes")])[0]
    assert scoped == "The `V` and `C` axes.\n\nFix a cell $C$ and a set $S$.\n"


def test_the_ledger_is_read_with_its_scoped_exceptions(tmp_path: Path) -> None:
    ledger = tmp_path / "ledger.yaml"
    ledger.write_text(
        "files:\n  a.md:\n    keep:\n      - V\n      - {span: C, where: axes}\n  b.md: {}\n"
    )
    assert load_ledger(ledger) == {"a.md": (Keep("V"), Keep("C", "axes")), "b.md": ()}
    ledger.write_text("files:\n  a.md:\n    keep:\n      - {where: axes}\n")
    with pytest.raises(TypeError, match="keep entry"):
        load_ledger(ledger)


def test_the_ratchet_fails_a_migrated_file_with_math_in_code(tmp_path: Path) -> None:
    (tmp_path / "done.md").write_text("Here $s(11) \\ge 31/8$ and the `V` ladder.\n")
    (tmp_path / "later.md").write_text("Not yet: `s(11) ≥ 31/8`.\n")
    ledger = {"done.md": (Keep("V"),)}
    assert check_math_markup.problems(ledger, tmp_path) == []

    (tmp_path / "done.md").write_text("A regression: `s(11) ≥ 31/8`, and `V`.\n")
    (problem,) = check_math_markup.problems(ledger, tmp_path)
    assert problem.startswith("done.md:1: math written as code `s(11) ≥ 31/8`")
    assert problem.endswith("write $s(11) \\ge 31/8$")


def test_the_ratchet_refuses_a_stale_exception_or_a_missing_file(tmp_path: Path) -> None:
    (tmp_path / "done.md").write_text("Nothing kept here.\n")
    found = check_math_markup.problems({"done.md": (Keep("V"),), "gone.md": ()}, tmp_path)
    assert found == [
        "done.md: keeps `V`, which no math-like span there matches any more",
        "gone.md: listed in math-migrated.yaml but not a Markdown file here",
    ]


def test_the_repository_ledger_holds() -> None:
    assert check_math_markup.problems(load_ledger()) == []
    assert check_math_markup.main([]) == 0


def test_apply_writes_only_what_both_measurements_pass(tmp_path: Path) -> None:
    page = tmp_path / "page.md"
    page.write_text("The bound `s(11) ≥ 381/100` and `T-018`.\n")
    # `true` stands in for the formatter: it leaves the copy as it is, so every span
    # survives, and the test measures the tool rather than the pinned flowmark.
    assert migrate_math.main([str(page), "--apply", "--flowmark", "true"]) == 0
    assert page.read_text() == "The bound $s(11) \\ge 381/100$ and `T-018`.\n"
    assert migrate_math.main([str(page), "--apply", "--flowmark", "true"]) == 0
    assert page.read_text() == "The bound $s(11) \\ge 381/100$ and `T-018`.\n"


def test_apply_refuses_when_the_formatter_would_change_a_span(tmp_path: Path) -> None:
    page = tmp_path / "page.md"
    original = "The bound `s(11) ≥ 381/100`.\n"
    page.write_text(original)
    rewrite = tmp_path / "rewrite.sh"
    rewrite.write_text('#!/bin/sh\nsed -i "s/381/382/" "$2"\n')
    rewrite.chmod(0o755)
    assert migrate_math.main([str(page), "--apply", "--flowmark", str(rewrite)]) == 1
    assert page.read_text() == original
