---
title: H-275 — the per-state price of n17 residue states in the strata H-264's draw never reached
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-275
  kind: open_question
  claim: >-
    On a seeded draw of one residue state from each of the 21 strata of
    survey_n17_residue's arity8 frame that H-264's seed-182 draw never reached (827 of the
    frame's 2,255 non-endpoint orbits), two where a stratum holds more orbits than the
    mean of those strata, what fraction does the 17-owner kernel under SW9's frozen
    adaptive-row recipe exclude by a certificate the standing kernel verifier re-proves in
    full, and at what producer, checker and verifier cost per state?
  lane: proof
  derived_from: [X-048]
  instrument: >-
    devtools.check_n17_subpattern --cells CELLS17 --bins 64 --max-rounds 24 --hull-limit
    16 --producer-share 0.6 --split-floor 512 --max-rows 1152 --split-patience 1
    --max-seconds 7000, from the clean run worktree at the session-182 registration commit
    cebb5d15a; closures re-proved by devtools.verify_n17_kernel_certificate in full mode
    under the kernel-streamed listing. The recipe is the one BC-424's endpoint-state
    control passed on the whole endpoint state (PASS_CERTIFIED_STALL at its 24-round cap)
    and lane K's endpoint7 control passed on its west-wall cells.
  instrument_ready: true
  regime: >-
    n=17; the H-266 unique-state cover at U = 1169/250; the 31 states frozen in
    packing/campaign/explorations/X048-session-182-overnight/kernel-targets-bc428.txt,
    one run each, in the frozen run order on two workers, until the run operator's
    deadline at 2026-10-06T07:14:04Z. The draw is numpy's default_rng(428) over the
    unsampled strata in name order, with the run order a permutation from the same
    generator and every stratum's first draw before any second; the command is
    receipts/U/draw-bc428.cmd.txt. The two distance-2 draws are a secondary stratum,
    reported separately as H-264 does, because such a state may be feasible at U. States
    not run by the deadline are reported as not run, not extrapolated.
  instance: {axis: n, point: 17}
  priority: 2
  cost_estimate: At most 7,000 s per state and 4,000 s per verification; about 9 hours on two workers
  prereqs: [H-264, H-266, H-274]
  replication: false
  registered: '2026-10-05'
  notes: >-
    Registered by Session 182 (BC-428) at the coordinator's re-plan after BC-427. A new
    hypothesis rather than a follow-on experiment under H-264, because H-264's claim fixes
    both its draw (--sample 12 --seed 182) and its instrument (N1's 32 uniform bins), and
    its regime reports the unreached strata as unsampled rather than extending to them.
    This question changes both: the states come from those strata, and the recipe is the
    adaptive-row one under which all four of H-264's counted stalls closed (H-274). The
    answer prices the tail H-264 left unpriced. Strata of 39 or fewer orbits get one draw,
    so their shares rest on one state each and describe the draws, not a closure rate.
---
# H-275: The Per-State Price in H-264’s Unsampled Strata

H-264 priced per-state exclusion on twelve draws that reached ten of the arity8 frame’s
31 non-endpoint strata, and reported the other 21, 827 orbits, as unsampled.
H-274 then closed all four of H-264’s counted stalls under the adaptive-row recipe.
This question draws from the strata H-264 never reached and runs them under that recipe,
so the residue tail has a measured price where it had none.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
