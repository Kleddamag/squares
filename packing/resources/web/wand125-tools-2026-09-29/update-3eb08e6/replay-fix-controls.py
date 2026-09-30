"""Replay scoped wand125 wrapper-admission controls without a real certificate.

The fake certifier below deliberately returns a synthetic summary. It demonstrates
whether the wrapper reaches its certificate-claim branch; it does not verify any
geometry. Run with the project's Python 3.14 and an external-scratch TMPDIR.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import cast

REPO = Path(__file__).resolve().parents[5]
UPSTREAM = REPO / "attic/wand125-tools"
OLD = "0d33ab61726c2ab03e3eb8f457dabaf22db8571f"
CURRENT = "3eb08e6c675d8d5aa953cb93da049a3f3cdc6123"
SCRIPT = "transfer/scale_and_verify.py"
REPLAY_COMMAND = (
    "source /Volumes/spud-ext1/agent-scratch/wand125-tools-01a0ebfc/env.sh && "
    "packing/.venv/bin/python3 "
    "packing/resources/web/wand125-tools-2026-09-29/update-3eb08e6/"
    "replay-fix-controls.py"
)
FAKE_CERTIFIER = """from pathlib import Path
import argparse, json, os
p = argparse.ArgumentParser()
p.add_argument("candidate")
p.add_argument("--out", required=True)
p.add_argument("--workers")
a = p.parse_args()
Path(os.environ["FAKE_CERTIFIER_MARKER"]).write_text("called\\n")
out = Path(a.out)
out.mkdir(parents=True, exist_ok=True)
(out / "verification_summary.json").write_text(json.dumps({
    "status": os.environ["FAKE_CERTIFIER_STATUS"],
    "angle_cases": 201, "nodes": 1,
    "minimum_printed_leaf_lower_bound": 1.001,
}))
"""


def git(*args: str) -> bytes:
    return subprocess.check_output(("git", "-C", str(UPSTREAM), *args))


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def require(condition: object, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def candidate(path: Path, *, n: int | None, weight: str) -> None:
    data: dict[str, object] = {"L": "1.5", "weights": [weight], "rectangles": [[0, 0, 1, 1]]}
    if n is not None:
        data["n"] = n
    path.parent.mkdir(parents=True, exist_ok=True)
    _ = path.write_text(json.dumps(data), encoding="utf-8")


def wrapper(
    script: Path,
    case: Path,
    *,
    n: int | None,
    weight: str,
    args: tuple[str, ...] = (),
    fake_status: str = "VERIFIED",
) -> tuple[subprocess.CompletedProcess[str], bool, bool]:
    search, out, marker = case / "search", case / "out", case / "fake-called"
    candidate(search / "candidate.json", n=n, weight=weight)
    solver = case / "solver"
    solver.mkdir()
    _ = (solver / "certify.py").write_text(FAKE_CERTIFIER)
    env = dict(os.environ)
    env.update(FAKE_CERTIFIER_MARKER=str(marker), FAKE_CERTIFIER_STATUS=fake_status)
    result = subprocess.run(
        (
            sys.executable,
            str(script),
            str(search),
            str(out),
            "--solver-dir",
            str(solver),
            *args,
        ),
        cwd=case,
        env=env,
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    return result, marker.exists(), out.exists()


def replay() -> dict[str, object]:
    require(git("rev-parse", "HEAD").decode().strip() == CURRENT, "upstream checkout changed")
    old_raw = git("show", f"{OLD}:{SCRIPT}")
    current_raw = git("show", f"{CURRENT}:{SCRIPT}")
    require((UPSTREAM / SCRIPT).read_bytes() == current_raw, "current wrapper bytes changed")
    cap_raw = git("show", f"{CURRENT}:transfer/l_cap.py")
    require((UPSTREAM / "transfer/l_cap.py").read_bytes() == cap_raw, "L-cap bytes changed")
    scratch = Path(os.environ["TMPDIR"]).resolve()
    require(scratch.is_dir() and os.access(scratch, os.W_OK), "external TMPDIR unavailable")
    require(
        str(scratch).startswith("/Volumes/spud-ext1/agent-scratch/"),
        "TMPDIR is not external scratch",
    )

    with tempfile.TemporaryDirectory(prefix="wand125-fix-control-", dir=scratch) as name:
        root = Path(name)
        old_script = root / "old/transfer/scale_and_verify.py"
        old_script.parent.mkdir(parents=True)
        _ = old_script.write_bytes(old_raw)
        paths = root / "old/ladder/paths.py"
        paths.parent.mkdir(parents=True)
        _ = paths.write_text("from pathlib import Path\ndef solver_dir(): return Path('.')\n")
        current_script = UPSTREAM / SCRIPT

        old, old_called, _ = wrapper(
            old_script, root / "old-invalid", n=1, weight="0.5", args=("--target", "28.9")
        )
        require(
            old.returncode == 0 and old_called,
            "historical wrapper did not reach fake certifier",
        )
        require("certificate for s(1) >= 1.5" in old.stdout, "historical claim path changed")

        fixed, fixed_called, fixed_out = wrapper(
            current_script, root / "new-invalid", n=1, weight="0.5", args=("--target", "28.9")
        )
        require(
            fixed.returncode != 0 and "below n" in fixed.stderr, "invalid target not refused"
        )
        require(
            not fixed_called and not fixed_out,
            "invalid target reached certifier or wrote proof",
        )

        default, default_called, default_out = wrapper(
            current_script, root / "default", n=1, weight="1"
        )
        require(
            default.returncode != 0 and "at or above the target" in default.stderr,
            "default n-1/100 budget not enforced",
        )
        require(
            not default_called and not default_out,
            "default over-budget input reached certifier",
        )

        missing, missing_called, missing_out = wrapper(
            current_script, root / "missing", n=None, weight="0.5"
        )
        require(
            missing.returncode != 0 and "pass --n" in missing.stderr, "missing n not refused"
        )
        require(not missing_called and not missing_out, "missing n reached certifier")

        mismatch, mismatch_called, mismatch_out = wrapper(
            current_script, root / "mismatch", n=2, weight="0.5", args=("--n", "1")
        )
        require(
            mismatch.returncode != 0 and "disagrees" in mismatch.stderr,
            "conflicting n not refused",
        )
        require(not mismatch_called and not mismatch_out, "conflicting n reached certifier")

        partial, partial_called, _ = wrapper(
            current_script, root / "partial", n=3, weight="0.5", fake_status="PARTIAL"
        )
        require(partial_called and partial.returncode != 0, "non-VERIFIED status not refused")
        require(
            "not verified: no certificate" in partial.stdout, "partial status message changed"
        )
        require(
            "=> certificate for" not in partial.stdout,
            "partial status printed certificate claim",
        )

        cap = subprocess.run(
            (sys.executable, str(UPSTREAM / "transfer/l_cap.py"), "29", "78", "83"),
            cwd=root,
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        require(cap.returncode == 0, "L-cap guide failed")
        rows = [cast(dict[str, object], json.loads(line)) for line in cap.stdout.splitlines()]
        require([row["n"] for row in rows] == [29, 78, 83], "L-cap row order changed")
        require(rows[0]["factor"] == "399908091/400000000", "general-angle factor changed")
        require(
            rows[1]["factor"] == "9977/10000" and rows[1]["L_cap"] == 8.979,
            "on-net integer factor changed",
        )
        require(
            all(row["note"] == "search guide, not a proven bound" for row in rows),
            "L-cap guide was promoted to a proof claim",
        )

    return {
        "status": "PASS_WRAPPER_ADMISSION_CONTROLS_ONLY",
        "old_commit": OLD,
        "current_commit": CURRENT,
        "old_wrapper_sha256": sha(old_raw),
        "current_wrapper_sha256": sha(current_raw),
        "current_l_cap_sha256": sha(cap_raw),
        "control_runner_sha256": sha(Path(__file__).read_bytes()),
        "replay_command_from_repository_root": REPLAY_COMMAND,
        "old_invalid_n1_target_28_9_reached_fake_claim_path": True,
        "fixed_invalid_n1_target_28_9_refused_before_fake_certifier": True,
        "fixed_default_budget_and_n_mismatch_refused": True,
        "fixed_nonverified_summary_refused": True,
        "l_cap_general_and_on_net_factors_checked": True,
        "fake_certifier_only": True,
        "canonical_cpp_executed": False,
        "geometry_verified": False,
        "speed_parity_measured": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = cast(Path | None, args.output)
    result = replay()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output:
        with output.open("x", encoding="utf-8") as stream:
            _ = stream.write(encoded)
    _ = sys.stdout.write(encoded)


if __name__ == "__main__":
    main()
