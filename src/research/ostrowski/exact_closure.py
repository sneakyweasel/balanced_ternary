"""Backward co-reachability of a seed, versus the adder live set.

Reverse contraction of ``A^{-1}`` makes the basin of a *bounded* seed
finite. The adder's accepting slice ``{s_3=0}`` is an infinite plane, so
that argument does not bound the unread-tail live set from ``(0,0,0)``.

``C({0})`` is computed by backward least fixed point (integer preimages).
It is the basin of the origin, not the analogue of ``B_MIN``.
"""

from __future__ import annotations

import hashlib
from functools import lru_cache

from research.ostrowski.contraction_certificate import (
    APRIORI_AXIS_BOUND,
    a_priori_preimage_bound,
    q_norm_squared,
)
from research.ostrowski.live_growth import growth_table, legal_w, reachable_live
from research.ostrowski.nonpisot_search import HUB, l1
from research.ostrowski.reverse_map import integer_preimage
from research.ostrowski.spectral_residual import transition_affine
from research.ostrowski.system import nonpisot_order3
from research_engine.reachability.reverse import reverse_closure

State3 = tuple[int, int, int]

# Regression constants for the basin of (0,0,0) under the union alphabet.
# This is C({0}), not the adder live set and not an analogue of B_MIN.
BASIN_OF_ZERO_CARDINALITY = 9164
BASIN_STABILIZATION_DEPTH = 67
BASIN_EXTREMA: tuple[tuple[int, int], tuple[int, int], tuple[int, int]] = (
    (-33, 32),
    (-30, 29),
    (-11, 10),
)
BASIN_MAX_L1 = 57
BASIN_MAX_Q_NORM_SQUARED = 14460
BASIN_FINGERPRINT = "c4487dbeaab216fd340b54fada7be21d4c57a35648328d62a82f5d516366e70f"


def union_alphabet() -> tuple[int, ...]:
    sys = nonpisot_order3()
    return tuple(sorted(set(legal_w(sys, 0)) | set(legal_w(sys, 1))))


def seed_justification() -> dict[str, object]:
    """Why reverse contraction does not bound the adder live set."""
    return {
        "accepting_slice_F": "s3 == 0, an infinite plane",
        "F_finite": False,
        "honest_finite_seed": ((0, 0, 0),),
        "C_of_F_bounded_by_reverse_contraction": False,
        "C_of_zero_is_basin_of_origin": True,
        "C_of_zero_is_not_adder_live_set": True,
        "reason": (
            "Reverse contraction bounds preimages of a bounded seed. "
            "Acceptance is s3=0 with (s1,s2) free at remaining 0, so F is "
            "infinite. The adder live set is forward unread-tail reachability "
            "from (0,0,0) ending at some point of F, not co-reachability of 0."
        ),
    }


def _fingerprint(states: tuple[State3, ...]) -> str:
    blob = b";".join(f"{a},{b},{c}".encode() for a, b, c in states)
    return hashlib.sha256(blob).hexdigest()


@lru_cache(maxsize=1)
def basin_of_zero() -> dict[str, object]:
    """Least fixed point ``C({0})``: integer states that can reach the origin.

    Serialized as a deterministic sorted tuple (see
    ``canonical_basin_states``), not as a 9164-line analogue of ``B_MIN``.
    """
    alphabet = union_alphabet()

    def predecessors(state: State3) -> tuple[State3, ...]:
        found: list[State3] = []
        for w in alphabet:
            pred = integer_preimage(state, w)
            if pred is not None:
                found.append(pred)
        return tuple(found)

    result = reverse_closure(((0, 0, 0),), predecessors)
    states = result.union
    depth = result.horizon if result.horizon is not None else 0
    canonical = tuple(sorted(states))
    extrema = (
        (min(s[0] for s in states), max(s[0] for s in states)),
        (min(s[1] for s in states), max(s[1] for s in states)),
        (min(s[2] for s in states), max(s[2] for s in states)),
    )
    max_abs = (
        max(abs(s[0]) for s in states),
        max(abs(s[1]) for s in states),
        max(abs(s[2]) for s in states),
    )
    return {
        "states": states,
        "canonical": canonical,
        "fingerprint": _fingerprint(canonical),
        "cardinality": len(states),
        "stabilization_depth": depth,
        "extrema": extrema,
        "max_abs": max_abs,
        "max_l1": max(l1(s) for s in states),
        "max_q_norm_squared": max(q_norm_squared(s) for s in states),
        "hub_in_basin": HUB in states,
        "origin_in_basin": (0, 0, 0) in states,
        "sample_outside_adder_terminal": (30, 25, 0) not in states,
        "inside_apriori_box": max(max_abs) <= APRIORI_AXIS_BOUND,
        "apriori": a_priori_preimage_bound(),
    }


def canonical_basin_states() -> tuple[State3, ...]:
    """Deterministic dump of ``C({0})`` as sorted triples."""
    return basin_of_zero()["canonical"]  # type: ignore[return-value]


def check_a_every_state_can_step_toward_origin(states: frozenset[State3]) -> bool:
    """Every non-origin basin state has a legal forward image still in the basin."""
    sys = nonpisot_order3()
    alphabet = union_alphabet()
    for s in states:
        if s == (0, 0, 0):
            continue
        if not any(transition_affine(sys, s, w) in states for w in alphabet):
            return False
    return True


def check_b_no_extra_preimage(states: frozenset[State3]) -> bool:
    """No reverse image of the basin leaves the basin; hull points cannot enter."""
    alphabet = union_alphabet()
    for t in states:
        for w in alphabet:
            pred = integer_preimage(t, w)
            if pred is not None and pred not in states:
                return False
    xs = [s[0] for s in states]
    ys = [s[1] for s in states]
    zs = [s[2] for s in states]
    box = [
        (x, y, z)
        for x in range(min(xs), max(xs) + 1)
        for y in range(min(ys), max(ys) + 1)
        for z in range(min(zs), max(zs) + 1)
    ]
    sys = nonpisot_order3()
    for s in box:
        if s in states:
            continue
        for w in alphabet:
            if transition_affine(sys, s, w) in states:
                return False
    return True


# Recorded depth-growth paradox. ``R_≤N`` grows; that is not infinitude.
# ``outside_basin`` counts live-from-0 states that cannot reach the origin.
PARADOX_AT = {
    8: {"live_states": 154, "max_abs": (15, 14, 5), "outside_basin": 51},
    10: {"live_states": 310, "max_abs": (21, 18, 7), "outside_basin": 120},
    12: {"live_states": 532, "max_abs": (27, 24, 9), "outside_basin": 242},
    14: {"live_states": 867, "max_abs": (30, 31, 10), "outside_basin": 436},
    16: {"live_states": 1351, "max_abs": (36, 37, 12), "outside_basin": 700},
}


def compare_forward_to_basin(max_depth: int = 12) -> dict[str, object]:
    """``R_≤N`` versus ``C({0})``. Finite depth is not infinitude.

    ``R_≤N`` is a transient shell of expanding ``A``. Monotone growth is
    not infinitude. States of ``R`` that lie outside ``C({0})`` are
    forward images of the origin, not reverse-contraction preimages.
    """
    sys = nonpisot_order3()
    basin = basin_of_zero()["states"]
    rows = []
    for row in growth_table(sys, max_depth):
        live = reachable_live(sys, int(row["depth"]))
        states: frozenset[State3] = live["states"]  # type: ignore[assignment]
        rows.append(
            {
                **{k: row[k] for k in row},
                "in_basin": sum(1 for s in states if s in basin),
                "outside_basin": sum(1 for s in states if s not in basin),
            }
        )
    last = reachable_live(sys, max_depth)["states"]
    return {
        "table": rows,
        "R_subset_of_basin": last <= basin,
        "R_minus_basin_count": len(last - basin),
        "basin_minus_R_count": len(basin - last),
        "finite_depth_is_not_infinitude": True,
        "hub_in_both": HUB in last and HUB in basin,
        "R_exits_computed_basin_box": any(
            abs(s[i]) > max(abs(BASIN_EXTREMA[i][0]), abs(BASIN_EXTREMA[i][1]))
            for s in last
            for i in range(3)
        ),
        "R_still_inside_apriori_box": all(
            max(abs(s[0]), abs(s[1]), abs(s[2])) <= APRIORI_AXIS_BOUND for s in last
        ),
    }
