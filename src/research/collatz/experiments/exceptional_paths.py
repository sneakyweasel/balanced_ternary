"""Search among expansionary valuation prefixes (exceptional-itinerary pipeline).

An itinerary is *expanding* when ``2^K < 3^m`` (exact integer comparison).
``B_m`` here is the set of length-``m`` words with ``K = m`` (all ones) or
more generally ``2^K < 3^m``. The float ``epsilon`` only *selects* a
stricter integer cut ``K <= floor((log2(3)-eps)*m)`` and is labelled
OBSERVATION as a selector, not as a Lyapunov margin.

This does not claim that expansionary prefixes are unrealisable.
"""

from __future__ import annotations

from math import floor, log2

from research.collatz.automata.valuation_shift import growth_budget
from research.collatz.experiments.fixed_budget import compositions_of
from research.collatz.min_realizer import itinerary_signature
from research.collatz.zero_lift import lift_digits


LOG2_3 = log2(3)


def is_expanding(ks: tuple[int, ...]) -> bool:
    return growth_budget(ks).kind == "expanding"


def k_cut(m: int, epsilon: float) -> int:
    """Largest integer K with ``K/m <= log2(3) - epsilon``."""
    if epsilon < 0:
        raise ValueError("epsilon must be >= 0")
    raw = (LOG2_3 - epsilon) * m
    return int(floor(raw))


def run_exceptional_search(
    length: int,
    k_max: int = 3,
    epsilon: float = 0.1,
) -> dict[str, object]:
    if isinstance(length, bool) or not isinstance(length, int) or length < 1:
        raise ValueError(f"length must be an integer >= 1, got {length!r}")
    if isinstance(k_max, bool) or not isinstance(k_max, int) or k_max < 1:
        raise ValueError(f"k_max must be an integer >= 1, got {k_max!r}")
    cut = k_cut(length, epsilon)
    rows = []
    for k_sum in range(length, cut + 1):
        for ks in compositions_of(k_sum, length, k_max):
            if not is_expanding(ks):
                continue
            sig = itinerary_signature(ks)
            digits = lift_digits(ks)
            rows.append(
                {
                    "ks": list(ks),
                    "K": k_sum,
                    "R": sig.R,
                    "C": sig.C,
                    "lift_digits": list(digits),
                    "zero_lift_count": sum(t == 0 for t in digits),
                    "BT(R)": sig.bt_word,
                    "length_BT": sig.features.length,
                    "weight": sig.features.weight,
                    "status": "EXACT signature; membership in B_m(eps) is a float cut (OBSERVATION selector)",
                }
            )
    rs = [row["R"] for row in rows]
    return {
        "length": length,
        "k_max": k_max,
        "epsilon": epsilon,
        "K_cut": cut,
        "count": len(rows),
        "R_min": min(rs) if rs else None,
        "R_max": max(rs) if rs else None,
        "sample": rows[:40],
        "status": "COMPUTATIONAL census of expansionary words. Not a Collatz theorem.",
    }
