"""Finance-weighted floor-remainder control on E_run leftovers.

Not a halt theorem, not a leftover-word census, not a new period
identity, not Fourier, and not a residue system. Phase 0 asks
whether CycleMin-legal square/cube-cell positions are forced away
from the top often enough to shrink the run-type budget.

The published 6/5 cell bound is the top-of-cell case log z <=
2 log(y+1). Normalized position pos = rho / (2 T + 1) is the
usable fraction of that bound. Finance is paid at odd valleys;
even terms sit at n^2 and do not move E_run(10^6).

Dossier: docs/problems/juggler_cycle_remainder_finance.md.
"""

from __future__ import annotations

import json
import math
from math import isqrt
from typing import Any

from research.juggler_sequence.cycle_budget_opt import (
    budget_rhs,
    oe_start_min,
    run_type_counts,
)
from research.juggler_sequence.cycle_finance import (
    DATA_DIR,
    EPS_CONST,
    PUBLISHED_FLOOR,
    o_min_and_theta,
    sha256_int_list,
)

REMAINDER_DIR = DATA_DIR / "remainder_finance"
SPOTLIGHT = (25781, 55293)
START = PUBLISHED_FLOOR + 1
VALLEY_WINDOW = 20_000
OE_WINDOW = 8_000
NEAR_TOP = 0.99
KILL_FACTOR_55293 = 0.988


def cell_record(x: int) -> dict[str, Any]:
    """Normalized position of x in its exact square or cube cell."""

    if x < 2:
        raise ValueError("cell_record requires x >= 2")
    odd = x % 2 == 1
    power = x * x * x if odd else x
    image = isqrt(power)
    rho = power - image * image
    width = 2 * image + 1
    pos = rho / width
    top_gap = width - 1 - rho
    usable = 0.0
    if image >= 1:
        bound = 2.0 * math.log1p(1.0 / image)
        if bound > 0.0:
            usable = math.log1p(rho / (image * image)) / bound
    return {
        "x": x,
        "odd": odd,
        "image": image,
        "rho": rho,
        "width": width,
        "pos": pos,
        "top_gap": top_gap,
        "usable": usable,
        "image_odd": image % 2 == 1,
    }


def ooe_legal(rec: dict[str, Any]) -> bool:
    return rec["odd"] and rec["image_odd"]


def oe_legal(rec: dict[str, Any]) -> bool:
    return rec["odd"] and not rec["image_odd"]


def even_image_record(odd_rec: dict[str, Any]) -> dict[str, Any] | None:
    """Cell position of the even landing after an odd step."""

    image = odd_rec["image"]
    if image < 2 or image % 2 == 1:
        return None
    return cell_record(image)


def scan_odds(lo: int, hi: int) -> dict[str, Any]:
    start = lo if lo % 2 == 1 else lo + 1
    n_odd = 0
    n_ooe = 0
    n_oe = 0
    odd_pos = 0.0
    ooe_pos = 0.0
    oe_pos = 0.0
    odd_usable = 0.0
    ooe_usable = 0.0
    max_odd = 0.0
    max_ooe = 0.0
    max_oe = 0.0
    max_even = 0.0
    min_top = 10**9
    min_ooe_top = 10**9
    n_odd_near = 0
    n_ooe_near = 0
    n_oe_near = 0
    n_ooe_kill = 0
    n_even_near = 0
    n_ooe_top1 = 0
    n_ooe_top5 = 0
    best_ooe: dict[str, Any] | None = None
    for x in range(start, hi, 2):
        rec = cell_record(x)
        n_odd += 1
        odd_pos += rec["pos"]
        odd_usable += rec["usable"]
        max_odd = max(max_odd, rec["pos"])
        min_top = min(min_top, rec["top_gap"])
        if rec["pos"] >= NEAR_TOP:
            n_odd_near += 1
        if ooe_legal(rec):
            n_ooe += 1
            ooe_pos += rec["pos"]
            ooe_usable += rec["usable"]
            max_ooe = max(max_ooe, rec["pos"])
            min_ooe_top = min(min_ooe_top, rec["top_gap"])
            if rec["pos"] >= NEAR_TOP:
                n_ooe_near += 1
            if rec["pos"] >= KILL_FACTOR_55293:
                n_ooe_kill += 1
            if rec["top_gap"] <= 1:
                n_ooe_top1 += 1
            if rec["top_gap"] <= 5:
                n_ooe_top5 += 1
            if best_ooe is None or rec["pos"] > best_ooe["pos"]:
                best_ooe = rec
        if oe_legal(rec):
            n_oe += 1
            oe_pos += rec["pos"]
            max_oe = max(max_oe, rec["pos"])
            if rec["pos"] >= NEAR_TOP:
                n_oe_near += 1
            even = even_image_record(rec)
            if even is not None:
                max_even = max(max_even, even["pos"])
                if even["pos"] >= NEAR_TOP:
                    n_even_near += 1
    return {
        "lo": lo,
        "hi": hi,
        "n_odd": n_odd,
        "n_ooe": n_ooe,
        "n_oe": n_oe,
        "mean_odd_pos": odd_pos / n_odd if n_odd else None,
        "mean_ooe_pos": ooe_pos / n_ooe if n_ooe else None,
        "mean_oe_pos": oe_pos / n_oe if n_oe else None,
        "mean_odd_usable": odd_usable / n_odd if n_odd else None,
        "mean_ooe_usable": ooe_usable / n_ooe if n_ooe else None,
        "max_odd_pos": max_odd,
        "max_ooe_pos": max_ooe,
        "max_oe_pos": max_oe,
        "max_even_landing_pos": max_even,
        "min_top_gap": min_top if n_odd else None,
        "min_ooe_top_gap": min_ooe_top if n_ooe else None,
        "n_odd_near_top": n_odd_near,
        "n_ooe_near_top": n_ooe_near,
        "n_oe_near_top": n_oe_near,
        "n_ooe_above_kill_factor": n_ooe_kill,
        "n_even_landing_near_top": n_even_near,
        "n_ooe_top_gap_le_1": n_ooe_top1,
        "n_ooe_top_gap_le_5": n_ooe_top5,
        "best_ooe": best_ooe,
    }


def load_run_rows() -> list[dict[str, Any]]:
    payload = json.loads((DATA_DIR / "budget_opt.json").read_text(encoding="utf-8"))
    return [row for row in payload["rows"] if not row["budget_excludes"]]


def factor_kill(factor: float, rows: list[dict[str, Any]]) -> list[int]:
    killed = []
    for row in rows:
        packed = row["budget_rhs"]
        if row["theta"] > packed * factor * (1.0 + 1e-12):
            killed.append(row["L"])
    return killed


def spotlight_margin(length: int, n: int) -> dict[str, Any]:
    odd_count, theta = o_min_and_theta(length)
    packed = budget_rhs(n, length, odd_count)
    oo_count, oe_count = run_type_counts(odd_count, length - odd_count)
    return {
        "L": length,
        "o": odd_count,
        "theta": theta,
        "budget_rhs": packed,
        "ratio": packed / theta if theta else None,
        "need_factor": theta / packed if packed else None,
        "oo_count": oo_count,
        "oe_count": oe_count,
    }


def remainder_scan(*, start: int = START) -> dict[str, Any]:
    n = start
    valley = scan_odds(n, n + VALLEY_WINDOW)
    oe_lo = oe_start_min(n)
    oe_scale = scan_odds(oe_lo, oe_lo + OE_WINDOW)
    rows = load_run_rows()
    mean_factor = valley["mean_ooe_usable"] or 0.5
    max_factor = valley["max_ooe_pos"]
    killed_mean = factor_kill(mean_factor, rows)
    killed_max = factor_kill(max_factor, rows)
    killed_99 = factor_kill(NEAR_TOP, rows)
    killed_988 = factor_kill(KILL_FACTOR_55293, rows)
    spots = {str(length): spotlight_margin(length, n) for length in SPOTLIGHT}
    need_55293 = spots["55293"]["need_factor"]
    unrestricted = (
        valley["max_ooe_pos"] >= KILL_FACTOR_55293
        and valley["n_ooe_above_kill_factor"] > 0
        and oe_scale["max_oe_pos"] >= NEAR_TOP
    )
    return {
        "bound": "remainder_finance",
        "floor": PUBLISHED_FLOOR,
        "n": n,
        "oe_start": oe_lo,
        "const": EPS_CONST,
        "valley": valley,
        "oe_scale": oe_scale,
        "spotlights": spots,
        "n_run_survivors": len(rows),
        "mean_ooe_usable": mean_factor,
        "max_ooe_pos": max_factor,
        "killed_by_mean_usable": killed_mean,
        "killed_count_mean": len(killed_mean),
        "killed_by_max_pos": killed_max,
        "killed_count_max": len(killed_max),
        "killed_by_0_99": killed_99,
        "killed_by_0_988": killed_988,
        "need_factor_55293": need_55293,
        "uniform_bound_kills_55293": bool(killed_988),
        "near_top_ooe_exists": valley["n_ooe_near_top"] > 0,
        "near_top_oe_exists": oe_scale["n_oe_near_top"] > 0
        or valley["n_oe_near_top"] > 0,
        "top_gap_one_exists": valley["n_ooe_top_gap_le_1"] > 0,
        "even_landing_near_top": valley["n_even_landing_near_top"] > 0
        or oe_scale["n_even_landing_near_top"] > 0,
        "remainders_unrestricted": unrestricted,
        "mean_is_not_a_theorem": True,
        "reduces_to_top_of_cell_bound": True,
        "leftover_killer": False,
        "emptied_count": 0,
        "emptied_lengths": [],
        "halt_theorem": False,
        "no_cycle_all_lengths": False,
        "sha256_spotlights": sha256_int_list(list(SPOTLIGHT)),
    }


def write_remainder_artifacts(
    payload: dict[str, Any] | None = None,
    *,
    start: int = START,
) -> dict[str, Any]:
    data = payload if payload is not None else remainder_scan(start=start)
    REMAINDER_DIR.mkdir(parents=True, exist_ok=True)
    slim = dict(data)
    for key in ("valley", "oe_scale"):
        rec = dict(slim[key])
        best = rec.get("best_ooe")
        if best is not None:
            rec["best_ooe"] = {
                "x": best["x"],
                "pos": best["pos"],
                "top_gap": best["top_gap"],
                "usable": best["usable"],
                "image": best["image"],
            }
        slim[key] = rec
    path = REMAINDER_DIR / "summary.json"
    path.write_text(json.dumps(slim, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return data


if __name__ == "__main__":
    report = write_remainder_artifacts()
    print(
        json.dumps(
            {
                "max_ooe_pos": report["max_ooe_pos"],
                "mean_ooe_usable": report["mean_ooe_usable"],
                "n_ooe_near_top": report["valley"]["n_ooe_near_top"],
                "n_ooe_above_kill": report["valley"]["n_ooe_above_kill_factor"],
                "min_ooe_top_gap": report["valley"]["min_ooe_top_gap"],
                "max_oe_pos": report["oe_scale"]["max_oe_pos"],
                "killed_mean": report["killed_count_mean"],
                "killed_max": report["killed_count_max"],
                "unrestricted": report["remainders_unrestricted"],
                "need_55293": report["need_factor_55293"],
            },
            indent=2,
        )
    )
