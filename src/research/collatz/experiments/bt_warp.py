"""Reproducible balanced-ternary warp / Collatz commutator experiments."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from research.collatz.experiments.schema import (
    BT_WARP_SCHEMA_VERSION,
    ExperimentManifest,
    validate_bt_warp_row,
)
from research.collatz.experiments.table_io import write_experiment
from research.collatz.warp import (
    commutator_census,
    enumerate_operator_words,
    identity_table,
    palindrome_along_trajectory,
    realizer_warp_census,
    special_class_report,
    warp_state,
)


@dataclass(frozen=True)
class BtWarpCensusResult:
    limit: int
    rows: tuple[dict[str, Any], ...]
    census: dict[str, Any]
    special_classes: dict[str, dict[str, Any]]
    identities: dict[str, Any]
    schema_version: str
    paths: dict[str, str]


def warp_rows(limit: int) -> tuple[dict[str, Any], ...]:
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise ValueError("limit must be an integer >= 1")
    rows = []
    for n in range(1, limit + 1, 2):
        row = warp_state(n).experiment_row()
        validate_bt_warp_row(row)
        rows.append(row)
    return tuple(rows)


def run_bt_warp_census(
    limit: int,
    *,
    identity_length: int = 6,
    output_dir: Path | str | None = None,
) -> BtWarpCensusResult:
    rows = warp_rows(limit)
    census = commutator_census(limit)
    special = special_class_report(limit)
    identities = identity_table(limit, max_length=identity_length)
    paths: dict[str, str] = {}
    if output_dir is not None:
        manifest = ExperimentManifest(
            experiment_name="bt-warp-census",
            parameters={
                "limit": limit,
                "identity_length": identity_length,
                "domain": "positive odd integers",
            },
            row_count=len(rows),
            claim_status="VERIFIED COMPUTATIONALLY on the stated odd bound",
            schema_version=BT_WARP_SCHEMA_VERSION,
        )
        paths = write_experiment(list(rows), output_dir, "bt_warp_census", manifest)
    return BtWarpCensusResult(
        limit=limit,
        rows=rows,
        census=census,
        special_classes=special,
        identities=identities,
        schema_version=BT_WARP_SCHEMA_VERSION,
        paths=paths,
    )


@dataclass(frozen=True)
class BtWarpRealizerResult:
    max_length: int
    max_k: int
    rows: tuple[dict[str, Any], ...]
    report: dict[str, Any]
    schema_version: str
    paths: dict[str, str]


def run_bt_warp_realizer(
    max_length: int,
    max_k: int,
    *,
    output_dir: Path | str | None = None,
) -> BtWarpRealizerResult:
    report = realizer_warp_census(max_length, max_k)
    rows = tuple(report["rows"])
    for row in rows:
        validate_bt_warp_row(row, cylinder=True)
    paths: dict[str, str] = {}
    if output_dir is not None:
        manifest = ExperimentManifest(
            experiment_name="bt-warp-realizer",
            parameters={"max_length": max_length, "max_k": max_k},
            row_count=len(rows),
            claim_status="VERIFIED COMPUTATIONALLY on the bounded exponent-code sample",
            schema_version=BT_WARP_SCHEMA_VERSION,
        )
        paths = write_experiment(list(rows), output_dir, "bt_warp_realizer", manifest)
    return BtWarpRealizerResult(
        max_length=max_length,
        max_k=max_k,
        rows=rows,
        report=report,
        schema_version=BT_WARP_SCHEMA_VERSION,
        paths=paths,
    )


def semigroup_agreement_sample(
    max_length: int,
    sample_limit: int,
) -> dict[str, Any]:
    """Cluster operator words by their values on a finite odd sample.

    Agreement on the sample is not a theorem. Unexpected equalities are
    recorded as computational observations together with any later
    disagreement found while scanning a larger bound.
    """
    words = enumerate_operator_words(max_length)
    from research.collatz.warp import apply_word, smallest_disagreement

    signatures: dict[tuple[object, ...], list[str]] = {}
    odds = tuple(range(1, sample_limit + 1, 2))
    for ops in words:
        signature = tuple(apply_word(ops, n) for n in odds)
        key = " ".join(ops) if ops else "id"
        signatures.setdefault(signature, []).append(key)
    clusters = [group for group in signatures.values() if len(group) > 1]
    unexpected = []
    for group in clusters:
        if "id" in group and "W W" in group:
            continue
        if any(item.replace("Wt Wt ", "").replace(" Wt Wt", "") != item for item in group):
            # Involutive tail-reverse cancellation is expected.
            continue
        unexpected.append(group)
    return {
        "max_length": max_length,
        "sample_limit": sample_limit,
        "word_count": len(words),
        "cluster_count": len(clusters),
        "clusters": clusters[:40],
        "ww_agrees_with_id_on_sample": any(
            "id" in group and "W W" in group for group in clusters
        ),
        "wt_wt_agrees_with_id_on_sample": any(
            "id" in group and "Wt Wt" in group for group in clusters
        ),
        "W_W_counterexample": smallest_disagreement(("W", "W"), (), sample_limit),
        "Wt_Wt_counterexample": smallest_disagreement(("Wt", "Wt"), (), sample_limit),
        "status": "VERIFIED COMPUTATIONALLY on the stated sample",
    }


def palindrome_orbit_sample(starts: tuple[int, ...], max_steps: int) -> dict[str, Any]:
    rows = []
    for n in starts:
        flags = palindrome_along_trajectory(n, max_steps)
        pal_count = sum(1 for row in flags if row["palindrome"])
        rows.append(
            {
                "start": n,
                "length": len(flags),
                "palindrome_count": pal_count,
                "first_palindrome": next(
                    (row["n"] for row in flags if row["palindrome"]), None
                ),
            }
        )
    return {
        "starts": list(starts),
        "max_steps": max_steps,
        "rows": rows,
        "status": "OBSERVATION on named trajectories",
    }
