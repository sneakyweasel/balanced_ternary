"""Return-cost valley coupling. Not a halt test."""

from __future__ import annotations

import json
from pathlib import Path

from research.conjectures import get_conjecture
from research.juggler_sequence.cycle_budget_opt import run_type_counts
from research.juggler_sequence.cycle_valley_coupling import (
    NINE_EIGHTHS,
    circuit_legal,
    coupling_row,
    exact_reset_to_one_exists,
    exponent_log2,
    land,
    n_max_separated,
    ooe_landing_beats_n_plus_two,
    ooe_landing_lower,
    shortest_descent_from_nine_eighths,
)

REPO = Path(__file__).resolve().parents[3]


def test_shortest_descent_is_five_three():
    report = shortest_descent_from_nine_eighths()
    assert report["is_five_three"]
    shortest = report["shortest"]
    assert shortest is not None
    assert shortest["k"] == 5
    assert shortest["ell"] == 3
    assert circuit_legal(*NINE_EIGHTHS, 5, 3)
    landed = land(*NINE_EIGHTHS, 5, 3)
    assert landed == (7, 11)
    assert abs(shortest["land_ratio"] - 2187 / 2048) < 1e-12
    assert exponent_log2(*landed) > 0


def test_no_exact_reset_to_exponent_one():
    assert exact_reset_to_one_exists() is False
    assert not circuit_legal(*NINE_EIGHTHS, 2, 1) or land(*NINE_EIGHTHS, 2, 1) != (
        0,
        0,
    )


def test_ooe_landing_beats_n_plus_two_on_realized_ooe():
    for seed in (37, 365, 1999, 1000053, 1000057):
        first_odd = seed
        from research.juggler_sequence.cycle_finance import first_odd_image

        image = first_odd_image(first_odd)
        if image % 2 == 0:
            continue
        assert ooe_landing_lower(seed) > seed + 2
        assert ooe_landing_beats_n_plus_two(seed)


def test_n_separated_strictly_below_packing_at_25781():
    oo_count, _oe_count = run_type_counts(16266, 9515)
    assert oo_count == 6751
    assert n_max_separated(16266, 9515, 5, 3) == 2324
    assert 2324 < oo_count


def test_certified_bound_does_not_kill_25781():
    row = coupling_row(25781)
    assert row["n_cheap_strictly_below_packing"]
    assert row["n_separated_53"] == 2324
    assert not row["packed_excludes"]
    assert not row["nine_excludes"]
    assert not row["greedy_excludes"]
    assert row["nine_eighths_rhs"] > row["theta"]
    assert row["greedy_rhs"] > row["theta"]


def test_artifact_records_diagnostic_not_certified_kills():
    payload = json.loads(
        (
            REPO
            / "data"
            / "research"
            / "juggler"
            / "cycle_finance"
            / "valley_coupling"
            / "summary.json"
        ).read_text(encoding="utf-8")
    )
    assert payload["shortest_is_five_three"] is True
    assert payload["exact_reset_to_one"] is False
    assert payload["all_n_cheap_below_packing"] is True
    assert payload["nine_kills_25781"] is False
    assert payload["greedy_kills_25781"] is False
    assert payload["certified_leftover_kills"] == []
    assert payload["diagnostic_only"] is True
    assert payload["ooe_landings_beat_n_plus_two"] is True
    assert payload["lowest_from_one"] == {"k": 53, "ell": 31}
    assert payload["greedy53_25781"]["excludes"] is False
    assert payload["spotlights"]["25781"]["n_separated_53"] == 2324


def test_dossier_records_close():
    dossier = (
        REPO / "docs" / "problems" / "juggler_cycle_valley_coupling.md"
    ).read_text(encoding="utf-8")
    assert "## Branch budget" in dossier
    assert "## Decision" in dossier
    assert "CLOSE" in dossier.split("## Decision", 1)[1].split("## ", 1)[0]
    assert "juggler_cycle_valley_coupling_leftover_killer" in dossier
    rec = get_conjecture("juggler_cycle_valley_coupling_leftover_killer")
    assert rec["status"] == "REFUTED"
    assert rec["counterexamples"]
