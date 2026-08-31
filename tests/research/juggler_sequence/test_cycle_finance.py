"""Cycle finance inequality. Not a halt test, not a no-cycle-of-any-length test."""

from __future__ import annotations

import json
from pathlib import Path

from research.juggler_sequence.cycle_finance import (
    CLASS_CLOSED,
    CLASS_GREEN,
    CLASS_INCOMPLETE,
    CLASS_PARK,
    ELIAHOU_LEAN_PERIOD,
    ELIAHOU_TABLE_CUTOFF,
    EXISTING_LEAN,
    EXPECTED_LEAN_KILL,
    FORBIDDEN_NEW_API,
    FORBIDDEN_THEOREMS,
    LEAN_FLOOR,
    TEST_FLOOR,
    census_cross_check,
    classify,
    eliahou_exceptions,
    eliahou_leftover,
    eliahou_packaging,
    eliahou_table_holds,
    finance_rows,
    lean_api_present,
    n_max_from_bound,
    orbit_slack,
    probe_payload,
    render_markdown,
    verify_floor,
)

REPO = Path(__file__).resolve().parents[3]


def test_finance_rows_exact_small_values():
    rows = finance_rows(12)
    by_length = {row["L"]: row for row in rows}
    # L=1: o=1, theta=1/3, B=3.6 -> n_max=3.
    assert by_length[1]["o"] == 1
    assert by_length[1]["n_max"] == 3
    # L=3 is the first near-tight length (2^3=8 vs 3^2=9).
    assert by_length[3]["o"] == 2
    assert by_length[3]["record"] is True
    assert by_length[3]["n_max"] == 13
    # L=12: gap 3^8 - 2^12 = 2465.
    assert by_length[12]["o"] == 8
    assert 12 <= by_length[12]["n_max"] <= 15
    # o is always minimal admissible: 3^o > 2^L > 3^(o-1).
    for row in rows:
        assert 3 ** row["o"] > 2 ** row["L"]
        assert 3 ** (row["o"] - 1) <= 2 ** row["L"]


def test_n_max_from_bound_monotone():
    values = [n_max_from_bound(b) for b in (0.1, 3.6, 32.4, 1000.0)]
    assert values == sorted(values)
    assert values[0] == 1
    assert values[1] >= 3


def test_census_cross_check_matches_lean_census():
    census = census_cross_check(finance_rows(8))
    assert census["matches_expected"] is True
    assert tuple(census["killed_by_lean_floor"]) == EXPECTED_LEAN_KILL
    assert tuple(census["census_only_lengths"]) == (3, 6)
    for length in census["killed_by_lean_floor"]:
        assert census["n_max_by_length"][length] <= LEAN_FLOOR


def test_verify_floor_descent_induction():
    result = verify_floor(300)
    assert result["verified"] is True
    assert result["failures"] == []
    assert result["max_first_passage_steps"] >= 1


def test_orbit_slack_bounds_hold():
    for seed in (25, 37, 365):
        row = orbit_slack(seed)
        assert row["step_bound_ok"] is True
        assert row["defect_bound_ok"] is True
        assert row["reached_one"] is True
        assert row["identity_rel_err"] < 1e-9
        assert row["worst_margin"] is None or row["worst_margin"] > 0.0
        assert row["tightness"] is None or row["tightness"] < 1.0


def test_probe_and_classify_vocabulary():
    payload = probe_payload()
    assert payload["experiment"] == "juggler_cycle_finance"
    assert payload["engine_control_layer_modified"] is False
    assert payload["decision"]["classification"] in {
        CLASS_GREEN,
        CLASS_PARK,
        CLASS_CLOSED,
        CLASS_INCOMPLETE,
    }
    assert payload["decision"]["classification"] not in {
        CLASS_CLOSED,
        CLASS_INCOMPLETE,
    }
    assert payload["anti_overclaim"]["halt_theorem"] is False
    assert payload["anti_overclaim"]["no_cycle_all_lengths"] is False
    assert payload["scan"]["eliahou"]["table_holds"] is True
    assert payload["scan"]["eliahou"]["lean_period"] == ELIAHOU_LEAN_PERIOD
    text = render_markdown(payload)
    assert "Eliahou leftover" in text
    assert "Not a halt theorem" in text
    lean = lean_api_present()
    assert classify(payload["scan"], lean)["classification"] == payload[
        "decision"
    ]["classification"]


def test_lean_api_finance_layer():
    lean = lean_api_present()
    assert lean["sorry_free"] is True
    for name in EXISTING_LEAN:
        assert lean[name] is True, name
    for name in FORBIDDEN_THEOREMS:
        assert lean[f"has_{name}"] is False, name
    for name in FORBIDDEN_NEW_API:
        assert lean[f"has_api_{name}"] is False, name
    assert lean["cycle_finance_present"] is True
    assert lean["no_extra_finance_file"] is True
    assert lean["not_in_paper_barrel"] is True


def test_science_summary_is_green():
    summary = json.loads(
        (
            REPO / "data" / "research" / "juggler" / "cycle_finance" / "summary.json"
        ).read_text(encoding="utf-8")
    )
    assert summary["classification"] == CLASS_GREEN
    assert summary["floor_verified"] is True
    assert summary["contiguous_prefix"] >= 1053


def test_eliahou_leftover_covers_survivors():
    rows = finance_rows(400)
    floor = TEST_FLOOR
    exceptions = eliahou_exceptions(rows, floor)
    leftover = eliahou_packaging(rows, floor, cutoff=400)
    assert leftover["table_holds"] is True
    assert leftover["lean_period"] == ELIAHOU_LEAN_PERIOD
    assert eliahou_table_holds(rows, floor, exceptions, cutoff=400)
    for row in rows:
        length = row["L"]
        survives = row["n_max"] > floor
        if survives:
            assert eliahou_leftover(length, exceptions, cutoff=400)
        if length < 400 and length != ELIAHOU_LEAN_PERIOD and length not in exceptions:
            assert survives is False


def test_eliahou_instance_matches_science_table():
    exceptions = json.loads(
        (
            REPO / "data" / "research" / "juggler" / "cycle_finance" / "exceptions.json"
        ).read_text(encoding="utf-8")
    )
    science = next(item for item in exceptions if item["floor"] == 1_000_000)
    lengths = science["lengths"]
    assert science["count"] == 397
    assert science["first_exception"] == 1054
    assert science["contiguous_prefix"] == 1053
    assert science["truncated"] is False
    assert ELIAHOU_LEAN_PERIOD not in lengths
    assert 19 not in lengths
    assert 1054 in lengths
    assert 50508 in lengths
    assert eliahou_leftover(ELIAHOU_LEAN_PERIOD, lengths)
    assert eliahou_leftover(1054, lengths)
    assert eliahou_leftover(ELIAHOU_TABLE_CUTOFF, lengths)
    assert not eliahou_leftover(19, lengths)
    assert not eliahou_leftover(30, lengths)
    assert not eliahou_leftover(38, lengths)
    assert not eliahou_leftover(57, lengths)
    assert not eliahou_leftover(76, lengths)
    assert not eliahou_leftover(1053, lengths)


def test_dossier_boundary():
    dossier = (
        REPO / "docs" / "problems" / "juggler_cycle_finance.md"
    ).read_text(encoding="utf-8")
    paper = (REPO / "formal" / "Problems" / "JugglerPaper.lean").read_text(
        encoding="utf-8"
    )
    assert "## Branch budget" in dossier
    assert "## Decision" in dossier
    assert "## Publication assessment" in dossier
    assert "**PROMOTE**" in dossier
    assert "cycle_word_formally_expanding" in dossier
    assert "simons-de-weger-2005-collatz-m-cycles" in dossier
    assert "cycle_word_eliahou_leftover" in dossier
    assert "cycle_word_length_eighty_four_m_ge_three_or_ge_eighty_five" in dossier
    assert "theorem no_cycle_word_any_length" not in dossier
    assert "CycleFinance" not in paper
    assert "CycleHeightFinance" not in paper
