"""Bunched last-cluster leftover tails. Not an engine-control or halt test."""

from __future__ import annotations

import json

from research.juggler_sequence.bunched_last_cluster import (
    A_MAX,
    CLASS_GREEN,
    FAMILIES,
    LEAN_THEOREMS,
    classify,
    eee_coarse_holds,
    eee_cubes_from,
    expanding_family,
    family_word,
    first_cutoff,
    first_expanding_a,
    lean_api_present,
    render_markdown,
    run_probe,
    tail_holds,
    tail_word,
)
from research.juggler_sequence.cycle_length_nine import tail_fires
from research.juggler_sequence.power_words import ANTI_OVERCLAIM


def test_seven_families_and_first_expanding_a():
    assert [family["name"] for family in FAMILIES] == [
        "EEE",
        "EOEE",
        "EOOEE",
        "EOOOEE",
        "EEOE",
        "EOEOE",
        "EOOEOE",
    ]
    assert family_word(6, 0, 0) == "OOOOOOEEE"
    assert family_word(5, 1, 0) == "OOOOOEOEE"
    assert family_word(3, 3, 0) == "OOOEOOOEE"
    assert family_word(2, 4, 0) == "OOEOOOOEE"
    assert tail_word(0, 0) == "EEE"
    assert tail_word(3, 0) == "EOOOEE"
    assert tail_word(2, 1) == "EOOEOE"
    for family in FAMILIES:
        assert first_expanding_a(family["b"], family["c"]) == family["a_min"]
        assert expanding_family(family["a_min"], family["b"], family["c"]) is True
        if family["a_min"] > 2:
            assert expanding_family(family["a_min"] - 1, family["b"], family["c"]) is False


def test_first_cutoffs_and_n_le_4():
    assert first_cutoff(6, 0, 0) == 73
    assert first_cutoff(5, 1, 0) == 89
    assert first_cutoff(4, 2, 0) == 120
    assert first_cutoff(3, 3, 0) == 188
    assert first_cutoff(5, 0, 1) == 60
    assert first_cutoff(4, 1, 1) == 81
    assert first_cutoff(3, 2, 1) == 126
    assert tail_fires(73, 6, 0, 0) is True
    assert tail_fires(72, 6, 0, 0) is False
    assert tail_holds(188, 3, 3, 0) is True
    assert tail_holds(187, 3, 3, 0) is False
    for family in FAMILIES:
        a = family["a_min"] + 4
        for n in (2, 3, 4):
            assert tail_holds(n, a, family["b"], family["c"]) is False
    assert eee_coarse_holds(73, 6) is True
    assert eee_coarse_holds(72, 6) is False
    assert eee_cubes_from() is True


def test_probe_and_classify_green():
    scan = run_probe()
    lean = lean_api_present()
    decision = classify(scan, lean)
    assert decision["classification"] == CLASS_GREEN
    assert scan["family_count"] == 7
    assert scan["max_n0"] == 188
    assert scan["plateau_is_five"] is True
    assert scan["all_tables_empty"] is True
    assert scan["all_tails_fire"] is True
    assert scan["eee_cubes"] is True
    assert scan["eee_coarse_n0_at_six"] == 73
    assert scan["length_eight_census"] is False
    assert scan["length_nine_census"] is False
    assert scan["first_e_at_four"] is False
    for block in scan["blocks"]:
        assert block["rows"][0]["n0"] == block["first_n0"]
        assert all(row["n0"] == 5 for row in block["rows"] if row["a"] >= block["plateau_from"])
        for row in block["rows"]:
            assert row["a"] <= A_MAX
            assert row["table"]["hit_count"] == 0


def test_lean_api_without_bunched_or_census_theorem():
    lean = lean_api_present()
    assert lean["sorry_free"] is True
    for name in LEAN_THEOREMS:
        assert lean[name] is True, name
    assert lean["no_cycle_word_three_even_eee"] is True
    assert lean["three_even_eee_tail"] is True
    assert lean["no_bunched_tail_theorem"] is True
    assert lean["no_length_eight_theorem"] is True
    assert lean["no_length_nine_theorem"] is True
    assert lean["length_eight_open_in_census"] is True


def test_classify_render_and_artifacts():
    scan = run_probe()
    lean = lean_api_present()
    decision = classify(scan, lean)
    text = render_markdown(
        {
            "decision": decision,
            "scan": scan,
            "lean": lean,
            "engine_control_layer_modified": False,
            "anti_overclaim": {
                **dict(ANTI_OVERCLAIM),
                "cycles_impossible": False,
                "length_nine_census": False,
                "bunched_lean": False,
                "eee_lean": True,
            },
        }
    )
    assert CLASS_GREEN in text
    assert "OOOOOOEEE" in text or "EEE" in text
    assert "no_cycle_word_three_even_eee" in text
    from research.juggler_sequence.bunched_last_cluster import JSON_PATH

    assert JSON_PATH.is_file()
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert data["experiment"] == "juggler_bunched_last_cluster"
    assert data["decision"]["classification"] == CLASS_GREEN
    assert data["anti_overclaim"]["cycles_impossible"] is False
    assert data["lean"]["no_bunched_tail_theorem"] is True
    assert data["lean"]["no_cycle_word_three_even_eee"] is True
    assert data["anti_overclaim"]["bunched_lean"] is False
    assert data["anti_overclaim"]["eee_lean"] is True
    assert data["scan"]["max_n0"] == 188


def test_dossier_boundary():
    from pathlib import Path

    repo = Path(__file__).resolve().parents[3]
    dossier = (repo / "docs" / "problems" / "juggler_bunched_last_cluster.md").read_text(
        encoding="utf-8"
    )
    note = (repo / "docs" / "theory" / "juggler_finite_dynamics_note.md").read_text(
        encoding="utf-8"
    )
    assert "## Branch budget" in dossier
    assert "## Decision" in dossier
    assert "PROMOTE" in dossier
    assert "no_cycle_word_length_eight" in dossier
    assert "no_cycle_word_length_nine" in dossier
    assert "no_cycle_word_three_even_eee" in dossier
    assert "not a length-8" in dossier or "not a length-8/9" in dossier
    assert "theorem no_cycle_word_length_eight" not in note
    assert "theorem no_cycle_word_length_nine" not in note
