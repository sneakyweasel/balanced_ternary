"""Ordered excursion closure. Not a halt test."""

from __future__ import annotations

import json
from pathlib import Path

from research.conjectures import get_conjecture
from research.juggler_sequence.block_map_q import a_of, block_map
from research.juggler_sequence.cycle_budget_opt import oe_start_min
from research.juggler_sequence.cycle_finance import PUBLISHED_FLOOR, o_min_and_theta
from research.juggler_sequence.cycle_ordered_excursion import (
    SPOTLIGHT,
    START,
    control_row,
    excursion_map,
    first_a2,
    ooe_blocks_oe,
    ooe_cell_holds,
    spotlight_row,
    two_block_envelope_row,
    two_ooe_still_blocks_oe,
)

REPO = Path(__file__).resolve().parents[3]
SUMMARY = (
    REPO
    / "data"
    / "research"
    / "juggler"
    / "cycle_finance"
    / "ordered_excursion"
    / "summary.json"
)


def test_excursion_map_agrees_with_block_map():
    for seed in (365, 1517, 1000057):
        run = a_of(seed)
        rec = excursion_map(seed, run)
        assert rec is not None
        assert rec[1] == block_map(seed)


def test_prescribed_run_rejects_wrong_length():
    assert excursion_map(1000057, 1) is None
    assert excursion_map(365, 1) is None
    assert excursion_map(365, 2) is not None


def test_ooe_cell_and_scale_lemmas():
    seed = first_a2(START)
    assert seed == 1000057
    rec = excursion_map(seed, 2)
    assert rec is not None
    assert ooe_cell_holds(seed, rec[1])
    assert ooe_blocks_oe(seed, START)
    assert two_ooe_still_blocks_oe(seed, START)
    assert rec[1] < oe_start_min(START)
    row = two_block_envelope_row(seed)
    assert row is not None
    assert row["composed_cell"]
    assert row["z"] < oe_start_min(START)
    assert row["deficit"] == 7
    assert row["rel_deficit"] < 1e-6


def test_two_block_lemma_at_controls():
    for seed in (365, 1517):
        assert two_ooe_still_blocks_oe(seed, seed)
        rec = excursion_map(seed, 2)
        assert rec is not None
        second = excursion_map(rec[1], 2)
        assert second is not None
        assert second[1] < oe_start_min(seed)


def test_prefix_222_does_not_determine_the_fourth_run():
    left = control_row(365)
    right = control_row(1517)
    assert left["prefix_222"]
    assert right["prefix_222"]
    assert left["fourth_run"] == 2
    assert right["fourth_run"] == 1
    assert left["fourth_valley_ge_oe"]
    assert right["fourth_valley_ge_oe"]


def test_spotlight_counts():
    row = spotlight_row(25781)
    odd_count, _theta = o_min_and_theta(25781)
    assert row["L"] == 25781
    assert row["o"] == odd_count
    assert row["ooe_count"] == 6751
    assert row["oe_count"] == 2764
    assert row["ratio_near_climb"]
    tight = spotlight_row(55293)
    assert tight["ooe_count"] == 14479
    assert tight["oe_count"] == 5928
    assert tight["ratio_near_climb"]
    assert not row["emptied"]
    assert row["reduces_to_envelope"]


def test_ordered_scan_closes():
    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert payload["emptied_count"] == 0
    assert payload["emptied_lengths"] == []
    assert payload["leftover_killer"] is False
    assert payload["reduces_to_envelope"] is True
    assert payload["two_block_correction_nontrivial"] is False
    assert payload["descent_requires_compensation"] is False
    assert payload["triple_222_realized"] is True
    assert payload["pair_21_legal_near_n"] is False
    assert payload["triple_221_legal_near_n"] is False
    assert payload["triple_221_legal_mid"] is True
    assert payload["prefix_222_split"] is True
    assert payload["unscaled_pairs_realized"] is True
    assert payload["requires_word_enumeration"] is True
    assert payload["scanned_other_97"] is False
    assert payload["halt_theorem"] is False
    assert payload["no_cycle_all_lengths"] is False
    assert payload["floor"] == PUBLISHED_FLOOR
    assert payload["first_a2"] == 1000057
    assert payload["two_block"]["rel_deficit"] < 1e-6
    assert payload["a3_from_n"]["w_ge_oe"] is True
    assert payload["descent"]["sequel"]["landing"] == 189
    for length in SPOTLIGHT:
        spot = payload["spotlights"][str(length)]
        assert spot["emptied"] is False
        assert spot["reduces_to_envelope"] is True
        assert spot["ratio_near_climb"] is True


def test_dossier_and_conjecture_record_close():
    dossier = (
        REPO / "docs" / "problems" / "juggler_cycle_ordered_excursion.md"
    ).read_text(encoding="utf-8")
    assert "## Branch budget" in dossier
    assert "## Decision" in dossier
    assert "## Publication assessment" in dossier
    assert "**CLOSE**" in dossier
    assert "ordered_excursion/summary.json" in dossier
    assert "juggler_cycle_ordered_excursion_leftover_killer" in dossier
    rec = get_conjecture("juggler_cycle_ordered_excursion_leftover_killer")
    assert rec["status"] == "REFUTED"
