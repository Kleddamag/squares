#!/usr/bin/env python3
"""Cut a film's poster out of a captured video, by the step its receipt names.

Each published film shows a poster until a reader presses play: a frame of the film itself,
scaled to 1280x720, the video's own 16:9, so the box the poster fills is the box the video
fills. The explainer's n = 1..100 film shows `assets/ascent-n1-100-poster.png`, its n = 88;
the overview's n = 1..324 film shows `assets/ascent-n1-324-poster.png`, its n = 290. The cut
a receipt describes picks its poster, by the last n of its range, so neither re-cut can
overwrite the other's. The frame carries the version stamp, so a re-cut from new data
leaves the old poster naming the old data until it is cut again.

**The receipt says where the poster's n is.** It lists every step the cut drew, in order,
with the frames each owns, so a step's frames are a contiguous run and the last of them is
the step's settled end (`capture_video.frame_schedule`). This takes that frame, or one
`--before-end` frames earlier, and checks the video beside the receipt is the one the
receipt describes before reading anything from it.

The seek is to half a frame before the wanted frame's own instant, so the first frame at or
after it is that frame whichever way ffmpeg rounds the time.

Usage, from `packing/`, once per cut:
    uv run --frozen --all-extras --group dev python -m workbench_tools.poster \
        site/workbench/ascent-n1-100-1080p60-citations.receipt.json
    uv run --frozen --all-extras --group dev python -m workbench_tools.poster \
        site/workbench/ascent-n1-324-1080p60-citations.receipt.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from strif import atomic_output_file

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
POSTER = PACKAGE_ROOT / "assets/ascent-n1-100-poster.png"

#: The n the published poster shows: a diagonal band of tilted squares across the grid, with
#: the facts column carrying its bound, its citation and the version stamp.
POSTER_N = 88

#: Each published cut's poster and the n it shows, by the last n of the cut's range. The
#: n = 1..324 film's is n = 290 (2026-09-30): two tilted blocks in one grid, with both
#: bounds and both citations in the facts column, where n = 324 itself is a full grid.
POSTERS: dict[int, tuple[Path, int]] = {
    100: (POSTER, POSTER_N),
    324: (PACKAGE_ROOT / "assets/ascent-n1-324-poster.png", 290),
}

#: The poster's size since it was first published (2026-09-22): the stage's 16:9 at two
#: thirds.
POSTER_WIDTH = 1280
POSTER_HEIGHT = 720


def poster_frame(receipt: Mapping[str, Any], n: int, *, before_end: int = 0) -> int:
    """The index in the cut of step `n`'s settled end, or of `before_end` frames before it."""
    start = 0
    for step in receipt["steps"]:
        frames = int(step["frames"])
        if int(step["n"]) == n:
            if not 0 <= before_end < frames:
                raise ValueError(
                    f"n = {n} owns {frames} frames, so --before-end must be 0 to {frames - 1}"
                )
            return start + frames - 1 - before_end
        start += frames
    raise ValueError(f"n = {n} is not a step of this cut, which covers {receipt.get('range')}")


def published_poster(receipt: Mapping[str, Any]) -> tuple[Path, int]:
    """The poster this cut publishes and the n it shows, by the last n of its range."""
    last = int(receipt["range"][1])
    if last not in POSTERS:
        raise ValueError(f"no published poster for a cut ending at n = {last}")
    return POSTERS[last]


def seek_seconds(index: int, fps: int) -> float:
    """Half a frame before frame `index`, so the first frame at or after it is that one."""
    if fps <= 0:
        raise ValueError(f"fps must be positive, got {fps}")
    return max(0.0, (index - 0.5) / fps)


def extract_arguments(
    ffmpeg: str, video: Path, index: int, fps: int, out: Path, *, width: int, height: int
) -> list[str]:
    """The ffmpeg command that writes frame `index` of `video`, scaled, to the PNG `out`."""
    return [
        ffmpeg,
        "-v",
        "error",
        "-y",
        "-ss",
        f"{seek_seconds(index, fps):.6f}",
        "-i",
        str(video),
        "-frames:v",
        "1",
        "-vf",
        f"scale={width}:{height}:flags=lanczos",
        "-update",
        "1",
        str(out),
    ]


def _digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("receipt", type=Path, help="the cut's .receipt.json, beside its video")
    ap.add_argument(
        "--n", type=int, help="the step to take the frame from (default: the cut's poster n)"
    )
    ap.add_argument(
        "--before-end",
        type=int,
        default=0,
        help="frames before the step's settled end (0, the default, is the settled end)",
    )
    ap.add_argument("--width", type=int, default=POSTER_WIDTH)
    ap.add_argument("--height", type=int, default=POSTER_HEIGHT)
    ap.add_argument("--out", type=Path, help="the PNG to write (default: the cut's poster)")
    o = ap.parse_args(argv)

    receipt = json.loads(o.receipt.read_text(encoding="utf-8"))
    if o.n is None or o.out is None:
        try:
            default_out, default_n = published_poster(receipt)
        except ValueError as error:
            raise SystemExit(f"{error}; pass --n and --out") from error
        o.n = default_n if o.n is None else o.n
        o.out = default_out if o.out is None else o.out
    video = o.receipt.parent / str(receipt["video"])
    if not video.exists():
        raise SystemExit(f"{video} is not beside its receipt")
    if _digest(video) != receipt["video_sha256"]:
        raise SystemExit(f"{video} is not the video {o.receipt.name} describes")
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise SystemExit("no ffmpeg on PATH")
    fps = int(receipt["fps"])
    try:
        index = poster_frame(receipt, o.n, before_end=o.before_end)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    with atomic_output_file(o.out, make_parents=True, tmp_suffix=".partial.png") as partial:
        command = extract_arguments(
            ffmpeg, video, index, fps, partial, width=o.width, height=o.height
        )
        done = subprocess.run(command, capture_output=True, text=True, check=False)
        if done.returncode != 0:
            raise SystemExit(f"ffmpeg failed:\n{done.stderr[-2000:]}")
    print(
        f"{o.out}: n = {o.n}, frame {index} of {receipt['frames']} "
        f"({index / fps:.3f} s), {o.width}x{o.height}, stamped {receipt['version']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
