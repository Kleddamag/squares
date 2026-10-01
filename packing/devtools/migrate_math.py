#!/usr/bin/env python3
# ruff: noqa: RUF001, RUF002, RUF003 -- this module reads and writes mathematical Unicode.
"""Move mathematics out of code spans and into LaTeX math, one file at a time.

Much of this repository's prose writes mathematics as inline code: `` `s(11) ≥ 31/8` ``,
`` `2 + 4/√5` ``, `` `k² − 4` ``. Code spans render in a fixed-width face and are what a
reader expects for identifiers and commands, not for a bound. GitHub, kpress (which
builds the published site with KaTeX) and the pinned flowmark all support LaTeX math, so
the prose can say what it means. This is the tool for that migration (`OR-1`); the
ratchet that keeps a migrated file migrated is `devtools.check_math_markup`.

**What is a code span here.** Spans are found by parsing, not by a regex over the file.
`markdown-it-py` (the parser kpress itself is built on) decides which blocks carry
inline content, so fenced and indented code, HTML blocks and comments are never read.
Inside those blocks a small CommonMark backtick tokenizer finds each span's exact
source offsets, and the list it finds is compared with the parser's own `code_inline`
tokens for the same block; a block where the two disagree converts nothing. Regions
between `<!-- BEGIN ... -->` and `<!-- END ... -->` markers belong to the renderer that
writes them and are skipped: generated Markdown is migrated at its renderer.

**Classification.** Every span is `math`, `identifier`, or `uncertain`, with the name of
the rule that decided it. Identifiers are tested first and stay code: result and
evidence ids (`T-018`, `E-...`), rung and label names (`V4`, `C3`), bead and session
ids, paths, file names, commands and flags, dotted and snake_case names, schema names,
hashes, version tags, measurements with units, and HTML. A span is math when it is an
expression (a relation, an operation, a root, a power, an interval), a fraction or
decimal standing as a value, an angle, or a single variable -- and when every word in
it is a single letter, a Greek letter's name, or a known function (`sqrt`, `ceil`,
`sin`, ...). Everything else is uncertain and left alone for a person to read: a bare
integer (a count, a case number, an exit status?), scientific notation (usually a
machine tolerance), a named term such as `Feas(s)`, or an expression this translator
does not know how to write.

Context can also hold a span back. A math span stays code, reported as uncertain, when
it is in a heading (its text is the anchor other documents link to), in link text,
across a line break, touching a letter or digit -- see the delimiter form below -- or
first in a paragraph or table cell whose text ends in a digit, which kpress's parser
misreads (`_parsed_spans` says how). A span a person has read and decided is not
mathematics in its file -- `V` naming the verification ladder -- is listed as kept in
the ledger, `math-migrated.yaml`, and stays code too.

**The delimiter form: plain `$...$`, never GitHub's `` $`...`$ ``.** GitHub renders both,
but kpress parses math with `mdit_py_plugins.dollarmath` (`allow_space=False,
allow_digits=False`, in `vendor/kpress/src/kpress/format/markdown.py`), which reads the
backtick form as math whose source contains backticks. The plain form is the one both
renderers read, under the intersection of their rules: the content never begins or ends
with a space (kpress's `allow_space=False`, and GitHub's own rule), and the span never
touches a letter or digit outside it (kpress's `allow_digits=False` refuses a digit;
GitHub does not open math after a word character). A span that would touch one is left
as code. Inside the math nothing is written that GitHub's Markdown pass could take
first: no `\\{` or other backslash-punctuation escape (sets use `\\lbrace`/`\\rbrace`),
no bare `|` (a table would split on it; `\\lvert`/`\\rvert` instead), `<` and `>` with
spaces around them so neither reads as an HTML tag, and no `*` (`\\ast`, `\\cdot`).
`test_migrate_math` pins each of these against kpress's parser.

**The translation** is idiomatic LaTeX: `>=` and `≥` become `\\ge`, `sqrt(x)` and `√x`
become `\\sqrt{x}`, `²` becomes `^2`, `…` and `...` become `\\ldots`, `−` becomes `-`,
`×` becomes `\\times`, Greek letters their commands, `ℝ` becomes `\\mathbb{R}`. A
fraction written `a/b` stays `a/b`: inline in running text the slash reads better than
`\\frac`, which is reserved for display math and tables.

**Safety.** `--apply` writes only when the result passes two measurements: kpress's
parser must read each converted span back as exactly the math that was written, and the
pinned flowmark must keep every math span in the file whole
(`devtools.check_math_spans`). Either failing leaves the file untouched and exits 1.

Usage, from `packing/`:

    uv run --frozen --group dev python -m devtools.migrate_math FILE... --report
    uv run --frozen --group dev python -m devtools.migrate_math FILE... --conversions
    uv run --frozen --group dev python -m devtools.migrate_math FILE... --apply

Without `--apply` nothing is written. Converting twice is a no-op, since a converted
span is no longer code.
"""

from __future__ import annotations

import argparse
import re
import shlex
import sys
import tempfile
from collections import Counter
from collections.abc import Collection, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, cast

from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdit_py_plugins.dollarmath import dollarmath_plugin

from devtools.check_math_spans import check_file, pinned_formatter
from sqpack.yamlio import load_yaml

Kind = Literal["math", "identifier", "uncertain"]

# ---------------------------------------------------------------------------------------
# Identifiers: tested in order against the whole stripped span, first match wins.
# ---------------------------------------------------------------------------------------

_IDENTIFIERS: tuple[tuple[str, re.Pattern[str]], ...] = tuple(
    (name, re.compile(pattern))
    for name, pattern in (
        ("html", r"^</?[A-Za-z!][^>]*>?.*$|^\{[.#]|^\[[^\]]*\]\{"),
        ("record-id", r"^[A-Z]{1,3}-\d+[a-z]?$|^[A-Z]-[a-z0-9][\w-]*$"),
        ("placeholder-id", r"^[A-Za-z]+-(N+)?$"),
        ("label-list", r"^[A-Z](/[A-Z])+$"),
        ("time-label", r"^T[+-]\d+$"),
        ("slug-id", r"^([a-z][a-z0-9]+|[a-z](?=-(\d{3}|[a-z])))(-[a-z0-9]+)+(\.\w+)?$"),
        ("label", r"^[A-Z]\d+(/[A-Z]\d+)?$|^[A-Za-z]+\d+[A-Za-z]*$"),
        ("hash", r"^(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}$|\+sha256-"),
        ("version", r"^v\d+(\.\d+)+$|^\d+\.\d+\.\d+$"),
        ("flag", r"^--?[A-Za-z]|\s--[A-Za-z]"),
        (
            "command",
            (
                r"^(uv|git|make|python3?|packing-\w+|tbd|gh|npm|npx|node|cargo|sqsearch|"
                r"runner\.py|flowmark|pprose)(\s|$)"
            ),
        ),
        ("path", r"^(?=.*[A-Za-z]{2}|.*\.[A-Za-z])[\w.*<>~@+-]*/[\w.*<>/~@+-]*$"),
        ("file", r"^[\w.*<>-]*\.[A-Za-z][A-Za-z0-9]{0,4}$|^\.\w"),
        ("dotted-name", r"^[A-Za-z_]\w*(\.[A-Za-z_]\w*)+$"),
        ("word-or-name", r"^[A-Za-z_]\w*$"),
        ("key-value", r"^[A-Za-z_][\w-]*:(\s|$)|^[a-z][\w-]*:[\w-]+$"),
        ("timestamp", r"\d{2}:\d{2}|^\d{4}-\d{2}-\d{2}"),
        (
            "measurement",
            r"^[~≈+−-]?\s*\d[\d.,]*(e[+-]?\d+)?\s?(s|ms|µs|us|ns|GB|MB|KB|x|×|%|h|min)$",
        ),
    )
)

# `word-or-name` above matches any bare word. Only these shapes of it are identifiers; a
# single letter, a Greek name, `P_TR` or `g_j` falls through to the math rules.
_SNAKE = re.compile(r"^[A-Za-z]{2,}_|_[A-Za-z]{3,}|^[A-Za-z]{2,}$")

# ---------------------------------------------------------------------------------------
# The translator: known words, symbols, and the pieces of the scan.
# ---------------------------------------------------------------------------------------

GREEK_NAMES = frozenset(
    {
        *("alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", "iota"),
        *("kappa", "lambda", "mu", "nu", "xi", "pi", "rho", "sigma", "tau", "upsilon"),
        *("phi", "chi", "psi", "omega", "Gamma", "Delta", "Theta", "Lambda", "Xi", "Pi"),
        *("Sigma", "Phi", "Psi", "Omega"),
    }
)
FUNCTIONS = frozenset(
    {
        *("sin", "cos", "tan", "arctan", "arcsin", "arccos", "log", "ln", "exp"),
        *("min", "max", "deg", "gcd"),
    }
)
BRACKETED = {"ceil": (r"\lceil ", r" \rceil"), "floor": (r"\lfloor ", r" \rfloor")}

SYMBOLS = {
    "α": r"\alpha",
    "β": r"\beta",
    "γ": r"\gamma",
    "δ": r"\delta",
    "ε": r"\varepsilon",
    "ϵ": r"\epsilon",
    "ζ": r"\zeta",
    "η": r"\eta",
    "θ": r"\theta",
    "κ": r"\kappa",
    "λ": r"\lambda",
    "μ": r"\mu",
    "ν": r"\nu",
    "ξ": r"\xi",
    "π": r"\pi",
    "ρ": r"\rho",
    "σ": r"\sigma",
    "τ": r"\tau",
    "φ": r"\varphi",
    "ϕ": r"\phi",
    "χ": r"\chi",
    "ψ": r"\psi",
    "ω": r"\omega",
    "Γ": r"\Gamma",
    "Δ": r"\Delta",
    "Θ": r"\Theta",
    "Λ": r"\Lambda",
    "Π": r"\Pi",
    "Σ": r"\Sigma",
    "Φ": r"\Phi",
    "Ψ": r"\Psi",
    "Ω": r"\Omega",
    "≤": r"\le",
    "≥": r"\ge",
    "≠": r"\ne",
    "≈": r"\approx",
    "≡": r"\equiv",
    "∼": r"\sim",
    "×": r"\times",
    "·": r"\cdot",
    "⋅": r"\cdot",
    "−": "-",
    "±": r"\pm",
    "∓": r"\mp",
    "…": r"\ldots",
    "∈": r"\in",
    "∉": r"\notin",
    "∪": r"\cup",
    "∩": r"\cap",
    "⊂": r"\subset",
    "⊆": r"\subseteq",
    "→": r"\to",
    "↦": r"\mapsto",
    "←": r"\leftarrow",
    "↔": r"\leftrightarrow",
    "⇒": r"\Rightarrow",
    "∞": r"\infty",
    "∇": r"\nabla",
    "∂": r"\partial",
    "∑": r"\sum",
    "⌈": r"\lceil ",
    "⌉": r" \rceil",
    "⌊": r"\lfloor ",
    "⌋": r" \rfloor",
    "⟨": r"\langle ",
    "⟩": r" \rangle",
    "ℝ": r"\mathbb{R}",
    "ℚ": r"\mathbb{Q}",
    "ℤ": r"\mathbb{Z}",
    "ℕ": r"\mathbb{N}",
    "ℂ": r"\mathbb{C}",
    "𝒫": r"\mathcal{P}",
    "𝒳": r"\mathcal{X}",
    "°": r"^{\circ}",
    "½": r"\tfrac{1}{2}",
    "¼": r"\tfrac{1}{4}",
    "¾": r"\tfrac{3}{4}",
    "′": "'",
}
SUPERSCRIPTS = dict(zip("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ⁿⁱ", "0123456789+-ni", strict=True))
# `ᵧ` is GREEK SUBSCRIPT SMALL LETTER GAMMA, but the prose uses it as a subscript y.
SUBSCRIPTS = dict(
    zip("₀₁₂₃₄₅₆₇₈₉₊₋ᵢⱼₖₗₘₙₓᵧᵣₐₑₒₕₚₛₜ", "0123456789+-ijklmnxyraeohpst", strict=True)
)
PLAIN = frozenset("+-=()[]/,.:'! ")

_NUMBER = re.compile(
    r"(?P<mantissa>\d{1,3}(?:,\d{3})+(?![\d/])|\d*\.\d+|\d+)"
    r"(?:e(?P<exponent>[+-]?\d+)(?![A-Za-z]))?"
)
_WORD = re.compile(r"[A-Za-z]+")
_SUPERSCRIPT_RUN = re.compile(f"[{''.join(SUPERSCRIPTS)}]+")
_SUBSCRIPT_RUN = re.compile(f"[{''.join(SUBSCRIPTS)}]+(?:,[{''.join(SUBSCRIPTS)}]+)*")
_COMMAND_TAIL = re.compile(r"\\[A-Za-z]+$")


class UnconvertibleError(ValueError):
    """The span cannot be written as math by this translator; the message is the rule."""


def _group(text: str, start: int) -> int:
    """The index just past the parenthesis group opening at `start`."""
    depth = 0
    for index in range(start, len(text)):
        if text[index] == "(":
            depth += 1
        elif text[index] == ")":
            depth -= 1
            if depth == 0:
                return index + 1
    raise UnconvertibleError("unbalanced-parentheses")


class _Writer:
    """Accumulate LaTeX, inserting the space a control word needs before a letter."""

    def __init__(self) -> None:
        self.parts: list[str] = []

    def emit(self, piece: str) -> None:
        if self.parts and piece[:1].isalpha() and _COMMAND_TAIL.search(self.parts[-1]):
            self.parts.append(" ")
        self.parts.append(piece)

    def text(self) -> str:
        return re.sub(r" {2,}", " ", "".join(self.parts)).strip()


def _number(match: re.Match[str]) -> str:
    mantissa = match.group("mantissa").replace(",", "{,}")
    exponent = match.group("exponent")
    if exponent is None:
        return mantissa
    power = str(int(exponent))
    power = f"10^{{{power}}}" if len(power) > 1 else f"10^{power}"
    return power if mantissa == "1" else rf"{mantissa} \times {power}"


def _argument(text: str, index: int) -> tuple[str, int]:
    """The operand of a root or a power at `index`, translated, and where it ends."""
    if index < len(text) and text[index] == "(":
        end = _group(text, index)
        return to_latex(text[index + 1 : end - 1]), end
    if match := re.compile(r"-?\d+(\.\d+)?").match(text, index):
        return match.group(), match.end()
    if index < len(text) and (text[index].isascii() and text[index].isalpha()):
        return text[index], index + 1
    if index < len(text) and text[index] in SYMBOLS and text[index].isalpha():
        return SYMBOLS[text[index]], index + 1
    raise UnconvertibleError("operand")


def _star(text: str, index: int) -> str:
    """`*` is a postfix star (`a*`, `τ*(3.85)`) or a product (`955000*sqrt(...)`)."""
    before = text[index - 1] if index else " "
    after = text[index + 1] if index + 1 < len(text) else " "
    if before == " " or (after not in " ),(" and not before.isalpha()):
        return r" \cdot "
    return r"^{\ast}"


def _word(text: str, index: int, out: _Writer) -> int:
    """Translate the letter run at `index`; return where it ends."""
    match = _WORD.match(text, index)
    assert match is not None
    word, end = match.group(), match.end()
    if word == "sqrt":
        while end < len(text) and text[end] == " ":
            end += 1
        argument, end = _argument(text, end)
        out.emit(rf"\sqrt{{{argument}}}")
        return end
    if word in BRACKETED:
        if end >= len(text) or text[end] != "(":
            raise UnconvertibleError("bracket-function")
        close = _group(text, end)
        left, right = BRACKETED[word]
        out.emit(f"{left}{to_latex(text[end + 1 : close - 1])}{right}")
        return close
    if word in FUNCTIONS or word in GREEK_NAMES:
        out.emit("\\" + word)
        return end
    if len(word) == 1:
        out.emit(word)
        return end
    raise UnconvertibleError("named-term")


def _power(text: str, index: int, out: _Writer) -> int:
    after = index + 1
    if after < len(text) and text[after].isalpha() and text[after + 1 : after + 2] == "(":
        raise UnconvertibleError("ambiguous-superscript")
    argument, end = _argument(text, after)
    out.emit(f"^{{{argument}}}" if len(argument) > 1 else f"^{argument}")
    return end


def _subscript(text: str, index: int, out: _Writer) -> int:
    after = index + 1
    if after < len(text) and text[after] == "(":
        end = _group(text, after)
        out.emit(f"_{{{to_latex(text[after + 1 : end - 1])}}}")
        return end
    match = re.compile(r"[A-Za-z0-9]+").match(text, after)
    if match is None:
        raise UnconvertibleError("subscript")
    body = match.group()
    out.emit(f"_{{{body}}}" if len(body) > 1 else f"_{body}")
    return match.end()


def to_latex(text: str) -> str:
    """LaTeX for the mathematical expression `text`, or `UnconvertibleError`."""
    out = _Writer()
    bars = 0
    index = 0
    while index < len(text):
        char = text[index]
        for ascii_operator, latex in ((">=", r" \ge "), ("<=", r" \le "), ("!=", r" \ne ")):
            if text.startswith(ascii_operator, index):
                out.emit(latex)
                index += 2
                break
        else:
            if text.startswith("->", index):
                out.emit(r" \to ")
                index += 2
            elif text.startswith("...", index):
                out.emit(r"\ldots ")
                index += 3
            elif text.startswith("..", index):
                out.emit(r"\ldots ")
                index += 2
            elif number := _NUMBER.match(text, index):
                out.emit(_number(number))
                index = number.end()
            elif char.isascii() and char.isalpha():
                index = _word(text, index, out)
            elif char == "√":
                argument, index = _argument(text, index + 1)
                out.emit(rf"\sqrt{{{argument}}}")
            elif char == "^":
                index = _power(text, index, out)
            elif char == "_":
                index = _subscript(text, index, out)
            elif superscript := _SUPERSCRIPT_RUN.match(text, index):
                body = "".join(SUPERSCRIPTS[c] for c in superscript.group())
                out.emit(f"^{{{body}}}" if len(body) > 1 else f"^{body}")
                index = superscript.end()
            elif subscript := _SUBSCRIPT_RUN.match(text, index):
                body = "".join(SUBSCRIPTS.get(c, c) for c in subscript.group())
                out.emit(f"_{{{body}}}" if len(body) > 1 else f"_{body}")
                index = subscript.end()
            elif char == "*":
                out.emit(_star(text, index))
                index += 1
            elif char == "|":
                out.emit(r"\lvert " if bars % 2 == 0 else r"\rvert ")
                bars += 1
                index += 1
            elif char in "{}":
                out.emit(r"\lbrace " if char == "{" else r"\rbrace ")
                index += 1
            elif char in "<>":
                out.emit(f" {char} ")
                index += 1
            elif char == "~":
                out.emit(r"\sim ")
                index += 1
            elif char in SYMBOLS:
                out.emit(SYMBOLS[char])
                index += 1
            elif char == "–" and text[index - 1 : index].isdigit():
                # An en dash in a numeric range, `39–41`: text, since `-` would be a minus.
                out.emit(r"\text{–}")
                index += 1
            elif char in PLAIN:
                out.emit(char)
                index += 1
            else:
                raise UnconvertibleError(f"character-U+{ord(char):04X}")
    if bars % 2:
        raise UnconvertibleError("unpaired-bar")
    # A control word's trailing space is noise before a closing bracket or a script.
    return re.sub(r"(\\[A-Za-z]+) (?=[)\]},^_'/])", r"\1", out.text())


# ---------------------------------------------------------------------------------------
# Classification.
# ---------------------------------------------------------------------------------------

_INTEGER = re.compile(r"^[+−-]?(\d{1,3}(,\d{3})+|0|[1-9]\d{0,5})$")
_LONG_INTEGER = re.compile(r"^\d{7,}$|^0\d+$")
_SCIENTIFIC = re.compile(r"^[+−-]?\d+(\.\d+)?e[+-]?\d+$")
_FRACTION = re.compile(r"^[+−-]?\d+/\d+$")
_DECIMAL = re.compile(r"^[+−~≈-]?\s*\d*\.\d+(…|\.\.\.)?$")
_ANGLE = re.compile(r"^[+−-]?\d+(\.\d+)?°$")
_VARIABLE = re.compile(r"^[^\W\d_]['*]?$")
_VARIABLES = re.compile(r"^[^\W\d_](,\s*[^\W\d_])+$")
_PRODUCT = re.compile(r"^\d+[A-Za-z]$")
_APPLICATION = re.compile(r"^[^\W\d_]\(")
_FUNCTION = re.compile(rf"\b({'|'.join(sorted(FUNCTIONS | set(BRACKETED)))})\b")
_BOUND = re.compile(r"(?<![A-Za-z])s\(")
_EXPRESSION = re.compile(
    "[=<>≤≥≈≠∈∪→↔×·√^+−*/|⌈⌊⟨_…°{}"
    + "".join(SUPERSCRIPTS)
    + "".join(SUBSCRIPTS)
    + r"]|\.\.|\d–\d|\bsqrt\b"
)
# A letter run straight into a digit, `f1` or `Q0`: a label, or a subscript written flat.
_LABEL_IN_EXPRESSION = re.compile(r"(?<![\w.])[A-Za-z]+\d")


@dataclass(frozen=True)
class Classification:
    kind: Kind
    rule: str
    latex: str | None = None


def _math_rule(text: str) -> str | None:
    """The math rule `text` satisfies, before any attempt to translate it."""
    for rule, pattern in (
        ("integer-value", _INTEGER),
        ("scientific-value", _SCIENTIFIC),
        ("fraction", _FRACTION),
        ("decimal-value", _DECIMAL),
        ("angle", _ANGLE),
        ("variable", _VARIABLE),
        ("variables", _VARIABLES),
        ("product", _PRODUCT),
        ("bound-in-s(n)", _BOUND),
        ("application", _APPLICATION),
        ("function", _FUNCTION),
    ):
        if pattern.search(text):
            return rule
    if _EXPRESSION.search(text) or re.search(r"[\[(].*[,;].*[\])]", text):
        return "expression"
    return None


def classify(content: str) -> Classification:  # noqa: PLR0911 -- one verdict per rule
    """Decide what the text of one code span is, and give its LaTeX when it is math."""
    text = content.strip()
    if not text:
        return Classification("identifier", "empty")
    for rule, pattern in _IDENTIFIERS:
        if pattern.search(text) and (rule != "word-or-name" or _SNAKE.search(text)):
            return Classification("identifier", rule)
    if not any(char.isalnum() for char in text):
        return Classification("uncertain", "no-operand")
    if re.fullmatch(r"\d+(/\d+){2,}", text):
        return Classification("uncertain", "slash-sequence")
    if _LONG_INTEGER.match(text):
        return Classification("uncertain", "long-integer")
    if re.search(r"[A-Za-z]{2,}_|_[A-Za-z]{3,}", text):
        return Classification("uncertain", "snake-name-in-expression")
    if _LABEL_IN_EXPRESSION.search(text):
        return Classification("uncertain", "label-in-expression")
    rule = _math_rule(text)
    if rule is None:
        return Classification("uncertain", "no-math-signal")
    try:
        latex = to_latex(text)
    except UnconvertibleError as error:
        return Classification("uncertain", str(error))
    if not latex or "$" in latex or "`" in latex:
        return Classification("uncertain", "unwritable")
    return Classification("math", rule, latex)


# ---------------------------------------------------------------------------------------
# Finding code spans in a Markdown file.
# ---------------------------------------------------------------------------------------

_GENERATED_BEGIN = re.compile(r"^\s*<!--\s*BEGIN\b")
_GENERATED_END = re.compile(r"^\s*<!--\s*END\b")
_BACKTICKS = re.compile(r"`+")


@dataclass(frozen=True)
class CodeSpan:
    """One inline code span: where it is in the file, and what may be done with it."""

    line: int
    start: int
    end: int
    content: str
    context: str | None
    """Why the span may not be converted whatever it holds, or None when it may be."""
    block: tuple[int, int] = (0, 0)
    """The offsets of the paragraph, heading or table row that holds the span."""


@dataclass(frozen=True)
class Finding:
    span: CodeSpan
    classification: Classification
    kept: bool = False
    """A person read this span in context and decided it stays code (see `LEDGER`)."""

    @property
    def converts(self) -> bool:
        return (
            self.classification.kind == "math" and self.span.context is None and not self.kept
        )

    @property
    def kind(self) -> Kind:
        if self.kept:
            return "identifier"
        if self.classification.kind == "math" and self.span.context is not None:
            return "uncertain"
        return self.classification.kind

    @property
    def rule(self) -> str:
        if self.kept:
            return "kept"
        if self.classification.kind == "math" and self.span.context is not None:
            return f"math-but-{self.span.context}"
        return self.classification.rule


def _parser() -> MarkdownIt:
    return MarkdownIt("commonmark").enable("table")


def _generated_lines(lines: Sequence[str]) -> set[int]:
    """Zero-based line numbers inside BEGIN/END generated regions, markers included."""
    inside: set[int] = set()
    depth = 0
    for number, line in enumerate(lines):
        if _GENERATED_BEGIN.match(line):
            depth += 1
        if depth:
            inside.add(number)
        if _GENERATED_END.match(line):
            depth = max(0, depth - 1)
    return inside


def _raw_spans(text: str, offset: int) -> list[tuple[int, int, str]]:
    """(start, end, content) of every code span in `text`, offsets shifted by `offset`.

    CommonMark's rule: a backtick run opens a span closed by the next run of exactly the
    same length; a run with no such partner is literal. A backslash escapes the next
    character outside code, and an HTML comment or autolink holds no code.
    """
    spans: list[tuple[int, int, str]] = []
    index = 0
    while index < len(text):
        char = text[index]
        if char == "\\":
            index += 2
            continue
        if text.startswith("<!--", index):
            close = text.find("-->", index + 4)
            index = len(text) if close < 0 else close + 3
            continue
        if autolink := re.compile(r"<[A-Za-z][\w+.-]{1,31}:[^\s<>]*>").match(text, index):
            index = autolink.end()
            continue
        if char != "`":
            index += 1
            continue
        run = _BACKTICKS.match(text, index)
        assert run is not None
        width = len(run.group())
        search = run.end()
        while True:
            closing = _BACKTICKS.search(text, search)
            if closing is None:
                index = run.end()
                break
            if len(closing.group()) == width:
                body = text[run.end() : closing.start()].replace("\n", " ")
                if body.startswith(" ") and body.endswith(" ") and body.strip():
                    body = body[1:-1]
                spans.append((offset + index, offset + closing.end(), body))
                index = closing.end()
                break
            search = closing.end()
    return spans


def _parsed_spans(token: Token) -> list[tuple[str, str | None]]:
    """The parser's code spans in one inline token: content, and a context if any.

    Two contexts come from the parse. A span in link text stays code. And a span that
    opens its inline content -- the first thing in a paragraph or a table cell -- stays
    code when that content ends in a digit: `dollarmath` checks the character before an
    opening `$` by index, and at position 0 the index wraps to the content's last
    character, so kpress refuses `$x$ ... 11` as though the `$` followed a digit.
    """
    children = token.children or []
    wraps = token.content.rstrip()[-1:].isdigit()
    spans: list[tuple[str, str | None]] = []
    depth = 0
    for position, child in enumerate(children):
        if child.type == "link_open":
            depth += 1
        elif child.type == "link_close":
            depth -= 1
        elif child.type == "code_inline":
            context = "link-text" if depth else None
            leading = all(c.type == "text" and not c.content for c in children[:position])
            if context is None and wraps and leading:
                context = "kpress-leading-dollar"
            spans.append((child.content, context))
    return spans


def code_spans(text: str) -> list[CodeSpan]:
    """Every inline code span outside code blocks and generated regions, in order."""
    lines = text.splitlines(keepends=True)
    starts = [0]
    for line in lines:
        starts.append(starts[-1] + len(line))
    generated = _generated_lines(lines)
    tokens = _parser().parse(text)

    # Group inline tokens by their source lines: a table row is one range holding many
    # cells, a paragraph is one range holding one inline token.
    blocks: dict[tuple[int, int], list[tuple[str, str | None]]] = {}
    headings: set[tuple[int, int]] = set()
    for position, token in enumerate(tokens):
        if token.type != "inline" or token.map is None:
            continue
        first, last = token.map
        if first in generated:
            continue
        key = (first, last)
        blocks.setdefault(key, []).extend(_parsed_spans(token))
        if position and tokens[position - 1].type == "heading_open":
            headings.add(key)

    found: list[CodeSpan] = []
    for (first, last), parsed in blocks.items():
        if not parsed:
            continue
        bounds = (starts[first], starts[last])
        raw = _raw_spans(text[bounds[0] : bounds[1]], bounds[0])
        agree = [content for _, _, content in raw] == [content for content, _ in parsed]
        if not agree:
            # The parser is the authority on what a span is; offsets we cannot trust are
            # reported so a person can look, and never rewritten.
            found.extend(
                CodeSpan(first + 1, -1, -1, content, "parser-disagreement", bounds)
                for content, _ in parsed
            )
            continue
        for (start, end, content), (_, link) in zip(raw, parsed, strict=True):
            line = text.count("\n", 0, start) + 1
            found.append(
                CodeSpan(
                    line,
                    start,
                    end,
                    content,
                    _context(text, start, end, link, heading=(first, last) in headings),
                    bounds,
                )
            )
    found.sort(key=lambda span: (span.line, span.start))
    return found


def _context(text: str, start: int, end: int, link: str | None, *, heading: bool) -> str | None:
    if heading:
        return "heading"
    if link is not None:
        return link
    if "\n" in text[start:end]:
        return "line-break"
    before = text[start - 1] if start else " "
    after = text[end] if end < len(text) else " "
    if before.isalnum() or after.isalnum() or "$" in (before, after) or before == "\\":
        return "adjacent"
    return None


@dataclass(frozen=True)
class Keep:
    """A math-like span a person read in context and decided stays code.

    `where`, when set, limits the exception to spans whose paragraph (or heading, or
    table row) contains that text, compared with its whitespace collapsed so a reflow
    does not move it. It is for a file that uses one letter both ways: `S` naming the
    significance axis in one sentence and a point set in another.
    """

    span: str
    where: str | None = None

    def matches(self, text: str, span: CodeSpan) -> bool:
        if span.content != self.span:
            return False
        if self.where is None:
            return True
        start, end = span.block
        return self.where in " ".join(text[start:end].split())


def analyze(text: str, keep: Collection[Keep] = ()) -> list[Finding]:
    """Classify every code span in `text`; spans a `keep` entry matches stay code."""
    return [
        Finding(span, classify(span.content), kept=any(k.matches(text, span) for k in keep))
        for span in code_spans(text)
    ]


# ---------------------------------------------------------------------------------------
# The ledger of migrated files.
# ---------------------------------------------------------------------------------------

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
LEDGER = PACKING / "devtools" / "math-migrated.yaml"


def _keep(entry: object, where: str) -> Keep:
    if isinstance(entry, str):
        return Keep(entry)
    if isinstance(entry, dict):
        fields = cast(dict[str, object], entry)
        span, context = fields.get("span"), fields.get("where")
        if isinstance(span, str) and (context is None or isinstance(context, str)):
            return Keep(span, context)
    raise TypeError(f"{where}: a keep entry is a span, or a mapping of `span` and `where`")


def load_ledger(path: Path = LEDGER) -> dict[str, tuple[Keep, ...]]:
    """Each migrated file, repository-relative, with the math-like spans kept as code.

    The file maps each path to `{keep: [...]}`, or to nothing. A kept span is one a
    person read in context and decided is not mathematics there -- `V` and `C` naming
    the verification and confirmation ladders, say -- so neither this tool nor the
    ratchet converts it or complains about it.
    """
    document = load_yaml(path.read_text(encoding="utf-8")) or {}
    files = document.get("files") or {}
    if not isinstance(files, dict):
        raise TypeError(f"{path}: `files` must map a path to its settings")
    ledger: dict[str, tuple[Keep, ...]] = {}
    for name, settings in cast(dict[str, object], files).items():
        entries: object = []
        if isinstance(settings, dict):
            entries = cast(dict[str, object], settings).get("keep") or []
        if not isinstance(entries, list):
            raise TypeError(f"{path}: `{name}.keep` must be a list")
        where = f"{path.name}: {name}"
        ledger[str(name)] = tuple(_keep(entry, where) for entry in cast(list[object], entries))
    return ledger


def kept_for(path: Path, ledger: dict[str, tuple[Keep, ...]] | None = None) -> tuple[Keep, ...]:
    """The kept spans the ledger names for `path`, or none when it is not listed."""
    try:
        relative = path.resolve().relative_to(REPO).as_posix()
    except ValueError:
        return ()
    return (load_ledger() if ledger is None else ledger).get(relative, ())


# ---------------------------------------------------------------------------------------
# Rewriting, and the two measurements that must pass before a write.
# ---------------------------------------------------------------------------------------


def migrate(text: str, keep: Collection[Keep] = ()) -> tuple[str, list[Finding]]:
    """`text` with every convertible math span written as `$...$`, and the findings."""
    findings = analyze(text, keep)
    pieces: list[str] = []
    cursor = 0
    for finding in findings:
        if not finding.converts:
            continue
        latex = finding.classification.latex
        assert latex is not None
        pieces.extend((text[cursor : finding.span.start], f"${latex}$"))
        cursor = finding.span.end
    pieces.append(text[cursor:])
    return "".join(pieces), findings


def kpress_parser() -> MarkdownIt:
    """The math parsing kpress applies: `dollarmath` with the options kpress passes."""
    return _parser().use(dollarmath_plugin, allow_space=False, allow_digits=False)


def math_inline(text: str) -> Counter[str]:
    """The content of every inline math span kpress's parser reads in `text`."""
    found: Counter[str] = Counter()
    for token in kpress_parser().parse(text):
        for child in token.children or []:
            if child.type == "math_inline":
                found[child.content] += 1
    return found


def verify_kpress(before: str, after: str, findings: Sequence[Finding]) -> list[str]:
    """Problems if kpress would not read each converted span back as what was written."""
    expected = math_inline(before)
    for finding in findings:
        if finding.converts and finding.classification.latex is not None:
            expected[finding.classification.latex] += 1
    actual = math_inline(after)
    problems = [
        f"kpress reads {actual[latex]} math span(s) `{latex}`, expected {count}"
        for latex, count in sorted(expected.items())
        if actual[latex] != count
    ]
    problems.extend(
        f"kpress reads an unexpected math span `{latex}`"
        for latex in sorted(actual)
        if latex not in expected
    )
    return problems


def verify_formatter(path: Path, after: str, command: Sequence[str]) -> list[str]:
    """Problems if the pinned flowmark would split or retype a math span in `after`."""
    with tempfile.TemporaryDirectory(prefix="migrate-math-") as directory:
        copy = Path(directory) / path.name
        copy.write_text(after, encoding="utf-8")
        result = check_file(copy, list(command))
    if result.ok:
        return []
    return [
        (
            f"flowmark changes {result.changed} math span(s), breaks {result.broken}, "
            f"and moves the count from {result.before} to {result.after}"
        )
    ]


# ---------------------------------------------------------------------------------------
# Command line.
# ---------------------------------------------------------------------------------------


def _report(path: Path, findings: Sequence[Finding], *, conversions: bool) -> None:
    kinds = Counter(finding.kind for finding in findings)
    converting = sum(1 for finding in findings if finding.converts)
    print(
        f"{path.as_posix()}: {len(findings)} code spans -- {converting} math to convert, "
        f"{kinds['identifier']} identifier, {kinds['uncertain']} uncertain"
    )
    rules = Counter(finding.rule for finding in findings if finding.kind == "uncertain")
    if rules:
        print("  uncertain by rule: " + ", ".join(f"{r} {n}" for r, n in rules.most_common()))
    for finding in findings:
        if finding.kind == "uncertain":
            line = finding.span.line
            print(f"  {line:>5d}  uncertain [{finding.rule}]  `{finding.span.content}`")
        elif conversions and finding.converts:
            print(
                f"  {finding.span.line:>5d}  math [{finding.rule}]  `{finding.span.content}`"
                f"  ->  ${finding.classification.latex}$"
            )


def _arguments() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="migrate_math", description="Convert math written as code spans to LaTeX math."
    )
    parser.add_argument("files", nargs="+", type=Path, metavar="FILE")
    parser.add_argument("--apply", action="store_true", help="rewrite the files in place")
    parser.add_argument(
        "--report", action="store_true", help="print counts and every uncertain span"
    )
    parser.add_argument(
        "--conversions", action="store_true", help="with the report, list every conversion"
    )
    parser.add_argument(
        "--flowmark", default=None, metavar="COMMAND", help="formatter to measure against"
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _arguments().parse_args(argv)
    status = 0
    command: list[str] | None = None
    for path in arguments.files:
        if not path.is_file():
            print(f"no such file: {path.as_posix()}", file=sys.stderr)
            return 2
        before = path.read_text(encoding="utf-8")
        after, findings = migrate(before, kept_for(path))
        if arguments.report or arguments.conversions or not arguments.apply:
            _report(path, findings, conversions=arguments.conversions)
        if not arguments.apply or after == before:
            continue
        if command is None:
            command = shlex.split(arguments.flowmark or pinned_formatter())
        problems = verify_kpress(before, after, findings)
        problems += verify_formatter(path, after, command)
        if problems:
            status = 1
            print(f"{path.as_posix()}: refused, nothing written", file=sys.stderr)
            for problem in problems:
                print(f"  {problem}", file=sys.stderr)
            continue
        path.write_text(after, encoding="utf-8")
        converted = sum(1 for finding in findings if finding.converts)
        print(f"{path.as_posix()}: wrote {converted} math span(s)")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
