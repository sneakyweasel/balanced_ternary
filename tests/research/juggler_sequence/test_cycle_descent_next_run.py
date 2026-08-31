"""Cheap-band descent next-run type. Not a halt test."""

from __future__ import annotations

import json
from pathlib import Path

from research.conjectures import get_conjecture
from research.juggler_sequence.block_map_q import a_of, block_map
from research.juggler_sequence.cycle_descent_next_run import (
    CHEAP_LIFT,
    START,
    cheap_band_hi,
    in_cheap_band,
    one_even_peak,
    one_even_witness,
    spotlight_6187,
)
from research.juggler_sequence.cycle_ordered_excursion import excursion_map

REPO = Path(__file__).resolve().parents[3]
SUMMARY = (
    REPO
    / "data"
    / "research"
    / "juggler"
    / "cycle_finance"
    / "descent_next_run"
    / "summary.json"
)


def test_one_even_descent_hits_a2_in_the_cheap_band():
    row = one_even_witness(START)
    assert row is not None
    assert row["p"] == 1000057
    assert row["a"] == 2
    assert row["peak"] == one_even_peak(1000057)
    assert row["peak_ge_n2"]
    assert in_cheap_band(row["p"], START)
    assert a_of(1000057) == 2


def test_post_ooe_descent_from_first_a2_starts_a2():
    rec = excursion_map(1000057, 2)
    assert rec is not None
    peak, landing = rec
    assert landing == 5623773
    assert peak == 31626832356906
    assert peak >= START * START
    assert in_cheap_band(landing, START)
    assert a_of(landing) == 2
    assert landing < cheap_band_hi(START, CHEAP_LIFT)


def test_6187_q_descent_is_not_a_cyclemin_falsifier():
    row = spotlight_6187()
    assert row["matches_named"]
    assert row["mid"] == block_map(11189) == 1087
    assert row["end"] == block_map(1087) == 189
    assert row["a_mid"] == 1
    assert row["a_end"] == 1
    assert row["cyclemin_legal"] is False
    assert row["is_falsifier"] is False


def test_artifact_records_the_refutation():
    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert payload["n"] == START
    assert payload["lift"] == 19
    assert payload["slogan_false"] is True
    assert payload["one_even_a2"] is True
    assert payload["post_ooe_a2"] is True
    assert payload["one_even"]["p"] == 1000057
    assert payload["first_post_ooe_pair"]["v"] == 1000057
    assert payload["first_post_ooe_pair"]["p"] == 5623773
    assert payload["first_post_ooe_pair"]["a"] == 2
    assert payload["post_ooe"]["a2_after_descent"] == 297
    assert payload["post_ooe"]["landings_in_band"] == 1210
    assert payload["spotlight_6187"]["is_falsifier"] is False


def test_dossier_and_conjecture_record_close():
    dossier = (
        REPO / "docs" / "problems" / "juggler_cycle_descent_next_run.md"
    ).read_text(encoding="utf-8")
    assert "## Branch budget" in dossier
    assert "## Decision" in dossier
    assert "## Publication assessment" in dossier
    decision = dossier.split("## Decision", 1)[1].split("## ", 1)[0]
    assert "CLOSE" in decision
    rec = get_conjecture("juggler_cycle_descent_next_run")
    assert rec["status"] == "REFUTED"
    assert rec["counterexamples"]
