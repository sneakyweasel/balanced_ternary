"""Leftover length-six exclusions and the small-cycle census. Not a halt test."""

from __future__ import annotations

from pathlib import Path

from research.juggler_sequence.lean_paths import (
    BUNCHED_EEE,
    BUNCHED_EEOE,
    BUNCHED_EOEE,
    BUNCHED_EOEOE,
    BUNCHED_EOOEE,
    BUNCHED_EOOEOE,
    BUNCHED_EOOOEE,
    FIRST_E_TRANSPORT,
    GAPPED_CYCLE_WORD,
    LEFTOVER_CYCLES,
    LEFTOVER_EVAL,
    LEFTOVER_TWO_EVEN,
    SMALL_CYCLE_CENSUS,
    has_named,
    juggler_text,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
NOTE = REPO_ROOT / "docs" / "theory" / "juggler_finite_dynamics_note.md"


def test_leftover_cycle_theorems_present():
    text = juggler_text()
    leftover = LEFTOVER_CYCLES.read_text(encoding="utf-8")
    eval_src = LEFTOVER_EVAL.read_text(encoding="utf-8")
    assert has_named(text, "no_cycle_word_oooeoe")
    assert has_named(text, "no_cycle_word_ooooee")
    assert "theorem no_cycle_word_oooeoe" in leftover
    assert "theorem no_cycle_word_ooooee" in leftover
    assert "theorem no_cycle_word_ooooeoe" in leftover
    assert "theorem no_cycle_word_oooooee" in leftover
    assert "theorem no_cycle_word_ooooooeee" in leftover
    assert "theorem no_cycle_word_length_six" not in leftover
    assert "theorem no_cycle_word_length_nine" not in leftover
    assert has_named(text, "no_cycle_word_ooooeoe")
    assert has_named(text, "no_cycle_word_oooooee")
    assert has_named(text, "no_cycle_word_ooooooeee")
    assert has_named(text, "cycle_trailing_evens_lt")
    assert has_named(text, "no_cycle_word_two_even_ee")
    assert has_named(text, "no_cycle_word_two_even_eoe")
    two_even = LEFTOVER_TWO_EVEN.read_text(encoding="utf-8")
    assert "theorem no_cycle_word_two_even_ee" in two_even
    assert "theorem no_cycle_word_two_even_eoe" in two_even
    assert "theorem no_cycle_word_length_eight" not in two_even
    assert "theorem no_cycle_word_length_le_eight" not in two_even
    transport = FIRST_E_TRANSPORT.read_text(encoding="utf-8")
    assert "theorem no_cycleMin_gapped_three_even_ee" in transport
    assert "theorem no_cycleMin_gapped_three_even_eoe" in transport
    assert "theorem no_cycle_word_length_eight" not in transport
    assert "theorem no_cycle_word_length_nine" not in transport
    gapped = GAPPED_CYCLE_WORD.read_text(encoding="utf-8")
    assert "theorem no_cycle_word_gapped_three_even_ee" in gapped
    assert "theorem no_cycle_word_gapped_three_even_eoe" in gapped
    assert "theorem no_cycle_word_length_eight" not in gapped
    assert "theorem no_cycle_word_length_nine" not in gapped
    assert "sorry" not in gapped
    assert "admit" not in gapped
    assert has_named(text, "no_cycle_word_gapped_three_even_ee")
    assert has_named(text, "no_cycle_word_gapped_three_even_eoe")
    bunched = BUNCHED_EEE.read_text(encoding="utf-8")
    assert "theorem no_cycle_word_three_even_eee" in bunched
    assert "theorem three_even_eee_tail" in bunched
    assert "theorem no_cycle_word_length_eight" not in bunched
    assert "theorem no_cycle_word_length_nine" not in bunched
    assert "sorry" not in bunched
    assert "admit" not in bunched
    assert has_named(text, "no_cycle_word_three_even_eee")
    eoee = BUNCHED_EOEE.read_text(encoding="utf-8")
    assert "theorem no_cycle_word_three_even_eoee" in eoee
    assert "theorem no_cycle_word_length_eight" not in eoee
    assert "theorem no_cycle_word_length_nine" not in eoee
    assert "sorry" not in eoee
    assert "admit" not in eoee
    assert has_named(text, "no_cycle_word_three_even_eoee")
    eooee = BUNCHED_EOOEE.read_text(encoding="utf-8")
    assert "theorem no_cycle_word_three_even_eooee" in eooee
    assert "theorem no_cycle_word_length_eight" not in eooee
    assert "theorem no_cycle_word_length_nine" not in eooee
    assert "sorry" not in eooee
    assert "admit" not in eooee
    assert has_named(text, "no_cycle_word_three_even_eooee")
    eeoe = BUNCHED_EEOE.read_text(encoding="utf-8")
    assert "theorem no_cycle_word_three_even_eeoe" in eeoe
    assert "theorem no_cycle_word_length_eight" not in eeoe
    assert "theorem no_cycle_word_length_nine" not in eeoe
    assert "sorry" not in eeoe
    assert "admit" not in eeoe
    assert has_named(text, "no_cycle_word_three_even_eeoe")
    eoeoe = BUNCHED_EOEOE.read_text(encoding="utf-8")
    assert "theorem no_cycle_word_three_even_eoeoe" in eoeoe
    assert "theorem no_cycle_word_length_eight" not in eoeoe
    assert "theorem no_cycle_word_length_nine" not in eoeoe
    assert "sorry" not in eoeoe
    assert "admit" not in eoeoe
    assert has_named(text, "no_cycle_word_three_even_eoeoe")
    eoooee = BUNCHED_EOOOEE.read_text(encoding="utf-8")
    assert "theorem no_cycle_word_three_even_eoooee" in eoooee
    assert "theorem no_cycle_word_length_eight" not in eoooee
    assert "theorem no_cycle_word_length_nine" not in eoooee
    assert "sorry" not in eoooee
    assert "admit" not in eoooee
    assert has_named(text, "no_cycle_word_three_even_eoooee")
    eooeoe = BUNCHED_EOOEOE.read_text(encoding="utf-8")
    assert "theorem no_cycle_word_three_even_eooeoe" in eooeoe
    assert "theorem no_cycle_word_length_eight" not in eooeoe
    assert "theorem no_cycle_word_length_nine" not in eooeoe
    assert "sorry" not in eooeoe
    assert "admit" not in eooeoe
    assert has_named(text, "no_cycle_word_three_even_eooeoe")
    assert "sorry" not in transport
    assert "admit" not in transport
    assert "sorry" not in leftover
    assert "admit" not in leftover
    assert "sorry" not in eval_src
    assert "admit" not in eval_src
    assert "sorry" not in two_even
    assert "admit" not in two_even
    assert "native_decide" in eval_src
    assert "theorem juggler_reaches_one" not in leftover
    assert "def CycleSearch" not in leftover
    assert "PowerHeight" not in leftover


def test_small_cycle_census_theorems_present():
    census = SMALL_CYCLE_CENSUS.read_text(encoding="utf-8")
    assert "theorem no_cycle_word_length_le_six" in census
    assert "theorem no_cycle_word_length_le_seven" in census
    assert "theorem no_cycle_word_length_nine" not in census
    assert "theorem no_cycle_word_replicate_odd" in census
    assert "theorem cycleWord_exists_even_terminating" in census
    assert "theorem no_cycle_word_len_six_ends_even" in census
    assert "theorem no_cycle_word_len_seven_ends_even" in census
    assert "sorry" not in census
    assert "admit" not in census
    # The census is an assembly of existing exclusions; it needs no new
    # native_decide tables of its own.
    assert "native_decide" not in census
    assert "theorem juggler_reaches_one" not in census
    # Scope discipline: length eight stays open.
    assert "Length eight is open" in census


def test_note_records_census_without_overclaim():
    note = NOTE.read_text(encoding="utf-8")
    assert "Lemma 3.5" in note
    assert "Theorem 3.6" in note
    assert "Lemma 3.7" in note
    assert "Theorem 3.8" in note
    assert "Theorem 3.12" in note
    assert "Theorem 3.13" in note
    assert "Theorem 3.14" in note
    assert "Theorem 3.15" in note
    assert "Theorem 3.16" in note
    assert "Theorem 3.17" in note
    assert "Theorem 3.18" in note
    assert "Theorem 3.19" in note
    assert "Theorem 3.20" in note
    assert "Theorem 3.21" in note
    assert "remain open" not in note
    assert "OOOEOE" in note
    assert "OOOOEE" in note
    assert "OOOOEOE" in note
    assert "OOOOOEE" in note
    assert "no_cycle_word_length_le_six" in note
    assert "no_cycle_word_length_le_seven" in note
    assert "no_cycle_word_two_even_ee" in note
    assert "no_cycle_word_three_even_eee" in note
    assert "no_cycle_word_three_even_eoee" in note
    assert "no_cycle_word_three_even_eooee" in note
    assert "no_cycle_word_three_even_eoooee" in note
    assert "no_cycle_word_three_even_eeoe" in note
    assert "no_cycle_word_three_even_eoeoe" in note
    assert "no_cycle_word_three_even_eooeoe" in note
    assert "no_cycle_word_gapped_three_even_ee" in note
    assert "no_cycle_word_gapped_three_even_eoe" in note
    assert "theorem no_cycle_word_length_eight" not in note
    assert "theorem no_cycle_word_length_nine" not in note
    flat = " ".join(note.split())
    assert "No exclusion of cycles of length eight or more is claimed." in flat
    assert "no exclusion at length eight is claimed" in flat
