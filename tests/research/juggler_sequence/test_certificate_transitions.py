"""Certificate-transition iterator. Not a halt test."""

from __future__ import annotations

from pathlib import Path

from research.juggler_sequence.atlas.schema import LANGUAGE_IDS
from research.juggler_sequence.certificate_transitions import (
    CLASS_CLOSED,
    CLASS_GREEN,
    CLASS_INCOMPLETE,
    CLASS_PARK,
    EXISTING_LEAN,
    FORBIDDEN_NEW_API,
    FORBIDDEN_THEOREMS,
    LABS,
    TEST_N_MAX,
    classify,
    first_is_q_itinerary,
    iterate_certificates,
    lean_api_present,
    one_certificate,
    probe_payload,
    render_markdown,
    semantic_class,
)


def test_uniform_and_residual_labels():
    assert one_certificate(6)["cls"] == "E"
    assert one_certificate(7)["cls"] == "OE"
    assert one_certificate(5)["cls"] == "OOEE"
    assert one_certificate(9)["cls"] == "R"
    assert semantic_class("leftover") == "R"
    assert first_is_q_itinerary(9)
    assert first_is_q_itinerary(37)


def test_residual_landing_is_descent():
    step = one_certificate(9)
    assert step["landing"] < 9
    assert step["word"] == step["path_word"]
    chain = iterate_certificates(9)
    assert chain["classes"][0] == "R"
    assert chain["reached_one"] is True
    assert all(chain["seq"][i]["landing"] < chain["seq"][i]["n"] for i in range(len(chain["seq"])))


def test_labs_have_certificate_sequences():
    for n in (37, 365, 501):
        chain = iterate_certificates(n)
        assert chain["classes"]
        assert chain["classes"][0] == "R"
        assert chain["reached_one"] is True
        assert 37 in LABS


def test_tiny_window_reproduces():
    first = probe_payload()
    second = probe_payload()
    assert first["scan"]["scan"]["first_counts"] == second["scan"]["scan"]["first_counts"]
    assert first["scan"]["n_max"] == TEST_N_MAX
    assert first["scan"]["q_identity_all"] is True
    assert first["scan"]["every_descent_is_fp"] is True
    assert first["decision"]["classification"] in {
        CLASS_CLOSED,
        CLASS_GREEN,
        CLASS_PARK,
        CLASS_INCOMPLETE,
    }
    assert first["decision"]["classification"] != CLASS_INCOMPLETE
    text = render_markdown(first)
    assert "NOT OBSERVED WITHIN SEARCH BOUND" in text
    assert "finiteProgress_of_imageLt" in text


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
    assert "LANG_CERT_TRANS" not in LANGUAGE_IDS
    payload = probe_payload()
    assert classify(payload["scan"], lean)["classification"] == payload["decision"][
        "classification"
    ]


def test_dossier_boundary():
    repo = Path(__file__).resolve().parents[3]
    dossier = (repo / "docs" / "problems" / "juggler_certificate_transitions.md").read_text(
        encoding="utf-8"
    )
    paper = (repo / "formal" / "Problems" / "JugglerPaper.lean").read_text(
        encoding="utf-8"
    )
    assert "## Branch budget" in dossier
    assert "## Decision" in dossier
    assert "## Publication assessment" in dossier
    assert "LANG_CERT_TRANS" not in dossier
    assert "CertificateAutomaton" not in paper
    assert "theorem no_juggler_escape" not in dossier
