"""Build one full workbench page and run the browser behavior contracts against it."""

from __future__ import annotations

import argparse
import json
import tempfile
import time
from collections.abc import Callable, Sequence
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from strif import atomic_output_file

from workbench_tools.build_site import build, source_dirty, source_revision
from workbench_tools.check_accessibility import check as check_accessibility
from workbench_tools.check_animate_view import check as check_animate_view
from workbench_tools.check_animation_editor import check as check_animation_editor
from workbench_tools.check_pack_panel import check as check_pack_panel
from workbench_tools.check_page_policy import check as check_page_policy
from workbench_tools.check_search_panel import check as check_search_panel
from workbench_tools.check_stage_resize import check as check_stage_resize
from workbench_tools.check_transitions import check as check_transitions


def run_checks(
    page: Path, checks: Sequence[tuple[str, Callable[[Path], str]]], *, workers: int
) -> tuple[list[str], dict[str, float]]:
    """Run isolated browser owners concurrently, preserving declared result order."""
    if workers not in (1, 2):
        raise ValueError("browser checks support only one or two workers")

    def run(item: tuple[str, Callable[[Path], str]]) -> tuple[str, float]:
        started = time.monotonic()
        result = item[1](page)
        return result, time.monotonic() - started

    # Each check creates and closes its own Playwright driver/browser. Only the
    # already-built, read-only page is shared; output fixtures use private temp roots.
    with ThreadPoolExecutor(max_workers=workers) as pool:
        measured = list(pool.map(run, checks))
    return (
        [result for result, _ in measured],
        {name: elapsed for (name, _), (_, elapsed) in zip(checks, measured, strict=True)},
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Share the deterministic build across a bounded number of Chromium checks.

    The layout contract (`check_layout`) runs inside `check_stage_resize`'s browser session.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, choices=(1, 2), default=1)
    parser.add_argument("--timings", type=Path, help="write a new per-check timing receipt")
    args = parser.parse_args(argv)
    if args.timings is not None and args.timings.exists():
        parser.error("--timings refuses to overwrite an existing receipt")
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="squares-workbench-frontend-") as scratch:
        page = Path(scratch) / "workbench" / "index.html"
        build(page.parent)
        build_seconds = time.monotonic() - started
        results, timings = run_checks(
            page,
            (
                ("accessibility", check_accessibility),
                ("editor", check_animation_editor),
                ("pack", check_pack_panel),
                ("search", check_search_panel),
                ("animate", check_animate_view),
                ("policy", check_page_policy),
                ("resize", check_stage_resize),
                ("transitions", check_transitions),
            ),
            workers=args.workers,
        )
    if args.timings is not None:
        with atomic_output_file(args.timings, make_parents=True) as temporary:
            temporary.write_text(
                json.dumps(
                    {
                        "status": "passed",
                        "source_commit": source_revision(),
                        "source_dirty": source_dirty(),
                        "workers": args.workers,
                        "build_seconds": build_seconds,
                        "wall_seconds": time.monotonic() - started,
                        "checks": timings,
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
    print("OK: " + "; ".join(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
