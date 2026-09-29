"""The overview page: every register entry shown, every count read from the record."""

from __future__ import annotations

import re
from collections import Counter

import pytest

from devtools import overview_data, render_overview
from devtools.render_explainer import MARKDOWN as EXPLAINER_ARTICLE
from devtools.render_explainer import TEMPLATE as EXPLAINER_SHELL
from sqpack.yamlio import safe_load

ID = re.compile(r'\sid="([^"]+)"')
ROW = re.compile(r'<tr id="(t-\d{3})" data-source="(ours|others)" data-c="(C\d)">')


@pytest.fixture(scope="module")
def page() -> str:
    return render_overview.overview_page().html


@pytest.fixture(scope="module")
def register() -> list[dict]:
    return safe_load(overview_data.RESULTS.read_text(encoding="utf-8"))["results"]


def test_every_register_entry_is_one_row(page: str, register: list[dict]) -> None:
    rows = ROW.findall(page)
    assert sorted(row_id for row_id, _, _ in rows) == sorted(r["id"].lower() for r in register)
    declared = {r["id"].lower(): r for r in register}
    for row_id, source, confirmation in rows:
        record = declared[row_id]
        assert source == ("others" if record.get("attribution") else "ours"), row_id
        assert confirmation == record["confirmation"], row_id


def test_counts_are_the_declared_rungs(register: list[dict]) -> None:
    stats = overview_data.stats(overview_data.load())
    ours = [r for r in register if not r.get("attribution")]
    others = [r for r in register if r.get("attribution")]
    assert (stats.total, stats.ours, stats.others) == (len(register), len(ours), len(others))
    assert stats.verification == Counter(r["verification"] for r in register)
    assert stats.confirmation_ours == Counter(r["confirmation"] for r in ours)
    assert stats.confirmation_others == Counter(r["confirmation"] for r in others)
    assert stats.cases_1_100_proved + stats.cases_1_100_open == 100


def test_the_render_is_deterministic(page: str) -> None:
    assert render_overview.overview_page().html == page


def test_the_page_fetches_nothing(page: str) -> None:
    render_overview.assert_self_contained("index.html", page)


def test_no_placeholder_or_raw_math_is_left(page: str) -> None:
    article = re.sub(r"<script.*?</script>", "", page, flags=re.DOTALL).split("<article", 1)[1]
    assert not re.search(r"\{\{[A-Z0-9_]+\}\}", page)
    assert not re.search(r"\bs\(\d+\) *[<>]=", article)
    assert not re.search(r"(?<![\w\\])\$[^$\s][^$<]*\$", article)


def test_every_record_link_is_a_permalink_or_a_site_page() -> None:
    for result in overview_data.load().results:
        for link in result.records:
            assert (
                link.url.startswith(render_overview.REPO_URL + "/blob/")
                or link.url == "frontier.html"
            ), (result.id, link)
            assert "/blob/main/" not in link.url, (result.id, link)


def test_record_line_links_point_at_their_entry() -> None:
    lines = overview_data.RESULTS.read_text(encoding="utf-8").splitlines()
    for result in overview_data.load().results:
        (register,) = (link for link in result.records if link.label == "register")
        line = int(register.url.rsplit("#L", 1)[1])
        assert lines[line - 1].strip() == f"- id: {result.id}", result.id


def _slug(heading: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")


def test_overview_ids_never_shadow_an_explainer_anchor(page: str) -> None:
    """`forward.js` sends a fragment the overview lacks to the explainer, so an old
    explainer deep link lands on the overview only if the overview has the same id."""
    explainer = EXPLAINER_ARTICLE.read_text(encoding="utf-8")
    explainer_ids = set(ID.findall(explainer + EXPLAINER_SHELL.read_text(encoding="utf-8")))
    explainer_ids |= {
        _slug(h) for h in re.findall(r"^#{1,4} (.+)$", explainer, flags=re.MULTILINE)
    }
    ours = {i for i in ID.findall(page) if not i.startswith("kpress-")}
    assert not ours & explainer_ids


def test_the_nav_links_only_to_served_pages() -> None:
    nav = render_overview.nav_html("overview")
    served = {"./", *render_overview.SITE_PAGES, "workbench/"}
    for href in re.findall(r'href="([^"]+)"', nav):
        assert href.startswith("https://") or href in served, href
    assert nav.count('aria-current="page"') == 1


@pytest.mark.parametrize(
    ("prose", "tex"),
    [
        ("s(11) >= 2 + 4/sqrt(5) by a repair", [r"s(11) \ge 2 + 4/\sqrt{5}"]),
        ("s(17), s(18), s(19) >= 459/100 by", [r"s(17), s(18), s(19) \ge 459/100"]),
        ("a bound on s(N) for every 4 <= N <= 100", ["s(N)", r"4 \le N \le 100"]),
        ("s(46) = 7 from the 7 x 7 grid", ["s(46) = 7", r"7 \times 7"]),
        ("need side >= 3.8770835..., equal", [r"\ge 3.8770835\ldots"]),
        ("s(11) > 31/8 by a certificate", ["s(11) > 31/8"]),
    ],
)
def test_register_prose_math_is_found_and_set_in_tex(prose: str, tex: list[str]) -> None:
    runs = [match.group(0) for match in overview_data.MATH.finditer(prose)]
    assert [overview_data.prose_tex(run) for run in runs] == tex
    assert overview_data.tex_bounds(prose).count("data-kpress-math") >= len(tex)
