"""Versioned schemas for reproducible Collatz dual-code experiments."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


SCHEMA_VERSION = "collatz-dual-code/v1"
COMPATIBILITY_SCHEMA_VERSION = "collatz-compatibility/v1"
AFFINE_CENTER_SCHEMA_VERSION = "collatz-affine-center/v1"
BT_WARP_SCHEMA_VERSION = "collatz-bt-warp/v1"


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


REQUIRED_AFFINE_CENTER_FIELDS = frozenset(
    {
        "valuations",
        "m",
        "K",
        "C",
        "R",
        "X",
        "M",
        "two_power",
        "three_power",
        "gap",
        "n_star",
        "R_minus_n_star_raw",
        "X_minus_n_star_raw",
        "regime",
        "partition",
    }
)


def validate_affine_center_row(row: dict[str, Any]) -> None:
    """Validate exact integral and rational data in an affine-center row."""
    missing = REQUIRED_AFFINE_CENTER_FIELDS.difference(row)
    if missing:
        raise ValueError(f"affine-center row missing fields: {sorted(missing)}")
    validate_compatibility_row(row)
    if row["m"] < 1:
        raise ValueError("affine-center rows require a nonempty code")
    if row["two_power"] != 1 << row["K"]:
        raise ValueError("row two_power does not equal 2^K")
    if row["three_power"] != pow(3, row["m"]):
        raise ValueError("row three_power does not equal 3^m")
    if row["gap"] != row["two_power"] - row["three_power"] or row["gap"] == 0:
        raise ValueError("row gap must equal the nonzero value 2^K-3^m")
    if row["regime"] not in {"contracting", "expanding"}:
        raise ValueError("row regime must be contracting or expanding")
    if row["partition"] not in {"contracting", "critical-near", "expanding"}:
        raise ValueError("invalid affine-center partition")
    for field in ("n_star", "R_minus_n_star_raw", "X_minus_n_star_raw"):
        pair = row[field]
        if (
            not isinstance(pair, (list, tuple))
            or len(pair) != 2
            or any(isinstance(value, bool) or not isinstance(value, int) for value in pair)
            or pair[1] == 0
        ):
            raise ValueError(f"row {field} must be an integer numerator/denominator pair")


REQUIRED_BT_WARP_FIELDS = frozenset(
    {
        "n",
        "BT(n)",
        "W(n)",
        "BT(W(n))",
        "T(n)",
        "W(T(n))",
        "T(W(n))",
        "Comm_WT",
        "s3(n)",
        "s3(T(n))",
        "s3_alt(n)",
        "L3(n)",
        "L3(T(n))",
        "palindrome(n)",
        "palindrome(T(n))",
    }
)

REQUIRED_BT_WARP_CYLINDER_FIELDS = REQUIRED_BT_WARP_FIELDS | frozenset(
    {"itinerary", "R", "BT(R)", "W(R)", "next_k", "lift_digit"}
)


def validate_bt_warp_row(row: dict[str, Any], *, cylinder: bool = False) -> None:
    """Validate a collatz-bt-warp/v1 integer or cylinder row."""
    required = REQUIRED_BT_WARP_CYLINDER_FIELDS if cylinder else REQUIRED_BT_WARP_FIELDS
    missing = required.difference(row)
    if missing:
        raise ValueError(f"bt-warp row missing fields: {sorted(missing)}")
    if isinstance(row["n"], bool) or not isinstance(row["n"], int):
        raise ValueError("row n must be an integer")
    if row["T(n)"] is None:
        if row["W(T(n))"] is not None or row["palindrome(T(n))"] is not None:
            raise ValueError("undefined T(n) cannot have T-derived fields")
    elif isinstance(row["T(n)"], bool) or not isinstance(row["T(n)"], int):
        raise ValueError("row T(n) must be an integer or null")
    if row["T(W(n))"] is None:
        if row["Comm_WT"] is not None:
            raise ValueError("undefined T(W(n)) cannot have a commutator")
    elif row["Comm_WT"] != row["W(T(n))"] - row["T(W(n))"]:
        raise ValueError("row Comm_WT does not equal W(T(n))-T(W(n))")
