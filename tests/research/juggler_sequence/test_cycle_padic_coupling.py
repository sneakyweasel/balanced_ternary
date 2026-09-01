"""Archimedean / p-adic coupling Phase 0. Not a halt test."""

from __future__ import annotations

import json
from pathlib import Path

from research.conjectures import get_conjecture
from research.literature import get_reference
from research.juggler_sequence.cycle_padic_coupling import (
    CLASS_CLOSED,
    FORBIDDEN_LEAN_FILES,
    FORBIDDEN_NEW_API,
    KNOWN_O,
    gap_mod_valuations,
    lean_api_present,
    leftover_row,
    lte_grid,
    lte_v2_pow_minus_1,
    lte_v3_pow_minus_1,
    realized_record,
    unit_obstruction,
    valuation,
)
from research.juggler_sequence.cycle_finance import o_min_and_theta

DOSSIER = Path("docs/problems/juggler_cycle_padic_coupling.md")
CONJECTURE = Path("conjectures/refuted/juggler_cycle_padic_coupling.json")
ARTIFACT = Path("data/research/juggler/cycle_padic_coupling/summary.json")


def test_finance_gap_is_2_unit_and_3_unit():
    for length, odd in ((19, 12), (84, 53), (569, 359), (1054, 665)):
        row = leftover_row(length, exact_gap=True)
        assert row["o"] == odd
        assert row["v2_exact"] == 0
        assert row["v3_exact"] == 0
        assert row["matches_lemma"] is True
        lemma = gap_mod_valuations(length, odd)
        assert lemma["v2"] == 0
        assert lemma["v3"] == 0


def test_modular_lemma_covers_survivor_seeds():
    for length, odd in KNOWN_O.items():
        row = gap_mod_valuations(length, odd)
        assert row["v2"] == 0
        assert row["v3"] == 0
        assert row["gap_odd"] is True


def test_known_o_matches_finance_on_short_leftovers():
    for length in (19, 84, 569, 1054):
        odd, _theta = o_min_and_theta(length)
        assert odd == KNOWN_O[length]


def test_ratio_is_not_a_p_adic_unit():
    rec = unit_obstruction(19, 12)
    assert rec["v2_of_ratio"] == 19
    assert rec["v3_of_ratio"] == -12
    assert rec["is_2_adic_unit"] is False
    assert rec["is_3_adic_unit"] is False
    assert rec["v2_of_ratio_minus_1"] == 0
    assert rec["chim_form_at_2"] is False
    assert rec["chim_form_at_3"] is False


def test_lte_matches_small_grid_and_length_nineteen_gap():
    grid = lte_grid(n_max=41, k_max=16)
    assert grid["ok"] is True
    assert lte_v2_pow_minus_1(13, 7153) == valuation(12, 2) == 2
    assert 13 % 3 == 1
    assert lte_v3_pow_minus_1(13, 7153) == valuation(12, 3) == 1
    assert lte_v2_pow_minus_1(3, 12) == 4
    assert valuation(3**12 - 1, 2) == 4


def test_odd_landing_last_chunk_has_no_forced_2_valuation():
    rec = realized_record(365, "OOE")
    assert rec["is_return"] is False
    assert rec["last_chunk_v2"] == 0
    assert rec["coupled"] is False
    assert rec["v2_n_minus_1"] == 2


def test_nineteen_gap_factors_are_not_2_or_3():
    gap = 3**12 - (1 << 19)
    assert gap == 7153
    assert valuation(gap, 2) == 0
    assert valuation(gap, 3) == 0
    assert gap % 23 == 0
    assert gap % 311 == 0


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
    decision = dossier.split("## Decision", 1)[1].split("## ", 1)[0]
    assert "CLOSE" in decision
    assert "PROMOTE" not in decision
    assert "not claimed" in dossier
    assert "chim-2025-two-p-adic-logarithms" in dossier
    assert "wu-wang-2014-irrationality-log3" in dossier
    assert "PadicCoupling.lean" in dossier
    record = json.loads(CONJECTURE.read_text(encoding="utf-8"))
    assert record["id"] == "juggler_cycle_padic_coupling"
    assert record["status"] == "REFUTED"
    assert record["not_a_halt_theorem"] is True
    assert record["counterexamples"]
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert payload["classification"] == CLASS_CLOSED
    assert payload["not_a_halt_theorem"] is True
    assert payload["not_residue_census"] is True
    assert payload["not_baker_reopen"] is True
    assert payload["any_coupled"] is False
    assert payload["lte_grid_ok"] is True


def test_literature_and_conjecture_registry():
    get_reference("chim-2025-two-p-adic-logarithms")
    get_reference("wu-wang-2014-irrationality-log3")
    get_reference("rhin-1987-pade-irrationality")
    conj = get_conjecture("juggler_cycle_padic_coupling")
    assert conj["status"] == "REFUTED"


def test_lean_api_has_identities_and_no_new_file():
    lean = lean_api_present()
    assert lean["sorry_free"] is True
    assert lean["global_defect_identity"] is True
    assert lean["image_eq_start_defectRatio"] is True
    assert lean["cycleMin_finance"] is True
    assert lean["not_in_paper_barrel"] is True
    for name in FORBIDDEN_NEW_API:
        assert lean[f"has_api_{name}"] is False, name
    for path in FORBIDDEN_LEAN_FILES:
        assert path.exists() is False
