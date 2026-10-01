# ruff: noqa: RUF001 -- the fixtures are mathematical Unicode: en dashes, minus signs, Greek.
"""Controls for the code-span-to-LaTeX migration in `devtools.migrate_math`.

The tool's claims are that it converts mathematics and nothing else, that every
conversion says what the code span said (relations exactly, fractions in the style the
context wants), and that nothing it writes is read differently by kpress, KaTeX or the
pinned formatter. Each is pinned here: the classification table in both directions, the
contexts that must stay untouched, the kpress parse of every conversion, idempotence,
and the refusals. The formatter itself is never run, as in `test_check_math_spans`: it is
a pinned `uvx` runner, so the refusal is driven through an injected span check.
"""

from __future__ import annotations

import json
import re
import shutil
import textwrap
from collections import Counter
from pathlib import Path

import pytest

from devtools import migrate_math
from devtools.check_github_math import PROBE, probe_cases
from devtools.check_math_spans import FileResult
from devtools.migrate_math import (
    HEADING,
    SpanSafety,
    classify,
    demote_unsafe,
    flowmark_safety,
    github_safe_tex,
    github_unsafe_math,
    kpress_math,
    main,
    markdown_math,
    plain,
    plan,
    prove,
    register_latex,
    rewrite,
    to_latex,
)

# Every example the spec names, with the rule that decides it and its running-text LaTeX.
MATH = (
    ("s(11) ≥ 3.8269975…", "bound in s(n)", r"s(11) \ge 3.8269975\ldots"),
    ("s(21) = 5", "bound in s(n)", "s(21) = 5"),
    ("s(17) > 116511/25000", "bound in s(n)", "s(17) > 116511/25000"),
    ("s(11)", "s(n)", "s(11)"),
    ("31/8", "fraction", "31/8"),
    ("381/100", "fraction", "381/100"),
    ("3.875", "number", "3.875"),
    ("3.8264474…", "number", r"3.8264474\ldots"),
    ("−0.1747", "number", "-0.1747"),
    ("45°", "number", r"45^\circ"),
    ("1,039,500", "number", "1{,}039{,}500"),
    ("2 + (1/2)√2", "formula", r"2 + (1/2)\sqrt{2}"),
    ("2 + 4/√5", "formula", r"2 + 4/\sqrt{5}"),
    ("k² − 4", "formula", "k^2 - 4"),
    ("7/2+√7/2", "formula", r"7/2+\sqrt{7}/2"),
    ("n", "variable", "n"),
    ("k", "variable", "k"),
    ("θᵢ", "variable", r"\theta_i"),
    ("oᵢₖ,ₓ", "variable", "o_{ik,x}"),
    ("s*", "variable", r"s^{\ast}"),
    ("n = 11", "case or range", "n = 11"),
    ("n = 1…100", "case or range", r"n = 1\ldots100"),
    ("n = 18–95", "case or range", r"n = 18\text{–}95"),
    ("ℚ(α)", "formula", r"\mathbb{Q}(\alpha)"),
    ("ℝ²", "formula", r"\mathbb{R}^2"),
    ("10^22", "formula", "10^{22}"),
    ("8^C(n,2)", "formula", "8^{C(n,2)}"),
    ("10⁻⁹", "formula", "10^{-9}"),
    ("θᵣ = 2 arctan(tᵣ)", "formula", r"\theta_r = 2 \arctan(t_r)"),
    ("λ = min(t − 1/2, 3/2 − t)", "formula", r"\lambda = \min(t - 1/2, 3/2 - t)"),
    ("x≥y", "formula", r"x\ge y"),
    ("{0°, 45°}", "formula", r"\lbrace0^\circ, 45^\circ\rbrace"),
    ("ℝ^(3n+1)", "formula", r"\mathbb{R}^{3n+1}"),
    ("K_κ", "formula", r"K_{\kappa}"),
    ("oᵢₖ,ᵧ", "formula", r"o_{ik,\gamma}"),
    # `<` before a letter is spaced, so no parser can take it for an HTML tag.
    ("x<y", "formula", "x< y"),
    (
        "(xᵢ, yᵢ) + Rᵢ·(±½, ±½)",
        "formula",
        r"(x_i, y_i) + R_i\cdot(\pm\tfrac{1}{2}, \pm\tfrac{1}{2})",
    ),
    # A difference of two letters stays arithmetic beside the padded-label rule, a ratio
    # of two beside the label-list rule, and a decimal with its zero stays a number beside
    # the zero-less one.
    ("y-x", "formula", "y-x"),
    ("L/B", "formula", "L/B"),
    ("0.8", "number", "0.8"),
)

IDENTIFIERS = (
    ("T-018", "record id"),
    ("E-n011-…", "record id"),
    ("H-236", "record id"),
    ("X-027", "record id"),
    ("BC-241", "record id"),
    ("T-", "id prefix"),
    ("R068", "rung or label"),
    ("V4", "rung or label"),
    ("C3", "rung or label"),
    ("S5", "rung or label"),
    ("V4/C3", "rung or label"),
    ("V0/C0", "rung or label"),
    ("V", "rung axis"),
    ("packing/frontier/results.yaml", "path"),
    ("frontier/", "path"),
    ("Witness/v2", "path"),
    ("*.md", "path"),
    ("n-*/", "glob"),
    ("packing-validate --fast", "command"),
    ("python -m devtools.migrate_math", "command"),
    ("uv run pytest", "command"),
    ("-W", "command"),
    ("load_records()", "snake_case"),
    ("render(x)", "function call"),
    ("beat_record: true", "code punctuation"),
    ("sqpack.verify", "dotted name"),
    ("8b450a1", "commit hash"),
    ("909efafa+sha256-9c90a04e5691f168", "digest"),
    ("v0.4.2", "version"),
    ("v0.4.2-a48ad1", "version"),
    ("2026-09-22", "date"),
    ("03:18:37Z", "time"),
    ("apparently-novel", "kebab-case name"),
    ("n-011", "kebab-case name"),
    ("key: 'value'", "code punctuation"),
    ("[a, b]{.class}", "code punctuation"),
    (".flowmarkignore", "dotfile"),
    ("4.4e-16", "float literal"),
    ("verified", "word"),
    ("C.3", "label"),
    ("T5-01/0000", "label"),
    ("m1:j5", "label"),
    (":1748", "code punctuation"),
    ("H-00x → H-01x", "record id"),
    ("gpt-5.6-sol", "kebab-case name"),
    ("converged=True", "code punctuation"),
    ("Evidence<T>", "code punctuation"),
    ("[David Ellsworth]", "prose"),
    ("T+0", "time"),
    ("et al.", "prose"),
    # The overview branch's protections (3eebc2bdf): a list of three one-letter labels, a
    # padded one-letter label, and a lone label, which is a word.
    ("P/Q/E", "label list"),
    ("x-010", "kebab-case name"),
    ("f64", "word"),
)

UNCERTAIN = (
    ("s(11) >= 381/100", "ASCII relation"),
    ("Q(sqrt 2)", "ASCII sqrt"),
    ("n = 1..324", "ASCII ellipsis or range"),
    ("31/8 + 1e-8", "float literal in an expression"),
    ("81898608", "long digit string"),
    ("124:14", "colon between digits"),
    ("1.28 ms", "number with a unit"),
    ("1.38x", "number with a unit"),
    ("S", "rung axis or variable"),
    ("…", "a lone character"),
    ("≥", "a lone character"),
    ("sin", "bare function name"),
    ("contact + closure", "no LaTeX form"),
    # The overview branch's protections (3eebc2bdf): a label or a flat subscript inside a
    # formula, counts between slashes, and a decimal as its source prints it.
    ("f1 … f6", "label in an expression"),
    ("D4 x S3", "label in an expression"),
    ("Q0=[0,1]^2", "label in an expression"),
    ("x1 + x2", "label in an expression"),
    ("0/1/0", "slash sequence"),
    ("8/6/8", "slash sequence"),
    (".8", "decimal without its zero"),
    (".79", "decimal without its zero"),
    ("", "empty"),
)


@pytest.mark.parametrize(("source", "rule", "latex"), MATH)
def test_math_converts_to_the_expected_latex(source: str, rule: str, latex: str) -> None:
    verdict = classify(source)
    assert verdict.kind == "math", verdict
    assert verdict.rule == rule
    assert verdict.latex == latex


@pytest.mark.parametrize(("source", "rule"), IDENTIFIERS)
def test_identifiers_stay_code(source: str, rule: str) -> None:
    verdict = classify(source)
    assert verdict.kind == "identifier", verdict
    assert verdict.rule == rule
    assert verdict.latex is None


@pytest.mark.parametrize(("source", "rule"), UNCERTAIN)
def test_uncertain_spans_are_left_with_a_reason(source: str, rule: str) -> None:
    verdict = classify(source)
    assert verdict.kind == "uncertain", verdict
    assert verdict.rule == rule
    assert verdict.reason
    assert verdict.latex is None


@pytest.mark.parametrize(
    ("source", "latex"),
    [
        ("31/8", r"\frac{31}{8}"),
        ("s(17) > 116511/25000", r"s(17) > \frac{116511}{25000}"),
        ("2 + (1/2)√2", r"2 + \frac{1}{2}\sqrt{2}"),
        ("7/2+√7/2", r"\frac{7}{2}+\sqrt{7}/2"),
        # Parentheses that mean application or multiplication stay.
        ("s(1/2)", r"s(\frac{1}{2})"),
        ("2(1/2)", r"2(\frac{1}{2})"),
        # A case written with a slash names two cases, not a fraction.
        ("n = 68/69", "n = 68/69"),
        # A decimal and a chain are not integer fractions. (A chain of integers alone,
        # `1/2/3`, is not math at all: it is a slash sequence, left as code.)
        ("3.5/2", "3.5/2"),
        ("x/2/3", "x/2/3"),
    ],
)
def test_table_and_display_form_uses_frac(source: str, latex: str) -> None:
    assert classify(source, frac=True).latex == latex


def test_every_relation_is_kept_exactly_as_written() -> None:
    """A strict bound never becomes non-strict, nor the reverse."""
    for source, relation in (
        ("s(17) > 4.66", ">"),
        ("s(17) ≥ 4.66", r"\ge"),
        ("s(11) < 4", "<"),
        ("s(11) ≤ 4", r"\le"),
        ("s(21) = 5", "="),
        ("x ≠ y", r"\ne"),
        ("a ≈ 3.8288", r"\approx"),
    ):
        latex = to_latex(source)
        others = {">", r"\ge", "<", r"\le", r"\ne", r"\approx"} - {relation}
        assert relation in latex, (source, latex)
        assert not any(other in latex for other in others if other != "="), (source, latex)


@pytest.mark.parametrize(
    "source",
    [
        "3.8770835…",
        "31/8 = 3.875",
        "3.875 < s(11) ≤ 3.8770835…",
        "s(12) ≥ 99/25",
        "2 + 4/√5",
        "1 + 5√2/4",
        "√(2 + √2)",
        "α = 1/m",
        "x ≠ y ± 0.5",
    ],
)
def test_a_figure_reads_back_from_its_latex(source: str) -> None:
    """A checker reading a migrated figure sees what was written, in either style."""
    for frac in (False, True):
        assert plain(to_latex(source, frac=frac)) == source, (source, frac)


#: The GitHub probe, and the sections of it that are about where a formula sits rather than
#: what it holds.
GITHUB_PROBE = migrate_math.REPO / PROBE
PLACEMENT_SECTIONS = ("## Before the Opening Dollar", "## After the Closing Dollar",
                      "## Inside Inline Markup")  # fmt: skip


def _placement_cases() -> list[tuple[int, str]]:
    """Each placement case's number and recorded outcome."""
    text = GITHUB_PROBE.read_text(encoding="utf-8")
    placement = text[text.index(PLACEMENT_SECTIONS[0]) : text.index("## Inside the Formula")]
    numbers = {int(n) for n in re.findall(r"c_\{(\d+)\}", placement)}
    return [
        (case.number, case.recorded or "")
        for case in probe_cases(text)
        if case.number in numbers
    ]


def test_every_placement_github_leaves_as_dollars_stays_code() -> None:
    """The probe's record, against the plan: a span in each context GitHub was measured
    to leave as dollars is kept as code, and one in each context it draws is converted.

    Every case's formula becomes the code span `` `k` `` in place, so the characters
    around it and the markup it sits in are the probe's own.
    """
    text = GITHUB_PROBE.read_text(encoding="utf-8")
    numbers = re.findall(r"\$c_\{(\d+)\}\$", text)
    as_code = re.sub(r"\$c_\{(\d+)\}\$", "`k`", text)
    decisions = [d for d in plan(as_code).decisions if d.span.content == "k"]
    assert len(decisions) == len(numbers)
    converts = dict(
        zip((int(n) for n in numbers), (d.converts for d in decisions), strict=True)
    )
    wrong = {
        number: recorded
        for number, recorded in _placement_cases()
        if converts[number] != (recorded == "math")
    }
    assert wrong == {}


def test_every_formula_github_alters_holds_what_to_latex_never_writes() -> None:
    """`[altered]` cases are TeX GitHub rewrites: each holds a backslash before ASCII
    punctuation, which `to_latex` refuses to write."""
    altered = [
        c for c in probe_cases(GITHUB_PROBE.read_text("utf-8")) if c.recorded == "altered"
    ]
    assert altered
    for case in altered:
        assert re.search(r"\\[^A-Za-z]", case.tex), case


def test_every_escape_github_alters_is_rewritten_and_every_safe_formula_left_alone() -> None:
    """The probe's `[altered]` formulas come out of `github_safe_tex` with no escape GitHub
    strips, unless they hold one with no safe form; its `[math]` formulas come out as they
    went in, stars aside."""
    cases = probe_cases(GITHUB_PROBE.read_text("utf-8"))
    for case in cases:
        safe, left = github_safe_tex(case.tex)
        if case.recorded == "math":
            # A star is always written as `\ast`, which GitHub draws; nothing else moves.
            def stars(tex: str) -> str:
                return tex.replace("{\\ast}", "*").replace("\\ast ", "*").replace("\\ast", "*")

            assert (stars(safe), left) == (stars(case.tex), []), case
        elif case.recorded == "altered":
            assert safe != case.tex or left, case
            assert left or not re.search(r"\\[!-/:-@\[-`{-~]", safe), case


def test_the_safe_forms_are_the_letter_named_commands() -> None:
    assert github_safe_tex(r"\{x\}") == (r"\lbrace x\rbrace", [])
    assert github_safe_tex(r"a\,b\;c\:d\!e") == (
        r"a\thinspace b\thickspace c\medspace d\negthinspace e",
        [],
    )
    assert github_safe_tex(r"\begin{aligned} a &= 1 \\ b &= 2 \end{aligned}") == (
        r"\begin{aligned} a &= 1 \cr b &= 2 \end{aligned}",
        [],
    )
    assert github_safe_tex(r"27\%") == (r"27\%", [r"\%"])
    assert github_safe_tex(r"L_* + a^*b * c") == (r"L_{\ast} + a^{\ast}b \ast c", [])
    assert github_safe_tex(r"\*x") == (r"\*x", [r"\*"])
    assert github_safe_tex(r"a \\[2pt] b")[1] == [r"\\["]


def test_a_rewrite_keeps_its_delimiters_and_a_kept_span_is_never_converted() -> None:
    text = "The set $\\{x\\}$ and\n\n$$\na\\,b\n$$\n\nwith `n = 11` kept.\n"
    safe, changed, left = demote_unsafe(text)
    assert (
        safe
        == "The set $\\lbrace x\\rbrace$ and\n\n$$\na\\thinspace b\n$$\n\nwith `n = 11` kept.\n"
    )
    assert len(changed) == 2
    assert left == []
    assert [d.converts for d in plan(safe).decisions] == [True]
    assert [d.converts for d in plan(safe, keep=frozenset({"n = 11"})).decisions] == [False]


def test_math_github_would_not_draw_goes_back_to_code_when_this_tool_wrote_it() -> None:
    text = (
        "A closed side-$B$ square, the [$n = 7$ case](n.md), *the $n = 11$ one*, "
        "$0.1747$/$0.3839$, and $s(11) \\ge 3.82$ (fine) beside $10^2$–$10^3$ boxes.\n"
    )
    demoted, back, left = demote_unsafe(text)
    assert [item.tex for item in back] == ["B", "n = 7", "n = 11", "0.3839"]
    assert [item.tex for item in left] == ["10^3"]
    assert demoted == (
        "A closed side-`B` square, the [`n = 7` case](n.md), *the `n = 11` one*, "
        "$0.1747$/`0.3839`, and $s(11) \\ge 3.82$ (fine) beside $10^2$–$10^3$ boxes.\n"
    )
    assert [item.tex for item in github_unsafe_math(demoted)] == ["10^3"]


def test_a_formula_ending_in_a_parenthesis_before_a_parenthesis_stays_code() -> None:
    """GitHub left ten of ten such formulas as dollars (the probe's c_87): `(see $s(21)$)`
    shows its dollars, where `(for every $n$)` and `$s(21)$,` are drawn."""
    text = "The bound (see `s(21)`) holds (for every `n`), as `s(21)`, and `(a, b)` too.\n"
    verdicts = [d.verdict for d in plan(text).decisions]
    assert [v.kind for v in verdicts] == ["uncertain", "math", "math", "math"]
    assert verdicts[0].rule == "delimiter adjacency"
    assert "ends in `)`" in verdicts[0].reason
    written = "T-052 ($s(21)$) and ($n$), $s(21)$, and the pair ($(x, y)$).\n"
    demoted, back, left = demote_unsafe(written)
    assert [item.tex for item in back] == ["s(21)", "(x, y)"]
    assert left == []
    assert demoted == "T-052 (`s(21)`) and ($n$), $s(21)$, and the pair (`(x, y)`).\n"
    assert github_unsafe_math(demoted) == []


def test_no_conversion_holds_a_delimiter_or_a_markdown_escape() -> None:
    for source, _rule, _latex in MATH:
        for frac in (False, True):
            latex = to_latex(source, frac=frac)
            assert "$" not in latex
            assert "`" not in latex
            assert re.search(r"\\[^A-Za-z]", latex) is None, latex
            assert re.search(r"<[A-Za-z/!?]", latex) is None, latex


DOCUMENT = textwrap.dedent(
    """\
    ---
    title: A `n = 11` frontmatter value
    ---
    # The `n = 11` case

    The bound `s(11) ≥ 3.8269975…` improves `2 + 4/√5`, for every `n` in `T-018`.

    ```bash
    echo `n = 11` stays in a fence
    ```

    <!-- a comment with `31/8` stays -->

    <!-- BEGIN GENERATED: recent (devtools.render_recent_results) -->
    A generated `s(21) = 5` belongs to its renderer.
    <!-- END GENERATED: recent -->

        an indented `k² − 4` code block

    <div class="note">`31/8` in an HTML block</div>

    | Case | Bound |
    | --- | --- |
    | `n = 17` | `s(17) > 116511/25000` |
    | `|O|` | an orbit |

    Touching: 2`n` and `n`th and $`k`.

    `p = 1` opens a run that ends in 1

    `p = 1` opens a run that ends in words.
    """
)


def test_contexts_that_are_not_prose_are_never_touched() -> None:
    migration_plan = plan(DOCUMENT)
    lines = {decision.span.line for decision in migration_plan.decisions}
    # Frontmatter, fence, comment, indented code and HTML block lines hold no decision.
    for skipped in (2, 9, 12, 18, 20):
        assert skipped not in lines, skipped
    assert migration_plan.generated == 1
    converted = rewrite(DOCUMENT, migration_plan.decisions)
    for kept in (
        "title: A `n = 11` frontmatter value",
        "echo `n = 11` stays in a fence",
        "<!-- a comment with `31/8` stays -->",
        "A generated `s(21) = 5` belongs to its renderer.",
        "    an indented `k² − 4` code block",
        '<div class="note">`31/8` in an HTML block</div>',
    ):
        assert kept in converted, kept


def test_heading_spans_stay_code_as_identifiers() -> None:
    """kpress drops math from a heading's slug, so an anchor would move under its links."""
    heading = next(d for d in plan(DOCUMENT).decisions if d.span.line == 4)
    assert heading.verdict.kind == "identifier"
    assert heading.verdict.reason == HEADING
    assert "# The `n = 11` case" in rewrite(DOCUMENT, plan(DOCUMENT).decisions)
    setext = plan("The `s(11)` case\n===\n\nBody `s(11)`.\n")
    assert [d.verdict.kind for d in setext.decisions] == ["identifier", "math"]


def test_prose_and_table_rows_convert_in_their_own_style() -> None:
    converted = rewrite(DOCUMENT, plan(DOCUMENT).decisions)
    assert r"The bound $s(11) \ge 3.8269975\ldots$ improves $2 + 4/\sqrt{5}$," in converted
    assert "for every $n$ in `T-018`." in converted
    assert r"| $n = 17$ | $s(17) > \frac{116511}{25000}$ |" in converted
    # A `|` inside a table cell's math would split the cell.
    assert "| `|O|` | an orbit |" in converted


def test_a_dollar_that_would_touch_a_word_or_a_dollar_is_refused() -> None:
    decisions = {d.span.text: d.verdict for d in plan(DOCUMENT).decisions if d.span.line == 27}
    assert decisions["n"].kind == "uncertain"
    assert decisions["n"].rule == "delimiter adjacency"
    assert decisions["k"].kind == "uncertain"
    assert "Touching: 2`n` and `n`th and $`k`." in rewrite(DOCUMENT, plan(DOCUMENT).decisions)


def test_math_opening_a_run_that_ends_in_a_digit_is_refused() -> None:
    """kpress's dollarmath reads `src[-1]` at a run's start: `$p = 1$ … 1` is not math."""
    by_line = {d.span.line: d.verdict for d in plan(DOCUMENT).decisions}
    assert by_line[29].kind == "uncertain"
    assert "dollarmath" in by_line[29].reason
    assert by_line[31].kind == "math"
    assert not kpress_math("$p = 1$ opens a run that ends in 1").sources
    assert kpress_math("$p = 1$ opens a run that ends in words.").sources == Counter(
        {"p = 1": 1}
    )


def test_a_pipe_that_splits_a_table_cell_leaves_the_row_alone() -> None:
    row = "| a | b |\n| --- | --- |\n| `|x|^2` and `p = 1` | c |\n"
    verdicts = [d.verdict for d in plan(row).decisions]
    assert [v.kind for v in verdicts] == ["uncertain", "uncertain"]
    assert {v.rule for v in verdicts} == {"split by a table cell"}


def test_kpress_parses_every_conversion_as_one_inline_math_span() -> None:
    migration = prove(Path("fixture.md"), DOCUMENT, safety=None)
    assert not migration.refusals
    expected = Counter(d.verdict.latex or "" for d in migration.plan.converting())
    assert expected.total() == 6
    found = kpress_math(migration.converted).sources
    assert found - kpress_math(DOCUMENT).sources == expected
    assert found.total() == kpress_math(DOCUMENT).sources.total() + expected.total()


def test_a_second_apply_changes_nothing() -> None:
    first = prove(Path("fixture.md"), DOCUMENT, safety=None).converted
    second = prove(Path("fixture.md"), first, safety=None)
    assert second.converted == first
    assert not second.plan.converting()


def test_a_span_kpress_does_not_read_as_math_is_demoted(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real = migrate_math.kpress_math

    def forgetful(text: str) -> migrate_math.KpressMath:
        found = real(text)
        found.sources.pop("n", None)
        return found

    monkeypatch.setattr(migrate_math, "kpress_math", forgetful)
    monkeypatch.setattr(migrate_math, "katex_refusals", lambda _text, _sources: set())
    migration = prove(Path("doc.md"), "For every `n` and `k`.\n", safety=None)
    verdicts = {d.span.text: d.verdict for d in migration.plan.decisions}
    assert verdicts["n"].kind == "uncertain"
    assert verdicts["n"].rule == "the kpress parse"
    assert migration.converted == "For every `n` and $k$.\n"


def test_math_the_rewrite_did_not_write_refuses_the_file(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real = migrate_math.kpress_math

    def inventive(text: str) -> migrate_math.KpressMath:
        found = real(text)
        if "$k$" in text:
            found.sources["invented"] += 1
        return found

    monkeypatch.setattr(migrate_math, "kpress_math", inventive)
    migration = prove(Path("doc.md"), "For every `k`.\n", safety=None)
    assert migration.refusals
    assert "invented" in migration.refusals[0]


def test_a_span_katex_refuses_is_demoted(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        migrate_math, "katex_refusals", lambda _text, sources: {"k"} & set(sources)
    )
    migration = prove(Path("doc.md"), "For every `n` and `k`.\n", safety=None)
    assert migration.converted == "For every $n$ and `k`.\n"


@pytest.mark.skipif(shutil.which("node") is None, reason="the pinned KaTeX runs under Node")
def test_the_pinned_katex_accepts_every_conversion() -> None:
    sources = [to_latex(source, frac=frac) for source, _r, _l in MATH for frac in (False, True)]
    text = "\n\n".join(f"Math ${source}$ here." for source in sources)
    assert migrate_math.katex_refusals(text, sources) == set()


def _broken(_converted: str, name: str) -> SpanSafety:
    return SpanSafety(FileResult(Path(name), 2, 2, 1, 1), (("s(11)", "s(11\n)"),))


def test_a_rewrite_the_formatter_would_break_is_refused() -> None:
    migration = prove(Path("doc.md"), "Here `s(11)` and `n`.\n", safety=_broken)
    assert migration.refusals
    assert "pinned formatter" in migration.refusals[0]
    assert "$s(11)$ became $s(11\n)$" in migration.refusals[0]


def test_the_span_check_is_check_math_spans_own_comparison(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The formatter is replaced; the span reader and the comparison are the real ones."""
    monkeypatch.setattr(
        migrate_math,
        "format_copy",
        lambda path, _command: path.read_text().replace(" + ", "\n+ "),
    )
    outcome = flowmark_safety("A $2 + x$ and $y$.\n", "doc.md", ["flowmark"])
    assert not outcome.result.ok
    assert outcome.result.broken == 1
    assert outcome.changed == (("2 + x", "2\n+ x"),)
    monkeypatch.setattr(migrate_math, "format_copy", lambda path, _command: path.read_text())
    assert flowmark_safety("A $2 + x$.\n", "doc.md", ["flowmark"]).result.ok


def test_apply_refuses_to_write_what_the_formatter_would_break(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "doc.md"
    source.write_text("Here `s(11)` and `n`.\n", encoding="utf-8")
    monkeypatch.setattr(migrate_math, "pinned_safety", lambda _flowmark=None: _broken)
    assert main(["--apply", str(source)]) == 1
    assert source.read_text(encoding="utf-8") == "Here `s(11)` and `n`.\n"


def test_apply_writes_the_proved_rewrite_and_reports(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "doc.md"
    source.write_text("The bound `s(11) ≥ 31/8` for `T-018` at `1e-11`.\n", encoding="utf-8")
    report = tmp_path / "report.json"

    def clean(converted: str, name: str) -> SpanSafety:
        count = converted.count("$") // 2
        return SpanSafety(FileResult(Path(name), count, count, 0, 0))

    monkeypatch.setattr(migrate_math, "pinned_safety", lambda _flowmark=None: clean)
    assert main(["--apply", "--report", str(report), str(source)]) == 0
    assert source.read_text(encoding="utf-8") == (
        "The bound $s(11) \\ge 31/8$ for `T-018` at `1e-11`.\n"
    )
    (entry,) = json.loads(report.read_text(encoding="utf-8"))
    assert entry["counts"] == {"math": 1, "identifier": 2, "uncertain": 0}
    assert entry["conversions"][0]["math"] == r"s(11) \ge 31/8"


def test_without_apply_the_file_is_only_read(tmp_path: Path) -> None:
    source = tmp_path / "doc.md"
    source.write_text("A `31/8` and `sqrt 2`.\n", encoding="utf-8")
    assert main([str(source)]) == 0
    assert source.read_text(encoding="utf-8") == "A `31/8` and `sqrt 2`.\n"


def test_a_renderer_converts_a_markdown_fragment_in_its_cell_style() -> None:
    headline = "`s(17) ≥ 4426213/1000000 = 4.426213`, from a sixteen-point unavoidable set"
    assert markdown_math(headline) == (
        r"$s(17) \ge 4426213/1000000 = 4.426213$, from a sixteen-point unavoidable set"
    )
    assert markdown_math(headline, table=True) == (
        r"$s(17) \ge \frac{4426213}{1000000} = 4.426213$, from a sixteen-point unavoidable set"
    )
    # A cell that opens with math and ends in a digit is one kpress would print as dollars.
    quirk = "`s(18) ≥ 4426213/1000000`, by monotonicity from T-001"
    assert markdown_math(quirk, table=True) == quirk


def test_a_register_literal_renders_as_latex() -> None:
    assert register_latex("s(11) >= 381/100") == r"s(11) \ge 381/100"
    assert register_latex("s(11) >= 381/100", frac=True) == r"s(11) \ge \frac{381}{100}"
    assert register_latex("2 + 4/sqrt(5) = 3.788854...") == r"2 + 4/\sqrt{5} = 3.788854\ldots"
    assert register_latex("955000*sqrt(518400042893309449)/179696714646249") == (
        r"955000\cdot\sqrt{518400042893309449}/179696714646249"
    )
    assert register_latex("sqrt(17 - 2*floor(sqrt(17)) + 1) + 1") == (
        r"\sqrt{17 - 2\cdot\lfloor\sqrt{17}\rfloor + 1} + 1"
    )
    assert register_latex("ceil(sqrt(n))^2") == r"\lceil\sqrt{n}\rceil^{2}"
    with pytest.raises(migrate_math.UnconvertibleError, match="the word"):
        register_latex("s(11) >= 381/100, by a certificate")


def test_only_a_renderer_owned_block_is_skipped_and_a_quoted_marker_is_text() -> None:
    text = textwrap.dedent(
        """\
        Blocks sit between `<!-- BEGIN GENERATED: … -->` markers, and `n = 3` is prose.

        <!-- BEGIN CURRENT-RESEARCH-READINESS -->
        A hand-written dashboard at `n = 5`.
        <!-- END CURRENT-RESEARCH-READINESS -->

        <!-- BEGIN GENERATED: table (devtools.render_research_tables) -->
        A rendered `n = 7`.
        <!-- END GENERATED: table -->
        """
    )
    migration_plan = plan(text)
    converted = rewrite(text, migration_plan.decisions)
    assert "`<!-- BEGIN GENERATED: … -->` markers, and $n = 3$ is prose." in converted
    assert "A hand-written dashboard at $n = 5$." in converted
    assert "A rendered `n = 7`." in converted
    assert migration_plan.generated == 1
