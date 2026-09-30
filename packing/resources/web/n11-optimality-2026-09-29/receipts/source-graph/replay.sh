#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 4 ]; then
  echo "usage: replay.sh EXTERNAL_SOURCE_DIR NEAR_JSON NEAR_GZ EXTERNAL_OUTPUT_DIR" >&2
  exit 2
fi

source /Volumes/spud-ext1/agent-scratch/wand125-tools-01a0ebfc/env.sh
test -d /Volumes/spud-ext1
test -w "$4"

repo_root=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
cd "$repo_root/packing"
/opt/homebrew/bin/gtimeout 45 /usr/bin/time -lp \
  .venv/bin/python3 -m devtools.check_n11_optimality_source_graph \
  --packets resources/web/n11-optimality-2026-09-29/receipts/capture-ancestry/objects \
  --upstream "$repo_root/attic/11SquaresOptimal" \
  --source-dir "$1" \
  --near-source "$2" \
  --near-compressed "$3" \
  --output "$4/result.json" \
  --max-seconds 30 \
  > "$4/stdout.json" 2> "$4/outer-time.txt"
