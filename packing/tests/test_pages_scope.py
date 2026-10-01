"""Each page's pull-request checks run exactly when that page's declared inputs change.

`devtools.pages_scope` is what lets the Pages workflow skip a page on a pull request, and
a skip is the dangerous direction: an input the scope does not know about is a change
that ships a page nobody checked. So these tests do not compare the scope to a list
written here. They compare it to the builders' own declarations and to the commands the
workflow actually runs, and they prove it reads those declarations live rather than
holding a copy.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from pathlib import Path

import pytest

from devtools import (
    overview_data,
    pages_scope,
    render_explainer,
    render_n11_optimality_explainer,
    render_overview,
)
from devtools.pages_scope import (
    REPO,
    WORKFLOW,
    decide,
    declared_inputs,
    half_jobs,
    load_workflow,
    matches,
    pull_request_jobs,
)
from workbench_tools import build_site


@pytest.fixture(scope="module")
def declared() -> dict[str, tuple[Path, ...]]:
    return declared_inputs()


def probe(path: Path) -> str:
    """A repository-relative changed path standing for a declared file or directory."""
    relative = path.relative_to(REPO).as_posix()
    return f"{relative}/__changed__" if path.is_dir() else relative


def in_scope(changed: list[str], declared: dict[str, tuple[Path, ...]]) -> set[str]:
    return {decision.half for decision in decide(changed, declared) if decision.in_scope}


@pytest.mark.parametrize(
    ("half", "builder_inputs"),
    [
        ("explainer", lambda: render_explainer.RENDER_INPUTS),
        ("workbench", lambda: build_site.RENDER_INPUTS),
        ("overview", lambda: render_overview.RENDER_INPUTS),
        ("overview", lambda: overview_data.INPUTS),
        ("optimality", lambda: render_n11_optimality_explainer.RENDER_INPUTS),
    ],
)
def test_every_builder_input_puts_its_page_in_scope(
    declared: dict[str, tuple[Path, ...]],
    half: str,
    builder_inputs: Callable[[], tuple[Path, ...]],
) -> None:
    """Every path the builder declares selects its page, file or directory alike."""
    inputs = builder_inputs()
    assert inputs, f"the {half} builder declares no inputs"
    missed = [probe(path) for path in inputs if half not in in_scope([probe(path)], declared)]
    assert missed == [], f"{half} inputs a pull request could change without checking"


def test_the_scope_reads_each_builder_declaration_live(monkeypatch: pytest.MonkeyPatch) -> None:
    """A copy of `RENDER_INPUTS` would pass the test above and still drift from it.

    Adding an input to the renderer's declaration has to change the scope with no edit
    here, and the control shows the added path was out of scope before it was declared.
    """
    added = REPO / "packing" / "devtools" / "templates" / "a-new-render-input.css"
    before = declared_inputs()
    assert "explainer" not in in_scope([probe(added)], before)
    monkeypatch.setattr(
        render_explainer, "RENDER_INPUTS", (*render_explainer.RENDER_INPUTS, added)
    )
    assert "explainer" in in_scope([probe(added)], declared_inputs())
    monkeypatch.setattr(build_site, "RENDER_INPUTS", (*build_site.RENDER_INPUTS, added))
    assert in_scope([probe(added)], declared_inputs()) == {"explainer", "workbench"}
    monkeypatch.setattr(overview_data, "INPUTS", (*overview_data.INPUTS, added))
    assert in_scope([probe(added)], declared_inputs()) == {
        "explainer",
        "workbench",
        "overview",
    }


def test_every_tool_a_pull_request_runs_for_a_page_is_that_pages_input(
    declared: dict[str, tuple[Path, ...]],
) -> None:
    """A checker is an input of the verdict: editing it has to run it.

    Read from the workflow text independently of the tool's own parser, so a regex the
    tool gets wrong cannot agree with itself here.
    """
    workflow = load_workflow()
    runnable = pull_request_jobs(workflow)
    members = half_jobs(workflow)
    for half, jobs in members.items():
        text = "\n".join(
            str(step.get("run", ""))
            for name in sorted(jobs & runnable)
            for step in workflow["jobs"][name].get("steps", [])
        )
        modules = set(re.findall(r"python -m (devtools\.\w+|workbench_tools\.\w+)", text))
        tests = set(re.findall(r"pytest -q (tests/\S+\.py)", text))
        assert modules, f"no {half} job runs a tool"
        expected = (
            {
                REPO / "packing" / f"{module.replace('.', '/')}.py"
                for module in modules
                if module.startswith("devtools.")
            }
            | {
                REPO / "packages/workbench/tools" / f"{module.replace('.', '/')}.py"
                for module in modules
                if module.startswith("workbench_tools.")
            }
            | {REPO / "packing" / test for test in tests}
        )
        missing = sorted(
            path.relative_to(REPO).as_posix() for path in expected if path not in declared[half]
        )
        assert missing == [], f"{half}: tools its jobs run that do not select it"


def test_the_workflow_and_the_scope_itself_select_every_page(
    declared: dict[str, tuple[Path, ...]],
) -> None:
    for path in (WORKFLOW, Path(pages_scope.__file__)):
        assert in_scope([probe(path)], declared) == set(pages_scope.BUILDER_INPUTS), path


def test_a_helper_a_checker_imports_is_an_input(declared: dict[str, tuple[Path, ...]]) -> None:
    """A tool's first-party imports change its verdict as much as the tool does.

    `check_scroll_restoration` reads the page path from `render_explainer_pdf`, so the
    closure the scope computes over the files a job runs has to reach that module.
    """
    closure = pages_scope.import_closure(
        {REPO / "packing/devtools/check_scroll_restoration.py"}
    )
    assert REPO / "packing/devtools/render_explainer_pdf.py" in closure
    assert REPO / "packing/devtools/render_explainer_pdf.py" in declared["explainer"]


def test_every_pdf_browser_control_probe_selects_the_explainer(
    declared: dict[str, tuple[Path, ...]],
) -> None:
    """The PDF test executes sibling probes that are not visible to import closure."""
    controls = REPO / "packing/tests/probes/pdf_math_browser"
    probes = sorted(path for path in controls.rglob("*") if path.is_file())
    assert probes
    assert controls in declared["explainer"]
    missed = [
        probe(path) for path in probes if "explainer" not in in_scope([probe(path)], declared)
    ]
    assert missed == []


def test_pull_request_178_would_have_run_no_browser_work(
    declared: dict[str, tuple[Path, ...]],
) -> None:
    """The case that motivated the scope: workbench probes and their checkers.

    Ten files under `packages/workbench` and one devtools register; the explainer's
    Chromium checks ran on all of it. None is a page input: the probes and the
    `check_*` tools belong to Packing validation's frontend lane, not to either build.
    """
    changed = [
        "packages/workbench/probes/accessibility/active-pack-index.js",
        "packages/workbench/probes/api/refusal.js",
        "packages/workbench/probes/dom/transforms.js",
        "packages/workbench/probes/layout/scroll-width.js",
        "packages/workbench/probes/pack/scene-matches-snapshot.js",
        "packages/workbench/tests/fixtures/self-contained/allowed/blob-object-url.html",
        "packages/workbench/tests/test_self_contained.py",
        "packages/workbench/tools/workbench_tools/check_accessibility.py",
        "packages/workbench/tools/workbench_tools/check_candidate.py",
        "packages/workbench/tools/workbench_tools/check_pack_panel.py",
        "packing/devtools/embedded-javascript.yaml",
    ]
    assert in_scope(changed, declared) == set()
    assert in_scope([*changed, "packages/workbench/src/application.js"], declared) == {
        "workbench"
    }
    assert in_scope([*changed, "packing/devtools/check_math_faces.py"], declared) == {
        "explainer"
    }


def test_a_change_to_the_record_or_the_reader_documents_builds_only_the_overview(
    declared: dict[str, tuple[Path, ...]],
) -> None:
    """The site's own pages read what neither other build does, and share what they do.

    A register evidence entry, a case record, the bibliography, `epistemics.md` and the
    tutorial are the overview's alone, so a pull request changing only those
    runs its job and no explainer Chromium. The register itself is read by the explainer
    too, and so is n = 11's case record, whose exact T-060 endpoint Figure 3 checks
    (`render_explainer.n11_solved`); the renderer module by all three, since it also
    writes the navigation bar the Visualizer's build takes (`nav_shell`); and kpress by
    all three.
    """
    for changed in (
        "TUTORIAL.md",
        "epistemics.md",
        "packing/frontier/evidence.yaml",
        "packing/frontier/n-012.md",
        "packing/resources/bibliography.yaml",
        "packing/devtools/overview/forward.js",
        "packing/devtools/templates/overview-article.md",
    ):
        assert in_scope([changed], declared) == {"overview"}, changed
    for shared in ("packing/frontier/results.yaml", "packing/frontier/n-011.md"):
        assert in_scope([shared], declared) == {"explainer", "overview"}, shared
    assert in_scope(["packing/devtools/render_overview.py"], declared) == set(
        pages_scope.BUILDER_INPUTS
    )
    assert in_scope(["vendor/kpress"], declared) == set(pages_scope.BUILDER_INPUTS)
    assert in_scope(["AGENTS.md", "packing/resources/n11/source.md"], declared) == set()


def test_t060_article_selects_only_its_page(declared: dict[str, tuple[Path, ...]]) -> None:
    assert in_scope(["packing/devtools/templates/n11-optimality-article.md"], declared) == {
        "optimality"
    }
    assert in_scope(
        ["packing/resources/web/n11-optimality-2026-09-29/receipts/final-composition.json"],
        declared,
    ) == {"optimality"}


def test_t060_page_has_an_independent_required_build() -> None:
    jobs = load_workflow()["jobs"]
    assert "needs.scope.outputs.optimality == 'true'" in jobs["optimality"]["if"]
    assert jobs["optimality"]["timeout-minutes"] == 10
    browser_control = next(
        step
        for step in jobs["optimality"]["steps"]
        if step.get("name") == "Check T-060 figures and article renderer"
    )
    assert browser_control["env"]["SQPACK_N11_PAPER_BROWSER"] == "1"
    commands = "\n".join(str(step.get("run", "")) for step in jobs["optimality"]["steps"])
    assert "render_n11_optimality_explainer --output-dir site/n11-optimality --pdf" in commands
    assert (
        "render_n11_optimality_explainer --output-dir site/n11-optimality --check" in commands
    )
    assert "test -s site/n11-optimality/t-060-explainer.pdf" in commands
    assert "optimality" in jobs["publish"]["needs"]
    assert "optimality" in jobs["pages-required"]["needs"]
    assert "optimality-unchanged" in jobs["pages-required"]["needs"]
    required = next(
        step["run"]
        for step in jobs["pages-required"]["steps"]
        if step.get("name") == "Require every page this run builds to pass"
    )
    assert (
        '(.scope.outputs.optimality != "true" or .optimality.result == "success")' in required
    )


def test_a_matching_input_is_a_path_not_a_string_prefix() -> None:
    sqpack = REPO / "packing/src/sqpack"
    assert matches("packing/src/sqpack", sqpack)
    assert matches("packing/src/sqpack/render/palette.py", sqpack)
    assert not matches("packing/src/sqpack_extra/module.py", sqpack)
    assert not matches("packing/src/sqpac", sqpack)


def test_membership_follows_needs_and_leaves_out_what_a_pull_request_never_runs() -> None:
    workflow = {
        "jobs": {
            "scope": {},
            "prepare": {"needs": "scope", "if": "needs.scope.outputs.explainer == 'true'"},
            "check": {"needs": ["prepare"]},
            "note": {"needs": "scope", "if": "needs.scope.outputs.explainer != 'true'"},
            "build": {"needs": "scope", "if": "needs.scope.outputs.workbench == 'true'"},
            "publish": {"needs": ["check", "build"]},
            "deploy": {
                "needs": "publish",
                "if": "github.ref == 'refs/heads/main' && github.event_name != 'pull_request'",
            },
            "verify": {"needs": "deploy"},
            "timing": {"needs": "prepare", "if": "github.event_name == 'workflow_dispatch'"},
            "required": {"needs": ["publish", "timing"], "if": "always()"},
        }
    }
    members = half_jobs(workflow)
    assert members["explainer"] == {
        "prepare",
        "check",
        "publish",
        "deploy",
        "verify",
        "timing",
        "required",
    }
    assert members["workbench"] == {"build", "publish", "deploy", "verify", "required"}
    assert pull_request_jobs(workflow) == {
        "scope",
        "prepare",
        "check",
        "note",
        "build",
        "publish",
        "required",
    }


def test_a_gate_on_an_undeclared_page_is_refused() -> None:
    workflow = {"jobs": {"x": {"if": "needs.scope.outputs.atlas == 'true'"}}}
    with pytest.raises(SystemExit, match="unknown half 'atlas'"):
        half_jobs(workflow)


def test_every_page_says_why_it_was_skipped(declared: dict[str, tuple[Path, ...]]) -> None:
    decisions = decide(["AGENTS.md", "packing/campaign/ledger.md"], declared)
    assert [d.half for d in decisions] == list(pages_scope.BUILDER_INPUTS)
    for decision in decisions:
        assert not decision.in_scope
        assert decision.reason.startswith("none of the 2 changed files is among the ")
    (single,) = decide(["README.md"], declared)[:1]
    assert single.reason.startswith("none of the 1 changed file is among the ")


def test_the_workflow_outputs_and_summary_are_written(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    outputs = tmp_path / "output"
    summary = tmp_path / "summary"
    monkeypatch.setenv("GITHUB_OUTPUT", str(outputs))
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))
    assert pages_scope.main(["--all", "a test"]) == 0
    lines = outputs.read_text(encoding="utf-8").splitlines()
    assert lines == [
        "explainer=true",
        "explainer_reason=every page is built on a test",
        "workbench=true",
        "workbench_reason=every page is built on a test",
        "overview=true",
        "overview_reason=every page is built on a test",
        "optimality=true",
        "optimality_reason=every page is built on a test",
    ]
    assert "| explainer | builds and checks |" in summary.read_text(encoding="utf-8")
    assert "| overview | builds and checks |" in summary.read_text(encoding="utf-8")
    assert "explainer: in scope" in capsys.readouterr().out


def test_an_identical_pair_of_revisions_changes_nothing() -> None:
    assert pages_scope.changed_paths("HEAD", "HEAD") == []
    with pytest.raises(SystemExit, match="git diff"):
        pages_scope.changed_paths("HEAD", "no-such-revision-anywhere")
