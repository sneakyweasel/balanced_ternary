"""Versioned schemas for reproducible Collatz dual-code experiments."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


SCHEMA_VERSION = "collatz-dual-code/v1"
COMPATIBILITY_SCHEMA_VERSION = "collatz-compatibility/v1"


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


REQUIRED_COMPATIBILITY_FIELDS = frozenset({"valuations", "m", "K", "C", "R", "M"})


def validate_compatibility_row(row: dict[str, Any]) -> None:
    """Validate the stable exact core of a compatibility experiment row.

    Additional balanced-ternary, lift, rate, provenance, and estimate fields
    are deliberately allowed so the v1 schema remains forward compatible.
    """
    missing = REQUIRED_COMPATIBILITY_FIELDS.difference(row)
    if missing:
        raise ValueError(f"compatibility row missing fields: {sorted(missing)}")
    valuations = row["valuations"]
    if not isinstance(valuations, (list, tuple)):
        raise ValueError("row valuations must be a list or tuple")
    if row["m"] != len(valuations):
        raise ValueError("row m does not match valuation length")
    if any(isinstance(k, bool) or not isinstance(k, int) or k < 1 for k in valuations):
        raise ValueError("row valuations must be integers >= 1")
    if row["K"] != sum(valuations):
        raise ValueError("row K does not equal the valuation sum")
    if any(isinstance(row[name], bool) or not isinstance(row[name], int) for name in ("C", "R", "M")):
        raise ValueError("row C, R, and M must be integers")
    if row["R"] < 1:
        raise ValueError("row R must be positive")
    if row["m"] == 0:
        if row["C"] != 0:
            raise ValueError("empty valuation word must have C=0")
    elif not 1 <= row["M"] <= pow(3, row["m"]):
        raise ValueError("nonempty row M must be the least positive residue modulo 3^m")
