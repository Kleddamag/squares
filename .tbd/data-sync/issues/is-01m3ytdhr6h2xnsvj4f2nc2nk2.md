---
type: is
id: is-01m3ytdhr6h2xnsvj4f2nc2nk2
title: "Import squarepacker: s(12) >= 31360/7901, Daniel's s(12) certificate rescaled by 7902/7901 (#309)"
kind: task
status: in_progress
priority: 1
version: 2
labels:
  - result-import
  - packing
dependencies: []
parent_id: is-01m3yrdxte02c7bnygkke34ct4
created_at: 2026-10-02T17:26:00.710Z
updated_at: 2026-10-02T17:26:06.287Z
---
Result import process, stages 1-4, lane AA. jlevy/squares#309 (squarepacker, Ryu Sungjoon, opened 2026-10-02) reports s(12) >= 31360/7901 = 3.96911783..., Evan Daniel's 1,736-point weighted certificate s12_lower_3.9686.txt (T-049, evand/square-packing at 7d6f46d) with every coordinate and the container multiplied by 7902/7901, weights unchanged (total 11.9738036 < 12), verified by Daniel's Rust verifier at N = 24000 (rejected at 6000 and 12000) and by the reporter's tools/indep_check.cpp. Source: github.com/squarepacker/s12-lower-bound; Zenodo 10.5281/zenodo.23106582; certificate sha256 6ad9b0e8...7578. Plan: retain the repository at a pinned commit (devtools.acquire_source), exact preflight against Daniel's retained certificate, the angle-net argument, replays (Daniel's verify at N = 24000, indep_check.cpp at 24000, the native parent-core checker if it decides this shape), two mutated controls per checker, review docs/project/reviews/review-2026-10-02-s12-rescaled-certificate.md, handoff of register and evidence entries to the records lane. Answer bead: think-5mkr.
