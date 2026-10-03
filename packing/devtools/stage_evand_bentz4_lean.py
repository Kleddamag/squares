"""Stage Evan Daniel's Lean reduction for s(k^2 - 4) = k from retained bytes, ready to build.

The reduction is ``SquarePacking.Bentz4.bentz4_of_validTilt9 : ValidTilt9 -> forall k,
8 <= k -> minSide (k ^ 2 - 4) = k`` in ``s12/lean/Sqpack/ValidSplit9.lean`` of
evand/square-packing at ``2eb15455``, the commit jlevy/squares#316 names. Its import
closure is sixteen project modules and Mathlib, all retained in the October 3 evand
packet as the upstream bytes, with the three lake files, the source's ``Axioms.lean`` and
the four data generators. The data files the generators read come from the same packet,
except ``L4_k02_family.txt``, which is the October 1 packet's copy, and the s(32) cover,
which is the September 26 packet's.

``stage --out DIR [--json RECEIPT]`` writes ``DIR/s12/`` and refuses any file whose Git
blob is not the one ``UPSTREAM`` names from the ``2eb15455`` tree. It regenerates the
four data modules, ``Bentz4Data.lean``, ``ValidSplitData.lean``, ``BentzData.lean`` and
``S32Data.lean``, with the source's own generators from the retained data files, and
refuses any that differs from the retained module: the source's ``verify.sh`` check that
the Lean data are these files. It also writes ``AxiomsBentz4.lean``, the probe that
prints the theorem, its hypotheses and the axioms, and scans the staged sources for the
tokens that would let a proof skip the kernel. It runs the generators under this
interpreter and builds nothing.

The build needs elan with ``leanprover/lean4:v4.33.1`` and the Mathlib cache. From
``DIR/s12/lean``::

    lake exe cache get
    python -m devtools.replay_receipt --receipt R/build_bentz4.log ... \\
        -- lake build Sqpack.ValidSplit9
    python -m devtools.replay_receipt --receipt R/axioms_bentz4.log ... \\
        -- lake env lean AxiomsBentz4.lean

``Sqpack/Bentz.lean`` is in the closure and peaks above 13 GB resident; see the October 1
packet's README for the swap it needed.
"""

from __future__ import annotations

import argparse
import gzip
import json
import shutil
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

from strif import atomic_write_text

from devtools.retained_data import git_blob
from devtools.stage_evand_bentz_lean import escapes

REPO = Path(__file__).resolve().parents[2]
WEB = REPO / "packing/resources/web"
PACKET = WEB / "evand-square-packing-2026-10-03"
OCT03 = PACKET / "square-packing/s12"
OCT01 = WEB / "evand-square-packing-2026-10-01/source/s12"
SEP26 = WEB / "evand-square-packing-2026-09-26/square-packing/s12"
RECEIPT = PACKET / "receipts/lean/bentz4_stage.json"
PIN = "2eb15455a6f178213287a84ab4d0576c060baabe"
#: Git blobs of the build's inputs in ``s12/`` at the pin, from ``git ls-tree``.
UPSTREAM = {
    "lean/lean-toolchain": "a8afa7d1b02d96f0671eba854a8dc4b416beb473",
    "lean/lakefile.toml": "3d90112e8d0f492f5d0d18d3a64e57fc04c932e0",
    "lean/lake-manifest.json": "43e6e5aafbfd523d9ff7b16869798d739d1cd16c",
    "lean/Axioms.lean": "4b3b070b0148781fd3699e79d8f02e17286c9915",
    "lean/Sqpack/Basic.lean": "cbfe567fe20c6b81899bd1ed6eb8cbd8611c090b",
    "lean/Sqpack/Chord.lean": "913bd7dfd7d8804315ba6adf132f95dddd768cc6",
    "lean/Sqpack/ZeroMargin.lean": "7d40021f619994ac900178c9a7e94f8cb4dcc27f",
    "lean/Sqpack/D4.lean": "d599b89dba509df9ab33adf2273249a2bc7fa00e",
    "lean/Sqpack/Cover.lean": "4fd6f59fc9c5943f5f884598e04820fe2ad67395",
    "lean/Sqpack/S32Data.lean": "b8ea5d9487edc11cb7c801af7f4c1c4724f79be0",
    "lean/Sqpack/S32.lean": "065a2c43515c363fbfce38bb7efc2e85d4d47578",
    "lean/Sqpack/MixedMeasure.lean": "196d723865ed62532795cbe229f3eaf2af525079",
    "lean/Sqpack/BentzData.lean": "74cf901dc4e8bbb321511e7a647229cdcae33210",
    "lean/Sqpack/Bentz.lean": "fe5cd3b7cc6fc55eaa5c2a3436925db90fef215f",
    "lean/Sqpack/BentzFam.lean": "629486a294f95f229b9a6a828dd1031572c28a3c",
    "lean/Sqpack/Bentz4Data.lean": "195987d3f28715d1217716afb9ca78972331e8a9",
    "lean/Sqpack/Bentz4.lean": "f28d6180b778e687b0739edbbffa5259818f2197",
    "lean/Sqpack/ValidSplit.lean": "dbff982340cc6f63c2d70fe31ce0322ffc058930",
    "lean/Sqpack/ValidSplitData.lean": "394cef7eca478fb8504324c807867e92d4813dce",
    "lean/Sqpack/ValidSplit9.lean": "7c2395839ab39b636f35d7bb3598d90b7155ab53",
    "lean/scripts/gen_s32_data.py": "7b32805f22a9feeab0400460913582c949a861a6",
    "lean/scripts/gen_bentz_data.py": "62fbcc3b2c18197b67af5ab4da558607a1f0566d",
    "lean/scripts/gen_bentzfam_data.py": "2264ab72abc197b1154f570bb02e586332656356",
    "lean/scripts/gen_validsplit_data.py": "319f36f9590bb849ff576d62a66893349cb116ea",
    "search/qx2_data/K4_k008_box9.txt": "cb803ebb08c3271301bc11e483aa4e377199d4be",
    "search/qx2_data/K4_k008_family.txt": "a18e20e3017d145981bd555f7d9e03dca5265294",
    "search/qx2_data/L4_k02_box7.txt": "e28fabfaa309334983e4e2e33355afbcf758b962",
    "search/qx2_data/L4_k02_family.txt": "be71d3dbb0370bd95d39c9c667973aafc7d3e1b2",
    "certificates/s32/s32_closed_cover_6.txt": "ece6239cd96f89c9249a2dd62d5736b2981d647f",
}
#: Where each input is retained; a ``.gz`` holds the gzipped upstream bytes.
RETAINED = {
    **{
        name: OCT03 / name
        for name in UPSTREAM
        if name.startswith("lean/") and name != "lean/lean-toolchain"
    },
    "lean/lean-toolchain": OCT03 / "lean/lean-toolchain",
    "search/qx2_data/K4_k008_box9.txt": OCT03 / "search/qx2_data/K4_k008_box9.txt.gz",
    "search/qx2_data/K4_k008_family.txt": OCT03 / "search/qx2_data/K4_k008_family.txt",
    "search/qx2_data/L4_k02_box7.txt": OCT03 / "search/qx2_data/L4_k02_box7.txt",
    "search/qx2_data/L4_k02_family.txt": OCT01 / "certificates/k2m3/L4_k02_family.txt",
    "certificates/s32/s32_closed_cover_6.txt": SEP26
    / "certificates/s32/s32_closed_cover_6.txt.gz",
}
#: Each regenerated data module and the generator argv (from ``s12/``) that writes it.
GENERATORS = {
    "lean/Sqpack/Bentz4Data.lean": [
        "lean/scripts/gen_bentzfam_data.py",
        "--search",
        "search",
        "--out",
        "regenerate/Bentz4Data.lean",
    ],
    "lean/Sqpack/ValidSplitData.lean": [
        "lean/scripts/gen_validsplit_data.py",
        "--search",
        "search",
        "--out",
        "regenerate/ValidSplitData.lean",
    ],
    "lean/Sqpack/BentzData.lean": [
        "lean/scripts/gen_bentz_data.py",
        "--search",
        "search",
        "--out",
        "regenerate/BentzData.lean",
    ],
}
THEOREM = "SquarePacking.Bentz4.bentz4_of_validTilt9"
#: Lemmas whose axioms the probe prints besides the theorem's.
LEMMAS = (
    "SquarePacking.Bentz4.valid9_of_tilt",
    "SquarePacking.Bentz4.valid9_of_tilt_axis",
    "SquarePacking.Bentz4.validAxis9",
    "SquarePacking.Bentz4.box9_grid",
    "SquarePacking.Bentz4.d4_box9",
    "SquarePacking.Bentz4.bentz4_of_valid9",
    "SquarePacking.Bentz4.box9Cover_measure",
    "SquarePacking.Bentz4.famCover_total4",
    "SquarePacking.ValidSplit.valid_of_tilt_axis",
    "SquarePacking.ValidSplit.validAxis_packed",
)
PROBE = (
    "import Sqpack.ValidSplit9\n\n"
    f"#check @{THEOREM}\n"
    "#print SquarePacking.Bentz4.ValidTilt9\n"
    "#print SquarePacking.ValidSplit.ValidTilt\n"
    "#print SquarePacking.Bentz4.Valid9\n"
    "#print SquarePacking.minSide\n"
    "#print SquarePacking.Packs\n"
    + "".join(f"#print axioms {name}\n" for name in (THEOREM, *LEMMAS))
)


def _read(path: Path) -> bytes:
    data = path.read_bytes()
    return gzip.decompress(data) if path.suffix == ".gz" else data


def _generate(s12: Path, argv: list[str]) -> str:
    done = subprocess.run(
        [sys.executable, *argv], cwd=s12, capture_output=True, text=True, check=False
    )
    if done.returncode:
        msg = f"{argv[0]} failed: {done.stderr.strip()}"
        raise SystemExit(msg)
    return done.stdout.strip()


def stage(out: Path) -> dict[str, object]:
    """Write ``out/s12`` from retained bytes, regenerate the data modules, check blobs."""
    s12 = out / "s12"
    if s12.exists():
        shutil.rmtree(s12)
    problems: list[str] = []
    for name, source in RETAINED.items():
        target = s12 / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(_read(source))
    retained = {
        name: (s12 / name).read_bytes() for name in (*GENERATORS, "lean/Sqpack/S32Data.lean")
    }
    (s12 / "regenerate").mkdir()
    logs: dict[str, str] = {}
    for name, argv in GENERATORS.items():
        logs[Path(argv[0]).stem] = _generate(s12, argv)
        if (s12 / argv[-1]).read_bytes() != retained[name]:
            problems.append(
                f"{Path(name).name} regenerated from the data differs from the retained one"
            )
    shutil.rmtree(s12 / "regenerate")
    s32 = "lean/Sqpack/S32Data.lean"
    logs["gen_s32_data"] = _generate(
        s12, ["lean/scripts/gen_s32_data.py", "certificates/s32/s32_closed_cover_6.txt"]
    )
    if (s12 / s32).read_bytes() != retained[s32]:
        problems.append("S32Data.lean regenerated from the cover differs from the retained one")
    blobs: dict[str, str] = {}
    for name, want in UPSTREAM.items():
        blobs[name] = git_blob((s12 / name).read_bytes())
        if blobs[name] != want:
            problems.append(f"{name} is blob {blobs[name][:12]}, upstream {want[:12]}")
    lean = s12 / "lean"
    (lean / "AxiomsBentz4.lean").write_text(PROBE, encoding="utf-8")
    found = escapes(lean)
    problems += [
        f"{count} x {token} in the staged sources" for token, count in found.items() if count
    ]
    return {
        "kind": "evand-bentz4-lean-stage/v1",
        "ok": not problems,
        "problems": problems,
        "upstream": f"evand/square-packing {PIN} s12/",
        "toolchain": (lean / "lean-toolchain").read_text(encoding="utf-8").strip(),
        "blobs": blobs,
        "regenerated": logs,
        "kernel_escapes": found,
        "probe": "lean/AxiomsBentz4.lean",
        "theorem": THEOREM,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--out", type=Path, required=True, help="directory to stage s12/ in")
    parser.add_argument("--json", type=Path, help="also write the receipt here")
    args = parser.parse_args(argv)
    receipt = stage(args.out)
    text = json.dumps(receipt, indent=2) + "\n"
    if args.json:
        atomic_write_text(args.json, text)
    print(text, end="")
    print("BENTZ4_LEAN_STAGED" if receipt["ok"] else "BENTZ4_LEAN_STAGE_FAILED")
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
