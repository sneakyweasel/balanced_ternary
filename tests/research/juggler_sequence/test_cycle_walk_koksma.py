"""Koksma +1/L Phase 0. Not a halt test and not a floor raise."""

from __future__ import annotations

import json
from pathlib import Path

DOSSIER = Path("docs/problems/juggler_cycle_walk_koksma.md")
CONJECTURE = Path("conjectures/refuted/juggler_walk_koksma_one_over_L.json")
ARTIFACT = Path("data/research/juggler/cycle_walk_koksma/summary.json")


def test_plus_one_over_L_fails_on_offsets_and_holds_on_seeds():
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    by_l = {row["length"]: row for row in payload["rows"]}
    seed = by_l[50508]
    assert seed["seed"] is True
    assert seed["plus_1_over_L_hug"] is True
    assert seed["excess_hug_times_L"] < 0.5
    worst = by_l[180467]
    assert worst["plus_1_over_L_hug"] is False
    assert worst["plus_1_over_L_iet"] is False
    assert worst["excess_hug_times_L"] > 1.0
    assert abs(worst["iet_minus_hug"]) < 1e-10


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
    assert "not claimed" in dossier
    record = json.loads(CONJECTURE.read_text(encoding="utf-8"))
    assert record["id"] == "juggler_walk_koksma_one_over_L"
    assert record["status"] == "REFUTED"
    assert record["counterexamples"]
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert payload["not_a_halt_theorem"] is True
    assert payload["no_cycle_all_lengths"] is False
    assert payload["not_a_uniform_ratio_theorem"] is True
    assert payload["classification"]["label"] == "WALK_KOKSMA_CLOSED"
    assert payload["survey"]["n_plus1_hug"] < payload["survey"]["n_rows"]
    assert payload["survey"]["n_below_bound"] == payload["survey"]["n_rows"]
    assert 180467 in payload["survey"]["plus1_hug_failures"]
