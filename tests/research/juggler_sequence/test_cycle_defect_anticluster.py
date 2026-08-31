"""Near-top defect anti-clustering. Not a halt test."""

from __future__ import annotations

import json
from pathlib import Path

from research.conjectures import get_conjecture
from research.juggler_sequence.cycle_defect_anticluster import (
    START,
    conversions_hold,
    odd_observables,
)
from research.juggler_sequence.cycle_finance import PUBLISHED_FLOOR

REPO = Path(__file__).resolve().parents[3]
SUMMARY = (
    REPO
    / "data"
    / "research"
    / "juggler"
    / "cycle_finance"
    / "defect_anticluster"
    / "summary.json"
)


def test_conversions_are_the_same_numerator():
    for x in (3, 15, 365, 1000001, 1016445, 2745367):
        assert conversions_hold(x)
        rec = odd_observables(x)
        assert rec["rho"] == x * x * x - rec["y"] * rec["y"]
        assert rec["width"] == 2 * rec["y"] + 1


def test_same_pair_near_top_witness():
    rec = odd_observables(2745367)
    nxt = odd_observables(rec["y"])
    assert rec["y_odd"]
    assert rec["u"] > 0.997
    assert nxt["u"] > 0.9998


def test_anticluster_scan_closes():
    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert payload["n"] == START
    assert payload["floor"] == PUBLISHED_FLOOR
    assert payload["conversions_equivalent"] is True
    assert payload["both_995_total"] == 12
    assert payload["both_999_total"] == 0
    assert payload["high_f_oo"] > 0.99995
    assert payload["high_f_999"] > 0.988
    assert payload["n_high_oo_total"] == 2893
    assert payload["n_ge_999_total"] == 576
    assert payload["high_followup"][0]["best"]["x"] == 2745367
    assert payload["leftover_killer"] is False
    assert payload["emptied_count"] == 0
    assert payload["halt_theorem"] is False
    assert payload["no_cycle_all_lengths"] is False
    assert payload["reopens_defect_correlation"] is True


def test_dossier_and_conjecture_record_close():
    dossier = (
        REPO / "docs" / "problems" / "juggler_cycle_defect_anticluster.md"
    ).read_text(encoding="utf-8")
    assert "## Branch budget" in dossier
    assert "## Decision" in dossier
    assert "## Publication assessment" in dossier
    assert "**CLOSE**" in dossier
    assert "Do not run phases" in dossier
    assert "juggler_cycle_defect_anticluster" in dossier
    rec = get_conjecture("juggler_cycle_defect_anticluster")
    assert rec["status"] == "REFUTED"
    assert rec["counterexamples"]
