"""Arch-bound payoff Phase 0. Not a halt test and not an envelope edit."""

from __future__ import annotations

import json
from pathlib import Path

from research.juggler_sequence.cycle_walk_arch import (
    BLOCKER,
    FLOOR_ONE,
    required_excess_for_kill,
)
from research.juggler_sequence.cycle_walk_competition import dk_price

DOSSIER = Path("docs/problems/juggler_cycle_walk_arch.md")
CONJECTURE = Path("conjectures/refuted/juggler_walk_arch_kills_blocker.json")
ARTIFACT = Path("data/research/juggler/cycle_walk_arch/summary.json")
COMPETITION = Path("data/research/juggler/cycle_walk_competition/summary.json")
DP_BLOCKER = Path(
    "data/research/juggler/cycle_walk_charge/new_floor_kills/L478245.json"
)


def test_required_excess_is_negative_at_the_blocker():
    stored = json.loads(COMPETITION.read_text(encoding="utf-8"))
    row = next(r for r in stored["rows"] if int(r["length"]) == BLOCKER)
    need = required_excess_for_kill(
        BLOCKER, int(row["odd_count"]), float(row["theta"]), FLOOR_ONE + 1
    )
    # A kill at the certified floor would need C_L well below C_*.
    assert need["margin_at_cap_zero"] < 0.5
    assert need["required_excess"] < -1.0e4
    price = dk_price(
        BLOCKER, int(row["odd_count"]), 2, float(row["theta"]), FLOOR_ONE + 1
    )
    assert price["margin"] < 1.0
    assert price["dk_cap"] / price["C_star"] < 2.0e-4


def test_arch_payoff_artifact():
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    by_l = {r["length"]: r for r in payload["rows"]}
    assert BLOCKER in by_l
    blocker = by_l[BLOCKER]
    assert blocker["digit_sum"] == 2
    assert blocker["required_excess"] < -1.0e4
    assert blocker["n_star_cap_zero_above_floor"] is True
    assert blocker["n_star_cap_zero"] > FLOOR_ONE
    assert blocker["n_star_relative_drop"] < 1.0e-3
    assert blocker["cap_over_c_star"] < 2.0e-4
    # Cap-zero cannot create a kill the 2s envelope misses.
    for row in payload["rows"]:
        if row["margin_2s"] < 1.0:
            assert row["margin_cap_zero"] < 1.0
            assert row["n_star_cap_zero_above_floor"] is True
    dp = payload["blocker_dp"]
    stored = json.loads(DP_BLOCKER.read_text(encoding="utf-8"))
    assert dp["dp_excludes"] is False
    assert dp["dp_margin"] == stored["kill_margin"]
    assert dp["dp_margin"] < 0.45
    assert dp["dp_vs_dk_rel"] < 1.0e-3
    assert payload["classification"]["label"] == "WALK_ARCH_PAYOFF_DEAD"
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
    assert record["id"] == "juggler_walk_arch_kills_blocker"
    assert record["status"] == "REFUTED"
    assert record["not_a_halt_theorem"] is True
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert payload["no_new_kills"] is True
    assert payload["envelope_unchanged"] is True
    assert payload["no_arch_proof_attempt"] is True
    assert payload["not_a_halt_theorem"] is True
    assert payload["no_cycle_all_lengths"] is False
    assert payload["not_a_uniform_ratio_theorem"] is True
    assert payload["no_new_period_bound"] is True
    assert payload["no_floor_raise"] is True
