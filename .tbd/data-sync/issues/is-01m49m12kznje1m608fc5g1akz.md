---
type: is
id: is-01m49m12kznje1m608fc5g1akz
title: "Register builder: devtools.build_exact_values -> frontier/exact-values.json with exact checks"
kind: task
status: open
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
labels:
  - packing
dependencies:
  - type: blocks
    target: is-01m49m137apdxtdrpp6n5g74r8
  - type: blocks
    target: is-01m49m13z0csh9tpmfw82d1vse
  - type: blocks
    target: is-01m49m15ctm6vtvqj8pmk3mkkb
  - type: blocks
    target: is-01m49m1v8q316etk1g7kkr3hsq
  - type: blocks
    target: is-01m49m1xf6rk0b5nms5bgarbp8
  - type: blocks
    target: is-01m49m1z4zbjx4cft07yzzgvh2
parent_id: is-01m49m0enx3qf7mm1kyrra0z10
created_at: 2026-10-06T22:05:59.294Z
updated_at: 2026-10-06T22:06:28.510Z
---
Per n=1..324: side, lower, status, exact form, primitive integer polynomial, degree, algebraic_source; checks: irreducibility certificate (factorization or mod-p degree-pattern primes), rational isolating interval with exactly one root containing the recorded side, digits of agreement with Daniel's S_exact (resources/web/evand-square-packing-2026-10-05 batch/results.json.gz), Galois group and solvability for degree<=6; notes for superseded catalogue polynomials (102,106,123,130,172,177,199,206,228,259,269,292,302), n=83 missing text, numeric-only route + owning bead. --update/--check. Tests with negative controls: reducible polynomial, wrong root, perturbed coefficient, superseded polynomial. Spec component 3.
