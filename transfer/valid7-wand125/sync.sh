#!/bin/bash
# copies receipts and records for shards 7-9 into transfer/, gzips jsonl, skips files >90MB
W=$HOME/valid7-work; T=/home/user/squares/transfer/valid7-wand125
cd /home/user/squares
for f in $W/receipts/wand125_shard0[789]_*; do [ -e "$f" ] && cp "$f" $T/; done
for f in $W/runs/wand125_shard0[789]_*; do
  [ -e "$f" ] || continue
  b=$(basename $f)
  gzip -9nc "$f" > $T/$b.gz
  s=$(stat -c %s $T/$b.gz)
  if [ $s -gt 94371840 ]; then echo "$b.gz $s $(sha256sum $T/$b.gz | cut -d' ' -f1)" >> $T/LARGE-w3.txt; rm $T/$b.gz; fi
done
git add -A transfer && git commit -q -m "transfer: valid7 wand125 shards 7-9 (partial or complete)

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0185351vkZWnES4rr5vzafud"
d=2; for i in 1 2 3 4 5; do git push -q -u origin claude/replay-valid7-w3 && break; sleep $d; d=$((d*2)); done
