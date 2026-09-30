#!/usr/bin/env python3
"""The frontier atlas and tutorial pages of the published site, and the site's link checks.

`devtools.render_overview` collects the two pages from `pages()` and renders them into the
shared site shell.

**The frontier atlas** (`frontier.html`) has one row for every case, each read from the
`packing:` envelope of `packing/frontier/n-NNN.md` through
`render_research_tables.load_cases` and validated against the enforced
`packing.squares:SquarePackingCase/v2` contract, as `sqpack.cli.validate` has
`devtools.validate_schemas` do; an invalid record refuses the render rather than rendering
a blank cell. No value on the page is typed by hand or read from `STATUS.md`. Exact forms
are set as mathematics through kpress, decimals are cut and never rounded, a reported value
the verified lane confirms at its declared precision is printed once, and a lower bound
reads `≥` unless a register entry citing its evidence claims it strictly. The page's prose
is `templates/frontier-article.md`, whose every fact is a placeholder.

**The tutorial** (`tutorial.html`) is `TUTORIAL.md` rendered by kpress in sanitized mode
with a table-of-contents rail, its heading ids from kpress's GitHub-compatible slugger so
that `TUTORIAL.md#…` anchors carry over. Its links are rewritten in the parsed HTML, never
by a pattern over the Markdown: a link to a site page becomes that page, a reader document
the document on GitHub's default branch, and a record a permalink at the build commit.

**Link checks.** `link_problems` proves a page's links offline: every repository path a
link names exists at the build commit, read from one `git ls-tree` listing (the Pages jobs
clone with `filter: blob:none`, where `git cat-file` would fetch blobs over the network),
and every in-page anchor has its target, which is kpress's `broken_anchor` rule raised to a
failure. `default_branch_links` lists the links a page names on `main` rather than on the
build commit, for the published-site check's ref rule.
"""

from __future__ import annotations

import operator
import posixpath
import re
import subprocess
import sys
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction
from functools import cache
from html import escape, unescape
from html.parser import HTMLParser
from math import floor, isqrt
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal
from urllib.parse import quote, unquote, urlsplit

from devtools import (
    build_bound_citations,
    check_basic_bounds,
    overview_media,
    render_explainer,
    render_research_tables,
    validate_schemas,
)
from devtools.site_kit import REPO_URL, SITE_NAME, SITE_URL, TEMPLATES, Page, base_for
from sqpack.assurance import bounds_agree_at_declared_precision
from sqpack.yamlio import safe_load

if TYPE_CHECKING:
    from kpress.format.model import DocumentTree, TocEntry

REPO = render_explainer.REPO
FRONTIER = render_research_tables.FRONTIER
EVIDENCE = FRONTIER / "evidence.yaml"
RESULTS = FRONTIER / "results.yaml"
BOUND_CITATIONS = validate_schemas.BOUND_CITATIONS
TUTORIAL = REPO / "TUTORIAL.md"
FRONTIER_TEMPLATE = TEMPLATES / "frontier-article.md"
#: The site's table script: sorting, and the filters above a `data-site-table`.
TABLE_SCRIPT = Path(__file__).with_name("overview") / "table.js"

#: Every repository path these pages read. The case records, the evidence and results
#: registers and the case schema are all under `frontier/`.
RENDER_INPUTS: tuple[Path, ...] = (
    Path(__file__),
    FRONTIER_TEMPLATE,
    FRONTIER,
    BOUND_CITATIONS,
    TUTORIAL,
    Path(render_research_tables.__file__),
    Path(validate_schemas.__file__),
    Path(check_basic_bounds.__file__),
    Path(build_bound_citations.__file__),
    Path(overview_media.__file__),
)

#: The declaration every case record carries, as `sqpack.cli.validate` requires it.
CASE_CONTRACT = {
    "contract": "packing.squares:SquarePackingCase/v2",
    "schema": "square-packing-case.schema.yaml",
    "envelope": "packing",
    "status": "enforced",
}
DEFAULT_BRANCH = "main"
RAW_URL = "https://raw.githubusercontent.com/jlevy/squares"
#: Decimal places a value is shown to before it is cut and marked with an ellipsis.
PLACES = 7
#: Places the sort key of a computed gap carries.
SORT_PLACES = 12
#: Significant digits for evaluating a radical; far past `SORT_PLACES`.
PRECISION = 60
ELLIPSIS = "…"
THUMBNAIL_SIZE = 48

FRONTIER_DESCRIPTION = (
    "One row for every case of the square packing problem the record tracks: the best "
    "known packing, and the reported and verified bounds on s(n), each read from the "
    "case's record."
)
TUTORIAL_DESCRIPTION = (
    "A conceptual on-ramp to square packing: what the objects are, why the approach is "
    "shaped the way it is, and what the research has and has not established."
)

UPPER_METHODS = {
    "trivial-grid": "grid",
    "hand-construction": "by hand",
    "diagonal-strip": "diagonal strip",
    "pattern-family": "pattern family",
    "extension": "extension",
    "composition": "composition",
    "simulated-annealing": "annealing",
    "inflation-billiard": "inflation billiard",
}
LOWER_KINDS = {
    "area": "area",
    "perfect-square": "perfect square",
    "nagamochi": "Nagamochi",
    "monotonicity": "monotonicity",
    "unavoidable-points": "unavoidable points",
    "counting": "counting",
}


# ---------------------------------------------------------------------------------------
# Exact forms: the record's ASCII expressions, read into mathematics and exact values.
# ---------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Num:
    text: str


@dataclass(frozen=True)
class Call:
    """`sqrt(x)` (also written `√k`, as `pretty` prints it) or `floor(x)`."""

    name: str
    arg: Node


@dataclass(frozen=True)
class Op:
    """A binary operation; `*` also stands for juxtaposition, as in `(1/2)√2`."""

    op: str
    left: Node
    right: Node


@dataclass(frozen=True)
class Neg:
    arg: Node


@dataclass(frozen=True)
class Group:
    inner: Node


type Node = Num | Call | Op | Neg | Group

_TOKEN = re.compile(r"\s*(?:(\d+(?:\.\d+)?)|(sqrt|floor)|(√)|([-+*/()]))")


class ExactFormError(ValueError):
    """An exact form this reader does not understand."""


def _tokens(text: str) -> list[str]:
    tokens: list[str] = []
    at = 0
    text = text.rstrip()
    while at < len(text):
        match = _TOKEN.match(text, at)
        if match is None or match.end() == at:
            raise ExactFormError(f"cannot read {text!r} at {text[at:]!r}")
        tokens.append(next(group for group in match.groups() if group is not None))
        at = match.end()
    return tokens


class _Reader:
    """Recursive descent over `+ -`, then `* /` and juxtaposition, then unary minus."""

    def __init__(self, text: str) -> None:
        self.text = text
        self.tokens = _tokens(text)
        self.at = 0

    def peek(self) -> str | None:
        return self.tokens[self.at] if self.at < len(self.tokens) else None

    def take(self, expected: str | None = None) -> str:
        token = self.peek()
        if token is None or (expected is not None and token != expected):
            raise ExactFormError(f"cannot read {self.text!r}: expected {expected or 'more'}")
        self.at += 1
        return token

    def read(self) -> Node:
        node = self.sum()
        if self.peek() is not None:
            raise ExactFormError(f"cannot read {self.text!r}: {self.peek()!r} left over")
        return node

    def sum(self) -> Node:
        node = self.product()
        while self.peek() in {"+", "-"}:
            op = self.take()
            node = Op(op, node, self.product())
        return node

    def product(self) -> Node:
        node = self.unary()
        while True:
            token = self.peek()
            if token in {"*", "/"}:
                self.take()
                node = Op(token, node, self.unary())
            elif token is not None and (token[0].isdigit() or token in {"(", "sqrt", "√"}):
                node = Op("*", node, self.unary())
            else:
                return node

    def unary(self) -> Node:
        if self.peek() == "-":
            self.take()
            return Neg(self.unary())
        return self.atom()

    def atom(self) -> Node:
        token = self.take()
        if token[0].isdigit():
            return Num(token)
        if token == "(":
            inner = self.sum()
            self.take(")")
            return Group(inner)
        if token == "√":
            radicand = self.take()
            if not radicand.isdigit():
                raise ExactFormError(f"cannot read {self.text!r}: √ takes digits")
            return Call("sqrt", Num(radicand))
        if token in {"sqrt", "floor"}:
            self.take("(")
            inner = self.sum()
            self.take(")")
            return Call(token, inner)
        raise ExactFormError(f"cannot read {self.text!r} at {token!r}")


def read_exact(text: str) -> Node:
    """An exact form, as `render_research_tables.pretty` prints it, read into a tree."""
    return _Reader(text).read()


def _unwrap(node: Node) -> Node:
    while isinstance(node, Group):
        node = node.inner
    return node


def _is_fraction(node: Node) -> bool:
    node = _unwrap(node)
    return (
        isinstance(node, Op)
        and node.op == "/"
        and isinstance(_unwrap(node.left), Num)
        and isinstance(_unwrap(node.right), Num)
    )


def tex(node: Node, *, coefficient: bool = False) -> str:
    """The tree as idiomatic LaTeX: `\\frac`, `\\tfrac` for a coefficient, `\\sqrt`."""
    if isinstance(node, Num):
        return node.text
    if isinstance(node, Group):
        inner = _unwrap(node)
        if isinstance(inner, Num | Call) or _is_fraction(inner):
            return tex(inner, coefficient=coefficient)
        return rf"\left({tex(inner)}\right)"
    if isinstance(node, Neg):
        return f"-{tex(node.arg)}"
    if isinstance(node, Call):
        argument = tex(node.arg)
        return (
            rf"\sqrt{{{argument}}}" if node.name == "sqrt" else rf"\lfloor {argument} \rfloor"
        )
    return _tex_operation(node, coefficient=coefficient)


def _tex_operation(node: Op, *, coefficient: bool) -> str:
    if node.op == "/":
        command = r"\tfrac" if coefficient else r"\frac"
        return rf"{command}{{{tex(node.left)}}}{{{tex(node.right)}}}"
    if node.op == "*":
        right = _unwrap(node.right)
        if isinstance(right, Call) and right.name == "sqrt":
            return f"{tex(node.left, coefficient=True)}{tex(node.right)}"
        return rf"{tex(node.left)} \cdot {tex(node.right)}"
    # The reader is left-associative, so a sum on the right was written in parentheses,
    # and its Group keeps them.
    return f"{tex(node.left)} {node.op} {tex(node.right)}"


#: An exact real in Q(√2, √3, …): the coefficient of each square-free radicand, with the
#: rational part under radicand 1.
type Surd = dict[int, Fraction]


def _square_free(k: int) -> tuple[int, int]:
    """`k = outside² · inside` with `inside` square-free."""
    outside, inside, factor = 1, k, 2
    while factor * factor <= inside:
        while inside % (factor * factor) == 0:
            inside //= factor * factor
            outside *= factor
        factor += 1
    return outside, inside


def _surd_sum(left: Surd, right: Surd, sign: int = 1) -> Surd:
    total = dict(left)
    for radicand, coefficient in right.items():
        total[radicand] = total.get(radicand, Fraction(0)) + sign * coefficient
    return {radicand: value for radicand, value in total.items() if value}


def _surd_product(left: Surd, right: Surd) -> Surd:
    total: Surd = {}
    for a, x in left.items():
        for b, y in right.items():
            outside, inside = _square_free(a * b)
            total = _surd_sum(total, {inside: x * y * outside})
    return total


def _rational(surd: Surd) -> Fraction | None:
    if set(surd) <= {1}:
        return surd.get(1, Fraction(0))
    return None


def surd(node: Node) -> Surd | None:
    """The tree's exact value, or None where it leaves the square-root field (`√(1 + √2)`)."""
    if isinstance(node, Num):
        value = Fraction(node.text)
        return {1: value} if value else {}
    if isinstance(node, Group):
        return surd(node.inner)
    if isinstance(node, Neg):
        inner = surd(node.arg)
        return None if inner is None else {k: -v for k, v in inner.items()}
    if isinstance(node, Call):
        inner = surd(node.arg)
        if inner is None:
            return None
        return _floor_surd(inner) if node.name == "floor" else _sqrt_surd(inner)
    return _operation_surd(node)


def _operation_surd(node: Op) -> Surd | None:
    left, right = surd(node.left), surd(node.right)
    if left is None or right is None:
        return None
    if node.op in {"+", "-"}:
        return _surd_sum(left, right, 1 if node.op == "+" else -1)
    if node.op == "*":
        return _surd_product(left, right)
    divisor = _rational(right)
    return {k: v / divisor for k, v in left.items()} if divisor else None


def _sqrt_surd(inner: Surd) -> Surd | None:
    """`√x` for a non-negative rational `x`; a radical under a radical leaves the field."""
    value = _rational(inner)
    if value is None or value < 0:
        return None
    outside, inside = _square_free(value.numerator * value.denominator)
    return {inside: Fraction(outside, value.denominator)} if outside else {}


def _floor_surd(inner: Surd) -> Surd | None:
    """`⌊x⌋` for a rational or a single non-negative radical term, exactly."""
    value = _rational(inner)
    if value is None:
        if len(inner) != 1:
            return None
        ((radicand, coefficient),) = inner.items()
        if coefficient < 0:
            return None
        # ⌊p·√r / q⌋ = ⌊isqrt(p²·r) / q⌋ for whole p, r and q.
        value = Fraction(isqrt(coefficient.numerator**2 * radicand) // coefficient.denominator)
    whole = floor(value)
    return {1: Fraction(whole)} if whole else {}


_OPERATIONS: dict[str, Callable[[Decimal, Decimal], Decimal]] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


def _decimal(node: Node) -> Decimal:
    """The tree's value to `PRECISION` digits, for forms outside the square-root field."""
    if isinstance(node, Num):
        return Decimal(node.text)
    if isinstance(node, Group | Neg):
        inner = _decimal(node.inner if isinstance(node, Group) else node.arg)
        return inner if isinstance(node, Group) else -inner
    if isinstance(node, Call):
        inner = _decimal(node.arg)
        return inner.sqrt() if node.name == "sqrt" else Decimal(floor(inner))
    return _OPERATIONS[node.op](_decimal(node.left), _decimal(node.right))


def surd_decimal(value: Surd) -> Decimal:
    total = Decimal(0)
    for radicand, coefficient in value.items():
        term = Decimal(coefficient.numerator) / Decimal(coefficient.denominator)
        total += term if radicand == 1 else term * Decimal(radicand).sqrt()
    return total


def cut(value: Fraction, *, places: int = PLACES, exact: bool = True) -> str:
    """A non-negative value in decimals: whole where it terminates within `places`, else
    cut there, never rounded, and marked with an ellipsis. An inexact value (a radical's
    expansion) is always marked.
    """
    if value < 0:
        raise ValueError(f"cut() shows non-negative values; got {value}")
    if exact:
        for shown in range(places + 1):
            scaled = value * 10**shown
            if scaled.denominator == 1:
                return _fixed(scaled.numerator, shown)
    return _fixed(value.numerator * 10**places // value.denominator, places) + ELLIPSIS


def _fixed(scaled: int, places: int) -> str:
    if places == 0:
        return str(scaled)
    whole, fraction = divmod(scaled, 10**places)
    return f"{whole}.{fraction:0{places}d}"


@dataclass(frozen=True)
class Shown:
    """One bound as the page prints it.

    `value` and `exact` are the record's own strings, carried on the cell as `data-value`
    and `data-exact` so a test can parse the value back. `tex` is the exact form as LaTeX,
    None for an integer or a bound with no closed form; `decimal` is the value cut;
    `magnitude` is the exact value where the form is rational, else a `PRECISION`-digit
    approximation; `surd` is the exact value in the square-root field where it has one.
    """

    value: str
    exact: str | None
    tex: str | None
    decimal: str
    magnitude: Fraction
    surd: Surd | None
    root_of: str | None = None


_ROOT = re.compile(r"root\((?P<name>[A-Za-z0-9_]+),\s*(?P<value>\d+(?:\.\d+)?)\)")


def shown(bound: Mapping[str, Any]) -> Shown:
    """A bound's cell: its exact form where it has one, as `compact_bound` chooses."""
    value = str(bound["value"])
    exact = bound.get("exact_form") or None
    if exact is None:
        recorded = Fraction(value)
        return Shown(value, None, None, cut(recorded), recorded, None)
    root = _ROOT.fullmatch(str(exact))
    if root is not None:
        approximation = Fraction(root["value"])
        return Shown(
            value,
            exact,
            None,
            cut(approximation, exact=False),
            approximation,
            None,
            root_of=root["name"],
        )
    printed = render_research_tables.compact_bound(dict(bound)).strip("`")
    node = read_exact(printed)
    exact_value = surd(node)
    rational = None if exact_value is None else _rational(exact_value)
    if rational is not None:
        form = None if rational.denominator == 1 else tex(node)
        return Shown(value, exact, form, cut(rational), rational, exact_value)
    with localcontext() as context:
        context.prec = PRECISION
        approximation = Fraction(
            surd_decimal(exact_value) if exact_value is not None else _decimal(node)
        )
    return Shown(
        value, exact, tex(node), cut(approximation, exact=False), approximation, exact_value
    )


@dataclass(frozen=True)
class Gap:
    """Verified upper minus verified lower: exact where both bounds are in the field.

    `decimal` is the gap cut for the cell, and `sort` the same cut further, for `table.js`.
    """

    decimal: str
    sort: str
    exact: bool


def gap(upper: Shown, lower: Shown) -> Gap:
    """Verified upper minus verified lower, refused if the record puts the upper below."""
    difference = None
    if upper.surd is not None and lower.surd is not None:
        difference = _surd_sum(upper.surd, lower.surd, -1)
        rational = _rational(difference)
        if rational is not None:
            if rational < 0:
                raise SystemExit(f"a verified upper bound {upper.exact} is below {lower.exact}")
            return Gap(cut(rational), cut(rational, places=SORT_PLACES), exact=True)
        with localcontext() as context:
            context.prec = PRECISION
            approximation = Fraction(surd_decimal(difference))
    else:
        approximation = upper.magnitude - lower.magnitude
    if approximation < 0:
        raise SystemExit(f"a verified upper bound {upper.value} is below {lower.value}")
    return Gap(
        cut(approximation, exact=False),
        cut(approximation, places=SORT_PLACES, exact=False).removesuffix(ELLIPSIS),
        exact=difference is not None,
    )


# ---------------------------------------------------------------------------------------
# The record: validated cases, relations from the register, evidence lines, recent bounds.
# ---------------------------------------------------------------------------------------


def case_problems(path: Path, case: Mapping[str, Any]) -> list[str]:
    """What is wrong with one case file under its enforced contract, one line each."""
    problems = [f"{path.name}: {problem}" for problem in validate_schemas.check(path)]
    meta = safe_load(path.read_text(encoding="utf-8").split("---\n")[1]).get("softschema")
    if meta != CASE_CONTRACT:
        problems.append(f"{path.name}: declares {meta}, not the enforced {CASE_CONTRACT}")
    if case.get("n") != int(path.stem.removeprefix("n-")):
        problems.append(f"{path.name}: records n = {case.get('n')!r}")
    return problems


@cache
def _validated(frontier: Path) -> tuple[Mapping[str, Any], ...]:
    paths = sorted(frontier.glob("n-*.md"))
    cases = render_research_tables.load_cases()
    if len(paths) != len(cases):
        raise SystemExit(f"{len(paths)} case files but {len(cases)} cases loaded")
    problems = [
        problem
        for path, case in zip(paths, cases, strict=True)
        for problem in case_problems(path, case)
    ]
    if problems:
        for problem in problems:
            print(f"frontier.html: {problem}", file=sys.stderr)
        raise SystemExit(
            f"{len(problems)} case records fail their contract; refusing to render the "
            "frontier atlas"
        )
    return tuple(cases)


def frontier_cases() -> tuple[Mapping[str, Any], ...]:
    """Every case record, loaded by `load_cases` and validated against its contract."""
    return _validated(render_research_tables.FRONTIER)


def entry_lines(path: Path, prefix: str) -> dict[str, int]:
    """The line of each `  - id: <prefix>…` entry, for a permalink's `#L` anchor."""
    lines: dict[str, int] = {}
    pattern = re.compile(rf"^  - id: ({re.escape(prefix)}\S+)$")
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if match := pattern.match(line):
            lines[match.group(1)] = number
    return lines


_CLAIMED = re.compile(r"s\((\d+)\)\s*(>=|≥|>)\s*(\d+(?:/\d+)?(?:\.\d+)?)")


@dataclass(frozen=True)
class Claim:
    """A register entry's claim on one case's lower bound: `s(n) > value` or `≥`."""

    result: str
    n: int
    strict: bool
    value: Fraction
    evidence: frozenset[str]


def register_claims(results: Sequence[Mapping[str, Any]]) -> list[Claim]:
    """Every `s(n) ≥ v` or `s(n) > v` a register entry's headline or claim states."""
    claims = []
    for entry in results:
        text = f"{entry.get('headline', '')} {entry.get('claim', '')}"
        claims.extend(
            Claim(
                result=str(entry["id"]),
                n=int(match.group(1)),
                strict=match.group(2) == ">",
                value=Fraction(match.group(3)),
                evidence=frozenset(entry.get("evidence") or ()),
            )
            for match in _CLAIMED.finditer(text)
        )
    return claims


def relation(
    n: int, bound: Mapping[str, Any], magnitude: Fraction, claims: Sequence[Claim]
) -> tuple[str, tuple[str, ...]]:
    """`>` and the entries claiming it, where a register entry citing the bound's evidence
    claims the strict inequality at exactly its value; else `≥`, which the record states.
    """
    evidence = set(bound.get("evidence") or ())
    strict = tuple(
        dict.fromkeys(
            claim.result
            for claim in claims
            if claim.strict and claim.n == n and claim.value == magnitude
            if claim.evidence & evidence
        )
    )
    return (">", strict) if strict else ("≥", ())


def recent_lower_bounds() -> frozenset[int]:
    """The cases whose lower bound the atlas figure stars, from `bound-citations.json`."""
    document = safe_load(BOUND_CITATIONS.read_text(encoding="utf-8"))
    return frozenset(
        int(entry["n"])
        for entry in document["citations"]["entries"]
        if entry.get("lower") and entry["lower"].get("recent")
    )


# ---------------------------------------------------------------------------------------
# The frontier atlas page.
# ---------------------------------------------------------------------------------------


#: kpress diagnostics that are warnings to kpress and failures here: an in-page link with
#: no target, and a formula kpress could not read, which would reach the page as source.
REFUSED_DIAGNOSTICS = frozenset({"broken_anchor", "math_render_error"})


def parse_markdown_html(
    source: str, *, title: str, trust_mode: Literal["trusted", "sanitized"], where: str
) -> DocumentTree:
    """Render Markdown with kpress as the site's pages are, refusing on any error.

    `REFUSED_DIAGNOSTICS` are failures here, though kpress only warns of them. Math is
    `auto`, with the explainer's kerning inside each `$…$` span, so formulas set as the
    explainer's do.
    """
    from kpress.format.markdown import parse_markdown  # noqa: PLC0415

    document = parse_markdown(
        render_explainer.kerned_math_spans(source),
        title=title,
        trust_mode=trust_mode,
        math="auto",
    )
    failures = [
        diagnostic
        for diagnostic in document.diagnostics
        if diagnostic.severity == "error" or diagnostic.type in REFUSED_DIAGNOSTICS
    ]
    for diagnostic in document.diagnostics:
        print(f"{where}: {diagnostic.severity}: {diagnostic.message}", file=sys.stderr)
    if failures:
        raise SystemExit(f"{where} did not render cleanly; refusing to write the page")
    return document


class Formulas:
    """The inline formulas of a page, all set by one kpress parse.

    `slot` holds a formula's place in the HTML being built and `fill` puts kpress's markup
    for every formula in its place: the TeX that KaTeX typesets, and MathML beneath it. One
    parse of all of them costs what a few separate parses do.
    """

    OPEN, CLOSE = "\ue000", "\ue001"

    def __init__(self) -> None:
        self.sources: dict[str, int] = {}

    def slot(self, source: str) -> str:
        index = self.sources.setdefault(source, len(self.sources))
        return f"{self.OPEN}{index}{self.CLOSE}"

    def fill(self, html: str) -> str:
        if not self.sources:
            return html
        document = parse_markdown_html(
            "\n\n".join(f"${source}$" for source in self.sources),
            title="formulas",
            trust_mode="trusted",
            where="the frontier atlas's formulas",
        )
        rendered = re.findall(r"<p>(.*?)</p>", document.html, flags=re.DOTALL)
        if len(rendered) != len(self.sources) or not all(
            item.startswith('<span class="kpress-math') for item in rendered
        ):
            raise SystemExit("kpress did not set each formula as one inline formula")
        return re.sub(
            f"{self.OPEN}(\\d+){self.CLOSE}", lambda match: rendered[int(match[1])], html
        )


@dataclass(frozen=True)
class Links:
    """Permalinks at the build commit, and the register lines they anchor to."""

    commit: str
    evidence: Mapping[str, int]
    results: Mapping[str, int]

    def blob(self, path: str, line: int | None = None) -> str:
        anchor = f"#L{line}" if line else ""
        return f"{REPO_URL}/blob/{self.commit}/{quote(path)}{anchor}"

    def tree(self, path: str) -> str:
        return f"{REPO_URL}/tree/{self.commit}/{quote(path)}"

    def evidence_link(self, identifier: str) -> str:
        if identifier not in self.evidence:
            raise SystemExit(f"evidence {identifier} is cited but not in evidence.yaml")
        url = self.blob("packing/frontier/evidence.yaml", self.evidence[identifier])
        return f'<a href="{escape(url)}"><code>{escape(identifier)}</code></a>'

    def result_link(self, identifier: str) -> str:
        url = self.blob("packing/frontier/results.yaml", self.results[identifier])
        return f'<a href="{escape(url)}">{escape(identifier)}</a>'


def value_html(bound: Shown, formulas: Formulas, *, relation_mark: str | None = None) -> str:
    """A value: its relation, its exact form as mathematics, and its decimal, cut."""
    parts = []
    if relation_mark:
        parts.append(f'<span class="frontier-relation">{escape(relation_mark)}</span> ')
    if bound.tex is not None:
        parts.append(f'<span class="frontier-exact">{formulas.slot(bound.tex)}</span> ')
        parts.append(f'<span class="frontier-decimal">= {escape(bound.decimal)}</span>')
    else:
        parts.append(f'<span class="frontier-decimal">{escape(bound.decimal)}</span>')
    return f'<span class="frontier-value">{"".join(parts)}</span>'


def _cell(
    content: str,
    column: str,
    *,
    value: str | None = None,
    exact: str | None = None,
    **data: str,
) -> str:
    """One cell: its column's class, its sort value, and its record's exact form."""
    attributes = [f'class="site-col-{column}"']
    if value is not None:
        attributes.append(f'data-value="{escape(value)}"')
    if exact is not None:
        attributes.append(f'data-exact="{escape(exact)}"')
    attributes.extend(f'data-{key.replace("_", "-")}="{escape(v)}"' for key, v in data.items())
    return f"<td {' '.join(attributes)}>{content}</td>"


def _names(people: Iterable[str], year: object) -> str:
    who = ", ".join(people)
    when = str(year) if year else ""
    return " ".join(part for part in (who, when) if part)


def _verified_mark() -> str:
    return (
        '<span class="frontier-verified" title="The verified bound agrees at the precision '
        'the report declares; the value is printed once, in the verified column.">'
        "\u2713 verified</span>"
    )


@dataclass(frozen=True)
class Row:
    """One case, as the table and its tests read it."""

    n: int
    status: str
    reported_status: str
    flags: tuple[str, ...]
    reported_upper: Shown
    verified_upper: Shown
    reported_lower: Shown
    verified_lower: Shown
    upper_agrees: bool
    lower_agrees: bool
    relation: str
    strict_by: tuple[str, ...]
    reported_relation: str
    reported_strict_by: tuple[str, ...]
    gap: Gap
    recent: bool


def frontier_row(
    case: Mapping[str, Any], *, claims: Sequence[Claim], recent: frozenset[int]
) -> Row:
    n = int(case["n"])
    try:
        bounds = {
            key: shown(case[key])
            for key in (
                "reported_upper_bound",
                "verified_upper_bound",
                "reported_lower_bound",
                "verified_lower_bound",
            )
        }
    except ExactFormError as error:
        raise SystemExit(f"n = {n}: {error}") from error
    verified_lower = bounds["verified_lower_bound"]
    reported_lower = bounds["reported_lower_bound"]
    mark, strict_by = relation(
        n, case["verified_lower_bound"], verified_lower.magnitude, claims
    )
    reported_mark, reported_strict_by = relation(
        n, case["reported_lower_bound"], reported_lower.magnitude, claims
    )
    difference = gap(bounds["verified_upper_bound"], verified_lower)
    flags = tuple(
        flag
        for flag, present in (("open", case["status"] == "open"), ("recent", n in recent))
        if present
    )
    return Row(
        n=n,
        status=str(case["status"]),
        reported_status=str(case["reported_status"]),
        flags=flags,
        reported_upper=bounds["reported_upper_bound"],
        verified_upper=bounds["verified_upper_bound"],
        reported_lower=reported_lower,
        verified_lower=verified_lower,
        upper_agrees=bounds_agree_at_declared_precision(
            case["reported_upper_bound"], case["verified_upper_bound"]
        ),
        lower_agrees=bounds_agree_at_declared_precision(
            case["reported_lower_bound"], case["verified_lower_bound"]
        ),
        relation=mark,
        strict_by=strict_by,
        reported_relation=reported_mark,
        reported_strict_by=reported_strict_by,
        gap=difference,
        recent=n in recent,
    )


def _best_known_html(case: Mapping[str, Any], row: Row, formulas: Formulas) -> str:
    upper = case["reported_upper_bound"]
    parts = [] if row.upper_agrees else [value_html(row.reported_upper, formulas)]
    credit = _names(upper.get("found_by") or (), upper.get("found_year"))
    method = UPPER_METHODS.get(str(upper["construction_method"]))
    rigid = upper.get("catalogue_rigid")
    notes = (credit, method or "", rigid if rigid in {"rigid", "semi-rigid"} else "")
    line = " · ".join(escape(part) for part in notes if part)
    if row.upper_agrees:
        line += f" {_verified_mark()}"
    if line.strip():
        parts.append(f'<span class="site-cell-note frontier-credit">{line.strip()}</span>')
    return " ".join(parts)


def _reported_lower_html(case: Mapping[str, Any], row: Row, formulas: Formulas) -> str:
    lower = case["reported_lower_bound"]
    parts = (
        []
        if row.lower_agrees
        else [value_html(row.reported_lower, formulas, relation_mark=row.reported_relation)]
    )
    credit = _names(lower.get("proved_by") or (), lower.get("proved_year"))
    kind = LOWER_KINDS.get(str(lower["kind"]), str(lower["kind"]))
    line = " · ".join(escape(part) for part in (credit, kind) if part)
    if row.lower_agrees:
        line += f" {_verified_mark()}"
    parts.append(f'<span class="site-cell-note frontier-credit">{line.strip()}</span>')
    return " ".join(parts)


def _details_html(case: Mapping[str, Any], row: Row, links: Links, formulas: Formulas) -> str:
    items = []
    for label, key in (
        ("Best known packing", "reported_upper_bound"),
        ("Verified upper", "verified_upper_bound"),
        ("Reported lower", "reported_lower_bound"),
        ("Verified lower", "verified_lower_bound"),
    ):
        cited = case[key].get("evidence") or ()
        if cited:
            joined = ", ".join(links.evidence_link(identifier) for identifier in cited)
            items.append(f"<li>{label}: {joined}</li>")
    polynomial = case["reported_upper_bound"].get("minimal_polynomial")
    if polynomial:
        degree = case["reported_upper_bound"].get("algebraic_degree")
        lead = (
            "The verified upper bound is a root of the minimal polynomial of the best "
            "known side"
            if row.verified_upper.root_of
            else "Minimal polynomial of the best known side"
        )
        of_degree = f", of degree {int(degree)}" if degree else ""
        formula = formulas.slot(str(polynomial))
        items.append(
            f'<li>{lead}{of_degree}: <span class="frontier-polynomial">{formula}</span></li>'
        )
    for strict_by, which in (
        (row.strict_by, "verified"),
        (row.reported_strict_by, "reported"),
    ):
        if strict_by:
            named = ", ".join(links.result_link(result) for result in strict_by)
            items.append(f"<li>The {which} lower bound is strict, as {named} claims.</li>")
    return (
        '<details class="frontier-details"><summary>Details</summary>'
        '<div class="site-details-body">'
        f'<ul class="frontier-records">{"".join(items)}</ul></div></details>'
    )


def _status_html(row: Row) -> str:
    status = (
        f'<span class="site-chip site-chip-status" data-status="{escape(row.status)}">'
        f"{escape(row.status)}</span>"
    )
    if row.reported_status != row.status:
        status += (
            f' <span class="site-cell-note frontier-reported-status">reported '
            f"{escape(row.reported_status)}</span>"
        )
    return status


def row_html(
    case: Mapping[str, Any], row: Row, links: Links, formulas: Formulas, *, base: str
) -> str:
    n = row.n
    thumbnail = (
        f'<img class="site-thumb frontier-thumb" loading="lazy" decoding="async" '
        f'src="{escape(base + overview_media.thumbnail_path(n))}" '
        f'alt="The best known packing of {n} unit squares" '
        f'width="{THUMBNAIL_SIZE}" height="{THUMBNAIL_SIZE}">'
    )
    case_file = f"packing/frontier/n-{n:03d}.md"
    recent = (
        '<span class="site-chip site-chip-star" title="A recent lower bound, starred as on '
        'the atlas figure."><span class="site-visually-hidden">recent</span></span>'
        if row.recent
        else ""
    )
    cells = [
        _cell(f'<span class="frontier-n">{n}</span> {thumbnail}', "n", value=str(n)),
        _cell(_status_html(row), "status"),
        _cell(
            _best_known_html(case, row, formulas),
            "best-known",
            value=row.reported_upper.value,
            exact=row.reported_upper.exact,
        ),
        _cell(
            value_html(row.verified_upper, formulas),
            "verified-upper",
            value=row.verified_upper.value,
            exact=row.verified_upper.exact,
        ),
        _cell(
            _reported_lower_html(case, row, formulas),
            "reported-lower",
            value=row.reported_lower.value,
            exact=row.reported_lower.exact,
            relation=row.reported_relation,
        ),
        _cell(
            value_html(row.verified_lower, formulas, relation_mark=row.relation),
            "verified-lower",
            value=row.verified_lower.value,
            exact=row.verified_lower.exact,
            relation=row.relation,
        ),
        _cell(
            f'<span class="frontier-decimal">{escape(row.gap.decimal)}</span>',
            "gap",
            value=row.gap.sort,
            gap_exact="true" if row.gap.exact else "false",
        ),
        _cell(recent, "recent", value="1" if row.recent else "0"),
        _cell(
            f'<a href="{escape(links.blob(case_file))}">n-{n:03d}.md</a> '
            + _details_html(case, row, links, formulas),
            "records",
        ),
    ]
    return (
        f'<tr id="n-{n:03d}" data-n="{n}" data-status="{escape(row.status)}" '
        f'data-flags="{escape(" ".join(row.flags))}">' + "".join(cells) + "</tr>"
    )


#: The columns: a class suffix, a header, and how `table.js` sorts it (None: it does not).
#: The `n` header is a formula, as the page's prose sets `n`.
HEADERS: tuple[tuple[str, str, str | None], ...] = (
    ("n", "$n$", "number"),
    ("status", "Status", "text"),
    ("best-known", "Best known packing", "number"),
    ("verified-upper", "Verified upper", "number"),
    ("reported-lower", "Reported lower", "number"),
    ("verified-lower", "Verified lower", "number"),
    ("gap", "Bound gap", "number"),
    ("recent", "Recent", "number"),
    ("records", "Records", None),
)


def _label(text: str, formulas: Formulas) -> str:
    return formulas.slot(text[1:-1]) if text.startswith("$") else escape(text)


def filters_html(first: int, last: int, formulas: Formulas) -> str:
    """The filter panel `table.js` shows and reads: status, open only, recent only, and a
    range of `n`. It is hidden until the script runs, since without it nothing filters."""
    n = formulas.slot("n")
    return (
        '<div class="site-table-filters" data-filters-for="frontier-table" hidden>'
        '<label>Status <select data-filter="status">'
        '<option value="">All</option><option value="open">Open</option>'
        '<option value="proved">Proved</option></select></label>'
        '<label><input type="checkbox" data-filter-flag="open"> Open only</label>'
        '<label><input type="checkbox" data-filter-flag="recent"> Recent only</label>'
        f'<label>{n} from <input type="number" data-filter-min="n" min="{first}" '
        f'max="{last}" step="1" inputmode="numeric" placeholder="{first}"></label>'
        f'<label>to <input type="number" data-filter-max="n" min="{first}" max="{last}" '
        f'step="1" inputmode="numeric" placeholder="{last}"></label>'
        '<output class="site-table-count" data-filter-count></output>'
        "</div>"
    )


def table_html(
    cases: Sequence[Mapping[str, Any]], rows: Sequence[Row], links: Links, *, base: str
) -> str:
    """The filters and the table, which scrolls in its own wrap under a sticky header."""
    formulas = Formulas()
    head = "".join(
        f'<th scope="col" class="site-col-{column}"'
        + (f' data-sort="{sort}">' if sort else ">")
        + f"{_label(label, formulas)}</th>"
        for column, label, sort in HEADERS
    )
    body = "\n".join(
        row_html(case, row, links, formulas, base=base)
        for case, row in zip(cases, rows, strict=True)
    )
    table = (
        f"{filters_html(rows[0].n, rows[-1].n, formulas)}\n"
        '<div class="kpress-table-wrap site-table-wrap site-table-scroll" '
        'data-kpress-table-scale="wide">'
        '<table class="kpress-table site-table frontier-table" data-site-table '
        'id="frontier-table" aria-label="The frontier atlas, one row per case">'
        f"<thead><tr>{head}</tr></thead>\n<tbody>\n{body}\n</tbody></table></div>"
    )
    return formulas.fill(table)


#: The raw block the article's `{{FRONTIER_TABLE}}` placeholder becomes before kpress
#: parses the article; the rendered table replaces it afterwards, so the table's markup
#: never passes through the Markdown parser.
TABLE_SLOT = '<div class="frontier-table-slot"></div>'


def frontier_facts(rows: Sequence[Row], links: Links) -> dict[str, str]:
    """Every fact the article's placeholders name, from the rows."""
    since = build_bound_citations.RECENT_SINCE
    return {
        "CASE_COUNT": str(len(rows)),
        "FIRST_N": str(rows[0].n),
        "LAST_N": str(rows[-1].n),
        "PROVED_COUNT": str(sum(row.status == "proved" for row in rows)),
        "OPEN_COUNT": str(sum(row.status == "open" for row in rows)),
        "RECENT_COUNT": str(sum(row.recent for row in rows)),
        "RECENT_SINCE": f"{since.day} {since:%B %Y}",
        "STRICT_COUNT": str(sum(bool(row.strict_by) for row in rows)),
        "FRONTIER_URL": links.tree("packing/frontier"),
        "EVIDENCE_URL": links.blob("packing/frontier/evidence.yaml"),
        "EPISTEMICS_URL": f"{REPO_URL}/blob/{DEFAULT_BRANCH}/epistemics.md",
        "FRONTIER_TABLE": TABLE_SLOT,
    }


def frontier_page(commit: str) -> Page:
    cases = frontier_cases()
    results = safe_load(RESULTS.read_text(encoding="utf-8"))["results"]
    claims = register_claims(results)
    recent = recent_lower_bounds()
    rows = [frontier_row(case, claims=claims, recent=recent) for case in cases]
    links = Links(
        commit=commit, evidence=entry_lines(EVIDENCE, "E-"), results=entry_lines(RESULTS, "T-")
    )
    path = "frontier.html"
    template = FRONTIER_TEMPLATE.read_text(encoding="utf-8")
    article = render_explainer.fill(
        template, frontier_facts(rows, links), where=FRONTIER_TEMPLATE.name
    )
    title = f"Frontier Atlas · {SITE_NAME}"
    document = parse_markdown_html(
        article, title=title, trust_mode="trusted", where=FRONTIER_TEMPLATE.name
    )
    if document.html.count(TABLE_SLOT) != 1:
        raise SystemExit(f"{FRONTIER_TEMPLATE.name} must place {{{{FRONTIER_TABLE}}}} once")
    # kpress has already refused a broken in-page anchor in the article, and the table
    # carries none; `link_problems` proves the whole page's links.
    html = document.html.replace(
        TABLE_SLOT, table_html(cases, rows, links, base=base_for(path))
    )
    return Page(
        key="frontier",
        path=path,
        title=title,
        description=FRONTIER_DESCRIPTION,
        html=html,
        scripts=(TABLE_SCRIPT,),
    )


# ---------------------------------------------------------------------------------------
# The tutorial page and its links.
# ---------------------------------------------------------------------------------------


class _Attributes(HTMLParser):
    """Each start tag's position and attributes, so one attribute can be replaced in place."""

    def __init__(self, html: str) -> None:
        super().__init__(convert_charrefs=True)
        self.starts = [0]
        self.starts.extend(index + 1 for index, char in enumerate(html) if char == "\n")
        self.tags: list[tuple[int, str, str, list[tuple[str, str | None]]]] = []
        self.feed(html)
        self.close()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._record(tag, attrs)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._record(tag, attrs)

    def _record(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        line, column = self.getpos()
        text = self.get_starttag_text() or ""
        self.tags.append((self.starts[line - 1] + column, text, tag, attrs))


LINK_ATTRIBUTES = frozenset({"href", "src", "poster"})


def rewrite_links(html: str, rewrite: Callable[[str, str, str], str]) -> str:
    """Replace each link attribute's value with `rewrite(tag, attribute, value)`.

    The HTML is parsed, and only the value of an `href`, `src` or `poster` attribute of a
    start tag the parser found is replaced, so text that merely looks like a link, in a
    code span or anywhere else, is never touched.
    """
    edits: list[tuple[int, int, str]] = []
    for start, text, tag, attrs in _Attributes(html).tags:
        replaced = text
        for name, value in attrs:
            if name not in LINK_ATTRIBUTES or value is None:
                continue
            new = rewrite(tag, name, value)
            if new != value:
                replaced = _replace_attribute(replaced, name, value, new)
        if replaced != text:
            if html[start : start + len(text)] != text:
                raise SystemExit(f"lost the position of {text[:60]!r} while rewriting links")
            edits.append((start, start + len(text), replaced))
    for start, end, replaced in reversed(edits):
        html = html[:start] + replaced + html[end:]
    return html


def _replace_attribute(tag_text: str, name: str, old: str, new: str) -> str:
    pattern = re.compile(rf"(\s{re.escape(name)}\s*=\s*)(\"[^\"]*\"|'[^']*'|[^\s\"'>]+)")
    for match in pattern.finditer(tag_text):
        if unescape(match.group(2).strip("\"'")) == old:
            replacement = f'{match.group(1)}"{escape(new, quote=True)}"'
            return tag_text[: match.start()] + replacement + tag_text[match.end() :]
    raise SystemExit(f"cannot find {name}={old!r} in {tag_text[:80]!r}")


def is_reader_document(path: str) -> bool:
    """A document a reader is sent to on the default branch, so they land on its current
    text: a Markdown document at the repository root, where the reader documents live, or
    a research report. Everything else a page links is a record, named at the build commit.
    """
    return path.endswith(".md") and (
        "/" not in path or posixpath.dirname(path) == "docs/project/research"
    )


@cache
def served_assets() -> Mapping[str, str]:
    """Repository files the site already serves beside its pages, by repository path."""
    return {
        path.relative_to(REPO).as_posix(): path.name
        for path in render_explainer.COMPOSITE_ASSETS
        if path.is_relative_to(REPO)
    }


def site_link(rest: str, *, page: str) -> str:
    """A link into the published site, as a link relative to `page`.

    The site root with a fragment is an old deep link into the explainer, which was the
    root until the overview took it, so it goes to `explainer.html` with its fragment, as
    the overview's forwarder sends it; the bare root is the overview.
    """
    parts = urlsplit(rest)
    base = base_for(page)
    fragment = f"#{parts.fragment}" if parts.fragment else ""
    target = parts.path or "index.html"
    if target == "index.html":
        return f"{base}explainer.html{fragment}" if fragment else base or "./"
    if target == page:
        return fragment or posixpath.basename(page)
    return base + rest


def repository_link(
    target: str, *, commit: str, source: str, page: str, image: bool = False
) -> str:
    """A link the Markdown document `source` makes, as the site page `page` carries it."""
    parts = urlsplit(target)
    if parts.scheme or target.startswith("//") or not parts.path:
        if target.startswith(SITE_URL):
            return site_link(target.removeprefix(SITE_URL), page=page)
        return target
    path = posixpath.normpath(posixpath.join(posixpath.dirname(source), unquote(parts.path)))
    if path == ".." or path.startswith(("../", "/")):
        raise SystemExit(f"{source} links outside the repository: {target}")
    fragment = f"#{parts.fragment}" if parts.fragment else ""
    if path == source:
        return fragment or posixpath.basename(page)
    return path_link(path, fragment, commit=commit, page=page, image=image)


def path_link(path: str, fragment: str, *, commit: str, page: str, image: bool) -> str:
    """A repository path as a page links it: the site's own copy where it serves one, a
    raw permalink for an image, a reader document on `main`, else a permalink at `commit`,
    `tree/` for a directory and `blob/` for a file."""
    if path in served_assets():
        return base_for(page) + served_assets()[path] + fragment
    if image:
        return f"{RAW_URL}/{commit}/{quote(path)}"
    if is_reader_document(path):
        return f"{REPO_URL}/blob/{DEFAULT_BRANCH}/{quote(path)}{fragment}"
    return f"{REPO_URL}/{_kind(path, commit)}/{commit}/{quote(path)}{fragment}"


def _kind(path: str, commit: str) -> str:
    """`tree` for a directory at the commit, else `blob`. The commit's own listing decides,
    not the checkout, which in the Pages jobs is sparse; only a commit git cannot list, such
    as a test's placeholder, falls back to the checkout."""
    paths = _listing(commit)
    if paths is None:
        return "tree" if (REPO / path).is_dir() else "blob"
    return "tree" if path in paths.directories else "blob"


def toc_html(entries: Sequence[TocEntry]) -> str:
    """kpress's table-of-contents rail over `entries`, in kpress's own markup.

    The same elements and classes `kpress.format.render` writes for a document it renders
    whole, so kpress's stylesheet lays the rail out: a sticky sidebar in the wide band, a
    drawer below it, opened by the toggle once kpress's `toc.js` runs.
    """
    items = "".join(
        f'<li class="kpress-toc-level-{entry.level} toc-h{entry.level}">'
        f'<a class="toc-link" href="{escape(entry.href)}">{escape(entry.title)}</a></li>'
        for entry in entries
    )
    return (
        '<button class="kpress-toc-toggle" type="button" data-kpress-toc-toggle '
        'aria-expanded="false" aria-label="Table of contents" title="Table of contents">'
        '<svg class="kpress-toc-toggle-icon" width="20" height="20" aria-hidden="true">'
        '<use href="#kpress-icon-list"></use></svg></button>'
        '<div class="kpress-toc-backdrop" data-kpress-toc-backdrop aria-hidden="true"></div>'
        '<nav class="kpress-toc kpress-no-print" aria-label="Table of contents" '
        'data-kpress-toc><a href="#" class="kpress-toc-title toc-link toc-title" '
        f'data-kpress-toc-top>Contents</a><ol class="toc-list">{items}</ol></nav>'
    )


def markdown_page_html(
    source: str, *, commit: str, source_path: str, page: str, title: str
) -> str:
    """A reader document as a site page: sanitized kpress HTML, its links rewritten, with
    kpress's table-of-contents rail beside it."""
    document = parse_markdown_html(
        source, title=title, trust_mode="sanitized", where=source_path
    )

    def rewrite(tag: str, attribute: str, value: str) -> str:
        return repository_link(
            value,
            commit=commit,
            source=source_path,
            page=page,
            image=tag == "img" and attribute == "src",
        )

    body = rewrite_links(document.html, rewrite)
    html = (
        '<div class="kpress-doc-layout kpress-content-with-toc">'
        f"{toc_html(document.toc)}"
        f'<div class="kpress-prose kpress-long-text">\n{body}\n</div></div>'
    )
    problems = anchor_problems(html, ids=("kpress-icon-list",))
    if problems:
        raise SystemExit(f"{page}: " + "; ".join(problems))
    return html


def tutorial_title(source: str) -> str:
    first = source.lstrip().splitlines()[0]
    if not first.startswith("# "):
        raise SystemExit("TUTORIAL.md must open with its title as a level-one heading")
    return first.removeprefix("# ").strip()


def tutorial_page(commit: str) -> Page:
    source = TUTORIAL.read_text(encoding="utf-8")
    title = tutorial_title(source)
    return Page(
        key="tutorial",
        path="tutorial.html",
        title=title,
        description=TUTORIAL_DESCRIPTION,
        html=markdown_page_html(
            source,
            commit=commit,
            source_path=TUTORIAL.relative_to(REPO).as_posix(),
            page="tutorial.html",
            title=title,
        ),
    )


# ---------------------------------------------------------------------------------------
# Offline link checks, for every page of the site.
# ---------------------------------------------------------------------------------------


@dataclass(frozen=True)
class RepositoryLink:
    """A link to a path in this repository on GitHub: a file, a directory or a raw file."""

    url: str
    kind: str
    ref: str
    path: str


_GITHUB = re.compile(
    rf"^{re.escape(REPO_URL)}/(?P<kind>blob|tree|raw)/(?P<ref>[^/?#]+)(?:/(?P<path>[^?#]*))?"
)
_RAW = re.compile(rf"^{re.escape(RAW_URL)}/(?P<ref>[^/?#]+)/(?P<path>[^?#]*)")


class _Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.values: list[str] = []
        self.ids: set[str] = set()
        self.fragments: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del tag
        for name, value in attrs:
            if value is None:
                continue
            if name in {"id", "name"}:
                self.ids.add(value)
            elif name in LINK_ATTRIBUTES:
                self.values.append(value)
                if value.startswith("#") and len(value) > 1 and not value.startswith("#:~:"):
                    self.fragments.append(value)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)


def _parse_links(html: str) -> _Links:
    parser = _Links()
    parser.feed(html)
    parser.close()
    return parser


def repository_links(html: str) -> list[RepositoryLink]:
    """Every link on the page to a path in this repository, in page order."""
    found = []
    for value in _parse_links(html).values:
        if match := _GITHUB.match(value):
            found.append(
                RepositoryLink(value, match["kind"], match["ref"], unquote(match["path"] or ""))
            )
        elif match := _RAW.match(value):
            found.append(RepositoryLink(value, "raw", match["ref"], unquote(match["path"])))
    return found


@dataclass(frozen=True)
class Listing:
    """The paths at one commit: files, and the directories and submodules holding them."""

    files: frozenset[str]
    directories: frozenset[str]


@cache
def _listing(commit: str) -> Listing | None:
    found = subprocess.run(
        ("git", "ls-tree", "-r", "-z", commit),
        cwd=REPO,
        capture_output=True,
        check=False,
    )
    if found.returncode != 0:
        return None
    files: set[str] = set()
    directories: set[str] = {""}
    for record in found.stdout.decode("utf-8").split("\0"):
        if not record:
            continue
        mode_type, path = record.split("\t", 1)
        if mode_type.split()[1] == "commit":
            directories.add(path)
        else:
            files.add(path)
        parent = posixpath.dirname(path)
        while parent and parent not in directories:
            directories.add(parent)
            parent = posixpath.dirname(parent)
    return Listing(frozenset(files), frozenset(directories))


def listing(commit: str) -> Listing:
    """The paths at `commit`, from one `git ls-tree -r`, which reads trees and never a blob,
    so it costs nothing in the Pages jobs' partial clone."""
    paths = _listing(commit)
    if paths is None:
        raise SystemExit(f"git cannot list commit {commit}; the links cannot be checked")
    return paths


def repository_link_problems(html: str, commit: str) -> list[str]:
    """Each repository link whose path does not exist at `commit`, or that names a ref other
    than the build commit or the default branch, one line each."""
    paths = listing(commit)
    problems = []
    for link in repository_links(html):
        if link.ref not in {commit, DEFAULT_BRANCH}:
            problems.append(f"{link.url} names {link.ref}, not the build commit or main")
        elif link.kind == "tree":
            if link.path.rstrip("/") not in paths.directories:
                problems.append(f"{link.url}: no directory {link.path!r} at {commit[:12]}")
        elif link.path not in paths.files:
            problems.append(f"{link.url}: no file {link.path!r} at {commit[:12]}")
    return list(dict.fromkeys(problems))


def anchor_problems(html: str, *, ids: Iterable[str] = ()) -> list[str]:
    """Each in-page link whose target is on no element: kpress's `broken_anchor`.

    `ids` are targets the page's shell supplies beside this HTML, such as kpress's icon
    sprite.
    """
    parser = _parse_links(html)
    present = parser.ids | set(ids)
    return list(
        dict.fromkeys(
            f"in-page link {fragment} has no target"
            for fragment in parser.fragments
            if unquote(fragment[1:]) not in present
        )
    )


def link_problems(html: str, commit: str) -> list[str]:
    """Everything wrong with a whole page's links, proved offline: repository paths
    against the build commit, and in-page anchors against the page's own ids."""
    return [*repository_link_problems(html, commit), *anchor_problems(html)]


def default_branch_links(html: str) -> tuple[str, ...]:
    """The repository links a page names on `main` rather than on the build commit, which
    the published-site check's ref rule accepts for exactly these URLs."""
    return tuple(
        sorted({link.url for link in repository_links(html) if link.ref == DEFAULT_BRANCH})
    )


def pages(commit: str | None = None) -> Iterable[Page]:
    """The frontier atlas and the tutorial, their records linked at `commit` (the checkout's
    `HEAD` unless given)."""
    commit = commit or render_explainer.link_revision()
    yield frontier_page(commit)
    yield tutorial_page(commit)
