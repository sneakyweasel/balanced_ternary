"""Strategies B/C/D, parallel depth, FST-by-bound, add/mul/FMA."""

from __future__ import annotations

from bt.normtheory.arithmetic import (
    add_coeff,
    add_matches_encode,
    compare_fma,
    mul_coeff,
    mul_matches_encode,
)
from bt.normtheory.coeffword import CoeffWord
from bt.normtheory.complexity import (
    enumerate_words,
    family_all_c,
    family_alternating,
    family_power,
    family_power_plus,
    measure,
    profile_families,
    random_word,
    worst_case,
)
from bt.normtheory.locality import (
    BoundedNormalizeTransducer,
    classify_alphabet,
    single_coeff_carry_bound,
)
from bt.normtheory.strategies import all_strategies, normalize_lsd_to_msd
from bt.representation import encode
from bt.transducers.zoo import zoo


def test_B_can_differ_in_rewrite_count():
    found = False
    for word in enumerate_words(4, 2):
        traces = all_strategies(word)
        assert traces["A"].result.coeffs == traces["B"].result.coeffs
        if traces["A"].rewrite_count != traces["B"].rewrite_count:
            found = True
            break
    assert found, "expected an A/B rewrite-count gap on width<=4, |c|<=2"


def test_parallel_and_sequential_depths():
    for word in enumerate_words(3, 2):
        rep = measure(word)
        assert rep.strategies_agree
        assert rep.rewrite_D == 0
    witness = measure(CoeffWord((-2, -2, 2)))
    assert witness.strategies_agree
    assert witness.parallel_depth == 3
    assert witness.sequential_depth == 2
    assert witness.parallel_depth > witness.sequential_depth


def test_complexity_families():
    rows = profile_families(5)
    assert rows
    assert any(r["family"].startswith("3^") for r in rows)
    w = family_all_c(5, 2)
    assert measure(w).value == w.value()
    assert family_power(4).value() == 81
    assert family_power_plus(3, 1).value() == 28
    assert family_alternating(3, 2).coeffs == (2, -2, 2)
    rnd = random_word(6, 4)
    assert rnd.width() <= 6
    worst, rep = worst_case([family_all_c(3, 2), family_alternating(3, 2)])
    assert rep.rewrite_A >= 0
    assert worst.width() >= 1


def test_enumeration_rejects_huge_box():
    try:
        enumerate_words(12, 5)
        raise AssertionError("expected ValueError")
    except ValueError:
        pass
    assert len(enumerate_words(2, 1)) == 3**2


def test_fst_classification_by_bound():
    trit = classify_alphabet(1)
    assert trit.finite_state is True
    bounded = classify_alphabet(5)
    assert bounded.finite_state is True
    assert single_coeff_carry_bound(5) == 2
    unbounded = classify_alphabet(None)
    assert unbounded.finite_state is False
    machine = BoundedNormalizeTransducer(4)
    for word in enumerate_words(3, 2):
        got = machine.apply(word)
        assert got == encode(word.value())
    names = [e.function for e in zoo()]
    assert "normalize on unbounded Z coeffs" in names
    assert "normalize LSD on fixed [-B,B]" in names


def test_add_mul_match_encode():
    words = enumerate_words(3, 2)
    for p in words:
        for q in words:
            assert add_matches_encode(p, q)
            assert mul_matches_encode(p, q)
            assert add_coeff(p, q).value() == p.value() + q.value()
            assert mul_coeff(p, q).value() == p.value() * q.value()


def test_fma_values_equal_costs_may_differ():
    savings = 0
    staged_wins = 0
    sample = enumerate_words(2, 2)
    for p in sample:
        for q in sample:
            for r in sample:
                cmp = compare_fma(p, q, r)
                assert cmp.values_equal
                assert cmp.fused.result.value() == p.value() * q.value() + r.value()
                if cmp.fused_cheaper:
                    savings += 1
                if cmp.staged_cheaper:
                    staged_wins += 1
    assert savings >= 0
    assert staged_wins >= 0


def test_canonical_mul_then_nf():
    p = normalize_lsd_to_msd(CoeffWord((2, 2))).result
    q = normalize_lsd_to_msd(CoeffWord((-2,))).result
    assert p.is_canonical() and q.is_canonical()
    assert mul_matches_encode(p, q)
