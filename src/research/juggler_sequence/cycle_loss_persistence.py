"""Cross-excursion usable-loss persistence on E_run leftovers.

Not a halt theorem, not a leftover-word census, not a new period
identity, not Fourier, and not a residue system. Phase 0 asks
whether large usable odd-run floor loss can occur at successive
finance-critical odd valleys, or whether a two-excursion tax
appears after finance weighting.

One-step near-top remainders and consecutive-letter cell corners
are already unrestricted (remainder_finance, defect_correlation).
This probe records the joint signature (R_0, R_1) of two
consecutive odd-run blocks v --O^a E--> v' --O^b E--> v''.

Dossier: docs/problems/juggler_cycle_loss_persistence.md.
"""

from __future__ import annotations

import json
import math
from math import isqrt, log, log1p
from typing import Any

from research.juggler_sequence.cycle_budget_opt import (
    budget_rhs,
    oe_start_min,
)
from research.juggler_sequence.cycle_finance import (
    DATA_DIR,
    PUBLISHED_FLOOR,
    o_min_and_theta,
    sha256_int_list,
)
SPOTLIGHT = (25781, 55293)
START = PUBLISHED_FLOOR + 1
VALLEY_WINDOW = 20_000
OE_WINDOW = 8_000
A_CAP = 16
EVEN_CAP = 32
THRESHOLDS = (0.9, 0.95, 0.99, 0.999)
NEAR = 0.99
PERSISTENCE_DIR = DATA_DIR / "loss_persistence"


def _ratio(num: int, den: int) -> float:
    """True division that stays inside float range for huge integers."""

    if den == 0:
        return 0.0
    shift = max(num.bit_length(), den.bit_length()) - 900
    if shift > 0:
        num >>= shift
        den >>= shift
        if den == 0:
            return 0.0
    return num / den


def _log_int(n: int) -> float:
    if n <= 0:
        raise ValueError("log is defined on positive integers")
    bits = n.bit_length()
    if bits <= 900:
        return log(n)
    shift = bits - 900
    return log(n >> shift) + shift * log(2)


def _log1p_frac(num: int, den: int) -> float:
    """log(1 + num/den) for nonnegative integers."""

    if num <= 0 or den <= 0:
        return 0.0
    if num.bit_length() + 20 < den.bit_length():
        return log1p(_ratio(num, den))
    return _log_int(den + num) - _log_int(den)


def odd_loss(x: int) -> dict[str, Any]:
    """Normalized cell position and usable odd-step logarithm at odd x."""

    if x < 1 or x % 2 == 0:
        raise ValueError("odd_loss requires an odd positive integer")
    y = isqrt(x * x * x)
    rho = x * x * x - y * y
    width = 2 * y + 1
    pos = _ratio(rho, width) if width else 0.0
    eps = 0.5 * _log1p_frac(rho, y * y) if y else 0.0
    eps_max = 0.5 * _log1p_frac(2 * y, y * y) if y else 0.0
    usable = eps / eps_max if eps_max > 0.0 else 0.0
    if x >= 3:
        logx = _log_int(x)
        weight = math.exp(-logx - log(logx)) if logx > 0.0 else 0.0
    else:
        weight = 0.0
    return {
        "x": x,
        "y": y,
        "rho": rho,
        "pos": pos,
        "eps": eps,
        "eps_max": eps_max,
        "usable": usable,
        "weight": weight,
        "eps_w": eps * weight,
        "eps_w_max": eps_max * weight,
    }


def next_odd_valley(landing: int, *, cap: int = EVEN_CAP) -> tuple[int, int] | None:
    """First odd state on or after a block-map landing."""

    current = landing
    skipped = 0
    while current >= 2 and current % 2 == 0 and skipped < cap:
        current = isqrt(current)
        skipped += 1
    if current < 3 or current % 2 == 0:
        return None
    return current, skipped


def excursion_score(v: int, *, cap: int = A_CAP) -> dict[str, Any] | None:
    """Odd-run block loss from valley v through the closing even step."""

    if v < 3 or v % 2 == 0:
        return None
    odds: list[dict[str, Any]] = []
    current = v
    for _ in range(cap):
        if current % 2 == 0:
            break
        rec = odd_loss(current)
        odds.append(rec)
        current = rec["y"]
    if not odds or current % 2 == 1:
        return None
    landing = isqrt(current)
    r_sum = sum(row["eps"] for row in odds)
    r_max = sum(row["eps_max"] for row in odds)
    w_sum = sum(row["eps_w"] for row in odds)
    w_max = sum(row["eps_w_max"] for row in odds)
    first = odds[0]
    return {
        "v": v,
        "a": len(odds),
        "peak": current,
        "landing": landing,
        "p": first["pos"],
        "u": first["usable"],
        "R": r_sum,
        "R_max": r_max,
        "U": r_sum / r_max if r_max > 0.0 else 0.0,
        "W": w_sum,
        "W_max": w_max,
        "Uw": w_sum / w_max if w_max > 0.0 else 0.0,
        "odds": odds,
    }


def pair_record(x: int) -> dict[str, Any] | None:
    """Two consecutive odd-run signatures starting at odd x."""

    first = excursion_score(x)
    if first is None:
        return None
    nxt = next_odd_valley(first["landing"])
    if nxt is None:
        return None
    v1, n_even = nxt
    second = excursion_score(v1)
    if second is None:
        return None
    return {
        "x": x,
        "a0": first["a"],
        "p0": first["p"],
        "u0": first["u"],
        "R0": first["R"],
        "R0_max": first["R_max"],
        "U0": first["U"],
        "W0": first["W"],
        "W0_max": first["W_max"],
        "Uw0": first["Uw"],
        "v1": v1,
        "n_even": n_even,
        "a1": second["a"],
        "p1": second["p"],
        "u1": second["u"],
        "R1": second["R"],
        "R1_max": second["R_max"],
        "U1": second["U"],
        "W1": second["W"],
        "W1_max": second["W_max"],
        "Uw1": second["Uw"],
        "Rsum": first["R"] + second["R"],
        "Rsum_max": first["R_max"] + second["R_max"],
        "Wsum": first["W"] + second["W"],
        "Wsum_max": first["W_max"] + second["W_max"],
        "growth": _ratio(v1, x) if x else None,
        "within": [
            (first["odds"][i]["pos"], first["odds"][i + 1]["pos"])
            for i in range(len(first["odds"]) - 1)
        ],
        "within_u": [
            (first["odds"][i]["usable"], first["odds"][i + 1]["usable"])
            for i in range(len(first["odds"]) - 1)
        ],
    }


def run_class(a: int) -> str:
    if a == 1:
        return "OE"
    if a == 2:
        return "OOE"
    return "long"


def _corr(xs: list[float], ys: list[float]) -> float | None:
    n = len(xs)
    if n < 3:
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx <= 0.0 or vy <= 0.0:
        return None
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / math.sqrt(vx * vy)


def _persist(pairs: list[tuple[float, float]]) -> dict[str, Any]:
    n = len(pairs)
    out: dict[str, Any] = {"n": n}
    if not n:
        return out
    first = [a for a, _ in pairs]
    second = [b for _, b in pairs]
    out["mean"] = sum(first) / n
    out["corr"] = _corr(first, second)
    for thresh in THRESHOLDS:
        n_prev = sum(1 for a, _ in pairs if a > thresh)
        n_next = sum(1 for _, b in pairs if b > thresh)
        n_both = sum(1 for a, b in pairs if a > thresh and b > thresh)
        p_marg = n_prev / n
        p_cond = n_both / n_prev if n_prev else None
        out[f"c_{thresh}"] = {
            "n_prev": n_prev,
            "n_next": n_next,
            "n_both": n_both,
            "p": p_marg,
            "p_cond": p_cond,
            "ratio": (p_cond / p_marg) if p_cond is not None and p_marg > 0.0 else None,
        }
    return out


def _int_out(n: int) -> int | str:
    if n.bit_length() <= 128:
        return n
    return f"bits:{n.bit_length()}"


def _slim(row: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "x",
        "a0",
        "p0",
        "u0",
        "U0",
        "R0",
        "R0_max",
        "W0",
        "v1",
        "n_even",
        "a1",
        "p1",
        "u1",
        "U1",
        "R1",
        "R1_max",
        "W1",
        "Rsum",
        "Rsum_max",
        "Wsum",
        "Wsum_max",
        "growth",
    )
    out = {key: row[key] for key in keys}
    out["x"] = _int_out(row["x"])
    out["v1"] = _int_out(row["v1"])
    return out


def summarize_pairs(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {
            "count": 0,
            "joint_cellmax_ratio": None,
            "separable_R_ratio": None,
            "joint_weighted_ratio": None,
            "separable_W_ratio": None,
            "both_near_U": 0,
            "both_near_p": 0,
            "max_Usum": None,
            "max_min_U": None,
            "max_min_Uw": None,
            "two_excursion_tax": False,
        }
    r0 = [row["R0"] for row in rows]
    r1 = [row["R1"] for row in rows]
    w0 = [row["W0"] for row in rows]
    w1 = [row["W1"] for row in rows]
    rsum = [row["Rsum"] for row in rows]
    wsum = [row["Wsum"] for row in rows]
    cell = [row["Rsum"] / row["Rsum_max"] for row in rows if row["Rsum_max"] > 0.0]
    cell_w = [row["Wsum"] / row["Wsum_max"] for row in rows if row["Wsum_max"] > 0.0]
    u_pairs = [(row["U0"], row["U1"]) for row in rows]
    p_pairs = [(row["p0"], row["p1"]) for row in rows]
    uw_pairs = [(row["Uw0"], row["Uw1"]) for row in rows]
    within_p = [pair for row in rows for pair in row["within"]]
    within_u = [pair for row in rows for pair in row["within_u"]]
    near = [row for row in rows if row["p0"] > NEAR]
    near_u = [row for row in rows if row["U0"] > NEAR]
    both_u = sum(1 for row in rows if row["U0"] > NEAR and row["U1"] > NEAR)
    both_p = sum(1 for row in rows if row["p0"] > NEAR and row["p1"] > NEAR)
    both_uw = sum(1 for row in rows if row["Uw0"] > NEAR and row["Uw1"] > NEAR)
    u_sum = [row["U0"] + row["U1"] for row in rows]
    min_u = [min(row["U0"], row["U1"]) for row in rows]
    min_uw = [min(row["Uw0"], row["Uw1"]) for row in rows]
    joint = max(cell) if cell else None
    joint_w = max(cell_w) if cell_w else None
    sep_r = (max(r0) + max(r1)) if r0 else None
    sep_w = (max(w0) + max(w1)) if w0 else None
    max_rsum = max(rsum)
    max_wsum = max(wsum)
    best_joint = max(rows, key=lambda row: row["Rsum"] / row["Rsum_max"])
    best_sum = max(rows, key=lambda row: row["Rsum"])
    best_min = max(rows, key=lambda row: min(row["U0"], row["U1"]))
    payment = None
    if near:
        ooe_near = [row for row in near if row["a0"] == 2]
        growths = [row["growth"] for row in ooe_near if row["growth"] is not None]
        payment = {
            "n": len(near),
            "n_ooe": len(ooe_near),
            "mean_growth_ooe": sum(growths) / len(growths) if growths else None,
            "min_growth_ooe": min(growths) if growths else None,
            "max_growth_ooe": max(growths) if growths else None,
            "mean_U1": sum(row["U1"] for row in near) / len(near),
            "max_U1": max(row["U1"] for row in near),
            "min_U1": min(row["U1"] for row in near),
            "n_U1_near": sum(1 for row in near if row["U1"] > NEAR),
            "witness_max_U1": _slim(max(near, key=lambda row: row["U1"])),
            "witness_min_U1": _slim(min(near, key=lambda row: row["U1"])),
        }
    return {
        "count": len(rows),
        "max_R0": max(r0),
        "max_R1": max(r1),
        "max_Rsum": max_rsum,
        "separable_R": sep_r,
        "separable_R_ratio": max_rsum / sep_r if sep_r else None,
        "joint_cellmax_ratio": joint,
        "min_cellmax_ratio": min(cell) if cell else None,
        "max_W0": max(w0),
        "max_W1": max(w1),
        "max_Wsum": max_wsum,
        "separable_W": sep_w,
        "separable_W_ratio": max_wsum / sep_w if sep_w else None,
        "joint_weighted_ratio": joint_w,
        "min_weighted_ratio": min(cell_w) if cell_w else None,
        "both_near_U": both_u,
        "both_near_p": both_p,
        "both_near_Uw": both_uw,
        "max_Usum": max(u_sum),
        "max_min_U": max(min_u),
        "max_min_Uw": max(min_uw),
        "n_near_p0": len(near),
        "n_near_U0": len(near_u),
        "cross_p": _persist(p_pairs),
        "cross_U": _persist(u_pairs),
        "cross_Uw": _persist(uw_pairs),
        "within_p": _persist(within_p),
        "within_u": _persist(within_u),
        "payment": payment,
        "two_excursion_tax": bool(max(min_u) < 0.95 and max(u_sum) < 1.9),
        "best_joint": _slim(best_joint),
        "best_sum": _slim(best_sum),
        "best_min_U": _slim(best_min),
    }


def scan_odds(
    lo: int,
    hi: int,
    *,
    min_valley: int,
) -> tuple[list[dict[str, Any]], int]:
    start = lo if lo % 2 == 1 else lo + 1
    rows = []
    n_below = 0
    for x in range(start, hi, 2):
        rec = pair_record(x)
        if rec is None:
            continue
        if rec["v1"] < min_valley:
            n_below += 1
            continue
        rows.append(rec)
    return rows, n_below


def by_class(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {"OE": [], "OOE": [], "long": []}
    for row in rows:
        grouped[run_class(row["a0"])].append(row)
    return {name: summarize_pairs(group) for name, group in grouped.items()}


def window_report(lo: int, hi: int, *, min_valley: int) -> dict[str, Any]:
    rows, n_below = scan_odds(lo, hi, min_valley=min_valley)
    return {
        "lo": lo,
        "hi": hi,
        "min_valley": min_valley,
        "n_pairs": len(rows),
        "n_below_floor": n_below,
        "all": summarize_pairs(rows),
        "by_class": by_class(rows),
    }


def leftover_tax(length: int, coupling: float | None, n: int) -> dict[str, Any]:
    """Bookkeeping only: a window max(min U) is not a CycleMin theorem."""

    odd_count, theta = o_min_and_theta(length)
    packed = budget_rhs(n, length, odd_count)
    tax = packed * (1.0 - coupling) if coupling is not None else None
    return {
        "L": length,
        "o": odd_count,
        "theta": theta,
        "budget_rhs": packed,
        "ratio": packed / theta if theta else None,
        "need_factor": theta / packed if packed else None,
        "max_min_U": coupling,
        "tax": tax,
        "tax_over_theta": (tax / theta) if tax and theta else None,
        "would_kill_if_uniform": bool(tax is not None and packed - tax < theta),
        "kills": False,
    }


def persistence_scan(*, start: int = START) -> dict[str, Any]:
    n = start
    valley = window_report(n, n + VALLEY_WINDOW, min_valley=n)
    oe_lo = oe_start_min(n)
    oe_scale = window_report(oe_lo, oe_lo + OE_WINDOW, min_valley=n)
    couplings = [
        report["all"]["max_min_U"]
        for report in (valley, oe_scale)
        if report["all"].get("max_min_U") is not None
    ]
    coupling = max(couplings) if couplings else None
    both_near = any(
        report["all"]["both_near_U"] > 0 or report["all"]["both_near_Uw"] > 0
        for report in (valley, oe_scale)
    )
    spots = {str(length): leftover_tax(length, coupling, n) for length in SPOTLIGHT}
    emptied = [length for length, row in spots.items() if row["kills"]]
    weighted_corr = [
        report["all"]["cross_Uw"]["corr"]
        for report in (valley, oe_scale)
        if report["all"].get("cross_Uw")
        and report["all"]["cross_Uw"].get("corr") is not None
    ]
    max_usum = max(
        report["all"]["max_Usum"]
        for report in (valley, oe_scale)
        if report["all"].get("max_Usum") is not None
    )
    independent = both_near or (
        coupling is not None and (coupling >= 0.95 or max_usum >= 1.9)
    )
    return {
        "bound": "loss_persistence",
        "floor": PUBLISHED_FLOOR,
        "n": n,
        "oe_start": oe_lo,
        "valley": valley,
        "oe_scale": oe_scale,
        "spotlights": spots,
        "max_min_U": coupling,
        "max_Usum": max_usum,
        "both_near_attained": both_near,
        "two_excursion_tax": not independent,
        "anti_correlation_after_weighting": any(
            value < -0.05 for value in weighted_corr
        ),
        "emptied_lengths": emptied,
        "emptied_count": len(emptied),
        "leftover_killer": False,
        "window_max_is_not_a_theorem": True,
        "reduces_to_independent_corners": independent,
        "halt_theorem": False,
        "no_cycle_all_lengths": False,
        "sha256_spotlights": sha256_int_list(list(SPOTLIGHT)),
    }


def write_persistence_artifacts(
    payload: dict[str, Any] | None = None,
    *,
    start: int = START,
) -> dict[str, Any]:
    data = payload if payload is not None else persistence_scan(start=start)
    PERSISTENCE_DIR.mkdir(parents=True, exist_ok=True)
    path = PERSISTENCE_DIR / "summary.json"
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return data


if __name__ == "__main__":
    report = write_persistence_artifacts()
    print(
        json.dumps(
            {
                "max_min_U": report["max_min_U"],
                "max_Usum": report["max_Usum"],
                "both_near": report["both_near_attained"],
                "tax": report["two_excursion_tax"],
                "emptied": report["emptied_count"],
                "valley": {
                    "n": report["valley"]["n_pairs"],
                    "below": report["valley"]["n_below_floor"],
                    "max_min_U": report["valley"]["all"]["max_min_U"],
                    "max_Usum": report["valley"]["all"]["max_Usum"],
                    "both_U": report["valley"]["all"]["both_near_U"],
                    "corr_U": report["valley"]["all"].get("cross_U", {}).get("corr"),
                    "corr_W": report["valley"]["all"].get("cross_Uw", {}).get("corr"),
                    "by_class": {
                        name: {
                            "n": block["count"],
                            "max_min_U": block["max_min_U"],
                            "both_U": block["both_near_U"],
                            "p_cond_90": (block.get("cross_U") or {})
                            .get("c_0.9", {})
                            .get("p_cond"),
                            "p_90": (block.get("cross_U") or {})
                            .get("c_0.9", {})
                            .get("p"),
                            "p_cond_99": (block.get("cross_U") or {})
                            .get("c_0.99", {})
                            .get("p_cond"),
                        }
                        for name, block in report["valley"]["by_class"].items()
                    },
                },
                "oe_scale": {
                    "n": report["oe_scale"]["n_pairs"],
                    "below": report["oe_scale"]["n_below_floor"],
                    "max_min_U": report["oe_scale"]["all"]["max_min_U"],
                    "max_Usum": report["oe_scale"]["all"]["max_Usum"],
                    "both_U": report["oe_scale"]["all"]["both_near_U"],
                    "corr_U": report["oe_scale"]["all"].get("cross_U", {}).get("corr"),
                    "corr_W": report["oe_scale"]["all"].get("cross_Uw", {}).get("corr"),
                },
                "best_min_U": report["valley"]["all"].get("best_min_U"),
                "25781": report["spotlights"]["25781"],
                "55293": report["spotlights"]["55293"],
            },
            indent=2,
        )
    )
