"""Origin residual is the control convolution. Not an L_0 bound.

Unnormalized embeddings grow on remaining 0. Normalized |λ|^{-k}|z|
bounded is not residual boundedness.
"""

from __future__ import annotations

from research.ostrowski.live_layers import ORIGIN, forward_layers
from research.ostrowski.spectral_control import (
    GROWTH_NOT_INFINITUDE,
    KNOWN_PACKAGING,
    NORMALIZED_NOT_RESIDUAL,
    THREE_EXPANDING,
    all_embeddings_expanding,
    compare_remaining_zero,
    control_convolution,
    convolution_matches_apply_word,
    energy_of_particular_holds,
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
        (2, -4, -4, 0, 0, -4, 1, 1, -4, 1, 1, -2),
    )
    for word in samples:
        assert convolution_matches_apply_word(word)
        assert z_from_word(word) == control_convolution(word)
        assert energy_of_particular_holds(16, word)


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
    assert top["state"] == (-27, -6, 0)
    assert top["convolution_ok"]
    assert top["word"] == (2, -4, -4, 0, 0, -4, 1, 1, -4, 1, 1, -2)


def test_layer_prefix_is_the_particular():
    sys = nonpisot_order3()
    fwd = forward_layers(sys, 12, live_only=True)
    s_max = fwd["layers"][0]["s_max"]
    prefix = fwd["layers"][0]["prefix"]
    assert s_max is not None and prefix is not None
    assert control_convolution(prefix) == s_max
