"""Cyclic run-type finance extremum on E_run leftovers.

Not a halt theorem, not a leftover-word census, and not a new
dynamical invariant. Level A/B asks whether the OOE/OE packing
already maximises the coarse run-cost among partitions of o odds
into e runs. Level C asks whether cheap OOE adjacency forces
N_cheap < o-e.

Dossier subsection: docs/problems/juggler_cycle_budget_opt.md.
"""

from __future__ import annotations

import json
from math import isqrt
from typing import Any

from research.juggler_sequence.cycle_budget_opt import (
    budget_excludes,
    budget_rhs,
    inv_log,
    oe_start_min,
    run_type_counts,
)
from research.juggler_sequence.cycle_finance import (
    DATA_DIR,
    EPS_CONST,
    MIN_STATE,
    PARITY_ABS_PAD,
    PARITY_REL_GUARD,
    PUBLISHED_FLOOR,
    first_odd_image,
    o_min_and_theta,
    sha256_int_list,
)

SPOTLIGHT = (25781, 55293)
EXCHANGE_DEPTH = 8


def run_heights(valley: int, depth: int) -> list[int]:
    """tau_0 = valley; tau_{j+1} = least odd >= T(tau_j)."""

    if depth < 1:
        return []
    heights = [valley]
    current = valley
    for _ in range(depth - 1):
        image = isqrt(current * current * current)
        if image % 2 == 0:
            image += 1
        heights.append(image)
        current = image
    return heights


def f_coarse(depth: int, n: int) -> float:
    """Coarse finance of one odd-run of length `depth`.

    A run of length 1 must start at oe_start_min(n). A run of
    length >= 2 may start at n. Internals sit at tau_j(start).
    """

    if depth < 1:
        return 0.0
    start = n if depth >= 2 else oe_start_min(n)
    return sum(inv_log(height) for height in run_heights(start, depth))


def delta_coarse(depth: int, n: int) -> float:
    """F_coarse(depth+1) - F_coarse(depth)."""

    return f_coarse(depth + 1, n) - f_coarse(depth, n)


def two_type_beats_merge(n: int) -> bool:
    """F(2)+F(2) >= F(3)+F(1): two OOE beat one OOO plus one OE."""

    return f_coarse(2, n) + f_coarse(2, n) + PARITY_ABS_PAD >= (
        f_coarse(3, n) + f_coarse(1, n)
    )


def two_type_beats_deepen(n: int) -> bool:
    """F(2)+F(1) >= F(3): deepening one OOE by eating an OE lowers F."""

    return f_coarse(2, n) + f_coarse(1, n) + PARITY_ABS_PAD >= f_coarse(3, n)


def two_type_odd_sum(n: int, odd_count: int, even_count: int) -> float:
    """Odd-state part of the two-type packing, unique min off.

    o-e copies of F(2,n) plus 2e-o copies of F(1,n). Evens are
    charged separately at n^2, as in budget_sum_terms.
    """

    oo_count, oe_count = run_type_counts(odd_count, even_count)
    return oo_count * f_coarse(2, n) + oe_count * f_coarse(1, n)


def deepen_one_oo_odd_sum(n: int, odd_count: int, even_count: int) -> float:
    """Replace one OOE and one OE by one OOOE: (2,1) -> (3)."""

    oo_count, oe_count = run_type_counts(odd_count, even_count)
    if oo_count < 1 or oe_count < 1:
        return two_type_odd_sum(n, odd_count, even_count)
    return (
        (oo_count - 1) * f_coarse(2, n)
        + (oe_count - 1) * f_coarse(1, n)
        + f_coarse(3, n)
    )


def merge_two_oo_odd_sum(n: int, odd_count: int, even_count: int) -> float:
    """Replace two OOE by one OE and one OOO: (2,2) -> (1,3)."""

    oo_count, oe_count = run_type_counts(odd_count, even_count)
    if oo_count < 2:
        return two_type_odd_sum(n, odd_count, even_count)
    return (
        (oo_count - 2) * f_coarse(2, n)
        + (oe_count + 1) * f_coarse(1, n)
        + f_coarse(3, n)
    )


def ooe_next_valley_min(n: int) -> int:
    """Ideal one-even landing after OO from n, isqrt(T^2(n)) or isqrt(T(n)).

    If T(n) is even the run is OE and the landing is below n, so
    this n is not a CycleMin start. The finance constraint is the
    power_bound_word envelope, not a new count on cheap valleys.
    """

    image = first_odd_image(n)
    if image % 2 == 1:
        image = first_odd_image(image)
    return isqrt(image)


def cheap_ooe_cannot_feed_oe(n: int) -> bool:
    """A cheap OOE cannot be followed by OE: the landing is below n^{4/3}."""

    landing = ooe_next_valley_min(n)
    return landing < n or landing < oe_start_min(n)


def n_cheap_still_o_minus_e(odd_count: int, even_count: int) -> bool:
    """Known constraints still allow o-e cheap valleys.

    Unique visit forbids repeating n, not repeating the n-scale
    class (n+2, n+4, ...). Adjacency after one cheap OOE forces
    the *next* valley to n^{9/8}, but does not cap the number of
    non-adjacent cheap starts. So N_cheap = o-e remains attainable
    under the present model.
    """

    oo_count, _oe_count = run_type_counts(odd_count, even_count)
    return oo_count == max(odd_count - even_count, 0)


def exchange_report(n: int) -> dict[str, Any]:
    deltas = [delta_coarse(depth, n) for depth in range(1, EXCHANGE_DEPTH)]
    decreasing = all(
        deltas[index] + PARITY_ABS_PAD >= deltas[index + 1]
        for index in range(len(deltas) - 1)
    )
    return {
        "n": n,
        "f1": f_coarse(1, n),
        "f2": f_coarse(2, n),
        "f3": f_coarse(3, n),
        "deltas": deltas,
        "deltas_decreasing": decreasing,
        "two_type_beats_merge": two_type_beats_merge(n),
        "two_type_beats_deepen": two_type_beats_deepen(n),
        "oe_start": oe_start_min(n),
        "ooe_next": ooe_next_valley_min(n),
        "cheap_ooe_cannot_feed_oe": cheap_ooe_cannot_feed_oe(n),
    }


def extremum_row(
    length: int,
    *,
    floor: int = PUBLISHED_FLOOR,
    const: float = EPS_CONST,
) -> dict[str, Any]:
    odd_count, theta = o_min_and_theta(length)
    even_count = length - odd_count
    start = max(floor + 1, MIN_STATE)
    two_type = two_type_odd_sum(start, odd_count, even_count)
    deepen = deepen_one_oo_odd_sum(start, odd_count, even_count)
    merge = merge_two_oo_odd_sum(start, odd_count, even_count)
    even_term = even_count * inv_log(start * start)
    relaxed = const * (two_type + even_term)
    packed = budget_rhs(start, length, odd_count, const=const, unique_min=False)
    return {
        "L": length,
        "o": odd_count,
        "e": even_count,
        "theta": theta,
        "n": start,
        "two_type_odd_sum": two_type,
        "deepen_odd_sum": deepen,
        "merge_odd_sum": merge,
        "two_type_is_max": two_type + PARITY_ABS_PAD >= deepen
        and two_type + PARITY_ABS_PAD >= merge,
        "relaxed_rhs": relaxed,
        "budget_rhs": packed,
        "relaxed_matches_budget": abs(relaxed - packed) <= packed * PARITY_REL_GUARD
        + PARITY_ABS_PAD,
        "n_cheap": run_type_counts(odd_count, even_count)[0],
        "n_cheap_still_o_minus_e": n_cheap_still_o_minus_e(odd_count, even_count),
        "budget_excludes": budget_excludes(
            length, odd_count, theta, floor, const=const
        ),
        "level_c_excludes": False,
    }


def survivor_lengths(*, floor: int = PUBLISHED_FLOOR) -> list[int]:
    payload = json.loads(
        (DATA_DIR / "budget_opt.json").read_text(encoding="utf-8")
    )
    killed = set(payload["killed_by_budget"])
    return [row["L"] for row in payload["rows"] if row["L"] not in killed]


def extremum_scan(
    *,
    floor: int = PUBLISHED_FLOOR,
    const: float = EPS_CONST,
) -> dict[str, Any]:
    start = max(floor + 1, MIN_STATE)
    exchange = exchange_report(start)
    rows = [
        extremum_row(length, floor=floor, const=const)
        for length in survivor_lengths(floor=floor)
    ]
    not_max = [row["L"] for row in rows if not row["two_type_is_max"]]
    not_match = [row["L"] for row in rows if not row["relaxed_matches_budget"]]
    n_cheap_drop = [
        row["L"] for row in rows if not row["n_cheap_still_o_minus_e"]
    ]
    killed = [row["L"] for row in rows if row["level_c_excludes"]]
    spotlights = {
        str(length): next(row for row in rows if row["L"] == length)
        for length in SPOTLIGHT
        if any(row["L"] == length for row in rows)
    }
    return {
        "bound": "run_extremum",
        "floor": floor,
        "n": start,
        "survivor_count": len(rows),
        "sha256_survivors": sha256_int_list([row["L"] for row in rows]),
        "exchange": {
            "n": exchange["n"],
            "f1": exchange["f1"],
            "f2": exchange["f2"],
            "f3": exchange["f3"],
            "deltas": exchange["deltas"],
            "deltas_decreasing": exchange["deltas_decreasing"],
            "two_type_beats_merge": exchange["two_type_beats_merge"],
            "two_type_beats_deepen": exchange["two_type_beats_deepen"],
            "oe_start": exchange["oe_start"],
            "ooe_next": exchange["ooe_next"],
            "cheap_ooe_cannot_feed_oe": exchange["cheap_ooe_cannot_feed_oe"],
        },
        "two_type_is_relaxed_max": not not_max,
        "two_type_max_failures": not_max,
        "relaxed_matches_budget": not not_match,
        "relaxed_match_failures": not_match,
        "n_cheap_drop_failures": n_cheap_drop,
        "n_cheap_still_o_minus_e": not n_cheap_drop,
        "level_c_binds": False,
        "killed_by_level_c": killed,
        "spotlights": spotlights,
        "rows": rows,
        "halt_theorem": False,
        "no_cycle_all_lengths": False,
    }


def write_run_extremum_artifacts(
    payload: dict[str, Any] | None = None,
    *,
    floor: int = PUBLISHED_FLOOR,
) -> dict[str, Any]:
    data = payload if payload is not None else extremum_scan(floor=floor)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / "run_extremum.json"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return data
