"""Finance-conditioned exact closure. Not a halt test."""

from __future__ import annotations

import json
from pathlib import Path

from research.conjectures import get_conjecture
from research.juggler_sequence.cycle_conditioned_closure import (
    SPOTLIGHT,
    deepen_cost,
    deficit_row,
    lose_cheap_cost,
    run_type_n_max,
)
from research.juggler_sequence.cycle_finance import PUBLISHED_FLOOR, o_min_and_theta

REPO = Path(__file__).resolve().parents[3]
SUMMARY = (
    REPO
    / "data"
    / "research"
    / "juggler"
    / "cycle_finance"
    / "conditioned_closure"
    / "summary.json"
)
START = PUBLISHED_FLOOR + 1


def test_deviations_are_cheaper_than_the_margin():
    row = deficit_row(25781)
    assert row["packed_over_theta"] > 20.0
    assert row["k_lose_cheap"] == 6532
    assert row["k_deepen"] == 2764
    assert row["deepen_all_still_above_theta"]
    assert row["residual_exponential"]
    assert not row["concentrates"]
    assert not row["closure_empty"]
    assert row["requires_word_enumeration"]
    assert row["hull_meets"]
    assert row["n_max_run"] == 19010076


def test_tight_leftover_still_affords_deepen_all():
    row = deficit_row(55293)
    assert 1.0 < row["packed_over_theta"] < 1.02
    assert row["k_lose_cheap"] == 177
    assert row["k_deepen"] == 5928
    assert row["deepen_all_still_above_theta"]
    assert row["residual_log10_lose"] > 200.0
    assert not row["concentrates"]
    assert not row["closure_empty"]
    assert row["hull_meets"]
    assert row["n_max_run"] == 1011446
    assert row["n_hi"] == 1011445


def test_n_max_run_is_the_raw_packed_crossing():
    odd_count, theta = o_min_and_theta(25781)
    assert run_type_n_max(25781, odd_count, theta) == 19010076
    odd_tight, theta_tight = o_min_and_theta(55293)
    assert run_type_n_max(55293, odd_tight, theta_tight) == 1011446
    assert lose_cheap_cost(START) > deepen_cost(START) > 0.0


def test_conditioned_scan_closes():
    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert payload["emptied_count"] == 0
    assert payload["emptied_lengths"] == []
    assert payload["concentrates"] is False
    assert payload["deepen_all_still_above_theta"] is True
    assert payload["hull_feasible"] is True
    assert payload["stronger_than_packing"] is False
    assert payload["requires_word_enumeration"] is True
    assert payload["reduces_to_envelope"] is True
    assert payload["halt_theorem"] is False
    assert payload["no_cycle_all_lengths"] is False
    for length in SPOTLIGHT:
        spot = payload["spotlights"][str(length)]
        assert spot["closure_empty"] is False
        assert spot["deepen_all_still_above_theta"] is True
        assert spot["hull"]["reduces_to_envelope"] is True
        assert spot["stronger_than_packing"] is False


def test_dossier_and_conjecture_record_close():
    dossier = (
        REPO / "docs" / "problems" / "juggler_cycle_conditioned_closure.md"
    ).read_text(encoding="utf-8")
    assert "## Branch budget" in dossier
    assert "## Decision" in dossier
    assert "## Publication assessment" in dossier
    assert "**CLOSE**" in dossier
    assert "conditioned_closure/summary.json" in dossier
    assert "juggler_cycle_conditioned_closure_leftover_killer" in dossier
    rec = get_conjecture("juggler_cycle_conditioned_closure_leftover_killer")
    assert rec["status"] == "REFUTED"
