"""Record-excursion transfer. Not a halt test."""

from __future__ import annotations

from pathlib import Path

from research.juggler_sequence.atlas.schema import LANGUAGE_IDS
from research.juggler_sequence.block_map_q import q_blocks
from research.juggler_sequence.excursion_transfer import (
    CLASS_CLOSED,
    CLASS_GREEN,
    CLASS_INCOMPLETE,
    CLASS_PARK,
    CLIMB_365,
    EXISTING_LEAN,
    FORBIDDEN_NEW_API,
    FORBIDDEN_THEOREMS,
    HARD_LABS,
    SOURCES_37,
    TEST_N_MAX,
    classify,
    excursion_chain,
    formal_c,
    lean_api_present,
    probe_payload,
    render_markdown,
    sources_of,
)
from research.juggler_sequence.odd_source_return import source_chain


def test_37_is_return_b_q_chain():
    xs = sources_of(37)
    assert xs[:3] == list(SOURCES_37)
    assert source_chain(37)[:3] == list(SOURCES_37)
    q_sources = [row["x"] for row in q_blocks(37)]
    assert q_sources[:3] == list(SOURCES_37)
    chain = excursion_chain(37)
    assert chain["rows"]
    first = chain["rows"][0]
    assert first["L"] == 37
    assert first["L_next"] == 9317
    assert first["L_a"] == 9317
    assert first["H"] >= 86818724
    assert first["r"] == 4


def test_365_climb_and_known_two_step_refutation():
    xs = sources_of(365)
    assert xs[:5] == list(CLIMB_365)
    assert 2233 > 37
    assert 1749 > 365


def test_return_a_and_b_on_37():
    rows = excursion_chain(37)["rows"]
    assert rows[0]["L_a"] == rows[0]["L_next"] == 9317
    assert any(row["L_a"] != row["L_next"] for row in rows[1:])


def test_formal_scale_bounds_r_two():
    assert formal_c(1) == 0.75
    assert formal_c(2) == 9 / 8
    assert formal_c(4) == 81 / 32


def test_tiny_window_reproduces():
    first = probe_payload()
    second = probe_payload()
    assert first["scan"]["starts"] == second["scan"]["starts"]
    assert first["scan"]["excursions"] == second["scan"]["excursions"]
    assert first["scan"]["sources_37"] == second["scan"]["sources_37"]
    assert first["scan"]["all_integer_candidates_fail"] is True
    assert first["scan"]["growth_growth"] > 0
    assert first["scan"]["return_b_is_q_on_37"] is True
    assert first["scan"]["envelope_dominated"] is True
    assert 365 in HARD_LABS
    assert first["scan"]["n_max"] == TEST_N_MAX


def test_probe_and_classify_vocabulary():
    payload = probe_payload()
    assert payload["experiment"] == "juggler_excursion_transfer"
    assert payload["engine_control_layer_modified"] is False
    assert payload["anti_overclaim"]["two_episode_descent_theorem"] is False
    assert payload["anti_overclaim"]["compensation_theorem"] is False
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
    assert "LANG_EXCURSION" not in LANGUAGE_IDS


def test_dossier_boundary():
    repo = Path(__file__).resolve().parents[3]
    dossier = (repo / "docs" / "problems" / "juggler_excursion_transfer.md").read_text(
        encoding="utf-8"
    )
    paper = (repo / "formal" / "Problems" / "JugglerPaper.lean").read_text(
        encoding="utf-8"
    )
    assert "## Branch budget" in dossier
    assert "## Decision" in dossier
    assert "## Publication assessment" in dossier
    assert "MACRO_EVENT_CLOSED" in dossier
    assert "J-two-episode-source-descent" in dossier
    assert "**CLOSE**" in dossier
    assert "ExcursionTransfer" not in paper
    assert "theorem no_juggler_escape" not in dossier
    assert "LANG_EXCURSION" not in dossier
