"""Regression tests for exact compatibility experiments."""

from __future__ import annotations

import json
from pathlib import Path

from research.collatz.experiments.information_content import (
    S1_BT_THEOREM,
    balanced_ternary_collision_witness,
    determinism_report,
    diagnostic_row,
    run_information_content,
    smallest_collision_witness,
    state_key,
)
from research.collatz.experiments.near_critical import (
    ExactDriftBand,
    adversarial_rearrangements,
    critical_K,
    exhaustive_near_critical_codes,
    is_near_critical,
    mechanical_critical_code,
    rozier_terracol_fixture_pairs,
    run_near_critical,
    seeded_random_critical_codes,
)
from research.collatz.experiments.schema import (
    COMPATIBILITY_SCHEMA_VERSION,
    validate_compatibility_row,
)
from research.collatz.experiments.table_io import read_jsonl


def test_s0_s3_partitions_and_exact_s1_bt_theorem():
    rows = [diagnostic_row(ks) for ks in ((1, 2), (2, 1), (1, 1, 1), (3,))]
    assert state_key(rows[0], "S0") == (2, 3)
    assert state_key(rows[0], "S1") == (2, 3, rows[0]["R"])
    assert state_key(rows[0], "S2")[-1] == rows[0]["M"]
    assert state_key(rows[0], "S3")[-1] == rows[0]["C"]
    report = determinism_report(rows, "BT(R)")
    assert report["states"]["S1"]["determines_on_sample"]
    assert report["states"]["S1"]["status"] == S1_BT_THEOREM
    assert report["states"]["S2"]["determines_on_sample"]
    assert report["states"]["S3"]["determines_on_sample"]


def test_smallest_s0_witness_is_reproducible():
    rows = [diagnostic_row(ks) for ks in ((1, 2), (2, 1), (1, 1, 1))]
    witness = smallest_collision_witness(rows, "S0", "R")
    assert witness is not None
    assert witness["row_a"]["valuations"] == [1, 2]
    assert witness["row_b"]["valuations"] == [2, 1]


def test_full_balanced_ternary_does_not_determine_successor_or_lifts():
    rows = [diagnostic_row(ks) for ks in ((1,), (1, 4))]
    assert rows[0]["R"] == rows[1]["R"] == 3
    assert rows[0]["BT(R)"] == rows[1]["BT(R)"] == "+0"
    successor = balanced_ternary_collision_witness(rows, "next_zero_lift_k")
    proposed = balanced_ternary_collision_witness(rows, "proposed_lift_digits")
    assert successor is not None
    assert successor["status"] == "EXACT COLLISION WITNESS"
    assert {successor["row_a"]["next_zero_lift_k"], successor["row_b"]["next_zero_lift_k"]} == {2, 4}
    assert proposed is not None


def test_information_rows_manifest_and_truncated_analysis(tmp_path):
    result = run_information_content(3, 3, precisions=(1, 2), output_dir=tmp_path)
    assert result.schema_version == COMPATIBILITY_SCHEMA_VERSION
    assert read_jsonl(result.paths["jsonl"]) == list(result.rows)
    manifest = json.loads(Path(result.paths["manifest"]).read_text(encoding="utf-8"))
    assert manifest["parameters"]["max_length"] == 3
    assert manifest["row_count"] == len(result.rows)
    assert all(item["status"].startswith("VERIFIED COMPUTATIONALLY") for item in result.truncated)
    assert result.balanced_ternary_collisions["next_zero_lift_k"] is not None


def test_compatibility_schema_core_is_nonbreaking():
    row = diagnostic_row((1, 4))
    validate_compatibility_row(row)
    enriched = {**row, "future_optional_field": {"allowed": True}}
    validate_compatibility_row(enriched)


def test_exact_near_critical_membership_uses_closed_rational_band():
    singleton = ExactDriftBand(3, 4, 3, 4)
    assert singleton.contains(1, 2)  # 3/4 exactly
    assert not singleton.contains(2, 3)  # 9/8
    assert is_near_critical(1, 2, band=singleton)
    assert is_near_critical((2,), band=singleton)
    assert critical_K(2) == 3


def test_exhaustive_seeded_mechanical_and_adversarial_generators():
    band = ExactDriftBand(1, 2, 2, 1)
    exhaustive = exhaustive_near_critical_codes(3, 3, band=band)
    assert exhaustive
    first = seeded_random_critical_codes(12, 20, seed=8675309, band=band)
    second = seeded_random_critical_codes(12, 20, seed=8675309, band=band)
    assert first == second
    assert all(len(code) == 12 and band.contains(12, sum(code)) for code in first)
    mechanical = mechanical_critical_code(30)
    assert len(mechanical) == 30
    assert set(mechanical) <= {1, 2}
    arrangements = adversarial_rearrangements((1, 2, 1, 3))
    assert len({sum(code) for code in arrangements}) == 1
    assert all(sorted(code) == [1, 1, 2, 3] for code in arrangements)


def test_rozier_terracol_fixture_pairs_are_exact_and_named():
    fixtures = rozier_terracol_fixture_pairs()
    assert [(row["K_standard_steps"], row["m_odd_steps"]) for row in fixtures] == [
        (8, 5),
        (27, 17),
        (46, 29),
        (54, 34),
        (65, 41),
        (73, 46),
        (92, 58),
    ]
    assert all(row["three_power"] < row["two_power"] for row in fixtures)
    assert all("COMPUTATIONAL" in row["source_status"] for row in fixtures)


def test_near_critical_rows_and_manifest_are_seed_reproducible(tmp_path):
    kwargs = {
        "exhaustive_max_length": 2,
        "exhaustive_max_k": 3,
        "random_length": 8,
        "random_count": 5,
        "seed": 17,
        "mechanical_lengths": (5, 8),
        "permutation_code": (1, 2, 2),
    }
    first = run_near_critical(**kwargs, output_dir=tmp_path / "a")
    second = run_near_critical(**kwargs, output_dir=tmp_path / "b")
    assert first.rows == second.rows
    assert first.fixtures == second.fixtures
    assert first.seed == second.seed == 17
    assert read_jsonl(first.paths["jsonl"]) == list(first.rows)
