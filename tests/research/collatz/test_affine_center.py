"""Tests for exact affine-center geometry."""

from __future__ import annotations

from fractions import Fraction
from itertools import product

import pytest

from research.collatz.affine_center import AffineCenterState, AffineRegime


def test_expanding_singleton_has_exact_negative_center():
    state = AffineCenterState.from_valuations((1,))
    assert (state.m, state.K, state.C, state.R, state.X, state.M) == (
        1,
        1,
        1,
        3,
        5,
        2,
    )
    assert state.gap == -1
    assert state.n_star == -1
    assert state.R_minus_n_star == 4
    assert state.X_minus_n_star == 6
    assert state.homogeneous_factor == Fraction(3, 2)
    assert state.regime is AffineRegime.EXPANDING
    assert all(state.exact_inequalities().values())


def test_contracting_fixed_point_word_two():
    state = AffineCenterState.from_valuations((2,))
    assert state.gap == 1
    assert state.n_star == 1
    assert state.R == state.X == state.M == 1
    assert state.R_minus_n_star == state.X_minus_n_star == 0
    assert state.regime is AffineRegime.CONTRACTING
    assert all(state.exact_inequalities().values())


def test_raw_and_reduced_centered_numerators():
    state = AffineCenterState.from_valuations((1, 4, 2))
    assert state.R_difference_raw == (
        state.gap * state.R - state.C,
        state.gap,
    )
    assert state.X_difference_raw == (
        state.gap * state.X - state.C,
        state.gap,
    )
    assert state.R_difference_raw[0] == state.two_power * (state.R - state.X)
    assert state.X_difference_raw[0] == state.three_power * (state.R - state.X)
    assert Fraction(*state.R_difference_reduced) == state.R_minus_n_star
    assert Fraction(*state.X_difference_reduced) == state.X_minus_n_star
    assert state.X == state.M + state.endpoint_lift_quotient * state.three_power


def test_exact_regime_geometry_exhaustive_small():
    for length in range(1, 5):
        for valuations in product(range(1, 5), repeat=length):
            state = AffineCenterState.from_valuations(valuations)
            assert state.validates()
            assert all(state.exact_inequalities().values()), valuations
            assert state.gap != 0
            assert state.partition(0) == state.regime.value


def test_critical_near_partition_is_explicit_and_exact():
    state = AffineCenterState.from_valuations((1,))
    assert state.partition(0) == "expanding"
    assert state.partition(1) == "critical-near"
    with pytest.raises(ValueError):
        state.partition(-1)
    with pytest.raises(ValueError):
        AffineCenterState.from_valuations(())
