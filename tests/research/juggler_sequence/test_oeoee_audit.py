"""Second-pass audit of the OEOEE envelope constants (docs/theory/juggler_oeoee_production.md §11)."""

from __future__ import annotations

from research.juggler_sequence.oeoee_audit import assemble, measured, t3_worst_ratio


def test_sizes_and_chain_inequalities_hold_on_exact_data() -> None:
    out = measured(60, Q=6)
    assert out["sizes_ok"] and out["omega_deviation_max"] <= 1.5
    for row in out["per_q"]:
        assert row["sum_abs_S"] <= row["note_bound"]
        assert row["annulus_max_over_4V1"] <= 1.0
        assert row["kusmin_landau_worst_ratio"] <= 1.0
        assert 1 - 8 / (9 * 60) <= row["block_length_over_delta_min"] <= row["block_length_over_delta_max"] <= 1.0 + 1e-9


def test_lambda3_pairing_constant_is_corrected() -> None:
    """The note's 0.89 m'^{14/9} is exceeded by the data at m' = 200; the (T5) bound with V Delta/2 holds."""

    out = measured(200, Q=1)
    assert out["lambda3_alone_sum"] > out["lambda3_note_bound"]
    assert out["lambda3_alone_sum"] <= out["lambda3_T5_exact"] <= 1.1 * out["lambda3_corrected_bound"]


def test_second_derivative_test_with_plus_two_holds_on_the_modes() -> None:
    assert t3_worst_ratio(60, s_max=4, u_max=4) < 1.0


def test_independent_assembly_confirms_the_envelope_from_four_on() -> None:
    for mp in (4, 10, 60, 200, 10**4, 10**6):
        assert assemble(mp)["ratio_to_note_envelope"] < 1.0
    assert assemble(2)["ratio_to_note_envelope"] > 1.0  # vacuous there anyway: the bound exceeds 200
    assert assemble(2)["theta_bound"] > 200
    out = measured(60, Q=1)
    assert out["deviation"] <= assemble(60)["total"]
