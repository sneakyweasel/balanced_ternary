"""Realizable-prefix finance. Not a halt test."""

from __future__ import annotations

import json
from pathlib import Path

from research.conjectures import get_conjecture
from research.juggler_sequence.cycle_conditioned_closure import deficit_row
from research.juggler_sequence.cycle_finance import PUBLISHED_FLOOR
from research.juggler_sequence.cycle_realizable_finance import (
    completed_ooe_blocks,
    false_implication_row,
    prefix_tax_row,
    slack_row,
)

REPO = Path(__file__).resolve().parents[3]
DOSSIER = REPO / "docs" / "problems" / "juggler_cycle_realizable_finance.md"
SUMMARY = (
    REPO
    / "data"
    / "research"
    / "juggler"
    / "cycle_finance"
    / "realizable_finance"
    / "summary.json"
)


def test_dossier_has_triage_and_closed_gates():
    text = DOSSIER.read_text(encoding="utf-8")
    assert "## Branch budget" in text
    assert "Mathematical target" in text
    assert "## Closed-bridge gates" in text
    assert "## Decision" in text
    assert "## Publication assessment" in text
    assert "**CLOSE**" in text
    assert "branch-and-bound" in text
    assert "6532" in text
    assert "Do **not** prove" in text or "K\\le 20" in text or "K<=20" in text


def test_slack_matches_conditioned_closure():
    slack = slack_row()
    row = deficit_row(25781, floor=PUBLISHED_FLOOR)
    assert abs(slack["packed_over_theta"] - row["packed_over_theta"]) < 1e-12
    assert slack["k_lose_cheap"] == 6532
    assert slack["deepen_all_still_above_theta"] is True
    assert slack["margin"] > 0.0


def test_floor_prefix_tax_is_zero_on_two_ooe():
    walk = prefix_tax_row(1_000_057, "OOE" * 6)
    assert walk["R"] == 7
    assert walk["completed_ooe"] == 2
    assert walk["prefix_tax"] is not None
    assert abs(walk["prefix_tax"]) < 1e-12


def test_local_ooe_cap_is_not_a_valid_killer():
    slack = slack_row()
    row = false_implication_row(1_000_057, "OOE" * 6, slack)
    assert row["completed_ooe"] == 2
    assert row["implied_loss"] == slack["n_ooe"] - 2
    assert row["implied_loss"] > slack["k_lose_cheap"]
    assert row["would_kill_if_local_were_global"] is True
    assert row["implication_valid"] is False


def test_365_completes_four_bunched_ooe():
    assert completed_ooe_blocks(365, "OOE" * 8) == 4


def test_science_artifact_closes():
    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert payload["bound"] == "realizable_finance"
    assert payload["L"] == 25781
    decision = payload["decision"]
    assert decision["decision"] == "CLOSE"
    assert decision["classification"] == "REALIZABLE_FINANCE_CLOSED"
    assert decision["prefix_tax_zero"] is True
    assert decision["false_implication_valid"] is False
    assert decision["false_implication_would_kill"] is True
    assert decision["max_forced_start_deviations"] <= 2
    assert decision["forced_start_inside_slack"] is True
    assert decision["deepen_all_still_above_theta"] is True
    assert decision["no_two_type_cycle_would_kill"] is False
    assert decision["leftover_killer"] is False
    assert decision["halt_theorem"] is False
    assert decision["raise_n0"] is False
    assert decision["open_55293"] is False
    assert decision["k20_proof"] is False
    assert decision["branch_and_bound"] is False
    assert payload["charged_excludes"]["parity_excludes"] is False
    assert payload["charged_excludes"]["budget_excludes"] is False


def test_dossier_and_conjecture_record_close():
    dossier = DOSSIER.read_text(encoding="utf-8")
    assert "**CLOSE**" in dossier
    rec = get_conjecture("juggler_cycle_realizable_finance")
    assert rec["status"] == "REFUTED"
    assert rec["counterexamples"]
