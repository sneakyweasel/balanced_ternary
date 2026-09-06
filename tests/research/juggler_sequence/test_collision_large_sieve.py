"""The collision route: its price, its bad-word count, and the statistic its falsifier needs.

The route is Cauchy--Schwarz between a one-sided collision bound and Lemma 8.2's bad-word
count, so the two things worth testing are that the price is what the arithmetic says and
that the measurement cannot mistake a finite sample for a deviation.
"""

from __future__ import annotations

import math

from research.juggler_sequence.collision_large_sieve import (
    bad_depth,
    bad_word_count,
    collision_census,
    half_exponent_least_C,
    juggler_word,
    verdict,
)
from research.juggler_sequence.tao_reduction import (
    LOG2_3,
    REQUIRED_RATE,
    REQUIRED_RATE_STAR3,
    chernoff_exponent,
)


def test_cauchy_schwarz_costs_exactly_twelve_letters_of_depth() -> None:
    """Half the exponent moves the least depth constant from 20 to 32, and 18 to 28."""

    assert half_exponent_least_C(REQUIRED_RATE) == 32
    assert half_exponent_least_C(REQUIRED_RATE_STAR3) == 28
    assert chernoff_exponent(32) / 2 > REQUIRED_RATE
    assert chernoff_exponent(31) / 2 <= REQUIRED_RATE
    assert chernoff_exponent(28) / 2 > REQUIRED_RATE_STAR3
    assert chernoff_exponent(27) / 2 <= REQUIRED_RATE_STAR3


def test_the_bad_word_count_is_the_walk_dynamic_program() -> None:
    """Counted directly against the definition: the walk never reaches ``-L``."""

    for L in (0.4, 0.9, 2.5):
        for d in range(1, 13):
            direct = 0
            for mask in range(1 << (d - 1)):
                word = (1,) + tuple((mask >> i) & 1 for i in range(d - 1))
                o = 0
                bad = True
                for t, letter in enumerate(word, start=1):
                    o += letter
                    if o * LOG2_3 - t <= -L:
                        bad = False
                        break
                direct += bad
            assert bad_word_count(L, d) == direct, (L, d)


def test_badness_is_prefix_closed_so_one_pass_gives_every_depth() -> None:
    word = juggler_word(10**12 + 1, 20)
    cut = bad_depth(word, 0.5258)
    for d in range(1, cut + 1):
        assert bad_word_count(0.5258, d) > 0
    o = 0
    for t, letter in enumerate(word, start=1):
        o += letter
        reached = o * LOG2_3 - t <= -0.5258
        assert reached == (t > cut), (t, cut)
        if reached:
            break


def test_a_descending_start_is_not_bad_which_is_what_excludes_the_all_O_tails() -> None:
    """Reaching the floor means the walk reached ``-L``; the ``O``-tail afterwards cannot
    undo that.  This is the whole reason the collision count is taken over bad words --
    over all words it is dominated by terminating starts sharing a tail."""

    L = 0.5258
    descended = [n for n in range(10**12 + 1, 10**12 + 400, 2)
                 if bad_depth(juggler_word(n, 18), L) < 18]
    assert descended, "no start descended in the sample range"
    for n in descended[:20]:
        word = juggler_word(n, 18)
        cut = bad_depth(word, L)
        assert cut < 18
        assert sum(word[cut:]) >= 0  # the tail exists and does not restore badness


def test_the_null_absorbs_the_finite_sample_term_and_the_raw_excess_does_not() -> None:
    """At ``d = 18`` every bad word is occupied at most once, so the raw excess reads 2
    while the ratio against the matched null stays at 1.  A falsifier stated on the raw
    excess would fire on sample size alone."""

    census = collision_census(12, samples=20_000, d_max=18)
    deep = [r for r in census["rows"] if r["d"] == 18][0]
    assert deep["K_measured"] / deep["K_fair_coin"] > 1.5
    assert 0.9 < deep["ratio_to_null"] < 1.1


def test_the_operative_depth_at_1e12_is_inside_the_measured_range() -> None:
    census = collision_census(12, samples=5_000, d_max=18)
    assert census["operative_depth_C32"] == math.ceil(32 * census["L"]) == 17
    assert any(r["is_operative_depth"] for r in census["rows"])


def test_phase0_does_not_fire_the_falsifier() -> None:
    censuses = [collision_census(e, samples=20_000, d_max=16) for e in (12, 30)]
    out = verdict(censuses)
    assert not out["falsifier_fired"]
    assert out["worst_ratio_to_finite_sample_null"] < 1.25
    assert out["worst_depth_to_depth_growth_of_that_ratio"] < 1.10
