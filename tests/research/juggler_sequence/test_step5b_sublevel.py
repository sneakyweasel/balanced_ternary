"""Fast checks for Step 5b sublevel geometry vs Lemma 3.9."""

from __future__ import annotations

from research.juggler_sequence.step5b_sublevel import (
    ANTI,
    C7,
    C7_ROW,
    FAMILY_NAMES,
    family_params,
    measure_model,
    paper_shifts,
    vandermonde_matrix,
)


def test_anti_overclaim() -> None:
    assert ANTI["sums_evaluated"] is False
    assert ANTI["paper_b_modified"] is False
    assert ANTI["k3_reopened"] is False
    assert ANTI["harvest_reopened"] is False
    assert ANTI["alpha_33_32"] is False
    assert ANTI["kernel_retagged"] is False


def test_c7_positive_on_printed_triple() -> None:
    assert C7 > 0.0
    assert C7_ROW["c7_positive_octant"] > 0.0
    assert abs(C7_ROW["det"]) > 1e-12
    m = vandermonde_matrix()
    assert len(m) == 3
    assert abs(m[1][0] + 0.75) < 1e-15
    assert abs(m[1][1] + 0.625) < 1e-15
    assert abs(m[1][2] + 0.5) < 1e-15


def test_w0_opposite_sign_one_omega_interval() -> None:
    params = family_params(10**6, "centre_cancel_w0", k=1)
    assert params is not None
    row = measure_model(params, which="phi", n_grid=20_000)
    assert row["omega_intervals"] == 1
    assert row["count_ok"]
    assert row["single_signed_complement"]


def test_same_sign_empty_omega() -> None:
    params = family_params(10**6, "centre_same_w0", k=1)
    assert params is not None
    row = measure_model(params, which="phi", n_grid=20_000)
    assert row["omega_intervals"] == 0
    assert row["omega_length"] == 0.0
    assert row["count_ok"]
    assert row["single_signed_complement"]


def test_p1e6_interval_count_at_most_cap() -> None:
    sh = paper_shifts(10**6)
    assert sh["h1"] >= 1
    seen = 0
    for name in FAMILY_NAMES:
        params = family_params(10**6, name, k=1)
        if params is None:
            continue
        row = measure_model(params, which="phi", n_grid=20_000)
        assert row["omega_intervals"] <= row["interval_cap"]
        assert row["count_ok"]
        seen += 1
    assert seen == len(FAMILY_NAMES)
