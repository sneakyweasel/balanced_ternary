"""Finance-conditioned exact closure on E_run leftovers.

Not a halt theorem, not a leftover-word census, not a new global
finance identity, not Fourier, not Q-return, and not a residue
system. Phase 0 asks whether leftover surplus forces near-extremal
run structure tightly enough that exact cells empty L=25781 or
L=55293.

The packed RHS already maximises the present run-type model. A
deviation that lowers that RHS is affordable whenever the drop
stays inside theta-to-packed slack. Exact closure is then the
existing word-independent hull on the run-type n-window.

Dossier: docs/problems/juggler_cycle_conditioned_closure.md.
"""

from __future__ import annotations

import json
import math
from typing import Any

from research.juggler_sequence.cycle_budget_opt import (
    budget_rhs,
    inv_log,
    oe_start_min,
    run_type_counts,
)
from research.juggler_sequence.cycle_closure import (
    first_last_cells,
    next_oo_start,
    word_independent_hull,
)
from research.juggler_sequence.cycle_finance import (
    DATA_DIR,
    EPS_CONST,
    MIN_STATE,
    PUBLISHED_FLOOR,
    o_min_and_theta,
    parity_n_max,
    sha256_int_list,
)
from research.juggler_sequence.cycle_run_extremum import (
    f_coarse,
    ooe_next_valley_min,
)

SPOTLIGHT = (25781, 55293)
CONDITIONED_DIR = DATA_DIR / "conditioned_closure"


def run_type_n_max(
    length: int,
    odd_count: int,
    theta: float,
    *,
    const: float = EPS_CONST,
) -> int:
    """Largest n with theta <= packed run-type RHS. Raw crossing."""

    def holds(n: int) -> bool:
        return n >= 3 and theta <= budget_rhs(n, length, odd_count, const=const)

    if not holds(MIN_STATE):
        lo = 2
        hi = MIN_STATE - 1
        if not holds(lo):
            return 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if holds(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
    hi = MIN_STATE
    while holds(hi):
        if hi > 10**18:
            return hi
        nxt = hi * 2
        if nxt <= hi:
            return hi
        hi = nxt
    lo = hi // 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if holds(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


def affordable_count(margin: float, cost: float, cap: int) -> int:
    """How many equal-cost deviations still leave packed > theta."""

    if cap <= 0:
        return 0
    if cost <= 0.0:
        return cap
    return min(cap, int(math.floor(margin / cost)))


def log10_choose(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float("-inf")
    k = min(k, n - k)
    total = 0.0
    for index in range(k):
        total += math.log10(n - index) - math.log10(index + 1)
    return total


def lose_cheap_cost(n: int) -> float:
    """Packed drop from moving one cheap OOE start from n+2 to oe_start."""

    return EPS_CONST * (inv_log(n + 2) - inv_log(oe_start_min(n)))


def deepen_cost(n: int) -> float:
    """Packed drop from (OOE, OE) -> OOOE."""

    return EPS_CONST * (f_coarse(2, n) + f_coarse(1, n) - f_coarse(3, n))


def merge_cost(n: int) -> float:
    """Packed drop from (OOE, OOE) -> (OOO, OE)."""

    return EPS_CONST * (
        2.0 * f_coarse(2, n) - f_coarse(3, n) - f_coarse(1, n)
    )


def raise_to_2n_cost(n: int) -> float:
    return EPS_CONST * (inv_log(n + 2) - inv_log(2 * n))


def raise_to_landing_cost(n: int) -> float:
    """Packed drop from moving one cheap start to the legal OOE landing."""

    landing = ooe_next_valley_min(n)
    return EPS_CONST * (inv_log(n + 2) - inv_log(max(landing, 3)))


def deficit_row(length: int, *, floor: int = PUBLISHED_FLOOR) -> dict[str, Any]:
    odd_count, theta = o_min_and_theta(length)
    even_count = length - odd_count
    oo_count, oe_count = run_type_counts(odd_count, even_count)
    start = max(floor + 1, MIN_STATE)
    legal = next_oo_start(start, up=True) or start
    packed = budget_rhs(start, length, odd_count)
    margin = packed - theta
    cost_lose = lose_cheap_cost(start)
    cost_deep = deepen_cost(start)
    cost_merge = merge_cost(start)
    cost_2n = raise_to_2n_cost(start)
    cost_land = raise_to_landing_cost(legal)
    k_lose = affordable_count(margin, cost_lose, oo_count)
    k_deep = affordable_count(margin, cost_deep, min(oo_count, oe_count))
    k_merge = affordable_count(margin, cost_merge, oo_count // 2)
    k_2n = affordable_count(margin, cost_2n, oo_count)
    k_land = affordable_count(margin, cost_land, oo_count)
    deepen_all = k_deep == min(oo_count, oe_count)
    packed_after_deepen_all = packed - k_deep * cost_deep
    n_run = run_type_n_max(length, odd_count, theta)
    n_par = parity_n_max(length, odd_count, theta)
    n_hi = min(n_run, n_par)
    if n_hi % 2 == 0:
        n_hi -= 1
    n_hi = max(n_hi, start if start % 2 == 1 else start + 1)
    n_lo = start if start % 2 == 1 else start + 1
    hull = word_independent_hull(n_lo, n_hi, odd_count, length)
    cells = first_last_cells(legal)
    residual_log10 = log10_choose(oo_count, k_lose)
    concentrates = (
        k_lose == 0 and k_deep == 0 and k_merge == 0 and not hull["start_meets_envelope"]
    )
    return {
        "L": length,
        "o": odd_count,
        "e": even_count,
        "oo_count": oo_count,
        "oe_count": oe_count,
        "theta": theta,
        "n": start,
        "legal_oo_start": legal,
        "ooe_landing": ooe_next_valley_min(legal),
        "packed": packed,
        "margin": margin,
        "packed_over_theta": packed / theta if theta else None,
        "cost_lose_cheap": cost_lose,
        "cost_deepen": cost_deep,
        "cost_merge": cost_merge,
        "cost_raise_2n": cost_2n,
        "cost_raise_landing": cost_land,
        "k_lose_cheap": k_lose,
        "k_deepen": k_deep,
        "k_merge": k_merge,
        "k_raise_2n": k_2n,
        "k_raise_landing": k_land,
        "lose_fraction": k_lose / oo_count if oo_count else None,
        "deepen_all_affordable": deepen_all,
        "packed_after_deepen_all": packed_after_deepen_all,
        "deepen_all_still_above_theta": packed_after_deepen_all > theta,
        "n_max_run": n_run,
        "n_max_par": n_par,
        "n_lo": n_lo,
        "n_hi": n_hi,
        "residual_log10_lose": residual_log10,
        "residual_exponential": residual_log10 > 10.0,
        "hull": hull,
        "first_last": cells,
        "hull_meets": hull["start_meets_envelope"],
        "first_and_last_are_different_indices": cells["different_indices"],
        "concentrates": concentrates,
        "stronger_than_packing": False,
        "closure_empty": False,
        "requires_word_enumeration": True,
        "reduces_to_envelope": hull["reduces_to_envelope"],
    }


def conditioned_scan(*, floor: int = PUBLISHED_FLOOR) -> dict[str, Any]:
    spots = {str(length): deficit_row(length, floor=floor) for length in SPOTLIGHT}
    emptied = [length for length, row in spots.items() if row["closure_empty"]]
    return {
        "bound": "conditioned_closure",
        "floor": floor,
        "spotlights": spots,
        "emptied_lengths": emptied,
        "emptied_count": len(emptied),
        "concentrates": any(row["concentrates"] for row in spots.values()),
        "deepen_all_still_above_theta": all(
            row["deepen_all_still_above_theta"] for row in spots.values()
        ),
        "hull_feasible": all(row["hull_meets"] for row in spots.values()),
        "stronger_than_packing": False,
        "requires_word_enumeration": True,
        "reduces_to_envelope": True,
        "sha256_spotlights": sha256_int_list(list(SPOTLIGHT)),
        "halt_theorem": False,
        "no_cycle_all_lengths": False,
    }


def write_conditioned_artifacts(
    payload: dict[str, Any] | None = None,
    *,
    floor: int = PUBLISHED_FLOOR,
) -> dict[str, Any]:
    data = payload if payload is not None else conditioned_scan(floor=floor)
    CONDITIONED_DIR.mkdir(parents=True, exist_ok=True)
    path = CONDITIONED_DIR / "summary.json"
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return data


if __name__ == "__main__":
    report = write_conditioned_artifacts()
    print(
        json.dumps(
            {
                "emptied": report["emptied_count"],
                "concentrates": report["concentrates"],
                "deepen_all": report["deepen_all_still_above_theta"],
                "hull": report["hull_feasible"],
                "25781": {
                    "margin": report["spotlights"]["25781"]["margin"],
                    "k_lose": report["spotlights"]["25781"]["k_lose_cheap"],
                    "k_deepen": report["spotlights"]["25781"]["k_deepen"],
                    "n_max_run": report["spotlights"]["25781"]["n_max_run"],
                    "ratio": report["spotlights"]["25781"]["packed_over_theta"],
                },
                "55293": {
                    "margin": report["spotlights"]["55293"]["margin"],
                    "k_lose": report["spotlights"]["55293"]["k_lose_cheap"],
                    "k_deepen": report["spotlights"]["55293"]["k_deepen"],
                    "n_max_run": report["spotlights"]["55293"]["n_max_run"],
                    "ratio": report["spotlights"]["55293"]["packed_over_theta"],
                },
            },
            indent=2,
        )
    )
