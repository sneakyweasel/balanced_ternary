"""Finance-to-cell bridge. Not a halt test."""

from __future__ import annotations

import json
from pathlib import Path

from research.conjectures import get_conjecture
from research.juggler_sequence.cycle_finance import PUBLISHED_FLOOR
from research.juggler_sequence.cycle_finance_cell_bridge import (
    coincidence_row,
    composed_21_cell,
    expanding_last_ooe_hits,
    first_pair,
    isolated_minority,
    last_blocks,
    triple221_into,
)
from research.juggler_sequence.cycle_ordered_excursion import excursion_map
from research.juggler_sequence.cycle_prefix_feasibility import extremal_word

REPO = Path(__file__).resolve().parents[3]
SUMMARY = (
    REPO
    / "data"
    / "research"
    / "juggler"
    / "cycle_finance"
    / "finance_cell_bridge"
    / "summary.json"
)


def test_record_leftovers_collapse_and_end_21():
    for length in (19, 84, 1054, 25781):
        row = coincidence_row(length)
        assert row["all_equal"]
        assert row["ends_oe"]
        assert row["ends_21"]
        assert row["isolated_oe"]
        assert row["a0"] == 2


def test_f2_is_expanding_on_small_window():
    rec = expanding_last_ooe_hits(3, 5000)
    assert rec["n_a2"] > 0
    assert rec["n_F2_le_v"] == 0
    assert rec["expanding"]


def test_terminal_21_is_realized_at_the_published_floor():
    pair = first_pair(PUBLISHED_FLOOR + 1, 1, 2)
    assert pair is not None
    u, v = pair
    assert u == 12915515
    assert v == 100000159
    first = excursion_map(u, 2)
    second = excursion_map(v, 1)
    assert first is not None and first[1] == v
    assert second is not None and second[1] == PUBLISHED_FLOOR + 1
    cells = composed_21_cell(PUBLISHED_FLOOR + 1, u, v)
    assert cells["oe_cell"]
    assert cells["ooe_cell"]
    assert cells["necessary_u27_ge_n32"]


def test_terminal_221_misses_at_the_published_floor():
    assert triple221_into(PUBLISHED_FLOOR + 1) is None


def test_canonical_suffix_is_aab():
    word = extremal_word(25781)
    isol = isolated_minority(word)
    assert isol["isolated_minority"]
    assert isol["suffix"].endswith("AAB")
    assert last_blocks(word, 2) == [(2, 1), (1, 1)]


def test_science_artifact_closes():
    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert payload["bound"] == "finance_cell_bridge"
    assert payload["L"] == 25781
    assert payload["words"]["all_equal"] is True
    assert payload["words"]["ends_21"] is True
    assert payload["expanding_last_ooe"]["expanding"] is True
    assert payload["census_floor"]["n_21"] >= 1
    assert payload["census_floor"]["n_221"] == 0
    assert payload["terminal_21_empty_as_law"] is False
    assert payload["bridge_theorem"] is False
    assert payload["leftover_killer"] is False
    assert payload["halt_theorem"] is False
    assert payload["reduces_to_known"] is True


def test_dossier_and_conjecture_record_close():
    dossier = (
        REPO / "docs" / "problems" / "juggler_cycle_finance_cell_bridge.md"
    ).read_text(encoding="utf-8")
    assert "## Branch budget" in dossier
    assert "## Decision" in dossier
    assert "## Publication assessment" in dossier
    assert "**CLOSE**" in dossier
    rec = get_conjecture("juggler_cycle_finance_cell_bridge")
    assert rec["status"] == "REFUTED"
    assert rec["counterexamples"]
