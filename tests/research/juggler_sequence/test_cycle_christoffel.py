"""Christoffel leftover reduction. Not a halt test and not Lebel sieving."""

from __future__ import annotations

import json
from pathlib import Path

from research.conjectures import get_conjecture
from research.literature import get_reference
from research.juggler_sequence.cycle_christoffel import (
    ALL_PROBE_LENGTHS,
    CLASS_CLOSED,
    CLASS_GREEN,
    CLASS_INCOMPLETE,
    EXISTING_LEAN,
    FORBIDDEN_NEW_API,
    FORBIDDEN_THEOREMS,
    IDENTIFICATIONS,
    LEFTOVER_RECORDS,
    christoffel_word,
    classify,
    cyclic_hamming,
    cyclemin_census,
    cyclemin_rotations,
    farey_neighbor,
    farey_sum,
    identification_holds,
    is_balanced_oe,
    lean_api_present,
    leftover11_distances,
    probe_payload,
    render_markdown,
)
from research.juggler_sequence.cycle_gap_baker import o_min

REPO = Path(__file__).resolve().parents[3]


def test_christoffel_words_match_ceiling_mechanical():
    assert christoffel_word(11, 7) == "OOEOOEOOEOE"
    assert christoffel_word(19, 12) == "OOEOOEOOEOEOOEOOEOE"
    assert christoffel_word(38) == christoffel_word(19) * 2
    assert is_balanced_oe(christoffel_word(11))
    assert is_balanced_oe(christoffel_word(19))
    assert is_balanced_oe(christoffel_word(84))


def test_leftover_lengths_are_beatty_approximations():
    assert o_min(11) == 7
    assert o_min(19) == 12
    assert o_min(38) == 24
    assert o_min(84) == 53
    assert o_min(569) == 359
    assert o_min(1054) == 665
    assert farey_neighbor((2, 3), (5, 8))
    assert farey_sum((2, 3), (5, 8)) == (7, 11)
    assert farey_sum((53, 84), (306, 485)) == (359, 569)
    for length in ALL_PROBE_LENGTHS:
        assert identification_holds(length)
        spec = IDENTIFICATIONS[length]
        assert tuple(spec["ratio"]) == (o_min(length), length)


def test_cyclic_hamming_is_necklace_distance():
    word = "OOEOOEOOEOE"
    rotated = word[3:] + word[:3]
    assert cyclic_hamming(word, rotated) == 0
    assert cyclic_hamming(word, "OOOOOOOEEEE") == 4
    assert len(cyclemin_rotations(word)) == 4


def test_thirty_leftovers_are_not_the_christoffel_necklace():
    leftover = leftover11_distances()
    assert leftover["family_size"] == 30
    assert leftover["length_11_count"] == 30
    assert leftover["contains_christoffel"] is True
    assert leftover["histogram"] == {"0": 1, "2": 16, "4": 13}
    assert leftover["max"] == 4
    assert "OOOOOOOEEEE" in leftover["far_words"]


def test_length_nineteen_candidates_have_median_hamming_six():
    census = cyclemin_census(19)
    assert census["count"] == 12376
    assert census["radius_0"] == 7
    assert census["radius_le_2"] == 389
    assert census["median"] == 6
    assert census["isolated_even"]["count"] == 462
    assert census["one_parameter"] is False
    assert census["necklace"] == 7


def test_probe_closes_and_does_not_claim_halt():
    payload = probe_payload()
    assert payload["experiment"] == "juggler_cycle_christoffel"
    assert payload["engine_control_layer_modified"] is False
    assert payload["anti_overclaim"]["halt_theorem"] is False
    assert payload["anti_overclaim"]["lebel_modular_sieving"] is False
    assert payload["anti_overclaim"]["monochrome_reopened"] is False
    assert payload["anti_overclaim"]["affine_equation"] is False
    assert payload["decision"]["classification"] == CLASS_CLOSED
    assert payload["decision"]["classification"] not in {
        CLASS_GREEN,
        CLASS_INCOMPLETE,
    }
    assert payload["scan"]["slogan_false"] is True
    assert payload["scan"]["identifications_hold"] is True
    assert payload["scan"]["square_of_nineteen"] is True
    text = render_markdown(payload)
    assert "Not a halt theorem" in text
    assert "Lebel" in text
    lean = lean_api_present()
    assert classify(payload["scan"], lean)["classification"] == CLASS_CLOSED


def test_lean_api_has_finance_and_no_christoffel_file():
    lean = lean_api_present()
    assert lean["sorry_free"] is True
    for name in EXISTING_LEAN:
        assert lean[name] is True, name
    for name in FORBIDDEN_THEOREMS:
        assert lean[f"has_{name}"] is False, name
    for name in FORBIDDEN_NEW_API:
        assert lean[f"has_api_{name}"] is False, name
    assert lean["cycle_finance_present"] is True
    assert lean["no_christoffel_lean"] is True
    assert lean["not_in_paper_barrel"] is True


def test_science_summary_is_closed():
    summary = json.loads(
        (
            REPO
            / "data"
            / "research"
            / "juggler"
            / "cycle_christoffel"
            / "summary.json"
        ).read_text(encoding="utf-8")
    )
    assert summary["classification"] == CLASS_CLOSED
    assert summary["slogan_false"] is True
    assert summary["identifications_hold"] is True
    assert summary["leftover11_family"] == 30
    assert summary["census19_median"] == 6
    assert summary["isolated_even_19"] == 462


def test_dossier_and_literature():
    dossier = (
        REPO / "docs" / "problems" / "juggler_cycle_christoffel.md"
    ).read_text(encoding="utf-8")
    paper = (REPO / "formal" / "Problems" / "JugglerPaper.lean").read_text(
        encoding="utf-8"
    )
    assert "## Branch budget" in dossier
    assert "## Decision" in dossier
    assert "## Publication assessment" in dossier
    assert "**CLOSE**" in dossier
    assert "fernandez-ibanez-2026" in dossier
    assert "lebel-2026" in dossier
    assert "juggler_cycle_near_tight" in dossier
    assert tuple(LEFTOVER_RECORDS) == (38, 84, 569, 1054)
    assert "CycleChristoffel" not in paper
    assert "MechanicalWord" not in paper
    get_reference("fernandez-ibanez-2026")
    get_reference("lebel-2026")
    conj = get_conjecture("juggler_christoffel_one_parameter")
    assert conj["status"] == "REFUTED"
    assert conj["counterexamples"]
