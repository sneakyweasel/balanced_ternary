"""Leftover length-six cycle orientations. Not a census or halt test."""

from __future__ import annotations

from pathlib import Path

from research.juggler_sequence.lean_paths import (
    LEFTOVER_CYCLES,
    LEFTOVER_EVAL,
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
    assert "theorem no_cycle_word_length_six" not in leftover
    assert "theorem no_cycle_word_ooooeoe" not in leftover
    assert "sorry" not in leftover
    assert "admit" not in leftover
    assert "sorry" not in eval_src
    assert "admit" not in eval_src
    assert "native_decide" in eval_src
    assert "theorem juggler_reaches_one" not in leftover
    assert "def CycleSearch" not in leftover
    assert "PowerHeight" not in leftover


def test_note_records_theorem_32_without_open_gap():
    note = NOTE.read_text(encoding="utf-8")
    assert "Theorem 3.2" in note
    assert "remain open" not in note
    assert "OOOEOE" in note
    assert "OOOOEE" in note
    assert "not an exclusion of every length-six word" in note
