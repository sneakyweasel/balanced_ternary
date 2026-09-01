"""Greedy-hug Phase 0. Not a halt test and not a floor raise."""

from __future__ import annotations

import json
import math
from pathlib import Path

from research.juggler_sequence.cycle_christoffel import christoffel_word
from research.juggler_sequence.cycle_walk_excursion import replay_charge
from research.juggler_sequence.cycle_walk_greedy import hug_charge, hug_word
from research.juggler_sequence.cycle_walk_mechanical import (
    greedy_word,
    prefix_min_odds,
)

DOSSIER = Path("docs/problems/juggler_cycle_walk_greedy.md")
CONJECTURE = Path("conjectures/active/juggler_walk_greedy_prefix.json")
ARTIFACT = Path("data/research/juggler/cycle_walk_greedy/summary.json")


def test_hug_is_prefix_min_at_four_three():
    assert hug_word(4, 3) == "OOEO"
    assert hug_word(4, 3) == greedy_word(4, 3)
    assert hug_word(4, 3) != christoffel_word(4, 3)
    assert prefix_min_odds(4, 3) == [0, 1, 2, 2, 3]


def test_hug_is_prefix_min_on_leftover_nineteen():
    assert hug_word(19, 12) == greedy_word(19, 12)
    assert hug_word(19, 12) == christoffel_word(19, 12)
    hugged = hug_word(19, 12)
    odds = [0]
    count = 0
    for letter in hugged:
        if letter == "O":
            count += 1
        odds.append(count)
    assert odds == prefix_min_odds(19, 12)


def test_hug_charge_matches_replay():
    word = hug_word(19, 12)
    streamed = hug_charge(19, 12, 1000)
    replayed = replay_charge(word, 1000)
    assert math.isclose(streamed, replayed, rel_tol=1e-12)


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
    assert record["id"] == "juggler_walk_greedy_prefix"
    assert record["status"] == "ACTIVE"
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert payload["not_a_halt_theorem"] is True
    assert payload["no_cycle_all_lengths"] is False
    assert payload["not_a_uniform_ratio_theorem"] is True
    assert payload["classification"]["label"] == "WALK_GREEDY_GREEN"
    assert payload["census"]["n_prefix_min"] == payload["census"]["n_feasible"]
    assert payload["survey_compare"]["all_match"] is True
    assert payload["survey_compare"]["max_relative_mismatch"] < 1e-9
    assert payload["survey_compare"]["uniform_ratio_false"] is True
    assert payload["classification"]["c_relative_spread_vs_mechanical"] < 2.5e-3
