#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "usage: replay.sh PINNED_DECODED_NEAR_JSON EXTERNAL_OUTPUT_DIR" >&2
  exit 2
fi

source /Volumes/spud-ext1/agent-scratch/wand125-tools-01a0ebfc/env.sh
test -d /Volumes/spud-ext1
test -w "$2"

repo_root=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
cd "$repo_root/packing"
/opt/homebrew/bin/gtimeout 60 /usr/bin/time -lp \
  .venv/bin/python3 -m devtools.check_n11_optimality_pose_inclusion \
  --source "$1" \
  --guards resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/guard.json \
  --focused resources/web/n11-optimality-2026-09-29/receipts/local-dual-residual/objects/9a9cf4e0fdcb1b1d226b9c07ec08d08cbbc572749cec9bc09cf3cd92bd4d88f3.gz \
  --local-result resources/web/n11-optimality-2026-09-29/receipts/local-isolation/result.json \
  --output "$2/result.json" \
  --derived-output "$2/derived-state.json.gz" \
  --max-seconds 30 \
  > "$2/stdout.json" 2> "$2/outer-time.txt"
