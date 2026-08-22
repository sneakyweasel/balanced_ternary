"""Exact census of affine-center geometry across exponent codes."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import Callable, Iterable

from research.collatz.affine_center import AffineCenterState
from research.collatz.experiments.schema import (
    AFFINE_CENTER_SCHEMA_VERSION,
    ExperimentManifest,
    validate_affine_center_row,
)
from research.collatz.experiments.table_io import write_experiment


Relation = Callable[[AffineCenterState], bool]


def enumerate_affine_centers(
    max_length: int,
    max_k: int,
) -> tuple[AffineCenterState, ...]:
    if (
        isinstance(max_length, bool)
        or not isinstance(max_length, int)
        or max_length < 1
    ):
        raise ValueError("max_length must be an integer >= 1")
    if isinstance(max_k, bool) or not isinstance(max_k, int) or max_k < 1:
        raise ValueError("max_k must be an integer >= 1")
    return tuple(
        AffineCenterState.from_valuations(valuations)
        for length in range(1, max_length + 1)
        for valuations in product(range(1, max_k + 1), repeat=length)
    )


def _state_order(state: AffineCenterState) -> tuple[int, int, tuple[int, ...]]:
    return state.m, state.K, state.valuations


def _relation_record(
    states: Iterable[AffineCenterState],
    relation: Relation,
) -> dict[str, object]:
    ordered = sorted(states, key=_state_order)
    true_states = [state for state in ordered if relation(state)]
    false_states = [state for state in ordered if not relation(state)]
    return {
        "true_count": len(true_states),
        "false_count": len(false_states),
        "smallest_true": (
            true_states[0].as_dict() if true_states else None
        ),
        "smallest_false": (
            false_states[0].as_dict() if false_states else None
        ),
        "universal_on_sample": not false_states,
        "status": "VERIFIED COMPUTATIONALLY on the bounded census",
    }


def coordinate_order_report(
    states: Iterable[AffineCenterState],
) -> dict[str, dict[str, object]]:
    """Test simple candidate coordinate orders and preserve both witnesses."""
    relations: dict[str, Relation] = {
        "R_le_M": lambda state: state.R <= state.M,
        "M_le_R": lambda state: state.M <= state.R,
        "C_le_R": lambda state: state.C <= state.R,
        "R_le_C": lambda state: state.R <= state.C,
        "n_star_le_R": lambda state: state.n_star <= state.R,
        "R_le_n_star": lambda state: state.R <= state.n_star,
        "n_star_le_M": lambda state: state.n_star <= state.M,
        "M_le_n_star": lambda state: state.M <= state.n_star,
    }
    materialized = tuple(states)
    return {
        name: _relation_record(materialized, relation)
        for name, relation in relations.items()
    }


def exact_inequality_report(
    states: Iterable[AffineCenterState],
) -> dict[str, dict[str, object]]:
    """Aggregate the theorem-backed inequalities checked by each state."""
    materialized = tuple(states)
    names = sorted(
        {
            name
            for state in materialized
            for name in state.exact_inequalities()
        }
    )
    report: dict[str, dict[str, object]] = {}
    for name in names:
        applicable = [
            state
            for state in materialized
            if name in state.exact_inequalities()
        ]
        failures = [
            state
            for state in applicable
            if not state.exact_inequalities()[name]
        ]
        report[name] = {
            "applicable_count": len(applicable),
            "failure_count": len(failures),
            "smallest_failure": failures[0].as_dict() if failures else None,
            "status": "PROVED identity/inequality; bounded regression",
        }
    return report


@dataclass(frozen=True)
class AffineCenterCensus:
    rows: tuple[dict[str, object], ...]
    partition_counts: dict[str, int]
    exact_inequalities: dict[str, dict[str, object]]
    coordinate_orders: dict[str, dict[str, object]]
    closest_to_critical: tuple[dict[str, object], ...]
    paths: dict[str, str]
    schema_version: str = AFFINE_CENTER_SCHEMA_VERSION


def run_affine_center_census(
    max_length: int,
    max_k: int,
    *,
    critical_gap: int = 1,
    closest_count: int = 20,
    output_dir: Path | str | None = None,
) -> AffineCenterCensus:
    if (
        isinstance(critical_gap, bool)
        or not isinstance(critical_gap, int)
        or critical_gap < 0
    ):
        raise ValueError("critical_gap must be an integer >= 0")
    if (
        isinstance(closest_count, bool)
        or not isinstance(closest_count, int)
        or closest_count < 0
    ):
        raise ValueError("closest_count must be an integer >= 0")
    states = enumerate_affine_centers(max_length, max_k)
    rows = tuple(state.as_dict(critical_gap) for state in states)
    for row in rows:
        validate_affine_center_row(row)
    partition_counts: dict[str, int] = {}
    for row in rows:
        partition = str(row["partition"])
        partition_counts[partition] = partition_counts.get(partition, 0) + 1
    closest_states = sorted(
        states,
        key=lambda state: (abs(state.gap), state.m, state.K, state.valuations),
    )[:closest_count]
    closest = tuple(state.as_dict(critical_gap) for state in closest_states)
    paths: dict[str, str] = {}
    if output_dir is not None:
        manifest = ExperimentManifest(
            experiment_name="affine_center_census",
            parameters={
                "max_length": max_length,
                "max_k": max_k,
                "critical_gap": critical_gap,
                "closest_count": closest_count,
                "selection": "exhaustive exponent-code product",
                "arithmetic": "exact integers and reduced rational pairs",
            },
            row_count=len(rows),
            claim_status=(
                "EXACT rows and center identities; coordinate-order summaries "
                "are bounded computations"
            ),
            schema_version=AFFINE_CENTER_SCHEMA_VERSION,
        )
        paths = write_experiment(rows, output_dir, "affine_center", manifest)
    return AffineCenterCensus(
        rows=rows,
        partition_counts=partition_counts,
        exact_inequalities=exact_inequality_report(states),
        coordinate_orders=coordinate_order_report(states),
        closest_to_critical=closest,
        paths=paths,
    )


def fraction_from_pair(pair: list[int] | tuple[int, int]) -> Fraction:
    """Public helper used by report consumers."""
    if len(pair) != 2:
        raise ValueError("fraction pair must have length two")
    return Fraction(pair[0], pair[1])
