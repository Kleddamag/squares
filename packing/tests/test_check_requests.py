"""The result requests record joins each issue to the register; the tool says what each is owed.

`devtools.check_requests` derives each reported result's state, whether a reply is due
and whether the issue can be closed from `campaign/result-requests.yaml` and the
register, and stores none of it. These hold the live record to its schema and ids, each
derivation to a synthetic register, the draft to its footer and its refusal off `main`,
and the GitHub comparison to a recorded fetch.
"""

from __future__ import annotations

import copy
from collections.abc import Mapping
from typing import Any

import pytest

from devtools import check_requests
from devtools.check_requests import (
    CONFIRMED,
    DEFECT,
    FOOTER,
    OPEN,
    QUEUED,
    REFUTED,
    Register,
)

Record = dict[str, Any]
URL = "https://github.com/owner/repo/issues/7#issuecomment-{}"


def result_entry(
    rid: str, verification: str, confirmation: str, *evidence: str, **more: Any
) -> Record:
    return {
        "id": rid,
        "verification": verification,
        "confirmation": confirmation,
        "evidence": list(evidence),
        "next_rung": f"{rid}'s next rung (think-abcd).",
        **more,
    }


REGISTER = Register(
    results={
        "T-001": result_entry("T-001", "V3", "C3", "E-replay"),
        "T-002": result_entry("T-002", "V0", "C1", "E-report"),
        "T-003": result_entry("T-003", "V3", "C1", "E-defect"),
        "T-004": result_entry(
            "T-004",
            "V3",
            "C3",
            "E-replay",
            reviews=[{"path": "docs/r.md", "date": "2026-10-01", "verdict": "refuted"}],
        ),
        "T-005": result_entry(
            "T-005",
            "V0",
            "C0",
            "E-report",
            activity={
                "state": "in-analysis",
                "what": "a replay",
                "since": "2026-10-01",
                "link": "think-abcd",
            },
        ),
    },
    evidence={
        "E-report": {
            "origin": "external",
            "assurance": "reported",
            "replay_status": "not-attempted",
        },
        "E-replay": {
            "origin": "replayed-here",
            "assurance": "verified",
            "replay_status": "passed",
            "verifier_relation": "producer-code",
            "verifier_program": "zmx2",
        },
        "E-defect": {
            "origin": "external",
            "assurance": "verified",
            "external_review": {"state": "defect-found", "date": "2026-10-01"},
        },
    },
)


def issue(**over: Any) -> Record:
    base: Record = {
        "number": 7,
        "title": "A request",
        "author": "someone",
        "opened": "2026-10-01",
        "state": "open",
        "kind": "result-report",
        "triage": "done",
        "summary": "It reports a bound.",
        "read_through": "2026-10-01T00:00:00Z",
        "results": [{"key": "bound", "claim": "s(9) >= 3", "register": ["T-001"]}],
        "beads": ["think-abcd"],
        "answer_bead": "think-efgh",
        "replies": [],
        "close_when": "T-001 is confirmed.",
    }
    base.update(over)
    return base


def record(*issues: Record) -> Record:
    return {
        "softschema": {
            "contract": "packing.squares:ResultRequests/v1",
            "schema": "schemas/result-requests.schema.yaml",
            "status": "enforced",
        },
        "repository": "owner/repo",
        "owner": "owner",
        "last_reviewed": "2026-10-02",
        "issues": list(issues) or [issue()],
    }


def reply(number: int, date: str = "2026-10-02", **over: Any) -> Record:
    return {
        "url": URL.format(number),
        "date": date,
        "by": "owner",
        "kind": "import",
        "reported": [],
        **over,
    }


def test_the_live_record_holds_its_schema_and_every_id_it_names_exists(
    capsys: pytest.CaptureFixture[str],
) -> None:
    live = check_requests.load_record()
    assert check_requests.problems(live, check_requests.load_register()) == []
    assert check_requests.main([]) == 0
    assert "every id resolves" in capsys.readouterr().out


def test_the_live_record_has_one_entry_an_issue_and_names_its_answer_bead() -> None:
    live = check_requests.load_record()
    numbers = [entry["number"] for entry in live["issues"]]
    assert len(numbers) == len(set(numbers))
    assert {170, 227, 238, 247, 256, 279, 280, 281, 282, 294, 295, 296, 308} <= set(numbers)
    assert all(entry["answer_bead"].startswith("think-") for entry in live["issues"])


@pytest.mark.parametrize(
    ("mutate", "expected"),
    [
        (
            lambda r: r["issues"][0]["results"][0].update(register=["T-999"]),
            "T-999 is not in results.yaml",
        ),
        (
            lambda r: r["issues"][0]["results"][0].update(evidence=["E-none"]),
            "E-none is not in evidence.yaml",
        ),
        (
            lambda r: r["issues"][0]["replies"].append(
                reply(1) | {"url": "https://github.com/owner/repo/issues/8#issuecomment-1"}
            ),
            "is not a comment on this issue",
        ),
        (
            lambda r: r["issues"][0]["replies"].append(
                reply(1, reported=[{"result": "bound", "id": "T-002"}])
            ),
            "record a renumbered id as `as`",
        ),
        (
            lambda r: r["issues"][0]["replies"].append(
                reply(1, reported=[{"result": "other"}])
            ),
            "unknown result 'other'",
        ),
        (
            lambda r: r["issues"][0]["replies"].extend(
                [reply(1, "2026-10-03"), reply(2, "2026-10-02")]
            ),
            "dated before the one above it",
        ),
        (
            lambda r: r["issues"][0]["replies"].append(reply(1, corrects=[URL.format(9)])),
            "which is not an earlier reply here",
        ),
        (
            lambda r: r["issues"].append(copy.deepcopy(r["issues"][0])),
            "issue #7 is recorded twice",
        ),
        (lambda r: r["issues"][0].update(state="closed"), "closed"),
        (lambda r: r["issues"][0].update(answer_bead="other-1234"), "answer_bead"),
    ],
)
def test_the_check_refuses_an_unknown_id_a_misplaced_reply_and_a_broken_schema(
    mutate: Any, expected: str
) -> None:
    broken = record(issue())
    mutate(broken)
    found = check_requests.problems(broken, REGISTER)
    assert any(expected in problem for problem in found), found


def test_a_result_is_confirmed_at_v3_c3_and_open_below_it() -> None:
    confirmed = check_requests.result_state(
        {"key": "a", "claim": "c", "register": ["T-001"]}, REGISTER
    )
    assert (confirmed.state, confirmed.settled) == (CONFIRMED, True)
    reviewed = check_requests.result_state(
        {"key": "a", "claim": "c", "register": ["T-002"]}, REGISTER
    )
    assert (reviewed.state, reviewed.settled) == (OPEN, False)
    both = check_requests.result_state(
        {"key": "a", "claim": "c", "register": ["T-001", "T-002"]}, REGISTER
    )
    assert both.state == OPEN


def test_a_defect_or_refutation_decides_a_result_and_settles_only_a_refutation() -> None:
    defect = check_requests.result_state(
        {"key": "a", "claim": "c", "register": ["T-003"]}, REGISTER
    )
    assert (defect.state, defect.settled) == (DEFECT, False)
    refuted = check_requests.result_state(
        {"key": "a", "claim": "c", "register": ["T-004"]}, REGISTER
    )
    assert (refuted.state, refuted.settled) == (REFUTED, True)


def test_a_reported_defect_is_settled_when_the_record_holds_it() -> None:
    held = {"key": "a", "claim": "c", "evidence": ["E-defect"], "defect": True}
    assert check_requests.result_state(held, REGISTER).settled
    unheld = {"key": "a", "claim": "c", "register": ["T-002"], "defect": True}
    assert not check_requests.result_state(unheld, REGISTER).settled


def test_a_report_entry_beside_a_confirmed_register_entry_does_not_hold_it_open() -> None:
    beside = {"key": "a", "claim": "c", "register": ["T-001"], "evidence": ["E-report"]}
    assert check_requests.result_state(beside, REGISTER).state == CONFIRMED
    evidence_only = {"key": "a", "claim": "c", "evidence": ["E-replay"]}
    assert check_requests.result_state(evidence_only, REGISTER).state == CONFIRMED


def test_a_result_not_registered_is_settled_unless_it_is_queued() -> None:
    queued = {"key": "a", "claim": "c", "not_registered": "later", "queued": True}
    assert (
        check_requests.result_state(queued, REGISTER).state,
        check_requests.result_state(queued, REGISTER).settled,
    ) == (QUEUED, False)
    declined = {"key": "a", "claim": "c", "not_registered": "below the bound", "queued": False}
    assert check_requests.result_state(declined, REGISTER).settled


def due(entry: Record) -> list[str]:
    return list(check_requests.issue_state(entry, REGISTER).replies_due)


def test_an_issue_with_no_reply_is_owed_an_acknowledgement_and_the_import() -> None:
    reasons = due(issue())
    assert reasons[0].startswith("an acknowledgement")
    assert any(
        "T-001 at V3/C3" in reason and "no reply has said so" in reason for reason in reasons
    )


def test_a_pending_triage_is_owed_only_the_acknowledgement() -> None:
    assert due(issue(triage="pending", results=[])) == [
        "an acknowledgement, once triage has mapped the claims"
    ]


def test_a_reply_that_states_the_current_state_leaves_nothing_due() -> None:
    said = [
        {
            "result": "bound",
            "id": "T-001",
            "verification": "V3",
            "confirmation": "C3",
            "status": "confirmed",
        }
    ]
    assert due(issue(replies=[reply(1, reported=said)])) == []


def test_a_moved_rung_a_renumbered_id_and_an_unnamed_entry_are_each_due() -> None:
    said = [
        {
            "result": "bound",
            "id": "T-001",
            "as": "T-058",
            "verification": "V4",
            "confirmation": "C4",
        }
    ]
    reasons = due(issue(replies=[reply(1, reported=said)]))
    assert any("named T-001 as T-058" in reason for reason in reasons)
    assert any("stated T-001 at V4/C4; it is now V3/C3" in reason for reason in reasons)
    acknowledged = due(issue(replies=[reply(1, reported=[{"result": "bound"}])]))
    assert acknowledged == ["bound: T-001 at V3/C3: confirmed since the reply of 2026-10-02"]


def test_an_outdated_statement_is_due_until_a_later_reply_corrects_it() -> None:
    said = [{"result": "bound", "id": "T-001", "verification": "V3", "confirmation": "C3"}]
    first = reply(1, "2026-10-01", reported=said, outdated=["a link into a branch"])
    assert due(issue(replies=[first])) == [
        "a follow-up: the reply of 2026-10-01 said a link into a branch"
    ]
    unrelated = reply(2, "2026-10-02")
    assert len(due(issue(replies=[first, unrelated]))) == 1
    fixed = reply(2, "2026-10-02", corrects=[URL.format(1)])
    assert due(issue(replies=[first, fixed])) == []


def test_closeable_needs_every_result_settled_triage_done_and_no_ask_queued() -> None:
    assert check_requests.issue_state(issue(), REGISTER).closeable
    asked = issue(asks=[{"what": "change the text", "state": "queued"}])
    state = check_requests.issue_state(asked, REGISTER)
    assert not state.closeable
    assert state.blockers == ("asked: change the text",)
    assert not check_requests.issue_state(issue(triage="pending"), REGISTER).closeable
    open_result = issue(results=[{"key": "b", "claim": "c", "register": ["T-002"]}])
    assert check_requests.issue_state(open_result, REGISTER).blockers == ("b is open",)


@pytest.mark.parametrize(
    ("relation", "expected"),
    [
        (
            {"verifier_relation": "producer-code", "verifier_program": "zmx2"},
            "reproduced here with the author's own checker (zmx2)",
        ),
        (
            {"verifier_relation": "independent-implementation", "verifier_program": "sqpack"},
            "re-verified here by an independent implementation (sqpack)",
        ),
        (
            {
                "verifier_relation": {
                    "relation": "shared-components",
                    "components": ["the point test"],
                }
            },
            "re-verified by code sharing the point test with the author's",
        ),
        (
            {"verifier_relation": "producer-code", "origin": "independently-external"},
            "reproduced by a third party with the author's own checker",
        ),
    ],
)
def test_a_confirmation_says_whose_code_reproduced_it(
    relation: Mapping[str, Any], expected: str
) -> None:
    assert check_requests.verifier_phrase({"origin": "replayed-here", **relation}) == expected


def test_a_confirmation_without_the_relation_says_it_is_not_yet_recorded() -> None:
    bare = Register(
        results={"T-001": result_entry("T-001", "V3", "C3", "E-bare")},
        evidence={"E-bare": {"origin": "replayed-here", "replay_status": "passed"}},
    )
    assert (
        check_requests.entry_state("T-001", bare).how
        == "how it was re-verified is not yet recorded"
    )
    assert "not yet recorded" in check_requests.draft(issue(), bare, "owner/repo")


def test_the_draft_states_each_result_links_main_and_ends_in_the_footer() -> None:
    entry = issue(
        results=[
            {"key": "bound", "claim": "s(9) >= 3", "register": ["T-001"]},
            {"key": "open", "claim": "s(10) >= 3", "register": ["T-005"]},
            {
                "key": "later",
                "claim": "s(11) >= 3",
                "not_registered": "Queued for import.",
                "queued": True,
            },
        ]
    )
    text = check_requests.draft(entry, REGISTER, "owner/repo")
    assert text.endswith(FOOTER)
    assert (
        "T-001, confirmed, at V3/C3: reproduced here with the author's own checker (zmx2)."
        in text
    )
    assert "registered as reported" in text
    assert "Under way here since 2026-10-01: a replay" in text
    assert "T-005: T-005's next rung." in text, "bead ids are this project's and are left out"
    assert "https://github.com/owner/repo/blob/main/packing/frontier/RESULTS.md" in text
    assert "stays open" in text
    closing = check_requests.draft(issue(), REGISTER, "owner/repo")
    assert "closed with this comment" in closing


def test_the_draft_refuses_off_main(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    live = check_requests.load_record()
    number = str(live["issues"][0]["number"])
    monkeypatch.setattr(check_requests, "head_on_main", lambda: False)
    assert check_requests.main(["--draft", number]) == 2
    assert "refusing to draft" in capsys.readouterr().err
    monkeypatch.setattr(check_requests, "head_on_main", lambda: True)
    assert check_requests.main(["--draft", number]) == 0
    assert capsys.readouterr().out.rstrip().endswith(FOOTER)
    assert check_requests.main(["--draft", "1"]) == 2


def comment(number: int, login: str, created: str, body: str = "thanks") -> Record:
    return {
        "html_url": URL.format(number),
        "user": {"login": login},
        "created_at": created,
        "body": body,
    }


def test_the_github_comparison_lists_missing_replies_unread_comments_and_unknown_issues() -> (
    None
):
    recorded = record(
        issue(replies=[reply(1, "2026-10-01")], read_through="2026-10-01T12:00:00Z")
    )
    live = {
        "repos/owner/repo/issues?state=all&per_page=100": [
            {"number": 7, "state": "open", "title": "A request"},
            {"number": 8, "state": "open", "title": "Another"},
            {"number": 9, "state": "open", "title": "A pull request", "pull_request": {}},
        ],
        "repos/owner/repo/issues/7/comments?per_page=100": [
            comment(1, "owner", "2026-10-01T10:00:00Z"),
            comment(2, "owner", "2026-10-02T10:00:00Z"),
            comment(3, "agent", "2026-10-02T11:00:00Z", f"text\n\n{FOOTER}\n"),
            comment(4, "someone", "2026-10-02T12:00:00Z", f"the author's own\n\n{FOOTER}"),
            comment(5, "someone", "2026-09-30T12:00:00Z"),
        ],
    }
    differences = check_requests.compare_github(recorded, live.__getitem__)
    assert differences == [
        "#8 is not in the record: Another",
        f"#7: reply missing from the record: {URL.format(2)} (owner, 2026-10-02)",
        f"#7: reply missing from the record: {URL.format(3)} (agent, 2026-10-02)",
        f"#7: unread comment {URL.format(4)} (someone, 2026-10-02T12:00:00Z)",
    ]


def test_the_backlog_lists_every_entry_below_v3_or_c3_with_its_beads_and_issues() -> None:
    lines = check_requests.backlog(
        record(issue(results=[{"key": "a", "claim": "c", "register": ["T-002"]}])), REGISTER
    )
    rows = [line for line in lines if line.startswith("| T-")]
    assert [row.split(" | ")[0] for row in rows] == ["| T-002", "| T-003", "| T-005"]
    assert "think-abcd" in rows[0]
    assert "#7" in rows[0]
    assert "in analysis since 2026-10-01" in rows[2]


def test_the_live_backlog_and_report_render() -> None:
    live = check_requests.load_record()
    register = check_requests.load_register()
    backlog = "\n".join(check_requests.backlog(live, register))
    below = [
        rid
        for rid, entry in register.results.items()
        if int(entry["verification"][1]) < 3 or int(entry["confirmation"][1]) < 3
    ]
    assert all(f"| {rid} |" in backlog for rid in below)
    report = check_requests.report(live, register, None)
    assert report[0] == "# Result Requests"
    assert sum(line.startswith("## #") for line in report) == len(live["issues"])
