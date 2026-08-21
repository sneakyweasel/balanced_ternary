"""Versioned schemas for reproducible Collatz dual-code experiments."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


SCHEMA_VERSION = "collatz-dual-code/v1"


@dataclass(frozen=True)
class ExperimentManifest:
    experiment_name: str
    parameters: dict[str, Any]
    row_count: int
    claim_status: str
    code_version: str = "working-tree"
    schema_version: str = SCHEMA_VERSION

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


REQUIRED_DUAL_FIELDS = frozenset(
    {
        "itinerary",
        "m",
        "K",
        "C",
        "residue",
        "modulus",
        "R",
        "lift_digits",
        "BT(R)",
        "budget_comparison",
        "zero_lift_flag",
        "status",
    }
)


def validate_dual_row(row: dict[str, Any]) -> None:
    missing = REQUIRED_DUAL_FIELDS.difference(row)
    if missing:
        raise ValueError(f"dual-code row missing fields: {sorted(missing)}")
    if row["m"] != len(row["itinerary"]):
        raise ValueError("row m does not match itinerary length")
    if len(row["lift_digits"]) != row["m"]:
        raise ValueError("lift digit count does not match m")
    if row["modulus"] != 1 << (row["K"] + 1):
        raise ValueError("row modulus does not equal 2^(K+1)")
    if row["residue"] != row["R"]:
        raise ValueError("Q=1 residue must equal canonical R")
