"""Multi-step itinerary-parity census. Not a halt test, not a frequency theorem."""

from __future__ import annotations

from math import isqrt

from research.juggler_sequence.power_words import floor_power
from research.juggler_sequence.two_step_parity import (
    ANTI_OVERCLAIM,
    CONTRACTING_TARGET,
    SCALE,
    WORDS4,
    gap_decomposition_check,
    identity_error_scaled,
    identity_scan,
    itinerary_word,
    juggler_step,
    scan,
    word_counts,
)

# Exact depth-4 counts over odd n in [3, 10^5], pinned from the census.
PINNED_COUNTS_1E5 = {
    "OEEE": 6453,
    "OEEO": 6053,
    "OEOE": 6086,
    "OEOO": 6423,
    "OOEE": 6176,
    "OOEO": 6291,
    "OOOE": 6332,
    "OOOO": 6185,
}


def test_juggler_step_matches_floor_power():
    for n in (2, 3, 7, 9, 16, 365, 3889, 10_000):
        assert juggler_step(n) == floor_power(n)


def test_itinerary_words_small():
    # 3 -> 5 -> 11 -> 36: OOOE. 9 -> 27 -> 140 -> 11: OOEO.
    assert itinerary_word(3, 4) == "OOOE"
    assert itinerary_word(9, 4) == "OOEO"
    # 15 -> 58 -> 7 -> 18: OEOE.
    assert itinerary_word(15, 4) == "OEOE"
    assert all(itinerary_word(n, 4)[0] == "O" for n in range(3, 51, 2))


def test_words4_enumeration():
    assert len(WORDS4) == 8
    assert all(w[0] == "O" and len(w) == 4 for w in WORDS4)
    assert CONTRACTING_TARGET in WORDS4


def test_pinned_counts_at_1e5():
    assert word_counts(100_000) == PINNED_COUNTS_1E5
    assert sum(PINNED_COUNTS_1E5.values()) == 49_999


def test_scan_small_window_flat_and_descending():
    row = scan(100_000)
    assert row["final"]["counts4"] == PINNED_COUNTS_1E5
    # No linear bias: every depth-4 class within 5% of the product density.
    odds = row["final"]["odds"]
    for w in WORDS4:
        assert abs(row["final"]["counts4"][w] - odds / 8) < 0.05 * odds / 8
    # Every census OOEE start satisfied the four-step descent T^4(n) < n.
    assert row["ooee"]["descent_violations"] == 0
    # Envelope exponents on this window stay well below 1.
    for d in ("2", "3", "4"):
        assert row["fitted_exponent"][d] is not None
        assert row["fitted_exponent"][d] < 0.9


def test_ooee_is_contracting_word():
    # 3^oddCount < 2^length for OOEE: the formal power bound contracts.
    assert 3**2 < 2**4
    # Exact spot check of a realized OOEE start.
    for n in range(3, 20_001, 2):
        if itinerary_word(n, 4) == "OOEE":
            x = n
            for _ in range(4):
                x = juggler_step(x)
            assert x < n
            # Exact certificate shape: x^16 <= n^9 forces x < n for n >= 2.
            assert x**16 <= n**9


def test_anti_overclaim_flags():
    assert ANTI_OVERCLAIM["parity_frequency_theorem"] is False
    assert ANTI_OVERCLAIM["depth2_analytic_lemma_proved"] is False
    assert ANTI_OVERCLAIM["global_termination"] is False


def test_isqrt_agreement_on_odd_branch():
    for n in range(3, 501, 2):
        assert juggler_step(n) == isqrt(n * n * n)


def test_lemma_a_identity_bounds():
    # Lemma A: m^{3/2} = (3/2) m n^{3/4} - (1/2) n^{9/4} + E(n),
    # 0 <= E(n) <= (1/2) n^{-3/4}, exact scaled-integer check.
    samples = tuple(range(3, 1001, 2)) + (10**6 + 1, 10**9 + 1)
    result = identity_scan(samples)
    assert result["holds"] is True
    # The supremum of E / bound is 3/4, attained as theta -> 1.
    assert result["worst_ratio"] < 0.7501


def test_lemma_a_single_value_shape():
    err, bound = identity_error_scaled(101)
    assert 0 <= err <= bound
    # bound*scale = scale^2 // (2 n^{3/4} scale) is positive and small.
    assert 0 < bound < SCALE


def test_lemma_b_gap_decomposition():
    # g(n) = floor(delta) + [ {n^{3/2}} >= 1 - {delta} ] exactly.
    for h in (1, 2):
        result = gap_decomposition_check(100_001, 400, h)
        assert result["holds"] is True
        assert result["matches"] >= 398
