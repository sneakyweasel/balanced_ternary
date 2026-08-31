"""Cyclic run-type extremum. Not a halt test."""

from __future__ import annotations

import json
from pathlib import Path

from research.juggler_sequence.cycle_budget_opt import budget_excludes
from research.juggler_sequence.cycle_finance import (
    PUBLISHED_FLOOR,
    o_min_and_theta,
    sha256_int_list,
)
from research.juggler_sequence.cycle_run_extremum import (
    cheap_ooe_cannot_feed_oe,
    delta_coarse,
    extremum_row,
    f_coarse,
    n_cheap_still_o_minus_e,
    ooe_next_valley_min,
    two_type_beats_deepen,
    two_type_beats_merge,
)

REPO = Path(__file__).resolve().parents[3]
START = PUBLISHED_FLOOR + 1


def test_exchange_two_type_is_relaxed_max():
    assert two_type_beats_merge(START)
    assert two_type_beats_deepen(START)
    assert f_coarse(2, START) + f_coarse(2, START) >= (
        f_coarse(3, START) + f_coarse(1, START)
    )
    assert delta_coarse(1, START) > delta_coarse(2, START)
    assert delta_coarse(2, START) > delta_coarse(3, START)


def test_spotlight_25781_and_55293_do_not_die():
    row = extremum_row(25781)
    assert row["o"] == 16266
    assert row["e"] == 9515
    assert row["n_cheap"] == 6751
    assert row["two_type_is_max"]
    assert row["relaxed_matches_budget"]
    assert row["n_cheap_still_o_minus_e"]
    assert not row["budget_excludes"]
    assert not row["level_c_excludes"]
    odd_count, theta = o_min_and_theta(25781)
    assert not budget_excludes(25781, odd_count, theta, PUBLISHED_FLOOR)
    tight = extremum_row(55293)
    assert tight["two_type_is_max"]
    assert tight["relaxed_matches_budget"]
    assert not tight["budget_excludes"]
    assert tight["theta"] / tight["budget_rhs"] < 1.0


def test_level_c_is_envelope_without_n_cheap_drop():
    assert cheap_ooe_cannot_feed_oe(START)
    assert ooe_next_valley_min(START) < START
    assert n_cheap_still_o_minus_e(16266, 9515)


def test_run_extremum_scan_closes():
    payload = json.loads(
        (
            REPO / "data" / "research" / "juggler" / "cycle_finance"
            / "run_extremum.json"
        ).read_text(encoding="utf-8")
    )
    assert payload["survivor_count"] == 99
    assert payload["two_type_is_relaxed_max"] is True
    assert payload["two_type_max_failures"] == []
    assert payload["relaxed_matches_budget"] is True
    assert payload["relaxed_match_failures"] == []
    assert payload["n_cheap_still_o_minus_e"] is True
    assert payload["n_cheap_drop_failures"] == []
    assert payload["level_c_binds"] is False
    assert payload["killed_by_level_c"] == []
    assert payload["exchange"]["two_type_beats_merge"] is True
    assert payload["exchange"]["two_type_beats_deepen"] is True
    assert payload["exchange"]["deltas_decreasing"] is True
    assert payload["exchange"]["cheap_ooe_cannot_feed_oe"] is True
    assert payload["sha256_survivors"] == sha256_int_list(
        [row["L"] for row in payload["rows"]]
    )
    assert payload["spotlights"]["25781"]["L"] == 25781
    assert payload["spotlights"]["55293"]["L"] == 55293


def test_dossier_records_close():
    dossier = (
        REPO / "docs" / "problems" / "juggler_cycle_budget_opt.md"
    ).read_text(encoding="utf-8")
    assert "Cyclic run-type extremum" in dossier
    assert "run_extremum.json" in dossier
    assert "juggler_cycle_run_extremum_leftover_killer" in dossier
