"""Formal vs realized AboveAnchor language. Not a halt test."""

from __future__ import annotations

from pathlib import Path

from research.juggler_sequence.atlas.schema import LANGUAGE_IDS
from research.juggler_sequence.formal_realized_gap import (
    CLASS_CLOSED,
    CLASS_GREEN,
    CLASS_INCOMPLETE,
    CLASS_PARK,
    EXISTING_LEAN,
    FORBIDDEN_NEW_API,
    FORBIDDEN_THEOREMS,
    LEFTOVERS,
    TEST_K_MAX,
    TEST_N_MAX,
    WITNESS_STARTS,
    classify,
    formal_by_length,
    is_formal,
    lean_api_present,
    leftover_aa_words,
    probe_payload,
    render_markdown,
    run_probe,
    walk_aa,
)
from research.juggler_sequence.minimum_relative import above_anchor
from research.juggler_sequence.near_extremal_prefixes import prefix_nc_words
from research.juggler_sequence.parity_balance import prefix_survives


def test_formal_membership_matches_prefix_envelope():
    assert is_formal("O") is True
    assert is_formal("OO") is True
    assert is_formal("OOE") is True
    assert is_formal("O" * 8) is True
    assert is_formal("O" * 7 + "E") is True
    assert is_formal("E") is False
    assert is_formal("OE") is False
    assert is_formal("OOEE") is False
    assert is_formal("OOEOE") is False
    for word in ("O", "OOE", "OOOOE", "O" * 6 + "E"):
        assert is_formal(word) == prefix_survives(word)


def test_formal_enumeration_is_prefix_nc():
    by_len = formal_by_length(8)
    expected = prefix_nc_words(8)
    flat = [word for length in range(1, 9) for word in by_len[length]]
    assert sorted(flat) == sorted(expected)
    assert by_len[1] == ["O"]
    assert "E" not in by_len[1]
    assert "OE" not in by_len[2]


def test_leftover_and_witness_aa_prefixes_are_formal():
    rows = leftover_aa_words(TEST_K_MAX)
    for n in WITNESS_STARTS:
        row = rows[str(n)]
        assert row["formal"] is True
        assert row["above_anchor"] is True
        if row["word"]:
            assert is_formal(row["word"]) is True
            assert above_anchor(n, row["word"]) is True
    packed, depth = walk_aa(365, 8)
    assert depth >= 3
    assert packed & 1 == 1


def test_tiny_window_gap_is_reproducible():
    first = run_probe(k_max=TEST_K_MAX, n_max=TEST_N_MAX)
    second = run_probe(k_max=TEST_K_MAX, n_max=TEST_N_MAX)
    assert first["gaps"] == second["gaps"]
    assert first["n_minimal"] == second["n_minimal"]
    assert first["minimal_by_length"] == second["minimal_by_length"]
    assert first["extra_aa_not_formal"] == 0
    assert first["leftover_formal"] is True
    last = first["last"]
    assert last["N"] == TEST_K_MAX
    assert last["formal"] > 0
    assert 0.0 <= last["R_N"] <= 1.0
    assert last["dead"] == last["formal"] - last["realized_aa"]
    for n in LEFTOVERS:
        assert str(n) in first["leftover_S"]


def test_probe_and_classify_are_in_vocabulary():
    payload = probe_payload(k_max=TEST_K_MAX, n_max=TEST_N_MAX)
    assert payload["experiment"] == "juggler_formal_realized_gap"
    assert payload["engine_control_layer_modified"] is False
    assert payload["scan"]["halt_theorem"] is False
    assert payload["scan"]["cyclemin_in_language"] is False
    assert payload["scan"]["new_atlas_language"] is False
    assert payload["anti_overclaim"]["global_non_realizability"] is False
    assert payload["anti_overclaim"]["forbidden_factor_theorem"] is False
    assert payload["anti_overclaim"]["search_horizon_is_L"] is False
    assert payload["decision"]["classification"] in {
        CLASS_CLOSED,
        CLASS_GREEN,
        CLASS_PARK,
        CLASS_INCOMPLETE,
    }
    text = render_markdown(payload)
    assert "NOT_OBSERVED_WITHIN_BOUND" in text
    assert payload["decision"]["classification"] != CLASS_INCOMPLETE
    lean = lean_api_present()
    decision = classify(payload["scan"], lean)
    assert decision["classification"] == payload["decision"]["classification"]


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
    assert lean["no_atlas_lang_formal"] is True


def test_no_new_atlas_language_tag():
    assert "LANG_FORMAL" not in LANGUAGE_IDS
    assert "LANG_ABOVE_ANCHOR" not in LANGUAGE_IDS
    schema = (
        Path(__file__).resolve().parents[3]
        / "src"
        / "research"
        / "juggler_sequence"
        / "atlas"
        / "schema.py"
    ).read_text(encoding="utf-8")
    assert "LANG_FORMAL" not in schema
    assert "LANG_ABOVE_ANCHOR" not in schema


def test_dossier_boundary():
    repo = Path(__file__).resolve().parents[3]
    dossier = (repo / "docs" / "problems" / "juggler_formal_realized_gap.md").read_text(
        encoding="utf-8"
    )
    paper = (repo / "formal" / "Problems" / "JugglerPaper.lean").read_text(
        encoding="utf-8"
    )
    assert "## Branch budget" in dossier
    assert "## Decision" in dossier
    assert "## Publication assessment" in dossier
    assert "prefixNoncontracting" in dossier
    assert "JUGGLER_LANGUAGE_IS_KNOWN_GRAMMAR" in dossier
    assert "**CLOSE**" in dossier
    assert "FormalLanguage" not in paper
    assert "theorem no_juggler_escape" not in dossier
    assert "LANG_FORMAL" not in dossier
