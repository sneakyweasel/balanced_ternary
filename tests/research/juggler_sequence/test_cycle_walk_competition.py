"""Walk-charge vs finance competition Phase 0.

Arithmetic only: no floor verification, no new period bound, not a
halt test, not a uniform B/theta claim.
"""

from __future__ import annotations

import json
from pathlib import Path

from research.juggler_sequence.cycle_finance import o_min_and_theta
from research.juggler_sequence.cycle_walk_competition import (
    FLOOR_ONE,
    FLOOR_ZERO,
    break_even_floor,
    dk_price,
    o_min_exact,
    theta_exact,
)

DOSSIER = Path("docs/problems/juggler_cycle_walk_competition.md")
CONJECTURE = Path("conjectures/active/juggler_walk_finance_competition.json")
ARTIFACT = Path("data/research/juggler/cycle_walk_competition/summary.json")
OSTROWSKI = Path("data/research/juggler/cycle_walk_ostrowski/summary.json")
DP_KILL = Path(
    "data/research/juggler/cycle_walk_charge/new_floor_kills/L176251.json"
)


def test_theta_exact_matches_finance():
    for length in (19, 84, 1054, 25781, 50508):
        o_ref, theta_ref = o_min_and_theta(length)
        row = theta_exact(length)
        assert row["odd_count"] == o_ref
        assert abs(row["theta"] - theta_ref) <= 1e-18
    row = theta_exact(176_251)
    assert row["odd_count"] == 111_202
    assert abs(row["theta"] - 3.600206691677816e-06) < 1e-17
    # o decided by the deep interval, certified minimal by the power
    # sandwich inside theta_exact
    assert o_min_exact(50_508) == 31_867
    assert o_min_exact(478_245) == 301_739


def test_dk_price_reproduces_certified_margins():
    stored = json.loads(OSTROWSKI.read_text(encoding="utf-8"))
    by_length = {int(r["length"]): r for r in stored["rows"]}
    for length in (50_508, 151_524, 176_251):
        r = by_length[length]
        price = dk_price(
            length,
            int(r["odd_count"]),
            int(r["digit_sum"]),
            float(r["theta"]),
            FLOOR_ZERO + 1,
        )
        rel = abs(price["margin"] - r["margin_dk"]) / r["margin_dk"]
        assert rel < 1e-9, (length, rel)


def test_break_even_reproduces_the_new_floor_kill():
    dp = json.loads(DP_KILL.read_text(encoding="utf-8"))
    assert dp["floor"] == FLOOR_ONE
    row = theta_exact(176_251)
    price = dk_price(176_251, row["odd_count"], 1, row["theta"], FLOOR_ONE + 1)
    # DK is a slightly larger bound than the certified DP: it must
    # still kill, with margin at most the DP margin.
    assert 1.0 < price["margin"] < dp["kill_margin"]
    be = break_even_floor(176_251, row["odd_count"], 1, row["theta"])
    assert 1.2e8 < be["n_star"] < FLOOR_ONE
    assert be["margin_at_n_star"] >= 1.0
    assert 0.5 < be["law_ratio"] < 1.0
    # 50508 is killed at the certified floor, so its break-even floor
    # sits below it.
    row0 = theta_exact(50_508)
    be0 = break_even_floor(50_508, row0["odd_count"], 1, row0["theta"])
    assert be0["n_star"] < FLOOR_ZERO
    assert 0.5 < be0["law_ratio"] < 1.0


def test_competition_artifact():
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert payload["x_certification_old"]["certified"] is True
    assert payload["x_certification_deep"]["certified"] is True
    cf = payload["theta_cf"]
    assert cf["reached"] == 85_137_581
    assert 16_785_921 in cf["denominators"]
    checks = payload["cross_checks"]
    assert checks["max_theta_rel_err"] < 1e-9
    assert checks["max_margin_rel_err"] < 1e-6
    assert checks["digit_sums_unchanged"] is True
    assert checks["dk_kills_176251_at_floor1"] is True
    assert checks["dk_below_dp"] is True
    rows = {r["length"]: r for r in payload["rows"]}
    # 478245 is fan A at k = 1 with Ostrowski digits 301994 + 176251.
    assert rows[478_245]["tag"] == "fanA_k1"
    assert rows[478_245]["digit_sum"] == 2
    assert rows[478_245]["margin_floor1"] < 1.0
    assert rows[176_251]["margin_floor1"] > 1.0
    # break-even floors grow along the dangerous seeds
    seeds = [r for r in payload["rows"] if r["tag"] == "seed"]
    n_stars = [r["n_star"] for r in sorted(seeds, key=lambda r: r["length"])]
    assert n_stars == sorted(n_stars)
    assert n_stars[-1] > 1e12
    schedule = payload["schedule"]
    assert schedule["all_lengths_killed_at_final"] is True
    assert all(e["contiguous_over_rows"] for e in schedule["levels"])
    assert schedule["levels"][0]["floor"] == FLOOR_ZERO + 1
    assert schedule["levels"][1]["floor"] == FLOOR_ONE + 1
    assert schedule["levels"][1]["first_survivor"] == 478_245
    scaling = payload["scaling"]
    assert scaling["law_ratio_in_band"] is True
    assert 0.5 < scaling["law_ratio_min"] <= scaling["law_ratio_max"] < 1.0
    assert payload["classification"]["label"] == "WALK_COMPETITION_GREEN"


def test_anti_overclaim_and_dossier_headings():
    dossier = DOSSIER.read_text(encoding="utf-8")
    for heading in (
        "## Problem",
        "## Exact statement",
        "## Current literature",
        "## Branch budget",
        "## Decision",
        "## Publication assessment",
    ):
        assert heading in dossier
    assert "not claimed" in dossier
    record = json.loads(CONJECTURE.read_text(encoding="utf-8"))
    assert record["id"] == "juggler_walk_finance_competition"
    assert record["not_a_halt_theorem"] is True
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert payload["not_a_halt_theorem"] is True
    assert payload["no_cycle_all_lengths"] is False
    assert payload["not_a_uniform_ratio_theorem"] is True
    assert payload["no_new_period_bound"] is True
    assert payload["floors"]["later_floors_hypothetical"] is True
