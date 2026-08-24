"""Regression tests for affine-center censuses."""

from __future__ import annotations

import json
from pathlib import Path

from research.collatz.experiments.affine_center import (
    coordinate_order_report,
    enumerate_affine_centers,
    fraction_from_pair,
    run_affine_center_census,
)
from research.collatz.experiments.schema import (
    AFFINE_CENTER_SCHEMA_VERSION,
    validate_affine_center_row,
)
from research.collatz.experiments.table_io import read_jsonl


def test_affine_center_census_schema_and_manifest(tmp_path):
    result = run_affine_center_census(
        3,
        4,
        critical_gap=1,
        closest_count=5,
        output_dir=tmp_path,
    )
    assert result.schema_version == AFFINE_CENTER_SCHEMA_VERSION
    assert len(result.rows) == 4 + 16 + 64
    assert sum(result.partition_counts.values()) == len(result.rows)
    assert len(result.closest_to_critical) == 5
    assert read_jsonl(result.paths["jsonl"]) == list(result.rows)
    manifest = json.loads(Path(result.paths["manifest"]).read_text(encoding="utf-8"))
    assert manifest["schema_version"] == AFFINE_CENTER_SCHEMA_VERSION
    assert manifest["row_count"] == len(result.rows)
    for row in result.rows:
        validate_affine_center_row(row)


def test_all_theorem_backed_inequalities_have_no_failures():
    result = run_affine_center_census(4, 4)
    assert result.exact_inequalities
    assert all(
        record["failure_count"] == 0
        for record in result.exact_inequalities.values()
    )


def test_simple_coordinate_orders_preserve_counterexamples():
    states = enumerate_affine_centers(4, 4)
    report = coordinate_order_report(states)
    for name in ("R_le_M", "M_le_R", "C_le_R", "R_le_C"):
        assert report[name]["smallest_true"] is not None
        assert report[name]["smallest_false"] is not None
        assert not report[name]["universal_on_sample"]


def test_exact_fraction_pairs_round_trip():
    result = run_affine_center_census(2, 3)
    for row in result.rows:
        center = fraction_from_pair(row["n_star"])
        R_delta = fraction_from_pair(row["R_minus_n_star_reduced"])
        X_delta = fraction_from_pair(row["X_minus_n_star_reduced"])
        assert R_delta == row["R"] - center
        assert X_delta == row["X"] - center
