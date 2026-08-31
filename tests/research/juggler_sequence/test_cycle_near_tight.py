"""Cycle versus open-orbit near-tightness. Not a halt test."""

from __future__ import annotations

import json
from pathlib import Path

from research.conjectures import get_conjecture
from research.literature import get_reference
from research.juggler_sequence.cycle_gap_baker import exact_gap
from research.juggler_sequence.cycle_near_tight import (
    CLASS_CLOSED,
    CLASS_GREEN,
    CLASS_INCOMPLETE,
    EXISTING_LEAN,
    FORBIDDEN_LEAN_FILES,
    FORBIDDEN_NEW_API,
    FORBIDDEN_THEOREMS,
    RECORD_LENGTHS,
    SLOGAN_LENGTHS,
    classify,
    cycle_exponent_gap,
    cycle_ln_one_plus_q,
    cycle_one_plus_q,
    envelope_growth_log,
    lean_api_present,
    open_q_lt_cycle_q,
    ooe_open_census,
    ooe_open_row,
    probe_payload,
    record_row,
    render_markdown,
    successor_illustration,
)
from research.juggler_sequence.expansion_slack import NEAR_TIGHT
from research.juggler_sequence.global_defect import image_after

REPO = Path(__file__).resolve().parents[3]


def test_cycle_q_is_n_to_the_exponent_gap():
    nineteen = exact_gap(19)
    assert nineteen["o"] == 12
    assert nineteen["gap"] == 7153
    assert cycle_exponent_gap(19) == 7153
    assert cycle_one_plus_q(2, 3) == 2
    assert cycle_one_plus_q(5, 3) == 5
    assert cycle_one_plus_q(2, 19) == 2**7153
    assert abs(cycle_ln_one_plus_q(53, 19) - 7153 * __import__("math").log(53)) < 1e-9


def test_open_q_lt_cycle_q_is_image_comparison():
    assert open_q_lt_cycle_q(9, 11) is True
    assert open_q_lt_cycle_q(9, 9) is False
    assert open_q_lt_cycle_q(9, 8) is False
    nine = ooe_open_row(9)
    assert nine is not None
    assert nine["image"] == image_after(9, "OOE")
    assert nine["expands"] is True
    assert nine["returns"] is False
    assert nine["open_q_lt_cycle_q"] is True
    assert nine["q_cycle"] == 8
    assert nine["q_open"] < nine["q_cycle"]
    assert nine["R"] < 1


def test_record_hamming_grows_on_slogan_lengths():
    rows = {row["L"]: row for row in (record_row(length) for length in RECORD_LENGTHS)}
    assert rows[1]["hamming_to_monochrome"] == 0
    assert rows[3]["even_count"] == 1
    assert rows[3]["hamming_to_monochrome"] == 1
    assert rows[11]["even_count"] == 4
    assert rows[19]["even_count"] == 7
    assert rows[19]["gap"] == 7153
    hammings = [rows[length]["hamming_to_monochrome"] for length in SLOGAN_LENGTHS]
    assert hammings == [7, 31, 210, 389]
    assert hammings == sorted(hammings)
    assert all(rows[length]["almost_monochrome"] is False for length in SLOGAN_LENGTHS)


def test_zero_defect_path_would_expand_not_return():
    growth = envelope_growth_log(53, 19)
    assert growth > 0
    assert __import__("math").expm1(growth) > 0.05


def test_ooe_census_never_returns():
    census = ooe_open_census(n_max=400)
    assert census["checked"] >= 20
    assert census["returns"] == 0
    assert census["all_expand"] is True
    assert census["all_open_q_lt_cycle_q"] is True
    assert census["all_R_lt_one"] is True
    assert census["max_R"] is not None and census["max_R"] < 1


def test_successor_is_mixed_near_tight_and_expanding():
    row = successor_illustration()
    assert row["y"] == NEAR_TIGHT["x"]
    assert row["expands"] is True
    assert row["returns"] is False
    assert row["q_open_below_1e_30"] is True
    assert row["open_q_lt_cycle_q"] is True
    assert row["q_cycle"] == row["y"] - 1


def test_probe_closes_and_does_not_claim_halt():
    payload = probe_payload()
    assert payload["experiment"] == "juggler_cycle_near_tight"
    assert payload["engine_control_layer_modified"] is False
    assert payload["anti_overclaim"]["halt_theorem"] is False
    assert payload["anti_overclaim"]["almost_monochrome_forced"] is False
    assert payload["anti_overclaim"]["leftover_killed"] is False
    assert payload["decision"]["classification"] == CLASS_CLOSED
    assert payload["decision"]["classification"] not in {
        CLASS_GREEN,
        CLASS_INCOMPLETE,
    }
    assert payload["scan"]["slogan_fails"] is True
    assert payload["scan"]["leftover_killed_by_near_tight"] is False
    text = render_markdown(payload)
    assert "Not a halt theorem" in text
    lean = lean_api_present()
    assert classify(payload["scan"], lean)["classification"] == CLASS_CLOSED


def test_lean_api_reuses_return_identity_and_forbids_new_file():
    lean = lean_api_present()
    assert lean["sorry_free"] is True
    for name in EXISTING_LEAN:
        assert lean[name] is True, name
    for name in FORBIDDEN_THEOREMS:
        assert lean[f"has_{name}"] is False, name
    for name in FORBIDDEN_NEW_API:
        assert lean[f"has_api_{name}"] is False, name
    assert lean["no_extra_near_tight_cycle_file"] is True
    assert lean["not_in_paper_barrel"] is True
    for path in FORBIDDEN_LEAN_FILES:
        assert path.is_file() is False


def test_science_summary_is_closed():
    summary = json.loads(
        (
            REPO
            / "data"
            / "research"
            / "juggler"
            / "cycle_near_tight"
            / "summary.json"
        ).read_text(encoding="utf-8")
    )
    assert summary["classification"] == CLASS_CLOSED
    assert summary["slogan_fails"] is True
    assert summary["leftover_killed_by_near_tight"] is False
    assert summary["ooe_returns"] == 0
    assert summary["successor_q_open_below_1e_30"] is True


def test_dossier_and_literature():
    dossier = (
        REPO / "docs" / "problems" / "juggler_cycle_near_tight.md"
    ).read_text(encoding="utf-8")
    paper = (REPO / "formal" / "Problems" / "JugglerPaper.lean").read_text(
        encoding="utf-8"
    )
    assert "## Branch budget" in dossier
    assert "## Decision" in dossier
    assert "## Publication assessment" in dossier
    assert "**CLOSE**" in dossier
    assert "image_eq_start_defectRatio" in dossier
    assert "NearTightScale" in dossier
    assert "CycleNearTight" not in paper
    get_reference("simons-de-weger-2005-collatz-m-cycles")
    get_reference("oeis-A007320")
    conj = get_conjecture("juggler_cycle_near_tight_monochrome")
    assert conj["status"] == "REFUTED"
    assert conj["counterexamples"]
