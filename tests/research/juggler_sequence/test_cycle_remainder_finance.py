"""Finance-weighted floor-remainder control. Not a halt test."""

from __future__ import annotations

import json
from pathlib import Path

from research.conjectures import get_conjecture
from research.juggler_sequence.cycle_budget_opt import oe_start_min
from research.juggler_sequence.cycle_finance import PUBLISHED_FLOOR
from research.juggler_sequence.cycle_remainder_finance import (
    KILL_FACTOR_55293,
    SPOTLIGHT,
    START,
    cell_record,
    oe_legal,
    ooe_legal,
)

REPO = Path(__file__).resolve().parents[3]
SUMMARY = (
    REPO
    / "data"
    / "research"
    / "juggler"
    / "cycle_finance"
    / "remainder_finance"
    / "summary.json"
)


def test_cell_position_on_a_square_and_a_near_top_ooe():
    rec = cell_record(16)
    assert rec["odd"] is False
    assert rec["rho"] == 0
    assert rec["pos"] == 0.0
    assert rec["usable"] == 0.0
    witness = cell_record(1016445)
    assert ooe_legal(witness)
    assert witness["pos"] > 0.99997
    assert witness["usable"] > 0.99997
    assert witness["pos"] >= KILL_FACTOR_55293


def test_oe_and_ooe_split_on_parity_of_the_image():
    odd_odd = cell_record(START | 1)
    assert odd_odd["odd"]
    assert ooe_legal(odd_odd) != oe_legal(odd_odd)


def test_remainder_scan_closes():
    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert payload["n"] == START
    assert payload["oe_start"] == oe_start_min(START)
    assert payload["n_run_survivors"] == 99
    assert payload["remainders_unrestricted"] is True
    assert payload["near_top_ooe_exists"] is True
    assert payload["near_top_oe_exists"] is True
    assert payload["even_landing_near_top"] is True
    assert payload["uniform_bound_kills_55293"] is False
    assert payload["killed_count_max"] == 0
    assert payload["killed_by_max_pos"] == []
    assert payload["killed_count_mean"] == 49
    assert 55293 in payload["killed_by_mean_usable"]
    assert 25781 not in payload["killed_by_mean_usable"]
    assert payload["valley"]["best_ooe"]["x"] == 1016445
    assert payload["valley"]["n_ooe_above_kill_factor"] == 62
    assert payload["valley"]["n_ooe_near_top"] == 56
    assert payload["mean_ooe_usable"] < 0.5
    assert payload["max_ooe_pos"] > 0.99997
    assert payload["need_factor_55293"] < KILL_FACTOR_55293
    assert payload["spotlights"]["25781"]["need_factor"] < 0.05
    assert payload["leftover_killer"] is False
    assert payload["emptied_count"] == 0
    assert payload["halt_theorem"] is False
    assert payload["no_cycle_all_lengths"] is False
    assert payload["floor"] == PUBLISHED_FLOOR
    for length in SPOTLIGHT:
        assert str(length) in payload["spotlights"]


def test_dossier_and_conjecture_record_close():
    dossier = (
        REPO / "docs" / "problems" / "juggler_cycle_remainder_finance.md"
    ).read_text(encoding="utf-8")
    assert "## Branch budget" in dossier
    assert "## Decision" in dossier
    assert "## Publication assessment" in dossier
    assert "**CLOSE**" in dossier
    assert "remainder_finance/summary.json" in dossier
    assert "juggler_cycle_remainder_finance_leftover_killer" in dossier
    rec = get_conjecture("juggler_cycle_remainder_finance_leftover_killer")
    assert rec["status"] == "REFUTED"
    assert rec["counterexamples"]
