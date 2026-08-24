"""Zero-value complete words need not reset and are not a monoid.

Identically zero-for-all-alignments remains the recurrence reset
sublattice. Zero at one alignment is the fiber on F. Live complete
remaining-0 is L_0(N). Val_s(B) is energy_telescope at remaining 0.
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
    BLOCK_VAL_IS_S3,
    FULLY_LIVE,
    GROWTH_NOT_INFINITUDE,
    HUB,
    HUB_SQUARE,
    HUB_SQUARE_STATE,
    HUB_SQUARE_VAL,
    KNOWN_PACKAGING,
    L0_N12_COUNT,
    L0_N12_LINF,
    LIVE_IS_L0,
    NOT_MONOID,
    PREFIX_LEGAL,
    RAY_NOT_FAMILY,
    SHORTEST_NONRESET,
    TELESCOPE_PACKAGING,
    VAL_CONCAT_ENERGY,
    VAL_NOT_RESET,
    affine_holds,
    block_val,
    block_val_holds,
    c3_equals_minus_val,
    census_complete,
    classify_complete,
    complete_words,
    consumed_sum_append_holds,
    coordinates_match_impulse,
    hub_block_iterates,
    hub_square_witness,
    hub_witness,
    msd_val,
    n12_maximizer_off_ray,
    on_legal_two_step_ray,
    on_two_step_ray_line,
    phase0_zero_value_kernel,
    t_of,
    val_concat_energy_holds,
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
    assert report["live_fiber_N12"]["is_L0"]
    assert N12_MAXIMIZER_STATE[2] == 0
    assert report[VAL_NOT_RESET]
    assert report[RAY_NOT_FAMILY]
    assert report[KNOWN_PACKAGING]


def test_consumed_sum_splits_at_two_starts():
    pairs = (
        (SHORTEST_NONRESET, SHORTEST_NONRESET),
        (SHORTEST_NONRESET, (0,)),
        ((0,), SHORTEST_NONRESET),
        (RECURRENCE_WORD_MSD, (0,)),
        ((), SHORTEST_NONRESET),
        (SHORTEST_NONRESET, ()),
    )
    for n in range(3):
        for u, v in pairs:
            assert consumed_sum_append_holds(n, u, v)
            assert val_concat_energy_holds(u, v)


def test_complete_zero_value_is_not_a_monoid():
    square = hub_square_witness()
    assert HUB_SQUARE == (1, -2, 1, -2)
    assert msd_val(SHORTEST_NONRESET) == 0
    assert square["val"] == HUB_SQUARE_VAL == 5
    assert square["c_B"] == HUB_SQUARE_STATE == (-6, -2, -5)
    assert square["on_F"] is False
    assert square[NOT_MONOID]
    assert square[VAL_CONCAT_ENERGY]
    assert msd_val((0,) + SHORTEST_NONRESET) == 0
    report = phase0_zero_value_kernel()
    assert report["consumed_sum_append"]
    assert report["val_concat_energy"]
    assert report[NOT_MONOID]
    assert report[VAL_CONCAT_ENERGY]
    assert report["reset_then_hub_zero"]


def test_live_complete_zero_is_existing_L0_off_the_two_step_ray():
    off = n12_maximizer_off_ray()
    assert off["state"] == N12_MAXIMIZER_STATE == (-27, -6, 0)
    assert off["on_F"]
    assert off["on_two_step_legal_ray"] is False
    assert on_legal_two_step_ray(HUB)
    assert not on_legal_two_step_ray(N12_MAXIMIZER_STATE)
    assert off[LIVE_IS_L0]
    assert off[GROWTH_NOT_INFINITUDE]
    report = phase0_zero_value_kernel()
    assert report[LIVE_IS_L0]
    assert report["live_fiber_N12"]["is_L0"]


def test_block_val_is_minus_s3_off_origin():
    seeds = (ORIGIN, HUB, N12_MAXIMIZER_STATE)
    words = ((), (0,), SHORTEST_NONRESET, RECURRENCE_WORD_MSD, (1, 0, -2))
    for state in seeds:
        for word in words:
            assert block_val_holds(state, word)
            assert t_of(state, word)[2] == -block_val(state, word)
            if word:
                assert affine_holds(word, state)
    report = phase0_zero_value_kernel()
    assert report["block_val_is_minus_s3"]
    assert report["affine_holds_off_origin"]
    assert report[BLOCK_VAL_IS_S3]
    assert report[TELESCOPE_PACKAGING]


def test_hub_iterates_stay_on_bounded_ray_not_a_family():
    it = hub_block_iterates()
    assert it["from_origin"] == HUB
    assert it["from_origin_on_ray"]
    assert it["from_hub_on_F"] is False
    assert it["from_hub"] == HUB_SQUARE_STATE
    assert it["legal_on_ray_line"]
    assert it["legal_k_bounded"]
    assert it["legal_ks"] == (0, 1, 2)
    assert all(on_two_step_ray_line(s) for s in it["legal_from_hub"])
    assert it["symbolic_family"] is False
    assert it[RAY_NOT_FAMILY]
    assert it[GROWTH_NOT_INFINITUDE]
    report = phase0_zero_value_kernel()
    assert report["hub_iterates"]["legal_k_bounded"]
    assert report["symbolic_family"] is False
