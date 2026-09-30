"""The film poster is the frame its receipt says, and ffmpeg is asked for exactly that frame.

`poster_frame` and `seek_seconds` are pure, so the arithmetic is checked over a plain
receipt. The seek itself is checked against a real ffmpeg on a clip whose every frame is a
different grey, because a mocked ffmpeg proves nothing about which frame ffmpeg returns; that
one case is skipped where there is no ffmpeg.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest
from PIL import Image

from workbench_tools import poster

RECEIPT = {
    "range": [2, 5],
    "fps": 60,
    "steps": [
        {"n": 3, "frames": 4},
        {"n": 4, "frames": 5},
        {"n": 5, "frames": 3},
    ],
}


def test_the_poster_is_the_last_frame_its_step_owns() -> None:
    assert poster.poster_frame(RECEIPT, 3) == 3
    assert poster.poster_frame(RECEIPT, 4) == 8
    assert poster.poster_frame(RECEIPT, 5) == 11


def test_before_end_counts_back_inside_the_step() -> None:
    assert poster.poster_frame(RECEIPT, 4, before_end=4) == 4
    with pytest.raises(ValueError, match="0 to 4"):
        poster.poster_frame(RECEIPT, 4, before_end=5)
    with pytest.raises(ValueError, match="0 to 4"):
        poster.poster_frame(RECEIPT, 4, before_end=-1)


def test_a_step_outside_the_cut_is_refused() -> None:
    with pytest.raises(ValueError, match="not a step of this cut"):
        poster.poster_frame(RECEIPT, 88)


def test_each_published_cut_writes_its_own_poster() -> None:
    """The n = 1..324 cut must not overwrite the explainer's n = 1..100 poster."""
    assert poster.published_poster({"range": [2, 100]}) == (poster.POSTER, poster.POSTER_N)
    long_out, long_n = poster.published_poster({"range": [2, 324]})
    assert long_out != poster.POSTER
    assert long_n == 290
    for out, _ in poster.POSTERS.values():
        with Image.open(out) as image:
            assert image.size == (poster.POSTER_WIDTH, poster.POSTER_HEIGHT)
    with pytest.raises(ValueError, match="n = 5"):
        poster.published_poster(RECEIPT)


def test_the_seek_lands_half_a_frame_early() -> None:
    assert poster.seek_seconds(0, 60) == 0.0
    assert poster.seek_seconds(7864, 60) == pytest.approx(7863.5 / 60)
    with pytest.raises(ValueError, match="positive"):
        poster.seek_seconds(3, 0)


FRAMES = 12


def _grey(index: int) -> int:
    return 10 + 20 * index


@pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="needs ffmpeg")
def test_ffmpeg_returns_the_frame_asked_for(tmp_path: Path) -> None:
    frames = tmp_path / "frames"
    frames.mkdir()
    for index in range(FRAMES):
        Image.new("RGB", (64, 36), (_grey(index),) * 3).save(frames / f"f{index:03d}.png")
    video = tmp_path / "clip.mp4"
    subprocess.run(
        [
            "ffmpeg", "-v", "error", "-framerate", "60", "-i", str(frames / "f%03d.png"),
            "-c:v", "mpeg4", "-q:v", "1", "-pix_fmt", "yuv420p", str(video),
        ],
        check=True,
    )  # fmt: skip
    ffmpeg = str(shutil.which("ffmpeg"))
    for index in range(FRAMES):
        out = tmp_path / f"poster-{index}.png"
        command = poster.extract_arguments(ffmpeg, video, index, 60, out, width=32, height=18)
        subprocess.run(command, check=True)
        with Image.open(out) as image:
            assert image.size == (32, 18)
            grey = image.convert("L").getpixel((16, 9))
        assert isinstance(grey, int)
        assert abs(grey - _grey(index)) <= 4, f"frame {index} came back grey {grey}"


def test_a_video_its_receipt_does_not_describe_is_refused(tmp_path: Path) -> None:
    (tmp_path / "cut.mp4").write_bytes(b"not the cut")
    receipt = tmp_path / "cut.receipt.json"
    receipt.write_text(
        json.dumps({**RECEIPT, "video": "cut.mp4", "video_sha256": "0" * 64}), encoding="utf-8"
    )
    with pytest.raises(SystemExit, match="not the video"):
        poster.main([str(receipt), "--n", "4", "--out", str(tmp_path / "poster.png")])
