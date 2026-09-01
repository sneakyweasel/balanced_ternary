"""Fan-growth Wu-Wang transfer Phase 0. Arithmetic only, not a halt test."""

from __future__ import annotations

import json
from pathlib import Path

from research.juggler_sequence.cycle_walk_fan_growth import (
    WW_EXPONENT,
    WU_WANG_MU,
    convergents_from_partial,
)

DOSSIER = Path("docs/problems/juggler_cycle_walk_fan_growth.md")
RECORD = Path("conjectures/proved/juggler_walk_fan_growth_measure.json")
ARTIFACT = Path("data/research/juggler/cycle_walk_fan_growth/summary.json")
WU_WANG = Path("literature/wu-wang-2014-irrationality-measure-log3.json")


def test_cf_algebra_and_transfer_exponent():
    # 12/19 and 53/84 are the classical leftover convergents of α.
    conv = convergents_from_partial([0, 1, 1, 1, 2, 2, 3, 1])
    pairs = {(p, q) for _, p, q in conv}
    assert (12, 19) in pairs
    assert (53, 84) in pairs
    assert abs(WW_EXPONENT - (WU_WANG_MU - 2.0)) < 1e-15
    assert 3.116 < WW_EXPONENT < 3.117


def test_fan_growth_artifact():
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    alpha = payload["alpha_cf_certified"]["partial_quotients"]
    assert alpha[:16] == [0, 1, 1, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2, 1, 1, 55]
    theta = payload["theta_cf_certified"]["partial_quotients"]
    assert theta[:15] == [0, 2, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2, 1, 1, 55]
    obs = payload["alpha_cf_observed_uncertified"]
    assert obs["prefix_matches_certified"] is True
    census = payload["certified_census"]
    assert census["all_below_ww_diagnostic"] is True
    assert census["max_a"] == 55
    assert census["q_at_max_a"] == 301994
    assert census["max_a_over_ww_cap"] < 3e-4
    # The 55-fan is many orders below the diagnostic envelope.
    fan55 = next(
        r
        for r in payload["large_certified_alpha_quotients"]
        if r["a_next"] == 55
    )
    assert fan55["a_over_ww_cap"] < 1e-15
    # WW already allows R_min near 1 at the first leftover.
    q19 = next(s for s in payload["ww_scale_table"] if s["q"] == 19)
    assert q19["R_min_ww_floor"] < 1.001
    thresh = {t["target_R_min"]: t for t in payload["r_min_thresholds"]}
    assert thresh[1.001]["q_threshold"] < 20
    assert payload["classification"]["label"] == "WALK_FAN_GROWTH_GREEN"
    assert payload["transfer"]["does_not_prevent_R_min_to_1"] is True
    assert payload["transfer"]["not_a_leftover_killer"] is True


def test_anti_overclaim_and_dossier_headings():
    dossier = DOSSIER.read_text(encoding="utf-8")
    for heading in (
        "## Problem",
        "## Exact statement",
        "## Branch budget",
        "## Decision",
        "## Publication assessment",
    ):
        assert heading in dossier
    assert "not claimed" in dossier
    assert "REFUTED" in dossier
    assert "**PROMOTE.**" in dossier
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    assert record["id"] == "juggler_walk_fan_growth_measure"
    assert record["not_a_halt_theorem"] is True
    assert record["status"] == "EXACT — HUMAN PROOF"
    lit = json.loads(WU_WANG.read_text(encoding="utf-8"))
    assert lit["id"] == "wu-wang-2014-irrationality-measure-log3"
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert payload["not_a_halt_theorem"] is True
    assert payload["no_new_period_bound"] is True
    assert payload["baker_killer_stays_refuted"] is True
