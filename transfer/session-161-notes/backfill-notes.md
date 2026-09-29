# Backfill Notes: Others’ Results in the Register

Draft for `think-z9wy`, 2026-09-29. `backfill.yaml` holds 19 new entries, `T-037` to
`T-055`, in the order requested, and attribution blocks for `T-004`, `T-008`, `T-011`,
`T-015`, `T-016` and `T-032`. Nothing in the checkout was edited.

The plan's prose says 21 new entries, 57 in all and 27 of them others'. Its own table
has 19 rows. With this draft the register would hold 55 entries, 22 of them others'.

HEAD moved from `901dbc59` to `c7ee598d` while this was drafted, because another lane
committed to the branch. `evidence.yaml`, `results.yaml` and the case frontmatter are
unchanged between the two. The bibliography now carries credit lines for Kleddamag
`v1.0.0`, R052 and R012 that name this project. The working tree also has an
uncommitted `release.py` edit that belongs to that other lane.

## Validation

Scripts are in `../backfill-tools/`: `validate_backfill.py`, with its output in
`validation-output.json`, and `coverage_before.py`. Both run under
`packing/.venv/bin/python3`.

- **`check_results.main()`** ran over `results.yaml` plus the 19 drafts, with
  `attribution` removed. It exits 0 with 55 results. Every evidence id resolves, every
  artifact, control and `produced_by` path or id resolves, every rung passes, and the
  ids are contiguous.
- **The v1 schema** accepts every stripped draft entry.
- **Attribution** has four problems, all in the retrofits:
  - `[Ellsworth SVG]` (`T-011`) is missing from `bibliography.yaml`.
  - `[Burns–Massaccesi n17]` (`T-015`, `T-016`) is missing from `bibliography.yaml`.
  - `T-011` has `published: '1979'`, which is a year only. The packing was sent to
    Martin Gardner in 1979, according to Trump’s 2023 note, and no day is recorded.
  - `[Kingbird]` does resolve, but its credit is Friedman and Ellsworth, not Trump.
    `T-011` needs a bibliography entry for Trump’s packing and a ruling on whether a
    year-only date is allowed.
- **Derived rungs match the declared ones** except in five places, each covered by a
  `composition` note:
  - `T-052`, `T-053` and `T-054` derive `C4`, because the lower half is on zmx2
    (interval) and the grid is exact. Both are declared `C3`, since the two methods
    certify different halves. That is how `T-008` reads its own halves.
  - `T-055` derives `V4`/`C3` from the grid entry, but its lower half is reported only,
    so it is declared `V0`/`C0`.
  - `T-032` (existing) derives `C5` from its mapped `review_artifact` and declares `C4`.
    That is the precedent for declining a literal `C5`.
- **Rungs that differ from the plan table:**
  - `T-046` (the wand125 rectangle reports), `T-048` (`s(50)`) and `T-055`
    (point-only `s(21)`) derive `C0`, not the `C1` the plan expects. No cited report
    entry has an `external_review`.
  - The reviews that would make them `C1` already exist:
    `review-2026-09-27-wand125-rectangle-scaling`,
    `review-2026-09-28-wand125-n50-mixed-verifier` and
    `review-2026-09-28-wand125-point-only-s21-s45`. They are recorded on the replay
    entries or not recorded at all. Adding an `external_review` block to each report
    entry gives `C1`.

## Coverage Gap

**Before this draft** the proposed gate would flag 23 evidence ids. These are ids that a
case's reported or verified lower bound cites, whose source is dated on or after
2026-08-22, and that no entry cites. `coverage_before.py` lists each one and the draft
entry that closes it.

**After this draft** no such id is left.

Two ids from recent sources are cited by no entry and by no case field:

- `E-wand125-rectangle-monotone-report` is the superseded `s(77) ≥ 89/10` transfer. It
  was left out of `T-046` because it supports no current claim.
- `E-n013-evand-casefree-cover-report` is the plan's open question 2.

**Gaps in the gate as specified.** The gate reads `dated` from the bibliography, and
that fails in two ways:

- **Some sources have no `dated`.** Forty-nine case-field citations go to Göbel 1979,
  Kearney–Shiu 2002, Stromquist 2003, Bentz 2016 and Friedman DS7. By year they are
  old, but the gate needs a year fallback to know that.
- **Some sources are not in the bibliography at all.** The ones this repository cites
  are `[Friedman DS7]`, `[Burns–Massaccesi n17]`, `[Ellsworth SVG]`,
  `[GitHub n17 certificates 2026]`, `[MacIver 2026 n17]`, `[Kingbird n=5 SVG]`,
  `[Kingbird n=29 SVG]`, `[Schadt n=29 repository]` and `[T-017]`. Two of them are
  2026 sources: GitHub n17 and MacIver. The gate could not date either one if a field
  cited it.

## Judgement Calls

- **Scopes wider than the plan's labels:**
  - `T-044` adds `n = 26` and `n = 29`. These were replayed here, and Tokoharu
    superseded them on the day of intake, so they qualify under rule 2.
  - `T-047` adds `n = 27`, `28` and `31`. They held the verified field by transfer from
    22 to 27 September (checked at `63368dce^`).
  - `T-045` includes `n = 32` as asked, although the scope of
    `E-wand125-rectangle-source-replay` omits it. The replay receipt `rect_n32_L595` is
    retained, and the entry's composition note says so.
- **`n = 27` is in both `T-045` and `T-046`.** The case's reported field still cites
  the report entry, and its verified field cites the replay.
- **Equality entries cite `E-basic-grid-upper`,** following `T-008`. The alternative is
  to state the grid half in prose and drop it from the evidence. That would remove the
  `C4` and `V4` understatements above.
- **Significance scores:**
  - `T-037` is `S5`: movement on the central open case, and T-019 gave not being that
    case as its first reason for staying below `S5`. This departs from the convention in
    `T-015` and `T-032`, which scored external results `S3`. `S4` is the fallback.
  - `T-047` (Tokoharu) is `S4`, as a reusable technique that wand125 builds on.
  - `T-051`, `T-052` and `T-053` are `S4`, as exact values forming the `s(k² − 4) = k`
    family. `T-053` states the calibration exemption it relies on.
  - `T-042`, `T-054` and `T-055` are `S2`, as intermediates or second routes.
  - Every other entry is `S3`.
- **No entry has a `review_artifact`, so none reaches `C5`.** Every replayed entry has a
  mapped, non-superseded review in `document-map.yaml`, so under the literal predicate
  citing it would derive `C5` across the board. Whether a same-project review of
  another author's certificate qualifies is for the owner to decide. The case record at
  `n-011` explicitly declined `C5`.
- **Controls:**
  - No test under `packing/tests` reads the Kleddamag `v1.0.0` packet (`T-038`), so its
    control is the release's own `independent_controls.py`.
  - `T-040` and `T-041` also name the release's `controls.py`. The only test there,
    `test_retained_data.py`, checks compressed files only.
  - `T-044` names `test_fractional_certificate.py`, the verifier's own suite, because no
    test reads the wand125-points packet.
  - All three packets are candidates for new tests.
- **`published` dates** are the author's-clock commit dates as the sources and cases
  state them. `n-012` says s(12) “entered the source on 2026-08-25”. In UTC, four of
  them fall one day later: `T-049` 08-26, `T-050` 09-24, `T-051` 09-27 and `T-053`
  09-28.
- **Two entries use the bibliography's 2026-09-22 although earlier certificates may
  exist.** For `T-044`, wand125's README reads “Draft, 2026-09-14”, and every file
  except the `n53` and `n69` certificates existed at the earlier commit `8ec3d79`, which
  is undated here. `T-047` has the same issue.
- **`T-046` spans two revisions.** It uses 2026-09-27, the first key's date, although
  some certificates arrived on 26 September.
- **`T-015` and `T-016` use 2026-08-21,** the date header of Massaccesi's post
  (`massaccesi-lower-bound-4_5058.html:699`). That is one day before `RECENT_SINCE`, so
  they qualify under rule 3, not rule 2.
- **`produced_by`** names the intake session, following the precedent of `T-015` and
  `T-032`. `T-037` is given `session-152`, although the native `C4` decision ran in
  `session-153`.
- **`T-037`'s advance** is measured from `T-033`, which was on main at 18:46Z on 22
  September before the intake branch merged.

## Open for the Owner

1. Record the existing reviews as `external_review` on the three report entries, to
   reach the plan's `C1`.
2. Decide the `C5` policy for others' results.
3. Add bibliography entries for `[Burns–Massaccesi n17]` and for Trump 1979 or
   `[Ellsworth SVG]`, and decide the `T-011` date format.
4. **`T-051` (`s(32) = 6`) can reach `C4` now.** The complete zmx2
   `--d4 --pair-points` run on the same cover passed here on 2026-09-28. Its receipt is
   `evand-square-packing-2026-09-28/receipts/s32_zmx2_d4_pairpoints.log`, with 3,600
   roots and none uncertified. It needs an interval-certified evidence entry.
5. Before registering `T-048` and `T-055`, check whether the `s(50)` and point-only
   `s(21)` replays have finished. They were running when their evidence was written.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
