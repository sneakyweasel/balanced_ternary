"""/2^k and L_k complexity spectrum."""

from __future__ import annotations

from collatz.experiments.complexity_spectrum import complexity_row, run_complexity_spectrum
from collatz.transducers.divide_by_two_power import DivideByTwoPowerTransducer


def test_n_k_small_values():
    expected = {1: 3, 2: 5, 3: 9, 4: 17}
    for k, n_k in expected.items():
        report = DivideByTwoPowerTransducer(k).complexity_report()
        assert report["minimized"] == n_k
        row = complexity_row(k)
        assert row["N_k"] == n_k
        assert row["matches_two_k_plus_one"]
        assert row["A_k"] >= 1
        assert row["C_k"] == {"A_k": row["A_k"], "N_k": n_k}


def test_spectrum_range_holds_conjecture():
    result = run_complexity_spectrum(4)
    assert result.k_max == 4
    assert result.n_k_equals_two_k_plus_one
    assert "CONJECTURE" in result.format()
