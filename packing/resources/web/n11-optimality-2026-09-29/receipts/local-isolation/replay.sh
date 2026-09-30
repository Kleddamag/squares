#!/usr/bin/env bash
set -euo pipefail

receipt_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$receipt_dir/../../../../../.." && pwd)"
source /Volumes/spud-ext1/agent-scratch/wand125-tools-01a0ebfc/env.sh
test -d /Volumes/spud-ext1/agent-scratch/wand125-tools-01a0ebfc
test -w /Volumes/spud-ext1/agent-scratch/wand125-tools-01a0ebfc

for role in weighted focused; do
    case "$role" in
        weighted)
            key=ffe9f89d40a9538ec9a10d8700999f05483d0ccfad17b84d430590da7dd65889
            oid=25f7ca79130e14bf63a2a08f2246bc6b02b53effd85b87b3831207539014ba1c ;;
        focused)
            key=9a9cf4e0fdcb1b1d226b9c07ec08d08cbbc572749cec9bc09cf3cd92bd4d88f3
            oid=cb67f9e3b0d473f1a6c32c561cd9a2f03bf002118d335e7ec73e5eea4051d610 ;;
    esac
    object="$receipt_dir/../local-dual-residual/objects/$key.gz"
    test "$(shasum -a 256 "$object" | cut -d ' ' -f 1)" = "$oid"
    gzip -cd "$object" > "$TMPDIR/n11-local-$role.json"
    test "$(shasum -a 256 "$TMPDIR/n11-local-$role.json" | cut -d ' ' -f 1)" = "$key"
done

cd "$repo_root/packing"
/usr/bin/time -p /opt/homebrew/bin/timeout 55s .venv/bin/python3 -B \
    -m devtools.check_n11_optimality_local_isolation \
    --weighted "$TMPDIR/n11-local-weighted.json" \
    --focused "$TMPDIR/n11-local-focused.json" \
    --branch-limit 128 --max-seconds 45 \
    --output "$TMPDIR/n11-local-isolation-result.json" \
    > "$TMPDIR/n11-local-isolation-stdout.json" \
    2> "$TMPDIR/n11-local-isolation-outer-time.txt"
