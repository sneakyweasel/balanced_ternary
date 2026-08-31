"""Coupled exponent-walk charge. Not a halt test."""

from __future__ import annotations

import json
import math
from pathlib import Path

from research.juggler_sequence.cycle_walk_charge import (
    MU,
    STEP,
    brute_force_budget,
    classify,
    transport_bound,
    walk_budget,
)

ARTIFACT = Path("data/research/juggler/cycle_walk_charge/summary.json")
DOSSIER = Path("docs/problems/juggler_cycle_walk_charge.md")
CONJECTURE = Path("conjectures/active/juggler_cycle_walk_charge.json")


def test_lattice_constants():
    assert math.isclose(MU, math.log2(1.5))
    assert math.isclose(STEP, 1.0 + MU)


def test_dp_matches_brute_force_on_tiny_lengths():
    for length, odd_count in [(5, 4), (8, 6), (11, 7), (12, 8)]:
        dp = walk_budget(length, odd_count, 1000)["walk_sum"]
        bf = brute_force_budget(length, odd_count, 1000)
        assert math.isclose(dp, bf, rel_tol=1e-12)


def test_transport_bound_is_small_at_the_certified_floor():
    eta = transport_bound(50_508, 31_867, 26_254_996)
    assert 0 < eta < 1e-4


def test_committed_target_is_green_with_margin():
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    target = payload["target"]
    assert target["length"] == 50_508
    assert target["floor"] == 26_254_995
    assert target["improvement_over_parity"] > 6.87
    for row in target["eta_rows"]:
        assert row["walk_excludes"] is True
        assert row["kill_margin"] > 1.0
    assert payload["classification"]["label"] == "WALK_CHARGE_GREEN"
    assert classify(target)["label"] == "WALK_CHARGE_GREEN"
    assert payload["not_a_halt_theorem"] is True


def test_calibration_reproduces_archived_necklace_value():
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    calib = payload["calibration"]
    assert calib["length"] == 25_781
    assert calib["floor"] == 1_000_000
    row0 = calib["eta_rows"][0]
    assert math.isclose(row0["walk_rhs"], 1.2984e-4, rel_tol=1e-3)
    assert row0["walk_excludes"] is False
    assert row0["kill_margin"] < 0.2


def test_dossier_and_conjecture_record_are_consistent():
    dossier = DOSSIER.read_text(encoding="utf-8")
    assert "WALK_CHARGE_GREEN" in dossier
    assert "PROMOTE" in dossier
    assert "not claimed" in dossier
    record = json.loads(CONJECTURE.read_text(encoding="utf-8"))
    assert record["status"] == "active"
    assert record["tag"] == "CONJECTURE"
    assert record["not_a_halt_theorem"] is True
