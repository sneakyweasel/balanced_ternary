"""Cycle-finance error-budget optimization on E_par leftovers.

Not a halt theorem, not a leftover-word census, and not a new
dynamical invariant. The length-only packing uses only CycleMin,
cycleMin_even_ge_sq, unique visit of n, and the odd-run type split
forced by o_min: an OE-start is even, hence at least n^2, so the
valley is at least n^{4/3}.

Dossier: docs/problems/juggler_cycle_budget_opt.md.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from research.juggler_sequence.cycle_finance import (
    DATA_DIR,
    EPS_CONST,
    MIN_STATE,
    PARITY_ABS_PAD,
    PARITY_REL_GUARD,
    PUBLISHED_FLOOR,
    first_odd_image,
    o_min_and_theta,
    parity_excludes,
    parity_rhs,
    sha256_int_list,
)

def inv_log(x: int) -> float:
    if x < 3:
        return math.inf
    return 1.0 / (float(x) * math.log(x))


def oe_start_min(n: int) -> int:
    """Least odd v with T(v) >= n^2, i.e. v^3 >= n^4.

    An OE-start is followed by an even state, so cycleMin_even_ge_sq
    gives T(v) >= n^2 and therefore v >= n^{4/3}.
    """

    if n < 2:
        return n
    target = n * n * n * n
    lo = n
    hi = n * n
    while lo < hi:
        mid = (lo + hi) // 2
        if mid * mid * mid < target:
            lo = mid + 1
        else:
            hi = mid
    if lo % 2 == 0:
        lo += 1
    return lo


def run_type_counts(odd_count: int, even_count: int) -> tuple[int, int]:
    """Adversarial (OO, OE) counts at o_min: OO = o-e, OE = 2e-o.

    Each OO-run uses two odds and one even from n; each OE-run uses
    one odd and one even from n^{4/3}. This maximises the number of
    n-valleys among length-only CycleMin geometries. Extra depth or
    extra evens only move states up and shrink the sum.
    """

    oo_count = max(odd_count - even_count, 0)
    oe_count = max(2 * even_count - odd_count, 0)
    return oo_count, oe_count


def first_even_after_oo(n: int) -> int:
    """Lower bound for the first even after an OO-run from n.

    CycleMin forbids T(n) even (that landing is < n^2). The next
    image T^2(n) is at least n^{9/4} and is the first possible even.
    """

    image = first_odd_image(n)
    if image % 2 == 1:
        return first_odd_image(image)
    return image


def budget_sum_terms(
    n: int,
    length: int,
    odd_count: int,
    *,
    unique_min: bool = True,
    drop_max_even: bool = False,
) -> float:
    """Worst-case Σ 1/(x ln x) under uniqueness + run-type + max.

    Valleys: one at n and oo-1 at n+2 (unique visit); oe at oe_start.
    Internals: one at T(n), the rest at T(n+2). Evens at n^2, or
    one even omitted when drop_max_even tests M -> infinity.
    """

    if n < 3:
        return math.inf
    even_count = length - odd_count
    oo_count, oe_count = run_type_counts(odd_count, even_count)
    n_low = n + 2 if unique_min and oo_count > 1 else n
    oe_v = oe_start_min(n)
    image = first_odd_image(n)
    image_low = first_odd_image(n_low)
    valley = inv_log(n)
    if oo_count > 1:
        valley += (oo_count - 1) * inv_log(n_low)
    elif oo_count == 1:
        pass
    climb = inv_log(image) if oo_count >= 1 else 0.0
    if oo_count > 1:
        climb += (oo_count - 1) * inv_log(image_low)
    high = oe_count * inv_log(oe_v)
    evens = even_count
    if drop_max_even and evens:
        evens -= 1
    even_term = evens * inv_log(n * n)
    return valley + climb + high + even_term


def budget_rhs(
    n: int,
    length: int,
    odd_count: int,
    *,
    const: float = EPS_CONST,
    unique_min: bool = True,
    drop_max_even: bool = False,
) -> float:
    return const * budget_sum_terms(
        n,
        length,
        odd_count,
        unique_min=unique_min,
        drop_max_even=drop_max_even,
    )


def budget_rhs_upper(
    n: int,
    length: int,
    odd_count: int,
    *,
    const: float = EPS_CONST,
    unique_min: bool = True,
    drop_max_even: bool = False,
) -> float:
    raw = budget_rhs(
        n,
        length,
        odd_count,
        const=const,
        unique_min=unique_min,
        drop_max_even=drop_max_even,
    )
    if not math.isfinite(raw):
        return math.inf
    return raw * (1.0 + PARITY_REL_GUARD) + PARITY_ABS_PAD


def budget_rhs_lower(
    n: int,
    length: int,
    odd_count: int,
    *,
    const: float = EPS_CONST,
    unique_min: bool = True,
    drop_max_even: bool = False,
) -> float:
    raw = budget_rhs(
        n,
        length,
        odd_count,
        const=const,
        unique_min=unique_min,
        drop_max_even=drop_max_even,
    )
    if not math.isfinite(raw):
        return 0.0
    return max(0.0, raw * (1.0 - PARITY_REL_GUARD) - PARITY_ABS_PAD)


def budget_survives_floor(
    length: int,
    odd_count: int,
    theta: float,
    n0: int,
    *,
    const: float = EPS_CONST,
    unique_min: bool = True,
    drop_max_even: bool = False,
) -> bool:
    start = max(n0 + 1, MIN_STATE)
    theta_hi = theta * (1.0 + PARITY_REL_GUARD)
    return theta_hi < budget_rhs_lower(
        start,
        length,
        odd_count,
        const=const,
        unique_min=unique_min,
        drop_max_even=drop_max_even,
    )


def budget_n_max(
    length: int,
    odd_count: int,
    theta: float,
    *,
    const: float = EPS_CONST,
    unique_min: bool = True,
    drop_max_even: bool = False,
) -> int:
    """Largest n at which the padded packed inequality can still hold."""

    def holds(n: int) -> bool:
        return theta <= budget_rhs_upper(
            n,
            length,
            odd_count,
            const=const,
            unique_min=unique_min,
            drop_max_even=drop_max_even,
        )

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


def budget_excludes(
    length: int,
    odd_count: int,
    theta: float,
    n0: int,
    *,
    const: float = EPS_CONST,
    unique_min: bool = True,
    drop_max_even: bool = False,
) -> bool:
    start = max(n0 + 1, MIN_STATE)
    theta_lo = theta * (1.0 - PARITY_REL_GUARD)
    return theta_lo > budget_rhs_upper(
        start,
        length,
        odd_count,
        const=const,
        unique_min=unique_min,
        drop_max_even=drop_max_even,
    )


def climb_fits_tau1(odd_count: int, even_count: int) -> bool:
    """At o_min one has o-e < e, so every internal can sit at T(n)."""

    return odd_count - even_count < even_count


def budget_row(
    length: int,
    *,
    floor: int = PUBLISHED_FLOOR,
    const: float = EPS_CONST,
) -> dict[str, Any]:
    odd_count, theta = o_min_and_theta(length)
    even_count = length - odd_count
    start = max(floor + 1, MIN_STATE)
    oo_count, oe_count = run_type_counts(odd_count, even_count)
    parity = parity_rhs(start, length, odd_count, const=const)
    packed = budget_rhs(start, length, odd_count, const=const)
    packed_no_unique = budget_rhs(
        start, length, odd_count, const=const, unique_min=False
    )
    dropped = budget_rhs(
        start, length, odd_count, const=const, drop_max_even=True
    )
    return {
        "L": length,
        "o": odd_count,
        "e": even_count,
        "oo_count": oo_count,
        "oe_count": oe_count,
        "theta": theta,
        "n": start,
        "oe_start": oe_start_min(start),
        "climb_fits_tau1": climb_fits_tau1(odd_count, even_count),
        "parity_rhs": parity,
        "budget_rhs": packed,
        "budget_rhs_no_unique": packed_no_unique,
        "budget_rhs_drop_max": dropped,
        "strictly_below_parity": packed < parity,
        "parity_excludes": parity_excludes(
            length, odd_count, theta, floor, const=const
        ),
        "budget_excludes": budget_excludes(
            length, odd_count, theta, floor, const=const
        ),
        "drop_max_excludes": budget_excludes(
            length,
            odd_count,
            theta,
            floor,
            const=const,
            drop_max_even=True,
        ),
    }


def budget_scan(
    *,
    floor: int = PUBLISHED_FLOOR,
    const: float = EPS_CONST,
) -> dict[str, Any]:
    payload = json.loads(
        (DATA_DIR / "exceptions_parity.json").read_text(encoding="utf-8")
    )
    lengths = list(payload["lengths"])
    rows = [budget_row(length, floor=floor, const=const) for length in lengths]
    killed = [row["L"] for row in rows if row["budget_excludes"]]
    killed_drop = [row["L"] for row in rows if row["drop_max_excludes"]]
    not_strict = [row["L"] for row in rows if not row["strictly_below_parity"]]
    tau1_fail = [row["L"] for row in rows if not row["climb_fits_tau1"]]
    spotlight = next(row for row in rows if row["L"] == 25781)
    return {
        "bound": "budget_opt",
        "floor": floor,
        "n": max(floor + 1, MIN_STATE),
        "oe_start": oe_start_min(max(floor + 1, MIN_STATE)),
        "leftover_count": len(rows),
        "killed_by_parity": [row["L"] for row in rows if row["parity_excludes"]],
        "killed_by_budget": killed,
        "killed_count": len(killed),
        "remaining_count": len(rows) - len(killed),
        "sha256_killed": sha256_int_list(killed),
        "killed_by_drop_max": killed_drop,
        "not_strictly_below_parity": not_strict,
        "climb_fits_tau1_failures": tau1_fail,
        "max_unbounded_changes_extremum": killed_drop != killed,
        "spotlight_25781": spotlight,
        "rows": rows,
        "halt_theorem": False,
        "no_cycle_all_lengths": False,
    }


def write_budget_opt_artifacts(
    payload: dict[str, Any] | None = None,
    *,
    floor: int = PUBLISHED_FLOOR,
) -> dict[str, Any]:
    data = payload if payload is not None else budget_scan(floor=floor)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / "budget_opt.json"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return data
