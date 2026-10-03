---
id: H-007
title: Branch-free directed rounding halves the search
registered: "2026-10-02T19:44Z"
metric: search instructions over the three callgrind cells
direction: lower
criterion: accept rule of the campaign README
---
# Branch-Free Directed Rounding

In H-006’s profile the inlined bodies of `f64::next_up` and `next_down` (sign, NaN and
infinity tests, then integer arithmetic on the bit pattern) were three quarters of the
edge-length enclosure.
Stepping outward by adding $\mathrm{fl}(|x| 2^{-52}) + 2^{-1074}$ instead is three
floating-point operations with no branch, and lemma I1 shows it still reaches the
adjacent binary64 value.

Prediction: identical node counts (the bounds move by a few units in the last place),
and 30 to 50% fewer search instructions.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
