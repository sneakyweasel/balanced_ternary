"""Affine n-gap diagnostic Phase 0. Not a halt test."""

from __future__ import annotations

import json
from pathlib import Path

from research.juggler_sequence.cycle_affine_n_gap import (
    LSTAR,
    LSTEP,
    NINETEEN_GAP,
    OSTAR,
    OSTEP,
    dominance_nineteen,
    identity_table,
    lattice_point,
    reading_table,
)

DOSSIER = Path("docs/problems/juggler_cycle_affine_n_gap.md")
CONJECTURE = Path(
    "conjectures/refuted/juggler_affine_n_gap_escapes_dominance.json"
)
ARTIFACT = Path("data/research/juggler/cycle_affine_n_gap/summary.json")


def test_lattice_matches_lean_families():
    assert LSTAR * OSTEP - LSTEP * OSTAR == 1
    assert lattice_point(1, 0) == (25781, 16266)
    assert lattice_point(2, -1) == (50508, 31867)
    assert lattice_point(3, -1) == (76289, 48133)


def test_nineteen_dominance_lock():
    assert NINETEEN_GAP == 7153
    row = dominance_nineteen()
    assert row["n_max_exact"] == 297
    assert row["n_max_weaker"] >= 297
    assert row["n_max_half"] > 297
    assert row["dominance_holds"] is True
    assert row["half_gap_strictly_worse"] is True
    assert row["theta_depends_only_on_L_o"] is True


def test_identity_and_reading_tags_are_closed():
    closed = {"REPARAMETERIZATION", "KNOWN", "REFUTED"}
    identities = identity_table()
    assert {i["id"] for i in identities} == {
        "cycleMin_finance",
        "global_defect_identity",
        "image_eq_start_defectRatio",
        "exponent_budget",
        "inhomogeneous_p_plus_lambda",
        "height_position_finance",
    }
    for item in identities:
        assert item["tag"] in closed
        assert item["tag"] != "NEW"
    n_forms = [i for i in identities if i["uses_n"]]
    assert all(
        i["kind"] in {"upper_bound_on_G", "return_identity", "upper_bound_on_theta"}
        for i in n_forms
    )
    readings = reading_table()
    assert {r["id"] for r in readings} == {"R1", "R2", "R3", "R4", "R5"}
    assert all(r["status"] in closed for r in readings)


def test_affine_n_gap_artifact():
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    by_l = {r["length"]: r for r in payload["seeds"]}
    assert set(by_l) == {19, 25781, 50508, 76289, 478245}
    assert by_l[25781]["family"] == "F1"
    assert by_l[50508]["family"] == "F2"
    assert by_l[76289]["family"] == "F3"
    assert by_l[478245]["family"] == "fanA_k1"
    assert by_l[19]["odd_count"] == 12
    assert by_l[25781]["odd_count"] == 16266
    assert by_l[50508]["odd_count"] == 31867
    assert by_l[76289]["odd_count"] == 48133
    assert by_l[478245]["odd_count"] == 301739
    for row in payload["seeds"]:
        assert row["dominance_holds"] is True
        assert row["theta_depends_only_on_L_o"] is True
        assert row["lattice_matches"] is True
    assert payload["lattice"]["unimodular"] == 1
    nineteen = payload["dominance_nineteen"]
    assert nineteen["n_max_exact"] == 297
    assert nineteen["half_gap_strictly_worse"] is True
    assert payload["classification"]["label"] == "AFFINE_N_GAP_CLOSED"
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
    assert "no successor" in dossier.lower() or "not a fan-minimum successor" in dossier
    record = json.loads(CONJECTURE.read_text(encoding="utf-8"))
    assert record["id"] == "juggler_affine_n_gap_escapes_dominance"
    assert record["status"] == "REFUTED"
    assert record["not_a_halt_theorem"] is True
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert payload["not_a_halt_theorem"] is True
    assert payload["no_baker_reopen"] is True
    assert payload["no_floor_raise"] is True
    assert payload["no_fan_minimum_successor"] is True
    assert payload["no_new_period_bound"] is True
