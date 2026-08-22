"""Dual-code traces for periodic valuation words."""

from __future__ import annotations

from itertools import product

from research.collatz.cycle_codes import exponent_root
from research.collatz.dual_code import CollatzDualCode
from research.collatz.periodic_itineraries import periodic_candidate


def primitive_period(period: tuple[int, ...]) -> tuple[int, ...]:
    """Shortest word whose repetition equals ``period``."""
    return exponent_root(period)


def periodic_dual_trace(period: tuple[int, ...], repeats: int) -> dict[str, object]:
    if not period or any(k < 1 for k in period):
        raise ValueError("period must be a nonempty positive valuation word")
    if repeats < 1:
        raise ValueError("repeats must be >= 1")
    word = period * repeats
    dual = CollatzDualCode.from_valuations(word)
    rows = []
    for m in range(1, len(word) + 1):
        prefix = word[:m]
        code = CollatzDualCode.from_valuations(prefix)
        rows.append(
            {
                "m": m,
                "K": code.K,
                "R": code.R,
                "lift_digit": code.lift_digits[-1],
                "BT(R)": code.balanced_ternary_R,
                "two_power": 1 << code.K,
                "three_power": pow(3, m),
                "budget_comparison": code.as_dict()["budget_comparison"],
                "status": "EXACT",
            }
        )
    candidate = periodic_candidate(period)
    return {
        "period": list(period),
        "primitive_period": list(primitive_period(period)),
        "repeats": repeats,
        "rows": rows,
        "lift_digits": list(dual.lift_digits),
        "stabilized_in_sample": all(
            row["lift_digit"] == 0 for row in rows[-len(period) :]
        ),
        "periodic_candidate": candidate.as_dict(),
        "status": "EXACT finite trace; infinite classification uses the proved candidate test",
    }


def periodic_census(
    max_period: int,
    k_max: int,
    repeats: int,
    primitive_only: bool = True,
) -> dict[str, object]:
    rows = []
    for length in range(1, max_period + 1):
        for period in product(range(1, k_max + 1), repeat=length):
            if primitive_only and primitive_period(period) != period:
                continue
            trace = periodic_dual_trace(period, repeats)
            candidate = trace["periodic_candidate"]
            rows.append(
                {
                    "period": list(period),
                    "compatible": candidate["compatible"],
                    "candidate_n": candidate["n"],
                    "final_R": trace["rows"][-1]["R"],
                    "zero_lift_count": sum(
                        t == 0 for t in trace["lift_digits"]
                    ),
                    "lift_digits": trace["lift_digits"],
                    "status": "VERIFIED COMPUTATIONALLY on finite trace",
                }
            )
    return {
        "max_period": max_period,
        "k_max": k_max,
        "repeats": repeats,
        "primitive_only": primitive_only,
        "rows": rows,
        "status": "COMPUTATIONAL census; candidate compatibility per row is EXACT",
    }
