"""Crude-envelope Phase 0. Not a halt test and not a floor raise."""

from __future__ import annotations

import json
from pathlib import Path

from research.juggler_sequence.cycle_walk_envelope import (
    HIT_CAP,
    analytic_covers,
    gap_lower,
    j_upper,
)

DOSSIER = Path("docs/problems/juggler_cycle_walk_envelope.md")
CONJECTURE = Path("conjectures/active/juggler_walk_crude_envelope.json")
REFUTED = Path("conjectures/refuted/juggler_walk_hitting_one.json")
ARTIFACT = Path("data/research/juggler/cycle_walk_envelope/summary.json")


def test_j_upper_and_analytic_cover():
    assert j_upper(17.0) < 1.0
    assert gap_lower(17.0) > 0.005
    report = analytic_covers()
    assert report["hit"] == HIT_CAP
    assert report["covers"] is True
    assert report["binning_excess"] < report["gap_lower"]


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
    assert record["id"] == "juggler_walk_crude_envelope"
    assert record["status"] == "ACTIVE"
    refuted = json.loads(REFUTED.read_text(encoding="utf-8"))
    assert refuted["id"] == "juggler_walk_hitting_one"
    assert refuted["status"] == "REFUTED"
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert payload["not_a_halt_theorem"] is True
    assert payload["no_cycle_all_lengths"] is False
    assert payload["not_a_uniform_ratio_theorem"] is True
    assert payload["classification"]["label"] == "WALK_ENVELOPE_GREEN"
    assert payload["survey"]["all_within_one"] is False
    assert payload["survey"]["all_within_cap"] is True
    assert payload["survey"]["n_envelope_kills"] == 18
    assert payload["survey"]["uniform_ratio_false"] is True
    assert payload["survey"]["margin_50508"] > 1.0
    assert payload["survey"]["margin_176251"] < 1.0
    assert payload["survey"]["max_over"] > 1.0
    assert payload["survey"]["max_over"] <= HIT_CAP
