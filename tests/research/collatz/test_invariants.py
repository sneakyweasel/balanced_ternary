"""Exhaustive checks of Collatz / balanced ternary identities."""

from __future__ import annotations

from bt.metrics import weight
from bt.representation import encode
from research.collatz.core import collatz_step
from research.collatz.experiments.exhaustive import run_exhaustive_experiment
from research.collatz.invariants import verify_collatz_invariants


def test_odd_n_has_odd_weight_and_3n1_even_weight_range():
    for n in range(1, 20_001, 2):
        assert weight(encode(n)) % 2 == 1
        y = 3 * n + 1
        assert y % 2 == 0
        assert weight(encode(y)) % 2 == 0
        t = collatz_step(n)
        assert weight(encode(t)) % 2 == 1


def test_verify_collatz_invariants_helper():
    report = verify_collatz_invariants(1500, automaton_precision=8, inverse_k_max=12)
    assert report.ok
    assert report.checked_odd == 750


def test_exhaustive_experiment_in_memory(tmp_path):
    result = run_exhaustive_experiment(200, output_dir=tmp_path, sample_size=3)
    assert result.checked == 100
    assert result.weight_parity_failures == 0
    assert result.ternary_shift_failures == 0
    assert result.rows_written == 100
    assert result.output_metadata is not None
    assert len(result.sample_rows) == 3
    assert result.sample_rows[0]["n"] == 1
    meta = (tmp_path / "reports").glob("*.json")
    assert list(meta)
