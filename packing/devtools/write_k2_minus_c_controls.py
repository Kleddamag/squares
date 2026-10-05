"""Write the two control inputs for the replay of Lemma 4.10 of Ryu's k^2 - c preprint.

The certificate of Lemma 4.10 (``data/kw9_data.zip`` in the
``squarepacker-k2-minus-c-2026-10-05`` packet) is 13 lists of accepted boxes. Its
checkers decide two things: ``verify_leaves2.py`` that every box has rigorous bound at
most ``T = 9``, and the three coverage programs that the boxes leave no gap. Each needs
a control it must refuse, and both come from one box: the box of
``bnb_n2_T9_0of1_final_leaves.jsonl`` that holds the preprint's sharp configuration, two
inner centres at radius ``1/2`` and angles ``0`` and ``pi`` (``code/attack_kw/hand9.json``,
nine pairs at the uncovered point, Remark 7.5).

- ``sharp-leaf/``: that box alone. ``verify_leaves2.py`` with ``T = 9`` accepts it;
  with ``T = 8`` it must refuse, since any box holding a configuration with nine pairs has
  rigorous bound at least nine.
- ``drop-one/``: the n = 2 list with that box removed. Every coverage program must
  report the gap it leaves.

The box is chosen by rule, the first box whose closed intervals contain ``r_1 = r_2 =
1/2`` and the exact ``theta_2 = pi`` (its lower end is the double below ``pi``), so the
outputs are deterministic. Run from ``packing/``::

    uv run --frozen --all-extras --group dev python -m devtools.write_k2_minus_c_controls OUT
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import zipfile
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path

PACKET = (
    Path(__file__).resolve().parents[1] / "resources/web/squarepacker-k2-minus-c-2026-10-05"
)
ARCHIVE = PACKET / "k2-minus-c/data/kw9_data.zip"
LEAVES = "bnb_n2_T9_0of1_final_leaves.jsonl"
#: The exact pi lies above the double nearest it, so a closed interval of doubles holds
#: it when its lower end is at most math.pi and its upper end is above math.pi.
_PI_DOUBLE = Fraction(math.pi)


def _holds_sharp_point(record: dict) -> bool:
    (r1_lo, r1_hi, _, _), (r2_lo, r2_hi, t_lo, t_hi) = record["box"]
    return (
        r1_lo <= 0.5 <= r1_hi
        and r2_lo <= 0.5 <= r2_hi
        and Fraction(t_lo) <= _PI_DOUBLE
        and Fraction(t_hi) > _PI_DOUBLE
    )


def sharp_index(lines: Sequence[str]) -> int:
    """The index of the first box that holds the sharp configuration."""
    for index, line in enumerate(lines):
        if _holds_sharp_point(json.loads(line)):
            return index
    msg = f"no box of {LEAVES} holds the sharp configuration"
    raise ValueError(msg)


def write_controls(out: Path, archive: Path = ARCHIVE) -> dict[str, object]:
    """Write ``sharp-leaf/`` and ``drop-one/`` under ``out``; return their record."""
    with zipfile.ZipFile(archive) as bundle:
        text = bundle.read(LEAVES).decode("utf-8")
    lines = text.splitlines(keepends=True)
    index = sharp_index(lines)
    outputs = {
        "sharp-leaf": [lines[index]],
        "drop-one": lines[:index] + lines[index + 1 :],
    }
    record: dict[str, object] = {
        "source": f"{LEAVES} in data/kw9_data.zip",
        "source_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "source_boxes": len(lines),
        "sharp_box_index": index,
        "sharp_box": json.loads(lines[index]),
    }
    for name, chosen in outputs.items():
        path = out / name / LEAVES
        path.parent.mkdir(parents=True, exist_ok=True)
        data = "".join(chosen).encode("utf-8")
        path.write_bytes(data)
        record[name] = {
            "path": f"{name}/{LEAVES}",
            "boxes": len(chosen),
            "sha256": hashlib.sha256(data).hexdigest(),
        }
    return record


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("out", type=Path, help="directory to write the controls into")
    args = parser.parse_args(argv)
    record = write_controls(args.out)
    sys.stdout.write(json.dumps(record, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
