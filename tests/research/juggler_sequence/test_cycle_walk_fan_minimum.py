"""Fan-minimum balance law Phase 0. Arithmetic only, not a halt test."""

from __future__ import annotations

import json
import math
from pathlib import Path

from research.juggler_sequence.cycle_walk_fan_minimum import eps_of_theta

DOSSIER = Path("docs/problems/juggler_cycle_walk_fan_minimum.md")
CONJECTURE = Path("conjectures/active/juggler_walk_fan_minimum_law.json")
ARTIFACT = Path("data/research/juggler/cycle_walk_fan_minimum/summary.json")


def test_eps_conversion():
    # theta = 1 - e^{-eps ln 3}: exact round trip
    for eps in (1e-9, 3.28e-6, 0.1):
        theta = -math.expm1(-eps * math.log(3.0))
        assert abs(eps_of_theta(theta) - eps) < 1e-15 * max(1.0, eps)


def test_fan_minimum_artifact():
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    fans = {f["tag"]: f for f in payload["fans"]}
    fan_a = fans["fanA"]
    # A ~ the certified quotient 55; k* ~ 27.6; minimum matches the
    # competition schedule value 1.0735 at survivor 8632083
    assert 55.0 < fan_a["A"] < 56.5
    assert 27.0 < fan_a["k_star"] < 28.5
    assert abs(fan_a["R_min_pred"] - fan_a["R_min_measured"]) < 5e-4
    assert fan_a["argmin_survivor_exact"] == 8_632_083
    assert fan_a["argmin_matches"] is True
    fan_b = fans["fanB"]
    assert 4.0 < fan_b["A"] < 4.6
    assert fan_b["argmin_survivor_exact"] == 50_961_751
    assert fan_b["within_second_order_exact"] is True
    assert payload["classification"]["label"] == "WALK_FAN_MINIMUM_GREEN"
    # future-fan table: certified rows only through a16
    for row in payload["future_fans"]:
        assert row["R_min_lower"] > 1.0
        if row["quotient_index"] > 16:
            assert row["certified"] is False


def test_anti_overclaim_and_dossier_headings():
    dossier = DOSSIER.read_text(encoding="utf-8")
    for heading in (
        "## Problem",
        "## Exact statement",
        "## Branch budget",
        "## Decision",
        "## Publication assessment",
    ):
        assert heading in dossier
    assert "not claimed" in dossier
    assert "OPEN" in dossier
    record = json.loads(CONJECTURE.read_text(encoding="utf-8"))
    assert record["id"] == "juggler_walk_fan_minimum_law"
    assert record["not_a_halt_theorem"] is True
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert payload["not_a_halt_theorem"] is True
    assert payload["no_new_period_bound"] is True
