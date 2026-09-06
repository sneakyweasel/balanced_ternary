"""The collision route: its price, its bad-word count, and the statistic its falsifier needs.

The route is Cauchy--Schwarz between a one-sided collision bound and Lemma 8.2's bad-word
count, so the two things worth testing are that the price is what the arithmetic says and
that the measurement cannot mistake a finite sample for a deviation.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


def fp_root() -> Path:
    return Path(__file__).resolve().parents[3]


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


def test_the_graded_family_returns_the_original_depth_constant_at_gamma_one() -> None:
    """The first export was the weakest member. gamma = 1 is the fair-coin value of the
    restricted count and costs no depth at all; gamma = 0 costs twelve letters."""

    from research.juggler_sequence.collision_large_sieve import graded_least_C

    assert [graded_least_C(g) for g in (0.0, 0.25, 0.5, 0.75, 1.0)] == [32, 27, 24, 22, 20]
    assert [graded_least_C(g, REQUIRED_RATE_STAR3) for g in (0.0, 0.5, 1.0)] == [28, 21, 18]


def test_H_of_C_A_is_false_as_literally_quantified() -> None:
    """Stated over *every* O-rooted word of length d(y) it fails, and not marginally: the
    all-O tails of terminating starts pile a constant proportion onto one cylinder. The
    manuscripts' prose already restricts to bad words; the quantifier does not."""

    from research.juggler_sequence.collision_large_sieve import max_cylinder_overpopulation

    row = max_cylinder_overpopulation(12, C=20, samples=20_000)
    assert row["d"] == 11
    assert row["overpopulation"] > 20, row
    assert row["top_word_bad_depth"] == 2, "the witness is not L-bad, as the mechanism predicts"
    assert row["top_word"].endswith("OO")

    deeper = max_cylinder_overpopulation(12, C=32, samples=20_000)
    assert deeper["overpopulation"] > row["overpopulation"], "the defect grows with depth"


def test_H_of_C_A_now_reads_over_bad_words_in_every_place_that_states_it() -> None:
    """The repair is a quantifier move, so it is checkable by reading the sources."""

    for path in (
        "docs/theory/juggler_fate_almost_all_note.md",
        "juggler_review/juggler_fate_almost_all_note.md",
        "docs/theory/juggler_tao_reduction_note.md",
    ):
        text = (fp_root() / path).read_text(encoding="utf-8")
        assert "-*bad* word" in text, path
        assert "every word\n\\(w\\in\\{O,E\\}^d\\) beginning with \\(O\\)" not in text, path

    ledger = json.loads((fp_root() / "docs/theory/theorem_ledger.json").read_text(encoding="utf-8"))
    row = next(r for r in ledger if r["id"] == "J-tao-loglog-depth-bound")
    assert "every L(y)-bad O-rooted word" in row["statement"]
    record = json.loads(
        (fp_root() / "conjectures/active/juggler_loglog_depth_cylinder_bound.json")
        .read_text(encoding="utf-8")
    )
    assert "every L(y)-bad word" in record["statement"]
    assert "REFUTED IN THE UNRESTRICTED FORM" in record["counterexamples"]


def test_H_q_needed_the_repair_and_the_witness_still_stands() -> None:
    """The witness that forced the stopped martingale: a cylinder whose members have all
    reached 1, so its odd-continuation share is exactly one."""

    from research.juggler_sequence.collision_large_sieve import worst_odd_continuation_share

    worst = worst_odd_continuation_share(12, C=20, samples=20_000)
    assert worst["violates_H_q"], worst
    assert worst["share"] > 0.99, worst
    assert worst["bad_depth"] == 2, "the witness has already descended"
    assert worst["mass"] > 0.01, "and it is not a rare cylinder"


def test_H_q_now_reads_over_bad_prefixes_and_the_proof_is_stopped() -> None:
    """Both halves of the repair are checkable by reading: the quantifier, and the stopping
    time that lets the hypothesis be used only where it is asserted."""

    for path in (
        "docs/theory/juggler_fate_almost_all_note.md",
        "juggler_review/juggler_fate_almost_all_note.md",
        "docs/theory/juggler_tao_reduction_note.md",
    ):
        text = (fp_root() / path).read_text(encoding="utf-8")
        assert "-*bad* \\(w\\in\\{O,E\\}^t\\)" in text, path
        assert "\\sigma=\\min\\{t\\ge 1:\\ u_t\\le-L\\}" in text or \
               "\\sigma=\\min\\{t\\ge1:u_t\\le-L\\}" in text, path
        assert "\\tilde\\eta_t=\\eta_t\\mathbf 1[\\sigma>t]" in text, path
        assert "\\tilde M" in text, path


def test_stopping_leaves_the_biased_split_exponent_where_it_was() -> None:
    """The claim the repair rests on: e_q(C) is untouched, so the printed least-C table is
    still the one the code computes."""

    from research.juggler_sequence.tao_reduction import least_C_biased

    assert [least_C_biased(q) for q in (0.5, 0.55, 0.60, 0.62)] == [20, 44, 240, 1715]
    assert [least_C_biased(q, REQUIRED_RATE_STAR3) for q in (0.5, 0.55, 0.60, 0.62)] == [
        18, 39, 206, 1451
    ]
    note = (fp_root() / "docs/theory/juggler_tao_reduction_note.md").read_text(encoding="utf-8")
    assert "Stopping costs nothing" in note
    for C in ("20", "44", "240", "1715"):
        assert f"| \\({C}\\) |" in note, C


def test_tau_is_at_most_sigma_and_never_exceeds_it() -> None:
    """Lemma 8.1 read at t = sigma: u_sigma <= -L forces J^sigma(n) <= N0, so tau <= sigma.
    The converse fails -- the power envelope is an upper bound and the orbit sits under it."""

    import random as _random

    from research.juggler_sequence.tao_reduction import LOG2_3, N0_CERTIFIED, scale_L

    L = scale_L(20 * math.log(10.0), N0_CERTIFIED)
    rng = _random.Random(7)
    strict = 0
    for _ in range(1500):
        n = rng.randrange(10**20 + 1, 2 * 10**20 + 1) | 1
        x, o, tau, sigma = n, 0, None, None
        for t in range(1, 60):
            o += x & 1
            x = math.isqrt(x * x * x) if x & 1 else math.isqrt(x)
            if tau is None and x <= N0_CERTIFIED:
                tau = t
            if sigma is None and o * LOG2_3 - t <= -L:
                sigma = t
            if tau is not None and sigma is not None:
                break
        if tau is not None and sigma is not None:
            assert tau <= sigma, (n, tau, sigma)
            strict += tau < sigma
    assert strict > 0, "tau = sigma everywhere would make the two notions interchangeable"


def test_the_containment_costs_almost_nothing_at_the_operative_depth() -> None:
    """Theorem 8.3 and the collision route both replace the live count by the bad-word count
    in their first step. That substitution is where tau != sigma could have cost something."""

    from research.juggler_sequence.collision_large_sieve import tau_vs_sigma

    for e10, C in ((12, 20), (20, 32)):
        row = tau_vs_sigma(e10, C=C, samples=4_000)
        assert row["containment_cost"] is not None
        assert 1.0 <= row["containment_cost"] < 1.10, row


def test_the_tower_threshold_has_two_readings_and_they_differ_slightly() -> None:
    """0.836 is right for "can the tower alone break P_theta" and slightly generous for
    "does it contribute a bounded total to the no-momentum sum", where the denominator is
    the live tilted mass and shrinks."""

    from research.juggler_sequence.collision_large_sieve import tower_threshold

    for C, printed in ((19, 0.8365), (20, 0.8342)):
        row = tower_threshold(C)
        assert abs(row["threshold_against_P_theta"] - printed) < 5e-5, row
        assert row["threshold_for_the_no_momentum_sum"] < row["threshold_against_P_theta"]
        # the correction is real but small: under half a percent
        assert 0.995 < row["live_decay_rate_rho"] < 1.0, row
        assert abs(row["threshold_for_the_no_momentum_sum"] - printed) < 0.003, row
        # and it does not disturb the ordering the section actually argues
        assert 0.6309 < row["threshold_for_the_no_momentum_sum"] < 0.981


def test_the_correction_is_small_because_the_tilt_already_selects_survivors() -> None:
    """The tilt sits at odd share p_C ~ 0.599 and the barrier asks for 1/log2(3) = 0.631,
    so the live mass decays only slowly relative to the unrestricted one."""

    from research.juggler_sequence.collision_large_sieve import tower_threshold

    row = tower_threshold(20)
    assert row["tilt_odd_share_p_C"] < row["barrier_needs_odd_share"]
    assert row["barrier_needs_odd_share"] - row["tilt_odd_share_p_C"] < 0.04


def test_the_manuscript_now_carries_both_tower_readings() -> None:
    """9.3(b) printed one number for two questions; it now prints both, and the computed
    values still match what the passage claims."""

    from research.juggler_sequence.collision_large_sieve import tower_threshold

    row = tower_threshold(19)
    for path in (
        "docs/theory/juggler_fate_almost_all_note.md",
        "juggler_review/juggler_fate_almost_all_note.md",
    ):
        text = (fp_root() / path).read_text(encoding="utf-8")
        assert "can breach\n\\(\\mathrm P_\\theta\\) by itself" in text, path
        assert "no-momentum\nthreshold is \\(\\rho\\cdot0.836=0.835\\)" in text, path
        assert "every\nmember of \\([O^t]\\) is live at depth \\(t\\)" in text, path

    # the passage truncates rather than rounds: 0.83651 is printed 0.836
    assert abs(row["threshold_against_P_theta"] - 0.836) < 1e-3
    assert round(row["threshold_for_the_no_momentum_sum"], 3) == 0.835
    assert round(row["live_decay_rate_rho"], 4) == 0.9977
    assert round(row["overpopulation_factor_printed"], 2) == 1.67
    assert round(row["overpopulation_factor_live"], 2) == 1.67
