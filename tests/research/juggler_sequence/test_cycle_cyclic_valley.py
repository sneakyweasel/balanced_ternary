"""Cyclic valley necklace. Not a halt test."""

from __future__ import annotations

import json
from pathlib import Path

from research.conjectures import get_conjecture
from research.juggler_sequence.cycle_almost_search import circuits, packed_block_word
from research.juggler_sequence.cycle_budget_opt import budget_rhs, run_type_counts
from research.juggler_sequence.cycle_cyclic_valley import (
    START,
    exact_chain,
    two_type_cheap_cap,
    two_type_cyclic_rhs,
    walk_runs,
)
from research.juggler_sequence.cycle_finance import o_min_and_theta
from research.juggler_sequence.cycle_prefix_feasibility import prefix_admissible

REPO = Path(__file__).resolve().parents[3]
DOSSIER = REPO / "docs" / "problems" / "juggler_cycle_cyclic_valley.md"
SUMMARY = (
    REPO
    / "data"
    / "research"
    / "juggler"
    / "cycle_finance"
    / "cyclic_valley"
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
    assert "2764" in text


def test_two_type_cheap_cap_is_n_oe():
    odd, _theta = o_min_and_theta(25781)
    even = 25781 - odd
    n_ooe, n_oe = run_type_counts(odd, even)
    assert n_ooe == 6751
    assert n_oe == 2764
    assert two_type_cheap_cap(odd, even) == n_oe
    assert n_oe < n_ooe


def test_cyclic_rhs_stays_above_theta_and_below_packing():
    odd, theta = o_min_and_theta(25781)
    cyclic = two_type_cyclic_rhs(START, 25781, odd)
    packed = budget_rhs(START, 25781, odd)
    assert cyclic < packed
    assert cyclic > theta
    assert cyclic / theta > 11.0


def test_beatty_packed_attains_the_cheap_cap():
    odd, _theta = o_min_and_theta(25781)
    word = packed_block_word(25781, odd)
    assert prefix_admissible(word)
    walked = walk_runs(circuits(word))
    assert walked["all_cyclemin"] is True
    assert walked["oe_illegal"] == 0
    assert walked["cheap"] == 2764


def test_interleave_oe_after_one_ooe_is_illegal():
    walked = walk_runs([(2, 1), (1, 1)] * 4)
    assert walked["all_cyclemin"] is False
    assert walked["oe_illegal"] >= 1


def test_365_true_wrap_does_not_close():
    row = exact_chain(365)
    assert row["wrap_first"] == 365
    assert row["true_wrap_closes"] is False
    assert all(not attempt["hits_first"] for attempt in row["wrap_attempts"])
    assert row["valleys"][:3] == [365, 763, 1749]


def test_science_artifact_closes():
    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert payload["bound"] == "cyclic_valley"
    assert payload["L"] == 25781
    cyclic = payload["two_type_cyclic"]
    assert cyclic["cheap_cap"] == 2764
    assert cyclic["lost_vs_packing"] == 3987
    assert cyclic["inside_k_lose"] is True
    assert cyclic["excludes"] is False
    assert cyclic["over_theta"] > 11.0
    decision = payload["decision"]
    assert decision["decision"] == "CLOSE"
    assert decision["classification"] == "CYCLIC_VALLEY_CLOSED"
    assert decision["leftover_killer"] is False
    assert decision["exact_wrap_closes"] is False
    assert decision["cap_survives_every_cut"] is True
    assert decision["wrap_is_privileged"] is False
    assert decision["small_m_independent_larger"] is True
    assert decision["halt_theorem"] is False
    assert decision["raise_n0"] is False
    assert decision["branch_and_bound"] is False
    assert payload["charged_excludes"]["parity_excludes"] is False
    assert payload["charged_excludes"]["budget_excludes"] is False
    assert payload["small_m"]["cyclic_beats_independent"] == 0
    legal = [row for row in payload["necklaces"] if row["all_cyclemin"]]
    assert legal
    assert all(row["cheap"] <= row["cheap_cap"] for row in legal)


def test_dossier_and_conjecture_record_close():
    dossier = DOSSIER.read_text(encoding="utf-8")
    assert "**CLOSE**" in dossier
    rec = get_conjecture("juggler_cycle_cyclic_valley")
    assert rec["status"] == "REFUTED"
    assert rec["counterexamples"]
