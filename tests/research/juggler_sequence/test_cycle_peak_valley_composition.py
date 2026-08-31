"""Peak–valley interval composition. Not a halt test."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from research.conjectures import get_conjecture
from research.juggler_sequence.cycle_peak_valley_composition import (
    WORD_L11,
    WORD_OOE,
    WORD_OOOEE,
    WORD_TWO_OOE,
    blocks_exponent,
    composite_exponent,
    exact_peak_composite,
    exact_valley_composite,
    first_peak,
    follow_word,
    naive_block_image,
    naive_odd_image,
    peak_valley_blocks,
    rotate_to_first_peak,
    slack_row,
)

REPO = Path(__file__).resolve().parents[3]
DOSSIER = REPO / "docs" / "problems" / "juggler_cycle_peak_valley_composition.md"
SUMMARY = (
    REPO
    / "data"
    / "research"
    / "juggler"
    / "cycle_finance"
    / "peak_valley_composition"
    / "summary.json"
)


def test_dossier_has_triage_and_closed_gates():
    text = DOSSIER.read_text(encoding="utf-8")
    assert "## Branch budget" in text
    assert "Mathematical target" in text
    assert "## Closed-bridge gates" in text
    assert "## Decision" in text
    assert "## Publication assessment" in text
    assert "**CLOSE**" in text
    assert "Do **not** raise" in text
    assert "power_bound_word" in text
    assert "cycle_trailing_evens_lt" in text
    assert "exponent budget" in text


def test_block_product_is_the_word_envelope():
    for word, num, den in (
        ("OE", 3, 4),
        (WORD_OOE, 9, 8),
        (WORD_OOOEE, 27, 32),
        (WORD_TWO_OOE, 81, 64),
        (WORD_L11, 2187, 2048),
    ):
        mu = composite_exponent(word)
        assert mu == Fraction(num, den)
        assert blocks_exponent(peak_valley_blocks(word)) == mu


def test_exact_cells_compose_to_the_word_map():
    assert follow_word(25, WORD_OOOEE) == 15
    assert exact_valley_composite(25, WORD_OOOEE) == 15
    assert follow_word(365, WORD_TWO_OOE) == 1749
    assert exact_valley_composite(365, WORD_TWO_OOE) == 1749
    peak = first_peak(365, WORD_TWO_OOE)
    assert peak == 582276
    assert exact_peak_composite(peak, WORD_TWO_OOE) == follow_word(
        peak, rotate_to_first_peak(WORD_TWO_OOE)
    )


def test_naive_exponent_is_an_envelope():
    assert naive_odd_image(365, 2) == 582316
    assert naive_block_image(365, 2, 1) == 763
    assert first_peak(365, WORD_OOE) == 582276
    assert follow_word(365, WORD_OOE) == 763


def test_real_slack_follows_the_exponent_sign():
    contract = slack_row(52214.0, WORD_OOOEE)
    assert contract["entirely_below"] is True
    leftover = slack_row(1_000_000.0, WORD_L11)
    assert leftover["entirely_above"] is True
    assert leftover["contains_peak"] is False


def test_science_artifact_closes():
    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert payload["bound"] == "peak_valley_composition"
    assert payload["expanding_witness"]["image"] == 1749
    assert payload["realized_l11"] == {"start": 429, "word": WORD_L11, "image": 646}
    decision = payload["decision"]
    assert decision["decision"] == "CLOSE"
    assert decision["classification"] == "PEAK_VALLEY_COMPOSITION_CLOSED"
    assert decision["exact_cells_are_functional"] is True
    assert decision["onesided_is_power_bound"] is True
    assert decision["leftover_real_interval_above"] is True
    assert decision["contracting_real_interval_below"] is True
    assert decision["leftover_killer"] is False
    assert decision["paper_a_edit"] is False
    assert decision["reopens_exponent_budget"] is False


def test_dossier_and_conjecture_record_close():
    dossier = DOSSIER.read_text(encoding="utf-8")
    assert "**CLOSE**" in dossier
    rec = get_conjecture("juggler_cycle_peak_valley_composition")
    assert rec["status"] == "REFUTED"
    assert rec["lean_reference"] == "power_bound_word"
    assert rec["counterexamples"]
