"""Uniform window envelope Phase 0. Not a halt test and not a floor raise."""

from __future__ import annotations

import json
from pathlib import Path

from research.juggler_sequence.cycle_walk_greedy import hug_word
from research.juggler_sequence.cycle_walk_ostrowski import exact_hug_word
from research.juggler_sequence.cycle_walk_window import o_min

DOSSIER = Path("docs/problems/juggler_cycle_walk_window.md")
CONJECTURE = Path("conjectures/proved/juggler_walk_window_envelope.json")
ARTIFACT = Path("data/research/juggler/cycle_walk_window/summary.json")


def test_o_min_and_word_identity_small():
    assert o_min(19) == 12
    assert o_min(50_508) == 31_867
    assert o_min(176_251) == 111_202
    word, odds = exact_hug_word(1_054)
    assert odds == o_min(1_054) == 665
    assert word == hug_word(1_054, 665)


def test_window_artifact():
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert payload["x_certification"]["certified"] is True
    scan = payload["scan"]
    assert scan["window"] == [50_508, 301_994]
    assert scan["caps_ok"] is True
    assert scan["max_digit_sum"] == 37
    assert scan["max_digit_sum"] <= scan["cap_sum"] == 47
    assert scan["all_below_gap"] is True
    assert scan["max_ratio"] < 0.2
    assert scan["min_envelope_margin"] > 5.0
    assert scan["max_digit_per_level"]["1054"] == 23
    assert payload["word_identity"]["all_match"] is True
    assert payload["classification"]["label"] == "WALK_WINDOW_GREEN"


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
    assert "no new kills" in dossier.lower()
    record = json.loads(CONJECTURE.read_text(encoding="utf-8"))
    assert record["id"] == "juggler_walk_window_envelope"
    assert record["status"] == "EXACT — HUMAN PROOF"
    assert record["not_a_halt_theorem"] is True
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert payload["no_new_kills"] is True
    assert payload["not_a_halt_theorem"] is True
    assert payload["no_cycle_all_lengths"] is False
    assert payload["not_a_uniform_ratio_theorem"] is True
