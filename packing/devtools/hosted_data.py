"""Data kept outside Git: a manifest of where each file is hosted, and a verified fetch.

Some retained data is too large to belong in the repository's history, such as the n17
sub-pattern certificate dumps, about 112 MB of gzip; OR-18 keeps such bulk data out of
Git. Its small records stay in Git: the
producer receipts, the verification receipts and the verdicts that cite them. The bytes
are hosted elsewhere, for instance as release assets, and a repository-relative manifest
lists every hosted file:

- `name`: the hosted file's name, which is the last part of its URL;
- `path`: the repository-relative path where it is placed when fetched, which is where
  the tools that read it look;
- `size` in bytes, and `sha256`, the SHA-256 of the hosted bytes;
- `url`: where to download it.

A download crosses a real trust boundary (OR-16), so `fetch` checks the size and the
SHA-256 of every file it downloads against the manifest before it moves the file into
place, and leaves nothing behind when either check fails. A file already in place is
not hashed again. `state` only compares its size with the manifest's, which catches a
truncated or wrong file, and is how a reader learns whether a full re-check can run.

The manifest is YAML:

    schema: hosted-data-manifest/v1
    files:
      - name: <name>
        path: <repository-relative path>
        size: <bytes>
        sha256: <hex>
        url: <https URL ending in name>

Usage, from `packing/`:

    uv run --frozen --all-extras --group dev python -m devtools.hosted_data write \
        MANIFEST --url-prefix URL FILE...
    uv run --frozen --all-extras --group dev python -m devtools.hosted_data fetch MANIFEST

`write` lists local files with their sizes and digests, each to be hosted at
`URL-prefix + name`; `fetch` downloads every listed file that is not in place.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import tempfile
import urllib.request
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import IO, Any

from sqpack.yamlio import load_yaml

SCHEMA = "hosted-data-manifest/v1"
REPO = Path(__file__).resolve().parents[2]
FIELDS = ("name", "path", "size", "sha256", "url")
HEX64 = re.compile(r"[0-9a-f]{64}")
DESCRIPTION = "Data kept outside Git: write a manifest, or fetch what it lists."
CHUNK = 1 << 20
TIMEOUT_SECONDS = 120

#: Something that opens a URL for reading, as `urllib.request.urlopen` does.
Opener = Callable[[str], IO[bytes]]


class HostedDataError(ValueError):
    """A manifest, a placed file or a download disagrees with what the manifest says."""


@dataclass(frozen=True)
class HostedFile:
    """One hosted file, as the manifest lists it."""

    name: str
    path: str
    size: int
    sha256: str
    url: str

    def as_record(self) -> dict[str, Any]:
        return {field: getattr(self, field) for field in FIELDS}


def load_manifest(root: Path, declared: str) -> dict[str, HostedFile]:
    """The manifest's files keyed by their repository-relative paths, refusing a malformed
    one."""
    if not declared or Path(declared).is_absolute():
        raise HostedDataError(f"{declared!r} is not a repository-relative manifest path")
    path = root / declared
    if not path.is_file():
        raise HostedDataError(f"{declared} does not exist")
    document = load_yaml(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or document.get("schema") != SCHEMA:
        raise HostedDataError(f"{declared}: not a {SCHEMA} manifest")
    raw = document.get("files")
    if not isinstance(raw, list):
        raise HostedDataError(f"{declared}: files must be a list")
    files: dict[str, HostedFile] = {}
    names: set[str] = set()
    for index, item in enumerate(raw):
        where = f"{declared}: file {index}"
        if not isinstance(item, dict) or set(item) != set(FIELDS):
            raise HostedDataError(f"{where}: fields must be {', '.join(FIELDS)}")
        record = HostedFile(
            name=str(item["name"]),
            path=str(item["path"]),
            size=item["size"],
            sha256=str(item["sha256"]),
            url=str(item["url"]),
        )
        size = record.size
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            raise HostedDataError(f"{where}: size must be a byte count")
        if not HEX64.fullmatch(record.sha256):
            raise HostedDataError(f"{where}: sha256 must be 64 lowercase hex digits")
        if Path(record.path).is_absolute() or ".." in Path(record.path).parts:
            raise HostedDataError(f"{where}: {record.path!r} is not repository-relative")
        if Path(record.path).name != record.name or not record.url.endswith(f"/{record.name}"):
            raise HostedDataError(f"{where}: the path and the URL must end in {record.name}")
        if record.path in files or record.name in names:
            raise HostedDataError(f"{where}: {record.name} is listed twice")
        files[record.path] = record
        names.add(record.name)
    return files


def state(root: Path, record: HostedFile) -> str:
    """`present` when the file is in place with the manifest's size, `absent` when it is
    not there; a file of another size is refused."""
    path = root / record.path
    if not path.is_file():
        return "absent"
    size = path.stat().st_size
    if size != record.size:
        raise HostedDataError(
            f"{record.path} holds {size:,} bytes, not the manifest's {record.size:,}; "
            "remove it and fetch it again"
        )
    return "present"


def _open(url: str) -> IO[bytes]:
    if not url.startswith(("https://", "file://")):
        raise HostedDataError(f"{url}: only https and file URLs are fetched")
    return urllib.request.urlopen(url, timeout=TIMEOUT_SECONDS)


def _copy(record: HostedFile, opener: Opener, temporary: Path) -> None:
    """Stream the file's URL into `temporary`, refusing a byte beyond the listed size, a
    short file, or a SHA-256 other than the manifest's."""
    hasher, size = hashlib.sha256(), 0
    with temporary.open("wb") as sink, opener(record.url) as source:
        while chunk := source.read(CHUNK):
            size += len(chunk)
            if size > record.size:
                raise HostedDataError(f"{record.url}: more than {record.size:,} bytes")
            hasher.update(chunk)
            _ = sink.write(chunk)
    if size != record.size:
        raise HostedDataError(f"{record.url}: {size:,} bytes, not {record.size:,}")
    if hasher.hexdigest() != record.sha256:
        raise HostedDataError(f"{record.url}: the SHA-256 is not the manifest's")


def download(root: Path, record: HostedFile, opener: Opener = _open) -> None:
    """Download one file beside its place, check its size and SHA-256, then move it in."""
    target = root / record.path
    target.parent.mkdir(parents=True, exist_ok=True)
    handle, name = tempfile.mkstemp(prefix=f".{record.name}.", dir=target.parent)
    os.close(handle)
    temporary = Path(name)
    try:
        _copy(record, opener, temporary)
        _ = temporary.replace(target)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def fetch(root: Path, records: Iterable[HostedFile], opener: Opener = _open) -> list[str]:
    """Download every listed file that is not in place; the paths downloaded."""
    fetched: list[str] = []
    for record in records:
        if state(root, record) == "absent":
            download(root, record, opener)
            fetched.append(record.path)
    return fetched


def describe(root: Path, path: Path, url_prefix: str) -> HostedFile:
    """A manifest record for a local file, to be hosted at `url_prefix + name`."""
    hasher, size = hashlib.sha256(), 0
    with path.open("rb") as source:
        while chunk := source.read(CHUNK):
            size += len(chunk)
            hasher.update(chunk)
    resolved = path.resolve()
    return HostedFile(
        name=path.name,
        path=resolved.relative_to(root.resolve()).as_posix(),
        size=size,
        sha256=hasher.hexdigest(),
        url=url_prefix.rstrip("/") + "/" + path.name,
    )


def render(records: Iterable[HostedFile], header: str = "") -> str:
    """The manifest's YAML text, files sorted by path."""
    lines = [*(f"# {line}".rstrip() for line in header.splitlines()), f"schema: {SCHEMA}"]
    lines.append("files:")
    for record in sorted(records, key=lambda item: item.path):
        lines.append(f"  - name: {record.name}")
        lines.append(f"    path: {record.path}")
        lines.append(f"    size: {record.size}")
        # Quoted, since a digest of decimal digits alone would read as a YAML number.
        lines.append(f'    sha256: "{record.sha256}"')
        lines.append(f"    url: {record.url}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    commands = parser.add_subparsers(dest="command", required=True)
    write = commands.add_parser("write", help="list local files in a new manifest")
    _ = write.add_argument("manifest", type=Path)
    _ = write.add_argument("--url-prefix", required=True, help="hosted at PREFIX/name")
    _ = write.add_argument("--root", type=Path, default=REPO)
    _ = write.add_argument("--header", default="", help="comment lines for the top")
    _ = write.add_argument("files", nargs="+", type=Path)
    get = commands.add_parser("fetch", help="download every listed file not in place")
    _ = get.add_argument("manifest", help="repository-relative")
    _ = get.add_argument("--root", type=Path, default=REPO)
    arguments = parser.parse_args(argv)
    root: Path = arguments.root
    if arguments.command == "write":
        records = [describe(root, path, arguments.url_prefix) for path in arguments.files]
        _ = arguments.manifest.write_text(render(records, arguments.header), encoding="utf-8")
        print(f"{arguments.manifest}: {len(records)} files, {sum(r.size for r in records):,} B")
        return 0
    try:
        files = load_manifest(root, arguments.manifest)
        fetched = fetch(root, files.values())
    except (HostedDataError, OSError) as error:
        print(f"refused: {error}")
        return 2
    print(f"{arguments.manifest}: fetched {len(fetched)} of {len(files)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
