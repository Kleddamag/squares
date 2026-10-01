---
type: is
id: is-01m3v3enx1t8say9qddw19n0s2
title: "Reader-facing text: drop commit hashes, clocks and other certification ceremony; keep credit and a link to the source"
kind: task
status: in_progress
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-10-01T06:46:57.176Z
updated_at: 2026-10-01T06:46:58.774Z
---
Owner, 2026-10-01: 'Drop verbose nonsense like "certified at commit c8b36419 on 26 September 2026 by the author's clock:". The point is not certifying timezones or commits, it is proper credit and having a link to the appropriate sources. Hashes can be recorded at the point of ingestion but should not appear in text. Look for more examples of this kind of needless ceremony and clean them up.' A separate PR, delegated, not blocking the website work. Rule: reader-facing prose (register claims, headlines and credit lines, case-file prose, README, TUTORIAL, SYNOPSIS, site templates and the pages they render) says who established what and when, with a link to the source; commit hashes, digests, clock and timezone qualifiers and similar provenance mechanics live in structured fields recorded at ingestion (evidence and packet records), never in sentences. Before removing a hash from prose, confirm it is retained in a structured field, and add it there if prose was its only home. Archived sources, dated reviews and session records are historical and are not rewritten.
