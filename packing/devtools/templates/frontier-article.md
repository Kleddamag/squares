<!--
The frontier atlas page's article, rendered by devtools.site_pages through kpress in
trusted mode. Placeholders in double braces are filled from the case records before
parsing, so no bound and no count is written here as a literal, and the table takes the
place of its own placeholder after parsing. The design system is in site-design.md.
-->

# The Frontier Atlas

One row for each case from $n = {{FIRST_N}}$ to $n = {{LAST_N}}$: the best known packing
of $n$ unit squares in a square, and the bounds on $s(n)$, the side of the smallest
square that holds them.
Every value is read from the case’s record in [`packing/frontier/`]({{FRONTIER_URL}})
and validated against the record’s schema when the page is built; none is typed by hand.

Of the {{CASE_COUNT}} cases, {{PROVED_COUNT}} are proved and {{OPEN_COUNT}} are open.
A star marks the {{RECENT_COUNT}} whose lower bound is a recent result, one dated on or
after {{RECENT_SINCE}}, as on the atlas figure.

**How to read a row.** The reported columns keep what the published sources say.
The verified columns hold only exact formal bounds: a complete proof, an exact algebraic
replay, or a rigorous certificate.
A finite-precision result is numerically checked and does not enter a verified column,
however small its tolerance ([`epistemics.md`]({{EPISTEMICS_URL}}) defines the terms).

- Where a report agrees with the verified bound at the precision it declares, the value
  is printed once, in the verified column, and the report is marked verified.
- A lower bound reads $s(n) \ge$ its value, or $s(n) >$ its value where a register entry
  citing its evidence claims the strict inequality, as for {{STRICT_COUNT}} cases.
- Exact values are set as mathematics.
  Decimals are cut, never rounded, and an ellipsis marks digits that continue.
- The bound gap is the verified upper bound minus the verified lower bound, computed
  exactly where both are exact.
- Each row’s details list the evidence behind its bounds, each linked to its entry in
  [`evidence.yaml`]({{EVIDENCE_URL}}), and the minimal polynomial of an algebraic side.

{{FRONTIER_TABLE}}
