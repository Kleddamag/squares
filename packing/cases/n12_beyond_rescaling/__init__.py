"""A weighted point certificate for s(12) >= 15680000/3949423 = 3.9702002...

Evan Daniel's 1,736 points (s12_lower_3.9686.txt), scaled by 3951000/3949423, with weights
re-solved here by linear programming (`devtools.s12_reweight`). Decided at N = 96000 by
the source's own verifier, built from the retained packet with overflow checks
(`receipts/route-b-source-verifier.json`). `rescaled-certificate.txt.gz` is the
whole-certificate rescaling, after jlevy/squares#309, for s(12) >= 1568000/395039.
`claim.json` states both; the write-up is
docs/project/research/research-2026-10-02-s12-beyond-rescaling.md.
"""
