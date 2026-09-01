"""DK/Ostrowski envelope Phase 0. Not a halt test and not a floor raise."""

from __future__ import annotations

import json
from pathlib import Path

from research.juggler_sequence.cycle_walk_greedy import hug_word
from research.juggler_sequence.cycle_walk_ostrowski import (
    exact_hug_word,
    greedy_digits,
)

DOSSIER = Path("docs/problems/juggler_cycle_walk_ostrowski.md")
CONJECTURE = Path("conjectures/proved/juggler_walk_dk_envelope.json")
ARTIFACT = Path("data/research/juggler/cycle_walk_ostrowski/summary.json")


def test_greedy_digits_and_exact_word():
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    denominators = payload["theta_cf"]["denominators"]
    assert denominators[-1] == 176_251
    assert 50_508 in denominators and 1_054 in denominators
    assert greedy_digits(50_508, denominators)["digit_sum"] == 1
    assert greedy_digits(154_686, denominators)["digit_sum"] == 6
    assert greedy_digits(180_467, denominators)["digit_sum"] == 5
    assert all(
        greedy_digits(row["length"], denominators)["exact"]
        for row in payload["rows"]
    )
    word, odds = exact_hug_word(19)
    assert odds == 12
    assert word == hug_word(19, 12)


def test_dk_envelope_artifact():
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert payload["x_certification"]["certified"] is True
    survey = payload["survey"]
    assert survey["all_greedy_exact"] is True
    assert survey["all_word_match"] is True
    assert survey["all_odds_match"] is True
    assert survey["all_within_dk"] is True
    assert survey["all_cap_below_gap"] is True
    assert survey["max_digit_sum"] <= 6
    assert 1.0 < survey["max_excess_times_L"] < 2.0
    assert survey["n_dk_kills"] == 18
    assert survey["margin_dk_50508"] > 1.0
    assert survey["margin_dk_176251"] < 1.0
    assert survey["uniform_ratio_false"] is True
    assert payload["classification"]["label"] == "WALK_OSTROWSKI_GREEN"


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
    assert record["id"] == "juggler_walk_dk_envelope"
    assert record["status"] == "EXACT — HUMAN PROOF"
    assert record["not_a_halt_theorem"] is True
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert payload["not_a_halt_theorem"] is True
    assert payload["no_cycle_all_lengths"] is False
    assert payload["not_a_uniform_ratio_theorem"] is True
