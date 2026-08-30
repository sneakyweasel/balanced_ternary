"""Leftover-class certificate harvest. Not a halt test."""

from __future__ import annotations

from pathlib import Path

from research.juggler_sequence.atlas.schema import LANGUAGE_IDS
from research.juggler_sequence.certificate_harvest import (
    CLASS_CLOSED,
    CLASS_GREEN,
    CLASS_INCOMPLETE,
    CLASS_PARK,
    EXISTING_LEAN,
    FIXTURE_E,
    FIXTURE_LEFTOVER,
    FIXTURE_OE,
    FIXTURE_OOEE,
    FORBIDDEN_NEW_API,
    FORBIDDEN_THEOREMS,
    TEST_N_MAX,
    classify,
    first_certificate,
    harvest_exact,
    lean_api_present,
    leftover_rows,
    probe_payload,
    render_markdown,
)


def test_fixtures_e_oe_ooee_leftover():
    assert first_certificate(FIXTURE_E[0])["word"] == FIXTURE_E[1]
    assert first_certificate(FIXTURE_E[0])["cls"] == "E"
    assert first_certificate(FIXTURE_OE[0])["word"] == FIXTURE_OE[1]
    assert first_certificate(FIXTURE_OE[0])["cls"] == "OE"
    assert first_certificate(FIXTURE_OOEE[0])["word"] == FIXTURE_OOEE[1]
    assert first_certificate(FIXTURE_OOEE[0])["cls"] == "OOEE"
    assert first_certificate(FIXTURE_LEFTOVER[0])["word"] == FIXTURE_LEFTOVER[1]
    assert first_certificate(FIXTURE_LEFTOVER[0])["cls"] == "leftover"


def test_exact_window_histogram():
    tables = harvest_exact(2, 20, k_max=20)
    assert tables["count_e"] == 10
    assert tables["count_oe"] + tables["count_ooee"] + tables["count_leftover"] == 9
    rows = leftover_rows(tables)
    words = {row["word"]: row for row in rows}
    assert "OOEOE" in words
    assert words["OOEOE"]["min_n"] == 9
    assert words["OOEOE"]["count"] >= 1
    assert all(row["word"] not in {"E", "OE", "OOEE"} for row in rows)


def test_tiny_window_reproduces():
    first = probe_payload()
    second = probe_payload()
    assert first["scan"]["coarse"] == second["scan"]["coarse"]
    assert first["scan"]["n_max"] == TEST_N_MAX
    assert first["scan"]["fixtures_ok"] is True
    assert first["engine_control_layer_modified"] is False
    assert first["decision"]["classification"] in {
        CLASS_CLOSED,
        CLASS_GREEN,
        CLASS_PARK,
        CLASS_INCOMPLETE,
    }
    assert first["decision"]["classification"] != CLASS_INCOMPLETE
    text = render_markdown(first)
    assert "NOT OBSERVED WITHIN SEARCH BOUND" in text
    assert "halt theorem" in text.lower()


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
    assert "LANG_HARVEST" not in LANGUAGE_IDS
    payload = probe_payload()
    assert classify(payload["scan"], lean)["classification"] == payload["decision"][
        "classification"
    ]


def test_dossier_boundary():
    repo = Path(__file__).resolve().parents[3]
    dossier = (repo / "docs" / "problems" / "juggler_certificate_harvest.md").read_text(
        encoding="utf-8"
    )
    paper = (repo / "formal" / "Problems" / "JugglerPaper.lean").read_text(
        encoding="utf-8"
    )
    schema = (repo / "src" / "research" / "juggler_sequence" / "atlas" / "schema.py").read_text(
        encoding="utf-8"
    )
    assert "## Branch budget" in dossier
    assert "## Decision" in dossier
    assert "## Publication assessment" in dossier
    assert "LANG_HARVEST" not in dossier
    assert "LANG_HARVEST" not in schema
    assert "CertificateHarvest" not in paper
    assert "theorem no_juggler_escape" not in dossier
    assert "word atlas recensus" not in dossier.lower() or "not a" in dossier.lower()
