"""Fan successor rigidity Phase 0. Not a halt test."""

from __future__ import annotations

import json
from pathlib import Path

from research.juggler_sequence.cycle_walk_fan_successor import (
    ANCHOR,
    BLOCKER,
    GENERATORS,
    NEXT_FAN,
    O_BLOCKER,
    O_NEXT,
    defect_product,
    dirichlet_cap,
    invert_defect,
    leftover_crude_cap,
    legendre_cap,
)

DOSSIER = Path("docs/problems/juggler_cycle_walk_fan_successor.md")
CONJECTURE = Path("conjectures/refuted/juggler_fan_successor_rigidity.json")
ARTIFACT = Path("data/research/juggler/cycle_walk_fan_successor/summary.json")
FLIGHT = Path("data/research/juggler/flight_anchor_period/summary.json")


def test_lattice_generators_match_known_pairs():
    assert GENERATORS[0] == (25781, 16266, "vstar")
    assert GENERATORS[1] == (50508, 31867, "F2")
    assert GENERATORS[2] == (176251, 111202, "seed_q")
    assert GENERATORS[3] == (301994, 190537, "fan_step")
    assert BLOCKER == 176251 + 301994
    assert NEXT_FAN == 176251 + 2 * 301994
    assert O_NEXT - O_BLOCKER == 190537
    assert 25781 * 665 - 1054 * 16266 == 1


def test_defect_product_inverts():
    left, right = 3.5e-6, 7.3e-6
    total = defect_product(left, right)
    assert abs(invert_defect(total, left) - right) < 1e-15
    assert abs(defect_product(left, invert_defect(total, left)) - total) < 1e-15


def test_dirichlet_misses_leftover_epsilon():
    for length in (BLOCKER, NEXT_FAN):
        crude = leftover_crude_cap(length, float(ANCHOR))
        diri = dirichlet_cap(length)
        leg = legendre_cap(length)
        assert crude > 30.0 * diri
        assert crude > 60.0 * leg
        assert not (crude < diri)
        assert not (crude < leg)


def test_successor_artifact():
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    flight = json.loads(FLIGHT.read_text(encoding="utf-8"))
    stored = {int(r["length"]) for r in payload["stored_leftovers"]}
    flight_left = {
        int(r["length"]) for r in flight["scan"]["parity_survivors"]
    }
    assert stored == flight_left
    assert stored == {
        478245,
        504026,
        528753,
        579261,
        629769,
        654496,
        680277,
        705004,
        730785,
        755512,
        780239,
    }
    cone = set(payload["cone_ominimal_lengths"])
    assert stored <= cone
    assert payload["cone_ominimal_count"] == 46
    assert payload["classification"]["extra_ominimal_count"] == 35
    assert payload["classification"]["missing_count"] == 0
    extras = {int(r["length"]) for r in payload["extras_ominimal"]}
    assert 529807 in extras
    assert extras.isdisjoint(stored)
    for chk in payload["defect_checks"]:
        assert chk["holds"] is True
        assert chk["relative_error"] < 1e-10
    shape = payload["shape"]
    assert 0.98 < shape["theta_ratio"] < 0.99
    assert shape["margin_k1"] > 1.0
    assert shape["margin_k2"] < 1.0
    assert shape["k2_worse_margin"] is True
    comp = payload["completeness"]
    assert comp["dirichlet_reaches"] is False
    assert comp["legendre_reaches"] is False
    assert payload["classification"]["label"] == "FAN_SUCCESSOR_CLOSED"
    assert payload["classification"]["decision"] == "CLOSE"


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
    assert "CLOSE" in decision
    assert "PROMOTE" not in decision
    assert "not claimed" in dossier
    record = json.loads(CONJECTURE.read_text(encoding="utf-8"))
    assert record["id"] == "juggler_fan_successor_rigidity"
    assert record["status"] == "REFUTED"
    assert record["not_a_halt_theorem"] is True
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert payload["not_a_halt_theorem"] is True
    assert payload["no_census"] is True
    assert payload["no_baker_reopen"] is True
    assert payload["no_floor_raise"] is True
    assert payload["no_paper_a_edit"] is True
    assert payload["no_fan_minimum_reopen"] is True
    assert payload["no_new_period_bound"] is True
