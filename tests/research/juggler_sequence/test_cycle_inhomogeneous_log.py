"""Inhomogeneous Wu-Wang third-coefficient Phase 0. Not a halt test."""

from __future__ import annotations

import json
import math
from pathlib import Path

from research.juggler_sequence.cycle_inhomogeneous_log import (
    lambda_from_theta,
    seed_row,
)

DOSSIER = Path("docs/problems/juggler_cycle_inhomogeneous_log.md")
CONJECTURE = Path(
    "conjectures/refuted/juggler_inhomogeneous_ww_beats_finance.json"
)
ARTIFACT = Path("data/research/juggler/cycle_inhomogeneous_log/summary.json")


def test_lambda_matches_nineteen_gap():
    theta = 7153 / (3**12)
    lam = lambda_from_theta(theta)
    assert abs(lam - (12 * math.log(3.0) - 19 * math.log(2.0))) < 1e-14
    row = seed_row(19, 12, theta)
    assert row["obeys_integer_gap"] is True
    assert row["homogeneous_smallest"] is True
    assert abs(row["min_inhomogeneous"] - (1.0 - lam)) < 1e-14


def test_inhomogeneous_artifact():
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    by_l = {r["length"]: r for r in payload["seeds"]}
    assert set(by_l) == {19, 84, 569, 1054, 25781, 50508, 176251}
    for row in payload["seeds"]:
        assert row["obeys_integer_gap"] is True
        assert row["homogeneous_smallest"] is True
        assert row["clearing"]["form_over_ww"] > 1e6
    nineteen = by_l[19]
    assert nineteen["min_inhomogeneous"] > 0.98
    assert nineteen["clearing"]["k"] == 74
    assert payload["classification"]["label"] == "INHOMOGENEOUS_LOG_CLOSED"
    assert payload["classification"]["decision"] == "CLOSE"


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
    decision = dossier.split("## Decision", 1)[1].split("## ", 1)[0]
    assert "CLOSE" in decision
    assert "PROMOTE" not in decision
    assert "not claimed" in dossier
    record = json.loads(CONJECTURE.read_text(encoding="utf-8"))
    assert record["id"] == "juggler_inhomogeneous_ww_beats_finance"
    assert record["status"] == "REFUTED"
    assert record["not_a_halt_theorem"] is True
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert payload["not_a_halt_theorem"] is True
    assert payload["no_baker_reopen"] is True
    assert payload["no_new_period_bound"] is True
