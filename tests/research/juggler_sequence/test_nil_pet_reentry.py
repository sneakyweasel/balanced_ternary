"""PET re-entry: Mal'cev difference identity and GG species of A{ΔB}."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

from research.juggler_sequence.nil_pet_reentry import (
    ANTI,
    CLASS_GREEN,
    TEST_BLOCKS,
    build_summary,
    pet_difference,
    pet_identity_check,
    species_check,
)
from research.literature import get_reference

DOSSIER = Path("docs/problems/juggler_nil_pet_reentry.md")
CONJECTURE = Path(
    "conjectures/active/juggler_tower_rate_free_equidistribution.json"
)
REFUTED = Path("conjectures/refuted/juggler_nil_pet_stays_coordinate.json")
LIT_IDS = ("host-kra-2005-nilmanifolds",)


def test_pet_difference_identity_is_exact():
    for a, b, ap, bp in (
        (Fraction(37, 13), Fraction(155, 17), Fraction(41, 13), Fraction(200, 17)),
        (Fraction(3, 2), Fraction(9, 4), Fraction(2), Fraction(3)),
        (Fraction(-5, 2), Fraction(11, 7), Fraction(-1, 4), Fraction(20, 7)),
    ):
        d = pet_difference(a, b, ap, bp)
        assert d["raw_x"] == d["pred_x"] == ap - a
        assert d["raw_y"] == d["pred_y"] == bp - b
        assert d["raw_z"] == d["pred_z"] == -a * (bp - b)
        assert d["chi"] == d["split"]


def test_pet_identity_check_passes():
    r = pet_identity_check()
    assert r["exact_identity"]
    assert r["scaled_identity"]


def test_species_is_gg_and_leftover_not_o1():
    s = species_check(TEST_BLOCKS)
    assert s["pairs"] > 0
    assert s["increment_gg"]
    assert s["leftover_not_o1"]
    assert s["frac_not_tiny"]
    assert s["reentry"]
    assert s["mean_da_over_n18"] > 1.0
    assert s["mean_leftover_over_n34"] > 0.05


def test_summary_green_and_anti_overclaim():
    summary = build_summary(TEST_BLOCKS)
    assert summary["decision"]["classification"] == CLASS_GREEN
    assert summary["decision"]["branch"] == "PROMOTE"
    assert summary["decision"]["method"] == "CLOSE"
    assert summary["decision"]["conjecture"] == "ACTIVE"
    assert not ANTI["equidistribution_claimed"]
    assert not ANTI["k3_bound_claimed"]
    assert not ANTI["toolkit_reopened"]
    assert not ANTI["paper_b_modified"]
    assert not ANTI["pet_proves_equidistribution"]
    assert not ANTI["conjecture_refuted"]


def test_dossier_and_records():
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
    assert "PROMOTE" in decision
    assert "J-nil-pet-reentry" in dossier
    assert "not a Paper B" in dossier or "Not a Paper B" in dossier
    rec = get_reference(LIT_IDS[0])
    assert rec["id"] == LIT_IDS[0]
    assert '"status": "ACTIVE"' in CONJECTURE.read_text(encoding="utf-8")
    refuted = REFUTED.read_text(encoding="utf-8")
    assert '"status": "REFUTED"' in refuted
    assert "amplitude-product" in refuted


def test_conjecture_notes_record_pet_reentry():
    text = CONJECTURE.read_text(encoding="utf-8")
    assert "J-nil-pet-reentry" in text or "PET" in text
