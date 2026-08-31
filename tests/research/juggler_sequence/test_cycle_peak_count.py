"""Peak count p = m. Not a halt test."""

from __future__ import annotations

import json
from pathlib import Path

from research.conjectures import get_conjecture
from research.juggler_sequence.cycle_peak_count import (
    ALPHA,
    ONE_MINUS_ALPHA,
    cell_row,
    denom_cell_fires,
    expanding,
    leftover_m_row,
    o_min_for_even,
    peak_cap,
    plus_chain_fires,
    plus_exponents,
)
from research.juggler_sequence.cycle_position_finance import odd_run_heights

REPO = Path(__file__).resolve().parents[3]
SUMMARY = (
    REPO
    / "data"
    / "research"
    / "juggler"
    / "cycle_finance"
    / "peak_count"
    / "summary.json"
)


def test_peak_cap_is_min_e_and_o_minus_1():
    assert peak_cap(12, 7) == 7
    assert peak_cap(7, 4) == 4
    assert peak_cap(3, 5) == 2
    assert peak_cap(1, 4) == 0


def test_o_minus_1_never_binds_on_expanding_words():
    for even_count in range(4, 13):
        odd_count = o_min_for_even(even_count)
        assert expanding(odd_count, even_count)
        assert odd_count - 1 >= even_count
        assert peak_cap(odd_count, even_count) == even_count
    assert ONE_MINUS_ALPHA == 1.0 - ALPHA
    assert 0.3690 < ONE_MINUS_ALPHA < 0.3691


def test_plus_chain_recovers_o7eeee_exponents():
    exp = plus_exponents(7, 4)
    assert exp["left"] == 6177
    assert exp["right"] == 6038
    assert exp["slack"] == 139
    assert exp["slack"] == 3**7 - (1 << 11)
    assert plus_chain_fires(16, 7, 4)
    assert not plus_chain_fires(15, 7, 4)


def test_denom_cell_leaks_at_leftover_one_peak_shapes():
    assert denom_cell_fires(828484409, 7, 4)
    assert not denom_cell_fires(10**12, 12, 7)
    row = cell_row(12, 7)
    assert row["L"] == 19
    assert row["denom_leaks_cap"] is True
    assert row["plus_n0"] == 55
    assert row["plus_slack_is_3o_minus_2L"]


def test_height_kills_m1_at_25781():
    heights = odd_run_heights(1_000_001)
    row = leftover_m_row(25781, n0=1_000_001, heights=heights)
    assert row["height_kills_m1"]
    assert row["height_kills_m2"]
    assert row["joint_kills_m1"]
    assert row["p_max_is_e"]
    assert row["o_minus_1_binds"] is False


def test_artifact_records_the_close():
    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert payload["p_is_m"] is True
    assert payload["classification"] == "PEAK_COUNT_CLOSED"
    assert payload["survivor_count"] == 99
    assert payload["height_kills_all_m1"] is True
    assert payload["height_kills_all_m2"] is True
    assert payload["joint_kills_all_m1"] is True
    assert payload["live_m1"] == []
    assert payload["live_m2"] == []
    assert payload["o_minus_1_never_binds"] is True
    assert payload["p_max_is_e_on_all"] is True
    assert payload["plus_slack_identity"] is True
    assert payload["leftover_denom_all_leak"] is True
    assert payload["leftover_plus_all_fire"] is True
    assert payload["grid_denom_leaks"] == [19]
    assert payload["o7eeee"]["slack"] == 139
    assert payload["o7eeee"]["left"] == 6177
    assert payload["b2_leftover"][0]["L"] == 25781
    assert payload["b2_leftover"][0]["plus_n0"] == 12492
    assert payload["b2_leftover"][0]["denom_n0"] is None
    assert payload["halt_theorem"] is False
    assert payload["paper_a_edit"] is False


def test_dossier_and_conjecture_record_close():
    dossier = (REPO / "docs" / "problems" / "juggler_cycle_peak_count.md").read_text(
        encoding="utf-8"
    )
    assert "## Branch budget" in dossier
    assert "## Decision" in dossier
    assert "## Publication assessment" in dossier
    decision = dossier.split("## Decision", 1)[1].split("## ", 1)[0]
    assert "CLOSE" in decision
    rec = get_conjecture("juggler_cycle_peak_count")
    assert rec["status"] == "REFUTED"
    assert rec["counterexamples"]
