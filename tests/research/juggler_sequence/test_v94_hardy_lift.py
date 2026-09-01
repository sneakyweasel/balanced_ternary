"""Three-term remainder of {v^{9/4}}: witnesses that the identity is Lemma G."""

from __future__ import annotations

from research.juggler_sequence.v94_hardy_lift import (
    A2P_LEADING,
    ANTI,
    BOUND_R3,
    CLASS_GREEN,
    TEST_CENSUS_WINDOW,
    a2_species,
    build_summary,
    hardy_pair_census,
    remainder_check,
)

TEST_SAMPLES = tuple(range(5, 201, 2)) + (10**4 + 1, 10**6 + 1)


def test_cubic_remainder_vanishes():
    rem = remainder_check(TEST_SAMPLES)
    assert rem["holds"]
    assert rem["r3_vanishes"]
    assert rem["worst_ratio"] <= BOUND_R3 * (1.0 + 1e-3)
    assert rem["samples_used"] > 20


def test_quadratic_passenger_is_tame():
    a2 = a2_species(TEST_SAMPLES)
    assert a2["tame"]
    assert a2["a2prime_exponent"] < 0
    assert a2["pairs_used"] > 20
    assert abs(a2["mean_a2prime_times_n58"] - A2P_LEADING) < 0.05


def test_hardy_pair_fills_torus_on_small_window():
    pair = hardy_pair_census(TEST_CENSUS_WINDOW)
    assert pair["occupied_cells"] == pair["cells"]
    assert pair["occupied_all"]
    assert pair["fills_torus"]


def test_summary_green_and_anti_overclaim():
    summary = build_summary(
        identity_samples=TEST_SAMPLES, census_n_max=TEST_CENSUS_WINDOW
    )
    assert summary["decision"]["classification"] == CLASS_GREEN
    assert summary["decision"]["reparameterization_of_lemma_g"]
    assert summary["decision"]["not_a_published_theorem"]
    assert summary["decision"]["door_still_unbuilt"]
    assert not ANTI["equidistribution_claimed"]
    assert not ANTI["k3_bound_claimed"]
    assert not ANTI["toolkit_reopened"]
    assert not ANTI["paper_b_modified"]
    assert not ANTI["richter_cited_as_theorem"]
    assert not ANTI["density_one_claimed"]
