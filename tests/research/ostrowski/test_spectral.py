"""Spectral comparison: Pisot control vs one non-Pisot order-3 Gamma."""

from __future__ import annotations

from research.ostrowski.live_growth import (
    growth_table,
    legal_w,
    reachable_live,
)
from research.ostrowski.nonpisot_search import (
    HUB,
    hub_live_certificate,
    hub_reachable_at_even_remaining,
)
from research.ostrowski.residual import next_state
from research.ostrowski.residual_closure import B_MIN
from research.ostrowski.spectral import exact_pisot_cubic_certificate, spectral_data
from research.ostrowski.spectral_residual import (
    residual_matrix,
    spectral_residual_report,
    transition_affine,
    transition_matches_next_state,
)
from research.ostrowski.system import (
    characteristic_poly_coeffs,
    nonpisot_order3,
    phase0_order3,
)


def test_gamma_np_is_irreducible_perron_non_pisot():
    sys = nonpisot_order3()
    data = spectral_data(sys)
    cert = exact_pisot_cubic_certificate(data["characteristic_polynomial"])
    assert data["digits"] == (2, 1, 3)
    assert data["irreducible_cubic"]
    assert data["pisot"] is False
    assert data["perron"] is True
    assert cert["irreducible"]
    assert cert["one_real_two_complex"]
    assert cert["perron_non_pisot"]
    assert cert["pisot"] is False
    assert cert["real_root_interval"] == (2, 3)
    assert cert["product_of_roots"] == 3


def test_gamma_p_is_pisot_by_the_same_certificate():
    sys = phase0_order3()
    data = spectral_data(sys)
    cert = exact_pisot_cubic_certificate(data["characteristic_polynomial"])
    assert data["digits"] == (2, 1, 1)
    assert data["pisot"]
    assert cert["pisot"]
    assert cert["perron_non_pisot"] is False
    assert cert["product_of_roots"] == 1


def test_memoryless_alphabets_agree():
    p, np_sys = phase0_order3(), nonpisot_order3()
    assert legal_w(p, 0) == legal_w(np_sys, 0) == (-2, -1, 0, 1)
    assert legal_w(p, 1) == legal_w(np_sys, 1) == tuple(range(-4, 3))


def test_affine_transition_matches_next_state_on_both_systems():
    for sys in (phase0_order3(), nonpisot_order3()):
        for state in ((0, 0, 0), (1, -1, 2), (-2, 3, -1)):
            for w in range(-4, 3):
                assert transition_matches_next_state(sys, state, w)
                assert transition_affine(sys, state, w) == next_state(sys, state, w, 8)


def test_residual_matrix_has_the_place_value_characteristic_polynomial():
    for sys in (phase0_order3(), nonpisot_order3()):
        report = spectral_residual_report(sys)
        assert report["matches_place_value_polynomial"]
        d1, d2, d3 = report["digits"]
        assert residual_matrix(sys) == ((0, 0, d3), (1, 0, d2), (0, 1, d1))
        assert report["matrix_characteristic_polynomial"] == characteristic_poly_coeffs(sys)


def test_control_live_set_is_still_b_min():
    report = reachable_live(phase0_order3(), 12)
    assert report["live_states"] == 55
    assert report["states"] == B_MIN


def test_nonpisot_live_union_grows_in_the_scan_window():
    rows = growth_table(nonpisot_order3(), 10)
    lives = [row["live_states"] for row in rows]
    assert lives[0] == 1
    assert all(lives[i] < lives[i + 1] for i in range(len(lives) - 1))
    last = rows[-1]
    assert last["max_abs_s3"] >= 3
    assert last["max_abs_s1"] >= 10
    # Finite depth is not a proof that the union is infinite.
    assert last["depth"] == 10


def test_hub_is_live_and_reached_by_the_length_two_prefix():
    sys = nonpisot_order3()
    assert HUB == (-3, -1, 0)
    for i in range(0, 24):
        assert hub_live_certificate(sys, i)
    for m in range(0, 8):
        assert hub_reachable_at_even_remaining(2 * m, sys)


def test_hollander_is_registered():
    from research.literature import get_reference

    rec = get_reference("hollander-1998-greedy-regularity")
    assert rec["year"] == 1998
