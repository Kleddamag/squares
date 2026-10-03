"""The n11 receipts register documents every receipt and matches what the receipts say."""

from devtools.inventory_n11_completion import FIXED
from devtools.render_n11_receipts_register import (
    ENTRIES,
    FAMILIES,
    REGISTER,
    TIERS,
    bindings,
    hashes_in,
    receipt_names,
    render,
    tier_contradictions,
)

# Curated tiers the derived bindings contradict, kept here by name so a new contradiction
# fails and a resolved one forces this list to shrink. Each awaits a reviewer's decision.
KNOWN_TIER_CONTRADICTIONS: dict[str, str] = {}


def test_every_receipt_has_a_curated_entry_and_every_entry_exists() -> None:
    on_disk = set(receipt_names())
    assert on_disk - set(ENTRIES) == set(), "undocumented receipts"
    assert set(ENTRIES) - on_disk == set(), "curated entries for missing receipts"


def test_curated_entries_are_well_formed() -> None:
    for name, entry in ENTRIES.items():
        assert entry.tier in TIERS, name
        assert entry.family in FAMILIES, name
        assert entry.purpose.endswith("."), name
        assert "{" not in entry.purpose, name


def test_every_unbound_receipt_says_why_it_is_kept() -> None:
    unbound = {name for name, binding in bindings().items() if not binding.labels()}
    assert {name for name in unbound if not ENTRIES[name].kept} == set()


def test_committed_register_matches_a_fresh_render() -> None:
    assert REGISTER.read_text(encoding="utf-8") == render()


def test_derived_bindings_match_the_known_record() -> None:
    every = bindings()
    assert "capture-root-chain" in FIXED
    assert every["capture-root-chain"].composer_pinned
    assert every["nonfield-batch-a2-direct-1"].labels() == []
    assert every["capture-root-pilot"].by_path == (
        "capture-root-bridge",
        "capture-root-bridge-final",
        "capture-root-bridge-final2",
    )
    assert every["capture-root-round7-final"].by_result_hash[0] == "capture-root-chain"
    assert every["nonfield-batch-final-sequential"].exclusion_inventory
    assert every["generic-case2175-complete"].pilot_registry
    assert every["capture-child-near"].capture_join


def test_derived_bindings_agree_with_the_curated_tiers() -> None:
    assert tier_contradictions() == KNOWN_TIER_CONTRADICTIONS


def test_hash_scan_takes_only_whole_64_digit_runs() -> None:
    digest = "ab" * 32
    text = f'"{digest}" {digest}0 x{digest[:63]} /{digest}.gz'.encode()
    assert hashes_in(text) == {digest}
    assert hashes_in(digest.encode()) == {digest}
