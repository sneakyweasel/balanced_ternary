"""Leftover length-six exclusions and the small-cycle census. Not a halt test."""

from __future__ import annotations

from pathlib import Path

from research.juggler_sequence.lean_paths import (
    LEFTOVER_CYCLES,
    LEFTOVER_EVAL,
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
    assert "sorry" not in leftover
    assert "admit" not in leftover
    assert "sorry" not in eval_src
    assert "admit" not in eval_src
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
    assert "remain open" not in note
    assert "OOOEOE" in note
    assert "OOOOEE" in note
    assert "OOOOEOE" in note
    assert "OOOOOEE" in note
    assert "no_cycle_word_length_le_six" in note
    assert "no_cycle_word_length_le_seven" in note
    flat = " ".join(note.split())
    assert "No exclusion of cycles of length eight or more is claimed." in flat
    assert "no exclusion at length eight is claimed" in flat
