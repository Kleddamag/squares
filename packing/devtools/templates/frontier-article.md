<div class="site-hero">

# The Frontier Survey

<p class="subtitle">A survey of everything known for cases {{CASE_RANGE}}</p>

</div>

For each number $n$ of unit squares, $s(n)$ is the side of the smallest square that
holds them without overlap.
This page lists all {{COUNT}} cases the project tracks: {{PROVED}} have a proved optimum
and {{OPEN}} are open.
Every row is read from the case’s record, `packing/frontier/n-NNN.md`, when the page is
built; nothing on it is typed by hand.
For how the results fit together, start at the [overview](./).

**Reported and verified.** The *best known packing* and the *reported lower* bound are
what the published sources say, credited to whoever found or proved them.
The *verified* columns hold only exact formal bounds: a complete proof, an exact
algebraic replay, or a rigorous certificate.
Where the verified bound is the reported one, the cell says so rather than printing the
value twice.
A finite-precision result is numerically checked and never enters a verified
column.

**The other columns.** The *gap* is the verified upper bound minus the verified lower
bound, exact where both are closed forms and zero where the case is solved.
A star marks a recent result: one of the {{RECENT}} verified lower bounds proved since
{{RECENT_SINCE}}. *Records* links each case file.
Values that are roots of a polynomial are shown as decimals, cut rather than rounded.

**A row’s details.** Open a row for how its packing was built, the polynomial behind a
decimal, the sources, how its bounds were verified and the evidence entries behind them.
A case’s *n* opens its full record.

The same table, as Markdown with full provenance, is
[`frontier/STATUS.md`]({{STATUS_URL}}). Click a column heading to sort; the filters
narrow the rows.

{{TABLE}}
