"""Neighboring energies invert s. Homogeneous A^k is energy-neutral.

Origin-live |s_orth| grows in ker(u_n). That is not |L_0|=∞.
"""

from __future__ import annotations

from fractions import Fraction

from research.ostrowski.energy_kernel import (
    GROWTH_NOT_INFINITUDE,
    HOMOGENEOUS_IS_STEP_ZERO,
    KNOWN_PACKAGING,
    NORMALIZED_NOT_COORDINATE,
    ORIGIN,
    adjoint_det,
    adjoint_det_closed_form,
    adjoint_det_table,
    adjoint_u,
    complementary_step_holds,
    compare_kernel_horizons,
    energy_canonical,
    energy_homogeneous_holds,
    energy_parallel_and_perp,
    gcd_adjoint,
    inversion_recovers,
    kernel_targeted_blocks,
    neighboring_energies,
)
from research.ostrowski.system import nonpisot_order3


def test_adjoint_det_is_three_pow():
    report = adjoint_det_table(16)
    assert report["all_match_closed_form"]
    assert report["all_nonzero"]
    assert report["first_zero_n"] is None
    sys = nonpisot_order3()
    assert adjoint_det(sys, 2) == 1
    assert adjoint_det(sys, 3) == 3
    assert adjoint_det_closed_form(4) == 9
    assert report[KNOWN_PACKAGING]


def test_inversion_recovers_and_orth_in_kernel():
    sys = nonpisot_order3()
    samples = (
        (ORIGIN, 5),
        ((-3, -1, 0), 4),
        ((6, 5, 1), 6),
        ((2, -7, 3), 8),
        ((15, 2, -2), 4),
    )
    for state, remaining in samples:
        assert inversion_recovers(sys, state, remaining)
        split = energy_parallel_and_perp(sys, state, remaining)
        assert split["recovers"]
        u = adjoint_u(sys, remaining)
        orth_dot = sum(u[i] * split["s_orth"][i] for i in range(3))
        assert orth_dot == 0
        e, v, z = neighboring_energies(sys, state, remaining)
        assert e == energy_canonical(sys, state, remaining)
        assert split["E"] == e and split["V"] == v and split["Z"] == z
    assert all(gcd_adjoint(sys, n) == 1 for n in range(2, 17))


def test_homogeneous_is_energy_step_at_zero():
    sys = nonpisot_order3()
    assert energy_homogeneous_holds(sys, ORIGIN, 3, 2)
    assert energy_homogeneous_holds(sys, (-3, -1, 0), 4, 3)
    assert energy_homogeneous_holds(sys, (6, 5, 1), 2, 4)
    assert complementary_step_holds(sys, ORIGIN, 0, 5)
    assert complementary_step_holds(sys, (-3, -1, 0), -4, 4)
    assert complementary_step_holds(sys, (6, 5, 1), 2, 6)


def test_origin_live_kernel_grows_with_horizon():
    cmp = compare_kernel_horizons(12, 16, 4)
    assert cmp["small"]["L"] == 166
    assert cmp["large"]["L"] == 427
    assert cmp["small"]["max_linf"] == 15
    assert cmp["large"]["max_linf"] == 24
    assert cmp["perp_grows_with_horizon"]
    assert cmp["within_level_linf_grows_with_horizon"]
    assert cmp["V_grows_with_horizon"]
    assert cmp["global_orth_grows"]
    assert cmp["small"]["max_linf_orth"] == Fraction(28850, 1931)
    assert cmp["large"]["max_linf_orth"] == Fraction(46414, 1931)
    assert cmp[GROWTH_NOT_INFINITUDE]
    assert cmp[NORMALIZED_NOT_COORDINATE]
    # Geometric kernel size tracks |s|, not a complementary bound.
    assert cmp["large"]["max_linf_orth"] > 20


def test_kernel_targeted_blocks_are_not_a_family():
    report = kernel_targeted_blocks(12, 8, 4)
    assert report["source_found"]
    assert report["seed"] == (6, 2, -3)
    assert report["checked"] == 2800
    assert report["symbolic_family"] is False
    assert report[GROWTH_NOT_INFINITUDE]
    assert report[HOMOGENEOUS_IS_STEP_ZERO]
    # Local expanders at one horizon are not |L_0|=∞.
    assert report["expanding_live_count"] > 0
