"""Phase-0 tests for the order-(m) Ostrowski residual adder."""

from __future__ import annotations

from research.ostrowski.adder_search import (
    phase0_report,
    polynomial_is_irreducible_cubic,
    verify_addition,
    verify_boxed_addition,
)
from research.ostrowski.digits import canonicality_census
from research.ostrowski.minimize import boxed_minimality
from research.ostrowski.problem import PROBLEM
from research.ostrowski.residual import (
    accepts_msd,
    difference_word,
    lsd_to_msd,
    next_state,
    order2_transition,
    residual_integer,
    run_msd,
    zero_state,
)
from research.ostrowski.system import (
    characteristic_poly_coeffs,
    fibonacci_system,
    ostrowski_order2,
    phase0_order3,
)


def test_problem_is_registered():
    from research.literature import get_reference
    from research.open_problems import get_problem

    assert get_problem("ostrowski_order_m_adder") is PROBLEM
    assert PROBLEM.status == "STRUCTURAL"
    assert PROBLEM.docs == ("docs/problems/ostrowski_order_m_adder.md",)
    assert get_reference("baranwal-2020-ostrowski-thesis")["year"] == 2020
    assert get_reference("baranwal-schaeffer-shallit-2021-ostrowski-automatic")["year"] == 2021
    assert get_reference("hieronymi-terry-2018-ostrowski-addition")["year"] == 2018
    assert get_reference("frougny-solomyak-1996-linear-numeration")["year"] == 1996
    assert get_reference("shallit-1994-numeration-regular")["year"] == 1994
    assert get_reference("hieronymi-et-al-2024-sturmian-decidability")["year"] == 2024


def test_fibonacci_place_values_are_zeckendorf():
    assert fibonacci_system().place_values(8) == (1, 2, 3, 5, 8, 13, 21, 34)


def test_phase0_gamma_is_genuine_cubic():
    system = phase0_order3()
    assert system.order == 3
    assert system.place_values(6) == (1, 2, 5, 13, 33, 84)
    coeffs = characteristic_poly_coeffs(system)
    assert coeffs == (1, -2, -1, -1)
    assert polynomial_is_irreducible_cubic(coeffs)


def test_theorem_2_2_order2_regression():
    pell = ostrowski_order2((), (2,))
    for r in (-1, 0, 1):
        for s in (-1, 0, 1):
            for t in (-1, 0, 1):
                w = r + s * 2 - t
                assert order2_transition(r, s, w, 2) == (s, t)
                assert next_state(pell, (r, s), w, 5) == (s, t)


def test_residual_integer_follows_the_recurrence():
    system = phase0_order3()
    diffs = (1, -2, 0, 2, -1)
    state = zero_state(3)
    n = len(diffs)
    for step, w in enumerate(diffs):
        i = n - step
        expected = residual_integer(system, state, i) - w * system.place_value(i - 1)
        state = next_state(system, state, w, i)
        assert residual_integer(system, state, i - 1) == expected
    assert run_msd(system, diffs) == state


def test_acceptance_is_zero_weighted_difference():
    system = phase0_order3()
    x = (1, 0, 2, 0)
    y = (0, 1, 0, 1)
    z = (1, 1, 2, 1)
    assert system.val(x) + system.val(y) == system.val(z)
    assert accepts_msd(system, lsd_to_msd(difference_word(x, y, z)))
    z_wrong = (0, 1, 2, 1)
    assert system.val(x) + system.val(y) != system.val(z_wrong)
    assert not accepts_msd(system, lsd_to_msd(difference_word(x, y, z_wrong)))


def test_classical_ostrowski_is_unique_on_fibonacci():
    fib = fibonacci_system()
    census = canonicality_census(fib, 7, order_m=False)
    assert census["unique_on_range"]
    assert census["modulus"] == 34


def test_proposed_order_m_rules_are_not_unique_on_fibonacci():
    fib = fibonacci_system()
    census = canonicality_census(fib, 7, order_m=True)
    assert census["complete_on_range"]
    assert census["collision_count"] > 0


def test_proposed_order_m_rules_are_complete_not_unique_on_phase0():
    system = phase0_order3()
    census = canonicality_census(system, 5, order_m=True)
    assert census["complete_on_range"]
    assert census["collision_count"] > 0
    # smallest collision: q_2 = 2 q_1 + q_0
    assert system.val((0, 0, 1)) == system.val((1, 2, 0)) == 5


def test_unrestricted_adder_matches_values_on_fibonacci():
    fib = fibonacci_system()
    report = verify_addition(fib, 6, order_m=False)
    assert report["ok"]
    assert report["agree"] > 0


def test_unrestricted_adder_matches_values_on_phase0():
    system = phase0_order3()
    report = verify_addition(system, 5, order_m=True)
    assert report["ok"]
    assert report["false_accept"] == 0
    assert report["false_reject"] == 0
    assert report["agree"] > 0


def test_tm_box_one_is_insufficient_box_two_suffices():
    system = phase0_order3()
    tight = verify_boxed_addition(system, 5, tm_bound=1, order_m=True)
    loose = verify_boxed_addition(system, 5, tm_bound=2, order_m=True)
    assert tight["false_reject"] > 0
    assert loose["ok"]
    assert loose["false_reject"] == 0


def test_boxed_graph_minimizes_below_raw_state_count():
    system = phase0_order3()
    report = boxed_minimality(system, tm_bound=2)
    assert report["raw_states"] == 85
    assert report["minimal_live"] < report["raw_states"]
    assert report["merged"]
    assert report["max_abs_coord"] <= 4


def test_phase0_report_shape():
    report = phase0_report(length=5, box_steps=6, coord_limit=8)
    assert report["order"] == 3
    assert report["irreducible_cubic"]
    assert report["canonicality"]["complete_on_range"]
    assert not report["canonicality"]["injective_on_range"]
    assert report["addition"]["ok"]
    assert report["boxed_tm_2"]["ok"]
    assert report["boxed_tm_1"]["false_reject"] > 0
    assert report["minimality_tm_2"]["merged"]
