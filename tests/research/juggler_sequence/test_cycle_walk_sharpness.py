"""DK sharpness Phase 0. Not a halt test and not an envelope edit."""

from __future__ import annotations

import json
import math
from pathlib import Path

from research.juggler_sequence.cycle_walk_sharpness import (
    representative_log_n,
)

DOSSIER = Path("docs/problems/juggler_cycle_walk_sharpness.md")
CONJECTURE = Path("conjectures/active/juggler_walk_excess_arch.json")
ARTIFACT = Path("data/research/juggler/cycle_walk_sharpness/summary.json")


def test_representative_base():
    assert math.isclose(representative_log_n(), 17.0826, abs_tol=1e-3)


def test_sharpness_artifact():
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    rep = payload["report"]
    assert -0.3 < rep["excess_min"] < 0.0
    assert 4.9 < rep["max_abs_excess"] < 5.0
    assert rep["window_max_ratio_to_2s"] < 0.5
    assert rep["overall_max_ratio_to_2s"] < 0.5
    # Saturation: the 1054-tower dominates, later levels add little.
    running = rep["running_max_abs_at"]
    assert running["301993"] < 1.1 * running["24727"]
    # The three structural laws fail.
    assert abs(rep["alt_fit_window"]["pearson_r"]) < 0.5
    assert rep["digit_fit"]["r_squared"] < 0.5
    assert rep["collapse_fails"] is True
    # Arch shape along the 1054-tower.
    tower = rep["towers"]["1054"]
    assert tower[11] > 2.9
    assert abs(tower[23]) < 0.1
    assert payload["leftover_cross_check"]["max_abs_diff"] < 1e-3
    assert payload["classification"]["label"] == "WALK_SHARPNESS_BOUNDED"


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
    assert "PARK" in decision
    assert "not claimed" in dossier
    record = json.loads(CONJECTURE.read_text(encoding="utf-8"))
    assert record["id"] == "juggler_walk_excess_arch"
    assert record["status"] == "COMPUTATIONALLY_SUPPORTED"
    assert record["not_a_halt_theorem"] is True
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert payload["no_new_kills"] is True
    assert payload["envelope_unchanged"] is True
    assert payload["not_a_halt_theorem"] is True
    assert payload["no_cycle_all_lengths"] is False
    assert payload["not_a_uniform_ratio_theorem"] is True
