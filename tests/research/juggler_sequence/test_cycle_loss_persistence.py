"""Cross-excursion usable-loss persistence. Not a halt test."""

from __future__ import annotations

import json
import math
from pathlib import Path

import pytest

from research.conjectures import get_conjecture
from research.juggler_sequence.cycle_budget_opt import oe_start_min
from research.juggler_sequence.cycle_finance import PUBLISHED_FLOOR
from research.juggler_sequence.cycle_loss_persistence import (
    SPOTLIGHT,
    START,
    next_odd_valley,
    odd_loss,
    pair_record,
)

REPO = Path(__file__).resolve().parents[3]
SUMMARY = (
    REPO
    / "data"
    / "research"
    / "juggler"
    / "cycle_finance"
    / "loss_persistence"
    / "summary.json"
)


def test_odd_loss_matches_the_cell_logarithm():
    rec = odd_loss(3)
    assert rec["y"] == 5
    assert rec["rho"] == 2
    assert rec["pos"] == 2 / 11
    assert rec["eps"] == pytest.approx(0.5 * math.log1p(2 / 25))
    assert rec["eps_max"] == pytest.approx(0.5 * math.log1p(10 / 25))
    assert 0.0 < rec["usable"] < 1.0


def test_jointly_near_maximal_ooe_pair():
    rec = pair_record(1000301)
    assert rec is not None
    assert rec["a0"] == 2
    assert rec["v1"] == 5625317
    assert rec["v1"] > START
    assert rec["U0"] > 0.97
    assert rec["U1"] > 0.99
    assert rec["U0"] + rec["U1"] > 1.96


def test_jointly_near_maximal_long_then_oe_pair():
    rec = pair_record(1018335)
    assert rec is not None
    assert rec["a0"] == 3
    assert rec["a1"] == 1
    assert min(rec["U0"], rec["U1"]) > 0.97
    nxt = next_odd_valley(rec["v1"])
    assert nxt is not None


def test_persistence_scan_closes():
    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert payload["n"] == START
    assert payload["oe_start"] == oe_start_min(START)
    assert payload["valley"]["n_pairs"] == 2878
    assert payload["valley"]["n_below_floor"] == 6340
    assert payload["valley"]["by_class"]["OE"]["count"] == 0
    assert payload["valley"]["by_class"]["OOE"]["count"] == 1210
    assert payload["valley"]["all"]["max_min_U"] > 0.97
    assert payload["valley"]["all"]["max_Usum"] > 1.96
    assert payload["valley"]["all"]["best_min_U"]["x"] == 1018335
    assert payload["valley"]["by_class"]["OOE"]["best_sum"]["x"] == 1000301
    ooe = payload["valley"]["by_class"]["OOE"]["cross_U"]["c_0.9"]
    assert ooe["p_cond"] > ooe["p"]
    assert payload["both_near_attained"] is False
    assert payload["two_excursion_tax"] is False
    assert payload["window_max_is_not_a_theorem"] is True
    assert payload["leftover_killer"] is False
    assert payload["emptied_count"] == 0
    assert payload["emptied_lengths"] == []
    assert payload["spotlights"]["55293"]["would_kill_if_uniform"] is True
    assert payload["spotlights"]["55293"]["kills"] is False
    assert payload["spotlights"]["25781"]["would_kill_if_uniform"] is False
    assert payload["halt_theorem"] is False
    assert payload["no_cycle_all_lengths"] is False
    assert payload["floor"] == PUBLISHED_FLOOR
    for length in SPOTLIGHT:
        assert str(length) in payload["spotlights"]


def test_dossier_and_conjecture_record_close():
    dossier = (
        REPO / "docs" / "problems" / "juggler_cycle_loss_persistence.md"
    ).read_text(encoding="utf-8")
    assert "## Branch budget" in dossier
    assert "## Decision" in dossier
    assert "## Publication assessment" in dossier
    assert "**CLOSE**" in dossier
    assert "loss_persistence/summary.json" in dossier
    assert "juggler_cycle_loss_persistence_leftover_killer" in dossier
    rec = get_conjecture("juggler_cycle_loss_persistence_leftover_killer")
    assert rec["status"] == "REFUTED"
    assert rec["counterexamples"]
