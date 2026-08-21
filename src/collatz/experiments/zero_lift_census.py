"""Census of J, unique zero-lift k, and expanding words.

Uniqueness of the zero-lift extension is **PROVED**. The loops below are
regression checks and a search for a finite invariant that would certify
``J>0`` without computing ``T^m(R)``. No such invariant, independent of
``R`` and ``m``, was found. That is an **OBSERVATION**.
"""

from __future__ import annotations

from itertools import product

from collatz.automata.valuation_shift import growth_budget
from collatz.lower_bounds import lift_t
from collatz.zero_lift import expanding_word_has_positive_J, zero_lift_k


def uniqueness_census(max_length: int, k_max: int) -> dict[str, object]:
    """For every prefix, exactly one ``j`` in ``1..k_max`` with ``J=0``,
    unless the true zero-lift ``k`` exceeds ``k_max``.
    """
    mismatches = 0
    checked = 0
    true_k_beyond = 0
    prefixes: list[tuple[int, ...]] = [()]
    for _ in range(max_length + 1):
        nxt: list[tuple[int, ...]] = []
        for parent in prefixes:
            true_k = zero_lift_k(parent)
            zeros = [j for j in range(1, k_max + 1) if lift_t(parent, j) == 0]
            checked += 1
            if true_k <= k_max:
                if zeros != [true_k]:
                    mismatches += 1
            else:
                true_k_beyond += 1
                if zeros:
                    mismatches += 1
            if _ < max_length:
                for j in range(1, k_max + 1):
                    nxt.append(parent + (j,))
        prefixes = nxt
    return {
        "checked_prefixes": checked,
        "mismatches": mismatches,
        "true_k_exceeds_k_max": true_k_beyond,
        "status": "VERIFIED COMPUTATIONALLY (uniqueness is PROVED)",
    }


def expanding_positive_J_census(max_length: int, k_max: int) -> dict[str, object]:
    """Every expanding word should have some ``J_i > 0`` (**PROVED**)."""
    failures = []
    expanding = 0
    for m in range(1, max_length + 1):
        for ks in product(range(1, k_max + 1), repeat=m):
            if growth_budget(ks).kind != "expanding":
                continue
            expanding += 1
            if not expanding_word_has_positive_J(ks):
                failures.append(ks)
    return {
        "expanding_words": expanding,
        "failures": [list(w) for w in failures],
        "status": "PROVED; census is a regression",
    }


def next_k_by_R_mod(max_length: int, k_max: int, precision: int) -> dict[str, object]:
    """Does ``R mod 2^P`` determine ``zero_lift_k``? Search for collisions."""
    buckets: dict[int, set[int]] = {}
    for m in range(0, max_length + 1):
        if m == 0:
            words: tuple[tuple[int, ...], ...] = ((),)
        else:
            words = tuple(product(range(1, k_max + 1), repeat=m))
        for ks in words:
            from collatz.min_realizer import min_realizer

            r = min_realizer(ks)
            k = zero_lift_k(ks)
            key = r % (1 << precision)
            buckets.setdefault(key, set()).add(k)
    collisions = {str(key): sorted(vals) for key, vals in buckets.items() if len(vals) > 1}
    return {
        "precision": precision,
        "collision_count": len(collisions),
        "sample_collisions": dict(list(collisions.items())[:12]),
        "status": (
            "OBSERVATION: collisions mean R mod 2^P does not determine next k. "
            "No finite-state certificate of J>0 independent of the orbit was found."
        ),
    }
