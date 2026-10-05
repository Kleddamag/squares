#!/usr/bin/env python3
"""Capture the Kingbird catalogue into a dated scratch directory for an intake pass.

The retained capture under `resources/web/` is the record's, and refreshing it is a dated
W1 research survey (`frontier/README.md`, Source Coverage and Freshness). This command is
the network half of that survey and nothing more. It fetches the page, transcribes it the
way the retained transcription was made, and writes both into a capture directory outside
the record, `attic/intake/kingbird-YYYY-MM-DD/` by default, which Git ignores. There
`devtools.intake_sweep` finds the newest capture and compares it count by count with the
retained one through `devtools.diff_kingbird_catalogue`. It never writes the retained
capture, and no validation tier runs it.

Usage, from `packing/`::

    uv run --frozen --all-extras --group dev python -m devtools.capture_kingbird_catalogue
    uv run --frozen --all-extras --group dev python -m devtools.capture_kingbird_catalogue \\
        --html page.html --retrieved 2026-10-05T06:00:00Z

`--html` transcribes a page fetched some other way, with no network beyond the pinned
transcriber; `--out` names the directory.

The transcriber is `html2text` 2025.4.15 with `--body-width=0`, through a pinned `uvx`
runner. The 2026-09-30 capture was made that way and reproduced the 2026-08-22
transcription byte for byte from its own HTML. On 2026-10-05 this command, given each
retained HTML file, reproduced the body of each retained transcription byte for byte, so a
capture it writes compares with the record's on content alone. The header it writes is
the archive header the retained transcription carries, so taking a capture into the
record is a copy and a one-line edit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import urllib.request
from collections.abc import Callable, Sequence
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from devtools.audit_kingbird_catalogue import USER_AGENT
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
COVERAGE = ROOT / "frontier" / "source-coverage.yaml"
#: Where captures go unless `--out` says otherwise: Git-ignored scratch, one per day.
CAPTURES = REPO / "attic" / "intake"
CAPTURE_PREFIX = "kingbird-"
#: The archive's name for the page, which both files in a capture take.
STEM = "kingbird-squares-in-squares"
#: The transcriber the retained captures were made with, pinned.
TRANSCRIBER = ("uvx", "--from", "html2text==2025.4.15", "html2text", "--body-width=0")
FETCH_TIMEOUT_SECONDS = 60

Transcribe = Callable[[Path], str]


@dataclass(frozen=True)
class Capture:
    """What one capture holds, as `capture.json` records it."""

    url: str
    retrieved_utc: str
    last_modified: str | None
    html_bytes: int
    html_sha256: str
    method: str


def catalogue_url(coverage: Path = COVERAGE) -> str:
    """The catalogue's address, as the source register gives it."""
    document = safe_load(coverage.read_text(encoding="utf-8"))
    return next(s["url"] for s in document["sources"] if s["id"] == "kingbird-current")


def fetch(url: str) -> tuple[bytes, str | None]:
    """The page's bytes and the server's `Last-Modified`, if it sends one."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=FETCH_TIMEOUT_SECONDS) as response:
        return response.read(), response.headers.get("Last-Modified")


def transcribe(html: Path) -> str:
    """The pinned `html2text` transcription of one saved page."""
    shown = subprocess.run(
        (*TRANSCRIBER, str(html)), check=True, capture_output=True, text=True
    )
    return shown.stdout


def header(capture: Capture) -> str:
    """The archive header the retained transcription opens with."""
    retrieved = datetime.fromisoformat(capture.retrieved_utc)
    served = (
        f"; the server reported `Last-Modified: {capture.last_modified}`"
        if capture.last_modified
        else "; the server sent no `Last-Modified`"
    )
    return (
        f"# Archived: {STEM}\n\n"
        f"**Source:** {capture.url}\n"
        f"**Archived:** {retrieved:%Y-%m-%d}, retrieved {retrieved:%H:%M:%S} UTC{served}.\n"
        f"**Method:** {capture.method}; the original HTML is preserved alongside as "
        f"`{STEM}.html`, SHA-256 `{capture.html_sha256}`.\n\n---\n\n"
    )


def write_capture(
    html: bytes,
    *,
    url: str,
    retrieved_utc: str,
    last_modified: str | None,
    out: Path,
    transcriber: Transcribe = transcribe,
) -> Capture:
    """Write the page, its transcription and `capture.json` into `out`."""
    out.mkdir(parents=True, exist_ok=True)
    page = out / f"{STEM}.html"
    page.write_bytes(html)
    capture = Capture(
        url=url,
        retrieved_utc=retrieved_utc,
        last_modified=last_modified,
        html_bytes=len(html),
        html_sha256=hashlib.sha256(html).hexdigest(),
        method="`devtools.capture_kingbird_catalogue`, `html2text==2025.4.15 --body-width=0`",
    )
    (out / f"{STEM}.md").write_text(header(capture) + transcriber(page), encoding="utf-8")
    (out / "capture.json").write_text(
        json.dumps(asdict(capture), indent=2) + "\n", encoding="utf-8"
    )
    return capture


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    command.add_argument("--html", type=Path, help="transcribe this saved page; no fetch")
    command.add_argument(
        "--retrieved",
        help="when the saved page was fetched, as an ISO UTC time (with --html)",
    )
    command.add_argument("--last-modified", help="the server's Last-Modified (with --html)")
    command.add_argument("--out", type=Path, help="the capture directory")
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    url = catalogue_url()
    if args.html is None:
        try:
            html, last_modified = fetch(url)
        except OSError as error:
            print(f"capture failed: {url}: {error}", file=sys.stderr)
            return 1
        retrieved = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        html, last_modified = args.html.read_bytes(), args.last_modified
        retrieved = args.retrieved or datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    out = args.out or CAPTURES / f"{CAPTURE_PREFIX}{retrieved[:10]}"
    capture = write_capture(
        html, url=url, retrieved_utc=retrieved, last_modified=last_modified, out=out
    )
    print(f"captured {capture.html_bytes} bytes of {url} into {out}")
    print("compare it with the record: python -m devtools.intake_sweep --offline")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
