#!/usr/bin/env python3
# ruff: noqa: RUF001, RUF002, RUF003 -- the subject is mathematical Unicode: en dashes,
# minus signs and Greek letters are the characters this tool reads and converts.
"""Move mathematics written as code spans to LaTeX math, one Markdown file at a time.

Most of this repository's prose writes its mathematics as code: `` `s(11) ≥ 3.8269975…` ``,
`` `31/8` ``, `` `2 + (1/2)√2` ``. GitHub renders `$…$`, kpress renders it with KaTeX on
the site, and the pinned flowmark keeps a math span whole, so the prose can say what it
means. This is the instrument that moves it (`OR-1`): a hand edit of fifteen hundred files
is an edit nobody can re-run or review.

**Every inline code span is classified**, outside fenced and indented code, raw HTML
blocks, HTML comments, YAML frontmatter and the `<!-- BEGIN … -->`/`<!-- END … -->`
blocks a renderer owns (those move at their renderer, never here). A span is one of:

- `identifier` -- literal text that stays code: result, evidence, hypothesis and agenda
  ids (`T-018`, `E-n011-…`, `BC-241`, `R068`), rung labels (`V4`, `V4/C3`), paths and
  globs, commands and flags, dotted and snake_case names, calls such as
  `load_records()`, commit hashes, versions, dates, bare words, and anything carrying
  code punctuation (quotes, backslashes, `==`, a YAML `key: value`).
- `math` -- an expression whose every character has a LaTeX form: a bound or equation in
  `s(n)`, a number or fraction standing as a value, a formula, a variable.
- `uncertain` -- everything else, left untouched and listed with its reason: ASCII
  register literals (`s(11) >= 381/100`, `sqrt`), float literals (`1e-11`), numbers
  with units, words inside a formula, and math whose surroundings make `$…$` unsafe.

`classify` decides from the span's text alone; `plan` then applies its surroundings.
Every span in a heading stays code, as an `identifier`: kpress drops math from a heading's
slug, so converting one would move the anchor under every link to it. A math span
elsewhere stays code, as `uncertain`, when a letter, digit, `$` or backslash touches
either delimiter (kpress's dollarmath refuses a digit beside a `$`, and GitHub's reading
of `$n$th` is not one to depend on), or when its table-cell form would contain a `|`.

**Conversion is to idiomatic LaTeX**, with every relation kept exactly as written (`≥`
is `\\ge`, `>` stays `>`): `≤ ≠ ≈ ± × · ∈ …` become `\\le \\ne \\approx \\pm \\times
\\cdot \\in \\ldots`, `√5` and `√(…)` become `\\sqrt{…}`, `k²` becomes `k^2`, Unicode
subscripts become `_{…}`, `−` becomes `-`, Greek letters become their commands, `°`
becomes `^\\circ`, and an en dash between numbers becomes `\\text{–}`. A fraction keeps
its slash in running text and becomes `\\frac{a}{b}` in a table row or display math, the
style the overview spec recommends. No conversion contains a `$`, a backtick, or a
backslash before ASCII punctuation (`\\{`, `\\,`), which a Markdown parser may take for an
escape before the math renderer sees it: braces are `\\lbrace`/`\\rbrace`, and a marking
star is `^{\\ast}`.

**`--apply` proves each rewrite before writing it**, and writes atomically:

1. kpress parses the result with the site's parser (dollarmath with `allow_space=False`
   and `allow_digits=False`), and every converted span must come back as exactly one
   inline math span its MathML converter accepts. A span that does not is demoted to
   `uncertain` and the plan is proved again; math appearing or vanishing that the tool
   did not write refuses the file, since no single span can be blamed for it.
2. The pinned KaTeX bundle parses every converted span in strict mode
   (`devtools.check_katex`), where Node is available; a refusal demotes the span.
3. `devtools.check_math_spans` formats a copy of the result with the pinned flowmark and
   compares every math span; one that breaks, changes, appears or vanishes refuses the
   write.

Usage, from `packing/`:

    uv run --frozen --all-extras --group dev python -m devtools.migrate_math FILE...
    uv run --frozen --all-extras --group dev python -m devtools.migrate_math --apply FILE...
    ... --list               # also print every conversion, before and after
    ... --report PATH        # also write the report as JSON

Without `--apply` the files are only read. With it, exit 1 if any file was refused.
`devtools.check_math_markup` is the ratchet that keeps a migrated file migrated.

**Generated Markdown is migrated at its renderer**, never by editing the output, and the
renderers share this module's rules through two entry points: `markdown_math` for a
Markdown fragment they did not write (a register `headline`, in running text or as a
table cell), and `register_latex` for an ASCII register literal (`s(11) >= 381/100`,
`2 + 4/sqrt(5) = 3.788854...`), which the register keeps ASCII.
"""

from __future__ import annotations

import argparse
import bisect
import html
import json
import re
import shlex
import shutil
import sys
import tempfile
import unicodedata
from collections import Counter
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field, replace
from functools import cache
from pathlib import Path
from typing import Literal, TypedDict

from markdown_it import MarkdownIt
from strif import atomic_output_file

from devtools.check_math_spans import (
    FileResult,
    format_copy,
    mask_fences,
    math_spans,
    pinned_formatter,
)

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent

Kind = Literal["math", "identifier", "uncertain"]
Where = Literal["text", "heading", "table", "raw"]
KINDS: tuple[Kind, ...] = ("math", "identifier", "uncertain")

# ---------------------------------------------------------------------------------------
# Finding the code spans
# ---------------------------------------------------------------------------------------

#: YAML frontmatter at the very top of a file: data, never prose.
FRONTMATTER = re.compile(r"\A---[ \t]*\n.*?\n(?:---|\.\.\.)[ \t]*(?:\n|\Z)", re.DOTALL)
#: A block a renderer owns, from `<!-- BEGIN GENERATED: … -->` to its `END GENERATED`. Other
#: marked blocks, such as the synopsis's hand-written readiness dashboard, are prose.
GENERATED = re.compile(
    r"<!--\s*BEGIN GENERATED\b[^>]*?-->.*?<!--\s*END GENERATED\b[^>]*?-->", re.DOTALL
)
COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
TICKS = re.compile(r"`+")
BLANK_LINE = re.compile(r"\n[ \t]*\n")


def _blank(text: str) -> str:
    """`text` with every character but its newlines replaced by a space."""
    return "\n".join(" " * len(line) for line in text.split("\n"))


def _matches(
    text: str, pattern: re.Pattern[str], spans: Sequence[CodeSpan] = ()
) -> list[re.Match[str]]:
    """Every match of `pattern` that does not open inside a code span, in order.

    A marker quoted as code (`` `<!-- BEGIN GENERATED: … -->` ``) is text, not a comment,
    since CommonMark reads whichever construct opens first. A match refused for opening
    inside a span is searched again from its next character, so a real comment it
    overlapped is still found.
    """
    starts = [span.start for span in spans]
    found: list[re.Match[str]] = []
    position = 0
    while (match := pattern.search(text, position)) is not None:
        index = bisect.bisect_right(starts, match.start()) - 1
        if index >= 0 and spans[index].start < match.start() < spans[index].end:
            position = match.start() + 1
            continue
        found.append(match)
        position = max(match.end(), match.start() + 1)
    return found


def _mask(text: str, pattern: re.Pattern[str], spans: Sequence[CodeSpan] = ()) -> str:
    """`text` with every match of `pattern` outside a code span blanked."""
    pieces: list[str] = []
    position = 0
    for match in _matches(text, pattern, spans):
        pieces.extend((text[position : match.start()], _blank(match.group(0))))
        position = match.end()
    pieces.append(text[position:])
    return "".join(pieces)


def _only(text: str, pattern: re.Pattern[str], spans: Sequence[CodeSpan] = ()) -> str:
    """`text` with everything but the pattern's matches outside code spans blanked."""
    pieces: list[str] = []
    position = 0
    for match in _matches(text, pattern, spans):
        pieces.extend((_blank(text[position : match.start()]), match.group(0)))
        position = match.end()
    pieces.append(_blank(text[position:]))
    return "".join(pieces)


def mask(text: str) -> tuple[str, str]:
    """The prose of `text` with everything else blanked, and its generated blocks alone.

    Both keep every offset and newline of `text`, so a span found in either sits where it
    sits in the file. Fences go first, so a marker quoted inside a code block never opens
    a generated block.
    """
    code_free = _mask(mask_fences(text), FRONTMATTER)
    quoted = code_spans(code_free) if "<!--" in code_free else []
    prose = _mask(_mask(code_free, GENERATED, quoted), COMMENT, quoted)
    generated = _mask(_only(code_free, GENERATED, quoted), COMMENT, quoted)
    return prose, generated


@dataclass(frozen=True)
class CodeSpan:
    """One inline code span: where its backtick runs sit and what lies between them."""

    start: int
    end: int
    ticks: int
    content: str
    line: int

    @property
    def text(self) -> str:
        """The content a reader sees, without the padding a backtick may need."""
        return self.content.strip()


def _escaped(text: str, index: int) -> bool:
    """Whether the character at `index` follows an odd run of backslashes."""
    backslashes = 0
    while index - backslashes - 1 >= 0 and text[index - backslashes - 1] == "\\":
        backslashes += 1
    return backslashes % 2 == 1


def code_spans(masked: str) -> list[CodeSpan]:
    """Every inline code span in already-masked text, in order.

    The CommonMark rule: a run of n backticks opens a span that the next run of exactly n
    backticks closes. A span never crosses a blank line, and a backslash before the first
    backtick of a run makes that one backtick literal.
    """
    starts = [0, *(match.end() for match in re.finditer("\n", masked))]
    spans: list[CodeSpan] = []
    position = 0
    while (opener := TICKS.search(masked, position)) is not None:
        begin = opener.start()
        if _escaped(masked, begin):
            position = begin + 1
            continue
        width = len(opener.group(0))
        closer = next(
            (run for run in TICKS.finditer(masked, opener.end()) if len(run.group(0)) == width),
            None,
        )
        if closer is None or BLANK_LINE.search(masked, opener.end(), closer.start()):
            position = opener.end()
            continue
        spans.append(
            CodeSpan(
                start=begin,
                end=closer.end(),
                ticks=width,
                content=masked[opener.end() : closer.start()],
                line=bisect.bisect_right(starts, begin),
            )
        )
        position = closer.end()
    return spans


_BLOCKS: dict[str, Where] = {
    "fence": "raw",
    "code_block": "raw",
    "html_block": "raw",
    "heading_open": "heading",
    "table_open": "table",
}


@cache
def _block_parser() -> MarkdownIt:
    # kpress's own preset and options: raw HTML blocks are blocks, not paragraphs.
    parser = MarkdownIt("js-default", {"html": True})
    # Only the block structure is wanted, and inline parsing is most of the cost.
    parser.core.ruler.disable(["inline", "text_join"], ignoreInvalid=True)
    return parser


@dataclass(frozen=True)
class Blocks:
    """A file's block structure, as a CommonMark parser with GFM tables reads it.

    `lines` says what kind of block each line belongs to: `raw` for code and HTML blocks,
    where a backtick is a literal character and no code span exists; `heading` and `table`
    for the blocks that change how a span may be written; `text` for the rest. `runs`
    holds the inline source of every paragraph, heading and table cell, keyed by the
    zero-based line it starts on.
    """

    lines: list[Where]
    runs: dict[int, list[str]]


def block_context(text: str) -> Blocks:
    """Parse `text`'s block structure once, for every span `plan` places."""
    lines: list[Where] = ["text"] * (text.count("\n") + 1)
    runs: dict[int, list[str]] = {}
    for token in _block_parser().parse(text):
        if token.map is None:
            continue
        first, last = token.map
        if token.type == "inline":
            runs.setdefault(first, []).append(token.content)
        where = _BLOCKS.get(token.type)
        if where is None:
            continue
        for index in range(first, min(last, len(lines))):
            if lines[index] != "raw":
                lines[index] = where
    return Blocks(lines, runs)


# ---------------------------------------------------------------------------------------
# Classifying one span's text
# ---------------------------------------------------------------------------------------

EXTENSIONS = (
    "md|py|pyi|yaml|yml|json|jsonl|toml|lock|rs|ts|tsx|js|mjs|cjs|html|css|svg|png|jpg|"
    "jpeg|gif|webp|pdf|mp4|webm|txt|csv|tsv|sh|bash|cfg|ini|tex|bib|ipynb|zip|gz|tar|"
    "whl|log|sql|mmd|dot|woff2?|ttf|otf"
)
COMMANDS = (
    "uv|uvx|python3?|pip|git|gh|make|npm|npx|node|cargo|rustc|tbd|pytest|packing-[a-z]+|"
    "sqsearch|flowmark|ruff|basedpyright|pprose|softschema|bash|sh|cd|ls|cat|grep|rg|curl|"
    "jq|sed|awk|docker|export|source"
)

#: Identifier rules, tried in order on the span's text; the first match decides.
IDENTIFIER_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("url", re.compile(r"[a-z][a-z0-9+.-]*://|^www\.")),
    ("date", re.compile(r"^\d{4}-\d{2}-\d{2}(?:[T ][\d:.]+Z?)?$")),
    # A clock time or a launch-relative time: `03:18:37Z`, `T+0`.
    ("time", re.compile(r"^\d{1,2}:\d{2}(?::\d{2})?(?:\.\d+)?Z?$|^T\+\d+\w*$")),
    (
        "version",
        re.compile(r"^v\d+(?:\.\d+)+(?:[-+.][\w.-]+)?$|^\d+\.\d+\.\d+(?:[-+.][\w.-]+)?$"),
    ),
    # T-018, E-n011-…, H-236, X-027, BC-241, D-397, OR-2, and placeholders such as T-NNN.
    # An id anywhere in the span (`H-00x → H-01x`) makes it about ids, not arithmetic.
    ("record id", re.compile(r"^[A-Z]{1,4}-[A-Za-z0-9][\w.…-]*$|\b[A-Z]{1,4}-\d{2,}")),
    # The prefix of an id family: `T-`, `exp-`, `H-`.
    ("id prefix", re.compile(r"^[A-Za-z]{1,8}-$")),
    # V4, C3, S5, V4/C3, V0/C0, C0–C5, and labels such as R068 and BC303.
    ("rung or label", re.compile(r"^[A-Z]{1,3}\d+[a-z]?(?:\s*[/–-]\s*[A-Z]{1,3}\d+[a-z]?)*$")),
    # Section and run labels: `C.3`, `T5-01/0000`, `m1:j5`.
    (
        "label",
        re.compile(r"^[A-Z]{1,3}\.\d+(?:\.\d+)*$|^[A-Z]{1,3}\d+(?:[-/]\d+)+$|\w:[A-Za-z]"),
    ),
    # The confirmation and verification axes, alone or as `V/C`.
    ("rung axis", re.compile(r"^[VC]$|^[VCSN](?:/[VCSN])+$")),
    # A number printed by a program in exponent form: run output lifted verbatim, which
    # the conventions never retype. In an expression it is left `uncertain` below.
    ("float literal", re.compile(r"^[+\-−]?\d+(?:\.\d+)?[eE][+\-−]?\d+$")),
    ("placeholder", re.compile(r"^<[\w .:/-]+>$")),
    ("html", re.compile(r"^</?[a-z][\w-]*[\s>/]")),
    ("command", re.compile(rf"(?:^|\s)--?[A-Za-z][\w-]*|(?:^|\s)-m\s|^(?:{COMMANDS})(?:\s|$)")),
    ("dotfile", re.compile(r"^\.[A-Za-z]")),
    (
        "path",
        re.compile(
            rf"^[~.]{{0,2}}/|[A-Za-z]{{2,}}[\w.*-]*/|/[\w.*-]*[A-Za-z]{{2,}}|\w/$"
            rf"|\.(?:{EXTENSIONS})(?:[#:?]\S*)?$"
        ),
    ),
    ("glob", re.compile(r"\*\*|\*\.\w|/\*|\*/|[A-Za-z_-]{2,}\*")),
    # A content address or digest: `909efafa+sha256-9c90a04e5691f168`.
    ("digest", re.compile(r"sha\d+[-:]|\b(?=[0-9a-f]*[a-f])(?=[0-9a-f]*\d)[0-9a-f]{8,}\b")),
    (
        "code punctuation",
        re.compile(
            r"""[`'"\\$#@;~&%?]|==|!=|->|=>|::|:=|&&|\|\||^[\w.-]{2,}:(?:\s|$)"""
            r"""|[A-Za-z]{2,}:\S|\w\[|\[\]|\{[.#]|^:\d|[A-Za-z]{2,}<[A-Z]\w*>"""
            r"""|^(?:if|elif|else|for|while|return|def|class|import|from|assert)\b"""
            r"""|\b(?:True|False|None)\b"""
        ),
    ),
    ("dotted name", re.compile(r"[A-Za-z_][\w-]*\.[A-Za-z_]")),
    # A name with an underscore, or a subscript of three letters or more, which reads as a
    # code name (`q_chart`) where `ν_ij` and `P_TR` read as subscripts.
    (
        "snake_case",
        re.compile(r"(?:^|\W)[A-Za-z][A-Za-z0-9]+_\w|(?:^|\W)_\w|\w__\w|_\w*_|_[A-Za-z]{3,}"),
    ),
    ("commit hash", re.compile(r"^(?=[0-9a-f]*[a-f])(?=[0-9a-f]*\d)[0-9a-f]{7,40}$")),
    # exp-001, think-qqzs, apparently-novel, known-best-1-324, and case ids such as n-011.
    # `n-1` is arithmetic, so a kebab name needs a two-letter run or a padded case number.
    (
        "kebab-case name",
        re.compile(r"^(?=.*[A-Za-z]{2})[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9.]+)+$|^n-\d{3}$"),
    ),
)

#: Spans whose LaTeX would silently say something else, or that may be a character named
#: rather than used; tried after the identifiers.
UNCERTAIN_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    # `1e-11` in LaTeX reads as 1·e−11.
    ("float literal in an expression", re.compile(r"\d(?:\.\d+)?[eE][+\-−]?\d")),
    # The register's ASCII form, often quoted as the literal it is.
    ("ASCII relation", re.compile(r">=|<=|=<")),
    ("ASCII sqrt", re.compile(r"\bsqrt\b")),
    ("ASCII ellipsis or range", re.compile(r"\.\.")),
    # A long run of digits is as often an id or an abbreviated hash as a value.
    ("long digit string", re.compile(r"^\d{7,}$")),
    # A position or a time: `124:14`.
    ("colon between digits", re.compile(r"\d:\d")),
    # A measurement: `1.28 ms`, `1369.60 s`, `13.8 GB`, `1.38x`.
    (
        "number with a unit",
        re.compile(r"^[+\-−≈~]?\s*[\d.,]+\s*(?:[µu]s|ms|ns|s|min|h|[KMGT]i?B|B|x|×|%)$"),
    ),
    # `S` names the significance axis, and `N` the novelty axis, as often as a variable.
    ("rung axis or variable", re.compile(r"^[SN]$")),
    # One character alone is as often the character discussed as the symbol used:
    # "maps `…` back to `...`".
    ("a lone character", re.compile(r"^[^\w\s]$")),
)

# Each rule set as one alternation: most spans are identifiers, and one search that finds
# none is how a span skips twenty. The rule that matched is then named by the loop.
_ANY_IDENTIFIER = re.compile(
    "|".join(f"(?:{pattern.pattern})" for _rule, pattern in IDENTIFIER_RULES)
)
_ANY_UNCERTAIN = re.compile(
    "|".join(f"(?:{pattern.pattern})" for _rule, pattern in UNCERTAIN_RULES)
)

MATH_FUNCTIONS = frozenset({
    "sin", "cos", "tan", "sec", "csc", "cot", "arcsin", "arccos", "arctan", "sinh", "cosh",
    "tanh", "log", "ln", "exp", "lim", "inf", "sup", "min", "max", "det", "dim", "deg",
    "gcd", "ker", "arg",
})  # fmt: skip
#: A named call, ASCII-only so `F₃(2)` is not one: `load_records()`, `render(x)`.
CALL = re.compile(r"(?<![\w\\])(?P<name>[A-Za-z_][A-Za-z0-9_]+)\s*\(", re.ASCII)
#: Two or more letters with no operator: a word or a name, never a formula.
WORD = re.compile(r"^[A-Za-z][A-Za-z0-9]+$")
#: Words and the punctuation of a sentence, with no digit or operator: literal prose.
PROSE = re.compile(r"^[\[(]?[A-Za-z][A-Za-z0-9]*(?:[ ,.’()]+[A-Za-z0-9]+)*[.)\]]*$")


@dataclass(frozen=True)
class Verdict:
    """What one span is, the rule that decided it, and its LaTeX when it is math."""

    kind: Kind
    rule: str
    latex: str | None = None
    reason: str = ""


class UnconvertibleError(ValueError):
    """A span with no faithful LaTeX form; the message says which character or word."""


def _named(text: str) -> Verdict | None:
    """A call of a function that is not mathematics, a word, or prose, is literal text."""
    if any(match.group("name") not in MATH_FUNCTIONS for match in CALL.finditer(text)):
        return Verdict("identifier", "function call")
    if WORD.match(text) and text in MATH_FUNCTIONS:
        return Verdict("uncertain", "bare function name", reason=f"`{text}` alone")
    if WORD.match(text):
        return Verdict("identifier", "word")
    if PROSE.match(text) and set(re.findall(r"[A-Za-z]{2,}", text)) - MATH_FUNCTIONS:
        return Verdict("identifier", "prose")
    return None


def _literal(text: str) -> Verdict | None:
    """The verdict for a span that is not mathematics, or `None` if it may be."""
    if not text:
        return Verdict("uncertain", "empty", reason="an empty span")
    groups: tuple[tuple[Kind, tuple[tuple[str, re.Pattern[str]], ...]], ...] = (
        ("identifier", IDENTIFIER_RULES),
        ("uncertain", UNCERTAIN_RULES),
    )
    for kind, rules in groups:
        rule = next((rule for rule, pattern in rules if pattern.search(text)), None)
        if rule is not None:
            return Verdict(kind, rule, reason=rule if kind == "uncertain" else "")
    return _named(text)


def classify(content: str, *, frac: bool = False) -> Verdict:
    """Classify one code span's content, knowing nothing of where it sits.

    `frac` asks for the form a table row or display math takes: `\\frac{a}{b}` for a
    fraction of two integers, where running text keeps the slash. A case or range never
    takes it, since `n = 68/69` names two cases rather than a fraction. A span that
    crosses a line break is read as CommonMark reads it, with the break as a space.

    Cached: a file repeats its spans (`n = 11` a hundred times in the synopsis), and the
    ratchet classifies every span of every migrated file on each run.
    """
    return _classify(" ".join(content.split()), frac=frac)


@cache
def _classify(text: str, *, frac: bool) -> Verdict:
    if _ANY_IDENTIFIER.search(text) is None and _ANY_UNCERTAIN.search(text) is None:
        verdict = _named(text) if text else _literal(text)
    else:
        verdict = _literal(text)
    if verdict is not None:
        return verdict
    rule = _math_rule(text)
    try:
        latex = to_latex(text, frac=frac and rule != "case or range")
    except UnconvertibleError as error:
        return Verdict("uncertain", "no LaTeX form", reason=str(error))
    return Verdict("math", rule, latex=latex)


_RELATION = re.compile(r"[≥≤><=≠≈]")
#: The kinds of mathematics the report names, tried in order; the last always matches.
MATH_RULES: tuple[tuple[str, Callable[[str], object]], ...] = (
    ("s(n)", re.compile(r"s\s*\([^()]*\)").fullmatch),
    (
        "bound in s(n)",
        lambda text: re.search(r"(?<![A-Za-z\\])s\s*\(", text) and _RELATION.search(text),
    ),
    (
        "case or range",
        lambda text: (
            re.fullmatch(r"[nkm]\s*=\s*[\d+\-−].*", text)
            and not re.search(r"[A-Za-z]{2}", text)
        ),
    ),
    (
        "number",
        re.compile(r"(?=.*\d)[+\-−]?(?:\d{1,3}(?:,\d{3})+|\d+)?(?:\.\d+)?…?°?").fullmatch,
    ),
    ("fraction", re.compile(r"\d+/\d+").fullmatch),
    (
        "variable",
        re.compile(
            r"(?:[A-Za-z]|[α-ωΓΔΘΛΞΠΣΥΦΨΩϑϕϵϱϖ])[₀-₉ₐ-ₜᵢⱼᵣᵤᵥ,]*[⁰¹²³⁴-⁹ⁿⁱ]*[*′]?"
        ).fullmatch,
    ),
    ("symbol", lambda text: len(text) == 1),
    ("formula", lambda _text: True),
)


def _math_rule(text: str) -> str:
    """Name the kind of mathematics a convertible span is, for the report."""
    return next(name for name, test in MATH_RULES if test(text))


# ---------------------------------------------------------------------------------------
# Converting to LaTeX
# ---------------------------------------------------------------------------------------

_GREEK_NAMES = (
    ("α", "alpha"), ("β", "beta"), ("γ", "gamma"), ("δ", "delta"), ("ε", "varepsilon"),
    ("ϵ", "epsilon"), ("ζ", "zeta"), ("η", "eta"), ("θ", "theta"), ("ϑ", "vartheta"),
    ("ι", "iota"), ("κ", "kappa"), ("λ", "lambda"), ("μ", "mu"), ("ν", "nu"), ("ξ", "xi"),
    ("π", "pi"), ("ϖ", "varpi"), ("ρ", "rho"), ("ϱ", "varrho"), ("σ", "sigma"),
    ("ς", "varsigma"), ("τ", "tau"), ("υ", "upsilon"), ("φ", "varphi"), ("ϕ", "phi"),
    ("χ", "chi"), ("ψ", "psi"), ("ω", "omega"), ("Γ", "Gamma"), ("Δ", "Delta"),
    ("Θ", "Theta"), ("Λ", "Lambda"), ("Ξ", "Xi"), ("Π", "Pi"), ("Σ", "Sigma"),
    ("Υ", "Upsilon"), ("Φ", "Phi"), ("Ψ", "Psi"), ("Ω", "Omega"),
)  # fmt: skip
#: Greek letters as their commands. `φ` and `ε` are the curly forms LaTeX calls `\varphi`
#: and `\varepsilon`; the capitals that look Latin have no command and are refused.
GREEK = {letter: rf"\{name}" for letter, name in _GREEK_NAMES}
#: Each symbol's LaTeX and the token kind it reads as: a relation or operator, something
#: that can carry a script (a `letter` or `number`), an opening or closing bracket, or a
#: script itself.
SYMBOLS: dict[str, tuple[str, str]] = {
    "≥": (r"\ge", "relation"),
    "≤": (r"\le", "relation"),
    "≠": (r"\ne", "relation"),
    "≈": (r"\approx", "relation"),
    "≡": (r"\equiv", "relation"),
    "∼": (r"\sim", "relation"),
    "≅": (r"\cong", "relation"),
    "∝": (r"\propto", "relation"),
    "≪": (r"\ll", "relation"),
    "≫": (r"\gg", "relation"),
    "∈": (r"\in", "relation"),
    "∉": (r"\notin", "relation"),
    "⊂": (r"\subset", "relation"),
    "⊆": (r"\subseteq", "relation"),
    "⊃": (r"\supset", "relation"),
    "⊇": (r"\supseteq", "relation"),
    "⊥": (r"\perp", "relation"),
    "∥": (r"\parallel", "relation"),
    "→": (r"\to", "relation"),
    "↦": (r"\mapsto", "relation"),
    "⇒": (r"\Rightarrow", "relation"),
    "⟹": (r"\implies", "relation"),
    "↔": (r"\leftrightarrow", "relation"),
    "±": (r"\pm", "op"),
    "∓": (r"\mp", "op"),
    "×": (r"\times", "op"),
    "·": (r"\cdot", "op"),
    "⋅": (r"\cdot", "op"),
    "∘": (r"\circ", "op"),
    "∪": (r"\cup", "op"),
    "∩": (r"\cap", "op"),
    "∖": (r"\setminus", "op"),
    "∧": (r"\wedge", "op"),
    "∨": (r"\vee", "op"),
    "¬": (r"\neg", "op"),
    "∀": (r"\forall", "op"),
    "∃": (r"\exists", "op"),
    "∑": (r"\sum", "op"),
    "∏": (r"\prod", "op"),
    "∫": (r"\int", "op"),
    "−": ("-", "op"),
    "-": ("-", "op"),
    "…": (r"\ldots", "op"),
    "⋯": (r"\cdots", "op"),
    "∅": (r"\emptyset", "letter"),
    "∞": (r"\infty", "letter"),
    "∂": (r"\partial", "letter"),
    "∇": (r"\nabla", "letter"),
    "ℓ": (r"\ell", "letter"),
    "½": (r"\tfrac{1}{2}", "number"),
    "¼": (r"\tfrac{1}{4}", "number"),
    "¾": (r"\tfrac{3}{4}", "number"),
    "⟨": (r"\langle", "open"),
    "⌈": (r"\lceil", "open"),
    "⌊": (r"\lfloor", "open"),
    "{": (r"\lbrace", "open"),
    "(": ("(", "open"),
    "[": ("[", "open"),
    "⟩": (r"\rangle", "close"),
    "⌉": (r"\rceil", "close"),
    "⌋": (r"\rfloor", "close"),
    "}": (r"\rbrace", "close"),
    ")": (")", "close"),
    "]": ("]", "close"),
    "°": (r"^\circ", "script"),
    "′": (r"^{\prime}", "script"),
    "″": (r"^{\prime\prime}", "script"),
    "+": ("+", "op"),
    "=": ("=", "relation"),
    "<": ("<", "relation"),
    ">": (">", "relation"),
    ",": (",", "op"),
    ":": (":", "op"),
    "!": ("!", "op"),
    "|": ("|", "op"),
    "/": ("/", "slash"),
}
SUBSCRIPTS = {
    **dict(
        zip("₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₒₓₕₖₗₘₙₚₛₜᵢⱼᵣᵤᵥ", "0123456789+-=()aeoxhklmnpstijruv", strict=True)
    ),
    # The Greek subscripts are written as the letters they are. `ᵧ` often stands in for a
    # subscript y, which Unicode lacks; `\gamma` keeps the glyph the prose already shows
    # rather than guess at what it meant.
    **dict(zip("ᵦᵧᵨᵩᵪ", (r"\beta", r"\gamma", r"\rho", r"\varphi", r"\chi"), strict=True)),
}
SUPERSCRIPTS = dict(zip("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿⁱ", "0123456789+-=()ni", strict=True))
#: A number: with thousands separators (`1,039,500`), a decimal, or a bare fraction part.
_NUMBER_TOKEN = re.compile(r"\d{1,3}(?:,\d{3})+(?![\d,])(?:\.\d+)?|\d+(?:\.\d+)?|\.\d+")
_LETTERS = re.compile(r"[A-Za-z]+")
_CONTROL_WORD_END = re.compile(r"\\[A-Za-z]+$")
#: A backslash before anything but a letter: an escape to a Markdown parser.
_ESCAPE = re.compile(r"\\[^A-Za-z]")


def _join(pieces: Iterable[str]) -> str:
    """Concatenate LaTeX, spacing a control word from a letter that follows it."""
    latex = ""
    for piece in pieces:
        if _CONTROL_WORD_END.search(latex) and piece[:1].isascii() and piece[:1].isalpha():
            latex += " "
        latex += piece
    return latex


def _styled_letter(char: str) -> str | None:
    """`\\mathbb{R}` for `ℝ`, `\\mathcal{X}` for `𝒳`: letters in a mathematical alphabet."""
    name = unicodedata.name(char, "")
    if match := re.fullmatch(r"(?:MATHEMATICAL )?DOUBLE-STRUCK CAPITAL ([A-Z])", name):
        return rf"\mathbb{{{match.group(1)}}}"
    if match := re.fullmatch(r"(?:MATHEMATICAL )?SCRIPT CAPITAL ([A-Z])", name):
        return rf"\mathcal{{{match.group(1)}}}"
    return None


@dataclass(frozen=True)
class _Token:
    kind: str
    latex: str


@dataclass
class _Scanner:
    """A left-to-right reader of one span that turns its characters into LaTeX tokens."""

    source: str
    frac: bool
    index: int = 0
    tokens: list[_Token] = field(default_factory=list)

    def peek(self, offset: int = 0) -> str:
        at = self.index + offset
        return self.source[at] if 0 <= at < len(self.source) else ""

    def base(self) -> _Token | None:
        """The last token that is not a space: what a script would attach to."""
        return next((token for token in reversed(self.tokens) if token.kind != "space"), None)

    def emit(self, kind: str, latex: str) -> None:
        self.tokens.append(_Token(kind, latex))


def _script(scanner: _Scanner, table: dict[str, str], mark: str) -> None:
    """A run of Unicode sub- or superscripts as one `_{…}` or `^{…}` group."""
    base = scanner.base()
    if base is None or base.kind in {"op", "relation", "open", "slash"}:
        raise UnconvertibleError(f"a {'sub' if mark == '_' else 'super'}script with no base")
    pieces: list[str] = []
    while scanner.peek() in table or (
        mark == "_" and scanner.peek() == "," and pieces and scanner.peek(1) in table
    ):
        pieces.append(table.get(scanner.peek(), ","))
        scanner.index += 1
    run = _join(pieces)
    scanner.emit("script", f"{mark}{run}" if len(run) == 1 else f"{mark}{{{run}}}")


def _radicand(scanner: _Scanner) -> str:
    """What a `√` applies to: a parenthesised group, a number, or one symbol."""
    head = scanner.peek()
    if head == "(":
        return to_latex(_group(scanner, scanner.index), frac=scanner.frac)
    if number := _NUMBER_TOKEN.match(scanner.source, scanner.index):
        scanner.index = number.end()
        return number.group(0)
    if head.isascii() and head.isalpha():
        scanner.index += 1
        return head
    if head in GREEK:
        scanner.index += 1
        return GREEK[head]
    raise UnconvertibleError(f"`√` before {head!r}")


def _group(scanner: _Scanner, at: int) -> str:
    """The text inside the parentheses opening at `at`, consumed through the closing one."""
    depth, end = 0, at
    while end < len(scanner.source):
        depth += {"(": 1, ")": -1}.get(scanner.source[end], 0)
        if depth == 0:
            break
        end += 1
    if depth != 0:
        raise UnconvertibleError("an unclosed parenthesis")
    scanner.index = end + 1
    return scanner.source[at + 1 : end]


def _caret(scanner: _Scanner) -> None:
    """An ASCII exponent, braced: `10^22` is `10^{22}`, which `10^22` in LaTeX is not.

    A parenthesised exponent loses the parentheses that only grouped it (`ℝ^(3n+1)` is
    `\\mathbb{R}^{3n+1}`), and an exponent that is a call keeps its argument
    (`8^C(n,2)` is `8^{C(n,2)}`, where `8^C(n,2)` would raise only the `C`).
    """
    scanner.index += 1
    if scanner.peek() == "(":
        exponent = to_latex(_group(scanner, scanner.index), frac=scanner.frac)
        scanner.emit("script", f"^{{{exponent}}}")
        return
    head = scanner.peek()
    if head.isascii() and head.isalpha() and scanner.peek(1) == "(":
        scanner.index += 1
        argument = to_latex(_group(scanner, scanner.index), frac=scanner.frac)
        scanner.emit("script", f"^{{{head}({argument})}}")
        return
    sign = ""
    if scanner.peek() in {"-", "−"}:
        sign = "-"
        scanner.index += 1
    if number := _NUMBER_TOKEN.match(scanner.source, scanner.index):
        scanner.index = number.end()
        scanner.emit("script", f"^{{{sign}{number.group(0)}}}")
        return
    if not sign and scanner.peek().isascii() and scanner.peek().isalpha():
        scanner.emit("script", f"^{scanner.peek()}")
        scanner.index += 1
        return
    raise UnconvertibleError("an ASCII `^` before something other than a number or letter")


def _underscore(scanner: _Scanner) -> None:
    """An ASCII subscript on a one-letter base: `ν_ij` is `\\nu_{ij}`; `K_κ`, `K_{\\kappa}`."""
    base = scanner.base()
    if base is None or base.kind not in {"letter", "greek"}:
        raise UnconvertibleError("an `_` that is not a subscript on a letter")
    if (greek := GREEK.get(scanner.peek(1))) is not None:
        scanner.index += 2
        scanner.emit("script", f"_{{{greek}}}")
        return
    run = re.match(r"[A-Za-z0-9]+", scanner.source[scanner.index + 1 :])
    if run is None:
        raise UnconvertibleError("an `_` with no subscript after it")
    scanner.index += 1 + run.end()
    text = run.group(0)
    scanner.emit("script", f"_{text}" if len(text) == 1 else f"_{{{text}}}")


def _star(scanner: _Scanner) -> None:
    """`s*` and `a*` mark a distinguished value; any other `*` is ASCII arithmetic."""
    base = scanner.base()
    after = scanner.peek(1)
    if base is None or base.kind not in {"letter", "greek", "script"} or after.isalnum():
        raise UnconvertibleError("an ASCII `*` that is not a marking star")
    scanner.index += 1
    scanner.emit("script", r"^{\ast}")


def _en_dash(scanner: _Scanner) -> None:
    """An en dash is a range only between two numbers: `18–95` is `18\\text{–}95`."""
    before = scanner.source[: scanner.index].rstrip()
    after = scanner.source[scanner.index + 1 :].lstrip()
    if not (before[-1:].isdigit() or before.endswith("°")) or not after[:1].isdigit():
        raise UnconvertibleError("an en dash outside a numeric range")
    scanner.index += 1
    scanner.emit("op", r"\text{–}")


def _letters(scanner: _Scanner) -> None:
    """One letter is a variable; a longer run must be a known function."""
    word = _LETTERS.match(scanner.source, scanner.index)
    if word is None:  # pragma: no cover - `_step` only calls this on a letter
        raise UnconvertibleError("no letters")
    text = word.group(0)
    scanner.index = word.end()
    if len(text) == 1:
        scanner.emit("letter", text)
    elif text in MATH_FUNCTIONS:
        scanner.emit("function", rf"\{text}")
    else:
        raise UnconvertibleError(f"the word `{text}`")


_HANDLERS: dict[str, Callable[[_Scanner], None]] = {
    "^": _caret,
    "_": _underscore,
    "*": _star,
    "–": _en_dash,
}


def _step(scanner: _Scanner) -> None:
    """Read one token from `scanner`, or refuse the character in front of it."""
    char = scanner.peek()
    if char.isspace():
        while scanner.peek().isspace():
            scanner.index += 1
        scanner.emit("space", " ")
    elif number := _NUMBER_TOKEN.match(scanner.source, scanner.index):
        scanner.index = number.end()
        digits = number.group(0)
        # A thousands comma is `{,}`: bare, LaTeX spaces it as punctuation, `1, 039`.
        kind = "integer" if digits.isdigit() else "number"
        scanner.emit(kind, digits.replace(",", "{,}"))
    elif char.isascii() and char.isalpha():
        _letters(scanner)
    elif char in _HANDLERS:
        _HANDLERS[char](scanner)
    elif char in SUBSCRIPTS:
        _script(scanner, SUBSCRIPTS, "_")
    elif char in SUPERSCRIPTS:
        _script(scanner, SUPERSCRIPTS, "^")
    elif char == "√":
        scanner.index += 1
        scanner.emit("letter", rf"\sqrt{{{_radicand(scanner)}}}")
    elif char in GREEK:
        scanner.index += 1
        scanner.emit("greek", GREEK[char])
    elif char in SYMBOLS:
        scanner.index += 1
        latex, kind = SYMBOLS[char]
        scanner.emit(kind, latex)
    elif styled := _styled_letter(char):
        scanner.index += 1
        scanner.emit("letter", styled)
    else:
        raise UnconvertibleError(f"no LaTeX for {char!r}")


def _fractions(tokens: list[_Token]) -> list[_Token]:
    """`a/b` of two integers as `\\frac{a}{b}`, and `(\\frac{a}{b})` without its parens.

    The parentheses stay where they mean application or multiplication (`s(1/2)`,
    `2(1/2)`), and a slash in a chain (`1/2/3`) or beside a script is left alone.
    """
    out: list[_Token] = []
    index = 0
    while index < len(tokens):
        kinds = [token.kind for token in tokens[index : index + 3]]
        before = out[-1].kind if out else "start"
        after = tokens[index + 3].kind if index + 3 < len(tokens) else "end"
        if (
            kinds == ["integer", "slash", "integer"]
            and before not in {"slash", "script"}
            and after not in {"slash", "script", "integer", "number"}
        ):
            numerator, denominator = tokens[index].latex, tokens[index + 2].latex
            out.append(_Token("frac", rf"\frac{{{numerator}}}{{{denominator}}}"))
            index += 3
            continue
        out.append(tokens[index])
        index += 1
    unwrapped: list[_Token] = []
    index = 0
    while index < len(out):
        window = out[index : index + 3]
        before = unwrapped[-1].kind if unwrapped else "start"
        if (
            [token.latex for token in window[::2]] == ["(", ")"]
            and window[1].kind == "frac"
            and before in {"start", "space", "op", "relation"}
        ):
            unwrapped.append(window[1])
            index += 3
            continue
        unwrapped.append(out[index])
        index += 1
    return unwrapped


def to_latex(source: str, *, frac: bool = False) -> str:
    """The LaTeX for one mathematical expression, or `UnconvertibleError` saying why not.

    Spacing is the source's, collapsed; a control word gains a space when a letter comes
    next, so `x≥y` is `x\\ge y` rather than the undefined `\\gey`.
    """
    scanner = _Scanner(source.strip(), frac=frac)
    while scanner.index < len(scanner.source):
        _step(scanner)
    tokens = _fractions(scanner.tokens) if frac else scanner.tokens
    # `<` before a letter could open an HTML tag to a parser that reads it before the
    # math, so it is spaced: `x<y` is `x< y`, which LaTeX sets identically.
    latex = re.sub(r"<(?=[A-Za-z/!?])", "< ", _join(token.latex for token in tokens))
    if not latex or "$" in latex or "`" in latex or _ESCAPE.search(latex):
        raise UnconvertibleError("a conversion Markdown could read as an escape or a delimiter")
    return latex


#: Every control word this module writes, back to the character it came from. Where two
#: characters share a command (`·` and `⋅`, `−` and `-`), the first listed is the answer.
_PLAIN_WORDS = {
    **{latex: char for char, (latex, _) in reversed(SYMBOLS.items()) if latex.startswith("\\")},
    **{latex: letter for letter, latex in GREEK.items()},
}
_FRACTION = re.compile(r"\\t?frac\{([^{}]*)\}\{([^{}]*)\}")
_SQRT = re.compile(r"\\sqrt\{([^{}]*)\}")
_TEXT = re.compile(r"\\text\{([^{}]*)\}")
_WORD = re.compile(r"\\[A-Za-z]+")


def plain(latex: str) -> str:
    """The expression `to_latex` was given, near enough to read a figure back from.

    A checker that holds prose to a record reads its figures out of the prose, and once a
    file is migrated those figures are `$…$` rather than code. This undoes the conversions
    `to_latex` makes -- control words to their characters, `\\frac{a}{b}` to `a/b`,
    `\\sqrt{x}` to `√x` or `√(…)`, `\\text{–}` to `–` -- so `$\\frac{31}{8} = 3.875$` reads
    `31/8 = 3.875` and `$3.8770835\\ldots$` reads `3.8770835…`. Spacing is the LaTeX's,
    so the space `to_latex` puts after a control word before a letter stays.
    """
    def root(match: re.Match[str]) -> str:
        return f"√{match[1]}" if match[1].isalnum() else f"√({match[1]})"

    text = _TEXT.sub(r"\1", latex)
    # Innermost first, until nothing is left to fold: `\\sqrt{2 + \\sqrt{2}}`.
    while (folded := _SQRT.sub(root, _FRACTION.sub(r"\1/\2", text))) != text:
        text = folded
    text = text.replace("^\\circ", "°").replace("^{\\prime\\prime}", "″")
    text = text.replace("^{\\prime}", "′")
    return _WORD.sub(lambda m: _PLAIN_WORDS.get(m[0], m[0]), text)


# ---------------------------------------------------------------------------------------
# Planning a file
# ---------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Decision:
    """One code span and what happens to it."""

    span: CodeSpan
    verdict: Verdict

    @property
    def converts(self) -> bool:
        return self.verdict.kind == "math" and self.verdict.latex is not None


@dataclass(frozen=True)
class Plan:
    """Every code span in a file with its decision, and the spans renderers own."""

    decisions: tuple[Decision, ...]
    generated: int

    def converting(self) -> list[Decision]:
        return [decision for decision in self.decisions if decision.converts]


def _adjacent(text: str, span: CodeSpan) -> str | None:
    """Why a `$` in place of this span's backticks would touch something it must not."""
    before = text[span.start - 1] if span.start > 0 else ""
    after = text[span.end] if span.end < len(text) else ""
    for side, char in (("before", before), ("after", after)):
        if char == "$" or (side == "before" and char == "\\"):
            return f"`{char}` {side} the span"
        if char.isalnum():
            return f"`{char}` directly {side} the span"
    return None


#: Why a heading's code spans are left alone, whatever they hold. kpress drops math from a
#: heading's slug (`## The $n = 11$ case` becomes `#the--case`), so a converted span would
#: move the anchor under every link to it, the tutorial's contents entries among them.
HEADING = "heading: math would change the anchor"


def _run_quirk(raw: str, runs: Sequence[str]) -> str | None:
    """Why kpress would refuse math that opens an inline run, or `None`.

    mdit-py-plugins' dollarmath, which kpress uses with `allow_digits=False`, checks the
    character before an opening `$` as `src[pos - 1]`. At the start of a paragraph, list
    item or table cell `pos` is 0, the index wraps, and the check reads the run's *last*
    character: `$x$ is 1` is refused as if a digit touched the `$`. GitHub is not affected;
    the site would print the dollars.
    """
    for run in runs:
        if run.lstrip().startswith(raw) and run.rstrip()[-1:].isdigit():
            return "math opening a run that ends in a digit, which kpress's dollarmath refuses"
    return None


def _in_table(raw: str, cells: Sequence[str]) -> bool:
    """Whether a table row's parsed cells hold this span, unsplit by a `|` inside it."""
    return any(raw in cell for cell in cells)


def _in_context(text: str, span: CodeSpan, verdict: Verdict, blocks: Blocks) -> Verdict:
    """A verdict adjusted for where its span sits.

    Every span in a heading is kept as code, as an `identifier`; elsewhere only a math
    verdict can change, to `uncertain` when a `$` could not safely replace the backticks.
    """
    where = blocks.lines[span.line - 1]
    if where == "heading":
        return Verdict("identifier", "in a heading", reason=HEADING)
    if verdict.kind != "math":
        return verdict
    raw = text[span.start : span.end]
    runs = blocks.runs.get(span.line - 1, [])
    if reason := _adjacent(text, span) or _run_quirk(raw, runs):
        return Verdict("uncertain", "delimiter adjacency", reason=reason)
    if where == "table":
        if not _in_table(raw, runs):
            reason = "a `|` in the row splits this span across table cells"
            return Verdict("uncertain", "split by a table cell", reason=reason)
        verdict = classify(span.content, frac=True)
        if verdict.latex is not None and "|" in verdict.latex:
            return Verdict("uncertain", "pipe in a table", reason="a `|` would split the cell")
    return verdict


def plan(text: str) -> Plan:
    """Classify every code span in `text` and decide, in context, which ones convert."""
    prose, generated = mask(text)
    blocks = block_context(text)
    decisions = tuple(
        Decision(span, _in_context(text, span, classify(span.content), blocks))
        for span in code_spans(prose)
        if blocks.lines[span.line - 1] != "raw"
    )
    return Plan(decisions, generated=len(code_spans(generated)))


def has_math_spans(text: str) -> bool:
    """Whether any code span's content alone reads as math: `plan`'s cheap first pass.

    A file for which this is false has nothing `plan` could convert, so a caller that only
    wants the math can skip the block parse.
    """
    prose, _generated = mask(text)
    return any(_reads_as_math(" ".join(span.content.split())) for span in code_spans(prose))


@cache
def _reads_as_math(text: str) -> bool:
    """`classify(text).kind == "math"`, without naming the rule of a span that is not."""
    if _ANY_IDENTIFIER.search(text) is not None or _ANY_UNCERTAIN.search(text) is not None:
        return False
    return _classify(text, frac=False).kind == "math"


def rewrite(text: str, decisions: Iterable[Decision]) -> str:
    """`text` with every converting span's backticks replaced by `$…$` around its LaTeX."""
    pieces: list[str] = []
    position = 0
    for decision in sorted(decisions, key=lambda item: item.span.start):
        if decision.converts:
            pieces.extend((text[position : decision.span.start], f"${decision.verdict.latex}$"))
            position = decision.span.end
    pieces.append(text[position:])
    return "".join(pieces)


# ---------------------------------------------------------------------------------------
# For renderers: generated Markdown is migrated where it is written, never after
# ---------------------------------------------------------------------------------------

_CELL_PREFIX = "| x |\n| --- |\n| "
_CELL_SUFFIX = " |\n"


def markdown_math(fragment: str, *, table: bool = False) -> str:
    """A Markdown fragment with its math code spans as `$…$`, planned as a file would be.

    For a renderer that writes prose it does not own, such as a register's `headline`.
    `table` plans the fragment as one table cell, so it takes the cell's `\\frac` style
    and the cell's refusals: a `|` in the math, and math opening a cell that ends in a
    digit, which kpress's dollarmath would print as dollars.
    """
    if not table:
        return rewrite(fragment, plan(fragment).decisions)
    source = f"{_CELL_PREFIX}{fragment}{_CELL_SUFFIX}"
    converted = rewrite(source, plan(source).decisions)
    return converted[len(_CELL_PREFIX) : len(converted) - len(_CELL_SUFFIX)]


#: The register's ASCII operators and their Unicode forms, which `to_latex` then reads.
_REGISTER_ASCII = (
    (re.compile(r">="), "≥"),
    (re.compile(r"<="), "≤"),
    (re.compile(r"!="), "≠"),
    (re.compile(r"\.\.\."), "…"),
    (re.compile(r"\bsqrt\s*\("), "√("),
    (re.compile(r"\*"), "·"),
)


def register_latex(literal: str, *, frac: bool = False) -> str:
    """The LaTeX for one ASCII register literal: an exact form, a value or a bound.

    The register stores `s(11) >= 955000*sqrt(518400042893309449)/179696714646249` and
    keeps it ASCII; a renderer shows it as mathematics. Only the literal goes in, never
    the prose around it: a word raises `UnconvertibleError`, as it does in `to_latex`.
    """
    text = literal
    for pattern, replacement in _REGISTER_ASCII:
        text = pattern.sub(replacement, text)
    for name, (left, right) in _BRACKETS.items():
        text = _bracketed(text, name, left, right)
    return to_latex(text, frac=frac)


#: The register's rounding functions and the brackets that write them.
_BRACKETS = {"floor": ("⌊", "⌋"), "ceil": ("⌈", "⌉")}


def _bracketed(text: str, name: str, left: str, right: str) -> str:
    """`floor(x)` as `⌊x⌋`, innermost first, so the parentheses always balance."""
    call = re.compile(rf"\b{name}\(")
    while (match := call.search(text)) is not None:
        depth, end = 1, match.end()
        while end < len(text) and depth:
            depth += {"(": 1, ")": -1}.get(text[end], 0)
            end += 1
        if depth:
            raise UnconvertibleError(f"an unclosed `{name}(`")
        text = f"{text[: match.start()]}{left}{text[match.end() : end - 1]}{right}{text[end:]}"
    return text


# ---------------------------------------------------------------------------------------
# Proving a rewrite
# ---------------------------------------------------------------------------------------

# kpress writes each inline span's TeX source into the element KaTeX enhances, and writes a
# source its MathML converter refused into an element flagged as an error. Reading both
# from the page is reading exactly what the site's parser took for math.
_RENDERED = re.compile(
    r'<span class="kpress-math-render" aria-hidden="true">\\\((?P<source>.*?)\\\)</span>',
    re.DOTALL,
)
_REFUSED = re.compile(
    r'<span class="kpress-math kpress-math-inline" data-kpress-math="inline" '
    r'data-kpress-math-renderer="katex" data-kpress-math-error="true">(?P<source>.*?)</span>',
    re.DOTALL,
)


@dataclass(frozen=True)
class KpressMath:
    """The inline math kpress reads in a document, and the part it cannot render."""

    sources: Counter[str]
    refused: Counter[str]


def kpress_math(text: str) -> KpressMath:
    """Parse `text` as the site does and collect the source of every inline math span."""
    from kpress.format.markdown import parse_markdown  # noqa: PLC0415

    page = parse_markdown(text, title="migrate_math", trust_mode="trusted", math="auto").html
    rendered = Counter(
        html.unescape(match.group("source")) for match in _RENDERED.finditer(page)
    )
    refused = Counter(html.unescape(match.group("source")) for match in _REFUSED.finditer(page))
    return KpressMath(rendered + refused, refused)


def katex_refusals(text: str, sources: Iterable[str]) -> set[str] | None:
    """The given sources the pinned KaTeX refuses in strict mode, or `None` without Node."""
    wanted = set(sources)
    if not wanted:
        return set()
    if shutil.which("node") is None:
        return None
    from devtools.check_katex import check_files  # noqa: PLC0415

    with tempfile.TemporaryDirectory(prefix="migrate-math-katex-") as directory:
        copy = Path(directory) / "converted.md"
        copy.write_text(text, encoding="utf-8")
        try:
            report = check_files([copy])
        except OSError, ValueError:
            return None
    return {error["source"] for file in report["files"] for error in file["errors"]} & wanted


@dataclass(frozen=True)
class SpanSafety:
    """What the pinned formatter did to the math spans of a converted file."""

    result: FileResult
    changed: tuple[tuple[str, str], ...] = ()


def flowmark_safety(text: str, name: str, command: Sequence[str]) -> SpanSafety:
    """Format a copy of `text` with the pinned formatter and compare its math spans.

    `check_math_spans`' own measurement, taken on text rather than on a path: its span
    reader and its copy formatter, so this and `make format` cannot disagree about what a
    span is. The pairs that changed are kept so a refusal can say which they were.
    """
    with tempfile.TemporaryDirectory(prefix="migrate-math-") as directory:
        copy = Path(directory) / name
        copy.write_text(text, encoding="utf-8")
        before = math_spans(text)
        after = math_spans(format_copy(copy, list(command)))
    pairs = tuple((old, new) for old, new in zip(before, after, strict=False) if old != new)
    broken = sum(1 for old, new in pairs if "\n" in new and "\n" not in old)
    return SpanSafety(
        FileResult(Path(name), len(before), len(after), broken, len(pairs)), pairs
    )


#: Given the converted text and the file's name, what the formatter does to its math.
SafetyCheck = Callable[[str, str], SpanSafety]


def pinned_safety(flowmark: str | None = None) -> SafetyCheck:
    """The span check with the given formatter command, or the Makefile's pin."""
    command = shlex.split(flowmark or pinned_formatter())

    def check(converted: str, name: str) -> SpanSafety:
        return flowmark_safety(converted, name, command)

    return check


@dataclass
class Migration:
    """The outcome of migrating one file: its final plan, text, refusals and notes."""

    path: Path
    plan: Plan
    text: str
    converted: str
    refusals: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def _demote(decisions: Iterable[Decision], bad: set[str], check: str) -> tuple[Decision, ...]:
    return tuple(
        replace(
            decision,
            verdict=Verdict(
                "uncertain", check, reason=f"`${decision.verdict.latex}$` failed {check}"
            ),
        )
        if decision.converts and decision.verdict.latex in bad
        else decision
        for decision in decisions
    )


def _kpress_round(
    migration: Migration, current: Plan, baseline: Counter[str]
) -> tuple[Plan, bool]:
    """One proof by kpress and KaTeX: the plan to try next, and whether it is settled."""
    converted = rewrite(migration.text, current.decisions)
    expected = Counter(decision.verdict.latex or "" for decision in current.converting())
    found = kpress_math(converted)
    gained = found.sources - baseline
    stray = (gained - expected) + (baseline - found.sources)
    if stray:
        listed = ", ".join(f"${source}$" for source in sorted(stray))
        migration.refusals.append(f"kpress math changed beyond the rewrite: {listed}")
        return current, True
    missing = set(expected - gained) | (set(found.refused) & set(expected))
    if missing:
        return replace(
            current, decisions=_demote(current.decisions, missing, "the kpress parse")
        ), False
    refused = katex_refusals(converted, expected)
    if refused is None:
        migration.notes.append("KaTeX strict parse skipped: Node or the bundle is unavailable")
    elif refused:
        return replace(
            current, decisions=_demote(current.decisions, refused, "the KaTeX parse")
        ), False
    return current, True


def prove(path: Path, text: str, *, safety: SafetyCheck | None) -> Migration:
    """Plan `text`, then demote or refuse until every rewrite is proved safe.

    kpress must read each converted span as exactly one inline math span it can render,
    and KaTeX must accept it; a span that fails either is demoted and the plan proved
    again. `safety`, when given, is the pinned formatter's span check on the final text.
    """
    current = plan(text)
    migration = Migration(path, current, text, text)
    if current.converting():
        baseline = kpress_math(text).sources
        for _attempt in range(4):
            current, settled = _kpress_round(migration, current, baseline)
            if settled or not current.converting():
                break
        else:
            migration.refusals.append("the plan did not settle in four proofs")
    migration.plan = current
    migration.converted = rewrite(text, current.decisions)
    if safety is not None and not migration.refusals and migration.converted != text:
        outcome = safety(migration.converted, path.name)
        if not outcome.result.ok:
            detail = "; ".join(f"${old}$ became ${new}$" for old, new in outcome.changed[:5])
            migration.refusals.append(
                "the pinned formatter does not keep the math whole: "
                + " ".join(outcome.result.line().split())
                + (f" ({detail})" if detail else "")
            )
    return migration


# ---------------------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------------------


class Conversion(TypedDict):
    line: int
    code: str
    math: str
    rule: str


class Uncertain(TypedDict):
    line: int
    code: str
    rule: str
    reason: str


class FileReport(TypedDict):
    path: str
    spans: int
    generated_spans: int
    counts: dict[str, int]
    rules: dict[str, dict[str, int]]
    conversions: list[Conversion]
    uncertain: list[Uncertain]
    refusals: list[str]
    notes: list[str]


def display_path(path: Path) -> str:
    """`path` relative to the repository when it is inside it."""
    resolved = path.resolve()
    return (
        resolved.relative_to(REPO).as_posix()
        if resolved.is_relative_to(REPO)
        else path.as_posix()
    )


def file_report(migration: Migration) -> FileReport:
    """One file's account: counts per class and rule, every conversion and uncertain span."""
    decisions = migration.plan.decisions
    rules: dict[str, Counter[str]] = {kind: Counter() for kind in KINDS}
    for decision in decisions:
        rules[decision.verdict.kind][decision.verdict.rule] += 1
    return {
        "path": display_path(migration.path),
        "spans": len(decisions),
        "generated_spans": migration.plan.generated,
        "counts": {kind: rules[kind].total() for kind in KINDS},
        "rules": {kind: dict(rules[kind].most_common()) for kind in KINDS},
        "conversions": [
            {
                "line": item.span.line,
                "code": item.span.text,
                "math": item.verdict.latex or "",
                "rule": item.verdict.rule,
            }
            for item in decisions
            if item.converts
        ],
        "uncertain": [
            {
                "line": item.span.line,
                "code": item.span.text,
                "rule": item.verdict.rule,
                "reason": item.verdict.reason,
            }
            for item in decisions
            if item.verdict.kind == "uncertain"
        ],
        "refusals": list(migration.refusals),
        "notes": list(migration.notes),
    }


def print_report(report: FileReport, *, listing: bool) -> None:
    counts = report["counts"]
    generated = report["generated_spans"]
    print(
        f"{report['path']}: {report['spans']} code spans -- {counts['math']} math, "
        f"{counts['identifier']} identifier, {counts['uncertain']} uncertain"
        + (
            f" ({generated} more in generated blocks, left to their renderers)"
            if generated
            else ""
        )
    )
    for kind in KINDS:
        if report["rules"][kind]:
            rules = ", ".join(
                f"{rule} {count}" for rule, count in report["rules"][kind].items()
            )
            print(f"  {kind}: {rules}")
    if listing:
        for item in report["conversions"]:
            print(f"  L{item['line']}: `{item['code']}` -> ${item['math']}$")
    for item in report["uncertain"]:
        print(
            f"  L{item['line']}: uncertain `{item['code']}` -- {item['reason'] or item['rule']}"
        )
    for note in report["notes"]:
        print(f"  note: {note}")
    for refusal in report["refusals"]:
        print(f"  REFUSED: {refusal}")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="migrate_math",
        description="Classify code spans as math, identifier or uncertain; rewrite the math.",
    )
    parser.add_argument("files", nargs="+", type=Path, metavar="FILE")
    parser.add_argument(
        "--apply", action="store_true", help="rewrite the math spans in place, once proved"
    )
    parser.add_argument("--report", type=Path, metavar="PATH", help="also write JSON here")
    parser.add_argument("--list", action="store_true", help="print every conversion")
    parser.add_argument(
        "--flowmark",
        default=None,
        metavar="COMMAND",
        help="formatter command for the span check (default: the Makefile's FLOWMARK pin)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    safety = pinned_safety(arguments.flowmark) if arguments.apply else None
    reports: list[FileReport] = []
    refused = 0
    for path in arguments.files:
        if not path.is_file():
            print(f"no such file: {path.as_posix()}", file=sys.stderr)
            return 2
        text = path.read_text(encoding="utf-8")
        if arguments.apply:
            migration = prove(path, text, safety=safety)
        else:
            migration = Migration(path, plan(text), text, text)
        report = file_report(migration)
        reports.append(report)
        print_report(report, listing=arguments.list)
        if migration.refusals:
            refused += 1
        elif arguments.apply and migration.converted != text:
            with atomic_output_file(path) as temporary:
                Path(temporary).write_text(migration.converted, encoding="utf-8")
            print(f"  wrote {len(migration.plan.converting())} math spans")
    totals: Counter[str] = Counter()
    for report in reports:
        totals.update(report["counts"])
    print(
        f"total: {len(reports)} files, {totals['math']} math, {totals['identifier']} "
        f"identifier, {totals['uncertain']} uncertain"
        + (f", {refused} refused" if arguments.apply else "")
    )
    if arguments.report is not None:
        arguments.report.write_text(
            json.dumps(reports, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    return 1 if refused else 0


if __name__ == "__main__":
    raise SystemExit(main())
