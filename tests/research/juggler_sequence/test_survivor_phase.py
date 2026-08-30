"""Survivor rounding-phase census. Not a halt test."""

from __future__ import annotations

from pathlib import Path

from research.juggler_sequence.atlas.schema import LANGUAGE_IDS
from research.juggler_sequence.survivor_phase import (
    CLASS_CLOSED,
    CLASS_GREEN,
    CLASS_INCOMPLETE,
    CLASS_PARK,
    EXISTING_LEAN,
    FORBIDDEN_NEW_API,
    FORBIDDEN_THEOREMS,
    HARD_LABS,
    TEST_N_MAX,
    classify,
    floor_phase,
    lean_api_present,
    probe_payload,
    render_markdown,
    walk_phases,
)


def test_phase_identities():
    y, defect, u, odd = floor_phase(5)
    assert odd is True
    assert y == 11
    assert defect == 4
    assert abs(u - 4 / 23) < 1e-12
    _y, d225, u225, odd225 = floor_phase(225)
    assert odd225 is True
    assert d225 == 0
    assert u225 == 0.0
    _ye, de, ue, odde = floor_phase(8)
    assert odde is False
    assert de == 4
    assert abs(ue - 4 / 5) < 1e-12
    assert 0.0 <= floor_phase(37)[2] < 1.0


def test_37_walk_hits_odd_square_and_survives():
    walked = walk_phases(37)
    assert walked["S"] >= 9
    assert walked["status"] == "RETURNED"
    us = [row[0] for row in walked["trace"]]
    assert any(abs(u) < 1e-12 for u in us)
    assert 365 in HARD_LABS
    assert 33391 in HARD_LABS


def test_tiny_window_reproduces():
    first = probe_payload()
    second = probe_payload()
    assert first["scan"]["starts"] == second["scan"]["starts"]
    assert first["scan"]["s_counts"] == second["scan"]["s_counts"]
    assert first["scan"]["u_225"] == 0.0
    assert first["scan"]["n_max"] == TEST_N_MAX
    assert first["scan"]["fills_unit_interval"] in (True, False)


def test_probe_and_classify_vocabulary():
    payload = probe_payload()
    assert payload["experiment"] == "juggler_survivor_phase"
    assert payload["engine_control_layer_modified"] is False
    assert payload["anti_overclaim"]["histogram_is_theorem"] is False
    assert payload["anti_overclaim"]["pvalue_is_theorem"] is False
    assert payload["decision"]["classification"] in {
        CLASS_CLOSED,
        CLASS_GREEN,
        CLASS_PARK,
        CLASS_INCOMPLETE,
    }
    assert payload["decision"]["classification"] != CLASS_INCOMPLETE
    text = render_markdown(payload)
    assert "NOT_OBSERVED_WITHIN_BOUND" in text
    lean = lean_api_present()
    assert classify(payload["scan"], lean)["classification"] == payload["decision"][
        "classification"
    ]


def test_lean_api_without_new_layer():
    lean = lean_api_present()
    assert lean["sorry_free"] is True
    for name in EXISTING_LEAN:
        assert lean[name] is True, name
    for name in FORBIDDEN_THEOREMS:
        assert lean[f"has_{name}"] is False, name
    for name in FORBIDDEN_NEW_API:
        assert lean[f"has_api_{name}"] is False, name
    assert lean["new_lean_file"] is False
    assert lean["not_in_paper_barrel"] is True
    assert lean["no_atlas_lang"] is True
    assert "LANG_PHASE" not in LANGUAGE_IDS


def test_dossier_boundary():
    repo = Path(__file__).resolve().parents[3]
    dossier = (repo / "docs" / "problems" / "juggler_survivor_phase.md").read_text(
        encoding="utf-8"
    )
    paper = (repo / "formal" / "Problems" / "JugglerPaper.lean").read_text(
        encoding="utf-8"
    )
    assert "## Branch budget" in dossier
    assert "## Decision" in dossier
    assert "## Publication assessment" in dossier
    assert "EXCURSION_TRANSFER_CLOSED" in dossier
    assert "J-mixed-oe-defect-gap" in dossier
    assert "**CLOSE**" in dossier
    assert "FloorPhase" not in paper
    assert "theorem no_juggler_escape" not in dossier
    assert "LANG_PHASE" not in dossier
