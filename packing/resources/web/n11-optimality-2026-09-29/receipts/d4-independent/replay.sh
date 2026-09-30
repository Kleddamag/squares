#!/usr/bin/env bash
set -euo pipefail

receipt_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$receipt_dir/../../../../../.." && pwd)"
source /Volumes/spud-ext1/agent-scratch/wand125-tools-01a0ebfc/env.sh
test -d /Volumes/spud-ext1/agent-scratch/wand125-tools-01a0ebfc
test -w /Volumes/spud-ext1/agent-scratch/wand125-tools-01a0ebfc

for role in cover overlay distance; do
    case "$role" in
        cover)
            key=df7938d9ba27095a38fabe45f8b26b259a2cc896c2ae4aac6bae874f417adc4e
            oid=7c6d14012f06eb892912a50c93cc7408ce1f90524d46693c6178a01ceae71a99 ;;
        overlay)
            key=845b5f748843dd60fa7e290a5ea1a304da4e439ae229bd73a841aec816f4e700
            oid=4b36026f5f16998929032abf5e730b56a2166a0880d5b6464b3abf9d9ed62bda ;;
        distance)
            key=4f960f4001faa6c9c1e7521f3a2344f71e10b41cd38a6425f6821cc1fd2ccd47
            oid=64bcfe233d888ef1a435589ec68ad9d04c4fe33cd20f9864d719281af663e2f9 ;;
    esac
    test "$(shasum -a 256 "$receipt_dir/objects/$key.gz" | cut -d ' ' -f 1)" = "$oid"
    gzip -cd "$receipt_dir/objects/$key.gz" > "$TMPDIR/n11-d4-$role.json"
    test "$(shasum -a 256 "$TMPDIR/n11-d4-$role.json" | cut -d ' ' -f 1)" = "$key"
done

cd "$repo_root"
/usr/bin/time -p /opt/homebrew/bin/timeout 55s \
    packing/.venv/bin/python3 -B packing/devtools/check_n11_optimality_d4.py \
    --cover "$TMPDIR/n11-d4-cover.json" \
    --overlay "$TMPDIR/n11-d4-overlay.json" \
    --distance "$TMPDIR/n11-d4-distance.json" \
    --max-seconds 45 --output "$TMPDIR/n11-d4-result.json" \
    > "$TMPDIR/n11-d4-stdout.json" 2> "$TMPDIR/n11-d4-outer-time.txt"
