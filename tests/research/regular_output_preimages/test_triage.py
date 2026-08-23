"""Phase-0 tests for regular-output preimages of x^2."""

from __future__ import annotations

from bt.calculus.lifting import is_lift_node
from bt.calculus.residual import TRITS, delta, output_along, rho
from bt.calculus.section import parse_poly
from research.regular_output_preimages.problem import PROBLEM
from research.regular_output_preimages.triage import (
    DEAD,
    LIVE,
    MAX_DEPTH,
    X,
    X2,
    census_count,
    census_table,
    distinction_holds,
    distinguish_accept,
    distinguishing_word,
    family_x2_plus_two,
    first_k_digits_of_one_minus_3k,
    first_outputs_of_x2,
    is_safe_word,
    linear_live_count,
    pack_all_minus,
    prefix_one_then_zeros,
    reachable_live,
    signature_of,
    step_safety,
    triage_report,
    zero_output_is_proper_subset,
)


def test_problem_is_registered():
    from research.open_problems import get_problem

    assert get_problem("regular_output_preimages") is PROBLEM
    assert PROBLEM.status == "STRUCTURAL"
    assert PROBLEM.docs == ("docs/problems/regular_output_preimages.md",)


def test_safety_automaton_dies_exactly_on_minus():
    assert step_safety(LIVE, 0) == LIVE
    assert step_safety(LIVE, 1) == LIVE
    assert step_safety(LIVE, -1) == DEAD
    assert step_safety(DEAD, 0) == DEAD
    assert step_safety(DEAD, 1) == DEAD
    assert step_safety(DEAD, -1) == DEAD


def test_accept_signature_is_recursive():
    g = X2
    sig1 = signature_of(g, LIVE, 1)
    parts = []
    for a in TRITS:
        if rho(g, a) == -1:
            parts.append("D")
        else:
            parts.append(signature_of(delta(g, a), LIVE, 0))
    assert sig1 == tuple(parts)
    assert signature_of(g, DEAD, 3) == ("D",)
    assert signature_of(g, LIVE, 0) == ("L",)


def test_identity_has_one_live_type():
    record = linear_live_count(4)
    assert record["single_live_type"]
    assert reachable_live(X, 3) == [X]
    assert census_count(X, 2, 3) == 1


def test_x2_root_never_emits_minus():
    assert first_outputs_of_x2() == (1, 0, 1)
    for a in TRITS:
        assert rho(X2, a) != -1


def test_zero_output_language_is_a_proper_subset():
    record = zero_output_is_proper_subset(X2, max_len=3)
    assert record["proper_subset"]
    witness = tuple(record["safe_non_lift"])
    assert is_safe_word(output_along(X2, witness))
    assert not is_lift_node(X2, witness)
    assert witness == (1,) or witness == (-1,)


def test_census_is_deterministic_and_bounded():
    table = census_table(X2, 3)
    assert table == census_table(X2, 3)
    assert table[0][0] == 1
    for row in table:
        assert all(count >= 1 for count in row)


def test_plus_two_family_is_the_stated_residual():
    word = (1, 0, 0)
    assert family_x2_plus_two(1).coeffs == parse_poly("9x^2+2x").coeffs
    assert family_x2_plus_two(2).coeffs == parse_poly("27x^2+2x").coeffs
    assert family_x2_plus_two(0).coeffs == delta(X2, 1).coeffs
    along = X2
    for a in word:
        along = delta(along, a)
    assert along.coeffs == family_x2_plus_two(2).coeffs


def test_distinguish_accept_finds_an_asymmetric_word():
    left = family_x2_plus_two(0)
    right = parse_poly("3x^2")
    word = distinguish_accept(left, right, 3)
    assert word is not None
    assert is_safe_word(output_along(left, word)) != is_safe_word(output_along(right, word))


def test_minus_pack_and_low_digits_of_one_minus_power():
    from bt.calculus.quadratic import pack_word
    from bt.representation import encode

    for k in range(1, 7):
        word = (-1,) * k
        assert pack_all_minus(k) == pack_word(word)
        digits = encode(1 - 3**k).digits_lsd()
        padded = digits + (0,) * (k - len(digits))
        assert padded[:k] == first_k_digits_of_one_minus_3k(k)


def test_infinite_distinguishing_family_is_exact():
    from bt.calculus.residual import delta

    for m in range(6):
        residual = X2
        for a in prefix_one_then_zeros(m):
            residual = delta(residual, a)
        assert residual.coeffs == family_x2_plus_two(m).coeffs
        assert family_x2_plus_two(m).eval(-1) == 3 ** (m + 1) - 2
        for n in range(m + 1, 7):
            assert distinction_holds(m, n)
            word = distinguishing_word(m)
            assert word == (-1,) * (m + 1) + (0,)


def test_triage_report_shape():
    report = triage_report(3)
    assert report["polynomial"] == "x^2"
    assert report["root_never_minus"]
    assert report["zero_output"]["proper_subset"]
    assert report["linear"]["single_live_type"]
    assert len(report["x2_census"]) == 4
    assert report["ahmed_savchuk_unrestricted_infinite"]
    assert MAX_DEPTH == 7
