"""Return-cost coupling of cheap CycleMin valleys.

Not a halt theorem, not a leftover-word census, and not a floor
raise. After a cheap OOE the next valley is at envelope 9/8, not
at n+2. Independent n-scale copies of OOE are not a realized
geometry. Dossier: docs/problems/juggler_cycle_valley_coupling.md.
"""

from __future__ import annotations

import json
import math
from math import isqrt
from typing import Any

from research.juggler_sequence.cycle_budget_opt import (
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
from research.juggler_sequence.cycle_run_extremum import survivor_lengths

K_MAX = 53
ELL_MAX = 32
NINE_EIGHTHS = (2, 3)  # 3^2 / 2^3
SPOTLIGHT = (25781, 55293)


def three_ge_two(exp3: int, exp2: int) -> bool:
    """3^{exp3} >= 2^{exp2}."""

    if exp3 < 0 or exp2 < 0:
        return False
    if exp3 <= 40 and exp2 <= 80:
        return 3**exp3 >= (1 << exp2)
    return exp3 * math.log(3) + 1e-15 >= exp2 * math.log(2)


def circuit_legal(exp3: int, exp2: int, odd_run: int, even_run: int) -> bool:
    """Envelope circuit from 3^{exp3}/2^{exp2} stays at least 1.

    Peak >= 2^{even_run} is the same comparison: landing >= 1.
    Intermediate evens are weaker once the landing is at least 1.
    """

    if odd_run < 1 or even_run < 1:
        return False
    return three_ge_two(exp3 + odd_run, exp2 + odd_run + even_run)


def land(exp3: int, exp2: int, odd_run: int, even_run: int) -> tuple[int, int]:
    return exp3 + odd_run, exp2 + odd_run + even_run


def exponent_log2(exp3: int, exp2: int) -> float:
    """log2(3^{exp3}/2^{exp2})."""

    return exp3 * math.log(3) / math.log(2) - exp2


def lowest_circuit(
    exp3: int,
    exp2: int,
    odd_left: int,
    even_left: int,
    *,
    k_max: int = K_MAX,
    ell_max: int = ELL_MAX,
) -> tuple[int, int] | None:
    """Legal (k, ell) whose landing is closest to 1 from above."""

    best: tuple[int, int] | None = None
    best_log = math.inf
    k_hi = min(k_max, odd_left)
    ell_hi = min(ell_max, even_left)
    for odd_run in range(1, k_hi + 1):
        for even_run in range(1, ell_hi + 1):
            if not circuit_legal(exp3, exp2, odd_run, even_run):
                continue
            landed = land(exp3, exp2, odd_run, even_run)
            log_val = exponent_log2(*landed)
            if log_val + 1e-15 < 0:
                continue
            if log_val < best_log - 1e-15:
                best_log = log_val
                best = (odd_run, even_run)
    return best


def shortest_descent_from_nine_eighths(
    *,
    k_max: int = K_MAX,
    ell_max: int = ELL_MAX,
) -> dict[str, Any]:
    """Least letter-cost circuit from 9/8 that lands strictly below 9/8."""

    start = NINE_EIGHTHS
    start_log = exponent_log2(*start)
    hits: list[dict[str, Any]] = []
    for odd_run in range(1, k_max + 1):
        for even_run in range(1, ell_max + 1):
            if not circuit_legal(*start, odd_run, even_run):
                continue
            landed = land(*start, odd_run, even_run)
            log_val = exponent_log2(*landed)
            if log_val + 1e-15 < 0 or log_val >= start_log - 1e-15:
                continue
            hits.append(
                {
                    "k": odd_run,
                    "ell": even_run,
                    "letters": odd_run + even_run,
                    "land_exp3": landed[0],
                    "land_exp2": landed[1],
                    "land_log2": log_val,
                    "land_ratio": 2.0**log_val,
                }
            )
    hits.sort(key=lambda row: (row["letters"], row["k"], row["ell"]))
    shortest = hits[0] if hits else None
    return {
        "start": "9/8",
        "shortest": shortest,
        "is_five_three": (
            shortest is not None
            and shortest["k"] == 5
            and shortest["ell"] == 3
        ),
        "count": len(hits),
        "hits": hits[:12],
    }


def exact_reset_to_one_exists(
    *,
    k_max: int = K_MAX,
    ell_max: int = ELL_MAX,
) -> bool:
    """3^{k+2} = 2^{k+ell+3} is impossible, and the scan agrees."""

    start = NINE_EIGHTHS
    for odd_run in range(1, k_max + 1):
        for even_run in range(1, ell_max + 1):
            if not circuit_legal(*start, odd_run, even_run):
                continue
            landed = land(*start, odd_run, even_run)
            if landed[0] == 0 and landed[1] == 0:
                return True
            if exponent_log2(*landed) == 0.0:
                return True
    return False


def n_max_separated(odd_count: int, even_count: int, odd_run: int, even_run: int) -> int:
    """Max n-scale OOE copies if each extra copy pays a (k, ell) return.

    N OOE plus N-1 returns use 2N+(N-1)k odds and N+(N-1)ell evens.
    """

    if odd_run < 1 or even_run < 1:
        return 1
    by_odds = (odd_count + odd_run) // (2 + odd_run)
    by_evens = (even_count + even_run) // (1 + even_run)
    return max(1, min(by_odds, by_evens))


def ooe_landing_lower(v: int) -> int:
    """Integer lower bound for an OOE landing from odd v.

    T(v) >= isqrt(v^3) if we only walk when the first image is odd.
    The second odd image p satisfies p >= isqrt(T(v)^3) - 0 in the
    integer floor-power, and the even landing is isqrt(p).
    """

    if v < 3:
        return 0
    first = first_odd_image(v)
    if first % 2 == 0:
        return isqrt(first)
    second = first_odd_image(first)
    return isqrt(second)


def ooe_landing_beats_n_plus_two(v: int) -> bool:
    """The OOE landing is strictly above the unique-visit slot n+2."""

    return ooe_landing_lower(v) > v + 2


def nine_eighths_height(n: int) -> int:
    """Conservative integer height n^{9/8} rounded down, minus 4 floors."""

    if n < 3:
        return n
    # n^{9/8} = n * n^{1/8} = n * (n)^{1/8}. Use integer root chain:
    # n^{9/8} = (n^9)^{1/8}. For n~10^6 this overflows 64-bit if naive.
    # (n^{1/2})^{1/4} * n = n * n^{1/8}.
    square = isqrt(n)
    fourth = isqrt(square)
    eighth = isqrt(fourth)
    height = n * eighth
    return max(n + 3, height - 4)


def nine_eighths_sum_terms(n: int, length: int, odd_count: int) -> float:
    """Charge 1 valley at n and the other OOE starts at n^{9/8}.

    This is the first coupling increment: the next valley after a
    cheap OOE cannot sit at n+2. Remaining OE starts stay at
    oe_start_min. Internals of the n-OOE sit at T(n); other
    internals sit at T of the 9/8 height. Evens stay at n^2.
    """

    even_count = length - odd_count
    oo_count, oe_count = run_type_counts(odd_count, even_count)
    high = nine_eighths_height(n)
    image = first_odd_image(n)
    image_high = first_odd_image(high) if high % 2 == 1 else high
    valley = inv_log(n)
    if oo_count > 1:
        valley += (oo_count - 1) * inv_log(high)
    climb = inv_log(image) if oo_count >= 1 else 0.0
    if oo_count > 1:
        climb += (oo_count - 1) * inv_log(max(image_high, high))
    high_oe = oe_count * inv_log(oe_start_min(n))
    even_term = even_count * inv_log(n * n)
    return valley + climb + high_oe + even_term


def nine_eighths_rhs(
    n: int,
    length: int,
    odd_count: int,
    *,
    const: float = EPS_CONST,
) -> float:
    return const * nine_eighths_sum_terms(n, length, odd_count)


def greedy_walk(
    odd_budget: int,
    even_budget: int,
    *,
    k_max: int = 12,
    ell_max: int = 8,
) -> dict[str, Any]:
    """Lowest-landing circuits from exponent 1 until the budget dies.

    k_max=12 covers the length-19 convergent (k=10, ell=6) and the
    shortest descent (5,3). The length-84 reset is a separate row.
    """

    exp3, exp2 = 0, 0
    odds = odd_budget
    evens = even_budget
    steps: list[dict[str, Any]] = []
    valley_logs: list[float] = []
    while odds >= 1 and evens >= 1:
        choice = lowest_circuit(
            exp3, exp2, odds, evens, k_max=k_max, ell_max=ell_max
        )
        if choice is None:
            break
        odd_run, even_run = choice
        valley_logs.append(exponent_log2(exp3, exp2))
        exp3, exp2 = land(exp3, exp2, odd_run, even_run)
        odds -= odd_run
        evens -= even_run
        steps.append(
            {
                "k": odd_run,
                "ell": even_run,
                "land_log2": exponent_log2(exp3, exp2),
            }
        )
        if len(steps) > odd_budget + even_budget:
            break
    return {
        "steps": len(steps),
        "odd_left": odds,
        "even_left": evens,
        "final_log2": exponent_log2(exp3, exp2),
        "valley_logs": valley_logs,
        "first_circuits": steps[:8],
        "last_circuits": steps[-4:] if len(steps) > 8 else steps,
    }


def walk_valley_sum(n: int, valley_logs: list[float]) -> float:
    """Σ 1/(n^α α ln n) plus one internal at (3/2)α and one even at 2α
    for each valley, using the envelope heights. Internals/evens are
    charged at the peak/image scales implied by a length-2-or-more run
    when α is the valley exponent. This is an upper bound only if each
    recorded valley is an OOE-scale start; extra climb letters sit
    higher and shrink the sum.
    """

    if n < 3 or not valley_logs:
        return 0.0
    log_n = math.log(n)
    total = 0.0
    for log2_alpha in valley_logs:
        alpha = 2.0**log2_alpha
        height = math.exp(alpha * log_n)
        if height < 3:
            continue
        total += 1.0 / (height * alpha * log_n)
    return total


def coupling_row(
    length: int,
    *,
    floor: int = PUBLISHED_FLOOR,
    const: float = EPS_CONST,
) -> dict[str, Any]:
    odd_count, theta = o_min_and_theta(length)
    even_count = length - odd_count
    start = max(floor + 1, MIN_STATE)
    oo_count, _oe_count = run_type_counts(odd_count, even_count)
    packed = budget_rhs(start, length, odd_count, const=const)
    nine = nine_eighths_rhs(start, length, odd_count, const=const)
    n_sep = n_max_separated(odd_count, even_count, 5, 3)
    walk = greedy_walk(odd_count, even_count)
    walk_sum = const * (
        walk_valley_sum(start, walk["valley_logs"])
        + even_count * inv_log(start * start)
        + max(odd_count - len(walk["valley_logs"]), 0)
        * inv_log(max(first_odd_image(start), 3))
    )
    return {
        "L": length,
        "o": odd_count,
        "e": even_count,
        "theta": theta,
        "n": start,
        "n_cheap_packing": oo_count,
        "n_separated_53": n_sep,
        "n_cheap_strictly_below_packing": n_sep < oo_count,
        "packed_rhs": packed,
        "nine_eighths_rhs": nine,
        "greedy_steps": walk["steps"],
        "greedy_rhs": walk_sum,
        "nine_excludes": theta * (1.0 - PARITY_REL_GUARD)
        > nine * (1.0 + PARITY_REL_GUARD) + PARITY_ABS_PAD,
        "greedy_excludes": theta * (1.0 - PARITY_REL_GUARD)
        > walk_sum * (1.0 + PARITY_REL_GUARD) + PARITY_ABS_PAD,
        "packed_excludes": theta * (1.0 - PARITY_REL_GUARD)
        > packed * (1.0 + PARITY_REL_GUARD) + PARITY_ABS_PAD,
    }


def coupling_scan(
    *,
    floor: int = PUBLISHED_FLOOR,
    const: float = EPS_CONST,
) -> dict[str, Any]:
    start = max(floor + 1, MIN_STATE)
    descent = shortest_descent_from_nine_eighths()
    rows = [
        coupling_row(length, floor=floor, const=const)
        for length in survivor_lengths(floor=floor)
    ]
    below = [row["L"] for row in rows if row["n_cheap_strictly_below_packing"]]
    nine_kills = [row["L"] for row in rows if row["nine_excludes"]]
    greedy_kills = [row["L"] for row in rows if row["greedy_excludes"]]
    spotlights = {
        str(length): next(row for row in rows if row["L"] == length)
        for length in SPOTLIGHT
        if any(row["L"] == length for row in rows)
    }
    walk53 = greedy_walk(16266, 9515, k_max=53, ell_max=32)
    start_n = max(floor + 1, MIN_STATE)
    greedy53_rhs = EPS_CONST * (
        walk_valley_sum(start_n, walk53["valley_logs"])
        + 9515 * inv_log(start_n * start_n)
        + max(16266 - len(walk53["valley_logs"]), 0)
        * inv_log(max(first_odd_image(start_n), 3))
    )
    theta_star = o_min_and_theta(25781)[1]
    lowest_from_one = lowest_circuit(0, 0, 16266, 9515, k_max=53, ell_max=32)
    landing_samples = []
    seed = start
    while len(landing_samples) < 5 and seed < start + 40000:
        if seed % 2 == 1:
            first = first_odd_image(seed)
            if first % 2 == 1:
                landing_samples.append(
                    {
                        "v": seed,
                        "landing": ooe_landing_lower(seed),
                        "beats_n_plus_two": ooe_landing_beats_n_plus_two(seed),
                    }
                )
        seed += 2
    for seed in (37, 365, 1999):
        first = first_odd_image(seed)
        if first % 2 == 1:
            landing_samples.append(
                {
                    "v": seed,
                    "landing": ooe_landing_lower(seed),
                    "beats_n_plus_two": ooe_landing_beats_n_plus_two(seed),
                }
            )
    return {
        "bound": "valley_coupling",
        "floor": floor,
        "n": start,
        "shortest_descent": descent["shortest"],
        "shortest_is_five_three": descent["is_five_three"],
        "exact_reset_to_one": exact_reset_to_one_exists(),
        "ooe_landing_samples": landing_samples,
        "ooe_landings_beat_n_plus_two": all(
            row["beats_n_plus_two"] for row in landing_samples
        ),
        "survivor_count": len(rows),
        "sha256_survivors": sha256_int_list([row["L"] for row in rows]),
        "n_cheap_below_count": len(below),
        "n_cheap_below": below[:8],
        "all_n_cheap_below_packing": len(below) == len(rows),
        "killed_by_nine_eighths": nine_kills,
        "killed_by_greedy": greedy_kills,
        "nine_kills_25781": 25781 in nine_kills,
        "greedy_kills_25781": 25781 in greedy_kills,
        "certified_leftover_kills": [],
        "diagnostic_only": True,
        "spotlights": spotlights,
        "lowest_from_one": {
            "k": lowest_from_one[0] if lowest_from_one else None,
            "ell": lowest_from_one[1] if lowest_from_one else None,
        },
        "greedy53_25781": {
            "steps": walk53["steps"],
            "rhs": greedy53_rhs,
            "theta": theta_star,
            "excludes": theta_star * (1.0 - PARITY_REL_GUARD)
            > greedy53_rhs * (1.0 + PARITY_REL_GUARD) + PARITY_ABS_PAD,
            "valleys_below_nine_eighths": sum(
                1 for log_val in walk53["valley_logs"] if log_val < 0.169925
            ),
        },
        "rows": rows,
        "halt_theorem": False,
        "no_cycle_all_lengths": False,
    }


def write_coupling_artifacts(
    payload: dict[str, Any] | None = None,
    *,
    floor: int = PUBLISHED_FLOOR,
) -> dict[str, Any]:
    data = payload if payload is not None else coupling_scan(floor=floor)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / "valley_coupling" / "summary.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return data


if __name__ == "__main__":
    write_coupling_artifacts()
