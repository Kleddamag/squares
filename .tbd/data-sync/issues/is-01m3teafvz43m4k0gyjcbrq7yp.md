---
type: is
id: is-01m3teafvz43m4k0gyjcbrq7yp
title: "Review the verification and confirmation ladders: the top rung is reproducible formal verification plus expert human review and confirmation"
kind: task
status: in_progress
priority: 1
version: 5
labels: []
dependencies: []
created_at: 2026-10-01T00:37:39.747Z
updated_at: 2026-10-01T00:45:10.469Z
---
Owner, 2026-09-30: 'We need to review the confirmation and verification ladder rungs. The absolute highest confirmation level should be reproducible formal verification plus expert human review and confirmation of the proof and the formal verification. This should be C5 or perhaps C6. V5 would be formal verification plus human review that hasn't been externally confirmed from this project or other additional sources.' Deliver a proposal, not a change: the current V0-V5 and C0-C5 predicates from epistemics.md and what check_results derives; the owner's proposed top rungs made precise (what counts as formal verification, reproducible, expert human review, external confirmation; where AI review sits); two or three candidate ladders (redefine within six rungs, or add C6); the re-derived rungs of all registered results under each, with every change listed (T-060 is C5 today on a same-project AI-assisted review; T-006 is V5/C3 on jlevy/squares#249 by a Lean kernel check; T-037; T-051); the migration (epistemics.md, check_results, results.yaml, RESULTS/STATUS, the site's rung cards, README/SYNOPSIS copies of the rubric); and the decisions the owner must make. Related: think-7khl (does a recorded execution satisfy V4's replay predicate), think-yf6t (does a same-project review of another author's certificate earn C5). Workflow W4 process review. No edit to epistemics.md, check_results or any rating until the owner approves.

## Notes

Owner, 2026-09-30, added: delegate a sub-agent on this; it can be a stacked PR proposing the epistemics changes and enforcing the levels on the data, including n = 11 optimality. The n = 11 result should not be at the highest V or C, since neither is formal, though both are mechanized and confirmed: second-highest rung for V and C. Decide levels consistent with what has been done and with what is wanted in future; clarify what C4, C5 and a possible C6 mean. Today: V5 proof-assistant checked is the top V and T-060 is V4, already second-highest; C5 review-ready is the top C and T-060 is C5, so C must change. Plan: proposal document on claude/epistemics-ladder-review, then a draft implementation on claude/epistemics-ladder stacked on jlevy/squares#255.

Owner's preferred design, 2026-09-30: 'Ideally V5 and C5 would be reserved for formal verification, but not as a blind checklist; it must also have gone through human expert review on the formalization. V4 and C4 would be mechanized verification or highly formal verification of some form, possibly not fully human reviewed, but should have extensive AI review at a minimum, from multiple adversarial attempts with AI and best models confirming it.' So no C6: the tops stay at 5 and are redefined; T-060 lands at V4/C4. Register on main at the time: V5 0, V4 50, C5 8 (T-014, T-018, T-022, T-025, T-026, T-034, T-035, T-060), C4 14; jlevy/squares#249 would add T-006 at V5/C3 by a Lean kernel check.

Owner principle, 2026-09-30: 'In no case do we blindly trust any formal reasoning system or any agent. For V4 and C4, some human oversight of the mechanization and AI checking is needed with credible documentation and human review.' So rung 4 needs mechanized or highly formal verification, extensive adversarial AI review, and a retained, auditable human-oversight record; rung 5 needs formal verification and human expert review of the formalization. Results without a recorded human oversight drop below 4 until one exists; the proposal lists each.
