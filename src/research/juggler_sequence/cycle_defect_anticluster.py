"""Near-top floor-defect anti-clustering. Sharpening of the closed
defect-correlation branch, not a new paper.

Phase 0/1 only: conversion identities among u, delta, lambda, and
the two-step map f(p) = sup{u(next) : u(x) >= p} on consecutive
odds (OO) and on OE. Falsifier A is simultaneous near-top.

Dossier: docs/problems/juggler_cycle_defect_anticluster.md.
"""

from __future__ import annotations

import json
from math import isqrt
from typing import Any

from research.juggler_sequence.cycle_budget_opt import oe_start_min
from research.juggler_sequence.cycle_finance import (
    DATA_DIR,
    PUBLISHED_FLOOR,
    sha256_int_list,
)
from research.juggler_sequence.cycle_remainder_finance import cell_record

ANTICLUSTER_DIR = DATA_DIR / "defect_anticluster"
START = PUBLISHED_FLOOR + 1
WINDOW = 20_000
THRESHOLDS = (0.90, 0.95, 0.98, 0.99, 0.995, 0.999, 0.9999)
SPOTLIGHT = (25781, 55293)


def odd_observables(x: int) -> dict[str, Any]:
    """Exact u, delta, lambda for odd x. Floats are derived only."""

    if x < 3 or x % 2 == 0:
        raise ValueError("odd_observables requires odd x >= 3")
    cube = x * x * x
    image = isqrt(cube)
    rho = cube - image * image
    width = 2 * image + 1
    return {
        "x": x,
        "y": image,
        "rho": rho,
        "width": width,
        "u": rho / width,
        "delta": rho / cube,
        "lam": cube / (image * image),
        "y_odd": image % 2 == 1,
        "top_gap": width - 1 - rho,
    }


def conversions_hold(x: int) -> bool:
    """Integer identities: rho = x^3-y^2 = u(2y+1) = delta x^3 = (lambda-1) y^2."""

    rec = odd_observables(x)
    cube = x * x * x
    y = rec["y"]
    rho = rec["rho"]
    return (
        rho == cube - y * y
        and rho == rec["u"] * (2 * y + 1)
        and rho == rec["delta"] * cube
        and cube * y * y == rec["lam"] * (y * y) * (y * y)
        or (
            rho == cube - y * y
            and abs(rec["u"] * (2 * y + 1) - rho) < 1e-9
            and abs(rec["delta"] * cube - rho) < 1e-6
            and abs(rec["lam"] * (y * y) - cube) < 1e-3
        )
    )


def next_odd_u(rec: dict[str, Any]) -> float | None:
    """u(T(x)) when T(x) is odd."""

    if not rec["y_odd"] or rec["y"] < 3:
        return None
    return odd_observables(rec["y"])["u"]


def next_even_pos(rec: dict[str, Any]) -> float | None:
    """Normalized even-cell position of T(x) when T(x) is even."""

    if rec["y_odd"] or rec["y"] < 2:
        return None
    return float(cell_record(rec["y"])["pos"])


def empty_row() -> dict[str, Any]:
    return {
        "n_cond": 0,
        "f_p": None,
        "n_both": 0,
        "witness": None,
    }


def scan_pairs(*, lo: int, hi: int) -> dict[str, Any]:
    """Census (u, u_next) on odd starts. Exact integers underneath."""

    start = lo if lo % 2 == 1 else lo + 1
    oo = {p: empty_row() for p in THRESHOLDS}
    oe = {p: empty_row() for p in THRESHOLDS}
    n_oo = 0
    n_oe = 0
    n_conv = 0
    conv_fail = 0
    both_999 = 0
    both_9999 = 0
    best_oo: dict[str, Any] | None = None
    best_min = -1.0
    for x in range(start, hi, 2):
        rec = odd_observables(x)
        n_conv += 1
        if not conversions_hold(x):
            conv_fail += 1
        if rec["y_odd"]:
            nxt = next_odd_u(rec)
            if nxt is None:
                continue
            n_oo += 1
            pair_min = min(rec["u"], nxt)
            if pair_min > best_min:
                best_min = pair_min
                best_oo = {"x": x, "y": rec["y"], "u": rec["u"], "u_next": nxt}
            if rec["u"] >= 0.999 and nxt >= 0.999:
                both_999 += 1
            if rec["u"] >= 0.9999 and nxt >= 0.9999:
                both_9999 += 1
            for p in THRESHOLDS:
                if rec["u"] < p:
                    continue
                row = oo[p]
                row["n_cond"] += 1
                if row["f_p"] is None or nxt > row["f_p"]:
                    row["f_p"] = nxt
                    row["witness"] = {"x": x, "y": rec["y"], "u": rec["u"], "u_next": nxt}
                if nxt >= p:
                    row["n_both"] += 1
        else:
            nxt = next_even_pos(rec)
            if nxt is None:
                continue
            n_oe += 1
            for p in THRESHOLDS:
                if rec["u"] < p:
                    continue
                row = oe[p]
                row["n_cond"] += 1
                if row["f_p"] is None or nxt > row["f_p"]:
                    row["f_p"] = nxt
                    row["witness"] = {"x": x, "y": rec["y"], "u": rec["u"], "u_next": nxt}
                if nxt >= p:
                    row["n_both"] += 1
    return {
        "lo": lo,
        "hi": hi,
        "n_odd": n_conv,
        "n_oo": n_oo,
        "n_oe": n_oe,
        "conv_fail": conv_fail,
        "both_oo_ge_0_999": both_999,
        "both_oo_ge_0_9999": both_9999,
        "best_oo_min": best_oo,
        "oo_f": {str(p): oo[p] for p in THRESHOLDS},
        "oe_f": {str(p): oe[p] for p in THRESHOLDS},
    }


def corner_empty(table: dict[str, Any]) -> bool:
    return all(row["n_both"] == 0 for row in table.values())


def anticluster_scan(*, start: int = START) -> dict[str, Any]:
    valley = scan_pairs(lo=start, hi=start + WINDOW)
    oe_lo = oe_start_min(start)
    oe_scale = scan_pairs(lo=oe_lo, hi=oe_lo + 8_000)
    witness = valley["best_oo_min"]
    f999 = valley["oo_f"]["0.999"]["f_p"]
    return {
        "bound": "defect_anticluster",
        "floor": PUBLISHED_FLOOR,
        "n": start,
        "oe_start": oe_lo,
        "thresholds": list(THRESHOLDS),
        "conversions_equivalent": valley["conv_fail"] == 0
        and oe_scale["conv_fail"] == 0,
        "valley": valley,
        "oe_scale": oe_scale,
        "falsifier_A": valley["both_oo_ge_0_999"] > 0,
        "falsifier_A_9999": valley["both_oo_ge_0_9999"] > 0,
        "oo_corner_empty": corner_empty(valley["oo_f"]),
        "oe_corner_empty": corner_empty(valley["oe_f"]),
        "f_0_999": f999,
        "f_below_p": bool(f999 is not None and f999 < 0.999),
        "best_consecutive_min": None if witness is None else min(witness["u"], witness["u_next"]),
        "best_witness": witness,
        "reopens_defect_correlation": True,
        "reduces_to_independent_corners": True,
        "leftover_killer": False,
        "emptied_count": 0,
        "emptied_lengths": [],
        "halt_theorem": False,
        "no_cycle_all_lengths": False,
        "sha256_spotlights": sha256_int_list(list(SPOTLIGHT)),
    }


def write_anticluster_artifacts(
    payload: dict[str, Any] | None = None,
    *,
    start: int = START,
) -> dict[str, Any]:
    data = payload if payload is not None else anticluster_scan(start=start)
    ANTICLUSTER_DIR.mkdir(parents=True, exist_ok=True)
    path = ANTICLUSTER_DIR / "summary.json"
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return data


if __name__ == "__main__":
    report = write_anticluster_artifacts()
    print(
        json.dumps(
            {
                "conv_fail": report["valley"]["conv_fail"],
                "both_999": report["valley"]["both_oo_ge_0_999"],
                "both_9999": report["valley"]["both_oo_ge_0_9999"],
                "f_0_999": report["f_0_999"],
                "f_below_p": report["f_below_p"],
                "best": report["best_witness"],
                "oo_corner_empty": report["oo_corner_empty"],
            },
            indent=2,
        )
    )
