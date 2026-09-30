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
/opt/homebrew/bin/gtimeout 30 /usr/bin/time -lp \
  .venv/bin/python3 -m devtools.check_n11_optimality_capture_ancestry \
  --packets resources/web/n11-optimality-2026-09-29/receipts/capture-ancestry/objects \
  --near-source "$1" \
  --pose-result resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/result.json \
  --output "$2/refusal-result.json" \
  --max-seconds 15 \
  > "$2/stdout.json" 2> "$2/outer-time.txt"
