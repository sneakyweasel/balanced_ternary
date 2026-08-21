"""Finite dual-code census conditioned by the exact homogeneous budget.

This module does not infer an infinite-itinerary theorem from finite rows.
"""

from __future__ import annotations

from collatz.dual_code import CollatzDualCode
from collatz.experiments.fixed_budget import compositions_of


def largest_noncontracting_K(m: int) -> int:
    """Largest ``K`` with ``2^K <= 3^m``, using integer arithmetic only."""
    if m < 1:
        raise ValueError("m must be >= 1")
    three = pow(3, m)
    K = 0
    while (1 << (K + 1)) <= three:
        K += 1
    return K


def run_noncontracting_dual(
    length: int,
    k_max: int,
    row_limit: int | None = None,
) -> dict[str, object]:
    if length < 1 or k_max < 1:
        raise ValueError("length and k_max must be positive")
    K_cut = largest_noncontracting_K(length)
    rows = []
    truncated = False
    for K in range(length, K_cut + 1):
        for ks in compositions_of(K, length, k_max):
            if row_limit is not None and len(rows) >= row_limit:
                truncated = True
                break
            dual = CollatzDualCode.from_valuations(ks)
            rows.append(
                {
                    **dual.as_dict(),
                    "zero_lift_count": sum(t == 0 for t in dual.lift_digits),
                    "positive_lift_count": sum(t > 0 for t in dual.lift_digits),
                    "status": "EXACT finite row",
                }
            )
        if truncated:
            break
    return {
        "length": length,
        "k_max": k_max,
        "K_cut": K_cut,
        "rows": rows,
        "truncated": truncated,
        "known_local_counterexample": {
            "itinerary": [1, 2, 1, 1, 1, 1, 2, 2, 1, 2],
            "lift_digits": [1, 2, 1, 0, 0, 0, 0, 0, 0, 0],
            "R_from_depth_3": 27,
            "status": (
                "EXACT finite counterexample to claims that every expanding "
                "extension must lift; it says nothing by itself about an "
                "infinite asymptotically non-contracting itinerary"
            ),
        },
        "status": (
            "COMPUTATIONAL finite census. Infinite positive-lift frequency "
            "remains CONJECTURE."
        ),
    }
