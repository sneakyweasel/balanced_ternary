"""Fan multi-point Attack A Phase 0. Not a halt test."""

from __future__ import annotations

import json
from pathlib import Path

from research.juggler_sequence.cycle_fan_multipoint import (
    hug_circuit_census,
    theta_float,
)
from research.juggler_sequence.cycle_finance import o_min_and_theta
from research.literature import get_reference

DOSSIER = Path("docs/problems/juggler_cycle_fan_multipoint.md")
CONJECTURE = Path("conjectures/refuted/juggler_fan_multipoint_constraints.json")
ARTIFACT = Path("data/research/juggler/cycle_fan_multipoint/summary.json")

LITERATURE_IDS = (
    "wu-wang-2014-irrationality-measure-log3",
    "salikhov-2007-irrationality-measure-ln3",
    "tao-2011-hilbert-seventh-powers-2-3",
    "chim-2025-p-adic-two-logarithms",
    "mathoverflow-2012-powers-2-3",
)


def test_hug_nineteen_is_only_short_circuits():
    odd_count, _ = o_min_and_theta(19)
    assert odd_count == 12
    census = hug_circuit_census(19, 12)
    assert census["only_short"] is True
    types = {tuple(row[:2]): row[2] for row in census["types"]}
    assert types[(1, 1)] == 2
    assert types[(2, 1)] == 5
    assert 2 * 2 + 5 * 3 == 19


def test_exponent_neighbor_of_nineteen_is_far():
    # exact: 3^12 - 2^19 = 7153, theta = 7153 / 3^12
    theta19 = 7153 / (3**12)
    ratio = theta_float(20) / theta19
    assert ratio > 20


def test_literature_records_are_registered():
    for ref_id in LITERATURE_IDS:
        rec = get_reference(ref_id)
        assert rec["id"] == ref_id
        assert rec["year"]
        assert rec["title"]


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
    assert record["id"] == "juggler_fan_multipoint_constraints"
    assert record["status"] == "REFUTED"
    assert record["not_a_halt_theorem"] is True
    assert record["counterexamples"]
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert payload["not_a_halt_theorem"] is True
    assert payload["no_new_period_bound"] is True
    assert payload["no_baker_reopen"] is True
    assert payload["no_floor_raise"] is True
    assert payload["no_paper_a_edit"] is True
    cls = payload["classification"]
    assert cls["label"] == "FAN_MULTIPOINT_CLOSED"
    assert cls["decision"] == "CLOSE"
    assert cls["hug_only_short"] is True
    assert cls["forced_second_fan_pair"] is False
    assert cls["exponent_neighbors_separated"] is True
    assert all(row["only_short"] for row in payload["hug_circuits"])
    exp = payload["exponent_neighbors"]
    assert exp["seed_50508"]["ratio_plus"] > 4e4
    assert exp["min_neighbor_ratio"] > 4e4
    assert payload["leftover_splits"]["n_two_good"] == 5
    assert "B_padic_coupling" in payload["attacks_not_opened"]
