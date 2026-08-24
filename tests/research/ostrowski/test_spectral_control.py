"""Origin residual is the control convolution. Not an L_0 bound.

The impulse A^r e3 is the place-value triple. Large |s| does not
force unique Ext. Normalized |λ|^{-k}|z| bounded is not residual
boundedness.
"""

from __future__ import annotations

from research.ostrowski.ext_feasibility import live_ext
from research.ostrowski.live_layers import ORIGIN, forward_layers, linf
from research.ostrowski.spectral_control import (
    EXT_NOT_UNIQUE,
    GROWTH_NOT_INFINITUDE,
    IMPULSE_IS_PLACE,
    KNOWN_PACKAGING,
    N12_MAXIMIZER_STATE,
    N12_MAXIMIZER_WORD,
    NORMALIZED_NOT_RESIDUAL,
    SCALAR_FORCING,
    THREE_EXPANDING,
    all_embeddings_expanding,
    compare_remaining_zero,
    control_convolution,
    control_convolution_reindexed,
    convolution_matches_apply_word,
    energy_of_particular_holds,
    impulse_matches_place,
    impulse_recurrence_holds,
    large_s_ext_not_unique,
    ostrowski_s1,
    ostrowski_s3,
    place_impulse,
    scalar_forcing_holds,
    z_from_word,
    z_step_holds,
)
from research.ostrowski.system import nonpisot_order3


def test_convolution_matches_apply_word():
    samples = (
        (),
        (0,),
        (-4, 2),
        (1, -3, 0, 2),
        (-4, -4, -4, 1, 1),
        N12_MAXIMIZER_WORD,
    )
    for word in samples:
        assert convolution_matches_apply_word(word)
        assert control_convolution(word) == control_convolution_reindexed(word)
        assert z_from_word(word) == control_convolution(word)
        assert energy_of_particular_holds(16, word)
        assert control_convolution(word)[0] == ostrowski_s1(word)
        assert control_convolution(word)[2] == ostrowski_s3(word)
        assert scalar_forcing_holds(word)


def test_impulse_is_place_value():
    assert place_impulse(0) == (0, 0, 1)
    assert place_impulse(1) == (3, 1, 2)
    assert place_impulse(2) == (6, 5, 5)
    assert place_impulse(3) == (15, 11, 15)
    for r in range(12):
        assert impulse_matches_place(r)
    for r in range(8):
        assert impulse_recurrence_holds(r)


def test_z_recurrence_is_companion_step():
    assert z_step_holds(ORIGIN, 0)
    assert z_step_holds((-3, -1, 0), -4)
    assert z_step_holds((6, 5, 1), 2)
    assert z_step_holds((15, 2, -2), -1)
    assert z_step_holds((-27, -6, 0), 1)


def test_all_three_embeddings_expand():
    report = all_embeddings_expanding()
    assert report["all_gt_one"]
    assert report[THREE_EXPANDING]
    assert report[NORMALIZED_NOT_RESIDUAL]


def test_unnormalized_mode_grows_on_remaining_zero():
    cmp = compare_remaining_zero(12, 16)
    assert cmp["small"]["L0"] == 165
    assert cmp["large"]["L0"] == 379
    assert cmp["small"]["max_linf"] == 27
    assert cmp["large"]["max_linf"] == 37
    assert cmp["unnormalized_z_grows"]
    assert cmp["coeff_norm_grows"]
    assert cmp["uniform_cancellation_refuted"]
    assert cmp["symbolic_family"] is False
    assert cmp["maximizer_all_constant"] is False
    assert cmp[GROWTH_NOT_INFINITUDE]
    assert cmp[NORMALIZED_NOT_RESIDUAL]
    assert cmp[KNOWN_PACKAGING]
    top = cmp["small"]["maximizers"][0]
    assert top["state"] == N12_MAXIMIZER_STATE
    assert top["convolution_ok"]
    assert top["word"] == N12_MAXIMIZER_WORD


def test_layer_prefix_is_the_particular():
    sys = nonpisot_order3()
    fwd = forward_layers(sys, 12, live_only=True)
    s_max = fwd["layers"][0]["s_max"]
    prefix = fwd["layers"][0]["prefix"]
    assert s_max is not None and prefix is not None
    assert control_convolution(prefix) == s_max
    assert control_convolution_reindexed(prefix) == s_max


def test_large_s_does_not_force_unique_ext():
    report = large_s_ext_not_unique()
    assert report["refuted"]
    assert report[EXT_NOT_UNIQUE]
    assert SCALAR_FORCING
    assert IMPULSE_IS_PLACE
    large = [row for row in report["witnesses"] if row["linf"] >= 8]
    assert large
    hit = next(row for row in large if row["remaining"] == 5)
    assert hit["state"] == (12, -2, -1)
    assert hit["ext"] == (-1, 0, 1)
    assert len(hit["ext"]) > 1
    assert linf(hit["state"]) >= 8
    assert live_ext((12, -2, -1), 5) == (-1, 0, 1)
