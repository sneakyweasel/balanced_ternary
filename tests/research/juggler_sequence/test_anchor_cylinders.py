"""Nested AboveAnchor start-sets. Not a halt test."""

from __future__ import annotations

from pathlib import Path

from research.juggler_sequence.anchor_cylinders import (
    CLASS_CLOSED,
    CLASS_GREEN,
    CLASS_INCOMPLETE,
    CLASS_PARK,
    EXISTING_LEAN,
    FORBIDDEN_NEW_API,
    FORBIDDEN_THEOREMS,
    HARD_LABS,
    TEST_K_MAX,
    TEST_WINDOWS,
    classify,
    hard_word,
    lean_api_present,
    probe_payload,
    render_markdown,
    run_probe,
)
from research.juggler_sequence.atlas.schema import LANGUAGE_IDS
from research.juggler_sequence.formal_realized_gap import walk_aa
from research.juggler_sequence.minimum_relative import above_anchor


def test_r_and_a_are_distinct_on_oe():
    scan = run_probe(k_max=TEST_K_MAX, windows=TEST_WINDOWS)
    assert scan["oe_a_empty"] is True
    assert scan["oe_r_positive"] is True
    assert scan["oe"]["a_count"] == 0
    assert scan["oe"]["r_count"] > 0
    assert scan["ooe"]["a_count"] > 0
    assert scan["ooe"]["a_min"] == 5


def test_nested_support_is_monotone_on_365():
    scan = run_probe(k_max=TEST_K_MAX, windows=TEST_WINDOWS)
    lab = next(row for row in scan["labs_detail"] if row["n"] == 365)
    rows = lab["by_X"]["400"]["rows"]
    assert lab["word"].startswith("OOE")
    counts = [row["a_count"] for row in rows]
    assert counts == sorted(counts, reverse=True)
    assert all(row["a_count"] <= row["r_count"] for row in rows)
    assert above_anchor(365, lab["word"]) is True


def test_hard_word_matches_walk_aa():
    packed, depth = walk_aa(37, TEST_K_MAX)
    from research.juggler_sequence.atlas.packed import unpack_word

    assert hard_word(37, TEST_K_MAX) == (unpack_word(depth, packed) if depth else "")
    assert 365 in HARD_LABS
    assert 33391 in HARD_LABS


def test_child_sum_does_not_exceed_parent():
    scan = run_probe(k_max=TEST_K_MAX, windows=TEST_WINDOWS)
    for row in scan["siblings"]:
        if "parent" in row:
            assert row["child_sum"] <= row["parent"]


def test_tiny_window_reproduces():
    first = run_probe(k_max=TEST_K_MAX, windows=TEST_WINDOWS)
    second = run_probe(k_max=TEST_K_MAX, windows=TEST_WINDOWS)
    assert first["oe"] == second["oe"]
    assert first["ooe"] == second["ooe"]
    assert first["M_k"] == second["M_k"]
    assert first["extra_aa_not_formal"] == 0


def test_probe_and_classify_vocabulary():
    payload = probe_payload()
    assert payload["experiment"] == "juggler_anchor_cylinders"
    assert payload["engine_control_layer_modified"] is False
    assert payload["anti_overclaim"]["A_w_empty_from_window"] is False
    assert payload["anti_overclaim"]["density_theorem"] is False
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
    assert "LANG_ANCHOR" not in LANGUAGE_IDS


def test_dossier_boundary():
    repo = Path(__file__).resolve().parents[3]
    dossier = (repo / "docs" / "problems" / "juggler_anchor_cylinders.md").read_text(
        encoding="utf-8"
    )
    paper = (repo / "formal" / "Problems" / "JugglerPaper.lean").read_text(
        encoding="utf-8"
    )
    assert "## Branch budget" in dossier
    assert "## Decision" in dossier
    assert "## Publication assessment" in dossier
    assert "A_w" in dossier
    assert "FORMAL_REALIZED_GAP_CLOSED" in dossier
    assert "**CLOSE**" in dossier
    assert "AnchorCylinder" not in paper
    assert "theorem no_juggler_escape" not in dossier
