"""Mechanical-charge Phase 0. Not a halt test and not a floor raise."""

from __future__ import annotations

import json
import math
from pathlib import Path

from research.juggler_sequence.cycle_christoffel import christoffel_word
from research.juggler_sequence.cycle_walk_excursion import replay_charge
from research.juggler_sequence.cycle_walk_mechanical import (
    christoffel_charge,
    greedy_word,
    prefix_dominance_holds,
)

DOSSIER = Path("docs/problems/juggler_cycle_walk_mechanical.md")
CONJECTURE = Path("conjectures/refuted/juggler_walk_christoffel_prefix.json")
ARTIFACT = Path("data/research/juggler/cycle_walk_mechanical/summary.json")


def test_prefix_min_holds_on_leftover_nineteen():
    assert prefix_dominance_holds(19, 12)["holds"] is True
    assert greedy_word(19, 12) == christoffel_word(19, 12)


def test_prefix_min_fails_at_four_three():
    dom = prefix_dominance_holds(4, 3)
    assert dom["holds"] is False
    assert greedy_word(4, 3) == "OOEO"
    assert christoffel_word(4, 3) == "OOOE"
    assert greedy_word(4, 3) != christoffel_word(4, 3)


def test_christoffel_charge_matches_replay():
    word = christoffel_word(19, 12)
    streamed = christoffel_charge(19, 12, 1000)
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
    assert "CLOSE" in dossier.split("## Decision", 1)[1].split("## ", 1)[0]
    assert "not claimed" in dossier
    record = json.loads(CONJECTURE.read_text(encoding="utf-8"))
    assert record["id"] == "juggler_walk_christoffel_prefix"
    assert record["status"] == "REFUTED"
    assert record["counterexamples"]
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert payload["not_a_halt_theorem"] is True
    assert payload["no_cycle_all_lengths"] is False
    assert payload["not_a_uniform_ratio_theorem"] is True
    assert payload["classification"]["label"] == "WALK_MECHANICAL_CLOSED"
    assert payload["survey_compare"]["uniform_ratio_false"] is True
    seeds = [50508, 101016, 151524, 176251]
    by_l = {row["length"]: row for row in payload["survey_rows"]}
    for length in seeds:
        assert by_l[length]["relative_mismatch"] < 1e-14
    assert payload["survey_compare"]["max_relative_mismatch"] > 1e-4
