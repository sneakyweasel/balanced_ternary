"""Fast checks for the divergent flight structure probe."""

from __future__ import annotations

import json

from research.juggler_sequence.flight_divergent_structure import (
    CLASS_CONFIRMED,
    JSON_PATH,
    _hug_table,
    all_anchor_check,
    lean_wired,
    trajectory,
)
from research.juggler_sequence.flight_walk_divergence import hug_odds

TEST_WINDOW = 200


def test_hug_table_matches_hug_odds() -> None:
    table = _hug_table(300)
    for k in range(0, 301):
        assert table[k] == hug_odds(k)


def test_all_anchor_mirrors_hold_on_window() -> None:
    for n in range(2, TEST_WINDOW + 1):
        row = all_anchor_check(trajectory(n))
        assert row["hug_violations"] == 0
        assert row["envelope_violations"] == 0


def test_all_anchor_mirrors_hold_on_a_flyer() -> None:
    row = all_anchor_check(trajectory(37))
    assert row["segments"] >= 5
    assert row["hug_violations"] == 0
    assert row["envelope_violations"] == 0


def test_trajectory_terminates_small() -> None:
    xs = trajectory(37)
    assert xs[0] == 37
    assert xs[-1] == 1


def test_lean_wiring() -> None:
    assert all(lean_wired().values())


def test_artifact_certifies_mirrors() -> None:
    summary = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert summary["classification"] == CLASS_CONFIRMED
    census = summary["window_census"]
    assert census["hug_violations"] == 0
    assert census["envelope_violations"] == 0
    assert census["segments"] > 20000
    rates = summary["high_flyer_rates"]
    assert len(rates) == 7
    assert all(r["bound_ok"] for r in rates)
    anti = summary["anti_overclaim"]
    assert anti["halt_theorem"] is False
    assert anti["divergence_excluded"] is False
    assert anti["odd_tower_excluded"] is False
    assert anti["excursion_envelope_reopened"] is False
