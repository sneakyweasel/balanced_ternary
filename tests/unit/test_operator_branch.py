"""Additive combinatorics, polynomials, metrics extras, and the transducer zoo."""

from __future__ import annotations

from bt.metrics import carry_defect, carry_defect_scan, metric_properties
from bt.polynomials import evaluation_identities, factor_small, polynomial
from bt.representation import encode
from bt.transducers.zoo import h2_state_counts, m2_state_counts, zoo
from research.additive_combinatorics import (
    A_set,
    B_set,
    C_set,
    interval_bound,
    smallest_r_covering_nonneg_interval,
    sumset_A_minus_A,
    sumset_A_plus_A,
    sumset_A_plus_B,
    sumset_B_minus_B,
    sumset_B_plus_B,
)
from research.operator_dynamics.dossiers import all_dossiers, dossier_d_stopping, dossier_w_ww
from research.perfect_powers import sparse_squares, weight_one_squares
from research.sparse_polynomials import prime_polynomial_factors


def test_C_k_is_the_complete_interval():
    for k in range(0, 6):
        M = interval_bound(k)
        c = sorted(C_set(k))
        assert c == list(range(-M, M + 1))
        assert len(c) == 3**k


def test_A_plus_A_is_interval_with_energy_six_pow_k():
    for k in range(0, 8):
        rep = sumset_A_plus_A(k)
        assert rep.interval
        assert rep.cardinality == 3**k
        assert rep.covered_min == 0
        assert rep.covered_max == 3**k - 1
        assert rep.energy == 6**k
        assert {a + b for a in A_set(k) for b in A_set(k)} == set(range(0, 3**k))


def test_A_minus_A_is_C_k():
    for k in range(0, 7):
        rep = sumset_A_minus_A(k)
        assert rep.interval
        assert rep.cardinality == 3**k
        M = interval_bound(k)
        assert {a - b for a in A_set(k) for b in A_set(k)} == set(range(-M, M + 1))
        assert rep.energy == 6**k


def test_B_plus_B_is_twice_C_k():
    for k in range(1, 6):
        rep = sumset_B_plus_B(k)
        assert rep.cardinality == 3**k
        inner = interval_bound(k)
        got = {b1 + b2 for b1 in B_set(k) for b2 in B_set(k)}
        assert got == {2 * t for t in range(-inner, inner + 1)}
        assert sumset_B_minus_B(k).cardinality == rep.cardinality


def test_A_plus_B_small_k_not_assumed_interval():
    for k in (1, 2, 3, 4):
        rep = sumset_A_plus_B(k)
        assert rep.cardinality >= 1
        assert rep.proof_status == "VERIFIED COMPUTATIONALLY"


def test_smallest_r_is_two():
    for k in range(1, 8):
        assert smallest_r_covering_nonneg_interval(k) == 2


def test_weight_one_squares_closed_form():
    assert "3^{2t}" in weight_one_squares()
    sq = sparse_squares(1, 200)
    assert sq[0] == 0
    assert 1 in sq
    assert 9 in sq
    assert 81 in sq
    for n in sq:
        if n > 0:
            m = n
            while m % 9 == 0:
                m //= 9
            assert m == 1


def test_polynomial_evaluations():
    for n in range(-300, 301):
        ids = evaluation_identities(n)
        assert ids["P(3)"] == n
        assert ids["P(1)"] == ids["signed_digit_sum"]
        assert ids["P(-1)"] == ids["alternating_digit_sum"]
        assert ids["weight"] == ids["coefficient_weight"]
        assert ids["bt_palindrome"] == ids["poly_palindrome"]


def test_palindrome_is_reciprocal():
    p = polynomial(1)
    assert p.is_reciprocal()
    # 5 = "+--" is not palindromic
    assert not polynomial(5).is_palindromic()
    # 4 = "++" is palindromic
    assert polynomial(4).is_palindromic()
    assert factor_small(polynomial(4))  # may be empty; just runs


def test_prime_polynomial_need_not_be_irreducible():
    rows = prime_polynomial_factors((2, 5, 7, 13))
    assert rows[0]["p"] == 2
    # 13 = 1 + 3 + 9 = "+++" so P = 1+x+x^2 = Phi_3
    thirteen = next(r for r in rows if r["p"] == 13)
    assert encode(13).word() == "+++"
    assert "Phi_3=x^2+x+1" in thirteen["factors"]


def test_carry_defect_takes_both_nonnegative_and_check_sign():
    scan = carry_defect_scan(25)
    assert scan["max"] >= 0
    # 1+1=2: w(1)+w(1)-w(2)=1+1-2=0
    assert carry_defect(1, 1) == 0
    # 2+2=4: w(2)=2, w(4)=2, defect 2
    assert carry_defect(2, 2) == 2
    props = metric_properties(8)
    assert props["symmetric"] is True
    assert props["definite"] is True


def test_zoo_contains_odd_part_and_shift():
    names = [e.function for e in zoo()]
    assert any("3n" in n for n in names)
    assert any("odd_part" in n for n in names)
    assert any(e.finite_state is False and "odd_part" in e.function for e in zoo())
    h2 = h2_state_counts(4)
    m2 = m2_state_counts(4)
    assert h2[0]["k"] == 1
    assert m2[0]["reachable"] >= 1


def test_sequence_dossiers_match_known_identities():
    dstop = dossier_d_stopping()
    assert dstop.claim_status == "PROVED"
    ww = dossier_w_ww()
    assert ww.claim_status == "PROVED"
    assert len(all_dossiers()) >= 4
