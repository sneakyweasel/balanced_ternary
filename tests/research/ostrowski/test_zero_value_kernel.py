"""Zero-value complete words need not reset. Not an L_0 bound.

Identically zero-for-all-alignments remains the recurrence reset
sublattice. Zero at one alignment is the fiber on F.
"""

from __future__ import annotations

from research.ostrowski.energy_trajectory import apply_word, consumed_sum
from research.ostrowski.exceptional_kernel import W_LSD
from research.ostrowski.live_layers import ORIGIN
from research.ostrowski.recurrence_zero import RECURRENCE_WORD_MSD, enumerate_combos
from research.ostrowski.spectral_control import N12_MAXIMIZER_STATE, ostrowski_s3
from research.ostrowski.system import nonpisot_order3
from research.ostrowski.zero_value_kernel import (
    ALGEBRAIC_ZERO,
    FULLY_LIVE,
    GROWTH_NOT_INFINITUDE,
    HUB,
    KNOWN_PACKAGING,
    L0_N12_COUNT,
    L0_N12_LINF,
    PREFIX_LEGAL,
    RAY_NOT_FAMILY,
    SHORTEST_NONRESET,
    VAL_NOT_RESET,
    c3_equals_minus_val,
    census_complete,
    classify_complete,
    complete_words,
    coordinates_match_impulse,
    hub_witness,
    msd_val,
    phase0_zero_value_kernel,
)


def test_c3_equals_minus_val():
    sys = nonpisot_order3()
    samples = ((), (0,), (1, -2), (-1, 2), RECURRENCE_WORD_MSD, (1, 0, -2))
    for word in samples:
        assert c3_equals_minus_val(word)
        assert apply_word(sys, ORIGIN, word)[2] == -msd_val(word)
        assert ostrowski_s3(word) == -consumed_sum(sys, len(word), word)
        assert coordinates_match_impulse(word)


def test_shortest_nonreset_is_known_hub():
    row = classify_complete(SHORTEST_NONRESET)
    hub = hub_witness()
    assert SHORTEST_NONRESET == (1, -2)
    assert SHORTEST_NONRESET[-1] in W_LSD
    assert row[ALGEBRAIC_ZERO]
    assert row["val"] == 0
    assert row["c_B"] == HUB == (-3, -1, 0)
    assert row["reset"] is False
    assert row["nonreset"]
    assert row[PREFIX_LEGAL]
    assert row[FULLY_LIVE]
    assert row["on_F"]
    assert hub["c_B_is_hub"]
    assert hub["two_step_image"] == HUB
    assert hub[RAY_NOT_FAMILY]
    assert hub[GROWTH_NOT_INFINITUDE]


def test_k_star_is_two_among_complete_words():
    census = census_complete(4)
    assert census["k_star"] == 2
    assert census["shortest"] == ((1, -2),)
    rows = {r["k"]: r for r in census["rows"]}
    assert rows[1]["Z"] == 1 and rows[1]["nonresets"] == 0
    assert rows[2]["Z"] == 2 and rows[2]["nonresets"] == 1
    assert rows[2]["live_nonresets"] == 1
    assert rows[2]["max_c_linf"] == 3
    assert all(w[-1] in W_LSD for w in complete_words(2))
    assert census[VAL_NOT_RESET]
    assert census[GROWTH_NOT_INFINITUDE]


def test_star_and_recurrence_combos_remain_reset_sublattice():
    star = classify_complete(RECURRENCE_WORD_MSD)
    assert star[ALGEBRAIC_ZERO]
    assert star["reset"]
    assert star["c_B"] == ORIGIN
    assert star["nonreset"] is False
    combos = enumerate_combos(6)
    assert len(combos) == 11
    assert all(r["reset"] for r in combos)
    report = phase0_zero_value_kernel()
    assert report["c3_equals_minus_val"]
    assert report["coordinates_match"]
    assert report["star_reset"]
    assert report["recurrence_combos_all_reset"]
    assert report["k_star"] == 2
    assert report["symbolic_family"] is False
    assert report["live_fiber_N12"]["count"] == L0_N12_COUNT == 165
    assert report["live_fiber_N12"]["max_linf"] == L0_N12_LINF == 27
    assert N12_MAXIMIZER_STATE[2] == 0
    assert report[VAL_NOT_RESET]
    assert report[RAY_NOT_FAMILY]
    assert report[KNOWN_PACKAGING]
