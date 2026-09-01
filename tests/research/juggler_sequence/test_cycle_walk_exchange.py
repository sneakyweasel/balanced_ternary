"""Hug-exchange Phase 0. Not a halt test and not a floor raise."""

from __future__ import annotations

import json
import math
from pathlib import Path

from research.juggler_sequence.cycle_christoffel import christoffel_word
from research.juggler_sequence.cycle_walk_charge import MU, STEP
from research.juggler_sequence.cycle_walk_exchange import (
    c_star_integral,
    exchange_holds,
    first_disagreement,
    prefix_odds,
)
from research.juggler_sequence.cycle_walk_greedy import hug_word

DOSSIER = Path("docs/problems/juggler_cycle_walk_exchange.md")
CONJECTURE = Path("conjectures/proved/juggler_walk_hug_exchange.json")
ARTIFACT = Path("data/research/juggler/cycle_walk_exchange/summary.json")


def test_exchange_holds_at_four_three():
    report = exchange_holds(4, 3)
    assert report["hug"] == "OOEO"
    assert report["hug"] != christoffel_word(4, 3)
    assert report["n_admissible"] == 2
    assert report["prefix_min"] is True
    assert report["first_split_is_e_vs_o"] is True
    split = first_disagreement("OOEO", "OOOE")
    assert split == {"k": 2, "hug": "E", "other": "O"}
    hug_a = prefix_odds("OOEO")
    other_a = prefix_odds("OOOE")
    assert hug_a == [0, 1, 2, 2, 3]
    assert all(h <= o for h, o in zip(hug_a, other_a))


def test_iet_is_rotation_by_alpha():
    below = 0.3
    assert below + MU < STEP
    assert abs((below + MU) - (below + MU) % STEP) < 1e-15
    above = 1.2
    wrapped = above + MU - STEP
    assert abs(wrapped - (above - 1.0)) < 1e-15


def test_c_star_two_forms_and_simple_bound():
    star = c_star_integral(17.08262118877416)
    assert math.isclose(star["C"], star["C_u_check"], rel_tol=1e-6)
    assert star["C"] < star["bound"]
    assert 0.047 < star["C"] < 0.049
    assert math.isclose(star["mean_u"], STEP / 2.0, rel_tol=1e-12)


def test_anti_overclaim_and_dossier_headings():
    dossier = DOSSIER.read_text(encoding="utf-8")
    for heading in (
        "## Problem",
        "## Exact statement",
        "## Current literature",
        "## Branch budget",
        "## Decision",
        "## Publication assessment",
    ):
        assert heading in dossier
    decision = dossier.split("## Decision", 1)[1].split("## ", 1)[0]
    assert "PROMOTE" in decision
    assert "not claimed" in dossier
    record = json.loads(CONJECTURE.read_text(encoding="utf-8"))
    assert record["id"] == "juggler_walk_hug_exchange"
    assert record["status"] == "EXACT — HUMAN PROOF"
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert payload["not_a_halt_theorem"] is True
    assert payload["no_cycle_all_lengths"] is False
    assert payload["not_a_uniform_ratio_theorem"] is True
    assert payload["classification"]["label"] == "WALK_EXCHANGE_GREEN"
    assert payload["exchange_census"]["n_ok"] == payload["exchange_census"][
        "n_feasible"
    ]
    assert payload["envelope"]["all_hug_below_bound"] is True
    assert payload["envelope"]["n_bound_kills"] == 18
    assert payload["envelope"]["uniform_ratio_false"] is True
    assert payload["c_star"]["C"] < payload["c_star"]["bound"]
    assert hug_word(4, 3) == "OOEO"
