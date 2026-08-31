"""Adjacent-seam incompatibility propagation. Not a halt test."""

from __future__ import annotations

import json
from pathlib import Path

from research.conjectures import get_conjecture
from research.juggler_sequence.cycle_budget_opt import oe_start_min
from research.juggler_sequence.cycle_e_block import prefix_allows_first_run
from research.juggler_sequence.cycle_exponent_budget import rho
from research.juggler_sequence.cycle_ordered_excursion import (
    excursion_map,
    ooe_blocks_oe,
    two_ooe_still_blocks_oe,
)
from research.juggler_sequence.cycle_seam_propagate import (
    START,
    block_image,
    block_propagate,
    first_ooe_start,
    log_width,
    walk_blocks,
)
from research.juggler_sequence.cyclic_feasibility import Bound, propagate_cycle, with_parity

REPO = Path(__file__).resolve().parents[3]
DOSSIER = REPO / "docs" / "problems" / "juggler_cycle_seam_propagate.md"
SUMMARY = (
    REPO
    / "data"
    / "research"
    / "juggler"
    / "cycle_finance"
    / "seam_propagate"
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
    assert "prefix_allows_first_run" in text
    assert "propagate_cycle" in text
    assert "ooe_blocks_oe" in text


def test_prefix_pairs_recover_the_expanding_test():
    assert prefix_allows_first_run(2, 1) is True
    assert prefix_allows_first_run(2, 2) is False
    assert prefix_allows_first_run(3, 2) is False
    assert prefix_allows_first_run(4, 2) is True


def test_archived_ooe_blocks_oe_at_first_ooe_start():
    assert ooe_blocks_oe(START, START) is True
    assert two_ooe_still_blocks_oe(START, START) is True
    start = first_ooe_start(START)
    assert start == 1_000_057
    mapped = excursion_map(start, 2)
    assert mapped is not None
    _peak, landing = mapped
    assert landing < oe_start_min(START)
    second = excursion_map(landing, 2)
    assert second is not None
    assert second[1] < oe_start_min(START)


def test_log_width_of_ooe_matches_rho():
    src = with_parity(Bound(1001, 3001), True)
    out = block_image(src, 2, 1)
    width_in = log_width(src)
    width_out = log_width(out)
    assert width_in is not None and width_out is not None
    ratio = width_out / width_in
    assert abs(ratio - float(rho(2, 1))) < 0.15


def test_realized_graph_has_an_ooe_self_loop():
    blocks = walk_blocks(365)
    types = [(rec["a"], rec["r"]) for rec in blocks]
    assert types[:3] == [(2, 1), (2, 1), (2, 1)]
    assert (2, 1) in {(types[i], types[i + 1])[0] for i in range(len(types) - 1)}
    assert any(
        types[i] == (2, 1) and types[i + 1] == (2, 1) for i in range(len(types) - 1)
    )


def test_block_closure_is_not_strictly_stronger():
    word = "OOOOEE"
    _letter, letter_empty = propagate_cycle(word, 8000)
    _block, block_empty = block_propagate(word, 8000)
    assert not (block_empty and not letter_empty)


def test_science_artifact_closes():
    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert payload["bound"] == "seam_propagate"
    assert payload["archived_cyclemin"]["ooe_start"] == 1_000_057
    assert payload["archived_cyclemin"]["landing_below_oe_min"] is True
    assert payload["wide_pairs"]["n_new_empty"] == 0
    assert payload["tube_pairs"]["n_new_empty"] == 0
    assert payload["middle_pairs"]["n_new_empty"] == 0
    assert payload["realized_graph"]["full"]["has_directed_cycle"] is True
    assert payload["realized_graph"]["full"]["self_loop_ooe"] is True
    assert payload["realized_graph"]["cyclemin_shaped"]["has_directed_cycle"] is True
    assert payload["controls"]["shared_prefix_then_split"] is True
    assert payload["shrink"]["all_match_rho"] is True
    assert payload["closure"]["all_agree"] is True
    decision = payload["decision"]
    assert decision["decision"] == "CLOSE"
    assert decision["classification"] == "SEAM_PROPAGATE_CLOSED"
    assert decision["new_composed_emptiness"] is False
    assert decision["leftover_killer"] is False
    assert decision["halt_theorem"] is False
    assert decision["paper_a_edit"] is False


def test_dossier_and_conjecture_record_close():
    dossier = DOSSIER.read_text(encoding="utf-8")
    assert "**CLOSE**" in dossier
    rec = get_conjecture("juggler_cycle_seam_propagate")
    assert rec["status"] == "REFUTED"
    assert rec["lean_reference"] == "cycle_trailing_evens_lt"
    assert rec["counterexamples"]
