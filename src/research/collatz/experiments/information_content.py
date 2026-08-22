"""Deterministic information tests for exact and deliberately lossy states.

These routines test finite partitions; they do not estimate entropy and do
not use machine learning.  One conclusion is global, not experimental:
``S1=(m,K,R)`` determines the canonical balanced-ternary word and every
feature computed from it because balanced ternary is a function of ``R``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from itertools import product
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

from balanced_ternary.representation import encode
from research.collatz.compatibility import ExponentCodeDiagnostic
from research.collatz.cylinders import parse_ks
from research.collatz.dual_code import lift_digit_formula
from research.collatz.experiments.schema import (
    COMPATIBILITY_SCHEMA_VERSION,
    ExperimentManifest,
    validate_compatibility_row,
)
from research.collatz.experiments.table_io import write_experiment
from research.collatz.features import features_of_int
from research.collatz.zero_lift import zero_lift_k


STATE_FIELDS: dict[str, tuple[str, ...]] = {
    "S0": ("m", "K"),
    "S1": ("m", "K", "R"),
    "S2": ("m", "K", "R", "M"),
    "S3": ("m", "K", "R", "M", "C"),
}
S1_BT_THEOREM = (
    "PROVED: S1=(m,K,R) determines BT(R) and every deterministic BT(R) feature."
)
CODE_DETERMINISM_THEOREM = (
    "PROVED: the full exponent code determines S0-S3 and BT(R)."
)
FINITE_PARTITION_LABEL = "VERIFIED COMPUTATIONALLY on the recorded finite sample"


def _mapping(value: object) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    method = getattr(value, "as_dict", None)
    if callable(method):
        return dict(method())
    if is_dataclass(value):
        return asdict(value)
    raise TypeError("diagnostic must be a mapping, dataclass, or expose as_dict()")


def _first(data: Mapping[str, Any], *names: str) -> Any:
    for name in names:
        if name in data:
            return data[name]
    raise KeyError(f"none of {names!r} appears in diagnostic")


def diagnostic_row(
    valuations: tuple[int, ...] | list[int] | str,
    *,
    proposed_k_max: int = 4,
) -> dict[str, Any]:
    """Return a normalized, JSON-safe compatibility row."""
    ks = parse_ks(valuations)
    if (
        isinstance(proposed_k_max, bool)
        or not isinstance(proposed_k_max, int)
        or proposed_k_max < 1
    ):
        raise ValueError("proposed_k_max must be an integer >= 1")
    diagnostic = ExponentCodeDiagnostic.from_valuations(ks)
    raw = _mapping(diagnostic)
    r = int(_first(raw, "R", "realizer", "refined_R"))
    m = int(raw.get("m", len(ks)))
    K = int(raw.get("K", sum(ks)))
    C = int(_first(raw, "C", "affine_constant"))
    M = int(_first(raw, "M", "endpoint_M", "endpoint"))
    bt = str(raw.get("BT(R)", raw.get("bt_R", raw.get("balanced_ternary_R", encode(r)))))
    feature_dict = _json_safe(features_of_int(r).as_dict())
    lifts = raw.get("lift_digits", raw.get("lifts", ()))
    row: dict[str, Any] = {
        "valuations": list(ks),
        "m": m,
        "K": K,
        "C": C,
        "R": r,
        "M": M,
        "BT(R)": bt,
        "bt_features": feature_dict,
        "lift_digits": list(lifts),
        "next_zero_lift_k": zero_lift_k(ks),
        "proposed_lift_digits": [
            lift_digit_formula(ks, k) for k in range(1, proposed_k_max + 1)
        ],
        "exact_drift_numerator": pow(3, m),
        "exact_drift_denominator": 1 << K,
        "claim_status": "EXACT row; floating fields, if present, are estimates",
    }
    for name in ("r", "d", "rho_r", "rho_M"):
        if name in raw:
            row[name] = raw[name]
    validate_compatibility_row(row)
    return row


def state_key(row: Mapping[str, Any], state: str) -> tuple[Any, ...]:
    """Project a row to one of the exact states S0--S3."""
    try:
        fields = STATE_FIELDS[state.upper()]
    except KeyError as exc:
        raise ValueError(f"state must be one of {tuple(STATE_FIELDS)}, got {state!r}") from exc
    return tuple(row[field] for field in fields)


def partition_rows(
    rows: Iterable[Mapping[str, Any]], state: str
) -> dict[tuple[Any, ...], list[dict[str, Any]]]:
    partitions: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    for original in rows:
        row = dict(original)
        partitions.setdefault(state_key(row, state), []).append(row)
    return partitions


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return tuple(sorted((key, _freeze(item)) for key, item in value.items()))
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    return value


def _json_safe(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    return value


def smallest_collision_witness(
    rows: Iterable[Mapping[str, Any]],
    state: str,
    observable: str | Callable[[Mapping[str, Any]], Any],
) -> dict[str, Any] | None:
    """Return the lexicographically smallest state collision, if one exists."""
    get_value = (
        observable
        if callable(observable)
        else lambda row: row[observable]  # noqa: E731 - compact selector
    )
    candidates: list[dict[str, Any]] = []
    for key, group in partition_rows(rows, state).items():
        by_value: dict[Any, dict[str, Any]] = {}
        for row in group:
            by_value.setdefault(_freeze(get_value(row)), row)
        if len(by_value) > 1:
            representatives = sorted(
                by_value.values(),
                key=lambda row: (
                    row["m"],
                    row["K"],
                    tuple(row["valuations"]),
                ),
            )
            candidates.append(
                {
                    "state": state.upper(),
                    "state_key": list(key),
                    "observable": observable if isinstance(observable, str) else "callable",
                    "row_a": representatives[0],
                    "row_b": representatives[1],
                    "status": FINITE_PARTITION_LABEL,
                }
            )
    if not candidates:
        return None
    return min(
        candidates,
        key=lambda item: (
            item["row_b"]["m"],
            item["row_b"]["K"],
            tuple(item["row_a"]["valuations"]),
            tuple(item["row_b"]["valuations"]),
        ),
    )


def determinism_report(
    rows: Sequence[Mapping[str, Any]],
    observable: str = "BT(R)",
) -> dict[str, Any]:
    """Test whether each S0--S3 cell has one observed output value."""
    states: dict[str, Any] = {}
    for state in STATE_FIELDS:
        witness = smallest_collision_witness(rows, state, observable)
        states[state] = {
            "determines_on_sample": witness is None,
            "smallest_collision": witness,
            "status": S1_BT_THEOREM if state in {"S1", "S2", "S3"} and observable in {
                "BT(R)",
                "bt_features",
            } else FINITE_PARTITION_LABEL,
        }
    return {
        "observable": observable,
        "states": states,
        "theorems": [S1_BT_THEOREM, CODE_DETERMINISM_THEOREM],
        "scope": "Exact determinism for S1+ and BT(R); other results are finite partition tests.",
    }


def balanced_ternary_collision_witness(
    rows: Iterable[Mapping[str, Any]],
    observable: str,
) -> dict[str, Any] | None:
    """Smallest witness that the full BT word alone does not determine an output."""
    by_word: dict[str, dict[Any, dict[str, Any]]] = {}
    for original in rows:
        row = dict(original)
        word = str(row["BT(R)"])
        by_word.setdefault(word, {}).setdefault(_freeze(row[observable]), row)
    candidates: list[dict[str, Any]] = []
    for word, by_value in by_word.items():
        if len(by_value) < 2:
            continue
        representatives = sorted(
            by_value.values(),
            key=lambda row: (row["m"], row["K"], tuple(row["valuations"])),
        )
        candidates.append(
            {
                "BT(R)": word,
                "observable": observable,
                "row_a": representatives[0],
                "row_b": representatives[1],
                "status": "EXACT COLLISION WITNESS",
            }
        )
    if not candidates:
        return None
    return min(
        candidates,
        key=lambda item: (
            item["row_b"]["m"],
            item["row_b"]["K"],
            tuple(item["row_a"]["valuations"]),
            tuple(item["row_b"]["valuations"]),
        ),
    )


def truncated_state_collision_analysis(
    rows: Sequence[Mapping[str, Any]],
    precision: int,
    observable: str = "lift_digits",
) -> dict[str, Any]:
    """Find collisions after replacing exact ``R`` by ``R mod 2^precision``."""
    if isinstance(precision, bool) or not isinstance(precision, int) or precision < 1:
        raise ValueError("precision must be an integer >= 1")
    transformed: list[dict[str, Any]] = []
    mask = (1 << precision) - 1
    for original in rows:
        row = dict(original)
        row["R"] = int(row["R"]) & mask
        transformed.append(row)
    witness = smallest_collision_witness(transformed, "S1", observable)
    return {
        "precision": precision,
        "truncated_state": ("m", "K", f"R mod 2^{precision}"),
        "observable": observable,
        "collision_found": witness is not None,
        "smallest_collision": witness,
        "status": FINITE_PARTITION_LABEL,
        "caution": "A collision diagnoses this lossy state only, not exact S1.",
    }


@dataclass(frozen=True)
class InformationContentResult:
    rows: tuple[dict[str, Any], ...]
    reports: dict[str, dict[str, Any]]
    balanced_ternary_collisions: dict[str, dict[str, Any] | None]
    truncated: tuple[dict[str, Any], ...]
    paths: dict[str, str]
    schema_version: str = COMPATIBILITY_SCHEMA_VERSION


def run_information_content(
    max_length: int,
    max_k: int,
    *,
    precisions: Sequence[int] = (1, 2, 3, 4),
    output_dir: Path | str | None = None,
) -> InformationContentResult:
    """Exhaustively run deterministic finite partition tests."""
    if isinstance(max_length, bool) or not isinstance(max_length, int) or max_length < 1:
        raise ValueError("max_length must be an integer >= 1")
    if isinstance(max_k, bool) or not isinstance(max_k, int) or max_k < 1:
        raise ValueError("max_k must be an integer >= 1")
    codes = (
        ks
        for length in range(1, max_length + 1)
        for ks in product(range(1, max_k + 1), repeat=length)
    )
    rows = tuple(diagnostic_row(ks, proposed_k_max=max_k) for ks in codes)
    reports = {
        observable: determinism_report(rows, observable)
        for observable in ("BT(R)", "bt_features", "lift_digits")
    }
    balanced_ternary_collisions = {
        observable: balanced_ternary_collision_witness(rows, observable)
        for observable in ("next_zero_lift_k", "proposed_lift_digits")
    }
    truncated = tuple(
        truncated_state_collision_analysis(rows, precision) for precision in precisions
    )
    paths: dict[str, str] = {}
    if output_dir is not None:
        manifest = ExperimentManifest(
            experiment_name="compatibility_information_content",
            parameters={
                "max_length": max_length,
                "max_k": max_k,
                "precisions": list(precisions),
                "enumeration": "lexicographic exhaustive product",
            },
            row_count=len(rows),
            claim_status=(
                f"{S1_BT_THEOREM} Other partition/collision results are "
                f"{FINITE_PARTITION_LABEL}."
            ),
            schema_version=COMPATIBILITY_SCHEMA_VERSION,
        )
        paths = write_experiment(rows, output_dir, "compatibility_information", manifest)
    return InformationContentResult(
        rows, reports, balanced_ternary_collisions, truncated, paths
    )
