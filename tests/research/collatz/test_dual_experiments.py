"""Dual-code experiment regressions and exact counterexamples."""

from __future__ import annotations

from research.collatz.experiments.noncontracting_dual import (
    largest_noncontracting_K,
    run_noncontracting_dual,
)
from research.collatz.experiments.periodic_dual import (
    periodic_dual_trace,
    primitive_period,
)
from research.collatz.experiments.schema import ExperimentManifest, validate_dual_row
from research.collatz.experiments.suffix_determination import suffix_determination_census
from research.collatz.experiments.table_io import read_jsonl, write_experiment
from research.collatz.order_analysis import (
    adjacent_swap_delta_R_residue,
    extremal_orders,
    verify_swap_R_residue_formula,
)


def test_suffix_census_contains_exact_full_R_counterexample():
    result = suffix_determination_census(3, 4, 4)
    counterexample = result["exact_full_R_counterexample"]
    assert counterexample["R"] == 3
    assert counterexample["zero_lift_a"] != counterexample["zero_lift_b"]
    assert counterexample["lift_digit_a"] != counterexample["lift_digit_b"]
    assert any(not row["next_value_determined"] for row in result["rows"])


def test_R_adjacent_swap_residue_formula():
    for ks in ((1, 2), (1, 1, 2), (3, 1, 2, 2)):
        for index in range(len(ks) - 1):
            assert verify_swap_R_residue_formula(ks, index)
            assert 0 <= adjacent_swap_delta_R_residue(ks, index) < (
                1 << (sum(ks) + 1)
            )


def test_permutation_rows_include_lift_patterns_and_exact_covariance():
    result = extremal_orders((1, 1, 2))
    assert result["C_R_covariance_numerator"] == 0 or isinstance(
        result["C_R_covariance_numerator"], int
    )
    assert result["lift_patterns"]
    assert not result["R_extremal_are_sorted"]


def test_periodic_benchmarks():
    assert primitive_period((2, 2, 2)) == (2,)
    ones = periodic_dual_trace((1,), repeats=6)
    assert ones["lift_digits"] == [1] * 6
    assert [row["R"] for row in ones["rows"]] == [
        3,
        7,
        15,
        31,
        63,
        127,
    ]
    twos = periodic_dual_trace((2,), repeats=6)
    assert twos["lift_digits"] == [0] * 6
    assert all(row["R"] == 1 for row in twos["rows"])


def test_noncontracting_uses_exact_integer_cut_and_records_local_counterexample():
    for m in range(1, 15):
        K = largest_noncontracting_K(m)
        assert (1 << K) <= pow(3, m)
        assert (1 << (K + 1)) > pow(3, m)
    result = run_noncontracting_dual(length=5, k_max=3)
    assert not result["truncated"]
    example = result["known_local_counterexample"]
    assert example["lift_digits"][-1] == 0
    assert "nothing" in example["status"]


def test_versioned_experiment_round_trip(tmp_path):
    trace = periodic_dual_trace((2,), repeats=2)
    rows = trace["rows"]
    manifest = ExperimentManifest(
        experiment_name="periodic_dual_test",
        parameters={"period": [2], "repeats": 2},
        row_count=len(rows),
        claim_status="EXACT finite rows",
    )
    paths = write_experiment(rows, tmp_path, "periodic_dual_test", manifest)
    assert read_jsonl(paths["jsonl"]) == rows
    assert paths["manifest"]


def test_dual_row_schema():
    from research.collatz.dual_code import CollatzDualCode

    row = CollatzDualCode.from_valuations((1, 4, 2)).as_dict()
    validate_dual_row(row)
