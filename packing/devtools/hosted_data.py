"""Stage, check, publish and fetch bulk data hosted as GitHub release assets (OR-18).

A manifest in ``packing/hosted/`` names one release and every object on it;
`sqpack.hosted_data` holds the contract and the logic. development.md, Publishing Hosted
Data, is the procedure a pull request that adds hosted data follows.

Usage, from ``packing/``::

    python -m devtools.hosted_data stage --manifest hosted/n17-dumps.yaml \\
        --from cases/n17/dumps --repository jlevy/squares --tag data/n17-dumps-v1
    python -m devtools.hosted_data check --manifest hosted/n17-dumps.yaml
    python -m devtools.hosted_data publish --manifest hosted/n17-dumps.yaml
    python -m devtools.hosted_data fetch --manifest hosted/n17-dumps.yaml [--only 'GLOB']

``check`` is offline. ``publish`` and ``fetch`` run ``gh``, which needs the GitHub proxy
bypass that AGENTS.md, GitHub CLI, sets out.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from sqpack.hosted_data import (
    GhClient,
    HostedDataError,
    check,
    fetch,
    fetch_command,
    load_manifest,
    publish,
    repository_root,
    stage,
)


def _mib(size: int) -> str:
    return f"{size / 2**20:,.1f} MiB"


def _report(problems: list[str], manifest: Path) -> int:
    for problem in problems:
        print(f"{manifest}: {problem}", file=sys.stderr)
    return 1 if problems else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    commands = parser.add_subparsers(dest="command", required=True)
    staging = commands.add_parser("stage", help="write or update a manifest from local files")
    staging.add_argument("--manifest", type=Path, required=True)
    staging.add_argument("--from", dest="source", type=Path, required=True)
    staging.add_argument("--repository", help="OWNER/NAME; required for a new manifest")
    staging.add_argument("--tag", help="data/<subject>-v<N>; required for a new manifest")
    checking = commands.add_parser("check", help="check manifests offline")
    checking.add_argument("--manifest", type=Path, action="append", required=True)
    fetching = commands.add_parser("fetch", help="download and verify hosted objects")
    fetching.add_argument("--manifest", type=Path, required=True)
    fetching.add_argument("--only", metavar="GLOB", help="match against path or asset name")
    fetching.add_argument(
        "--replace", action="store_true", help="overwrite a present file whose bytes differ"
    )
    publishing = commands.add_parser("publish", help="create the release, upload, verify")
    publishing.add_argument("--manifest", type=Path, required=True)
    publishing.add_argument("--title", help="the release title; defaults to the tag")
    publishing.add_argument("--notes", help="the release notes; defaults to a pointer")
    publishing.add_argument("--target", help="commit or branch the new tag points at")
    args = parser.parse_args(argv)
    repo = repository_root()
    try:
        if args.command == "check":
            problems: list[str] = []
            for path in args.manifest:
                problems += [
                    f"{path}: {problem}" for problem in check(load_manifest(path), repo)
                ]
            for problem in problems:
                print(problem, file=sys.stderr)
            if not problems:
                print(f"{len(args.manifest)} manifest(s) pass")
            return 1 if problems else 0
        if args.command == "stage":
            manifest = stage(
                args.manifest, args.source, repo, repository=args.repository, tag=args.tag
            )
            print(
                f"{args.manifest}: {len(manifest.objects)} objects, "
                f"{_mib(manifest.total_size)}, for {manifest.repository}@{manifest.tag}"
            )
            return _report(check(manifest, repo), args.manifest)
        manifest = load_manifest(args.manifest)
        if problems := check(manifest, repo):
            return _report(problems, args.manifest)
        if args.command == "fetch":
            for outcome in fetch(
                manifest, repo, GhClient(), only=args.only, replace_local=args.replace
            ):
                print(f"{outcome.action:8} {outcome.path}")
            return 0
        named = Path(os.path.relpath(args.manifest.resolve(), repo)).as_posix()
        notes = args.notes or (
            f"Hosted data named by `{named}`: "
            f"{len(manifest.objects)} objects, {_mib(manifest.total_size)}. "
            f"Fetch with `{fetch_command(args.manifest)}` from `packing/`. "
            "Data, not a version of the project."
        )
        result = publish(
            manifest,
            repo,
            GhClient(),
            title=args.title or manifest.tag,
            notes=notes,
            target=args.target,
        )
    except HostedDataError as error:
        print(f"refused: {error}", file=sys.stderr)
        return 1
    url = f"https://github.com/{manifest.repository}/releases/tag/{manifest.tag}"
    print(f"{'created' if result.created else 'existing'} {url}")
    print(f"uploaded {len(result.uploaded)}, already present {len(result.already_present)}")
    print(f"verified {len(result.verified)} served assets, {_mib(manifest.total_size)}")
    for name in result.unnamed:
        print(f"note: {name} is on the release but not in the manifest", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
