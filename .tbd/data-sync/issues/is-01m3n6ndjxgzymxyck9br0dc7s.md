---
type: is
id: is-01m3n6ndjxgzymxyck9br0dc7s
title: "Replay evand's Lean builds: s(13) = 4 and s(32) = 6 reported kernel-checked with no hypothesis (a V5 candidate), s(21)'s reduction, and the small s(11)/s(12) bounds"
kind: task
status: open
priority: 2
version: 1
labels:
  - packing
  - wand125-update
  - low-n
dependencies: []
parent_id: is-01m3n5wh72rsqd2z97m8v1vv4q
created_at: 2026-09-28T23:47:37.180Z
updated_at: 2026-09-28T23:47:37.180Z
---
evand/square-packing at 6aa82ba reports s(13) = 4 and s(32) = 6 kernel-checked hypothesis-free (commits 6e1223c, 92cc5bb: a generic box-tree verifier ZMTree in Lean), s(21) = 5 reduced in Lean to the zm_mixed D4 checker statement, and s(12) >= 35/9, 3920/997 and s(11) >= 3040/797 kernel-checked. epistemics.md's V5 is 'proof-assistant checked': building the Lean project here (elan, Mathlib cache or a full build) and running lake env lean Axioms.lean would support V5 for s(13) and s(32) if the statements are the standard ones. Decide after Session 161's Lane 2 reports whether the toolchain and Mathlib cache are reachable from this environment.
