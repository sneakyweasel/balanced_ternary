"""Baker transfer on |3^o - 2^L|. Not a halt test and not x^3 - y^2."""

from __future__ import annotations

import json
import math
from pathlib import Path

from research.conjectures import get_conjecture
from research.literature import get_reference
from research.juggler_sequence.cycle_gap_baker import (
    CLASS_CLOSED,
    CLASS_GREEN,
    CLASS_INCOMPLETE,
    EXISTING_LEAN,
    FORBIDDEN_NEW_API,
    FORBIDDEN_THEOREMS,
    LEAN_FLOOR,
    LEFTOVER_RECORDS,
    PYTHON_FLOOR,
    RECORD_LENGTHS,
    bound_row,
    classify,
    exact_gap,
    lean_api_present,
    leftover_exclusions,
    needed_floor_for_rhin,
    o_min,
    probe_payload,
    render_markdown,
    rhin_lambda_lower,
    squeeze_row,
    theta_from_lambda,
)

REPO = Path(__file__).resolve().parents[3]


def test_exact_gap_matches_known_near_convergents():
    first = exact_gap(1)
    assert first["o"] == 1
    assert first["gap"] == 1
    three = exact_gap(3)
    assert three["o"] == 2
    assert three["gap"] == 1
    eleven = exact_gap(11)
    assert eleven["o"] == 7
    assert eleven["gap"] == 139
    nineteen = exact_gap(19)
    assert nineteen["o"] == 12
    assert nineteen["gap"] == 7153
    assert o_min(19) == 12


def test_rhin_is_weaker_than_exact_on_records():
    for length in RECORD_LENGTHS:
        row = bound_row(length)
        assert row["rhin_weaker_than_exact"] is True
        assert row["rhin_n_max_ge_exact"] is True
        assert row["rhin_n_max"] >= row["exact_n_max"]


def test_perfect_gap_does_not_kill_length_nineteen_at_lean_floor():
    row = bound_row(19)
    assert row["exact_n_max"] > LEAN_FLOOR
    assert row["exact_n_max"] == 297
    assert needed_floor_for_rhin(19) > PYTHON_FLOOR


def test_squeeze_never_fires_on_leftover_records():
    for length in LEFTOVER_RECORDS:
        for floor in (53, 1_000_000, 1_000_000_000):
            row = squeeze_row(length, floor)
            assert row["fires"] is False
            assert row["rhin_theta"] <= row["finance_theta_cap"]


def test_rhin_kills_no_dense_leftovers():
    rows = [bound_row(length) for length in range(1, 401)]
    for floor in (53, 1_000_000, 1_000_000_000):
        summary = leftover_exclusions(rows, floor)
        assert summary["rhin_killed"] == []


def test_theta_from_lambda_matches_relative_gap():
    lam = abs(3 * math.log(2) - 2 * math.log(3))
    theta = theta_from_lambda(lam)
    assert abs(theta - (1.0 - 8.0 / 9.0)) < 1e-12


def test_rhin_formula_is_sdw_lemma_12():
    value = rhin_lambda_lower(12)
    expected = math.exp(-13.3 * (0.46057 + math.log(12)))
    assert abs(value - expected) < 1e-18 * max(expected, 1e-30)


def test_probe_closes_and_does_not_claim_halt():
    payload = probe_payload()
    assert payload["experiment"] == "juggler_cycle_gap_baker"
    assert payload["engine_control_layer_modified"] is False
    assert payload["anti_overclaim"]["halt_theorem"] is False
    assert payload["anti_overclaim"]["x3_y2_campaign"] is False
    assert payload["anti_overclaim"]["baker_solver"] is False
    assert payload["decision"]["classification"] == CLASS_CLOSED
    assert payload["decision"]["classification"] not in {
        CLASS_GREEN,
        CLASS_INCOMPLETE,
    }
    assert payload["scan"]["dominance"] is True
    assert payload["scan"]["squeeze_fires_on_leftover_records"] is False
    assert payload["scan"]["perfect_gap_kills_nineteen_at_lean_floor"] is False
    text = render_markdown(payload)
    assert "Not a halt theorem" in text
    assert "parked x^3 - y^2 campaign" in text
    lean = lean_api_present()
    assert classify(payload["scan"], lean)["classification"] == CLASS_CLOSED


def test_lean_api_has_finance_and_no_baker_file():
    lean = lean_api_present()
    assert lean["sorry_free"] is True
    for name in EXISTING_LEAN:
        assert lean[name] is True, name
    for name in FORBIDDEN_THEOREMS:
        assert lean[f"has_{name}"] is False, name
    for name in FORBIDDEN_NEW_API:
        assert lean[f"has_api_{name}"] is False, name
    assert lean["cycle_finance_present"] is True
    assert lean["no_baker_lean"] is True
    assert lean["not_in_paper_barrel"] is True


def test_science_summary_is_closed():
    summary = json.loads(
        (
            REPO
            / "data"
            / "research"
            / "juggler"
            / "cycle_gap_baker"
            / "summary.json"
        ).read_text(encoding="utf-8")
    )
    assert summary["classification"] == CLASS_CLOSED
    assert summary["dominance"] is True
    assert summary["squeeze_fires_on_leftover_records"] is False
    assert summary["perfect_gap_kills_nineteen_at_lean_floor"] is False
    assert all(count == 0 for count in summary["rhin_killed_dense"].values())


def test_dossier_and_literature():
    dossier = (
        REPO / "docs" / "problems" / "juggler_cycle_gap_baker.md"
    ).read_text(encoding="utf-8")
    paper = (REPO / "formal" / "Problems" / "JugglerPaper.lean").read_text(
        encoding="utf-8"
    )
    assert "## Branch budget" in dossier
    assert "## Decision" in dossier
    assert "## Publication assessment" in dossier
    assert "**CLOSE**" in dossier
    assert "simons-de-weger-2005-collatz-m-cycles" in dossier
    assert "rhin-1987-pade-irrationality" in dossier
    assert "x^3-y^2" in dossier
    assert "CycleGapBaker" not in paper
    get_reference("simons-de-weger-2005-collatz-m-cycles")
    get_reference("rhin-1987-pade-irrationality")
    get_reference("laurent-mignotte-nesterenko-1995-two-logarithms")
    conj = get_conjecture("juggler_baker_kills_near_convergents")
    assert conj["status"] == "REFUTED"
    assert conj["counterexamples"]
