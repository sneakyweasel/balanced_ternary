"""Rewrite system: balanced_divmod, value preservation, Strategy A ≡ encode."""

from __future__ import annotations

from bt.normalization import rewrite_sum
from bt.normtheory.coeffword import CoeffWord
from bt.normtheory.complexity import enumerate_words
from bt.normtheory.rewrite import (
    agrees_with_rewrite_sum_on_small,
    balanced_divmod,
    critical_pair_join,
    irreducible,
    joinable,
    legal_sites,
    lex_decreases,
    locally_confluent,
    normalize_step,
    successors,
    weighted_l1_increases_on_two,
)
from bt.normtheory.strategies import agrees_with_encode, all_strategies, normal_form
from bt.representation import encode, from_digits_lsd


def test_balanced_divmod_unique_trit():
    for c in range(-40, 41):
        r, q = balanced_divmod(c)
        assert r in (-1, 0, 1)
        assert c == 3 * q + r
        assert agrees_with_rewrite_sum_on_small()
    for s in range(-3, 4):
        assert balanced_divmod(s) == rewrite_sum(s)
    r, q = balanced_divmod(5)
    assert (r, q) != rewrite_sum(5)
    assert r in (-1, 0, 1)
    assert 5 == 3 * q + r


def test_rewrite_sum_contract_unchanged():
    assert rewrite_sum(5) == (2, 1)


def test_step_preserves_value_and_lex():
    for width, bound in ((4, 2), (3, 3)):
        for word in enumerate_words(width, bound):
            for i, nxt in successors(word):
                assert nxt.value() == word.value()
                assert lex_decreases(word, nxt)
                assert i in legal_sites(word)


def test_irreducible_iff_canonical():
    assert irreducible(CoeffWord((1, 0, -1)))
    assert not irreducible(CoeffWord((2,)))
    assert CoeffWord((1, 0, -1)).is_canonical()
    assert CoeffWord((2, 0)).coeffs == (2,)


def test_strategy_A_equals_encode():
    for n in range(-2000, 2001):
        word = CoeffWord.from_value(n)
        assert agrees_with_encode(word)
        nf = normal_form(word)
        assert from_digits_lsd(nf.coeffs) == encode(n)
    for word in enumerate_words(4, 2):
        assert agrees_with_encode(word)
    targeted = [
        CoeffWord((20,) * 8),
        CoeffWord((0, 0, 15, -7, 3)),
        family_like(),
    ]
    for word in targeted:
        assert agrees_with_encode(word)


def family_like() -> CoeffWord:
    return CoeffWord((0,) * 12 + (2,))


def test_strategies_agree_on_normal_form():
    for word in enumerate_words(3, 2):
        traces = all_strategies(word)
        results = {t.result.coeffs for t in traces.values()}
        assert len(results) == 1
        assert traces["D"].rewrite_count == 0


def test_weighted_l1_is_not_a_rank():
    assert weighted_l1_increases_on_two()


def test_critical_pairs_join_on_box():
    for a in range(-8, 9):
        for b in range(-8, 9):
            assert critical_pair_join(a, b)
    for word in enumerate_words(3, 2):
        assert locally_confluent(word)


def test_overlap_minus5_two_joins_after_strip():
    """Raw Lean lists [1,0] vs [1,0,0]; Python CoeffWord strips both to (1,)."""
    word = CoeffWord((-5, 2))
    via0 = normalize_step(word, 0)
    via1 = normalize_step(word, 1)
    assert via0.coeffs == (1,)
    assert via0.value() == via1.value() == word.value()
    assert joinable(via0, via1)
    assert locally_confluent(word)
