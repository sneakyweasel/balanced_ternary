"""Fixed-integer affine-center identities, G recurrence, and n_* search."""

from __future__ import annotations

from fractions import Fraction

from research.collatz.affine_gap import affine_gap, next_affine_gap, addend_sign_law
from research.collatz.asymptotic import (
    N_STAR_LE_N_SMALLEST_COUNTEREXAMPLE,
    compatibility_ledger,
    positivity_inequalities,
    run_fixed_integer_census,
    scan_n_star_le_n,
    special_case_report,
    stronger_gap_statements,
    walk_integer_ledger,
)
from research.collatz.affine_center import AffineCenterState
from research.collatz.core import collatz_step, collatz_valuation
from research.collatz.fixed_integer import (
    InfiniteTrajectoryAffineState,
    iterate_states,
    next_C,
    next_normalized_C,
    next_state,
    normalized_C,
    normalized_C_finite_bounds,
    normalized_C_series,
    required_start_residue,
)
from research.collatz.itinerary import affine_constant, partial_sums_K
from research.collatz.periodic_code import PeriodicFixedPointTheorem


def test_empty_prefix_of_27():
    state = InfiniteTrajectoryAffineState.prefix(27, 0)
    assert state.m == 0
    assert state.x == 27
    assert state.C == 0
    assert state.G == 0
    assert state.A == 0
    assert state.B == 27
    assert state.affine_center is None


def test_forms_and_series_along_27():
    states = iterate_states(27, 20)
    assert states[0].n == 27
    x = 27
    for i, state in enumerate(states):
        assert state.validates()
        assert state.x == x
        assert state.A == normalized_C_series(partial_sums_K(state.valuations))
        assert state.A == normalized_C(state.C, state.m)
        assert state.B == state.n + state.A
        assert state.G == state.two_power * (state.n - state.x)
        assert affine_constant(state.valuations) == state.C
        if i + 1 < len(states):
            x = collatz_step(x)
            assert next_state(state).x == x


def test_g_recurrence_matches_definition():
    n = 41
    x = n
    C = 0
    two = 1
    three = 1
    G = 0
    for _ in range(12):
        k = collatz_valuation(x)
        predicted = next_affine_gap(G, n, two, k)
        C = 3 * C + two
        two <<= k
        three *= 3
        x = collatz_step(x)
        G = affine_gap(n, two, three, C)
        assert G == predicted
        assert G == two * (n - x)


def test_n_star_le_n_equivalent_to_orbit_test_on_27():
    for state in iterate_states(27, 25)[1:]:
        if state.regime == "contracting":
            assert (state.affine_center <= state.n) == (state.x <= state.n)
            assert (state.G >= 0) == (state.x <= state.n)
        else:
            assert state.affine_center < 0
            assert state.x > state.n
            assert state.G < 0
            assert state.affine_center <= state.n


def test_positivity_is_not_g_nonnegative():
    state = InfiniteTrajectoryAffineState.prefix(7, 1)
    assert state.x == 11
    assert state.x > 1
    assert state.G < 0
    report = positivity_inequalities(state)
    assert report["x_ge_1"]["holds"]
    assert report["G_eq_two_power_times_n_minus_x"]["holds"]


def test_required_residue_is_the_cylinder():
    state = InfiniteTrajectoryAffineState.prefix(27, 4)
    residue = required_start_residue(state.valuations)
    assert 27 % state.start_modulus == residue % state.start_modulus
    assert state.start_residue == residue


def test_n_equals_1_cycle():
    states = iterate_states(1, 3)
    assert states[1].valuations == (2,)
    assert states[1].x == 1
    assert states[1].G == 0
    assert states[1].affine_center == 1
    theorem = PeriodicFixedPointTheorem.from_valuations((2,))
    assert theorem.positive_candidate == 1
    assert not theorem.expanding_excludes_positive


def test_all_ones_period_is_expanding():
    theorem = PeriodicFixedPointTheorem.from_valuations((1, 1, 1))
    assert theorem.expanding_excludes_positive
    assert theorem.positive_candidate is None


def test_addend_sign_law_and_stronger_statements():
    assert addend_sign_law(7, 1) < 0
    assert addend_sign_law(7, 2) > 0
    assert addend_sign_law(1, 2) == 0
    state = InfiniteTrajectoryAffineState.prefix(7, 3)
    report = stronger_gap_statements(state)
    assert report["G_divisible_by_two_power"]["holds"]
    assert report["G_divisible_by_two_power"]["value"] == state.n - state.x
    bounds = normalized_C_finite_bounds(partial_sums_K(state.valuations))
    assert bounds["lower_K_j_ge_0"] <= bounds["A"] <= bounds["upper_K_j_le_K_last"]
    A = Fraction(0)
    C = 0
    two = 1
    for i, k in enumerate(state.valuations):
        A = next_normalized_C(A, two, i)
        C = next_C(C, two)
        two <<= k
    assert A == state.A
    assert C == state.C


def test_periodic_ones_and_twos():
    ones = PeriodicFixedPointTheorem.from_valuations((1, 1))
    assert ones.expanding_excludes_positive
    twos = PeriodicFixedPointTheorem.from_valuations((2,))
    assert twos.positive_candidate == 1
    assert twos.gap == 1


def test_even_two_is_out_of_domain():
    import pytest
    from research.collatz.core import require_positive_odd

    with pytest.raises(ValueError):
        require_positive_odd(2)


def test_ledger_agrees_with_full_state():
    rows = walk_integer_ledger(7, 10)
    states = compatibility_ledger(7, 10)
    assert len(rows) == len(states)
    for row, state in zip(rows[1:], states[1:]):
        assert row["G"] == state.G
        assert row["C"] == state.C
        assert row["x"] == state.x


def test_n_star_le_n_smallest_counterexample():
    witness = N_STAR_LE_N_SMALLEST_COUNTEREXAMPLE
    state = InfiniteTrajectoryAffineState.prefix(witness["n"], witness["m"])
    assert state.x == witness["x"]
    assert state.regime == "contracting"
    assert state.G < 0
    assert state.n_star_le_n() is False
    assert state.affine_center > state.n
    center = AffineCenterState.from_valuations(witness["valuations"])
    assert center.R == witness["n"]
    assert center.n_star > center.R
    failures, _, _, counts = scan_n_star_le_n(165, 40)
    assert counts["n_star_le_n_failures"] >= 1
    assert failures[0]["n"] == 165
    assert failures[0]["m"] == 17


def test_n_star_scan_small_and_census(tmp_path):
    failures, min_G, min_contracting_G, counts = scan_n_star_le_n(200, 40)
    assert counts["odd_count"] == 100
    assert min_G is not None
    assert min_contracting_G is not None
    result = run_fixed_integer_census(50, 20, output_dir=tmp_path)
    assert result.schema_version == "collatz-fixed-integer/v1"
    special = special_case_report(20)
    assert special["n=2"]["status"].startswith("even")
    assert special["n=1"]["final_x"] == 1
    assert special["n_star_le_n_smallest_counterexample"]["n"] == 165
    assert isinstance(failures, list)
    assert result.paths["jsonl"]
