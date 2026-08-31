"""First-intersection E^r block. Not a halt test."""

from __future__ import annotations

import json
from pathlib import Path

from research.conjectures import get_conjecture
from research.juggler_sequence.cycle_e_block import (
    START,
    cyclemin_shaped_block,
    even_tower_bounds,
    first_oe_block,
    in_even_tower,
    isqrt_iter,
    odd_parent_outer_bounds,
    prefix_allows_first_run,
    r1_recovers_oe_corridor,
)
from research.juggler_sequence.cycle_entry_corridor import corridor_bounds, ee_entry_count

REPO = Path(__file__).resolve().parents[3]
DOSSIER = REPO / "docs" / "problems" / "juggler_cycle_e_block.md"
SUMMARY = (
    REPO
    / "data"
    / "research"
    / "juggler"
    / "cycle_finance"
    / "e_block"
    / "summary.json"
)


def test_dossier_has_triage_and_closed_gates():
    text = DOSSIER.read_text(encoding="utf-8")
    assert "## Branch budget" in text
    assert "Mathematical target" in text
    assert "## Closed-bridge gates" in text
    assert "## Decision" in text
    assert "## Publication assessment" in text
    assert "**CLOSE**" in text
    assert "Do **not** raise" in text
    assert "cycle_trailing_evens_lt" in text
    assert "power_bound_word" in text
    assert "entry corridor" in text.lower() or "OE corridor" in text


def test_r1_outer_envelope_is_the_archived_corridor():
    rec = r1_recovers_oe_corridor(START)
    corr = corridor_bounds(START)
    assert rec["matches_outer"] is True
    assert rec["u3_lo"] == corr["n4"] == START**4
    assert rec["u3_hi"] == corr["np1_4"] == (START + 1) ** 4


def test_even_tower_is_exact_nested_isqrt():
    v, r = 5, 2
    cell = even_tower_bounds(v, r)
    assert cell["p_lo"] == 5**4
    assert cell["p_hi"] == 6**4
    assert isqrt_iter(cell["p_lo"], r) == v
    assert isqrt_iter(cell["p_hi"] - 1, r) == v
    assert isqrt_iter(cell["p_hi"], r) == v + 1
    assert in_even_tower(cell["p_lo"], v, r)
    assert not in_even_tower(cell["p_hi"], v, r)


def test_odd_parent_outer_for_r2_is_eighth_powers():
    outer = odd_parent_outer_bounds(START, 2)
    assert outer["u3_lo"] == START**8
    assert outer["u3_hi"] == (START + 1) ** 8


def test_first_run_cap_is_the_expanding_prefix_test():
    assert prefix_allows_first_run(2, 1) is True
    assert prefix_allows_first_run(2, 2) is False
    assert prefix_allows_first_run(3, 2) is False
    assert prefix_allows_first_run(4, 2) is True
    assert prefix_allows_first_run(5, 3) is False
    assert prefix_allows_first_run(6, 3) is True
    assert 2 ** (4 + 2) <= 3**4
    assert 2 ** (3 + 2) > 3**3


def test_last_run_r2_is_the_archived_ee_count():
    assert ee_entry_count(START) == START * (START * START + START + 1)


def test_short_climb_r2_contracts_below_start():
    rec = first_oe_block(25)
    assert rec["a0"] == 3
    assert rec["r"] == 2
    assert rec["valley"] < 25
    assert prefix_allows_first_run(3, 2) is False
    assert cyclemin_shaped_block(rec) is False


def test_longer_climb_can_be_cyclemin_shaped():
    rec = first_oe_block(115)
    assert rec["a0"] == 5
    assert rec["r"] == 2
    assert rec["valley"] >= 115
    assert cyclemin_shaped_block(rec) is True


def test_realized_window_records_r_ge_2_and_last_run_occupancy():
    data = json.loads(SUMMARY.read_text(encoding="utf-8"))
    realized = data["realized_first_runs"]
    assert realized["n_r_ge_2"] > 0
    hit = realized["first_r2"]
    assert hit is not None
    check = first_oe_block(hit["n"])
    assert check["a0"] == hit["a0"]
    assert check["r"] == hit["r"] >= 2
    assert data["last_run"]["r2_count"] == START * (START * START + START + 1)
    assert data["last_run"]["r3_found"] is True
    assert data["decision"]["classification"] == "E_BLOCK_CLOSED"


def test_dossier_and_conjecture_record_close():
    dossier = DOSSIER.read_text(encoding="utf-8")
    assert "**CLOSE**" in dossier
    rec = get_conjecture("juggler_cycle_e_block")
    assert rec["status"] == "REFUTED"
    assert rec["lean_reference"] == "cycle_trailing_evens_lt"
    assert rec["counterexamples"]
