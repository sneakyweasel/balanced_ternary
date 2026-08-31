"""Correlated floor-defect finance. Not a halt test."""

from __future__ import annotations

import json
from pathlib import Path

from research.conjectures import get_conjecture
from research.juggler_sequence.cycle_defect_correlation import (
    SPOTLIGHT,
    START,
    first_following,
    oe_identity_holds,
    oo_identity_holds,
    spotlight_row,
)
from research.juggler_sequence.global_defect import compose_formula, global_defect

REPO = Path(__file__).resolve().parents[3]
SUMMARY = (
    REPO
    / "data"
    / "research"
    / "juggler"
    / "cycle_finance"
    / "defect_correlation"
    / "summary.json"
)


def test_oe_and_oo_identities_hold_at_first_starts():
    oe_start = first_following("OE", START)
    oo_start = first_following("OO", START)
    assert oe_start == START
    assert oo_start == 1000053
    assert oe_identity_holds(oe_start)
    assert oo_identity_holds(oo_start)
    assert global_defect(oe_start, "OE") == compose_formula(oe_start, "O", "E")
    assert global_defect(oo_start, "OO") == compose_formula(oo_start, "O", "O")


def test_oe_attains_independent_corners():
    row = spotlight_row(25781)
    oe = row["blocks"]["OE"]["near_n"]
    assert oe["count"] > 1000
    assert oe["both_cheap"] > 0
    assert oe["both_max"] > 0
    assert oe["independent_corners"]
    assert oe["finance_gap"] == 0.0
    assert oe["pair_eps_ratio_max"] > 0.999
    assert not row["kills"]


def test_tight_leftover_still_has_no_tax():
    row = spotlight_row(55293)
    assert 1.0 < row["packed_over_theta"] < 1.02
    assert row["both_max_attained"]
    assert row["both_cheap_attained"]
    assert row["pair_eps_ratio_max"] > 0.999
    assert row["tax_over_theta"] < 0.01
    assert not row["kills"]


def test_correlation_scan_closes():
    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert payload["emptied_count"] == 0
    assert payload["emptied_lengths"] == []
    assert payload["both_max_attained"] is True
    assert payload["both_cheap_attained"] is True
    assert payload["reduces_to_global_defect"] is True
    assert payload["halt_theorem"] is False
    assert payload["no_cycle_all_lengths"] is False
    for length in SPOTLIGHT:
        spot = payload["spotlights"][str(length)]
        assert spot["kills"] is False
        assert spot["blocks"]["OE"]["identities"]["oe"] is True
        assert spot["blocks"]["OO"]["identities"]["oo"] is True
        assert spot["blocks"]["OE"]["near_n"]["finance_gap"] == 0.0


def test_dossier_and_conjecture_record_close():
    dossier = (
        REPO / "docs" / "problems" / "juggler_cycle_defect_correlation.md"
    ).read_text(encoding="utf-8")
    assert "## Branch budget" in dossier
    assert "## Decision" in dossier
    assert "## Publication assessment" in dossier
    assert "**CLOSE**" in dossier
    assert "defect_correlation/summary.json" in dossier
    assert "juggler_cycle_defect_correlation_leftover_killer" in dossier
    rec = get_conjecture("juggler_cycle_defect_correlation_leftover_killer")
    assert rec["status"] == "REFUTED"
