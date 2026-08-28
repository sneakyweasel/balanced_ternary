"""Multi-step itinerary-parity census. Not a halt test, not a frequency theorem."""

from __future__ import annotations

from math import isqrt

from research.juggler_sequence.power_words import floor_power
from research.juggler_sequence.two_step_parity import (
    ANTI_OVERCLAIM,
    CONTRACTING_TARGET,
    SCALE,
    WORDS4,
    branch_freeze_scan,
    deep_word_counts,
    differenced_kernel_probe,
    double_gap_identity_check,
    fourth_letter_scan,
    fourth_letter_smoothing_check,
    gap_decomposition_check,
    kernel_reformulation_scan,
    identity_error_scaled,
    identity_scan,
    itinerary_word,
    juggler_step,
    kernel_probe,
    level3_inner_linearization_scan,
    level3_kernel_probe,
    level3_raw_gap_wildness,
    level3_reformulation_scan,
    differenced_level3_kernel_probe,
    oooo_indicator_identity_check,
    ooeooee_indicator_identity_check,
    oooeoee_indicator_identity_check,
    sixth_ooeoo_scan,
    sixth_oooeo_scan,
    v_level_cell_scan,
    w_gap_freeze_scan,
    lemma_a_prime_scan,
    lemma_m_scan,
    level2_gap_check,
    m12_scan,
    oeo_indicator_identity_check,
    oeo_mode_probe,
    oeo_smoothing_scan,
    oe_indicator_identity_check,
    ooee_indicator_identity_check,
    ooo_indicator_identity_check,
    oooee_indicator_identity_check,
    oooee_mode_probe,
    oooee_smoothing_scan,
    ooeoe_indicator_identity_check,
    ooeoe_mode_probe,
    ooeoe_smoothing_scan,
    scan,
    second_gap_collision_check,
    second_order_scan,
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
    assert ANTI_OVERCLAIM["global_termination"] is False
    assert ANTI_OVERCLAIM["predictive_state_claim"] is False
    # Flipped by the Phase-2 review pass (J-nested-parity-discrepancy).
    assert ANTI_OVERCLAIM["depth2_analytic_lemma_proved"] is True
    # Flipped by the Phase-3 review pass (J-triple-parity-discrepancy).
    assert ANTI_OVERCLAIM["depth4_even_branch_proved"] is True
    # Flipped by the Phase-9 review pass (J-kernel-cancellation,
    # J-depth4-complete): the tier-2 kernel bound and the depth-4
    # completion are theorems. Density one stays unclaimed (depth >= 5
    # equidistribution is open).
    assert ANTI_OVERCLAIM["tier2_analytic_lemma_proved"] is True
    assert ANTI_OVERCLAIM["kernel_bound_proved"] is True
    assert ANTI_OVERCLAIM["depth4_complete_proved"] is True
    assert ANTI_OVERCLAIM["density_one_claimed"] is False


def test_smooth_cancellation_constant():
    # |A1''| n^{7/4} / h^2 -> 81/256 = 0.31640625 (j = 1).
    from research.juggler_sequence.two_step_parity import (
        smooth_cancellation_check,
    )

    for n, h in ((10_001, 1), (100_001, 3), (1_000_001, 10)):
        ratio = smooth_cancellation_check(n, h)
        assert abs(ratio - 81 / 256) < 0.01


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


def test_lemma_d_fourth_letter_smoothing():
    # Lemma D: v^{1/2} = n^{9/8} + D(n), -(3/4) n^{-3/8} - n^{-9/8} <= D <= 0.
    samples = tuple(range(3, 1001, 2)) + (10**6 + 1, 10**9 + 1)
    result = fourth_letter_scan(samples)
    assert result["holds"] is True
    # The supremum of |D| / bound is 1, approached as theta -> 1.
    assert result["worst_ratio"] < 1.0


def test_lemma_d_single_value_shape():
    diff, bound = fourth_letter_smoothing_check(101)
    assert -bound <= diff <= 0
    assert 0 < bound < SCALE


def test_ooee_indicator_identity():
    # itinerary_word(n,4) == "OOEE" iff (psi1, psi2, psi3) = (-1,+1,+1):
    # the branch-consistency claim behind Corollary F.
    result = ooee_indicator_identity_check(5001)
    assert result["holds"] is True


def test_lemma_g_coefficient_identities():
    # Both Lemma G identities and the Proposition H polynomial recover
    # the nominal value at (m, v) = (X, X^{3/2}).
    from fractions import Fraction as F

    assert F(5, 32) + F(15, 16) - F(3, 32) == 1
    assert F(5, 32) - F(9, 16) + F(45, 32) == 1
    assert (
        -F(5, 64) + F(9, 32) - F(45, 64) + F(15, 64) + F(45, 32) - F(9, 64)
    ) == 1


def test_lemma_g_second_order_scan():
    # Second-order linearization bricks, exact at scale 10^60.
    samples = tuple(range(5, 501, 2)) + (10**6 + 1, 10**9 + 1)
    result = second_order_scan(samples)
    assert result["holds"] is True


def test_ooo_indicator_identity():
    # itinerary_word(n,4) == "OOOE" iff (psi1, psi2, psi4) = (-1,-1,+1):
    # the branch-consistency claim for the tier-2 target class.
    result = ooo_indicator_identity_check(5001)
    assert result["holds"] is True


def test_composed_cell_obstruction():
    # Negative knowledge: on Lemma-B cells the second-level gap g2
    # takes a new value at essentially every point, so the naive
    # two-level cell composition fails. Do not retry that route.
    result = second_gap_collision_check(10**6 + 1, 1500, 1)
    assert result["distinct_ratio"] >= 0.99


def test_proposition_l_m12_smoothing():
    # OE-branch third-letter brick: m^{1/2} = n^{3/4} + D1 with
    # -(1/2)n^{-3/4} - n^{-9/4} <= D1 <= 0, exact at scale 10^30.
    samples = tuple(range(3, 1001, 2)) + (10**6 + 1, 10**9 + 1, 10**12 + 1)
    assert m12_scan(samples)["holds"] is True


def test_oe_indicator_identity():
    # itinerary_word(n,3) == "OEE" iff m even and isqrt(m) even: the
    # branch-consistency claim behind Proposition L (depth-3 closure).
    assert oe_indicator_identity_check(5001)["holds"] is True


def test_lemma_m_second_order_forms():
    # Plain and shifted second-order forms with realized gaps G;
    # poly - lhs = -R with R the positive Taylor remainder.
    samples = tuple(range(5, 501, 2)) + (10**6 + 1, 10**9 + 1)
    for h in (1, 2):
        assert lemma_m_scan(samples, h=h)["holds"] is True


def test_lemma_n_level2_gap():
    # g2 = floor(DY) + [theta2 >= 1 - {DY}]: exact on orbit data,
    # guard-band skips only.
    result = level2_gap_check(10**6 + 1, 400, 1)
    assert result["holds"] is True
    assert result["matches"] >= 390


def test_kernel_probe_cancels():
    # Conjecture O support: the isolated tier-2 kernel exhibits strong
    # cancellation (far below the trivial bound; loose threshold).
    result = kernel_probe(10**4)
    assert result["abs_sum"] < 0.1 * result["count"]


def test_kernel_reformulation_identity():
    # Lemma R1: (1/2)(m^{9/4} - v^{3/2}) - (3/4) v^{1/2} theta_2 lies
    # in [0, (3/16) v^{-1/2}]; exact scaled integers through 10^12.
    samples = tuple(range(5, 1001, 2)) + (10**6 + 1, 10**9 + 1, 10**12 + 1)
    assert kernel_reformulation_scan(samples)["holds"] is True


def test_double_gap_identity():
    # Lemma R2: D2 g2 = floor(D2 D1 Y) + kappa'' + D2 kappa_2, exact
    # on orbit data (Lean: seq_floor_gap_second).
    for h1, h2 in ((1, 1), (1, 3), (2, 5)):
        result = double_gap_identity_check(10**6 + 1, 200, h1, h2)
        assert result["holds"] is True
        assert result["matches"] >= 190


def test_branch_freeze():
    # Lemma R3: per-branch floors of D2 D1 Y are frozen at the drift
    # scale; the j = 0 branch is constant across the whole cell.
    result = branch_freeze_scan(10**6, 1, 1, 400)
    assert result["in_cell"] >= 10
    assert result["branch_0"]["distinct"] == 1
    for j in (-1, 1):
        assert result[f"branch_{j}"]["distinct"] <= 5


def test_differenced_kernel_cancels():
    # Theorem R support: the once-, twice- and thrice-differenced kernel
    # sums cancel far below the trivial bound (loose threshold). The
    # third difference backs the targeted extra differencing of the
    # Phase-9 review repair.
    t1 = differenced_kernel_probe(10**4, 1)
    t2 = differenced_kernel_probe(10**4, 1, 2)
    t3 = differenced_kernel_probe(10**4, 1, 2, 3)
    assert t1["abs_sum"] < 0.1 * t1["count"]
    assert t2["abs_sum"] < 0.1 * t2["count"]
    assert t3["abs_sum"] < 0.1 * t3["count"]


def test_lemma_a_prime_w_level_linearization():
    # Theorem Q brick: w^{3/2} = -(1/2)m^{3/4} + (3/2)w m^{1/4} + E,
    # 0 <= E <= (3/8)(U-1)^{-1/2}, exact at scale 10^30.
    samples = tuple(range(5, 1001, 2)) + (10**6 + 1, 10**9 + 1, 10**12 + 1)
    assert lemma_a_prime_scan(samples)["holds"] is True


def test_oeo_smoothing_identity():
    # Full OEO* smoothing: w^{3/2} = n^{9/8} - (3/2) m^{1/4} theta_w
    # + d2 with the asymmetric decaying window.
    samples = tuple(range(5, 1001, 2)) + (10**6 + 1, 10**9 + 1, 10**12 + 1)
    assert oeo_smoothing_scan(samples)["holds"] is True


def test_oeo_indicator_identity():
    # All four OE** depth-4 words match the sign data (m even, parity
    # of w, parity of the branch-correct fourth value): the branch
    # consistency behind Theorem Q.
    result = oeo_indicator_identity_check(5001)
    assert result["holds"] is True
    assert result["checked"] > 1000


def test_oeo_mode_probe_cancels():
    # Theorem Q's mode sum cancels strongly (empirically ~P^{5/8},
    # the coherent w-cell random-walk scale; loose threshold).
    result = oeo_mode_probe(10**4)
    assert result["abs_sum"] < 0.1 * result["count"]


def test_oooee_smoothing_identity():
    samples = tuple(range(5, 1001, 2)) + (10**6 + 1, 10**9 + 1, 10**12 + 1)
    assert oooee_smoothing_scan(samples)["holds"] is True


def test_ooeoe_smoothing_identity():
    samples = tuple(range(5, 1001, 2)) + (10**6 + 1, 10**9 + 1, 10**12 + 1)
    assert ooeoe_smoothing_scan(samples)["holds"] is True


def test_oooee_indicator_identity():
    result = oooee_indicator_identity_check(5001)
    assert result["holds"] is True
    assert result["checked"] > 100


def test_ooeoe_indicator_identity():
    result = ooeoe_indicator_identity_check(5001)
    assert result["holds"] is True
    assert result["checked"] > 100


def test_oooee_mode_probe_cancels():
    result = oooee_mode_probe(10**4)
    assert result["count"] > 100
    assert result["abs_sum"] < 0.1 * result["count"]


def test_ooeoe_mode_probe_cancels():
    result = ooeoe_mode_probe(10**4)
    assert result["count"] > 100
    assert result["abs_sum"] < 0.1 * result["count"]


def test_depth5_contracting_words_near_product():
    counts = deep_word_counts(100_000, 5)
    odds = sum(counts.values())
    expected = odds / 16
    for w in ("OOOEE", "OOEOE", "OOOEO", "OOEOO"):
        assert abs(counts[w] - expected) < 80
    # Guard: every OOOEE / OOEOE start in the window descends in 5 steps.
    for n in range(3, 10_001, 2):
        w = itinerary_word(n, 5)
        if w in ("OOOEE", "OOEOE"):
            x = n
            for _ in range(5):
                x = juggler_step(x)
            assert x < n


def test_anti_overclaim_depth5_flag():
    assert ANTI_OVERCLAIM["depth5_contracting_proved"] is True
    assert ANTI_OVERCLAIM["depth5_kernel_isolated"] is True
    assert ANTI_OVERCLAIM["depth5_kernel_bound_proved"] is False
    assert ANTI_OVERCLAIM["scale_invariant_R_extension_refuted"] is True
    assert ANTI_OVERCLAIM["depth7_engine_contracting_proved"] is True
    assert ANTI_OVERCLAIM["density_one_claimed"] is False


def test_level3_reformulation_identity():
    # Lemma V1: (1/2)(v^{9/4} - z^{3/2}) - (3/4) z^{1/2} theta_3 lies
    # in [0, (3/16) z^{-1/2}]; exact scaled integers through 10^12.
    samples = tuple(range(5, 1001, 2)) + (10**6 + 1, 10**9 + 1, 10**12 + 1)
    assert level3_reformulation_scan(samples)["holds"] is True


def test_level3_kernel_probe_cancels():
    # Conjecture V support: the isolated level-3 kernel exhibits
    # square-root-scale cancellation (loose threshold).
    result = level3_kernel_probe(10**4)
    assert result["count"] > 1000
    assert result["abs_sum"] < 0.1 * result["count"]


def test_differenced_level3_kernel_cancels():
    t1 = differenced_level3_kernel_probe(10**4, 1)
    t2 = differenced_level3_kernel_probe(10**4, 1, 2)
    t3 = differenced_level3_kernel_probe(10**4, 1, 2, 3)
    assert t1["abs_sum"] < 0.1 * t1["count"]
    assert t2["abs_sum"] < 0.1 * t2["count"]
    assert t3["abs_sum"] < 0.1 * t3["count"]


def test_level3_raw_gap_is_wild():
    # Negative knowledge: raw Δ⁴ Z is not frozen. The smooth model
    # G^{(4)} ≪ 1 does not descend to the discrete nested floor.
    result = level3_raw_gap_wildness(10**4, 80)
    assert result["raw_d4_wild"] is True
    assert result["d3_above_smooth"] is True


def test_oooo_indicator_identity():
    result = oooo_indicator_identity_check(5001)
    assert result["holds"] is True
    assert result["checked"] > 100


def test_level3_inner_linearization_identity():
    # Lemma V2: v^{3/2} = m^{9/4} - (3/2) m^{3/4} theta_2 + E,
    # 0 <= E <= (3/8) v^{-1/2}; exact scaled integers through 10^12.
    samples = tuple(range(5, 1001, 2)) + (10**6 + 1, 10**9 + 1, 10**12 + 1)
    assert level3_inner_linearization_scan(samples)["holds"] is True


def test_v_level_has_no_cells():
    # Proposition W: floor(ΔY) and Δv have run length 1 — there are
    # no v-level b-runs, so Lemma R3 cannot be copied one layer up.
    for p in (10**4, 10**5, 10**6):
        result = v_level_cell_scan(p, 400)
        assert result["no_v_level_cells"] is True
        assert result["floor_dY_mean_run"] == 1.0
        assert result["dv_mean_run"] == 1.0


def test_sixth_ooeoo_identity():
    samples = tuple(range(5, 1001, 2)) + (10**6 + 1, 10**9 + 1, 10**12 + 1)
    assert sixth_ooeoo_scan(samples)["holds"] is True


def test_sixth_oooeo_identity():
    samples = tuple(range(5, 1001, 2)) + (10**6 + 1, 10**9 + 1, 10**12 + 1)
    assert sixth_oooeo_scan(samples)["holds"] is True


def test_w_gap_freezes_on_ooeo():
    result = w_gap_freeze_scan(10**4, 400)
    assert result["frozen"] is True
    assert result["mean_run"] >= 8


def test_ooeooee_indicator_identity():
    result = ooeooee_indicator_identity_check(5001)
    assert result["holds"] is True
    assert result["checked"] > 50


def test_oooeoee_indicator_identity():
    result = oooeoee_indicator_identity_check(5001)
    assert result["holds"] is True
    assert result["checked"] > 50


def test_depth7_engine_contractors_descend():
    assert 3**4 < 2**7
    counts = deep_word_counts(20_000, 7)
    odds = sum(counts.values())
    expected = odds / 128
    for w in ("OOEOOEE", "OOOEOEE"):
        assert abs(counts[w] - expected) < 1.5 * (20_000 ** (2 / 3))
    for n in range(3, 10_001, 2):
        w = itinerary_word(n, 7)
        if w in ("OOEOOEE", "OOOEOEE"):
            x = n
            for _ in range(7):
                x = juggler_step(x)
            assert x < n


def test_depth6_census_minimal_scale_envelope():
    # All 32 depth-6 words realized; deviations obey the two-regime
    # envelope max((N/2) N^{-gamma_min}, N^{2/3}) with constant <= 1.5.
    n_max = 100_000
    counts = deep_word_counts(n_max, 6)
    assert len(counts) == 32
    odds = sum(counts.values())
    expected = odds / 32

    def gamma_min(word: str) -> float:
        g, gm = 1.0, float("inf")
        for ch in word:
            g *= 1.5 if ch == "O" else 0.5
            gm = min(gm, g)
        return gm

    for w, c in counts.items():
        envelope = max((n_max / 2) * n_max ** (-gamma_min(w)), n_max ** (2 / 3))
        assert abs(c - expected) <= 1.5 * envelope
