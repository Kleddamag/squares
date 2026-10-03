---
type: is
id: is-01m41d7mmrmyb877fgfqpq2ve3
title: "Results table: fit the significance column in the 1280 width budget"
kind: task
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m41d7edgm9wc99zdrkaa5ehy
created_at: 2026-10-03T17:33:18.872Z
updated_at: 2026-10-03T22:59:12.577Z
---
Adding the S column put the table 111px past its 1200px frame at 1280 (floors: S 121, result 288). Win the room back by measurement (a compact mark; the result column's floor to its widest formula piece, 248.5px) and update the column tests' pinned widths.

## Notes

Resumed after the sub-agent stopped at a usage limit with its work committed (be33790fe, 3b8974b82). After #315's second merge with main, two results' tenth evidence links set the details column 6.3px wider and the floors 4.3 past 1200 at 1280; the result floor went to 16.55rem and the S padding to 0.2rem, floors 1197.9, 2.1 to spare (577ccf2cd).
