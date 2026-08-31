"""Inverse-tube occupancy. Not a halt test."""

from __future__ import annotations

import json
from pathlib import Path

from research.conjectures import get_conjecture
from research.juggler_sequence.cycle_almost_search import follow_depth
from research.juggler_sequence.cycle_inverse_width import (
    ARCHIVED_DEATH,
    PREFIX_LEN,
    inverse_walk,
    word_catalog,
)

REPO = Path(__file__).resolve().parents[3]
DOSSIER = REPO / "docs" / "problems" / "juggler_cycle_inverse_width.md"
SUMMARY = (
    REPO
    / "data"
    / "research"
    / "juggler"
    / "cycle_finance"
    / "inverse_width"
    / "summary.json"
)


def test_dossier_has_triage_and_closed_bridge_gates():
    text = DOSSIER.read_text(encoding="utf-8")
    assert "## Branch budget" in text
    assert "Mathematical target" in text
    assert "## Closed-bridge gates" in text
    assert "juggler_cycle_finance_cell_bridge" in text
    assert "BACKWARD_COMPLEX" in text
    assert "## Decision" in text
    assert "## Publication assessment" in text
    assert "**CLOSE**" in text
    assert "55293" in text


def test_catalog_prefixes_are_complete_and_short():
    for spec in word_catalog():
        word = spec["word"]
        assert 1 <= len(word) <= PREFIX_LEN
        if spec["name"] != "all_e":
            assert word[0] == "O"
        if spec["family"] == "near":
            assert word[-1] == "E"


def test_ooe_hull_can_be_thin_and_occupied():
    walk = inverse_walk("OOE", 11)
    assert walk["survived"] is True
    assert walk["occupied_thin"] is True
    assert walk["final_count"] == 1
    last = walk["steps"][-1]
    assert last["letter"] == "O"
    assert last["exact_count"] == 1
    assert last["real_width"] < 1.0
    assert follow_depth(9, "OOE") == 3


def test_near_convergent_inverse_dies_at_empty_ooe_on_the_floor():
    for spec in word_catalog():
        if spec["name"] in ("extra_even_front", "all_oe", "all_e", "all_o"):
            continue
        walk = inverse_walk(spec["word"], 1_000_001)
        assert walk["death_tag"] == "empty_ooe"
        assert walk["death_k"] == 3
        assert walk["archived"] is True
        assert walk["survived"] is False


def test_pure_odd_dies_at_the_odd_cell():
    walk = inverse_walk("O" * 12, 1_000_001)
    assert walk["death_tag"] == "empty_odd_cell"
    assert walk["archived"] is True


def test_even_inverse_does_not_empty():
    walk = inverse_walk("E" * 6, 101)
    assert walk["death_tag"] is None
    assert walk["hulled"] is True or walk["survived"] is True


def test_365_realizes_thirteen_bunched_ooe_letters():
    assert follow_depth(365, "OOE" * 8) == 13


def test_science_artifact_closes():
    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert payload["bound"] == "inverse_width"
    assert payload["L"] == 25781
    decision = payload["decision"]
    assert decision["decision"] == "CLOSE"
    assert decision["classification"] == "INVERSE_WIDTH_CLOSED"
    assert decision["occupied_thin"] is True
    assert decision["empty_wide_real"] is False
    assert decision["unarchived_deaths"] == 0
    assert decision["near_survived"] == 0
    assert decision["new_mechanism"] is False
    assert decision["scale_growth"] is False
    assert decision["leftover_killer"] is False
    assert decision["halt_theorem"] is False
    assert decision["raise_n0"] is False
    assert decision["open_55293"] is False
    assert set(ARCHIVED_DEATH) >= {"empty_ooe", "empty_oe", "empty_odd_cell"}


def test_dossier_and_conjecture_record_close():
    dossier = DOSSIER.read_text(encoding="utf-8")
    assert "**CLOSE**" in dossier
    rec = get_conjecture("juggler_cycle_inverse_width")
    assert rec["status"] == "REFUTED"
    assert rec["counterexamples"]
