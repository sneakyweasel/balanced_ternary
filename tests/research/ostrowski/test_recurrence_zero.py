"""Recurrence word is a zero-sum reset. Not an L_0 bound.

Algebraic zero-sum is not fully live. A reset is not a family.
"""

from __future__ import annotations

from research.ostrowski.energy_trajectory import apply_word, consumed_sum
from research.ostrowski.exceptional_kernel import W_LSD
from research.ostrowski.live_layers import ORIGIN
from research.ostrowski.recurrence_zero import (
    ALGEBRAIC_ZERO,
    FULLY_LIVE,
    GROWTH_NOT_INFINITUDE,
    KNOWN_PACKAGING,
    LSD_NOT_INTERIOR,
    PREFIX_LEGAL,
    RECURRENCE_WORD_MSD,
    RESET_NOT_FAMILY,
    classify_word,
    convolution_matches_c_b,
    enumerate_combos,
    lattice_words,
    msd_val,
    phase0_recurrence_zero,
    recurrence_word_val_zero,
    val_equals_minus_s3,
)
from research.ostrowski.system import nonpisot_order3


def test_msd_val_is_consumed_sum_and_minus_s3():
    sys = nonpisot_order3()
    word = RECURRENCE_WORD_MSD
    assert msd_val(word, 4) == consumed_sum(sys, 4, word)
    assert val_equals_minus_s3(word)
    assert apply_word(sys, ORIGIN, word)[2] == -msd_val(word, 4)
    for n in range(6):
        assert recurrence_word_val_zero(n)
        assert msd_val(word, n + 4) == 0


def test_star_is_algebraic_zero_reset_not_lsd():
    row = classify_word(RECURRENCE_WORD_MSD)
    assert row["word"] == (1, -2, -1, -3)
    assert row[ALGEBRAIC_ZERO]
    assert row["reset"]
    assert row["c_B"] == ORIGIN
    assert row["lsd_legal_complete"] is False
    assert RECURRENCE_WORD_MSD[-1] not in W_LSD
    assert row[PREFIX_LEGAL]
    assert row[FULLY_LIVE]
    assert row["fully_live_complete"] is False
    assert row["convolution_ok"]
    assert convolution_matches_c_b(RECURRENCE_WORD_MSD)
    assert row["iteration"]["live_all"]
    assert row["iteration"]["grew"] is False
    assert row["candidate_expander"] is False
    assert row[RESET_NOT_FAMILY]
    assert row[LSD_NOT_INTERIOR]
    assert row[GROWTH_NOT_INFINITUDE]
    assert row[KNOWN_PACKAGING]


def test_short_combos_are_resets_not_a_family():
    assert lattice_words(4) == [RECURRENCE_WORD_MSD]
    rows = enumerate_combos(6)
    assert len(rows) == 11
    assert all(r[ALGEBRAIC_ZERO] for r in rows)
    assert all(r["reset"] for r in rows)
    assert all(r["c_B"] == ORIGIN for r in rows)
    assert all(r["candidate_expander"] is False for r in rows)
    lsd_live = [r for r in rows if r["fully_live_complete"]]
    assert len(lsd_live) == 4
    assert all(r["word"][-1] in W_LSD for r in lsd_live)
    report = phase0_recurrence_zero()
    assert report["n_combos"] == 11
    assert report["n_reset"] == 11
    assert report["n_iterate_live_nonreset"] == 0
    assert report["expanders"] == []
    assert report["symbolic_family"] is False
    assert report["val_star_zero"]
    assert report[RESET_NOT_FAMILY]
    assert report[GROWTH_NOT_INFINITUDE]
